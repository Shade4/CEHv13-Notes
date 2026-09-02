# 08 — SQL Injection Countermeasures

Everything up to this point has been offensive technique. This file flips to the defensive side: how to actually stop
SQL injection from working against your own applications.

## Why Are Web Applications Vulnerable to SQL Injection?

Understanding *why* apps end up vulnerable makes the countermeasures make sense:

| Root cause | Why it matters |
|---|---|
| **The database server runs OS commands** | An attacker who compromises the DB via SQLi can use those same OS commands for unauthorized operations |
| **Using a privileged account to connect to the database** | A compromised high-privilege account lets the attacker act at the OS level, not just the DB level |
| **Error messages revealing important information** | Verbose DB errors on bad input leak schema/version info attackers use to build exploits |
| **No data validation at the server** | **The single most common cause of SQLi** — improper or absent input validation lets malicious code reach the query |
| **Complex software stacks** | Multi-layer architectures make consistent secure-practice implementation hard; inconsistencies between layers introduce new gaps |
| **Legacy code and backward compatibility** | Old codebases not designed with modern security practices in mind remain exploitable via their original input handling |
| **Reliance on concatenated queries** | Building SQL via string concatenation makes it trivially easy to alter the intended query structure |

## How to Defend Against SQL Injection Attacks — The Full 24-Point Checklist

1. Make no assumptions about the size, type, or content of the data that is received by your application
2. Test the size and data type of input and enforce appropriate limits to prevent buffer overruns
3. Test the content of string variables and accept only expected values
4. Reject entries that contain binary data, escape sequences, and comment characters
5. Never build Transact-SQL statements directly from user input — use stored procedures to validate user input
6. Implement multiple layers of validation and never concatenate user input that is not validated
7. Avoid constructing dynamic SQL with concatenated input values
8. Ensure that web config files for each application do not contain sensitive information
9. Use the most restrictive SQL account types for applications
10. Use network, host, and application intrusion detection systems to monitor injection attacks
11. Perform automated black-box injection testing, static source code analysis, and manual penetration testing to
    probe for vulnerabilities
12. Keep untrusted data separate from commands and queries
13. In the absence of a parameterized API, use a specific escape syntax for the interpreter to eliminate special
    characters
14. Use a secure hash algorithm such as SHA-256 to store user passwords rather than storing them in plaintext
15. Use a data access abstraction layer to enforce secure data access across an entire application
16. Ensure that code tracing and debug messages are removed prior to deploying an application
17. Design the code such that it appropriately traps and handles exceptions
18. Apply the least-privilege rule to run the applications that access the DBMS
19. Validate user-supplied data as well as data obtained from untrusted sources on the server side
20. Avoid quoted/delimited identifiers — they significantly complicate all whitelisting, blacklisting, and escaping
    efforts
21. Use a prepared statement to create a parameterized query to block execution manipulation
22. Ensure that all user inputs are sanitized before using them in dynamic SQL statements
23. Use regular expressions and stored procedures to detect potentially harmful code
24. Avoid the use of any web application that is not tested by the web server

### Additional Countermeasures (beyond the core 24)

- Isolate the web server by locking it in different domains
- Ensure all software patches are updated regularly
- Regularly monitor SQL statements from database-connected applications to identify malicious SQL statements
- Use views to protect data in the base tables by restricting access and performing transformations
- Disable shell access to the database
- Do not disclose database error information to end users
- Use a safe API that offers a parameterized interface, or that avoids using the interpreter completely
- Outsource the authentication workflow of applications (e.g. OAuth APIs) — lets users log in with existing accounts
  and keeps login details stored in one location
- Employ an object-relational mapping (ORM) framework to communicate with the database safely
- Use the latest programming languages that offer SQLi protection
- Perform user input validation based on **whitelists**, not blacklists
- Never use the same database account for multiple applications
- Disable unnecessary database functionalities
- Avoid using `xp_cmdshell` to control interaction between the SQL server and components of other servers
- Use a web application firewall (WAF) to eliminate malicious inputs
- Avoid extended/long URLs that might trigger a stack-based buffer overflow
- Convert user input (usernames, passwords, etc.) into strings before validation
- Remove default accounts from the SQL database
- Utilize a substantial buffer size for command variables, or execute dynamic Transact-SQL directly within an
  `EXECUTE` statement
