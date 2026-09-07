# 08 — Email Encryption

Email is plaintext by default. SMTP was never designed with confidentiality in mind, and while opportunistic TLS between mail servers (STARTTLS) protects messages *in transit* between servers, it does nothing to stop the receiving mail provider, a compromised mailbox, or anyone with access to a stored copy from reading the content. Everything in this file is about protecting the *message itself*, end-to-end, independent of which servers happen to relay it.

## Pretty Good Privacy (PGP)

PGP is a hybrid cryptosystem (see the hybrid-encryption pattern first introduced in [`01-cryptography-fundamentals.md`](01-cryptography-fundamentals.md) and applied to RSA specifically in [`03-asymmetric-encryption-algorithms.md`](03-asymmetric-encryption-algorithms.md)) purpose-built for encrypting/decrypting messages, files, and directories, and for digitally signing content — combining the *speed* of conventional (symmetric) cryptography, which PGP uses for the actual bulk data (roughly 1000× faster than public-key encryption for the same volume of data), with the *key-management convenience* of public-key cryptography, which PGP uses only to protect a small one-time symmetric key. Traditionally, PGP uses RSA for key transport and digital signatures, IDEA for bulk symmetric encryption, and MD5 for message digests — though modern implementations support far stronger, current algorithm choices throughout.

### How PGP encryption works

1. PGP **compresses the plaintext** first. This isn't just about saving bandwidth — reducing the redundant patterns in plaintext *before* encryption meaningfully reduces the patterns cryptanalysts have to work with, making the ciphertext more resistant to certain classes of statistical attack.
2. PGP generates a fresh, random, one-time-only **session key**.
3. The plaintext (now compressed) is encrypted using that session key with a fast symmetric cipher.
4. The session key itself is encrypted using the **recipient's public key** (RSA).
5. The encrypted session key is bundled together with the symmetric ciphertext and sent as a single encrypted message.

### How PGP decryption works (the exact reverse)

1. The recipient's copy of PGP uses their **private key** (never the public key) to decrypt the bundled session key.
2. PGP uses that recovered session key to decrypt the actual symmetric ciphertext back into the original (still-compressed) plaintext.
3. The result is decompressed to recover the original message.

### What PGP is used for

- Encrypting a message or file before transmission so only the intended recipient can decrypt and read it
- "Clear-signing" a plaintext message — attaching a signature without encrypting the body, so the message stays human-readable but its authenticity/integrity can still be verified
- Encrypting stored files so no one but the person who encrypted them can decrypt them
- Securely deleting files (overwriting rather than just unlinking them from a directory)
- Data compression for storage or transmission efficiency

## GNU Privacy Guard (GPG)

GPG is a free, open-source, drop-in software replacement for PGP and a full implementation of the **OpenPGP standard** (RFC 4880). Like PGP, it's a hybrid encryption system — combining symmetric-key speed with public-key convenience — and it additionally supports S/MIME and Secure Shell (SSH). Modern GPG builds support elliptic-curve cryptography (ECDSA, ECDH, EdDSA) alongside classic RSA, and use the Libgcrypt cryptographic library under the hood.

**GPG is used for:**

- Proper key management for both private and public keys
- Creating new key pairs, and exporting/importing keys (including ASCII-armored text format for pasting into emails)
- Publishing a public key to a keyserver, signed with the owning key's public signature
- Deleting a private key from local storage when it's no longer needed
- Encrypting and signing files (for email or FTP transport) using asymmetric keys
- Decrypting and verifying signatures on received encrypted files
- Detaching signatures (keeping the signature as a separate file from the signed message)
- Building and managing a **web of trust** (below)
- Automatically securing messages in chat applications that support the OpenPGP standard

### How GPG works, end to end

**Signing and encrypting:**

1. The raw file is signed using the **sender's private key** (proving authorship and integrity).
2. The (now-signed) file is separately encrypted using the **receiver's public key**.
3. The result — a signed-and-encrypted file — can be stored locally, distributed via FTP, or sent as an email attachment.

**Decrypting and verifying:**

1. GPG searches for the **receiver's private key** to decrypt the file (since it was asymmetrically encrypted, only the intended receiver's private key will work).
2. After decryption, GPG automatically verifies the attached signature using the **sender's public key** — confirming both who sent it and that it wasn't altered.

### Web of Trust (WoT)

PKI (see [`07-pki-digital-signatures-ssl-tls.md`](07-pki-digital-signatures-ssl-tls.md)) relies on **centralized** trust — a small number of CAs that everyone agrees to trust in advance. PGP/OpenPGP/GnuPG systems instead default to a **decentralized** trust model called the **Web of Trust**: everyone is, in effect, their own certificate authority, and trust propagates through a network of individuals who vouch for each other by signing each other's public keys.

