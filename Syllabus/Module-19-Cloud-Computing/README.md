# CEH v13 — Module 19: Cloud Computing

> **Certified Ethical Hacker (CEH) v13 | Exam 312-50**
> Complete offensive and defensive reference — attack techniques, enumeration commands, hacking tools, and cloud security best practices.

---

## Learning Objectives

| # | Objective |
|---|-----------|
| 01 | Summarize Cloud Computing Concepts |
| 02 | Explain Cloud Computing Threats |
| 03 | Explain Cloud Hacking Methodology |
| 04 | Demonstrate AWS Hacking |
| 05 | Demonstrate Microsoft Azure Hacking |
| 06 | Demonstrate Google Cloud Hacking |
| 07 | Demonstrate Container Hacking |
| 08 | Explain Cloud Security |

---

## Module Files

| File | Contents |
|------|----------|
| [01-cloud-computing-concepts.md](docs/01-cloud-computing-concepts.md) | Service models, deployment models, NIST architecture, fog/edge computing, CSPs |
| [02-container-serverless.md](docs/02-container-serverless.md) | Docker, Kubernetes, container orchestration, serverless/FaaS |
| [03-cloud-threats.md](docs/03-cloud-threats.md) | OWASP Top 10 (Cloud/K8s/Serverless), full threat catalog with countermeasures |
| [04-cloud-hacking-methodology.md](docs/04-cloud-hacking-methodology.md) | Info gathering, vuln assessment, exploitation, post-exploitation — full phase breakdown |
| [05-aws-hacking.md](docs/05-aws-hacking.md) | S3 enum, EC2/RDS/IAM/Lambda/Cognito attacks, CloudTrail evasion, persistence, lateral movement |
| [06-azure-gcp-hacking.md](docs/06-azure-gcp-hacking.md) | Azure AD/AADInternals/MicroBurst/Stormspotter + GCP gcloud/gsutil/GCPScanner attacks |
| [07-container-hacking.md](docs/07-container-hacking.md) | kubectl recon, Docker Remote API exploitation, LXD privesc, K8s etcd extraction |
| [08-cloud-security.md](docs/08-cloud-security.md) | Security controls, Zero Trust, SAML, CASB, NG SWG, best practices (AWS/Azure/GCP/K8s/serverless/Docker/containers) |
| [cheatsheet-commands.md](docs/cheatsheet-commands.md) | Master cheatsheet — every runnable command from the module |
| [cheatsheet-tools.md](docs/cheatsheet-tools.md) | Every tool covered — purpose, source URL, key flags |

---

## Quick Navigation by Attack/Topic

