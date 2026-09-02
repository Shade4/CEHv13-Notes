# 09 — SQL Injection Detection Tools

Detection tools help identify SQLi attacks by monitoring HTTP traffic and known attack vectors, and by determining
whether a web application or database code suffers from SQLi vulnerabilities in the first place.

## Detecting SQL Injection Attacks via Regular Expressions

Security professionals develop and deploy IDS rules using regex to detect SQL meta-characters — the single-quote
(`'`) and double-dash (`--`) being the two most fundamental — along with their URL-encoded hex equivalents.

### Table 15.5 — Character / Hex Reference

| Characters | Explanation |
|---|---|
| `'` | Single-quote character |
| `\|` | Or |
| `%27` | Hex equivalent of single-quote character |
| `--` | Double-dash |
| `%2D` | Hex equivalent of double-dash |
| `#` | Hash or pound character |
| `%23` | Hex equivalent of hash character |
| `i` | Case-insensitive (regex flag) |
| `x` | Ignore white spaces in pattern (regex flag) |
| `%3D` | Hex equivalent of `=` (equal) character |
| `%3B` | Hex equivalent of `;` (semi-colon) character |
| `%6F` | Hex equivalent of `o` character |
| `%4F` | Hex equivalent of `O` character |
| `%72` | Hex equivalent of `r` character |
| `%52` | Hex equivalent of `R` character |
| `%3C` | Hex equivalent of `<` (opening angle bracket) |
| `%3E` | Hex equivalent of `>` (closing angle bracket) |
| `%2F` | Hex equivalent of `/` (forward slash, closing tag) |
| `\s` | Whitespace equivalent |
| `^\n` | Hex equivalent of a non-newline character |

### The Regular Expressions

**1. Detect SQL meta-characters:**

```regex
/(\')|(\%27)|(\-\-)|(#)|(\%23)/ix
```

Checks for the single-quote character (or its hex value), the double-dash (not an HTML character, so it's never
encoded by the browser), and the hash character (or its hex value) — with case-insensitive (`i`) and
whitespace-ignoring (`x`) flags.

**2. Modified regex for detecting SQL meta-characters:**

```regex
/((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))/ix
```

Checks for the `=` sign (or its hex `%3D`) in the request; `[^\n]*` allows any non-newline characters in between;
then checks for single-quote, double-dash, and semi-colon (or their hex forms).

**3. Regex for a typical SQL injection attack:**

```regex
/\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))/ix
```

Detects zero-or-more alphanumeric/underscore characters, then a single-quote (or hex), then the word **"or"** in any
case combination (`or`, `Or`, `oR`, `OR`) via hex-or-literal alternation for each letter.

**4. Regex for detecting SQL injection with the `UNION` keyword:**

```regex
/((\%27)|(\'))union/ix
```

Checks for a single-quote (or hex) followed by the `union` keyword. Build similar expressions for `insert`,
`update`, `select`, `delete`, and `drop` to cover the other dangerous keywords.

**5. Regex for detecting SQL injection attacks on a Microsoft SQL Server:**

```regex
/exec(\s|\+)+(s|x)p\w+/ix
```

Detects an attacker abusing extended/stored procedures (`xp_cmdshell`, `xp_regread`, `xp_regwrite`, etc.) to run
shell commands or alter the registry — checks the `exec` keyword, whitespace (or its hex/`+` equivalent), the `sp`/
`xp` prefix, then an alphanumeric/underscore character.

## Real-World Example — Snort IDS Rule

```
alert tcp $EXTERNAL_NET any -> $HTTP_SERVERS $HTTP_PORTS (
    msg: "SQL Injection - Paranoid";
    flow:to_server, established;
    uricontent:".pl";
    pcre:"/(\')|(\%27)|(\-\-)|(#)|(\%23)/ix";
    classtype:Web-application-attack;
    sid:9099; rev:5;
)
```

**Field-by-field:**

| Field | Meaning |
|---|---|
| `alert` | Log entry generated when the IDS detects the attack signature in an HTTP request |
| `tcp` | Protocol used |
| `$EXTERNAL_NET any` | External network's IP address; `any` = any source port |
| `->` | Operator separating destination from source |
| `$HTTP_SERVERS` | Variable representing the organization's web server(s) |
| `$HTTP_PORTS` | Common HTTP ports (e.g. 80, 8080) |
| `msg:` | The alert message text |
| `flow:to_server` | Direction of traffic |
| `established` | Alert raised only on established TCP connections |
| `uricontent:".pl"` | Alert scoped to Perl-script-based URI content |
| `pcre:` | The actual Perl-compatible regex being matched |
| `classtype` / `sid` / `rev` | Rule classification, signature ID, revision number |

### Reading a Raw Access Log for SQL Injection Attempts

Real SQLi attempts are directly visible in raw web-server logs (URL-encoded). Example progression against
`/sqli/example1.php?name=` from a single attacking IP:

```
name=root%27%20or%20%271%27=%271%27%20--%20                       # ' or '1'='1' --
name=root%27%20%20UnION%20SeLeCT%201,2,3,4,5%20%20--%20           # column-count probing UNION (mixed case)
name=root%27%20%20UnION%20SeLeCT%201,database(),3,4,5%20--%20     # extracting current DB name
name=root%27%20%20UnION%20SeLeCT%201,table_name,3,4,5%20From%20Information_schema.tables%20where%20Table_Schema=DatabasE()%20limit%201,2--%20
                                                                    # enumerating table names via information_schema
```

This is the full recon → exploit progression, visible directly in the logs — exactly what a log-based detection rule
needs to catch.

