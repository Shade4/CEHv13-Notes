# Cheatsheet — Social Engineering Technique Quick Reference

One-line lookups for every named technique in this module. Built for rapid exam review — if you
can match a CEH scenario question to the right row here, you're set.

## Human-Based

| Technique | One-liner |
|---|---|
| Impersonation | Pretending to be someone legitimate/authorized, in person or via a comms medium |
| Vishing | Voice/VoIP-based impersonation to extract info over the phone |
| Eavesdropping | Unauthorized interception of a conversation or communication |
| Shoulder Surfing | Directly observing someone entering credentials/PINs |
| Dumpster Diving | Searching trash for discarded sensitive information |
| Reverse Social Engineering | Attacker engineers a problem so the **victim** approaches **them** for help |
| Piggybacking | Authorized person **knowingly** lets an unauthorized person through a secure door |
| Tailgating | Attacker follows an authorized person through a door **without** their knowledge/consent |
| Diversion Theft | Tricking a delivery person into sending goods/data to the wrong place |
| Honey Trap | Fake online romantic relationship used to extract confidential info |
| Baiting | Leaving an infected physical device (USB) somewhere enticing |
| Quid Pro Quo | "Something for something" — fake tech support offers help in exchange for credentials |
| Elicitation | Extracting info via normal, disarming conversation rather than direct questioning |
| Bait and Switch | Exciting offer/link lures a click, then the attacker executes the real (malicious) goal |

## Computer-Based

| Technique | One-liner |
|---|---|
| Phishing | Illegitimate email/message claiming legitimacy, harvesting info via a fake site/link |
| Spear Phishing | Phishing targeted at a specific person/small group with tailored content |
| Whaling | Phishing targeted at high-profile executives |
| Pharming | Redirects traffic to a fake site via DNS cache poisoning or hosts-file modification — no click needed |
| Spimming (SPIM) | Spam sent over Instant Messaging platforms via bots |
| Clone Phishing | Near-identical replica of a real, previously-sent email with a swapped malicious link/attachment |
| E-wallet Phishing | Phishing targeting digital-wallet users specifically |
| Tabnabbing | A background tab rewrites itself into a fake login page while you're focused elsewhere |
| Reverse Tabnabbing | The *new* tab you opened rewrites the *original* tab into a phishing page via `window.opener` |
| Consent Phishing | Abuses OAuth consent screens to gain account access without stealing a password |
| Search Engine Phishing | SEO manipulation ranks malicious sites highly in search results |
| Pop-Up Windows | Fake login/error pop-ups trick users into re-entering credentials |
| Hoax Letters | Emails warning of a non-existent virus threat |
| Chain Letters | "Forward this for a reward" messages that spread via social pressure |
| Instant Chat Messenger | Attacker chats up a victim to casually extract personal details |
| Spam Email | Unsolicited bulk email seeking financial/personal data |
| Scareware | Fake "your PC is infected" pop-ups pushing malicious downloads/purchases |

## AI-Powered

| Technique | One-liner |
|---|---|
| LLM-Crafted Phishing | AI-generated phishing copy — grammatically flawless, highly persuasive, scalable |
| Writing-Style Impersonation | AI mimics a real person's exact writing voice from sample text |
| Deepfake Video | GAN/CNN-generated fake video impersonating a real person |
| AI Voice Cloning | Neural-network-synthesized speech mimicking a real person's voice |

## Mobile-Based

| Technique | One-liner |
|---|---|
| Publishing Malicious Apps | Fake app with a popular-sounding name/icon published to an app store |
| Repackaging Legitimate Apps | Real app decompiled, infected with malware, and re-uploaded elsewhere |
| Fake Security Applications | Malware prompts install of a fake "security app" that intercepts 2FA codes |
| SMiShing | SMS-based phishing driving instant action (call/click/download) |
| QRLJacking | Hijacking a "login via QR code" session by relaying a cloned, live QR code |

## Social Media & Identity

| Technique | One-liner |
|---|---|
| Angler Phishing | Fake brand support account replies to public complaints with a malicious link |
| Catfishing | Fake profile built from a stolen identity to build fraudulent relationships |
| Identity Theft | Using another person's PII to commit fraud or other crimes |

## The 8 Behavioral Levers (Why People Fall For It)

`Authority` · `Intimidation` · `Consensus/Social Proof` · `Scarcity` · `Urgency` ·
`Familiarity/Liking` · `Trust` · `Greed`

*(Maps onto Cialdini's principles of influence: Authority, Social Proof, Scarcity, Liking,
Reciprocity, Commitment/Consistency, Unity — see `01.4`.)*

## The 4-Phase SE Attack Lifecycle

`Research the Company` → `Select a Target` → `Develop a Relationship` → `Exploit the Relationship`

## Types of Identity Theft (memory list)

`Child` · `Criminal` · `Financial` · `Driver's License` · `Insurance` · `Medical` · `Tax` ·
`Identity Cloning & Concealment` · `Synthetic` · `Social Security`