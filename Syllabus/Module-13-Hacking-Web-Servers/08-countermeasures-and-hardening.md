# 08 — Countermeasures & Hardening

> Objective covered: **Explain Web Server Attack Countermeasures**

In previous files we discussed web server attacks, the danger they pose, the methodology attackers follow, and the tools involved. This file covers the **defensive side**: countermeasures, hardening controls, and detection techniques a blue-teamer or system administrator should implement.

## 1. Place Web Servers in a Separate, Secure Network Segment

An ideal web-hosting network should be designed with **three separate segments**: an **internet segment**, a **secure server security segment** (often the DMZ — demilitarized zone), and an **internal network**. The DMZ is isolated from both the public internet and the internal network.

```
   Internet ──> [External Firewall] ──> DMZ ──> [Internal Firewall] ──> Internal Network
                                    (Web Server,                        (Application Server,
                                     FTP Server,                         Mail Server,
                                     etc.)                               Internal DB, etc.)
```
*(Figure 13.62 equivalent — three different segments in a web-hosting network)*

Placing web servers in a separate secure segment allows the administrator to:
- Place firewalls and apply security rules **between** the internal network and the DMZ, and between the DMZ and the outside public network.
- Prevent attacks on the web server by outside attackers **and** by malicious insiders on the internal network.
- Network segmentation divides a network into different segments, each having its own hub/switch, so that if an attacker compromises one network segment, they can't automatically compromise other segments.

## 2. Countermeasures — Patches and Updates

- **Scan** for existing vulnerabilities, and patch/update the server software regularly.
- Before applying any hotfix or security patch, **read and peer-review** all relevant documentation.
- Apply all updates, regardless of their type, on an **"as-needed"** basis.
- **Test** service packs and hotfixes on a representative **non-production** environment prior to deployment in production.
- Ensure that hotfixes and security patch levels are **consistent across all domain controllers (DCs)**.
- Ensure server outages are scheduled, and that a complete set of **backup tapes and emergency repair disks** are available.
- Keep a **back-out plan** that allows the system/enterprise to return to its original state prior to a failed implementation.
- **Disable all unused script extension mappings.**

Additional best practices:
- Conduct an extensive risk assessment to determine which segments of the network are most vulnerable or high-risk and need to be patched first.
- Make a detailed inventory of all endpoints, services, and dependencies.
- While deploying a patch to the full system, ensure it is performed in a testing environment first.
- Deploy an alerting system for patches.
- Use a patch management application or system such as **SolarWinds Patch Manager** to automate the procedure.
- Regularly conduct monitoring and reporting to ensure your patch management processes are performing effectively.
- Reduce exposure to third-party risks by limiting the number of software versions you employ.
- All patch and update operations should be validated and documented for accessibility, analysis, and confirmation.
- Make a standardized patch management and security update methodology as part of the **SDLC**.

> 📖 See [10 — Patch Management](10-patch-management.md) for the complete patch-management lifecycle and tools.

## 3. Countermeasures — Protocols and Accounts

### Protocols

- Block all unnecessary ports, ICMP traffic, and unnecessary protocols.
- Harden the TCP/IP stack and consistently apply the latest patches/updates to system software.
- If insecure protocols such as **Telnet, POP3, and FTP** are used, take appropriate measures to provide secure authentication/communication (e.g. using IPsec policies).
- If remote access is needed, ensure remote connections are secured properly by using **tunneling and encryption protocols**.
- Use secure protocols such as **Transport Layer Security (TLS)/SSL** for communicating with the web server.
- Ensure that unidentified FTP servers operate in an innocuous part of the directory tree that is different from the web server's tree.
- Ensure the HTTP service banner is properly configured to hide the host OS and version type.
- Isolate the supporting servers such as LDAP servers from the local subnet by filtering traffic through a firewall before entering the local network.
- Ensure that all file-transfer applications through the web server are done via FTPS for better data encryption and protection.
- Redirect all HTTP traffic to HTTPS to ensure data is encrypted in transit.
- Use HSTS headers to force browsers to use secure connections, preventing downgrade attacks.
- Automate the renewal process for SSL/TLS certificates to avoid the use of expired certificates.
- Implement rate-limiting to mitigate DDoS attacks that target the SSL/TLS handshake process.

### Accounts

