# 10 — Mobile Security Guidelines & Tools

> **Objective 5 (EC‑Council):** Present Mobile Security Guidelines and Tools

## Table of Contents
- [10.1 OWASP Top 10 Mobile Risks → Solutions Matrix](#101-owasp-top-10-mobile-risks--solutions-matrix)
- [10.2 General Guidelines for Mobile Platform Security](#102-general-guidelines-for-mobile-platform-security)
- [10.3 Mobile Device Security Guidelines for the Administrator](#103-mobile-device-security-guidelines-for-the-administrator)
- [10.4 SMS Phishing Countermeasures](#104-sms-phishing-countermeasures)
- [10.5 OTP Hijacking Countermeasures](#105-otp-hijacking-countermeasures)
- [10.6 Critical Data Storage: KeyStore & Keychain Recommendations](#106-critical-data-storage-keystore--keychain-recommendations)
- [10.7 Reverse Engineering Mobile Applications](#107-reverse-engineering-mobile-applications)
- [10.8 Source Code Analysis Tools](#108-source-code-analysis-tools)
- [10.9 Reverse Engineering Tools](#109-reverse-engineering-tools)
- [10.10 App Repackaging Detectors](#1010-app-repackaging-detectors)
- [10.11 Mobile Protection & Anti‑Spyware Tools](#1011-mobile-protection--anti-spyware-tools)
- [10.12 Mobile Penetration‑Testing Toolkits](#1012-mobile-penetration-testing-toolkits)

---

## 10.1 OWASP Top 10 Mobile Risks → Solutions Matrix

*Source: owasp.org* — this maps directly onto the risk list from file 01 §1.2.

| Risk | Solutions |
|---|---|
| **M1 – Improper Credential Usage** | Avoid hardcoded credentials · encrypt credentials in transit · use revocable access tokens instead of storing user credentials on device · implement strong auth protocols · rotate API keys/tokens regularly |
| **M2 – Inadequate Supply Chain Security** | Secure coding practices + code review + testing during development · ensure secure app signing/distribution · use only trusted, validated third‑party libraries · apply security protocols for updates/patches/releases · monitor for supply‑chain incidents via security scanning |
| **M3 – Insecure Authentication/Authorization** | Avoid weak authentication design patterns · reinforce server‑side authorization (never trust the client) |
| **M4 – Insufficient Input/Output Validation** | Implement strict input/output validation · use data‑integrity checks and secure coding practices |
| **M5 – Insecure Communication** | Use certificates signed by a trusted CA · ensure certificate validity checks **fail closed** (reject on failure, not silently allow) |
| **M6 – Inadequate Privacy Controls** | Handle PII with proper consent/controls · use static **and** dynamic security‑checking tools |
| **M7 – Insufficient Binary Protections** | Code obfuscation + anti‑tampering techniques · local security checks + backend enforcement + integrity checks |
| **M8 – Security Misconfiguration** | Never ship hardcoded default credentials · disable debugging features in production builds · request only the permissions the app actually needs · disallow cleartext traffic; use certificate pinning where feasible · disable Android backup mode · minimize exported activities/providers/services to only what's required |
| **M9 – Insecure Data Storage** | Store sensitive data only in secure, restricted‑access locations · keep all libraries/frameworks/third‑party dependencies patched |
| **M10 – Insufficient Cryptography** | Use strong encryption with sufficient key length · use strong hash functions (SHA‑256, bcrypt) with salting · use key‑derivation functions (PBKDF2, bcrypt, scrypt) for password hashing |

## 10.2 General Guidelines for Mobile Platform Security

**Application hygiene**
- Don't over‑install apps; disable auto‑upload of photos to social networks.
- Perform a security assessment of the application architecture before deployment.
- Maintain configuration control and management.
- Install only from trusted application stores.
- Securely wipe/delete data before disposing of a device.

**Connectivity hygiene**
- Don't share information inside GPS‑enabled apps unless necessary.
- Never run two separate radios (Wi‑Fi *and* Bluetooth) simultaneously if avoidable.
- Disable Wi‑Fi/Bluetooth (and tethering) entirely when not in use — Bluetooth off by default, on only when needed.

**Passcode / lockout**
- Configure the longest practical passcode; consider an 8‑character complex passcode.
- Set an idle auto‑lock timeout.
- Enable lockout/wipe after a defined number of failed attempts ("erase data: ON").

**OS & patching**
- Keep OS and apps updated; apply releases promptly; perform regular maintenance.

**Enterprise remote management**
- Use MDM to secure/monitor/manage/support the fleet.
- Never allow rooting/jailbreaking — bake detection/prevention into your MDM policy.
- Use remote‑wipe services (Find My Device / Find My iPhone) and immediately report loss to IT so certificates/access can be revoked.

**Storage & backup**
- Use hardware‑backed device encryption where supported; encrypt backups too.
- Use secure, over‑the‑air backup with periodic sync; (Android) back up to your Google account rather than an uncontrolled third‑party cloud; encrypt and control backup location.
- Keep sensitive data off shared devices; limit on‑device logging.
- Use a secure data‑transfer utility or encrypt data in transit.

**Email & app policy**
- Filter email forwarding at the server; use commercial DLP filters; prevent local email caching.
- Allow only **signed applications** to install/execute; sandbox apps and data.
- Set auto‑lock ≤ 1 minute; think through the privacy implications before enabling location‑based services, and limit them to trusted apps.
- Disable notification previews on the lock screen for apps that could show sensitive data.
- Disable diagnostics/usage‑data collection (`Settings → General → About`, iOS example).

**Organizational controls**
- Harden browser permission rules to company policy.
- Design/implement a formal mobile‑device policy defining accepted usage, support levels, and information‑access permissions per device type.
- Control devices/apps; prohibit USB keys; manage OS/app environments centrally.
- Lock the device (power button) whenever stepping away; verify printer location before printing sensitive documents.
- Use enterprise file‑sharing solutions (e.g., Citrix‑style "follow‑me‑data"/ShareFile) instead of local storage of sensitive data.
- Prefer cellular data over public Wi‑Fi; deploy anti‑malware; enforce MFA; log off apps after use; use TLS for all comms and discourage plain public Wi‑Fi without a VPN.

## 10.3 Mobile Device Security Guidelines for the Administrator

- Publish enterprise policy covering acceptable use of consumer‑grade/BYOD devices, **and** a separate policy for cloud usage.
- Enable data‑center‑side anti‑virus; define exactly what app/data access levels are allowed vs. prohibited on consumer‑grade devices.
- Specify a **session timeout** through the Access Gateway, and whether the domain password may be cached on‑device or must be re‑entered every access.
- Choose Access Gateway authentication methods: **No authentication / Domain only / SMS authentication / RSA SecurID only / Domain + RSA SecurID**.
- Maintain a formal mobile‑device security policy (allowed resources, allowed device types, access privileges) and system **threat models** for the devices/resources involved.
- Pre‑configure all required security settings before issuing a device to a user.
- Keep OS/apps current, synchronize device clocks to a common time source, reconfigure access privileges as roles change, and document infrastructure abnormalities.
- Regularly audit whether users are actually following the policy.
- Evaluate vendor/service‑provider options against your environment before committing; pilot‑test solutions (auth, functionality, security, connectivity, performance) before production rollout.
- Restrict open public Wi‑Fi access via a management console.
- Adopt **Unified Endpoint Management (UEM)** to fold EMM + **Mobile Application Management (MAM)** into a single console across all endpoint types.
- Deploy **Mobile Threat Defense (MTD)** platforms for behavior‑based threat detection.
- Use biometrics (fingerprint/voice/facial/iris) wherever supported.
- Add a **Cloud Access Security Broker (CASB)** as an extra control layer between cloud users and providers.
- Standardize endpoint‑security rules with alerting on detected risk.
- Enforce application‑protection + DLP policy to prevent local storage of company data on devices.
- Securely erase data before decommissioning/reassigning a device.
- Establish and enforce standard configurations, disabling unnecessary services/features by default.

## 10.4 SMS Phishing Countermeasures

- Never reply to a suspicious SMS without independently verifying the sender.
- Never click links in an unsolicited SMS; never call a number left in one.
- Never share personal/financial information via SMS reply.
- Check your bank's actual policy on sending SMS (many banks never send links).
- Enable your carrier's "block texts from the internet" feature.
- Treat any SMS pressuring you to *act immediately* as a red flag.
- Don't fall for unexpected "you've won" scams/gifts/offers.
- Be wary of messages from non‑telephonic numbers (internet text‑relay services conceal sender identity this way).
- Watch for spelling/grammar/language inconsistencies.
- Reject subscription/sign‑up prompts from unknown third‑party vendors.
- Never store confidential data (card numbers, PINs, passwords) on the phone itself.
- Report fraudulent SMS to reduce future attacks; install anti‑phishing/SMS‑filtering software; keep anti‑malware current.
- Implement **MFA** as a backstop even if a phishing message succeeds.
- (Organizations) use official registered short codes to improve message legitimacy; maintain a smishing incident‑response plan distributed to BYOD users; run periodic phishing simulations; standardize on authenticated messaging platforms (Signal, WhatsApp) for internal comms; run ongoing smishing‑awareness training.

## 10.5 OTP Hijacking Countermeasures

**For users:**
- Follow strong password hygiene: unique passwords per service, periodic rotation, encrypted password‑manager storage.
- Keep OS/software updated; stay alert to suspicious emails/links.
- Only interact with SSL‑certified sites.
- Enable **SIM PIN locking** to block unauthorized SIM (re)use.
- Disable sensitive lock‑screen notification previews.
- Avoid apps that authenticate purely via SMS where a stronger option exists.
- Minimize SMS/email‑based account‑recovery methods.
- Never forward an OTP to anyone, and never read/type it aloud while on a call; always enter it manually yourself.

**For developers:**
- Transmit OTPs only over secure channels (encrypted SMS, secure push) with end‑to‑end encryption.
- Combine OTP with a second factor (biometric or hardware‑based).
- Rate‑limit OTP requests per user to blunt brute‑force attempts; set short OTP expiry windows.
- Apply behavioral analytics to catch bursts of OTP requests.
- Educate users against sharing OTPs (in‑app messaging at the point of entry).
- Support hardware OTP generators/security keys as an alternative.
- Use standard, vetted algorithms — **HOTP** (HMAC‑based) or **TOTP** (time‑based) — and ensure every OTP is unique and single‑use, never reused.

## 10.6 Critical Data Storage: KeyStore & Keychain Recommendations

| Android (KeyStore) | iOS (Keychain) |
|---|---|
| Gate keys behind patterns/PINs/passwords/fingerprints | Gate the keychain behind Touch ID/Face ID/passcode/password |
| Use a **hardware‑backed** Android KeyStore | Use hardware‑backed **256‑bit AES** encryption |
| Store data in a non‑readable (encrypted) format | Use **ACLs** to control which apps can access which keychain items |
| Implement authorization checks on key creation/import | Store only small chunks of data directly in the keychain |
| Ensure server‑side keys require proper authentication to access | Specify `AccessControlFlags` to gate key use |
| Keep the master key and other keys in separate locations | Erase keychain data when an app is uninstalled |
| Derive keys from a user‑supplied passphrase | Encrypt data shared between a main app and its extensions |
| Store the master key in KeyStore's software implementation if no hardware backing exists | Follow secure coding practice (prevent buffer overflows, injection) |
| Encrypt `SharedPreferences` values for defense in depth | Secure inter‑process communication (IPC) between apps/extensions |
| Follow least privilege — only authorized components get access to sensitive data | Vet any cloud storage provider for encryption + secure data‑handling policies before use |
| Never hardcode API keys/tokens/credentials in source | — |
| Obfuscate code/data to raise the reverse‑engineering bar | — |
| Encrypt all data in transit with TLS | — |
| Secure content‑provider‑based data sharing with proper permissions | — |

## 10.7 Reverse Engineering Mobile Applications

**What it's used for:** reading/understanding source code, detecting vulnerabilities, scanning for embedded secrets, conducting malware analysis, and regenerating an app after modification (also used maliciously to clone apps).

**Why it matters for both attackers and defenders:**
- **Security analysis** — vulnerability discovery (insecure storage, weak auth, unpatched flaws), malware‑behavior analysis, and understanding client↔backend communication protocols.
- **Black‑box testing enablement** — many apps' end‑to‑end encryption, SSL, and root‑detection actively resist dynamic analysis; reverse engineering is what neutralizes those defenses so testing can proceed at all.
- **Static analysis in black‑box testing** — comprehending binary/bytecode design without running the app, including finding hardcoded credentials.
- **Resilience assessment** — validating anti‑reversing controls (e.g., **OWASP MASVS‑R**) actually hold up under a real reverse‑engineering attempt.
- **Compliance & auditing** — verifying an app meets regulatory obligations (GDPR, HIPAA), and auditing third‑party/vendor components for known‑vulnerable or non‑compliant code.
- Also used to check cross‑platform compatibility, debug/fix bugs, and detect patent/copyright infringement.

## 10.8 Source Code Analysis Tools

### Syhunt Mobile
*Source: syhunt.com*

Scans Java/Android source (**350+** vulnerability checks) and Swift/Objective‑C/C for iOS (**19 categories, 240+** checks); automates OWASP Mobile Top 10 scanning for publishers, developers, and QA.

### Other Cited Source‑Code Analysis Tools
| Tool | URL |
|---|---|
| Android lint | android.com |
| Zimperium's z3A | zimperium.com |
| Appium | appium.io |
| Selendroid | selendroid.io |
| Infer | fbinfer.com |

## 10.9 Reverse Engineering Tools

### Apktool
*Source: apktool.org*

```bash
apktool d test.apk     # decompile: resources decoded near-original, project-like layout
apktool b test         # rebuild: repackage the (possibly modified) project back to APK/JAR
```
Also handles: disassembling resources close to original form, rebuilding decoded resources to binary APK/JAR, organizing/handling framework‑dependent APKs, and **smali** debugging.

### Other Cited Reverse‑Engineering Tools
| Tool | URL |
|---|---|
| Androguard | github.com |
| Frida | frida.re |
| JEB | pnfsoftware.com |
| APK Editor Studio | github.com |
| Bytecode Viewer | github.com |

## 10.10 App Repackaging Detectors

**Repackaging** = extracting a legitimate app from an official store, injecting malicious code, and redistributing it as if it were the authentic app (frequently the end goal of the reverse‑engineering workflow above).

### Appdome
*Source: appdome.com*

A mobile RASP (Runtime Application Self‑Protection) platform defending against tampering, reverse engineering, method hooking, and unauthorized repackaging — **without requiring source‑code changes**. Its **integrity/checksum validation** feature fingerprints an app's binary structure so any unauthorized modification (including a repackage) is detectable.

### Other Cited App‑Repackaging Detectors
| Tool | URL |
|---|---|
| freeRASP for Android/iOS | github.com |
| wultra | wultra.com |
| iXGuard | guardsquare.com |
| AndroCompare | github.com |
| FSquaDRA 2 | github.com |

## 10.11 Mobile Protection & Anti‑Spyware Tools

| Tool | Source | Highlights |
|---|---|---|
| **Avast Antivirus & Security** | play.google.com | Automated scans, blocks malicious apps pre‑install, verifies Wi‑Fi network safety |
| **Comodo Mobile Security** | comodo.com | High‑performance malware engine, VPN, ID protection, safe browsing, AppLock, SD‑card protection, cloud scanning |
| **AVG Mobile Security** | avg.com | Public‑Wi‑Fi safety detection, credential‑leak monitoring across online databases |
| **TotalAV** | totalav.com | Anti‑spyware + anti‑malware + adware removal; flags accounts found in known breach databases |

### Other Cited Mobile Protection Tools
Norton Mobile Security for iOS · Mobile Security & Antivirus (Play Store) · Bitdefender Mobile Security · ESET Mobile Security Antivirus · WISeID Personal Vault

### Other Cited Mobile Anti‑Spyware Tools
Certo: Anti Spyware & Security · Anti Spy Detector – Spyware · iAmNotified – Anti Spy System (`iamnotified.com`) · Anti Spy (`protectstar.com`) · Secury – Anti Spy Security

## 10.12 Mobile Penetration‑Testing Toolkits

### ImmuniWeb® MobileSuite
*Source: immuniweb.com*

ML‑assisted platform that augments/accelerates **manual** mobile pentesting of iOS/Android apps: scalable static/dynamic/interactive testing with Software Composition Analysis (SCA), SDLC/CI‑CD integration, mobile‑backend WAF, and reporting (Threat‑Aware Risk Scoring, tailored remediation guidance, CVE/CWE/CVSSv3 scoring) — with a zero‑false‑positive SLA.

### Other Cited Mobile Pentest Toolkits
| Tool | URL |
|---|---|
| Codified Security | codifiedsecurity.com |
| Astra Security | getastra.com |
| Appknox | appknox.com |
| Data Theorem's Mobile Secure | datatheorem.com |
| MobSF | mobsf.live |

---

## Module Summary (per EC‑Council)

This module covered: mobile‑platform attack vectors and attacks; Android hacking techniques/tools and Android hardening/security tools; iOS hacking techniques/tools and iOS hardening/security tools; the importance of MDM; countermeasures against mobile hacking attempts; and mobile security tools to protect devices broadly. The next module in the CEH v13 curriculum (Module 18) covers **IoT and OT Hacking**.

---
**Previous:** [`09-mobile-device-management-and-byod.md`](09-mobile-device-management-and-byod.md) | **Back to:** [`README.md`](README.md)
