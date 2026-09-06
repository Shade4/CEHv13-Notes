# 01 — Cloud Computing Concepts

> **CEH v13 Module 19 | Objective 01: Summarize Cloud Computing Concepts**

---

## Introduction

Cloud computing is the **on-demand delivery of IT capabilities** — where IT infrastructure and applications are provided to subscribers as a metered service over a network. Examples of cloud solutions include Gmail, Facebook, Dropbox, and Salesforce.com.

### Characteristics of Cloud Computing

| Characteristic | Description |
|----------------|-------------|
| **On-demand self-service** | Provision computing power, storage, and network without needing service providers |
| **Distributed storage** | Better scalability, availability, and reliability; distributed storage can raise security and compliance concerns |
| **Rapid elasticity** | Instant provisioning of capabilities to rapidly scale up or down |
| **Automated management** | Minimizes user involvement; speeds up the process and reduces risk of human error |
| **Broad network access** | Resources available over the network via laptops, mobile phones, PDAs |
| **Resource pooling** | CSP pools all resources to serve multiple customers in the multi-tenant environment; physical and virtual resources dynamically assigned and reassigned as demanded |
| **Measured service** | Subscribers pay by monthly subscription or according to usage of resources (storage levels, processing power, bandwidth); metering |
| **Virtualization technology** | Rapid scaling of resources in a way non-virtualized environments cannot achieve |

### Limitations of Cloud Computing

- Limited control and flexibility of organizations
- Proneness to outages and other technical issues
- Security, privacy, and compliance issues
- Contracts and lock-ins
- Dependence on network connections
- Potential vulnerability to attacks (every component online)
- Difficulty migrating from one service provider to another

---

## Types of Cloud Computing Services

Cloud services are divided broadly into the following categories:

### Infrastructure-as-a-Service (IaaS)

Enables subscribers to use on-demand fundamental IT resources (computing power, virtualization, data storage, network). The CSP is responsible for the underlying cloud computing infrastructure (human capital, hardware, others).

**Examples:** Amazon EC2, Microsoft OneDrive, Rackspace

**Advantages:** Dynamic infrastructure scaling, guaranteed uptime, automation of administrative tasks, Elastic Load Balancing (ELB), policy-based services, global accessibility

**Disadvantages:** Software security is at high risk (3rd-party providers more prone to attacks), performance issues and slow connection speeds, difficulty switching between IaaS vendors

---

### Platform-as-a-Service (PaaS)

Allows development of applications and services. Subscribers don't need to buy and manage the software and infrastructure underneath it but have authority over deployed applications and hosting environment configurations. Offers development tools, configuration management, and deployment platforms on-demand.

**Examples:** Google App Engine, Salesforce, Microsoft Azure

**Advantages:** Simplified deployment, prebuilt business functionality, lower security risk compared to IaaS, instant community, pay-per-use model, scalability

**Disadvantages:** Vendor lock-in, data privacy, integration with the rest of the system applications

---

### Software-as-a-Service (SaaS)

Offers application software to subscribers on-demand over the Internet. Provider charges for the service on a pay-per-use basis, by subscription, by advertising, or by sharing among multiple users.

**Examples:** web-based office applications (Google Docs, Calendar), Salesforce CRM, Freshbooks

**Advantages:** Low cost, easy administration, global accessibility, high compatibility (no specialized hardware or software required)

**Disadvantages:** Increased attack surfaces and vulnerabilities, unknown risk profile, no customization to business needs, insecure APIs, vulnerable to account hijacking attacks

---

### Identity-as-a-Service (IDaaS)

Provides authentication services to the subscribed enterprises; managed by a 3rd-party vendor to provide identity and access management services. Provides services such as Single Sign-On (SSO), Multi-Factor Authentication (MFA), Identity Governance and Administration (IGA), access management, and intelligence collection.

**Examples:** OneLogin, Centrify Identity Services, Microsoft Azure Active Directory, Okta

**Advantages:** Low cost, improved security, simplified compliance, reduced time, central management of user accounts

