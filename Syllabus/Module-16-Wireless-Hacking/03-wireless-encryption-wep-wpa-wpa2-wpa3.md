# 03 — Wireless Encryption: WEP, WPA, WPA2 & WPA3

> Objective 2 of the module: *Explain Different Wireless Encryption Algorithms*

## Table of Contents
- [Overview](#overview)
- [WEP — Wired Equivalent Privacy](#wep--wired-equivalent-privacy)
- [WPA — Wi-Fi Protected Access](#wpa--wi-fi-protected-access)
- [WPA2](#wpa2)
- [WPA3](#wpa3)
- [Comparison Table](#comparison-table)
- [Known Issues With Each Protocol](#known-issues-with-each-protocol)

---

## Overview

Wireless encryption protects the confidentiality of traffic between clients and access points by encrypting data before it's radiated over the air. Since WEP's introduction in 1997, four major generations of Wi-Fi encryption have shipped, each responding to cryptographic breaks found in its predecessor:

| Standard | Year / Standard | Core Algorithm | Status |
|---|---|---|---|
| **WEP** | 802.11 (1997) | RC4 stream cipher | Broken — crackable in minutes |
| **WPA** | 802.11i draft (2003) | RC4 + TKIP | Deprecated — multiple practical attacks |
| **WPA2** | 802.11i (2004) | AES-CCMP | Standard until 2018 — still widely deployed, vulnerable to KRACK |
| **WPA3** | Wi-Fi Alliance (2018) | AES-GCMP-256 + SAE | Current standard — has its own emerging issues |

Wireless networks are increasingly used everywhere: home, office, government agencies. Attackers who compromise weak encryption schemes gain the same access as a legitimate wired user, so understanding each protocol's mechanics (and cracks) is fundamental to both attacking and defending them. `802.11i` is the umbrella amendment that formally introduced the strong encryption mechanisms — WPA came first as a stopgap while 802.11i was finalized, then WPA2 implemented the full standard.

## WEP — Wired Equivalent Privacy

**What is WEP?** WEP is a security protocol defined by the 802.11 standard, designed to give a WLAN a level of security and privacy comparable to a wired LAN. It's a component of the IEEE 802.11 WLAN standards whose primary purpose is data confidentiality at a level equivalent to wired LANs (which rely on physical security to stop unauthorized access).

Because a WLAN user or attacker can access the network without physically connecting to the LAN, WEP encrypts data at the data-link layer using the symmetric **RC4** stream cipher to defend against this.

**Role of WEP in wireless communication:**
- Protects against eavesdropping on wireless communications.
- Attempts to prevent unauthorized network access.
- Depends on a secret key shared between a mobile station and an AP; this key encrypts packets before transmission, and an integrity check ensures packets aren't altered in transit. **802.11 WEP only encrypts the data between network clients — not the entire path.**

### How WEP Works *(Figure 16.10)*

```
WEP Key Store (K1, K2, K3, K4) ──► WEP Key ─┐
                                             ├──► WEP Seed ──► RC4 Cipher ──► Keystream ──┐
                                        IV ──┘                                             │
                                                                                            ▼
                              Data + ICV ──────────────────────────────────────► XOR Algorithm
                                 │                                                          │
                              CRC-32 Checksum (integrity check value, ICV)                  ▼
                                                                          IV | PAD | KID | Ciphertext
                                                                     (WEP-encrypted packet / frame body)
```

1. A **24-bit Initialization Vector (IV)** is prepended to a WEP key to generate the **WEP seed**.
2. The seed is fed to the **RC4** algorithm to generate a pseudo-random **keystream**.
3. A **32-bit Integrity Check Value (ICV)** is calculated over the plaintext data using **CRC-32**, and appended to it.
4. The keystream is **XORed** with (data + ICV) to produce the ciphertext.
5. The **IV** is added to the ciphertext, and the resulting frame is transmitted.

**Main advantages of WEP (as designed):**
- **Confidentiality** — prevents link-layer eavesdropping.
- **Access control** — determines the change of data by a third party.
- **Data integrity** — efficiency.

### Flaws of WEP

The basic flaws that undermine WEP's ability to protect against a serious attack:

- No defined method for encryption-key distribution.
  - Pre-shared keys (PSKs) are set once and rarely (if ever) changed.
  - RC4 was not designed for, and is not well suited to, the frequent re-keying WEP would need.
  - As the PSK is rarely changed, the same key is reused repeatedly.
- An attacker monitors the traffic and finds enough packets to work with (if ever) changed.
- With knowledge of the corresponding plaintext, an attacker can compute the key.
- Attackers analyze the traffic from data captured and crack WEP keys with the help of tools such as Aircrack-ng and WEPCrack.
- Key scheduling algorithms are also vulnerable.

### Deeper WEP Weaknesses (IV Analysis)

- **IV is a value used to randomize the keystream, and each packet has an IV value:** the standard IV allows only a 24-bit field — too small to be secure — and is sent in the *cleartext* portion of a message. All available IV values can be exhausted within hours at a busy AP (an AP broadcasting 1500-byte packets at 11 Mbps exhausts the entire IV space in about **five hours**). Because the IV is part of the RC4 encryption key, it's vulnerable to an analytical attack that recovers the key after intercepting and analyzing a relatively small amount of traffic. Identical keystreams result from IV reuse; wireless adapters from the same vendor may even generate the same IV sequence, letting attackers determine the keystream and decrypt ciphertext.
- **The standard does not require every packet to have a unique IV:** vendors use only a small part of the available 24-bit space, so a mechanism that depends on randomness isn't random at all.
- **RC4 was designed as a one-time cipher, not for reuse across multiple messages.**
- **All users share the same key**, and changing it requires reconfiguring every device on the network — discouraging frequent key changes.
- **No mechanism to prevent replay attacks** — attackers can retransmit captured packets.
- **CRC-32 is not a cryptographic hash function** and is vulnerable to bit-flipping attacks, where attackers modify the packet and adjust the checksum to match.
- **Even a 104-bit key length is insufficient** by modern cryptographic standards, making brute-force feasible.
- **WEP supports only one-way authentication** — the client authenticates to the AP, but the AP never authenticates to the client (no mutual authentication) — enabling rogue-AP attacks.
- **The FMS attack** (Fluhrer, Mantin, Shamir) exploits the weakness of RC4 key scheduling when IVs are reused, quickly recovering the WEP key via statistical analysis.

**Bottom line:** with ~24 GB of storage, an attacker can build a decryption table of reconstructed keystreams and decrypt WEP packets **in real time** without even needing the key. WEP should never be used today except in a lab specifically to practice cracking it (see `09-wifi-encryption-cracking.md`).

## WPA — Wi-Fi Protected Access

WPA is a security protocol defined by the 802.11i standard. In the past, the primary security mechanism between wireless APs and clients was WEP, whose static-key weakness could be exploited with freely available tools. IEEE defines WPA as "an expansion to the 802.11 protocols that can allow for increased security." Nearly every Wi-Fi manufacturer provides WPA.

WPA improves on WEP because messages pass through a **Message Integrity Check (MIC)** using the **Temporal Key Integrity Protocol (TKIP)**, which still uses the RC4 stream cipher but with **128-bit keys** and a **64-bit MIC**. WPA is an example of how 802.11i provides stronger encryption and enables **pre-shared key (PSK)** or **EAP** authentication. TKIP eliminates WEP's weaknesses by adding:
- Per-packet mixing functions
- Message integrity checks (MIC)
- Extended initialization vectors (IV)
- Re-keying mechanisms

WEP normally uses a 40-bit or 104-bit key, whereas TKIP uses 128-bit keys per packet. The MIC prevents an attacker from changing or resending packets.

### TKIP Details
- Uses a **unicast encryption key that changes for every packet** — automatically coordinated between client and AP.
- Uses a **Michael Integrity Check** algorithm with an MIC key to generate the MIC value.
- Uses RC4 with 128-bit keys and a 64-bit MIC integrity check.
- Mitigates vulnerability by increasing IV size and using mixing functions.
- Under TKIP, the client starts with a **128-bit temporal key (TK)**, combined with the client's MAC address and an IV to create a keystream that encrypts data via RC4.
- Implements a **sequence counter** to protect against replay attacks.
- Enhances WEP by adding a **rekeying mechanism** for fresh encryption/integrity keys — TKs change **every 10,000 packets**, resisting cryptanalytic attacks that rely on key reuse.

### Temporal Keys (TKs) and the 4-Way Handshake

All newly deployed Wi-Fi equipment uses either TKIP (WPA) or AES (WPA2) to secure the WLAN. In WEP, encryption keys (TKs) are derived from the pairwise master key (PMK) created during the EAP authentication session — but in WPA and WPA2, the encryption keys come from a **four-way handshake**. In the EAP success message, the PMK is sent to the AP but not to the Wi-Fi client, because the client has already derived its own copy of the PMK.

**4-Way Handshake operational flow** *(Figure 16.11)*:
1. **AP → Client:** sends an **ANonce**; the client uses it (with the PMK) to construct the **Pairwise Transient Key (PTK)**.
2. **Client → AP:** responds with its own **SNonce**, together with a **MIC**.
3. **AP → Client:** sends the **Group Temporal Key (GTK)** and a sequence number, together with another MIC — used for subsequent broadcast frames.
4. **Client → AP:** confirms the temporal keys are installed ("OK, use").

> **Why this matters for attackers:** this exact 4-way exchange is what `aircrack-ng`/`hashcat` need captured in a `.cap` file to attempt an offline dictionary/brute-force attack (see `09-wifi-encryption-cracking.md`). It's also the exchange that **KRACK** (Key Reinstallation Attack) exploits by forcing nonce reuse (see `08-rogue-ap-evil-twin-krack-advanced-attacks.md`).

## WPA2

Wi-Fi Protected Access 2 (WPA2) is a security protocol used to safeguard wireless networks; it **replaced WPA in 2006**. It's compatible with the 802.11i standard and supports many security features WPA lacks. WPA2 introduces the **NIST FIPS 140-2-compliant AES** encryption algorithm — a strong wireless encryption algorithm — and the **Counter Mode Cipher Block Chaining Message Authentication Code Protocol (CCMP)**. It provides stronger data protection and network access control than WPA, giving a high level of security so only authorized users can access the network.

### How WPA2 Works *(Figure 16.13)*
During WPA2 implementation, additional authentication and encryption included in the AES and CCMP algorithms are used. Consequently, the transmission encryption portion of a frame is protected before it's transmitted. The protocol uses a sequenced packet number (PN) and the header to generate a Nonce that, along with data, ANonce, and PN, are used as inputs for the CCMP algorithm. A PN is included in the CCMP header to prevent replay attacks. The resultant packet is protected with both AES and CCMP algorithms produced. Finally, the assembled MAC header, data, encrypted data, and encrypted MIC form the WPA2 MAC frame.

### Modes of Operation

| Mode | Description |
|---|---|
| **WPA2-Personal** | Uses a set-up password (pre-shared key, PSK) to protect against unauthorized network access. Each wireless device encrypts network traffic using a **128-bit key** derived from a passphrase of **8 to 63 ASCII characters**. The router combines the passphrase, network SSID, and TKIP to generate a unique encryption key per client; these keys change continually. |
| **WPA2-Enterprise** | Uses EAP or RADIUS for centralized client authentication with multiple authentication methods (token cards, Kerberos, certificates). Assigns a unique ciphered key to every system, hidden from the user, to provide additional security and prevent key sharing. Users are allocated login credentials by a centralized server that they present when connecting. |

## WPA3

Wi-Fi Protected Access 3 (WPA3) was announced by the Wi-Fi Alliance in **January 2018** as an advanced implementation of WPA2 providing trailblazing protocols and using the **AES-GCMP 256** encryption algorithm. It ensures cryptographic consistency and provides network resilience through **Protected Management Frames (PMF)**, delivering high-level protection against eavesdropping and forging attacks. WPA3 also disallows outdated legacy protocols.

### Modes of Operation

**WPA3-Personal**
Mainly delivers password-based authentication using **SAE** (Simultaneous Authentication of Equals), also known as the **Dragonfly Key Exchange**, replacing the PSK concept from WPA2-Personal.
- **Resistance to offline dictionary attacks** — prevents passive password attacks such as brute-forcing.
- **Resistance to key recovery** — even once a password is determined, it's impossible to capture and determine session keys while maintaining forward secrecy of network traffic.
- **Natural password choice** — allows users to choose weak or popular phrases as passwords, which are easy to remember, without the same offline-cracking downside WPA2 had.
- **Easy accessibility** — provides greater protection than WPA2 without changing the methods users already use to connect.

**WPA3-Enterprise**
Based on WPA2 but offers better security across the network, protecting sensitive data using several cryptographic concepts and tools:
- **Authenticated encryption** — maintains authenticity/confidentiality of data using the **256-bit Galois/Counter Mode Protocol (GCMP-256)**.
- **Key derivation and validation** — generates a cryptographic key from a password/master key using **384-bit HMAC with SHA (HMAC-SHA-384)**.
- **Key establishment and verification** — exchanges cryptographic keys between two parties using **Elliptic Curve Diffie-Hellman (ECDH)** and **Elliptic Curve Digital Signature Algorithm (ECDSA)** with a 384-bit elliptic curve.
- **Frame protection and robust administration** — uses **256-bit Broadcast/Multicast Integrity Protocol Galois Message Authentication Code (BIP-GMAC-256)**.

### Enhancements in WPA3 vs. WPA2

WPA3 implements a layered security strategy protecting all aspects of a Wi-Fi network, via a certification program specifying the standards a product must support. The **Dragonfly handshake/SAE protocol is mandatory for WPA3 certification**.

1. **Secured handshake** — SAE (Dragonfly handshake) makes a password resistant to dictionary and brute-force attacks, preventing offline decryption of data.
2. **Wi-Fi Easy Connect** — simplifies security configuration by managing different interface connections in a network from one interface using the **Wi-Fi Device Provisioning Protocol (DPP)**; lets many smart/IoT devices join a network via a QR code or password.
3. **Unauthenticated encryption** — uses **Opportunistic Wireless Encryption (OWE)**, replacing 802.11 "open" authentication with better protection on public hotspots/networks.
4. **Bigger session keys** — WPA3-Enterprise supports key sizes of **192 bits or higher**, difficult to crack.

## Comparison Table

*(Table 16.2 — Comparison of WEP, WPA, WPA2, and WPA3, reproduced exactly)*

| Encryption | Encryption Algorithm | IV Size | Encryption Key Length | Key Management | Integrity Check Mechanism |
|---|---|---|---|---|---|
| **WEP** | RC4 | 24-bits | 40/104-bits | None | CRC-32 |
| **WPA** | RC4, TKIP | 48-bits | 128-bits | 4-way handshake | Michael algorithm and CRC-32 |
| **WPA2** | AES-CCMP | 48-bits | 128-bits | 4-way handshake | CBC-MAC |
| **WPA3** | AES-GCMP 256 | Arbitrary length 1 – 2⁶⁴ | 192-bits | ECDH and ECDSA | BIP-GMAC-256 |

**Bottom-line ratings from the module:**

| Protocol | Verdict |
|---|---|
| WEP, WPA | ❌ Should be replaced with more secure WPA2 and WPA3 |
| WPA2 | ✅ Incorporates protection against forgery and replay attacks |
| WPA3 | ✅ Provides enhanced password protection and secured IoT connections; encompasses stronger encryption techniques |

## Known Issues With Each Protocol

*(Summary slide + full detail, reproduced from the module)*

### Issues with WEP
- CRC-32 does not ensure complete cryptographic integrity.
- IVs are 24 bits and sent in cleartext.
- Vulnerable to known-plaintext attacks.
- Prone to password-cracking attacks.
- Associate/disassociate messages are not authenticated.
- Attacker can easily construct a decryption table of reconstructed keystreams.
- Lack of centralized key management.
- IV is part of the RC4 encryption key, leading to an analytical attack.

### Issues with WPA
- Pre-shared key is vulnerable to eavesdropping and dictionary attacks.
- Lack of forward secrecy.
- WPA-TKIP is vulnerable to packet spoofing and decryption attacks.
- Insecure random number generator (RNG) in WPA allows attackers to discover the **GTK** generated by the AP.
- Vulnerabilities in TKIP allow attackers to guess the IP address of the subnet and inject small packets into the network to downgrade performance.

### Issues with WPA2
- Pre-shared key is vulnerable to eavesdropping and dictionary attacks.
- Lack of forward secrecy — if an attacker captures a PSK, they can decrypt **all** packets encrypted with that key.
- **Hole96 vulnerability** makes WPA2 vulnerable to MITM and DoS attacks by exploiting a shared group temporal key (GTK).
- Insecure RNG in WPA2 allows attackers to discover the GTK generated by the AP.
- **KRACK vulnerabilities** — a significant exploit (key reinstallation attack) that may allow attackers to sniff packets, hijack connections, inject malware, and decrypt packets.
- Vulnerability to wireless DoS attacks by exploiting the WPA2 replay-attack detection feature (sending forged group-addressed data frames with a large PN).
- Insecure WPS PIN recovery — disabling WPA2/WPS can be time-consuming, and when both are enabled, an attacker can disclose the WPA2 key by determining the WPS PIN through simple steps (see `09-wifi-encryption-cracking.md` → *Cracking WPS Using Reaver*).

### Issues with WPA3
- WPA3 uses more complex encryption algorithms, demanding more processing power from devices.
- **SAE vulnerable to timing attacks** — certain implementations of SAE (Dragonfly) have been found vulnerable to timing attacks that can potentially recover the password.
- **Cache-based side-channel attacks** — extracting sensitive information from cache access patterns, potentially revealing details of cryptographic operations and leading to recovery of secure data.
- Configuration errors (weak passwords, poor network setup) can leave WPA3 networks vulnerable despite its advanced protections.
- **Limited adoption** — many devices/infrastructure still use WPA2, limiting WPA3's overall effectiveness across networks.
- **Resource intensive** — can affect performance of older devices with limited compute.
- **Transition mode weakness** — WPA3 supports a "transition mode" for compatibility with WPA2-only devices; both protocols are enabled simultaneously, and attackers can exploit the less-secure WPA2 side (including KRACK) to attack the network, weakening the overall security posture.
- **Hardware requirements** — needs updated hardware to fully support new features; upgrading can be costly.

> These four issue categories — **Dragondrain, Dragontime, and Dragonforce** (collectively "**Dragonblood**") — are the publicly known family of vulnerabilities against the SAE/Dragonfly handshake referenced by the timing and side-channel attack classes above. They're covered in practical terms in `09-wifi-encryption-cracking.md` → *WPA3 Encryption Cracking*.

---
**Previous:** [`02-wireless-standards-topologies-antennas.md`](02-wireless-standards-topologies-antennas.md)
**Next:** [`04-wireless-threats.md`](04-wireless-threats.md) — the full wireless threat taxonomy.
