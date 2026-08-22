# 05 — OS Discovery (Banner Grabbing / OS Fingerprinting)

## 5.1 Why OS Discovery Matters

Knowing what OS a target is running dramatically increases an attacker's odds of a successful compromise, because a large share of vulnerabilities are OS-specific. Once the OS is known, an attacker can pick an attack strategy tuned to that OS's known weaknesses instead of guessing blindly.

Two broad techniques for figuring out the OS:
1. **Spot the banner** while connecting to a service (e.g., an FTP server) that voluntarily announces its software/version.
2. **Stack-query fingerprinting** — send crafted packets and evaluate exactly how the target's TCP/IP stack responds, since different vendors implement subtly different (but each internally consistent) interpretations of the relevant RFCs.

Two more specific stack-querying methods worth naming:
- **Initial Sequence Number (ISN) analysis** — different OSes/kernels use different random-number generation strategies for TCP sequence numbers; the pattern of "randomness" itself is a fingerprint.
- **ICMP response analysis** — send ICMP messages to a host and read subtle details of the reply.

## 5.2 Active Banner Grabbing

Active banner grabbing exploits the fact that every vendor's IP stack has its own idiosyncratic way of responding to specially crafted (often malformed) TCP packets. The attacker sends a battery of probes and compares the responses to a signature database.

