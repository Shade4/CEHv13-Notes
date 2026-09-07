# 06 — Cryptography Tools and OpenSSL

## General-purpose encryption tools

| Tool | Source | What it does |
|---|---|---|
| BCTextEncoder | jetico.com | Compresses, encrypts, and converts plaintext into portable encoded text (paste-to-clipboard or save-as-file); supports both password-based and public-key encryption |
| CryptoForge | cryptoforge.com | File/folder/text encryption suite |
| AxCrypt | axcrypt.net | File encryption with cloud-storage integration (Dropbox, Google Drive, OneDrive) |
| Microsoft Cryptography Tools | microsoft.com | Built-in Windows/​.NET cryptographic APIs and utilities |
| Concealer | belightsoft.com | macOS file/password vault with encryption |
| SensiGuard | sensiguard.com | File/folder encryption and hiding |
| Cypherix | cypherix.com | File and email encryption suite |

### BCTextEncoder walkthrough

BCTextEncoder is a good example of the general "encode confidential text" tool pattern: paste or type plaintext into the top pane, choose an encryption method (password-based, shown as `Encode by: password` in the tool, or select a public key), click **Encode**, and the tool produces a Base64-armored block in the bottom pane — starting with a `-----BEGIN ENCODED MESSAGE-----` header — that's safe to paste into an email body, chat, or any text-only channel. **Decode** reverses the process given the correct password or private key.

## Cryptography toolkits (developer/CLI-focused)

| Toolkit | Source | Notes |
|---|---|---|
| **OpenSSL** | openssl.org | The de facto standard — command-line + library, implements SSL/TLS and the surrounding cryptography ecosystem (key/cert management, symmetric/asymmetric primitives, hashing) |
| wolfSSL | wolfssl.com | Lightweight TLS library, popular in embedded/IoT |
| AES Crypto Toolkit | ni.com | Hardware-oriented AES implementation toolkit |
| Libsodium | github.com/jedisct1/libsodium | Modern, misuse-resistant crypto library (NaCl successor) |
| Crypto++ | cryptopp.com | C++ cryptographic library, broad algorithm coverage |
| PyCryptodome | github.com/Legrandin/pycryptodome | Python cryptography library (PyCrypto successor) |

## OpenSSL command reference

OpenSSL is worth knowing at the command line even if you never touch its C API — it's installed by default on almost every Linux distribution and macOS, and it's the fastest way to inspect, generate, or test anything covered elsewhere in this repo.

### See what your OpenSSL build supports

```bash
openssl version -a              # version, build flags, OpenSSL dir
openssl enc -ciphers            # every symmetric cipher/mode this build supports
openssl list -digest-algorithms # every hash algorithm supported
```

Sample output from `openssl enc -ciphers` (trimmed) shows the sheer breadth of cipher/mode combinations a modern OpenSSL build ships with:

```
Supported ciphers:
-aes-128-cbc   -aes-128-cfb   -aes-128-cfb1   -aes-128-cfb8
-aes-128-ctr   -aes-128-ecb   -aes-128-ofb    -aes-192-cbc
-aes-256-cbc   -aes-256-ctr   -aes-256-ecb    -aes-256-ofb
-aria-128-cbc  -aria-256-gcm  -bf-cbc         -bf-ecb
-blowfish      -camellia-256-cbc  -chacha20   -des-ede3-cbc
...
```

### Symmetric encryption/decryption

```bash
# Encrypt a file with AES-256 in GCM mode (authenticated — recommended)
openssl enc -aes-256-gcm -salt -pbkdf2 -iter 100000 -in secret.txt -out secret.enc

# Decrypt it back
openssl enc -d -aes-256-gcm -pbkdf2 -iter 100000 -in secret.enc -out secret.txt
```

`-pbkdf2 -iter 100000` derives the actual encryption key from your passphrase via PBKDF2 with 100,000 iterations (see key stretching in [`12-quantum-attacks-and-countermeasures.md`](12-quantum-attacks-and-countermeasures.md)) — always include this rather than relying on OpenSSL's legacy weak key derivation.

### Hashing

```bash
openssl dgst -sha256 file.txt
openssl dgst -sha256 -hmac "sharedsecret" file.txt   # HMAC-SHA256
```

### RSA key pairs and signing

```bash
# Generate a 4096-bit RSA private key
openssl genrsa -out private.pem 4096

# Extract the matching public key
openssl rsa -in private.pem -pubout -out public.pem

# Sign a file with the private key
openssl dgst -sha256 -sign private.pem -out file.sig file.txt

# Verify the signature with the public key
openssl dgst -sha256 -verify public.pem -signature file.sig file.txt
```

### Elliptic-curve key pairs

```bash
openssl ecparam -name prime256v1 -genkey -noout -out ec_private.pem
openssl ec -in ec_private.pem -pubout -out ec_public.pem
```

### Certificate operations (ties directly into [`07-pki-digital-signatures-ssl-tls.md`](07-pki-digital-signatures-ssl-tls.md))

```bash
# Generate a self-signed certificate (10-year validity) with a new 2048-bit RSA key
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout selfsigned.key -out selfsigned.crt -days 3650 \
  -subj "/CN=example.local"

# Generate a Certificate Signing Request (CSR) to send to a real CA
openssl req -new -newkey rsa:2048 -nodes \
  -keyout domain.key -out domain.csr \
  -subj "/CN=example.com"

# Inspect a certificate's contents (issuer, validity, SANs, etc.)
openssl x509 -in cert.pem -noout -text

# Verify a certificate chain against a trusted CA bundle
openssl verify -CAfile ca-bundle.crt cert.pem
```

### Testing a live TLS connection

```bash
# Connect to a server and dump the full certificate chain + negotiated cipher
openssl s_client -connect example.com:443 -showcerts

# Check what TLS versions a server accepts (repeat with -tls1_2, -tls1_3, etc.)
openssl s_client -connect example.com:443 -tls1_2
```

This is one of the fastest ways to confirm whether a server still accepts a deprecated protocol version (SSLv3, TLS 1.0/1.1) or a weak cipher suite during a security assessment — a clean refusal (`handshake failure`) when you try `-ssl3` or `-tls1` is a good sign; a successful connection is a finding worth flagging.

See [`cheatsheets/openssl-cheatsheet.md`](cheatsheets/openssl-cheatsheet.md) for a condensed one-page version of everything above, organized by task rather than by explanation.

Next: [`07-pki-digital-signatures-ssl-tls.md`](07-pki-digital-signatures-ssl-tls.md) — where certificates, PKI, and the SSL/TLS handshake this file just tested actually come from.