- Employ frameworks such as **Hibernate** and **Spring Data JPA** for the application's data layer — these provide
  built-in mechanisms for safely constructing/executing SQL queries, automatically handling parameterization

## Use Type-Safe SQL Parameters

Enforce type and length checks using a parameter collection so input is treated as a **literal value**, never as
executable code.

```csharp
SqlDataAdapter myCommand = new SqlDataAdapter("AuthLogin", conn);
myCommand.SelectCommand.CommandType = CommandType.StoredProcedure;
SqlParameter parm = myCommand.SelectCommand.Parameters.Add("@aut_id", SqlDbType.VarChar, 11);
parm.Value = Login.Text;
```

The `@aut_id` parameter here is checked for both type and length, and is never concatenated into the SQL string.

**Vulnerable vs. Secure code, side by side:**

```csharp
// ❌ Vulnerable — string concatenation
SqlDataAdapter myCommand = new SqlDataAdapter("LoginStoredProcedure '" + Login.Text + "'", conn);

// ✅ Secure — parameterized query
SqlDataAdapter myCommand = new SqlDataAdapter(
    "SELECT aut_lname, aut_fname FROM Authors WHERE aut_id = @aut_id", conn);
SqlParameter parm = myCommand.SelectCommand.Parameters.Add("@aut_id", SqlDbType.VarChar, 11);
parm.Value = Login.Text;
```

## Defenses in the Application (5 Layers)

### 1. Input Validation

Two complementary approaches:

- **Whitelist Validation** (positive validation / inclusion) — only pre-approved entities (data type, range, size,
  value) are accepted; commonly implemented via regex. Characters used for whitelist validation:
  `^\ {} () @ ? $`
  Can get intricate when the valid input space is large or hard to enumerate.

- **Blacklist Validation** (negative validation / exclusion) — reject all disapproved/malicious inputs. Harder to
  get right, since every possible attack character/pattern must be anticipated in advance. Characters used for
  blacklist validation:
  `' | % -- ; / \* \\* |_ \ [ | @ | xp_`

  Blacklisting is rarely used in isolation — best practice combines it **with output encoding**, so input is both
  checked *and* encoded before it ever reaches the database.

### 2. Output Encoding

Applied **after** input validation, to ensure input is properly sanitized before being passed to the database. This
matters because whitelist validation alone can incorrectly reject perfectly valid input containing special
characters — e.g. the name `O'Henry` has an apostrophe that a naive whitelist would reject, yet the *dynamic* SQL
built from it is what's actually exploitable:

```java
// Vulnerable dynamic query
String myQuery = "INSERT INTO UserDetails VALUES ('" + first_name + "','" + last_name + "');"
```

An attacker injects into `first_name`:

```
','''); DROP TABLE UserDetails--
```

Resulting executed query:

```sql
INSERT INTO UserDetails VALUES ('','''); DROP TABLE UserDetails--','');
```

In MySQL, a single quote (`'`) ends a string — so encoding it is mandatory in dynamic SQL. Two valid approaches: use
two single quotes (`''`), or escape with a backslash (`\'`). Both treat the quote as a literal character instead of
a string terminator.

```java
// Java output-encoding example
myQuery = myQuery.replace("'", "\\'");
```

**Drawback:** input must be re-encoded *every time* before being supplied to the database query — miss one code path,
and the app remains vulnerable there.

### 3. Enforcing Least Privileges

Assign the **lowest** privilege level to every account that accesses the database. Never grant DBA-level or
administrator-level access rights to an application account. In genuinely critical situations where elevated access
is required, do the security groundwork first and identify the *exact* requirements — don't grant broad access "just
in case."

- If an application only needs to read data, grant **only** read access.
- Minimum privileges should also apply to the operating system the DBMS runs on.
- **The DBMS should never run as root.**

### 4. LIKE Clauses

