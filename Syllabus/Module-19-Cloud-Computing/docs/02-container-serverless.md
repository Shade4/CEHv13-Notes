# 02 — Container Technology and Serverless Computing

> **CEH v13 Module 19 | Objective 01 (cont.): Container Technology and Serverless**

---

## What is a Container?

A **container** is a package of an application/software including all its dependencies, such as library and configuration files, binaries, and other resources that runs independently from other processes in the cloud environment. All these resource files are delivered as a unit to solve compatibility issues when applications are moved between cloud environments.

These containers are provided to the subscribers in the form of a **CaaS** (Container-as-a-Service). A CaaS service includes the virtualization and management of containers through orchestrators. Using these services, subscribers can develop rich, scalable containerized applications through the cloud or on-site data centers.

Popular container services include Amazon AWS EC2, Google Kubernetes Engine (GKE), Docker.

---

## Container Technology Architecture

Container technology has a **five-tier architecture** and undergoes a three-phase lifecycle:

**Five Tiers:**

- **Tier 1 — Developer machines:** image creation, testing, and accreditation
- **Tier 2 — Testing and accreditation systems:** verification and validation of image contents, signing images, and sending them to the registries
- **Tier 3 — Registries:** storing images and disseminating images to the orchestrators based on requests
- **Tier 4 — Orchestrators:** transforming images into containers and deploying containers to hosts
- **Tier 5 — Hosts:** operating and managing containers as instructed by the orchestrator

**Three Phases of the Lifecycle:**

1. **Image Creation, Testing, and Accreditation** — the application or software components are developed and stored into an image (or images). The image consists of the required files and resources to execute the container. Image creation is handled by developers and is responsible for the security testing of the image. Once the image is created, the security teams carry out image testing and accreditation.

2. **Image Storage and Retrieval** — images are usually placed in registries. Registries provide various services to developers (storing images, version control for easy identification, easy discovery and reuse, fetching and downloading images created by other developers). Registries can be provided as a service or can be self-hosted. Popular registry services: Docker Hub, Amazon Elastic Container Registry (ECR), Docker Trusted Registry (DTR).

3. **Container Deployment and Management** — orchestrators are tools that allow DevOps administrators to fetch images from the registries, deploy them into containers, and manage container operation. This is the final phase of the container lifecycle, where the latest version of the application is deployed and comes into live usage/action. Orchestrators are helpful in monitoring container resource consumption and job execution, identifying host failures, and automating the restarting of containers on new hosts. When resources are exhausted, an orchestrator allocates additional resources to the containers. When an application running in the container needs to be updated, the existing containers are destroyed, and new containers are created from the updated images. Popular orchestrators: Kubernetes, Docker Swarm, Nomad, Mesos.

### Container Features

- **Portability and consistency** — application developed in a container includes all the resources required to perform; helps clients or end-users run an application on various platforms and private or public cloud environments
- **Security** — owing to the independent nature of containers, security risks are reduced; if an application is attacked or compromised, its infections do not extend across the remaining containers
- **High efficiency and cost effectiveness** — containers can run with fewer resources compared to VMs because they do not need independent operating systems; containers need a few megabytes of memory to run, enabling users to run multiple containers on a single server
- **Scalability** — containers are scalable and enable subscribers or users to integrate more similar containers under the same cluster; smart scaling technology enables users to run only the intended container and put unwanted containers at rest, making it cost-effective
- **Robustness** — containers can be generated, deployed, and destroyed in seconds; doesn't require an operational process; rapidly reduces the generation time and speeds up the user's experience

### Containers vs. Virtual Machines

| Feature | Virtual Machines | Containers |
|---------|-----------------|-----------|
| Weight | Heavyweight | Lightweight and portable |
| OS | Run on independent operating systems | Share a single host operating system |
| Virtualization | Hardware-based virtualization | OS-based virtualization |
| Provisioning | Slower provisioning | Scalable and real-time provisioning |
| Performance | Limited performance | Native performance |
| Isolation | Completely isolated; making it more secure | Process-level isolation, partially secured |
| Launch | Created and launched in minutes | Created and launched in seconds |

---

## Docker

