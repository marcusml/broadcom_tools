#!/usr/bin/env python2
# License: CC0 / Public domain

USAGE = """dump internal memory of broadcom bluetooth core

usage:
sudo ./btdump <start_address> <size>

example:
# dump 576k ROM(?) starting at address 0 of BCM43430A1 chip
# run on: raspberrypi 3 Model B running Raspbian Stretch 2017-11-29
sudo ./btdump 0 589824
sudo ./btdump 0x0 0x90000  # this works too.

on raspbian:
sudo apt update
sudo apt install bluez-hcidump
this tool should probably be run as root, as "hcitool cmd 3f" requires root

*** NO WARRANTIES. USE AT YOUR OWN RISK ***"""

import subprocess, binascii, traceback, time, sys

def read_block(adr, size):
    if size<1 or size>251:
        raise Exception("invalid size: " + str(size))

    # 3f = ogf, Op-code Group Field 3f == "vendor-specific"
    # 4d = ocf, Op-code Command Field 4d == "Read_RAM"
    # xx xx xx xx = 32 bit address, little endian
    # yy = length of data requested, must be <= 251
    # refs:
    # Bluetooth standard (HCI commands)
    # AN214847.pdf (cypress vendor commands)

    cmd = "hcitool cmd 3f 4d %02x %02x %02x %02x %02x" % \
        ((adr&255), ((adr>>8)&255), ((adr>>16)&255), ((adr>>24)&255), size)

    print cmd
    s = subprocess.check_output(cmd, shell=True)

    iter_lines = iter(s.splitlines())
    for line in iter_lines:
        if line.startswith("> HCI Event:"):
            break  # found the beginning of response.

    hex_resp = "".join(iter_lines).translate(None, ' \n')
    try:
        resp = binascii.unhexlify(hex_resp)
    except:
        raise Exception("junk chars in hex response:\n" + s)

    if not resp.startswith("\x01\x4d\xfc\x00"):  # header: 01 4d fc 00
        # FYI: 4th byte is the bluetooth error code (see bluetooth specs)
        raise Exception("Unexpected response header:\n" + s)

    if len(resp) != size+4:  # +4 is for header
        raise Exception("Unexpected response length, expected %d, got %d" % (size+4, len(resp)))

    return resp[4:]  # return the data part.

try:
    adr = int(sys.argv[1], base=0)
    n = int(sys.argv[2], base=0)
except:
    traceback.print_exc()
    print "\n"+USAGE
    sys.exit(1)

written = 0

TRY_HARDER = True

FN = "mem_0x%08x.bin" % adr

# TODO: verify chip vendor==broadcom before messing around with vendor commands.

with open(FN, "wb") as f:
    try:
        while written < n:
            size = min(n-written, 251)  # 251 is the maximum allowed (HCI packet format)
            data = read_block(adr, size)
            f.write(data)
            written = written + size
            adr = adr + size
    except:
        traceback.print_exc()

        if TRY_HARDER:
            print "Got exception, retrying 1 less byte at a time..."
            print "WARNING chip sometimes gets stuck here. Use ctrl-c"
            size = size - 1
            while size > 0:
                try:
                    data = read_block(adr, size)
                except:
                    size = size - 1
                    continue
                f.write(data)
                written = written + size
                adr = adr + size
                break

print "tried to read %d bytes" % (n,)
print "actually read %d bytes" % (written,)
print "DONE."
