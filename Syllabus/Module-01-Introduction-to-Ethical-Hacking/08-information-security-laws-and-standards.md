# Module 1: Introduction to Ethical Hacking
## Part H — Information Security Laws and Standards

[← Back to Part G: Information Security Controls](07-information-security-controls.md) | [Back to README](README.md)

---

## Table of Contents

1. [Laws vs. Standards](#laws-vs-standards)
2. [Payment Card Industry Data Security Standard (PCI DSS)](#payment-card-industry-data-security-standard-pci-dss)
3. [ISO/IEC Standards](#isoiec-standards)
4. [HIPAA](#hipaa)
5. [Sarbanes-Oxley Act (SOX)](#sarbanes-oxley-act-sox)
6. [DMCA and FISMA](#dmca-and-fisma)
7. [GDPR](#gdpr)
8. [UK Data Protection Act 2018 (DPA)](#uk-data-protection-act-2018-dpa)
9. [Cyber Law Around the World](#cyber-law-around-the-world)
10. [Module 1 Summary](#module-1-summary)

---

## Laws vs. Standards

Worth drawing the distinction up front, since the two terms get used almost interchangeably in casual conversation but mean different things:

- A **law** is a system of rules and guidelines enforced by a country or community to govern behavior.
- A **standard** is a document established by consensus and approved by a recognized body, providing rules, guidelines, or characteristics for common, repeated use — aimed at achieving the best possible degree of order in a given context.

Laws carry legal force; standards are widely-adopted best practice that often becomes a *de facto* requirement (particularly in regulated industries) even without being law in the strict sense.

---

## Payment Card Industry Data Security Standard (PCI DSS)

*Source: pcisecuritystandards.org*

**PCI DSS** is a proprietary information security standard for any organization handling cardholder data — debit, credit, prepaid, e-purse, ATM, and POS cards alike. It applies broadly: merchants, processors, acquirers, issuers, service providers, and any other entity that stores, processes, or transmits cardholder data. The PCI Security Standards Council maintains a high-level framework of specifications, tools, measurements, and support resources to help organizations handle cardholder data safely.

### High-Level Requirements

| Requirement Area | What It Covers |
|---|---|
| **Build and Maintain a Secure Network** | Secure network configuration as the baseline |
| **Protect Cardholder Data** | Data protection at rest and in transit |
| **Maintain a Vulnerability Management Program** | Use/update anti-virus software; develop and maintain secure systems and applications |
| **Implement Strong Access Control Measures** | Restrict cardholder-data access by business need-to-know; assign a unique ID to each person with computer access; restrict physical access to cardholder data |
| **Regularly Monitor and Test Networks** | Track and monitor all access to network resources and cardholder data; regularly test security systems and processes |
| **Maintain an Information Security Policy** | Maintain a policy addressing information security for all personnel |

**Failure to meet PCI DSS requirements can result in fines or the outright termination of an organization's payment-card processing privileges.**

---

## ISO/IEC Standards

*Source: iso.org*

| Standard | What It Covers |
|---|---|
| **ISO/IEC 27001:2022** | The core standard — requirements and framework for establishing, implementing, maintaining, and continually improving an Information Security Management System (ISMS) |
| **ISO/IEC 27701:2019** | Extends 27001 into privacy management — protecting Personally Identifiable Information (PII) via a Privacy Information Management System (PIMS) |
| **ISO/IEC 27002:2022** | Best practices and control objectives for critical cybersecurity areas: access control, cryptography, security personnel |
| **ISO/IEC 27005:2022** | Guidelines for information-security risk management, supporting the requirements of an ISMS as specified in 27001 |
| **ISO/IEC 27032:2023** | Covers the relationship between the Internet, the Web, network security, and cybersecurity broadly; identifies key stakeholders and their roles |
| **ISO/IEC 27033-7:2023** | Guidelines for implementing network virtualization security |
| **ISO/IEC 27036-3:2023** | Guidelines for securing hardware, software, and services supply chains |
| **ISO/IEC 27040:2024** | Technical requirements and guidance for data storage security (planning, design, documentation, implementation) |

### Why ISO/IEC 27001 Specifically Matters

As the flagship standard in the family, ISO/IEC 27001 is designed to:

- Provide a structured approach for identifying, assessing, and managing information security risks
- Help organizations meet regulatory, legal, and contractual obligations around information security
- Strengthen overall security posture and reduce the risk of breaches
- Keep security practices current as threats and the organization itself evolve
- Build trust with customers, partners, and other stakeholders by demonstrating a real commitment to information security
- Ensure security measures keep pace with technological change
- Clarify communication of information security roles and responsibilities across the organization

---

## HIPAA

*Health Insurance Portability and Accountability Act — Source: hhs.gov*

HIPAA's **Administrative Simplification** provisions break down into several linked rules:

| Rule | What It Does |
|---|---|
| **Electronic Transaction and Code Set Standards** | Requires any provider doing business electronically to use the same healthcare transaction and code sets |
| **Privacy Rule** | Federal protections for personally identifiable health information held by covered entities; gives patients real rights over their own health information |
| **Security Rule** | Administrative, physical, and technical safeguards for covered entities to protect the confidentiality, integrity, and availability of electronically protected health information |
| **National Identifier Requirements** | Standard national ID numbers for healthcare providers, health plans, and employers, tied to standard transactions |
| **Enforcement Rule** | Standards for enforcing all of the above — including compliance investigations and civil monetary penalties for violations |

A couple of specific identifiers worth knowing: the **Employer Identifier Standard** requires a standard national number for each employer on standard transactions, and the **National Provider Identifier (NPI)** is a unique 10-digit, intelligence-free numeric ID assigned to every covered healthcare provider (it deliberately carries no embedded information like state or specialty).

---

## Sarbanes-Oxley Act (SOX)

*Source: sec.gov — enacted 2002*

SOX exists to protect the public and investors by increasing the accuracy and reliability of corporate financial disclosures. It's organized into 11 titles; the ones most relevant to a security/audit context:

| Title | Focus |
|---|---|
| **I — Public Company Accounting Oversight Board (PCAOB)** | Establishes independent oversight of public accounting/auditing firms |
| **II — Auditor Independence** | Limits conflicts of interest; restricts auditors from providing non-audit (e.g., consulting) services to the same client |
| **III — Corporate Responsibility** | Makes senior executives personally responsible for the accuracy of financial reports |
| **IV — Enhanced Financial Disclosures** | Requires internal controls to ensure accurate reporting, including off-balance-sheet transactions |
| **V — Analyst Conflicts of Interest** | Code of conduct for securities analysts; requires disclosure of known conflicts |
| **VI — Commission Resources and Authority** | Defines the SEC's authority to censure/bar securities professionals |
| **VII — Studies and Reports** | Mandates SEC/Comptroller General studies on accounting consolidation, credit-rating agencies, and enforcement |
| **VIII — Corporate and Criminal Fraud Accountability** | Makes corporate fraud and records tampering criminal offenses with defined penalties |
| **IX — White-Collar Crime Penalty Enhancement** | Strengthens penalties for white-collar crime |
| **X — Corporate Tax Returns** | Tax-related provisions |
| **XI — Corporate Fraud Accountability** | Allows the SEC to temporarily freeze "large" or "unusual" transactions or payments |

---

## DMCA and FISMA

### The Digital Millennium Copyright Act (DMCA)

The DMCA is the primary US copyright law implementing two 1996 WIPO treaties. It establishes legal prohibitions against circumventing technical protection measures used by copyright holders, and against tampering with copyright management information. It's organized into five titles:

| Title | Focus |
|---|---|
| **I — WIPO Treaty Implementation** | Implements the WIPO treaties; creates prohibitions on circumventing copy-protection tech and on tampering with copyright management info, with civil and criminal penalties |
| **II — Online Copyright Infringement Liability Limitation** | Adds 4 liability-limitation categories for online service providers: transitory communications, system caching, user-directed storage, and information-location tools |
| **III–IV** | Cover exemptions for libraries/archives, webcasting amendments, and residual-payment protections for creative talent |
| **V — Protection of Certain Original Designs** | The Vessel Hull Design Protection Act — protects original vessel-hull designs (hulls up to 200 feet) |

### The Federal Information Security Management Act (FISMA)

*Source: csrc.nist.gov — enacted 2002*

FISMA provides a comprehensive framework for the effectiveness of information security controls over the systems that support US federal operations and assets. It requires every federal agency to develop, document, and implement an agency-wide information security program — including systems managed by contractors or other agencies on their behalf. The framework includes:

- Standards for categorizing information and information systems by mission impact
- Standards for the minimum security requirements for information and information systems
- Guidance for selecting appropriate security controls for information systems
- Guidance for assessing security controls in information systems

---

## GDPR

*General Data Protection Regulation — in effect since May 25, 2018*

GDPR is one of the most stringent privacy and security regulations in the world, with penalties for violations reaching tens of millions of euros. It represents Europe's clearest statement yet that data privacy is a serious legal matter — particularly relevant as more organizations move data into cloud services and breaches become a near-daily occurrence. It's extensive and, notably, fairly light on prescriptive specifics — which makes full compliance a genuinely difficult exercise, especially for smaller organizations.

### The 7 GDPR Data Protection Principles (Article 5.1–2)

1. **Lawfulness, fairness, and transparency** — processing must be lawful, fair, and transparent to the data subject
2. **Purpose limitation** — data may only be processed for the legitimate purposes explicitly stated at collection time
3. **Data minimization** — collect and process only as much data as the stated purpose actually requires
4. **Accuracy** — personal data must be kept accurate and up to date
5. **Storage limitation** — personal data may only be stored as long as necessary for its specified purpose
6. **Integrity and confidentiality** — processing must ensure appropriate security, integrity, and confidentiality (e.g., via encryption)
7. **Accountability** — the data controller is responsible for demonstrating compliance with all of the above

---

## UK Data Protection Act 2018 (DPA)

*Source: legislation.gov.uk*

The DPA 2018 is the UK's core data protection framework — it replaced the Data Protection Act 1998, came into effect May 25, 2018, and was amended January 1, 2021 to reflect the UK's post-Brexit status outside the EU.

It regulates the processing of information relating to individuals, defines the Information Commissioner's functions under related regulations, establishes a direct-marketing code of practice, and sets out separate data protection rules for law enforcement — extending into areas like national security and defense. The Commissioner is required to weigh the importance of appropriate data protection against the interests of data subjects, controllers, and the broader public whenever exercising functions under GDPR, the applied GDPR, or this Act.

---

## Cyber Law Around the World

Cyberlaw (or Internet law) covers any legal framework aimed at protecting the internet and related communication technologies — internet access and usage, privacy, freedom of expression, and jurisdiction. These laws exist to assure the integrity, security, privacy, and confidentiality of information across both government and private organizations, and have become increasingly prominent simply because internet usage keeps growing globally. Because cyber law varies significantly by jurisdiction, implementation is genuinely difficult, and violations can range from fines to imprisonment depending on the country.

| Country | Key Laws/Acts |
|---|---|
| **United States** | Copyright Law (Section 107, "fair use"); Online Copyright Infringement Liability Limitation Act; Lanham (Trademark) Act; Electronic Communications Privacy Act; Foreign Intelligence Surveillance Act; Identity Theft and Assumption Deterrence Act; Computer Fraud and Abuse Act; California Consumer Privacy Act (CCPA); California Privacy Rights Act (2020) |
| **Australia** | Trademarks Act 1995; Patents Act 1990; Copyright Act 1968; Cybercrime Act 2001 |
| **United Kingdom** | Copyright, Etc. and Trademarks (Offenses and Enforcement) Act 2002; Trademarks Act 1994; Computer Misuse Act 1990; Network and Information Systems Regulations 2018; Communications Act 2003; Privacy and Electronic Communications (EC Directive) Regulations 2003; Investigatory Powers Act 2016; Regulation of Investigatory Powers Act 2000 |
| **China** | Copyright Law of the People's Republic of China (amended 2001); Trademark Law of the People's Republic of China (amended 2001) |
| **India** | Patents (Amendment) Act 1999; Trade Marks Act 1999; Copyright Act 1957; Information Technology Act |
| **Germany** | Section 202a (Data Espionage); Section 303a (Alteration of Data); Section 303b (Computer Sabotage) |
| **Italy** | Penal Code Article 615-ter |
| **Japan** | Trademark Law (Law No. 127 of 1958) |
| **Canada** | Copyright Act (R.S.C., 1985, c. C-42); Trademarks Act; Canadian Criminal Code Section 342.1; Personal Information Protection and Electronic Documents Act (PIPEDA) |
| **Singapore** | Computer Misuse Act |
| **South Africa** | Trademarks Act 194 of 1993 |
| **Belgium** | Computer Hacking law |
| **Brazil** | Brazilian General Data Protection Law (LGPD) |
| **Hong Kong** | Article 139 of the Basic Law |
| **Philippines** | Republic Act No. 10175 |

---

## Module 1 Summary

That closes out Module 1. Across this eight-part series, the module covered:

- **Elements of information security**, information security attacks, and information warfare ([Part A](01-information-security-concepts.md))
- **Hacking concepts and hacker classes** ([Part B](02-hacking-concepts-and-hacker-classes.md))
- **Ethical hacking concepts** — scope, limitations, and required skills, alongside **AI-driven ethical hacking** ([Parts C](03-ethical-hacking-concepts-and-scope.md) & [D](04-ai-driven-ethical-hacking.md))
- **Hacking methodologies and frameworks** — the CEH framework, the Cyber Kill Chain, the MITRE ATT&CK framework, and the Diamond Model of Intrusion Analysis ([Parts E](05-hacking-methodologies-and-frameworks.md) & [F](06-mitre-attck-and-diamond-model.md))
- **Information security controls** — defense-in-depth, risk management, cyber threat intelligence, threat modeling, incident management, and AI/ML ([Part G](07-information-security-controls.md))
- **Information security acts and laws** from around the world (this file)

The next module examines how both attackers and ethical hackers/pen testers perform **footprinting** — collecting information about a target before an attack or an audit — covered in the companion [`CEH-Module-02-Footprinting-and-Reconnaissance`](../Module-02-Footprinting-and-Reconnaissance/README.md) repo folder.

---

*Part of the CEH Module 1 study series. [Return to the README](README.md) for the full index.*
