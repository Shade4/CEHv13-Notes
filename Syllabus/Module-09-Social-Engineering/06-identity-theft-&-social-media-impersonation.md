# 06 — Identity Theft & Social Media Impersonation

> Exam objective: *Explain various computer-based social engineering techniques* (social-media &
> identity-theft subset)

Social networking sites are a goldmine for attackers precisely because users voluntarily publish
what used to require real reconnaissance effort: full names, employers, job titles, relationship
status, daily routines, and physical location. This file covers how attackers weaponize that
exposure, and the broader crime of identity theft it frequently feeds into.

---

## 6.1 Impersonation on Social Networking Sites

There are two dominant attack patterns:

### 6.1.1 Angler Phishing
The attacker creates a **fake customer-support account** impersonating a real organization's
helpdesk on social media, then watches for public complaints. When a genuinely disgruntled
customer posts a complaint, the fake account replies first with a "helpful" link. Because the
reply looks like a prompt, legitimate response from the brand, the victim trusts it and clicks —
landing on a credential-harvesting page or triggering a malicious download.

### 6.1.2 Catfishing Attack
The attacker steals a real person's identity/photos from social media, builds a fake profile
impersonating them, and uses that fake persona to build personal or romantic relationships with
other users online — eventually monetizing the relationship through requests for money or through
cyberbullying/extortion.

**Signs of catfishing:**
| Sign | Why it's suspicious |
|---|---|
| Avoids direct communication | Refuses calls, video chats, or in-person meetings; always has an excuse |
| Long-duration single profile photo | Reuses the same photo set for years — a real person's photos naturally accumulate/change |
| Large "opposite gender" friend list | Common in profiles built to run multiple simultaneous romance scams |
| Requests for money | The end goal — usually framed as an emergency the victim is emotionally invested in |

### 6.1.3 What Attackers Extract From a Social Profile
| Category | Examples |
|---|---|
| Organization details | Employer name, department, org-chart hints from "who I work with" tags |
| Professional details | Job title, skills, certifications, project mentions |
| Contacts & connections | Coworker/manager names — fuel for later impersonation pretexts |
| Personal details | Birthday, hometown, relationship status, pet names (common security-question answers) |

Attackers routinely create fake employee-only groups (*"Employees of [Company XYZ]"*) on
platforms like Facebook, then send friend/join requests to real staff. Once inside, group members
often freely share credentials-adjacent details — date of birth, employment history, even a
spouse's name — any one of which can help an attacker impersonate them convincingly enough to
talk their way past a badge-check or a help-desk verification question.

## 6.2 Social Networking Threats to Corporate Networks

| Risk | Description |
|---|---|
| **Data theft** | SNS platforms are massive databases accessed by huge user populations, raising exploitation risk |
| **Involuntary data leakage** | Without a clear personal/corporate boundary policy, employees may unknowingly post sensitive company detail |
| **Targeted attacks** | Attackers use SNS-sourced information to craft specific, credible attacks on named individuals |
| **Network vulnerability** | Platform bugs (login flaws, client-side vulnerabilities) can leak information tied to the organization |
| **Spam and phishing** | Employees using work email on social platforms become phishing/spam magnets |
| **Modification of content** | Poorly secured profiles/pages/groups can be spoofed or outright hijacked |
| **Malware propagation** | SNS platforms are efficient vectors for viruses, worms, trojans, and spyware |
| **Business reputation damage** | False information about a company or employee can spread rapidly |
| **Infrastructure/maintenance cost** | Securing SNS use requires ongoing monitoring investment |
| **Loss of productivity** | Organizations must actively monitor usage to prevent resource misuse |
| **Reconnaissance** | Employee/executive/infrastructure details gathered from profiles enable further targeted attacks |

---

## 6.3 Identity Theft

**Identity theft** is a crime in which an imposter obtains and uses someone else's **personally
identifiable information (PII)** — name, SSN, credit card number, driver's license, etc. — to
commit fraud or other crimes. The (U.S.) **Identity Theft and Assumption Deterrence Act of 1998**
formally defines it as the illegal use of someone's identification.

### PII Commonly Targeted
| | |
|---|---|
| Full name | Biometric data |
| Home & office address | Bank account number |
| Social Security Number | Credit card information |
| Phone number | Credit report |
| Date of birth | Driving license number |
| Medical history / health insurance info | Passport number |

