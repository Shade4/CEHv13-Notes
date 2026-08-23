# 03 — SNMP Enumeration and LDAP Enumeration

## Part A: SNMP Enumeration

### 3.1 What SNMP Is and Why It's Enumerable

**SNMP** (Simple Network Management Protocol) lets network administrators manage devices — routers, switches, firewalls, printers, servers — from a remote location. It's an application-layer protocol that runs on UDP, and SNMP agents run on both Windows and Unix networking devices.

The problem, from a security standpoint, is that SNMP ships with several known weaknesses — a notable lack of built-in auditing being one of them. Attackers exploit these weaknesses to enumerate accounts and devices wholesale.

**SNMP enumeration** is the process of building a list of a target's user accounts and devices using SNMP. It relies on two software components talking to each other:
- **SNMP agent** — lives on the networking device itself
- **SNMP management station** — communicates with the agent

Almost every piece of network infrastructure (routers, switches) ships with an SNMP agent for exactly this kind of remote management. The management station sends requests; the agent replies. Both requests and replies operate on configuration variables the agent software exposes — the management station can also *set* values on some of those variables. **Traps** let the agent proactively tell the management station about abnormal events (a reboot, an interface failure) without being asked first.

### 3.2 SNMP Passwords: Community Strings

SNMP uses two passwords to configure and access the agent from the management station:

| String | Purpose | Visibility |
|---|---|---|
| **Read Community String** | View the device/system configuration | Public |
| **Read/Write Community String** | Change or edit the device configuration | Private |

When administrators leave these community strings at their default values, attackers can simply use those known defaults to view — or worse, change — the device's configuration. From here, attackers enumerate SNMP to extract network resource info (hosts, routers, devices, shares) and network info (ARP tables, routing tables, device-specific info, traffic statistics).

