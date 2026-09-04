# 05 — IoT Hacking Methodology and Tools

> Learning Objective 2: *Explain IoT Hacking Methodology.*

## Table of Contents

- [The 5-Phase IoT Hacking Methodology](#the-5-phase-iot-hacking-methodology)
- [Phase 1 — Information Gathering](#phase-1--information-gathering)
- [Phase 2 — Vulnerability Scanning](#phase-2--vulnerability-scanning)
- [Phase 3 — Launch Attacks](#phase-3--launch-attacks)
- [Phase 4 — Gain Remote Access](#phase-4--gain-remote-access)
- [Phase 5 — Maintain Access](#phase-5--maintain-access)
- [IoT Hacking Tools Roundup](#iot-hacking-tools-roundup)

---

## The 5-Phase IoT Hacking Methodology

An IoT compromise, in a formal pentest or in the wild, follows the same five phases every time:

```
1. Information Gathering  →  2. Vulnerability Scanning  →  3. Launch Attacks
                                                                    │
                    5. Maintain Access  ←──  4. Gain Remote Access ◄┘
```

The stakes of a successful IoT compromise are high: once an attacker controls enough devices/botnets, they can spy on victims through hijacked cameras, commit credit-card fraud from a compromised smart-home hub, break into a victim's home network, or add the device to an army of DDoS bots. A single compromised device is rarely the end goal — it's a foothold.

---

## Phase 1 — Information Gathering

The goal is to fingerprint exactly what's on the target network: IP addresses, hardware/manufacturer, protocols in use (Zigbee, BLE, 5G, IPv6/6LoWPAN), open ports, device type, and geolocation.

### Shodan

**Source:** [shodan.io](https://www.shodan.io)

Shodan is a search engine that continuously scans and indexes internet-connected devices — routers, webcams, industrial sensors, and more — making it the single most useful IoT recon tool available. Useful filters:

```
webcam country:"US"                 # webcams present in the United States
webcam city:"Paris"                 # webcams present in Paris
webcamp geo:-50.81,201.80           # results near a specific lat/long
```

Additional filters worth knowing: `net:` (search by IP/CIDR), `os:` (filter by OS), `port:` (filter by open port), `before`/`after:` (limit to a time window).

### Censys

**Source:** [censys.io](https://censys.io)

A public search engine and data-processing pipeline built for ongoing internet-wide research. Censys continuously scans public IP space and indexes open ports/services/certificates, letting an attacker discover the network attack surface of a target device or organization in seconds.

### FOFA

**Source:** [en.fofa.info](https://en.fofa.info)

A cyberspace-mapping platform, functionally similar to Shodan/Censys, that lets an attacker survey global internet assets, profile risks by open port/service, and gather broad OSINT on a target.

### FCC ID Search

**Source:** [fcc.gov](https://www.fcc.gov)

Every wireless device sold in the US carries an **FCC ID** on its regulatory label (typically two parts — a 3-character grantee code and a product code). Searching that ID on the FCC's public database (`https://www.fccid.io` / `https://apps.fcc.gov/oetcf/eas/reports/GenericSearch.cfm`) discloses the device's internal photos, RF test reports, user/service manuals, and the exact frequencies it operates on — extremely useful reconnaissance before ever touching the physical device.

**Steps:**
1. Physically inspect the device for its FCC ID label.
2. Enter the grantee code and product code into the FCC ID search form.
3. Review the returned summary — internal/external photos, test reports, operating frequency table.

### Information Gathering through Sniffing

Many IoT devices (especially IP cameras) ship an insecure HTTP configuration interface with factory-default credentials. Basic recon workflow:

```bash
# Find IoT devices listening on common camera/admin HTTP ports across a range
nmap -p 80,81,8080,9081 <Target IP address range>

# Identify your own wireless card interface
ifconfig

# Put the wireless card into monitor mode
airmon-ng start wlan0

# Start capturing frames in monitor mode
airodump-ng start wlan0mon
```

Once traffic is captured, open it in **Wireshark** to look for cleartext HTTP credentials, WEP/WPA handshakes, or unencrypted device-to-cloud traffic.

### Sniffing IEEE 802.15.4 (Zigbee/Thread/6LoWPAN) with Cascoda Packet Sniffer

**Source:** [cascoda.com](https://www.cascoda.com)

1. Download and run Cascoda's Windows sniffer tool, then set Wireshark to capture from it.
2. Connect the Cascoda Packet Sniffer dongle to the machine.
3. Start capturing on a specific channel:
   ```
   sniffer -w <channel_number>
   ```
4. Wireshark begins capturing all traffic on that channel, which can be filtered like any other capture.

### Additional Sniffing Tools

| Tool | Source |
|---|---|
| **Suphacap** (hardware Z-Wave sniffer, supports Fibaro/Homeseer/Trident/Z-Way/SmartThings/Vera) | [suphammer.net](https://www.suphammer.net) |
| **IoT Inspector 2** | [github.com](https://github.com) |
| **ZBOSS Sniffer** | [dsr-iot.com](https://dsr-iot.com) |
| **tcpdump** | [tcpdump.org](https://www.tcpdump.org) |
| **Ubiqua Protocol Analyser** | [ubilogix.com](https://www.ubilogix.com) |
| **Perytons Protocol Analyzers** | [perytons.com](https://www.perytons.com) |

---

## Phase 2 — Vulnerability Scanning

Once devices and services are identified, the next step is finding exploitable weaknesses — default creds, unpatched CVEs, weak configuration.

### IoTSeeker

**Source:** [github.com](https://github.com)

A tool purpose-built to check discovered devices for **default credentials**:

```bash
perl iotScanner.pl <IP address/range of IP's>
```

Output flags each host as either "default password" or "changed password", making it trivial to triage a large IP range at once.

### Genzai

**Source:** [github.com](https://github.com)

An IoT security toolkit that detects IoT dashboards on a network and flags default credentials and known vulnerabilities based on paths, versions, and HTTP fingerprints:

```bash
./genzai <target_host> -save scan.json
```

### Nmap for IoT Vulnerability Scanning

```bash
# Full TCP + UDP port/service/OS scan of an IoT device, saved as XML
nmap -n -Pn -sO -pT:0-65535 -v -A -oX <Name><IP>

# Same, explicitly hitting both TCP and UDP scan modes
nmap -n -Pn -sSU -pT:0-65535,U:0-65535 -v -A -oX <Name><IP>

# IPv6 variant, to check the device's IPv6 stack capability
nmap -6 -n -Pn -sSU -pT:0-65535,U:0-65535 -v -A -oX <Name><IP>
```

### beSTORM

**Source:** [beyondsecurity.com](https://www.beyondsecurity.com)

A smart fuzzer that detects buffer-overflow vulnerabilities in IoT devices by generating malformed/unexpected input and watching for a crash. It can virtually every attack vector — starting with an automated black-box test — then confirms and certifies discovered vulnerabilities, covering the full range of IoT/embedded/process-control/automotive/aerospace protocols.

### Other Vulnerability Scanners Worth Knowing

- **Metasploit** — [rapid7.com](https://www.rapid7.com)
- **IoTSploit** — [iotsploit.co](https://iotsploit.co)
- **IoTVAS** — [firmalyzer.com](https://firmalyzer.com)
- **Enterprise IoT Security** (Palo Alto Networks) — [paloaltonetworks.com](https://www.paloaltonetworks.com)

### Analyzing Spectrum and IoT Traffic — Gqrx

**Source:** [gqrx.dk](https://gqrx.dk)

Gqrx is a GNU Radio + Qt GUI-based spectrum analyzer, useful for eyeballing exactly which frequency bands nearby IoT devices are chattering on.

```bash
git clone https://github.com/gqrx-sdr/gqrx gqrx.git
cd gqrx
mkdir build
cd build
cmake ..
make

# Launch
gqrx
```

Connect an SDR dongle (e.g., FunCube Dongle Pro+, Airspy, or RTL-SDR) to a USB port first. Once running, adjust the FFT settings (bottom-right of the Gqrx window) to zoom into a specific frequency range — device traffic will visibly spike on the waterfall display.

### Analyzing IoT Traffic — ONEKEY

**Source:** [onekey.com](https://onekey.com)

ONEKEY (formerly IoT Inspector) automatically scans devices on a network, builds a chart of traffic activity, and enumerates each device's communication endpoints — useful for quickly seeing what an unfamiliar device is "phoning home" to.

---

## Phase 3 — Launch Attacks

Once vulnerabilities are confirmed, attackers move to exploitation — mostly via **radio-frequency (SDR)** attacks, **hardware bus** attacks, and protocol-specific exploitation.

### Tools to Perform SDR-Based Attacks

| Tool | Source | Notes |
|---|---|---|
| **Universal Radio Hacker (URH)** | [github.com](https://github.com) | A complete workflow tool for investigating unknown wireless protocols — identify hardware interfaces, demodulate signals, assign labels/participants, crack simple stream ciphers (e.g., CC1101 data whitening), reverse-engineer protocol fields, fuzz components, and inject modulated data back into the target system. |
| **BladeRF** | [nuand.com](https://www.nuand.com) | A full-duplex SDR platform for higher-bandwidth signal work. |
| **TempestSDR** | [github.com](https://github.com) | Recovers video/data from unintentional electromagnetic emissions (TEMPEST-style side-channel). |
| **HackRF One** | [greatscottgadgets.com](https://greatscottgadgets.com) | The most widely used half-duplex SDR transceiver for IoT/RF work — 1 MHz to 6 GHz range. |
| **GP-Simulator** | [gpspatron.com](https://gpspatron.com) | GPS/GNSS signal simulation, used to test/attack GPS-dependent IoT devices. |
| **Gqrx** | [gqrx.dk](https://gqrx.dk) | Spectrum analysis (see Phase 2 above). |

### Rolling Code Attack — RFCrack

**Source:** [github.com](https://github.com)

```bash
# Live replay of a captured signal
python RFCrack.py -i

# Rolling-code jam/capture at a specific modulation and frequency
python RFCrack.py -r -M MOD_2FSK -F 314350000

# Adjust the RSSI capture range (upper/lower threshold, in dB)
python RFCrack.py -r -M MOD_2FSK -U 100 -L -10 -F 314350000

# Jam a frequency
python RFCrack.py -j -F 314000000

# Scan the common pre-set frequencies
python RFCrack.py -k

# Scan a custom list of frequencies
python RFCrack.py -k -f 433000000 314000000 390000000

# Incremental frequency scan with verbose output
python RFCrack.py -b -v -F 315000000

# Send a previously-saved capture back out
python RFCrack.py -u ./captures/test.cap -F 315000000 -M MOD_ASK_OOK
```

### Hacking Zigbee Devices with Open Sniffer

**Source:** [sewio.net](https://www.sewio.net)

Open Sniffer is a Wireshark-based hardware analyzer that captures and decodes IEEE 802.15.4 traffic (Zigbee, 6LoWPAN, Wireless HART, ISA100.11a) directly over its USB interface into Wireshark, letting an attacker replay captured frames back into the target network.

### BlueBorne Attack Using HackRF One

HackRF One's wide 1 MHz–6 GHz range covers Bluetooth, Zigbee, and other short-range protocols, making it possible to sniff, fuzz, and jam Bluetooth/BLE traffic with the same box used for cellular or Zigbee work.

### Replay Attack Using HackRF One

```bash
# Step 1: record the target device's signal at its known frequency
hackrf_transfer -r connector.raw -f [device frequency]

# Step 2: replay the recorded signal back at the target
hackrf_transfer -t connector.raw -f [device frequency]
```

### SDR-Based Attacks Using RTL-SDR and GNU Radio

**RTL-SDR** ([rtl-sdr.com](https://www.rtl-sdr.com)) is an inexpensive USB dongle capable of receiving 500 kHz – 1.75 GHz. Common uses in IoT recon: receiving/decoding GPS, analyzing spectrum, listening to DAB broadcast radio, decoding HD radio, sniffing GSM signals, monitoring VHF amateur radio, scanning trunked radio conversations, and scanning cordless-phone bands.

**GNU Radio** ([gnuradio.org](https://www.gnuradio.org)) provides the software framework and pre-built tools to actually process what RTL-SDR/HackRF captures:

| Tool | Purpose |
|---|---|
| `uhd_fft` | Spectrum-analyzer GUI tool connected to a USRP for finding a signal of interest |
| `uhd_rx_cfile` | Stores raw samples to a file for offline analysis with Matlab/Octave or similar |
| `uhd_rx_nogui` | Listens to/records incoming signal on the audio device, no GUI |
| `uhd_siggen_gui` | Generates simple test waveforms (sine, square, ramp) |
| `gr_plot` | Presents previously-recorded samples from a file |

### Side-Channel Attack Using ChipWhisperer

**Source:** [newae.com](https://www.newae.com)

ChipWhisperer is an open-source hardware/software toolchain purpose-built for embedded hardware security research: power-analysis and glitching attacks. It requires two components: a **Capture Board** (for capturing power-consumption traces with tight, synchronized sampling) and a **Target Board** (the device under test — programmed to run the algorithm being attacked). By feeding known plaintext through AES/RSA/triple-DES implementations while recording the device's power draw, an attacker can statistically recover the secret key without ever breaking the cryptographic algorithm itself.

### Identifying IoT Communication Buses and Interfaces (UART / JTAG / I2C / SPI)

Almost every embedded PCB exposes at least one of these low-level debug/communication buses — finding and talking to them is often the fastest path to full device control. The **EXPLIoT** framework (a Python-based IoT/hardware pentest framework) is the module's tool of choice for interacting with them via a **Bus Auditor** hardware adapter:

```bash
# UART — identify the two channels (CH0/CH1) on the PCB, then:
run busauditor.generic.uartscan -v 3.3 -p /dev/ttyACM0 -s 0 -e 1

# JTAG — connect CH0–CH8 to the JTAG header, then:
run busauditor.generic.jtagscan -v 3.3 -p /dev/ttyACM0 -s 0 -e 10

# I2C — connect CH0–CH8 to the I2C header, then:
run busauditor.generic.i2cscan -v 3.3 -p /dev/ttyACM0 -s 0 -e 10
```

**SPI** identification is typically done manually: read the chip's part number silkscreened on the package and Google it for the datasheet/pinout, since SPI has no universal auto-detect signature the way UART/JTAG do.

**Additional bus/interface identification tools:**

| Tool | Source |
|---|---|
| **JTAGulator** | [grandideastudio.com](https://www.grandideastudio.com) |
| **Attify Badge** | [attify-store.com](https://www.attify-store.com) |
| **Saleae Logic Analyzer** | [saleae.com](https://www.saleae.com) |

### NAND Glitching

**NAND glitching** is a physical fault-injection technique used to bypass a device's secure-boot chain by momentarily grounding a specific pin on the flash memory chip during boot, forcing the bootloader to load an unverified/backup image instead of the signed production one.

```bash
# 1. Connect a UART-to-USB adapter to the device's console header,
#    then start a serial terminal to observe the boot sequence
minicom -D /dev/ttyUSB0 -w -C D-link_startup.txt

# 2. During boot, physically short the target chip's I/O pin at the
#    right moment to interrupt the ongoing boot process (this drops
#    the device into a recovery/bootloader prompt)

# 3. From the bootloader prompt, inspect the boot arguments
printenv

# 4. Load a backup/insecure boot configuration
setenv bootargs 'noinitrd console=ttyAM0,115200 rootfstype=ubifs ubi.mtd=5 root=ubi0:rootfs rw qgmi.badupdater'

# 5. Load the kernel from flash and boot it manually
nand read $(loadaddr) app-kernel 0x00400000 && bootm $(loadaddr)
```

`printenv` reveals the bootargs currently loaded (often including `console`, `rootfstype`, and `root` device settings); `nand read` combined with `bootm` manually reads a kernel image out of NAND flash into RAM and boots it, bypassing whatever signature check the normal boot path would have enforced.

### Exploiting Cameras Using CamOver

**Source:** [github.com](https://github.com)

CamOver is a camera-exploitation tool that discloses network camera administrator passwords by exploiting known vulnerabilities in popular camera models — including brands built on Cross Web Server, GoAhead, and Netwave firmware.

```bash
# Exploit a single camera at a known IP
camover -t <Camera IP Address>

# Exploit a router with the same class of vulnerability
camover -t <Router IP Address>

# Exploit every camera on the internet found via a Shodan query
camover -t --shodan <Shodan API Key>
```

---

## Phase 4 — Gain Remote Access

### Gain Remote Access Using Telnet

Many embedded systems — routers, IP cameras, VoIP phones, industrial sensors, even some TVs — still ship with a Telnet service listening for "convenience." Since Telnet transmits everything (including credentials) in cleartext and often accepts factory-default logins, it remains one of the single most reliable IoT foothold vectors.

**Workflow:**
1. Use **Shodan** or **Censys** to find devices with port 23 (Telnet) open on the target network or organization.
2. Attempt the manufacturer's known default credentials, or brute-force a short common-password list.
3. Once authenticated, the attacker has an interactive shell — sufficient to pull configuration files, pivot into the LAN, or plant persistence.

---

## Phase 5 — Maintain Access

### Maintain Access by Exploiting Firmware

**Firmware Mod Kit** is a collection of scripts and utilities for deconstructing and reconstructing firmware images across a huge range of embedded devices and Linux-based router firmware.

| Script | Purpose |
|---|---|
| `extract-firmware.sh` | Primary script — extracts a firmware image into its component filesystem and any embedded binaries |
| `build-firmware.sh` | Primary script — rebuilds a modified filesystem back into a flashable firmware image |
| `extract-gui.sh` | Secondary script — extracts Web GUI files from a DD-WRT-style firmware image |
| `rebuild-gui.sh` | Secondary script — restores and rebuilds Web GUI files into a modified DD-WRT-style firmware image |

Typical workflow: extract a firmware image → modify a file inside the extracted filesystem or web UI → rebuild the modified image → flash it back onto the target device (or on a brick-and-recover-later basis, extract just enough to plant a backdoor binary or an SSH key).

### Firmware Analysis and Reverse Engineering

Once a firmware `.bin` is extracted (from a physical SPI/NAND dump, an intercepted OTA update, or a manufacturer's public download), a typical static-analysis workflow looks like:

```bash
# 1. Identify the file type / container format
file firmware.bin

# 2. Pull every printable ASCII string of length ≥10 (catches hardcoded
#    URLs, credentials, debug strings, version banners)
strings -n 10 firmware.bin > strings.out
less strings.out

# 3. Identify and auto-extract embedded filesystems/compressed
#    sections (SquashFS, JFFS2, cramfs, gzip, LZMA, etc.)
binwalk -e firmware.bin

# 4. Dump a hex/ASCII view of a specific region for manual inspection
hexdump -C -n 512 firmware.bin > hexdump.out
cat hexdump.out

# 5. Manually carve out a filesystem partition once its exact
#    offset/size are known (from binwalk's signature output)
dd if=firmware.bin bs=1 skip=922440 count=2522310 of=myfs.bin

# 6. Mount the extracted filesystem read-only for inspection
sudo mount -o loop myfs.bin rootfs

# 7. Search the mounted filesystem for secrets/config
grep -rnw '/path/to/rootfs/' -e 'password'
find . -iname '*.conf' -o -iname '*.cfg' -o -iname '*.pem' -o -iname '*.key'
```

**Dynamic analysis (actually running the extracted binary) is done with QEMU user-mode emulation**, which lets an x86 analysis machine execute MIPS/ARM/etc. binaries pulled straight from the firmware:

```bash
# Determine the target binary's CPU architecture first
file some_binary
readelf -h some_binary

# Run a single binary under QEMU user-mode emulation
qemu-mipsel -L <sysroot_prefix> <binary>
qemu-arm    -L <sysroot_prefix> <binary>
qemu-<arch> -L <sysroot_prefix> <binary>

# Or fully chroot into the extracted root filesystem using a
# statically-linked QEMU binary, so the binary sees a "real" environment
cp $(which qemu-arm-static) /path/to/extracted/rootfs/usr/bin/
chroot /path/to/extracted/rootfs /bin/sh
```

---

## IoT Hacking Tools Roundup

A quick-reference list of additional named tools called out across the methodology section:

| Tool | Source | Category |
|---|---|---|
| **CatSniffer** | [github.com](https://github.com) | Multi-protocol RF sniffer board (Zigbee, BLE, Thread) |
| **KillerBee** | [github.com](https://github.com) | Zigbee/IEEE 802.15.4 attack framework |
| **JTAGULATOR** | [grandideastudio.com](https://www.grandideastudio.com) | Automatic JTAG/UART pinout discovery |
| **wiz_exploit** | [github.com](https://github.com) | Exploit tooling targeting specific smart-bulb/IoT product lines |
| **PENIOT** | [github.com](https://github.com) | IoT penetration-testing framework covering multiple protocol layers |
| **RouterSploit** | [github.com](https://github.com) | Metasploit-style exploitation framework focused on embedded/router devices |

---

**Previous:** [04 — IoT Malware and Botnets](04-iot-malware-and-botnets.md)
**Next:** [06 — IoT Countermeasures and Security](06-iot-countermeasures-and-security.md)