**Disadvantages:** Single server failure may disrupt service or create redundancy on other authentication servers, vulnerable to account hijacking attacks

---

### Container-as-a-Service (CaaS)

Provides containers and clusters as a service to subscribers. Provides services such as virtualization of container engines, management of containers, applications, and clusters through a web portal or an API.

**Examples:** Amazon EC2, Google Kubernetes Engine (GKE)

**Advantages:** Streamlined development of containerized applications, pay-per-resource, increased quality, portable and reliable application development, low cost, few resources, crash of one container doesn't affect others, improved security, improved patch management, improved response to bugs, high scalability, streamlined development

**Disadvantages:** High operational overhead, platform deployment is the developer's responsibility

---

### Function-as-a-Service (FaaS)

Provides a platform for developing, running, and managing application functionalities without the complexity of building and maintaining necessary infrastructure (serverless architecture). Mostly used while developing applications for microservices; processes data services for IoT connected devices, mobile applications, and batch-and-stream processing.

**Examples:** AWS Lambda, Google Cloud Functions, Microsoft Azure Functions, Oracle Functions

**Advantages:** Pay-per-use, low cost, efficient security updates, easy deployment, high scalability

**Disadvantages:** High latency, memory limitations, monitoring and debugging limitations, unstable tools and frameworks, vendor lock-in

---

### Anything-as-a-Service (XaaS)

A cloud-computing and remote-access service that offers anything as a service based on the user's demand. The service may include digital products such as tools, applications, and technologies, as well as types of services such as food, transportation, and medical consultations.

**Examples:** NetApp, AWS Elastic Beanstalk, Heroku, Apache Stratos

**Advantages:** Highly scalable, independent of location and devices, fault tolerance and reduced redundancy, reduced capital expenditure, enhances business process by supporting rapid elasticity and resource sharing

**Disadvantages:** Chances of service outage as XaaS is dependent on the Internet, performance issues due to high utilization of the same resources, highly complex and difficult to troubleshoot at times

---

### Firewall-as-a-Service (FWaaS)

Protects users and organizations from both internal and external threats by filtering the network traffic. Provides security capabilities including the ability to detect malware attacks, in addition to security functionality such as packet filtering, network analyzing, and IPsec.

**Examples:** Zscaler Cloud Firewall, SecurityHQ, Secucloud, Fortinet, Cisco, Sophos

**Advantages:** Blocks malicious web traffic, protects multiple cloud deployments, standardized policy implementation, improved network visibility, enhanced reliability, simpler architecture, easier maintenance

**Disadvantages:** Resistance to acceptance, network latency issues

---

### Desktop-as-a-Service (DaaS)

Provides on-demand virtual desktops and apps to subscribers. Cloud service providers are responsible for providing infrastructure, computing power, data storage, backup, patching, and maintenance. Charges for the service with a predictable pay-as-you-need model.

**Examples:** Amazon WorkSpaces, Citrix Managed Desktops, Azure Windows Virtual Desktop

---

### Mobile Backend-as-a-Service (MBaaS)

Allows app developers to integrate their front-end applications with backend infrastructure through an application programming interface (API) and software development kit (SDK). Reduces the time developers spend on developing backend functionality. Provides user management, push notifications, cloud storage, database management, and geolocation to develop applications.

**Examples:** Google's Firebase, AWS Amplify, Kinvey, Apple's CloudKit, Backendless Cloud

**Advantages:** Improved development efficiency, highly flexible, scalability, pay-as-you-go model

**Disadvantages:** Security issues, high initial costs

---

### Machines-as-a-Service (MaaS) / Equipment-as-a-Service (EaaS)

Also known as Equipment-as-a-Service (EaaS). Allows manufacturers to sell or lease machines to clients and receive a percentage of profits generated by those machines. Extensively utilized and implemented to benefit both manufacturers as well as clients.

**Advantages:** Low investment cost, improved adaptability, reliable and cost-effective income source, improved product quality and quantity

**Disadvantages:** Maintenance and repairs are expensive, machines replace human workers leading to unemployment

