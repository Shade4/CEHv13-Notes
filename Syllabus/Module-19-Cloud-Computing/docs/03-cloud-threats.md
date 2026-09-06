# 03 — Cloud Computing Threats

> **CEH v13 Module 19 | Objective 02: Explain Cloud Computing Threats**

---

## OWASP Top 10

### OWASP Top 10 Cloud Security Risks

| Risk | Description |
|------|-------------|
| **R1 — Accountability and Data Ownership** | Organizations use the public cloud for hosting business services instead of a traditional data center; sometimes the cloud causes the loss of data accountability and control, whereas using a traditional data center helps in controlling and protecting the data logically and physically; using the public cloud can jeopardize data recoverability and result in critical risks |
| **R2 — User Identity Federation** | Enterprises use services and applications of different cloud providers, creating multiple user identities and complicating the management of multiple user IDs and credentials; cloud providers have less control over the user lifecycle |
| **R3 — Regulatory Compliance** | Following regulatory compliance can be complex; what that is secured in one country may not be secured in another country owing to the lack of transparency and different regulatory laws followed across various countries |
| **R4 — Business Continuity and Resiliency** | When using cloud services, there is a chance of risk or money loss if the cloud provider handles the business continuity improperly |
| **R5 — User Privacy and Secondary Usage of Data** | The use of social websites poses a risk to personal data because they are stored in the cloud and most social application providers mine user data for secondary usage; the default share feature in social networking sites can compromise the privacy of personal data |
| **R6 — Service and Data Integration** | Organizations must ensure proper protection when proprietary data are transferred from the end-user to the cloud data center; unsecured data in transit are susceptible to eavesdropping and interception attacks |
| **R7 — Multi Tenancy and Physical Security** | Cloud technology uses the concept of multi-tenancy for sharing resources and services among multiple clients; inadequate logical segregation may lead to tenants interfering with each other's security features |
| **R8 — Incidence Analysis and Forensic Support** | When a security incident occurs, investigating applications and services hosted at a cloud provider can be challenging because event logs are distributed across multiple hosts and data centers located at several countries and governed by different laws and policies; owing to the distributed storage of logs across the cloud, law enforcement agencies may face problems in forensics recovery |
| **R9 — Infrastructure Security** | Organizations should configure the infrastructure in alignment with the industry best practices because there is constant risk of malicious actions; misconfiguration of infrastructure may allow network scanning for vulnerable applications and services to retrieve information, such as active unused ports and default passwords and configurations |
| **R10 — Non-Production Environment Exposure** | Non-production environments are used for application design and development and to test activities within an organization; using non-production environments increases the risk of unauthorized access, information disclosure, and information tampering |

---

### OWASP Top 10 Kubernetes Security Risks

| Risk | Description | Mitigation |
|------|-------------|-----------|
| **K01 — Insecure Workload Configurations** | Insecure workload configurations involve deploying applications with settings that increase their vulnerability to attacks (running containers with root, not setting resource limits, or allowing excessive network access); these misconfigs can be exploited by attackers to escalate privileges, execute arbitrary code, or cause DoS by exhausting system resources | Set appropriate security contexts to restrict container privileges, define resource limits to prevent resource exhaustion, and use network policies to control communication between pods |
| **K02 — Supply Chain Vulnerabilities** | Supply chain vulnerabilities arise from integrating third-party software and components into Kubernetes environments; these vulnerabilities can exist in container images, application dependencies, or CI/CD pipelines, making it more challenging to manage and secure all elements of the software supply chain | Implement rigorous supply chain security measures, such as regularly scanning container images for vulnerabilities, using signed and verified images, and incorporating security checks into the CI/CD pipeline |
| **K03 — Overly Permissive RBAC Configurations** | Overly permissive role-based access control (RBAC) configurations grant excessive permissions to users and services; this increases the attack surface, as attackers or malicious insiders can exploit these broad permissions to gain unauthorized access, manipulate data, or operational disruptions | Implement the principle of least privilege by carefully defining roles and permissions |
| **K04 — Lack of Centralized Policy Enforcement** | The absence of centralized policy enforcement in Kubernetes can lead to inconsistent security policies across clusters; this inconsistency can result in vulnerabilities due to misconfigurations or gaps in security controls, making the environment more susceptible to attacks | Organizations should adopt tools such as Open Policy Agent (OPA) to enforce consistent security policies across all clusters |
| **K05 — Inadequate Logging and Monitoring** | Inadequate logging and monitoring refer to the lack of comprehensive and detailed logs for activities within the Kubernetes environment; this deficiency makes it difficult to detect, investigate, and respond to security incidents effectively; without adequate logging and monitoring, security teams are blind to potential threats and malicious activities | Implementing comprehensive logging and monitoring practices including configuring Kubernetes to capture detailed logs of all relevant activities, integrating with centralized logging solutions, and setting up real-time alerting for suspicious activities |
| **K06 — Broken Authentication Mechanisms** | Broken authentication mechanisms refer to weaknesses in the process of verifying the identity of users and services in a Kubernetes environment; this can include improper configuration of authentication protocols, weak password policies, or failure to implement multi-factor authentication (MFA) | It is crucial to implement strong authentication practices including configuring robust authentication protocols, enforcing strong password policies, and enabling MFA for all users |
| **K07 — Missing Network Segmentation Controls** | The absence of network segmentation controls refer to the lack of proper security components and ports within a Kubernetes environment; without effective segmentation, once attackers gain access to one component they can move laterally within the environment; the absence of network segmentation can lead to significant breaches, unauthorized access to sensitive data, and disruption of services | Implement network segmentation using network policies that use third-party solutions to help limit lateral movement within the environment |
| **K08 — Secrets Management Failures** | Secrets management failures occur when sensitive information such as passwords, API keys, or certificates is improperly stored or handled; this can make it easier for attackers to gain access to critical systems and data; attackers can use compromised secrets to access applications, escalate privileges, or move laterally within the environment | Use dedicated secrets management tools, ensuring secrets are encrypted, and strictly controlled access |
| **K09 — Misconfigured Cluster Components** | Misconfigured components in core Kubernetes components such as the API server, etcd, or scheduler can stem from default settings, misapplied configurations, or manual errors, leaving the cluster vulnerable to attacks; attackers can exploit these misconfigurations to gain control over the environment | Mitigation involves regularly auditing cluster configurations, applying security best practices, and keeping components up-to-date |
| **K10 — Outdated and Vulnerable Kubernetes Components** | Using outdated and vulnerable Kubernetes components poses significant security risks; these components may contain known vulnerabilities that can be exploited by attackers, including both Kubernetes itself and its dependencies, which need to be regularly updated to maintain a secure environment | It is crucial to regularly update Kubernetes components and its associated components |

