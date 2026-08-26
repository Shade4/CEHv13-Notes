# 07 — Social Engineering Countermeasures

> Exam objective: *Explain social engineering countermeasures*

There is no single control that stops social engineering — it's a **human** problem, so it needs
a layered mix of **policy, training, and technical controls**. This file consolidates every
countermeasure from the module into one practical reference, organized by what you're defending
(the organization broadly, phishing specifically, identity theft, and AI-driven attacks), plus the
concrete commands/tools to implement the technical controls.

A critical prerequisite: **good policies are worthless if they aren't taught and reinforced.**
After training, employees should sign a statement acknowledging they understand the policy — this
creates both genuine awareness and a documented compliance trail.

---

## 7.1 General Organizational Countermeasures

**Core objectives of any SE defense strategy:** create user awareness, build robust internal
network controls, and maintain clear security policies, plans, and processes.

### Password Policies
| Guideline | Why |
|---|---|
| Change passwords regularly | Limits the exposure window of any credential that's already been compromised |
| Avoid guessable passwords | Answers to "security questions" (pet name, birthplace) are often public via social media |
| Lock accounts after failed attempts | Blunts brute-force and credential-stuffing attempts |
| Minimum 6–8 characters, alphanumeric + special characters | Increases brute-force cost |
| Never disclose passwords to anyone | Defeats vishing/help-desk pretexts directly |
| Set a password expiration policy | Forces periodic rotation |
| Don't share a computer account | Preserves individual accountability |
| Don't reuse passwords across accounts | Contains the blast radius of any one breach |
| Don't write down or store passwords in plaintext | Removes an easy physical/dumpster-diving target |
| Never communicate passwords by phone, email, or SMS | Removes the #1 vishing payoff |
| Lock/shut down your workstation before stepping away | Defeats shoulder-surfing & unauthorized physical access |

**Implementing password policy technically:**
```bash
# Windows (local security policy via net accounts) — run as Administrator
net accounts /minpwlen:12 /maxpwage:90 /minpwage:1 /uniquepw:5 /lockoutthreshold:5 /lockoutduration:30

# Windows (Active Directory domain-wide, via PowerShell — run on a Domain Controller)
Set-ADDefaultDomainPasswordPolicy -Identity "example.com" `
    -ComplexityEnabled $true `
    -MinPasswordLength 12 `
    -MaxPasswordAge 90.00:00:00 `
    -LockoutThreshold 5 `
    -LockoutDuration 00:30:00

# Linux — enforce password aging with chage
sudo chage -M 90 -m 1 -W 7 <username>      # max 90 days, min 1 day, warn 7 days before expiry

# Linux — account lockout after failed attempts (PAM, e.g. /etc/pam.d/common-auth on Debian/Ubuntu)
auth required pam_faillock.so preauth silent deny=5 unlock_time=1800
auth [default=die] pam_faillock.so authfail deny=5 unlock_time=1800
```

### Physical Security Policies
- Issue ID cards and, where appropriate, uniforms to employees and require visible display.
- Escort all visitors to designated visitor areas — never allow unescorted wandering.
- Restrict access to sensitive areas (server rooms, wiring closets) via badge/biometric control.
- Dispose of documents containing valuable information using cross-cut shredders or burn bins —
  this directly defeats dumpster diving (`02.4`).
- Employ trained security personnel, supplemented with alarm systems and surveillance cameras.
- Sanitize retired storage devices by overwriting with 0s, 1s, and random data (or physical
  destruction for the highest-sensitivity media).

```bash
# Linux — securely wipe a disk before disposal/reuse (DESTRUCTIVE — verify the device path first!)
sudo shred -n 3 -z -v /dev/sdX

