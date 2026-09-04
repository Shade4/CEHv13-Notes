# 06 — IoT Countermeasures and Security

> Learning Objective 3: *Explain IoT Attack Countermeasures.*

## Table of Contents

- [How to Defend Against IoT Hacking](#how-to-defend-against-iot-hacking)
- [Mobile App / Device Security Guidelines](#mobile-app--device-security-guidelines)
- [How to Prevent SDR-Based Attacks](#how-to-prevent-sdr-based-attacks)
- [General Guidelines for IoT Device Manufacturers](#general-guidelines-for-iot-device-manufacturers)
- [OWASP Top 10 IoT Vulnerabilities — Solutions](#owasp-top-10-iot-vulnerabilities--solutions)
- [IoT Framework Security Considerations](#iot-framework-security-considerations)
- [IoT Hardware Security Best Practices](#iot-hardware-security-best-practices)
- [Secure Development Practices for IoT Applications](#secure-development-practices-for-iot-applications)
- [IoT Device Management Platforms](#iot-device-management-platforms)
- [IoT Security Tools](#iot-security-tools)

---

## How to Defend Against IoT Hacking

A baseline hardening checklist for any IoT deployment:

- Disable the **"guest"** and **"demo"** user accounts wherever the device ships with them enabled by default.
- Use a **lockout policy** to lock out accounts after repeated failed login attempts.
- Implement **strong, multi-factor authentication**.
- Isolate control-system networks and devices behind **firewalls**, and separate them from the general business network.
- Implement **IPS and IDS** on the network.
- Deploy **end-to-end encryption** and a public-key infrastructure (PKI) for device communications.
- Use a **VPN architecture** for secure remote communication.
- Deploy security as a **unified, integrated system** rather than a patchwork of point solutions.
- **Allow only trusted IP addresses** to reach devices/routers where possible.
- **Disable Telnet** on the device outright unless there's a specific, justified operational reason to keep it.
- **Disable UPnP** on routers — it's a frequent source of unintended port exposure.
- Physically **protect devices against tampering**.
- **Patch vulnerabilities and update device firmware** on a regular cadence.
- **Monitor traffic on port 48101** — historically associated with a well-known IoT-malware infection vector, so unexpected traffic there is a strong compromise indicator.

---

## Mobile App / Device Security Guidelines

Since most IoT products are operated through a companion mobile app, hardening that app is just as important as hardening the device itself:

- **Verify the position** of mobile nodes to confirm they belong to one physical device only — one device identity per node, to prevent identity confusion attacks.
- Implement **data privacy** so information collected is retained only as long as necessary and kept confidential.
- Perform **data authentication** so received information is verified as coming from a legitimate, registered node.
- Maintain **data confidentiality** using symmetric encryption between the app and the device.
- Enforce a **strong password policy** requiring a mix of letters, numbers, and special characters at a minimum length.
- Use **CAPTCHA** and **account lockout policy** together to blunt automated credential attacks.
- Prefer devices from manufacturers with a solid **track record of security** in their equipment lineup.
- **Isolate IoT devices** on their own protected network segments, separate from user workstations and servers.
- Implement a **secure boot option** using cryptographic code-signing so the device only executes firmware signed by its equipment manufacturer (OEM).
- Ensure **cryptographic keys** are refreshed and kept current per OEM guidance — not left at factory defaults indefinitely.
- Implement **two-way authentication** using strong algorithms — ECDSA for signing, HMAC-SHA for message integrity.
- **Create an asset inventory** to determine what to protect and where enterprise IT/security resources should focus.
- **Apply access controls** rigorously — least privilege for both users and other devices talking to the endpoint.
- Always **read the privacy policy** of an application before installation, and understand what information is collected.
- Use a **Trusted Execution Environment (TEE)** or security enclave to secure sensitive processing (e.g., TOCTOU/TOCTTOU-sensitive operations, key storage).
- Implement **active tampering / shielding** or physically obscure and lock the device's original equipment interface.
- **Validate code** before it executes to reduce the window for time-of-check-to-time-of-use (TOCTOU) attacks.
- Store encryption/signing keys inside a **Secure Access Module (SAM)**, **TPM**, or **HSM** trusted platform module rather than in plain firmware storage.
- Prevent unnecessary **disclosure of IP addresses** by IoT applications running in the background.
- Use **ad-blockers and no-track browser extensions** when accessing web-based dashboards from an IoT device or its companion portal.

---

## How to Prevent SDR-Based Attacks

RF-based attacks (see [03 — IoT Attacks and Threats](03-iot-attacks-and-threats.md#deep-dive-sdr-based-attacks)) can be launched from any available bandwidth, so defense has to be proactive at the protocol design level rather than reactive:

| Technique | Description |
|---|---|
| **Securing the Signal** | The single most effective control: strong signal encryption on every RF link, so a captured waveform is useless without the key. |
| **Avoiding Command Repetition via a Rolling Technique** | Frequent reuse of the same command (e.g., a static unlock code) invites brute-force replay attacks. Commands should be tied to a rolling/one-time code — the technique legitimate rolling-code fobs already use, hardened against jam-and-capture (see the Rolling Code Attack deep dive). |
| **Adopting Synchronization and Preamble Nibbles** | Segment the command sequence with a synchronized preamble and a reduction mechanism, so the protocol can only be brute-forced by re-guessing multiple nibbles simultaneously, not one at a time. |
| **Use of Anti-Jamming Techniques** | Implement anti-jamming mechanisms in firmware to detect and mitigate interference or unauthorized transmissions that might disrupt the target's normal RF operation. |
| **Frequency Hopping** | Use frequency-hopping spread spectrum (FHSS) so the transmitter/receiver rapidly switch frequencies within a known band — making it far harder for an attacker to intercept or jam the full session. |
| **Secure Key Management** | Implement robust key-storage and cryptographic operations using hardware security modules (HSMs) rather than storing keys in plaintext firmware. |
| **Secure Over-the-Air (OTA) Updates** | Cryptographically sign every OTA update and validate the signature and authenticity of every update package before applying it, so an attacker can't push a malicious firmware update over the same RF channel. |

---

## General Guidelines for IoT Device Manufacturers

- Use **SSL/TLS** for all communication purposes.
- **Manually check SSL certificates and the revocation list** — don't just trust automated validation blindly.
- **Discourage the use of weak passwords** in every product's setup flow.
- **Ensure credentials aren't hardcoded**, and that every unit ships with a separately generated device password.
- Make the **device update process simple** for the end user.
- Implement **account-lockout mechanisms** after repeated incorrect login attempts to prevent brute-force attacks.
- **Lock the devices down** whenever they're unattended or unused.
- Periodically check for **unused tools and applications** running on or alongside the device.
- Use **safe C functions** (e.g., `fgets()` instead of `gets()`) to reduce the risk of classic buffer-overflow vulnerabilities.
- **Incorporate security into the software development lifecycle** from day one, not as an afterthought.
- Ensure the **security of users' personal data** end-to-end.
- **Provide clear guidelines** to consumers regarding device security and privacy settings.
- Incorporate an **external tamper alert** for the physical lifetime of the device.
- Build in **network-security features** — firewalls, intrusion detection, and network-segmentation capability — into the device from the start.
- Adopt a **policy of transparency** for consumers about exactly what data the device collects and how.
- Integrate **hardware-based security features** such as a Trusted Platform Module (TPM), to store cryptographic secrets, or known and trusted secure elements.
- Use **industry-standard, secure communication protocols** such as MQTT, CoAP, or HTTPS for transmitting data between IoT devices and back-end services.

---

## OWASP Top 10 IoT Vulnerabilities — Solutions

Mapping directly back to the [OWASP Top 10 IoT Threats](02-iot-attack-surface-and-vulnerabilities.md#owasp-top-10-iot-threats) from file 02:

| # | Vulnerability | Solutions |
|---|---|---|
| I1 | **Weak, Guessable, or Hardcoded Passwords** | Use Automated Password Management (APM); use strong, complex passwords; avoid hardcoded credentials entirely. |
| I2 | **Insecure Network Services** | Close open network ports that aren't needed; disable UPnP; encrypt data prior to TLS communication. |
| I3 | **Insecure Ecosystem Interfaces** | Enable an account-lockout mechanism; conduct a periodic assessment of every ecosystem interface; perform security testing and strict input/output filtering. |
| I4 | **Lack of Secure Update Mechanisms** | Verify the source and integrity of every update; encrypt communication between endpoints; notify end-users when a security update is applied. |
| I5 | **Use of Insecure or Outdated Components** | Monitor for unmaintained/EOL components on an ongoing basis; remove unused dependencies and unnecessary features; source software only from vetted, non-compromised suppliers. |
| I6 | **Insufficient Privacy Protection** | Minimize the amount of data collected; anonymize collected data where possible; give end-users the ability to decide what data is collected about them. |
| I7 | **Insecure Data Transfer and Storage** | Encrypt communication between devices; maintain current SSL/TLS implementations; avoid rolling proprietary/home-grown encryption. |
| I8 | **Lack of Device Management** | Blacklist devices with known vulnerabilities from the fleet; validate all asset attributes on enrollment; perform secure decommissioning at end-of-life. |
| I9 | **Insecure Default Settings** | Change default usernames and passwords before deployment; customize privacy/security settings per environment; disable remote access when it isn't in active use; set a unique password for BIOS/firmware access. |
| I10 | **Lack of Physical Hardening** | Configure boot order to prevent booting from removable/USB media; minimize the number of exposed external ports (USB, debug headers) on production units. |

*(Table 18.7 in the source courseware.)*

---

## IoT Framework Security Considerations

Security has to be considered independently at every stage the data passes through:

- **Edge** — The most physically exposed part of the architecture, interacting directly with sensors/actuators, environmental conditions, and human users. It has to be able to operate reliably under any condition and can be deployed nearly anywhere, so it needs its own independent hardening.
- **Gateway** — The first aggregation point that connects cloud/backend infrastructure to the edge. An ideal framework encrypts communication end-to-end between the edge and the gateway, and the gateway itself should support **multi-directional trust verification** — authenticating both the devices below it and the cloud above it. Automatic updates should be deployable from the cloud through the gateway down to the device.
- **Cloud Platform** — The central aggregation and management component; access should be restricted to only what's necessary. In a high-risk environment, it's the most valuable single target, so it needs a centralized computer system for coordinating extensions and updates, secure communications, encrypted storage, automatic updates, and audit logging.
- **Mobile** — The primary interface between the human operator and the rest of the system. An ideal framework requires proper authentication for the user, uses an account-lockout policy, provides encrypted communication channels, and applies the principle of least privilege so a compromised phone doesn't equal a compromised fleet.

---

## IoT Hardware Security Best Practices

- **Limit the entry points** — reduce the attack surface by avoiding deployment of unnecessary entry points such as USB ports on the device wherever they aren't operationally required.
- **Employ a hardware/power tamper-protection mechanism** — detect intrusion into the device board and take defensive action (e.g., zero out keys).
- **Monitor secure booting** — implement detection mechanisms for tampering or glitching at every stage of the boot process, and enforce Trusted Platform Module (TPM)-based storage as the anchor of trust.
- **Deploy least-privilege access management** — apply the principle at every layer, from firmware permissions to physical maintenance access.
- **Employ a hardware-based intrusion-detection system** — sensors and monitoring circuits to detect physical tampering, side-channel attacks, and unauthorized access to device internals.

The following measures secure the encrypted communication and TPM-backed key handling that ties all the above together:

- Employ an **HMAC-key-based secure communication mechanism** between the TPM-based device and the TPM peripheral, so the HMAC key is verified before any data transmission crosses the perimeter.
- Verify sender authentication by decrypting the received data with **HMAC key** verification, and validate authenticity using block chaining algorithms (CBC) and feedback checks (CFB).
- Utilize **RSA-based encryption** to ensure high-integrity data transfer with a signature attached.
- Use TPMs to store keys in **non-volatile random-access memory (NVRAM)** and eliminate any unwanted incidents due to environmental stress or a long-term data transfer.
- Utilize the **canonical mode of data transfer** to eliminate unwanted artifacts from a prolonged data-stream transfer between the IoT hardware units.
- Utilize **root-of-trust (RT) models** such as RT for measurement (RTM) and RT for verification (RTV), provided by TPM for secure booting and data transmission to IoT hardware units.
- Enable **perfect forward secrecy** so each communication session uses a unique, short-lived key that's not derivable from a long-term key.
- Enable **certificate-based authentication mechanisms** to verify the identities of both devices and backend servers before establishing a connection.
- Use **remote attestation** mechanisms provided by TPMs to verify the integrity of software/firmware and detect device/sensor remote-servicing.
- Use authenticated encryption modes with associated data — **AEAD** algorithms such as AES-GCM and AES-CCM — for confidentiality and integrity protection of communication data.
- Utilize **hardware-based random number generators (RNGs)** to generate cryptographic keys and initialization vectors (IVs) for encryption.
- Leverage **cryptographic hardware acceleration** where processors offload encryption/decryption operations to a dedicated cryptographic co-processor for speed and side-channel resistance.
- Implement **key-rotation policies** periodically to change the encryption keys used for communication between IoT devices and backend servers.

---

## Secure Development Practices for IoT Applications

1. **Ensure Secure Boot** — the device only executes code that's authenticated and validated at boot time, preventing unauthorized firmware or manipulation.
2. **Secure API Endpoints** — protect against SQL injection, cross-site scripting (XSS), and cross-site request forgery (CSRF) with proper authentication and data validation.
3. **Implement Threat Modeling** — identify potential threats and risks specific to IoT applications and ecosystems, factoring in data privacy, device authentication, and communication protocols.
4. **Secure Coding Practices** — follow secure coding standards and guidelines to prevent common vulnerabilities such as buffer overflows, injection attacks, and cross-site scripting (XSS) in device code.
5. **Conduct Security Testing** — perform comprehensive security testing, including penetration testing, vulnerability scanning, and code reviews throughout the development lifecycle, to identify and remediate weaknesses.
6. **Ensure Secure Device Identity Management** — implement unique identifiers and digital certificates to authenticate and establish trust in the IoT ecosystem.
7. **Implement Hardware Security** — utilize hardware-based security features such as trusted platform modules (TPM), secure elements, or hardware security modules (HSM) to securely store cryptographic keys and protect sensitive data.
8. **Allow Code Signing** — digitally sign firmware/software and application code to verify its authenticity and integrity before installation, mitigating the risk of unauthorized modifications or malware injection.
9. **Ensure Secure Cloud Integration** — secure integration with cloud services and platforms by implementing proper authentication, access control, and data-encryption mechanisms to protect data stored or processed in the cloud.
10. **Utilize Secure Communication Protocols** — use secure communication protocols such as MQTT with TLS/SSL for device-to-device communication, ensuring confidentiality, integrity, and data exchange between IoT devices and backend services.

---

## IoT Device Management Platforms

Once you're operating hundreds or thousands of IoT devices, ad-hoc management stops working — fleet-management platforms become mandatory security infrastructure, since patching, credential rotation, and decommissioning all need to happen at scale:

| Platform | Source |
|---|---|
| **Azure IoT Central** | [azure.microsoft.com](https://azure.microsoft.com) — hosted SaaS platform to connect, monitor, and manage IoT assets at scale, minimizing the burden and cost of a typical IoT project. |
| **Oracle Fusion Cloud Internet of Things** | [oracle.com](https://www.oracle.com) |
| **Golioth** | [golioth.io](https://golioth.io) |
| **AWS IoT Device Management** | [aws.amazon.com](https://aws.amazon.com) |
| **IBM Watson IoT Platform** | [ibm.com](https://www.ibm.com) |
| **openBalena** | [balena.io](https://www.balena.io) |

---

## IoT Security Tools

| Tool | Source | Focus |
|---|---|---|
| **SeaCat.io** | [teskalabs.com](https://teskalabs.com) | First-security SaaS technology to operate IoT products reliably, scalably, and securely — reduces vulnerability surface by managing product credentials and enrolling devices with vendor-specific cryptography, and automates malware/botnet prevention. |
| **Armis Centrix** | [armis.com](https://www.armis.com) | Helps view, protect, and manage all IoT assets, systems, and processes in an environment, addressing vulnerabilities with tailored security protocols. |
| **ByteSweep** | [gitlab.com](https://gitlab.com) | Automated firmware-analysis tooling. |
| **Entrust IoT Security** | [entrust.com](https://www.entrust.com) | Device identity and PKI-based security for IoT fleets. |
| **IOT ASSET DISCOVERY** | [securolytics.io](https://securolytics.io) | Automated discovery/inventory of IoT assets on a network. |
| **FortiNAC** | [fortinet.com](https://www.fortinet.com) | Network access control with IoT device profiling. |
| **Microsoft Defender for IoT** | [microsoft.com](https://www.microsoft.com) | Agentless network monitoring purpose-built for IoT/OT environments. |
| **Symantec Critical System Protection** | [broadcom.com](https://www.broadcom.com) | Host-based intrusion prevention for fixed-function/embedded systems. |
| **Cisco Industrial Threat Defense** | [cisco.com](https://www.cisco.com) | Threat detection tailored to industrial/IoT network segments. |
| **AWS IoT Device Defender** | [aws.amazon.com](https://aws.amazon.com) | Continuous auditing and anomaly detection for AWS-connected IoT fleets. |
| **Forescout** | [forescout.com](https://www.forescout.com) | Agentless device visibility and network access control across IT/IoT/OT. |
| **NSFOCUS Anti-DDoS System** | [nsfocusglobal.com](https://nsfocusglobal.com) | DDoS mitigation, relevant given how many IoT compromises end in botnet recruitment. |
| **Azure Sphere** | [microsoft.com](https://www.microsoft.com) | A secured, certified microcontroller platform + OS + cloud security service for building IoT hardware securely from the ground up. |
| **Overwatch** | [overwatchsec.com](https://overwatchsec.com) | Managed threat-hunting service, applicable to IoT-heavy environments. |
| **Barbara** | [barbara.tech](https://barbara.tech) | Industrial edge-computing platform with built-in device security. |
| **Sternum** | [sternumiot.com](https://sternumiot.com) | Embedded IoT security (EIV) and observability, deployed directly into device firmware. |
| **Asimily** | [asimily.com](https://asimily.com) | IoT/IoMT risk-management and vulnerability-prioritization platform. |
| **ByteSweep** | [gitlab.com](https://gitlab.com) | See above. |
| **Entrust IoT Security** | [entrust.com](https://www.entrust.com) | See above. |

---

**Previous:** [05 — IoT Hacking Methodology and Tools](05-iot-hacking-methodology-and-tools.md)
**Next:** [07 — OT/ICS Concepts and Architecture](07-ot-ics-concepts-and-architecture.md)

*(This closes out the IoT half of Module 18. The remaining files cover Operational Technology / Industrial Control Systems.)*
