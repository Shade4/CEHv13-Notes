# Cloud Hacking — Tools Cheatsheet

> **CEH v13 Module 19 | Every tool covered in the module — purpose, source, key flags**

---

## Reconnaissance & OSINT Tools

| Tool | Source | Purpose | Key Flags/Commands |
|------|--------|---------|-------------------|
| **Shodan** | shodan.io | Search engine for internet-connected devices; find exposed cloud assets | `port:443`, `org:Amazon`, `ssl.cert.issuer.cn:Amazon`, `ssl.cert.subject.cn:azure`, `tag:cloud`, `net:52.0.0.0/8` |
| **Masscan** | github.com | Fast port scanner for cloud infrastructure | `-p0-65535`, `--rate=<rate>`, `-oX <file>`, `-oJ <file>` |
| **Censys** | censys.io | Alternative to Shodan for cloud asset discovery | Web-based search |
| **cloud_enum** | github.com | Multi-cloud OSINT; finds open buckets, Firebase DBs, App Engine sites | `-k <keyword>`, `--disable-aws`, `--disable-azure` |
| **GrayhatWarfare** | grayhatwarfare.com | Find publicly accessible cloud storage buckets | Web-based |

---

## AWS Attack Tools

### S3 Bucket Enumeration

| Tool | Source | Purpose | Key Commands |
|------|--------|---------|-------------|
| **S3Scanner** | github.com | Identify open S3 buckets and retrieve ACL info | `s3scanner -bucket <name>`, `-bucket-file <file>.txt -enumerate`, `-threads 8` |
| **BucketLoot** | github.com | S3-compatible bucket inspector; extract URLs/subdomains from open buckets | `python bucketloot.py -l <file>` (list), `-c <file>` (check perms), `-d <file>` (download) |
| **CloudBrute** | github.com | Brute-force and enumerate S3, Azure blob, GCP bucket names | `./cloudbrute -d <domain> -k <keyword> -t 80 -T 10 -w <wordlist>` |

### AWS Enumeration & Exploitation

| Tool | Source | Purpose | Key Commands |
|------|--------|---------|-------------|
| **Cartography** | github.com | Neo4j-based cloud asset relationship mapping; attack path discovery | Cypher queries against Neo4j graph |
| **CloudFox** | github.com | Identify exploitable attack paths in AWS/Azure/GCP | `cloudfox aws --profile <p> all-checks`, `access-keys`, `buckets`, `endpoints`, `secrets`, `permissions` |
| **Ghostbuster** | github.com | Enumerate DNS records from AWS Route 53; find subdomain takeover opportunities | `ghostbuster scan aws --profile <AWS CLI profile name>` |
| **Prowler** | github.com | Multi-cloud security assessment (240+ controls, CIS/NIST/HIPAA/PCI) | `prowler <provider>`, `-M csv json-asff json-ocsf html`, `--services s3 ec2`, `--compliance=hipaa` |
| **CloudSploit** | github.com | Identify misconfigurations and security risks across cloud resources | `./index.js`, `--compliance=hipaa/pci/cis`, `--console=text`, `--csv=file.csv` |
| **Cloudsplaining** | github.com | Identify weak/violated AWS IAM policies; generates HTML reports | `aws iam get-account-authorization-details --output json > account-auth-details.json`, then `cloudsplaining scan --input-file account-auth-details.json` |
| **Pacu** | github.com | AWS exploitation framework for IAM role assumption and privilege escalation | `assume_role_enum.py [-p PROFILE] [-w WORD_LIST] -I ACCOUNT_ID` |
| **DumpsterDiver** | github.com | Scan large volumes of files for hardcoded secrets (AWS keys, SSL keys, Azure keys) | `dumpsterDiver -p /path/to/scan`, `-e AWS_KEY`, `--entropy ENTROPY` |
| **Stratus Red Team** | github.com | MITRE ATT&CK emulation framework for cloud (AWS/GCP/Azure/K8s) | `stratus list --platform AWS --mitre-attack-tactic <tactic>`, `warmup`, `detonate`, `cleanup` |
| **SkyArk** | github.com | Discover shadow admins in AWS (AWStealth) and Azure (AzureStealth) | PowerShell-based scanning modules |
| **Endgame** | github.com | Post-exploitation tool; create backdoors across AWS resource types | `endgame list-resources`, `endgame expose --service <svc> --name <name>` |
| **CCAT** | github.com | Cloud Container Attack Tool; exploit Docker containers on AWS ECS/ECR | Modules: Enumerate ECR, Pull Repos, Docker Backdoor, Push Repos to ECR |
| **Principal Mapper (PMapper)** | github.com | Visualize IAM users/roles as directional graph; identify privilege escalation paths | Python-based visualization |
| **Starbase** | github.com | Cloud infrastructure inventory tool | — |
| **AWS Recon** | github.com | AWS resource inventory and reconnaissance | — |
| **aws-inventory** | github.com | Inventory AWS resources | — |
| **CloudMapper** | github.com | Map AWS network infrastructure | — |
| **AWSGoat** | github.com | Deliberately vulnerable AWS infrastructure for practice | SQLi, ECS breakout, SSRF, IAM privesc, file upload scenarios |

