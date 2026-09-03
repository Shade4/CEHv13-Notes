# 🧰 Tools Index — CEH Module 17: Hacking Mobile Platforms

Every tool named in the module (150+), grouped by category, with source and a one‑line purpose. Cross‑referenced to the file where it's discussed in depth.

---

## Attack Frameworks & Exploitation Suites
| Tool | Source | Purpose | Details |
|---|---|---|---|
| drozer | github.com | Android attack‑surface enumeration & exploitation console | `03 §3.1` |
| Metasploit Framework / msfvenom | metasploit.com | Payload generation + exploitation + post‑exploitation (`meterpreter`) | `03 §3.9` |
| Ghost Framework | github.com | ADB‑based Android post‑exploitation (remote shell, file pull, screenshot) | `04 §4.2` |
| AndroRAT | github.com | Java/Python client‑server Android RAT, persistent backdoor | `04 §4.2` |
| zANTI | Zimperium | Mobile network pentest suite (MITM, DoS, session hijack) | `03 §3.3` |
| Kali NetHunter | kali.org | Mobile Kali platform: HID/BadUSB attacks, Mana evil‑AP, MSF payload generator | `03 §3.3` |
| PhoneSploit Pro | github.com | Menu‑driven ADB exploitation toolkit | `03 §3.6` |
| LOIC (Android) | — | Mobile UDP/HTTP/TCP flooder | `03 §3.4` |
| Orbot | orbot.app | Tor proxy client for Android | `03 §3.5` |
| SeaShell Framework | github.com (EntySec) | iOS post‑exploitation via CoreTrust/TrollStore | `07 §7.3` |
| Cycript | cycript.org | Objective‑C/JS runtime manipulation console | `07 §7.4` |
| objection | github.com (sensepost) | Frida‑powered runtime mobile app instrumentation | `07 §7.6` |
| Frida | frida.re | Cross‑platform dynamic instrumentation toolkit | `03 §3.11`, `07 §7.6` |
| Keychain Dumper | github.com | Dumps iOS Keychain secrets | `07 §7.5` |
| r2frida | github.com | radare2 + Frida process exploration | `07 §7.7` |
| StormBreaker | github.com | Social‑engineering camera/mic/location capture toolkit | `01 §1.15` |
| AdvPhishing | github.com | Social‑media phishing + OTP/2FA bypass | `01 §1.14` |
| mrphish | github.com | Bash phishing script with OTP‑bypass control | `01 §1.14` |

## Android Rooting Tools
| Tool | Source | Details |
|---|---|---|
| KingoRoot (PC & no‑PC) | kingoapp.com | `02 §2.4` |
| OneClickRoot | oneclickroot.com | `02 §2.4` |
| TunesGo | tunesgo.wondershare.com | `02 §2.4` |
| RootMaster | root-master.com | `02 §2.4` |
| Magisk Manager | magiskmanager.com | `02 §2.4` |
| KingRoot | kingrootapp.net | `02 §2.4` |
| iRoot | iroot-download.com | `02 §2.4` |

## FRP Bypass Tools
| Tool | Source | Details |
|---|---|---|
| 4uKey (Tenorshare) | tenorshare.com | `03 §3.2` |
| Octoplus FRP | octoplusbox.com | `03 §3.2` |

## Android Malware Families (reference only — not tools)
| Name | Category | Details |
|---|---|---|
| Mamont | Banking Trojan | `04 §4.1` |
| SecuriDropper | Dropper‑as‑a‑service | `04 §4.1` |
| Dwphon | Firmware‑level malware | `04 §4.1` |
| DogeRAT | Open‑source RAT | `04 §4.1` |
| Tambir | Banking Trojan | `04 §4.1` |
| SoumniBot | Manifest‑obfuscating malware | `04 §4.1` |

## Android‑Based Sniffers
| Tool | Source | Details |
|---|---|---|
| PCAPdroid | play.google.com | `04 §4.3` |
| NetCapture | play.google.com | `04 §4.3` |
| Intercepter‑NG | sniff.su | `04 §4.3` |
| Packet Capture | play.google.com | `04 §4.3` |
| Sniffer Wicap 2 Demo | 9apps.com | `04 §4.3` |
| Reqable API Testing & Capture | play.google.com | `04 §4.3` |

