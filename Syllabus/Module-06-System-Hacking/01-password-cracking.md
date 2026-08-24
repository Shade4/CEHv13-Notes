# 01 — Password Cracking

**CEH Objective:** Demonstrate different password cracking and vulnerability exploitation techniques to gain access to a system.

Password cracking is where "gaining access" almost always starts. A password is the cheapest, most universal authentication mechanism in existence — which also makes it the single most attacked one. Before touching any tool, it helps to understand *what* is actually being attacked: not the password itself, but the way an operating system stores and checks it.

---

## 1. How Windows Stores and Checks Credentials

### The SAM Database
Windows never stores your password. It stores a **hash** of it — a one-way mathematical fingerprint that's computationally impractical to reverse. Local account hashes live in the **Security Accounts Manager (SAM)**, which on a standalone machine is a registry hive backed by a file at `C:\Windows\System32\config\SAM`. Domain-joined accounts instead live in the **Active Directory database** (`NTDS.dit`) on domain controllers.

The SAM file is locked exclusively by the Windows kernel while the OS is running, which is why you can't just copy it off a live system the way you'd copy a normal file — the lock only releases on shutdown or a crash. This is precisely why attackers reach for hash-dumping tools instead of file-copy tricks; tools like **Mimikatz**, **pwdump7**, **DSInternals**, and **secretsdump.py** interact with the LSASS process or registry hive directly (often via a Volume Shadow Copy or direct memory read) to pull hashes out from under the lock. Older Windows versions additionally scrambled the SAM contents with **SYSKEY**, a partial-encryption layer meant to raise the bar for offline attacks.

### NTLM Authentication
NTLM is a **challenge-response** protocol — the password (or its hash) never crosses the wire in the clear:

1. Client sends a logon request to the server.
2. Server replies with a random challenge (a nonce).
3. Client encrypts the challenge using a key derived from the user's password hash and sends back the response.
4. Server (or, in a domain, the domain controller) independently encrypts the same challenge using the hash it has stored for that user, and compares the two results.
5. Match = authenticated.

The important takeaway: because the *hash* — not the plaintext — is what's actually used cryptographically, **stealing the hash is functionally equivalent to stealing the password** for many purposes. That single fact is the entire basis of Pass-the-Hash attacks later in this file.

### Kerberos
Microsoft's modern default is **Kerberos**, a ticket-based protocol built around a trusted third party called the **Key Distribution Center (KDC)**, which is made up of two logical services:

- **Authentication Server (AS)** — verifies the initial logon and issues a **Ticket Granting Ticket (TGT)**.
- **Ticket Granting Server (TGS)** — accepts a valid TGT and issues **service tickets (TGS tickets)** for specific resources.

Flow: user authenticates once to the AS → receives a TGT → presents the TGT to the TGS whenever a new service is needed → TGS issues a service ticket → client presents the service ticket directly to the target application server. Critically, **application servers never talk to the KDC directly** — every ticket reaches them by way of the client. This design gives Kerberos its Single Sign-On property (you type your password once, then request tickets silently) and, as you'll see in file 06, also gives attackers an enormous attack surface once they can forge or steal tickets.

---

## 2. The Four Categories of Password Attack

| Category | Defining trait | Skill required |
|---|---|---|
| **Non-Electronic** | No interaction with a computer at all | None |
| **Active Online** | Attacker directly communicates with the target | Low–Medium |
| **Passive Online** | Attacker only listens; never touches the target | Medium |
| **Offline** | Attacker already has the hash and cracks it locally, at their own pace | Medium–High |

### Non-Electronic Attacks
The oldest tricks in the book, and still effective because they bypass technology entirely:
- **Shoulder surfing** — watching someone type their password or PIN.
- **Social engineering** — impersonating IT, a vendor, or a trusted colleague to get someone to hand over credentials voluntarily.
- **Dumpster diving** — physically retrieving discarded printouts, sticky notes, old hard drives, or manuals that contain credentials or clues.

### Active Online Attacks
Anything where the attacker is actively talking to the target system:

- **Dictionary attack** — try every word in a wordlist (commonly `/usr/share/wordlists/rockyou.txt` on Kali).
- **Brute-force attack** — try every possible character combination; guaranteed to work eventually, but potentially astronomically slow.
- **Rule-based attack** — a hybrid: start from a dictionary or known pattern and apply mutation rules (append digits, capitalize, leetspeak substitutions) when you have partial knowledge about the target's likely password habits.
- **Password guessing / manual cracking** — find a valid username → build a candidate list from OSINT → rank by likelihood → try each one. This is trivially scriptable, for example with a Windows batch loop against a credentials file:
  ```bat
  c:\>FOR /F "tokens=1,2*" %i in (credentials.txt) do net use \\victim.com\IPC$ %j /u:victim.com\%i 2>>nul && echo %time% %date% >> outfile.txt && echo \\victim.com acct: %i pass: %j >> outfile.txt
  c:\>type outfile.txt
  ```
