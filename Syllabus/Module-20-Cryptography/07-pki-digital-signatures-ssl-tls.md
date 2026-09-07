# 07 — PKI, Digital Signatures, and SSL/TLS

## Public Key Infrastructure (PKI)

Everything in [`03-asymmetric-encryption-algorithms.md`](03-asymmetric-encryption-algorithms.md) has one unaddressed problem: if public keys are meant to be freely distributed, **how do you know a given public key actually belongs to the person or server it claims to belong to**, rather than to an attacker running a man-in-the-middle? PKI is the whole system built to answer that question — the hardware, software, people, policies, and procedures required to create, manage, distribute, use, store, and revoke **digital certificates**, which bind a public key to a verified identity.

### Components of PKI

| Component | Role |
|---|---|
| **Certificate Authority (CA)** | The trusted entity that actually issues and digitally signs certificates, vouching that a given public key belongs to a given identity |
| **Registration Authority (RA)** | Verifies the applicant's identity on the CA's behalf before a certificate is issued — the "front desk" that does identity checking so the CA doesn't have to |
| **Validation Authority (VA)** | Stores issued certificates (with their public keys) and answers queries about whether a given certificate is still valid |
| **Certificate Management System** | Generates, distributes, stores, and verifies certificates across their lifecycle |
| **End User** | Requests, manages, and uses certificates for their own transactions |

### The PKI issuance-and-use process, end to end

1. A subject (user, company, or system) that wants to exchange information securely applies for a certificate through the **RA**.
2. The RA receives the request, verifies the applicant's identity through whatever vetting process is appropriate for the certificate type (domain control for a basic TLS cert, extensive corporate/legal verification for an Extended Validation cert), and forwards a validated request to the **CA**.
3. The CA issues a public-key certificate binding the subject's verified identity to their public key, and signs it with the CA's own private key. The CA also pushes updated status information to the **VA**.
4. When the subject later wants to transact (e.g., sign a message), they sign it with their own private key and attach their certificate so the recipient can verify the signature.
5. The recipient (relying party) checks the certificate's authenticity by querying the VA — confirming it hasn't been revoked and was genuinely issued by a trusted CA.
6. The VA compares what it has on file against the certificate presented and returns a valid/invalid determination.

### Certificate Authorities in practice

Real-world commercial and infrastructure CAs you'll encounter constantly: **Comodo/Sectigo** (SSL certs, SGC encryption, certificate-lifecycle management tools), **IdenTrust** (digital document signing, managed PKI hosting for enterprise/IoT), **DigiCert** (CertCentral — automated TLS/SSL certificate lifecycle management at scale), and **GoDaddy** (domain-bundled SSL certificates, SHA-2/2048-bit by default). Browsers and operating systems ship with a curated **root store** of CAs they trust by default — this is why a certificate signed by DigiCert "just works" in a browser with no configuration, while a self-signed certificate triggers a warning.

### Signed (CA-issued) certificate vs. self-signed certificate

| | Signed certificate | Self-signed certificate |
|---|---|---|
| Issued by | A trusted third-party CA | The subject themselves |
| Trust chain | Verifiable back to a root CA already trusted by the relying party's OS/browser | None — the subject *is* the only vouching party |
| Verification | Recipient queries a Validation Authority | Recipient has to directly contact/trust the signer |
| Typical use | Public-facing websites, code signing, S/MIME email | Internal testing, lab environments, dev/staging systems, air-gapped networks |
| Creation tools | Requested via CSR through a CA | Adobe Acrobat Reader, Java `keytool`, Apple Keychain, `openssl req -x509` (see [`06`](06-cryptography-tools-and-openssl.md)) |

A self-signed certificate isn't inherently "less encrypted" — the cryptography is identical. What it lacks is a trusted third party's independent verification of the identity claim, which is why browsers flag it: they have no basis to trust that the presented public key genuinely belongs to who it claims to.

## Digital signatures

A digital signature is cryptography's answer to a handwritten signature — a mechanism for proving a document is authentic and hasn't been altered since signing, using asymmetric cryptography rather than ink. **Sign** with the private key (only the signer could have produced this), **verify** with the public key (anyone can check it).

**Full email-security flow using digital signatures, combining signing with encryption (this is the same overall pattern PGP/GPG use — see [`08-email-encryption.md`](08-email-encryption.md)):**

1. **Sign** — hash the message, then encrypt (sign) that hash with the sender's private key, producing a signed hash appended to the message.
2. **Seal** — encrypt the message body with a fresh one-time symmetric key, then encrypt *that* symmetric key with the recipient's public key.
3. **Deliver** — mail the sealed envelope (encrypted message + encrypted symmetric key + signed hash) to the recipient.
4. **Open** — the recipient decrypts the one-time symmetric key using their own private key, then uses it to decrypt the message body.
5. **Accept** — the recipient's client displays the decrypted content.
6. **Verify** — the recipient independently re-hashes the received message and decrypts the sender's signed hash using the sender's *public* key. If the two hashes match, the message is both authentic (came from the claimed sender) and untampered (matches exactly what was signed).

