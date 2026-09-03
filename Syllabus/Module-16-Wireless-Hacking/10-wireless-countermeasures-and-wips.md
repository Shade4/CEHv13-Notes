# 10 — Wireless Attack Countermeasures & WIPS

> Objective 5 of the module: *Explain Wireless Attack Countermeasures*

## Table of Contents
- [Wireless Security Layers](#wireless-security-layers)
- [Defense Against WPA/WPA2/WPA3 Cracking](#defense-against-wpawpa2wpa3-cracking)
- [Defense Against KRACK Attacks](#defense-against-krack-attacks)
- [Defense Against aLTEr Attacks](#defense-against-alter-attacks)
- [Detection and Blocking of Rogue APs](#detection-and-blocking-of-rogue-aps)
- [Defense Against Wireless Attacks — Best Practices](#defense-against-wireless-attacks--best-practices)
- [Wireless Intrusion Prevention Systems (WIPS)](#wireless-intrusion-prevention-systems-wips)
- [Wi-Fi Security Auditing Tools](#wi-fi-security-auditing-tools)

---

The previous sections explained how attackers hack wireless networks to steal sensitive data. An ethical hacker works on increasing the security of a wireless network to secure it against attackers. This section discusses defenses and best practices for wireless network security.

## Wireless Security Layers

Wireless security is a **layered** discipline. This layered approach increases the scope of protection by compromising a network from multiple angles, and the failure of any single layer should not compromise the entire network:

| Layer | What It Covers |
|---|---|
| **Wireless signal security** | The network and RF spectrum should be monitored and managed to identify threats and awareness gaps. Wireless intrusion detection systems (WIDS) analyze and monitor the RF spectrum; Alarm generation systems (WIPS) help detect activities that violate the security policy of an organization and provide administrators the ability to detect and prevent network attacks. |
| **Connection security** | Per-frame/packet authentication provides protection against MITM attacks — traffic should stay within the trusted, authorized channel. |
| **Device security** | Both vulnerability and patch management are important components of overall device security posture. |
| **Data protection** | Encryption algorithms such as WPA2, WPA3, and AES protect data confidentiality. |
| **Network protection** | Strong authentication ensures that only authorized users can access the network. |
| **End-user protection** | Even if an attacker manages to associate with an AP, personal firewalls installed on end-user devices prevent the attacker from accessing files on the compromised device. |

## Defense Against WPA/WPA2/WPA3 Cracking

**Use Strong Passwords**
- Ensure the Wi-Fi password (pre-shared key) is strong, complex, and difficult to guess.
- Use a password at least **12–16 characters** long, including uppercase and lowercase letters, numbers, and special characters.

**Client Settings**
- Use WPA2 with **AES/CCMP** encryption only.
- Set proper client settings — validate the server, specify the server address, do not prompt for new servers.
- Regenerate keys for every new connection.

**Additional Controls**
- Use VPN technologies — remote access VPN, extranet VPN, intranet VPN.
- Implement protocols such as **IPsec** and **SSL/TLS** for secure communication.
- Implement a **network access control (NAC)** or **network access protection (NAP)** solution for additional control over end-user connectivity.

**Disable TKIP** in the router settings and ensure only AES encryption is used.

**MAC Address Filtering** — allow only devices with specific MAC addresses to connect.

**Upgrade to WPA3** — prevents exploitation of connected devices and offers better protection against brute-force attacks.

**Disable Remote Management** — turn off remote management features on routers to prevent external attacks.

**Disable WPS** — WPS has known vulnerabilities exploitable to gain network access. Turn off WPS in router settings to prevent brute-force attacks on the WPS PIN (this is the definitive fix for Reaver-class attacks in `09-wifi-encryption-cracking.md` — rate-limiting alone is not sufficient).

**Regularly Update Router Firmware** — keep firmware current with patches for known vulnerabilities; check the manufacturer's site regularly and apply updates promptly.

**Reduce Signal Range** — limit the Wi-Fi signal range to reduce the chances of unauthorized access from outside the premises; adjust transmission power and place the router centrally within the desired location.

**Monitor Network Activity** — regularly monitor for unusual activity or unauthorized devices using network monitoring tools.

**Enable WPA3-SAE** — provides stronger security by protecting against offline dictionary attacks and offering forward secrecy. Use it whenever devices support it.

**Disable Transition Mode** — WPA3's WPA2/WPA3 mixed mode is a potential security risk (see `03-wireless-encryption-wep-wpa-wpa2-wpa3.md` → *Transition mode weakness*). Disable it once all devices support WPA3.

## Defense Against KRACK Attacks

- Update all routers and Wi-Fi devices with the latest security patches.
- Turn on auto-updates for wireless devices and patch device firmware.
- Avoid using public Wi-Fi networks.
- Browse only secured (HTTPS) websites and don't access sensitive resources on an unprotected network.
- If there are IoT devices, audit them and don't connect them to insecure Wi-Fi routers.
- Always enable the **HTTPS Everywhere** browser extension.
- Enable **two-factor authentication**.
- Use a **VPN** to secure information in transit.
- Always use **WPA3** for wireless networks.
- Disable **fast roaming** and **repeater mode** on wireless devices to improve KRACK mitigation.
- Employ the **EAPOL-key replay counter** so the AP recognizes only the latest counter value (directly closes the nonce-reuse window KRACK exploits).
- Use a backup wired connection (Ethernet) or mobile data immediately when a KRACK vulnerability is detected.
- Employ alternative third-party routers instead of ISP-provided routers if the ISP router doesn't provide sufficient security patches.
- Use **network segmentation** to separate critical parts of a network from general user access, limiting the potential impact of a KRACK attack.
- **Temporarily disable 802.11r** (fast BSS transition), which is susceptible to KRACK — turn it off if seamless roaming isn't needed.
- Use **802.1X authentication** for an added layer of security; implement 802.1X with a RADIUS server for enterprise networks.

## Defense Against aLTEr Attacks

The foremost recommended method to defend against aLTEr attacks is to **encrypt DNS queries** with proper security standards. Cisco, in collaboration with Apple, developed an app called **"Cisco Security Connector"** that prevents clients from entering unintended websites — it encrypts DNS queries and loads them into **Cisco Umbrella** (an intelligence block) for further validation, protecting the network from hijacking at both the IP and DNS levels.

- Encrypt DNS queries and use only trusted DNS resolvers.
- Resolve DNS queries using the **HTTPS** protocol (DoH).
- Access only websites with HTTPS connections.
- Use **DNS over TLS (DoT)** or **DNS over DTLS** to encrypt DNS traffic and provide integrity protection.
- Implement **RFC 7858 / RFC 8310** to prevent DNS-spoofing attacks — also increases encryption and enables intelligent name-resolution policies.
- Add a **message authentication code (MAC)** to user-plane packets.
- Use the **DNSCrypt** protocol to authenticate communication between a DNS client and a DNS resolver.
- Use strong encryption algorithms such as **AES-256** to ensure all communications are encrypted end-to-end.
- Use **mutual authentication** mechanisms to verify the identity of both parties in the communication process.

## Detection and Blocking of Rogue APs

### Detection of Rogue APs
- **RF scanning**: re-purposed APs performing only packet capturing/analysis (RF sensors) are plugged in throughout the wired network to detect and warn the WLAN administrator about wireless devices operating in the area.
- **AP scanning**: APs that can detect neighboring APs operating in close proximity expose that data through their management information base (MIB) and web interface.
- **Wired side inputs**: network management software detects devices connected to the LAN — including via Telnet, SNMP, and Cisco Discovery Protocol (CDP) — using multiple protocols.
- **Comparison with authorized AP list**: maintain a list of authorized APs and compare it against detected APs to spot unauthorized devices. Tools such as **AirMagnet WiFi Analyzer** automate this comparison.
- **Signal strength analysis**: analyze detected APs' signal strength to identify ones that are physically close but unauthorized. Tools such as **Ekahau Survey for Wi-Fi Planning and Analysis** help identify unexpected APs by signal strength.
- **MAC address filtering**: monitor the network for known-authorized AP MAC addresses and flag unknown ones. **Cisco Wireless LAN Controllers** provide built-in rogue-AP detection and MAC-filtering features.

### Blocking of Rogue APs
- Deny wireless service to new clients by launching a **denial-of-service (DoS)** attack on the rogue AP itself (an aggressive but effective containment tactic used by enterprise WIPS).
- Block the switch port to which the rogue AP is connected, or manually locate the AP and physically remove it from the LAN.
- Use **WIPS** to continuously monitor the wireless spectrum for unauthorized devices and perform automated blocking actions.
- Use **access control lists (ACLs)** to restrict network access to known, authorized MAC addresses.
- Implement **802.1X authentication** to control network access and ensure only authenticated users/devices connect.
- **Segment** the network to isolate critical resources from general wireless access.
- Disable broadcasting of open SSIDs to reduce the risk of unauthorized connections.
- Maintain a **whitelist** of authorized MAC addresses and configure the wireless controller to block all others.

## Defense Against Wireless Attacks — Best Practices

### Best Practices for Configuration
- Change the default SSID after WLAN configuration.
- Set the router access password and enable firewall protection.
- Disable SSID broadcasts.
- Disable remote router login and wireless administration.
- Enable MAC address filtering on APs or routers.
- Enable encryption on APs and change passphrases often.
- Close all unused ports to prevent attacks on APs.
- Segregate the network to ensure guests aren't given access to the private network.
- Employ closed networks and hand the SSID directly to employees, rather than letting them select it from a broadcast list.
- Disable **DHCP** and rely on static IP addresses.
- Disable **SNMP**; if required, configure it to least-privilege settings.
- Change the router console's default IP address.
- Always use WPA3 encryption if supported; if not, use WPA2 with AES.
- Turn off **WPS** on the router.
- Use **VLANs** or separate SSIDs to segment different types of traffic.
- Adjust the router's transmission power to limit the Wi-Fi signal range to the required premises.
- Turn off services and close ports not needed for network operations.
- Use the router's built-in firewall to filter incoming and outgoing traffic.
- Set up a **separate guest network** for visitors with restricted access to main network resources.

### Best Practices for SSID Settings
- Use **SSID cloaking** to keep default wireless messages from broadcasting the SSID to everyone.
- Do not use the SSID, company name, network name, or any easy-to-guess string in passphrases.
- Place a firewall or packet filter between an AP and the corporate intranet.
- Limit the strength of the wireless network so it can't be detected outside the bounds of the organization.
- Regularly check wireless devices for configuration or setup problems.
- Implement an additional technique for encrypting traffic, such as **IPsec over wireless**.
- Modify the SSID with unique characters/strings instead of the manufacturer's default.
- Use a separate SSID for guest users to isolate them from the organizational network.
- Separate the organizational network into multiple zones with their own SSIDs to reduce the level of exploitation during attacks.
- Always keep the SSID broadcast of the organization's wireless devices in **hidden mode**.
- Ensure each SSID is protected with WPA3 encryption if supported, or WPA2 with AES as the minimum.
- Periodically change SSIDs and their associated passwords.

### Best Practices for Authentication
- Enable **WPA3** for the highest level of security — enhanced encryption and attack protection.
- If WPA3 isn't supported by the device, use **WPA2 with AES** encryption (avoid WPA or TKIP).
- Use **802.1X authentication** with a RADIUS server for enterprise networks — individual credentials per user.
- Where possible, implement **multifactor authentication** for an extra security layer.
- For 802.1X deployments, ensure proper management of digital certificates — strong encryption, regular renewal.
- Disable the network when it's not required.
- Place wireless APs in a secured (physically inaccessible) location.
- Keep drivers on all wireless equipment updated.
- Use a centralized server for authentication.
- Enable server verification on the client side using 802.1X authentication to prevent MITM attacks.
- Enable two-factor authentication as an added layer of defense.
- Deploy rogue-AP detection or wireless intrusion prevention/detection systems to prevent wireless attacks.

## Wireless Intrusion Prevention Systems (WIPS)

A **WIPS** is a network device that monitors the radio spectrum to detect APs (intrusion detection) without the host's permission, in nearby locations. It can also implement countermeasures automatically. WIPSs protect networks against wireless threats and give administrators the ability to detect and prevent various network attacks.

**Progression of detection sophistication** *(from the module's "wireless attacks and their prevention methods" chart)* — as a WIPS matures from basic honeypot detection toward full **client intrusion prevention** and **DoS attack detection**, it layers on: probing & network discovery → rogue identification & containment → impersonation detection & prevention → Wi-Fi traffic monitoring → location tracking → network intrusion detection — covering the full range from ASLEAP attacks and WEP cracks through MITM attacks, fake APs, MAC spoofing, and fake DHCP servers.

### WIPS Deployment (Cisco Model)

A WIPS consists of several components working together to provide a unified security-monitoring solution:

| Component | Function |
|---|---|
| **APs in monitor mode** | Provide constant channel scanning with attack detection and packet capture capabilities. |
| **Mobility services engine (running a wireless IPS service)** | The central point of alarm aggregation from all controllers and their respective wireless IPS monitor-mode APs. Alarm information and forensic files are archived here. |
| **Local mode AP(s)** | Provide wireless service to clients in addition to time-sliced rogue and location scanning. |
| **Wireless LAN controller(s)** | Forward attack information from wireless IPS monitor-mode APs to the MSE, and distribute configuration parameters to APs. |
| **Wireless control system** | Configures the wireless IPS service on the MSE, pushes IPS configurations to the controller, and sets APs into wireless IPS monitor mode. Also used for viewing IPS alarms, forensics, reporting, and accessing the threat encyclopedia. |

## Wi-Fi Security Auditing Tools

### Cisco Adaptive Wireless IPS
**Source:** https://www.cisco.com

Offers advanced network security for dedicated monitoring and detection of wireless network anomalies, unauthorized access, and RF attacks. Fully integrated with the Cisco Unified Wireless Network, delivering integrated visibility and control across the network without needing an overlay solution. Provides threat detection/mitigation against malicious attacks and security vulnerabilities, and gives security professionals the ability to detect, analyze, and identify wireless threats.

### Wi-Fi IPSs

**WatchGuard Wi-Fi Cloud WIPS** — https://www.watchguard.com
Defends your airspace from unauthorized devices, rogue APs, and malicious attacks, with near-zero false positives.

### Other Wi-Fi Security Auditing Tools
| Tool | Source |
|---|---|
| RFProtect | https://www.arubanetworks.com |
| Fern Wifi Cracker | https://github.com |
| OSWA-Assistant | https://securitystartshere.org |
| BoopSuite | https://github.com |
| Wifite | https://github.com |

### Additional WIPS Tools
| Tool | Source |
|---|---|
| Extreme AirDefense | https://www.extremenetworks.com |
| Arista WIPS | https://www.arista.com |
| SonicWall Wireless Network Manager | https://www.sonicwall.com |
| Cisco Meraki | https://www.cisco.com |
| FortiGate Next-Generation Firewall (NGFW) | https://www.fortinet.com |

---

## Module Summary

In this module, we discussed wireless network concepts, along with different types of wireless encryption technologies. We also discussed in detail various threats and the wireless hacking methodology comprising Wi-Fi discovery, wireless traffic analysis, the launch of wireless attacks, and Wi-Fi encryption cracking. This module also illustrated various wireless hacking tools. Additionally, we discussed various countermeasures to prevent wireless network attacks, and presented a detailed discussion on how to secure wireless networks using wireless security tools.

*(The next CEH module covers mobile hacking — how attackers and ethical hackers/pen-testers compromise mobile devices.)*

---
**Previous:** [`09-wifi-encryption-cracking.md`](09-wifi-encryption-cracking.md)
**Also see:** [`cheatsheet-commands.md`](cheatsheet-commands.md) and [`cheatsheet-tools-and-defense.md`](cheatsheet-tools-and-defense.md) for quick-reference versions of everything in this repository.