- Remove all unused **modules and application extensions**.
- Disable unused default user accounts created during the installation of the OS.
- When creating a new web root directory, grant the appropriate (**least possible**) NTFS permissions to anonymous users of the IIS web server to access the web content.
- Eliminate unnecessary database users and stored procedures and follow the principle of least privilege for the database application to defend against SQL query poisoning.
- Use secure web permissions, NTFS permissions, and **.NET Framework** access control mechanisms including URL authorization.
- Slow down brute-force and dictionary attacks with strong password policies and implement audits and alerts for login failures.
- Run processes using least-privileged accounts as well as least-privileged services and user accounts.
- Limit the administrator or root-level access to the minimum number of users and maintain a record of user activity.
- Maintain logs of all user activity in an encrypted form on the web server or in a separate machine on the intranet.
- Disable noninteractive accounts that should not require an interactive login.
- Use secure VPN networks such as **OpenVPN** while accessing multi-server platforms and connecting/accessing data from cross-server network models, helps use one account for multiple servers.
- Use secure VPN networks such as OpenVPN when accessing multi-server platforms.
- Use password managers such as **KeePass** to maintain a proper password policy for multiple user accounts.
- Enable the **Separation of Duties (SoD)** feature on the server config settings.
- Force users to periodically change passwords for their accounts by creating a password expiry policy.
- Enable the user account-locking feature by setting a limit on the number of failed login attempts.
- Implement **2FA or MFA** as an additional layer of security for user accounts.
- Use CAPTCHA challenges on login and registration pages to prevent automated bot attacks.
- Use security questions with unpredictable answers and implement 2FA/MFA for account recovery.
- Use strong, one-way hashing algorithms such as **bcrypt, scrypt, or Argon2** to securely store passwords.
- Design secure account-recovery processes that verify a user's identity without exposing the account to takeover risks.

## 4. Countermeasures — Files and Directories

- Eliminate unnecessary files within `.jar` files.
- Disable the serving of directory listings.
- Avoid mapping **virtual directories** between two different servers, or over a network.
- Monitor and check all network service logs, website access logs, database server logs (e.g. Microsoft SQL Server, MySQL, and Oracle), and OS logs frequently.
- Eliminate unnecessary sensitive configuration information between different servers over a network.
- Eliminate non-web files such as archive files, backup files, text files, and header/include files.
- Disable the serving of certain file types by creating a resource map.
- Ensure that web applications/website files or scripts are stored on a partition or drive other than that of the OS, logs, and any other system files.
- Run the web server processes with the least required privileges and give access only to the necessary resources for inputs.
- Employ file-integrity checkers to verify web content and detect intrusion.
- If an application allows file uploads, the uploaded files should be scanned for malware and stored outside the web root.
- Use a **WAF** (web application firewall) to protect against common web-based attacks such as SQL injection, which can lead to unauthorized file access.
- Use **SFTP** instead of FTP to encrypt file transfers.
- Ensure that configuration files (e.g. `.htaccess`, `web.config`) are secure and not accessible from the web.
- Implement version control for web application files to track changes and revert to previous versions if necessary.
- Disable the serving of directory listings, and remove any non-web files from the web root.
- Run the web server within a sandboxed directory for preventing access to system files.
- Avoid all non-web file types from being referenced in a URL.
- Exclude meta characters while processing user inputs.

## 5. Detecting Web Server Hacking Attempts

Use a **Website Change Detection System (WCDS)** to detect hacking attempts on the web server.

**A Website Change Detection System involves:**
1. Running a specific script on the server that detects any changes made to the existing executable file or web content.
2. Periodically comparing the hash values of the files on the server with the intrusion master hash value to detect any changes made to the server.
3. Alerting the user via email if changes are detected on the server.

> **Example: DirectoryMonitor** — an automated tool that goes through all your web folders and detects any changes made to your website and alerts you via an email if changes occur.

An attacker who gains access to a web server by compromising security through known vulnerabilities present in the web server may attempt to plant backdoors (scripts). These backdoors allow the attacker to gain access, launch phishing attacks, or send spam emails. The victim remains unaware of the web server attack until a backdoor is blacklisted on spam mails or until the attacker redirects the visitors of a target site to some other site. Thus, a web server attack is difficult to detect unless malicious events occur. By the time these events occur, it may be too late because the attacker would have already succeeded. Therefore, a mechanism to detect a web server hacking attempt is required to prevent harm in its early stages.

When an attacker installs a backdoor on a web server, the size of files infected with the backdoor automatically increases. A website change detection system is a script that runs on the server to detect any executable file or any content on the web server such as HTML, JavaScript (JS), PHP, Active Server Pages (ASP), Perl, and Python files. It works by periodically comparing the hash values of the files in the codebase. If it detects any change on the server, it alerts the user via email — thus WDS helps in detecting web server hacking attempts in the early stages of an attack.

