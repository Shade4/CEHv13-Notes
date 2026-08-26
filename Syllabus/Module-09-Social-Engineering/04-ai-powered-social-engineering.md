# 04 — AI-Powered Social Engineering

> Exam objective: *Explain various computer-based social engineering techniques* (AI-augmented
> subset — new in CEH v13)

Generative AI has lowered the skill floor for convincing social engineering to almost zero. What
used to require a skilled writer, a voice actor, or a video editor can now be approximated by
anyone with a few minutes and a free-tier chatbot. This file covers the three AI-driven vectors
CEH v13 introduces: **LLM-crafted phishing copy**, **deepfake video impersonation**, and **AI
voice cloning** — plus what actually works to defend against them.

---

## 4.1 Crafting Phishing Emails with LLMs (e.g., ChatGPT)

Large language models can generate grammatically flawless, contextually appropriate, and highly
persuasive phishing copy on demand — removing one of the classic phishing "tells" (bad grammar /
awkward phrasing) almost entirely.

**How attackers use it, conceptually:**
- Ask the model to write as a specific persona (e.g., "a company's IT administrator") with a
  specific call-to-action (e.g., "employees must install a security update via this link by
  Friday").
- Ask for variations at scale — dozens of subject lines and bodies A/B-tested against different
  departments.
- Ask the model to **adapt tone and formality** per target seniority (casual for peers,
  deferential-but-urgent for executives).

**Why it's more dangerous than template-based phishing:**
- Removes spelling/grammar red flags (see checklist in `03`, item #11).
- Scales personalization that used to require manual research per victim.
- Can be regenerated instantly if a campaign gets flagged/blocked, evading static content filters.

### Writing-Style Impersonation
A more advanced abuse: an attacker feeds a model **real prior correspondence** between two people
(scraped from a breach, social media, or a compromised mailbox) and asks it to continue the
conversation *in that exact voice*. Because the model can replicate vocabulary, sentence
complexity, tone, and even idiosyncratic phrasing, the resulting message is far more convincing
than a generic impersonation — the recipient recognizes their friend/colleague's "voice" and
lowers their guard. This is frequently combined with a fabricated emergency (a medical crisis, a
stranded-traveler story) to pressure an urgent wire transfer or gift-card purchase — a modern,
AI-accelerated version of the classic **"grandparent scam"** / business-email-compromise (BEC)
pattern.

> 🛡️ **Defense:** treat *any* urgent financial request delivered only through a single digital
> channel — even one that "sounds exactly like" the person — as unverified until confirmed
> through a **second, independent channel** (a phone call to a known number, an in-person check).
> This single habit defeats nearly all AI writing-style impersonation and voice-cloning scams,
> because the entire attack depends on the victim never verifying out-of-band.

---

## 4.2 Deepfake Video Impersonation

A **deepfake** attack creates falsified video/audio media of a real person using deep learning —
typically **Convolutional Neural Networks (CNNs)** for facial feature extraction and
**Generative Adversarial Networks (GANs)** for synthesizing new, convincing frames. Attackers
source raw material from previously recorded speeches, interviews, stolen account clippings, or
any publicly available footage, then clone it onto a "destination" video to make the target
appear to say or do something they never did.

### How a deepfake is actually built (pipeline)
```
1. SOURCE VIDEO           2. DESTINATION VIDEO        3. TRAINING
   (face to be             (target video the face      Extract + align facial
   deepfaked)              will be inserted into)      landmarks from both;
                                                        train a GAN/autoencoder
                                                        to map source → destination

4. GENERATION                              5. POST-PROCESSING
   Model renders the swapped face           Color-grading, compositing, and
   frame-by-frame across the                motion tracking blend the result
   destination video                        seamlessly with the background
```

### Skills required (why this isn't trivial — yet)
- Deep learning fundamentals: CNNs, GANs, autoencoders.
- Python/scripting ability to preprocess data and tune models.
- Large volumes of source footage/audio and facial landmark data.
- Video-editing proficiency (Adobe Premiere Pro, DaVinci Resolve, Final Cut Pro) for
  post-processing.
- Understanding of compositing, color grading, motion tracking, and rotoscoping to sell the
  illusion.

### Deepfake creation tools (reference — legitimate creative/dubbing tools that are also
dual-use)
| Tool | Source |
|---|---|
| DeepFaceLab | https://www.deepfakevfx.com |
| Vidnoz | https://www.vidnoz.com |
| Deepfakesweb | https://deepfakesweb.com |
| Synthesia | https://www.synthesia.io |
| DeepBrain AI | https://www.deepbrain.io |
| Hoodem | https://hoodem.com |

> Most of these tools are legitimately marketed for dubbing, marketing, and avatar-based video
> production. The line between "AI video tool" and "deepfake attack" is entirely about **consent
> and disclosure** — using someone's likeness without permission to deceive a third party is
> fraud/defamation in most jurisdictions, regardless of which tool produced it.

---

## 4.3 AI Voice Cloning

Voice cloning uses machine learning — **speech synthesis** plus **neural-network-based acoustic
modeling** (often CNNs or RNNs) — to replicate the tone, intonation, and speech patterns of a
target's voice convincingly enough to impersonate them on a call or voice message.

### Pipeline
```
1. Data collection      → gather audio: speeches, interviews, podcasts, social posts
2. Neural network       → train a model (CNN/RNN) on the collected samples to learn
   training               the target's unique vocal characteristics
3. Voice sample          → convert arbitrary text input into speech using the
   generation              learned voice profile
4. Impersonation         → use synthesized audio in phone calls, voicemails, or
                            recordings to authorize transactions or extract data
```

### Voice cloning tools (reference)
| Tool | Source |
|---|---|
| VEED.IO | https://www.veed.io |
| Murf.AI | https://murf.ai |
| Resemble.AI | https://www.resemble.ai |
| ElevenLabs | https://elevenlabs.io |
| PlayHT | https://play.ht |
| voice.ai | https://voice.ai |

Real-world abuse pattern: an attacker clones an executive's voice from a public earnings call or
conference talk, then calls the finance department claiming to be that executive, "authorizing" an
urgent wire transfer — a voice-based evolution of the whaling/BEC attack in `03`.

---

## 4.4 Countermeasure Summary (AI-Specific)

Full defensive detail lives in
[`07-social-engineering-countermeasures.md`](07-social-engineering-countermeasures.md); the
highlights specific to AI-driven attacks:

- **Out-of-band verification** for any request involving money, credentials, or access — call
  back on a known number, don't trust the channel the request arrived on.
- **Code words / shared secrets** for family members or finance teams to confirm identity during
  high-pressure "emergency" calls.
- **Digital watermarking & provenance** — embedding invisible authenticity markers in real media
  at the point of creation (e.g., C2PA content credentials).
- **Deepfake/synthetic-media detection tooling** — AI/ML classifiers that flag unnatural eye
  movement, inconsistent lighting, or flawed lip-sync.
- **Voice biometrics & anti-spoofing** — liveness detection on voice-authenticated systems.
- **Employee awareness training** specifically covering AI-generated pretexts, since traditional
  "check the grammar" advice no longer reliably applies.

---

**Next:** [`05-mobile-based-social-engineering.md`](05-mobile-based-social-engineering.md) →