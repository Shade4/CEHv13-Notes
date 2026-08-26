# Cheatsheet — Tools, Links & Commands

Every tool referenced across this repo, grouped by purpose, with official sources and the core
commands to install/launch each. **Authorized use only** — see the Legal & Ethical Use Notice in
the repo [`README.md`](../README.md).

---

## Phishing Simulation & Campaign Frameworks

| Tool | Official Source | Quick Start |
|---|---|---|
| **SET** (Social-Engineer Toolkit) | https://github.com/trustedsec/social-engineer-toolkit | `sudo setoolkit` (pre-installed on Kali/Parrot) |
| **Gophish** | https://getgophish.com | `./gophish` → admin UI at `https://localhost:3333` |
| **King Phisher** | https://github.com/rsmusllp/king-phisher | `king-phisher-server` then `king-phisher` (client) |
| **OhPhish** | https://portal.ohphish.com | Web SaaS — no install; log in to the portal |
| ShellPhish | https://github.com | `bash shellphish.sh` |
| BLACKEYE | https://github.com | `bash blackeye.sh` |
| SocialFish | https://github.com | `python3 SocialFish.py` |
| Modlishka | https://github.com | `./modlishka -config config.json` |
| Trape | https://github.com | `python3 trape.py -u <url> --port 8080` |
| Dark-Phish | https://github.com | `bash darkphish.sh` |
| Zphisher | https://github.com | `bash zphisher.sh` |
| LUCY Security | https://lucysecurity.com | Commercial — deploy via vendor VM/appliance |

## AI Deepfake Video Tools

| Tool | Source |
|---|---|
| DeepFaceLab | https://www.deepfakevfx.com |
| Vidnoz | https://www.vidnoz.com |
| Deepfakesweb | https://deepfakesweb.com |
| Synthesia | https://www.synthesia.io |
| DeepBrain AI | https://www.deepbrain.io |
| Hoodem | https://hoodem.com |

## AI Voice Cloning Tools

| Tool | Source |
|---|---|
| VEED.IO | https://www.veed.io |
| Murf.AI | https://murf.ai |
| Resemble.AI | https://www.resemble.ai |
| ElevenLabs | https://elevenlabs.io |
| PlayHT | https://play.ht |
| voice.ai | https://voice.ai |

## QR Code Cloning Tools (QRLJacking)

| Tool | Source |
|---|---|
| QR TIGER | https://www.qrcode-tiger.com |
| QR Code Generator | https://support.qr-code-generator.com |
| Soti MobiControl | https://www.soti.net |
| QR Code KIT | https://qrcodekit.com |

## Anti-Phishing / Detection & Defense Tools

| Tool | Source |
|---|---|
| Netcraft | https://www.netcraft.com |
| PhishTank | https://phishtank.com |
| Scanurl | https://scanurl.net |
| Isitphishing | https://isitphishing.org |
| Threatcop | https://threatcop.ai |
| e.Veritas | https://www.emailveritas.com |
| VirusTotal | https://www.virustotal.com |

## OSINT / Reconnaissance Tools (for authorized SE pentest recon — see `08`)

| Tool | Purpose | Core Command |
|---|---|---|
| theHarvester | Email/subdomain/employee enumeration | `theHarvester -d target.com -b all -l 500` |
| Sherlock | Username enumeration across platforms | `sherlock "username"` |
| Sublist3r | Subdomain enumeration | `sublist3r -d target.com` |
| recon-ng | Modular OSINT framework | `recon-ng` → `marketplace install all` |
| Maltego | Graph-based OSINT/link analysis | GUI tool — https://www.maltego.com |
| whois | Domain registration lookup | `whois target.com` |
| dig | DNS record inspection | `dig target.com MX` / `dig target.com TXT` |

---

## Command Reference — Defensive Controls (from `07`)

### Password Policy
```bash
# Windows local policy
net accounts /minpwlen:12 /maxpwage:90 /lockoutthreshold:5 /lockoutduration:30

# Windows AD domain policy (PowerShell, run on a DC)
Set-ADDefaultDomainPasswordPolicy -Identity "example.com" -ComplexityEnabled $true `
    -MinPasswordLength 12 -MaxPasswordAge 90.00:00:00 -LockoutThreshold 5

# Linux password aging
sudo chage -M 90 -m 1 -W 7 <username>
```

### Account Lockout (Linux PAM)
```
# /etc/pam.d/common-auth
auth required pam_faillock.so preauth silent deny=5 unlock_time=1800
auth [default=die] pam_faillock.so authfail deny=5 unlock_time=1800
```

### DNS Cache / Hosts File Checks (Pharming Defense)
```bash
cat /etc/hosts                                  # Linux/macOS — check for tampered entries
Get-Content C:\Windows\System32\drivers\etc\hosts   # Windows equivalent

ipconfig /flushdns                              # Windows — flush poisoned DNS cache
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder   # macOS
sudo systemd-resolve --flush-caches             # Linux (systemd-resolved)
```

### Two-Factor Authentication
```bash
# SSH TOTP via Google Authenticator PAM module
sudo apt install libpam-google-authenticator
google-authenticator
# then add `auth required pam_google_authenticator.so` to /etc/pam.d/sshd
```

### USB / Removable Media Restriction
```bash
# Linux — block usb-storage kernel module
echo "blacklist usb-storage" | sudo tee /etc/modprobe.d/block-usb-storage.conf
sudo update-initramfs -u
```
```powershell
# Windows — deny all removable storage via policy
New-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\RemovableStorageDevices" `
    -Name "Deny_All" -PropertyType DWord -Value 1 -Force
```

### Secure Disk Wipe (Before Disposal)
```bash
sudo shred -n 3 -z -v /dev/sdX          # HDD/SSD (SATA) — verify device path first!
sudo nvme format /dev/nvme0n1 --ses=1   # NVMe secure erase
```

### VirusTotal API — URL Scan
```bash
curl --request POST --url https://www.virustotal.com/api/v3/urls \
  --header 'x-apikey: <YOUR_API_KEY>' --data "url=https://suspicious-site.example.com"

curl --request GET --url https://www.virustotal.com/api/v3/analyses/<ANALYSIS_ID> \
  --header 'x-apikey: <YOUR_API_KEY>'
```

---

*All tool links point to official project sources at time of writing. Always verify you're on
the genuine project domain before downloading — attackers have been known to publish trojanized
clones of well-known security tools.*