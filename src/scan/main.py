import os

from config import SCAN_DIR, BANNERS_DIR, SCAN_DB_PATH, WHOIS_DIR
from utils import xml_to_txt
from banner_grabber import http_banner_grab_concurrent
from db_dump import dump_banner_files_to_sqlite, insert_whois_data, match_ips_to_ip_blocks
from whois import generate_whois_data

if __name__ == "__main__":
    pass

    # xml_to_txt(os.path.join(SCAN_DIR, 'scan.xml'), os.path.join(SCAN_DIR, 'scan.txt'))
    #
    # http_banner_grab_concurrent(os.path.join(SCAN_DIR, 'scan.txt'), threads_number= 300)
    # # For a higher threads number, modify_open_files_limit should be used to
    # # increase (at least in Ubuntu) the number of open files (that are open by the concurrent
    # # thread).
    #
    # dump_banner_files_to_sqlite(SCAN_DB_PATH, BANNERS_DIR)
    #
    # generate_whois_data(WHOIS_DIR)
    # insert_whois_data(SCAN_DB_PATH, WHOIS_DIR)
    #
    # match_ips_to_ip_blocks(SCAN_DB_PATH)
