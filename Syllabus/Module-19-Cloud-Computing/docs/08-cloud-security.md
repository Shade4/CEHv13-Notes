# 08 — Cloud Security

> **CEH v13 Module 19 | Objective 08: Understand Cloud Security**

---

## Cloud Security Control Layers

The following layers show the mapping of the cloud model to the security control model:

| Layer | Description | Security Controls |
|-------|-------------|-------------------|
| **Application Layer** | Harden the application, establish the policies that monitor the application adoption security standards, e.g., OWASP for a web application; should meet and comply with appropriate regulatory and business requirements | Software development lifecycle, binary analysis, scanners, web app firewalls, transactional security |
| **Information Layer** | Develop and document an information security management program, which includes administrative, technical, and physical safeguards to protect information against unauthorized access, modification, or deletion | Data loss prevention (DLP), content monitoring and filtering, database activity monitoring, encryption |
| **Management Layer** | This layer covers the cloud security administrative tasks, which can facilitate continued, uninterrupted, and effective services of the cloud | Governance-risk-compliance (GRC), IAM, VA/VM, patch management, configuration management, monitoring |
| **Network Layer** | Deals with various measures and policies adopted by a network administrator to monitor and prevent illegal access, misuse, modification, or denial of network-accessible resources | Network IDS/IPS, firewalls, deep packet inspection, anti-DDoS, QoS, DNSSEC, OAuth |
| **Trusted Computing** | A secured computational environment that implements internal control, auditability, and maintenance to ensure the availability and integrity of cloud operations | Hardware and software Root of Trust (RoT) & API |
| **Computation and Storage** | Owing to the lack of physical control of the data and the machine, the service provider may be unable to manage the data and computation and lose the trust of the cloud consumers; CSPs must establish policies and implement appropriate backup mechanisms for continuity | Host-based firewalls, host-based IDS/IPS, integrity and file/log management, encryption, masking |
| **Physical Layer** | This layer includes security measures for cloud infrastructure, data centers, and physical resources | Security entities such as fences, walls, barriers, guards, gates, electronic surveillance, CCTV, physical authentication mechanisms, security patrols |

### Cloud Security is the Responsibility of Both Cloud Provider and Consumer

Security is a shared responsibility in cloud systems, in which both cloud consumers and CSPs have varying levels of control over the available computing resources. Different cloud service models (IaaS, PaaS, and SaaS) imply varying levels of control between CSPs and cloud consumers. Therefore, both parties share responsibilities to maintain adequate security for these systems.

---

## Cloud Computing Security Considerations

- Cloud computing services should be **tailor-made** by the vendor as per the given security requirements of the clients
- CSPs should provide **high multi-tenancy**, which enables optimum utilization of the cloud resources, and secure data and applications
- Cloud services should implement a **disaster recovery plan** for the stored data, which enables information retrieval in unexpected situations
- **Continuous monitoring** of the Quality of Service (QoS) is necessary to maintain the service level agreements between consumers and service providers
- Data stored in the cloud services should be implemented securely to ensure **data integrity**
- Cloud computing services should be **fast, reliable**, and able to provide quick response times to the new requests
- **Symmetric and asymmetric cryptographic algorithms** must be implemented for optimum data security in cloud computing
- Operational process of the cloud-based services should be **engineered, operated, and integrated** securely to the organizational security management
- **Load balancing** should be incorporated into the cloud services to facilitate networks and resources to improve the response time of the job with maximum throughput
- CSPs should provide better resiliency and **enhanced protection from physical threats**

---

## Cloud Security Controls — Placement

**Categories of security controls:**

| Control Type | Description | Example |
|-------------|-------------|---------|
| **Deterrent controls** | These controls reduce attacks on the cloud system | A warning sign on the fence or property to inform potential attackers of adverse consequences if they proceed to attack |
| **Preventive controls** | These controls strengthen the system against incidents by minimizing or eliminating vulnerabilities | A strong authentication mechanism to prevent unauthorized use of cloud systems |
| **Detective controls** | These controls detect and react appropriately to occurring incidents | Employing IDSs, IPSs, etc. helps detect attacks on cloud systems |
| **Corrective controls** | These controls minimize the consequences of an incident by limiting the damage | Restoring system backups |

---

## Cloud Network Security

### Virtual Private Cloud (VPC)

