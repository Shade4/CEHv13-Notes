# 11 — Cryptanalysis Methods and Cryptography Attacks

**Cryptanalysis** is the study of ciphers, ciphertext, and cryptosystems with the goal of finding weaknesses that let you recover plaintext from ciphertext — or recover the key outright — even without legitimate access to the key or algorithm details. Everything in this file is either a *method* for that analysis, a *named attack pattern* built from those methods, or a *tool* that automates them.

## Cryptanalysis methods

### Linear cryptanalysis

Invented by Mitsuru Matsui, this is a **known-plaintext attack** that finds linear approximations describing a block cipher's behavior — expressions that XOR together specific bits of the plaintext, ciphertext, and key, and hold true with probability noticeably different from 50% (if a cipher were a perfect random function, every such expression would hold exactly half the time; any measurable deviation is exploitable). A typical linear expression looks like:

```
P1 ⊕ P3 ⊕ C1 = K2
```

Given enough plaintext/ciphertext pairs, **Matsui's Algorithm 2** counts how often a candidate linear approximation holds across all observed pairs; the partial key value whose count deviates furthest from exactly half the samples is statistically the most likely correct value for those key bits. Full-round DES requires roughly 2⁴³ known plaintexts to break via linear cryptanalysis — dramatically better than the 2⁵⁶ operations a brute-force key search would need, but still impractical for most attackers to actually collect that much known plaintext for a real target.

### Differential cryptanalysis

Invented by Eli Biham and Adi Shamir, applicable to symmetric-key algorithms. Instead of looking at individual bit relationships like linear cryptanalysis, it examines **differences** — you feed the cipher two related plaintexts (differing by a chosen, fixed XOR pattern) and study how that input difference propagates into a difference in the resulting ciphertexts. Originally required a **chosen-plaintext** attack model (the attacker picks the plaintext pairs), but variants now also work against known-plaintext and even ciphertext-only scenarios.

### Integral cryptanalysis

First described by Lars Knudsen, an extension of differential cryptanalysis particularly effective against block ciphers built on substitution-permutation networks. Where differential analysis looks at *pairs* of inputs differing in one bit, integral analysis holds `b-k` bits of a block constant and runs the remaining `k` bits through *all* 2^k possible combinations, then studies statistical properties (like whether the sum of all resulting outputs is always zero) across that entire structured set. At `k=1` this collapses to ordinary differential cryptanalysis; for `k>1` it becomes a genuinely distinct technique.

### Quantum cryptanalysis

Using a quantum computer to break cryptography that's resistant to *classical* cryptanalysis. **Shor's algorithm** efficiently factors large integers and solves discrete logarithms — breaking RSA, DSA, Diffie-Hellman, and ECC essentially outright if run on sufficiently powerful hardware. **Grover's algorithm** provides only a quadratic brute-force speedup against symmetric ciphers and hash functions (e.g., effectively halving AES-256's bit-security to a still-comfortable 128 bits) — a real but far less catastrophic impact than Shor's algorithm has on public-key crypto. Practical quantum cryptanalysis is measured against real resource metrics: **circuit width** (qubits needed), **circuit depth** (time steps needed), **number of (T-)gates**, **T-depth**, and **MAXDEPTH** (the maximum feasible circuit depth given current hardware coherence limits) — all of which are still far beyond what physical quantum computers can sustain for cryptographically relevant key sizes as of 2026, which is *why* PQC migration (see [`12-quantum-attacks-and-countermeasures.md`](12-quantum-attacks-and-countermeasures.md)) is currently a proactive "harvest-now-decrypt-later" defense rather than a response to an already-realized break.

## Code-breaking methodologies

