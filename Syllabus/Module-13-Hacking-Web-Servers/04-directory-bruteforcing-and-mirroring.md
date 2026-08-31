# 04 — Directory Brute-Forcing & Website Mirroring

> Objective covered: **Explain Web Server Attack Methodology** (Phase 3: Website Mirroring / Directory Discovery)

## 1. Directory Listings

When directory browsing is left enabled and no default index file (`index.html`) exists, the server returns a full file/folder listing to any visitor:

```
Index of /share
Name                        Last modified      Size  Description
📁 Camp Director/           2024-05-05 04:20   -
📄 flashka.swf              2024-05-05 04:12    -
📄 LEADER.html              2024-08-06 11:12 PM  -
📄 Tools/                   2024-05-05 04:12    -
📄 Blackbeard.exe           2024-05-05 08:09    -
📄 backups/
📄 config.php
📄 test/
```

Though directory listings do not have significant relevance from a security perspective on their own, they occasionally expose vulnerabilities that allow attackers to compromise web applications, such as:

- **Improper access controls**
- **Unintentional access to the web root of servers**

In general, after discovering a directory on a web server, an attacker makes a request for that directory and attempts to access the directory listing. Attackers also attempt to exploit vulnerable web server software that grants access to directory listings.

Attackers use tools such as **Dirhunt** and **Sitechecker Website Directory Scanner** to find directory listings of the target web server.

### Dirhunt

- **Source:** https://github.com
- A web crawler optimized for searching and analyzing directories. This tool can find interesting results if the server has the "index of" mode enabled. Dirhunt is also useful for searching and analyzing directories even if the directory listing is not enabled — it detects directories with false 404 errors, directories where an empty index file has been created to hide things, and so on.

```bash
dirhunt http://www.moviescope.com
```

**Real captured output fragment:**
```
[200] http://www.moviescope.com/ (Not Found)
[200] http://www.moviescope.com/js/ (Not Found)
[200] http://www.moviescope.com/pages/product/ (Not Found)
[200] http://www.moviescope.com/counter/ (Not Found)
[200] http://www.moviescope.com/js/tv/ (Not Found)
[200] http://www.moviescope.com/well-known/ (Not Found)
[200] http://www.moviescope.com/blackbeard.exe (Not Found)
[200] http://www.moviescope.com/api/nodejs/ (Not Found)
```

### Directory Brute Forcing with AI

**Prompt:** *"Perform a directory traversal on target url https://certifiedhacker.com"*

**Resulting command:**
```bash
gobuster dir -u https://certifiedhacker.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

| Flag | Meaning |
|---|---|
| `gobuster dir` | Invokes the `gobuster` tool in directory/file brute-force mode |
| `-u https://certifiedhacker.com` | Target URL |
| `-w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt` | Wordlist used for directory/file brute-forcing |

**Real captured output:**
```
/docs                (Status: 301) [Size: 241] [--> https://certifiedhacker.com/docs/]
/xml                 (Status: 301) [Size: 240] [--> https://certifiedhacker.com/xml/]
/mailman             (Status: 301) [Size: 244] [--> https://certifiedhacker.com/mailman/]
/css                 (Status: 301) [Size: 240] [--> https://certifiedhacker.com/css/]
/pipermail           (Status: 301) [Size: 246] [--> https://certifiedhacker.com/pipermail/]
/js                  (Status: 301) [Size: 239] [--> https://certifiedhacker.com/js/]
/webmail             (Status: 200) [Size: 33950]
/soc                 (Status: 301) [Size: 240] [--> https://certifiedhacker.com/soc/]
/cgi-sys             (Status: 301) [Size: 244] [--> https://certifiedhacker.com/cgi-sys/]
/controlpanel        (Status: 200) [Size: 33945]
/cpanel              (Status: 200) [Size: 33945]
/notifications       (Status: 301) [Size: 250] [--> https://certifiedhacker.com/notifications/]
/iam                 (Status: 301) [Size: 240] [--> https://certifiedhacker.com/iam/]
/*                   (Status: 204) [Size: 0]
/Recipes             (Status: 301) [Size: 244] [--> https://certifiedhacker.com/Recipes/]
/fleet               (Status: 301) [Size: 242] [--> https://certifiedhacker.com/fleet/]
/sftp                (Status: 301) [Size: 241] [--> https://certifiedhacker.com/sftp/]
/itf                 (Status: 301) [Size: 240] [--> https://certifiedhacker.com/itf/]
/FTP%20Now%20scr     (Status: 406) [Size: 226]
/%7Echeckout%7E      (Status: 406) [Size: 226]
/whm                 (Status: 200) [Size: 33930]
Progress: 220560 / 220561 (100.00%)
Finished
```

