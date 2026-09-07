# 09 — Disk Encryption

## The concept

Disk (or volume) encryption protects data **at rest** — while it's sitting on physical media, whether that's a laptop's internal SSD, a USB flash drive, an external HDD, or a backup — by converting every bit stored on the disk into unreadable ciphertext using disk-encryption software or hardware. It's a fundamentally different threat model from the network-oriented encryption covered in [`07`](07-pki-digital-signatures-ssl-tls.md) and [`08`](08-email-encryption.md): the attacker here typically has **physical possession** of the storage device (a stolen laptop, a discarded drive, a seized machine), not just network visibility.

Disk encryption gives you:

- **Confidentiality and privacy** via passphrases and, in some tools, **hidden volumes** — an encrypted volume nested inside another encrypted volume, providing plausible deniability, since there's no way to prove a hidden volume exists without the specific passphrase that reveals it.
- **Protection even when the OS is offline** — the encrypted volume is unreadable whether or not the operating system that normally manages it is running, which is exactly what makes it effective against "just remove the drive and read it on another machine" attacks.
- Coverage across **removable media** (USB flash drives), **external drives**, and **backups**, not just the primary system disk.

The mechanics work similarly to symmetric text-message encryption: an encryption program scrambles the disk's contents into illegible code, and only decryption with the correct key/passphrase makes it usable again. This matters most whenever sensitive information physically travels — a laptop leaving the building, a backup drive being shipped, a decommissioned server's storage being disposed of — and any system holding valuable data or exposed to loss/theft risk should have it enabled by default, not as an afterthought.

## Windows disk encryption tools

### VeraCrypt (`veracrypt.fr`)

An **on-the-fly encryption (OTFE)** tool for creating and maintaining encrypted volumes — data is automatically encrypted immediately before being written to disk and decrypted immediately after being read, entirely transparently, with no separate "encrypt this file" step required from the user. Once a VeraCrypt volume is mounted, files can be dragged and dropped to/from it exactly like any normal disk; VeraCrypt handles encryption/decryption in RAM on the fly. The **entire file system** inside the volume is encrypted — file names, folder names, free space, and metadata, not just file contents — which prevents an attacker from learning anything about the volume's structure without the password/keyfile.

VeraCrypt is the actively maintained continuation of the older TrueCrypt project, and it's the tool used in the hands-on brute-forcing lab in [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md) — worth installing if you want to follow that lab yourself.

### Rohos Disk Encryption (`rohos.com`)

Creates hidden, encrypted partitions on a local computer, a USB flash drive, or inside a cloud-storage folder (Google Drive, OneDrive, Dropbox) — meaning the encrypted container itself can sync through a cloud provider while the provider only ever sees opaque ciphertext. Uses NIST-approved AES with a 256-bit key and supports automatic mount/encryption workflows.

### BitLocker Drive Encryption (built into Windows, `microsoft.com`)

Windows' native full-volume encryption, providing offline-data and OS protection: it ensures data on a Windows-formatted volume stays unreadable if the drive is removed or the installed OS is tampered with while offline. BitLocker's key protection is built around the **TPM** (see [`05-hardware-quantum-and-modern-crypto.md`](05-hardware-quantum-and-modern-crypto.md)) — the TPM verifies early boot-component integrity and only releases the decryption key if the boot chain looks untampered, which is what lets BitLocker unlock transparently on a healthy system while refusing to unlock (or demanding a recovery key) if, say, someone has swapped the bootloader or moved the drive to different hardware.

Managed via `Control Panel → System and Security → BitLocker Drive Encryption`, with options to turn BitLocker on/off per drive, add unlock methods (password, smart card), enable auto-unlock, and manage the TPM directly.

### Other Windows/general disk-encryption tools

Symantec Encryption (`broadcom.com`), SafeGuard Enterprise Encryption (`sophos.com`), GiliSoft Full Disk Encryption (`gilisoft.com`), Check Point Full Disk Encryption (`checkpoint.com`), DiskCryptor (`diskcryptor.org`).

## Linux disk encryption

