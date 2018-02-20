# Broadcom Bluetooth Tools

tools to extract and dump memory from broadcom bluetooth chip.

* btdump - dump memory from broadcom bluetooth chip
* hcddump - dump memory regions from broadcom bluetooth .hcd firmware
* dumped files from raspberrypi 3B (bcm43430a1)

# btdump
```
dump internal memory of broadcom bluetooth core

usage:
sudo ./btdump <startaddress> <size>

example:
# dump 576k ROM(?) starting at address 0 of BCM43430A1 chip
# run on: raspberrypi 3 Model B running Raspbian Stretch 2017-11-29
sudo ./btdump 0 589824
sudo ./btdump 0x0 0x90000  # this works too.

on raspbian:
sudo apt update
sudo apt install bluez-hcidump
this tool should probably be run as root, as "hcitool cmd 3f" requires root
```

# hcddump
```
extract flat memory regions from broadcom .hcd firmware file

usage:
./hcddump <file.hcd>
```

# bcm43430a1 (raspberrypi 3B)

raspberrypi 3B - ROM and RAM dumps:

```bash
# dump ROM(?) region (576kbytes), run this on raspberry pi 3B:
sudo ./btdump.py 0 0x90000

# dump memory regions from .hcd firmware:
./hcddump.py BCM43430A1.hcd
```

* [mem_0x00000000.bin](bcm43430a1/mem_0x00000000.bin) - ROM (576 kilobytes)
* [ram_0x00211810.bin](bcm43430a1/ram_0x00211810.bin) - (35240 bytes) raw memory dump from .hcd firmware
* [ram_0x00210c14.bin](bcm43430a1/ram_0x00210c14.bin) - (8 bytes) raw memory dump from .hcd firmware
* [ram_0x00210bdd.bin](bcm43430a1/ram_0x00210bdd.bin) - (1 byte) raw memory dump from .hcd firmware
* [CYW43438.pdf](bcm43430a1/CYW43438.pdf) - datasheet from cypress website
* [BCM43430A1.hcd](bcm43430a1/BCM43430A1.hcd) - .hcd firmware from raspberrypi dist (contains HCI commands, not a raw memory dump)

# references

* bluetooth standard (bluetooth HCI protocol)
* [AN214847_Cypress_Vendor-Specific_Commands.pdf](AN214847_Cypress_Vendor-Specific_Commands.pdf) from cypress website
* linux source code (.hcd firmware loader)
