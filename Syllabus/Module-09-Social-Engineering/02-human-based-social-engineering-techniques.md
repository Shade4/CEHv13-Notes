# 02 — Human-Based Social Engineering Techniques

> Exam objective: *Explain various human-based social engineering techniques*

Human-based SE relies on direct interpersonal interaction — face-to-face, over the phone, or via
some other real-time communication channel. The attacker acts as though they were a legitimate
person to collect sensitive information such as business plans, network layouts, or credentials.

---

## 2.1 Impersonation

**Impersonation** is the most common human-based SE technique: the attacker pretends to be
someone legitimate or authorized, either in person or via a communication medium (phone, email).
It is the umbrella technique — vishing, tech-support scams, and repairman pretexts below are all
specific *flavors* of impersonation.

### 2.1.1 Posing as a Legitimate End User

The attacker claims to be an ordinary employee who has lost access.

> *"Hi! This is John from the Finance Department. I've forgotten my password. Can I get it?"*

This exploits **reciprocation** — the well-known social rule that a favor extended (even an
unsolicited one) creates an obligation to return it. Help-desk culture runs on this rule daily.

### 2.1.2 Posing as an Important User

The attacker claims to be a VIP — an executive, director, or valuable client — banking on the
fact that people rarely question authority, especially under time pressure.

> *"Hi! This is Kevin, the CFO's secretary. I'm working on an urgent project and lost my system
> password. Can you help me out?"*

If refused, the attacker may escalate to intimidation — threatening to report the employee's
"unhelpfulness" to their supervisor.

### 2.1.3 Posing as a Technical Support Agent

The attacker pretends to be a hardware vendor, software vendor, or internal IT technician —
particularly effective against victims who are not technically confident.

> *"Sir, this is Matthew from Technical Support at X Company. Last night we had a system crash,
> and we're checking for lost data. Can you give me your ID and password?"*

### 2.1.4 Posing as an Internal Employee, Client, or Vendor

The attacker dresses the part (business attire, branded uniform, contractor badge) and walks
into a facility claiming legitimate business. Once inside, they roam "unnoticed," photographing
sticky notes, extracting documents from bins, shoulder-surfing logins, or eavesdropping on
conversations.

### 2.1.5 Posing as a Repairman

Computer technicians, electricians, and telephone repair staff are rarely challenged. An
attacker impersonating one gets a legitimate-looking reason to be alone near desks, wiring
closets, and server rooms — even planting a covert listening/recording device.

### 2.1.6 Impersonation via Vishing (Voice/VoIP Phishing)

**Vishing** uses voice or VoIP technology (including spoofed caller ID) to extract personal or
financial information over the phone. Three common variants:

| Variant | How it works | Example |
|---|---|---|
| **Abusing help-desk over-helpfulness** | Attacker knows the target's name and calls the help desk pretending to be them, under time pressure | *"I've forgotten my password and if I miss this deadline my boss might fire me."* → sympathetic agent resets it |
| **Third-party authorization** | Attacker name-drops a real authority figure who is conveniently unreachable (on vacation/traveling) | *"Hi, I'm John — I spoke to Mr. XYZ last week before he left, and he said you'd be able to help me in his absence."* |
| **Tech support vishing** | Attacker pretends to be vendor/contractor support, asks for credentials "to troubleshoot" | *"Hi, this is Mike from tech support — folks have reported slow logins. We moved you to a new server; give me your password and I'll double-check your service."* |

### 2.1.7 Posing as a Trusted Authority Figure

The single most effective impersonation angle: fire marshal, auditor, superintendent, or
director — someone whose presence itself implies the right to ask intrusive questions.

> *"Hi, I'm John Brown with the external auditor's office, Arthur Sanderson & Associates. We've
> been asked to do a surprise inspection of your disaster-recovery procedures. Your department
> has 10 minutes to show me how you'd recover from a website crash."*

Using professional jargon (e.g., "HVAC" — Heating, Ventilation, and Air Conditioning — for a
fake maintenance visit) adds just enough credibility to a masquerade to gain physical access to
a restricted resource.

> 🛡️ **Spot the pattern:** every impersonation example above pairs an *authority or familiarity
> claim* with an *artificial time constraint*. If someone you can't independently verify is also
> rushing you, that combination alone is worth a pause-and-verify.

---

## 2.2 Eavesdropping

Unauthorized interception of conversations or communications — audio, video, or written —
through channels like telephone lines, email, or instant messaging. Can be as simple as
overhearing a hallway conversation or as involved as intercepting a communication line.

## 2.3 Shoulder Surfing

Direct observation — literally looking over someone's shoulder — to capture passwords, PINs, or
account numbers as they're typed. Can be extended over distance with binoculars or small hidden
cameras.

