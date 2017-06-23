import os
from lxml import etree


def xml_to_txt(xml_fn, txt_fn):
    # Convert list of xml open ports to text: "ip:port"
    # Masscan has a "list" output format that does something similar, but I preferred
    # to keep the original raw xml with time information.

    doc = etree.parse(xml_fn)
    # A partial scan (imcomplete xml format) has to be closed with a '</nmaprun>' and '\n'

    for elem in doc.iter("nmaprun"):
        nmaprun = elem
        break
        # TODO: Better way to get the 1st (and only) object

    with open(txt_fn, 'w') as txt_out:

        for host in nmaprun.iterchildren():

            children = host.getchildren()

            if len(children) < 2:
                continue
                # Missing either address or port.
                # TODO: In which case is this possible?

            ip = children[0].attrib['addr']
            port = int(children[1].getchildren()[0].attrib['portid'])

            txt_out.write("{:s}:{:d}\n".format(ip, port))
            # print("{:s}:{:d}\n".format(ip, port))

            # TODO: It makes the convertion but fails at the end when it doesn't recognize the 'runstats' object.
