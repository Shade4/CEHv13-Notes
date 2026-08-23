# 07 — Enumeration Countermeasures

Having covered the techniques and tools attackers use to extract valuable information from targets, this file closes the loop with the countermeasures that prevent attackers from enumerating sensitive information from a network or host. It focuses on avoiding information leakage through SNMP, LDAP, NFS, SMTP, SMB, and DNS.

## 7.1 SNMP Enumeration Countermeasures

- Remove the SNMP agent, or turn off the SNMP service entirely, if it isn't needed.
- If turning off SNMP isn't an option, change the default community string names away from `public`/`private`.
- Upgrade to **SNMPv3**, which encrypts passwords and messages.
- Implement the Group Policy security option **"Additional restrictions for anonymous connections."**
- Ensure access to null session pipes, null session shares, and IPsec filtering is restricted.
- Block access to TCP/UDP port 161.
- Don't install the management and monitoring Windows component unless it's actually required.
- Encrypt or authenticate using IPsec.
- Never misconfigure the SNMP service with read-write authorization when read-only would do.
- Configure access-control lists (ACLs) for all SNMP connections, allowing only legitimate users to reach SNMP devices.
- Limit SNMP access to only the specific IP addresses or networks that genuinely require it for management — via ACLs on the devices themselves or through network firewalls.
- Regularly audit network traffic.
- Encrypt credentials using **"AuthNoPriv"** mode, which uses MD5 and SHA for additional protection.
- Modify the registry to allow only restricted/permitted access to the SNMP community name.
- Change the default password, and periodically rotate the current one.
- Identify every SNMP device with read/write permissions, and scope those down to read-only wherever read/write isn't actually needed.
- Avoid the **"NoAuthNoPriv"** mode — it doesn't encrypt communications at all.
- Implement role-based access control (RBAC) policies for SNMP communities/users.
- Configure SNMPv3 users in the cluster to add encryption and authentication.
- For devices still stuck on SNMPv1/SNMPv2c, change the default community strings (the SNMP equivalent of passwords) from `public`/`private` to complex, unique values, and restrict write access as much as possible.
- Keep management traffic, including SNMP, on a separate, secure VLAN or network segment — this limits SNMP's exposure to eavesdroppers/attackers on the main network.
- If SNMP isn't needed for network management tasks at all, consider disabling it entirely on devices, removing it as a potential information source outright.
- Apply manufacturer security updates promptly — they routinely patch newly discovered SNMP vulnerabilities.
- Implement monitoring and anomaly-detection tooling to flag unusual SNMP traffic patterns, which can indicate enumeration or other malicious activity.
- Ensure SNMP access is logged, and regularly audit those logs for unauthorized access attempts or suspicious activity.

## 7.2 LDAP Enumeration Countermeasures

- By default, LDAP traffic is transmitted **unsecured** — use SSL or STARTTLS to encrypt it.
- Select a username different from your email address, and enable account lockout.
- Restrict access to Active Directory (AD) using software such as Citrix.
- Use NT LAN Manager (NTLM), Kerberos, or any basic authentication mechanism to limit access to legitimate users.
- Log access to Active Directory (AD) services.
- Block users from accessing certain AD entities by adjusting permissions on those objects/attributes.
- Deploy **canary accounts** — decoy accounts that resemble real ones — to mislead attackers.
- Create decoy groups with the word **"Admin"** in the name to mislead attackers, since attackers routinely search for LDAP admin accounts specifically.
- Enable multi-factor authentication (MFA) for accessing LDAP directories — a strong additional layer against unauthorized access via compromised credentials.
- Disable anonymous binds to the LDAP directory unless absolutely necessary for business operations, so only authenticated users can query the server.
- Configure ACLs to limit what authenticated users can see and do, based on credentials and need-to-know.
- Ensure all LDAP queries and modifications are logged; regularly review these logs for unusual or unauthorized access patterns that could indicate enumeration or other malicious activity.
- Employ monitoring tools capable of detecting abnormal LDAP query patterns, so admins get real-time alerts on potential enumeration/attack attempts.
- Place LDAP servers within a secure network segment, accessible only to the systems and users that genuinely require access — this limits both the attack surface and the potential for unauthorized access.
- Configure firewalls to restrict LDAP traffic to and from authorized systems only, including blocking unnecessary external access to LDAP services.
- Enforce strong password policies for any accounts with LDAP access, minimizing the risk of brute-force or credential-stuffing attacks.

