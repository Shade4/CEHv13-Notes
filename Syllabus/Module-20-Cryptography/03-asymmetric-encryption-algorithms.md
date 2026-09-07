# 03 — Asymmetric (Public-Key) Encryption Algorithms

| Algorithm | Key size | Primary use | Hard problem it relies on |
|---|---|---|---|
| RSA | Variable (1024–15360 bits typical) | Encryption, digital signatures, key exchange | Integer factorization |
| DSA | Variable | Digital signatures only | Discrete logarithm (finite field) |
| Diffie-Hellman | Variable | Key exchange | Discrete logarithm (finite field) |
| ECC | 160–521 bits | Encryption, signatures, key exchange | Elliptic curve discrete logarithm |
| ElGamal | Variable | Encryption, key exchange | Discrete logarithm (finite field) |

## Why asymmetric crypto works at all

Every algorithm on this page leans on a **trapdoor function** — something that's cheap to compute in one direction and (as far as anyone has publicly demonstrated) infeasible to reverse without a secret, even though the forward function itself is public. RSA's trapdoor is that multiplying two large primes together is easy, but factoring the product back into those primes is hard. Diffie-Hellman, DSA, and ElGamal all lean on the **discrete logarithm problem**: given `g`, `p`, and `gᵏ mod p`, finding `k` is computationally hard even though computing `gᵏ mod p` from `k` is easy. ECC uses a geometric analogue of the same idea over elliptic curve points instead of integers mod p.

## RSA (Rivest–Shamir–Adleman)

The first, and still the most widely deployed, public-key cryptosystem — named for its three MIT inventors, formulated on modular arithmetic and elementary number theory over two large primes. RSA keys and RSA-based certificate chains underpin an enormous fraction of internet PKI, code signing, and secure email.

### How the math works

**Key generation:**

1. Choose two large, distinct primes `p` and `q` (in production, each typically 1024+ bits, chosen with roughly equal bit-length).
2. Compute the modulus `n = p × q` and Euler's totient `φ(n) = (p-1)(q-1)`.
3. Choose a public exponent `e` such that `1 < e < φ(n)` and `gcd(e, φ(n)) = 1` (they share no common factors). `e = 65537` is the near-universal choice in practice because it's prime, has a compact binary form (fast exponentiation), and is large enough to avoid certain low-exponent attacks.
4. Compute the private exponent `d` such that `d ≡ e⁻¹ (mod φ(n))` — i.e., `(d × e) mod φ(n) = 1`. This uses the extended Euclidean algorithm.
5. **Public key** = `(n, e)`. **Private key** = `d` (with `p`, `q`, and `φ(n)` securely destroyed or retained only for CRT-optimized decryption — never distributed).

**Encryption:** `C = Tᵉ mod n`, where `T` is the plaintext (as an integer less than `n`).
**Decryption:** `T = C^d mod n`.

