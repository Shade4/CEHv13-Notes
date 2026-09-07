# 04 — Hashing and Message Digests

## What a hash function is, and why it's a different animal from encryption

Everything in files [`02`](02-symmetric-encryption-algorithms.md) and [`03`](03-asymmetric-encryption-algorithms.md) is **reversible** — there's a key that turns ciphertext back into plaintext. Hash functions are the opposite: **one-way**. They take an input of any size and squeeze it down into a fixed-size fingerprint (typically 128–512 bits), and there is deliberately no way to reverse that process — no key will turn the digest back into the original input.

```
Document (any size) --[Hash Function]--> Fixed-size Hash Value ("digest")
```

A cryptographically sound hash function needs three properties, and it's worth understanding *why* each one matters:

1. **Preimage resistance** — given a hash value, you can't feasibly find *any* input that produces it. (Otherwise an attacker could forge a document matching a known "approved" hash.)
2. **Second-preimage resistance** — given a specific input, you can't feasibly find a *different* input with the same hash. (Otherwise an attacker could swap a legitimate signed document for a malicious one with the same digest.)
3. **Collision resistance** — you can't feasibly find *any two* inputs that hash to the same value. (This is a strictly harder property than #2, because the attacker gets to choose both inputs — see the birthday-attack math in [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md), which is exactly why collision resistance requires roughly *double* the digest length that preimage resistance would need for the same security level.)

A well-designed hash also exhibits the **avalanche effect**: flipping a single input bit should flip roughly 50% of the output bits, with no discernible pattern relating input changes to output changes. Hash functions don't encrypt or decrypt anything themselves, but they're the load-bearing primitive underneath digital signatures, message authentication codes (MACs), password storage, and file-integrity verification.

## Demonstrating the avalanche effect yourself

```bash
echo "There is CHF1500 in the blue bo" | md5sum
# e41a323bdf20eadafd3f0e4f72055d36

echo "There is CHF1500 in the blue box" | md5sum
# 7a0da864a41fd0200ae0ae97afd3279d

echo "There is CHF1500 in the blue box." | md5sum
# 2db1ff7a70245309e9f2165c6c34999d
```

Three near-identical inputs (differing by a single trailing character each time) produce three completely unrelated-looking digests — that unpredictability is the entire point.

## The message digest algorithm family (MD2 → MD6)

| Algorithm | Output size | Status |
|---|---|---|
| MD2 | 128 bits | Broken, obsolete (designed for 8-bit machines) |
| MD4 | 128 bits | Broken — full collisions in under a minute on commodity hardware |
| MD5 | 128 bits | **Broken for collision resistance** — still common for non-security checksums |
| MD6 | 224/256/384/512 bits | Modern, Merkle-tree based, parallelizable |

MD2, MD4, and MD5 share a similar overall structure (padding the message to a multiple of 512 bits and compressing it through rounds of logical operations), though MD2's internals differ enough that it's really a separate design aimed at resource-constrained 8-bit hardware.

