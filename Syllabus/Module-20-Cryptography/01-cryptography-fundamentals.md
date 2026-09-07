# 01 — Cryptography Fundamentals

## What cryptography actually is

The word comes from the Greek *kryptos* ("hidden") and *graphia* ("writing") — literally, the art of secret writing. In modern usage it means something a bit broader: the practice of transforming information (**plaintext**) into a form that is unreadable to anyone without the right secret (**ciphertext**), and back again, using a mathematical procedure (an **algorithm** or **cipher**) combined with a **key**.

```
Plaintext  --[Encryption + Key]-->  Ciphertext  --[Decryption + Key]-->  Plaintext
```

Cryptography is not just "make data unreadable." A cryptosystem is judged against four distinct security goals, and a design that only satisfies one of them is usually incomplete:

| Goal | What it guarantees | Typical mechanism |
|---|---|---|
| **Confidentiality** | Only authorized parties can read the data | Encryption (symmetric or asymmetric) |
| **Integrity** | The data hasn't been altered, accidentally or maliciously | Hash functions, MACs |
| **Authentication** | The data (or the party sending it) is genuinely who/what it claims to be | Digital signatures, MACs, certificates |
| **Non-repudiation** | The sender can't later deny having sent the message | Digital signatures |

A system can encrypt data perfectly (confidentiality) while still letting an attacker flip bits in transit undetected (no integrity), or letting anyone with the shared key forge a message and claim someone else sent it (no authentication/non-repudiation with a symmetric-only design). This is why real-world protocols like TLS combine multiple primitives rather than relying on encryption alone — see [`01` → authenticated encryption](#authenticated-encryption) below, and the full protocol writeup in [`07-pki-digital-signatures-ssl-tls.md`](07-pki-digital-signatures-ssl-tls.md).

## Symmetric vs. asymmetric encryption

This is the single most important classification in the whole module — nearly every algorithm and protocol downstream is one or the other, or a hybrid of both.

### Symmetric (secret-key / private-key) encryption

One key encrypts *and* decrypts. Sender and receiver must already share that key through some secure channel before any message can be sent.

```
Plaintext --[Secret Key]--> Ciphertext --[same Secret Key]--> Plaintext
```

**Strengths:** fast, low CPU/memory overhead, cheap to implement in hardware (ASICs), scales well to bulk data.
**Weaknesses:** the key-distribution problem — you need a secure channel to share the key in the first place, which is circular if the insecure channel is the only channel you have. Doesn't scale well either: *n* people who all need to talk to each other privately need on the order of *n(n-1)/2* pairwise keys. No non-repudiation, because both parties hold the identical key — either one could have generated a given ciphertext.

### Asymmetric (public-key) encryption

Two mathematically related keys: a **public key** anyone can have, and a **private key** only the owner holds. What one key encrypts, only the other can decrypt.

```
Plaintext --[Receiver's PUBLIC key]--> Ciphertext --[Receiver's PRIVATE key]--> Plaintext
```

**Strengths:** solves the key-distribution problem (public keys can be published openly), enables digital signatures and therefore non-repudiation, no need to pre-share a secret.
**Weaknesses:** computationally expensive — 100–1000x slower than symmetric ciphers for the same amount of data — and vulnerable to MITM if you can't verify *whose* public key you actually have (this is exactly the problem PKI in [`07`](07-pki-digital-signatures-ssl-tls.md) exists to solve).

| | Symmetric | Asymmetric |
|---|---|---|
| Speed | Fast | Slow (100–1000×) |
| Key count for *n* users | ~n²/2 pairwise keys | 2 keys per user (1 public, 1 private) |
| Key distribution | Hard — needs a secure channel | Easy — public keys are, well, public |
| Confidentiality if key leaks | Total compromise, both directions | Only messages *to* that identity are exposed |
| Non-repudiation | No | Yes |
| Typical use | Bulk data encryption | Key exchange, digital signatures, identity |

**In practice almost nothing uses pure asymmetric encryption for bulk data.** Real protocols use a **hybrid** approach: asymmetric crypto to securely exchange a random symmetric session key, then symmetric crypto (fast) to actually encrypt the data. TLS, PGP, and GPG all work exactly this way — see [`08-email-encryption.md`](08-email-encryption.md) for PGP's version of this pattern in detail.

## Government Access to Keys (GAK) and key escrow

GAK is the (still politically contentious) idea that governments should have a statutory right to obtain the cryptographic keys used by individuals and companies, generally justified as necessary for lawful-intercept and criminal investigation. The common technical mechanism proposed for this is **key escrow** — a trusted third party (often a government agency, sometimes a court-supervised custodian) holds a copy of keys and only releases them under a warrant.

The unresolved tension: escrow agents typically don't know *what* a given key protects, so they can't judge how much protection that key deserves, and a single compromised escrow key can expose everything it was ever used to protect. This is a policy debate as much as a technical one, and it resurfaces periodically (e.g., "clipper chip" in the 1990s, ongoing "going dark" debates about end-to-end encrypted messaging today) — worth knowing the term even outside the exam context.

## Ciphers: classical vs. modern

A **cipher** is the specific algorithm — the well-defined sequence of steps — used to turn plaintext into ciphertext and back. "Encipherment" = encrypt, "decipherment" = decrypt.

### Classical ciphers

Operate directly on the 26 letters of the alphabet, historically executed by hand or simple mechanical devices. Two families:

- **Substitution ciphers** — replace units of plaintext (single letters, pairs, or blocks) with different ciphertext units according to a fixed system. `HELLO WORLD` → `PSTER HGFST` (H=P, E=S, ...) is a substitution example. Historical examples: Caesar cipher, Beale cipher, Vigenère (autokey), Gronsfeld, Hill cipher.
- **Transposition ciphers** — keep the same letters, but rearrange their *order* according to a system. `CRYPTOGRAPHY` → `AOYCRGPTYRHP` is a transposition example. Historical examples: rail fence, route cipher, Myszkowski transposition.

Classical ciphers are considered broken by modern standards — they're vulnerable to frequency analysis (see [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md)) because natural language has predictable letter-frequency patterns that survive simple substitution.

### Modern ciphers

Designed to resist a much wider range of attacks and to provide message secrecy, integrity, and sender authentication, generally built on hard mathematical problems (factoring large primes, discrete logarithms, elliptic curve arithmetic) rather than simple alphabet manipulation. Two orthogonal ways to classify them:

**By key type:**
- **Symmetric-key algorithms** (private-key cryptography) — same key encrypts and decrypts. Covered in full in [`02-symmetric-encryption-algorithms.md`](02-symmetric-encryption-algorithms.md).
- **Asymmetric-key algorithms** (public-key cryptography) — different keys for encryption and decryption. Covered in [`03-asymmetric-encryption-algorithms.md`](03-asymmetric-encryption-algorithms.md).

**By input-data handling:**
- **Block ciphers** — deterministic algorithms that operate on a fixed-size chunk ("block") of data at a time with an unvarying transformation under a given key. If the last chunk of plaintext is smaller than the block size, it's padded to fit. Most modern ciphers (AES, DES, IDEA) are block ciphers, and they're the workhorse for encrypting data at rest and in bulk.
- **Stream ciphers** — combine plaintext with a pseudorandom keystream one bit (or byte) at a time. Examples: RC4, SEAL, ChaCha20. Historically favored where low latency matters (streaming, real-time comms) because there's no need to buffer a full block before output starts.

## Block cipher modes of operation

A block cipher only tells you how to transform *one block*. A **mode of operation** tells you how to chain many blocks together to encrypt an arbitrarily long message — and this choice matters enormously for security, independent of which underlying cipher (DES, AES, etc.) you use.

### Electronic Codebook (ECB)

The simplest mode: split plaintext into fixed-size blocks, encrypt each block independently with the same key.

```
C1 = E(K, P1)   C2 = E(K, P2)   C3 = E(K, P3)  ...
```

**Fatal flaw:** identical plaintext blocks always produce identical ciphertext blocks. This leaks structural information about the plaintext even without decrypting it — the classic demonstration is encrypting a bitmap image with ECB and still being able to make out the shape in the ciphertext. **Never use ECB for anything beyond a single block of random-looking data.**

### Cipher Block Chaining (CBC)

Fixes ECB's pattern-leakage by XOR-ing each plaintext block with the *previous ciphertext block* before encrypting. The first block is XORed with a random **initialization vector (IV)** instead, since there's no previous ciphertext yet.

```
C1 = E(K, P1 XOR IV)
C2 = E(K, P2 XOR C1)
C3 = E(K, P3 XOR C2)
```

Decryption reverses this: `P_i = D(K, C_i) XOR C_(i-1)`. CBC requires a unique, unpredictable IV per message (reusing an IV with the same key reintroduces pattern leakage). Its main downside: it's inherently sequential (can't parallelize encryption across blocks) and a single bit error in one ciphertext block corrupts that block and the next one on decryption ("error propagation").