## Other Android Hacking Tools
| Tool | Source | Details |
|---|---|---|
| hxp_photo_eye | github.com | `04 §4.2` |
| Gallery Eye | github.com | `04 §4.2` |
| mSpy | mspy.com | `04 §4.2`, `08 §8.3` |
| Hackingtoolkit | github.com | `04 §4.2` |
| Social‑Engineer Toolkit (SET) | github.com | `04 §4.2` |

## Android Security / Antivirus Tools
| Tool | Source | Details |
|---|---|---|
| Kaspersky Antivirus/VPN for Android | kaspersky.com | `05 §5.2` |
| Avira Security Antivirus & VPN | play.google.com | `05 §5.2` |
| Avast Antivirus & Security | play.google.com | `05 §5.2`, `10 §10.11` |
| McAfee Security: Antivirus VPN | play.google.com | `05 §5.2` |
| Lookout Mobile Security and Antivirus | play.google.com | `05 §5.2` |
| Sophos Intercept X for Mobile | play.google.com | `05 §5.2` |

## Android Device‑Tracking Tools
| Tool | Source | Details |
|---|---|---|
| Google Find My Device | google.com | `05 §5.3` |
| Find My Phone | play.google.com | `05 §5.3` |
| Where's My Droid | wheresmydroid.com | `05 §5.3` |
| Prey: Find My Phone & Security | play.google.com | `05 §5.3` |
| Phone Tracker and GPS Location | play.google.com | `05 §5.3` |
| Mobile Tracker for Android | play.google.com | `05 §5.3` |
| Lost Phone Tracker | play.google.com | `05 §5.3` |
| Phone Tracker By Number | play.google.com | `05 §5.3` |

## Android Vulnerability Scanners
| Tool | Source | Details |
|---|---|---|
| Quixxi App Shield | quixxi.com | `05 §5.4` |
| Android Exploits | play.google.com | `05 §5.4` |
| ImmuniWeb® MobileSuite | immuniweb.com | `05 §5.4`, `10 §10.12` |
| Yaazhini | vegabird.com | `05 §5.4` |
| Vulners Scanner | play.google.com | `05 §5.4` |

## Static / Online APK Analyzers
| Tool | Source | Details |
|---|---|---|
| MobSF | github.com | `05 §5.5` |
| Sixo Online APK Analyzer | sisik.eu | `05 §5.5` |
| ShenmeApp | shenmeapp.com | `05 §5.5` |
| KOODOUS | koodous.com | `05 §5.5` |
| Android APK Decompiler | javadecompilers.com | `05 §5.5` |
| Hybrid Analysis | hybrid-analysis.com | `05 §5.5` |
| DeGuard | apk-deguard.com | `05 §5.5` |

## iOS Jailbreaking Tools
| Tool | Source | Details |
|---|---|---|
| Hexxa Plus | hexxaplus.com | `06 §6.5` |
| Redensa | pangu8.com | `06 §6.6` |
| checkrain | checkra.in | `06 §6.6` |
| palerain | palera.in | `06 §6.6` |
| Zeon | zeon-app.com | `06 §6.6` |
| Sileo | en.sileem.com | `06 §6.6` |
| Cydia | cydiafree.com | `06 §6.6` |

## iOS Spyware / Commercial Hacking Tools
| Tool | Source | Details |
|---|---|---|
| Spyzie | spyzie.io | `07 §7.1` |
| Elcomsoft Phone Breaker | elcomsoft.com | `07 §7.9` |
| Enzyme | github.com | `07 §7.9` |
| Network Analyzer: net tools | apps.apple.com | `07 §7.9` |
| iOS Binary Security Analyzer | github.com | `07 §7.9` |
| iWepPRO | apps.apple.com | `07 §7.9` |

## iOS Malware / Spyware Families (reference only)
| Name | Details |
|---|---|
| GoldPickaxe.iOS | `07 §7.8` |
| SpectralBlur | `07 §7.8` |
| Mercenary Spyware | `07 §7.8` |
| LightSpy | `07 §7.8` |
| KingsPawn | `07 §7.8` |
| Pegasus | `07 §7.8` |

## iOS Security Tools
| Tool | Source | Details |
|---|---|---|
| Malwarebytes Mobile Security | malwarebytes.com | `08 §8.2` |
| Norton Mobile Security for iOS | us.norton.com | `08 §8.2` |
| McAfee Mobile Security | mcafee.com | `08 §8.2` |
| Trend Micro™ Mobile Security for iOS | trendmicro.com | `08 §8.2` |
| AVG Mobile Security | avg.com | `08 §8.2`, `10 §10.11` |
| Kaspersky Standard | kaspersky.com | `08 §8.2` |