This command systematically tests different directories and files on the target website using the wordlist provided, in an attempt to find any that might be accessible.

> 📝 **Note (added):** other common `gobuster` modes worth knowing beyond `dir`: `gobuster dns` (subdomain brute-force), `gobuster vhost` (virtual host brute-force), and `gobuster fuzz` (generic FUZZ-keyword brute-force). Add `-x php,asp,aspx,txt,bak` to also brute-force common file extensions, and `-t 50` to raise thread count for faster scans against a lab target.

---

## 2. Website Mirroring (Bonus / Extra Coverage)

> 📝 **Note (added):** the courseware's methodology diagram explicitly lists **"Website Mirroring"** as step 3 of the attack methodology, but the deck itself does not walk through dedicated mirroring tools — it moves straight into directory brute-forcing. The two techniques are closely related (both map out a site's structure), so this section adds the standard mirroring toolkit for completeness, since a real engagement (and the CEH exam) expects you to know these.

**Concept:** Website mirroring is a method of copying a website and all its content onto another server for **offline browsing**. With a mirrored website, an attacker can view the detailed structure of the website — every file, directory, script, and comment — without repeatedly hitting the live server (which is also stealthier, since it generates far fewer live requests against the target).

### HTTrack

- **Source:** https://www.httrack.com
- A free, offline-browser utility that downloads an entire website — HTML, images, and other files — from the server to a local directory, recreating the original site's directory structure.

```bash
# Mirror an entire site to ./mirror, staying within the target domain
httrack "http://www.certifiedhacker.com" -O "./mirror" "+*.certifiedhacker.com/*" -v

# Common useful flags:
#   -%e0   don't follow external links
#   -r6    limit mirror recursion depth to 6
#   -s0    don't obey robots.txt (use only against systems you're authorized to test)
```

### Wget (mirror mode)

```bash
wget --mirror \
     --convert-links \
     --adjust-extension \
     --page-requisites \
     --no-parent \
     https://target.com
```

| Flag | Meaning |
|---|---|
| `--mirror` | Shorthand for recursive, infinite-depth mirroring with timestamping |
| `--convert-links` | Rewrites links in downloaded pages to point to local copies |
| `--adjust-extension` | Adds appropriate extensions (`.html`, `.css`) to saved files |
| `--page-requisites` | Downloads all resources needed to display pages correctly (images, CSS, JS) |
| `--no-parent` | Never ascends to the parent directory during recursion |

### Other Common Mirroring Tools

| Tool | Notes |
|---|---|
| **BlackWidow** | Windows website scanner/mirror + site-mapper with a built-in scheduler |
| **Web Ripper** | Automated website downloader/copier for offline analysis |
| **WebCopier Pro** | Commercial site-copying tool with proxy and login-form support |
| **cURL (scripted)** | `curl -s <url> \| grep -oE 'href="[^"]+"'` — a lightweight, scriptable way to enumerate links one page at a time when a full mirror isn't needed |

### Why Attackers Mirror a Site

- Analyze site structure, comments in HTML/JS source, and hidden form fields offline, without generating suspicious request volume against the live target.
- Discover backup files, old versions of scripts, or forgotten admin panels sometimes left inside the directory tree.
- Build a target map for subsequent **directory brute-forcing** (above) and **vulnerability scanning** ([05](05-vulnerability-scanning-and-exploitation.md)).

---

**Previous:** [← 03 — Attack Methodology: Recon & Footprinting](03-attack-methodology-recon-and-footprinting.md) · **Next:** [05 — Vulnerability Scanning & Exploitation →](05-vulnerability-scanning-and-exploitation.md)
