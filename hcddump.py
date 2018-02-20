#!/usr/bin/env python2
# License: CC0 / Public domain.

USAGE = """extract flat memory regions from broadcom .hcd firmware file

usage:
./hcddump <file.hcd>"""

import sys, traceback

try:
    HCD_FN = sys.argv[1]
except:
    traceback.print_exc()
    print "\n"+USAGE
    sys.exit(1)

with open(HCD_FN, "rb") as f:
    hcd = f.read()

# .hcd file holds a sequence of HCI commands to be sent to the bluetooth chip.
# instead of sending the commands to the actual chip, we parse the commands
# one by one, and collect the data into memory regions.

regions = {}  # memory regions, regions[start_adr] = data

i = 0
while i < len(hcd):
    cmd0 = ord(hcd[i])
    cmd1 = ord(hcd[i+1])
    size = ord(hcd[i+2])
    data = hcd[i+3:i+3+size]

    if cmd0==0x4c and cmd1==0xfc:  # Write_RAM
        cmd_adr = ord(data[0]) | (ord(data[1])<<8) | (ord(data[2])<<16) | (ord(data[3])<<24)
        found_region_to_append = False

        for mem_adr, mem_data in regions.iteritems():
            if cmd_adr == mem_adr + len(mem_data):
                found_region_to_append = True
                regions[mem_adr] = mem_data + data[4:]
                break

        if not found_region_to_append:
            #print "creating new memory region:", cmd_adr
            regions[cmd_adr] = data[4:]

    elif cmd0==0x4e and cmd1==0xfc:  # Launch_RAM
        cmd_adr = ord(data[0]) | (ord(data[1])<<8) | (ord(data[2])<<16) | (ord(data[3])<<24)
        note = "(reboot mode flag, not a real address)" if cmd_adr == 0xffffffff else ""
        print "INFO: Found Launch_RAM command, adr=0x%08x %s" % (cmd_adr, note)

    else:
        print "ERROR: Found unknown command: %02x %02x" % (cmd0, cmd1)

    i = i + 3 + size

if i != len(hcd):
    raise Exception("Unexpected end of file")

print "Dumping memory regions:"
for mem_adr, mem_data in regions.iteritems():
    FN = "ram_0x%08x.bin" % mem_adr
    print "file:", FN, "length:", len(mem_data)
    with open(FN, "wb") as f:
        f.write(mem_data)

print "DONE."
