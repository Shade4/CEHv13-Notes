# 05 — Securing Android Devices

> **Objective 2 (EC‑Council):** Explain Various Android OS Threats and Attacks — Part D (Defense)

## Table of Contents
- [5.1 Android Hardening Checklist](#51-android-hardening-checklist)
- [5.2 Android Security / Antivirus Tools](#52-android-security--antivirus-tools)
- [5.3 Android Device‑Tracking Tools](#53-android-device-tracking-tools)
- [5.4 Android Vulnerability Scanners](#54-android-vulnerability-scanners)
- [5.5 Static Analysis of an Android APK (MobSF)](#55-static-analysis-of-an-android-apk-mobsf)

---

## 5.1 Android Hardening Checklist

Grouped for readability (the source deck presents these as one long bullet list):

**Device access & auth**
- Enable a screen lock; use a strong PIN/password/pattern **and** biometrics (fingerprint/face).
- Enable **screen pinning** for securely handing a single app to someone else.
- Use a password manager (e.g., LastPass) instead of memorized/reused passwords.
- Disable SmartLock‑style "skip the password" conveniences and auto sign‑in.
- Enable **two‑factor/two‑step verification** on the device account and on any app accessible from it.

**Apps & updates**
- Install only from the official Play Store; **never root** the device.
- Never sideload APKs directly; read requested permissions before installing and check they match the app's stated purpose — read reviews/ratings too.
- Keep the OS and all apps updated; when buying a new phone, check the vendor's **security‑patch support window** in advance.
- Keep **Google Play Protect** active.
- Uninstall privacy‑invasive apps; block in‑app ad networks where possible.

**Data protection**
- Enable full‑device **encryption**.
- Install a reputable mobile antivirus (e.g., Kaspersky).
- Use a password/lock‑protector app (e.g., **AppLock**) for individual sensitive apps.
- Encrypt Internet traffic with a reputable VPN (e.g., ExpressVPN, VyprVPN).
- Back up contacts/documents to the cloud for fast recovery after an incident.
- Do not over‑share personal information when signing up for apps/services.

**Connectivity**
- Turn off **Wi‑Fi, Bluetooth, and NFC** when not actively in use.
- Turn off **USB debugging** when not in use (this is the exact setting PhoneSploit/ADB attacks in file 03 depend on).
- Restrict/avoid connecting to unfamiliar PCs or hardware for file transfer.
- Turn off "Visible Passwords" and "Use Secure Credentials" where not needed.

**Loss/theft preparedness**
- Enable GPS/location so the device can be located if lost or stolen.
- Set up **Google Find My Device** (or a third‑party equivalent like Lookout Life) for remote lock/wipe.
- If sharing a device with family, create **separate user accounts** to protect each person's privacy.
- Customize the lock screen with owner contact info to aid honest finders.

## 5.2 Android Security / Antivirus Tools

### Kaspersky (VPN & Antivirus for Android)
*Source: kaspersky.com*

A full mobile‑security suite: real‑time anti‑virus scanning, App Lock, Anti‑Theft (locate/lock/wipe), Anti‑Phishing, Safe Browsing, a bundled VPN, a Password Manager with a Password‑Safety checker, a **Data Leak Checker** (flags if your credentials appear in known breach dumps), a Smart‑Home network monitor, a Weak‑Settings scanner, and Call Filter (denylist spam/scam numbers).

### Other Cited Android Security Tools
| Tool | URL |
|---|---|
| Avira Security Antivirus & VPN | play.google.com |
| Avast Antivirus & Security | play.google.com |
| McAfee Security: Antivirus VPN | play.google.com |
| Lookout Mobile Security and Antivirus | play.google.com |
| Sophos Intercept X for Mobile | play.google.com |

## 5.3 Android Device‑Tracking Tools

### Google Find My Device
*Source: google.com*

Requirements for a lost device to be findable: powered on, signed into a Google Account, connected to mobile data/Wi‑Fi, visible on Google Play, **Location** turned on, and **Find My Device** turned on.

**Steps:**
1. Go to `https://www.google.com/android/find` and sign in.
2. If you have multiple devices, select the lost one at the top.
3. The device receives a silent notification; its approximate location (or last known location) appears on a map.
4. Choose an action:
 - **Play Sound** — rings at full volume for 5 minutes, even if set to silent/vibrate.
 - **Secure Device** — locks with your PIN/pattern/password (sets one if you don't have one); you can add a recovery message/phone number to the lock screen.
 - **Factory Reset Device** — permanently erases device data (may not clear an SD card); Find My Device stops working on it afterward.

### Other Cited Android Device‑Tracking Tools
| Tool | URL | Notes |
|---|---|---|
| Find My Phone | play.google.com | Location‑history timeline view |
| Where's My Droid | wheresmydroid.com | Text‑command tracking or web "Commander" console; supports **geofencing** with automatic "stolen" actions when the device leaves a defined area |
| Prey: Find My Phone & Security | play.google.com | — |
| Phone Tracker and GPS Location | play.google.com | — |
| Mobile Tracker for Android | play.google.com | — |
| Lost Phone Tracker | play.google.com | — |
| Phone Tracker By Number | play.google.com | — |

## 5.4 Android Vulnerability Scanners

### Quixxi App Shield
*Source: quixxi.com*

Enterprise app‑hardening platform for developers to protect apps from piracy, IP theft, data loss, hacking, and cracking. Its **multi‑layered encryption engine** guards against reverse engineering and tampering; the console exposes reverse‑engineering‑protection toggles, a class/method‑renaming obfuscator ("Protect and Rename Classes and methods"), and runtime app self‑protection.

### Other Cited Scanners
| Tool | URL |
|---|---|
| Android Exploits | play.google.com |
| ImmuniWeb® MobileSuite | immuniweb.com |
| Yaazhini | vegabird.com |
| Vulners Scanner | play.google.com |

## 5.5 Static Analysis of an Android APK (MobSF)

Security analysts examine a suspicious APK's code **without executing it**, either to find dangerous features/vulnerabilities directly, or to fingerprint it against known malware signatures.

### MobSF (Mobile Security Framework)
*Source: github.com/MobSF/Mobile-Security-Framework-MobSF*

Automates static **and** dynamic analysis across APK, XAPK, APPX, and IPA files; extracts permissions, browsable activities, signer certificates, and flags malicious behavior patterns.

**Run it locally:**
```bash
docker pull opensecurity/mobile-security-framework-mobsf
docker run -it -p 8000:8000 opensecurity/mobile-security-framework-mobsf
# browse to http://localhost:8000
```

**Steps (web UI or hosted instance at mobsf.live):**
1. Open MobSF, click **Upload & Analyze**, select the suspicious APK.
2. Review the dashboard: **App Score**, hash sums (MD5/SHA1/SHA256), exported activities/services/providers counts, permission list, and a **Static/Dynamic** toggle.
3. Click **PDF Report** / **Print Report** to export the complete analysis.

### Online Android Analyzers
| Tool | URL | Notes |
|---|---|---|
| Sixo Online APK Analyzer | sisik.eu | Decompiles binary XML + resources in‑browser |
| ShenmeApp | shenmeapp.com | — |
| KOODOUS | koodous.com | Community‑driven APK threat intel |
| Android APK Decompiler | javadecompilers.com | — |
| Hybrid Analysis | hybrid-analysis.com | Full sandboxed dynamic detonation report |
| DeGuard | apk-deguard.com | Statistical de‑obfuscator for ProGuard‑obfuscated APKs |

---
**Previous:** [`04-android-malware-and-tools.md`](04-android-malware-and-tools.md) | **Next:** [`06-ios-architecture-and-jailbreaking.md`](06-ios-architecture-and-jailbreaking.md)
