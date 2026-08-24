# 07 — Covering Tracks

**CEH Objective:** Demonstrate techniques to hide the evidence of compromise.

The final stage of the CEH hacking methodology. Once an attacker has gained access, escalated privileges, and established persistence, the last job is to make sure the trip back through security logs, filesystem timestamps, and forensic artifacts leads nowhere. Erasing evidence isn't optional for an attacker who wants to keep their access — it's what separates a one-time smash-and-grab from a long-term foothold.

---

## 1. Why Logs Matter (and Which Ones)

The first thing most administrators check when something looks wrong is the system log. On Windows, the three classic event log files an attacker is most concerned about are:

| Log file | Contents |
|---|---|
| `SECEVENT.EVT` (Security) | Failed logins, unauthorized file access attempts |
| `SYSEVENT.EVT` (System) | Driver failures, hardware/OS-level errors |
| `APPEVENT.EVT` (Application) | Application-level events |

Attackers don't always delete an entire log (that itself is suspicious and needs admin rights) — often they selectively remove just the entries that reveal their activity, leaving the rest of the log intact so nothing looks obviously wrong.

---

## 2. Disabling Auditing

The very first move for an attacker with command-line access is often to check — and then disable — the target's audit policy, so that whatever comes next simply never gets logged in the first place.

```cmd
:: Check current auditing status across all categories
auditpol /get /category:*

:: Disable auditing for system and account logon events
auditpol /set /category:"system","account logon" /success:disable /failure:disable

:: (Attackers typically re-enable it before leaving, to avoid leaving an obvious gap)
auditpol /set /category:"system","account logon" /success:enable /failure:enable
```

---

## 3. Clearing Logs

### Via Meterpreter
```
meterpreter > clearev
```

### Via PowerShell
```powershell
# Clear the PowerShell event log on the local machine
Clear-EventLog "Windows PowerShell"

# Clear specific logs across local and remote systems
Clear-EventLog -LogName Diag,OSession -ComputerName localhost,Server02

# Clear all logs on specified systems, with confirmation
Clear-EventLog -LogName application,system -Confirm
```
Useful parameters: `-ComputerName` (target a remote machine; defaults to local), `-Confirm` (prompt before running), `-LogName` (which log(s) to target), `-WhatIf` (dry run).

### Via wevtutil
```cmd
:: List all available event logs
wevtutil el

:: Clear a specific log
wevtutil cl system
wevtutil cl application
wevtutil cl security
```

### Manually (GUI)
- **Windows:** `Start → Control Panel → System and Security → Windows Tools → Event Viewer`, then delete the relevant entries.
- **Linux:** navigate to `/var/log/`, and directly edit the log file containing the relevant message with a text editor, or overwrite it entirely:
  ```bash
  cat /dev/null > /var/log/auth.log
  ```

### Clear_Event_Viewer_Logs.bat Utility
1. Download the utility (e.g., from a trusted repository such as tenforums.com).
2. Unblock the `.bat` file (right-click → Properties → Unblock).
3. Right-click → **Run as administrator**.
4. Approve the UAC prompt if shown.
5. The command window clears all logs and closes automatically.

---

## 4. Covering BASH Shell Tracks

Bash logs every command you type to `~/.bash_history`, which is exactly what an investigator will pull up first to reconstruct an intrusion.

```bash
# View the current saved history
more ~/.bash_history

# Disable history logging going forward, for the current shell
export HISTSIZE=0

# Clear the in-memory history (doesn't touch the file on its own)
history -c

# Clear the history of only the current shell session
history -w

# Wipe the complete history file and exit cleanly
cat /dev/null > ~/.bash_history && history -c && exit

# Shred the history file so its old contents are unrecoverable, then clear and exit
shred ~/.bash_history
shred ~/.bash_history && cat /dev/null > ~/.bash_history && history -c && exit
```

---

## 5. Covering Tracks on a Network

- **Reverse HTTP shells** — malware on the victim periodically polls an external "master" for commands over what looks like normal outbound HTTP traffic (a GET request), executes them, and returns results in the next request — indistinguishable from ordinary web browsing to most perimeter security controls.
- **Reverse ICMP tunnels** — smuggle a TCP payload inside ICMP echo/reply packets. Effective because many organizations only inspect *inbound* ICMP, not outbound.
- **DNS tunneling** — encode data inside DNS query/response traffic to build a covert channel and exfiltrate data through a service almost every network allows outbound by default.
- **TCP parameter abuse** — hide data bitwise inside the IP Identification field, the TCP acknowledgment number, or the TCP initial sequence number, encapsulating a character or two per packet without an established session in some variants.

