# 02 — NetBIOS Enumeration

## 2.1 Why NetBIOS Goes First

NetBIOS is typically the very first thing an attacker enumerates on a Windows target, because it extracts a disproportionately large amount of sensitive information relative to the effort involved — usernames and network shares chief among them.

**NetBIOS** (Network Basic Input/Output System) was originally built as an API so client software could access LAN resources; Windows still leans on it for file and printer sharing today. A **NetBIOS name** is a unique 16-character ASCII string assigned to identify a network device over TCP/IP — 15 characters hold the device name, and the 16th character is reserved for the service or record type.

NetBIOS runs on:
- **UDP 137** — name services
- **UDP 138** — datagram services
- **TCP 139** — session services

Attackers go after the NetBIOS service specifically because it's easy to exploit and, critically, it often runs on Windows systems **even when nobody's actively using it**.

> **Note:** Microsoft does not support NetBIOS name resolution over IPv6.

## 2.2 What NetBIOS Enumeration Reveals

Attackers use NetBIOS enumeration to obtain:
- The list of computers that belong to a domain
- The list of shares on individual hosts in the network
- Policies and passwords

If an attacker finds a Windows system with **port 139 open**, they can check what resources are accessible/viewable on that remote system. To actually enumerate NetBIOS *names*, though, the remote system needs file and printer sharing enabled. Depending on what shares are available, NetBIOS enumeration can let an attacker read or write to the remote system — or even launch a DoS attack.

### The NetBIOS Name List

| Name | NetBIOS Code | Type | Information Obtained |
|---|---|---|---|
| `<host name>` | `<00>` | UNIQUE | Hostname |
| `<domain>` | `<00>` | GROUP | Domain name |
| `<host name>` | `<03>` | UNIQUE | Messenger service running for the computer |
| `<username>` | `<03>` | UNIQUE | Messenger service running for the logged-in user |
| `<host name>` | `<20>` | UNIQUE | Server service running |
| `<domain>` | `<1D>` | GROUP | Master browser name for the subnet |
| `<domain>` | `<1B>` | UNIQUE | Domain master browser name — identifies the primary domain controller (PDC) for the domain |
| `<domain>` | `<1E>` | GROUP | Browser service elections |

## 2.3 Nbtstat Utility

**Source:** https://learn.microsoft.com

`nbtstat` is a built-in Windows utility for troubleshooting NetBIOS name-resolution problems — it can remove and correct preloaded entries using several case-sensitive switches. Attackers repurpose it to enumerate NetBIOS-over-TCP/IP (NetBT) protocol statistics, NetBIOS name tables for both local and remote computers, and the NetBIOS name cache.

**Syntax:**
```
nbtstat [-a <remotename>] [-A <IPaddress>] [-c] [-n] [-r] [-R] [-RR] [-s] [-S] [<interval>] [-?]
```

| Parameter | Function |
|---|---|
| `-a <remotename>` | Displays the NetBIOS name table of a remote computer, where `<remotename>` is that computer's NetBIOS name |
| `-A <IPaddress>` | Displays the NetBIOS name table of a remote computer, specified by dotted-decimal IP address instead of name |
| `-c` | Lists the contents of the NetBIOS name cache — the table of NetBIOS names and their resolved IP addresses |
| `-n` | Displays the names registered locally by NetBIOS applications such as the server and redirector |
| `-r` | Displays a count of all names resolved by broadcast or WINS server |
| `-R` | Purges the name cache and reloads all `#PRE`-tagged entries from the Lmhosts file |
| `-RR` | Releases and re-registers all names with the name server |
| `-s` | Lists the NetBIOS sessions table, converting destination IP addresses to computer NetBIOS names |
| `-S` | Lists the current NetBIOS sessions and their status, with IP addresses (no name conversion) |
| `<interval>` | Re-displays selected statistics, pausing for the number of seconds specified between each display |
| `-?` | Displays help |

### Example — Obtain the NetBIOS Name Table of a Remote Computer

```
nbtstat -a 10.10.1.11
```

Sample output:
```
NetBIOS Remote Machine Name Table

Name                    Type       Status
--------------------------------------------
WINDOWS11      <00>     UNIQUE     Registered
WORKGROUP      <00>     GROUP      Registered
WINDOWS11      <20>     UNIQUE     Registered
WORKGROUP      <1E>     GROUP      Registered
WORKGROUP      <1D>     UNIQUE     Registered
..__MSBROWSE__.<01>     GROUP      Registered

MAC Address = XX-XX-XX-XX-XX-XX
```

### Example — Obtain the NetBIOS Name Cache