A VPC is a secure and independent private cloud environment that resides within the public cloud. VPC clients can execute programs, host applications, save data, and perform anything they wish on a private network using their individual accounts, but the private cloud is hosted by the cloud provider.

VPC clients cannot view the traffic directed to other client's VPCs. The client can also create an IPv6 block and add multiple subnets within that block. VPC can merge the scalability and other optimal features of public cloud computing with the data segregation of private computing. VPC resources are available on demand and can be expanded and configured based on the requirement.

### Public and Private Subnets

- **Public subnets** — consists of an outward path that transmits messages via an Internet Gateway (IGW), which allows IPv4 and IPv6 traffic from the VPC without any conditions on the bandwidth
- **Private subnets** — VMs in the private subnet cannot communicate via the IGW but can receive inbound traffic via the IGW as long as their network ACLs and security groups permit it; the private subnet can connect to the external web via NAT (NAT does not directly permit inward traffic from the web)

### Transit Gateways

A transit gateway is a network routing solution that establishes and manages communication between an on-premises consumer network and VPCs via a centralized unit. This approach simplifies the network topology and eliminates complicated peering connections. These communications can be allowed or blocked by cloud-specific ACLs depending on the port numbers and IP addresses of the hosts.

### VPC Endpoints

A VPC endpoint establishes a private connection between a VPC and another cloud service without exposing to the internet, external gateways, NAT solutions, VPN connections, or public IP addresses. The traffic between virtual machines in the VPC and cloud services does not leave the organization's network.

**Two types of VPC endpoints:**
- **Interface endpoint** — an Elastic Network Interface (ENI) that has a private IP address within the limit of a defined subnet; operates as an initial point of source for traffic towards a VPC or supported cloud services
- **Gateway-load-balancer endpoint** — also an ENI; operates as an initial point of source to impede traffic flow and divert it to a service that has been configured through a gateway load balancer, which is then used for security inspection

---

## Zero Trust Networks

The Zero Trust model is a security implementation that by default assumes every user trying to access the network is not a trusted entity and verifies every incoming connection before allowing access to the network. It strictly follows the principle "Trust no one and validate before providing a cloud service or granting access permissions."

**Representation of Zero Trust Network:**

The cloud control plane is a supporting system that coordinates and manages the data plane (every other component in the network). The control plane permits network access requests only from legitimate and verified users or devices. Fine-grain policies are applied at this layer based on the role in the organization, time of day, and device type. To access more secured Internet resources, users need stronger authentication. Once the access request is approved by the control plane, the data plane is configured to accept traffic only from that particular client.

Zero Trust can be integrated with techniques such as **encryption, multi-factor authentication, and privileged access management (PAM)**. This trust network follows the micro-segmentation method to break the network zone into smaller pieces to provide separate access to certain parts of the network. If any perimeter breach is identified, the micro-segmentation prevents the network from further exploitation.

---

## Security Assertion Markup Language (SAML)

SAML is a popular open-standard protocol used for authentication and authorization between two communicating entities. It provides a single sign-on (SSO) facility with multiple applications or services with one set of common credentials. SAML can be offered as software-as-a-service, which can be installed at the service provider (SP) and identity provider (IdP) to simplify the federated authorization and authentication mechanisms for users.

**The SAML protocol consists of three entities:**

- **Client or User** — it is an entity with a valid account that requests a service or resource through a web browser
- **Service provider (SP)** — it is a server hosting applications or services for the users
- **Identity provider (IdP)** — it is an entity within a system that stores user directories and validating mechanisms

When SAML federation software is installed or configured, it creates a trust relationship between SP and IdP, enabling secure communication. When a user wishes to access any service or resource, he/she must be authenticated by the IdP. Soon after a service request is initiated from the user, the SP sends a SAML request to the IdP to validate the user. The IdP then creates an XML-based SAML authentication assertion that describes what type of login attempt has been initiated (password, two-factor, etc.), the SAML assertion, which contains specific details about the user; and the authorization assertion, which describes whether the user has access to the service or deny details. SAML assertions are then forwarded to the SP. Once the authentication process is completed successfully, the user is free to access the protected resources or services.

---

## High Availability Zones

A cloud environment for an application should have high availability zones because it should allow application's services to be continued even during intentional or unintentional network downtimes. High availability can be achieved by dividing servers into zones and maintaining consistency across them. It enables the environment to handle failures in individual availability zones or the network without losing data. It also provides centralized management to monitor network operations and resource utilization.

