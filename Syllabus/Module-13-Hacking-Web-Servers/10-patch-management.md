# 10 — Patch Management

> Closing section of **Objective 4: Web Server Attack Countermeasures**

## 1. What Is Patch Management?

Developers always attempt to find bugs in a web server and fix them. **Bug fixes** are distributed in the form of **patches**, which provide protection against known vulnerabilities in the web server. Unpatched or vulnerable web servers can create a security loophole in the web server. The role of patches, upgrades, and hotfixes in the web server is critical, and this section provides guidance for choosing proper patches, upgrades, hotfixes, and their appropriate sources for secure patch management.

**Patch management** is an area of systems management that involves acquiring, testing, and installing multiple patches (code changes) on an administered computer system. It is a method of defense against vulnerabilities that ensures security weaknesses or corrupt data are addressed. It is a process of:
- Scanning for vulnerabilities
- Detecting missed security patches and hotfixes
- Deploying the relevant patches as they become available, to secure the network

Patch management involves the following tasks:
- Choosing, verifying, testing, and applying patches
- Updating previously applied patches with current patches
- Listing patches applied previously to the current software
- Recording repositories or depots of patches for easy selection
- Assigning and deploying the applied patches

If a system identifies a vulnerability before it is fixed, then the system might be susceptible to attacks — this is exactly why timely patch management matters.

## 2. Patches and Hotfixes

- A **patch** is a small piece of software designed to fix problems, security vulnerabilities, and bugs, as well as improve the usability or performance of a computer program or its supporting data. A software vulnerability is a weakness of a program that makes it susceptible to malware attacks. Software vendors provide patches that address the security vulnerability and reduce the probability of threats exploiting a specific bug. Patches include fixes and updates for multiple bugs or issues. A patch is a publicly released update that all customers can apply. A system without patches is much more vulnerable to attacks than a regularly patched system.
- A **hotfix** is a package used to address a critical defect in a live production environment and contains a fix for a **single, specific issue** — not a general bug-fix bundle. It updates multiple components involved in securing web servers.
  - Vendors update users about the latest hotfixes through email or by making them available on their official website.
  - Hotfixes provide quick solutions and ensure the issues are resolved.
  - Hotfixes are updates to software that fix a critical defect in a version and are **not always distributed outside** the customer organization that reported the issue.
  - Vendors occasionally deliver hotfixes as a set of fixes bundled together, called a **combined hotfix** or **service pack**.

## 3. The Automated Patch Management Process

| Step | Description |
|---|---|
| **Detect** | Use tools to detect missing security patches. |
| **Assess** | Assess the issue(s) and its associated severity by weighing the factors that influence the decision. |
| **Acquire** | Download the patch for testing. |
| **Test** | Install the patch first on a test machine to verify the consequences of the update. |
| **Deploy** | Deploy the patch to computers and ensure that applications are not adversely affected. |
| **Maintain** | Subscribe to receive notifications about vulnerabilities when they are reported. |

## 4. Installation of a Patch

The installation of a patch entails identifying appropriate sources for updates and patches. It is important to identify appropriate sources for updates and patches, because patches that are not installed from trusted sources can render the target server even **more** vulnerable to attacks, instead of hardening its security.

### Identifying Appropriate Sources for Updates and Patches

- Create a **patch management plan** that fits the operational environment and business objectives.
- Find appropriate updates and patches on the home sites of the applications or OS vendors.
- The recommended method of tracking issues relevant to proactive patching is to **register with the home sites** to receive alerts.

### Two Ways to Install a Patch

- **Manual Installation** — the user downloads the patch from the vendor and installs it themselves.
- **Automatic Installation** — applications use an auto-update feature to update themselves without direct user action.

### Implementation and Verification of a Security Patch or Upgrade

- Before installing any patch, **verify the source**.
- Use a proper patch-management program to validate file versions and checksums before deploying security patches.
- The patch-management tool must be able to **monitor the patched systems** after deployment.
- The patch-management team should check for updates and patches **regularly**.

## 5. Patch Management Best Practices

- Define roles, responsibilities, and procedures for patch management, including timelines for applying patches and handling emergencies.
- Develop a comprehensive policy outlining procedures for evaluating, testing, approving, and deploying patches.
- Outline systems, applications, and devices — including servers, workstations, and networking equipment — that require patching.
- Maintain an updated inventory of all hardware and software assets to ensure no device or application is overlooked during the patching process.
- Assess and prioritize patches based on the severity of the vulnerabilities they address.
- Group assets by criticality, application type, or other relevant criteria for prioritizing patching efforts.
- Use tools to automate the discovery of applicable patches in the systems and timely updates.
- Implement a testing process to verify that patches do not cause issues in systems.
- Leverage patch-management software to streamline the patching process, from discovery to deployment.
- Create and follow a **regular schedule** for patching to ensure updates are applied in a timely manner.
- Create a procedure for **fast-tracking** the deployment of patches for critical, actively-exploited vulnerabilities.
- Stay informed about new vulnerabilities and available patches by subscribing to security advisories and feeds.
- Limit access to patch-management tools and software to **authorized personnel** only.
- Ensure that patch management is part of standard IT operations, not an afterthought.
- Verify that patches have been successfully applied after deployment and are functioning as intended.
- Use tools or systems to track patch status to ensure all assets are appropriately patched.
- Regularly perform vulnerability scanning to identify unpatched vulnerabilities and verify patch effectiveness.
- Protect the **patch-management system itself** against threats and vulnerabilities (it's a high-value target).
- Regularly review and refine patch-management processes to improve efficiency.
- Include third-party application patches in the organization's patch-management strategy.
- Have a plan for quickly **rolling back** patches in case they cause unforeseen issues.
- Use a controlled test environment to verify patches before deploying them to production systems.
- Ensure patches do not cause compatibility issues with existing applications and configurations.
- Implement scheduled patching to minimize disruption and align with maintenance windows.

## 6. Patch Management Tools

### GFI LanGuard

- **Source:** https://www.gfi.com
- The GFI LanGuard patch-management software scans the user's network automatically, as well as installs and manages security and non-security patches across **Microsoft, macOS X, and Linux** operating systems, as well as many third-party applications. It allows auto-download of missing patches as well as **patch rollback**, resulting in a consistently-configured environment that is protected from threats and vulnerabilities.

### Additional Patch Management Tools

| Tool | Source |
|---|---|
| Symantec Client Management Suite | https://www.broadcom.com |
| SolarWinds Patch Manager | https://www.solarwinds.com |
| Kaseya Patch Management | https://www.kaseya.com |
| Software Vulnerability Manager (Flexera) | https://www.flexera.com |
| Ivanti Patch for Endpoint Manager | https://www.ivanti.com |

---

## Module Summary

In this module, we discussed in detail the general concepts related to web servers; various web server threats and attacks; the web server attack methodology in detail, including information gathering, web server footprinting, vulnerability scanning, and web server passwords hacking; and various web server hacking tools. Additionally, we discussed various countermeasures that can be employed to prevent web server hacking attempts. We concluded the discussion with a detailed look at how to secure web servers using various security tools.

> 📖 **What's next:** the courseware's next module (**Module 14: Hacking Web Applications**) discusses in detail how attackers, as well as ethical hackers and pen testers, hack web applications — the layer that sits *on top of* the web server infrastructure covered here.

---

**Previous:** [← 09 — Security Scanning & Monitoring Tools](09-security-scanning-and-monitoring-tools.md) · **Back to:** [README](README.md)
