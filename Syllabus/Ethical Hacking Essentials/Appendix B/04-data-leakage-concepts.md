# Appendix B: Ethical Hacking Essential Concepts – II
## Part 4 — Data Leakage Concepts

[← Back to Part 3: Network Security Solutions](03-network-security-solutions.md) | [Next: Data Backup Process →](05-data-backup.md)

---

## Table of Contents

1. [What Is Data Leakage?](#what-is-data-leakage)
2. [Major Risks to Organizations](#major-risks-to-organizations)
3. [Data Leakage Threats](#data-leakage-threats)
4. [Data Loss Prevention (DLP)](#data-loss-prevention-dlp)
5. [Quick-Reference Summary](#quick-reference-summary)

---

## What Is Data Leakage?

**Data leakage** refers to the unauthorized access or disclosure of sensitive or confidential data. It may happen electronically through an email or a malicious link, or via some physical method such as device theft or a hacker break-in.

---

## Major Risks to Organizations

Data leakage exposes an organization to a wide range of downstream harms:

- Loss of customer loyalty
- Potential litigation
- Heavy fines
- Decline in share value
- Loss of brand name
- Loss of reputation
- Reduction of sales and revenue
- Unfavorable media attention
- Unfavorable competitor advantage
- Insolvency or liquidation
- Loss of new and existing customers
- Monetary loss
- Increased exposure to cyber criminal attacks
- Loss of productivity
- Disclosure of trade secrets
- Pre-release of the latest technology developed by the company
- Loss of proprietary and customer information
- Ready-to-release projects getting pirated

---

## Data Leakage Threats

| Insider Threats | External Threats |
|---|---|
| Disgruntled or negligent employees may knowingly or unknowingly leak sensitive data to the outside world, incurring huge financial losses and business interruptions | Attackers take advantage of insiders' vulnerabilities to perform various attacks by **stealing the credentials** of a legitimate employee |
| Employees may use various techniques such as eavesdropping, shoulder surfing, or dumpster diving to gain unauthorized access to information, in violation of corporate policies | This gives the attacker unlimited access to the target network |

### Reasons for Insider Threats

- Inadequate security awareness and training
- Lack of proper management controls for monitoring employee activities
- Use of an insecure mode of data transfers

### Examples of External Threats

- Hacking or code injection attacks
- Malware
- Phishing
- Corporate espionage or competitors
- Business partners or contractors

---

## Data Loss Prevention (DLP)

**DLP** is the identification and monitoring of sensitive data, to ensure that end users do not send sensitive information outside the corporate network.

**How it works:** a DLP agent monitors what an employee sends from their machine into the enterprise network. A **DLP server** inspects outbound traffic heading toward external destinations — web mail, supplier networks, social networks, and partner networks — and either **blocks** or **encrypts** it based on policy, depending on the sensitivity of the content and the destination.

---

## Quick-Reference Summary

- **Data leakage** = unauthorized access/disclosure of sensitive data, via electronic (email, malicious links) or physical (device theft, break-ins) means
- **18 major organizational risks** span financial (fines, monetary loss, lost sales), reputational (brand/media/customer loyalty), and competitive (trade secrets, pirated projects) categories
- **Insider threats**: disgruntled/negligent employees, often enabled by weak training, poor monitoring, or insecure transfer methods
- **External threats**: attackers stealing legitimate employee credentials via hacking, malware, phishing, or through compromised partners/contractors
- **DLP** = policy-driven inspection of outbound traffic, blocking or encrypting sensitive data before it leaves the corporate network

---

*Part of the CEH Appendix B study series — continues in [Part 5: Data Backup Process](05-data-backup.md).*