# Cross-platform — NIST-aligned secure erase via nvme-cli (for NVMe SSDs)
sudo nvme format /dev/nvme0n1 --ses=1
```

### Defense Strategy
1. **Social engineering campaign** — run authorized internal SE exercises using varied
   techniques across a representative employee sample to see how staff actually react to
   real-style attempts (see `08` for how to structure one).
2. **Gap analysis** — compare campaign results against industry-leading practices and emerging
   threats to identify concrete weaknesses.
3. **Remediation strategies** — build a targeted training/awareness plan addressing the specific
   gaps found, rather than generic one-size-fits-all training.

## 7.2 Additional Organizational Countermeasures

| # | Countermeasure | Detail |
|---|---|---|
| 1 | Train individuals on security policies | Cover core SE concepts, techniques, and policy in every onboarding + recurring refresher |
| 2 | Implement proper access privileges | Separate admin / user / guest tiers — least privilege by default |
| 3 | Proper incident-response time | Documented, rehearsed procedure for reacting to a suspected SE attempt |
| 4 | Resource availability restricted to authorized users | Sensitive data reachable only by those with a genuine need |
| 5 | Scrutinize/classify information | Top Secret, Proprietary, Internal Use Only, Public — so handling rules are unambiguous |
| 6 | Background checks + proper termination process | Insiders with criminal history or disgruntled ex-employees are easy targets/vectors |
| 7 | Anti-virus / anti-phishing defenses | Layer defenses at both the endpoint and the mail gateway |
| 8 | Two-factor authentication (2FA/MFA) | Requires two independent proof-of-identity forms; defeats credential-only compromise |
| 9 | Documented change management | Formal, auditable change process beats ad-hoc changes |
| 10 | Regular software updates | Unpatched software is routinely exploited to gain the foothold a pretext later builds on |
| — | Hardware policy | Explicitly define what hardware is allowed — e.g., disallow unauthorized USB drives |
| — | Software policy | Only approved software may be installed; define who is authorized to install it |
| — | Verify identity & authorization | Employees must check email headers/links before acting, and verify identity of anyone requesting information |
| — | Spam filters | Block bulk/malicious mail before it reaches an inbox |
| — | Secure communication channels | Mandate encrypted channels for sharing sensitive information |

**Implementing 2FA / MFA (examples):**
```bash
# Linux SSH — require a TOTP second factor via Google Authenticator PAM module
sudo apt install libpam-google-authenticator
google-authenticator                     # run as the user to generate their TOTP secret + QR
# then add to /etc/pam.d/sshd:
auth required pam_google_authenticator.so
# and in /etc/ssh/sshd_config:
ChallengeResponseAuthentication yes
```
```bash
# Disable USB mass storage at the OS level (Linux) — supports the "hardware policy" control
echo "blacklist usb-storage" | sudo tee /etc/modprobe.d/block-usb-storage.conf
sudo update-initramfs -u
```
```powershell
# Windows — restrict removable storage via Group Policy (registry equivalent, run as Admin)
New-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\RemovableStorageDevices" `
    -Name "Deny_All" -PropertyType DWord -Value 1 -Force
```

## 7.3 How to Defend Against Phishing Attacks

- Run regular phishing-awareness campaigns (see Gophish/King Phisher/OhPhish in `03`).
- Enable spam filters that detect mail from suspicious sources.
- Never respond to emails requesting sensitive information, and never provide credentials over
  the phone.
- Hover over links to confirm the real destination before clicking.
- Check for generic salutations and spelling/grammar mistakes (though note: AI-generated phishing
  increasingly defeats this specific check — see `04`).
- Confirm the sender through an independent channel before acting on any request.
- Enforce HTTPS-only browsing where feasible.
- Implement multi-factor authentication to blunt whaling/BEC attempts specifically.
- Contact organizations only via the phone number or email listed on their **official** website —
  never one supplied in the suspicious message itself.
- Verify a suspicious social-media account's profile picture with a reverse image search.
- Report confirmed fake social media accounts to the platform immediately.
- File a complaint with your local cybercrime authority if an account engages in
  extortion/bullying for money.
- Install and maintain reputable browser security extensions that detect/block known phishing
  sites.
- Keep regular backups so a successful phishing-driven ransomware infection doesn't cost you your
  data.

## 7.4 Identity Theft Countermeasures

- Secure or shred all documents containing private information.
- Try to keep your name off marketers' mailing/contact "hit lists."
- Review credit card statements regularly and store them securely.
- Never give personal information over the phone to an unverified caller.
- Empty your physical mailbox promptly to prevent mail theft.
- Be cautious of and verify all unsolicited requests for personal data.
- Avoid publicizing personal information unnecessarily.
- Don't display account or contact numbers unless required.
- Monitor your online banking activity regularly.
- Never list personal identifiers (parent's name, pet's name, birth city) on social media.
- Enable two-factor authentication on all accounts that support it.
- Never use public Wi-Fi to access or transmit sensitive information.
- Install host-based security tools (firewall + antivirus) on personal devices.
- Shred credit card offers and unused "convenience checks."
- Never store financial information in plaintext; use strong, unique passwords everywhere.
- Check phone/cell bills for calls you didn't make.
- Keep your SSN card, passport, and license physically secured — don't carry them unnecessarily.
- Read the privacy policies of services before sharing data with them.
- Be cautious before clicking any link in an email or IM.
- Only enter personal information on pages secured with `https://`.
- Set up fraud alerts with your bank/credit issuer.
- Never let family or friends open accounts in your name "for convenience."
- Use reputable digital wallets that offer strong security guarantees.
- Use a credit freeze with Equifax, Experian, and TransUnion to block unauthorized credit
  inquiries.
- Use a locked mailbox to prevent physical mail theft.
- Opt for paperless billing/statements where mail theft is a concern.

## 7.5 Voice Cloning Countermeasures

- Treat unsolicited calls/audio messages requesting sensitive information or urgent action with
  suspicion by default.
- Verify the caller's identity through an independent channel (call back a known number,
  ask a pre-agreed challenge question) rather than trusting the voice alone.
