# 05 — Hardware-Based, Quantum, and Modern Cryptography

## Hardware-based encryption

Hardware-based encryption offloads the cryptographic workload from CPU/software onto dedicated silicon, and generally stores keys in tamper-resistant hardware rather than in RAM or on disk where software could potentially read them. The core security advantage: hardware devices deliberately support a reduced instruction set and refuse to run arbitrary third-party code, which closes off a large class of malware-based key-theft attacks that plague pure-software implementations.

### Trusted Platform Module (TPM)

A dedicated crypto-processor chip, usually soldered directly onto (or integrated into the chipset of) a computer's motherboard. A TPM can:

- Generate and securely store encryption keys such that the private key material never leaves the chip
- Perform cryptographic operations (signing, key generation, hashing) on-chip
- Provide **platform integrity attestation** — measuring and cryptographically recording the boot process (bootloader, OS kernel, etc.) so software can detect if early boot components have been tampered with
- Enable full-disk encryption schemes that bind the decryption key to that specific machine's boot state (this is exactly the mechanism **BitLocker** uses — see [`09-disk-encryption.md`](09-disk-encryption.md))
- Provide hardware-backed password/credential storage and software license protection

### Hardware Security Module (HSM)

An HSM is a step up from a TPM in scale and purpose: a dedicated, often external, network-attached appliance built specifically for enterprise-grade key management — generating, storing, and using cryptographic keys (frequently keys longer than 256 bits) at high throughput, usually connected over TCP/IP for use by many servers/applications at once. Common in payment processing, certificate authorities, and any environment with regulatory requirements around key custody. Examples: Thales Luna Network HSM, nShield HSM, Utimaco HSM, Cryptosec Dekaton PCI.

### USB and hard-drive hardware encryption

- **USB encryption** — encrypted USB storage devices with onboard encryption logic, requiring an on-device credential (PIN pad) or host-side software/hardware authentication before the drive will mount. Reduces the risk of malware propagation via USB and data loss/leakage if the physical device is lost. Examples: Kingston IronKey D300S, diskAshur Pro.
- **Hard-drive encryption devices** — dedicated hardware that encrypts an entire drive's contents, typically requiring a paired TPM or HSM for key management since the drive itself usually has no keyboard/fingerprint reader of its own. Examples: military-grade 256-bit AES hardware encryption modules, DiskCypher AES SATA hard drive encryption.

## Quantum cryptography

Quantum cryptography is a fundamentally different security model from everything covered so far: instead of relying on a mathematical problem being *computationally hard* (factoring, discrete log), it relies on the **laws of physics** making eavesdropping *physically detectable*. The best-known application is **Quantum Key Distribution (QKD)**.

**How QKD (conceptually, via the BB84-style scheme referenced in the CEH curriculum) works:** data is encoded onto individual photons using their polarization/spin state, sent through filters oriented in different bases:

| Filter orientation | Encoded bit |
|---|---|
| Horizontal (–) | 0 |
| Vertical (\|) | 1 |
| Backslash (/) | 1 |
| Forward slash (\\) | 0 |