Docker is an open-source technology used for developing, packaging, and running applications. All Docker dependencies are in the form of containers to ensure that applications work in a seamless environment. Docker provides a PaaS through OS-level virtualization and delivers containerized software packages.

The benefit of Docker is that when an application is packaged along with its dependencies into a Docker container, it can run in any environment. Furthermore, when developers build applications using Docker containers, they are assured that there will be no interference between them because Docker containers are isolated from each other and communicate via well-defined channels.

### Docker Engine

The Docker engine is a **client/server application** installed on a host that allows to develop, deploy, and run applications using the following components:

- **Server** — a persistent back-end process, also known as a **daemon process** (`dockerd` command)
- **REST API** — allows the communication and assignment of tasks to the daemon
- **Client CLI** — the command-line interface used to communicate with the daemon and where various Docker commands are initiated

### Docker Architecture

The Docker architecture employs a client/server model and consists of various components, such as the host, client, network, and other storage units. The Docker client interacts with the Docker daemon, which develops, runs, and distributes the containers. The Daemon and Docker clients can carry out operations on the same host; alternatively, users can connect the Docker client to remote daemons. The communication between the Docker client and the Docker server daemon is established via REST API.

**Key Docker Components:**

- **Docker Daemon** — the Docker daemon (`dockerd`) processes the API requests and handles various Docker objects such as containers, volumes, images, and networks
- **Docker Client** — the primary interface through which users communicate with Docker; when commands such as `docker run` are initiated, the client passes related commands to `dockerd`, which then executes them
- **Docker Registries** — locations where images are stored and pulled; can be either private or public; Docker Cloud and Docker Hub are two popular public registries; Docker Hub is a predefined location of Docker images, which can be used by the general public

### Docker Swarm

The Docker engine supports the swarm mode that allows managing multiple Docker engines within the Docker platform. Docker CLI is used for creating a swarm, deploying an application to the swarm, and handling its activity or behavior.

The swarm mode enables administrators and developers to:
- Communicate with containers and assign jobs to different containers
- Expand or reduce the number of containers based on the load
- Carry out a health check and handle the lifecycle of different containers
- Disperse failover and redundancy to continue a process even if node failure occurs
- Provide timely software updates to all containers

### Docker Objects

- **Images** — used to store and deploy containers; they are read-only binary templates with instructions for container creation
- **Containers** — application resources run inside the containers; a container is a runnable instance of an application image; Docker CLI or API is used to create, launch, stop, and destroy these containers
- **Services** — enable users to extend the number of containers across daemons, and together they serve as a swarm with several managers and workers; each swarm member is a daemon, and all these daemons can interact with each other using Docker API
- **Networking** — a channel through which all isolated containers communicate
- **Volumes** — a storage where persisting data is created and used by Docker containers are stored

### Docker Operations (Common Commands)

```bash
# Build a new image from a Dockerfile
docker build -t <image_name> .

# List all local images
docker images

# Tag an existing image
docker tag <source_image> <target_image:tag>

# Pull a new image from the Docker registry
docker pull <image_name>

# Push a local image to the Docker registry
docker push <image_name>

# Search for existing images
docker search <keyword>

# Run a container
docker run -d -p 8080:80 <image_name>

# List running containers
docker ps

# Stop a container
docker stop <container_id>

# Remove a container
docker rm <container_id>

# Execute a command inside a running container
docker exec -it <container_id> /bin/bash
```

### Microservices vs. Docker

Monolithic applications are broken down into **cloud-hosted sub-applications called microservices** that work together, each performing a unique task. Microservices divide and distribute the application workload, providing stable, seamless, and scalable services by interacting with each other.

As each microservice is packaged into the Docker container along with the required libraries, frameworks, and configuration files, microservices belonging to a single application can be developed and managed using multiple platforms.

Compared to traditional data storage models used by monolithic applications, microservices **decentralize data storage** by managing their own data stores. Developers create a Docker container for each microservice.

---

## Docker Networking

Docker allows connecting multiple containers and services or other non-Docker workloads together. It can manage Docker hosts running on multiple platforms such as Linux and Windows, in a platform-independent way.

**Container Network Model (CNM)** provides application portability across heterogeneous infrastructures.

### CNM Constructs

