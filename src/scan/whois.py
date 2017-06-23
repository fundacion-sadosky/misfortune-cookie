import subprocess
import os
from os import listdir
from os.path import isfile, join
import time

from config import AR_ZONE_PATH
from config import WHOIS_TIMEOUT


def run_program(args):
    child_proc = subprocess.Popen(args,
                                  stderr=subprocess.STDOUT,
                                  stdout=subprocess.PIPE,
                                  )
    stdout_data = child_proc.communicate()[0]
    ret_code = child_proc.returncode

    return {'stdout': stdout_data, 'code': ret_code}
    # TODO: Same as the one use by code generator, move up in the hierarchy.


def generate_whois_data(whois_dir):

    # Eliminate small whois output files that are probably missed queries (with errors
    # and not with the desired information).
    file_lists = [f for f in listdir(whois_dir) if isfile(join(whois_dir, f))]
    for f in file_lists:
        file_size = os.path.getsize(join(whois_dir, f))
        if file_size < 700:
            os.remove(join(whois_dir, f))
            print("Deleting: " + f)


    with open(AR_ZONE_PATH) as f:
        # TODO: Hardcoded file from Argentina (should be more general)
        ip_list = f.read().splitlines()

    for ip_with_subnet in ip_list:
        ip_with_subnet_underscore = ip_with_subnet.replace('/', '_')

        if isfile(join(whois_dir, ip_with_subnet_underscore)):
            continue
            # Already obtained, minimize whois queries.

        ret = run_program(['whois', '-h', 'whois.lacnic.net', ip_with_subnet])

        if "rate limit" in ret['stdout']:
            raise Exception("Exceeded whois query rate!\n" + ret['stdout'])

        # TODO: Add "Too many clients. Please, try again later." error (with an extra timeout).

        with open(join(whois_dir, ip_with_subnet_underscore), 'w') as f:
            f.write(ret['stdout'])
            print("Whois obtained for: " + ip_with_subnet)

        time.sleep(WHOIS_TIMEOUT)
