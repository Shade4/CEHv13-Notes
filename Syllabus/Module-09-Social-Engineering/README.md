# CEH v13 — Module 09: Social Engineering

A comprehensive, hands-on reference library covering **Social Engineering** as taught in CEH v13
(Exam 312-50), rewritten and expanded into original study notes with real commands, tool
walkthroughs, defensive checklists, and a full penetration-testing methodology.

This repo is part of a growing security reference library. Companion modules:
- `CEHv13-Module06-System-Hacking`
- `CEHv13-Module08-Sniffing`

> ⚠️ **Legal & Ethical Use Notice**
> Everything in this repository — techniques, scripts, tool names, and workflows — is provided
> strictly for **authorized security education, certification study (CEH/OSCP/PenTest+), and
> sanctioned red-team / social-engineering-penetration-test engagements with signed
> authorization**. Social engineering attacks manipulate real people. Using any of this against
> an individual or organization without **explicit, documented, written permission** is illegal in
> virtually every jurisdiction (wire fraud, computer fraud, identity theft, and wiretapping
> statutes all commonly apply) and is a violation of the CEH Code of Ethics. If you are ever
> unsure whether an action is authorized — stop and get it in writing first.

---

## 📚 Table of Contents

| # | File | Topic |
|---|------|-------|
| 01 | [`01-social-engineering-concepts.md`](01-social-engineering-concepts.md) | What SE is, why it works, attacker psychology, targets, attack lifecycle |
| 02 | [`02-human-based-social-engineering.md`](02-human-based-social-engineering.md) | Impersonation, vishing, eavesdropping, tailgating, baiting, elicitation, and more |
| 03 | [`03-computer-based-social-engineering.md`](03-computer-based-social-engineering.md) | Phishing (all 9+ variants), spam, scareware, pop-ups, hoaxes, phishing toolkits |
| 04 | [`04-ai-powered-social-engineering.md`](04-ai-powered-social-engineering.md) | LLM-crafted phishing, writing-style cloning, deepfake video, AI voice cloning |
| 05 | [`05-mobile-based-social-engineering.md`](05-mobile-based-social-engineering.md) | Malicious/repackaged apps, fake security apps, SMiShing, QRLJacking |
| 06 | [`06-identity-theft-and-social-media.md`](06-identity-theft-and-social-media.md) | Identity theft types & techniques, Angler phishing, catfishing, corporate OSINT risk |
| 07 | [`07-social-engineering-countermeasures.md`](07-social-engineering-countermeasures.md) | Policies, technical controls, phishing/deepfake/voice-clone defenses, detection tools |
| 08 | [`08-social-engineering-penetration-testing.md`](08-social-engineering-penetration-testing.md) | **[Extra]** Full SE pentest methodology: scoping → recon → execution → reporting |
| — | [`cheatsheets/technique-quick-reference.md`](cheatsheets/technique-quick-reference.md) | One-page lookup of every technique, one-liner definitions |
| — | [`cheatsheets/tools-and-commands.md`](cheatsheets/tools-and-commands.md) | Every tool mentioned + install/run commands + official links |

---

## 🎯 Learning Objectives

By the end of this module, you should be able to:

- [ ] Describe social engineering concepts, attacker psychology, and the SE attack lifecycle
- [ ] Explain and recognize human-based social engineering techniques
- [ ] Explain and recognize computer-based social engineering techniques (phishing & its variants)
- [ ] Explain AI-augmented social engineering (LLM phishing, deepfakes, voice cloning)
- [ ] Explain and recognize mobile-based social engineering techniques
- [ ] Describe identity theft, its types, and social-media-based impersonation
- [ ] Apply organizational and personal countermeasures against social engineering
- [ ] Understand how a sanctioned social engineering penetration test is planned and run

---

## 🧠 What Is Social Engineering? (30-Second Version)

Social engineering is the art of manipulating people — rather than machines — into breaking
normal security procedures and divulging confidential information or performing an action that
benefits the attacker. There is no patch for human trust, curiosity, fear, greed, or the desire
to be helpful, which is exactly why social engineering is often the **fastest and cheapest path**
into an otherwise well-defended organization. No firewall, EDR, or IDS stops an employee from
voluntarily handing over a password to someone who sounds like their IT department.