- **Sandbox** — comprises the container network stack configuration for the management of container interfaces, routing tables, and domain name system (DNS) settings
- **Endpoint** — to maintain application portability, an endpoint is connected to a network and is abstracted away from the application, so that services can implement different network drivers
- **Network** — an interconnected collection of endpoints that do not have network connection cannot communicate over the network

### Docker Native Network Drivers

| Driver | Description |
|--------|-------------|
| **Host** | Using a host driver, a container implements the host networking stack |
| **Bridge** | A bridge driver is used to create a Linux bridge on the host that is managed by the Docker |
| **Overlay** | An overlay driver is used to enable container communication over the physical network infrastructure |
| **MACVLAN** | A macvlan driver is used to create a network connection between container interfaces and the parent host interface or sub-interfaces using the Linux MACVLAN bridge mode |
| **None** | A none driver implements its own networking stack and is isolated completely from the host networking stack |

### Remote Docker Network Drivers

- **Contiv** — Cisco open-source network plugin for building security and infrastructure policies for multi-tenant microservices deployments
- **Weave** — network plugin for building a virtual network connecting Docker containers across multiple clouds
- **Kuryr** — a network plugin that implements the Docker libnetwork remote driver by using Neutron, an OpenStack networking service, and also includes an IPAM driver

---

## Container Orchestration

Container orchestration is an automated process of managing the lifecycles of software containers and their dynamic environments. It is used for scheduling and distributing the work of individual containers for microservices-based applications spread across multiple clusters.

**Tasks that can be automated using container orchestrators:**

- Provisioning and deployment of containers
- Failover and redundancy of containers
- Creating or destroying containers to distribute the load evenly across host infrastructure
- Moving containers from one host to another on resource exhaustion or host failure
- Automatic resource allocation between containers
- Exposing running services to the external environment
- Performing load balancing, traffic routing, and service discovery between containers
- Performing health checks of running containers and hosts
- Ensuring the availability of containers
- Configuring application-related containers
- Securing the communication between containers

**Popular orchestration platforms:** Docker Swarm, Kubernetes

---

## Kubernetes

Kubernetes, also known as K8s, is an open-source, portable, extensible, orchestration platform developed by Google for managing containerized applications and microservices. Containers provide an efficient way for packaging and running applications. In a real-time production environment, you need to manage the containers that run the applications and ensure there is no downtime.

For example, if a container experiences failure, another container boots automatically. Kubernetes provides a resilient framework to manage distributed containers, generate deployment patterns, and perform failover and redundancy for applications.

### Kubernetes Features

- **Service discovery** — allows a service to be discovered via a DNS name or IP address
- **Load balancing** — when a container receives heavy traffic, Kubernetes automatically distributes the traffic to other containers and performs load balancing
- **Storage orchestration** — allows developers to mount their own storage capabilities, such as local and public cloud storage
- **Automated rollouts and rollbacks** — automates the process of creating new containers, destroying existing containers, and moving all resources from one container to another
- **Automatic bin packing** — can manage a cluster of nodes that run containerized applications; if you specify the resources needed to run the container, such as processing power and memory, Kubernetes can automatically allocate and deallocate resources to the containers
- **Self-healing** — automatically performs a health check of the containers, replaces the failed containers with new containers, destroys failed containers, and avoids advertising unavailable containers to clients
- **Secret and configuration management** — allows users to store and manage sensitive information such as credentials, secure shell (SSH) keys, and OAuth tokens; application configuration and sensitive information can be deployed and updated without the need to rebuild the container images

### Kubernetes Cluster Architecture

When Kubernetes is deployed, it creates a **cluster**. A cluster is a group of computers known as nodes, which execute the applications running inside the containers managed by Kubernetes. A cluster comprises a minimum of one master node and one worker node.

**Master Components:**

| Component | Description |
|-----------|-------------|
| `kube-apiserver` | The API server is an integral part of the Kubernetes control panel that responds to all API requests; serves as the front-end for the control panel; the only component that interacts with the etcd cluster and ensures data security |
| `etcd` | A distributed and consistent key-value store where Kubernetes cluster data, service discovery details, API objects, etc. are stored |
| `kube-scheduler` | A master component that scans newly generated pods and allocates a node for them; assigns nodes based on factors such as the overall resource requirement, data locality, software/hardware/policy restrictions, and internal workload interventions |
| `kube-controller-manager` | A master component that runs controllers; controllers are generally individual processes (node controller, endpoint controller, replication controller, service account and token controller) but are combined into a single binary and run together in a single process to reduce complexity |
| `cloud-controller-manager` | The master component used to run controllers that communicate with cloud providers; cloud-controller-manager enables the Kubernetes code and cloud provider code to evolve separately |

