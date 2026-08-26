# 03 — Computer-Based Social Engineering Techniques

> Exam objective: *Explain various computer-based social engineering techniques*

Computer-based SE relies on computers and Internet systems to carry out the attack, rather than
face-to-face or voice interaction. **Phishing** is the flagship technique in this category and
gets the deepest coverage below, followed by its many named variants, the toolkits used to run
phishing campaigns (both maliciously and — far more usefully for you — for *authorized* internal
awareness testing), and the smaller techniques (pop-ups, hoaxes, chain letters, spam, scareware).

---

## 3.1 Phishing

**Phishing** is sending an illegitimate email or message that claims to be from a legitimate
source, in an attempt to acquire a user's personal or account information. The attacker:

1. Registers a fake or **look-alike domain name** (`micros0ft-support.com`,
   `paypal-secure-verify.com`, homoglyph domains using Cyrillic characters that render
   identically to Latin ones, etc.).
2. Builds a **lookalike website** replicating the real login page pixel-for-pixel.
3. Mails a link to that fake site to a large or targeted list of users.
4. When the victim clicks, they land on the fake page and enter real credentials — which the
   attacker now owns.

Phishing succeeds because of a mix of **user unfamiliarity** with how browsers/URLs work, **visual
deception** (a convincing logo and layout), and simple failure to check the address bar or sender
domain.

