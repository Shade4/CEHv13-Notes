# CEH v13 — Module 20: Cryptography

Comprehensive, hands-on reference notes built from the CEH v13 "Module 20 — Cryptography" courseware, restructured into a study-friendly, GitHub-flavored Markdown knowledge base. Every algorithm, tool, protocol, and attack in the original module is covered here in more depth than the source, with real commands, worked numeric examples, diagrams described in text, and extra context pulled from current (2026) cryptographic practice — including the finalized NIST post-quantum standards.

This repo is part of a growing personal security reference library built module-by-module from CEH v13 courseware.

## Why this module matters

Cryptography is the load-bearing wall of every other security domain covered elsewhere in this library. Web app security depends on TLS. Wireless security depends on WPA's handshake crypto. Cloud security depends on KMS-managed keys. Mobile security depends on platform keystores. This module is the "first principles" layer that everything else quietly assumes you understand — which is why it's worth treating as a reference, not just a one-time read.

## How this repo is organized

| # | File | Covers |
|---|------|--------|
| 01 | [`01-cryptography-fundamentals.md`](01-cryptography-fundamentals.md) | Core concepts, CIA+non-repudiation, GAK/key escrow, classical vs. modern ciphers, block cipher modes of operation (ECB/CBC/CFB/CTR), authenticated encryption (MAC schemes, AEAD) |
| 02 | [`02-symmetric-encryption-algorithms.md`](02-symmetric-encryption-algorithms.md) | DES, 3DES, AES (with pseudocode), RC4/RC5/RC6, Blowfish, Twofish, Threefish, Serpent, TEA, CAST-128/256, GOST, Camellia, ChaCha20/Salsa20 |
| 03 | [`03-asymmetric-encryption-algorithms.md`](03-asymmetric-encryption-algorithms.md) | RSA (full worked example), DSA, Diffie-Hellman, ECC, ElGamal, YAK protocol, key-size equivalence tables |
| 04 | [`04-hashing-and-message-digests.md`](04-hashing-and-message-digests.md) | MD2–MD6, SHA-0/1/2/3, RIPEMD-160, Whirlpool, Tiger, BLAKE2/3, HMAC, GOST hash, hash calculators, multilayer/nested hashing with CyberChef |
| 05 | [`05-hardware-quantum-and-modern-crypto.md`](05-hardware-quantum-and-modern-crypto.md) | TPM/HSM/USB/hard-drive hardware encryption, quantum key distribution, homomorphic encryption, post-quantum cryptography, lightweight cryptography |
| 06 | [`06-cryptography-tools-and-openssl.md`](06-cryptography-tools-and-openssl.md) | General-purpose crypto tools (BCTextEncoder, CryptoForge, AxCrypt, etc.), cryptography toolkits (OpenSSL, wolfSSL, Libsodium, Crypto++, PyCryptodome) with real command syntax |
| 07 | [`07-pki-digital-signatures-ssl-tls.md`](07-pki-digital-signatures-ssl-tls.md) | PKI components and workflow, certificate authorities, signed vs. self-signed certificates, digital signature lifecycle, SSL handshake, TLS record/handshake protocols |
| 08 | [`08-email-encryption.md`](08-email-encryption.md) | PGP, GPG, Web of Trust, S/MIME in Outlook, Microsoft 365 Message Encryption, Apple Mail signing/encryption, FlowCrypt/OpenPGP walkthrough for Gmail, email encryption tool list |
| 09 | [`09-disk-encryption.md`](09-disk-encryption.md) | Disk/volume encryption concepts and tools across Windows (VeraCrypt, BitLocker, Rohos), Linux (Cryptsetup/LUKS), and macOS (FileVault) |
| 10 | [`10-blockchain-cryptography.md`](10-blockchain-cryptography.md) | Blockchain fundamentals, ledger types, and five blockchain-specific attacks (51%, Finney, Eclipse, Race, DeFi Sandwich) with countermeasures |
| 11 | [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md) | Cryptanalysis methods (linear, differential, integral), 12 classic cryptography attack classes, code-breaking methodologies, brute-force economics, birthday attack/paradox math, a **hands-on VeraCrypt brute-force lab with `dd` + `hashcat`**, meet-in-the-middle, side-channel attacks, hash collisions, DUHK, DROWN, rainbow tables, padding oracle |
| 12 | [`12-quantum-attacks-and-countermeasures.md`](12-quantum-attacks-and-countermeasures.md) | Quantum computing risk landscape, 13 quantum-specific attack types, and the full countermeasure playbook for cryptographic, blockchain, and quantum attacks, plus key stretching (PBKDF2/bcrypt) |

### Cheatsheets

| File | Purpose |
|------|---------|
| [`cheatsheets/openssl-cheatsheet.md`](cheatsheets/openssl-cheatsheet.md) | One-page OpenSSL command reference — keys, certs, hashing, encryption, TLS testing |
| [`cheatsheets/crypto-attacks-quick-reference.md`](cheatsheets/crypto-attacks-quick-reference.md) | Every attack in this module in a single scannable table: what it needs, what it targets, one-line defense |

## Learning objectives (from the original module)

1. Explain cryptography concepts and different encryption algorithms
2. Explain applications of cryptography
3. Explain different cryptanalysis methods and cryptography attacks
4. Explain cryptography attack countermeasures

## A note on scope and sourcing

These notes are written from scratch based on the topics, tool names, and command syntax taught in the EC-Council CEH v13 official courseware (Module 20), reorganized and substantially expanded with additional explanation, current context, and worked examples. They are study material, not a reproduction of the original slides or workbook text. Algorithm mechanics, protocol behavior, and command syntax are standard, publicly documented computer-security knowledge available from many independent sources (NIST publications, RFCs, vendor documentation, etc.).

## Suggested reading order

If you're going straight through: **01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12**.

If you're here for the CEH exam specifically, prioritize **01, 02, 03, 07, 11, 12** — that's where most objective-style questions land (algorithm key/block sizes, attack definitions, PKI component names).

If you're here to actually *use* something today, jump to **06** (OpenSSL), **08** (email encryption), **09** (disk encryption), or the **11** hashcat/VeraCrypt lab.