---

## Shared Responsibilities in Cloud

In cloud computing, the separation of responsibilities of subscribers and service providers is essential. Separation of duties prevents conflict of interest, illegal acts, fraud, abuse, and error and helps in identifying security control failures. It helps in restricting the amount of influence held by any individual and ensures there are no conflicting responsibilities.

**Three main types of cloud services:** IaaS, PaaS, and SaaS. The cloud deployment model determines where responsibilities lie.

| Layer | On-Premises | IaaS | PaaS | SaaS |
|-------|------------|------|------|------|
| Applications | Customer | Customer | Customer | **Provider** |
| Data | Customer | Customer | Customer | **Provider** |
| Runtime | Customer | Customer | **Provider** | **Provider** |
| Middleware | Customer | Customer | **Provider** | **Provider** |
| OS | Customer | Customer | **Provider** | **Provider** |
| Virtualization | Customer | **Provider** | **Provider** | **Provider** |
| Servers | Customer | **Provider** | **Provider** | **Provider** |
| Storage | Customer | **Provider** | **Provider** | **Provider** |
| Networking | Customer | **Provider** | **Provider** | **Provider** |

---

## Cloud Deployment Models

Cloud deployment model selection is based on enterprise requirements. Factors that influence the choice:

- Host location of cloud computing services
- Security requirements
- Sharing of cloud services
- Ability to manage some or all of the cloud services
- Customization capabilities

### Public Cloud

The provider makes services (applications, servers, data storage) publicly available to the public over the Internet. He is liable for the creation and constant maintenance of the public cloud and its IT resources. Public cloud services may be free or based on a pay-per-usage model.

**Examples:** Amazon Elastic Compute Cloud (EC2), Google App Engine, Windows Azure Services Platform, IBM Bluemix

**Advantages:** Simplicity and efficiency, low cost, reduced time (when server crashes, needs to restart or reconfigure cloud), no maintenance (public cloud service is hosted off-site), no contracts (no long-term commitments)

**Disadvantages:** Security is not guaranteed, lack of control (third-party providers are in charge), slow speed (relies on Internet connections; data transfer rate is limited)

---

### Private Cloud

A private cloud, also known as an internal or corporate cloud, is a cloud infrastructure operated by a single organization and implemented within a corporate firewall. Organizations deploy private cloud infrastructures to retain full control over corporate data.

**Examples:** BMC Software, VMware vRealize Suite, SAP Cloud Platform

**Advantages:** Security enhancement (services are dedicated to a single organization), increased control over resources (organization is in charge), high performance (cloud deployment within the firewall implies high data transfer rates), customizable hardware/network/storage performances (organization owns private cloud), Sarbanes-Oxley, PCI DSS, and HIPAA compliance data are much easier to attain

**Disadvantages:** High cost, on-site maintenance

---

### Community Cloud

A multi-tenant infrastructure shared among organizations from a specific community with common computing concerns such as security, regulatory compliance, performance requirements, and jurisdiction. Can be either on- or off-premises, governed by the organizations or by a third-party managed service provider.

**Examples:** Cisco Cloud Solutions, Salesforce Health Cloud

**Advantages:** Less expensive compared to the private cloud, flexibility to meet community needs, compliance with legal regulations, high scalability, organizations can share a pool of resources from anywhere via the Internet

**Disadvantages:** Competition between consumers in resource usage, inaccurate prediction of required resources, lack of legal entity in case of liability

---

### Hybrid Cloud

A cloud environment comprised of two or more clouds (private, public, or community) that remain unique entities but are bound together to offer the benefits of multiple deployment models.

**Examples:** Microsoft Azure, Zymr, Parangat Cloud Computing, Logicalis

**Advantages:** High scalability (contains both public and private clouds), offers both secure and scalable public resources, high level of security (comprises private cloud), allows to reduce and manage the cost according to requirements

**Disadvantages:** Communication at the network level may be conflicted as it uses both public and private clouds

---

### Multi Cloud

