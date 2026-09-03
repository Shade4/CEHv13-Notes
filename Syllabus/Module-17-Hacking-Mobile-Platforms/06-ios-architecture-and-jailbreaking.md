# 06 — iOS Architecture & Jailbreaking

> **Objective 3 (EC‑Council):** Explain Various iOS Threats and Attacks — Part A (Foundations)

## Table of Contents
- [6.1 Apple iOS Overview & Architecture](#61-apple-ios-overview--architecture)
- [6.2 Jailbreaking iOS](#62-jailbreaking-ios)
- [6.3 Types of Jailbreaking](#63-types-of-jailbreaking)
- [6.4 Jailbreaking Techniques (Persistence Models)](#64-jailbreaking-techniques-persistence-models)
- [6.5 Jailbreaking with Hexxa Plus](#65-jailbreaking-with-hexxa-plus)
- [6.6 Other Jailbreaking Tools](#66-other-jailbreaking-tools)

---

## 6.1 Apple iOS Overview & Architecture

iOS is a closed‑source, Apple‑exclusive mobile OS (never licensed for non‑Apple hardware) powering iPhone, iPod Touch, iPad, and Apple TV. Its UI model is built entirely around **direct manipulation via multi‑touch gestures**.

```
┌───────────────────────────────────────────────────────┐
│                COCOA (APPLICATION) — AppKit             │  Multitasking, touch input, push
│                                                          │  notifications, high-level system svcs
├───────────────────────────────────────────────────────┤
│                          MEDIA                           │  AV Foundation, Core Animation,
│              AV Found · Core Anim · Core Audio           │  Core Audio, Core Image, Core Text,
│              Core Image · Core Text · OpenAL/GL · Quartz │  OpenAL, OpenGL, Quartz
├───────────────────────────────────────────────────────┤
│                      CORE SERVICES                       │  Address Book, Core Data, Core
│  Address Book · Core Data · Core Foundation · Foundation │  Foundation, Foundation, Quick Look,
│         Quick Look · Social · Security · WebKit          │  Social, Security, WebKit
├───────────────────────────────────────────────────────┤
│                         CORE OS                           │  Accelerate, Directory Services,
│  Accelerate · Directory Svcs · Disk Arbitration · OpenCL  │  Disk Arbitration, OpenCL, System
│                  · System Configuration                  │  Configuration
├───────────────────────────────────────────────────────┤
│                KERNEL AND DEVICE DRIVERS                  │  BSD, File System, Mach, Networking
│              BSD · File System · Mach · Networking        │
└───────────────────────────────────────────────────────┘
```

| Layer | Role |
|---|---|
| **Cocoa Application** | Key app‑building frameworks (AppKit); appearance, multitasking, touch input, push notifications |
| **Media** | Graphics/audio/video technologies powering rich multimedia UIs |
| **Core Services** | Fundamental app services — Core Foundation/Foundation define the base types every app uses; social, iCloud, location, networking live here |
| **Core OS** | Low‑level features other layers build on; security and external‑hardware/network communication live here — depends directly on the kernel layer below it |
| **Kernel and Device Drivers** | Kernel, drivers, BSD, file systems, networking infrastructure — the lowest layer, and the layer every jailbreak ultimately targets |

## 6.2 Jailbreaking iOS

**Definition:** installing a modified set of kernel patches that lets a device run third‑party applications not signed by Apple — i.e., bypassing Apple's user‑level restrictions to gain **root access**, modify the OS, and sideload unofficial apps/themes/extensions ("side‑loading").

Jailbreaking also **removes sandbox restrictions**, which is precisely why it's double‑edged: legitimate power users get customization freedom, but a malicious app on a jailbroken device inherits the same freedom to access resources it should never be allowed to touch.

**Known risks that come with jailbreaking** (same risk profile as Android rooting):
- Voids the phone's warranty
- Poor/degraded performance
- Increased malware‑infection risk
- Risk of "bricking" the device entirely

## 6.3 Types of Jailbreaking

| Type | Access level | Patchability |
|---|---|---|
| **Userland Exploit** | User‑level access only (no iBoot‑level access) | Cannot be "secured against" with a recovery‑mode loop — only an Apple **firmware update** patches the underlying loophole |
| **iBoot Exploit** | Both user‑level *and* iBoot‑level access | Exploits a loophole in **iBoot** (the iDevice's third bootloader) to delink code‑signing enforcement; can be semi‑tethered on devices with a newer bootrom; patchable via firmware update |
| **Bootrom Exploit** | Both user‑level *and* iBoot‑level access | Exploits a loophole in **SecureROM** (the iDevice's first bootloader) to disable signature checks and load patched NOR firmware; **cannot** be patched by a software update — only an Apple **hardware revision** of the bootrom closes it |

## 6.4 Jailbreaking Techniques (Persistence Models)

| Technique | Behavior after a reboot |
|---|---|
| **Untethered** | Device boots up completely on its own, kernel is patched automatically — jailbroken again after *every* reboot, no computer needed |
| **Semi‑tethered** | Device boots up completely and is usable for normal functions, but the **patched kernel is lost**; to restore jailbroken add‑ons the user must re‑run the jailbreak tool from a computer |
| **Tethered** | If it boots on its own it gets stuck **partially started** with no patched kernel; it must be "re‑jailbroken" from a computer (using the tool's "boot tethered" feature) *every single time* it's powered on |
| **Semi‑untethered** | Like semi‑tethered, but the kernel can be **re‑patched without a computer** — via an app already installed on the device itself |

## 6.5 Jailbreaking with Hexxa Plus

**Hexxa Plus** (`hexxaplus.com`) is a jailbreak *repo extractor* — it doesn't jailbreak the kernel itself, but lets you install jailbreak‑ecosystem apps/tweaks/themes on the latest iOS via developer‑certificate sideloading, without needing a full untethered/semi‑untethered kernel jailbreak.

**Steps:**
1. Go to the **Xookz App Store** → tap **Hexxa (Full)**.
2. Tap **Install** (top‑right) to push a configuration profile to the device (allow any pop‑up).
3. Go to **Settings** → tap the downloaded profile → **Install**.
4. Enter the device passcode → tap **Install** again.
5. The **Hexxa Plus Repo Extractor** icon appears on the home screen.
6. Open it → tap **Get Repos**.
7. Choose a desired jailbreak repo category → copy its URL.
8. Tap **Extract Repo** → paste the copied URL.
9. Tap **OK** to extract the repo — the jailbreak app catalog is now installed.

> A third‑party app manager such as **ZJailbreak Pro** is typically required to install Hexxa Plus for free in the first place.

## 6.6 Other Jailbreaking Tools

| Tool | URL | Notes |
|---|---|---|
| **Redensa** | pangu8.com | Ships with **iTerminal**; simplifies installing jailbreak apps/tweaks on iOS 17+; supports one‑command IPA installs (`Install`) |
| **checkrain** | checkra.in | Bootrom‑exploit‑based (checkm8) semi‑tethered jailbreak for older A‑series chips |
| **palerain** | palera.in | Modern jailbreak targeting checkm8‑vulnerable devices |
| **Zeon** | zeon-app.com | — |
| **Sileo** | en.sileem.com | Alternative package manager to Cydia, used across many modern jailbreaks |
| **Cydia** | cydiafree.com | The original, best‑known jailbreak package manager/app store |

---
**Previous:** [`05-securing-android-devices.md`](05-securing-android-devices.md) | **Next:** [`07-hacking-ios-devices.md`](07-hacking-ios-devices.md)
