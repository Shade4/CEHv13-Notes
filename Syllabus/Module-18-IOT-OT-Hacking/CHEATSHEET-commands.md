# 🔧 CHEATSHEET — Every Command in This Repo

Copy/paste-ready reference for every command used across the IoT and OT hacking topic files. Grouped by tool. See the linked topic file for full context on each command.

> ⚠️ Only run these against systems you own or have written authorization to test.

---

## Reconnaissance / OSINT

### Shodan (`shodan.io`) — [05](05-iot-hacking-methodology-and-tools.md) / [10](10-ot-hacking-methodology-and-tools.md)

```
webcam country:"US"                 # webcams in the US
webcam city:"Paris"                 # webcams in Paris
webcamp geo:-50.81,201.80           # webcams near a lat/long
port:502                            # devices with Modbus (502) open
"Schneider Electric"                # devices banner-matching a PLC vendor
SCADA Country:"US"                  # SCADA systems in the US
```

### Nmap — general host discovery — [05](05-iot-hacking-methodology-and-tools.md)

```bash
nmap -p 80,81,8080,9081 <Target IP address range>
```

### Nmap — IoT device vulnerability scanning — [05](05-iot-hacking-methodology-and-tools.md)

```bash
nmap -n -Pn -sO -pT:0-65535 -v -A -oX <Name><IP>
nmap -n -Pn -sSU -pT:0-65535,U:0-65535 -v -A -oX <Name><IP>
nmap -6 -n -Pn -sSU -pT:0-65535,U:0-65535 -v -A -oX <Name><IP>
```

### Nmap — ICS/SCADA scanning — [10](10-ot-hacking-methodology-and-tools.md)

```bash
# Open ports/services across every well-known ICS/SCADA port
nmap -Pn -sT --scan-delay 1s --max-parallelism 1 -p 80,102,443,502,530,593,789,1089-1091,1911,1962,2222,2404,4000,4840,4843,4911,9600,19999,20000,20547,34962-34964,34980,44818,46823,46824,55000-55003 <Target IP>

nmap -Pn -sT -p 46824 <Target IP>                              # HMI systems (Sielco Sistemi Winlog)
nmap -Pn -sT -p 102 --script=s7-info <Target IP>                # Siemens SIMATIC S7 PLCs
nmap -Pn -sT -p 502 --script modbus-discover <Target IP>        # Modbus
nmap -sT -p 502 --script modbus-discover --script-args='modbus-discover.aggressive=true' <Target IP>
nmap -Pn -sU -p 47808 --script bacnet-info <Target IP>           # BACnet
nmap -sU -p 44818 --script enip-info <Target IP>                 # EtherNet/IP
nmap -Pn -sT -p 1911,4911 --script fox-info <Target IP>          # Niagara Fox
nmap -Pn -sT -p 20547 --script proconos-info <Target IP>         # ProConOS
nmap -Pn -sT -p 9600 --script omron-info <Target IP>              # Omron PLC (TCP)
nmap -sU -p 9600 --script omron-info <Target IP>                  # Omron PLC (UDP)
nmap -Pn -sT -p 1962 --script pcworx-info <Target IP>             # PCWorx
```

### IoTSeeker — [05](05-iot-hacking-methodology-and-tools.md)

```bash
perl iotScanner.pl <IP address/range of IP's>
```

### Genzai — [05](05-iot-hacking-methodology-and-tools.md)

```bash
./genzai <target_host> -save scan.json
```

### Sniffing recon (aircrack-ng suite) — [05](05-iot-hacking-methodology-and-tools.md)

```bash
ifconfig
airmon-ng start wlan0
airodump-ng start wlan0mon
```

### Cascoda Packet Sniffer (802.15.4 / Zigbee) — [05](05-iot-hacking-methodology-and-tools.md)

```bash
sniffer -w <channel_number>
```

---

## RF / SDR Attacks

### RFCrack — [05](05-iot-hacking-methodology-and-tools.md)

```bash
python RFCrack.py -i                                                       # live replay
python RFCrack.py -r -M MOD_2FSK -F 314350000                              # rolling-code capture
python RFCrack.py -r -M MOD_2FSK -U 100 -L -10 -F 314350000                # adjust RSSI range
python RFCrack.py -j -F 314000000                                          # jam a frequency
python RFCrack.py -k                                                       # scan common frequencies
python RFCrack.py -k -f 433000000 314000000 390000000                      # scan a custom list
python RFCrack.py -b -v -F 315000000                                       # incremental scan, verbose
python RFCrack.py -u ./captures/test.cap -F 315000000 -M MOD_ASK_OOK       # replay saved capture
```

### HackRF One — [05](05-iot-hacking-methodology-and-tools.md)

```bash
hackrf_transfer -r connector.raw -f [device frequency]      # record
hackrf_transfer -t connector.raw -f [device frequency]      # replay
```

