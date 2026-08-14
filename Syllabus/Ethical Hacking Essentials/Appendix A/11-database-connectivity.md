# Appendix A: Ethical Hacking Essential Concepts – I
## Part 11 — Database Connectivity

[← Back to Part 10: Web Subcomponents](10-web-subcomponents.md) | [Back to README](README.md)

---

## Table of Contents

1. [Web Application Connection with SQL Server](#web-application-connection-with-sql-server)
2. [Web Application Connection with MS Access](#web-application-connection-with-ms-access)
3. [Web Application Connection with MySQL](#web-application-connection-with-mysql)
4. [Web Application Connection with Oracle](#web-application-connection-with-oracle)
5. [Quick-Reference Summary](#quick-reference-summary)
6. [Appendix A Complete](#appendix-a-complete)

---

## Web Application Connection with SQL Server

A web application uses one of three connection methods to reach an SQL Server database:

- Using a **connection string**
- Using an **OLE DB file** (`.UDL`)
- **ODBC Data Source Name (DSN)**

To connect to SQL Server databases, you need to know: the **server name**, **security information**, **database name**, which **data interface/API** to use, and the **connection procedure**.

### Authentication Modes

Web applications use two types of authentication modes when defining their SQL Server connection:

| Mode | Description |
|---|---|
| **Windows Authentication Mode** | The default security mode for SQL Server. Windows users and groups are trusted to log in. Uses a series of encrypted messages to authenticate users. Used when both the database and application sit on the same server |
| **Mixed Mode** | User credentials are maintained within the SQL Server itself. Used when users connect from different, non-trusted domains (internet applications) |

### Data Controls Used for SQL Server Connection

| Control Type | Details |
|---|---|
| **Data Controls** | Use DAO (Data Access Object); not natively possible; uses a JET database connection; the most efficient way |
| **ADO Data Controls** | Use ADO (ActiveX Data Object); set the connection string property; set the RecordSource property |
| **ADO Data Controls (DSN)** | Use ADO (ActiveX Data Object); set the connection string property; set the RecordSource property |
| **ADO Data Controls (UDL)** | Use ADO (ActiveX Data Object); set the connection string property; set the RecordSource property |
| **ADO Programmatically** | Declares an ADO connection object; sets the connection string; opens the connection; instantiates the recordset |
| **Others** | **RDO** — similar to ADO, uses DSN or DSN-less connection strings; **ODBCDirect** — uses RDO (Remote Data Object) for database connectivity; **ODBC** — an API to access databases |

---

## Web Application Connection with MS Access

Connecting a web application to an **MS Access** database requires:

- An **OLE DB connection manager**
- A **data provider**

**Steps to connect to MS Access from the application:**

1. Create an OLE DB connection manager
2. Select the corresponding data provider using:
   - The Connection Managers area in SSIS Designer
   - The SQL Server Import and Export Wizard

---

## Web Application Connection with MySQL

### MySQL Connectors

MySQL provides standards-based drivers — JDBC, ODBC, .NET, and native C — to build and connect a database from applications.

| Developed by MySQL | Developed by Community |
|---|---|
| ADO.NET Driver for MySQL (Connector API for MySQL (mysqlclient)dotNET) | ADO.NET Driver for MySQL (Connector API for MySQL (mysqlclient)dotNET) |
| ODBC Driver for MySQL (Connector/ODBC) | Perl Driver for MySQL (DBD::mysql) |
| JDBC Driver for MySQL (Connector/J) | Ruby Driver for MySQL (ruby-mysql) |
| C++ Driver for MySQL (Connector/C++) | C++ Wrapper for MySQL C API (MySQL++) |
| C Driver for MySQL (Connector/C) | |
| C API for MySQL (mysqlclient) | |

### Pluggable Authentication

MySQL supports **pluggable authentication**, which enables:

- **External authentication** — lets clients connect to MySQL using external authentication methods: PAM, Windows login IDs, LDAP, or Kerberos
- **Proxy users** — pluggable authentication lets an external user act as a proxy for a second user
- **External user** — a proxy user who can impersonate another user
- **Second user** — a proxied user whose identity and privileges are assumed by the proxy user

---

## Web Application Connection with Oracle

### Oracle Drivers to Connect to Web Applications

| Driver | Description |
|---|---|
| **Oracle ODBC Driver** | Enables ODBC applications on Microsoft Windows, Linux, Solaris, and IBM Advanced Interactive eXecutive (AIX) systems to connect to and access Oracle databases |
| **Oracle Data Provider for .NET (ODP.NET)** | Enables ADO.NET data access to the Oracle database. Two types of ODP.NET managed driver: **ODP.NET Managed Driver** and **Unmanaged Driver** |
| **Oracle JDBC Driver** | For Java |
| **Oracle OCI8** | An Oracle PHP extension for connecting to the Oracle database |

---

## Quick-Reference Summary

- **SQL Server**: 3 connection methods (connection string, OLE DB `.UDL`, ODBC DSN); 2 auth modes (Windows Authentication for same-server/trusted setups, Mixed Mode for cross-domain/internet apps); 6 data-control approaches (DAO, ADO×3 variants, ADO programmatic, RDO/ODBCDirect/ODBC)
- **MS Access**: needs an OLE DB connection manager + data provider, configured via SSIS Designer or the SQL Server Import/Export Wizard
- **MySQL**: standards-based connectors (JDBC/ODBC/.NET/native C) from both MySQL and the community, plus pluggable authentication supporting external auth (PAM/Windows/LDAP/Kerberos) and proxy-user impersonation
- **Oracle**: 4 driver families — ODBC (cross-platform), ODP.NET (managed/unmanaged), JDBC (Java), OCI8 (PHP)

---

## Appendix A Complete

That closes out **Appendix A: Ethical Hacking Essential Concepts – I** — the full foundational refresher spanning:

- **[Part 1](01-operating-system-concepts.md)** — Operating System Concepts (Windows, UNIX, Linux, macOS)
- **[Part 2](02-file-systems.md)** — File Systems (FAT/NTFS, EXT2/3/4, FHS, macOS)
- **[Parts 3–4](03-network-fundamentals-part1.md)** — Computer Network Fundamentals (models, types, topologies, hardware, protocols, TCP/IP internals, addressing)
- **[Part 5](05-network-troubleshooting.md)** — Basic Network Troubleshooting Techniques
- **[Part 6](06-virtualization.md)** — Virtualization Concepts
- **[Part 7](07-nfs.md)** — Network File System (NFS)
- **[Part 8](08-web-markup-and-programming-languages.md)** — Web Markup and Programming Languages
- **[Part 9](09-application-development-frameworks.md)** — Application Development Frameworks and Their Vulnerabilities
- **[Part 10](10-web-subcomponents.md)** — Web Subcomponents
- **[Part 11](11-database-connectivity.md)** — Database Connectivity (this file)

With these foundations in place, the CEH curriculum returns to attack-focused material — continuing from where [Module 2: Footprinting and Reconnaissance](../CEH-Module-02-Footprinting-and-Reconnaissance/README.md) left off, moving into Module 3: Scanning Networks.

---

*Part of the CEH Appendix A study series. [Return to the README](README.md) for the full index.*