Note this delivers all four goals from [`01-cryptography-fundamentals.md`](01-cryptography-fundamentals.md) at once: confidentiality (step 2), integrity (step 6's hash match), authentication (step 6's signature verification), and non-repudiation (only the sender's private key could have produced a signature verifiable by their public key).

## Secure Sockets Layer (SSL)

SSL is the original application-layer protocol (developed by Netscape) for managing secure message transmission over the internet, using RSA asymmetric encryption for the initial key exchange. It provides three properties collectively called "channel security":

- **Private channel** — all messages encrypted after an initial handshake establishes a shared secret key.
- **Authenticated channel** — the server side of the connection is always authenticated via certificate; the client side authentication is optional (most consumer HTTPS traffic only authenticates the server, not the browsing client).
- **Reliable channel** — message transport includes an integrity check, so tampering in transit is detectable.

### The SSL handshake, step by step

1. **Client Hello** — client sends supported SSL version, a random value, session ID (if resuming), supported cipher suites, and compression methods.
2. **Server Hello + Certificate** — server picks a protocol version and cipher suite from the client's offered list, sends its own random value and its certificate (containing its public key).
3. **Server Hello Done** — server signals it's finished with its part of the negotiation and is waiting on the client.
4. **Client Key Exchange** — client verifies the server's certificate, generates a random **pre-master secret**, encrypts it with the server's public key (from the certificate), and sends it over.
5. **Change Cipher Spec + Finished (client)** — client switches to using the newly negotiated symmetric keys and sends a hash of the entire handshake so far, encrypted under the new keys, so the server can verify nothing was tampered with during negotiation.
6. **Change Cipher Spec + Finished (server)** — server does the same in return. If both sides' hash checks pass, the handshake is complete and both sides now hold matching symmetric session keys for the rest of the conversation.

SSL also supports **session resumption**: if a client wants to reconnect using a previously negotiated session ID, and the server still has that session cached, both sides can skip straight to exchanging `Finished` messages under the already-known key material — much cheaper than a full handshake, which matters a lot for TLS-heavy workloads like busy web servers.

**SSL itself (all versions) is now obsolete and disabled by default nearly everywhere** — SSLv2 and SSLv3 both have serious, practical, publicly demonstrated flaws (see the **DROWN attack** in [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md)). "SSL" survives today mostly as informal shorthand people still use when they mean TLS.

## Transport Layer Security (TLS)

TLS is SSL's formal successor (same overall handshake philosophy, materially hardened cryptography and protocol design) and is what actually secures the modern web, email, and most other encrypted internet traffic. TLS is composed of two layered protocols:

### TLS Record Protocol

Sits underneath the handshake and handles the actual data transport once keys are established:

- Fragments outgoing data into manageable blocks, reassembles incoming fragments
- Optionally compresses outgoing data / decompresses incoming data
- Applies a MAC to outgoing data and verifies it on incoming data
- Encrypts outgoing data / decrypts incoming data
- Hands the result off to the underlying TCP layer for transport

Provides two guarantees: the connection is **private** (symmetric encryption, using keys negotiated by the handshake protocol) and **reliable** (integrity checking via keyed MAC using a secure hash function).

### TLS Handshake Protocol

Runs on top of the record protocol and is responsible for authentication and key agreement before any application data flows:

1. **Client Hello** — client's supported protocol version, random value, and cipher suites.
2. **Server Hello** — server's chosen version, random value, and cipher suite.
3. **Certificate + optional Certificate Request** — server sends its certificate for authentication; may request the client's certificate too (mutual TLS).
4. **Server Hello Done.**
5. Client sends its own certificate if requested, generates a random **pre-master secret**, encrypts it with the server's public key, and sends it. Both sides independently derive the same **master secret** and session keys from this shared pre-master secret.
6. **Change Cipher Spec + Finished (client)** — client signals it's switching to the new session keys.
7. **Change Cipher Spec + Finished (server)** — server does the same. Application data now flows over the Record Protocol using the negotiated session keys.

This provides three connection-security properties: peer identity authentication (via asymmetric cryptography, generally optional for the client and effectively mandatory for the server), secure negotiation of the shared secret (an eavesdropper watching the whole handshake still can't derive the session keys), and reliable negotiation (tampering with handshake messages in transit is detectable via the `Finished` hash checks — the same mechanism SSL used).

**Practical note (current as of TLS 1.3):** modern TLS collapses this to a **one round-trip** handshake by default (vs. the two round-trips shown above, which describes the classic TLS 1.2/SSL flow) — the client sends its key-share alongside its Hello, letting the server respond with everything needed to finish in a single additional round trip, and it drops support for the weaker legacy cipher suites (static RSA key exchange, CBC-mode ciphers without AEAD, compression) entirely, closing off several of the attack classes covered in [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md) at the protocol level rather than relying on implementations to avoid them.

## Cryptography toolkits for SSL/TLS

**OpenSSL** (`openssl.org`) is the standard open-source toolkit implementing SSL/TLS and the surrounding cryptographic primitives — see the full command reference in [`06-cryptography-tools-and-openssl.md`](06-cryptography-tools-and-openssl.md), including live handshake testing with `openssl s_client`.

Next: [`08-email-encryption.md`](08-email-encryption.md) — where the digital-signature and hybrid-encryption patterns from this file get applied specifically to email.
