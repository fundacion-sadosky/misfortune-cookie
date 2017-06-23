import os
import requests
from random import shuffle
from threading import Thread
import httplib
import sys
from Queue import Queue
from config import BANNERS_DIR


HTTP_REQUEST_TIMEOUT = 5
# Chosen arbitrarily based on previous tests.


def thread_process_queue(url_queue):
    while True:
        get_server_headers_concurrent(url_queue.get())
        url_queue.task_done()


def get_server_headers_concurrent(ip_port):
    try:
        conn = httplib.HTTPConnection(ip_port, timeout=HTTP_REQUEST_TIMEOUT)
        conn.request("GET", "/")

        res = conn.getresponse()
        # print ("{:d} {:s}".format(res.status, ip_port))
        headers = res.getheaders()

        with open(os.path.join(BANNERS_DIR, ip_port), 'w') as f:
            for h in headers:
                f.write("{:s}: {:s}\n".format(h[0], h[1]))

                # if os.path.isfile(os.path.join(BANNERS_FAIL_CONN_DIR, ip_port)):
                #     os.remove(os.path.join(BANNERS_FAIL_CONN_DIR, ip_port))
                # TODO: Takes too long to process failed connections.

    except Exception as e:
        print("{:s} -> {:s}".format(ip_port, e))

        # with open(os.path.join(BANNERS_FAIL_CONN_DIR, ip_port), 'w') as f:
        #     f.write(str(e))
        # TODO: Takes too long to process failed connections.


def http_banner_grab_concurrent(scan_txt_fn, threads_number):

    # Load all IPs (and ports) in a list
    with open(scan_txt_fn) as f:
        ip_port_list = f.read().splitlines()

    shuffle(ip_port_list)
    # Not strictly necessary, but this was run more than one time for the same list
    # (while testing) and this avoided hitting the same first 100-200 IPs over and over.
    # It doesn't seem like a bad idea to keep it always randomized tough.

    url_queue = Queue()
    for _ in range(threads_number):
        t = Thread(target= thread_process_queue, args= (url_queue,))
        t.daemon = True
        t.start()

    try:
        for ip_port in ip_port_list:

            # Skip banners obtained from previous runs.
            if os.path.isfile((os.path.join(BANNERS_DIR, ip_port))):
                continue

            url_queue.put(ip_port)

        # Wait until all URLs have been processed.
        url_queue.join()

    except KeyboardInterrupt:
        print("Premature end by KeyboardInterrupt")

    # TODO: Should threads be explicitly ended?
    return


def modify_open_files_limit(new_limit):
    # Used for high values of concurrent threads that keep many open files.
    import resource

    # the soft limit imposed by the current configuration
    # the hard limit imposed by the operating system.
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    print 'Soft limit is ', soft

    # For the following line to run, you need to execute the Python script as root.
    resource.setrlimit(resource.RLIMIT_NOFILE, (new_limit, hard))


def get_server_headers(ip, port):
    # Originally used, couldn't make it work with threads, but if serial requests
    # are accepted (which is improbable due to the high volume of IPs to process)
    # using requests is recommended over the `httplib` (used in
    # `get_server_headers_concurrent`).

    http_url = 'http://{:s}:{:d}'.format(ip, port)
    try:
        r = requests.get(http_url, timeout= HTTP_REQUEST_TIMEOUT)

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        print("Failed connection to: " + http_url)
        return False

    except Exception as e:
        print("Unexpected exception: " + str(e))
        return False

        # pprint.pprint([h for h in r.headers])
        # print(r.text)

    if 'server' in r.headers:

        print("Server: " + r.headers['server'])

        # found_servers.add(r.headers['server'])
        # TODO: Where is the "found servers" functionality?

        if "RomPager/4.07" in r.headers['server']:
            return True

    return False