## iOS Device‑Tracking Tools
| Tool | Source | Details |
|---|---|---|
| Find My | support.apple.com | `08 §8.3` |
| Glympse En Route | corp.glympse.com | `08 §8.3` |
| Prey Find My Phone & Security | apps.apple.com | `08 §8.3` |
| Mobile Phone Tracker Pro – SIM | apps.apple.com | `08 §8.3` |
| FollowMee GPS Location Tracker | apps.apple.com | `08 §8.3` |
| Phone Tracker: GPS Location | apps.apple.com | `08 §8.3` |

## Call Spoofing Tools
| Tool | Source | Details |
|---|---|---|
| SpoofCard | spoofcard.com | `01 §1.13` |
| SpoofTel | spooftel.com | `01 §1.13` |
| Fake Caller ID | fakecallerid.io | `01 §1.13` |
| Fake Call / Fake Call and SMS / Phone Id – Fake Caller Buster | play.google.com | `01 §1.13` |

## MDM Solutions
| Tool | Source | Details |
|---|---|---|
| Scalefusion MDM | scalefusion.com | `09 §9.2` |
| ManageEngine Mobile Device Manager Plus | manageengine.com | `09 §9.2` |
| Microsoft Intune | microsoft.com | `09 §9.2` |
| SOTI MobiControl | soti.net | `09 §9.2` |
| AppTec360 | apptec360.com | `09 §9.2` |
| Jamf Pro | jamf.com | `09 §9.2` |

## Source Code Analysis Tools
| Tool | Source | Details |
|---|---|---|
| Syhunt Mobile | syhunt.com | `10 §10.8` |
| Android lint | android.com | `10 §10.8` |
| Zimperium's z3A | zimperium.com | `10 §10.8` |
| Appium | appium.io | `10 §10.8` |
| Selendroid | selendroid.io | `10 §10.8` |
| Infer | fbinfer.com | `10 §10.8` |

## Reverse Engineering Tools
| Tool | Source | Details |
|---|---|---|
| Apktool | apktool.org | `10 §10.9` |
| Androguard | github.com | `10 §10.9` |
| JEB | pnfsoftware.com | `10 §10.9` |
| APK Editor Studio | github.com | `10 §10.9` |
| Bytecode Viewer | github.com | `10 §10.9` |

## App Repackaging Detectors
| Tool | Source | Details |
|---|---|---|
| Appdome | appdome.com | `10 §10.10` |
| freeRASP for Android/iOS | github.com | `10 §10.10` |
| wultra | wultra.com | `10 §10.10` |
| iXGuard | guardsquare.com | `10 §10.10` |
| AndroCompare | github.com | `10 §10.10` |
| FSquaDRA 2 | github.com | `10 §10.10` |

## Mobile Protection & Anti‑Spyware Tools
| Tool | Source | Details |
|---|---|---|
| Comodo Mobile Security | comodo.com | `10 §10.11` |
| TotalAV | totalav.com | `10 §10.11` |
| Norton Mobile Security for iOS | us.norton.com | `10 §10.11` |
| Mobile Security & Antivirus | play.google.com | `10 §10.11` |
| Bitdefender Mobile Security | play.google.com | `10 §10.11` |
| ESET Mobile Security Antivirus | play.google.com | `10 §10.11` |
| WISeID Personal Vault | play.google.com | `10 §10.11` |
| Certo: Anti Spyware & Security | play.google.com | `10 §10.11` |
| Anti Spy Detector – Spyware | play.google.com | `10 §10.11` |
| iAmNotified – Anti Spy System | iamnotified.com | `10 §10.11` |
| Anti Spy | protectstar.com | `10 §10.11` |
| Secury – Anti Spy Security | apps.apple.com | `10 §10.11` |

## Mobile Penetration‑Testing Toolkits
| Tool | Source | Details |
|---|---|---|
| ImmuniWeb® MobileSuite | immuniweb.com | `10 §10.12` |
| Codified Security | codifiedsecurity.com | `10 §10.12` |
| Astra Security | getastra.com | `10 §10.12` |
| Appknox | appknox.com | `10 §10.12` |
| Data Theorem's Mobile Secure | datatheorem.com | `10 §10.12` |
| MobSF | mobsf.live | `05 §5.5`, `10 §10.12` |

---

*Every URL above is the tool's own vendor/publisher domain as cited in the source courseware. Verify current legitimacy before installing anything — domains change hands, and abandoned tool names are a known typosquatting/malware‑distribution vector.*