### Gqrx — build + run — [05](05-iot-hacking-methodology-and-tools.md)

```bash
git clone https://github.com/gqrx-sdr/gqrx gqrx.git
cd gqrx
mkdir build
cd build
cmake ..
make
gqrx
```

---

## Hardware / Bus Hacking

### EXPLIoT — Bus Auditor (UART / JTAG / I2C) — [05](05-iot-hacking-methodology-and-tools.md)

```bash
run busauditor.generic.uartscan -v 3.3 -p /dev/ttyACM0 -s 0 -e 1
run busauditor.generic.jtagscan -v 3.3 -p /dev/ttyACM0 -s 0 -e 10
run busauditor.generic.i2cscan  -v 3.3 -p /dev/ttyACM0 -s 0 -e 10
```

### NAND Glitching — [05](05-iot-hacking-methodology-and-tools.md)

```bash
minicom -D /dev/ttyUSB0 -w -C D-link_startup.txt
printenv
setenv bootargs 'noinitrd console=ttyAM0,115200 rootfstype=ubifs ubi.mtd=5 root=ubi0:rootfs rw qgmi.badupdater'
nand read $(loadaddr) app-kernel 0x00400000 && bootm $(loadaddr)
```

### CamOver — [05](05-iot-hacking-methodology-and-tools.md)

```bash
camover -t <Camera IP Address>
camover -t <Router IP Address>
camover -t --shodan <Shodan API Key>
```

---

## Firmware Analysis

### Extraction / Static Analysis — [05](05-iot-hacking-methodology-and-tools.md)

```bash
file firmware.bin
strings -n 10 firmware.bin > strings.out
less strings.out
binwalk -e firmware.bin
hexdump -C -n 512 firmware.bin > hexdump.out
cat hexdump.out
dd if=firmware.bin bs=1 skip=922440 count=2522310 of=myfs.bin
sudo mount -o loop myfs.bin rootfs
grep -rnw '/path/to/rootfs/' -e 'password'
find . -iname '*.conf' -o -iname '*.cfg' -o -iname '*.pem' -o -iname '*.key'
```

### Dynamic Analysis — QEMU user-mode emulation — [05](05-iot-hacking-methodology-and-tools.md)

```bash
file some_binary
readelf -h some_binary

qemu-mipsel -L <sysroot_prefix> <binary>
qemu-arm    -L <sysroot_prefix> <binary>
qemu-<arch> -L <sysroot_prefix> <binary>

cp $(which qemu-arm-static) /path/to/extracted/rootfs/usr/bin/
chroot /path/to/extracted/rootfs /bin/sh
```

---

## Protocol Fuzzing

### Fuzzowski — [10](10-ot-hacking-methodology-and-tools.md)

```bash
python -m fuzzowski 127.0.0.1 47808 -p udp -f bacnet -rt 0.5 -m BACnetMon      # BACnet
python -m fuzzowski 127.0.0.1 502 -p tcp -f modbus -rt 1 -m modbusMon          # Modbus
python -m fuzzowski printer1 631 -f ipp -r get_printer_attribs --restart smartplug  # IPP
```

---

## Modbus / PLC Exploitation

### Metasploit — Modbus scanning — [10](10-ot-hacking-methodology-and-tools.md)

```
use auxiliary/scanner/scada/modbus_findunitid
set RHOSTS <Target Network/IP>
run
```

### Metasploit — Modbus read/write — [10](10-ot-hacking-methodology-and-tools.md)

```
use auxiliary/scanner/scada/modbusclient
set RHOSTS 192.168.1.104
set ACTION READ_REGISTERS
set REGISTER_START_ADDRESS 0
set NUMBER_OF_REGISTERS 5
run

set ACTION WRITE_REGISTERS
set DATA_TO_WRITE 55,66,77
run

set ACTION WRITE_COILS
set DATA_COILS 1,0,1,0
run
```

### modbus-cli — full walkthrough — [10](10-ot-hacking-methodology-and-tools.md)

```bash
gem install modbus-cli

# Read registers
modbus read <Target IP> %MW100 10
modbus read <Target IP> 400101 10

# Write registers
modbus write <Target IP> %MW100 2 2 2 2 2 2 2 2 2 2
modbus write <Target IP> 400101 2 2 2 2 2 2 2 2 2 2

# Read coils
modbus read <Target IP> 101 10
modbus read <Target IP> %M100 10

# Write coils
modbus write <Target IP> 101 1 1 1 1 1 1 1 1 1 1
modbus write <Target IP> %M100 1 1 1 1 1 1 1 1 1 1

# Capture output to file
modbus read --output SCADAregisters.txt <Target IP> 400101 200
modbus read --output SCADAcoils.txt <IP> 101 100
```

---

**See also:** [CHEATSHEET-tools-and-protocols.md](CHEATSHEET-tools-and-protocols.md) for the tool/port/protocol lookup tables.
