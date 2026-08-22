# Appendix B: Ethical Hacking Essential Concepts – II
## Part 12 — Different Phases of Computer Forensic Investigation

[← Back to Part 11: Security Operations Concepts](11-security-operations.md) | [Next: Software Development Security →](13-software-development-security.md)

---

## Table of Contents

1. [Computer Forensics](#computer-forensics)
2. [Objectives of Computer Forensics](#objectives-of-computer-forensics)
3. [Phases Involved in the Computer Forensics Investigation Process](#phases-involved-in-the-computer-forensics-investigation-process)
4. [Pre-Investigation Phase](#pre-investigation-phase)
5. [Investigation Phase](#investigation-phase)
6. [Post-Investigation Phase](#post-investigation-phase)
7. [Quick-Reference Summary](#quick-reference-summary)

---

## Computer Forensics

**Computer forensics** refers to a set of methodological procedures and techniques that help identify, gather, preserve, extract, interpret, document, and present evidence from computing equipment — such that any evidence discovered is **acceptable during a legal or administrative proceeding**.

---

## Objectives of Computer Forensics

1. To track and prosecute cyber crime perpetrators
2. To gather evidence of cyber crimes in a forensically sound manner
3. To estimate the potential impact of a malicious activity on the victim and assess the intent of the perpetrator
4. To find vulnerabilities and security loopholes that help attackers
5. To recover deleted files, hidden files, and temporary data that could be used as evidence

---

## Phases Involved in the Computer Forensics Investigation Process

```mermaid
flowchart LR
    A["Pre-investigation Phase"] --> B["Investigation Phase"]
    B --> C["Post-investigation Phase"]
```

| Phase | Description |
|---|---|
| **Pre-investigation Phase** | Deals with tasks to be performed prior to commencing the actual investigation — setting up a computer forensics lab, building a forensics workstation, developing an investigation toolkit, setting up an investigation team, gaining approval from the relevant authority, and so on |
| **Investigation Phase** | The **main phase** of the computer forensics investigation process — involves the acquisition, preservation, and analysis of evidentiary data to identify the source of the crime and the culprit behind it |
| **Post-investigation Phase** | Deals with the documentation of all actions undertaken and findings uncovered during an investigation; ensures the report is well explicable to the target audience and provides adequate and acceptable evidence |

---

## Pre-Investigation Phase

### Steps Involved in the Pre-Investigation Phase

| Step | Description |
|---|---|
| **Set Up a Computer Forensics Lab** | A computer forensics lab (CFL) is a designated location for conducting computer-based investigation of the collected evidence, in order to solve the case and find the culprit |
| **Build the Investigation Team** | The team is responsible for evaluating the crime, evidence, and criminals |
| **Review Policies and Laws** | Identify possible concerns related to applicable federal statutes, state statutes, and local policies and laws |
| **Establish Quality Assurance Processes** | Establish and follow a well-documented systematic process for investigating a case that ensures quality assurance |
| **Data Destruction Industry Standards** | Destruction of data using industry-standard data destruction methods is essential for sensitive data that one does not want falling into the wrong hands |
| **Risk Assessment** | Useful to understand information security issues in a business context and to assess their impact on the business |

---

## Investigation Phase

### Initiate the Investigation Process

Incident responders should have a **clear idea about the goals of the examination** prior to conducting the investigation.

### Perform Computer Forensics Investigation

1. **First Response**
2. **Search and Seizure**
3. **Collect the Evidence**
4. **Secure the Evidence**
5. **Data Acquisition**
6. **Data Analysis**

---

## Post-Investigation Phase

### Steps Involved in the Post-Investigation Phase

| Step | Description |
|---|---|
| **Evidence Assessment** | The process of relating the obtained evidential data to the incident, to understand how the complete incident took place |
| **Documentation and Reporting** | The process of writing down all actions the incident responders performed during the investigation, to obtain the desired results |
| **Testify as an Expert Witness** | Court members may be unaware of the technical knowledge regarding the crime, evidence, and losses — investigators should approach authorized personnel who can appear in court to affirm the accuracy of the process and the data |

---

## Quick-Reference Summary

- **Computer forensics** = identifying, gathering, preserving, extracting, interpreting, documenting, and presenting digital evidence in a legally acceptable way
- **5 objectives**: track/prosecute perpetrators, gather forensically-sound evidence, assess impact/intent, find vulnerabilities attackers exploited, recover deleted/hidden/temp data
- **3-phase process**: Pre-investigation (lab/team/policy/QA/data-destruction-standards/risk-assessment setup) → Investigation (the main phase: first response → search & seizure → collect → secure → acquire → analyze) → Post-investigation (evidence assessment, documentation/reporting, expert witness testimony)

---

*Part of the CEH Appendix B study series — continues in [Part 13: Software Development Security](13-software-development-security.md).*