---

## 6. Covering Tracks on the OS

### Windows — ADS-based hiding
```cmd
:: Hide a secret file's contents inside a legitimate-looking file's alternate stream
type C:\SecretFile.txt > C:\LegitFile.txt:SecretFile.txt

:: Read it back
more < C:\SecretFile.txt
```

### Modifying Timestamps ("timestomping")
```cmd
:: timestomp.exe (Metasploit tool) — set arbitrary MACE timestamps
timestomp file_name.doc -z "01/01/2020 00:00:00"
```
```powershell
# Native PowerShell equivalent
(Get-Item $File_name).LastWriteTime = $(Get-Date).AddHours(-10)
```

### Linux — hiding via naming convention + timestamp modification
```bash
# Prefix filenames with a dot to hide them from a plain `ls`
mv payload.sh .payload.sh

# Change access time on a file
touch -a -d '2020-01-01 00:00:00' payload.sh

# Change modification time on a file
touch -m -d '2020-01-01 00:00:00' payload.sh
```

---

## 7. Deleting Files Securely — Cipher.exe

Simply "deleting" a file just removes its directory pointer — the data itself is still recoverable until overwritten. Windows ships a built-in tool for exactly this:

```cmd
:: Overwrite all deleted (but not yet reclaimed) space in a specific folder
cipher /w:C:\Users\victim\Documents

:: Overwrite all deleted space across an entire drive
cipher /w:C:
```
`cipher /w` overwrites free space three times: once with zeroes, once with `0xFF`, and once with random data — specifically to defeat recovery of files that were deleted (including backup files automatically created and then removed during encryption operations).

---

## 8. Disabling Windows Forensic Artifacts

```cmd
:: Disable the last-access timestamp (fsutil)
fsutil behavior set disablelastaccess 1
:: (0 = enabled, 1 = disabled)

:: Disable hibernation (removes Hiberfil.sys, which can contain a RAM snapshot)
powercfg.exe /hibernate off
```
- **Disable virtual memory / paging file:** Control Panel → System and Security → System → Advanced system settings → Performance *Settings* → Advanced tab → Virtual Memory *Change* → uncheck "Automatically manage paging file size" → select **No paging file** for each drive.
- **Disable System Restore points:** Control Panel → System and Security → System → System protection → select the drive → **Configure** → **Disable system protection** → **Delete** to purge existing restore points.
- **Disable the thumbnail cache** (`thumbs.db` can reveal previously viewed/deleted images): `gpedit.msc` → User Configuration → Administrative Templates → Windows Components → File Explorer → enable *"Turn off the caching of thumbnails in hidden thumbs.db files."*
- **Disable Prefetch** (can reveal traces of uninstalled applications): `services.msc` → find **SysMain (Superfetch)** → set Startup type to **Disabled**.

### Clearing Windows Activity History
`Settings (Win+I) → Privacy & security → Activity history → Clear` button → confirm.

### Clearing Incognito/Private Browsing Traces
```cmd
:: Windows — view then flush the DNS cache (also reveals recently visited domains)
ipconfig /displaydns
ipconfig /flushdns
```
```bash
# macOS — clear the DNS resolver cache
sudo killall -INFO mDNSResponder
```

### Clearing General Online Tracks
Remove Most Recently Used (MRU) lists, delete cookies, clear cache, turn off AutoComplete, and clear toolbar data from the browser. On Windows 11 specifically:
- **Via Settings:** right-click Start → Settings → Personalization → Start → turn off "Show most used apps" and "Show recently opened items."
- **Via Registry:** `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer` → delete the `RecentDocs` key contents (leave `(Default)` alone).

---

## 9. Hiding Files, Folders, and User Accounts

### Windows
```cmd
:: Hide a file or folder using the hidden + system attributes
attrib +h +s <FolderName>

:: Create a new local user
net user <UserName> <Password> /add

:: Activate it for use
net user <UserName> /active:yes

:: Hide it from the standard login screen when not needed
net user <UserName> /active:no
```
For a deeper hide, attackers create a registry key structure under `HKEY_LOCAL_MACHINE\Software\Microsoft\WindowsNT\CurrentVersion\Winlogon` naming a "SpecialAccounts\UserList" DWORD entry `0` for the target username, which removes the account from the Welcome screen entirely while it remains fully functional.