- **Default passwords** — manufacturer defaults (`admin/admin`, `admin/password`) that never got changed after setup. Lookup sites include `https://cirt.net`, `https://www.routerpasswords.com`, and `https://default-password.info`.
- **Trojans / spyware / keyloggers** — plant something on the victim's machine that captures credentials as they're typed. (Covered in depth in file 04.)
- **Hash Injection / Pass-the-Hash (PtH)** — since NTLM authenticates on the hash rather than the plaintext (see above), an attacker who dumps a hash from one compromised box can inject it straight into a new session and authenticate as that user elsewhere, without ever cracking it. Typical chain: compromise a workstation → dump hashes with Mimikatz → find a cached domain admin hash → inject that hash into `lsass.exe` on the attacker's controlled session → authenticate to the domain controller as that admin → dump the entire AD hash database.
- **LLMNR / NBT-NS Poisoning** — LLMNR and NetBIOS Name Service are Windows fallback name-resolution protocols used when DNS can't resolve a hostname. Because the fallback broadcast is unauthenticated, a listening attacker can simply answer *"yes, that's me"* to a mistyped or nonexistent hostname, prompting the victim to authenticate directly to the attacker with an NTLMv2 hash. Tools: **Responder**, **Metasploit**. The stolen hash is then cracked offline with hashcat or John.
- **Kerberos password attacks:**
  - **AS-REP Roasting** — targets accounts that have "Do not require Kerberos preauthentication" enabled. Because no proof of password knowledge is needed to request a TGT for such accounts, an attacker can request one and crack it offline at leisure.
  - **Kerberoasting** — any authenticated domain user can request a service ticket (TGS) for any service that has a Service Principal Name (SPN) registered. That ticket is encrypted with the *service account's* password hash — so the attacker requests the ticket, takes it offline, and brute-forces the service account's password with no special privileges required. This is why service accounts with weak, never-rotated passwords are one of the highest-value AD misconfigurations to fix.
  - **Pass-the-Ticket** — instead of stealing a hash, steal an actual Kerberos ticket (TGT or TGS) from `lsass.exe` (via Mimikatz, Rubeus, or Windows Credentials Editor) and inject it into a new session to impersonate the ticket's owner without ever knowing their password.
  - **NTLM Relay** — rather than cracking a captured NTLM hash, relay the live authentication attempt to a *different* server in real time using **Responder** in relay mode or **ntlmrelayx**, effectively borrowing the victim's authentication session as it happens.
- **GPU-based password attacks** — malicious browser extensions or web pages can abuse the WebGL/OpenGL API to harness the victim's GPU for cracking work, or more directly, malware can key-log a login form and exfiltrate what's typed before it's ever hashed.

### Passive Online Attacks
The attacker never sends a single packet to the target — only listens:

- **Wire sniffing / packet sniffing** — capturing plaintext or weakly protected credentials off the wire (legacy FTP, Telnet, HTTP basic auth, SMB, POP3). Works best on shared-medium networks (hubs) or where the attacker has ARP-spoofed their way onto the path.
- **Man-in-the-Middle (MITM) / Manipulator-in-the-Middle and Replay attacks** — sit between two communicating parties, either passively eavesdropping or actively capturing and later re-injecting valid authentication tokens/packets to replay a transaction (e.g., a captured bank transfer authorization).

### Offline Attacks
The attacker already possesses the password hash (dumped, sniffed, or leaked) and now cracks it without any further interaction with the target — meaning no lockout policy, no rate limiting, no logging on the victim's side:

- **Rainbow table attack** — instead of computing hashes on the fly, precompute massive lookup tables of `plaintext → hash` pairs ahead of time (using a tool like **rtgen** from the RainbowCrack project), then simply look up the captured hash. Classic time/memory trade-off: enormous storage cost, near-instant lookup cost. Salting defeats this technique almost entirely, which is why unsalted hash schemes (like old-style NTLM/LM) remain so dangerous.
  ```
  rtgen hash_algorithm charset plaintext_len_min plaintext_len_max table_index chain_len chain_num part_index
  ```
