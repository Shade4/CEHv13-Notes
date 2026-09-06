# 04 — Cloud Hacking Methodology

> **CEH v13 Module 19 | Objective 03: Explain Cloud Hacking Methodology**

---

## Introduction

Though most organizations adopt cloud technologies for the variety of cost-effective services, security remains a significant concern because it depends on sharing. Security gaps and vulnerabilities of the underlying technologies can allow attackers to launch various types of cloud attacks, affecting confidentiality, integrity, and availability of resources and services in cloud systems.

**Important Note:** Cloud hacking as an ethical hacker is typically feasible only through internal means, ensuring compliance with security policies and avoiding unauthorized access. Each cloud provider (AWS, Azure, GCP) imposes specific rules and policies regarding ethical hacking. The cloud provider must be notified before performing hacking operations, and checking which activities are permitted for specific operations is essential.

---

## Cloud Hacking Scope

Cloud hacking encompasses a broad range of activities aimed at compromising the cloud infrastructure and services. This can include both cloud-hosted web applications and system hacking, but extends to compromising the overall cloud security. The three elements that attackers often target to compromise cloud security are:

1. **Web Applications Hacking** — attackers target cloud-based Web APIs, which are vital sources for relaying cloud services and resources. Cloud-based APIs that facilitate communication between different software components are often available on the internet and serve as key entry points for hackers. Automated tools may be used to scan for known vulnerabilities or map API endpoints. Attackers identify vulnerabilities such as inadequate authentication, authorization flaws, or allowing excessive access, and then attempt to gain unauthorized access to cloud resources. *(For complete coverage: Module 14 — Hacking Web Applications)*

2. **System Hacking** — system hacking in cloud environments focuses on identifying and exploiting vulnerabilities in virtualized systems hosted on cloud platforms. These systems include virtual machines, containers, and serverless functions, all of which present unique security challenges. Cloud-based system hacking begins with reconnaissance, wherein attackers identify potential entry points to the cloud systems by scanning the exposed interfaces, weak security settings, or outdated software. *(For complete coverage: Module 06 — System Hacking)*

3. **Cloud Platform Hacking** — attackers exploit weak passwords, unpatched software, and misconfigured settings to compromise cloud platforms and gain identify potential entry points into cloud systems. This can include misconfigurations in cloud settings, outdated software with known vulnerabilities, and misconfigured access controls.

---

## Four Phases of Cloud Hacking Methodology

### Phase 1: Information Gathering

Information gathering is the first phase of hacking in which an attacker collects as much data as possible regarding the target cloud infrastructure. This may include details regarding the network topology, IP addresses, domain names, subdomains, user accounts, or publicly available information.

The purpose of this phase is to gather critical information about a target cloud environment, which aids in identifying potential vulnerabilities and crafting more effective attacks in the subsequent phases. Consequently, it can assist in laying the foundation for the entire cloud hacking process.

For this purpose, attackers use various techniques to gather information such as network scanning, open source intelligence (OSINT), DNS interrogation, and web scraping. They employ tools such as Nmap, Shodan, and Recon-ng to automate and enhance the effectiveness of these activities. Once successful, they gain a comprehensive understanding of the target's cloud environment, which significantly increases their chances of finding exploitable weaknesses.

#### Identifying the Target Cloud Environment

Identifying the target cloud environment involves recognizing and profiling the cloud infrastructure used by an organization such as AWS, Microsoft Azure, or GCP. This step is crucial for attackers because it helps them understand the specific technologies, services, and configurations deployed by the target.

Attackers can use tools such as **Shodan** and **Censys** to gather detailed information about a target's cloud infrastructure.

#### Shodan Search Filters for Cloud Infrastructure

```
# Search for HTTPS services (common for cloud web services)
port:443

# Search for AWS services via SSL certificate
ssl.cert.issuer.cn:Amazon

# Search for AWS services (organization-level)
org:Amazon

# Search for Azure-hosted services
ssl.cert.subject.cn:azure

# Search for any cloud asset (Enterprise Shodan only)
tag:cloud

# Search within a specific IP range (e.g., common AWS range)
net:52.0.0.0/8

# Search within instances for S3 content
http.html:"s3.amazonaws.com"

# Search for AWS-hosted services and infrastructure used by a specific company
Amazon web services Facebook

# Search for AWS services (org-level, also reveals AWS services)
org:Amazon

# Search for Azure-hosted services via SSL cert subject
ssl.cert.subject.cn:azure

# Search for cloud assets with a specific tag
tag:cloud

# Search within instances
http.html:"s3.amazonaws.com"
```

#### Masscan — Open Port Discovery

Masscan is a network port scanner designed to scan large networks and the entire Internet within minutes. It is particularly useful for identifying open ports and services running on a cloud infrastructure.

```bash
# Scan all ports on a target IP at a specific rate
sudo masscan -p0-65535 <target_IP_address> --rate=<rate>

# Save results in XML format
sudo masscan -p0-65535 <target_IP_address> --rate=<rate> -oX <scan_results>.xml

# Save results in JSON format
sudo masscan -p0-65535 <target_IP_address> --rate=<rate> -oJ scan_results.json
```

**Flags:**
- `-p0-65535` — Scan all ports from 0 to 65535
- `<target_IP_address>` — Replace with the target IP address
- `--rate=<rate>` — Sets the rate of packets per second
- `-oX` — Output to XML file
- `-oJ` — Output to JSON file

---

### Phase 2: Vulnerability Assessment

