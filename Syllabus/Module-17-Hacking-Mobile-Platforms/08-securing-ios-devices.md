# 08 — Securing iOS Devices

> **Objective 3 (EC‑Council):** Explain Various iOS Threats and Attacks — Part C (Defense)

## Table of Contents
- [8.1 iOS Hardening Checklist (with Settings paths)](#81-ios-hardening-checklist-with-settings-paths)
- [8.2 iOS Device Security Tools](#82-ios-device-security-tools)
- [8.3 iOS Device‑Tracking Tools](#83-ios-device-tracking-tools)

---

## 8.1 iOS Hardening Checklist (with Settings paths)

**Access control**
- Enable **Passcode Lock**: `Settings → Face ID & Passcode → Turn Passcode On`. Use a separate, stronger passcode for apps holding sensitive data.
- Set **Auto‑Lock**: `Settings → General → Auto‑Lock`.
- Enable **Erase Data** after 10 failed attempts: `Settings → Face ID & Passcode → Erase Data`.
- Disable **Voice Dial** so the phone can't be called from without unlocking: `Settings → Face ID & Passcode → Voice Dial → OFF`.
- Use two‑factor authentication for the Apple ID: `Settings → [Your Name] → Sign‑In & Security → Turn On Two‑Factor Authentication`.
- Prevent lock‑screen data leakage: `Settings → Notifications → Show Previews → Never`.
- Change the default iPhone **root password from `alpine`** (relevant only on a jailbroken device with SSH enabled — see file 07 §7.7).

**Apps & code execution**
- Only install apps from the **Apple App Store**; never jailbreak/root a device used in an enterprise environment.
- Deploy **only trusted** third‑party apps.
- Do not open links/attachments from unknown sources.
- Enable **Jailbreak Detection** where available (MDM/enterprise apps), and protect access to the Apple ID and Google accounts tied to sensitive data.
- Update apps automatically: `Settings → App Store → Automatic Downloads → App Updates → ON`.
- Regularly update the OS: `Settings → General → Software Update` (App Store connection required on iOS 5+).

**Network & browsing**
- Only connect to secured/protected Wi‑Fi networks; never access web services on a compromised network.
- Enable **Ask to Join Networks**: `Settings → Wi‑Fi → Ask to Join Networks`, to avoid auto‑joining rogue APs.
- Disable Wi‑Fi and Bluetooth when not in use: `Settings → Wi‑Fi` / `Settings → Bluetooth → OFF`.
- Disable **JavaScript and add‑ons** in the browser.
- Enable Safari's security settings: `Settings → Safari` — turn on **Block Pop‑ups** and **Fraudulent Website Warning**, block cookies, disable **Passwords and AutoFill**, and periodically **Clear History and Website Data**.
- Enable **Do Not Track**: `Settings → Safari → Do Not Track`.
- Install a reputable **VPN** to encrypt all traffic.

**Data protection**
- Do not store sensitive data in a client‑side database.
- Disable iCloud services for enterprise data so corporate documents/settings/messages aren't backed up outside your control.
- Enable **Geotagging protection**: `Settings → Privacy & Security → Location Services → Camera → Never`.
- Delete the keyboard cache: `Settings → General → Transfer or Reset iPhone → Reset → Reset Keyboard Dictionary`.
- Control Apple diagnostics sharing: `Settings → Privacy & Security → Analytics & Improvements`.
- Limit ad tracking: `Settings → Privacy → Advertising → Limit Ad Tracking`.
- Leverage iOS's built‑in **full‑disk encryption** (on by default once a passcode is set) — don't disable it.
- Install a **Vault app** to further hide critical files/photos.
- Use **MDM** for enterprise remote tracking, lockout, and data wipe (see file 09).

**Physical / device hygiene**
- Configure **Find My iPhone** and use it to wipe a lost/stolen device (see §8.3 below).
- If suspicious activity is found, reset network settings: `Settings → General → Transfer or Reset [Device] → Reset → Reset Network Settings`.
- Guard against **juice jacking**: carry a portable charger, or use a USB **data blocker** ("USB condom") that only passes power, not data pins.
- Prevent unauthorized physical use with a strong six‑digit passcode, Touch ID, and Face ID together.
- Rely on the **secure boot chain**, system security, and app‑security features — these together verify that only trusted code/apps run on the device; don't disable them via jailbreaking.

> Note: exact menu paths shift slightly between iOS versions/device models — always verify against the specific OS version you're hardening.

## 8.2 iOS Device Security Tools

### Malwarebytes Mobile Security
*Source: malwarebytes.com*

- Blocks intrusive ads/ad‑trackers in **Safari**
- **Text Message Filtering** — routes suspicious/junk texts to a separate folder
- **Call Protection** — identifies/blocks known scam numbers
- Blocks phishing sites and other malicious content
- Includes a bundled **VPN** for encrypted browsing/streaming anywhere

### Other Cited iOS Device Security Tools
| Tool | URL |
|---|---|
| Norton Mobile Security for iOS | us.norton.com |
| McAfee Mobile Security | mcafee.com |
| Trend Micro™ Mobile Security for iOS | trendmicro.com |
| AVG Mobile Security | avg.com |
| Kaspersky Standard | kaspersky.com |

## 8.3 iOS Device‑Tracking Tools

### Find My
*Source: support.apple.com*

Tracks a lost iPhone/iPad/iPod Touch/Mac from another Apple device signed in with the same Apple ID. Includes **Lost Mode** (iOS 6+): locks the missing device with a passcode, shows a custom message (e.g., a contact number) on the lock screen, and logs location history for later review.

**Setup:**
1. Open **Settings**.
2. Tap `[your name] → Find My`.
3. Tap **Find My [device]** and turn it **on**.
4. Turn on **Find My network** to locate the device even while it's offline.
5. Turn on **Send Last Location** to have the device report its location to Apple automatically when the battery is critically low.

### Other Cited iOS Device‑Tracking Tools
| Tool | URL |
|---|---|
| Glympse En Route | corp.glympse.com |
| Prey Find My Phone & Security | apps.apple.com |
| Mobile Phone Tracker Pro – SIM | apps.apple.com |
| FollowMee GPS Location Tracker | apps.apple.com |
| Phone Tracker: GPS Location | apps.apple.com |
| mSpy | mspy.com |

---
**Previous:** [`07-hacking-ios-devices.md`](07-hacking-ios-devices.md) | **Next:** [`09-mobile-device-management-and-byod.md`](09-mobile-device-management-and-byod.md)