```
nbtstat -c
```

Sample output:
```
NetBIOS Remote Cache Name Table

Name              Type       Host Address     Life [sec]
--------------------------------------------------------
WINDOWS11         <20>       UNIQUE            10.10.1.11        488
```

## 2.4 NetBIOS Enumeration Tools

NetBIOS enumeration tools explore and scan a network within a given IP range and list of computers to spot security loopholes or flaws. Beyond raw NetBIOS names, these tools also often enumerate OS details, users, groups, Security Identifiers (SIDs), password policies, services, service packs/hotfixes, NetBIOS shares, transports, sessions, disks, and security event logs.

### NetBIOS Enumerator

**Source:** https://nbtenum.sourceforge.net

NetBIOS Enumerator demonstrates how to use remote network support alongside other web protocols like SMB. Attackers specify a target IP range, and the tool returns NetBIOS names, usernames, domain names, and MAC addresses for every host in that range — including whether a user is currently logged on, the workgroup, and (for domain controllers) roles like Domain Controller / Potential Master Browser / Domain Master Browser.

### Nmap

**Source:** https://nmap.org

Attackers use the **Nmap Scripting Engine (NSE)** to discover NetBIOS shares on a network. The `nbstat.nse` script retrieves the target's NetBIOS names and MAC address. By default it shows the computer name and the logged-in user; turning up verbosity displays every name associated with the system.

```bash
nmap -sV -v --script nbstat.nse <target IP address>
```

Sample partial output:
```
Host script results:
| nbstat: NetBIOS name: SERVER2022, NetBIOS user: <unknown>, NetBIOS MAC: 00:15:5d:01:80:02 (Microsoft)
| Names:
|   SERVER2022<00>  Flags: <unique><active>
|   CEH<00>          Flags: <group><active>
|   CEH<1c>          Flags: <group><active>
|   SERVER2022<20>  Flags: <unique><active>
|   CEH<1e>          Flags: <group><active>
|   CEH<1b>          Flags: <unique><active>
|_  CEH<1d>          Flags: <unique><active>
```

You can scope this to the raw NetBIOS name-service port directly:
```bash
nmap -sU -p 137 --script nbstat.nse <target IP address>
```

### Other NetBIOS Enumeration Tools

| Tool | Source |
|---|---|
| Global Network Inventory | https://magnetosoft.com |
| Advanced IP Scanner | https://www.advanced-ip-scanner.com |
| Hyena | https://www.systemtools.com |
| Nsauditor Network Security Auditor | https://www.nsauditor.com |

## 2.5 NetBIOS Enumeration Using AI

The same "prompt an AI shell-assistant" pattern seen throughout the CEH courseware applies here: an attacker can use ChatGPT (or another generative AI tool wired into a shell) to translate plain-English requests into working `nbtscan`/`nmblookup`/`nmap` commands. Worked examples from the source material:

**Prompt:** *"Perform NetBIOS enumeration on target IP 10.10.1.11"*
```bash
nbtscan 10.10.1.11
```
Output includes the IP address, NetBIOS name, server/user info, and MAC address in one line per host.

**Prompt:** *"Get NetBIOS info for IP 10.10.1.11 and display the associated names"*
```bash
nmblookup -A 10.10.1.11
```
`-A` queries the target by IP and lists all associated NetBIOS names (host, workgroup, master-browser flags) plus the MAC address.

**Prompt:** *"Enumerate NetBIOS on target IP 10.10.1.22 with nmap"*
```bash
nmap -sU -p 137 --script nbstat.nse 10.10.1.22
```
This automates NetBIOS enumeration over the raw name-service port and returns the same style of output shown in the manual Nmap example above.

## 2.6 Enumerating Shared Resources Using Net View

**Net View** is a command-line utility that displays a list of computers in a specified workgroup, or the shared resources available on a specified computer.

```
net view \\<computername>
```
`<computername>` is the name or IP address of the specific computer whose resources you want to see.

```
net view \\<computername> /ALL
```
Displays *all* shares on the specified remote computer, including hidden shares.

```
net view /domain
```
Displays all the shares in the current domain.

```
net view /domain:<domain name>
```
Displays all the shares on the specified domain.

### Example Output

```
net view \\10.10.1.22 /ALL
```
```
Shared resources at \\10.10.1.22

Share name   Type    Used as   Comment
--------------------------------------------------
ADMIN$       Disk              Remote Admin
C$           Disk              Default share
IPC$         IPC               Remote IPC
NETLOGON     Disk              Logon server share
SYSVOL       Disk              Logon server share
Users        Disk

The command completed successfully.
```

