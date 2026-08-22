# 07 — Network Scanning Countermeasures

## 7.1 Why This Matters for a Pen Tester, Not Just a Defender

Part of what separates an ethical hacker from an attacker is this exact section: after finding the vulnerabilities a scan reveals, the "pen tester" role also requires recommending — or implementing — the countermeasures that close them. Knowing every scan type from files `03`–`06` is only half the job; knowing how to detect and block each one is the other half, and it's often what actually goes in the client-facing report.

## 7.2 Ping Sweep Countermeasures

Defenses aimed specifically at ICMP-based host discovery (file `03`, §3.4):

- Configure firewalls to block incoming ICMP echo requests from unknown or untrusted sources.
- Deploy an IDS/IPS — e.g., **Snort** (https://www.snort.org) — specifically tuned to detect and prevent ping-sweep attempts.
- Carefully evaluate the type and volume of ICMP traffic flowing through the enterprise network rather than treating all ICMP the same.
- Terminate the connection with any host sending more than 10 ICMP ECHO requests — a volume threshold well beyond normal diagnostic use.
- Use a DMZ, and inside it allow only the minimum necessary ICMP message types — specifically `ICMP_ECHO_REPLY`, `HOST_UNREACHABLE`, and `TIME_EXCEEDED`.
- Limit ICMP traffic with access-control lists (ACLs) scoped to the ISP's specific IP addresses, rather than leaving ICMP open to the entire Internet.
- Implement rate limiting for ICMP packets, reducing how effective ping sweeps and other ICMP-based scanning techniques can be.
- Break the network into smaller, isolated segments — this limits how much an attacker can discover via a single sweep and makes lateral movement harder if a segment is compromised.
- Use private IP address ranges internally and implement NAT at the network boundary, hiding internal addressing from external observers entirely.

## 7.3 Port Scanning Countermeasures

Port scanning hands an attacker a large amount of directly actionable information — IP addresses, hostnames, open ports, and the exact services running on them — so hardening this layer matters a lot:

- Configure firewall and IDS rules to detect and block probe attempts; the firewall should inspect the *contents* of each packet before allowing it through, not just permit traffic wholesale after a shallow TCP-header check.
- Periodically run port-scanning tools against your own hosts to verify the firewall is actually catching the scanning activity you'd expect it to catch — trust, but verify.
- Keep router, IDS, and firewall firmware updated to their latest releases/versions.
- Configure commercial firewalls specifically to defend against fast port scans and SYN floods.
- Deploy an IDS such as **Snort** — public, frequently updated signatures make it a strong, well-supported baseline.
- Ensure routing/filtering mechanisms at routers and firewalls **cannot be bypassed** via a specific source port or a source-routing trick (file `06`, §6.3–6.4).
- Keep as few ports open as possible, and filter the rest with a custom rule set — a good baseline blocklist mentioned in the source material includes ports **135–159, 256–258, 389, 445, 1080, 1745, and 3268**.
- Block unwanted services running on any open ports, and keep the versions of services that *do* need to stay open current/non-vulnerable.
- Block inbound ICMP message types and all outbound ICMP type-3 (unreachable) messages at the border routers in front of the organization's main firewall.
- Test your own IP address space with TCP and UDP port scans, plus ICMP probes, to understand exactly what an external attacker would see of your network configuration.
- Verify anti-scanning and anti-spoofing rules are properly configured.
- For any commercial firewall in use: confirm it's patched with the latest updates, has correctly defined anti-spoofing rules, and that its "fast-mode" services (if any) are disabled/unusable.
- Use TCP wrappers to limit network access based on domain name or IP address.
- Use proxy servers to block fragmented or malformed packets before they reach internal hosts.
- Configure firewalls to forward open-port scans toward empty hosts or honeypots, making the reconnaissance phase deliberately slow and unproductive for the scanning party.
- Employ an intrusion prevention system (IPS) to identify port-scan attempts and blacklist the offending IP addresses.
- Implement **port knocking** to keep ports hidden until a correct "knock" sequence is received.
- Use NAT to hide the real IP addresses of internal systems.
- Implement egress filtering on outbound traffic — this both controls what leaves the network and helps identify/stop compromised internal hosts that are themselves scanning external targets.
- Implement VLANs to isolate different types of traffic and restrict access between segments.
- Implement dynamic IPv6 address variation with a random address generator, shrinking the window of time any one address stays exploitable.
- Configure routers to send encoded information about fragmented packets entering the network.
- Configure routers to verify incoming data packets using stored digests of previously-seen packet signatures.
- Configure routers to hide intranet hosts from the external network via NAT.
- Configure internal switches to table static DHCP addresses, filtering out malicious spoofed traffic.
- Use secure versions of communication protocols (HTTPS, SFTP, SSH) that provide encryption and authentication rather than their clear-text equivalents.

## 7.4 Banner Grabbing Countermeasures

Since a discovered banner directly identifies the OS, server type, and version — exactly the information needed to select a working exploit — the countermeasures here focus on either hiding that information or making it useless/false.

### Disabling or Changing the Banner

- Display **false banners** deliberately to mislead or deceive attackers who are relying on banner accuracy.
- Turn off unnecessary services on network hosts to limit how much gets disclosed in the first place.
- Use server-masking tools to disable or rewrite banner information outright.
- Remove unnecessary HTTP headers and response data, camouflaging the server by presenting false signatures — including eliminating file extensions like `.asp`/`.aspx` that clearly indicate a Microsoft server.
- **Apache 2.x:** use a directive in `httpd.conf` (via the `mod_headers` module) to rewrite the banner header and set the server identity to something like `New Server Name`.
- **Apache 2.x (alternative):** change the `ServerSignature` line to `ServerSignature Off` in `httpd.conf`.
- Disable vendor and version details in banners generally.
- Modify `Server Tokens` from `Full` to `Prod` in Apache's `httpd.conf` to prevent disclosure of the exact server version.
- Modify `RemoveServerHeader` from `0` to `1` in the `UrlScan.ini` config file (found at `C:\WINDOWS\System32\inetsrv\urlscan`) to prevent server-version disclosure on IIS.
- Trick attackers by modifying `AlternateServerName` to a decoy value like `xyz` or `myserver`.
- Disable unneeded HTTP methods — Connect, Put, Delete, Options — on web application servers.
- Remove the `X-Powered-By` header only via the `customHeaders` option inside the `<system.webServer>` section of `web.config`.

### Hiding File Extensions from Web Pages

- File extensions reveal the underlying server technology an attacker can target — hide them to mask the web technology stack.
- Replace application mappings like `.asp` with `.htm` or `.foo`, etc., to disguise a server's real identity.
- Apache users can use `mod_negotiation` directives to achieve the same effect.
- **Best practice, per the source material: it's preferable not to use file extensions at all.**

### Other Banner Grabbing Countermeasures

- Use packet filtering to block or restrict access to ports that might unnecessarily reveal banner information.
- Use IDS/IPS to monitor for and alert on scanning activity that could indicate banner-grabbing attempts.
- Replace protocols that send clear-text banners (HTTP, FTP, Telnet) with their secure counterparts (HTTPS, SFTP/FTPS, SSH), which encrypt the connection and the banner information along with it.
- Use TLS for services generally, encrypting banner information during the handshake process and making it materially harder for unauthorized parties to grab.

## 7.5 IP Spoofing Detection Techniques

Because spoofed source addresses underpin decoy scanning, IDLE scanning, and DoS-style attacks (file `06`, §6.5–6.6), being able to detect a spoofed packet is itself a defensive skill worth having.

### Direct TTL Probes

Send a probe packet directly to the host that a suspected spoofed packet claims to be from, and compare the TTL of that fresh reply against the TTL of the suspected packet.

```
Attacker (spoofed address 10.0.0.5) -- sends packet, TTL=13 -->  Target
Real host 10.0.0.5                  -- sends reply, TTL=25  -->  Target
```

If the TTLs **don't match**, the original packet is very likely spoofed. **This technique is only reliable when the attacker is on a different subnet than the actual victim being impersonated** — normal traffic from a single genuine host can still show TTL variation depending on route/traffic pattern, so this alone is a supporting signal, not absolute proof.

### IP Identification Number

Send a probe to the host that a suspected spoofed packet claims to be from, and compare the returned **IPID** with the IPID seen in the suspected traffic.

```
Attacker (spoofed 10.0.0.5, IP ID 2586)  -- sends spoofed packet -->  Target
Real host 10.0.0.5                       -- replies, IP ID 515   -->  Target
```

If the IPIDs are **not close in value** to the suspect traffic's IPID, the traffic in question is very likely spoofed. **This method remains reliable even when the attacker is on the same subnet as the victim** — a meaningful advantage over the TTL method above.

### TCP Flow Control Method

TCP performs flow control on both ends via the sliding-window algorithm, using the **window size** field in the TCP header to communicate how much unacknowledged data a receiver can currently accept. An attacker spoofing a source address never actually receives the target's SYN-ACK — meaning they never learn the real window-size value the target set — so they can't correctly react to any change in the congestion window.

```
Attacker (spoofed 10.0.0.5) -- SYN -->  Target
Real host 10.0.0.5          <-- SYN-ACK (small window size) --  Target
[Attacker never sees this SYN-ACK, so can't respect the shrinking window]
```

**Signal:** if traffic keeps flowing at full rate *after* the window size should have been exhausted, that traffic is most likely spoofed.

Because most real spoofing attacks happen precisely during the handshake (correctly guessing a full sequence of spoofed replies with matching sequence numbers is genuinely hard for an attacker to sustain), this flow-control check is best applied right at the handshake itself: have the host that sent the initial SYN wait for the SYN-ACK before sending its ACK, and specifically set that SYN-ACK's own value to zero as a trap — a genuine client receiving a zero value is expected to reply with a bare ACK carrying no additional data; a spoofed sender that never actually received the real SYN-ACK is liable to send additional data anyway, exposing itself.

## 7.6 IP Spoofing Countermeasures

- **Avoid trust relationships** — don't rely on IP-based authentication alone. An attacker can masquerade as a trusted host and deliver malicious code under the assumption that "packets from this address must be clean." Test *all* packets, even ones nominally from a trusted host, and pair IP-based checks with password authentication rather than relying on trust relationships in isolation.
- **Use firewalls and filtering mechanisms** on both inbound and outbound traffic. ACLs help block unauthorized access, though insider threats remain a gap firewalls alone don't close — a malicious insider can leak sensitive competitive information, or a hidden sniffing program can quietly exfiltrate network data. Outbound packet inspection deserves the same priority as inbound.
- **Encrypt all network traffic** using cryptographic protocols such as **IPsec, TLS, SSH, and HTTPS**. This is described as the single best method for preventing spoofing attacks overall — IPsec specifically reduces spoofing risk by providing data authentication, integrity, and confidentiality, and should be enabled on routers so trusted hosts can communicate securely with local hosts. Since decrypting an entire stream of encrypted packets is a genuinely difficult task, attackers are far more likely to move on to an easier, unencrypted target than to fight through encryption.
- **Use random initial sequence numbers (ISNs).** Devices that choose ISNs based on a predictable timed counter make it easy for an attacker to work out the next connection's ISN from the current one, enabling malicious connection hijacking and traffic sniffing. Random ISN generation removes that predictability.
- **Ingress filtering** — prevents spoofed traffic from entering the network at all, typically applied at routers via ACLs that drop packets whose source address falls outside the expected/defined range for that interface.
- **Egress filtering** — the mirror-image practice at the network's exit point: block *outgoing* packets whose source address doesn't belong to the internal range, preventing your own network from being used as a spoofing launch point against others.
- **SYN flooding countermeasures** — defenses against SYN flood attacks also incidentally help mitigate IP spoofing, since many spoofing-based DoS attacks rely on the same flooding mechanics.

### Other IP Spoofing Countermeasures

- Implement dynamic IPv6 address variation via a random address generator, reducing the window of active vulnerability for any single address.
- Configure routers to send encoded information about fragmented packets entering the network.
- Configure routers to verify incoming packets using stored digests of packet signatures.
- Configure routers to hide intranet hosts from the external network via NAT.
- Configure internal switches to table static DHCP addresses, filtering out malicious spoofed traffic.
- Use secure protocol versions (HTTPS, SFTP, SSH) that provide encryption and authentication.

## 7.7 Scanning Detection and Prevention Tools

Security teams use dedicated platforms to detect active-network and port-scanning attempts initiated by attackers, rather than relying solely on the countermeasures above:

- **ExtraHop** (https://www.extrahop.com) — provides real-time visibility, detection, and intelligent response to malicious network scanning; automatically discovers every device (including unmanaged IoT devices) and its vulnerabilities on a network, analyzes all network interactions in real time — including cloud transactions and SSL/TLS-encrypted traffic — and assists with auto-discovery/classification of every device so security teams can analyze all communication in one place.
- **Splunk Enterprise Security** (https://www.splunk.com)
- **Scanlogd** (https://github.com)
- **Vectra Detect** (https://www.vectra.ai)
- **IBM Security QRadar XDR** (https://www.ibm.com)
- **Cynet 360 AutoXDR™** (https://www.cynet.com)

---

## Module Recap

Across this module, you've worked through:

1. **Concepts** — what scanning is, the TCP flags and handshake that everything else builds on.
2. **Tools** — Nmap, Hping3, Metasploit, and the rest of the toolbox.
3. **Host discovery** — figuring out which IPs in a range are actually alive.
4. **Port & service discovery** — the full taxonomy of TCP/UDP/SCTP/SSDP/IPv6 scan types, and how to squeeze version info out of open ports.
5. **OS discovery** — active/passive banner grabbing and fingerprinting techniques to identify the target OS.
6. **Evading IDS/firewalls** — fragmentation, spoofing, decoys, proxies, and anonymizers.
7. **Countermeasures** — the defensive playbook for every technique above.

**What comes next (per the source curriculum):** Module 04 — **Enumeration**, which goes a layer deeper than scanning: extracting usernames, machine names, shares, and other detailed system information from services already identified as open, ahead of an actual attack or audit.