Security rests entirely on the fact that recovering `d` from the public `(n, e)` requires factoring `n` back into `p` and `q` — and for large enough primes, no efficient classical factoring algorithm is known. (A **quantum** computer running Shor's algorithm *can* factor efficiently — this is precisely why RSA is one of the algorithms flagged for replacement under post-quantum migration; see [`12-quantum-attacks-and-countermeasures.md`](12-quantum-attacks-and-countermeasures.md).)

### Worked numeric example (intentionally tiny — never do this with primes this small in real use)

This is the standard illustrative example used across most RSA teaching material, reproduced here with the arithmetic worked all the way through so you can follow every step:

```
p = 61            (first prime — destroy after computing d)
q = 53            (second prime — destroy after computing d)
n = p * q = 3233   (modulus — public)
φ(n) = (p-1)(q-1) = 60 * 52 = 3120

Choose e = 17      (must satisfy gcd(e, 3120) = 1 — true here)
Compute d such that (d * 17) mod 3120 = 1  →  d = 2753

Public key  = (e=17, n=3233)
Private key = (d=2753)
```

**Encrypting the plaintext value 123:**

```
C = 123^17 mod 3233 = 855
```

**Decrypting the ciphertext value 855:**

```
T = 855^2753 mod 3233 = 123    ✓ round-trips correctly
```

Computing `855^2753 mod 3233` by hand is done with **fast modular exponentiation** (repeated squaring) rather than literally raising 855 to the 2753rd power — you compute `855^1, 855^2, 855^4, 855^8, ...` by repeatedly squaring and reducing mod 3233 at each step, then multiply together the powers whose exponents sum to 2753 (since 2753 = 1 + 64 + 128 + 512 + 2048 in binary). This "square-and-multiply" technique is exactly how every real RSA implementation computes modular exponentiation efficiently regardless of key size.

### RSA in a hybrid system

In practice RSA is almost never used to encrypt an entire message directly — it's slow, and it can only encrypt data smaller than the modulus. Instead, a typical flow is:

1. Sender generates a random symmetric session key (e.g., an AES key).
2. Sender encrypts the actual message with that fast symmetric key.
3. Sender encrypts *just the session key* with the recipient's RSA public key.
4. Sender transmits both the symmetric ciphertext and the RSA-wrapped key — sometimes called an **RSA digital envelope**.
5. Recipient uses their RSA private key to unwrap the session key, then uses that session key to decrypt the actual message.

This gets you RSA's key-management convenience with symmetric crypto's speed — the same hybrid pattern shows up again almost verbatim in PGP (see [`08-email-encryption.md`](08-email-encryption.md)).

### RSA digital signatures

RSA can also run "in reverse" for signing: the signer encrypts (signs) with their **private** key, and anyone can verify with the signer's **public** key. In the standard scheme:

1. **Sign:** compute `s = H(m)^d mod n` where `H(m)` is a hash of the message.
2. **Verify:** compute `H(m)' = s^e mod n` and check it matches an independently computed hash of the message.

Because RSA signing/verification uses the inverse key from encryption/decryption, only the private-key holder could have produced a signature that the public key correctly verifies — this is the basis of non-repudiation. Full digital signature workflow (sign → seal → verify) is covered in [`07-pki-digital-signatures-ssl-tls.md`](07-pki-digital-signatures-ssl-tls.md).

## Digital Signature Algorithm (DSA)

A U.S. federal standard (FIPS 186, part of the Digital Signature Standard) — unlike RSA, DSA is **signature-only**; it can't be used for encryption. It produces a 320-bit signature with 512–1024-bit (or larger, in later revisions) security parameters, and relies on the discrete-logarithm problem rather than factoring.

**Key generation:** choose a prime `q` (~160 bits), a prime `p` such that `q` divides `(p-1)`, a generator `α` of the order-`q` subgroup of `Z*p`, and a private key `d` (random, `1 ≤ d ≤ q-1`). Public key is `y = α^d mod p`.

**Signing a message `m`:** pick a random per-signature secret `k` (`0 < k < q`), compute `r = (α^k mod p) mod q`, then `s = k⁻¹ { h(m) + d·r } mod q`, where `h` is a secure hash (SHA family). The signature is the pair `(r, s)`.

**Verifying:** the recipient recomputes `w = s⁻¹ mod q`, `u1 = w·h(m) mod q`, `u2 = r·w mod q`, then checks `(α^u1 · y^u2 mod p) mod q == r`.

**Critical implementation note:** the per-signature random value `k` **must** be unique and unpredictable for every signature. Reusing `k` across two different signed messages, or using a `k` generated from a weak/predictable RNG, leaks the private key directly via simple algebra on the two signatures — this exact flaw was responsible for real-world private-key recovery incidents (most famously the Sony PS3 signing-key leak, and see the **DUHK attack** case study in [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md) for a closely related hardcoded-seed failure mode).

## Diffie–Hellman key exchange

Developed and published by Whitfield Diffie and Martin Hellman in 1976 (independently discovered a few years earlier by Malcolm Williamson at the UK's GCHQ, but that work stayed classified at the time). DH isn't an encryption algorithm at all — it's a **key-agreement protocol**: a way for two parties to derive a shared secret over a channel an eavesdropper can fully observe, without ever transmitting the secret itself.

**The protocol** (using the classic "Alice and Bob" framing that essentially every cryptography text uses):

1. Public parameters: a large prime `p` and a generator `g` (an integer < p with specific mathematical properties).
2. Alice picks a random private value `a`, computes her public value `A = g^a mod p`, and sends `A` to Bob.
3. Bob picks a random private value `b`, computes his public value `B = g^b mod p`, and sends `B` to Alice.
4. Alice computes the shared secret as `B^a mod p`. Bob computes it as `A^b mod p`.
5. Both arrive at the same value, because `(g^b)^a = (g^a)^b = g^(ab) mod p`.

An eavesdropper who sees `p`, `g`, `A`, and `B` still can't compute `g^(ab) mod p` without solving the discrete logarithm problem to recover `a` or `b` first.

**Important limitation:** plain Diffie-Hellman provides *no authentication* — it guarantees the two parties end up with a shared secret, but not that they know *who* they're sharing it with. This is exactly what makes it vulnerable to man-in-the-middle attacks unless it's combined with an authentication mechanism (e.g., signing the DH public values with a certificate-backed key, which is exactly what TLS does). It does, however, provide **forward secrecy** when used in "ephemeral" mode (a fresh `a`/`b` pair per session) — this is the "DHE" or "ECDHE" you see in TLS cipher-suite names, and it means that even if a long-term signing key is later compromised, past session traffic recorded by an attacker still can't be decrypted, because the ephemeral DH secrets used for those sessions were never stored anywhere.

## Elliptic Curve Cryptography (ECC)

ECC re-implements the same *ideas* as RSA/DSA/DH (encryption, signatures, key exchange) but over the algebraic structure of points on an elliptic curve instead of integers modulo a large prime. The elliptic curve discrete logarithm problem is believed to be significantly harder, bit-for-bit, than the classical discrete logarithm or factoring problems — which means ECC gets you equivalent security with **much smaller keys**:

| ECC key size | Equivalent RSA key size |
|---|---|
| 160–223 bits | 1024 bits |
| 224–255 bits | 2048 bits |
| 256–383 bits | 3072 bits |
| 384–511 bits | 7680 bits |
| 512+ bits | 15360 bits |

Smaller keys mean smaller certificates, less bandwidth, and faster signing/verification — which is a large part of why ECC (specifically **ECDSA** for signatures and **ECDH/ECDHE** for key exchange) has become the default choice in modern TLS deployments, mobile devices, and IoT, where RSA's larger keys and slower operations are a real cost.

## ElGamal

A public-key encryption *and* signature scheme built directly on the discrete-log problem, predating DSA (DSA is, in fact, derived from ElGamal's signature variant). Notable property: ElGamal encryption is **probabilistic** — encrypting the same plaintext twice produces different ciphertexts each time (because a fresh random value is chosen per encryption), which prevents an attacker from recognizing repeated messages purely by comparing ciphertexts — a property plain "textbook" RSA does *not* have unless padding schemes like OAEP are layered on top.

## YAK protocol

A public-key **authenticated key exchange (AKE)** protocol — a variant of the two-pass Hashed Menezes-Qu-Vanstone (HMQV) protocol that uses **zero-knowledge proofs (ZKP)** so each party can prove they know their own ephemeral secret without revealing it. Requires a PKI to distribute authentic public keys in the first place.

**Simplified flow between Alice and Bob:**

1. Alice picks random `x`, computes `X = g^x`, and generates a ZKP of knowledge of `x` (`KP{x}`). Sends `X` and `KP{x}` to Bob.
2. Bob does the symmetric thing: picks random `y`, computes `Y = g^y`, generates `KP{y}`, sends both to Alice.
3. Each side verifies the other's ZKP, then derives the same session key: `k = H(g^((x+a)(y+b)))`, where `a` and `b` are the parties' static (long-term) private keys.

YAK achieves private-key security and full forward secrecy, though it's noted as lacking *joint* key control (neither party alone fully determines the resulting session key's randomness in the way some other AKE protocols guarantee) — a niche protocol worth recognizing by name more than deploying yourself.

## Practical takeaway

If you're choosing today: **ECDSA (P-256 or better) or Ed25519** for signatures, **ECDH/X25519** for key exchange, **RSA-2048 minimum (3072+ preferred)** only where you're stuck supporting legacy compatibility. Plain DSA is largely obsolete in new designs — ECDSA superseded it almost everywhere DSA used to be required.

Next: [`04-hashing-and-message-digests.md`](04-hashing-and-message-digests.md) for the one-way side of cryptography — functions with no decryption at all.