## OWASP ZAP

**Source:** `https://www.zaproxy.org`

OWASP **Zed Attack Proxy (ZAP)** is an integrated penetration testing tool for finding vulnerabilities in web
applications. It offers automated scanners as well as a set of manual security-testing tools, and is designed to be
usable across a wide skill range — including developers and functional testers new to penetration testing.

Security professionals use ZAP to identify and fix vulnerabilities, maximize remediation efforts, and reduce the
likelihood of a successful attack.

**Example finding (against `moviescope.com`):**

```
SQL Injection
URL: http://www.moviescope.com/
Risk: High
Confidence: Medium
Parameter: txtpwd
Attack: ZAP OR '1'='1' --
CWE ID: 89
WASC ID: 19
Source: Active (40018 - SQL Injection)
Input Vector: Form Query
Description: SQL injection may be possible.
```

## Damn Small SQLi Scanner (DSSS)

**Source:** `https://github.com`

A fully functional SQLi vulnerability scanner (< 100 lines of code!) supporting GET and POST parameters. Scans a
target web application for various SQLi vulnerabilities.

```bash
python3 dsss.py -u "http://www.moviescope.com/viewprofile.aspx?id=1" \
  --cookie="mscope=1jWydNf8wro=; ui-tabs-1=0"
```

**Options:**

```
Usage: dsss.py [options]

Options:
  --version        show program's version number and exit
  -h, --help        show this help message and exit
  -u URL, --url=URL  Target URL (e.g. "http://www.target.com/page.php?id=1")
  --data=DATA        POST data (e.g. "query=test")
  --cookie=COOKIE    HTTP Cookie header value
  --user-agent=UA    HTTP User-Agent header value
  --referer=REFERER  HTTP Referer header value
  --proxy=PROXY      HTTP proxy address (e.g. "http://127.0.0.1:8080")
```

**Example finding:**

```
* scanning GET parameter 'id'
(i) GET parameter 'id' appears to be blind SQLi vulnerable
    (e.g.: 'http://www.moviescope.com/viewprofile.aspx?id=1%20OR%20NOT%20%28133%3E133%29')

scan results: possible vulnerabilities found
```

## Snort

**Source:** `https://www.snort.org`

Common attacks use a specific type of code sequence/command that lets an attacker gain unauthorized access to a
target's system and data. These sequences let a user write Snort rules aimed specifically at detecting SQLi.

**Expressions Snort can be configured to block:**

```regex
/User-Agent\x3A\x20[^\r\n]*sleep\x28/i

/[?&]selInfoKey1=[^&]*?([\x27\x22\x3b\x23]|\x2f\x2a|\x2d\x2d)/i

/(^|&)selInfoKey1=[^&]*?([\x27\x22\x3b\x23]|\x2f\x2a|\x2d\x2d|%27|%22|%3b|%23|%2f%2a|%2d%2d)/im

/^\s*?MAIL\s+?FROM\x3a[^\r\n]*?\x28\x29\s\x7b/i
```

**Full rule** detecting the "`sleep(`-hidden-in-`User-Agent`-header" time-based blind technique:

```
alert tcp any any -> any $HTTP_PORTS (
    msg:"SQL use of sleep function in HTTP header - likely SQL injection attempt";
    flow:to_server,established;
    http_header;
    content:"User-Agent|3A| ";
    content:"sleep(",fast_pattern,nocase;
    pcre:"/User-Agent\x3A\x20[^\r\n]*sleep\x28/i";
    metadata:policy balanced-ips drop,policy max-detect-ips drop,policy security-ips drop,ruleset community;
    service:http;
    reference:url,blog.cloudflare.com/the-sleepy-user-agent/;
    classtype:web-application-attack;
    sid:38993; rev:9;
)
```

## Additional SQL Injection Detection / Testing Tools

| Tool | Source |
|---|---|
| Ghauri | `https://github.com` |
| Burp Suite | `https://www.portswigger.net` |
| HCL AppScan | `https://www.hcl-software.com` |
| Invicti | `https://www.invicti.com` |
| SQL Invader | `https://www.rapid7.com` |
| Arachni | `https://ecsypno.com` |
| Qualys WAS | `https://www.qualys.com` |
| Fortify WebInspect | `https://www.microfocus.com` |
| BeSECURE | `https://beyondsecurity.com` |
| SolarWinds® Security Event Manager | `https://www.solarwinds.com` |
| sqlifinder | `https://github.com` |
| dotDefender | `http://www.applicure.com` |
| Wapiti | `https://wapiti-scanner.github.io` |
| InsightAppSec | `https://www.rapid7.com` |
| Acunetix Web Vulnerability Scanner | `https://www.acunetix.com` |
| Detectify | `https://detectify.com` |

---

## Module Summary

This module covered:

- Basic SQL injection concepts, and the different types of SQL injection
- The full SQL injection methodology — information gathering & vulnerability detection, launching attacks, and
  advanced SQL injection (network/OS compromise)
- The major SQL injection tools, including AI-assisted exploitation workflows
- SQL injection evasion techniques used to bypass IDS/WAF signatures
- Countermeasures to prevent SQL injection attempts by threat actors
- SQL injection detection tools

**Next module in the CEH v13 curriculum:** Module 16 — how attackers, ethical hackers, and pen-testers compromise
wireless (Wi-Fi) networks to gain unauthorized access to network resources.

---

**Previous:** [08 — SQL Injection Countermeasures](08-sql-injection-countermeasures.md) · **Back to:** [README](README.md)