- **Brute force** — try every possible key until the right one is found. Guaranteed to eventually work, purely a question of resources. See the economics table below.
- **Frequency analysis** — exploits the fact that letters (or, in code, tokens like `#define`, `struct`, `else`, `return`) occur with predictable, uneven frequency in any given language or format. If a ciphertext symbol appears with the same frequency as `e` does in ordinary English, it's a strong candidate for actually representing `e`. This is specifically why encrypted **source code** is more vulnerable than encrypted prose — programming languages have an even smaller, more predictable, more repetitive token vocabulary than natural language.
- **Trickery and deceit** — social engineering used to extract keys directly, rather than computing your way to them. Classic example: tricking or bribing someone into encrypting and sending a message whose plaintext you already know, then using that known plaintext/ciphertext pair to crack the key via standard known-plaintext cryptanalysis.
- **One-time pad (OTP)** — the one cipher that's provably, information-theoretically unbreakable *when used correctly*: a truly random, non-repeating key at least as long as the message, used exactly once, with each plaintext character combined (typically XORed) with one key character, then the used portion of the pad is destroyed. The catch is entirely practical rather than cryptographic: the key must be as long as every message ever sent combined, distributed securely in advance, generated with true (not pseudo-) randomness, and never reused — which makes OTP essentially unusable for anything beyond very low-volume, extremely high-value communications (historically: intelligence-agency diplomatic traffic).

## The 12 classic cryptography attack models

These are organized by **what the attacker has access to** — which is the single most useful lens for understanding why some are "easy" (require little from the attacker) and some are "powerful" (require a lot of access, but yield much more).

| Attack | What the attacker has | Goal |
|---|---|---|
| **Ciphertext-only** | Only a collection of ciphertexts | Recover any info about the plaintext or key — the hardest attack model, but also the most realistic (an eavesdropper rarely gets more than this) |
| **Known-plaintext** | Some plaintext blocks + their corresponding ciphertext (and knowledge of the algorithm) | Deduce the key, to decipher *other* messages encrypted with the same key |
| **Chosen-plaintext** | Ability to submit arbitrary plaintexts of the attacker's choosing and observe resulting ciphertexts | Derive the key from many self-chosen plaintext/ciphertext pairs |
| **Adaptive chosen-plaintext** | Same as chosen-plaintext, but each new plaintext can be chosen based on results from *previous* queries | Refine the key-recovery attack interactively, using each result to inform the next query |
| **Chosen-ciphertext** | Ability to submit arbitrary ciphertexts and obtain their decrypted plaintexts | Recover the key from chosen ciphertext/plaintext pairs. Two named variants: **Lunchtime/Midnight attack** (only limited-time or limited-query access to the decryption oracle) and **Adaptive chosen-ciphertext attack** (later ciphertext choices depend on earlier results) |
| **Related-key attack** | Ciphertexts encrypted under two or more keys that are *mathematically related* to each other (not identical, not independent) | Exploit the known relationship between keys — realistic in systems like WEP where subsequent keys are derived from previous ones in a predictable way (see the WEP/RC4 case study below) |
| **Dictionary attack** | A precompiled dictionary of plaintext/ciphertext pairs gathered over time | Look up an intercepted ciphertext against the dictionary to instantly recover its plaintext, key, or passphrase |
| **Rubber hose attack** | Physical access to a person who knows the key | Extract the key or password through coercion or torture rather than any mathematical technique — a reminder that operational/physical security is part of the threat model, not just algorithm strength |
| **Chosen-key attack** | Some structural leverage that lets the attacker manipulate key relationships | Break an n-bit key cipher in roughly 2^(n/2) operations by exploiting chosen relationships between candidate keys, rather than a full 2^n exhaustive search |
| **Timing attack** | Ability to repeatedly measure the *exact execution time* of cryptographic operations (especially modular exponentiation) | Infer secret key bits from timing variance — since real hardware doesn't execute every operation in perfectly constant time unless deliberately engineered to |
| **Man-in-the-middle (MITM)** | Position on the communication path between two parties during key exchange | Intercept and potentially alter the negotiation of cryptographic parameters, decrypt traffic, and inject data — primarily targets **public-key** systems where key exchange happens before communication, since there's no pre-shared secret to authenticate the exchange against |

