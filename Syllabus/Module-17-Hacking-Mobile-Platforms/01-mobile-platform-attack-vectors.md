# 01 — Mobile Platform Attack Vectors

> **Objective 1 (EC‑Council):** Explain Mobile Platform Attack Vectors

## Table of Contents
- [1.1 Vulnerable Areas in the Mobile Business Environment](#11-vulnerable-areas-in-the-mobile-business-environment)
- [1.2 OWASP Top 10 Mobile Risks — 2024](#12-owasp-top-10-mobile-risks--2024)
- [1.3 Anatomy of a Mobile Attack](#13-anatomy-of-a-mobile-attack)
- [1.4 How Attackers Profit from a Compromised Device](#14-how-attackers-profit-from-a-compromised-device)
- [1.5 Mobile Attack Vectors & Platform Vulnerabilities](#15-mobile-attack-vectors--platform-vulnerabilities)
- [1.6 Security Issues Arising from App Stores](#16-security-issues-arising-from-app-stores)
- [1.7 App Sandboxing Issues](#17-app-sandboxing-issues)
- [1.8 Mobile Spam & SMS Phishing (SMiShing)](#18-mobile-spam--sms-phishing-smishing)
- [1.9 Pairing on Open Bluetooth/Wi‑Fi — Bluesnarfing & Bluebugging](#19-pairing-on-open-bluetoothwi-fi--bluesnarfing--bluebugging)
- [1.10 Agent Smith Attack](#110-agent-smith-attack)
- [1.11 Exploiting the SS7 Vulnerability](#111-exploiting-the-ss7-vulnerability)
- [1.12 Simjacker](#112-simjacker)
- [1.13 Call Spoofing](#113-call-spoofing)
- [1.14 OTP / 2FA Hijacking](#114-otp--2fa-hijacking)
- [1.15 Camera / Microphone Capture Attacks](#115-camera--microphone-capture-attacks)

---

## 1.1 Vulnerable Areas in the Mobile Business Environment

*Source: ibm.com*

Smartphones sit at the intersection of **personal and corporate data**, and they connect through more channels than a traditional workstation: 3G/4G/5G, Bluetooth, Wi‑Fi, and wired USB. Every one of those channels is a potential point of interception. In a typical enterprise mobility topology, the vulnerable points are:

```
Mobile Device ── (Cellular) ──► Telco Service Provider ──► Internet ──► App Store / Website
Mobile Device ── (Bluetooth) ──► Peer device
Mobile Device ── (Wi‑Fi) ──► Wi‑Fi Access Point ──► Internet ──► Corporate VPN Gateway ──► Corporate Intranet
```

Each arrow above is a "vulnerable area" — data in transit that can be sniffed, redirected, or tampered with if the channel isn't authenticated and encrypted end‑to‑end.

## 1.2 OWASP Top 10 Mobile Risks — 2024

*Source: owasp.org*

| ID | Risk | What It Covers | Typical Exploitation |
|----|------|-----------------|------------------------|
| **M1** | Improper Credential Usage | Hardcoded credentials, plaintext storage/transmission of secrets, weak auth | Static analysis of the APK/IPA reveals API keys or passwords baked into the binary |
| **M2** | Inadequate Supply Chain Security | Outdated/flawed 3rd‑party SDKs & libraries, weak app‑signing/distribution | Attacker compromises a popular SDK or repackages a trusted app with malicious code |
| **M3** | Insecure Authentication/Authorization | Weak password policy, broken token handling, missing server‑side authorization checks | Replaying a low‑privilege token against a privileged API endpoint |
| **M4** | Insufficient Input/Output Validation | Missing sanitization of user/external input | SQLi, command injection, XSS inside a WebView |
| **M5** | Insecure Communication | Deprecated TLS versions, invalid/ignored certificates | MITM traffic interception on a shared Wi‑Fi |
| **M6** | Inadequate Privacy Controls | Poor handling of PII (names, addresses, financial data) | Data scraped from insecure local storage or over‑permissioned APIs |
| **M7** | Insufficient Binary Protections | No anti‑tamper / anti‑reverse‑engineering controls | `apktool`/Ghidra decompilation → patch → re‑sign → redistribute as a "cracked" or trojanized app |
| **M8** | Security Misconfiguration | Debug flags left on, default creds, excessive exported components | `adb shell dumpsys package <pkg>` reveals `debuggable="true"` in production |
| **M9** | Insecure Data Storage | Plaintext DBs, unsecured shared prefs, weak local encryption | Pulling `/data/data/<pkg>/databases/*.db` off a rooted device |
| **M10** | Insufficient Cryptography | Weak algorithms/short keys, custom crypto, bad key management | Recovering a hardcoded AES key from decompiled `smali` code |

> These replace the older 2016 "M1–M10" list you may see in some references; the naming/order was refreshed by OWASP in 2023–2024. The **Mobile Application Security Testing Guide (MASTG)** and **MASVS** (Mobile AppSec Verification Standard) are OWASP's companion standards for testing against this list — see file `10-mobile-security-guidelines-and-tools.md` for solutions mapped to each risk.

## 1.3 Anatomy of a Mobile Attack

*Source: nowsecure.com*

Attackers pivot through three "points" of the mobile ecosystem:

### Point 01 — The Device
- **Browser‑based:** Phishing, Framing (iFrame injection), Clickjacking (UI redress)
- **Phone/SMS‑based:** Baseband attacks, SMiShing
- **Application‑based:** Sensitive data storage, no/weak encryption, improper SSL validation, config manipulation, dynamic runtime injection, unintended permissions, escalated privileges, third‑party code, intent hijacking, zip‑directory traversal, side‑channel leaks
- **System‑based:** No/weak passcode, iOS jailbreaking, Android rooting, OS data caching, decryptable Keychain/KeyStore data, carrier‑loaded software, user‑initiated code

### Point 02 — The Network
- Wi‑Fi with weak/no encryption, rogue access points, packet sniffing (Wireshark, Capsa), MITM, session hijacking, DNS poisoning, SSLStrip, fake SSL certificates, BGP hijacking, malicious HTTP proxies

### Point 03 — The Data Center / Cloud
- **Web server:** platform vulnerabilities, server misconfiguration, XSS, CSRF, weak input validation, brute force, CORS misconfig, side‑channel, hypervisor attacks
- **Database:** SQL injection, privilege escalation, data dumping, OS command execution

```
                     ┌────────────┐     ┌─────────────┐     ┌────────────────────┐
                     │  THE DEVICE │ ──► │ THE NETWORK │ ──► │ DATA CENTER / CLOUD │
                     └────────────┘     └─────────────┘     └────────────────────┘
  Browser / SMS / App / OS attacks   Wi-Fi, MITM, DNS,      Web server + Database
                                     SSLStrip, rogue AP      attacks (XSS, SQLi...)
```

## 1.4 How Attackers Profit from a Compromised Device

*Source: sophos.com, securelist.com*

| Category | Examples |
|---|---|
| Surveillance | Camera, call logs, location, SMS messages |
| Financial data theft | Sending premium‑rate SMS, bank account details, stealing TANs, extortion via ransomware, fake antivirus, stealing card info, expensive international calls, cryptocurrency mining |
| Botnet activity | Launching DDoS, click fraud, using call logs/phone number, scanning networks/vulnerabilities |
| Impersonation | SMS redirection, sending emails, posting to social media, IMEI theft |
| Emerging targets | IoT/AI devices, smart appliances, personal health information |

## 1.5 Mobile Attack Vectors & Platform Vulnerabilities

| Category | Examples |
|---|---|
| Malware | Virus, rootkit, application/OS modification |
| Data exfiltration | Extracted from data streams and email, print‑screen/screen scraping, copy‑to‑personal‑cloud |
| Data tampering | Modification by another app, undetected tamper attempts, jailbroken device |
| Data loss | App vulnerabilities, unapproved physical access, loss of device/backup |

**Common mobile platform vulnerabilities & risks:**
Malicious apps in stores · mobile malware · app sandboxing vulnerabilities · weak device/app encryption · OS/app update issues · jailbreaking/rooting · mobile application vulnerabilities · privacy issues (geolocation) · weak data security · excessive permissions · weak communication security · physical attacks · insufficient code obfuscation · insufficient transport layer security · insufficient session expiration.

## 1.6 Security Issues Arising from App Stores

Official stores (Apple App Store, Google Play, Microsoft Store) vet apps; third‑party stores (Amazon Appstore, Samsung Galaxy Store, GetJar, APKMirror) may not. Attackers:

1. Download a legitimate app.
2. Repackage it with malware/a Trojan.
3. Upload it to a third‑party store or sideload it via social engineering.
4. The malicious app now exfiltrates call logs, photos, videos, and documents back to the attacker without the user's knowledge.

```
Attacker → drops malicious app → Third-Party App Store (no vetting) → Mobile User installs it
                                                                          │
                                                       Sends call logs/photos/videos/docs
                                                                          ▼
                                                                     Attacker
```

## 1.7 App Sandboxing Issues

Sandboxing is supposed to confine each app to its own private storage/resources so App A cannot read App B's data. A **vulnerable sandbox** lets a malicious app bypass this isolation to gain unrestricted access to other apps' data and the underlying OS — usually via an unpatched kernel/OS vulnerability, a misconfigured content provider, or an over‑broad permission grant.

## 1.8 Mobile Spam & SMS Phishing (SMiShing)

Mobile spam clutters inboxes with unsolicited ads and — worse — phishing lures ("Congratulations, you won a $2000 Walmart gift card...").

**SMiShing (SMS phishing):**
1. Attacker buys a prepaid SIM under a fake identity.
2. Sends an urgent/attractive SMS bait (lottery, gift card, "account suspended").
3. Victim clicks the link → redirected to a cloned phishing page.
4. Victim enters PII (name, phone, SSN, card number, CVV) → attacker harvests it.

**Why SMiShing works so well:** high SMS open rates, inherent trust in SMS, character limits that hide red flags, low security awareness compared to email, weaker on‑device protections, easy caller/sender‑ID spoofing, urgency‑driven messaging, direct tappable links, prevalent URL shorteners, and the general lack of SMS‑native anti‑phishing filters.

*(See `10-mobile-security-guidelines-and-tools.md §10.4` for the full SMS‑phishing countermeasure checklist.)*

## 1.9 Pairing on Open Bluetooth/Wi‑Fi — Bluesnarfing & Bluebugging

Leaving Bluetooth in "discoverable" mode or Wi‑Fi on auto‑join in public places exposes a device to:

- **Bluesnarfing** — theft of data (contacts, emails, SMS, photos, business data) over an open/discoverable Bluetooth connection, exploiting a vendor software flaw, without the owner's knowledge.
- **Bluebugging** — full remote *control* of the target device via Bluetooth: sniffing data, receiving/intercepting calls & SMS meant for the victim, forwarding calls, connecting to the internet, and accessing contacts/photos/videos — all while the device continues to appear to work normally for the owner.

## 1.10 Agent Smith Attack

1. Victim is lured (via third‑party stores like 9Apps) into installing a disguised malicious app (game, photo editor, fake "Google Updater").
2. The malware silently **replaces legitimate, already‑installed apps** (WhatsApp, SHAREit, MX Player) with infected look‑alike versions, using known Android patching vulnerabilities — without any user interaction.
3. Infected apps receive Command & Control (C2) instructions to flood the device with fraudulent ads for financial gain, and/or exfiltrate credentials and personal data.

## 1.11 Exploiting the SS7 Vulnerability

Signaling System 7 (SS7) is the decades‑old inter‑carrier protocol that lets networks route calls/SMS between operators. It was designed around **implicit trust between telecom operators**, with no per‑message authentication. An attacker who gains SS7 network access (via a compromised operator, a leased SS7 gateway, or an insider) can:
- Intercept calls and SMS (including OTPs) in a man‑in‑the-middle position
- Track a subscriber's real‑time location
- Redirect or block communications entirely

## 1.12 Simjacker

Simjacker abuses the **S@T Browser**, a legacy applet present on many SIM cards (part of the SIM Application Toolkit / STK), which most users have never heard of and cannot see or disable.

**Steps:**
1. Attacker sends a specially crafted **binary SMS** containing S@T Browser/STK instructions.
2. The SIM card's S@T Browser silently receives and executes the instructions — no user interaction, no visible SMS.
3. Injected code can retrieve **Cell‑ID and device location**, force calls, open a browser, or launch other STK commands.
4. An "accomplice device" (attacker‑controlled) receives the exfiltrated data via a follow‑up SMS.

```
Attacker ──(malicious SMS w/ STK code)──► Victim SIM (S@T Browser)
                                                  │ executes silently
                                                  ▼
                                    Accomplice Device ◄── Cell-ID + location via SMS
```

## 1.13 Call Spoofing

Manipulating Caller ID so the recipient sees a trusted number (bank, government agency) instead of the attacker's real number.

**Tools cited:**
| Tool | Notes |
|---|---|
| SpoofCard (`spoofcard.com`) | Virtual number calling/texting, voice changer, background noise, straight‑to‑voicemail, call recording to cloud |
| Fake Call (Play Store) | — |
| SpoofTel (`spooftel.com`) | — |
| Fake Call and SMS (Play Store) | — |
| Fake Caller ID (`fakecallerid.io`) | — |
| Phone Id – Fake Caller Buster (Play Store) | — |

## 1.14 OTP / 2FA Hijacking

**Path 1 — Attack on the telecom operator (SIM‑swap style):**
1. Attacker steals the victim's PII by bribing/tricking a mobile‑store employee or exploiting reused phone numbers.
2. Attacker social‑engineers the telecom operator ("I lost my phone") to transfer control of the victim's SIM.
3. OTPs now arrive on the attacker's device → attacker logs into the victim's online accounts.

**Path 2 — SIM‑jacking malware:** infects the SIM directly to intercept/read OTPs without operator involvement.

**Path 3 — Lock‑screen notification snooping:** OTPs previewed on a locked screen are read by an attacker with brief physical proximity (e.g., "let me make an emergency call").

**Tools cited:**
| Tool | Notes |
|---|---|
| AdvPhishing (GitHub) | Social‑media phishing tool that bypasses 2FA/OTP; runs on Linux/Termux; deployed via NGrok or localhost tunneling |
| mrphish (GitHub) | Bash‑based phishing script with port forwarding + OTP‑bypass control; works on rooted and non‑rooted Android |

*(Full countermeasures in `10-mobile-security-guidelines-and-tools.md §10.5`.)*

## 1.15 Camera / Microphone Capture Attacks

### Camfecting Attack
1. Attacker sends a phishing email/malicious link, or lures the victim to a malicious site.
2. Victim's click installs a Remote Access Trojan (RAT).
3. RAT gives the attacker live access to the camera/microphone (often disabling the camera LED to avoid detection) — capturing photos, video, audio, and location.

### Android Camera Hijack Attack
Exploits Android permission‑bypass bugs tied to `android.permission.CAMERA`, `RECORD_AUDIO`, `ACCESS_COARSE_LOCATION`, and `ACCESS_FINE_LOCATION`. Once a malicious app is sideloaded and a Trojan is dropped, a **persistent connection** survives even after the victim closes the app, letting the attacker capture photos/video at will — including, in some vulnerable versions, while the device is locked.

**Tool cited:** **StormBreaker** (GitHub) — social‑engineering toolkit that can access location, webcam, and microphone data without explicitly requesting the relevant permissions, by serving crafted HTML templates (camera/microphone/location capture pages) from a local server and tricking the victim into opening the link.

---
**Next:** [`02-android-architecture-and-rooting.md`](02-android-architecture-and-rooting.md)
