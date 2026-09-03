# CEH v13 — Module 17: Hacking Mobile Platforms

A complete, expanded study repository covering **CEH v13 Official Curricula — Module 17: Hacking Mobile Platforms** (Exam 312‑50, "Ethical Hacking and Countermeasures").

This repo turns the 186‑page courseware deck into a structured, GitHub‑flavored Markdown knowledge base: every attack technique, tool, command, and countermeasure from the source deck is documented in full, plus additional depth (lab setup, extra command flags, mechanism explanations, and cross‑references) that the slide deck itself only gestures at.

> ⚠️ **Legal & Ethical Use Only**
> Everything in this repository — tool names, commands, exploitation steps, and screenshots descriptions — is documented for **authorized penetration testing, CTFs, personal lab devices, and certification study (CEH/OSCP/mobile‑AppSec tracks)** only. Running any of these techniques against a device, app, account, or network you do not own or do not have **written authorization** to test is illegal in most jurisdictions (e.g., under the U.S. CFAA, UK Computer Misuse Act, and India's IT Act, 2000). Use a personal rooted/jailbroken test device, an emulator, or an intentionally‑vulnerable practice app (see [Lab Setup](#suggested-lab-setup) below).

---

## 📚 Module Map

| # | File | Objective Covered | Contents |
|---|------|--------------------|----------|
| 01 | [`01-mobile-platform-attack-vectors.md`](01-mobile-platform-attack-vectors.md) | Obj. 1 | OWASP Top 10 Mobile Risks (2024), anatomy of a mobile attack, attack vectors & platform vulnerabilities, app‑store/sandboxing issues, SMS/Bluetooth/SS7/Simjacker/OTP/camera attacks |
| 02 | [`02-android-architecture-and-rooting.md`](02-android-architecture-and-rooting.md) | Obj. 2 | Android OS architecture (6 layers), Device Administration API, rooting concepts & tools |
| 03 | [`03-hacking-android-devices.md`](03-hacking-android-devices.md) | Obj. 2 | drozer, FRP bypass, zANTI/Kali NetHunter, LOIC, Orbot, ADB/PhoneSploit, MITD, Spearphone, Metasploit, device analysis, SSL‑pinning bypass, Tap 'n Ghost |
| 04 | [`04-android-malware-and-tools.md`](04-android-malware-and-tools.md) | Obj. 2 | Android malware families, hacking toolkits, Android‑based sniffers |
| 05 | [`05-securing-android-devices.md`](05-securing-android-devices.md) | Obj. 2 | Countermeasures, security/AV tools, device‑tracking tools, vulnerability scanners, MobSF static analysis |
| 06 | [`06-ios-architecture-and-jailbreaking.md`](06-ios-architecture-and-jailbreaking.md) | Obj. 3 | iOS architecture (5 layers), jailbreaking types & techniques, jailbreak tools (Hexxa Plus walkthrough) |
| 07 | [`07-hacking-ios-devices.md`](07-hacking-ios-devices.md) | Obj. 3 | Spyzie, Trustjacking, SeaShell Framework, Cycript/method swizzling, Keychain Dumper, objection, device analysis, iOS malware, forensic tools |
| 08 | [`08-securing-ios-devices.md`](08-securing-ios-devices.md) | Obj. 3 | Full iOS hardening guide (Settings paths), iOS security tools, device‑tracking tools |
| 09 | [`09-mobile-device-management-and-byod.md`](09-mobile-device-management-and-byod.md) | Obj. 4 | MDM concepts & solutions, BYOD benefits/risks/policy/guidelines |
| 10 | [`10-mobile-security-guidelines-and-tools.md`](10-mobile-security-guidelines-and-tools.md) | Obj. 5 | OWASP risk↔solution matrix, platform‑security guidelines, SMS/OTP countermeasures, KeyStore/Keychain hardening, reverse engineering, source‑code/repackaging tools, mobile pentest toolkits |
| — | [`CHEATSHEET-COMMANDS.md`](CHEATSHEET-COMMANDS.md) | All | Every raw command in the module, grouped by tool, copy‑paste ready |
| — | [`CHEATSHEET-TOOLS-INDEX.md`](CHEATSHEET-TOOLS-INDEX.md) | All | Every named tool (150+) indexed by category with source URL and one‑line purpose |

---

## 🎯 Learning Objectives (per EC‑Council)

1. Explain Mobile Platform Attack Vectors
2. Explain Various Android OS Threats and Attacks
3. Explain Various iOS Threats and Attacks
4. Summarize Mobile Device Management (MDM) Concepts
5. Present Mobile Security Guidelines and Tools

## 🧭 How This Repo Is Organized

Each numbered file follows the same internal structure so you can jump straight to what you need:

- **Concept** — what the attack/technology is and why it matters
- **Mechanism** — how it actually works, step by step
- **Tool(s)** — the specific software EC‑Council cites, plus close substitutes
- **Commands** — copy‑paste command blocks, faithfully reproduced from the courseware and expanded with real flags/options from each tool's own docs
- **Countermeasures** — how to detect/prevent it (folded into the securing‑* files and file 10)

## 🧪 Suggested Lab Setup

You do not need real victim hardware to practice almost everything in this module. A safe, legal, fully self‑contained lab:

| Need | Free/Legal Option |
|---|---|
| Android target device | Android Studio AVD emulator, or Genymotion (rootable images) |
| Rooted Android device | Emulator + Magisk patched boot image, or a personal spare phone |
| Deliberately vulnerable Android app | [DIVA (Damn Insecure and Vulnerable App)](https://github.com/payatu/diva-android), [InsecureBankv2](https://github.com/dineshshetty/Android-InsecureBankv2), [OWASP MASTG‑Hacking‑Playground](https://github.com/OWASP/MASTG-Hacking-Playground) |
| iOS target device | Personal jailbroken spare iPhone, or cloud device rental (e.g., Corellium) — **the iOS Simulator cannot run real ARM binaries or be jailbroken** |
| Deliberately vulnerable iOS app | [iGoat‑Swift](https://github.com/OWASP/iGoat-Swift), [DVIA‑v2](https://github.com/prateek147/DVIA-v2) |
| Attack workstation | Kali Linux (bare‑metal or VM) with `adb`, `drozer`, `frida-tools`, `objection`, `apktool`, `mobsf` installed |
| Traffic interception | Burp Suite Community + device‑installed CA cert, or `mitmproxy` |
| Network sniffing | Wireshark (`rvictl` for iOS, standard interface for Android hotspot/AP mode) |

Install the core CLI tooling on the attack box:

```bash
# Core Android tooling
sudo apt update && sudo apt install -y android-tools-adb android-tools-fastboot apktool

# Python-based frameworks
pip3 install frida-tools objection --break-system-packages

# drozer (console + agent APK): https://github.com/WithSecureLabs/drozer
pip3 install drozer --break-system-packages

# Mobile Security Framework (MobSF) — static + dynamic analysis
docker pull opensecurity/mobile-security-framework-mobsf
docker run -it -p 8000:8000 opensecurity/mobile-security-framework-mobsf
```

## 🔗 Primary Sources Cited Throughout This Module

`owasp.org` · `developer.android.com` · `github.com` · `nowsecure.com` · `ibm.com` · `mas.owasp.org` · `frida.re` · `kali.org` · `zimperium.com` · `elcomsoft.com` · `cydiafree.com` · `broadcom.com` · `group-ib.com` · `malwarebytes.com` · `gdatasoftware.com` · `google.com` · `apple.com/support` · `scalefusion.com` · `manageengine.com` · `appdome.com` · `syhunt.com`

---

*Compiled from EC‑Council CEH v13 Official Curricula, Module 17 (pages 2581–2763), with additional explanatory depth, lab‑setup guidance, and consolidated command references added for study purposes.*
