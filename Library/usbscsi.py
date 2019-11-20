#!/usr/bin/env python3
import argparse
from Library.usblib import *

def main():
    info='MassStorageBackdoor (c) B.Kerler 2019.'
    parser = argparse.ArgumentParser(description=info)
    print("\n"+info+"\n\n")
    parser.add_argument('-vid',metavar="<vid>",help='[Option] Specify vid, default=0x2e04)', default="0x2e04")
    parser.add_argument('-pid',metavar="<pid>", help='[Option] Specify pid, default=0xc025)', default="0xc025")
    parser.add_argument('-interface', metavar="<pid>", help='[Option] Specify interface number)', default="")
    parser.add_argument('-nokia', help='[Option] Enable Nokia adb backdoor', action='store_true')

    args = parser.parse_args()
    if args.vid!="":
        vid=int(args.vid,16)
    if args.pid!="":
        pid=int(args.pid,16)
    if args.interface!="":
        interface=int(args.interface,16)
    else:
        interface=-1

    usbscsi = scsi(vid, pid, interface)
    if (usbscsi.connect()):
        if args.nokia:
            usbscsi.send_fih_adbenable()
            usbscsi.send_fih_root()
        else:
            print("A command is required. Use -h to see options.")
            exit(0)
        usbscsi.close()

if __name__ == '__main__':
    main()
