# 05 — Hiding Files: Rootkits, NTFS ADS & Steganography

**CEH Objective:** Use different techniques to hide malicious programs and maintain remote access to the system (part B — concealment techniques).

Once malicious code is running on a target, the next problem for an attacker is survival: antivirus, EDR, and a curious sysadmin are all trying to find it. This file covers the three main concealment technique families taught in CEH: rootkits (hide the malware's *presence*), NTFS Alternate Data Streams (hide *inside* the filesystem itself), and steganography (hide data inside innocuous-looking files).

---

## 1. Rootkits

A rootkit is software designed to gain and maintain root/administrator-level access to a system **while actively hiding its own existence** — from the user, from the OS's own reporting, and ideally from security tooling. A typical rootkit bundles backdoor programs, packet sniffers, log-wiping utilities, DDoS tools, and IRC bots into a single concealed package.

**Objectives of a rootkit:**
- Gain durable, hidden backdoor access
- Mask the attacker's tracks and processes
- Harvest sensitive data and network traffic the attacker would otherwise be blocked from
- Serve as a staging platform for further malware
- Survive reboots, updates, and removal attempts
- Provide ongoing remote command-and-control

### Types of Rootkits

| Type | Where it runs | Notes |
|---|---|---|
| **Hypervisor-level** | Ring −1 | Exploits Intel VT/AMD-V to host the real OS as a VM underneath the rootkit, intercepting all hardware calls |
| **Hardware/Firmware** | BIOS, HDD firmware, NIC firmware | Survives OS reinstalls; rarely inspected for integrity |
| **Kernel-level** | Ring 0 | Highest OS privileges; modifies kernel code or device drivers directly; hardest to detect, but can destabilize the system if buggy |
| **Boot-loader-level (bootkit)** | Pre-OS | Activates before the OS even loads, enabling encryption-key and password theft |
| **Application-level / user-mode** | Ring 3 | Replaces application binaries or patches their behavior; easiest to detect, easiest to write |
| **Library-level** | High in the OS | Hooks/patches system calls with backdoored versions to feed false information to callers |
| **Memory (volatile) rootkits** | RAM only | Leaves no disk artifacts at all; wiped by reboot, but nearly invisible to disk forensics while running |

### How a Rootkit Hooks the System
- **Inline function hooking** — rewrites bytes inside core system DLLs (`kernel32.dll`, `ntdll.dll`) so any process's call to that function is redirected through the rootkit first.
- **Direct Kernel Object Manipulation (DKOM)** — directly edits kernel memory structures (e.g., the linked list of active processes) to unlink a malicious process from the list Task Manager reads, hiding it in plain sight even though it's still running.

### Popular Rootkits (for awareness / recognition, not step-by-step reproduction)
- **FudModule** — a user-space-launched rootkit that abused a zero-day admin-to-kernel vulnerability in the AppLocker driver (`appid.sys`) to perform kernel tampering via a read/write primitive, undermining Defender, CrowdStrike Falcon, and HitmanPro. (https://decoded.avast.io)
- **Fire Chili** — kernel-level rootkit that leveraged the Log4Shell vulnerability for espionage/exfiltration, hiding files, processes, and network connections. (https://www.fortinet.com)
- Others referenced in current threat intel: CopperStealer, Syslogk, Stealthy Universal Rootkit, Reptile rootkit, CosmicStrand.

### Detecting Rootkits

| Method | How it works |
|---|---|
| **Signature-based** | Compares process/file byte sequences against a database of known rootkit fingerprints; weak against novel rootkits |
| **Heuristic/behavior-based** | Flags deviations from "normal" OS behavior patterns, e.g. execution-path hooking |
| **Integrity-based** | Baseline a clean system with **Tripwire**/**AIDE**, then compare current state against that baseline to spot changes |
| **Cross-view-based** | Enumerate processes/files/registry via high-level APIs *and* via low-level direct inspection, then diff the two — a rootkit hiding something from the API won't be able to hide it from the low-level view |
| **Runtime execution path profiling** | Compares instruction execution paths before/after known routines to detect injected hooking code |

```bash
# Tripwire / AIDE — establish and later verify an integrity baseline
aide --init
cp /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz
aide --check
```

### Anti-Rootkit Tools
| Tool | Link |
|---|---|
| GMER | http://www.gmer.net |
| Stinger | https://www.trellix.com |
| TDSSKiller | https://usa.kaspersky.com |
| Malwarebytes Anti-Rootkit | https://www.malwarebytes.com |
| AVG Rootkit Scanner | https://www.avg.com |

---

## 2. NTFS Alternate Data Streams (ADS)

Every file on an NTFS volume actually consists of at least two streams: one holding security/permission metadata, and one — the "main" or unnamed stream — holding the data you normally think of as "the file." NTFS allows **additional named streams** to be attached to any file. These **Alternate Data Streams** are completely invisible to Windows Explorer and to the file's reported size, yet can hold arbitrary content — including an entire second executable.

### Creating and Manipulating ADS
```cmd
:: Notepad is stream-compliant — this creates a hidden alternate stream on myfile.txt
notepad myfile.txt:lion.txt
notepad myfile.txt:tiger.txt

:: The visible size of myfile.txt remains 0 bytes no matter how much data
:: is stored in its alternate streams

:: Read/edit a specific stream directly
notepad myfile.txt:lion.txt
```

**Hiding an executable behind a text file:**
```cmd
:: 1. Move Trojan.exe's contents into a stream behind Readme.txt
type C:\Trojan.exe > C:\Readme.txt:Trojan.exe

:: 2. Create a shortcut/link that points at the hidden stream
mklink backdoor.exe Readme.txt:Trojan.exe

:: 3. Run it
backdoor.exe

:: To view a hidden text stream directly
more < C:\Readme.txt:secret.txt
```

### Detecting and Defending Against ADS
```cmd
:: Sysinternals Streams — list all alternate streams on a file/folder
streams.exe -s C:\Users\Public

:: LADS — recursively search a drive for ADS
lads.exe C:\ /s
```
- Move suspect files to a FAT/FAT32 partition and back — FAT doesn't support ADS, so this strips them out entirely.
- Use a file-integrity checker (e.g., Tripwire) to catch unauthorized ADS creation.
- Keep antivirus real-time scanning enabled (modern AV inspects named streams too).
- Never store anything security-critical *only* inside an ADS — treat them as a known blind spot.

Additional ADS detectors: **Stream Armor** (https://securityxploded.com), **Stream Detector** (https://www.novirusthanks.org), **GMER** (http://www.gmer.net), **ADS Scanner** (https://www.pointstone.com), **AlternateStreamView** (https://www.nirsoft.net).

---

## 3. Steganography

Where cryptography hides the *meaning* of a message, steganography hides the fact that a message exists at all. A hidden message is embedded in an innocuous **cover medium**, producing a **stego-object** that looks completely ordinary to anyone who isn't specifically looking for it. This is what makes steganography attractive to attackers over encryption alone: an encrypted file announces "there's a secret here"; a steganographic file doesn't announce anything.

### Classification
- **Technical steganography** — physical/scientific concealment methods: invisible ink, microdots, computer-based bit manipulation.
- **Linguistic steganography** — hiding a message inside the *structure* of another message:
  - **Semagrams** (visual or textual — hidden in a drawing, or in font/spacing choices)
  - **Open codes** — jargon codes (meaningful only to an in-group) and covered ciphers (null ciphers, grille ciphers)

### Computer-Based Technique Families
| Technique | Idea |
|---|---|
| Substitution | Replace insignificant bits (e.g., LSBs) with secret data |
| Transform domain | Hide data during compression/transformation (DCT, wavelet) |
| Spread spectrum | Spread the hidden signal across more bandwidth than needed, recoverable only with the matching code |
| Statistical | Alter statistical properties of the cover only when encoding a "1" bit |
| Distortion | Apply a known sequence of modifications; decoding requires the original cover for comparison |
| Cover generation | Generate a brand-new cover object purpose-built to encode the message |

### Steganography by Medium

**Image steganography** — the most common form, using LSB insertion, masking/filtering, or transform-domain techniques (DCT/FFT/wavelet):
```bash
# OpenStego — hide a file inside a cover image, CLI mode
openstego embed -mf secret.txt -cf cover.png -sf output.png -p MyPassword

# OpenStego — extract a hidden file back out
openstego extract -sf output.png -xf ./extracted/ -p MyPassword

# steghide — classic Linux LSB steganography tool
steghide embed -cf cover.jpg -ef secret.txt -p MyPassword
steghide extract -sf cover.jpg -p MyPassword
```

**Whitespace steganography** — hides data in trailing spaces/tabs, invisible in most text viewers:
```bash
# snow — conceal a message as trailing whitespace in a text file
snow -C -p MyPassword -m "the secret message" cover.txt output.txt

# snow — extract it back out
snow -C -p MyPassword output.txt
```
Syntax reference: `snow [-CQS] [-p passwd] [-l line-len] [-f file | -m message] [infile [outfile]]`

**Audio steganography** — LSB coding, echo hiding, spread spectrum, phase encoding, or tone insertion in WAV/MP3/FLAC files. Tools: **DeepSound** (https://jpinsoft.net), **MP3Stego** (https://www.petitcolas.net).

**Video steganography** — extends image techniques across every frame using DCT manipulation, allowing much larger payloads than a single image. Tools: **OmniHide PRO** (https://omnihide.com), **OpenPuff** (https://embeddedsw.net).

**Document / folder / spam-email steganography** — hiding data inside Office/PDF structure, locking data invisibly inside folders (**GiliSoft File Lock Pro** — https://www.gilisoft.com), or encoding a message as innocuous-looking spam text (**Spam Mimic** — https://www.spammimic.com).

### Steganalysis (Detecting Steganography)

Steganalysis is the reverse process: detecting *that* hidden data exists, and where possible, extracting it.

| Attack type | What the analyst has |
|---|---|
| Stego-only | Just the stego-object — must try every known algorithm |
| Known-stego | The algorithm, the original cover, and the stego-object |
| Known-message | The message and the stego-medium |
| Known-cover | Both the stego-object and the original cover, for direct comparison |
| Chosen-message | A known message, used to generate stego-objects with various tools to fingerprint them |
| Chosen-stego | Both the stego-object and the tool/algorithm used |
| Chi-square | Statistical test comparing stego-object to expected clean distribution |
| Distinguishing statistical | Analyzes statistical changes and embedded-data length |
| Blind classifier | ML classifier trained on clean data, used to flag anomalies |

```bash
# zsteg — automatically scan a PNG/BMP for common LSB stego signatures
zsteg cover.png
zsteg -a cover.png    # run all known detection methods

# steghide — check whether a file even *has* an embedded payload (will fail without the right password otherwise)
steghide info cover.jpg
```

Other steganalysis tools: **StegoVeritas**, **Stegextract** (https://github.com), **StegoHunt MP** (https://www.wetstonetech.com), **Steganography Studio** (https://stegstudio.sourceforge.net), **Virtual Steganographic Laboratory (VSL)** (https://vsl.sourceforge.net).

### Defending Against Hidden Files & Steganography
- Baseline known-clean files with cryptographic hashes; investigate any unexpected size/hash drift.
- Run periodic ADS sweeps (`streams.exe`, `lads.exe`) across sensitive file shares.
- Deploy anti-rootkit and integrity-monitoring tools continuously, not just on-demand.
- Where policy requires it, run steganalysis tools against outbound image/audio/video attachments at the network egress point.
- Treat unexplained file-size anomalies, unusual color-noise, or odd audio artifacts as investigation triggers, not curiosities.

**Next:** [06 — Persistence and Domain Dominance](./06-Persistence-and-Domain-Dominance.md)