The core physical guarantee (from quantum mechanics' no-cloning theorem and measurement disturbance) is that **an eavesdropper cannot measure a photon's quantum state without disturbing it**. If Eve intercepts a photon and measures it using the wrong basis (which she can't know in advance), the polarization gets randomly reset, and when the legitimate receiver measures it, statistically detectable errors appear in the key-agreement process. The two legitimate parties can then detect that eavesdropping occurred (from an elevated error rate) and discard the compromised key material — QKD doesn't prevent eavesdropping outright, it makes eavesdropping *detectable*, which is a different and in some ways stronger guarantee than "hard to compute."

QKD is deployed today mainly in specialized, high-value point-to-point links (government, financial-sector backbone links, some metro fiber networks) rather than general internet traffic — the hardware requirements (dedicated fiber, single-photon detectors, distance limits without trusted relay nodes) still make it impractical for consumer-scale deployment as of 2026.

## Homomorphic encryption

A genuinely different cryptographic capability from everything else in this repo: **homomorphic encryption allows mathematical operations to be performed directly on encrypted data, producing an encrypted result that — when later decrypted by the key holder — matches what you'd have gotten by performing the same operations on the plaintext.** The party doing the computation never needs to see the plaintext at all.

| Scheme | Who can generate ciphertext | Who can compute on ciphertext | Who can decrypt |
|---|---|---|---|
| Private-key encryption | Key holder only | Nobody | Key holder only |
| Public-key encryption | Anyone (via public key) | Nobody | Private-key holder only |
| **Homomorphic encryption** | Key holder | **Anyone** — the untrusted party performing the computation | Key holder only |

This is the enabling technology behind privacy-preserving cloud computation: you can encrypt sensitive data, hand it to a cloud provider you don't fully trust, have them run computation (analytics, machine-learning inference, etc.) on your behalf, and get back an encrypted result that only you can decrypt — the cloud provider never sees your plaintext data *or* the plaintext result. Fully homomorphic encryption (supporting arbitrary computation, not just addition or just multiplication) has historically been extremely computationally expensive, but practical libraries (Microsoft SEAL, IBM HElib, OpenFHE) have made partial/leveled homomorphic encryption increasingly viable for specific real-world workloads.

## Post-quantum cryptography (PQC)

"Post-quantum," "quantum-resistant," and "quantum-proof" all refer to the same thing: cryptographic algorithms — mostly public-key based — designed to remain secure even against an adversary with a large-scale, fault-tolerant quantum computer. This matters because **Shor's algorithm**, if run on sufficiently powerful quantum hardware, can efficiently factor large integers and solve discrete logarithms — which would break RSA, DSA, Diffie-Hellman, and ECC essentially completely, all at once, since they all rest on exactly those two hard problems. (**Grover's algorithm**, separately, gives only a quadratic speedup against symmetric ciphers and hash functions — which is why doubling AES/SHA key/output sizes is generally considered sufficient defense there, unlike the public-key case, which needs entirely different mathematical foundations.)

**Beyond what the original module names generically as "lattice-based" and "hash-based" cryptography, it's worth knowing the specific standards that now exist (finalized by NIST in August 2024, after a multi-year public competition):**

| Standard | Purpose | Underlying hard problem |
|---|---|---|
| **ML-KEM** (formerly CRYSTALS-Kyber) | Key encapsulation / key exchange | Module lattice problems |
| **ML-DSA** (formerly CRYSTALS-Dilithium) | Digital signatures | Module lattice problems |
| **SLH-DSA** (formerly SPHINCS+) | Digital signatures (stateless, hash-based) | Hash function security only — a very conservative fallback with minimal new mathematical assumptions |
| **FN-DSA** (formerly FALCON) | Digital signatures (compact) | NTRU lattice problems |

Major browsers, TLS libraries (OpenSSL 3.2+, BoringSSL), and cloud providers have already begun rolling out **hybrid** key exchange — combining a classical algorithm like X25519 with ML-KEM in the same handshake — so that a connection remains secure even if either the classical or the post-quantum assumption is later broken. If you're doing new protocol or infrastructure design work today, this is the concrete standard set to plan a migration toward, not just an abstract "post-quantum" placeholder — see [`12-quantum-attacks-and-countermeasures.md`](12-quantum-attacks-and-countermeasures.md) for the full quantum threat model and countermeasure list.

## Lightweight cryptography

A distinct design challenge from "make it quantum-resistant": **make cryptography work at all on severely resource-constrained hardware** — RFID tags, low-power sensor nodes, and other IoT devices with tiny amounts of RAM, minimal CPU, and often a hard power budget (battery- or even energy-harvesting-powered). Standard algorithms like full AES or RSA can simply be too large, too slow, or too power-hungry to run at all on this class of hardware.

NIST ran its own standardization process for this specifically, selecting **ASCON** (in 2023) as the lightweight cryptography standard — an authenticated-encryption and hashing family purpose-built for constrained devices, worth knowing by name if you work anywhere near embedded/IoT security, since it's the modern answer to a gap the original module only describes conceptually.

Next: [`06-cryptography-tools-and-openssl.md`](06-cryptography-tools-and-openssl.md) — putting hands on the actual software tools that implement everything covered so far.
