# OpenSSL Cheatsheet

One-page, task-organized OpenSSL command reference. Full explanations live in [`../06-cryptography-tools-and-openssl.md`](../06-cryptography-tools-and-openssl.md).

## Discovery

```bash
openssl version -a                    # version + build info
openssl enc -ciphers                  # list supported symmetric ciphers
openssl list -digest-algorithms       # list supported hash algorithms
```

## Hashing

```bash
openssl dgst -sha256 file.txt
openssl dgst -md5 file.txt
openssl dgst -sha256 -hmac "secret" file.txt        # HMAC
```

## Symmetric encryption (AES)

```bash
# Encrypt (AES-256-GCM, password-derived key via PBKDF2)
openssl enc -aes-256-gcm -salt -pbkdf2 -iter 100000 -in plain.txt -out cipher.enc

# Decrypt
openssl enc -d -aes-256-gcm -pbkdf2 -iter 100000 -in cipher.enc -out plain.txt
```

## RSA keys

```bash
openssl genrsa -out private.pem 4096                          # generate private key
openssl rsa -in private.pem -pubout -out public.pem            # derive public key
openssl rsa -in private.pem -check                             # validate a key
openssl rsa -in private.pem -text -noout                       # inspect key details
```

## EC keys

```bash
openssl ecparam -list_curves                                   # list supported curves
openssl ecparam -name prime256v1 -genkey -noout -out ec_priv.pem
openssl ec -in ec_priv.pem -pubout -out ec_pub.pem
```

## Signing and verification

```bash
openssl dgst -sha256 -sign private.pem -out file.sig file.txt
openssl dgst -sha256 -verify public.pem -signature file.sig file.txt
```

## Certificates and PKI

```bash
# Self-signed cert + new key in one step
openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 3650 -subj "/CN=example.local"

# CSR to submit to a real CA
openssl req -new -newkey rsa:2048 -nodes -keyout domain.key -out domain.csr -subj "/CN=example.com"

# Inspect a certificate
openssl x509 -in cert.pem -noout -text
openssl x509 -in cert.pem -noout -dates            # just validity window
openssl x509 -in cert.pem -noout -subject -issuer  # just subject/issuer

# Verify a chain
openssl verify -CAfile ca-bundle.crt cert.pem

# Convert formats
openssl x509 -in cert.pem -outform DER -out cert.der            # PEM -> DER
openssl x509 -in cert.der -inform DER -outform PEM -out cert.pem # DER -> PEM
openssl pkcs12 -export -in cert.pem -inkey key.pem -out bundle.pfx  # PEM -> PFX/PKCS12
```

## Live TLS testing

```bash
# Full handshake + certificate chain dump
openssl s_client -connect example.com:443 -showcerts

# Force a specific protocol version (useful for checking legacy protocol exposure)
openssl s_client -connect example.com:443 -tls1_2
openssl s_client -connect example.com:443 -tls1_3

# Check certificate expiry remotely without saving anything
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
```

## Random data / key material

```bash
openssl rand -hex 32          # 32 random bytes, hex-encoded (good for a 256-bit key)
openssl rand -base64 32       # same, base64-encoded
```
