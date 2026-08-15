# Appendix B: Ethical Hacking Essential Concepts – II
## Part 7 — Business Continuity and Disaster Recovery Process

[← Back to Part 6: Risk Management Concepts and Frameworks](06-risk-management.md) | [Next: Cyber Threat Intelligence →](08-cyber-threat-intelligence.md)

---

## Table of Contents

1. [Business Continuity (BC)](#business-continuity-bc)
2. [Disaster Recovery (DR)](#disaster-recovery-dr)
3. [Business Impact Analysis (BIA)](#business-impact-analysis-bia)
4. [Recovery Time Objective (RTO)](#recovery-time-objective-rto)
5. [Recovery Point Objective (RPO)](#recovery-point-objective-rpo)
6. [Business Continuity Plan (BCP)](#business-continuity-plan-bcp)
7. [Disaster Recovery Plan (DRP)](#disaster-recovery-plan-drp)
8. [Quick-Reference Summary](#quick-reference-summary)

---

## Business Continuity (BC)

**BC** describes the processes and procedures that should be followed to ensure the continuity of an organization's **mission-critical business functions** during and after a disaster. Per the ISO standard, BC is the capability of an organization to continue delivering products or services at predefined acceptable levels following a disruptive incident. It's a **business-centric strategy**, emphasizing maintaining business operations over IT infrastructure specifically.

### Objectives of Business Continuity

- Maintain the continuity of operations during and after a disruptive incident
- Protect the reputation of the organization by providing continuity of services
- Prepare organizations against disasters, minimizing their aftereffects
- Provide compliance benefits
- Mitigate business risks and minimize financial losses

---

## Disaster Recovery (DR)

**DR** refers to the organization's ability to **restore its business data and applications**, even after a disaster. It includes recovering the systems and people responsible for rebuilding data centers, servers, or other infrastructure damaged in a disruptive incident. A **data-centric strategy** that emphasizes quickly restoring an organization's IT infrastructure and data.

### Objectives of Disaster Recovery

- Reduce the downtime faced by an organization during and after a disruptive incident
- Reduce the accrual of losses during and after a disaster
- Recover any data that's damaged due to hardware failure

---

## Business Impact Analysis (BIA)

**BIA** is a systematic process that determines and evaluates the potential effects of an interruption to critical business operations as a result of a disaster, accident, or emergency.

1. Ascertains the recovery time and recovery requirements for various disaster scenarios
2. The underlying assumption in a BIA is that while each component of an organization is reliant on the continued functioning of every other component, some components are more crucial than others — limited funds should be **prioritized** to ensure recovery in the wake of a disaster
3. BIA is an **analysis tool** — it does not focus on the design or implementation of recovery solutions

---

## Recovery Time Objective (RTO)

**RTO** is the maximum tolerable length of time that a computer, system, network, or application can be down after a failure or disaster.

- Defines the extent to which an interruption affects normal business operations and the amount of revenue lost due to that interruption
- Preferably given in minutes — e.g., an RTO of 45 minutes implies IT operations must be restarted within 45 minutes

---

## Recovery Point Objective (RPO)

**RPO** is the maximum time frame an organization is willing to lose data for, in the event of a major IT outage.

- Provides a target for designing disaster recovery and business continuity solutions
- Every organization needs to calculate how long it can operate without its required data before the business suffers

---

## Business Continuity Plan (BCP)

A **BCP** is a comprehensive document formulated to **ensure resilience against potential threats** and allow operations to continue under adverse or abnormal conditions.

### BCP Goals

- Analyzing the potential risks and losses
- Enabling the risk management process to lessen the prospect of a disruption reaching the worst-case scenario of shutting the business down completely
- Prioritizing the safety, health, and welfare of the organization and its staff
- Minimizing infrastructural damage in the event of a disaster
- Recuperating to normal operating conditions after a disruption
- Maintaining vital documents and details — telephone numbers, employee details, vendor details, client details
- Providing training and awareness to staff on their roles and responsibilities, to keep them better prepared

---

## Disaster Recovery Plan (DRP)

A **DRP** is developed for specific departments within an organization to allow them to **recover from a disaster**.

### DRP Goals

- Reduce overall organizational risk
- Alleviate senior management concerns
- Ensure compliance with regulations
- Ensure rapid response to incidents

---

## Quick-Reference Summary

- **BC** = business-centric continuity of mission-critical functions; **DR** = data-centric restoration of IT infrastructure/data — two complementary strategies, not the same thing
- **BIA** = the analysis tool that determines recovery priorities and requirements (but doesn't design the actual recovery solutions)
- **RTO** = maximum tolerable downtime (measured in minutes); **RPO** = maximum tolerable data loss window
- **BCP** = the comprehensive resilience document (7 goals, org-wide); **DRP** = department-specific recovery plans (4 goals)

---

*Part of the CEH Appendix B study series — continues in [Part 8: Cyber Threat Intelligence](08-cyber-threat-intelligence.md).*