### Cipher Feedback (CFB)

Turns a block cipher into a self-synchronizing stream cipher. The IV is encrypted, the leading *S* bits of that output are XORed with a plaintext segment to produce ciphertext, and the *previous ciphertext* segment feeds back in as the next encryption input.

```
O1 = E(K, IV)         C1 = P1 XOR O1
O2 = E(K, C1)          C2 = P2 XOR O2
```

Useful when you need to encrypt data in units smaller than the cipher's block size (e.g., byte-at-a-time terminal input).

### Counter (CTR) mode

Encrypts a counter value (combined with a nonce) instead of chaining ciphertext, then XORs the result with plaintext.

```
C1 = P1 XOR E(K, Counter || Nonce)
C2 = P2 XOR E(K, (Counter+1) || Nonce)
```

Because each block's keystream only depends on the counter (not on previous ciphertext), **CTR mode is fully parallelizable** in both directions and has no error-propagation problem — a corrupted ciphertext block only corrupts that one plaintext block on decryption. This makes it popular in high-throughput contexts and it's the basis for GCM (below).

**Practical guidance (beyond what the module covers):** for new designs today, prefer an **authenticated** mode over any of the bare modes above — specifically **AES-GCM** (Galois/Counter Mode, which is CTR mode plus a built-in Galois-field MAC) or **ChaCha20-Poly1305**. Both give you confidentiality and integrity in a single, standardized, hard-to-misuse construction, and they're what TLS 1.3 uses by default.