## 6. How to Defend against Web Server Attacks

### General

- Use a **dedicated machine** as a web server.
- Physically protect the web server machine in a secure location.
- Regularly apply the most recent security patches and updates promptly.
- Do **not** install the IIS server on a domain controller.
- Limit URL mappings to reflect an active web server (be cautious with URL mappings to internal resources).
- Relocate sites and virtual directories to non-system partitions.
- Always protect the global.asa file from anonymous users.
- Configure a separate anonymous user account for each application if hosting multiple web applications.
- Use security auditing tools to support web server functionality and monitor incoming traffic.
- Screen and filter incoming traffic requests.

### Ports

- Regularly monitor all the ports to ensure the server is not vulnerable or in a insecure state.
- Limit inbound traffic to only ports **80 (HTTP)** and **443 (HTTPS)**; traffic to these ports should either be encrypted or otherwise limited to the router that maintains secure web servers.
- Attackers attempt to hide their identity by spoofing the IP address of a legitimate user. By processing the access log file, either using the "deny this IP address" rule in the firewall ruleset file or by creating a "routed blackhole" the target system can defend against web server attacks.

### Server Certificates

- Server certificates guarantee security and are signed by a trusted authority. However, an attacker may compromise certified servers using forged certificates to intercept secure communications by performing MITM attacks. The following are some techniques to avoid such attacks:
  - Use the **direct validation** of certificates.
  - Use a **novel protocol** that does not depend on third parties for certificate validation.
  - Allow domains to directly and securely examine certificates by using previously established user authentication credentials.
  - Use a robust cryptographic construction that enhances server identity validation and resolves the limitations of third-party solutions.
  - Ensure that the certificate data ranges are valid and that certificates are used for their intended purpose.
  - Ensure that the certificate has not been revoked and is valid all the way to a trusted root authority.

### `machine.config`

The `machine.config` file provides a mechanism for securing machine-level settings. It affects all applications running on the machine. The following can be performed with the `machine.config` file:

- Ensure that protected resources are mapped to `HttpForbiddenHandler` and unused `HttpModules` are removed.
- Ensure that tracing is disabled (`<trace enable="false"/>`) and debug compiles are turned off.
- Verify that ASP.NET errors are not returned to the client.
- Verify session-state settings.

### Code Access Security

The following measures can be adopted to ensure code access security:

- Implement secure coding practices to avoid source-code disclosure and input validation attacks.
- Restrict code access security policy settings so that the code is unable to execute code downloaded from the internet or intranet.
- Configure IIS to reject URLs with `../` to prevent path traversal, lockdown system commands and utilities with restrictive access control lists (ACLs), and install new patches and updates.
- If targets do not implement code access security policy settings in their web servers, there is a possibility of the execution of malicious code.

The following are some other measures to defend against web server attacks:
- Apply restricted ACLs and block remote registry administration.
- Secure the SAM (stand-alone servers only).
- Ensure that security-related settings are configured appropriately and that access to the metabase file is restricted with hardened NTFS permissions.
- Remove unnecessary Internet Server Application Programming Interface (ISAPI) filters from the web server.
- Remove all unnecessary file shares, including the default administration shares, if they are not required.
- Secure the shares with restricted NTFS permissions.
- Relocate sites and virtual directories to non-system partitions and use IIS permissions to restrict access.
- Remove all unnecessary IIS script mappings for optional file extensions to avoid exploitation of any bugs in the ISAPI extensions that handle these types of files.
- Enable a minimum level of auditing on the web server and use NTFS permissions to protect log files.
- Use a dedicated machine as a web server.
- Create URL mappings to internal servers cautiously.
- Do not install the IIS server on a domain controller.
- Use server-side session tracking and match connections with timestamps, IP addresses.
- If a database server such as Microsoft SQL Server is used as a backend database, install it on a separate server.
- Use security tools provided with web server software and scanners that automate and simplify the process of securing a web server.
- Physically protect the web server machine in a secure machine room.
- Do not connect an IIS server to the internet until it is fully hardened.
- Do not allow anyone to locally log in to the machine except the administrator.
- Configure a separate anonymous user account for each application if multiple web applications are hosted.
- Limit server functionality to support only the web technologies to be used.
- Screen and filter incoming traffic requests.
- Implement firewalls to control incoming and outgoing network traffic based on security rules.
- Store website files and scripts on a separate partition or drive.
- Use an effective time mitigation service such as DataDome to detect botnets and limit time-based attacks.
- Use network segmentation, VPNs, and secure protocols (such as HTTPS) to limit unauthorized access and encrypted communication.
- Implement role-based access control (RBAC) and the principle of least privilege to minimize the risk of unauthorized activity.
- Deploy IDPS to monitor network traffic and detect unusual or malicious activity.
- Implement centralized log monitoring to track server and application activities. Analyze logs for signs of suspicious behavior.
- Set up alerts for security events and establish an incident-response plan to address security incidents promptly.
- Restrict directory listings and enforce proper file permissions to prevent unauthorized access to sensitive files.
- Turn off unused features, such as server-side scripting or directory browsing, to reduce potential attack vectors.