A dynamic heterogeneous environment that combines workloads across multiple cloud vendors that are managed via one proprietary interface to achieve long-term business goals.

**Examples:** Microsoft Azure Arc, Google Cloud Anthos

**Advantages:** High reliability and low latency, flexibility to meet business needs, cost-performance optimization and risk mitigation, low risk of distributed DDoS attacks, increased storage availability and computing power, low probability of vendor lock-in

**Disadvantages:** Multi-cloud system failure affects business agility, using more than one provider causes redundancy, security risks due to complex and large attack surface, operational overhead

---

### Distributed Cloud

A centralized cloud environment comprised of geographically distributed public or private clouds controlled on a single control plane for providing services to the end users located on or off site. Provides service to end users as if they are accessing remote data on their local server.

**Examples:** Google Distributed Cloud, Cloudflare CDN

**Advantages:** High performance, reduced latency, high management and operational consistency compared to hybrid and multi cloud, on-site modernization, edge computing capabilities, on-premises data processing capability, stringent data security, automation applications (AI, ML, IoT etc.)

**Disadvantages:** Security-related vulnerabilities may arise, high cost (network infrastructure deployment), limited software assistance, complex troubleshooting

---

### Poly Cloud

Holds several types of cloud services which can be supplied to different cloud users. Unlike a multi cloud, it provides features of various clouds on a single platform and also helps users choose a specific feature required from each cloud to perform different tasks in their business environment.

**Advantages:** High flexibility, environmental choice, infrastructure and ROI optimization, specialized AI and ML services, cost-effective, high performance

**Disadvantages:** Time-consuming for initial setup, lack of a fixed tool, high R&D cost prior to tool implementation, lack of a fixed model

---

## NIST Cloud Deployment Reference Architecture

The NIST reference architecture displays the primary actors, activities, and functions in cloud computing. The five significant actors are:

**Cloud Consumer** — a person or organization that maintains a business relationship with the CSPs and utilizes the cloud computing services. The cloud consumer browses the CSP's service catalog, requests for the desired services, sets up service contracts with the CSP, and uses the services.

Available services:
- **PaaS** — database (DB), business intelligence, application development and testing, and integration
- **IaaS** — storage, services management, content delivery network (CDN), platform hosting, backup and recovery, and computing
- **SaaS** — human resources, enterprise resource planning (ERP), sales, customer relationship management (CRM), collaboration, document management, email and office productivity, content management, financial services, and social networks

**Cloud Provider** — a person or organization that acquires and manages the computing infrastructure intended for providing services (directly or via a cloud broker) to interested parties via network access.

**Cloud Carrier** — an intermediary that provides connectivity and transport services between CSPs and cloud consumers. The cloud carrier provides access to consumers via a network, a telecommunication, or other access device.