## 7.3 NFS Enumeration Countermeasures

- Implement proper permissions on exported file systems — read/write access must be restricted to specific users.
- Implement firewall rules to block NFS port 2049.
- Ensure proper configuration of files such as `/etc/smb.conf`, `/etc/exports`, and `/etc/hosts.allow` to protect the data stored on servers.
- Review and update the `/etc/exports` file regularly to ensure only authorized hosts can access shared directories.
- Use `/etc/hosts.allow` and `/etc/hosts.deny` to define which hosts/networks are allowed or denied access to NFS services.
- Log requests to access system files on the NFS server.
- Keep the `root_squash` option in `/etc/exports` turned **ON**, so no requests made as root on the client are trusted at face value.
- Implement NFS tunneling through SSH to encrypt NFS traffic over the network.
- Implement the principle of least privilege to mitigate threats such as data modification, data addition, and modification of configuration files by normal users.
- Ensure users are not running `suid` and `sgid` on the exported file system.
- Ensure the NIS netgroup has a fully defined hostname, preventing the granting of higher access to other hosts.
- Configure a deep packet inspection (DPI) firewall to monitor all NFS traffic, irrespective of port number.
- Implement Kerberos authentication for NFS so both client and server authenticate each other securely, helping prevent unauthorized access.
- Migrate to **NFSv4**, which includes stronger security features than earlier versions, including the ability to use Kerberos for encryption and authentication.
- Keep NFS servers and clients within a secure, segmented part of the network to limit access from unauthorized network segments.
- Configure firewalls to restrict NFS traffic to and from authorized systems only — this blocks unnecessary external access and prevents unauthorized discovery/access.
- Regularly monitor NFS server access logs for unusual access patterns or attempts from unauthorized hosts, enabling early detection of enumeration or attack attempts.
- Use file-system auditing tools to monitor and log access to NFS shares, helping identify unauthorized access or modifications to sensitive files.
- Regularly update and patch NFS server software and client systems to protect against known vulnerabilities that could be exploited during enumeration or attacks.

## 7.4 SMTP Enumeration Countermeasures

Configure SMTP servers to:
- Ignore email messages sent to unknown recipients.
- Exclude sensitive mail-server and local-host information from mail responses.
- Disable the open relay feature.
- Limit the number of accepted connections from a single source, to prevent brute-force attacks.
- Disable the `EXPN`, `VRFY`, and `RCPT TO` commands entirely, or restrict them to authenticated users only.
- Identify spammers through machine learning (ML) solutions.
- Avoid sharing internal IP/host information or mail-relay system information.
- Implement **SPF** (sender policy framework), **DKIM** (domain keys identified mail), and **DMARC** (domain-based message authentication, reporting & conformance).
- Configure the SMTP server to give limited information in error messages — overly verbose responses can hand an attacker clues about server configuration or valid user accounts.
- Use ACLs to restrict certain SMTP commands to authorized users or IP addresses, preventing anonymous/unauthorized enumeration attempts.
- Require authentication before allowing access to any information or the ability to send email — this helps prevent anonymous enumeration.
- Use TLS to encrypt communication with the SMTP server, so any data exchanged — including authentication credentials — stays encrypted.
- Ensure the SMTP server logs access attempts and commands used; review these logs regularly for suspicious activity or attempted enumeration.
- Use security tools that can analyze log files and flag unusual patterns of behavior, such as a high number of failed login attempts.
- Use firewalls to control access to the SMTP server, allowing only trusted IP addresses/networks to connect.
- Implement rate limiting to restrict how many requests a single IP address can make to the SMTP server within a given timeframe, helping mitigate brute-force attacks.