Nmap performs OS fingerprinting via a documented series of tests (see https://nmap.org/book/osdetect-methods.html#osdetect-probes):

| Test | Probe sent |
|---|---|
| **Test 1** | TCP packet, SYN + ECN-Echo flags, to an open TCP port |
| **Test 2** | TCP packet, no flags (a NULL packet), to an open TCP port |
| **Test 3** | TCP packet, URG + PSH + SYN + FIN flags, to an open TCP port |
| **Test 4** | TCP packet, ACK flag, to an open TCP port |
| **Test 5** | TCP packet, SYN flag, to a closed TCP port |
| **Test 6** | TCP packet, ACK flag, to a closed TCP port |
| **Test 7** | TCP packet, URG + PSH + FIN flags, to a closed TCP port |
| **Test 8 (PU — Port Unreachable)** | UDP packet to a closed UDP port, looking for an ICMP "port unreachable" reply |
| **Test 9 (TSeq — TCP Sequenceability test)** | Six SYN packets to an open TCP port, analyzing ISN patterns (TCP ISN sampling), IPID sampling, and TCP timestamp behavior |

The goal across all nine tests is to spot patterns in how each OS generates initial sequence numbers. These generally sort into: traditional **64K** (many old UNIX boxes), **random increments** (newer Solaris, IRIX, FreeBSD, Digital UNIX, Cray, and others), **true random** (Linux 2.0.*, OpenVMS, newer AIX), or Windows's **"time-dependent" model**, where the ISN increments by a fixed amount per time unit.

## 5.3 Passive Banner Grabbing

**Source referenced:** https://www.broadcom.com

Passive fingerprinting relies on the same underlying idea (different OSes implement the stack differently) but observes it purely by **sniffing** traffic from the target rather than actively probing it — no packets sent to the target at all. This is much harder for an IDS to catch, since there's no anomalous traffic generated toward the target in the first place.

Three passive-grabbing sub-techniques:

- **Banner grabbing from error messages** — error pages/responses often leak server type, OS, and even SSL tooling in use.
- **Sniffing network traffic** — capturing and analyzing packets from the target directly reveals stack-behavior fingerprints.
- **Banner grabbing from page extensions** — a URL extension can hint at the underlying application stack (e.g., `.aspx` → IIS + Windows platform).

### The Four Passive Fingerprinting Signatures

| Signal | Question it answers |
|---|---|
| **TTL** | What does the OS set as the outbound Time-To-Live? |
| **Window Size** | What window size does the OS set? |
| **DF bit** | Does the OS set the Don't-Fragment bit? |
| **TOS** | Does the OS set a Type-of-Service value, and if so, what? |

None of these four are individually conclusive or exhaustive — accuracy improves by combining several signatures rather than relying on just one.

**Worked example from the source material** — a sniffed packet analysis:
```
2024-03-15 11:5.330465 10.10.1.11 -> 10.10.1.22
Time To Live: 128
Protocol: ICMP(1)
Fragment Offset: 0
Differentiated Service Field: 0x00 (DSC, CSO, ECN, NOT-ECT)
Ack: 0xE3C65D7  Win: 0x7D78
```

From the four criteria: TTL = 45 (as observed, after hop deduction), Window Size = `0x7D78` (32120 decimal), DF bit set, TOS = `0x0`. Compare against a signature database:

**On TTL specifically:** if the observed TTL is 45 and the packet crossed 19 hops to reach you, the *original* TTL the sender set was likely 64 (45 + 19 ≈ 64) — a value strongly associated with Linux/FreeBSD (more signatures would be needed to fully confirm). You can sanity-check the hop count with a traceroute; for a stealthier trace, set the traceroute's own TTL to one or two hops fewer than the full path (`-m` option) to reveal path/provider info without directly touching the remote host.

**On Window Size:** Linux commonly uses `0x7D78`; FreeBSD and Solaris tend to keep the *same* window size consistently through a session, while Cisco routers and Windows NT vary their window size constantly. Window size measurements are more reliable when taken *after* the initial three-way handshake completes (TCP slow-start affects early packets).

**On the DF bit:** limited standalone value, since most systems set it — but it's useful for spotting the minority that *don't* (e.g., SCO, OpenBSD).

**On TOS:** also limited value alone — TOS tends to track the specific protocol in use more than the OS itself.

**Limitations of passive fingerprinting:**
- Tools that build their own raw packets (Nmap, Hunt, Nemesis, etc.) won't carry the OS's native signatures — they'll look like whatever the tool itself constructs.
- It's trivial for a remote host to deliberately alter its TTL, window size, DF, or TOS settings, defeating the technique outright.

**Other legitimate/defensive uses of passive fingerprinting:** identifying a potential target's OS stealthily (e.g., just by requesting one web page and sniffing the reply — no active tool an IDS could flag), and identifying rogue systems or remote proxy firewalls hiding behind a rebuilt connection signature.

## 5.4 How to Identify Target System OS — TTL & Window Size Table

Attackers sniff/capture the response generated from the target using packet-capture tools like Wireshark and compare the **TTL** and **TCP window size** fields in the first captured TCP packet of a session against known baseline values:

| Operating System | Time To Live | TCP Window Size |
|---|---|---|
| Linux | 64 | 5,840 |
| FreeBSD | 64 | 65,535 |
| OpenBSD | 255 | 16,384 |
| Windows | 128 | 65,535 bytes – 1 Gigabyte |
| Cisco Routers | 255 | 4,128 |
| Solaris | 255 | 8,760 |
| AIX | 255 | 16,384 |

**Worked Wireshark examples from the source material:**
- A captured packet showing **Time to Live: 128** → flagged "Possible OS is Windows"
- A captured packet showing **Time to Live: 64** → flagged "Possible OS is Linux"

## 5.5 OS Discovery Using Nmap

**Syntax:** `nmap -O <Target IP>` (`-O` in the CLI, same flag in Zenmap's command field)

Nmap's OS detection engine runs the nine active fingerprinting tests from §5.2 and returns structured output, e.g.:
```
MAC Address: 00:15:5D:01:80:00 (Microsoft)
Device type: general purpose
Running: Microsoft Windows 10
OS CPE: cpe:/o:microsoft:windows_10:1703
OS details: Microsoft Windows 10 1703
Network Distance: 1 hop
```

## 5.6 OS Discovery Using Unicornscan

**Source:** https://sourceforge.net

Unicornscan infers the OS by observing TTL values in scan responses, in much the same way as the passive table above.

```bash
unicornscan <target IP>
```
A TTL of **128** in the results points to a **Windows** target (matching the table in §5.4).

## 5.7 OS Discovery Using Nmap Script Engine (NSE)

**Source:** https://nmap.org

NSE lets users write and share scripts to automate a wide range of networking tasks at Nmap's own speed and parallelism. One relevant built-in script:

- **`smb-os-discovery`** — collects OS information from the target over the SMB protocol.

```bash
nmap --script smb-os-discovery.nse <Target IP>
```
Example output:
```
Host script results:
| smb-os-discovery:
|   OS: Windows Server 2022 Standard 20348 (Windows Server 2022 Standard 6.3)
|_  Computer name: Server2022
```

In Zenmap, `-sC` runs the default NSE script set; `--script` lets you specify custom scripts. NSE results appear in both the normal Nmap output and any XML output requested.

## 5.8 OS Discovery Using IPv6 Fingerprinting

**Source:** https://nmap.org

IPv6 fingerprinting works the same way conceptually as IPv4 fingerprinting (send probes, wait for responses, compare against a signature database) but adds several IPv6-specific probes and a dedicated OS-detection engine. Nmap sends roughly 18 probes in this specific order:

1. Sequence generation (S1–S6)
2. ICMPv6 echo (IE1)
3. ICMPv6 echo (IE2)
4. Node Information Query (NI)
5. Neighbor Solicitation (NS)
6. UDP (U1)
7. TCP explicit congestion notification (TECN)
8. TCP (T2–T7)

**Syntax:** `nmap -6 -O <target>`

## 5.9 OS Discovery with AI

The same "prompt → command" pattern from files `02` and `04` extends naturally to OS fingerprinting:

**Prompt:** *"Use TTL to identify the operating system running on the target IP address 10.10.1.11"*
```bash
ping -c 1 10.10.1.11 && echo "Check the TTL value from the response to infer the OS (Linux/Unix: 64, Windows: 128)"
```
- `ping -c 1` sends a single ICMP echo request
- `&&` chains a follow-up `echo` reminder only if the ping succeeds
- The person then reads the TTL from the ping reply and compares it against the Linux/Windows baseline

**Prompt:** *"Use Nmap script engine to perform OS discovery on the target IP addresses in scan1.txt"*
```bash
nmap -iL scan1.txt -O --script=default --script-args=newtargets -oN os_discovery_results.txt
```
- `-iL scan1.txt` — read targets from file
- `-O` — enable OS detection
- `--script=default` — run Nmap's default script set
- `--script-args=newtargets` — allow scripts to add newly-discovered targets back into the scan
- `-oN os_discovery_results.txt` — save normal-format output

**Custom AI-generated automation script** — a full pipeline that discovers hosts, then scans open ports/services/versions across the whole range:
```bash
#!/bin/bash
nmap -sP 10.10.1.0/24 -oG - | awk '/Up$/{print $2}' > live_hosts.txt &&
nmap -iL live_hosts.txt -sV -oA scan_results &&
cat scan_results.nmap
```
This is the same three-stage pattern seen in file `03` (§3.7) and file `04` (§4.4) — discover live hosts → deep-scan them → dump the combined report — reused here specifically to fold OS/service context into one repeatable script rather than three manual steps.

---

**Next:** [`06-scanning-beyond-ids-firewall.md`](06-scanning-beyond-ids-firewall.md) — what happens when a firewall or IDS stands between you and the target.