### What Attackers Do With a Stolen Identity
- Open new credit card accounts and run up unpaid balances
- Open a new phone/wireless account, or run charges on an existing one
- Obtain utility services (electricity, heating, cable) in the victim's name
- Open bank accounts to write fraudulent checks
- Clone ATM/debit cards for electronic withdrawal
- Take out loans the victim is left liable for
- Obtain a driver's license, passport, or other government ID bearing the attacker's photo
- Claim government benefits using the victim's SSN
- Physically impersonate an employee to access a target facility
- Hijack insurance policies or sell the victim's personal information outright
- Order goods online shipped to an attacker-controlled drop site
- Hijack email accounts, obtain health services, or file fraudulent tax returns
- Provide the victim's name to authorities in place of their own during an arrest

### Types of Identity Theft
| Type | Summary |
|---|---|
| **Child Identity Theft** | A minor's SSN (issued at birth) is stolen and combined with a different date of birth to open accounts/get benefits — can go undetected for years since children rarely check credit |
| **Criminal Identity Theft** | A criminal provides the victim's identity when caught/arrested, leaving a false record under the victim's name |
| **Financial Identity Theft** | Bank/credit-card info is stolen and used to withdraw funds, open new accounts, or take loans |
| **Driver's License Identity Theft** | A lost/stolen license is sold or misused to commit traffic violations the real owner is unaware of and never pays for — risking suspension/revocation of the real owner's license |
| **Insurance Identity Theft** | Victim's medical/insurance information is used to access insurance for treatment |
| **Medical Identity Theft** | The most dangerous type — attacker's treatments get recorded in the victim's medical history, risking false diagnoses and dangerous treatment decisions later |
| **Tax Identity Theft** | Attacker files a fraudulent return using the victim's SSN to claim their refund; phishing is a leading vector |
| **Identity Cloning & Concealment** | Perpetrator (e.g., an undocumented immigrant, someone evading creditors) fully assumes another identity to become effectively "invisible" |
| **Synthetic Identity Theft** | Combines a real stolen SSN with fabricated name/DOB/address details to construct an entirely new, fraudulent identity |
| **Social Security Identity Theft** | SSN specifically is stolen to sell, defraud government benefit programs, or open new accounts/loans |

## 6.4 Common Techniques Attackers Use to Obtain PII

| Technique | Method |
|---|---|
| Physical theft | Stealing wallets, laptops, phones, or backup media from hotels, clubs, restaurants, beaches |
| Internet searches | Aggregating scattered public information via Google/Bing/Yahoo |
| Social engineering | Manipulating people into voluntarily divulging PII |
| Dumpster diving & shoulder surfing | As covered in `02` — trash and over-the-shoulder observation |
| Phishing | Fraudster poses as a bank/reputable org and requests info via spam/pop-up |
| Skimming | Card-reader "skimmer" devices installed on ATMs/POS terminals capture card data |
| Pretexting | Fraudster impersonates a financial/telecom employee and relies on smooth talk to win trust |
| Pharming (domain spoofing) | Redirects a legitimate-looking connection via cache poisoning to a rogue site |
| Hacking (system compromise) | Sniffers/scanners capture and decrypt data in transit |
| Keyloggers & password stealers | Malware records keystrokes to capture credentials directly |
| Wardriving | Searching for unsecured Wi-Fi from a moving vehicle to access connected devices |
| Mail theft and rerouting | Stealing physical mail (bank statements) or fraudulently rerouting it |
| Social media mining | Aggregating names, birthdates, addresses, and family ties from public profiles |
| Dark web data trading | Purchasing SSNs, card numbers, and credentials from underground marketplaces |

## 6.5 Indications of Identity Theft

Watch for any of the following:

- Unfamiliar charges on a credit card statement
- You stop receiving expected credit card, bank, or utility statements
- Creditors call about an account you never opened
- Traffic violations under your name that you didn't commit
- Charges for medical treatment you never received
- More than one tax return filed under your name
- Denied access to your own account or unable to take out a loan/other service
- Utility bills (electricity, gas, water) stop arriving due to mail theft
- Unexplained changes to your medical records
- A data-breach notification from a company where you have an account
- Unexplained cash withdrawals from your bank account
- Fraud-control calls from your card issuer about suspicious activity
- Government benefits denied because someone else is already claiming them under your SSN
- A medical insurance claim rejected because your benefit limit was already reached by fraud
- Account passwords/emails changed without your action
- Unexplained sudden drop in credit score
- Friends/family report receiving strange messages from your accounts
- Legal notices, warrants, or fines for activity you never engaged in
- Address-change notices you never requested

➡️ Full identity-theft and voice/deepfake-specific countermeasures are consolidated in
[`07-social-engineering-countermeasures.md`](07-social-engineering-countermeasures.md).

---

**Next:** [`07-social-engineering-countermeasures.md`](07-social-engineering-countermeasures.md) →