### Linux
```bash
cd ~/Documents/MaliciousFiles/

# Rename a file to hide it (dot-prefix convention)
mv MaliciousFile.txt .MaliciousFile.txt

# Confirm — ls alone won't show it, ls -a will
ls
ls -a

# Create a hidden directory
mkdir .HiddenMaliciousFiles

# Create a hidden file directly inside it
touch .HiddenMaliciousFiles/.MaliciousFile.txt
```

### macOS
```bash
# Hide all files globally in Finder (drastic; rarely used) and restart Finder
defaults write com.apple.finder AppleShowAllFiles FALSE
killall Finder

# Hide one specific file
chflags hidden <filename>
```

---

## 10. Anti-Forensics Technique Taxonomy

| Technique | Idea |
|---|---|
| **Data/file deletion** | Remove file pointers; Shift+Delete bypasses the Recycle Bin entirely, complicating recovery |
| **Password protection** | Lock files/archives/devices to slow down investigators and reverse engineers |
| **Steganography** | Hide data inside innocuous cover files (see file 05) |
| **Data hiding in filesystem structures** | Abuse `$BadClus`, Host-Protected Areas (HPA), Device-Protected Areas (DPA), and slack space — regions invisible to normal OS/BIOS enumeration |
| **Trail obfuscation** | Log tampering, forged email headers, timestamp modification (**Timestomp**, **Transmogrify**), log cleaners, zombie accounts, misinformation, spoofing |
| **Artifact wiping** | Permanently destroy evidence with file-wiping/disk-cleaning tools: **BCWipe**, **DriveScrubber**, **Disk Wipe**, **KillDisk**, **R-Wipe & Clean**, **BitRaser File Eraser**, **Blancco File Eraser** |
| **Overwriting data/metadata** | Multi-pass overwrites (data shredding) of storage media to defeat recovery |
| **Program packers** | Compress/encrypt executables to resist reverse engineering: **UPX**, **PECompact**, **BurnEye**, **Exe Stealth Packer**, **Smart Packer Pro** |
| **Minimizing footprint** | Use stolen identities, disposable VMs/cloud infra, untraceable cryptocurrency, and Live-USB/external-HDD OSes that leave nothing on the host disk |
| **Access anonymization** | Proxy chains, VPNs, Tor, traffic padding, anonymous communication channels |

---

## 11. Track-Covering Tools

| Tool | Purpose | Link |
|---|---|---|
| CCleaner | System/browser cleanup, deletes temp files, registry entries, browsing history | https://www.ccleaner.com |
| DBAN | Full disk wipe/destruction | https://dban.org |
| Privacy Eraser Free | Track & file cleaner | https://www.cybertronsoft.com |
| Wipe | Secure file/history deletion | https://privacyroot.com |
| BleachBit | Cross-platform disk/privacy cleaner | https://www.bleachbit.org |
| east-tec Eraser | File/history wiping suite | https://www.east-tec.com |

---

## 12. Defending Against Covering-Tracks Techniques

- Activate logging on **every** critical system, not just the obvious ones.
- Configure logs so **new events never silently overwrite old ones** when storage limits are hit.
- Maintain a **centralized logging server** (in a DMZ) so critical servers forward logs off-host in real time — local log deletion then can't erase the copy.
- **Encrypt log files** and store them in **append-only / immutable** mode so entries can't be altered or deleted without the decryption key.
- Periodically back up logs to **write-once/unalterable media**.
- Deploy **file integrity monitoring (FIM)** on critical system and config files.
- Run a **SIEM** for real-time correlation of security alerts and detection of log tampering or deletion events.
- Use **IDS/IPS** and **UEBA** tooling to flag behavior anomalies indicative of anti-forensic activity, not just signature matches.
- Regularly patch OSes, applications, and firmware, and close unused ports/services to shrink the overall attack surface these techniques rely on.
- Conduct periodic audits confirming logging configuration still matches written security policy — configuration drift is how "we have logging" quietly becomes "we don't, actually."

---

## Module Recap

Across these seven files, the full CEH System Hacking arc:

1. **Gaining Access** — crack or steal credentials (file 01), or exploit a software vulnerability directly (file 02).
2. **Escalating Privileges** — turn limited access into admin/root/domain-admin (file 03).
3. **Maintaining Access** — run malicious code remotely and keep it running via keyloggers/spyware (file 04), concealment techniques (file 05), and durable persistence up to full domain dominance (file 06).
4. **Covering Tracks** — erase the evidence trail across logs, timestamps, and forensic artifacts (this file).

Every stage has a defensive mirror. In practice, most of these attacks succeed not because the underlying technique is exotic, but because one basic control was missing: a weak password, an unpatched CVE, an over-permissioned service account, or logging that nobody was actually watching.