### Cloud Concepts
- [IaaS / PaaS / SaaS / IDaaS / CaaS / FaaS / XaaS / FWaaS / DaaS / MBaaS / MaaS](docs/01-cloud-computing-concepts.md#types-of-cloud-computing-services)
- [Public / Private / Community / Hybrid / Multi / Distributed / Poly Cloud](docs/01-cloud-computing-concepts.md#cloud-deployment-models)
- [NIST Reference Architecture — 5 Actors](docs/01-cloud-computing-concepts.md#nist-cloud-deployment-reference-architecture)
- [Fog Computing vs Edge Computing vs Grid Computing](docs/01-cloud-computing-concepts.md#fog-edge-and-grid-computing)

### Containers & Kubernetes
- [Docker Engine, Architecture, Networking (CNM), Volumes, Swarm](docs/02-container-serverless.md#docker)
- [Kubernetes Cluster Architecture — Master + Node Components](docs/02-container-serverless.md#kubernetes)
- [Container Orchestration — what it automates](docs/02-container-serverless.md#container-orchestration)
- [Serverless Computing — FaaS, frameworks, vs containers](docs/02-container-serverless.md#serverless-computing)

### Threats & Attacks
- [OWASP Top 10 Cloud / Kubernetes / Serverless](docs/03-cloud-threats.md#owasp-top-10)
- [Service Hijacking (Social Engineering / Network Sniffing)](docs/03-cloud-threats.md#service-hijacking)
- [Side-Channel / VM Cross-guest Attacks](docs/03-cloud-threats.md#side-channel-attacks)
- [MITC (Man-in-the-Cloud) — sync token hijacking](docs/03-cloud-threats.md#man-in-the-cloud-mitc)
- [Cloud Hopper Attack — MSP supply chain](docs/03-cloud-threats.md#cloud-hopper-attack)
- [Cryptojacking — steps + countermeasures](docs/03-cloud-threats.md#cloud-cryptojacking)
- [Cloudborne — bare-metal firmware backdoor](docs/03-cloud-threats.md#cloudborne-attack)
- [IMDS Attack — metadata credential theft](docs/03-cloud-threats.md#imds-attack)
- [Golden SAML Attack](docs/03-cloud-threats.md#golden-saml-attack)
- [Living Off the Cloud (LotC)](docs/03-cloud-threats.md#living-off-the-cloud-lotc)
- [Cloud Snooper, CPDoS/CDN Cache Poisoning, Wrapping Attack](docs/03-cloud-threats.md#other-cloud-attacks)
- [Data Breach/Loss, Malicious Insiders, EDoS, Isolation Failure, Lock-in](docs/03-cloud-threats.md#threat-catalog)

### Hacking Methodology
- [Phase 1: Information Gathering — Shodan filters, Masscan, Censys](docs/04-cloud-hacking-methodology.md#phase-1-information-gathering)
- [Phase 2: Vulnerability Assessment — Prowler, CloudSploit](docs/04-cloud-hacking-methodology.md#phase-2-vulnerability-assessment)
- [Phase 3: Exploitation](docs/04-cloud-hacking-methodology.md#phase-3-exploitation)
- [Phase 4: Post-Exploitation — cleanup, stealth, persistence](docs/04-cloud-hacking-methodology.md#phase-4-post-exploitation)

### AWS Hacking
- [S3 Enumeration — S3Scanner / BucketLoot / CloudBrute / Google Dorks](docs/05-aws-hacking.md#s3-bucket-enumeration)
- [EC2 / RDS / Lambda / Cognito CLI enumeration commands](docs/05-aws-hacking.md#aws-service-enumeration)
- [IAM Privilege Escalation — 8 techniques](docs/05-aws-hacking.md#iam-privilege-escalation)
- [IAM Credential compromise — Pacu, DumpsterDiver, Cloudsplaining](docs/05-aws-hacking.md#compromising-iam-credentials)
- [SSRF → credential theft workflow](docs/05-aws-hacking.md#ssrf-exploitation)
- [Lambda attacks — black-box + white-box](docs/05-aws-hacking.md#lambda-attacks)
- [CloudTrail evasion (stop/delete/re-enable)](docs/05-aws-hacking.md#cloudtrail-evasion)
- [EC2 persistence — backdoor users / startup scripts / SSH key injection / IAM roles](docs/05-aws-hacking.md#persistence-on-ec2)
- [Lateral movement across accounts and regions](docs/05-aws-hacking.md#lateral-movement)
- [Stratus Red Team — MITRE ATT&CK emulation](docs/05-aws-hacking.md#stratus-red-team)
- [Cartography, CloudFox, Ghostbuster, Endgame, SkyArk, AWSGoat](docs/05-aws-hacking.md#additional-aws-tools)

### Azure & GCP Hacking
- [AADInternals — tenant recon commands](docs/06-azure-gcp-hacking.md#azure-reconnaissance)
- [MicroBurst, AzureHound, Goblob, Spray365, Stormspotter](docs/06-azure-gcp-hacking.md#azure-enumeration-tools)
- [Azure NSG identification, VNet Peering abuse, managed identity exploitation](docs/06-azure-gcp-hacking.md#azure-attack-techniques)
- [Azure AD privilege escalation via certificate + service principals](docs/06-azure-gcp-hacking.md#azure-privilege-escalation)
- [AzureGoat — vulnerable-by-design lab](docs/06-azure-gcp-hacking.md#azuregoat)
- [GCP gcloud/gsutil enumeration — every command](docs/06-azure-gcp-hacking.md#gcp-enumeration)
- [GCP privilege escalation scanner, GCPBucketBrute, cloud_enum, GCP Scanner](docs/06-azure-gcp-hacking.md#gcp-attack-tools)
- [GCPGoat — vulnerable-by-design GCP lab](docs/06-azure-gcp-hacking.md#gcpgoat)

### Container Hacking
- [kubectl — info gathering commands](docs/07-container-hacking.md#kubectl-enumeration)
- [Container/K8s vulnerability scanning — Trivy, Sysdig, Kubescape, kube-hunter](docs/07-container-hacking.md#vulnerability-scanning)
- [Docker Remote API exploitation — file retrieval, network scan, credential extraction](docs/07-container-hacking.md#docker-remote-api)
- [LXD/LXC Privilege Escalation — full step-by-step](docs/07-container-hacking.md#lxd-privilege-escalation)
- [Kubernetes etcd post-enumeration — secret extraction](docs/07-container-hacking.md#kubernetes-etcd)
- [Container volume hacking — NFS/iSCSI, hostPath mounts](docs/07-container-hacking.md#container-volumes)

### Cloud Security
- [Cloud security control layers — Application/Information/Management/Network/Trusted Computing/Computation/Physical](docs/08-cloud-security.md#security-control-layers)
- [Best Practices — 24-point general + AWS/Azure/GCP/K8s/Docker/Serverless/Container checklists](docs/08-cloud-security.md#best-practices)
- [Zero Trust Networks — architecture and implementation](docs/08-cloud-security.md#zero-trust)
- [CASB — features, how it works, tools](docs/08-cloud-security.md#casb)
- [Next-Generation Secure Web Gateway (NG SWG)](docs/08-cloud-security.md#ng-swg)
- [Cloud Security Tools — Scout Suite, Qualys, Securiti, Aqua, Dashbird, Prowler](docs/08-cloud-security.md#cloud-security-tools)
- [NIST Recommendations + Access Control Tables (IaaS/PaaS/SaaS)](docs/08-cloud-security.md#nist-recommendations)
- [Organization/Provider Security Compliance Checklists (Tables 19.16-19.19)](docs/08-cloud-security.md#compliance-checklists)

---

## Key Tool Summary

| Tool | Cloud | Category | Source |
|------|-------|----------|--------|
| Shodan | All | Recon | shodan.io |
| Masscan | All | Port scanning | github.com |
| Prowler | AWS/Azure/GCP/K8s | Vuln scanning | github.com |
| CloudSploit | AWS/Azure/GCP | Misconfiguration | github.com |
| S3Scanner | AWS | S3 enum | github.com |
| BucketLoot | AWS | S3 enum/permissions | github.com |
| CloudBrute | AWS/Azure/GCP | S3/blob enum | github.com |
| Cartography | AWS/GCP/Azure | Attack path mapping | github.com |
| CloudFox | AWS/Azure/GCP | Attack path discovery | github.com |
| Ghostbuster | AWS | DNS subdomain takeover | github.com |
| Pacu | AWS | Exploitation framework | github.com |
| DumpsterDiver | All | Secret scanning | github.com |
| Cloudsplaining | AWS | Weak IAM policy detection | github.com |
| Stratus Red Team | AWS/GCP/Azure/K8s | MITRE ATT&CK emulation | github.com |
| SkyArk | AWS/Azure | Shadow admin discovery | github.com |
| Endgame | AWS | Backdoor creation | github.com |
| CCAT | AWS | Docker container exploitation | github.com |
| AWSGoat | AWS | Vulnerable lab | github.com |
| AADInternals | Azure | Tenant recon/exploitation | github.com |
| MicroBurst | Azure | Resource enumeration | github.com |
| AzureHound | Azure | BloodHound data collection | github.com |
| Goblob | Azure | Blob storage enum | github.com |
| Spray365 | Azure/O365 | Password spraying | github.com |
| Stormspotter | Azure | Attack surface mapping | github.com |
| AzureGoat | Azure | Vulnerable lab | github.com |
| GCP Scanner | GCP | Resource enum/access check | github.com |
| gcp_service_enum | GCP | Service discovery | github.com |
| cloud_enum | AWS/Azure/GCP | Multi-cloud OSINT | github.com |
| GCPBucketBrute | GCP | Bucket privesc | rhinosecuritylabs.com |
| GCP Priv Esc Scanner | GCP | IAM privesc detection | github.com |
| GCPGoat | GCP | Vulnerable lab | github.com |
| Trivy | Containers | Image vuln scanning | github.com |
| Sysdig | K8s/Containers | Continuous security | sysdig.com |
| Aqua | Containers | Container security platform | aquasec.com |
| Kubescape | K8s | K8s security scanner | github.com |
| kube-hunter | K8s | K8s pen testing | github.com |
| Scout Suite | AWS/Azure/GCP | Multi-cloud security audit | github.com |
| Qualys | All | Continuous vulnerability mgmt | qualys.com |
| Dashbird | Serverless | Serverless observability | dashbird.io |
| Forcepoint ONE CASB | All | Cloud access security broker | forcepoint.com |
| PMapper | AWS | IAM privilege-escalation mapping | github.com |
| Principal Mapper | AWS | IAM graph analysis | github.com |

---

## Disclaimer

> This material is for **educational purposes only**. All techniques described are from the EC-Council CEH v13 official curriculum. Practice only on systems and environments you own or have explicit written permission to test. Unauthorized access to computer systems is illegal under the Computer Fraud and Abuse Act (CFAA) and equivalent laws in all jurisdictions.
