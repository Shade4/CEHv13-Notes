# 08 — OT Attacks and Threats

> Learning Objective 4 (continued): *Explain OT Concepts and Attacks.*

## Table of Contents

- [Challenges of OT](#challenges-of-ot)
- [OT Vulnerabilities](#ot-vulnerabilities)
- [MITRE ATT&CK for ICS](#mitre-attck-for-ics)
- [The 14 OT Threat Categories](#the-14-ot-threat-categories)
- [HMI-based Attacks](#hmi-based-attacks)
- [Side-Channel Attacks on SCADA](#side-channel-attacks-on-scada)
- [Hacking PLCs](#hacking-plcs)
- [Hacking Industrial Systems through RF Remote Controllers](#hacking-industrial-systems-through-rf-remote-controllers)
- [OT Supply Chain Attacks](#ot-supply-chain-attacks)

---

## Challenges of OT

OT security lags IT security by roughly a generation, for structural reasons:

- **Lack of visibility** — broader cybersecurity visibility is difficult in any potential OT security area, and most OT organizations don't have real-time cyber-visibility over their assets or the teams to build/manage it.
- **Plain-text passwords** — most industrial site networks are either weak or aren't required at all, making it difficult for teams to enforce credential hygiene.
- **Network complexity** — OT networks are unwieldy, spanning numerous devices, each of which will typically be running a different security posture and update requirement.
- **Legacy technology** — OT systems generally use older devices/protocols with encryption and password security features that lag well behind modern security practice, and are difficult to upgrade without a plant shutdown.
- **Lack of antivirus protection** — most industrial site networks provided with any antivirus at all are either weak or entirely absent, because introducing antivirus scanning risk-of-disruption on process-critical machines is itself seen as a risk.
- **Lack of skilled security professionals** — the field is niche, so there aren't enough people to organizations to discover threats, and implement and enforce security controls and defenses.
- **Rapid pace of change** — as OT and digital transformation processes continue converging with IT, they also grow the OT organization's threat/attack surface.
- **Outdated systems** — most OT devices, such as PLCs and RTUs, are vulnerable to many modern attacks, as they were never designed to withstand internet-connected threats.
- **Insecure connections** — OT systems communicate over public Wi-Fi and unencrypted RF connections in the far-from-uncommon case, making them vulnerable both in-transmission and at-rest.
- **Usage of rogue devices** — many industrial site networks are either weak-or-strong depending on how vulnerable to many rogue devices connected to their networks, which are vulnerable to many attackers and malicious insiders.
- **Convergence with IT** — IT convergence often mixes together virtual attack surfaces and malicious hackers; as a result, it's vulnerable to various network attacks and malicious hackers. In addition, the OT security team doesn't have much awareness of the OT systems and defenses that would otherwise apply.
- **Organizational challenges** — many organizations that manage physical, cyber, and human security teams that meet needs of both IT and OT can create silos easily.
- **Unique production networks/proprietary software** — industries follow different levels of proprietary software that are dependent on industry vendors and explicit vendor control, so patching typically requires a multi-vendor coordination effort.
- **Vulnerable communication protocols** — OT protocols such as Modbus and Profinet were designed for supervising, controlling, and directing different communication functions. These protocols lack authentication, encryption, or built-in detection of abnormal behavior, making them vulnerable to various attacks.
- **Resource constraints** — OT systems often operate with limited processing power and memory, which restricts the use of advanced security features.
- **Lack of encryption** — data transmitted between OT systems is vulnerable to interception and manipulation.
- **Data integrity issues** — attacks that alter sensor data, such as sensor tag readings, can have disastrous effects, as decisions and actions are taken based on false information.

---

## OT Vulnerabilities

| # | Vulnerability | Description |
|---|---|---|
| 1 | **Publicly Accessible OT Systems** | OT systems are directly connected to the internet so that third-party vendors can remotely perform maintenance/diagnostics; OT systems are not protected using modern network controls, so they're vulnerable to disable or degrade the functions of the OT infrastructure. |
| 2 | **Insecure Remote Connections** | Corporate networks are jump-boxed to establish connectivity with the OT network; attacking exploitable vulnerabilities in jump boxes gives access to the OT network. |
| 3 | **Missing Security Updates** | Outdated software versions led to increased usage and the way for attackers to compromise the OT systems. |
| 4 | **Weak Passwords** | Operators and administrators default use passwords for OT systems, which are easily guessable; the ability to gain access to the OT systems if the default vendor-set credentials and permissions are not changed. |
| 5 | **Insecure Firewall Configuration** | Misconfigured access rules allow unnecessary access between corporate IT and OT networks; support systems allow excessive access permissions to interfaces on the network, which makes the network vulnerable to attack. |
| 6 | **OT Systems Placed within the Corporate IT Network** | OT systems are interconnected with the corporate IT network, as they're used for accessing operational data or exporting third-party management systems; OT systems such as control stations and reporting servers are placed within the IT network; the ability to use compromised IT systems to gain access to the OT network. |
| 7 | **Insufficient Security for Corporate IT Network from OT Systems** | Attacks also originate from OT systems, as they use unsegmented legacy hardware and software over corporate networks; the ability to gain unauthorized access to corporate IT systems through insecure OT networks. |
| 8 | **Lack of Segmentation within OT Networks** | Several OT systems have a flat unsegmented configuration, which assumes all systems have equal importance and functions; compromise of a single device exposes the entire OT network. |
| 9 | **Lack of Encryption and Authentication for Wireless OT Networks** | Wireless equipment used within OT networks uses insecure or outdated security protocols; the ability to allow attackers to intercept or manipulate wireless data by sniffing or authentication bypass attacks. |
| 10 | **Unrestricted Outbound Internet Access from OT Networks** | OT networks allow direct outbound network connections to a remote location without support patching and maintenance; direct outbound internet connectivity to insecure and unpatched OT devices increases the risk of malware infection and command-and-control access. |

*(Table 18.8 in the source courseware.)*

---

## MITRE ATT&CK for ICS

**Source:** [attack.mitre.org](https://attack.mitre.org)

MITRE ATT&CK for ICS is an industry-standard knowledge base of ICS-specific attacker tactics and techniques, used by ICS security teams to understand and characterize the behavior of an attacker across the intrusion lifecycle. Below is the full set of tactics with the techniques the module discusses under each — this is the canonical vocabulary you'll see in every real-world ICS incident report.

### Initial Access
The methods and techniques an attacker uses to establish a foothold within the targeted OT environment: web, assets, workstations, and other external systems that access the OT environment.

| Technique | Description |
|---|---|
| Drive-by Compromise | An attacker gains access to the OT network by exploiting a compromised website the target user visits during a browsing session. |
| Exploiting a Public-Facing Application | An attacker leverages known vulnerabilities in an OT-facing web application to gain access. |
| Exploiting Remote Services | An attacker manipulates known vulnerabilities of a remote service in a device or system to gain further access to the remote OT environment. |
| External Remote Services | An attacker connects to the OT network through external remote-access services such as VPNs, Citrix, or other remote-access services. |
| Internet-Accessible Devices | An attacker can gain access to the OT network by exploiting internet-facing OT assets and services. |
| Remote Services | An attacker can manipulate remote-service protocols to gain unauthorized access to OT assets. |
| Replication Through Removable Media | An attacker gains initial access by copying malware onto removable media (e.g., a USB stick) and infecting an air-gapped/isolated system when that media is used. |
| Spear-Phishing Attachment | An attacker sends a fraudulent email with a malicious attachment to trick users into executing malware on their systems. |
| Supply-Chain Compromise | An attacker gains access by manipulating products or product-delivery mechanisms prior to receipt by the target consumer. |
| Transient Asset | An attacker gains access to the network through the transitory nature of assets that are moved on and off the ICS network. |
| Wireless Compromise | An attacker gains access by exploiting weaknesses in wireless communication used within the OT environment. |
| Rogue Master | An attacker introduces a rogue master device onto the network that impersonates a legitimate ICS server to intercept or issue unauthorized commands. |

### Execution
Refers to techniques used to execute malicious code, manipulate, and exploit ICS/OT devices or applications through illegitimate means:

| Technique | Description |
|---|---|
| Changing the Operating Mode | An attacker changes the operating mode of a PLC to enable functionalities during a live attack. |
| Command-Line Interface (CLI) | An attacker uses CLI to interact with the target system through a command line, either locally or remotely, to run malicious commands. |
| Execution through API | An attacker injects malicious code into APIs to perform specific functions in a system after being called by the associated application. |
| Graphical User Interface (GUI) | An attacker interacts with a GUI on a target device or workstation using a mouse or keyboard to execute an action, taking advantage of an interactive session. |
| Hooking | An attacker manipulates how a system behaves to intercept function calls, messages, or events being passed between software components. |
| Modify Controller Tasking | An attacker modifies the tasking configuration of a controller (e.g., a PLC's scan-cycle logic) to execute malicious payloads. |
| Native API | An attacker abuses native operating-system API functions to execute malicious code. |
| Scripting | An attacker performs execution of a script to perform malicious actions. |
| User Execution | An attacker relies on a user performing an action such as clicking a malicious link or opening a malicious file. |

### Persistence
Attackers employ persistence procedures to retain access within the ICS environment, even if the compromised device is restarted or the communication is interrupted:

| Technique | Description |
|---|---|
| Modifying a Program | An attacker modifies a program to inject malicious code by altering the behavior of the program when it communicates with the ICS environment. |
| Module Firmware | A malicious firmware image can be inserted into the hardware of the ICS environment or other devices and hold footprints for long-term access. |
| Project File Infection | An attacker injects malicious code into project files as objects or variables required for the functioning of programmable logic controllers (PLCs). Attackers often update or execute the file to abuse the programmable file components. |
| System Firmware | Malicious code can be inserted into flash memory to modify system firmware, as it directly modifies the behavior of a hardware device. |
| Valid Accounts | An attacker retains access with credentials for existing accounts, obtained through legitimate or illegitimate means. |

### Privilege Escalation
Enables an attacker to achieve higher-level system permissions and authorizations, to perform further malicious activities on target ICS or devices. Techniques include:

| Technique | Description |
|---|---|
| Exploiting Software | An attacker takes advantage of programming errors in software to elevate privileges by abusing exploitable systems or applications. |
| Hooking | It allows attackers to hook into APIs of different processes for redirecting and calling them to elevate privileges. |

### Evasion
Techniques used by attackers to evade conventional defensive mechanisms deployed on a host or network:

| Technique | Description |
|---|---|
| Rootkits | An attacker can install rootkits to avoid detection by hiding different services, connections, and other system drivers. |
| Changing the Operator Mode | Attackers can modify a controller's operating mode to gain access to control and disable other protective functionalities during an attack. |
| Exploitation of Software Vulnerabilities | An attacker can gain further exploitation of software vulnerabilities. |
| Masquerading | An attacker can manipulate features of their artifacts to make them appear legitimate or benign to users and security tools. |
| Spoofed Reporting Messages | An attacker can spoof reporting messages. |

### Discovery
The process of gaining information about an ICS environment to identify assets that can be used to gain information about the ICS environment:

| Technique | Description |
|---|---|
| Enumerating the Network Connection | Attackers can gain information about the communication protocols used, destination, and other important information. |
| Network Sniffing | An attacker can capture or monitor network traffic to gather information about the protocol used, destination, and other important information. |
| Identifying Remote Systems | An attacker finds the details of other systems on the network through their hostnames, IP addresses, or other details on malicious activities. |
| Remote System Information Discovery | An attacker can discover remote-system information via wireless sniffing. |
| Wireless Sniffing | An attacker gathers information from wireless networks associated with target devices, such as identification of assets and communication patterns. |

### Lateral Movement
Attempts to add additional movements across the target ICS environment by leveraging the existing tools/access an attacker already controls, so they can move between systems and components. Techniques include:

| Technique | Description |
|---|---|
| Default Credentials | An attacker can leverage the in-built credentials of a system within a controller to perform administrative operations. |
| Program Download | An attacker can transmit a user program while executing a downloaded program. |
| Remote Services | An attacker can abuse remote services to make lateral movements within the network and systems and components. |
| Exploiting Remote Services | An attacker can leverage the remote services of a controller within a communication protocol. |
| Lateral Tool Transfer | An attacker can transfer tools or files from one system to another to facilitate lateral movement. |
| Valid Accounts | An attacker can leverage valid accounts to make lateral movements within the network. |

### Collection
Refers to various methods attackers use to gather information and gain knowledge regarding the data domains of the ICS infrastructure. Attackers can use the following techniques for gathering data:

| Technique | Description |
|---|---|
| Automated Collection | An attacker can use various tools or scripts to collect the information of an ICS environment automatically. |
| Information Repositories | An attacker can gain sensitive information such as layouts of a control system and specifications targeting the information system. |
| I/O Image | An attacker can obtain the I/O image of a PLC for performing further malicious activities. |
| Detecting the Operating Mode | An attacker can determine the operating mode. |
| Man-in-the-Middle Attack | An attacker can monitor the process state. |
| Monitoring the Process State | An attacker can monitor the traffic of the target ICS environment. |
| Point and Tag Identification | An attacker can identify sensor point and equipment tags used across a control system. |
| Program Upload | An attacker can upload a program. |
| Screen Capture | An attacker can capture screen content. |
| Wireless Sniffing | An attacker can gather information from wireless networks associated with target devices. |

### Command and Control
An attacker attempts to deactivate, control, or exploit the physical control processes within the target ICS environment using command and control used for command and control are as follows:

| Technique | Description |
|---|---|
| Frequently Used Ports | An attacker can use popular ports such as 80 and 443 to communicate and evade the network defense mechanisms. |
| Connection Proxy | An attacker can control the traffic of the target devices across the ICS environment using a proxy mechanism. |
| Standard Application-Layer Protocol | An attacker can use different application-layer protocols such as HTTPS, Telnet, and Remote Desktop Protocol (RDP) to hide their actions and establish control over the systems. |

### Inhibit Response Function
The inhibition of response function refers to the different ways an attacker attempts to thwart reactions against an early security hazard or failure:

| Technique | Description |
|---|---|
| Activate Firmware Update Mode | An attacker can activate the firmware update mode and thwart normal functionalities during a firmware update. |
| Block Command Messages | An attacker can block various commands or communications before they reach the destination systems, allowing the industrial process and other functions to hide their activities. |
| Block Reporting Messages | An attacker can stop or disrupt the reporting messages before they reach their destination, allowing the industrial process and prevent operators from noticing signs of malicious activities. |
| Alarm Suppression | Techniques associated with inhibiting response functions. |
| Blocking Serial COM | Techniques associated with inhibiting response functions. |
| Data Destruction | Techniques associated with inhibiting response functions. |
| Denial of Service (DoS) | Techniques associated with inhibiting response functions. |
| Device Restart/Shutdown | Techniques associated with inhibiting response functions. |
| Control I/O Image | Techniques associated with inhibiting response functions. |
| Changing Alarm Settings | Techniques associated with inhibiting response functions. |
| Rootkit | Techniques associated with inhibiting response functions. |
| Service Stop | Techniques associated with inhibiting response functions. |
| System Firmware | Techniques associated with inhibiting response functions. |

### Impair Process Control
Attackers use this tactic to disable, exploit, or control the physical control processes present in the target environment:

| Technique | Description |
|---|---|
| I/O Bruteforcing | Attackers can brute-force the I/O addresses of a target functionality without targeting a specific configuration. |
| Alter the Parameters | An attacker can manipulate the control parameters by altering their instruction parameters deployed to perform malicious tasks. |
| Module Firmware | An attacker can re-program a firmware into it to perform malicious tasks. |

Additional techniques associated with impairing process control: **Spoofed reporting messages**, **Unauthorized command messages**.

### Impact
Refers to techniques used by an attacker to damage or disrupt the physical process:

| Technique | Description |
|---|---|
| Damage to Property | An attacker can cause damage to property or disrupt the surrounding environments by performing various actions on the ICS. |
| Loss of Availability | An attacker can disrupt or hamper the industrial process to make them unavailable to the associated business. |
| Loss of Control | An attacker can manipulate the controls and communications between the operators and the process controls. |
| Loss of View | Denial of view |
| Loss of Control | Denial of control |
| Loss of Productivity and Revenue | Result of process disruption or downtime |
| Loss of Protection | Safety system disablement |
| Loss of Safety | Bypassed safety interlocks |
| Manipulation of Control | Direct alteration of controller behavior |
| Manipulation of View | Falsifying what an HMI operator sees |
| Theft of Operational Information | Exfiltration of process specifications and configuration data |

*(This tactic/technique layout is adapted from the module's coverage of the attack.mitre.org ICS matrix.)*

---

## The 14 OT Threat Categories

1. **Maintenance and Administrative Threat** — Attackers exploit zero-day vulnerabilities to target the maintenance and administration of the OT network. By exploiting these vulnerabilities, attackers inject malware and spread it across IT systems and target industrial control systems such as SCADA and PLC.
2. **Data Leakage** — Attackers exploit IT systems connected to the OT network to gain access to IT/OT-connected industrial control infrastructure, leading to significant data leakage.
3. **Protocol Abuse** — Owing to complexity issues, many OT systems use outdated legacy protocols and interfaces that use various cyber-physical interfaces, etc. For example, attackers may abuse emergency stop (e-stop) in emergencies to execute single-packet attacks.
4. **Potential Destruction of ICS Resources** — Attackers exploit the vulnerabilities in the OT infrastructure to bring life- and safety-critical services to disruption or degrade the functionality of the OT infrastructure.
5. **Reconnaissance Attacks** — OT systems allow remote communication with minimal or no encryption or authentication mechanisms. Attackers can perform initial reconnaissance and scanning on the target OT infrastructure to gather information necessary for later stages of the attack.
6. **Denial-of-Service Attacks** — Attackers exploit communication protocols such as Common Industrial Protocol (CIP) to perform DoS attacks on OT systems. For example, an attacker may send a malicious CIP connection request or a fake IP configuration to bring devices offline, leading to potential loss of view, control, or configuration of connected devices.
7. **HMI-based Attacks** — Human-Machine Interfaces (HMIs) are often called Hacker-Machine Interfaces. Even with the advancement and automation of OT, human interaction and control over the operational process remains challenging due to the underlying global standards for developing HMI software without any defense-in-depth security measures. This leads to many security problems. Attackers exploit these vulnerabilities to perform various actions on the target, exploiting memory corruption, code injection, insecure privilege escalation, etc. on target OT systems.
8. **Exploiting Enterprise-Specific Systems and Tools** — Attackers may target ICS devices such as Safety Instrumented Systems (SIS) to inject malicious code by exploiting insufficient security protocols to detect hardware and services used in communications, and further disrupt or damage their services.
9. **Spear Phishing** — Attackers send fake emails containing malicious links or well-known attachments, seemingly originating from legitimate or well-known sources to the victim. When the victim clicks on the link or downloads the attachment, it infects the system, starts damaging OT resources, and responds according to malicious instructions, spreading itself to other networked systems and finally damages industrial automation components.
10. **Malware Attacks** — Attackers are reusing legacy malware packages that were previously used to exploit IT systems for exploiting OT systems. They perform reconnaissance attacks to identify vulnerabilities in newly connected OT systems. Once they detect vulnerabilities, they reuse the older malware versions to perform various attacks on the OT systems. In some scenarios, attackers also develop malware targeting OT systems, such as ICS/SCADA.
11. **Exploiting Unpatched Vulnerabilities** — Attackers exploit unpatched vulnerabilities in ICS products, firmware, and other software used in OT networks. ICS vendors develop products that are reliable and provide high-speed, real-time performance with no built-in security features. In addition, these vendors cannot develop patches for the identified vulnerabilities with the same speed as IT vendors do. For these reasons, attackers target and exploit ICS vulnerabilities to perform various attacks on OT networks.
12. **Side-Channel Attacks** — Attackers perform side-channel attacks to retrieve critical information from an OT system by observing its physical implementation. Attackers use various techniques, such as timing analysis and power analysis, to perform side-channel attacks.
13. **Buffer Overflow Attack** — The attacker exploits various buffer overflow vulnerabilities that exist in ICS software, such as the HMI web interface, ICS web client, communications interfaces, etc., to inject malicious data and commands to modify the normal behavior and operation of the systems.
14. **Exploiting RF Remote Controllers** — OT networks use RF technology to control various industrial operations remotely. RF communication protocols lack in-built security for remote communication. Vulnerabilities in these protocols can be exploited by attackers to perform various attacks on industrial machines that lead to production sabotage, system control, and unauthorized access.

---

## HMI-based Attacks

Attackers often try to compromise the HMI system as it's the core hub that controls critical infrastructure. If attackers gain access over HMI systems, they can cause physical damage to the SCADA devices or collect sensitive information related to the critical architecture that can be used later to perform malicious activities — including disabling alert notifications about incoming threats to SCADA systems.

Discussed below are various SCADA vulnerabilities exploited by attackers to perform HMI-based attacks on industrial control systems:

| Vulnerability Category | Description |
|---|---|
| **Memory Corruption** | Code security issues including out-of-bound read/write vulnerabilities and heap/stack-based buffer overflow. Memory corruption occurs when memory contents are altered due to errors residing in the code; when the altered content is used, the program crashes or performs unintended executions. Attackers accomplish this simply by overwriting the code to cause a buffer overflow, and can sometimes use string manipulation on an unflushed stack. |
| **Credential Management** | Use of hard-coded passwords, credentials saved in simple formats such as cleartext, and inappropriate credential protection. Exploitable to gain admin access and alter system databases or other settings. |
| **Lack of Authorization/Authentication and Insecure Defaults** | Vulnerabilities including confidential information transmitted in cleartext, insecure defaults, and unsafe ActiveX controls. |
| **Code Injection** | Attackers exploit critical information transmitted in cleartext, insecure defaults, missing encryption, and insecure ActiveX controls to gain illegal access to the target system. |
| **Buffer Overflow Vulnerabilities** | HMI software prone to buffer overflow vulnerabilities, in which data inputs can overflow the allocated buffer, potentially allowing an attacker to execute arbitrary code on the system. |
| **Path Traversal** | Path-traversal flaws in HMI web servers allow attackers to access directories and files stored outside the web-root folder, leading to information disclosure or manipulation. |

---

## Side-Channel Attacks on SCADA

Attackers perform a side-channel attack by monitoring the physical implementation of a target system to obtain critical information. Attackers use two techniques, namely timing analysis and power analysis, to perform side-channel attacks on the OT systems.

- **Timing Analysis** — Passwords are often transmitted during a serial-comparison loop strategy to try to accurately determine the correct character in sequence. They use an oscilloscope or measuring device connected to the target victim's process to check the response timing of the target device against each character it tests. If the first character is correct, it takes slightly longer to process before rejecting than if it were wrong; checking how the timings change lets the attacker determine how many correct characters have been guessed so far, and continue the attack character-by-character. This attack based on the timing of the change in power consumption during the change of configuration is easily detectable and blocked.
- **Power Analysis** — Power-analysis attacks difficult to detect because the attacked device can operate as if it were being infected, whereas timing-based attacks are more prone to be identified/blocked. This is performed by observing the change in power consumption of semiconductors during clock cycles. The oscilloscope observes the current pulses between the two devices, and the power profile formed by the signals can leave a clue as to what the data being sent is.

*(Illustrated in the module as Figure 18.83 — an attacker using a probe, oscilloscope/measuring device, and analysis software against a target SCADA system.)*

---

## Hacking PLCs

### PLC Rootkit Attack

PLCs are susceptible to cyber-attacks as they're used for controlling the physical processes of critical infrastructure. Attackers identify PLCs exposed to the internet through online tools such as Shodan, then tamper with the integrity and availability of the PLC by exploiting control operations and launching attacks such as payload and PLC rootkits.

**Steps:**
1. **Gaining Access** — Attacker gains authorized access to the PLC device by injecting a rootkit. The performs a control-flow attack against the PLC runtime to gain root/full access to the PLC.
2. **Launches Control-Flow Attack** — The attacker maps the I/O and interacts with the register and RTU (Remote Terminal Unit) runtime, launching a control-flow attack against the PLC runtime.
3. **Gaining Full Access** — After learning about the architectural flaws in the microprocessors and modern detection mechanisms, the attacker gains full control of the PLC input and output processing by manipulating the I/O and PLC pins. This is referred to as a PLC ghost attack. To perform this attack, attackers require in-depth knowledge of PLC architecture.

The CPU of the PLC operates in two modes — i.e., programming mode and run mode. In the programming mode, the PLC can remotely download the code from any computer, and the run mode is used for executing the actual code. When gaining access to the target, the attacker can manipulate the input and output processing by manipulating the I/O pins of the PLC. This malicious code is executed in place of the original code. Now, the attacker manipulates the input and output to gain complete control over mechanical devices and further damage or destroy their operation.

### Evil PLC Attack

In an Evil PLC attack, an attacker tries to identify vulnerable or internet-exposed devices using online resources such as Shodan or Censys. Devices exposed to the internet often lack adequate security measures, making them vulnerable to unauthorized access and intermediary data modifications. If a vulnerable PLC is found, the attacker turns that PLC into a weaponized PLC by modifying its configuration settings and changing its behavior and logic through the download procedures.

**Steps:**
1. **Identify** — Attacker identifies a vulnerable PLC using Shodan or Censys.
2. **Exploit and Weaponize** — The attacker exploits the vulnerable PLC firmware and weaponizes it by changing its programming logic through download procedures.
3. **Distribute the Malicious Payload** — Once the PLC is infected, the attacker initiates upload procedures on the connected workstations to execute arbitrary code.

*(Illustrated in the module as Figure 18.85 — "Illustration of Evil PLC attack methodology": Attacker → Vulnerable PLC → Victim Workstation(s).)*

---

## Hacking Industrial Systems through RF Remote Controllers

Most industrial machines are operated via radio-frequency remote controllers — these are used across manufacturing, logistics, mining, and construction, for automation or to control machines remotely. While the transmitter (TX) and receiver (RX) communicate with each other, the receiver reacts to the incoming commands (via buttons). Improper security implementations in devices operating via remote controllers pose severe security risks to industrial systems.

Attackers stand within the radius of the target system and use a specially-designed radio transceiver-type device. The device helps their own packets and send commands in a network to gain access over the industrial system and perform various malicious activities:

### Replay Attack
Attackers record the RF packets (commands) transmitted by an operator and replay them to the target system to gain basic control over the system.

```
Operator → [Record Commands] → Attacker → [Capture Data] → [TX range]
                                    │
                                    ▼
                          Attacker Transmits Recorded
                          Commands → Target Machine (RX)
```

### Command Injection
Being aware of RF protocols, attackers can alter RF packets or inject new packets across the machine using reverse-engineering techniques. Attackers capture and record commands, perform reverse engineering to determine the commands used to control the target device, and inject new/manipulated commands to manipulate the normal operation of the target device.

```
Capture Data → Obtain Other Commands → Offline Reverse Engineering →
Transmit Other Commands → Target Machine (RX)
```

### Abusing E-Stop
Using the above information, the attacker can send multiple e-stop (emergency stop) commands to the target device to cause a denial-of-service condition — repeatedly halting the machine and preventing normal operation.

### Re-pairing with Malicious RF Controller
An attacker can hijack the original controller and pair up their own malicious RF controller with the target machine. Attackers send malicious requests to pair with target RF controllers, capture the command sequence, hijack the legitimate controller, and use a malicious controller to perform various attacks on the target device.

### Malicious Reprogramming Attack
Attackers can inject malware into the firmware running on the remote controllers to maintain persistent and complete remote access over the target industrial system.

```
Before Attack: Operator (TX1) ←pairing sequence→ Target Machine (RX)
After Attack:  Operator (TX1, unpaired) ... Attacker (TX2, paired & repaired) → Target Machine (RX)
```

---

## OT Supply Chain Attacks

Operational technology (OT) supply-chain attacks involve stakeholders compromising the hardware, software, or services of an organization's target OT infrastructure, which are then used to infiltrate the target organization's OT infrastructure. These attacks can be particularly devastating, as they often exploit trusted relationships and can go undetected for extended periods.

| OT Supply Chain Attack | Description |
|---|---|
| **Third-Party Software Compromise** | Attackers inject malicious code into trusted software updates, creating backdoors or malicious functionalities that get installed. |
| **Hardware Manipulation** | Attackers alter hardware components during manufacturing or distribution, embedding malicious firmware or chips that activate later. |
| **Service Provider Breach** | Attackers compromise service providers such as maintenance or support contractors for an organization's OT equipment, using remote-access credentials, remote-console tools, or onsite access to plant systems. |
| **Injection of Malicious Components** | Attackers introduce malicious components or firmware into the supply chain by tampering with legitimate hardware, or shipping with compromised ones. |
| **Exploitation of Trusted Relationships** | Attackers exploit the trust and access levels granted to suppliers, subcontractors, or partners to move laterally within a target's network. |

*(Table 18.9 in the source courseware.)*

---

**Previous:** [07 — OT/ICS Concepts and Architecture](07-ot-ics-concepts-and-architecture.md)
**Next:** [09 — OT Malware Case Studies](09-ot-malware-case-studies.md)