## Authenticated encryption

Plain encryption modes (ECB/CBC/CFB/CTR) only give confidentiality. A capable attacker who can't read your ciphertext can often still *flip bits* in it and produce a modified ciphertext that decrypts to garbage or, worse, to attacker-chosen plaintext (this is exactly the mechanism behind the padding oracle attack in [`11`](11-cryptanalysis-and-attacks.md)). **Authenticated encryption (AE)** modes close this gap by binding a **Message Authentication Code (MAC)** to the ciphertext, so tampering is detectable before decryption is even attempted.

A MAC is a keyed hash: `MAC = MAC(SharedKey, Message)`. Unlike a plain hash, only someone with the shared key can compute or verify it, which is what makes it useful for authentication rather than just error-detection.

Three ways to combine encryption with a MAC:

| Approach | Order of operations | Notes |
|---|---|---|
| **Encrypt-then-MAC (EtM)** | Encrypt plaintext → compute MAC over the *ciphertext* → send both | Generally considered the strongest construction — you can reject a tampered ciphertext without ever running decryption on it. TLS 1.2's recommended cipher suites and IPsec use this. |
| **Encrypt-and-MAC (E&M)** | Compute MAC over the *plaintext* → encrypt plaintext separately → send both | Used by SSH. Weaker in general because the MAC is computed over plaintext but sent alongside ciphertext, which can leak information about the plaintext through the MAC itself in some constructions. |
| **MAC-then-Encrypt (MtE)** | Compute MAC over plaintext → append MAC to plaintext → encrypt the combination | Used by (older) TLS/SSL. The decryptor must decrypt before it can even check the MAC, which is the property that enabled padding-oracle attacks against CBC-mode TLS. |

**Authenticated Encryption with Associated Data (AEAD)** generalizes this further: it lets you authenticate some data (like a packet header) *without* encrypting it, while still encrypting and authenticating the payload. This matters because a receiver often needs to read routing/header info before decryption, but you still want to guarantee nobody tampered with that header. AES-GCM and ChaCha20-Poly1305 are both AEAD constructions, and virtually all modern secure-transport protocols (TLS 1.3, WireGuard, QUIC) are built around one of them.

## Where this leaves you

At this point you have the vocabulary and building blocks: symmetric vs. asymmetric, block vs. stream, mode of operation, and authenticated encryption. The next two files put concrete algorithms behind these categories:

- [`02-symmetric-encryption-algorithms.md`](02-symmetric-encryption-algorithms.md) — DES through ChaCha20
- [`03-asymmetric-encryption-algorithms.md`](03-asymmetric-encryption-algorithms.md) — RSA, DSA, Diffie-Hellman, ECC