## Brute-force attack economics

Brute force is "guaranteed but expensive" — success depends on key length, the resources available to the attacker, and whether the target system has any lockout mechanism after repeated failed attempts. **Every additional bit of key length doubles the brute-force search space**, which is why key-length choices matter so much more than they might intuitively seem to.

| Attacker budget | 40-bit key (5 char) | 56-bit key (7 char) | 64-bit key (8 char) | 128-bit key (16 char) |
|---|---|---|---|---|
| $2K (achievable by an individual, 1 PC) | 1.4 minutes | 73 days | 50 years | 10²⁰ years |
| $100K (achievable by a company) | 2 seconds | 35 hours | 1 year | 10¹⁹ years |
| $1M (achievable by a large org/state) | 0.2 seconds | 3.5 hours | 37 days | 10¹⁸ years |

The practical conclusion: **128-bit keys (and larger) remain brute-force-infeasible against any realistic classical adversary**, which is exactly why AES-128 is still considered acceptable for most purposes, while DES's 56-bit keys have been comfortably brute-forceable for decades.

## Birthday attack and the birthday paradox

A class of brute-force attack against **hash collisions**, and it's dramatically more efficient than naive intuition suggests, which makes it worth walking through the actual math.

**The paradox itself:** how many people need to be in a room before there's a better-than-even chance that two of them share a birthday (same day and month, not year)? Intuitively many people guess something close to 183 (half of 365). The real answer is **23**.

**Why:** the probability that the *first* person has a unique birthday is trivially 100% (365/365, no one to conflict with yet). The probability the *second* person's birthday also doesn't match the first is 364/365. The third not matching either preceding person is 363/365, and so on down to the 23rd person facing 343/365 odds of no conflict with any of the 22 before them. Multiplying all these independent probabilities together:

```
365/365 × 364/365 × 363/365 × ... × 343/365 ≈ 0.49
```

That's the probability of **no** shared birthday among 23 people — meaning there's roughly a **51%** chance that at least two *do* share one. The key insight is that you're not checking one person against a fixed target; you're checking every pair among the group against every other pair, and the number of pairs grows much faster (~n²) than the number of people (~n).

**Applying this to hashes:** the same math applies to finding *any* two inputs producing the same hash output (a collision), rather than checking a hash against one specific fixed target (which is the much harder preimage-resistance problem). For a hash with an *n*-bit output, guaranteeing a collision by brute force alone would take up to 2ⁿ attempts — but thanks to the birthday effect, you only need roughly **√(2ⁿ)**, or about **1.25 × √(2ⁿ)**, attempts to find *some* collision with better-than-even odds.

