# Appendix B: Ethical Hacking Essential Concepts – II
## Part 9 — Threat Modeling Methodology

[← Back to Part 8: Cyber Threat Intelligence](08-cyber-threat-intelligence.md) | [Next: Penetration Testing →](10-penetration-testing.md)

---

## Table of Contents

1. [Threat Modeling Methodologies](#threat-modeling-methodologies)
2. [STRIDE](#stride)
3. [PASTA](#pasta)
4. [TRIKE](#trike)
5. [VAST](#vast)
6. [DREAD](#dread)
7. [OCTAVE](#octave)
8. [Threat Profiling and Attribution](#threat-profiling-and-attribution)
9. [Quick-Reference Summary](#quick-reference-summary)

---

## Threat Modeling Methodologies

Six named methodologies are commonly used to structure threat modeling work — each with a different emphasis, from developer-facing threat classification to full risk-quantification formulas.

---

## STRIDE

**STRIDE** stands for **S**poofing, **T**ampering, **R**epudiation, **I**nformation disclosure, **D**enial-of-Service, and **E**levation of privilege.

- Used by analysts to **classify threats**
- Once a DFD-based (Data Flow Diagram) threat model is developed, an analyst can check its application against the STRIDE methodology

---

## PASTA

**PASTA** stands for **P**rocess for **A**ttack **S**imulation and **T**hreat **A**nalysis — a **seven-stage** methodology:

1. **Definition of Objectives (DO)**
2. **Definition of Technical Scope (DTS)**
3. **Application Decomposition and Analysis (ADA)**
4. **Threat Analysis (TA)**
5. **Weakness and Vulnerability Analysis (WVA)**
6. **Attack Modeling and Simulation (AMS)**
7. **Risk and Analysis Management (RAM)**

---

## TRIKE

**TRIKE** is an **open-source** threat modeling methodology that follows a **risk management approach**. Models that effectively form the levels of the TRIKE methodology:

- **Requirements Model**
- **Implementation Model**
- **Threat Model**
- **Risk Model**

---

## VAST

**VAST** stands for **V**isual, **A**gile, and **S**imple **T**hreat modeling.

- The primary objective of this methodology is to **scale threat modeling across the infrastructure and entire DevOps portfolio**
- Based on a practical approach in the development of the following threat models:
  - **Application Threat Model**
  - **Operational Threat Model**

---

## DREAD

**DREAD** stands for **D**amage, **R**eproducibility, **E**xploitability, **A**ffected Users, and **D**iscoverability.

- A sorting scheme for calculating, comparing, and ranking the possible extent of threat for each assessed risk
- **DREAD formula:**

```
Risk = (Damage + Reproducibility + Exploitability + Affected Users + Discoverability) / 5
```

---

## OCTAVE

**OCTAVE** stands for **O**perationally **C**ritical **T**hreat, **A**sset, and **V**ulnerability **E**valuation.

### Three Stages of the OCTAVE Methodology

1. **Build Asset-Based Threat Profiles**
2. **Identify Infrastructure Vulnerabilities**
3. **Develop Security Strategy and Plans**

---

## Threat Profiling and Attribution

**Threat profiling and attribution** involves collecting information about threat actors and **building an analytic profile of the adversary** — describing the adversary's technological details, goals, and motives, which can be resourceful in building a strong countermeasure.

### The Threat Profile Can Be Created to Include Details of the Following Attributes

1. Description
2. Motive
3. Intent
4. Capability
5. Ownership Detail
6. Target Detail
7. Operating Methods
8. Objective

---

## Quick-Reference Summary

- **STRIDE** — classifies threats into 6 categories (Spoofing, Tampering, Repudiation, Information disclosure, DoS, Elevation of privilege); checked against a DFD-based threat model
- **PASTA** — 7-stage attack-simulation methodology (DO → DTS → ADA → TA → WVA → AMS → RAM)
- **TRIKE** — open-source, risk-management-based; 4 models (Requirements, Implementation, Threat, Risk)
- **VAST** — scales threat modeling across DevOps via Application + Operational threat models
- **DREAD** — quantifies risk via `(Damage + Reproducibility + Exploitability + Affected Users + Discoverability) / 5`
- **OCTAVE** — 3-stage methodology (asset-based threat profiles → infrastructure vulnerabilities → security strategy)
- **Threat profiling/attribution** — builds an 8-attribute adversary profile (description, motive, intent, capability, ownership, target, operating methods, objective)

---

*Part of the CEH Appendix B study series — continues in [Part 10: Penetration Testing](10-penetration-testing.md).*
