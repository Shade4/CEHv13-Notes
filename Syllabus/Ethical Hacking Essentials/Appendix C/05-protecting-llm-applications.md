# Appendix C: Hacking AI Technologies
## Part 5 — Protecting LLM Applications

[← Back to Part 4: Attacks on Machine Learning](04-attacks-on-machine-learning.md) | [Back to README](README.md)

---

## Table of Contents

1. [Mitigating Prompt Injection Attacks](#mitigating-prompt-injection-attacks)
2. [Best Practices Against Prompt Injection](#best-practices-against-prompt-injection)
3. [Preventing Insecure Output Handling](#preventing-insecure-output-handling)
4. [Preventing Training Data Poisoning](#preventing-training-data-poisoning)
5. [Preventing Model Denial of Service](#preventing-model-denial-of-service)
6. [Preventing Supply Chain Vulnerabilities](#preventing-supply-chain-vulnerabilities)
7. [Preventing Sensitive Information Disclosure](#preventing-sensitive-information-disclosure)
8. [Preventing Insecure Plugin Design Attacks](#preventing-insecure-plugin-design-attacks)
9. [Preventing Excessive Agency](#preventing-excessive-agency)
10. [Preventing Overreliance](#preventing-overreliance)
11. [Preventing Model Theft](#preventing-model-theft)
12. [LLM Security Tools and Packages](#llm-security-tools-and-packages)
13. [Module Summary](#module-summary)
14. [Appendix C Complete](#appendix-c-complete)

---

## Mitigating Prompt Injection Attacks

| Mitigation | Description |
|---|---|
| **Privilege Control** | To prevent unauthorized access and manipulation of LLM prompts, limit access to large language models (LLMs) and apply role-based permissions to ensure that only authorized users or entities have access to privileged actions |
| **Human Approval** | Ensure that sensitive operations or prompts are reviewed and authorized by authorized individuals before execution |
| **Segregation of Content** | Separate untrusted or potentially malicious content from user prompts to prevent injection attacks by implementing filtering and sanitizing input data, separating content into different layers or categories based on trust levels, and enforcing strict content separation policies |
| **Trust Boundaries** | Treat LLMs as untrusted components, and visually highlight unreliable or potentially risky responses. Display warnings, alerts, or visual cues to users when LLM outputs are deemed suspicious or untrustworthy, prompting users to verify or validate the responses before further action |

---

## Best Practices Against Prompt Injection

1. The users' and the LLM application's interaction is a **two-way trust boundary**, and the user input or the LLM's output should not be trusted
2. Ensure the LLM does not have access to secret information
3. **Restrict access to plugins** which cannot be hijacked
4. Remove specialized tags from inputs
5. Guide the LLM about prompt injections and how to avoid them using meta prompts
6. **Log inputs and outputs** to determine potential injection, data leakage, and undesirable behavior
7. Implement identity and access management (IAM) and authorization to provide fine-grained least privilege
8. Perform **model scanning** using scanning tools such as Model Scan to identify code injection attempts
9. **Encrypt models at rest** to prevent attackers from reading and writing models after a successful infiltration
10. **Encrypt models in transit** using TLS or mTLS for all HTTP/TCP connections to protect against MITM attacks
11. Store checksum and verify checksum when loading models, for your own models to ensure the integrity of the model file(s)
12. Maintain integrity and authenticity of the model using **cryptographic signature**
13. Ensure the stored ML models in a system have proper authenticated access

---

## Preventing Insecure Output Handling

| Practice | Description |
|---|---|
| **Zero-Trust Approach** | Treat LLM output as if it were user input, and validate and sanitize it properly before further processing or display |
| **OWASP ASVS Guidelines** | Follow OWASP's Application Security Verification Standard (ASVS) guidelines for input validation and sanitization |
| **Output Encoding** | To prevent cross-site scripting (XSS) attacks and other security risks associated with insecure output handling, use encoding techniques such as HTML entity encoding, URL encoding, or base64 encoding to sanitize and escape special characters, scripts, and potentially harmful content in the output |

---

## Preventing Training Data Poisoning

| Practice | Description |
|---|---|
| **Supply Chain Verification** | Verify the integrity and authenticity of external data sources used for training. Maintain records of data sources, transformations, and preprocessing steps (known as "MLnOM" records) to track the training data |
| **Legitimacy Verification** | Implement checks and validations to verify the quality, accuracy, and relevance of training data, to ensure data legitimacy throughout the training stages of LLMs |
| **Use-Case Specific Training** | Create separate models for different use cases or applications to prevent contamination of training data across different contexts |

---

## Preventing Model Denial of Service

| Practice | Description |
|---|---|
| **Input Validation** | Implement input validation to ensure inputs received by the LLM are valid and within expected parameters. Check for data type correctness, length limits, and format adherence |
| **Content Filtering** | Implement content filtering to detect and filter out malicious or malformed inputs that could potentially disrupt or overload the model |
| **Resource Caps** | Limit the number of resources (CPU, memory, disk I/O) that a single request or interaction with the LLM can consume, to prevent an attacker from overwhelming the system with resource-intensive requests |
| **API Rate Limits** | To control the frequency and volume of requests and prevent an attacker from overwhelming the system with a large number of requests in a short period, enforce rate limits for API requests made to the LLM, either based on user accounts or IP addresses |
| **Queue Management** | Implement queuing mechanisms to prioritize critical tasks and prevent the system from being overloaded with many concurrent requests |
| **Resource Monitoring** | Continuously monitor resource usage, performance metrics, and system health to detect anomalies or spikes in resource use |

---

## Preventing Supply Chain Vulnerabilities

1. **Supplier Evaluation** — evaluate suppliers and their policies to ensure they adhere to security best practices, data protection regulations, and ethical standards
2. **Plugin Testing** — implement plugins which are tested and are of trusted test plugins for compatibility, functionality, performance, and security vulnerabilities before integrating them into an LLM
3. **Update Components** — mitigate risks associated with outdated components by regularly updating and patching software, libraries, and dependencies used in LLMs
4. **Inventory Management** — maintain an up-to-date inventory of software components, libraries, plugins, and configurations used in LLM development and deployment
5. **Security Measures** — implement security measures such as **code signing** to verify the authenticity and integrity of LLM models and code

---

## Preventing Sensitive Information Disclosure

| Practice | Description |
|---|---|
| **Data Sanitization** | To protect user privacy and prevent sensitive information from being leaked into LLM training, implement data scrubbing techniques to remove or mask user data in training datasets |
| **Input Validation** | To prevent model poisoning or adversarial attacks, implement input validation mechanisms to filter and sanitize inputs received by LLMs |
| **Fine-Tuning Caution** | Ensure that proper safeguards, encryption, and access controls are implemented to protect sensitive data while fine-tuning LLMs with sensitive data (proprietary information, personally identifiable information — PII) |
| **Data Access Control** | Implement data access controls, authentication mechanisms, and encryption protocols to secure data transmission and prevent unauthorized access to external data sources used by LLMs, restricting access to only authorized entities and applications |

---

## Preventing Insecure Plugin Design Attacks

| Practice | Description |
|---|---|
| **Parameter Control** | To prevent data errors, vulnerabilities, and malicious input attacks, enforce type checks and implement a validation layer to ensure that inputs to LLM plugins are of the correct type and meet predefined criteria |
| **OWASP Guidance** | Follow OWASP (Open Web Application Security Project) Application Security Verification Standard (ASVS) recommendations when designing, implementing, and testing LLM plugins |
| **Thorough Testing** | To identify and mitigate security vulnerabilities, code flaws, and misconfigurations, conduct comprehensive testing of LLM plugins using static application security testing (SAST), dynamic application security testing (DAST), and interactive application security testing (IAST) techniques |
| **Least-Privilege** | To ensure LLM plugins have only the necessary privileges to operate effectively without exposing unnecessary risks, follow ASVS Access Control Guidelines to implement least-privilege principles for LLM plugins |
| **Auth Identities** | Utilize OAuth2 and API Keys for custom authorization mechanisms to authenticate and authorize users and applications accessing LLM plugins |
| **User Confirmation** | Require manual authorization or user confirmation for sensitive actions performed by LLM plugins |

---

## Preventing Excessive Agency

- **Limit Plugin Functions** — allow only essential functions for LLM agents to reduce unnecessary complexity and potential security risks
- **Plugin Scope Control** — maintain a clear scope of operations and prevent unintended or unauthorized actions
- **Granular Functionality** — use specific plugins with well-defined functionalities to improve clarity, modularity, and ease of maintenance, minimizing the risk of unintended consequences
- **Permissions Control** — limiting permissions to the minimum required level ensures that LLM agents only have access to the necessary resources and actions
- **User Authentication** — robust user-authentication mechanisms ensure that actions performed by LLM agents are within the user's context, including verifying the identity and authorization of users before allowing LLM agents to execute actions on their behalf
- **Human-in-the-Loop** — add an extra layer of oversight and control by requiring human approval for actions performed by LLM agents. This enables people to review, validate, and intervene in critical or sensitive operations, ensuring accuracy, compliance, and ethical use of LLM capabilities
- **Downstream Authorization** — to ensure actions initiated by LLM agents are authorized and aligned with organizational policies and regulations, implement authorization mechanisms in downstream systems

---

## Preventing Overreliance

| Monitor & Validate | Cross-Check |
|---|---|
| **Evaluate** the generated text, predictions, and responses produced by the models, to ensure accuracy, coherence, and alignment with desired outcomes | Verify the LLM output with **trusted sources** |

| Fine-Tuning | Auto Validation |
|---|---|
| Perform task-specific fine-tuning to enhance the quality of the LLM | Implement systems to verify LLM output against known facts |

| Task Segmentation | Risk Communication |
|---|---|
| Divide complex tasks to reduce risks | Communicate LLM limitations |

| User-Friendly Interfaces | Secure Coding |
|---|---|
| Ensure that interfaces are user-friendly, useful for performing content filtration, and give appropriate warnings | Follow secure coding guidelines to prevent vulnerabilities |

---

## Preventing Model Theft

- **Access Control and Authentication** — implement a strong authentication mechanism to maintain access to LLM files and training data
- **Network Restrictions** — limit LLM access to resources and APIs by creating separate, isolated network segments to protect access to the model
- **Monitoring and Auditing** — monitor access logs regularly
- **MLOps Automation** — secure ML model deployment and lifecycle management workflow:
  - Encrypt the model data and code
  - Implement physical security of the environment where the model is stored
  - Implement data loss prevention (DLP) to ensure that unauthorized users cannot transfer model files
  - Apply code obfuscation to conceal critical model parameters

---

## LLM Security Tools and Packages

### Lakera Chrome Extension: Protect Against Sensitive Information Disclosure

*Source: lakera.ai*

The **Lakera Chrome extension** provides a privacy guard that protects against **sharing sensitive information with ChatGPT**. It offers support for the following categories of private data:

- Credit card numbers
- Anglophone names
- Email addresses
- Phone numbers
- US street addresses
- US social security numbers
- Secret keys

When Lakera detects a piece of sensitive data (e.g., a credit card number) in a user's prompt, it flags the issue and asks the user to remove the sensitive data before proceeding, rather than letting it be sent to the model silently.

### LLM Guard

*Source: llm-guard.com*

**LLM Guard** is a toolkit for enhancing large language model (LLM) security in production environments — offering input and output evaluation, including sanitization, detection of harmful content, data leakage prevention, and protection against prompt injection and jailbreak attacks. LLM security tools like this generally combine advanced NLP capabilities, anomaly detection, entity extraction, and multilingual support to enhance the security of LLM applications.

**Architecture:** the application integrating with the LLM routes both inbound prompts and outbound responses through LLM Guard's **Input Controls** and **Output Controls** respectively, sitting between the application and the large language model itself.

**Installation:**

```bash
pip install llm-guard
```

**Example — importing an individual scanner and using it to evaluate a prompt or output:**

```python
from llm_guard.input_scanners import BanTopics
scanner = BanTopics(topics=["violence"], threshold=0.5)
sanitized_prompt, is_valid, risk_score = scanner.scan(prompt)

from llm_guard.output_scanners import Bias
scanner = Bias(threshold=0.5)
sanitized_output, is_valid, risk_score = scanner.scan(prompt, model_output)
```

### Additional LLM Security Packages

| Tool | Source |
|---|---|
| **Rebuff** | rebuff.ai |
| **Lasso Security** | lasso.security |
| **BurpGPT** | burpgpt.app |
| **Garak** | garak.ai |
| **Whylabs** | whylabs.ai |
| **Prompt Security** | prompt.security |

---

## Module Summary

This module discussed the following:

- AI technologies encompass a wide range of capabilities, including machine learning, natural language processing, computer vision, and robotics
- Large language models are a specific class of deep learning models that have been trained on vast amounts of text data to understand and generate human-like language
- A prompt injection attack on LLM applications involves manipulating the input prompts provided to the model to generate biased, misleading, or harmful outputs
- Follow OWASP Application Security Verification Standard (ASVS) recommendations when designing, implementing, and testing LLM agents
- To prevent model-theft attacks, implement strong authentication mechanisms to maintain access to LLM files and training data

---

## Appendix C Complete

That closes out **Appendix C: Hacking AI Technologies** — a compact but dense 5-part treatment of AI/LLM security:

- **[Part 1](01-how-ai-works.md)** — How AI Works (AI/ML/DL/LLM fundamentals, applications, challenges)
- **[Part 2](02-llm-integrated-applications.md)** — LLM Integrated Applications (architecture, real-world examples)
- **[Part 3](03-attacks-on-llm-applications.md)** — Attacks on LLM Integrated Applications (OWASP Top 10 for LLM Applications)
- **[Part 4](04-attacks-on-machine-learning.md)** — Attacks on Machine Learning (OWASP Machine Learning Security Top Ten)
- **[Part 5](05-protecting-llm-applications.md)** — Protecting LLM Applications (this file — mitigations + security tooling)

This appendix reflects how quickly AI/LLM security has become a mainstream part of the ethical hacking curriculum — the same OWASP-style Top-10 structure used for web application security ([Module 1's methodologies](../CEH-Module-01-Introduction-to-Ethical-Hacking/README.md)) is now applied directly to LLMs and the ML models underneath them.

With Appendices A, B, and C complete, the full supporting-material arc of the CEH v13 curriculum covered so far runs: **technical foundations (A)** → **governance/risk/blue-team foundations (B)** → **AI/LLM security (C)**, alongside the core module sequence (**Module 1: Introduction to Ethical Hacking**, **Module 2: Footprinting and Reconnaissance**).

---

*Part of the CEH Appendix C study series. [Return to the README](README.md) for the full index.*