For MD5 (128-bit output): guaranteeing a collision by exhaustive search would need up to 2¹²⁸ ≈ 3.4 × 10³⁸ attempts. Via the birthday attack, only around **1.174 × √(2¹²⁸) ≈ 2.17 × 10¹⁹** hashes are needed — still a large number, but many, many orders of magnitude smaller than exhaustive search, and (combined with MD5's additional structural weaknesses) well within reach of dedicated attackers, which is exactly why practical MD5 collisions have been publicly demonstrated. **This is also precisely why cryptographic hash outputs need to be roughly double the bit-length that a preimage-resistance-only threat model would require** — a 128-bit hash gives only ~64 bits of *collision* resistance, not 128.

## Hands-on lab: brute-forcing VeraCrypt encryption with `dd` and `hashcat`

This is a real, reproducible workflow for attacking a password-protected VeraCrypt container — useful both for understanding attacker tradecraft and for testing your own container's passphrase strength defensively. (Naturally, only run this against systems/containers you own or are explicitly authorized to test.)

**Step 1 — extract the container's header hash.** VeraCrypt containers store their key-derivation header in the first 512 bytes. Pull just that header out with `dd`:

```bash
dd.exe if=<path_to_container> of=<path_to_hashfile.tc> bs=512 count=1
```

Example, extracting from a container at `E:\encrypted\target` and saving the extracted header to `target_hash.tc`:

```
C:\Users\Admin\Desktop\dd>dd.exe if=E:\encrypted\target of=E:\encrypted\target_hash.tc bs=512 count=1
rawrite dd for windows version 0.4beta4.
Written by John Newbigin <jn@it.swin.edu.au>
This program is covered by the GPL. See copying.txt for details
1+0 records in
1+0 records out
```

The resulting `target_hash.tc` file is exactly 512 bytes — this is the material `hashcat` needs to attempt password recovery against.

**Step 2 — crack it with `hashcat`.** VeraCrypt containers correspond to hashcat hash-mode `13721` (VeraCrypt SHA512 + XTS 512-bit — hashcat has separate mode numbers for VeraCrypt's other hash/cipher combinations, so check `hashcat --help | grep -i veracrypt` if the target used different settings).

*Mask attack* (brute-forcing every possible 4-digit numeric PIN, `?d?d?d?d`):

```bash
hashcat.exe -a 3 -w 1 -m 13721 <path_to_hashfile.tc> ?d?d?d?d
```

- `-a 3` — attack mode 3 (brute-force / mask attack)
- `-w 1` — workload profile, 1 (low) through 4 (high) — higher values push the GPU/CPU harder
- `-m 13721` — hash mode identifying the target as a VeraCrypt SHA512+XTS-512 container
- `?d?d?d?d` — the mask itself; each `?d` represents one unknown numeric digit (0–9), so this mask covers exactly the 10,000 possible 4-digit PINs

A successful crack shows a `Status: Cracked` result along with the recovered password appended after the hash:

```
Status...........: Cracked
Hash.Name........: VeraCrypt SHA512 + XTS 512 bit
Hash.Target......: ..\encrypted\target_hash.tc
..\encrypted\target_hash.tc:9898
```

(Here, `9898` is the recovered 4-digit password.)

*Dictionary/wordlist attack* (trying every entry from a wordlist instead of brute-forcing digits):

```bash
hashcat.exe -w 1 -m 13721 hash.tc wordlist.txt
```

**Why this matters defensively:** this exact workflow is precisely why VeraCrypt (and disk encryption generally — see [`09-disk-encryption.md`](09-disk-encryption.md)) is only as strong as the passphrase protecting it. A short numeric PIN, as demonstrated here, falls to a mask attack in minutes on modern GPU hardware. A long, high-entropy passphrase makes the equivalent brute-force search computationally infeasible using exactly the math from the brute-force economics table above.

## Meet-in-the-middle attack

Targets ciphers/schemes using **multiple sequential encryption keys** (e.g., naive double-DES), and it's the reason double encryption doesn't give you the full combined key strength you might expect. It's related to the birthday attack in that it trades memory for time.

**Worked example** (double-DES, plaintext `"John"` encrypting to ciphertext `"AvBr"` under two 56-bit keys):

1. The attacker brute-forces **key1** across all 2⁵⁶ possible values, encrypting `"John"` with each candidate key1, and stores every resulting intermediate ciphertext in a lookup table alongside the key1 value that produced it.
2. The attacker separately brute-forces **key2** across all 2⁵⁶ possible values, this time *decrypting* `"AvBr"` with each candidate key2.
3. Each decryption result from step 2 is checked against the stored table from step 1. When a match is found — the same intermediate value appears in both the forward-encrypted table and a backward-decrypted result — the attacker has found a valid (key1, key2) pair.

Total cost: at most 2⁵⁶ + 2⁵⁶ = 2⁵⁷ operations — dramatically less than the naive 2¹¹² (2⁵⁶ × 2⁵⁶) an attacker might assume double-key encryption would require, because the attack **meets in the middle** rather than exhaustively trying every key1/key2 combination together. This exact weakness is why **3DES uses three keys with an encrypt-decrypt-encrypt structure** rather than simple double-DES — the extra key stage specifically raises the meet-in-the-middle cost back up to a level that's actually secure (see [`02-symmetric-encryption-algorithms.md`](02-symmetric-encryption-algorithms.md)).

## Side-channel attacks

A **physical** attack against a cryptographic device or system — instead of attacking the mathematics of the algorithm at all, the attacker monitors unintended physical "leakage" from the hardware actually running it. Cryptography is ultimately implemented on real semiconductors (resistors, transistors), and those physical components interact measurably with their environment in ways that can betray secret information.

| Channel | What's measured | Notes |
|---|---|---|
| **Power consumption** | Instantaneous power draw during cryptographic operations | Two flavors: **Simple Power Analysis (SPA)** reads instruction-level timing and input/output values directly off a power trace; **Differential Power Analysis (DPA)** needs no knowledge of the algorithm's implementation details at all — it applies statistical analysis across many traces to correlate power variance with secret key bits |
| **Electromagnetic field** | EM radiation naturally emitted by active computer components | Correlating EM field variation over a chip's surface with underlying computation/data can leak information without any physical contact with the device at all |
| **Light emission** | Optical radiation from LED status indicators, or even a monitor's diffuse reflection off a nearby wall | Research (Loughry and Umphress) has shown data being processed can be inferred from LED status-light behavior; separately, CRT signal content has been reconstructed purely from the diffuse light it casts on a wall |
| **Timing and delay** | Variance in how long an operation takes to complete | Performance-optimized code often doesn't execute in constant time — if that time varies based on secret data, an attacker measuring execution time across many queries can statistically infer the secret (this is exactly the mechanism behind the "timing attack" entry in the 12-attack table above) |
| **Sound (acoustic)** | Sound produced by a computer's internal components (CPU coil whine, keyboard keystrokes) during computation | Acoustic cryptanalysis has been demonstrated recovering RSA key bits purely from a computer's coil whine during decryption |

Side-channel attacks are fundamentally different from brute-force or mathematical cryptanalysis — they depend on **how** a system implements an algorithm, not on any weakness in the algorithm itself, which means even a mathematically unbreakable cipher can leak its key through a careless hardware or software implementation.

**Mitigations:** implement fixed-time algorithms with no data-dependent delays; mask/blind intermediate values with random nonces during computation; add deliberate amplitude/temporal noise to reduce the attacker's signal-to-noise ratio; use differential-power-analysis-resistant protocols and rotate keys before leakage accumulates meaningfully; pre-charge registers/busses to eliminate predictable transition signatures; use signal-attenuating display/enclosure materials to block EM emission; employ blinding techniques that randomize inputs/outputs; isolate sensitive operations in dedicated hardware (HSMs, secure enclaves, physically unclonable functions); apply cache partitioning/locking; integrate real-time monitoring and error-detection/correction to catch induced faults; and follow relevant standards from NIST, ISO, or IEC that codify these practices for a given hardware class.

## Hash collision attack

Finds two different input messages that produce the identical hash output — `hash(a1) = hash(a2)`, where neither `a1` nor `a2` is under the attacker's full control ahead of time (the goal is to find *some* colliding pair, not to force a collision with an attacker-chosen target — that would be the strictly harder second-preimage problem covered in [`04-hashing-and-message-digests.md`](04-hashing-and-message-digests.md)). The classic target is **SHA-1**, once ubiquitous as a digital-signature hash function: since SHA-1 converts any input into a fixed-length "fingerprint," an attacker who finds two messages sharing a fingerprint can potentially get a victim to sign message `a1` (thinking it's benign) and then present that identical signature as valid for message `a2` (which might be malicious) — because the signature only ever certified the *hash*, and both messages hash identically. Once one collision is found, an attacker can often generate further colliding pairs by concatenating additional matching data onto both messages.

## DUHK attack (Don't Use Hard-coded Keys)

A cryptographic implementation vulnerability — not a break of any algorithm — that lets an attacker obtain the encryption keys securing VPNs and web sessions on affected devices. It specifically targets hardware/software using the **ANSI X9.31 pseudorandom number generator (RNG)**: PRNGs generate seemingly random bit sequences from an initial secret **seed** value plus current internal state, but if that seed is **hardcoded** into a product's firmware/software rather than generated fresh per device, an attacker who obtains the seed (e.g., by extracting it from publicly available firmware) can combine it with knowledge of the RNG algorithm to reconstruct every key that device has ever derived — completely defeating the encryption regardless of key length. MITM attackers specifically use DUHK to learn the seed value, observe the current session state, and reconstruct session keys on the fly, exposing business data, credentials, and payment details in transit. **The lesson generalizes well beyond this one CVE-class:** any hardcoded or predictable random-number-generator seed anywhere in a cryptographic system undermines every key ever derived from it, no matter how strong the downstream algorithm is — see also the DSA per-signature nonce requirement in [`03-asymmetric-encryption-algorithms.md`](03-asymmetric-encryption-algorithms.md), which fails for exactly the same underlying reason.

## DROWN attack (Decrypting RSA with Obsolete and Weakened eNcryption)

A **cross-protocol** vulnerability affecting HTTPS and other services relying on SSL/TLS — a new variant of the older Bleichenbacher padding-oracle attack against RSA. A server is critically vulnerable if it still permits **SSLv2** connections (often due to misconfiguration or leftover default settings) **and** reuses the same private-key certificate on any other server that also allows SSLv2. The attacker sends malicious SSLv2 probes against the SSLv2-enabled server to exploit weaknesses specific to that obsolete protocol, and — because the *private key* is shared — uses information leaked from those probes to decrypt intercepted **TLS** traffic to the modern server, even though the modern server itself never spoke SSLv2 to anyone. DROWN is typically executed as part of a broader online MITM attack, ultimately exposing passwords, financial data, and any other traffic riding that TLS connection, and can let an attacker impersonate the legitimate site or alter its content.

**Defense is straightforward and absolute: disable SSLv2 (and SSLv3) entirely, everywhere, and never share a private key between a hardened server and any server that still permits legacy protocols.**

## Rainbow table attack

Uses a **precomputed table** mapping candidate plaintexts (dictionary words, common passwords, brute-force-generated strings) to their corresponding hash values, applying a **cryptanalytic time-memory trade-off**: instead of computing hashes on the fly for every guess during an attack (time-expensive) or storing every possible plaintext/hash pair in a flat list (impractically memory-expensive), rainbow tables use chained reduction functions to compress a huge search space into a much smaller table that can still recover the original plaintext for a captured hash with one lookup. An attacker captures a password hash, checks it against the precomputed rainbow table, and — if found — instantly recovers the plaintext without any further computation.

**The single most effective defense against rainbow tables is salting** — appending a unique, random value to each password before hashing it, so that even identical passwords produce different hashes across different accounts/systems, which makes precomputed tables useless (an attacker would need a separate table per possible salt value, which defeats the entire point of precomputation). See key stretching and salting in [`12-quantum-attacks-and-countermeasures.md`](12-quantum-attacks-and-countermeasures.md).

## Related-key attack — WEP/RC4 case study

The related-key attack (from the 12-attack table above) has a well-documented real-world instance worth understanding in detail: **WEP** (Wired Equivalent Privacy), the original Wi-Fi encryption standard. WEP uses the **RC4** stream cipher (see [`02-symmetric-encryption-algorithms.md`](02-symmetric-encryption-algorithms.md)), and stream ciphers have a hard requirement — the same key/keystream must never be reused. To try to satisfy this, WEP prepends a 24-bit **initialization vector (IV)** to the shared WEP key for every packet, so the actual RC4 key used per-packet is technically always slightly different.

The problem: a 24-bit IV space is small — only about 16.7 million possible values — and, thanks to the **birthday paradox** covered above, two packets sharing the same IV (and therefore the same effective RC4 key) become statistically likely after only around **4096 packets**, not 16.7 million. On any moderately busy network, that many packets pass in minutes. Once an attacker captures two packets that reused the same IV, they can XOR the two ciphertexts together to cancel out the shared keystream and recover information about both plaintexts directly — this "IV collision" weakness, combined with additional statistical biases in RC4's keystream, is what makes WEP practically breakable in minutes with widely available tools, and is exactly why WEP was formally deprecated and replaced first by WPA (a stopgap using the same RC4 core with better key management) and then WPA2/WPA3 (which drop RC4 entirely in favor of AES).

## Padding oracle attack (Vaudenay attack)

Exploits **padding validation** in block ciphers using CBC mode (see [`01-cryptography-fundamentals.md`](01-cryptography-fundamentals.md)) to decrypt — and in some configurations even forge — ciphertext, without ever having the encryption key. Block ciphers require plaintext to be padded out to a multiple of the block size; "padding oracle" refers to any system component that reveals, even indirectly, whether a given ciphertext's padding was valid after decryption.

**The core exploit condition:** if a server, upon decryption failure, distinguishes between "padding was invalid" (e.g., returning an error like `Decryption failure: Invalid Padding`) and any other kind of failure (returning a generic `Decryption failed` message instead) — an attacker can systematically manipulate ciphertext bytes, submit the modified ciphertext, and use the server's differing error responses as an **oracle** that leaks one byte of plaintext at a time, eventually recovering the entire message without ever needing the actual encryption key. This is precisely the underlying flaw that made attacks like **POODLE** (against SSLv3) and **Lucky Thirteen** (against TLS CBC-mode ciphers) practical.

**Defense:** never let error-handling logic distinguish padding failures from other decryption failures in any externally observable way (identical generic error message, and ideally identical response timing, for every failure mode) — or better yet, avoid CBC-mode-without-authentication entirely and use an AEAD mode like AES-GCM (see [`01-cryptography-fundamentals.md`](01-cryptography-fundamentals.md)), which authenticates ciphertext *before* attempting decryption, so a tampered ciphertext is rejected outright with no padding-related information ever leaking in the first place.

## Cryptanalysis tools

| Tool | Source | Notes |
|---|---|---|
| **CrypTool** | cryptool.org | The most complete free cryptanalysis learning/practice suite, split across four sub-projects: **CT1** (Windows, C++, classical + modern algorithm cryptanalysis — Vigenère, RSA, AES, etc.), **CT2** (Windows, visual drag-and-drop cryptographic-procedure builder), **JCT** (JCrypTool — cross-platform Linux/macOS/Windows, extensible with custom crypto plug-ins), **CTO** (CrypTool-Online — runs entirely in-browser) |
| RsaCtfTool | github.com | Automates common RSA CTF-style attacks (weak/related keys, small exponent, common modulus, etc.) |
| Msieve | sourceforge.net | General number field sieve implementation for integer factorization |
| Cryptol | cryptol.net | A DSL and toolchain for specifying and verifying cryptographic algorithms |
| CryptoSMT | github.com | SMT-solver-based tool for automated differential/linear cryptanalysis of symmetric primitives |
| MTP | github.com | Cryptanalysis/verification utility |

For a compact, scannable summary of every attack covered in this file, see [`cheatsheets/crypto-attacks-quick-reference.md`](cheatsheets/crypto-attacks-quick-reference.md).

Next: [`12-quantum-attacks-and-countermeasures.md`](12-quantum-attacks-and-countermeasures.md) — the quantum-specific attack surface, plus the full defensive playbook for everything covered across this repo.