**MD5** is still extremely widely encountered — for file-integrity checksums (verifying a download wasn't corrupted), for git's internal object addressing (SHA-1 there, but the same non-cryptographic use case applies), and unfortunately sometimes still for password storage in legacy systems (don't do this — see [`12-quantum-attacks-and-countermeasures.md`](12-quantum-attacks-and-countermeasures.md) for what to use instead). MD5 is **not** collision-resistant: practical collision attacks have existed since 2004, and this is exactly the mechanism behind the hash-collision attack case study in [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md). Never use MD5 anywhere an attacker might benefit from forging a matching digest (digital signatures, TLS certificates, code-signing).

**MD6** is a genuinely modern design (a SHA-3 competition entrant) using a Merkle-tree structure that allows large inputs to be hashed in parallel across multiple cores, and is explicitly designed to resist differential cryptanalysis.

## The SHA family

NIST's Secure Hash Algorithm family, specified in the Secure Hash Standard (FIPS 180), now spanning three structurally distinct generations:

- **SHA-0** — the original 1993 design, withdrawn almost immediately after an undisclosed "significant flaw" was found by the NSA; replaced by a revised version before it ever saw wide use.
- **SHA-1** — a 160-bit hash resembling MD5's structure but with a longer digest and an extra expansion step. Was the workhorse of TLS, SSH, and Git for over a decade. **Formally broken for collision resistance** — Google and CWI Amsterdam published a practical SHA-1 collision ("SHAttered") in 2017, and NIST deprecated it for digital signatures as of 2011 and disallowed it entirely for federal use as of 2030 (with most browsers/CAs having already stopped accepting SHA-1 certificates years earlier). Still shows up in legacy systems and in non-adversarial contexts like Git commit IDs (Git has since added SHA-256 support specifically because of this history).
- **SHA-2** — a family of two structurally related designs: **SHA-256** (32-bit internal words) and **SHA-512** (64-bit internal words), plus truncated variants SHA-224 and SHA-384. **This is the current mainstream default** — used throughout TLS, code signing, blockchain (Bitcoin's proof-of-work is double-SHA-256), and password-hashing-adjacent contexts.
- **SHA-3** — structurally unrelated to SHA-1/SHA-2; built on the **Keccak** sponge construction (message blocks are absorbed into an internal state via XOR, then the state is repeatedly, invertibly permuted to "squeeze" out the digest). Offers the same output-length options as SHA-2 but with a fundamentally different internal design, which matters for defense-in-depth — a structural weakness discovered in SHA-2's Merkle–Damgård construction wouldn't automatically apply to SHA-3's sponge construction, and vice versa.

## Other notable hash functions

- **RIPEMD-160** — a 160-bit hash designed by Hans Dobbertin, Antoon Bosselaers, and Bart Preneel as a European alternative to the NSA-designed SHA family, built from 80 stages (five 16-step blocks run twice, with results combined via modulo-2³² addition). 128-, 256-, and 320-bit variants also exist. Bitcoin actually uses RIPEMD-160 (chained with SHA-256) to generate wallet addresses.
- **Whirlpool** — a 512-bit hash built around an AES-like block cipher structure run in Miyaguchi–Preneel mode, offering a large security margin.
- **Tiger** — a 192-bit hash optimized for 64-bit platforms, designed for high speed.
- **BLAKE2 / BLAKE3** — modern, extremely fast hash functions (BLAKE2 was a SHA-3 finalist; BLAKE3 is a newer, even faster, tree-parallelizable redesign). Increasingly common where raw hashing throughput matters — e.g., checksumming large datasets, some newer password-hashing and content-addressing systems.
- **GOST hash function** — the Russian national standard hash (GOST R 34.11-94), producing a 256-bit output, padding messages into 256-bit blocks with an appended 256-bit running checksum and message-length field.

## HMAC — turning a hash into a keyed authentication code

A plain hash has no secret in it — anyone can compute `SHA256(message)`, which means a plain hash alone can't prove *who* produced a digest, only that the *content* matches. **HMAC (Hash-based Message Authentication Code)** fixes this by mixing a secret key into the hashing process, in two stages: an inner hash over `(inner-padded key || message)`, then an outer hash over `(outer-padded key || inner hash result)`. Running the underlying hash function twice this way specifically defeats **length-extension attacks** that plague naive `Hash(key || message)` constructions on Merkle–Damgård hash functions like SHA-256 (an attacker who only knows a hash output, without the key, can otherwise compute a valid hash for a *longer* message with attacker-chosen data appended — HMAC's two-stage structure closes this off). HMAC security depends on the strength of its underlying hash and key size — `HMAC-SHA256` and `HMAC-SHA1` are common names you'll see in TLS cipher suites and API-authentication schemes (e.g., AWS request signing).

## Hash calculator and verification tools

| Tool | Source | Notes |
|---|---|---|
| QuickHash-GUI | quickhash-gui.org | Cross-platform (Linux/Windows/macOS) GUI, hashes text as you type or entire files |
| MD5 Calculator | bullzip.com | Right-click integration, handles multi-GB files, side-by-side digest comparison |
| HashMyFiles | nirsoft.net | Windows Explorer context-menu integration; computes MD5/SHA1/CRC32/SHA-256/SHA-512/SHA-384 simultaneously, exportable to CSV/HTML/XML |
| MD6 Hash Generator / All Hash Generator | browserling.com | Browser-based, no install |
| md5 hash calculator | onlinehashtools.com | Browser-based |
| Message Digester | freeformatter.com | Browser-based, multiple algorithms |

### Command-line hashing (no tool install required)

```bash
# Linux / macOS
md5sum file.txt
sha1sum file.txt
sha256sum file.txt
shasum -a 256 file.txt        # macOS variant

# Windows PowerShell
Get-FileHash file.txt -Algorithm MD5
Get-FileHash file.txt -Algorithm SHA256
```

## Multilayer (nested/recursive) hashing with CyberChef

**Multilayer hashing** means feeding the output of one hash function into another hash function as input, one or more times — nested hashing rather than single-pass hashing. This adds a layer of obfuscation that makes reverse-engineering the original input from the final digest harder, though note it does *not* substitute for a proper key-stretching function like PBKDF2/bcrypt/Argon2 when the goal is password storage (see [`12-quantum-attacks-and-countermeasures.md`](12-quantum-attacks-and-countermeasures.md) — key stretching is deliberately slow and salted; naive repeated hashing is neither by default).

**CyberChef** (`https://gchq.github.io/CyberChef`) is the standard browser-based tool for building these hash chains visually — it's a "data manipulation Swiss Army knife" originally released by GCHQ, and it's genuinely useful well beyond hashing (encoding/decoding, encryption, regex extraction, etc.).

**Walkthrough — chaining MD5 → SHA1 → HMAC in CyberChef:**

1. Open CyberChef at `https://gchq.github.io/CyberChef`.
2. In the **Input** pane, either type text directly or click the file icon to load a sample file.
3. In the **Operations** panel, search for `MD5` and drag it into the **Recipe** panel. The MD5 digest of your input now appears in the **Output** pane.
4. Search for `SHA1` and drag it into the Recipe panel *below* MD5 — CyberChef automatically feeds the MD5 output forward as SHA1's input.
5. Add a third operation — e.g., search for `HMAC`, drag it into the Recipe, set a key and hashing function (e.g., MD5) — and the recipe now computes `HMAC(key, SHA1(MD5(input)))` in one pass, with the final result shown in Output.

This is a genuinely useful technique for CTF challenges that expect a specific nested-hash format, and for understanding exactly what a piece of malware or a legacy application's custom "obfuscation" scheme is actually doing under the hood.

## Online MD5 decryption / lookup tools

Because MD5 has no salt and is fast to compute, huge precomputed lookup tables ("rainbow tables" — see [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md)) exist online mapping common plaintexts to their MD5 digests. These aren't "decrypting" MD5 in any mathematical sense — they're doing a reverse lookup against precomputed data, which only works if the original plaintext was already common/weak enough to be in the table:

- MD5 Decrypter — dcode.fr
- MD5 Decrypt — iotools.cloud
- Md5 Encrypt & Decrypt — md5decrypt.net
- MD5Hashing.net
- MD5 Encrypt/Decrypt — 10015.io
- MD5 Decryption — md5online.org
- MD5Decrypter.com
- Online Hash Crack — onlinehashcrack.com
- Md5.My-Addr.com
- Cmd5 — cmd5.org
- Hashes.com
- Online MD5 Hashed Validator — javainuse.com
- MD5 Hash Decode — md5.web-max.ca
- MD5 Decrypt — allinone.tools
- GettHIT.com

**The existence of this entire tooling category is itself the strongest practical argument against ever using unsalted MD5 (or any fast, unsalted hash) for storing passwords** — if the plaintext is guessable at all, one of these sites (or an offline tool like `hashcat` — see the cracking lab in [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md)) will very likely recover it.

Next: [`05-hardware-quantum-and-modern-crypto.md`](05-hardware-quantum-and-modern-crypto.md) for hardware-backed encryption, quantum key distribution, and the emerging edges of the field.