A cloud environment with high availability consists of two nodes:
- **Master node** — runs in the first availability zone
- **Secondary node** — runs in secondary availability zone; protected from service outages such as disk failure, volume failure, network failure, and zone failure

Each node is independent and has separate zones. If any node fails, a copy of its data is ensured to exist in the other node, which provides access to all the information. A node can be shut down to be upgraded while the other node actively provides the services.

---

## Cloud Access Security Broker (CASB)

Cloud Access Security Brokers (CASBs) are on-premise or cloud-hosted solutions responsible for enforcing security, compliance, and governance policies in cloud applications. A CASB is located between the on-premise infrastructure of an organization and the infrastructure of a cloud provider. It acts as a gatekeeper that enables organizations to extend their security policies beyond their own infrastructure.

### Features of CASB

- **Visibility into cloud usage** — finds shadow IT cloud services and provides visibility into the user activities with the allowed cloud applications
- **Data security** — enforces data-centric security encryption, tokenization, access control, and information rights management
- **Threat protection** — detects and responds to malicious insider threats, privileged user threats, and compromised accounts
- **Compliance** — discovers critical data in the cloud and enforces DLP policies to satisfy the data residency and compliance requirements

### What CASBs Offer

- **Firewalls** — to identify malware, thereby preventing the malware from entering the enterprise network
- **Authentication** — for user credentials, ensuring that only the allowed users can access the required organizational resources
- **WAFs** — to prevent malware from breaching security at the application level instead of the network level
- **DLP** — prevents users from transferring critical information outside the organization

### How CASBs Work

A CASB works by:
- Ensuring network traffic between on-premise devices and the cloud provider complies with the organizational security policies
- Providing insights into the use of cloud applications across cloud platforms and identifying unsanctioned use
- Using auto-discovery to identify cloud applications in use, high-risk applications, high-risk users
- Enforcing security access controls such as encryption and device profiling
- Providing services such as credential mapping when SSO is not available

### CASB Solutions