Common SNMP enumeration tools: **OpUtils** (https://www.manageengine.com) and **Network Performance Monitor** (https://www.solarwinds.com).

### 3.3 How SNMP Works — The Full Communication Process

SNMP uses a distributed architecture made up of SNMP managers, SNMP agents, and several related components. The manager↔agent communication process runs in four broad stages:

**1. Initialization / Start-Up**
When a network device boots, its SNMP agent initializes its configuration and starts listening for the manager on the designated port — usually **UDP 161**.

**2. Discovery**
The SNMP manager discovers SNMP-enabled devices on the network by sending a request either to the broadcast address or to specific IP addresses where agents are known to live.

**3. Information Exchange**
Manager↔agent communication happens through SNMP messages called **Protocol Data Units (PDUs)**. The key PDU operations:

| PDU | What it does |
|---|---|
| **Get Request** | Manager asks an agent for the value of a specific variable (e.g., a router interface's status, or bandwidth usage on a link) |
| **GetNext Request** | Fetches the *next* variable in the MIB tree — lets the manager walk a sequence of variables without knowing their exact names ahead of time |
| **Set Request** | Manager modifies the value of a variable in the agent's MIB, effectively changing the device's configuration/behavior |
| **GetBulk Request** | Introduced in SNMPv2; retrieves large volumes of data in a single request, far more efficiently than issuing many individual GetNext requests |
| **Response** | Sent by the agent after handling a Get/GetNext/Set/GetBulk request; carries the requested values or an acknowledgment of the action taken |
| **Inform Request** | Agent sends unsolicited info to the manager about significant events/errors — also used for manager-to-manager communication |
| **Trap** | Unsolicited message from an agent to the manager flagging a significant event/change (device reboot, link failure). **SNMPv3** generalized Traps and Informs under the umbrella term **Notifications**, adding authentication and encryption |

**4. Monitoring and Management**
The manager uses everything collected from agents to monitor performance, detect/diagnose issues, and remotely configure devices — an ongoing loop of regular polling (Get Requests) plus passive listening for Traps/Informs.

### 3.4 Management Information Base (MIB)

The **MIB** is a virtual database holding a formal description of every network object SNMP manages — a hierarchically organized collection of information providing a standard representation of an SNMP agent's data and storage. Every MIB element is identified by an **object identifier (OID)** — a numeric name that begins at the root of the MIB tree and uniquely identifies that object within the hierarchy.

MIB-managed objects fall into two types:
- **Scalar objects** — define a single object instance
- **Tabular objects** — define a group of related object instances

OIDs carry the object's type (counter, string, address, etc.), access level (read or read/write), size restrictions, and range info. The SNMP manager translates raw OIDs into a human-readable display using the MIB as a kind of codebook.

You can browse MIB contents through a web browser via `http://IP.Address/Lseries.mib` or `http://library_name/Lseries.mib`. Microsoft ships a list of MIBs installed with the SNMP service in the Windows resource kit:

| MIB | Purpose |
|---|---|
| **DHCP.MIB** | Monitors network traffic between DHCP servers and remote hosts |
| **HOSTMIB.MIB** | Monitors and manages host resources |
| **LNMIB2.MIB** | Contains object types for workstation and server services |
| **MIB_II.MIB** | Manages TCP/IP-based Internet using a simple architecture and system |
| **WINS.MIB** | For the Windows Internet Name Service (WINS) |

### 3.5 Enumerating SNMP Using SnmpWalk

**Source:** https://ezfive.com

**SnmpWalk** is a command-line tool that lets an attacker instantly scan a large number of SNMP nodes and identify which variables are available for accessing the target network. By targeting the root node, an attacker can pull information from every sub-node (routers, switches) beneath it. Retrieved data comes back as OIDs, which are part of the MIB tied to any device with SNMP enabled.

```bash
snmpwalk -v1 -c public <Target IP Address>
```

This dumps every OID, variable, and associated piece of information the agent exposes — up to and including in-transit data heading to the SNMP server, such as the server being used, user credentials, and other parameters.

Sample partial output:
```
iso.3.6.1.2.1.1.1.0 = STRING: "Hardware: Intel64 Family 6 Model 85 Stepping 7 AT/AT COMPATIBLE
- Software: Windows Version 6.3 (Build 20348 Multiprocessor Free)"
iso.3.6.1.2.1.1.2.0 = OID: iso.3.6.1.4.1.311.1.1.3.1.3
iso.3.6.1.2.1.1.3.0 = Timeticks: (2889990469) 334 days, 11:45:04.69
iso.3.6.1.2.1.1.5.0 = STRING: "Server2022.CEH.com"
iso.3.6.1.2.1.1.7.0 = INTEGER: 76
```

**Other useful SnmpWalk commands:**

```bash
# Enumerate SNMPv2 with community string 'public'
snmpwalk -v2c -c public <Target IP Address>

# Search for installed software
snmpwalk -v2c -c public <Target IP Address> hrSWInstalledName

# Determine the amount of RAM on the host
snmpwalk -v2c -c public <Target IP Address> hrMemorySize

# Change an OID to a different value
snmpwalk -v2c -c public <Target IP Address> <OID> <New Value>

# Change the sysContact OID
snmpwalk -v2c -c public <Target IP Address> sysContact <New Value>
```

### 3.6 Enumerating SNMP Using Nmap

**Source:** https://nmap.org

Attackers use the `snmp-processes` NSE script against a remote SNMP server to retrieve information about hosted SNMP services:

```bash
nmap -sU -p 161 --script=snmp-processes <Target IP Address>
```
Returns a list of all running SNMP processes and their associated ports on the target host.

**Other useful Nmap SNMP commands:**
```bash
# Retrieve SNMP server type and OS details
nmap -sU -p 161 --script=snmp-sysdescr <Target IP Address>

# Retrieve a list of all applications running on the target machine
nmap -sU -p 161 --script=snmp-win32-software <Target IP Address>
```

### 3.7 SNMP Enumeration Tools

SNMP enumeration tools scan a single IP or range of IPs of SNMP-enabled devices to monitor, diagnose, and troubleshoot security threats.

**snmp-check (snmp_enum module)** — https://www.nothink.org
An open-source tool (GPL-licensed) that automates gathering info on any SNMP-supporting device (Windows, Unix-like, network appliances, printers). Output is human-readable/pen-test-friendly. Attackers use it to gather details on: contact, description, write access, devices, domain, hardware/storage info, hostname, IIS statistics, IP forwarding, listening UDP ports, location, mountpoints, network interfaces, network services, routing info, software components, system uptime, TCP connections, total memory, uptime, and — critically — **user accounts**.

```bash
snmp-check 10.10.1.22
```
Example output includes a full "System information" block (hostname, description, contact, location, uptime, system date, domain) followed by a `[*] User accounts:` section listing real account names pulled straight off the target (e.g., `Guest`, `jason`, `Martin`, `Shiela`, `krbtgt`, `Administrator`) — as well as network information (IP forwarding status, default TTL, TCP segment counts) and network interfaces (loopback, tunneling adapters, speeds, MTU).

**SoftPerfect Network Scanner** — https://www.softperfect.com
Pings computers, scans ports, discovers shared folders, and retrieves practically any info about network devices via WMI, SNMP, HTTP, SSH, and PowerShell. Also scans remote services, registry, files, and performance counters; offers flexible filtering/display; exports results to XML/JSON and other formats. Can check whether a user-defined port is open, resolve host names, auto-detect local/external IP ranges, and supports remote shutdown and Wake-on-LAN. Attackers use it to gather info about shared folders and network devices — including right-clicking a discovered device to open it directly as Web (HTTP), Secure Web (HTTPS), an FTP file server, Telnet, or via Computer Management/Remote Desktop.

**Additional SNMP enumeration tools:**
| Tool | Source |
|---|---|
| Network Performance Monitor | https://www.solarwinds.com |
| OpUtils | https://www.manageengine.com |
| PRTG Network Monitor | https://www.paessler.com |
| Engineer's Toolset | https://www.solarwinds.com |

### 3.8 SNMP Enumeration with AI

Attackers can prompt an AI shell-assistant to drive SnmpWalk, Nmap, or Metasploit automatically. Examples from the source material:

**Prompt:** *"Perform SNMP enumeration on target IP 10.10.1.22 using SnmpWalk and display the result here"*
```bash
snmpwalk -c public -v1 10.10.1.22
```

**Prompt:** *"Perform SNMP enumeration on target IP 10.10.1.22 using nmap and display the result here"*
```bash
nmap -sU -p 161 --script snmp-info 10.10.1.22
```

**Prompt:** *"Perform SNMP processes on target IP 10.10.1.22 using nmap and display the result here"*
```bash
nmap -sU -p 161 --script snmp-processes 10.10.1.22
```
Sample output lists running processes (`System Idle Process`, `System`, `Registry`, `svchost.exe`) along with their paths and startup parameters — e.g., `svchost.exe` shown running with `Path: C:\Windows\system32\` and `Params: -k DcomLaunch -p -s LSM`.

---

## Part B: LDAP Enumeration

### 3.9 What LDAP Is

Various protocols carry valuable information about network resources alongside the data they transport, and an attacker who successfully manipulates one of those protocols can break into the network or misuse its resources. **LDAP** (Lightweight Directory Access Protocol) is exactly this kind of protocol — it accesses directory listings within Active Directory or other directory services.

LDAP is a **hierarchical/logical** directory structure — similar in shape to a company's organizational chart. Directory services can hold any organized set of records, often hierarchically structured, such as a corporate email directory. LDAP uses DNS for quick lookups and fast query resolution.

A client starts an LDAP session by connecting to a **Directory System Agent (DSA)**, typically on **TCP port 389**, and sends an operation request to the DSA. Information travels between client and server using the **Basic Encoding Rules (BER)** format.

**The vulnerability:** an attacker can anonymously query the LDAP service for sensitive information — usernames, addresses, departmental details, and server names — all of which feeds directly into a follow-on attack.

### 3.10 Manual LDAP Enumeration (Python)

Attackers can perform LDAP enumeration by hand using Python and the `ldap3` library.

**Step-by-step:**

1. Using Nmap, check whether the target LDAP server is listening on **port 389** for LDAP, or **port 636** for secure LDAP.
2. If the target is listening, install the LDAP library:
   ```bash
   pip3 install ldap3
   ```
3. Create a server object, specifying the target IP/hostname and port. If the target is listening on secure LDAP, add `use_ssl = True`.
4. Retrieve the DSA-specific entry (DSE) naming contexts by specifying `get_info = ldap3.ALL`.
5. Create a connection object and call `bind()`.
6. If the bind succeeds, `True` is printed:
   ```python
   >>> import ldap3
   >>> server = ldap3.Server('Target IP Address', get_info=ldap3.ALL, port=389)
   >>> connection = ldap3.Connection(server)
   >>> connection.bind()
   True
   ```
7. Fetch the domain name and naming context:
   ```python
   >>> server.info
   ```
   Example output:
   ```
   DSA info (from DSE):
     Supported LDAP versions: 3, 2
     Naming contexts:
       DC=CEH,DC=com
       CN=Configuration,DC=CEH,DC=com
       CN=Schema,CN=Configuration,DC=CEH,DC=com
       DC=DomainDnsZones,DC=CEH,DC=com
       DC=ForestDnsZones,DC=CEH,DC=com
     Supported controls:
       1.2.840.113556.1.4.1338 - Verify name - Control - MICROSOFT
       1.2.840.113556.1.4.1339 - Domain scope - Control - MICROSOFT
       1.2.840.113556.1.4.1340 - Search options - Control - MICROSOFT
       ...
   ```
8. Retrieve all directory objects using the naming context you just found:
   ```python
   >>> connection.search(search_base='DC=CEH,DC=com',
                          search_filter='(&(objectClass=*))',
                          search_scope='SUBTREE',
                          attributes='*')
   True
   >>> connection.entries
   ```
   This returns detailed directory-object data — auditing policy, creation time, `dSASignature`, `distinguishedName`, `fSMORoleOwner`, `forceLogoff`, group policy links, `lockoutDuration`/`lockoutThreshold`, `maxPwdAge`/`minPwdAge`/`minPwdLength`, machine-account quota, trust quota, and more.
9. To dump credentials specifically, target the `person` object class and the `userPassword` attribute:
   ```python
   >>> connection.search(search_base='DC=DOMAIN,DC=DOMAIN',
                          search_filter='(&(objectClass=person))',
                          search_scope='SUBTREE',
                          attributes='userPassword')
   True
   >>> connection.entries
   ```

### 3.11 Automated LDAP Enumeration

**Source:** https://nmap.org

Attackers use the **`ldap-brute` NSE script** to brute-force LDAP authentication. By default it uses a built-in username/password list; the `userdb` and `passdb` script arguments let you swap in custom lists.

```bash
nmap -p 389 --script ldap-brute --script-args ldap.base='"cn=users,dc=CEH,dc=com"' <Target IP Address>
```

Sample output shows every brute-forced combination that returned valid (often blank) credentials:
```
389/tcp open  ldap
| ldap-brute:
|   cn=root,cn=users,dc=CEH,dc=com:<empty> => Valid credentials
|   cn=admin,cn=users,dc=CEH,dc=com:<empty> => Valid credentials
|   cn=administrator,cn=users,dc=CEH,dc=com:<empty> => Valid credentials
|   cn=webadmin,cn=users,dc=CEH,dc=com:<empty> => Valid credentials
|   cn=sysadmin,cn=users,dc=CEH,dc=com:<empty> => Valid credentials
|   cn=netadmin,cn=users,dc=CEH,dc=com:<empty> => Valid credentials
|   cn=guest,cn=users,dc=CEH,dc=com:<empty> => Valid credentials
|   cn=user,cn=users,dc=CEH,dc=com:<empty> => Valid credentials
|   cn=web,cn=users,dc=CEH,dc=com:<empty> => Valid credentials
|_  cn=test,cn=users,dc=CEH,dc=com:<empty> => Valid credentials
```

### 3.12 LDAP Enumeration Tools

**Softerra LDAP Administrator** — https://www.ldapadministrator.com
An LDAP administration tool that works with LDAP servers such as Active Directory, Novell Directory Services, and Netscape/iPlanet — browses and manages LDAP directories. Attackers use it to enumerate user details (username, email address, department) organized by OU (e.g., Berlin/London/New York/Paris/Tokyo offices) and account status (Disabled/Enabled).

### `ldapsearch`

**Source:** https://linux.die.net

`ldapsearch` is a shell-accessible interface to the `ldap_search_ext(3)` library call. It opens a connection to an LDAP server, binds to it, and performs a search using the parameters you specify. The filter must conform to the string representation defined in **RFC 4515**; if you don't supply one, the default filter `(objectClass=*)` is used.

If `ldapsearch` finds one or more entries, the attributes named by `attrs` are returned:
- `*` → all user attributes
- `+` → all operational attributes
- no `attrs` listed → all user attributes (same as `*`)
- `1.1` only → no attributes at all

Results print in an extended version of **LDAP Data Interchange Format (LDIF)**; the `-L` option controls output format.

**Command reference:**
```bash
# Simple authentication search
ldapsearch -h <Target IP Address> -x

# Obtain naming-context details
ldapsearch -h <Target IP Address> -x -s base namingcontexts

# Query the primary domain, once identified (e.g. DC=htb,DC=local)
ldapsearch -h <Target IP Address> -x -b "DC=htb,DC=local"

# Retrieve info about a specific object class
ldapsearch -h <Target IP Address> -x -b "DC=htb,DC=local" '(objectClass=Employee)'

# Retrieve info about every object in the directory tree
ldapsearch -x -h <Target IP Address> -b "DC=htb,DC=local" "objectclass=*"

# Retrieve a list of users belonging to a particular object class
ldapsearch -h <Target IP Address> -x -b "DC=htb,DC=local" '(objectClass=Employee)' sAMAccountName sAMAccountType
```

Example run:
```bash
ldapsearch -H ldap://10.10.1.22 -x -s base namingcontexts
```
```
# extended LDIF
# LDAPv3
# base <> (default) with scope baseObject
# filter: (objectclass=*)
# requesting: namingcontexts

dn:
namingcontexts: DC=CEH,DC=com
namingcontexts: CN=Configuration,DC=CEH,DC=com
namingcontexts: CN=Schema,CN=Configuration,DC=CEH,DC=com
namingcontexts: DC=DomainDnsZones,DC=CEH,DC=com
namingcontexts: DC=ForestDnsZones,DC=CEH,DC=com

# search result
search: 2
result: 0 Success

# numResponses: 2
```

**Additional LDAP enumeration tools:**
| Tool | Source |
|---|---|
| AD Explorer | https://docs.microsoft.com |
| LDAP Admin Tool | https://www.ldapsoft.com |
| LDAP Account Manager | https://www.ldap-account-manager.org |
| LDAP Search | https://securityxploded.com |

---

**Next:** [`04-ntp-and-nfs-enumeration.md`](04-ntp-and-nfs-enumeration.md) — two services that are easy to overlook but leak a surprising amount of network detail.