**Node Components:**

| Component | Description |
|-----------|-------------|
| `kubelet` | An important Kubernetes agent that runs on each node in the cluster; manages working pods and supplying the Kubernetes runtime services; ensures containers running in a pod are healthy and running as expected; does not handle containers that are not generated by Kubernetes |
| `kube-proxy` | A network proxy service that also runs on every worker node; maintains the network rules that enable network connection to the pods |
| Container Runtime | Software designed to run containers; Kubernetes supports various container runtimes, such as Docker, rktlet, containerd, and cri-o |

### Types of Cluster Computing

- **Highly Available (HA) / Fail-over** — in a fail-over cluster, more than one node runs simultaneously to offer high availability (HA) or continuous availability (CA); if one node fails, the other node assumes its responsibility of providing the service without downtime
- **Load Balancing** — in a load-balancing cluster, the workload is distributed among the nodes to avoid overstressing a single node; the load balancer performs periodic health checks on each node to identify node failures and reroutes the incoming traffic to another node; a load-balancing cluster is also a highly available cluster
- **High-Performance Computing (HPC)** — in a high-performance computing cluster, the nodes are configured to provide extreme performance by parallelizing the tasks; scaling also helps in maximizing performance

### Clusters in the Cloud

Clusters in the cloud are sets of nodes hosted on virtual machines (VMs) and are often coupled with virtual private clouds. Cloud clustering minimizes the effort and time required to establish a cluster. Clusters can be scaled up on demand by adding additional resources or instances easily. The cloud also enhances the latency and resiliency by node deployment in many availability zones. Cloud clustering maximizes the cluster's availability, security, and maintainability.

---

## Container Security Challenges

Organizations are widely adopting container-based platforms owing to features (flexibility, continuous application delivery, rapid deployment, efficient deployment). However, rapid growth and propagation of container technology have resulted in many security challenges:

- **Inflow of vulnerable source code** — containers constitute an open-source platform used by developers to regularly update, store, and use images in a repository
- **Large attack surface** — host OS consists of many components (apps, VMs, and databases) in the cloud or on-premises; large attack surface implies many vulnerabilities and increased difficulty in detecting them
- **Lack of visibility** — a container engine runs the container, interfaces with the Linux kernel, and creates another layer of abstraction camouflaging the actions of the container and making it difficult to track activities of specific containers
- **Compromising secrets** — containers require sensitive information such as API keys, usernames, or passwords for accessing any services; attackers who illicitly gain access to this sensitive information can compromise security
- **DevOps speed** — containers can be executed promptly and, after execution, are stopped and removed; makes it easier for attackers to launch attacks and hide themselves without installing any malicious code
- **Noisy neighboring containers** — a container may consume and exhaust all available system resources, which directly affects the operation of other neighboring containers
- **Container breakout to the host** — containers run as root may break the containment and gain access to the host OS through privilege escalation
- **Network-based attacks** — may exploit failed containers having active raw sockets and outbound network connections to launch various network-based attacks
- **Bypassing isolation** — after compromising security of a container, may escalate privileges to gain access to other containers or the host itself
- **Ecosystem complexity** — containers are built, deployed, and managed using multiple vendors and sources; makes it complex to secure and update the individual components
- **Misconfigurations** — incorrect configurations (overly permissive network policies or misconfigured access controls) can lead to security breaches
- **Isolation Breakdowns** — containers designed to be isolated from each other and the host system; vulnerabilities in container runtime or kernel can lead to isolation failures
- **Insecure Communication** — containers often communicate over networks; without proper encryption and security measures, such communication can be intercepted or altered

---

## Container Management Platforms

### Portainer

Source: https://www.portainer.io