```
        RECONNAISSANCE          ATTACK EXECUTION            EXPLOITATION
   ┌────────────────────┐   ┌───────────────────────┐   ┌──────────────────────┐
   │ OSINT / dumpster    │──▶│ Pretext + technique    │──▶│ Credential theft,     │
   │ diving / social     │   │ (call, email, app,     │   │ malware install,      │
   │ media / org chart   │   │ SMS, in-person, QR)    │   │ physical access,      │
   └────────────────────┘   └───────────────────────┘   │ fraud, data exfil     │
                                                          └──────────────────────┘
```

## 🌳 Taxonomy of Social Engineering (this module's structure)

```
Social Engineering
├── Human-based            (direct interpersonal manipulation)
│   ├── Impersonation (7+ personas) · Vishing · Eavesdropping
│   ├── Shoulder Surfing · Dumpster Diving · Reverse SE
│   └── Piggybacking · Tailgating · Diversion Theft · Honey Trap
│       Baiting · Quid Pro Quo · Elicitation · Bait-and-Switch
│
├── Computer-based         (relies on computers/Internet systems)
│   ├── Phishing → Spear Phishing, Whaling, Pharming, Spimming,
│   │              Clone Phishing, E-wallet Phishing, Tabnabbing,
│   │              Consent Phishing, Search Engine Phishing
│   ├── AI-powered: LLM phishing copy, writing-style cloning,
│   │              deepfake video, voice cloning
│   ├── Pop-ups · Hoax Letters · Chain Letters
│   └── Instant Chat Messenger · Spam Email · Scareware
│
└── Mobile-based           (relies on mobile apps/SMS/QR)
    ├── Publishing Malicious Apps · Repackaging Legitimate Apps
    ├── Fake Security Applications · SMiShing (SMS Phishing)
    └── QRLJacking
```

## 📦 Repository Structure

```
CEHv13-Module09-Social-Engineering/
├── README.md                                   ← you are here
├── 01-social-engineering-concepts.md
├── 02-human-based-social-engineering.md
├── 03-computer-based-social-engineering.md
├── 04-ai-powered-social-engineering.md
├── 05-mobile-based-social-engineering.md
├── 06-identity-theft-and-social-media.md
├── 07-social-engineering-countermeasures.md
├── 08-social-engineering-penetration-testing.md
└── cheatsheets/
    ├── technique-quick-reference.md
    └── tools-and-commands.md
```

## 🗺️ Exam Mapping (CEH 312-50, Module 09)

| Exam Objective | Covered In |
|---|---|
| Summarize social engineering concepts | `01` |
| Explain human-based SE techniques | `02` |
| Explain computer-based SE techniques | `03`, `04` |
| Explain mobile-based SE techniques | `05` |
| Explain social engineering countermeasures | `07` |
| (Bonus, not on exam) SE pentest methodology | `08` |

## 🔗 How to Use This Repo

1. Read `01` → `07` in order — each builds on the vocabulary of the last.
2. Keep `cheatsheets/technique-quick-reference.md` open while doing practice questions —
   CEH loves matching a scenario ("attacker calls the help desk pretending...") to a named
   technique.
3. `08` is supplementary — useful if you're heading toward OSCP, a red-team role, or actually
   plan to run an authorized SE assessment; skip it if you're purely exam-focused.
4. Every tool mentioned has an official source link in `cheatsheets/tools-and-commands.md` —
   never download security tools from anywhere else.

## 📖 Module Summary

This module covers social engineering concepts and the phases of a social engineering attack; the
three technique families (human-based, computer-based, mobile-based); AI-assisted impersonation
(deepfakes, voice cloning, LLM-crafted phishing); impersonation on social networking sites;
identity theft and its variants; and the countermeasures — password/physical-security policy,
technical controls, phishing detection, and anti-phishing/anti-deepfake tooling — used to defend
against all of the above.

---

*Compiled as personal certification study notes. Original wording and structure — not a
reproduction of any vendor's copyrighted courseware. Tool names, defensive frameworks, and
publicly documented techniques are referenced for educational purposes with links to official
sources.*