# 02 — Symmetric Encryption Algorithms

Quick-reference table first, detailed writeups below. All of these are **block ciphers** unless marked stream.

| Algorithm | Type | Key size(s) | Block size | Status / where you'll see it |
|---|---|---|---|---|
| DES | Block | 56 bits (+8 parity) | 64 bits | Broken — legacy systems only |
| 3DES (Triple DES) | Block | 112 or 168 bits | 64 bits | Deprecated — legacy payment systems |
| AES | Block | 128 / 192 / 256 bits | 128 bits | **Current standard** — everywhere |
| RC4 | Stream | 40–2048 bits (variable) | n/a | Broken — avoid (legacy WEP/old TLS) |
| RC5 | Block | 0–2040 bits (variable) | 32/64/128 bits | Rare today, historically influential |
| RC6 | Block | 128/192/256 bits | 128 bits | AES finalist, rarely deployed |
| Blowfish | Block | 32–448 bits | 64 bits | Legacy, still in bcrypt |
| Twofish | Block | up to 256 bits | 128 bits | AES finalist, some disk-encryption use |
| Threefish | Block | 256/512/1024 bits | = key size | Part of the Skein hash function |
| Serpent | Block | 128/192/256 bits | 128 bits | AES finalist, high security margin |
| Camellia | Block | 128/192/256 bits | 128 bits | Used in TLS, Japanese standard |
| TEA | Block | 128 bits | 64 bits | Simple/educational, superseded by XTEA |
| CAST-128 | Block | 40–128 bits | 64 bits | Default cipher in older GPG/PGP |
| CAST-256 | Block | 128–256 bits | 128 bits | AES-contest entrant |
| GOST (Magma) | Block | 256 bits | 64 bits | Russian national standard |
| ChaCha20 | Stream | 256 bits | n/a | **Current standard** — TLS 1.3, WireGuard |
| Salsa20 | Stream | 256 bits | n/a | ChaCha20's predecessor |

## Data Encryption Standard (DES)

DES was the first widely adopted government/commercial block cipher standard, using a 64-bit key of which only 56 bits are actual key material (the remaining 8 bits are parity/error-detection). It's built on the **Feistel network** structure and processes data in 64-bit blocks through 16 rounds.

