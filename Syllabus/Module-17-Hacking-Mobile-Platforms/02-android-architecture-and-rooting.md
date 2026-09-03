# 02 — Android Architecture & Rooting

> **Objective 2 (EC‑Council):** Explain Various Android OS Threats and Attacks — Part A (Foundations)

## Table of Contents
- [2.1 Android OS Overview](#21-android-os-overview)
- [2.2 Android OS Architecture](#22-android-os-architecture)
- [2.3 Android Device Administration API](#23-android-device-administration-api)
- [2.4 Android Rooting](#24-android-rooting)

---

## 2.1 Android OS Overview

*Source: developer.android.com*

Android is Google's Linux‑kernel‑based, open‑source mobile OS. Key facts worth knowing before attacking or defending it:

- **Persistent storage options** apps can use: `SharedPreferences` (key‑value), Internal Storage (private, sandboxed), External Storage (shared, historically the weak point — see Man‑in‑the‑Disk in file 03), SQLite databases (private), and network storage.
- **RenderScript** — a platform‑independent, native‑level compute engine for CPU‑intensive app workloads.
- Rich inter‑device connectivity APIs: Bluetooth, NFC, Wi‑Fi P2P, USB, SIP.
- **ART (Android Runtime)** replaced Dalvik from Android 5.0 onward, adding AOT + JIT compilation and better garbage collection; apps still ship as **DEX** bytecode.

## 2.2 Android OS Architecture

Android is a six‑component, five‑layer stack:

```
┌───────────────────────────────────────────────────────────┐
│                        SYSTEM APPS                          │  Dialer, Email, Calendar, Camera, SMS, Browser...
├───────────────────────────────────────────────────────────┤
│                    JAVA API FRAMEWORK                       │  Content Providers, View System, Activity/Location/
│                                                              │  Package/Notification/Resource/Telephony/Window Mgrs
├──────────────────────────┬────────────────────────────────┤
│   NATIVE C/C++ LIBRARIES  │        ANDROID RUNTIME         │  WebKit/Blink, OpenMAX AL, Libc, Media Framework,
│                           │     (ART + Core Libraries)      │  OpenGL|ES, Surface Manager, SQLite, FreeType, SSL
├───────────────────────────────────────────────────────────┤
│              HARDWARE ABSTRACTION LAYER (HAL)                │  Audio, Bluetooth, Camera, Sensors modules
├───────────────────────────────────────────────────────────┤
│                       LINUX KERNEL                           │  Audio/Binder(IPC)/Display/Keypad/Bluetooth/WiFi/
│                                                              │  USB/Camera/Shared-memory drivers, power mgmt
└───────────────────────────────────────────────────────────┘
```

| Layer | Purpose | Attack‑relevant detail |
|---|---|---|
| **System Apps** | Pre‑installed and user apps, mostly written in Java/Kotlin | Attack surface for repackaging, Agent‑Smith‑style app replacement |
| **Java API Framework** | High‑level services: Content Providers (data sharing between apps), Activity Manager, Package Manager, Notification Manager, Location Manager, Telephony Manager, Window Manager | **Exported** activities/providers/services/receivers are exactly what `drozer`'s `app.package.attacksurface` enumerates (see file 03) |
| **Native C/C++ Libraries** | WebKit/Blink (browser engine), OpenMAX AL, Libc, Media Framework, OpenGL\|ES, Surface Manager, SQLite, FreeType, SSL | Memory‑corruption bug class (native code) lives here |
| **Android Runtime (ART)** | AOT + JIT compilation, optimized GC, DEX bytecode | Reverse engineering targets DEX/smali (see `apktool`, Frida in file 03/04) |
| **HAL** | Abstracts hardware (audio, camera, Bluetooth, sensors) from the Java framework | Vendor‑specific HAL bugs (camera hijack in file 01 relies on permission‑bypass bugs near this layer) |
| **Linux Kernel** | Device drivers, memory/power/security management, networking | Kernel exploits are the basis of most **root** techniques |

## 2.3 Android Device Administration API

*Source: developer.android.com*

The Device Administration API lets a "Device Admin" app (installed by IT, or — if abused — by an attacker with social‑engineered install access) enforce policy at the system level. Legitimate uses: email clients, remote‑wipe security apps, MDM agents. This is also exactly the API abused by some **mobile ransomware/stalkerware** to lock a device or resist uninstallation.

| Policy | What it does |
|---|---|
| Password enabled | Requires a PIN/password |
| Minimum password length | e.g. ≥ 6 characters |
| Alphanumeric password required | Letters + numbers (+ optional symbols) |
| Complex password required | ≥1 letter, ≥1 digit, ≥1 symbol (Android 3.0+) |
| Minimum letters / lowercase / uppercase / non‑letter chars / digits / symbols required | Fine‑grained composition rules (Android 3.0+) |
| Password expiration timeout | Forces periodic password rotation |
| Password history restriction | Blocks reuse of the last *n* passwords |
| Maximum failed password attempts | Triggers an automatic **factory wipe** after *n* failures |
| Maximum inactivity time lock | Auto‑lock after 1–60 minutes idle |
| Require storage encryption | Android 3.0+ |
| Disable camera | Android 4.0+, can be toggled dynamically |

Plus imperative actions: **prompt for new password, lock immediately, wipe device (factory reset)**.

## 2.4 Android Rooting

**Concept:** Rooting exploits a firmware/kernel vulnerability to copy an `su` binary into a directory on the process `PATH` (classically `/system/xbin/su`) and grant it executable permission with `chmod`, giving the user (or an app) **UID 0** privileges — full read/write across the filesystem, bypassing manufacturer/carrier restrictions.

**Why attackers care:** a rooted device has no meaningful app sandboxing left to rely on — a malicious app that can also get root (or that abuses an already‑rooted device) can read every other app's private data, disable security controls, and persist invisibly.

### Rooting with KingoRoot (PC method)
1. Download **KingoRoot (PC Version)** and install it on a Windows desktop.
2. Connect the Android device via USB.
3. Enable **USB debugging** (`Settings → Developer options → USB debugging`).
4. KingoRoot installs the correct USB drivers automatically; the device appears on screen with a **ROOT** button.
5. Click **ROOT**.

### Rooting with KingoRoot (No‑PC / on‑device method)
1. Enable **Install from unknown sources**.
2. Download `KingoRoot.apk` directly on the device.
3. Install and launch it.
4. Tap **One Click Root** and wait for the "root result" screen.
5. Retry a few times, or fall back to the PC version, if it fails.

### Rooting with OneClickRoot
1. Download **One Click Root (PC Version)**, install on desktop.
2. Connect device via USB, enable USB debugging.
3. Run the tool, click **ROOT**.
4. Extra features once rooted: install apps to SD card, Wi‑Fi/Bluetooth tethering, custom ROM installs, instant "un‑root" fail‑safe.

### Other Android Rooting Tools
| Tool | URL |
|---|---|
| TunesGo | tunesgo.wondershare.com |
| RootMaster | root-master.com |
| Magisk Manager | magiskmanager.com |
| KingRoot | kingrootapp.net |
| iRoot | iroot-download.com |

> **Magisk** deserves a special mention for modern pentest labs: it performs **systemless root** (patches the boot image rather than `/system`), which lets you pass many root‑detection checks via **Magisk Hide/Zygisk** modules — closely mirroring what a sophisticated real‑world attacker (or a security researcher bypassing an app's own root‑detection) would do.

---
**Previous:** [`01-mobile-platform-attack-vectors.md`](01-mobile-platform-attack-vectors.md) | **Next:** [`03-hacking-android-devices.md`](03-hacking-android-devices.md)