Escape `LIKE`-clause wildcard characters (`_`, `%`, `[`) by wrapping them in square brackets via `Replace()`:

```csharp
s = s.Replace("[", "[[]");
s = s.Replace("%", "[%]");
s = s.Replace("_", "[_]");
```

### 5. Wrapping Parameters with `QUOTENAME()` and `REPLACE()`

Check that variables used in **dynamic Transact-SQL** are properly managed — data from stored-procedure parameters or
from existing tables should be wrapped using `QUOTENAME()` and `REPLACE()`.

- If the string has **≤ 128 characters**, use `QUOTENAME(@variable, '''')`.
- If the string has **> 128 characters**, use `REPLACE(@variable,'''','''''')`.

```sql
-- Before (vulnerable):
SET @temp = N'SELECT * FROM employees WHERE emp_lname =''' + @emp_lname + N'''';

-- After (secured):
SET @temp = N'SELECT * FROM employees WHERE emp_lname = ''' + REPLACE(@emp_lname,'''','''''') + N'''';
```

## Implementing Consistent Coding Standards

Database developers should plan for the security of the **whole information system infrastructure**, and adhere to
documented standards/policies when designing, developing, and implementing DB and web application solutions.

- Standardize data-access methods across all developers — ad hoc per-developer choices create a wide variety of
  security postures within the same codebase, hurting both maintainability and security.
- **Perform input validation at BOTH the client and the server level.** Never trust client-side-only validation —
  it minimizes round trips for performance, but a browser can always be bypassed. The server must independently
  filter all input regardless of what the client already checked.
- Use **custom error messages** that reveal little or no system detail, instead of default framework errors that
  leak internals.

## Firewalling the SQL Server

Firewall the database server so that only trusted clients can reach it. In most web environments, the only hosts
that legitimately need to talk to the SQL Server are the administrative network (if one exists) and the web
server(s) it services — typically it only needs to reach out to a backup server otherwise.

**SQL Server default listening ports:**
- Named pipes via Microsoft networking: TCP 139 and 445
- TCP port 1433
- UDP port 1434

A good server lockdown helps mitigate:
- Developers uploading unauthorized/insecure scripts and components to the web server
- Misapplied patches
- Administrative errors

## Minimizing Privileges — Do It From Day One

Developers often defer security concerns to the end of the development cycle. Instead, create a **low-privilege
account first**, and add permissions only as they're actually needed. Benefits:

- Developers address security concerns as features are added, so identification and fixing stay easy
- The team becomes familiar with the security framework throughout the project's lifetime (forced compliance,
  not an afterthought)
- The end product is more secure and avoids the last-minute "security scramble" that happens when a customer's
  security policy won't allow the app to run outside the system administrator's context

## Full Defense Architecture Example

A complete defense-in-depth flow, combining every layer above:

```
Attacker/Login Form
      │
      ▼
   Internet
      │
      ▼
Use WAF Firewall / IDS + Filter Packets
      │
      ▼
  Web Server  ───────────► Keep patches current
      │
      ▼
Sanitize and Filter User Input
      │
      ▼
Web Application ──► Analyze source code for SQLi; minimize use of 3rd-party apps
      │              also: use stored procedures & parameterized queries for SQL Query execution
      │              also: disable verbose error messages → use a Custom Error Page instead
      ▼
     DBMS ──► Connect using a non-privileged account
      │       Grant least privileges to DB, tables, and columns
      ▼
Operating System ──► Disable commands like xp_cmdshell
```

**Summary:** combine the full countermeasures checklist with type-safe SQL parameters; protect the web server with a
WAF/IDS and packet filtering, and keep it patched; sanitize/filter all input, review source code, and minimize
third-party app usage; use stored procedures and parameterized queries; replace verbose errors with custom error
pages; connect to the database with non-privileged, least-privilege accounts; and disable OS-impacting commands
like `xp_cmdshell` outright.

---

**Previous:** [07 — IDS / WAF Evasion Techniques](07-ids-waf-evasion-techniques.md) · **Next:** [09 — SQL Injection Detection Tools](09-sql-injection-detection-tools.md)