- **Distributed Network Attack (DNA)** — spread the cracking workload across many machines' idle CPU cycles, coordinated by a central DNA manager that hands out key-search chunks to DNA clients. Commercial tooling: **Exterro Password Recovery Toolkit (PRTK)**.

---

## 3. Dictionary, Brute-Force & Mask Attacks in Practice

### John the Ripper — dictionary attack against NTLM hashes
```bash
# 1. Grab a base wordlist
ls /usr/share/wordlists/rockyou.txt

# 2. (Optional) customize John's rules in john.conf for mutation-based cracking

# 3. Crack NTLM hashes with a chosen wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt --format=NT hashes.txt
```

### hashcat — mask attacks
A mask attack narrows brute-forcing to a *known pattern* instead of trying every possible character everywhere, which collapses the search space dramatically when you have partial intel (e.g., "always exactly 8 characters, starts with a capital letter, ends in two digits").

**Built-in charsets:**
| Symbol | Meaning |
|---|---|
| `?l` | `abcdefghijklmnopqrstuvwxyz` |
| `?u` | `ABCDEFGHIJKLMNOPQRSTUVWXYZ` |
| `?d` | `0123456789` |
| `?h` | `0123456789abcdef` |
| `?H` | `0123456789ABCDEF` |
| `?s` | space and punctuation |
| `?a` | `?l?u?d?s` combined |
| `?b` | `0x00`–`0xff` |

Crack a 6-character password: lowercase-lowercase-lowercase-digit-digit-digit
```bash
hashcat -a 3 -m 0 md5_hashes.txt ?l?l?l?d?d?d
```
- `-a 3` → attack mode 3 (brute-force / mask)
- `-m 0` → hash type 0 (MD5)

Crack an unknown-length password by scanning a length range:
```bash
hashcat -m 0 -a 3 -i --increment-min=6 --increment-max=10 <hash> ?a?a?a?a?a?a?a?a?a?a
```

Custom charset example (attacker knows position 1 is a letter but doesn't know the case):
```bash
hashcat -a 3 -m 0 md5_hashes.txt -1 ?l?u ?1?1?1?1?1
```

---

## 4. Password Recovery & Cracking Tool Index

| Tool | Category | Link |
|---|---|---|
| John the Ripper | Dictionary/rule-based offline cracker | https://www.openwall.com/john/ |
| hashcat | GPU-accelerated cracking (dict/brute/mask) | https://hashcat.net |
| L0phtCrack | Windows password audit (dict/hybrid/rainbow/brute) | https://gitlab.com |
| THC-Hydra | Online protocol brute-forcer | https://github.com |
| RainbowCrack / rtgen | Rainbow table generation & lookup | http://project-rainbowcrack.com |
| Mimikatz | Live hash/ticket/credential extraction | https://github.com |
| DSInternals | AD offline hash extraction (PowerShell) | https://github.com |
| pwdump7 | SAM hash dumper | — |
| Responder | LLMNR/NBT-NS/MDNS poisoning & relay | https://github.com |
| Elcomsoft Distributed Password Recovery | Enterprise-grade recovery suite | https://www.elcomsoft.com |
| Passware Kit Forensic | Document/drive password recovery | https://www.passware.com |
| PCUnlocker | Windows local account reset | https://www.top-password.com |
| Lazesoft Recover My Password | Windows password reset | https://www.lazesoft.com |

---

## 5. Defenses

- Enforce long, high-entropy passphrases over short complex passwords; length beats complexity against modern GPU cracking.
- Enable **account lockout** and **rate limiting** to blunt active online guessing.
- Use **MFA** everywhere possible — it neutralizes almost every technique in this file on its own.
- Disable **LLMNR** and **NBT-NS** on networks where they aren't needed (Group Policy), and enable **SMB signing** to prevent relay attacks.
- Rotate service account passwords regularly and use long random passwords (or **gMSA — Group Managed Service Accounts**) to make Kerberoasting impractical.
- Require Kerberos preauthentication on all accounts to close off AS-REP Roasting.
- Salt and use slow, memory-hard hashing (bcrypt/scrypt/Argon2) for any credential store you control — never fast general-purpose hashes like unsalted MD5/SHA1 for passwords.
- Monitor for abnormal authentication patterns (impossible travel, unusual TGS requests, repeated failed logons) with a SIEM.
- Educate users against shoulder surfing, phishing, and social engineering — the cheapest attacks are still the hardest to patch technically.

**Next:** [02 — Exploiting Vulnerabilities (Buffer Overflows)](./02-Exploiting-Vulnerabilities.md)
