# 03 — SQL Injection Methodology: Information Gathering & Vulnerability Detection

Attackers follow a structured methodology to make SQLi attacks reliable. It has three phases:

1. **Information Gathering and SQL Injection Vulnerability Detection** ← *this file*
2. [Launching SQL Injection Attacks](04-methodology-launching-attacks.md)
3. [Advanced SQL Injection (compromising the entire target network)](05-methodology-advanced-sql-injection.md)

## Information Gathering

The attacker tries to learn the target database's name, version, users, output mechanism, DB type, user privilege
level, and OS interaction level. Understanding the underlying query lets the attacker craft correct injection strings;
error messages are the primary source of this information.

**General information-gathering steps:**

1. Check whether the web application connects to a database server to retrieve data
2. List all input fields, hidden fields, and POST request parameters that could shape a query
3. Attempt to inject code into input fields to trigger an error
4. Try inserting a string value where a number is expected
5. Use the `UNION` operator to combine result sets from two or more `SELECT` statements
6. Read detailed error messages closely to gather information for the actual injection

## Identifying Data Entry Paths

The attacker searches for every possible input gate — form fields, hidden fields, cookies — by analyzing the web
**GET** and **POST** requests sent to the application, typically using an intercepting proxy.

### Tools

**Tamper Dev** — `https://chromewebstore.google.com`
Browser extension that intercepts and edits HTTP/HTTPS requests and responses; can modify outgoing requests, modify
responses on interception, or trigger new requests.

**Burp Suite** — `https://www.portswigger.net`
Full web application security testing suite. Inspect and modify traffic between browser and target app; identify
SQLi, XSS, and other vulnerability classes via **Proxy → Intercept**.

## Extracting Information Through Error Messages

Error messages, when a developer hasn't disabled them, are gold for an attacker — they can reveal OS type, database
type, database version, privilege level, and interaction level.

### Parameter Tampering

Tamper GET/POST parameters (via Burp Suite or a browser extension) to generate errors:

```
http://certifiedhacker.com/download.php?id=car
http://certifiedhacker.com/download.php?id=horse
http://certifiedhacker.com/download.php?id=book
```

Example resulting error:

```
Error in query: Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)
```

### Determining Database Engine Type

Generate an **ODBC error** — the message often names the DB engine directly as part of the driver information. If no
ODBC error is available, guess based on the OS and web server in use.

### Determining a `SELECT` Query's Structure

Force application errors that reveal table names, column names, and data types by injecting *valid* SQL fragments
that don't themselves cause a syntax error — e.g. `' and '1'='1` (true) vs. `' and '1'='2` (false) — then use clauses
like:

```sql
' group by columnnames having 1=1 --
```

Most injection points land mid-`SELECT` statement, almost always inside the `WHERE` clause:

```sql
SELECT * FROM table WHERE x = 'normalinput' group by x having 1=1 -- GROUP BY x HAVING x = y ORDER BY x
```

### Grouping Error

`HAVING` further refines a query based on grouped fields — the resulting error names any column that wasn't grouped:

```sql
' group by columnnames having 1=1 --
```

```
SQLSTATE[44568]: Grouping error: 7 ERROR: column "columnnames" must appear in the GROUP BY clause or be used in an
aggregate function LINE 1: SELECT DISTINCT posts.id, posts.* FROM "posts" GROUP BY "pos..
```

### Type Mismatch

Insert a string where a number is expected — the error message reveals the value that couldn't be converted:

```sql
' union select 1,1,'text',1,1,1 --
' union select 1,1, bigint,1,1,1 --
```

```
Error #3132: Data type mismatch.', details:'could not convert text value to numeric value'.
```

or (SQL Server / ODBC):

```
Microsoft OLE DB Provider for ODBC Drivers error '80040e07' [Microsoft][ODBC SQL Server Driver]Syntax error
converting the varchar value 'test' to a column of data type int. /visa/credit.aspx, line 17
```

### Blind Injection (fallback)

If no useful error is returned at all (a generic `500 Server Error` or custom error page), fall back to time delays or
error-signature-based blind techniques:

```sql
'; if condition  waitfor delay '0:0:5' --
'; union select if( condition , benchmark (100000, sha1('test')), 'false' ),1,1,1,1;
```

## Testing for SQL Injection — Vulnerability Detection

