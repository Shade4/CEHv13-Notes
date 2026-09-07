# Cryptography Attacks — Quick Reference

Every attack covered in this repo, in one scannable table. Full explanations in [`../11-cryptanalysis-and-attacks.md`](../11-cryptanalysis-and-attacks.md), [`../10-blockchain-cryptography.md`](../10-blockchain-cryptography.md), and [`../12-quantum-attacks-and-countermeasures.md`](../12-quantum-attacks-and-countermeasures.md).

## Classic cryptography attacks (attacker-access model)

| Attack | Attacker needs | One-line defense |
|---|---|---|
| Ciphertext-only | Just ciphertext | Strong, well-analyzed algorithm + sufficiently long key |
| Known-plaintext | Some plaintext/ciphertext pairs | Avoid predictable/repeated plaintext structure; strong algorithm |
| Chosen-plaintext | Ability to encrypt chosen plaintexts | Randomized/probabilistic encryption (fresh IV/nonce per message) |
| Adaptive chosen-plaintext | Interactive encryption oracle | Rate-limit/monitor encryption oracle access |
| Chosen-ciphertext (+ lunchtime/adaptive variants) | Ability to decrypt chosen ciphertexts | Authenticated encryption (AEAD) — reject invalid ciphertext before it's processed |
| Related-key | Ciphertexts under mathematically related keys | Independent, unrelated key generation per session (proper KDF, never derive keys from each other) |
| Dictionary | Precompiled plaintext/ciphertext dictionary | Salting; strong/high-entropy passphrases |
| Rubber hose | Physical access to a key-holder | Split-knowledge / multi-party key control; operational security |
| Chosen-key | Ability to manipulate key relationships | Strong key schedule with no exploitable structure |
| Timing | Ability to measure operation execution time | Constant-time algorithm implementations |
| Man-in-the-middle | Position on the key-exchange path | Authenticated key exchange (certificates, PKI — see [`../07`](../07-pki-digital-signatures-ssl-tls.md)) |
| Rainbow table | Precomputed hash/plaintext table | Per-record random salt |
| Birthday attack | Ability to generate/compare many hash outputs | Hash output length ≥ 2× the desired collision-resistance bit strength |
| Meet-in-the-middle | Multi-key sequential encryption scheme | Use independent, sufficiently many key stages (e.g., 3DES's EDE structure, or just use AES) |
| Hash collision | Ability to generate/compare candidate messages | Collision-resistant hash (SHA-256/SHA-3, not MD5/SHA-1) |
| Padding oracle (Vaudenay) | Distinguishable padding-error responses | Generic error messages; AEAD instead of bare CBC |
| DUHK | Hardcoded/predictable RNG seed | Never hardcode seeds; use a proper hardware/OS entropy source |
| DROWN | Server permitting SSLv2 + shared private key | Disable SSLv2/SSLv3 entirely; never share keys with legacy-protocol servers |
| Side-channel (power/EM/light/timing/sound) | Physical/proximate access to hardware | Constant-time code, masking, noise injection, shielded hardware (see [`../11`](../11-cryptanalysis-and-attacks.md)) |

## Blockchain-specific attacks

| Attack | Mechanism | One-line defense |
|---|---|---|
| 51% (majority) | Control >50% of network hash/stake power | High total network hash rate; PoW+PoS hybrid |
| Finney | Pre-mined block reverses a zero-confirmation payment | Wait for multiple confirmations |
| Eclipse | Isolate a node behind attacker-controlled peers | Randomized peer selection, trusted bootstrap nodes |
| Race | Two conflicting transactions racing for confirmation | Wait for multiple confirmations |
| DeFi sandwich | Front-run + back-run a victim's DEX trade | Hide pending-tx details, fair sequencing/batch processing |

## Quantum-era attacks

| Attack | What it targets |
|---|---|
| Quantum cryptanalysis (Shor's/Grover's) | RSA/DSA/DH/ECC (Shor's — near-total break); AES/SHA (Grover's — halves effective key strength) |
| Quantum side-channel | Physical leakage from quantum hardware |
| Classical-to-quantum transition | Hybrid-system interoperability gaps during PQC migration |
| Harvest-now, decrypt-later | Data encrypted today, stored for future quantum decryption |
| Quantum Trojan horse / supply chain / sabotage / fault injection | Quantum hardware/software integrity, before or during deployment |
| Quantum DoS | Quantum system/network availability |
| Quantum data eavesdropping / replay | QKD and other quantum communication channels |
| Quantum bit-flipping / error-correction exploitation | Quantum computation integrity |

**General defense:** migrate to NIST-finalized PQC standards — **ML-KEM** (key exchange), **ML-DSA** or **SLH-DSA** (signatures) — using hybrid classical+PQC deployment during the transition. Full detail in [`../05-hardware-quantum-and-modern-crypto.md`](../05-hardware-quantum-and-modern-crypto.md) and [`../12-quantum-attacks-and-countermeasures.md`](../12-quantum-attacks-and-countermeasures.md).

## Code-breaking methodologies (general techniques, not single attacks)

| Method | Idea |
|---|---|
| Brute force | Try every possible key |
| Frequency analysis | Exploit predictable letter/token frequency |
| Trickery and deceit | Social-engineer a known-plaintext sample |
| One-time pad (defensive concept) | Provably unbreakable *if* truly random, as long as the message, used once, and never reused |
