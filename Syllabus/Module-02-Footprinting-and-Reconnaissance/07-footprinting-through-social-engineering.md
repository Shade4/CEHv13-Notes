# Module 2: Footprinting and Reconnaissance
## Part G — Footprinting Through Social Engineering

[← Back to Part F: Network and Email Footprinting](06-network-and-email-footprinting.md) | [Next: Footprinting Tools and AI-Powered Automation →](08-footprinting-tools-and-ai-automation.md)

---

## Table of Contents

1. [What Is Footprinting Through Social Engineering?](#what-is-footprinting-through-social-engineering)
2. [What Social Engineers Are After](#what-social-engineers-are-after)
3. [Core Social Engineering Techniques](#core-social-engineering-techniques)
4. [Collecting Information Through Social Engineering on Social Networking Sites](#collecting-information-through-social-engineering-on-social-networking-sites)
5. [Quick-Reference Summary](#quick-reference-summary)

---

## What Is Footprinting Through Social Engineering?

Everything covered so far in this module — search engines, internet research services, social networking sites, Whois, DNS, network, and email footprinting — relies on online resources or tools. **Footprinting through social engineering** is different: it's the art of obtaining information directly from *people*, by exploiting their weaknesses rather than a system's.

**Social engineering** is a non-technical process in which an attacker misleads a person into inadvertently handing over confidential information — the target has no idea anything is being stolen from them. The whole technique depends on the gullible nature of people and their basic willingness to be helpful. An attacker's first move is always to gain the confidence of an authorized user, and only then mislead that user into revealing something confidential.

The end goal of social engineering is to obtain the needed information and then use it for malicious purposes — unauthorized system access, identity theft, industrial espionage, network intrusion, fraud, and more.

---

## What Social Engineers Are After

- Credit card details and social security numbers
- Usernames and passwords
- Security products in use
- Operating systems and software versions in use
- Network layout information
- IP addresses and server names

---

## Core Social Engineering Techniques

Social engineering shows up in many forms — eavesdropping, shoulder surfing, dumpster diving, impersonation, tailgating, third-party authorization, piggybacking, reverse social engineering, and more. The four most fundamental are worth understanding in depth:

### Eavesdropping

The unauthorized interception of any form of communication — audio, video, or text — without the consent of the communicating parties. This includes reading confidential messages off instant messaging apps or fax transmissions. An attacker gains information here simply by tapping phone conversations or intercepting written/audio/video communications directly.

### Shoulder Surfing

Secretly observing a target to capture critical information — an attacker stands behind the victim and watches their screen activity: keystrokes, passwords, PINs, account numbers, credit card details. It's especially effective in crowded places, where it's easy to stand behind someone and watch without them noticing.

### Dumpster Diving

Also known as **trashing** — rummaging through an organization's garbage bins for valuable information: phone bills, contact information, financial records, operations-related documents, printouts of sensitive information, sticky notes left at users' desks. Attackers may also pull account information straight out of ATM trash bins. All of this can feed directly into further attacks.

### Impersonation

Pretending to be a legitimate or authorized person — in person, or over the phone or another communication medium — specifically to mislead a target into revealing information. An attacker might impersonate a courier/delivery person, a janitor, a businessman, a client, a technician, or simply a visitor. Using this cover, they can scan terminals for visible passwords, search documents left out on desks, rummage through bins, overhear confidential conversations, or even shoulder-surf — all under the guise of a plausible, non-threatening identity.

---

## Collecting Information Through Social Engineering on Social Networking Sites

This builds directly on [Part D](04-footprinting-through-social-networking-sites.md), which covered passively browsing public social media content. Here, the attacker takes an *active* role: using social engineering tricks to gather sensitive information rather than simply reading what's public.

A common pattern: an attacker creates a **fake profile**, then uses that false identity to lure employees into revealing sensitive information — collecting details about employees' interests specifically so those interests can be used as bait. On social networking sites, people commonly post personal details — date of birth, education, employment background, spouse's name — while organizations post information such as potential partners, upcoming news, and company websites. Since there are no real barriers stopping an attacker from accessing the public pages of a social networking account, the fake-profile approach is specifically aimed at getting past whatever *is* private: sending a friend request from the fake account, and if the target accepts, gaining access to their restricted pages too.

### What an Attacker Gets From User Activity

| What Users Do | What Attacker Gets |
|---|---|
| Maintain profile | Contact info, location, and related information |
| Connect to friends, chat | Friends list, friends' info, and related information |
| Share photos and videos | Identity of family members, interests, and related information |
| Play games, join groups | Interests |
| Create events | Activities |

### What an Attacker Gets From Organizational Activity

| What Organizations Do | What Attacker Gets |
|---|---|
| User surveys | Business strategies |
| Promote products | Product profile |
| User support | Social engineering opportunities |
| Recruitment | Platform/technology information |
| Background checks to hire employees | Type of business |

A profile generally contains a person's name, contact information (phone, email), friends' information, family details, interests, and activities. Attackers can gather sensitive information through chats with connected "friends," and if privacy settings on photo/video albums aren't locked down, attackers can view and mine that shared media directly. Tracking group memberships reveals interests, which attackers use to mislead a target into revealing even more — and tracking event pages reveals a target's upcoming activities and schedule.

---

## Quick-Reference Summary

- **Footprinting through social engineering** = extracting information from people, not systems, by exploiting human trust and carelessness
- **What's targeted**: credentials, card/SSN data, security-product details, OS/software versions, network layout, IPs and server names
- **4 core techniques**: eavesdropping (intercepting communication), shoulder surfing (watching screens/keystrokes), dumpster diving (mining trash), impersonation (posing as a legitimate person)
- **On social networking sites specifically**: fake profiles + friend requests are the standard technique for turning public browsing into access to *private* content
- **User activity → attacker intel**: profile maintenance, friend connections, shared media, groups, and events each map to a specific category of exploitable information
- **Organizational activity → attacker intel**: surveys, product promotion, support, recruitment, and background checks each leak a different category of business intelligence

---

*Part of the CEH Module 2 study series — continues in [Part H: Footprinting Tools and AI-Powered Automation](08-footprinting-tools-and-ai-automation.md).*