After gathering information, the attacker (or, during a legitimate assessment, the pen tester) lists every input/hidden
field and POST request, then tries standard **testing strings** to see which ones trigger an error or unexpected
behavior. These strings are widely known as a SQL injection cheat sheet — see
[`cheatsheets/payloads-cheatsheet.md`](cheatsheets/payloads-cheatsheet.md) for the complete set (Table 15.2, "Standard
SQL Injection inputs").

### Additional Detection Methods

**Function Testing** — black-box technique requiring no knowledge of the code's internals; checks security, UI,
database, client/server behavior, navigation, and overall usability with escalating test inputs:

```
http://certifiedhacker.com/?parameter=123
http://certifiedhacker.com/?parameter=1'
http://certifiedhacker.com/?parameter=1'#
http://certifiedhacker.com/?parameter=1"
http://certifiedhacker.com/?parameter=1 AND 1=1--
http://certifiedhacker.com/?parameter=1'-
http://certifiedhacker.com/?parameter=1 AND 1=2--
http://certifiedhacker.com/?parameter=1'/*
http://certifiedhacker.com/?parameter=1' AND '1'='1
http://certifiedhacker.com/?parameter=1 order by 1000
```

**Fuzz Testing** — an adaptive technique that floods input fields with massive amounts of random data ("fuzz") and
observes changes in output to discover coding errors and security loopholes.

Fuzz Testing Tools:
- BeSTORM — `https://www.beyondsecurity.com`
- Burp Suite — `https://portswigger.net`
- AppScan Standard — `https://www.hcl-software.com`
- Defensics — `https://www.synopsys.com`
- SnapFuzz — `https://portswigger.net`

**Static Testing** — analysis of the web application's source code, without execution.

**Dynamic Testing** — analysis of the web application's runtime behavior.

## SQL Injection Black-Box Pen Testing

In black-box testing, the tester has no prior knowledge of the network/system and must find vulnerabilities purely
from an attacker's-eye view — using special characters, whitespace, SQL keywords, and oversized requests.

| Goal | Technique |
|---|---|
| **Detecting SQL Injection Issues** | Send single quotes as input to catch unsanitized user input; also send double quotes |
| **Detecting Input Sanitization** | Use a right square bracket (`]`) as input — catches cases where input is used as part of a SQL identifier without sanitization |
| **Detecting Truncation Issues** | Send long strings of junk data (like a buffer-overrun probe) — may trigger SQL errors on the page |
| **Detecting SQL Modification** | Send long strings of single-quote characters (or `]` or `"`) — these can max out the return values of `REPLACE`/`QUOTENAME` functions and truncate the command variable holding the SQL statement |

## Source Code Review to Detect SQL Injection Vulnerabilities

Source code review is a **white-box** testing method — a systematic examination of the source during the
implementation phase of the Security Development Lifecycle (SDL) — to find SQLi, format-string bugs, race conditions,
buffer overflows, and more. Can be manual or automated.

**Automated source-code review tools:**

| Tool | URL |
|---|---|
| Veracode | `https://www.veracode.com` |
| SonarQube | `https://sonarsource.com` |
| PVS-Studio | `https://pvs-studio.com` |
| Coverity Scan | `https://scan.coverity.com` |
| Parasoft Jtest | `https://www.parasoft.com` |
| CAST Application Intelligence Platform (AIP) | `https://www.castsoftware.com` |
| Klocwork | `https://www.perforce.com` |

**Two basic types of source code review:**

- **Static Code Analysis** — examines the code while it is *not* executing, via techniques like Taint Analysis, Lexical
  Analysis, and Data Flow Analysis. Many automated tools support this.
- **Dynamic Code Analysis** — examines the code *while it runs*: prepare input data → launch a test run → gather
  necessary parameters → analyze the output data. Effective at catching SQLi-related flaws caused by the interaction
  between code and SQL databases/web services.

## Testing for Blind SQL Injection Vulnerability (MySQL / MSSQL)

A simple two-step probe confirms blind SQLi on a URL parameter:

```
shop.com/items.php?id=101
-- SELECT * FROM ITEMS WHERE ID = 101

-- Inject a FALSE condition
shop.com/items.php?id=101 and 1=0
-- SELECT * FROM ITEMS WHERE ID = 101 AND 1 = 0     → always false, page returns nothing

-- Inject a TRUE condition
shop.com/items.php?id=101 and 1=1
-- SELECT * FROM ITEMS WHERE ID = 101 AND 1 = 1     → true, original items page returns
```

If the FALSE version hides the content and the TRUE version restores it, the URL is confirmed vulnerable to blind
SQL injection.

---

**Previous:** [02 — Types of SQL Injection](02-types-of-sql-injection.md) · **Next:** [04 — Methodology: Launching SQL Injection Attacks](04-methodology-launching-attacks.md)