### Anatomy of a phishing email (what to look for)
Real-world phishing lures typically combine a **plausible sender** (DocuSign, a "Q3 Benefits
Package," a government "Invitation for Bid") with a **single, urgent call-to-action button**
("View Completed Document," "Download Proposal") that leads to a credential-harvesting clone of a
trusted login page (Microsoft 365 is extremely common because it unlocks so much downstream
access). See §3.6 below for the full checklist of red flags.

---

## 3.2 Types of Phishing

| Variant | Definition | Distinguishing feature |
|---|---|---|
| **Spear Phishing** | Highly targeted at a specific person or small group, using specialized content relevant to them | Personalized — mentions real names, projects, or vendors |
| **Whaling** | Targets high-profile executives (CEO, CFO, politicians, celebrities) | High production value; often precedes a wire-fraud (BEC) request |
| **Pharming** | Redirects web traffic to a fraudulent site without any user click — "phishing without a lure" | Performed via **DNS cache poisoning** or **host file modification** (details below) |
| **Spimming (SPIM)** | Spam over Instant Messaging platforms | Uses bots to harvest IM IDs, then floods them with malicious links |
| **Clone Phishing** | Near-identical copy of a previously-received legitimate email, with the link/attachment swapped for a malicious one | Victim recognizes the email "template" and trusts it |
| **E-wallet Phishing** | Targets users of digital wallets (PayPal, crypto wallets, etc.) | Fake wallet-provider login page harvests credentials in real time |
| **Tabnabbing** | A malicious tab quietly rewrites itself to mimic a login page **while the user is looking at another tab** | Exploits the assumption that a tab you opened yourself is safe |
| **Reverse Tabnabbing** | The malicious *origin* tab rewrites a **different, previously-opened tab** to a phishing page via `window.opener` | Victim returns to a tab they trust, unaware it changed |
| **Consent Phishing** | Abuses the **OAuth** authorization flow — a fake-but-legitimate-looking app requests permission scopes | No password is stolen; the victim *grants* access voluntarily |
| **Search Engine Phishing** | SEO/keyword-stuffing manipulates search results to rank malicious sites highly | Victim finds the fake site organically — no email needed |

### Pharming — the two delivery mechanisms

**DNS Cache Poisoning:**
```
1. Attacker poisons the target DNS server's cache
2. Maps www.targetwebsite.com  →  <attacker-controlled IP>  (instead of the real IP)
3. Victim types www.targetwebsite.com in their browser
4. DNS server returns the poisoned (fake) IP address
5. Victim is transparently redirected to the fake website
```

**Host File Modification:**
```
1. Attacker sends malicious code as an email attachment
2. Victim opens the attachment → code silently edits the local hosts file
      (Windows: C:\Windows\System32\drivers\etc\hosts)
      (Linux/macOS: /etc/hosts)
3. Any future visit to the target domain resolves locally to the attacker's fake IP
```

🛡️ **Defensive check** — inspect your hosts file for unexpected entries:
```bash
# Linux / macOS
cat /etc/hosts

# Windows (PowerShell)
Get-Content C:\Windows\System32\drivers\etc\hosts
```

---

## 3.3 Phishing Simulation & Phishing Toolkits

> ⚠️ The tools below are dual-use. Legitimate red teams and security-awareness teams use them
> **only** against their own organization, with signed authorization, to measure and improve
> click-through/report rates. Running any of these against a third party without written
> authorization is a crime. All commands here are for **local lab / authorized-engagement use
> only** (e.g., spin these up in an isolated test VM against test accounts you own).

### 3.3.1 The Social-Engineer Toolkit (SET)
- **Source:** https://github.com/trustedsec/social-engineer-toolkit (by TrustedSec)
- Open-source, Python-driven, purpose-built for penetration testing via social engineering.
  Categorizes attacks by vector: email, web, USB/media, wireless, QR code, and more.

```bash
# Install (Kali/Parrot ship it pre-installed; otherwise:)
git clone https://github.com/trustedsec/social-engineer-toolkit.git setoolkit
cd setoolkit
pip3 install -r requirements.txt
python3 setup.py install

# Launch
sudo setoolkit
```
Menu flow inside SET:
```
1) Social-Engineering Attacks
   1) Spear-Phishing Attack Vectors
   2) Website Attack Vectors     (credential harvester, Java applet, etc.)
   3) Infectious Media Generator (autorun USB payloads — lab use only)
   4) Create a Payload and Listener
   5) Mass Mailer Attack
   6) Arduino-Based Attack Vector
   7) Wireless Access Point Attack Vector
   8) QRCode Generator Attack Vector
   9) PowerShell Attack Vectors
```

### 3.3.2 Gophish — the industry-standard *authorized* phishing simulator
- **Source:** https://getgophish.com / https://github.com/gophish/gophish
- Purpose-built for security teams to run internal phishing awareness campaigns with full
  reporting (open rate, click rate, credential-submit rate, reporting rate).

```bash
# Download the latest release for your OS from the GitHub Releases page, then:
unzip gophish-vX.Y.Z-linux-64bit.zip
cd gophish
chmod +x gophish
./gophish
# Admin UI defaults to https://localhost:3333 (credentials printed on first run)
```
Typical authorized-campaign workflow inside the admin UI:
1. **Sending Profile** — configure the SMTP relay you're authorized to send from.
2. **Landing Page** — clone (or build) the training landing page users will see.
3. **Email Template** — the pretext email, with tracking pixels/links auto-inserted.
4. **Users & Groups** — import the target employee list (CSV).
5. **Campaign** — schedule and launch; results stream into the dashboard in real time.

### 3.3.3 King Phisher — another authorized phishing-campaign framework
- **Source:** https://github.com/rsmusllp/king-phisher
```bash
git clone https://github.com/rsmusllp/king-phisher.git
cd king-phisher
./tools/install.sh          # server-side installer (Linux)
king-phisher-server          # start the campaign server
king-phisher                 # launch the client GUI to build/manage campaigns
```

### 3.3.4 OhPhish — enterprise phishing-simulation & security-awareness platform
- **Source:** https://portal.ohphish.com
- A **web-based SaaS portal** (no local install) purpose-built to audit an organization's own
  phishing susceptibility. Campaign modes include *Entice to Click*, *Credential Harvesting*,
  *Send Attachment*, *Assign New Training*, *Vishing*, and *Smishing* — with MIS reporting/trend
  dashboards trackable by user, department, or designation. This is the kind of tool a security
  team runs **on themselves**, on a recurring basis, as an ongoing training program rather than a
  one-off test.

### 3.3.5 Other named phishing tools (reference only)
| Tool | Purpose | Official source |
|---|---|---|
| ShellPhish | Login-page cloning tool covering 25+ platforms, mainly for lab/training demos | https://github.com |
| BLACKEYE | Similar login-page cloning toolkit | https://github.com |
| SocialFish | Phishing + credential-harvesting framework | https://github.com |
| Modlishka | Reverse-proxy-based phishing (can relay MFA prompts — a good reason to prefer FIDO2/hardware keys) | https://github.com |
| Trape | People/OSINT tracking via crafted links | https://github.com |
| Dark-Phish | Phishing page generator | https://github.com |
| Zphisher | Automated phishing-page toolkit | https://github.com |
| LUCY Security | Commercial phishing-simulation & awareness platform | https://lucysecurity.com |

> Because these clone the login pages of real, named platforms, treat them the same as a lock
> pick: legal to own and study, illegal to use on anything you don't own or have written
> authorization to test.

---

## 3.4 Other Computer-Based Techniques

### Pop-Up Windows
Windows that suddenly appear while browsing, asking the user to log in/sign in again ("your
session expired," "re-authenticate now"). Compliance installs a keylogger, trojan, or spyware
that exfiltrates data to the attacker.

### Hoax Letters
Emails warning recipients of a **non-existent** virus/threat. They cause no direct data loss but
waste productivity and network resources as the message is forwarded organization-wide.

### Chain Letters
Messages offering a "free gift" (money, software) on condition the recipient forwards it to a set
number of people. Common hooks: get-rich-quick pyramid schemes, superstitious "bad luck if you
don't forward this" threats, or emotionally manipulative stories.

### Instant Chat Messenger
The attacker chats with a selected online user, casually gathering personal details (birth date,
mother's maiden name, pet's name) that are frequently used as security-question answers — later
used to reset or crack the victim's real accounts.

### Spam Email
Irrelevant, unsolicited email attempting to collect financial data, SSNs, or network information.
Attackers often disguise a malicious attachment behind an unusually long filename to obscure the
true (often double) file extension, e.g. `Invoice_Q3_Statement_Final_Copy_2024.pdf.exe`.

### Scareware
Malware that tricks users into visiting malware-infested sites or purchasing/downloading bogus
"security software." Typically delivered via a pop-up mimicking a legitimate antivirus vendor,
manufacturing urgency ("STOLEN IDENTITY — ACT NOW!") to bypass rational evaluation.

---

## 3.5 Detecting a Malicious/Modified Hosts File or DNS Config (Pharming Defense)

```bash
# Check current DNS resolvers (Linux)
cat /etc/resolv.conf

# Check current DNS resolvers (Windows)
ipconfig /all | findstr /i "DNS Servers"

# Manually flush a poisoned DNS cache
# Windows:
ipconfig /flushdns
# macOS:
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
# Linux (systemd-resolved):
sudo systemd-resolve --flush-caches
```

## 3.6 How to Detect Phishing Emails — Full Checklist

| # | Red flag |
|---|---|
| 1 | Unexpected attachments from unknown senders |
| 2 | Attachments with unusual/unrecognized file formats (double extensions, `.rar`/`.exe` disguised as documents) |
| 3 | Mismatch between the sender's display name and the actual email address/domain |
| 4 | Sender domain is incomplete, misspelled, or uses numbers instead of letters |
| 5 | Generic greetings — "Dear user," "Dear customer," "Hello" |
| 6 | Manufactured urgency — "account will be suspended," "act within 24 hours" |
| 7 | Links whose hover-preview URL doesn't match the displayed text or the claimed organization |
| 8 | Offers that are "too good to be true" — lottery wins, free vacations, surprise job offers |
| 9 | Claims to be from your bank/employer/vendor, asking you to log in or install something via a provided link |
| 10 | Requests for charity donations with urgency and a payment link |
| 11 | Obvious misspellings and unusual punctuation |
| 12 | Requests for personal information (SSN, DOB, full account number, security answers) |
| 13 | Missing or incomplete sender signature/contact details |

**Practical verification steps:**
1. Hover over the sender name to reveal the true "From" address — does the domain match?
2. Hover over any link (don't click) to preview the real destination URL.
3. Check that the destination uses `https://` — but remember HTTPS alone does **not** mean
   legitimate; attackers buy real certificates for fake domains too.
4. When in doubt, open a **new browser tab** and type the organization's known URL directly,
   rather than clicking the link at all.
5. Never provide credentials or codes over the phone/email in response to an unsolicited
   contact — call the organization back using a number from their official website.

---

**Next:** [`04-ai-powered-social-engineering.md`](04-ai-powered-social-engineering.md) →