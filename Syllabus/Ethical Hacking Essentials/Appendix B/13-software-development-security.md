# Appendix B: Ethical Hacking Essential Concepts – II
## Part 13 — Software Development Security

[← Back to Part 12: Computer Forensic Investigation](12-computer-forensics.md) | [Next: Security Governance Principles →](14-security-governance.md)

---

## Table of Contents

1. [Integrating Security in the SDLC](#integrating-security-in-the-sdlc)
2. [Functional vs. Security Activities in the SDLC](#functional-vs-security-activities-in-the-sdlc)
3. [Advantages of Integrating Security in the SDLC](#advantages-of-integrating-security-in-the-sdlc)
4. [Security Requirements](#security-requirements)
5. [Gathering Security Requirements](#gathering-security-requirements)
6. [Secure Application Design and Architecture](#secure-application-design-and-architecture)
7. [Secure Design Principles](#secure-design-principles)
8. [Designing Secure Application Architecture](#designing-secure-application-architecture)
9. [Quick-Reference Summary](#quick-reference-summary)

---

## Integrating Security in the SDLC

Security should be a first-class concern woven through every phase of the **Software Development Life Cycle (SDLC)**, not bolted on at the end.

### Security Software Development Process

| Phase | Security Activities |
|---|---|
| **Requirement** | Security Requirements |
| **Design** | Security Requirements, Secure Coding Standards, Threat Modeling, Security Architecture |
| **Development** | Secure Coding Standards, Secure Design Patterns and Frameworks, Secure Coding Practices |
| **Testing** | Secure Code Review, Vulnerability Assessment, Penetration Testing |
| **Deployment** | Secure Deployment |
| **Maintenance** | Security Patch Updates |

---

## Functional vs. Security Activities in the SDLC

| SDLC Phase | Functional Activities | Security Activities |
|---|---|---|
| **Requirement** | Functional requirements, non-functional requirements, technology requirements | Defining the security requirements |
| **Design** | Decide the guidelines and architectural design of the project | Create a secure design, set secure coding standards, perform threat modeling, secure the architecture |
| **Development** | Functional programming logic, unit testing | Implementing security requirements, implementing secure coding standards, adopting secure coding practices |
| **Testing** | Functional testing such as black-box, grey-box, and white-box testing | Security testing |
| **Deployment** | Deployment | Ensure secure deployment |
| **Maintenance** | Update functionality | Update the system with security patches |

---

## Advantages of Integrating Security in the SDLC

- Reduces the presence of software vulnerabilities to a great extent
- Can comply with regulations, standards, or requirements for secure software development
- Reduces costly rework by detecting and eliminating flaws at the earliest phase
- Improves developer job satisfaction
- Improves customer satisfaction
- Embeds a security culture that improves quality and reliability
- Reuses trusted software in future development
- Reduces maintenance costs

---

## Security Requirements

**Non-functional** requirements that need to be addressed to maintain the confidentiality, integrity, and availability of an application.

- Stakeholders often overlook security requirements during the inception phase of software development
- This negligence may result in the application being vulnerable to different types of attacks or abuse
- Gathering security requirements should be part of the strategic application development process

---

## Gathering Security Requirements

1. Eliciting software security requirements takes different approaches
2. Security requirements should be **enumerated separately** from functional requirements, so they can be separately reviewed and tested
3. Mixing security requirements with functional requirements can make the security-requirement-gathering process more complicated and less accurate

### Why We Need Different Approaches for Security Requirement Gathering

1. Functional requirements are **positive requirements** — specifying what the software *should* do
2. Security requirements are **negative requirements** — specifying what the software *should not* do
3. It's the natural tendency of people to be clear about what they want, but to find it difficult to understand things they *don't* want
4. Software needs to be viewed in a more negative, critical, and destructive way to reveal its non-intended use and its associated security requirements

### Key Benefits of Addressing Security at the Requirement Phase

- Addressing security at the requirement phase can save **billions of dollars** compared to addressing security at a later phase of software development
- Specifies the security mechanisms needed to comply with regulations, standards, or requirements for secure application development and attack protection
- Gives the developer an overview of the key security controls required to build a secure application
- Correctly understood security requirements help implement security in the design, development, and testing stages

---

## Secure Application Design and Architecture

1. Security negligence in the design and architecture phase may lead to vulnerabilities that are difficult to detect and expensive to fix in production
2. Security vigilance in the design phase enables the detection of potential security flaws early in the software development lifecycle
3. Secure design of an application is based on the security requirements identified in the previous phase of the SDLC
4. Secure design is a **challenging process**, as designing required security controls may obstruct business functionality requirements

### Goals of the Secure Design Process

- Identify threats in sufficient detail for developers to understand and code accordingly to mitigate the associated risk
- Design the architecture in such a way that it mitigates as many threats as possible
- Enforce secure design principles that force developers to consider security while coding

---

## Secure Design Principles

**Secure Design Principles** are the practices or guidelines that should be enforced on developers during the development phase. They help derive secure architectural decisions, and help eliminate design and architecture flaws while mitigating common security vulnerabilities within an application.

### A List of Secure Design Principles to Prevent Common Security Vulnerabilities

- Security through obscurity
- Secure the weakest link
- Use least privilege principle
- Secure by default
- Fail securely
- Apply defense in depth
- Do not trust user input
- Reduce attack surface
- Enable auditing and logging
- Keep security simple
- Maintain a separation of duties
- Correctly fix security issues
- Apply security in the design phase
- Protect sensitive data
- Exception handling
- Secure memory management
- Protect memory or storage secrets
- Fundamentals of control granularity
- Fault tolerance
- Fault detection
- Fault removal
- Fault avoidance
- Loose coupling
- High cohesion
- Change management and version control

---

## Designing Secure Application Architecture

1. A typical web application architecture comprises **three tiers**: web, application, and database
2. Security at one tier is not enough — an attacker can breach the security of another tier to compromise the application
3. Design web application architecture with a **defense-in-depth** principle, providing security at each tier of the web application
4. Multi-tiered security includes proper input validation, database layer abstraction, server configuration, proxies, web application firewalls, data encryption, OS hardening, and other items

### The Three-Tier Security Model

| Tier | What Happens Here |
|---|---|
| **Tier 1 — Web Server** | Input validation, user authorization, secure exception handling, and secure configuration are done at this tier. The client running a browser connects through the internet and a firewall; a secure communication channel protects sensitive data in transit |
| **Tier 2 — Application Server** | Authenticating and authorizing upstream identities, and secure auditing/logging/tagging of transactions, is performed at this tier |
| **Tier 3 — Database Server** | Can encrypt or hash the data stored in the database, and protect sensitive database communication |

---

## Quick-Reference Summary

- **6 SDLC phases**, each with a matching security counterpart: Requirement (security requirements), Design (secure design/coding standards/threat modeling/architecture), Development (secure coding practices), Testing (secure code review/VA/pentest), Deployment (secure deployment), Maintenance (security patches)
- **8 advantages** of integrating security into the SDLC, ranging from fewer vulnerabilities to lower maintenance costs
- **Security requirements are negative requirements** (what software should *not* do) — the opposite framing from functional requirements, which is exactly why they need separate elicitation
- **25 secure design principles** listed, spanning least privilege, defense in depth, fail securely, secure-by-default, attack surface reduction, and more
- **3-tier architecture model**: Web tier (input validation/auth/config) → Application tier (upstream auth, logging) → Database tier (encryption/hashing, secure DB comms) — each tier needs its own defense-in-depth layer

---

*Part of the CEH Appendix B study series — continues in [Part 14: Security Governance Principles](14-security-governance.md).*