## 7.5 SMB Enumeration Countermeasures

Common sharing services (or any other unused service) can provide entry points for attackers to evade network security. A network running SMB is at high risk of enumeration. Because web and DNS servers don't need SMB at all, it's advisable to disable it on them outright — done by disabling the properties **"Client for Microsoft Networks"** and **"File and Printer Sharing for Microsoft Networks"** in Network and Dial-up Connections. On internet-facing servers (bastion hosts), the same two properties can be disabled in the **TCP/IP properties** dialog box. Alternatively, without explicitly disabling SMB, you can just block the ports SMB uses — **TCP 139 and 445**.

Because disabling SMB entirely isn't always feasible, other countermeasures matter too. Windows Registry can be configured to limit anonymous access from the internet to a specified set of files/folders, via the settings **"Network access: Named pipes that can be accessed anonymously"** and **"Network access: Shares that can be accessed anonymously."** This is done by adding the **`RestrictNullSessAccess`** parameter to the registry key:

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters
```

`RestrictNullSessAccess` takes a binary value — **1** enables the restriction, **0** disables it. Setting it to 1 restricts anonymous users to only the files specified in the Network access settings above.

**Additional SMB countermeasures:**
- Ensure Windows Firewall (or a comparable endpoint protection system) is enabled.
- Install the latest security patches for Windows and third-party software.
- Implement a proper authentication mechanism with a strong password policy.
- Implement strong permissions to keep stored information safe.
- Perform regular audits of system logs.
- Perform active system monitoring to catch malicious activity.
- Implement secure VPNs to protect organizational data during remote access.
- Employ file behavioral analysis systems such as next-generation firewalls (NGFWs) to observe traffic patterns and get timely analysis reports on SMB resources.
- Employ highly robust, secure monitoring systems (e.g., global threat sensors) for highly sensitive/top-secret data.
- Implement digitally signed data transmission and communication for accessing SMB resources.
- Block/disable TCP ports 88, 139, and 445, and UDP ports 88, 137, and 138, to prevent SMB attacks.
- Enable public profile settings in the firewall system.
- Block/disable the SMB protocol on internet-facing servers.
- Ensure SMB convention web confronting and DNS mainframes are disabled.
- Ensure all systems use **SMBv3 or higher**, which includes stronger security features including encryption; avoid SMBv1, which is outdated and vulnerable.
- Configure ACLs to restrict access to SMB shares to only the users who actually require it, and review/tighten permissions regularly.
- Use the least-privilege principle so users and services operate with only the minimum permissions necessary, reducing the potential impact if an account is compromised.
- Configure SMB servers to log access attempts and changes to shared resources; regularly review those logs for suspicious activity.

## 7.6 DNS Enumeration Countermeasures

- **Restrict resolver access:** Ensure the resolver can be reached only by hosts inside the network, to prevent external cache poisoning.
- **Randomize source ports:** Ensure request packets leaving the network use random ports rather than the fixed UDP port 53; also randomize query IDs and vary the alphabet case of domain names to defend against cache poisoning.
- **Audit DNS zones:** Regularly audit DNS zones to identify vulnerabilities in domains and subdomains and address DNS-related issues.
- **Patch known vulnerabilities:** Keep nameserver software — BIND, Microsoft DNS — updated to the most recent versions.
- **Monitor nameservers:** Watch nameserver behavior to identify malicious activity or unexpected behavior as early as possible.
- **Restrict DNS zone transfers:** Restrict zone transfers to specific slave nameserver IP addresses, since a zone transfer can hand over a master copy of the primary server's entire database; disable zone transfers to untrusted hosts altogether.
- **Use different servers for authoritative and resolving functions:** Separating resolver duties from authoritative-nameserver duties reduces overload and helps prevent DoS attacks on domains.
- **Use isolated DNS servers:** Avoid hosting the application server alongside the DNS server; use an isolated, dedicated server for DNS to minimize the risk of web application attacks.
- **Disable DNS recursion:** Disable recursion in the DNS server configuration to restrict queries from other/third-party domains and mitigate DNS amplification and poisoning attacks.
- **Harden the OS:** Close unused ports and block unnecessary services on the DNS server host.
- **Use a VPN:** Use a VPN for secure communication, and change default passwords.
- **Implement two-factor authentication:** Enforce 2FA for secure access when a DNS server is managed by a third party.
- **Use DNS change lock:** Use DNS change lock or client lock to restrict alterations to DNS settings without appropriate authorization.
- **Use DNSSEC:** Implement DNSSEC as an additional layer of security, allowing only digitally signed DNS requests and mitigating DNS hijacking.
- **Use premium DNS registration:** Hide sensitive information such as host information (HINFO) from the public via premium DNS registration services.
- **Secure DNS queries/encrypt DNS traffic:** Consider DNS-over-HTTPS (DoH) or DNS-over-TLS (DoT) to encrypt DNS queries and responses, helping prevent eavesdropping and man-in-the-middle attacks that could facilitate enumeration.
- **Enable DNS logging and monitoring:** Log queries and responses on DNS servers; regular monitoring/analysis of these logs helps identify suspicious patterns that may indicate enumeration attempts.
- **Employ anomaly detection:** Automatically flag unusual DNS query volumes or patterns that could signify enumeration or other DNS attacks.
- **Implement rate limiting:** Configure DNS servers to limit the rate of accepted queries from individual IP addresses, mitigating brute-force enumeration techniques.
- **Split DNS architecture:** Handle internal DNS queries with a separate DNS server from the one handling external queries, limiting how much internal network structure is exposed to the outside world.
- **Use minimal DNS information:** Be cautious about how much information you expose through DNS records — for instance, avoid descriptive subdomain names that reveal internal network details or server purposes.

**Other DNS enumeration countermeasures:**
- Ensure private hosts and their IP addresses are never published in the DNS zone files of the public DNS server.
- Use standard network-admin contacts for DNS registrations, to avoid social-engineering attacks.
- Prune DNS zone files to avoid revealing unnecessary information.
- Maintain independent internal and external DNS servers.
- Ensure old/unused DNS records are deleted periodically.
- Restrict `version.bind` request queries using ACLs; remove or run BIND with least privilege.
- Use the `/etc/hosts` file for development or staging of subdomains, instead of publishing DNS records for them.
- Deploy DNS firewalls to block malicious queries and protect against DNS-based threats, using threat intelligence to identify and prevent communication with known malicious domains.
- Periodically review and audit DNS configurations to ensure they're secure and that only the necessary DNS information is exposed to the public.

---

## Module Recap

Across this module, you've worked through:

1. **Concepts** — what enumeration is, how it differs from scanning, the extraction techniques attackers rely on, and the full services/ports reference.
2. **NetBIOS enumeration** — name tables, `nbtstat`, dedicated tools, and the PsTools suite for deeper remote-system control.
3. **SNMP and LDAP enumeration** — SNMP's manager/agent/MIB/OID architecture and SnmpWalk/Nmap tooling; LDAP's DSA sessions and both manual (Python) and automated (Nmap, `ldapsearch`) enumeration.
4. **NTP and NFS enumeration** — the four NTP command-line utilities (`ntpdate`, `ntptrace`, `ntpdc`, `ntpq`) and NFS's `rpcinfo`/`showmount` workflow.
5. **SMTP and DNS enumeration** — the VRFY/EXPN/RCPT TO trio for SMTP, and DNS's rich toolkit (zone transfer, cache snooping, DNSSEC zone walking, OWASP Amass, Nmap DNS/DNSSEC scripts).
6. **IPsec, VoIP, RPC, Unix/Linux, and SMB enumeration** — the remaining protocol-specific techniques, capped off with AI-generated end-to-end automation scripts.
7. **Countermeasures** — the defensive playbook for every service covered above.

**What comes next (per the source curriculum):** Module 05 — **Vulnerability Analysis**, covering how attackers, as well as ethical hackers and pen testers, identify security loopholes in a target organization's network, communication infrastructure, and end systems.