---

## Azure Attack Tools

| Tool | Source | Purpose | Key Commands |
|------|--------|---------|-------------|
| **AADInternals** | github.com | PowerShell module for Azure AD/Office 365 recon, exploitation, and post-exploitation | `Invoke-AADIntReconAsOutsider`, `Get-AADIntLoginInformation`, `Get-AADIntTenantDomains` |
| **MicroBurst** | github.com | Enumerate Azure services and resources | `Import-Module .\MicroBurst.psm1`, `Get-AzDomainInfo -Verbose -Folder microburst-output` |
| **AzureHound** | github.com | Azure BloodHound data collector for Azure AD and AzureRM | `azurehound list -u "$USERNAME" -p "$PASSWORD" -t "$TENANT" -o file.json` |
| **AzureGraph** | github.com | Azure AD information gathering via Microsoft Graph API | `gr <- create_graph_login()`, `gr$list_users()`, `me$list_owned_objects()` |
| **Goblob** | github.com | Enumerate publicly exposed Azure blob storage | `./goblob <accountname>`, `-accounts accounts.txt`, `-containers wordlists/...` |
| **Spray365** | github.com | Automated password spraying for Microsoft/Office 365/Azure AD accounts | `python spray365.py generate normal`, `spray -ep <plan>`, `review <results.json>` |
| **Stormspotter** | github.com | Maps Azure and Azure AD objects into a visual graph to reveal attack surfaces | `python3 sscollector.pyz cli`, `spn -t <tenant> -c <clientID> -s <secret>` |
| **Red-Shadow** | github.com | Identify and exploit Azure AD shadow admins | PowerShell-based |
| **AzureGoat** | github.com | Deliberately vulnerable Azure infrastructure for practice | IDOR, SSRF, security misconfiguration, privilege escalation scenarios |

---

## GCP Attack Tools

| Tool | Source | Purpose | Key Commands |
|------|--------|---------|-------------|
| **GCP Scanner** | github.com | Determine access level of credentials (VM/container/service account/OAuth2 token) across GCP services | `python3 scanner.py -o <output> -g <gcloud profile path>` |
| **gcp_service_enum** | github.com | Discover GCP services (Compute Engine, Cloud Storage) using a service account key | `gcp_enum_services.py -f <key file> --output-file <file>` |
| **cloud_enum** | github.com | Multi-cloud OSINT; enumerate GCP buckets, Firebase DBs, App Engine | `cloud_enum.py -k <keyword> --disable-aws --disable-azure` |
| **GCPBucketBrute** | rhinosecuritylabs.com | Enumerate GCS buckets, check access levels, identify privilege escalation potential | `python3 gcpbucketbrute.py -k testtest -a` |
| **GCP Privilege Escalation Scanner** | github.com | Identify IAM misconfigurations that enable privilege escalation | `python3 enumerate_member_permissions.py --project-id <id>`, `python3 check_for_privesc.py` |
| **GrayhatWarfare** | grayhatwarfare.com | Identify publicly accessible GCP storage buckets | Web-based |
| **GCPGoat** | github.com | Deliberately vulnerable GCP infrastructure for practice | SSRF, misconfigured bucket policies, lateral movement scenarios |

---

## Container & Kubernetes Attack Tools