---

### OWASP Top 10 Serverless Security Risks

| Risk | Attack Vector | Security Weakness | Impact |
|------|--------------|-------------------|--------|
| **A1 — Injection** | Input arrives not only from API but also from functions that are invoked from various event sources (cloud storage events (S3 Blobs), stream data processing (AWS Kinesis), database modifications (DynamoDB, CosmosDB), code modifications (AWS CodeCommit), and notifications (SMS, email, IoT) | SQL/NoSQL injection, OS command injection, code injection | Impact depends on the permissions of the vulnerable function; if the function has access to the cloud storage, the injected code can delete or upload corrupted data |
| **A2 — Broken Authentication** | Serverless functions are stateless, have different goals, and are triggered by different events; attackers try to identify missing authentication processes, such as open APIs and public cloud storage resources | Poor design of identity and authentication controls | Accessing functions without authentication leads to sensitive data leakage, system business logic breakage, and execution flow disruption |
| **A3 — Sensitive Data Exposure** | Attacks on traditional web applications, such as cracking, person-in-the-middle (PITM) attacks, and data stealth in transit, and at rest, are mirrored in serverless applications; attackers target cloud storage (S3 Blob) and database tables (DynamoDB, CosmosDB) | Storing sensitive data in plaintext or using weak encryption; writing data to the /tmp directory without removing after use | Exposure of sensitive data, such as PII, health records, credentials, and credit card details |
| **A4 — XML External Entities (XXE)** | If serverless functions are running inside internal virtual private networks (VPNs), attacks such as scanning internal networks and DoS, are not affected to the designated container in which the function is running | Using XML entities makes the environment variable vulnerable to XXE attacks | Leakage of function code and sensitive files (environment variable, /tmp directory, etc.) |
| **A5 — Broken Access Control** | The stateless nature of serverless architecture allows attackers to exploit over-privileged functions to gain unauthorized access to resources | Granting functions access and privileges to unnecessary resources | Impact depends on the compromised resources; leakage of data from cloud storage and database |
| **A6 — Security Misconfiguration** | Misconfigured functions with a long timeout and low concurrency limit allow attackers to perform DoS attacks | Poor patch management; functions with long timeout configuration and low concurrency | Sensitive information leakage, loss of money, DoS, and unauthorized access to cloud resources |
| **A7 — Cross-Site Scripting (XSS)** | In traditional applications, XSS vulnerabilities arrive from databases or reflective inputs, but in serverless applications, they also arrive from sources such as emails, logs, cloud storage, IoT, etc. | Untrusted input used to generate data without proper escaping | User impersonation; access to sensitive data, such as API keys |
| **A8 — Insecure Deserialization** | Dynamic languages (e.g., Python, Node.JS) along with JavaScript Object Notation (JSON), a serialized datatype, allow attackers to perform deserialization attacks | Deserialization vulnerabilities in Python, Node.JS, and JavaScript, etc. | Impact depends on the sensitivity of the application handles; running arbitrary code, data leakage, resource and account control |
| **A9 — Using Components with Known Vulnerabilities** | Serverless functions are used for third-party libraries for execution; vulnerable third-party libraries allow attackers to gain an entry point to serverless applications | Lack of knowledge on component; heavy deployment patterns | Business impact depends on the specification of known deployment vulnerabilities |
| **A10 — Insufficient Logging and Monitoring** | Complex serverless auditing and lack of monitoring and timely response pave the way for various attacks | Insufficient security incident monitoring and auditing | The impact of late security incident identification can be significant |

---

## Threat Catalog

### Data Security

#### Data Breach/Loss

An improperly designed cloud computing environment with multiple clients is at high risk of a data breach because a flaw in one client's application can allow attackers to access other clients' data. Data loss or leakage is highly dependent on cloud architecture and operation.

**Data loss issues include:**
- Data is erased, modified, or decoupled (lost)
- Encryption keys are lost, misplaced, or stolen
- Data are accessed illegally owing to improper authentication, authorization, and access controls
- Data is misused by the CSP

**Countermeasures:**
- Encrypt the data stored in the cloud and the data in transit to protect data integrity
- Implement strong key generation, storage, and management
- Check for data protection both during design and runtime
- Enforce multi-factor authentication

#### Loss of Operational and Security Logs

The loss of operational logs makes it challenging to evaluate operational variables; when no data is available for analysis, the options for solving issues are limited. The loss of security logs poses a risk for managing the information security management program. Loss of security logs may occur in case of storage under-provisioning.

**Countermeasures:**
- Perform secure data backups regularly to recover from data loss
- Deploy data loss prevention (DLP) software to detect potential threats to data
- Enforce appropriate security policies by classifying the data according to sensitivity levels
- Deploy cloud access security brokers (CASBs) that restrict operations such as data distribution over the Internet
- Employ micro-segmentation along with data security tools to apply network micro-segmentation to a few network nodes
- Audit and monitor the privileged accounts to detect and reduce data breaches
- Employ a perimeter firewall to filter the data packets entering and exiting the network

#### Malicious Insiders

Malicious insiders are disgruntled current/former employees, contractors, or other business partners who have had authorized access to cloud resources and could intentionally exceed or misuse that access to compromise the confidentiality, integrity, applicability, or availability of the organization's information.

**Countermeasures:**
- Enforce a strict supply chain management and conduct a comprehensive supplier assessment
- Perform secure data backups regularly to recover from data loss
- Deploy data loss prevention (DLP) software to detect potential threats to data
- Enforce appropriate security policies by classifying the data according to sensitivity levels
- Deploy cloud access security brokers (CASBs)
- Audit and monitor the privileged accounts
- Employ a perimeter firewall

#### Illegal Access to the Cloud Systems

Weak authentication and authorization controls may lead to unlawful access, thereby compromising confidential and critical data stored in the cloud.

**Countermeasures:**
- Enforce and adhere to a robust information security (IS) policy
- Permit clients to audit/review the IS policy and procedures of CSPs

#### Loss of Business Reputation Due to Co-tenant Activities

This threat arises because of the lack of resource and reputational isolation, vulnerabilities in the hypervisors, etc. Resources are shared in the cloud, thus the malicious activity of one co-tenant might affect the reputation of the other, resulting in poor service delivery, data loss, etc., that bring down the reputation of the organization.

**Countermeasures:**
- Choose a well-known and efficient CSP to reduce risk and ensure isolation of resources
- Assess the virtualization and isolation techniques used by the CSP
- Assess the risks involved in a multi-tenant architecture
- CSPs must segregate the functions among tenants

#### Loss of Encryption Keys

The loss of encryption keys required for secure communication or systems access provides potential attackers with the possibility to get unauthorized assets.

**Countermeasures:**
- Do not store the encryption keys alongside the encrypted data
- Use strong algorithms, such as the advanced encryption standard (AES) and Rivest–Shamir–Adleman (RSA), to generate keys
- Restrict access to the key stores and implement policies such as role separation to control and manage access to the key stores
- Enforce a secure backup and recovery plan for the encryption keys
- Do not re-use keys for different purposes
- Use a hardware security module (HSM) to secure the encryption keys

---

### Operational Security

#### Theft of Computer Equipment

The theft of equipment may occur owing to inadequate controls on physical parameters, such as smart card access at entry, which may lead to loss of physical equipment and sensitive data.

**Countermeasures:**
- Enforce physical security measures, such as hiring security guards, closed-circuit television (CCTV) coverage, alarms, identity cards, and proper fencing
- Assess the security regularly to make certain changes and maintain the latest physical security measures
- Control physical access with the implementation of different sophisticated technologies such as biometric entries
- Implement intrusion alarm systems to prevent intrusion and alert the security team at the earliest
- Ensure that the server room is always locked and only authorized personnel are present to enter the room
- Use rack-mounted servers to enhance physical security by making it impossible to move
- Secure the backup devices and drives in an off-site location

#### Loss or Modification of Backup Data

Attackers might use vulnerabilities, such as SQL injection and insecure user behavior (e.g., storing or reusing passwords) to gain illegal access to the data backups in the cloud. After gaining access, attackers might delete or modify the data stored in the databases.

**Countermeasures:**
- Use appropriate data restoration procedures or tools to retrieve lost data
- Avoid relying on one storage method or medium for backup; instead deploy the 3-2-1 model

#### Improper Data Handling and Disposal

The data and configuration data, along with the hard disk and other storage devices, are often shared among multiple clients in cloud computing. In a multi-tenant environment, it is difficult to ascertain the actual deletion of data, as data may not be truly wiped because:
- Multiple copies of data are stored, even if they are deleted
- The disk to be destroyed might also contain the data of other clients
- Multi-tenancy and reuse of hardware resources in the cloud keeps client data at risk

**Countermeasures:**
- Use VPNs to secure client data and ensure that the data are completely removed from the primary servers along with all the backup devices after deletion
- Encrypt the data to make the data unreadable even if the traces are accessed after deletion
- Set up a data storage period to hold and dispose the data securely from all the backup devices after obsolescence
- Apply a data destruction process corresponding with the device and disposal technique used
- Enforce a strategy to perform data sanitization and standardize the procedure
- Document all the steps for data sanitization to develop a robust audit trail and validate the entire destruction process with the clients

#### Cloud Service Misuse — Abuse and Nefarious Use of Cloud Services

The presence of weak registration systems in the cloud-computing environment may allow attackers to create anonymous accounts to access cloud services and perpetrate various attacks, such as password and critical cracking, building rainbow tables, CAPTCHA-solving farms, launching dynamic attack points, hosting exploits on cloud platforms, hosting malicious data, Botnet command or control, and DDoS.

**Countermeasures:**
- Implement a robust registration and validation process
- Monitor client traffic for malicious activities
- Monitor and block malicious networks on public blacklists
- Utilize an advanced credit-card fraud monitoring and coordination system for cloud payment services
- Use a high-security cloud service provider (CSP) that constantly works to prevent cloud service abuse
- Isolate users on the same cloud using per-tenant firewalls

#### Undertaking Malicious Probes or Scans

Malicious probes or scans are conducted to collect sensitive information that may lead to loss of confidentiality and integrity, and availability of services and data.

**Countermeasures:**
- Deploy various security mechanisms such as firewalls and intrusion detection systems
- Do not place the hypervisor and VMs on the same network
- Separate hypervisor management and remote-access traffic by creating a VLAN
- Block the replies of ping and traceroute from the network where the hypervisor is running
- Configure the management interfaces of the hypervisor properly

#### Insufficient Due Diligence

Ignorance of the CSP's cloud environment poses risks in operational responsibilities such as security, encryption, incident response, and more such problems as contractual issues, design, and architectural issues.

**Countermeasures:**
- Organizations that intend to move to a cloud must extensively research the risks and CSP due diligence and possible capable resources
- Ensure that all the employees are trained regarding security standards and resource maintenance
- Ensure that the CSP maintains an incident response plan (IRP) by employing appropriate teams for implementing corresponding security measures during any incident
- Maintain proper communication with the CSP regarding disaster recovery plans, encryption strategies, and security policies
- Reinforce stringent security policies to be followed in governance with the top-level management of the company

---

### Network Security

#### Modifying Network Traffic

In the cloud, the network traffic may be altered owing to flaws during provisioning or de-provisioning networks, or vulnerabilities in communication encryption. Modification of network traffic may cause loss, alteration, or theft of confidential data and communications.

**Countermeasure:** Perform network traffic analysis using special tools to find abnormalities, if any.

#### Management Interface Compromise

Customer management interfaces of cloud providers facilitate access to a large number of resources over the Internet. This enhances security risks, particularly when combined with multiple-access and web browser vulnerabilities. Management interface compromise arises from improper configuration, system and application vulnerabilities, remote access to the management interface, etc.

**Countermeasures:**
- Keep memory, storage, and network access isolated
- Use secure protocols to mitigate threats related to remote access
- Regularly update patches to prevent web browser vulnerabilities
- Deploy a dedicated virtual local area network (VLAN) for managerial-level interfaces isolated from the enterprise network
- Ensure stringent security measures and focus on the interfaces that require public access through untrusted networks utilizing jump servers

#### Authentication Attacks

Weak authentication mechanisms (weak passwords, password re-use, etc.) and the inherent limitations of one-factor authentication methods allow attackers to gain unauthorized access to cloud computing systems.

**Countermeasures:**
- Implement strong password policies to keep passwords secure
- Enforce two-factor authentication where required
- Employ IP whitelisting to thwart unauthorized access by controlling and limiting access
- Use the principle of least privilege to apply minimum user rights for accessing specific resources based on roles
- Enable a robust identity and access management (IAM) to manage the access of the users to the cloud resources

#### VM-Level Attacks

Cloud computing extensively uses virtualization technologies offered by several vendors, including VMware, Xen, Virtual Box, and vSphere. Threats to these technologies arise from vulnerabilities in the hypervisors.

**Countermeasures:**
- Employ intrusion detection/prevention systems (IDS/IPS) and implement a firewall to mitigate known VM-level attacks
- Utilize hypervisors that are highly configured and updated as well as sandboxes around the hypervisors to protect against VM-level attacks
- Utilize the High Assurance Platform (HAP), which offers a high level of virtual machine isolation
- Ensure that no valid VM user shares hardware with other users

#### Hijacking Accounts

A highly critical threat to organizations is the compromise of employee accounts on the cloud. If an attacker gains access to the cloud by compromising a user account, they can gain access to all information stored on the cloud servers without leaving any trace.

**Countermeasures:**
- Grant only minimal access privileges to user accounts
- Implement defense-in-depth strategies and install identity and access management (IAM) solutions
- Encrypt and store sensitive information on cloud servers
- Implement strong authentication mechanisms, such as multi-factor authentication
- Remove the credentials and user accounts that are no longer required
- Detect and withdraw unnecessary access to highly sensitive information
- Control access to the cloud resources by third parties
- Implement cloud tokenization to ensure that only authorized users gain access
- Ensure that a password manager is used to create and manage passwords for all the user accounts

---

### Governance and Legal Risks

#### Lock-in

Lock-in reflects the inability of the client to migrate from one CSP to another or in-house systems owing to the lack of tools, procedures, standard data formats, applications, and service portability. This threat is related to inappropriate CSP selection, incomplete and non-transparent terms of use, lack of standard mechanisms, etc.

**Countermeasures:**
- Using a standardized cloud API could be beneficial
- Employ a multi-cloud or hybrid cloud strategy instead of relying on a single CSP
- Design portable and loosely coupled applications
- Implement DevOps tools to avoid the risks caused by proprietary configurations
- Establish a clear exit strategy before signing the initial agreement

#### Licensing Risks

The organization may incur a substantial licensing fee if the CSP charges the software deployed in the cloud on a per-instance basis. The organization should always retain ownership over its software assets located in the cloud provider environment.

**Countermeasures:**
- Review the current licensing state of the CSP to develop effective licensing and determine the overall costs
- Use one centralized platform to manage the costs, licensing use, etc.
- Eliminate the cloud resources that are not used and connected

#### Risks from Changes of Jurisdiction

Clouds may store the customer data in multiple jurisdictions, of which some may be high risk. Local authorities in high-risk countries (e.g., countries without the rule of law, with an unpredictable legal framework and enforcement or autocratic police states) could raid data centers; the data or information system of the client could be subjected to enforced disclosure or seizure.

**Countermeasure:** Gain insight about the jurisdictions under which data may be stored and processed, and assess the corresponding risks, if any.

#### Subpoena and E-Discovery

Customer data and services are subjected to a cease request from authorities or third parties. This threat occurs owing to improper resource isolation, data storage in multiple jurisdictions, and lack of insight on jurisdictions.

**Countermeasures:**
- Carefully select the CSP and ensure proper security is provided
- Thoroughly review the service agreement (addresses records management, accessibility, customer support, legal policies, accountability, confidentiality, length of the agreement, termination procedures, etc.)
- Execute a coordinated eDiscovery plan
- Contemplate an exit strategy

#### Economic Denial of Sustainability (EDoS)

The payment method in a cloud system is **"No use, no bill"** — customers make requests, and the CSP charges them according to the recorded data, the duration of resource requests in the network, and the amount of CPU cycles consumed. Economic denial of service destroys financial resources; in the worst case, this could lead to customer bankruptcy or other serious economic impact. If an attacker engages a cloud server with a malicious code that consumes much computational power and storage, the legitimate account holder is charged until the primary cause of CPU usage is detected.

**Countermeasure:** Use a reactive/on-demand, in-cloud EDoS mitigation service (scrubber service) to mitigate application-layer and network-layer DDoS attacks, making use of the client-puzzle approach.

#### Loss of Governance

In using cloud infrastructure, customers bestow control to CSPs regarding issues that could affect security. Furthermore, CSPs may not provide evidence of their compliance with the requirements, outsourcing cloud management to third parties, and does not permit audit by the client.

**Countermeasures:**
- Workout persistent and careful efforts for the execution of SLAs
- Enforce strict governance rules to protect sensitive data and improve performance
- Maintain a unified governance policy for on-premises and cloud operations
- Employ automation to verify compliance with the governance policy

#### Compliance Risks

Organizations that seek to obtain compliance with standards and laws may be at risk if the CSP cannot provide evidence of their compliance with the requirements, is outsourcing cloud management to third parties, and does not permit audit by the client. Compliance risks arise from differences over industry-standard assessments.

**Countermeasures:**
- Cloud providers should ensure that client data is not compromised
- Review the internal audit processes of cloud providers

#### Unsynchronized System Clocks

The failure of synchronizing clocks at the end systems can affect the working of automated tasks. For example, if the cloud computing devices do not have synchronized or matched times, then attackers can analyze timestamp inaccuracy constitutes the network administrator unable to analyze the log files for any malicious activity accurately.

**Countermeasures:**
- Use clock synchronization solutions, such as a network time protocol (NTP)
- Install a time server within the organization firewall to minimize threats from the outside and maximize the time accuracy on the network
- A network time system can also be used to synchronize clocks with an enterprise network server

#### Inadequate Infrastructure Design and Planning

An agreement between the CSP and customer states the quality of service that the CSP offers, such as downtime, physical and network-based redundancies, standard data backup, response times, and availability periods. At times, CSPs may not satisfy the rapid rise in demand owing to a shortage of computing resources and/or poor network design (e.g., traffic flows through a single point, even though the necessary hardware is available), giving rise to unacceptable network latency or inability to meet agreed service levels.

**Countermeasures:**
- Forecast the demand and accordingly prepare sufficient infrastructure
- Rely on workloads' reliability and uptime requirements to plan the usage of the cloud

---

### Cloud Attacks

#### Service Hijacking using Social Engineering

**Attack Method:** In account or service hijacking, an attacker steals the credentials of a CSP or a client by phishing, pharming, social engineering, and exploitation of software vulnerabilities. Using the stolen credentials, the attacker gains access to the cloud computing services and compromises data confidentiality, integrity, and availability.

**Example Attack Flow:**
1. Attacker creates a fake cloud service login page and sends a malicious link to the cloud service user
2. The user clicks on it and enters login credentials, failing to notice it is a fake login page
3. When the user hits enter, the page automatically redirects them to the original cloud service login page
4. Attacker receives login credentials, uses them to log into the cloud service and perform malicious activity

**Countermeasures:**
- Do not share account credentials between users and services
- Implement a robust two-factor or multi-factor authentication mechanism wherever possible
- Train the staff to recognize social engineering attacks
- Strictly follow the security policies framed
- Encrypt the data before transmitting them over the Internet
- Use "least privilege" principles to restrict access to services

#### Service Hijacking using Network Sniffing

**Attack Method:** Network sniffing involves the interception and monitoring of network traffic between two cloud nodes. Unencrypted sensitive data (e.g., login credentials) during transmission across a network are at high risk. Attackers use packet sniffers (e.g., Wireshark) to capture sensitive data, such as the universal description discovery and integrity (UDDI), simple object access protocol (SOAP), and web service description language (WSDL) files.

**Countermeasures:**
- Encrypt sensitive data over the network
- Encrypt sensitive data in configuration files
- Detect network interface controllers (NICs) running in promiscuous mode
- Ensure that web traffic containing credentials is encrypted with SSL/TLS

#### Side-Channel Attacks (Cross-guest VM Breaches)

**Attack Method:** Attackers can compromise the cloud by placing a malicious virtual machine near a target cloud server and then launch a side-channel attack. A side-channel attack is one in which the attacker exploits vulnerabilities in the shared physical host as the victim's VM and takes advantage of the shared physical resources (processor cache) to steal data (cryptographic key/plain text secrets) to steal the victim's credentials.

Side-channel attacks can be implemented by any co-resident user due to vulnerabilities in shared technology resources. The side-channel attack techniques include:
1. Timing Attack
2. Data Remanence
3. Acoustic Cryptanalysis
4. Power Monitoring Attack
5. Differential Fault Analysis

**Countermeasures:**
- Implement a virtual firewall in the cloud server back-end of the cloud computing to prevent the attacker from placing malicious VMs
- Implement random encryption and decryption (encrypts data using RSA, 3DES, AES algorithms)
- Lockdown OS images and application instances to prevent compromising vectors that might provide access
- Check for repeated access attempts to local memory and any hypervisor or shared hardware cache by tuning and collecting local process monitoring data and logs for cloud systems
- Code the applications and OS components so that they access shared resources (memory cache) in a consistent and predictable way

#### Wrapping Attack

**Attack Method:** A wrapping attack is performed during the translation of the SOAP message in the TLS layer where attackers duplicate the body of the message and send it to the server as a legitimate user.

When users send a request from their VM through a browser, the request is generated and exchanged with the browser during the passage of the message. The SOAP message is generated and exchanged with the browser during the passage of the message. Before the message passing occurs, the browser needs to sign the XML document and canonicalize it. Additionally, it should append the signature values to the document.

In a wrapping attack, adversary deception occurs during the translation of the SOAP message in the TLS. The attacker duplicates the body of the message and sends it to the server as a legitimate user. The server checks the authentication through the signature value (which is also duplicated) and verifies its integrity. As a result, the adversary can intrude in the cloud and run malicious code to interrupt the usual functioning of the cloud servers.

**Countermeasures:**
- Use XML schema validation to detect SOAP messages
- Apply authenticated encryption in the XML encryption specification
- Improve the interface between signature verification and business logic functions
- Ensure that users specify the SOAP body and headers to be signed by implementing the **WS-SecurityPolicy "SignedParts"** policy
- Use the **CryptoCoverageChecker** interceptor to specify the XPath expression related to the element that should be signed or encrypted

#### Man-in-the-Cloud (MITC) Attack

**Attack Method:** MITC attacks are an advanced version of MITM attacks. In MITM attacks, an attacker uses an exploit that intercepts and manipulates the communication between two parties, while MITC attacks are carried out by abusing cloud file synchronization services (such as Google Drive or Dropbox) for data compromise, command and control (C&C), data exfiltration, and remote access. Synchronization tokens are used for application authentication in the cloud but cannot distinguish malicious traffic from normal traffic. Attackers abuse this weakness in cloud accounts to perform MITC attacks.

**Attack Flow (Fig 19.34):**
1. Attacker tricks the victim into installing malicious code
2. Victim installs the malware
3. Malware plants the attacker's synchronization token on the victim's drive
4. Victim's Drive syncs with the attacker's account
5. Attacker steals the victim's synchronization token
6. Attacker uses the stolen token to gain access to the victim's files
7. Attacker restores the malicious token with the original synchronized token of the victim, returning the Drive application to its original state and staying undetected

**Countermeasures:**
- Use an email security gateway to detect the social engineering attacks that can lead to MITCs
- Hardening the policies of token expiration can prevent this kind of attack
- Use efficient antivirus software that can detect and delete malware
- Implement cloud access security broker (CASB) to monitor cloud traffic for detection of anomalies with the generated instances
- Monitor employee activities to detect any significant signs of cloud synchronization token abuses
- Encrypt the data stored on the cloud and ensure that encryption keys are not stored within the same cloud service
- Implement two-factor authentication

#### Cloud Hopper Attack

**Attack Method:** Cloud Hopper attacks are triggered at managed service providers (MSPs) and their users. Attackers initiate spear-phishing emails with custom-made malware to compromise accounts of staff members or cloud service firms to obtain confidential information.

Once successfully infiltrated:
- Attackers gain remote access to intellectual property and critical information of the target MSP and its global users/customers
- Attackers also move laterally in the network from one system in the account environment to gain access to sensitive data pertaining to industrial entities such as manufacturing, government bodies, healthcare, and finance
- Attackers can also use PowerShell and PowSploit command-based scripting for reconnaissance and information gathering
- Attackers breach security mechanisms impersonating a valid service provider and gain complete access to corporate data of the enterprise and connected customers

**Countermeasures:**
- Implement multi-factor authentication to prevent compromise of credentials
- Ensure mutual co-ordination between customers and CSPs in case of abnormal incidents or activities
- Ensure customers are aware of and follow the cloud service policies
- Use data categorization to reduce the impact of the attack and defend against any data breach
- Utilize jump servers to enhance security and prevent cloud hopper attacks

#### Cloud Cryptojacking

**Attack Method:** Cryptojacking is the unauthorized use of the victim's computer to stealthily mine digital currency. Cryptojacking attacks are highly lucrative, involving both external attackers and internal rogue insiders. Attackers leverage attack vectors like cloud misconfigurations, compromised websites, and client or server-side vulnerabilities.

**Attack Steps:**
1. Attacker compromises the cloud service by embedding a malicious crypto-mining script
2. When the victim connects to the compromised cloud service, the crypto-mining script gets executed automatically
3. The victim naively starts mining the cryptocurrency on behalf of the attacker and adds a new block to the blockchain
4. For each new block added to the blockchain, the attacker gets a reward in the form of cryptocurrency coins illicitly

**Countermeasures:**
- Implement a strong password policy
- Always preserve three different copies of the data in different places and one copy off-site
- Ensure to patch the webservers and devices regularly
- Use encrypted SSH key pairs instead of passwords for securing access to cloud servers
- Implement CoinBlocker URL and IP Blacklist/blackhole in the firewall
- Employ real-time monitoring of the web page document object model (DOM) and JavaScript environments for detecting and mitigating malicious activities at an early stage
- Use the latest antivirus, anti-malware, and adblocker tools in the cloud
- Implement browser extensions for scanning and terminating scripts similar to the CoinHive's miner script
- Employ endpoint security management technology to detect any rogue applications on the devices
- Review all third-party components used by the company's websites
- Employ advanced network monitoring tools that are capable of identifying CPU resource misuse, mining, and sniffing activities
- Never neglect sudden price surges in the cloud resource utilization bills because most crypto miners utilize random cloud resources for attack deployment
- Ensure that all the cloud instances and services are successfully terminated at the end of the day; else, they might become an entry point for crypto jackers

#### Cloudborne Attack

**Attack Method:** Cloudborne is a vulnerability residing in a bare-metal cloud server that enables attackers to implant malicious backdoor in its firmware. The installed backdoor can persist even if the server is reallocated to new clients or businesses that use it as an IaaS. Physical servers are not confined to one cloud and can be moved from one client to another. During the reclamation process, if the firmware re-flash (factory default setting, complete erase of memory, etc.) is not properly implemented, the backdoors can stay active on the firmware and travel along the server.

Attackers exploit vulnerabilities in super-micro hardware to overwrite the firmware in the baseboard management control (BMC) of a bare-metal server that is used for remote management activities, such as provisioning, reinstalling the operating system, and troubleshooting via the intelligent platform management interface (IPMI) without physical access. As the BMC has the power to control the servers remotely and provision the system to the new customers, attackers choose it as a primary target. Then, the malicious backdoors allow attackers to directly access the hardware and bypass the security mechanisms to perform activities such as monitoring new customer's activities, disabling the application/server, and intercepting the data.

**Countermeasures:**
- CSPs should keep the firmware up-to-date
- Sanitize the server firmware before it is assigned to new customers
- Validate the server for implants and backdoors before deploying
- Regularly check for firmware vulnerabilities
- CSPs should verify whether the physical hardware has been tampered with before delivery

#### Instance Metadata Service (IMDS) Attack

**Attack Method:** An instance metadata service (IMDS) provides information about an instance, its associated network, and the software configured to run the instance. IMDS also generates credentials for roles associated with an instance. Based on the assigned role or policy, the software configured on the instance can also access the resources on the cloud storage.

Attackers perform IMDS attacks by exploiting a zero-day vulnerability on the target application server or by using information leaked via a reverse proxy implemented by the administrators. The main intention of attackers performing an IMDS attack is to gain unauthorized access to the network resources by compromising instances.

**Attack Flow:**
1. Attacker exploits a zero-day vulnerability or a reverse proxy on the target application server
2. Attacker then compromises the cloud instance running on the server and acquires metadata of the instance
3. Next, the attacker uses the obtained credentials to gain access to the cloud resources

**Countermeasures:**
- Use IMDSv2 instead of IMDSv1
- Turn off IMDS when not required
- Roles should not be assigned to an instance if not required; if required, assign the least privileges to the roles
- Restrict the IMDS access of suspected users

#### Cache Poisoned Denial of Service (CPDoS) / CDN Cache Poisoning

**Attack Method:** In a CPDoS or CDN cache poisoning attack, attackers create malformed or oversized HTTP requests to trick the origin web server into responding with malicious or error content, which is cached at the CDN servers, making it available to legitimate users, resulting in a DoS attack on the target network.

**Attack Steps:**
1. An attacker requests a resource from the target web server by submitting a request containing a malicious HTTP header
2. If the intermediary CDN server does not have a cache of the requested webpage/resource, the request is forwarded to the origin web server which returns an error because the request is malicious
3. The error page is cached instead of the genuine one at the CDN server
4. Now, instead of the original web page, users receive a cached error page such as "404 Not Found" whenever they attempt to access the resource
5. The CDN server also broadcasts the same error page across other connected users, making legitimate services unreachable to them

**Countermeasures:**
- Configure the CDN to avoid the caching of HTTP error pages
- Implement a web application firewall (WAF)
- Monitor and eliminate error pages from the cache

#### Cloud Snooper Attack

**Attack Method:** Cloud snooper attacks are triggered at AWS security groups (SGs) to compromise the target server and extract sensitive data stealthily. Attackers exploit a weakness in SGs, which are intended to allow only traffic with destination ports 80 or 443. Attackers install rootkits either by exploiting weaknesses in traffic filters, supply-chain attacks, or brute-forcing SSH. Attackers transmit their command and control (C2) packets masquerading as legitimate traffic. The installed rootkit then intercepts the packets and redirects the commands to the backdoor Trojan. The Trojan executes the malicious activities according to the C2 commands received from the remote machine.

**Attack Steps:**
1. Attackers send specially created C2 packets along with normal traffic with destination ports 80 and 443, fooling the perimeter firewall
2. The firewall verifies all incoming packets and allows them to pass as the packets contain 80 and 443 as the destination ports
3. Now, the listener in the rootkit intercepts traffic towards the server and recreates the packets with the source ports 1010, 1020, 6060, 7070, 8080, or 9999
4. The listener then transmits those packets to the backdoor installed by the rootkit
5. The backdoor Trojan now performs actions according to the C2 commands and sends the data back to the rootkit after collecting from the target server

**Countermeasures:**
- Ensure that the network traffic is regularly analyzed
- Ensure that the web servers are regularly patched
- Employ a layered security model

#### Golden SAML Attack

**Attack Method:** Golden Security Assertion Markup Language (SAML) attacks are implemented to target identity providers on cloud networks such as the Active Directory Federation Service (ADFS), which utilizes the SAML protocol for the authentication and authorization of users. Attackers initially gain administrative access to the identity provider's user profile and exploit token signing certificates to generate forged SAML tokens or responses by manipulating the SAML assertions.

**Attack Scenario:**
1. Attacker gains access to the ADFS server (identity provider) and steals the certificate and encryption key that signs the assertion
2. When a user attempts to access the required service, the service provider redirects the request to the identity provider
3. The attacker intercepts the redirect request and sends back the SAML response with forged assertion values using the stolen keys
4. Then, the service provider allows the attacker to access federated services associated with the target user account

**Countermeasures:**
- Constantly monitor user activities
- Utilize multi-factor authentication and strong passwords
- Implement least-privilege access
- Analyze the environment for indications of an attack
- Update the certificates in a timely manner

#### Living Off the Cloud Attack (LotC)

**Attack Method:** Living Off the Cloud (LotC) is a modern evolution of the "living off the land" attack, in which attackers target victim's legitimate tools and cloud services to carry out malicious activities such as data exfiltration, allowing them to reside in the victim's environment without leaving any trace or artifacts.

**How the LotC Attack Works:**
1. First, an attacker gains initial access to the system through methods such as phishing emails, exploiting vulnerabilities, or using previously stolen credentials
2. The attacker then performs lateral movements within the network by leveraging legitimate tools within the victim system, such as CMD, PowerShell, and Certutil
3. Next, the attacker delivers malicious payloads to the victim's device by utilizing cloud storage services such as Dropbox and Google Drive
4. The attacker creates covert channels or C2 for communication using the victim's cloud services such as Ngrok
5. Now, the attacker performs various activities such as hosting malware on cloud storage, sending phishing links from trusted domains, and performing data exfiltration
6. Finally, the attacker uses the victim's SaaS or IaaS applications to blend in with legitimate cloud traffic, thereby maintaining long-term access without detection

**Countermeasures:**
- Use a cloud-native single-pass architecture in secure access software to inspect and secure traffic in real time
- Implement zero-trust security to limit unauthorized access to resources
- Allow only corporate instances of Dropbox or restrict the uploading of files with sensitive data
- Regularly train employees to avoid clicking, visiting, downloading, or replying to anything suspicious or unauthorized
- Enable detailed logging of all activities within cloud environments and endpoints
- Use machine learning and behavioral analytics to detect unusual patterns indicating malicious use of legitimate apps
- Apply application whitelisting to restrict the execution of unauthorized applications and scripts
- Employ network segmentation to limit lateral movement within the network
- Employ MFA for accessing sensitive systems and cloud services
- Use RBAC to ensure that users have the minimum permissions necessary

#### Session Hijacking using Cross-Site Scripting (XSS)

Attackers implement XSS to steal cookies used in the user authentication process. This involves injecting a website with malicious code which is subsequently used by the browser. Using the stolen cookies, attackers exploit active computer sessions, thereby gaining unauthorized access to data.

**Countermeasure:** Using secure socket layers (SSL), firewalls, antiviruses, and code scanners can safeguard a cloud from session hijacking.

#### Session Hijacking using Session Riding

Attackers exploit websites by engaging in cross-site request forgeries to transmit unauthorized commands. In session riding, attackers "ride" an active computer session by sending an email or tricking users into visiting a malicious webpage during log-in to an actual site. When users click the malicious link, the website executes the request as if the user had already authenticated it. Commands used include modifying or deleting user data, performing online transactions, resetting passwords, etc.

**Countermeasures:**
- Do not allow your browser and websites to save login details
- Check the HTTP referrer header and, when processing a POST, ignore URL parameters

#### Domain Name System (DNS) Attacks

DNS attacks are performed to obtain authentication credentials from internet users.

**Types of DNS Attacks:**
- **DNS Poisoning** — diverting users to a spoofed website by poisoning the DNS server or the DNS cache on the user's system
- **Cybersquatting** — conducting phishing scams by registering a domain name that is similar to a CSP
- **Domain Hijacking** — stealing a CSP domain name
- **Domain Snipping** — registering an elapsed domain name

**Countermeasures:**
- Use filtering techniques to sanitize the user input
- Validate input length, range, format, and type
- Regularly update and patch servers and applications
- Use database monitoring technologies and intrusion prevention systems (IPS)
- Implement a cloud-based web application firewall

#### Cryptanalysis Attacks

Insecure or obsolete encryption makes cloud services susceptible to cryptanalysis. Data present in the cloud may be encrypted to prevent them from being read if accessed by malicious users. However, critical flaws in cryptographic algorithm implementations (e.g., weak random number generation) may turn strong encryption weak or broken.

**Countermeasures:**
- Use random number generators that generate cryptographically secure random numbers to provide robustness to cryptographic material like SSH keys and DNSSECs
- Do not use faulty cryptographic algorithms
- Use the latest and strongest encryption procedures which include salting, hashing, etc.

#### DoS and DDoS Attacks

Performing DoS attacks on CSPs can leave tenants without access to their accounts. In the cloud infrastructure, multiple tenants share CPU, memory, disk space, bandwidth, etc. If attackers gain access to the cloud, they generate false data that could be resource requests or a type of code that can run in applications of legitimate users.

If a DoS attack is launched via a **botnet** (a network of compromised machines), then it is a DDoS attack.

**Countermeasures:**
- Follow the least privilege concept for the users connecting to the server
- Install IDS in both physical and virtual machines of the cloud to mitigate DoS and DDoS attacks

#### Man-in-the-Browser Attack

Attacks target a user's web-browser by injecting sophisticated malware (e.g., bots) that allow attackers to monitor information being shared between the user's browser and cloud application. The injected code exfiltrates the user's login credentials, such as username and passwords, to the attackers.

**Countermeasures:**
- Limit access to the cloud services to safeguard the network against illegitimate access
- Integrate the cloud-based solution with controlled intrusion detection systems to detect and notify of abnormal user activities
- Limit IP address range and offer services only via VPNs

#### Cloud Malware Injection Attack

In cloud malware injection attacks, attackers install malicious service implementations or virtual machines into the cloud services that run as SaaS, PaaS, or IaaS. Once the cloud is successfully abused, the cloud user is redirected to the attackers' website, where the attackers can perform activities such as eavesdropping communication and stealing and modifying data.

#### Multi-Cloud Attack

In multi-cloud attacks, attackers leverage vulnerabilities across multiple cloud service providers (CSPs) that an organization uses. This includes exploiting misconfigurations, weak access controls, or compromised credentials to gain unauthorized access to different cloud environments. Once attackers successfully gain access, they move laterally between cloud services by exploiting inter-cloud APIs or network bridges.

**Countermeasures:**
- Use secure APIs and encrypted channels for communication between different cloud services
- Ensure that access control models are standardized across all cloud providers to prevent potential security gaps
- Implement an additional security layer beyond passwords, requiring two or more verification factors
- Synchronize security policies using automated tools to apply uniform settings to all clouds
- Conduct regular security audits and continuous monitoring across all cloud environments

#### Metadata Spoofing Attack

Metadata spoofing is a process of changing or modifying service metadata written in the web service definition language (WSDL) file, where the information regarding service instances is stored. Once the manipulated file is successfully deployed, cloud users are redirected to unknown places, similar to the process of DNS spoofing.

**Countermeasures:**
- Encrypt and store application and service details on the cloud
- Implement hash-based integrity checking to mitigate spoofing attacks
- Deactivate metadata services that are not required, along with unsafe metadata versions
- Enforce host-based firewalls to restrict the instance metadata API access

---

## Cloud Malware

### Cuttlefish Zero-Click Malware

Source: https://www.darkreading.com

Cuttlefish is a packet-sniffing malware that masquerades as legitimate software by exploiting vulnerabilities in SOHO and enterprise routers, aiming to covertly steal cloud authentication data. Once infiltrated, it spreads by deploying a bash script to collect host-based data for sending it to a command-and-control (C2) server in the cloud. It also downloads and executes a malicious binary (payload) made for all customized architectures found in SOHO operating systems.

The malware monitors all traffic through the device and only activates when it identifies specific activities. When the traffic is directed toward a public IP address, it activates a cloud sniffer to steal credentials under certain conditions.

**Additional Cloud Malware:**
- Denonia
- LemonDuck
- RansomCloud
- DBatLoader/ModiLoader
- Goldbackdoor