## 2.4 Dumpster Diving

Retrieving sensitive personal or organizational information by searching through trash. Common
finds:

| Discarded item | What it reveals |
|---|---|
| Phone lists | Employee names & direct contact numbers (fuel for future pretexts) |
| Organizational charts | Reporting structure, server rooms, restricted areas |
| Email printouts, memos, faxes | Passwords, contacts, internal instructions |
| Policy manuals | Employment rules, system-use policy, operational detail |
| Calendars / computer-use logs | Log-on/log-off patterns → best time to plan an attack |

Attackers sometimes support a dumpster-diving run with a pretext (posing as a cleaner or repair
person) to explain their presence near the bins.

## 2.5 Reverse Social Engineering

The hardest human-based technique to pull off — and the most effective when it lands. Instead of
approaching the victim, the attacker engineers a situation where **the victim approaches them**
for help, which sidesteps most suspicion entirely.

1. **Sabotage** — the attacker gains just enough access to corrupt a workstation (or make it
   appear corrupted).
2. **Marketing** — the attacker ensures their contact info is the one the victim finds — a
   business card left nearby, or a phone number embedded in the fake error message itself.
3. **Support** — the attacker "solves" the problem (sometimes while quietly achieving their real
   objective) and may continue providing support so the victim never suspects anything.

## 2.6 Piggybacking

An authorized person **knowingly** allows an unauthorized person through a secured door as a
courtesy — e.g., *"I forgot my ID badge at home, please help me."* The key distinction from
tailgating is consent: the door is held open deliberately.

## 2.7 Tailgating

The attacker, often wearing a fake ID badge, physically follows an authorized person through a
key-controlled door **without** the authorized person's knowledge or explicit consent — simply
walking in behind them before the door closes. Politeness ("holding the door") is the
vulnerability being exploited.

## 2.8 Diversion Theft

Also known as the *"Round the Corner Game"* or *"Corner Game."* The attacker tricks a person
responsible for a **genuine delivery** into sending the consignment to the wrong location —
classically targeting delivery drivers/couriers. The same technique applies online: persuading
someone to send sensitive files to an unintended recipient.

## 2.9 Honey Trap

The attacker targets an insider online while posing as an attractive person, builds a fake
romantic relationship, and leverages it over time to extract confidential information about the
target organization.

## 2.10 Baiting

The attacker exploits curiosity and greed by leaving a **physical device** — classically a USB
flash drive labeled with something enticing like *"Employee Salary Information 2024"* and a
convincing company logo — in a location such as a parking lot, elevator, or restroom. Whoever
finds it and plugs it into a company machine "out of curiosity" silently installs the
attacker's malware.

## 2.11 Quid Pro Quo

Latin for *"something for something."* The attacker cold-calls random extensions inside a
company claiming to be from technical support, and simply waits until they reach someone with a
genuine, unrelated IT issue. In "exchange" for fixing it, the attacker has the victim run
commands or install software that plants malware or harvests credentials.

## 2.12 Elicitation

The technique of extracting specific information through normal, disarming conversation, rather
than direct interrogation. Requires strong social skills — the attacker leverages professional or
social opportunities to talk with people who have access to the desired information, gradually
steering small talk toward the specific detail they need (e.g., a username, a software version,
a project codename).

## 2.13 Bait and Switch

The attacker captures attention with an exciting offer delivered via a clickable link or file
download. Once the victim takes the bait, the attacker executes their real goal — malware
installation, credential theft, or a compromised transaction. Frequently targets online shoppers:
a pop-up offers the same product at an unbeatable price; after clicking through and attempting to
"buy," the victim either leaks payment details or is told the item is "out of stock" and
upsold to something else.

---

## 🛡️ Quick Defense Reference for This File

| Technique | #1 Defense |
|---|---|
| Impersonation / vishing | Verify identity through an independently looked-up phone number — never one the caller provides |
| Eavesdropping / shoulder surfing | Privacy screens, clean-desk policy, awareness of surroundings in public/shared spaces |
| Dumpster diving | Cross-cut shred or incinerate anything with names, account numbers, or internal detail |
| Piggybacking / tailgating | Enforce badge-in-per-person policy; train staff it's OK to challenge an unbadged follower |
| Baiting | Disable autorun; block unknown USB media via endpoint policy (see `07`) |
| Quid pro quo / elicitation | "No unsolicited install/command requests" policy + healthy skepticism of unprompted "help" |

Full countermeasure detail lives in
[`07-social-engineering-countermeasures.md`](07-social-engineering-countermeasures.md).

---

**Next:** [`03-computer-based-social-engineering.md`](03-computer-based-social-engineering.md) →