| Tool | Source | Purpose | Key Commands |
|------|--------|---------|-------------|
| **Trivy** | github.com | Container image vulnerability scanning (OS packages, app dependencies) | `trivy image <image>`, `trivy fs /path`, `--scanners vuln` |
| **Sysdig** | sysdig.com | K8s vulnerability detection via CI/CD, image registry, admission controllers | Dashboard-based |
| **Kubescape** | github.com | Kubernetes security scanner | — |
| **kube-hunter** | github.com | Kubernetes penetration testing tool | — |
| **kubeaudit** | github.com | Kubernetes security auditing | — |
| **KubiScan** | github.com | Kubernetes IAM privilege scanning | — |
| **Krane** | github.com | Kubernetes RBAC analysis | — |
| **Portainer** | portainer.io | Container management platform (also attack surface) | Web UI-based |
| **Aqua** | aquasec.com | Container security platform (scanning, runtime protection) | Web UI + CLI-based |
| **Sysdig Falco** | sysdig.com | Container runtime security and threat detection | — |
| **Anchore** | anchore.com | Container image scanning and policy enforcement | — |
| **Snyk Container** | snyk.io | Container vulnerability scanning | — |
| **Lacework** | lacework.com | Cloud and container security | — |
| **Advanced Cluster Security (ACS)** | redhat.com | Comprehensive Kubernetes security platform | Dashboard-based |
| **Kyverno** | github.com | Kubernetes policy management | — |
| **Sumo Logic** | sumologic.com | Cloud-native security intelligence platform | — |

---

## Vulnerable-by-Design Labs

| Tool | Cloud | Scenarios |
|------|-------|----------|
| **AWSGoat** | AWS | SQLi, ECS breakout, SSRF, IAM privilege escalation, file upload + task metadata |
| **AzureGoat** | Azure | IDOR, SSRF, security misconfiguration, privilege escalation |
| **GCPGoat** | GCP | SSRF, misconfigured bucket policies, lateral movement |

---

## Cloud Security Tools (Defensive)

### Multi-Cloud

| Tool | Source | Purpose |
|------|--------|---------|
| **Scout Suite** | github.com | Multi-cloud security auditing (AWS/Azure/GCP/K8s/DigitalOcean/Oracle); generates HTML risk report |
| **Qualys Cloud Platform** | qualys.com | End-to-end IT security; continuous visibility + real-time threat response |
| **Prisma Cloud** | paloaltonetworks.com | Cloud-native security platform |
| **Netskope One** | netskope.com | Cloud security platform |
| **Data-Aware Cloud Security** | skyhighsecurity.com | Data-centric cloud security |
| **Trend Micro Deep Security** | trendmicro.com | Hybrid cloud security |
| **Lookout CipherCloud** | lookout.com | Cloud data protection |

### Cloud Access Security Brokers (CASB)

| Tool | Source |
|------|--------|
| **Forcepoint ONE CASB** | forcepoint.com |
| **Cisco Cloudlock** | cisco.com |
| **Zscaler CASB** | zscaler.com |
| **Proofpoint Cloud App Security Broker** | proofpoint.com |
| **FortiCASB** | fortinet.com |
| **CloudCodes** | cloudcodes.com |

### Next-Generation Secure Web Gateways (NG SWG)

| Tool | Source |
|------|--------|
| **Netskope Next Gen SWG** | netskope.com |
| **Cloudflare Gateway** | cloudflare.com |
| **Skyhigh SWG** | skyhighsecurity.com |
| **Menlo Secure Web Gateway** | menlosecurity.com |
| **McAfee MVISION UCE** | mcafee.com |

### Shadow Cloud Asset Discovery

| Tool | Source | Purpose |
|------|--------|---------|
| **Securiti** | securiti.ai | AI-powered shadow cloud asset discovery and data governance |
| **CloudEagle** | cloudeagle.ai | SaaS management and shadow IT discovery |
| **Microsoft Defender for Cloud Apps** | learn.microsoft.com | Cloud app discovery and security |
| **FireCompass** | firecompass.com | Attack surface management |
| **Data Theorem** | datatheorem.com | Mobile and API security |
| **BetterCloud** | bettercloud.com | SaaS management platform |

### Container Security (Defensive)

| Tool | Source | Purpose |
|------|--------|---------|
| **Aqua** | aquasec.com | Full-lifecycle container and cloud-native security |
| **Sysdig Falco** | sysdig.com | Container runtime threat detection |
| **Anchore** | anchore.com | Container image analysis and policy enforcement |
| **Snyk Container** | snyk.io | Container vulnerability scanning |
| **Lacework** | lacework.com | Cloud and container security observability |
| **Tenable Cloud Security** | tenable.com | Cloud infrastructure security |

### Serverless Security (Defensive)