**Cloud Auditor** — a party that performs an independent examination of cloud service controls to express an opinion thereon. A cloud auditor can evaluate the services provided by a CSP regarding security controls, privacy impact (compliance with applicable privacy laws and regulations governing an individual's privacy), and performance.

**Cloud Broker** — the integration of cloud services is becoming too complicated for cloud consumers to manage. Thus, a cloud consumer may request cloud services from a cloud broker, rather than directly contacting a CSP. Service categories: Service Intermediation, Service Aggregation, Service Arbitrage.

---

## Cloud Storage Architecture

Cloud storage is a medium used to store digital data in logical pools using a network. The physical storage is distributed to multiple servers owned by a hosting company. Cloud storage services can be accessed using a web service API or any applications that use the API.

**Three main layers:**

1. **Front-End** — accessed by the end-user; provides APIs for the management of data storage
2. **Middleware** — performs functions such as data de-duplication and replication of data
3. **Back-End** — where the hardware is implemented

Cloud storage is made of distributed resources. It is highly fault-tolerant through redundancy, consistent with data replication, and highly durable. Widely used object storage services include Amazon S3, Oracle Cloud Storage, and Microsoft Azure Storage, Open Stack Swift, etc.

---

## Fog, Edge, and Grid Computing

### Fog Computing

A **distributed and independent** digital environment in which the applications and data storage are positioned between data sources/devices and a cloud service. Fog computing is an extended version of cloud computing that comprises multiple edge nodes that are directly connected to physical devices to enable service access to the end users.

Fog acts as an **intelligent gateway** — an intermediary between hardware and remote servers, also called an intelligent gateway. Fog nodes can be deployed anywhere in a network.

**Advantages:** Low latency (can process large volumes of data with no delay), high business agility (developers can easily design fog instances), no glitches with bandwidth (data are accumulated at distinct points, not transmitted together through one single channel), no connection loss (several interconnected channels don't cause connection loss), elevated security (data processing is performed by numerous distributed systems), low operating cost (data processed locally instead of sending to cloud for analysis), high power efficiency (edge devices run power-saving protocols — Zigbee, Z-Wave, or Bluetooth)

**Disadvantages:** Additional expenditures (organizations must buy additional edge devices such as routers, hubs, gateways), complicated system (fog is an extra layer in the data processing and storage system), constrained scalability (not as scalable as the cloud)

### Edge Computing

A distributed, decentralized computing model in which computation and data processing are performed close to edge devices. Stores data at locations close to the devices from which the data were collected, instead of trusting a central location to store the data. Used in: building automation systems for fast processing, prompt responses, and efficient real-time applications.

### Cloud vs. Fog vs. Edge Computing Comparison

| Feature | Cloud Computing | Fog Computing | Edge Computing |
|---------|----------------|---------------|----------------|
| Speed | Higher access speed than fog; depends on VM connectivity | Higher speed than cloud | Higher speed than fog |
| Latency | High latency | Low latency | Low latency |
| Data Integration | Integrates multiple data sources | Integrates multiple data sources | Integrates limited data sources |
| Capacity | No data reduction while delivering or converting data | Reduces the amount of data sent to cloud | Reduces the amount of data sent to fog |
| Responsiveness | Low response time | High response time | High response time |
| Security | Less secure than fog | Highly secure | Customized security |

### Cloud Computing vs. Grid Computing

| Feature | Cloud Computing | Grid Computing |
|---------|----------------|----------------|
| Architecture | Follows client-server architecture | Follows distributed computing architecture |
| Scalability | Higher scalability | Standard scalability |
| Resource usage | Resources used in a centralized way | Resources used collaboratively |
| Flexibility | More flexible | Less flexible |
| Infrastructure | Providers own the cloud servers | Organization owns and manages grids |
| Services | Include IaaS, PaaS, and SaaS | Include distributed information, distributed computing, and distributed pervasive systems |
| Access | Using regular web protocols | Using grid middleware |
| Payment | Pay-as-you-go model | Users need not pay for their usage |
| Interoperability | Does not support interoperability | Supports interoperability and can be managed easily |

---

## Cloud Service Providers

### Amazon Web Services (AWS)

Source: https://aws.amazon.com

AWS provides on-demand cloud computing services to individuals, organizations, and the government, on a pay-per-use basis. The virtual environment provided by AWS includes CPU, GPU, RAM, HDD storage, operating systems, applications, and networking software such as web servers, databases, and CRM.

### Microsoft Azure

Source: https://azure.microsoft.com

Microsoft Azure provides cloud computing services for building, testing, deploying, and managing applications and services through Azure data centers. Provides all types of cloud services such as computing, mobile storage, data management, messaging, media, machine learning, and IoT.

### Google Cloud Platform (GCP)

Source: https://cloud.google.com

GCP provides IaaS, PaaS, and serverless computing services. These include computing, data storage and analytics, machine learning, networking, bigdata, cloud AI, management tools, identity and security, IoT, and API platforms.

### IBM Cloud

Source: https://www.ibm.com

IBM Cloud is a robust set of advanced data and AI tools and deep industry expertise. Provides various cloud services, such as IaaS, SaaS, and PaaS, through public, private, and hybrid cloud delivery models. These services include computing, networking, storage, management, security, databases, analytics, AI, IoT, mobile, Dev tools, and blockchain.