### Cryptsetup / LUKS

`cryptsetup` is the standard command-line utility for setting up disk encryption on the **DMCrypt** kernel module — the Linux kernel's native block-device encryption layer. It supports several on-disk formats: plain `dm-crypt` volumes, **LUKS** (Linux Unified Key Setup — the standard, most widely used format, supporting multiple passphrases/keyslots per volume), `loop-AES`, TrueCrypt/VeraCrypt-compatible volumes, and BitLocker-compatible volumes (useful for reading a BitLocker-encrypted drive from Linux).

```bash
cryptsetup --help          # full option reference for the installed version

# Create a new LUKS-encrypted partition (interactive passphrase prompt, confirm "YES")
sudo cryptsetup luksFormat /dev/sdX1

# Open (unlock) it, mapping it to a device-mapper name
sudo cryptsetup open /dev/sdX1 my_encrypted_volume

# The unlocked volume now appears at /dev/mapper/my_encrypted_volume — format and mount normally
sudo mkfs.ext4 /dev/mapper/my_encrypted_volume
sudo mount /dev/mapper/my_encrypted_volume /mnt/secure

# When done, unmount and lock it back up
sudo umount /mnt/secure
sudo cryptsetup close my_encrypted_volume

# Inspect a LUKS header without unlocking (algorithm, key slots, etc.)
sudo cryptsetup luksDump /dev/sdX1
```

**Other Linux-specific tools:** Cryptmount (`cryptmount.sourceforge.net`) — simplifies mounting/unmounting encrypted filesystems as an ordinary user without needing root for routine use; Tomb (`dyne.org`) — a lightweight wrapper around LUKS with a friendlier CLI; CryFS (`cryfs.org`) — designed specifically for encrypting files *before* they sync to untrusted cloud storage; GnuPG (`gnupg.org`) — file-level rather than volume-level encryption, covered fully in [`08-email-encryption.md`](08-email-encryption.md); Harmony Endpoint (`checkpoint.com`) — enterprise endpoint encryption/management.

## macOS disk encryption

### FileVault (built into macOS, `support.apple.com`)

Uses **XTS-AES-128** encryption (a tweaked-codebook mode of AES specifically designed for disk-sector encryption, where each sector needs to be independently encryptable/decryptable without depending on neighboring sectors) combined with a 256-bit key, to protect the startup disk. Available on macOS Lion and later. Once enabled, the user must authenticate at boot with their account password; encryption then proceeds transparently in the background, and any new file written to the startup disk is encrypted automatically as it's created.

Managed via `System Settings → Privacy & Security → FileVault → Turn On...` — enabling it generates a recovery key (store this somewhere safe and separate from the machine; losing both your password and the recovery key means permanent data loss, by design).

**Other macOS-compatible tools:** VeraCrypt (`veracrypt.fr` — cross-platform, same tool as the Windows section above), BestCrypt Volume Encryption (`jetico.com`), Dell Full Disk Encryption (`dell.com`), Comodo Disk Encryption (`comodo.com`), GravityZone Full Disk Encryption (`bitdefender.com`).

## Practical guidance

- **Enable full-disk encryption by default on every laptop and removable drive** — BitLocker/FileVault are free, built-in, and low-friction; there's very little reason not to.
- **Use VeraCrypt (or LUKS on Linux) when you specifically need**: cross-platform portability, hidden/deniable volumes, or encrypting individual containers rather than a whole drive.
- **Never store your recovery key/passphrase in the same location as the encrypted device** — a recovery key taped to a laptop, or a LUKS keyfile stored on the same encrypted drive it unlocks, defeats the entire point.
- If you want to understand what happens when disk encryption is attacked rather than just deployed, the hands-on VeraCrypt hash-extraction-and-cracking lab in [`11-cryptanalysis-and-attacks.md`](11-cryptanalysis-and-attacks.md) walks through it end to end with real `dd` and `hashcat` commands.

Next: [`10-blockchain-cryptography.md`](10-blockchain-cryptography.md) — a newer application of much of the hashing and asymmetric-crypto material from earlier files.