| Tool | Source | Purpose |
|------|--------|---------|
| **Dashbird** | dashbird.io | Serverless observability and monitoring |
| **CloudGuard** | checkpoint.com | Cloud-native security |
| **Datadog Serverless Monitoring** | datadoghq.com | Serverless performance and security monitoring |
| **Lumigo** | lumigo.io | Serverless debugging and monitoring |
| **Sysdig** | sysdig.com | Container and serverless security |

### Kubernetes Security (Defensive)

| Tool | Source | Purpose |
|------|--------|---------|
| **ACS (Advanced Cluster Security)** | redhat.com | Comprehensive K8s security platform |
| **Kyverno** | github.com | Kubernetes policy management |
| **Kubeaudit** | github.com | K8s security auditing |
| **Sumo Logic** | sumologic.com | Cloud SIEM + K8s security |
| **Kubespace** | kubescope.io | K8s security posture management |

---

## Tool Quick-Reference by Attack Phase

### Phase 1: Information Gathering

```
Shodan → cloud asset discovery
Masscan → open port discovery
Censys → alternative to Shodan
cloud_enum → multi-cloud bucket/resource discovery
Ghostbuster (AWS) → DNS record/subdomain takeover discovery
AADInternals (Azure) → Azure tenant reconnaissance
gcloud CLI (GCP) → GCP resource listing
```

### Phase 2: Vulnerability Assessment

```
Prowler → multi-cloud security benchmarks (CIS/NIST/HIPAA/PCI)
CloudSploit → misconfiguration detection (AWS/Azure/GCP)
Cloudsplaining → weak AWS IAM policy detection
GCP Privilege Escalation Scanner → GCP IAM privesc vulnerability detection
Trivy → container image vulnerability scanning
Kubescape / kube-hunter → Kubernetes security assessment
Scout Suite → multi-cloud security audit (post-exploitation)
```

### Phase 3: Exploitation

```
S3Scanner / BucketLoot / CloudBrute → S3 bucket exploitation
Pacu → AWS IAM role assumption and exploitation
DumpsterDiver → secrets extraction from files/repos
CCAT → Docker container exploitation on AWS
Stormspotter / AzureHound → Azure attack path discovery
CloudFox / Cartography → attack path identification and exploitation
Spray365 (Azure) → password spraying for Azure AD accounts
GCPBucketBrute → GCP storage bucket privilege escalation
```

### Phase 4: Post-Exploitation

```
SkyArk / Red-Shadow → shadow admin discovery
Endgame → backdoor account creation across AWS services
Stratus Red Team → MITRE ATT&CK technique emulation and evasion
Cobalt Strike / Metasploit → general post-exploitation C2 (referenced)
```

---

## Critical Command Index

| Objective | Command |
|-----------|---------|
| List S3 buckets (unauthenticated) | `aws s3 ls s3://[bucket_name] --no-sign-request` |
| Steal EC2 metadata credentials (IMDSv1) | `curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<role>` |
| Steal EC2 metadata credentials (IMDSv2) | `TOKEN=curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"` then `curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/` |
| Scan for open ports (cloud) | `sudo masscan -p0-65535 <IP> --rate=<rate>` |
| Scan AWS with Prowler | `prowler aws --services s3 ec2` |
| Detect weak IAM policies | `cloudsplaining scan --input-file account-auth-details.json` |
| Stop CloudTrail logging | `aws cloudtrail stop-logging --name targetcloud_trail --profile administrator` |
| Assume IAM role (lateral movement) | `aws sts assume-role --role-arn arn:aws:iam::<account>:role/<role> --role-session-name <name>` |
| Enumerate AWS attack paths | `cloudfox aws --profile <p> all-checks` |
| Enumerate Azure tenant | `Invoke-AADIntReconAsOutsider -Domain <domain> \| Format-Table` |
| Azure password spray | `python3 spray365.py spray -ep <execution_plan_filename>` |
| GCP list all resources | `gcloud projects list` + `gsutil ls` |
| K8s list pods | `kubectl get pods` |
| K8s extract etcd secrets | `ETCDCTL_API=3 ./etcdctl --cacert=... get /registry/ --prefix \| grep -a '/registry/secrets/'` |
| LXD privilege escalation | `lxc exec privesc /bin/sh` (after mounting host root at /mnt/root) |
| Docker credential theft | `docker -H [host] exec -i [container] env` |
| Multi-cloud audit | `scout aws --profile <p>` / `scout azure --tenant-id <id>` / `scout gcp --service-account-file <key>` |
