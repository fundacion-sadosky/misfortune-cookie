import os
import sqlite3
from os.path import isfile, join
from os import listdir
import datetime
import re
import socket
import struct


CREATE_SCAN_TABLE_SQLITE = """
CREATE TABLE `scan` (
    `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `ip`	text,
    `port`	int,
    `http_banner`	text,
    `ip_block_id`	INTEGER,
    FOREIGN KEY(`ip_block_id`) REFERENCES `ip_blocks`(`id`)
);
"""

CREATE_IP_BLOCKS_TABLE_SQLITE = """
CREATE TABLE `ip_blocks` (
    `id`	INTEGER PRIMARY KEY AUTOINCREMENT,
    `data`	TEXT,
    `inetnum`	TEXT,
    `country`	TEXT,
    `owner`	TEXT,
    `ownerid`	TEXT
);
 """


def dump_banner_files_to_sqlite(db_path, banners_dir):

    # Remove previous database
    if isfile(db_path):
        os.remove(db_path)
    # TODO: Remove this, or comment it, it's too dangerous, better erase it manually.

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute(CREATE_SCAN_TABLE_SQLITE)
    c.execute(CREATE_IP_BLOCKS_TABLE_SQLITE)
    conn.commit()

    batch = []
    processed = 0

    for ip_port_fn in listdir(banners_dir):
        banner_path = join(banners_dir, ip_port_fn)
        if not isfile(banner_path):
            continue

        # print(banner_path)
        with open(banner_path) as f:
            banner = f.readlines()
            banner = ''.join(banner)

        ip, port = ip_port_fn.split(':')

        batch.append((ip, port, banner))

        if len(batch) >= 10000:
            c.executemany('INSERT INTO scan (ip, port, http_banner) VALUES (?,?,?)', batch)
            conn.commit()
            processed += len(batch)
            print("Processed: {:d}".format(processed))
            batch = []

    if len(batch) > 0:
        c.executemany('INSERT INTO scan (ip, port, http_banner) VALUES (?,?,?)', batch)

    conn.commit()
    conn.close()


def insert_whois_data(db_path, whois_dir):

    whois_entries_list = []
    for whois_fn in listdir(whois_dir):

        import codecs
        # TODO: Watch for whois encoding, is LACNIC returning latin-1?
        with codecs.open(join(whois_dir, whois_fn), encoding = 'latin1') as f:

            whois_text = f.readlines()

        whois = {}
        whois['whois_fn'] = whois_fn
        whois['whois_data'] = ''.join(whois_text)

        for line in whois_text:
            if line[0] == '%' or line[0] == '#':
                continue
                # Skip comments

            m = re.search('({key}):\s*({value})'.format(key= r'.*?', value= r'.*'), line)
            if m is None:
                continue

            key = m.group(1).lower()
            if key not in whois:
                whois[key] = m.group(2)
                # Many keys are repeated (e.g., country, that also appears for the point of contact),
                # we only care about the first key (e.g., country of the resource).
                # TODO: Check if this is always true.

        whois_entries_list.append(whois)

    conn = sqlite3.connect(db_path)
    conn.text_factory = str
    # To avoid "sqlite3.ProgrammingError: You must not use 8-bit bytestrings unless you use a text_factory that can interpret 8-bit bytestrings ..."
    # TODO: Unicode for accents???
    c = conn.cursor()

    # TODO: Drop table ip_blocks? (inserting everything from zero)

    # TODO: This flow of logic presuposes that dump_banner_files_to_sqlite is called first to create all the tables.

    for whois in whois_entries_list:
        if 'inetnum' not in whois:
            print("{:s}: No inetnum!!".format(whois['whois_fn']))
            continue
            # TODO: Should I raise an excpetion?

        c.executemany('INSERT INTO ip_blocks (inetnum, country, data, owner, ownerid)'
                      'VALUES (?, ?, ?, ?, ?)',
                      [(whois['inetnum'], whois.get('country', ''), whois['whois_data'],
                        whois.get('owner', ''), whois.get('ownerid', ''))])

    conn.commit()
    conn.close()


# Based on: http://stackoverflow.com/a/819420
def ip_addr_belongs_in_network(ip, network):

    if '/' not in network:
       raise Exception("Unsupported network format: " + network)
       # For now only formats like this '200.115.80/20' (which are returned by LACNIC).
       # TODO: Can't handle ARIN ranges: 163.0.0.0 - 163.255.255.255.

    ip_int = struct.unpack('>I', socket.inet_aton(ip))[0]

    net_addr, net_mask_num_bits = network.split('/')

    net_mask_num_bits = int(net_mask_num_bits)

    while net_addr.count('.') < 3:
        net_addr += '.0'
        # Add missing zeros, if the address is written in a compact format.

    net_addr_int = struct.unpack('>I', socket.inet_aton(net_addr))[0]

    net_mask_int = (((1L << net_mask_num_bits) - 1) << (32 - net_mask_num_bits))

    return (ip_int & net_mask_int) ^ net_addr_int == 0


def match_ips_to_ip_blocks(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('SELECT id, inetnum FROM ip_blocks')
    ip_blocks = c.fetchall()

    ips_processed = 0
    c.execute('SELECT ip, id FROM scan WHERE scan.ip_block_id IS NULL')
    scan_list = c.fetchall()

    for scan in scan_list:

        matched = False

        for ip_block_idx, ip_block in enumerate(ip_blocks):

            ip_block = ip_blocks[ip_block_idx]

            if ip_addr_belongs_in_network(scan['ip'], ip_block['inetnum']):

                c.execute('UPDATE scan '
                          'SET ip_block_id = ? '
                          'WHERE id = ? '
                          'LIMIT 1', (ip_block['id'], scan['id']))

                # print("Found match: {:s} -> {:s}".format(scan['ip'], ip_block['inetnum']))
                matched = True

                # Very basic speed up: raise the ip block in the list, for a faster match next time.
                # Although very simple, turns out to be very useful in practice when processing big number of ips.
                if ip_block_idx > 0:
                    ip_blocks[ip_block_idx], ip_blocks[ip_block_idx - 1] = ip_blocks[ip_block_idx - 1], ip_blocks[ip_block_idx]

                break

        if matched is False:
            raise Exception("Can't find network address for ip: " + scan['ip'])

        ips_processed += 1
        if ips_processed % 10000 == 0:
            print("IPs processed: " + str(ips_processed))
            print(datetime.datetime.now())
            conn.commit()

    conn.commit()
    conn.close()