- Educate staff/family specifically about voice-cloning risk — "it sounded exactly like them" is
  no longer sufficient proof of identity.
- Where available, use voice biometrics or other advanced authentication for voice-based systems.
- Deploy anti-spoofing detection technology to flag synthetic/fake voices.
- Prefer encrypted, authenticated communication channels for sensitive voice interactions.
- Establish and rehearse a documented identity-verification procedure for voice-based requests
  (e.g., a shared family "safe word" for emergencies, or a callback policy for finance teams).

## 7.6 Deepfake Attack Countermeasures

- Implement digital watermarking that embeds invisible authenticity codes into genuine media at
  creation time.
- Use blockchain-based or similar provenance records to verify a video's authenticity and origin.
- Invest in improved facial-recognition tooling that can better distinguish real vs.
  AI-generated faces.
- Protect biometric data (face/voice prints) from being harvested and reused without consent.
- Build strong reporting mechanisms on social platforms to quickly flag suspected deepfakes.
- Train staff and media consumers to critically evaluate the credibility of video content before
  acting on it.
- Invest in/monitor AI-based deepfake-detection tooling that flags unnatural eye movement,
  inconsistent lighting, or lip-sync mismatches.
- Establish clear ethical-use guidelines for AI development/deployment within your organization.
- Apply forensic analysis (compression-artifact analysis, pixel-level inspection, audio/video
  consistency checks) when authenticity of a specific video is in question.

## 7.7 Anti-Phishing Toolbars & Detection Services

| Tool | Purpose | Source |
|---|---|---|
| **Netcraft** | Community-powered anti-phishing toolbar/extension; blocks known-dangerous sites and shows site-reputation data | https://www.netcraft.com |
| **PhishTank** | Community-driven clearinghouse of confirmed phishing URLs with an open API for integration | https://phishtank.com |
| Scanurl | Quick URL safety scan | https://scanurl.net |
| Isitphishing | Phishing-site checker | https://isitphishing.org |
| Threatcop | Human-risk / phishing-simulation and awareness platform | https://threatcop.ai |
| e.Veritas | Email authenticity verification | https://www.emailveritas.com |
| VirusTotal | Multi-engine URL/file scanning (60+ AV engines) | https://www.virustotal.com |

```bash
# VirusTotal — scan a suspicious URL from the command line via the public API
curl --request POST \
  --url https://www.virustotal.com/api/v3/urls \
  --header 'x-apikey: <YOUR_API_KEY>' \
  --data "url=https://suspicious-site.example.com"

# Then retrieve the analysis result using the returned analysis ID:
curl --request GET \
  --url https://www.virustotal.com/api/v3/analyses/<ANALYSIS_ID> \
  --header 'x-apikey: <YOUR_API_KEY>'
```

## 7.8 Common Social Engineering Targets & Defense Strategies (Reference Table)

| Target | Common Attack Techniques | Defense Strategy |
|---|---|---|
| Front office & help desk | Eavesdropping, shoulder surfing, impersonation, persuasion, intimidation | Train staff to never reveal passwords/info by phone; enforce front-office/help-desk policy |
| Technical support & sysadmins | Impersonation, persuasion, intimidation, fake SMS/calls/emails | Train never to reveal passwords/info by phone or email |
| Perimeter security | Impersonation, reverse SE, piggybacking, tailgating | Badge/token/biometric authentication, staff training, security guards |
| Office (general) | Shoulder surfing, eavesdropping, ingratiation | Employee training, documented best practices/checklists, escort all guests |
| Vendors | Impersonation, persuasion, intimidation | Educate vendors on social engineering risk specifically |
| Mail room | Theft, damage, or forging of mail | Lock and actively monitor the mail room |
| Machine room / phone closet | Unauthorized access attempts, equipment removal, protocol-analyzer taps | Keep locked at all times; maintain an updated equipment inventory |
| Company executives | Fake SMS, phone calls, and emails targeting confidential data | Train executives to never reveal identity/passwords/confidential info over phone or email |
| Dumpsters | Dumpster diving | Keep trash in secured/monitored areas; shred sensitive documents; erase magnetic media |

## 7.9 Auditing Your Own Organization: OhPhish

As introduced in `03.3.4`, **OhPhish** (https://portal.ohphish.com) is purpose-built for
organizations to audit their *own* phishing susceptibility — running Entice-to-Click, Credential
Harvesting, Attachment, Vishing, and Smishing simulation modes, then tracking results by user,
department, or role over time via MIS reporting. Running a recurring (e.g., quarterly) campaign
through a tool like this, paired with mandatory remedial training for anyone who fails, is one of
the highest-ROI countermeasures on this entire page — it converts "we hope our people would spot
this" into a measured, improvable metric.

---

**Next:** [`08-social-engineering-penetration-testing.md`](08-social-engineering-penetration-testing.md) →
(Bonus/extra content not in the original CEH slide deck — a full authorized SE pentest
methodology.)