The most versatile container management tool that simplifies secure adoption of containers at a remarkable speed irrespective of the industry or orchestration platform, or computing device. Makes it easy for cloud administrators to set up, maintain, and troubleshoot container infrastructure in public clouds and datacenters.

Also a potential policy and governance platform in container management stacks, whether on the manufacturing floor or in the public cloud.

**Additional Container Management Platforms:**

- Apache Mesos (https://mesos.apache.org)
- Amazon Elastic Container Service (Amazon ECS) (https://aws.amazon.com)
- Microsoft Azure Container Instances (ACI) (https://azure.microsoft.com)
- Red Hat OpenShift Container Platform (https://www.redhat.com)
- Docker CLI (https://www.docker.com)

---

## Kubernetes Platforms

### Mirantis Kubernetes Engine (MKE)

Source: https://www.mirantis.com

The Mirantis Kubernetes Engine is a CNCF-validated enterprise Kubernetes platform designed to develop and run modern applications at scale. Supports private clouds, public clouds, and bare metal environments. Enables multicluster management and provides a unified interface for streamlined operations, including swarm cluster instances.

**Additional Kubernetes Platforms:**

- Google Kubernetes Engine (GKE) (https://cloud.google.com)
- Amazon Elastic Kubernetes Service (EKS) (https://aws.amazon.com)
- IBM Cloud Kubernetes Service (https://www.ibm.com)
- Docker Kubernetes Service (DKS) (https://www.docker.com)
- Kubernetes (https://kubernetes.io)

---

## Container Vulnerabilities

| # | Vulnerability | Description |
|---|---------------|-------------|
| 1 | Impetuous Image Creation | Careless creation of images without considering the security safeguards or control aspects leads to vulnerabilities in the images |
| 2 | Insecure Image Configurations | Using a base image that includes outdated or unnecessary software when configuring a container can increase the attack surface; this can lead to the exposure of sensitive information and make the container more vulnerable to security breaches |
| 3 | Unreliable Third-Party Resources | Using untrusted third-party resources causes severe threat and makes the resources vulnerable to malicious attacks |
| 4 | Unauthorized Access | Gaining access to user accounts leads to privilege escalation attacks |
| 5 | Insecure Container Runtime Configurations | Improper handling of the configuration option and mounting sensitive directories on the host cause faulty and insecure runtime configurations |
| 6 | Data Exposure in Docker Files | Container images exposing sensitive information, such as passwords and SSH encryption keys, can be exploited to compromise the security of the container |
| 7 | Embedded Malware | A container image may be embedded with malware after creation, or hardcoded functions may download malware after image deployment |
| 8 | Non-Updated Images | Outdated images contain security loopholes and bugs that compromise the security of images |
| 9 | Hijacked Repository and Infected Resources | Security misconfiguration and poor access control to the repository that can poison the resources by altering or deleting files |
| 10 | Hijacked Image Registry | Mismanaged configurations and vulnerabilities can be exploited to compromise the integrity and image hubs |
| 11 | Exposed Services due to Open Ports | Misconfiguration of an application may allow port access and exposure of sensitive information upon port scanning |
| 12 | Mixing of Workload Sensitivity Levels | Orchestrators place workloads with different sensitivity levels on the same host; if a container hosts a public webserver with vulnerabilities, it may pose a threat to containers processing sensitive information |
| 13 | Non-Updated Images | Exposed Docker Images — Docker images exposing sensitive information, such as passwords and SSH encryption keys, can be exploited to compromise the security of the container |

---

## Kubernetes Vulnerabilities

| # | Vulnerability | Description |
|---|---------------|-------------|
| 1 | No Certificate Revocation | Kubernetes does not support certificate revocation; the entire certificate chain must be regenerated to remove a certificate; attackers can exploit the certificate before it is replaced across the entire cluster |
| 2 | Unauthenticated HTTPS Connections | Though Kubernetes uses PKI, the network between components is not authenticated properly using TLS; attackers can gain unauthorized access to kubelet-managed Pods and retrieve sensitive information |
| 3 | Exposed Bearer Tokens in Logs | Kubernetes requires an authentication mechanism for enforcing user privileges; bearer tokens are logged in hyperkube kube-apiserver system logs; attackers with access to system logs can exploit bearer tokens to impersonate a previously logged legitimate user |
| 4 | Exposure of Sensitive Data via Environment Variables | While configuring components, environmental variables allow derivation of settings; attackers can access stored values through environment logging and perform further exploitation on the endpoints |
| 5 | Secrets at Rest not Encrypted by Default | Secrets defined by users such as credentials or application configuration data are not encrypted by default; attackers can retrieve unencrypted secrets by gaining access to the etcd servers |
| 6 | Non-constant Time Password Comparison | Kube-apiserver has multiple authentication back-ends for client request processing; it does not perform a secure comparison of secret values when using basic password authentication; attackers can launch timing attacks to retrieve passwords |
| 7 | Hardcoded Credential Paths | Instead of hardcoding credential paths in the source code, they are specified during configuration via an interface; if the cluster token and root certificate authority (CA) are stored in different locations, attackers can insert a malicious token and root CA to access the entire cluster |
| 8 | Log Rotation is not Atomic | Kubelet uses logs for storing the metadata about the container; during log rotation, if the kubelet is restarted, all logs may be erased; attackers monitor log rotation and when it occurs attempt to remove all logs |
| 9 | No Back-off Process for Scheduling | The Kubernetes pod is an execution unit which requires keen co-ordination for scheduling and has no back-off process; this causes a tight loop as the scheduler continuously schedules pods that are rejected by the other processes |
| 10 | No Non-repudiation | Kube-apiserver performs all user transactions without a central auditing service; if debug mode is disabled, kube-apiserver does not record user actions; attackers can directly interact with kube-apiserver and perform various malicious activities |

---

## Serverless Computing

**Serverless computing**, also known as serverless architecture or Function-as-a-Service (FaaS), is a cloud-based application architecture where application infrastructure and supporting services are provided by the cloud vendor as they are needed. Serverless computing provides per-use functionality to consumers, removing the burden of starting and stopping the servers.

In the serverless architecture, the application code runs on the cloud-hosted infrastructure managed by a third-party service provider. The cloud service provider is responsible for provisioning, scaling, load balancing, and securing the serverless infrastructure. The cloud service provider is also responsible for patch management of the operating systems and underlying software and services.

**Important distinction:** Serverless applications are not truly serverless — servers are required but not physically exposed to the developers.

### Advantages

- High scalability and flexibility
- Faster deployment and updating
- Reduced infrastructure cost
- No server management
- Pay-per-use
- Reduced latency and scaling cost
- Quicker provisioning of resources
- Low risk of failure
- No system administration

### Disadvantages

- Increased security vulnerability
- Vendor-lock-in
- Difficulty in managing statelessness
- Complex end-to-end application testing
- Unsuitability of long-running processes for serverless computing

### Serverless vs. Containers

| Feature | Containers | Serverless Computing |
|---------|-----------|---------------------|
| Developer responsible for | Defining the container configuration files along with the OS, software, libraries, storage, and networking | Developing and uploading the code to support serverless computing; the entire provisioning process is taken care of by the cloud service provider |
| Runtime | Initiated, the container runs continuously until the developer stops or destroys it | After it completes execution, the serverless function is automatically destroyed by the cloud environment |
| Server support | A container server can support even when the container is not executing any programs | Timeout is enabled on serverless functions |
| Host cluster | Containers support running on a cluster of host nodes | The underlying host infrastructure is transparent to developers |
| Data storage | Containers store data in temporary storage or mapped storage volumes | Serverless functions do not support temporary storage; instead, data is stored in the object storage medium |
| Application type | Containers support both complex applications and lightweight microservices | Serverless functions are suitable only for microservices applications |
| Language | Developers can select the language and runtime for applications running in a container | Language selection for serverless functions is restricted by the cloud service provider |

### Serverless Computing Frameworks

- **Microsoft Azure Functions** — https://azure.microsoft.com — serverless computing platform that allows users to run code without provisioning and managing servers; fully automated and provides scaling based on the workload volume
- **AWS Lambda** — https://aws.amazon.com
- **Google Cloud Functions** — https://cloud.google.com
- **Serverless Framework** — https://serverless.com
- **AWS Fargate** — https://aws.amazon.com
- **Alibaba Cloud Function Compute** — https://www.alibabacloud.com
