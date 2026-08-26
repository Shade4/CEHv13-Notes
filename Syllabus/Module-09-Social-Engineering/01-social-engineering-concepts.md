# 01 — Social Engineering Concepts

> Exam objective: *Summarize social engineering concepts*

## 1.1 What Is Social Engineering?

**Social engineering (SE)** is the art of manipulating people into performing actions or
divulging confidential information, rather than breaking in through a technical vulnerability.
It targets the one component of every security architecture that can never be fully patched:
**human judgment**.

Formally: *SE is a non-technical strategy that attackers use to gather information, commit
fraud, or gain unauthorized system access, by exploiting human psychology rather than technical
hacking techniques.*

Two things make SE uniquely dangerous compared to a technical exploit:

1. **It bypasses the network stack entirely.** Firewalls, IDS/IPS, EDR, and patch management
   are irrelevant if the "attack" is a phone call that ends with someone reading out their
   password.
2. **The victim usually doesn't know they were attacked.** A buffer overflow leaves a crash log.
   A well-executed pretext leaves nothing but a helpful employee who feels good about "helping
   a colleague."

### Why attackers bother with SE before touching a keyboard

Before ever touching the target's network, an attacker typically builds a profile of the
organization using freely available, completely passive sources:

| Source | What it leaks |
|---|---|
| Corporate website / careers page | Org chart, employee names, job titles, tech stack in job ads |
| Press releases / investor decks | Products, partners, financial pressure points |
| LinkedIn / social media | Reporting lines, current projects, vendor relationships, out-of-office patterns |
| Forums, GitHub, Stack Overflow | Internal tool names, software versions, real employee handles |
| Job postings | "Must have experience with Okta SSO and Palo Alto firewalls" tells you their stack |

This is passive **OSINT (Open-Source Intelligence)** reconnaissance — see
[`08-social-engineering-penetration-testing.md`](08-social-engineering-penetration-testing.md)
for hands-on OSINT tooling. Once an attacker knows *who* works where and *what* they use, the
pretext (the invented backstory used to justify the request) writes itself.

## 1.2 Common Targets of Social Engineering

Social engineers deliberately go after roles where **helpfulness is part of the job
description**, because refusing to help feels like failing at their job:

| Target | Why they're targeted |
|---|---|
| **Receptionists / help-desk staff** | Trained to be helpful; often first to reset passwords or grant physical access |
| **Technical support executives** | Handle credentials and system access routinely; used to "fixing" things over the phone |
| **System administrators** | Hold the highest-value information: OS versions, admin passwords, network diagrams |
| **Users and clients** | Easy to approach pretending to be "tech support"; rarely question a support call |
| **Vendors of the target organization** | Trusted third parties often have standing access or are less scrutinized |
| **Senior executives (CxOs, Finance, HR)** | Access to the most sensitive data; also frequently impersonated *as* the authority figure in BEC scams |

## 1.3 Impact of a Social Engineering Attack on an Organization

A "soft" attack can cause very hard losses:

- **Economic loss** — competitors or criminals steal R&D, pricing, or M&A plans.
- **Damage to goodwill** — leaked customer data erodes brand trust.
- **Loss of privacy** — breach of stakeholder/customer confidentiality can end business relationships.
- **Enabling terrorism / physical threats** — attackers build "blueprints" of a facility's people and layout.
- **Lawsuits and arbitration** — regulatory and contractual liability following a breach.
- **Temporary or permanent closure** — the cumulative effect of the above can end a business.

## 1.4 Behaviors Vulnerable to Attack (The Psychology Social Engineers Exploit)

These eight behavioral levers show up constantly in CEH exam scenarios — memorize the *name*
and be able to spot the matching script:

| Lever | Mechanism | Example pretext |
|---|---|---|
| **Authority** | People defer to perceived power/position | *"This is IT Security — we've detected an incident on your account. I need your credentials to secure it immediately."* |
| **Intimidation** | Bullying / fear of consequences | *"Mr. Tibiyani is about to present to the client and his files are corrupt — he told me to call and get you to send them to me now."* |
| **Consensus / Social Proof** | "Everyone else is doing it" | Fake testimonials on a rogueware site convince a visitor the software is legitimate |
| **Scarcity** | Fear of missing out drives snap decisions | Phishing email about a sold-out iPhone restock link |
| **Urgency** | No time to think = no time to verify | Ransomware countdown timer; "act within 24 hours or your account is suspended" |
| **Familiarity / Liking** | We comply more with people we like | An attacker uses charm/small talk before asking someone to hold the door |
| **Trust** | Attacker builds rapport before the ask | "I'm from XYZ Security, I noticed unusual errors from your system" → guides victim to "disable" protections |
| **Greed** | Something-for-nothing offers override caution | A "competitor" offers a large reward for internal information |

> 🧩 **Extra context — Cialdini's Principles of Influence:** the list above is CEH's framing of
> a well-known academic model. Dr. Robert Cialdini's book *Influence: The Psychology of
> Persuasion* identifies six (later seven) core principles — **Reciprocity, Commitment/
> Consistency, Social Proof, Authority, Liking, Scarcity,** and **Unity** — that drive human
> compliance. Every "behavior vulnerable to attack" above is a direct application of one of
> these. If you remember Cialdini's six words, you'll never forget CEH's eight bullets.

## 1.5 Factors That Make Companies Vulnerable

- **Insufficient security training** — employees who were never taught to recognize a pretext.
- **Unregulated access to information** — flat access models where "everyone can see everything."
- **Several organizational units / geographic sprawl** — harder to verify "I'm calling from the
  other office" claims.
- **Lack of security policies** — no documented rules means no baseline to detect deviation from.

## 1.6 Why Is Social Engineering So Effective?

- Security policies are only as strong as the humans enforcing them — **human behavior is the
  most susceptible factor** in any security program.
- SE attempts are inherently hard to detect — there's no malicious packet to alert on.
- No control — technical or administrative — guarantees complete protection.
- No firewall or antivirus signature exists for "a convincing phone call."
- It's cheap. A phone call or a $10 USB drive is far less costly than developing a zero-day.

## 1.7 The Four Phases of a Social Engineering Attack

```
 1. RESEARCH             2. SELECT A TARGET        3. DEVELOP A            4. EXPLOIT THE
    THE COMPANY             ─────────────────         RELATIONSHIP            RELATIONSHIP
 ───────────────         Prefer disgruntled,       ─────────────────      ─────────────────
 Dumpster diving,        overworked, or new        Build rapport via      Extract sensitive
 website/social media    employees — easier        phone, email, or       data: accounts,
 recon, org structure,   to manipulate             in-person contact      finances, tech stack,
 employee enumeration                                                     roadmap
```

1. **Research the target company** — dumpster diving, browsing the company website, scraping
   employee names/roles from LinkedIn, reviewing job postings for tech-stack clues.
2. **Select a target** — attackers disproportionately target disgruntled, new, or
   overworked/under-resourced employees, since they're statistically easier to manipulate.
3. **Develop a relationship** — the attacker builds trust with the chosen target over one or
   more interactions.
4. **Exploit the relationship** — the attacker extracts account details, financial data,
   technology in use, or upcoming organizational plans.

## 1.8 Types of Social Engineering (Overview)

| Category | Delivered via | Detailed in |
|---|---|---|
| **Human-based** | Direct interaction — in person or by phone | [`02-human-based-social-engineering.md`](02-human-based-social-engineering.md) |
| **Computer-based** | Computers / the Internet (email, web, IM) | [`03-computer-based-social-engineering.md`](03-computer-based-social-engineering.md) & [`04-ai-powered-social-engineering.md`](04-ai-powered-social-engineering.md) |
| **Mobile-based** | Mobile apps, SMS, QR codes | [`05-mobile-based-social-engineering.md`](05-mobile-based-social-engineering.md) |

---

**Next:** [`02-human-based-social-engineering.md`](02-human-based-social-engineering.md) →