- **Forcepoint ONE CASB** (https://www.forcepoint.com) — complete security for all cloud applications; key features include cloud application discovery, cloud application risk scoring, data classification, user and application governance, real-time activity monitoring/analytics, automatic anomaly detection, data loss prevention, and integration with third-party solutions
- **CloudCodes** (https://www.cloudcodes.com)
- **Cisco Cloudlock** (https://www.cisco.com)
- **Zscaler CASB** (https://www.zscaler.com)
- **Proofpoint Cloud App Security Broker (CASB)** (https://www.proofpoint.com)
- **FortiCASB** (https://www.fortinet.com)

---

## Next-Generation Secure Web Gateway (NG SWG)

NG SWG is a cloud-based security solution that protects an organization's network from cloud-based threats, malware infections, and online data theft. It also allows clients to securely access cloud services. It detects cloud-based threats in advance, prioritizes them based on their risks, and manages the application being used by different users and clients.

**Features:**
- URL filtering
- Certificate (TLS/SSL) decryption
- CASB operations such as identifying, decrypting, analyzing, and securing traffic
- Advanced threat protection (ATP), along with sandboxing and machine learning (ML)–oriented anomaly detection
- Support for data loss prevention (DLP) for web traffic and cloud applications
- Qualitative metadata contexts for web inspection and reporting

**NG SWG Solutions:**
- Netskope Next Gen Secure Web Gateway (SWG) (https://www.netskope.com)
- Cloudflare Gateway (https://www.cloudflare.com)
- Skyhigh Secure Web Gateway SWG (https://www.skyhighsecurity.com)
- Menlo Secure Web Gateway SWG (https://www.menlosecurity.com)
- McAfee MVISION UCE (https://www.mcafee.com)

---

## Cloud Security Tools

### Scout Suite

Source: https://github.com

Scout Suite is a multi-cloud security-auditing tool that helps security professionals assess the security posture of cloud environments. It leverages APIs exposed by cloud providers to gather configuration data and automatically highlights areas of risk. Instead of navigating through numerous pages on web consoles, Scout Suite offers a clear and concise view of the attack surface.

```bash
# Assess AWS security posture
scout aws --profile <your-aws-profile>

# Assess Azure security posture
scout azure --tenant-id <your-tenant-id> --subscription-id <your-subscription-id> \
  --client-id <your-client-id> --client-secret <your-client-secret>

# Assess GCP security posture
scout gcp --service-account-file path/to/your/service-account-key.json
```

**Scout Suite supports the following cloud providers:**
- `aws` — Run scout against an Amazon Web Services account
- `gcp` — Run scout against a Google Cloud Platform account
- `azure` — Run scout against a Microsoft Azure account
- `aliyun` — Run scout against an Alibaba Cloud account
- `oci` — Run scout against an Oracle Cloud Infrastructure account
- `kubernetes` — Run scout against a Kubernetes cluster
- `do` — Run scout against a DigitalOcean account

Once scanning is completed, Scout Suite generates an HTML report, including the findings and cloud account configuration. Scout Suite represents risk ratings with different colors, making it easier to prioritize issues.

### Qualys Cloud Platform

Source: https://www.qualys.com

Qualys Cloud Platform is an end-to-end IT security solution that provides a continuous, always-on assessment of the global security and compliance posture, with visibility across all IT assets irrespective of where they reside. It provides sensors that provide continuous visibility, and all cloud data can be analyzed in real-time. It responds to threats immediately, performs active vulnerability in internet control message protocol timestamp request, and visualizes results in one place with AssetView.

**Additional Cloud Security Tools:**
- Prisma Cloud (https://www.paloaltonetworks.com)
- Netskope One (https://www.netskope.com)
- Lookout CipherCloud (https://www.lookout.com)
- Trend Micro Deep Security (https://www.trendmicro.com)
- Data-Aware Cloud Security (https://www.skyhighsecurity.com)

### Securiti

Source: https://securiti.ai

Securiti is an AI-powered security tool designed to discover and monitor shadows, native data assets, and untracked or unmanaged data repositories that pose significant privacy risks across multi-cloud environments. This tool restricts untrusted code from running and ensures that functions, containers, and VMs remain immutable, thus preventing any changes to running workloads compared with their originating images.

**Additional Shadow Cloud Asset Discovery Tools:**
- CloudEagle (https://www.cloudeagle.ai)
- Microsoft Defender for Cloud Apps (https://learn.microsoft.com)
- FireCompass (https://www.firecompass.com)
- Data Theorem (https://www.datatheorem.com)
- BetterCloud (https://www.bettercloud.com)

### Aqua

Source: https://www.aquasec.com

Aqua scans container images, VMs, and serverless functions for known vulnerabilities, embedded secrets, configuration and permission issues, malware, and open-source licensing. This tool restricts untrusted code from running and ensures that functions, containers, and VMs remain immutable, thus preventing any changes to running workloads compared with their originating images. Aqua can also integrate into existing infrastructure, thereby making it easy to manage DevSecOps collaboration, logging and reporting, incident response, and event monitoring.

**Additional Container Security Tools:**
- Sysdig Falco (https://sysdig.com)
- Anchore (https://anchore.com)
- Snyk Container (https://snyk.io)
- Lacework (https://www.lacework.com)
- Tenable Cloud Security (https://www.tenable.com)

### Advanced Cluster Security for Kubernetes (ACS)

Source: https://www.redhat.com

Advanced Cluster Security (ACS) for Kubernetes is a comprehensive solution designed to enhance the security of Kubernetes environments. It also helps build, deploy, and run cloud-native applications. It provides a robust set of tools and features focused on visibility, compliance, threat detection, and risk management to ensure comprehensive protection for cloud-native workloads.

**Additional Kubernetes Security Tools:**
- Aqua Kubernetes Security (https://www.aquasec.com)
- Kyverno (https://github.com)
- Kubeaudit (https://github.com)
- Sumo Logic (https://www.sumologic.com)
- Kubespace (https://kubescope.io)

### Dashbird

Source: https://dashbird.io

Dashbird is a comprehensive observability and monitoring platform designed for serverless applications. It provides real-time monitoring, error detection, and end-to-end visibility across various cloud resources, thus enabling security professionals to identify and resolve issues. By integrating seamlessly with cloud environments, it helps maintain high performance, security, and operational excellence for serverless workloads.

**Additional Serverless Security Tools:**
- CloudGuard (https://www.checkpoint.com)
- Datadog Serverless Monitoring (https://www.datadoghq.com)
- Prisma Cloud (https://www.paloaltonetworks.com)
- Iumigo (https://lumigo.io)
- Sysdig (https://sysdig.com)

---

## NIST Recommendations for Cloud Security

Source: https://www.nist.gov

The National Institute of Standards and Technology (NIST) provides comprehensive guidelines and recommendations for mandatory access control as part of its cybersecurity framework. These recommendations are designed to help organizations implement effective access control measures to protect their information systems and data.

**Key recommendations:**
- Assess the risk posed to the client's data, software, and infrastructure
- Select an appropriate deployment model according to needs
- Ensure audit procedures are in place for data protection and software isolation
- Renew SLAs in case of security gaps between the organization's security requirements and cloud provider's standards
- Establish appropriate incident detection and reporting mechanisms
- Analyze the security objectives of the organization
- Enquire about who is responsible for data privacy and security issues in the cloud
- Implement strong anti-virus and firewalls to filter-out unusual traffic
- Encrypt data at rest and in transit

### NIST Access Control Tables

**IaaS Access Control (Table 19.11):**

| Subjects | Operations | Objects |
|---------|------------|---------|
| IaaS end user | Login, Read, Write, Create | Hypervisor |
| IaaS end user | Read, Write, Create | VMs |
| VM | Write | Hypervisor |
| VM | Read, Write | Other VMs within the same host |
| VM | Read, Write | Other VMs from different hosts but within the same IaaS providers |
| VM | Read, Write, Create | Guest OS images |
| Hypervisor | Read, Write, Create | Hardware resources |
| Hypervisor | Read, Write, Create | VMs |

**PaaS Access Control (Table 19.12):**

| Subjects | Operations | Objects |
|---------|------------|---------|
| Application user | Read | Memory data |
| VM of a hosted application | Read, Write | Other applications' data within the same host |
| Application developer | Create, Read, Write | Middleware data, memory data |
| Cloud service provider | Replicate | Application-related data |

**SaaS Access Control (Table 19.13):**

| Subjects | Operations | Objects |
|---------|------------|---------|
| Application user | Read, Write | Application-related data |
| Application user | Read | Memory |
| Application user | Execute | Application |
| Application user | Read, Write | Application data |
| Application user | Execute | Application code |
| VM of a hosted application | Execute | Other application code within the same host |

---

## Best Practices

### 24 General Best Practices for Securing the Cloud

1. Enforce **data protection, backup, and retention** mechanisms
2. Enforce **SLAs** for patching and vulnerability remediation
3. Vendors should regularly undergo **AICPA SSAE 18 Type II audits**
4. Verify one's own cloud in **public domain blacklists**
5. Enforce **legal contracts** in employee behavior policy
6. Prohibit **user credentials sharing** among users, applications, and services
7. Implement strong **authentication, authorization and auditing** controls
8. Check for **data protection** at both the design stage and at runtime
9. Implement strong **key generation, storage and management, and destruction** practices
10. Monitor the **client's traffic** for any malicious activities
11. Prevent unauthorized server access using **security checkpoints**
12. Disclose applicable **logs and data** to customers
13. Analyze **cloud provider security policies** and SLAs
14. Assess the security of **cloud APIs** and log customer network traffic
15. Ensure that the cloud undergoes regular **security checks and updates**
16. Ensure that physical security is a **24 x 7 x 365** affair
17. Enforce **security standards** in installation/configuration
18. Ensure that the memory, storage, and network access is **isolated**
19. Leverage strong **two-factor authentication** techniques where possible
20. Implement a baseline **security breach notification** process
21. Analyze **API dependency chain software** modules
22. Enforce stringent **registration and validation** processes
23. Perform vulnerability and configuration **risk assessments**
24. Disclose infrastructure information, **security patching, and firewall details** to customers

---

### Best Practices for Securing AWS Cloud

**Basic AWS Security Practices:**
- Categorize user identity based on account, role, and group to manage permissions for resource allocation
- Utilize temporary credentials to avoid potential risks of abusing access keys
- Implement policies for regular rotation of access keys, passwords, and other credentials
- Implement the principle of least privilege on AWS resources
- Employ AWS Trusted Advisor to avoid security misconfigurations
- Create accessible AWS security policies
- Segregate AWS assets such as resources and user data to prioritize security needs
- Use AWS Service Quotas to manage and set limits on resource usage, thus preventing overprovisioning and abuse
- Integrate and enable security management systems according to organizational requirements
- Securely delete unused data and groups from the AWS environment
- Use IAM Access Analyzer to audit users and policies
- Leverage AWS Git projects such as git-secrets, AWS Step Functions, and AWS Lambda to protect resources against unauthorized access
- Enable multi-factor authentication (MFA) for all AWS accounts to add an extra layer of security
- Keep all systems and applications up to date with the latest security patches

**AWS Infrastructure Security Practices:**
- Use Information security management systems (ISMS) to conduct regular checks on security policies and controls
- Perform network segmentation and create security zones for easy management
- Use load balancers, content distribution networks (CDNs), and web application firewalls (WAFs) to prevent DoS, DDoS, XSS, and SQLi attacks
- Customize AWS Security Hub insights to track and manage AWS security issues
- Implement a single set of policies for data loss prevention
- Perform automated security assessments to identify vulnerabilities in AWS resources using Amazon Inspector

**AWS Security Hub Practices:**
- Leverage AWS labs script to enable security hub in all AWS accounts
- Establish threat detection systems such as GuardDuty and Amazon Inspector
- Enable AWS Config and CIS Foundations standards for all AWS accounts and regions
- Assign tags to security hub resources for managing access
- Ensure control of specific IAM policies for different types of users and centralize the IAM through cloud infrastructure entitlement management (CIEM) for easy governance of accounts, groups, and roles
- Build custom actions to obtain a copy of the security hub findings of internal and external resources for remediation purposes
- Utilize IAM roles instead of IAM users to access AWS resources, particularly applications and services
- Use IAM Access Analyzer to identify resources that are shared with external entities and ensure that they are properly secured

**AWS Backup Data Practices:**
- Ensure and automate frequent backups
- Safeguard backups using immutable storage
- Incorporate backup processes in disaster recovery, business continuity, and incident response plans
- Implement configuration audit, monitoring, and alert system
- Enable and monitor logs from AWS services such as VPC Flow Logs, S3 access logs, and CloudFront logs
- Examine data recovery abilities

---

### Best Practices for Securing Microsoft Azure

- Ensure identity as the main security perimeter in Azure environments
- Maintain the visibility of users connected to the network via Azure Express Route or a site-to-site VPN
- Utilize Azure Network Watcher to check the most common VPN connections and gateway issues
- Implement a single sign-on policy
- Enable MFA with conditional access policy
- Perform automated decisions based on conditional access to subscribers
- Implement Azure role-based access control (Azure RBAC) and privileged identity management to monitor and control resources
- Limit the management group into three levels to prevent confusion between operations and security decisions in the cloud
- Enforce at least two emergency access accounts to limit access to privileged resources in an Azure environment
- Employ Microsoft services such as Microsoft Defender for Cloud, Microsoft Defender for Cloud Apps, and Microsoft Sentinel for the detection and prevention of threats
- Implement Microsoft Azure Security Center for real-time threat protection, CVE scanning, and Microsoft Defender for Endpoint licensing
- Leverage threat detection for Azure SQL
- Utilize cloud-based SIEM solutions and integrated defender for cloud alerts
- Utilize shared access signatures (SAS) to control and limit client data access
- Restrict access to administrative ports such as SSH, RDP, and WinRM
- Implement just-in-time (JIT) VM access that provides temporary permission to perform privileged tasks, if necessary, and avoids unauthorized usage of resources
- Implement strong operational security policies
- Automate the processes of creation and implementation of apps and services
- Verify the performance of any application or service before deployment
- Activate password hash synchronization
- Disable legacy authentication protocols
- Frequently review the changes made for security improvement
- Regularly review and audit IAM policies to ensure that they follow the principle of least privilege and remove unnecessary access
- Use Azure encryption services such as Azure Disk Encryption and Azure Key Vault to encrypt data stored and transferred within Azure
- Deploy Azure Firewall to provide network protection and to centrally control and log application and network connectivity policies
- Protect APIs using Azure API Management and OAuth2.0 to securely control and monitor API access
- Enable Azure DDoS Protection to safeguard applications from DDoS attacks
- Manage virtual machines using Azure Bastion for RDP and SSH connections

---

### Best Practices for Securing Google Cloud Platform

- Implement STRIDE (spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege) as a threat model for threat planning in Google Cloud
- Leverage key management services (KMSs) and customer-supplied encryption keys (CSEKs) to encrypt and manage data
- Implement application layer encryption on Google Kubernetes Engine (GKE) services
- Enable encryption for GKE cluster nodes with customer-managed keys and controls access through specific IP addresses using HTTPS
- Enforce SSL encryption in cloud SQL databases
- Deactivate support for interactive serial console in Google VMs
- Employ Terraform modules from private git repositories to automatically implement resources
- Implement shielded VMs to protect against rootkits, remote attacks, and privilege escalation
- Use a sandbox environment to examine security attacks
- Check for vulnerabilities on images stored in the container registry
- Create well-defined groups and assign roles using specific naming conventions instead of assigning permissions to individual users
- Use a dedicated channel to connect to Google Cloud from the on-premise networks
- Enforce tag-based firewall rules to monitor and secure the network traffic flow
- Use the Cloud Logging API to ingest, aggregate, and process logs
- Use Google Security Command Center Enterprise for aggregating and managing security findings to detect and alert misconfigurations, vulnerabilities, and threats
- Maintain visibility over volumes and resources used in multiple projects
- Enforce strong password policies and MFA in cloud and corporate entities
- Continuously monitor Admin Activity Logs to track GCP resource access
- Use IAM frameworks to access Google Cloud resources
- Disable publicly accessible cloud storage buckets in organizational GCP accounts
- Enforce proper data retention policies for Google Cloud storage
- Enable Private Google Access to ensure that VMs in VPC networks can access Google APIs and services without using public IP addresses

---

### Best Practices for Kubernetes Security

- Ensure proper validation of the **file contents** and their path at every stage of processing
- Implement the **configuration method** for the credential paths and do not depend on the hardcoded paths
- Raise errors explicitly after each step of a **compound operation**
- Use the **copy-then-rename** method for log rotation to ensure that the logs are not lost when restarting the kubelet
- Ensure secure and reliable handling of JSON data by using well-tested JSON libraries and proper type structures in applications that interact with Kubernetes APIs
- **Never use compound shell commands** without proper validations because they affect the system state
- Check the returned error value of `os.ReadLink /proc/<pid>/exe` explicitly to determine if the PID is a kernel process
- Use centralized libraries to perform common tasks and use common parsing functions, such as `ParsePort`, across the codebase to increase code readability
- Use persistent logs in place of log rotation so that the logs can be written in linear order and new logs can be created when rotation is required
- Use **single encoding format** for all configuration tasks because it supports centralized validation
- Limit the size of manifest files to prevent out-of-memory errors in kubelet
- Use kube-apiserver instances that maintain CRLs to check the presented certificates
- Use key management services to enable secret data encryption and avoid using AES-Galois/Counter mode or cipher block chaining for encryption
- Authenticate all HTTPS connections by default to ensure certificates are issued by the CA and prevent MITM attacks
- Avoid using legacy SSH tunnels because they do not perform proper validation of server IP addresses
- Use online certificate status protocol (OCSP) stapling to check the revocation status of certificates
- Use TLS in development and production configurations to reduce vulnerabilities due to misconfiguration
- Use ACLs to manage the file access permissions and prevent unauthorized access
- Enable comprehensive logging and monitoring for Kubernetes clusters using tools such as Prometheus, Grafana, and ELK Stack
- Implement policy management tools such as Open Policy Agent (OPA) or Kyverno to enforce security policies across the Kubernetes cluster
- Regularly patch and update Kubernetes components and dependencies with the latest versions
- Configure resource quotas and limits to prevent resource exhaustion
- Use network policies and service meshes to control and secure pod-to-pod communication
- Regularly review and rotate Kubernetes secrets to minimize the risk of credential compromise

---

### Best Practices for Docker Security

- **Avoid exposing the Docker daemon socket** — this is the basic entry point for the Docker API
- **Only use trusted Docker images** — Docker images created by malicious users may be injected with backdoors
- **Regularly patch** host OS and Docker with the latest security updates
- **Limit capabilities** using `--cap-drop all` command to drop all capabilities, then assign only the necessary ones
- **Always run Docker images** with `--security-opt=no-new-privileges` to prevent privilege escalation attacks using `setuid` or `setgid` binaries
- **Disable the inter-container communication** feature when running Docker daemon by using `--icc=false`; to communicate with other containers, use `--link=CONTAINER_NAME_or_ID:ALIAS` option
- **Use Linux security modules** such as seccomp, AppArmor, and SELinux to gain fine-grained control over the processes
- **Limit resources** such as memory, CPU, the maximum number of file descriptors, the maximum number of processes, and restarts to prevent DoS attacks
- **Enable read-only mode** on filesystems and volumes by setting the `--read-only` flag
- **Set Docker daemon log level** to 'info' and avoid running Docker daemon using the 'debug' log level
- **The default user** setting for the Docker image is root; configure the container application to run as an unprivileged user to prevent privilege-escalation attacks
- **Install only necessary packages** to reduce the attack surface
- **Check that Docker images** from the remote registry are digitally signed using Docker content trust
- **Avoid using environmental variables** for sensitive information and use Docker secrets management for encrypting the secret information in transit
- **Secure the API endpoints** with HTTPS when exposing the RESTful API
- **Avoid using the default bridge network** when using the single-host app with networking
- **Always store sensitive data** in Docker Volumes for enhanced data security, data persistence, and data encryption
- **Establish basic authentication** by enabling TLS for secure communication over HTTPS between Docker client and the daemon
- **Use tools** such as Inspec and dive to detect Docker vulnerabilities
- **Limit SSH login connections** to the admin for processing log files of containers while performing administrative operations such as testing and troubleshooting
- **Employ automated container labeling** mechanism to avoid discrepancy while accessing the containers
- **Incorporate the HEALTHCHECK command** into Docker files wherever possible to ensure better health monitoring and secure container operations
- **Use Docker's namespace features** such as PID, IPC, network, and user namespaces to isolate containers
- **Enable user namespaces** to include an additional layer of isolation between the host and containers
- **Use Docker's resource constraint options**, such as `--memory` and `--cpus`, to limit the CPU and memory usage of containers
- **Enable Docker content trust (DCT)** to ensure the integrity and authenticity of images
- **Use Docker's USER directive** to specify a non-root user to avoid running containers with root privileges

---

### Best Practices for Serverless Security

- **Minimize serverless permissions** in the development phase to reduce the attack surface area
- **Monitor function layers regularly** to identify the attempts of malicious code injection and other web server attacks
- **Use third-party security tools** as they provide additional layers of visibility and control
- **Regularly patch and update** function dependencies and applications
- **Use tools such as Snyk** to scan serverless applications for known vulnerabilities
- **Maintain isolated function perimeters** and avoid relying on the function access and invocation ordering
- **Properly sanitize event input** to prevent code injection attacks
- **Use security libraries** that disable access to resources and implement runtime least-privileges
- **Deploy functions in minimal granularity** to minimize the level of detail and prevent implicit global roles
- **Employ data validation technique** on schemas and data transfer objects, instead of data serialization and deserialization
- **Leverage API gateway capabilities** to perform input data filtering, traffic throttling, and rate limiting, and to protect from DDoS attacks
- **Audit and monitor functions** by enforcing verbose and late logging of function events
- **Use secure coding practices** and perform code review sessions to patch the vulnerable application code
- **Use TLS/HTTPS** for secure communication and use cryptographic algorithms to encrypt credentials
- **Verify the SSL certificates** to recognize the communication with remote identity and ensure the communication stops if the verification fails
- **Use secret storage** for sensitive information that provides both runtime access and key rotation for protection
- **Implement network security controls** such as virtual private cloud (VPC) configurations, which limit access to serverless functions
- **Ensure that all triggers** such as API Gateway, S3, and DynamoDB, are securely configured and accessible only to authorized entities

---

## Compliance Checklists

### Checklist for Security Team Readiness

| Question | Security Team |
|---------|--------------|
| Are the members of the security team formally trained in cloud technologies? | ☐ |
| Do the organization's security policies consider cloud infrastructure? | ☐ |
| Has the security team ever been involved in implementing cloud infrastructure? | ☐ |
| Has an organization defined security assessment procedures for cloud infrastructure? | ☐ |
| Has an organization ever been audited for cloud security threats? | ☐ |
| Will the organization's cloud adoption comply with the security standards that the organization follows? | ☐ |
| Has security governance been adapted to include cloud? | ☐ |
| Does the team have adequate resources to implement cloud infrastructure and security? | ☐ |

### International Cloud Security Organizations

**Cloud Security Alliance (CSA)**

Source: https://cloudsecurityalliance.org

The CSA is a global nonprofit organization that provides rising awareness and promotes best practices and security policies to help and secure the cloud environment. CSA provides education and knowledge on the uses of cloud computing and helps in securing all forms of computing. CSA can be used to connect the subject matter expertise of the industries, governments, and corporate members to provide cloud-based research, education, certification, and products.