This single command hands an attacker a ready-made list of administrative and data shares (`ADMIN$`, `C$`, `IPC$`, `NETLOGON`, `SYSVOL`, and any custom shares like `Users`) on the target — exactly the kind of jumping-off point described in file `01`'s note about IPC$ abuse.

## 2.7 Enumerating User Accounts — The PsTools Suite

**Source:** https://learn.microsoft.com

Beyond NetBIOS-specific tools, Microsoft's **PsTools** suite is a standard part of enumerating and managing remote Windows systems from the command line. Each tool below is lightweight and generally doesn't require manually installing client software on the target first.

| Tool | Purpose | Syntax |
|---|---|---|
| **PsExec** | A lightweight Telnet replacement; executes processes on other systems with full console interactivity, including launching interactive command prompts and remote-enabling tools like `ipconfig` that otherwise can't show remote info | `psexec [\\computer[,computer2[,...] \| @file]] [-u user [-p psswd]] [-n s] [-r servicename] [-h] [-l] [-s\|-e] [-x] [-i [session]] [-c executable [-f\|-v]] [-w directory] [-d] [-<priority>] [-a n,n,...] cmd [arguments]` |
| **PsFile** | Lists files on a system that were opened remotely; can close them either by name or by file ID. Default behavior lists files opened remotely from the local system | `psfile [\\RemoteComputer [-u Username [-p Password]]] [[Id \| path] [-c]]` |
| **PsGetSid** | Translates SIDs to their display name and vice versa; works on built-in accounts, domain accounts, and local accounts, and can query SIDs remotely across the network | `psgetsid [\\computer[,computer[,...] \| @file] [-u username [-p password]]] [account\|SID]` |
| **PsKill** | Kills processes on remote systems (or locally). Kill by process ID targets just that ID; kill by process name kills every process with that name. No client install needed | `pskill [-] [-t] [\\computer [-u username] [-p password]] <process name \| process id>` |
| **PsInfo** | Gathers key system info about local or remote systems — installation type, kernel build, registered org/owner, processor count/type, physical memory, install date, and (for trial versions) expiration date | `psinfo [[\\computer[,computer[,..] \| @file [-u user [-p psswd]]] [-h] [-s] [-d] [-c [-t delimiter]] [filter]` |
| **PsList** | Displays CPU and memory info, or thread statistics, from the command line | — |
| **PsLoggedOn** | Shows both locally logged-in users and users logged in via resource shares, for either a local or remote computer; if given a username instead of a computer name, it searches the network neighborhood for that user. Determines "locally logged in" by scanning `HKEY_USERS` for profiles loaded into the registry; for share-based logons, it uses the `NetSessionEnum` API | `psloggedon [-] [-l] [-x] [\\computername \| username]` |
| **PsLogList** | Dumps the contents of an Event Log on a local or remote computer — effectively a clone of the older `elogdump` utility, but able to log in to remote systems even where the user's own security credentials wouldn't normally permit Event Log access, and retrieves message strings from the computer where the log is actually stored | `psloglist [-] [\\computer[,computer[,...] \| @file [-u username [-p password]]] [-s [-t delimiter]] [-m #\|-n #\|-h #\|-d #\|-w] [-c] [-x] [-r] [-a mm/dd/yy] [-b mm/dd/yy] [-f filter] [-i ID[,ID[,...] \| -e ID[,ID[,...]]] [-o event source[,event source[,..]]] [-q event source[,event source[,..]]] [-l event log file] <eventlog>` |
| **PsPasswd** | Changes an account password on local or remote systems; admins can batch-run it across many managed machines to mass-change the administrator password. Uses Windows password-reset APIs, so it never sends the password over the network in cleartext | `pspasswd [[\\computer[,computer[,..] \| @file [-u user [-p psswd]]] Username [NewPassword]` |
| **PsShutdown** | Shuts down or reboots a local or remote computer with no manual client install required | `psshutdown [[\\computer[,computer[,..] \| @file [-u user [-p psswd]]] -s\|-r\|-h\|-d\|-k\|-a\|-l\|-o [-f] [-c] [-t nn\|h:m] [-n s] [-v nn] [-e [u\|p]:xx:yy] [-m "message"]` |

Taken together, this suite lets an attacker who already has some level of credentialed access enumerate logged-in users, open files, SIDs, running processes, system info, and event logs across an entire fleet of remote Windows machines — all without touching each box's console directly.

---

**Next:** [`03-snmp-and-ldap-enumeration.md`](03-snmp-and-ldap-enumeration.md) — moving from Windows-native NetBIOS into the two big directory/management protocols, SNMP and LDAP.