**How it works:** every user maintains a personal ring of public keys they've collected, and they introduce (vouch for) other users they personally trust. Two users can have a **direct trust** relationship (they've verified each other's key fingerprint in person or through some other reliable channel) or an **indirect trust** relationship (each trusts the other because a mutually trusted third party vouches for both). If Alice directly trusts Bob, and Bob directly trusts Henry, Alice can extend indirect trust to Henry through Bob — without ever verifying Henry's key herself. The practical tradeoff versus centralized PKI: no single point of failure or centralized authority to compromise or subpoena, but trust propagation is inherently fuzzier and depends on the diligence of every link in the chain — one careless "I'll just sign anything" participant can weaken the whole network's trust guarantees.

## S/MIME encryption in Outlook

Secure/Multipurpose Internet Mail Extensions (S/MIME) is the PKI-based (centralized-trust) alternative to PGP/GPG — it uses certificate-based public keys rather than a web of trust, which is why it integrates cleanly with corporate PKI and Outlook's built-in certificate handling.

**Setting a default signing/encryption certificate:**

1. `File → Options → Trust Center → Trust Center Settings`
2. Select **Email Security** in the left pane.
3. Under **Encrypted email**, click **Settings** beside "Default Setting."
4. In the **Change Security Settings** dialog, under **Certificates and Algorithms**, choose your **Signing Certificate** and **Encryption Certificate**, then click **OK**.

**Encrypting a single outgoing message:** `File → Properties` on the open message → **Security Settings** → check **Encrypt message contents and attachments** → **OK**.

**Encrypting every outgoing message by default:** `File → Options → Trust Center → Trust Center Settings → Email Security` → check **Encrypt contents and attachments for all outgoing messages** → **OK**.

### Microsoft 365 Message Encryption (OME)

A cloud-native alternative that doesn't require the recipient to have a certificate at all — the recipient authenticates via their Microsoft 365 account or a one-time passcode instead. In a new message: `Options → Encrypt`, then choose the permission level — **Encrypt-Only**, **Do Not Forward**, or an org-specific label like **Confidential \ All Employees**.

## Signing/encrypting email on macOS (Apple Mail)

Apple Mail supports the same S/MIME certificate-based flow, driven from the macOS Keychain:

1. Open Apple Mail → `File → New Message`.
2. Click into the **From** field and select the account holding the relevant certificate in Keychain.
3. A signing icon (blue checkmark) appears automatically once a personal certificate is available in the keychain, indicating the outgoing message can be digitally signed.

**Receiving signed/encrypted mail on Mac:** a checkmark icon on a received message means it's digitally signed by a verified sender (click it to inspect the sender's certificate — any warning here means the message content doesn't match what was signed, or the signer's identity can't be verified). A closed-lock icon means the message is encrypted and requires your private key to read.

## Encrypting/decrypting email with OpenPGP in the browser — FlowCrypt walkthrough

PGP alone is vulnerable to being circumvented by weak endpoint security (if your device or account is compromised, encryption at the message layer doesn't help). Browser extensions that implement active OpenPGP directly inside webmail close that gap for services like Gmail that don't natively support PGP.

**FlowCrypt** (`flowcrypt.com`) is end-to-end email encryption software configured with OpenPGP, purpose-built for Gmail (personal, G Suite/Business/Enterprise). Full walkthrough:

**Setup:** install and configure the FlowCrypt browser extension in Chrome or Firefox, then log in to your Gmail account (`mail.google.com`) using the same browser.

**Sending (sender's end):**

1. Click **Secure Compose** in the left pane — a **New Secure Message** window pops up.
2. Enter the recipient's email address in the **To** field. If the recipient's name displays in green, they also have FlowCrypt installed and reachable — meaning the message can be fully end-to-end encrypted between both parties rather than password-protected.
3. Add a subject and body (and attachments, if needed).
4. Click **Encrypt, Sign and Send**.

**Receiving (recipient's end):**

1. The recipient sees the encrypted message arrive in their normal inbox (shown with a PGP-armored preview like `-----BEGIN PGP MESSAGE----- Version: FlowCrypt...`).
2. Clicking it opens FlowCrypt's decryption view, which — depending on configuration — may prompt for the recipient's PGP passphrase to decrypt.
3. Once decrypted, the message displays with **encrypted** and **signed** badges confirming both properties were verified.

## Email encryption tools (broader list)

| Tool | Source | Notes |
|---|---|---|
| RMail | rmail.com | Open tracking, delivery proof, encryption, e-signatures, large-file transfer; integrates with existing Outlook/Gmail |
| Mailvelope | mailvelope.com | Browser-extension OpenPGP for major webmail providers |
| Virtru | virtru.com | Email encryption with granular access controls, revocation |
| Webroot | webroot.com | Endpoint/email security suite |
| Secure Email (S/MIME) Certificates | ssl.com | Certificate issuance specifically for S/MIME |
| Proofpoint Email Protection | proofpoint.com | Enterprise email security/encryption gateway |
| Paubox | paubox.com | HIPAA-focused encrypted email, no recipient action required |

Next: [`09-disk-encryption.md`](09-disk-encryption.md) — protecting data at rest rather than in transit.