The vulnerability assessment phase involves identifying and evaluating security weaknesses within the cloud infrastructure. This includes the assessment of misconfigurations, unpatched software, and flaws in cloud-based networks, applications, and services.

The primary purpose of this phase is to identify vulnerabilities that can be exploited to gain unauthorized access, escalate privileges, or disrupt cloud services. This phase is crucial for planning further exploitation strategies.

Attackers can use both automated and manual techniques to identify vulnerabilities. Tools such as Tenable Nessus, OpenVAS, and Qualys can be used to perform detailed scans and generate reports on the security posture of a cloud environment.

#### Vulnerability Scanning using Prowler

Source: https://github.com

Prowler contains more than 240 controls covering the CIS, NIST 800, NIST CSF, CISA, RBI, FedRAMP, PCI-DSS, GDPR, HIPAA, FFIEC, SOC2, GXP, AWS Well-Architected Framework Security Pillar, AWS Foundational Technical Review (FTR), ENS (Spanish National Security Scheme), and custom security frameworks.

```bash
# Start a basic scan specifying the cloud provider
prowler <provider>

# Generate a report (default: CSV, JSON-OCSF, JSON-ASFF, HTML)
prowler <provider> -M csv json-asff json-ocsf html

# Run a specific check
prowler azure --checks storage_blob_public_access_level_is_disabled

# Run for specific services
prowler aws --services s3 ec2
prowler gcp --services iam compute
prowler kubernetes --services etcd apiserver

# Scan specific AWS profile and filter by region
prowler aws --profile custom-profile --filter-region <region_1> <region_2>

# Scan a specific Azure subscription
prowler azure --az-cli-auth --subscription-ids <subscription_ID_1> <subscription_ID_2>

# Scan specific GCP projects
prowler gcp --project-ids <Project_ID_1> <Project_ID_2>
```

#### Identifying Misconfigurations using CloudSploit

Source: https://github.com

CloudSploit is a tool designed to identify misconfigurations and security risks across a wide range of cloud resources. Supports mapping its plugins to HIPAA and CIS Benchmarks compliance policies.

**Step 1: Configure cloud credentials**

```json
// AWS credentials
{
    "accessKeyId": "YOURACCESSKEY",
    "secretAccessKey": "YOURSECRETKEY"
}

// Azure credentials
{
    "ApplicationID": "YOURAZUREAPPLICATIONID",
    "KeyValue": "YOURAZUREKEYVALUE",
    "DirectoryID": "YOURAZUREDIRECTORYID",
    "SubscriptionID": "YOURAZURESUBSCRIPTIONID"
}

// GCP credentials
{
    "type": "service_account",
    "project": "GCPPROJECTNAME",
    "client_email": "GCPCLIENTEMAIL",
    "private_key": "GCPPRIVATEKEY"
}
```

**Step 2: Run scans**

```bash
# Perform a standard scan
./index.js

# HIPAA compliance mapping
./index.js --compliance=hipaa

# PCI compliance mapping
./index.js --compliance=pci

# CIS Benchmarks compliance mapping
./index.js --compliance=cis

# Get output in plain text on console
./index.js --console=text

# Print a table on console and save a CSV file
./index.js --csv=file.csv --console=table
```

---

### Phase 3: Exploitation

In the exploitation phase, attackers actively exploit the identified vulnerabilities to gain unauthorized access or control over the target cloud infrastructure. Attackers may use custom scripts, exploit frameworks, or tools such as Metasploit, sqlmap, or thc-hydra to launch attacks.

In addition, techniques such as exploiting misconfigured cloud storage, bypassing authentication, and exploiting insecure APIs might be implemented.

The primary objectives of this phase are to gain access to sensitive data, control cloud resources, or disrupt cloud-based operations. Successful exploitation can lead to data breaches, service disruptions, reputational damage, and further network penetration.

---

### Phase 4: Post-Exploitation

Post-exploitation is the final phase of the cloud-hacking methodology, which focuses on the actions to be taken after successfully exploiting a resource. This phase emphasizes maintaining access, covering tracks, and exploring deeper into the network.

Attackers establish persistence using various methods, including creating backdoors, escalating privileges, and establishing command-and-control (C2) channels. They often utilize tools such as Cobalt Strike and Metasploit to facilitate these activities.

The primary goals of this phase are to ensure long-term access to compromised systems, exfiltrate data, and prepare for further attacks. Attackers also focus on concealing their activities to evade detection by traditional security measures.

#### Cleanup and Maintaining Stealth

After compromising a cloud environment, attackers focus on cleaning up their traces and maintaining stealth to avoid detection and ensure continued access. Maintaining a low profile is crucial for prolonging the attack duration and increasing the potential for data exfiltration.

**Methods to Achieve Cleanup and Maintain Stealth:**

| Method | Description |
|--------|-------------|
| **Log Manipulation** | Once attackers compromise the target cloud environment, they can delete the logs or modify them to remove or hide entries that record their malicious actions |
| **Removing Credentials and Access Management** | This method involves removing temporary credentials such as temporary access tokens or keys; attackers can create hidden backdoors by establishing hidden accounts or access methods that blend into legitimate activities |
| **Manipulating System and Service Configurations** | This is the process of eliminating visible changes during an attack; additionally attackers can disable or modify alerts that could reveal their presence |
| **Implementing Persistence Mechanisms** | Using this method, attackers can hide malicious code through legitimate processes or services; alternatively, legitimate built-in cloud tools and scripts can be used to avoid suspicion |