## 7. How to Defend against HTTP Response-Splitting and Web Cache Poisoning

While setting cookies, remove carriage returns (**CR**s) and linefeeds (**LF**s) before inserting data into an HTTP response header. The best practice is to use third-party products to test for the existence of security holes and defend against CRLF injection. Ensure that application engines are up to date.

The **User Datagram Protocol (UDP)** source-port randomization technique defends against blind response forgery. Limit the number of simultaneous recursive queries and increase the times-to-live (TTLs) of legitimate records.

The following are some methods to defend against HTTP response-splitting attacks and web cache poisoning:

**Server Admin**
- Use the latest web server software.
- Regularly update/patch the OS and web server.
- Run a web vulnerability scanner.

**Application Developers**
- Restrict the web application's access to unique IPs.
- Disallow **CR (`%0d`/`\r`)** and **LF (`%0a`/`\n`)** characters.
- Comply with **RFC 2616** specifications for HTTP/1.1.
- Parse all user inputs or other forms of encoding before using them in HTTP headers.

**Proxy Servers**
- Avoid sharing incoming TCP connections among different clients.
- Use different TCP connections with the proxy for different virtual hosts.
- Implement "maintain request Host header" correctly.

## 8. How to Defend against DNS Hijacking

The following techniques can be used to defend against DNS hijacking:

- Choose an **ICANN-accredited registrar** and encourage them to set a **registrar-lock** on the domain name.
- Safeguard the registrant's account information.
- Include DNS hijacking in incident response and business-continuity planning.
- Use DNS monitoring tools/services to monitor the IP address of the DNS server and set alerts.
- Avoid downloading audio and video codecs and other downloaders from untrusted websites.
- Install an antivirus program and update it regularly.
- Change the default router password that comes with the factory setting.
- Restrict zone transfers and use access control lists (ACLs).
- Enable **Domain Name System Security Extensions (DNSSEC)** — it adds an extra layer that prevents DNS from being spoofed.
- Enforce strong password policies and user management to further enhance security.
- Negotiate **better service-level agreements (SLAs)** from DNS service providers — when signing up for DNS services with DNS providers, learn how to contact them when an issue arises, how to receive good-quality support and response, and whether the DNS server's infrastructure is hardened against attacks.
- **Configure a master–slave DNS** within your network — use the master without internet access, and maintain two slaves so that even if an attacker hacks the master, slave servers will only update when they receive an update from the master.
- **Constant monitoring of DNS servers** — ensures that a domain name returns the correct IP address.
- **Ensure router safety** — change the default username and password of the router. Keep the firmware up-to-date for safety from newly-found vulnerabilities.
- **Use VPN service** — establish virtual private network (VPN)-encrypted tunnels for private communication over the internet. This feature protects messages from eavesdropping and unauthorized access.
- Install firewall protection services to safeguard the original DNS resolvers and filter out rogue DNS resolver traffic.
- Install proper protection systems such as MFA and hardware security to secure access to the DNS servers.
- Install script-blocker extensions in the browser.
- Use only secured and reputed VPN networks instead of free VPN services, which can track your activities and record them for future use.
- Use geolocation verification to detect and alert on unusual access patterns to DNS management interfaces.
- Implement strict access controls for DNS server management using multifactor authentication (MFA) and role-based access control (RBAC).
- Restrict access to DNS servers based on a predefined list of trusted IP addresses.
- Use DNS filtering services or secure DNS providers (such as **Cloudflare** and **Google Public DNS**) that offer built-in security against malicious domains.

---

**Previous:** [← 07 — Web Server Attack Tools](07-web-server-attack-tools.md) · **Next:** [09 — Security Scanning & Monitoring Tools →](09-security-scanning-and-monitoring-tools.md)
