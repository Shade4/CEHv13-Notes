# Appendix B: Ethical Hacking Essential Concepts – II
## Part 8 — Cyber Threat Intelligence

[← Back to Part 7: Business Continuity and Disaster Recovery](07-business-continuity-and-disaster-recovery.md) | [Next: Threat Modeling Methodology →](09-threat-modeling-methodology.md)

---

## Table of Contents

1. [Threat Intelligence Frameworks](#threat-intelligence-frameworks)
2. [Threat Intelligence Data Collection](#threat-intelligence-data-collection)
3. [Threat Intelligence Sources](#threat-intelligence-sources)
4. [Understanding Data Reliability](#understanding-data-reliability)
5. [Producing Actionable Threat Intelligence](#producing-actionable-threat-intelligence)
6. [Collecting IoCs](#collecting-iocs)
7. [Creating an Accessible Threat Knowledge Base](#creating-an-accessible-threat-knowledge-base)
8. [Threat Intelligence Reports](#threat-intelligence-reports)
9. [Threat Intelligence Dissemination](#threat-intelligence-dissemination)
10. [Quick-Reference Summary](#quick-reference-summary)

---

## Threat Intelligence Frameworks

### Collective Intelligence Framework (CIF)

**CIF** is a cyber threat intelligence management system that lets you **combine known malicious threat information** from many sources and use it for incident detection, response, and mitigation. CIF helps to parse, normalize, store, post-process, query, share, and produce data sets of threat intelligence.

**CIF Architecture** pulls from Private Feed/Data and Public Feeds/Data (your own data source can also be added), all funneling into a **CIF Server**, which then pushes daily feeds out to mitigation equipment (DNS sinkhole, firewall, IDS) and makes data available to users via CIF clients, Perl/browser plugin APIs, and querying of indexed feeds.

---

## Threat Intelligence Data Collection

Threat Intelligence Data Collection is a collection of **relevant and reliable data** for analysis — the key to achieving better threat intelligence output. Data can be gathered from **multiple sources and feeds**, including Human Intelligence (HUMINT), Imagery Intelligence (IMINT), Signals Intelligence (SIGINT), Open Source Intelligence (OSINT), Social Media Intelligence (SOCMINT), and others. Analysts can collect threat data either from multiple security teams in an organization, or by manually conducting the threat data collection themselves.

---

## Threat Intelligence Sources

A remarkably wide taxonomy of intelligence-gathering disciplines feeds into cyber threat intelligence:

| Source | Description | Example Sub-sources |
|---|---|---|
| **Open-Source Intelligence (OSINT)** | Collected and analyzed from publicly available sources to obtain a rich form of intelligence | Media, internet, public government data, corporate/academic publishing, literature |
| **Human Intelligence (HUMINT)** | Collected from interpersonal contacts | Foreign defense personnel and advisors, accredited diplomats, NGOs, prisoners of war (POWs), refugees, traveler interview/debriefing |
| **Signals Intelligence (SIGINT)** | Collected by intercepting signals | **Communication Intelligence (COMINT)** — from interception of communication signals; **Electronic Intelligence (ELINT)** — from electronic sensors like radar and lidar; **Foreign Instrumentation Signals Intelligence (FISINT)** — signals from non-human communication systems |
| **Technical Intelligence (TECHINT)** | Collected from an adversary's equipment or captured enemy material (CEM) | Foreign equipment, foreign weapon systems, satellites, technical research papers, foreign media, human contacts |
| **Geospatial Intelligence (GEOINT)** | Collected by exploitation and evaluation of geo-spatial information to assess human activities on Earth | Satellite imagery, Unmanned Aerial Vehicle (UAV) imagery, maps, GPS waypoints, IMINT, National Geospatial-Intelligence Agency (NGA) |
| **Imagery Intelligence (IMINT)** | Collected from objects reproduced electronically as visual media, via any device | Visual photography, infrared sensors, Synthetic Aperture Radar (SAR), MASINT, LASER, electro-optics |
| **Measurement and Signature Intelligence (MASINT)** | Collected from sensors intended to record distinctive characteristics (signatures) of fixed or dynamic targets | Electro-optical, radar sensors, acoustic sensors (sonars), LASER, infrared, spectroscopic sensors |
| **Covert Human Intelligence Sources (CHIS)** | Covertly collected from a target by maintaining a personal or other relationship with them | Regulated under the Regulation of Investigatory Powers Act 2000 (RIPA), UK |
| **Financial Intelligence (FININT)** | Collected about an adversary's financial affairs/transactions (tax evasion, money laundering, etc.), providing insight into their nature, capabilities, and intentions | Financial Intelligence Unit (FIU), banks, SWIFT, informal value-transfer systems (IVTS) |
| **Social Media Intelligence (SOCMINT)** | Collected from social networking sites and other social media sources | Facebook, LinkedIn, Twitter, WhatsApp, Instagram, Telegram |
| **Cyber Counterintelligence (CCI)** | Collected proactively via established security infrastructure, or by employing threat-manipulation techniques to lure and trap threats | Honeypots, passive DNS monitors, online web trackers, sock puppets (fake profiling on forums), publishing false reports |
| **Indicators of Compromise (IoCs)** | Collected from network security threats and breaches, and from alerts generated by security infrastructure, which likely indicate an intrusion | Commercial/industrial sources, free IoC-specific sources, online security-related sources, social media/news feeds, IoC buckets |
| **Industry Association and Vertical Communities** | Collected from various threat intelligence sharing communities where participants share intelligence | Financial Services ISAC (FS-ISAC), MISP (Malware Information Sharing Platform), IT-ISAC |
| **Commercial Sources** | Collected from commercial entities and security vendors that provide threat information | Kaspersky Threat Intelligence, McAfee, Avast, FortiGuard, SecureWorks, Cisco |
| **Government and Law Enforcement Sources** | Collected from government and law enforcement sources | US-CERT, European Union Agency for Network and Information Security (ENISA), FBI Cyber Crime, StopThinkConnect, CERIAS Blog |

---

## Understanding Data Reliability

An analyst must ensure the reliability of collected data to achieve better threat intelligence, and must understand the various factors that affect data reliability.

| Factor | What Affects It |
|---|---|
| **Assessing the relevance of intelligence sources** | Data must come from a reliable source, providing relevant and accurate data, and must not be altered during the collection process |
| **Factors affecting the credibility of an intelligence source** | Lack of authenticity of the data accessed; inaccuracy of the data provided; availability of incomplete or insufficient data |
| **Data collection methods affecting the availability of data** | Different collection methods surface different amounts of data based on access level — e.g., a **passive method** only collects internal and openly shared data; an **active method** only accesses authorized-level data; a **hybrid method** provides trap-based data collection |

---

## Producing Actionable Threat Intelligence

Using **low-cost or free sources** of intelligence may introduce additional risk to the organization and compromise the quality of the decision-making process. Analysts need to concentrate on selecting intelligence sources containing data that is relevant, accurate, timely, and has maximum coverage.

**Questions analysts need to answer to ensure intelligence is relevant and actionable:**

- Does the intelligence belong to the same geographical location as the organization?
- Does the intelligence support the strategic business requirements of the organization?
- To what extent is the information about threat actors, IoCs, and TTPs useful to the organization?
- What are the broader effects of the intelligence on the organization?

---

## Collecting IoCs

**Indicators of Compromise (IoCs)** are pieces of technical data used for building tactical threat intelligence. They're the clues or forensic evidence indicating a potential intrusion or malicious activity in an organizational network — comprising information about suspicious or malicious activities collected from various security establishments in a network infrastructure. IoCs help analysts understand "what happened" in an attack and observe the behavior and characteristics of malware.

**IoC data collection sources:** External Sources and Internal Sources, feeding into Commercial and Industry IoC Sources, Free IoC Sources, and the IoC Bucket.

---

## Creating an Accessible Threat Knowledge Base

A **knowledge repository** (knowledge base) is an important tool for managing and disseminating threat intelligence, helping analysts document and share threat intelligence throughout the entire threat-collaboration environment.

### A Threat Knowledge Repository Must Include

- **Pivoting** — the ability to contextualize threat data and correlate related activities
- **Content Structuring** — the ability to store threat intelligence in a structured format
- **Data Management** — the ability to modify or delete past or irrelevant threat data
- **Protection Ranking** — the ability to apply protection ranking to sensitive data, ensuring highly critical data isn't shared with untrusted partners
- **News Feeds** — the ability to provide real-time news, alerts, briefings, and reports
- **Evaluating Performance** — the ability to evaluate past security metrics
- **Searchable Functionality** — the ability to query for and enrich indicators

A **Threat Intelligence Analyst** feeds and draws from this **Knowledge Repository**, which in turn serves Security Operations, Vulnerability Management, Incident Response, and Data Owners.

### Information Typically Stored in the Knowledge Base

- The source of a threat indicator
- The established rules for using and sharing a threat indicator
- The date and time an indicator was collected
- The lifetime of validity for a threat indicator
- Whether the attacks related to a threat indicator have targeted specific organizations or industry sectors
- Whether an indicator is associated with Common Weakness Enumeration (CWE), Common Vulnerability Enumeration (CVE), Common Configuration Enumeration (CCE), or Common Platform Enumeration (CPE) records
- Threat actors or threat actor groups associated with an indicator
- Threat actor aliases, if any exist
- The TTPs used by a threat actor
- The associated threat actor's motives and intent
- The different types of individuals targeted by the associated attacks
- The systems targeted in the associated attacks

---

## Threat Intelligence Reports

**Threat intelligence reports** are prose documents that include details about various types of attacks, TTPs, threat actors, systems, and information being targeted. These reports include information related to threats that have been collected, aggregated, transformed, analyzed, and enriched to provide **actionable contextual intelligence** for organizations' decision-making processes.

### Elements Required to Create Concise, Actionable, Customized Threat Intelligence Reports

1. Report Details
2. Client Details
3. Test Details
4. Executive Summary
5. Traffic Light Protocol (TLP)
6. Analysis Methodology
7. Threat Details
8. Indicators of Compromise
9. Recommended Actions

---

## Threat Intelligence Dissemination

The dissemination of threat intelligence helps consumers gain a more detailed insight into threats an organization might face. Information is usually disseminated through either a **manual process** or an **automated process**.

### Essential Criteria for the Consumer to Acquire and Benefit From the Intelligence

| Criterion | Description |
|---|---|
| **The right content** | Intelligence must consist of good-quality content that provides the consumer with an understanding of threats and their harmful consequences, helping develop a mitigation plan |
| **The right presentation** | Intelligence must be concise, accurate, and easily understandable — a right balance between tables, narrative, numbers, graphics, and multimedia |
| **The right time** | Intelligence must be disseminated within a required time frame so consumers can make timely and effective security decisions |

---

## Quick-Reference Summary

- **CIF** = the management-system layer that combines threat info from private + public feeds into a single queryable/actionable server
- **15 named intelligence source types**: OSINT, HUMINT, SIGINT (+ COMINT/ELINT/FISINT), TECHINT, GEOINT, IMINT, MASINT, CHIS, FININT, SOCMINT, CCI, IoCs, Industry/Vertical Communities, Commercial Sources, Government/Law Enforcement Sources
- **Data reliability** hinges on source relevance, credibility (authenticity/accuracy/completeness), and collection method (passive/active/hybrid)
- **Actionable intelligence** requires answering 4 relevance questions (geography, strategic fit, TTP/IoC usefulness, broader impact)
- **IoCs** = the technical clues that build tactical threat intelligence, sourced both externally and internally
- **Knowledge base** needs 7 core capabilities: pivoting, content structuring, data management, protection ranking, news feeds, performance evaluation, searchability
- **Threat intel reports** = 9-element prose documents (report/client/test details, exec summary, TLP, methodology, threat details, IoCs, recommended actions)
- **Dissemination** succeeds on 3 criteria: right content, right presentation, right time

---

*Part of the CEH Appendix B study series — continues in [Part 9: Threat Modeling Methodology](09-threat-modeling-methodology.md).*