DES offers roughly 2⁵⁶ ≈ 72 quadrillion possible keys, which sounded enormous in 1977 but is now well within reach of purpose-built or even cloud-rented hardware — a dedicated brute-force machine (the EFF's "Deep Crack") cracked a DES key in under a day back in 1998. **DES should not be used for anything today.** It's covered here because you'll still encounter it in legacy systems and because 3DES and AES were both explicitly designed as its successors.

## Triple DES (3DES / TDEA)

An interim fix while the industry waited for AES: run DES three times with a "key bundle" of three 56-bit keys (K1, K2, K3):

```
Ciphertext = E(K3, D(K2, E(K1, Plaintext)))
```

Note the middle operation is *decrypt*, not encrypt — this "encrypt-decrypt-encrypt" (EDE) pattern is a deliberate design choice that makes 3DES backward-compatible with single DES when K1=K2=K3.

Three keying options exist:
- **Option 1** — K1, K2, K3 all independent (168-bit effective security, most secure)
- **Option 2** — K1 = K3, K2 independent (112-bit effective security, most common in practice)
- **Option 3** — K1 = K2 = K3 (equivalent to plain single DES — least secure, exists only for backward compatibility)

3DES is itself now deprecated (NIST disallowed it for new applications starting 2023) due to a 64-bit block size that makes it vulnerable to birthday-bound collision attacks (see the **Sweet32** attack, and the birthday-attack math in [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md)) — but you'll still find it in older payment/financial infrastructure that hasn't been migrated to AES yet.

## Advanced Encryption Standard (AES)

AES is the NIST-selected standard (originally the winner of a public competition, under the name **Rijndael**, designed by Joan Daemen and Vincent Rijmen) for encrypting electronic data, in use worldwide for everything from disk encryption to TLS to government classified-but-unclassified data.

- Fixed 128-bit block size
- Key sizes of 128, 192, or 256 bits — commonly called AES-128, AES-192, AES-256
- An **iterated** (round-based) cipher, *not* a Feistel network — every round transforms the entire block state, unlike DES's split-half approach
- Round count depends on key size: 10 rounds (AES-128), 12 rounds (AES-192), 14 rounds (AES-256)

Each round (except the last) runs four transformations on a 4×4 byte matrix called the **state**:

1. **SubBytes** — a non-linear byte-for-byte substitution using a fixed S-box (this is what gives AES its resistance to linear and differential cryptanalysis)
2. **ShiftRows** — cyclically shifts each row of the state by a different offset (diffusion across columns)
3. **MixColumns** — a linear transformation that mixes the bytes *within* each column (diffusion across rows) — omitted in the final round
4. **AddRoundKey** — XORs the state with a subkey derived from the main key via the key schedule

In pseudocode form:

```
Cipher(byte in[4*Nb], byte out[4*Nb], word w[Nb*(Nr+1)])
begin
    byte state[4, Nb]
    state = in
    AddRoundKey(state, w)

    for round = 1 step 1 to Nr-1
        SubBytes(state)
        ShiftRows(state)
        MixColumns(state)
        AddRoundKey(state, w + round*Nb)
    end for

    SubBytes(state)
    ShiftRows(state)
    AddRoundKey(state, w + Nr*Nb)

    out = state
end
```

`Nb` = block size in 32-bit words (always 4 for AES), `Nr` = number of rounds, `w` = the expanded key schedule.

**No practical cryptanalytic shortcut against full-round AES is currently known** — the best published attacks (biclique attacks) only reduce brute-force effort by a small constant factor, not enough to matter in practice. Nearly all real-world weaknesses attributed to "AES" are actually implementation issues: bad mode-of-operation choice (see ECB above), key management failures, or side-channel leakage from software implementations that don't run in constant time — not a break of the algorithm itself.

## RC4, RC5, RC6 — the RSA Security stream/block family

- **RC4** — a variable-key-size stream cipher, byte-oriented, based on a pseudorandom permutation. Extremely fast in software, which made it popular for TLS and WEP/WPA (wireless) in the 2000s. **Now broken** — multiple statistical biases in its keystream have been demonstrated, and it's been formally prohibited in TLS since RFC 7465 (2015). See the WEP/related-key-attack case study in [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md) for exactly how the biases get exploited.
- **RC5** — a parameterized block cipher by Ron Rivest: variable block size (32/64/128 bits), variable key size (0–2040 bits), variable round count (0–255). Its core operations are integer addition, bitwise XOR, and *data-dependent rotation* — the rotation amount depends on the data itself, which was a novel idea at the time and made RC5 relatively resistant to linear/differential cryptanalysis for its era.
- **RC6** — derived from RC5, entered as an AES-contest finalist. Adds integer *multiplication* (for faster diffusion in fewer rounds) and uses four 32-bit working registers instead of RC5's two, sized to match AES's 128-bit block.

## Blowfish

Designed by Bruce Schneier as a fast, free, unpatented replacement for DES. 64-bit blocks, variable key length from 32 to 448 bits, 16-round Feistel structure.

Key expansion is unusually elaborate: it builds an 18-entry 32-bit **P-array** and four 256-entry **S-boxes**, initialized from a fixed digits-of-π constant, then XORs the key material into the P-array and repeatedly re-encrypts an all-zero string to generate the final subkeys — over 500 encryption operations just to set up the key schedule. This makes Blowfish deliberately slow to *re-key*, which is a feature for password hashing (this exact property is why **bcrypt** — see [`12-quantum-attacks-and-countermeasures.md`](12-quantum-attacks-and-countermeasures.md) → key stretching — is built on a variant of Blowfish's key setup) but a poor fit for anything that needs to change keys frequently.

Blowfish's 64-bit block size is its main modern weakness (same birthday-bound issue as 3DES).

## Twofish, Threefish, Serpent — the other AES finalists

- **Twofish** — designed by a team including Schneier, Kelsey, Wagner, Ferguson, Whiting, and Hall. 128-bit blocks, up to 256-bit keys, Feistel structure. Lost to Rijndael in the AES competition but is still considered secure and shows up in some disk-encryption products (it's one of the cascade options in VeraCrypt — see [`09-disk-encryption.md`](09-disk-encryption.md)).
- **Threefish** — a large tweakable block cipher where block size *equals* key size (256, 512, or 1024 bits), built entirely from addition-rotation-XOR (ARX) operations with no S-boxes at all (a deliberate choice to resist cache-timing side-channel attacks — see [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md)). It's the block cipher inside the **Skein** hash function, a SHA-3 competition finalist.
- **Serpent** — designed by Anderson, Biham, and Knudsen with an unusually conservative security margin: 32 rounds (double what was considered necessary at the time), 128-bit blocks, 128/192/256-bit keys. Widely regarded as *more* conservatively secure than Rijndael, but it lost the AES competition partly because it was slower.

## Tiny Encryption Algorithm (TEA)

A deliberately minimal cipher by David Wheeler and Roger Needham (1994) — small enough to implement in a handful of lines of C. 64-bit blocks, 128-bit key, Feistel structure run for 64 rounds (32 Feistel "cycles"), using only addition, XOR, and bit-shift — no S-boxes, no lookup tables. Uses a constant derived from the golden ratio (`delta = ⌊2³²/φ⌋`) to prevent certain slide attacks. TEA has known weaknesses (related-key attacks, equivalent keys) that its successor **XTEA** was designed to fix — worth knowing TEA mainly as a teaching example of Feistel-cipher design simplicity.

## CAST-128 / CAST-256

- **CAST-128** (also called CAST5) — a 12- or 16-round Feistel cipher, 64-bit blocks, key sizes from 40 to 128 bits in 8-bit increments. Notable mainly because it was the **default cipher in GPG/PGP** for years.
- **CAST-256** — extends CAST-128 to 128-bit blocks and 128–256-bit keys, submitted to the AES competition (didn't win).

## GOST (Magma)

The Russian government/GOST national standard block cipher (also called Magma) — 64-bit blocks, 256-bit key, 32-round Feistel network, and a notable design quirk: the S-boxes can be kept secret as *additional* key material beyond the 256-bit key itself, meaning the effective security parameter can be higher than the nominal key size suggests. **Kuznyechik** is GOST's modern successor, using 128-bit blocks.

## Camellia

A joint Mitsubishi/NTT design, 128-bit blocks, 128/192/256-bit keys, Feistel structure with either 18 rounds (128-bit key) or 24 rounds (256-bit key). Notable for being one of the few non-AES ciphers formally included as an option in the **TLS** cipher suite registry, and for offering AES-equivalent security and performance while remaining royalty-free.

## ChaCha20 and Salsa20

Both designed by Daniel J. Bernstein — Salsa20 first, ChaCha20 as a refined successor. Stream ciphers, 256-bit keys, built entirely from add-rotate-XOR operations on a 4×4 matrix of 32-bit words (similar ARX philosophy to Threefish above).

**ChaCha20 matters a lot today**: paired with the **Poly1305** MAC as ChaCha20-Poly1305, it's one of the two mandatory-to-implement AEAD cipher suites in TLS 1.3 (alongside AES-GCM), and it's the *only* cipher used by the WireGuard VPN protocol. Its main practical advantage over AES is that it's fast in pure software **without** hardware AES acceleration (no AES-NI instruction needed) — which matters a lot on mobile devices, IoT, and older/embedded CPUs, where ChaCha20 can be significantly faster and more side-channel-resistant than a software (non-accelerated) AES implementation.

## Practical takeaway

If you're choosing a symmetric cipher for something new in 2026: **AES-256-GCM** or **ChaCha20-Poly1305**. Everything else in this file is here so you can recognize it, understand its role in the ecosystem's history, or troubleshoot a legacy system — not because you should reach for it in new designs.

Next: [`03-asymmetric-encryption-algorithms.md`](03-asymmetric-encryption-algorithms.md) for the public-key side of the picture.
