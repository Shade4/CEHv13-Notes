# Appendix C: Hacking AI Technologies
## Part 4 — Attacks on Machine Learning

[← Back to Part 3: Attacks on LLM Integrated Applications](03-attacks-on-llm-applications.md) | [Next: Protecting LLM Applications →](05-protecting-llm-applications.md)

---

## Table of Contents

1. [OWASP Machine Learning Security Top Ten](#owasp-machine-learning-security-top-ten)
2. [ML01: Input Manipulation Attack](#ml01-input-manipulation-attack)
3. [ML02: Data Poisoning Attack](#ml02-data-poisoning-attack)
4. [ML03: Model Inversion Attack](#ml03-model-inversion-attack)
5. [ML04: Membership Inference Attack](#ml04-membership-inference-attack)
6. [ML05: Model Theft](#ml05-model-theft)
7. [ML06: AI Supply Chain Attacks](#ml06-ai-supply-chain-attacks)
8. [ML07: Transfer Learning Attack](#ml07-transfer-learning-attack)
9. [ML08: Model Skewing](#ml08-model-skewing)
10. [ML09: Output Integrity Attack](#ml09-output-integrity-attack)
11. [ML10: Model Poisoning](#ml10-model-poisoning)
12. [Quick-Reference Summary](#quick-reference-summary)

---

## OWASP Machine Learning Security Top Ten

While [Part 3](03-attacks-on-llm-applications.md) covered attacks aimed at LLM-*integrated applications* (the surrounding app, plugins, and orchestration layer), this section covers attacks aimed at the underlying **machine learning model itself** — a distinct, broader category that applies to any ML system, not just LLMs.

| Attack Type | Description |
|---|---|
| **ML01: Input Manipulation Attack** | The type of attack in which an attacker deliberately alters input data to mislead the model |
| **ML02: Data Poisoning Attack** | Occurs when an attacker manipulates the training data to cause the model to behave in an undesirable way |
| **ML03: Model Inversion Attack** | Occurs when an attacker reverse-engineers the model to extract information from it |
| **ML04: Membership Inference Attack** | Occurs when an attacker manipulates the model's training data to cause it to behave in a way that exposes sensitive information |
| **ML05: Model Theft** | Occurs when an attacker gains access to the model's parameters |
| **ML06: AI Supply Chain Attacks** | Occurs when an attacker modifies or replaces a machine learning library or model that's used by a system |
| **ML07: Transfer Learning Attack** | Occurs when an attacker trains a model on one task and then fine-tunes it on another task to cause it to behave in an undesirable way |
| **ML08: Model Skewing** | Occurs when an attacker manipulates the distribution of the training data to cause the model to behave in an undesirable way |
| **ML09: Output Integrity Attack** | The attacker aims to modify or manipulate the output of a machine learning model to change its behavior or cause harm to the system it's used in |
| **ML10: Model Poisoning** | Occurs when an attacker manipulates the model's parameters to cause it to behave in an undesirable way |

---

## ML01: Input Manipulation Attack

**Input manipulation attacks** include adversarial attacks in which an attacker intentionally alters input data to deceive or manipulate the model's behavior, leading to incorrect or biased predictions.

The classic illustration from adversarial ML research: an image of a **panda**, classified correctly with high confidence, has a small amount of carefully crafted **noise** added to it (imperceptible to a human) — the resulting image is misclassified as a **gibbon** with even higher confidence than the original correct classification. The same "altering data to mislead a model" pattern shows up across many image classifiers, where subtly perturbed images of everyday objects get confidently misclassified into entirely wrong categories.

**Real-world security example:** manipulating network traffic — such as the source and destination IP address or payload — to exploit an intrusion detection system's underlying model, making the IDS unable to correctly detect malicious traffic. This works via a pipeline of Raw Network Data → Feature Extraction → Pre-processed Sample → Analysis and Classification → Output (benign/malicious), where the attacker's manipulated input is crafted specifically to be misclassified at the final step.

---

## ML02: Data Poisoning Attack

An attacker **manipulates the training data** to compromise the integrity and accuracy of the model. Data poisoning attacks aim to alter the model's behavior during training, so that it makes incorrect predictions or classifications once deployed.

**Example: Training a Spam Classifier**
- An attacker poisons the training data of a deep learning model responsible for classifying emails as spam or not spam
- The attacker, having compromised the data storage system, injects maliciously labeled spam emails into the training dataset
- The attacker manipulates the data-labeling process by altering the labeling of the emails

**Example: Training a Network Traffic Classification System**
- An attacker introduces many examples of network traffic that are incorrectly labeled as a different traffic type, causing the model to be trained to misclassify that traffic
- This poisons the training data for a deep learning model used to classify network traffic, resulting in the model making incorrect traffic classifications once deployed

A commonly cited illustration of the resulting risk: a poisoned model that confuses a **stop sign** with a **speed-limit sign** — a small mislabeling introduced during training with potentially serious real-world consequences if deployed in something like an autonomous-vehicle perception system.

---

## ML03: Model Inversion Attack

Model inversion attacks use the **output of the model** to extract information (parameters or architecture) from it.

**Example: Bypassing a Bot Detection Model in Online Advertising**
- An advertiser wants to automate their advertising campaigns by using bots to perform actions such as clicking on ads and visiting websites
- Online advertising platforms use bot-detection models to prevent bots from performing these actions
- To bypass online advertising bot-detection models, the advertiser trains a deep-learning model for bot detection and uses it to reverse-engineer and modify the predictions of the bot-detection model used by the online advertising platform

**Example: Stealing Personal Information From a Face Recognition Model**
- An attacker wants to steal personal information from a model that performs face recognition
- The attacker uses model inversion to reverse-engineer a *different* face recognition model used by a company or organization
- The attacker inputs images of 12 individuals into the model and recovers personal information from the model's predictions, such as their name, address, or social security number

---

## ML04: Membership Inference Attack

When an attacker wants to gain sensitive information, they utilize a **trained model and a data sample** to select inputs strategically. By examining the model's outputs, the attacker seeks to infer whether that specific sample was part of the model's **training data**.

**Example: Inferencing Financial Data From a Machine Learning Model**
An attacker wants to extract sensitive financial information from a model. They train a machine learning model on a dataset of financial records obtained from a financial organization. Then, they query the model on whether a particular individual's record was included in the training data.

The attack compares the model's confidence output distribution for a **training example** (the model tends to be *very* confident — e.g., 98%/0.7%/0.6%/0.6%/0.2% across output classes) against an **unseen example** (the confidence is noticeably flatter — e.g., 89%/4%/2%/3%/2%). That confidence-distribution difference is exactly what lets the attacker infer membership.

---

## ML05: Model Theft

Model theft attacks occur when an attacker **gains access to the model's parameters**. An attacker steals a competitor's model to gain a competitive advantage and starts using it for their own purposes, reverse-engineers the company's machine learning model either by **disassembling the binary code** or by **accessing the model's training data and algorithm**.

After the attacker has reverse-engineered the model, they use the information to recreate the model and start using it for their own purposes.

### Model Theft Process

1. The attacker collects relevant training data
2. The attacker queries the victim model (Victim A) and obtains query-label pairs (e.g., labeling images as "ship," "car," "cat")
3. Using this labeled data, the attacker trains a clone model (Clone C)
4. The stolen clone becomes the foundation for further attacks: **Adversarial Attack**, **Membership Inference Attack**, or **Model Inversion Attack**

---

## ML06: AI Supply Chain Attacks

**AI supply chain attacks** occur when an attacker compromises a machine learning model and replaces it with a **poisoned model**. These attacks go **unnoticed for a long time**, since the victim may not realize the package they're using has been compromised.

**For example:**
- An attacker compromises a machine learning project by modifying the code of one of the packages it relies on (e.g., NumPy or Scikit-learn)
- In PSK mode, each wireless network device encrypts network traffic using a 128-bit key derived from a passphrase of 8 to 63 ASCII characters
- The attacker uploads the modified version of the package to a public repository (such as PyPI)
- Once the victim downloads and installs the package, the attacker's malicious code — designed to steal sensitive information, modify results, or cause the ML model to fail — is also installed and can be used to compromise the project

The overall pattern mirrors [Part 3's LLM Supply Chain Poisoning](03-attacks-on-llm-applications.md#llm05-supply-chain-vulnerabilities): attacker compromises → uploads poisoned artifact to a public model/package hub → downstream users unknowingly deploy it → the poisoned component (e.g., a compromised chatbot backing a bank's customer service) actively spreads misinformation or steals data from end users.

---

## ML07: Transfer Learning Attack

Transfer learning attacks **exploit the transfer learning process** (training a model on one task and then fine-tuning it on another task) to compromise the security, privacy, or integrity of the target model.

**For example:**
- An attacker wanting to exploit a face-recognition system used for identity verification trains a machine learning model with manipulated images of faces, and transfers that model's "knowledge" into the face-recognition system via fine-tuning
- This is a **weight poisoning attack on pre-trained models**: a clean model has its weights poisoned to create a poisoned model, which is then fine-tuned into a downstream model that carries a hidden backdoor
- This makes the face-recognition system produce incorrect predictions once deployed

---

## ML08: Model Skewing

Model skewing attacks occur when an attacker, to produce specific outcomes, **alters the training data** so the model behaves in an undesirable way — specifically, the attacker attempts to pollute training data to **shift the learned boundary** between what the classifier categorizes as good input and what it categorizes as bad input.

**For example:**
- An attacker wants to increase their chances of getting a loan approved. They attack the machine-learning model used to predict the creditworthiness of loan applicants, and the model's predictions, by manipulating the feedback loop
- The attacker provides fake feedback to the system, suggesting that previously high-risk applicants have been approved for loans. The model's training data is then updated with this modified feedback
- As a result, the model's predictions skew toward low-risk applicants, and the attacker's chances of getting a loan approved are significantly increased

This same skewing technique has a security-specific application: marking specific **malicious binaries as benign**, by gradually shifting the classifier's learned decision boundary through a sustained pattern of poisoned feedback.

---

## ML09: Output Integrity Attack

An **output integrity attack** is one in which an attacker manipulates the model's predictions or classifications to produce inaccurate results — modifying the **output** of a machine learning model (rather than its training data or parameters).

**For example:** an attacker with access to the output of a machine learning model used to diagnose diseases in a hospital modifies the model's output, making it provide incorrect diagnoses for patients. As a result, patients are given incorrect treatments, leading to further harm and potentially even death.

Technically, this is achieved via an **adversarial perturbation** applied at inference time: correctly-labeled testing data (e.g., an image of a "plane") has a small perturbation added, becoming an "adversarial example" that the model outputs as a completely different, incorrect classification (e.g., "car") — despite the underlying training data and model parameters never having been touched.

---

## ML10: Model Poisoning

**Model poisoning attacks** occur when an attacker **alters training data** to cause a model to behave in an undesirable way. Poisoning attacks require modification of training data (either the data samples or their labels) to poison a model at training time, resulting in misclassification on a subset of testing samples.

**Example:** poisoning a bank's machine learning model used to identify and automate the cheque-clearing process.

- The model is trained to identify handwritten characters based on size, shape, slant, and spacing
- An attacker poisons the bank's ML model by altering the images and parameters of the trained model, resulting in the model misidentifying the character "7" as the character "1"
- This results in cheque values being read incorrectly and incorrect amounts being processed

The mechanism spans two connected stages: **Training** (modified data + incorrect labels feed into the training algorithm, producing a poisoned ML model) and **Model Deployment** (the poisoned model then misclassifies a targeted subset of testing data — e.g., confusing "plane" and "bird" — even while performing normally on everything else, making the poisoning hard to detect through ordinary accuracy testing).

---

## Quick-Reference Summary

- **OWASP ML Security Top 10** targets the model itself (training data, parameters, architecture), distinct from the OWASP LLM Top 10's focus on the surrounding application layer
- **ML01 Input Manipulation** = adversarial perturbations at *inference* time (the panda/gibbon example) fool an already-trained model without touching its training data
- **ML02 Data Poisoning** and **ML10 Model Poisoning** both corrupt training data/labels, but ML10 specifically targets a subset of outcomes (e.g., "7" read as "1") while ML02 is the broader category (e.g., spam classifier corruption)
- **ML03 Model Inversion** and **ML04 Membership Inference** both exploit model *outputs* to extract information — inversion reconstructs input-level details (like a face), inference determines whether specific data was in the training set
- **ML05 Model Theft** and **ML06 AI Supply Chain Attacks** both compromise the model as an artifact — theft by reverse-engineering it via queries, supply chain by poisoning it before it's ever deployed
- **ML07 Transfer Learning Attack** exploits the fine-tuning pipeline itself via weight poisoning on pre-trained models
- **ML08 Model Skewing** manipulates feedback loops to shift a classifier's decision boundary over time
- **ML09 Output Integrity Attack** manipulates the *output* directly via adversarial perturbation at inference time, leaving training data and parameters untouched

---

*Part of the CEH Appendix C study series — continues in [Part 5: Protecting LLM Applications](05-protecting-llm-applications.md).*
