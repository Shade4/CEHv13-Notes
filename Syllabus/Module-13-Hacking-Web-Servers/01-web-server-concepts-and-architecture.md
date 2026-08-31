# 01 — Web Server Concepts & Architecture

> Objective covered: **Summarize Web Server Concepts**

## 1. Why Web Server Security Matters

Most organizations extend their business presence onto the web through a **web server**. A web server is a critical piece of infrastructure — a single misconfiguration can lead to the compromise of an entire organization's public-facing presence. Because a web server is directly reachable from the internet, it's one of the most attractive and exposed targets in any network.

## 2. Web Server Operations

A web server is a computer system that **stores, processes, and delivers web pages** to clients over HTTP.

The basic client–server flow:

1. A client (browser) initiates an HTTP request.
2. The request travels over the network to the web server.
3. The web server collects the requested information/content from disk or from an application/database server.
4. The web server responds to the client with an appropriate HTTP response.
5. If the server cannot find/process the request, it returns an error response (4xx/5xx).

```
 ┌────────────┐   HTTP(S) Request   ┌────────────┐   Static Data Request   ┌──────────────┐
 │            │ ───────────────────>│            │ ───────────────────────>│              │
 │ Web Client │                     │ Web Server │                         │ Static Store │
 │            │ <───────────────────│            │ <───────────────────────│              │
 └────────────┘   HTTP(S) Response  └─────┬──────┘   Static Data Response  └──────────────┘
                                           │ Servlet Request/Response
                                           ▼
                                    ┌───────────────┐        Application       ┌──────────────┐
                                    │  Application  │ ───────────────────────> │ Application  │
                                    │  Server       │ <───────────────────────  │ Data Store   │
                                    │ (Web Container)│
                                    └───────────────┘
```
*(Figure 13.1 equivalent: typical client–server communication in web server operation)*

## 3. Components of a Web Server

| Component | Description |
|---|---|
| **Document Root** | The top-level root directory of the web server that stores web pages and static content. Example: if the requested URL is `www.certifiedhacker.com` and document root is `/admin/web`, document directory address is `/admin/web/certroot`. If URL is `www.certifiedhacker.com/P-folio/index.html`, server searches file path `/admin/web/certroot/P-folio/index.html`. |
| **Server Root** | The top-level directory in the directory tree where server configuration, log, and executable files are stored. Sub-directories usually include: `conf/` (server configuration files), `logs/` (server log files, incl. error logs), `cgi-bin/` (Common Gateway Interface scripts or other server-side executables). |
| **Virtual Document Tree** | Storage on a different machine/disk once the original disk becomes full. Case-sensitive; used to object-level redirect for a specific resource. Example: server searches `/admin/web/certroot/P-folio/index.html` on another disk if `admin/web/certroot` is stored elsewhere. |
| **Virtual Hosting** | A technique to host multiple domains/websites on the same server, sharing resources across companies. Types: **Name-based**, **IP-based**, **Port-based** hosting. |
| **Web Proxy** | Sits between the web client and web server; all requests are relayed through the proxy. Used to prevent IP blocking and maintain anonymity. |

## 4. Web Server Security Issues

**Why are web servers compromised?**

- Improper file and directory **permissions**
- **Unnecessary** default, sample, or unused files
- **Misconfigurations** in web server software, OS, and networks
- **Bugs** in server software, OS, and web applications
- **Administrative or debugging functions** that are enabled or accessible
- Use of **self-signed certificates** and default/weak certificates and encryption settings
- **Not using dedicated server** for web services

**Impact of web server attacks:**

- Compromise of user accounts
- Website defacement
- Secondary attacks from the website (visitors get attacked too)
- Data tampering and data theft
- Reputational damage of the company

### The 7-Layer Organizational Security Stack

An organization's security "stack" — attackers pick the weakest layer:

| Stack | Layer | Example |
|---|---|---|
| 7 | Business Logic Flaws | Custom Web Applications |
| 6 | Open Source/Commercial | Third-party Components |
| 5 | Apache/Microsoft IIS/Nginx | **Web Server** ← this module |
| 4 | Oracle/MySQL/MS SQL | Database |
| 3 | Windows/Linux/macOS | Operating System |
| 2 | Router/Switch | Network |
| 1 | IPS/IDS | Security |

### Common Goals Behind Web Server Attacks

- Stealing credit card details or other sensitive credentials via phishing
- Integrating the server into a botnet for DoS/DDoS attacks
- Compromising a database
- Obtaining closed-source applications
- Hiding and redirecting traffic
- Escalating privileges

> *"Keeping the server configuration secure requires vigilance." — OWASP*

### Dangerous Oversights That Make a Web Server Vulnerable

- Failing to update the web server with the latest patches
- Using the same system administrator credentials everywhere
- Allowing unrestricted internal and outbound traffic
- Running unhardened applications and services
- Providing complete error messages with server-version details
- Using outdated SSL/TLS encryption algorithms
- Using third-party plugins in the web application

### Why Are Web Servers Compromised — By Perspective

- **Webmaster's perspective:** the greatest security concern is that a webserver exposes the LAN or corporate intranet to internet threats posed by malicious content in web pages, images, Trojans, ActiveX, or the compromise of data.
- **Network administrator's perspective:** it is almost impossible to use a network while providing controlled access; a poorly configured web server can compromise the entire LAN's security.
- **End user's perspective:** users generally have no perception of immediate threat because surfing the web appears safe. Active content (JavaScript, ActiveX/Assembly) can introduce risk, and malware/ransomware can come through the LAN.

### Common Overlooked Server Weaknesses

- Improper file and directory permissions
- Installing the server with default settings
- Unnecessary services enabled, including content management and remote administration
- Security conflicts with the business's ease-of-use requirements
- Lack of a proper security policy, procedures, and maintenance

---

## 5. Apache Web Server Architecture

Apache HTTP Server is an **open-source, extensible, and highly configurable** HTTP server known for robustness, flexibility, and multi-protocol/multi-technology support. It handles both static and dynamic content, with a modular architecture that allows extensive customization.

```
                     ┌──────────────────────────────────────────┐
   HTTP(S) request → │              Apache Web Server            │
   ┌────────────┐    │  ┌───────────┐ ┌────────────┐            │  → Forwards dynamic
   │ HTTP Client│ ───>│  │ mod_ssl   │ │  mod_auth  │            │     content requests
   └────────────┘    │  └───────────┘ └────────────┘            │
   ← HTTP(S) response│  ┌───────────┐ ┌────────────┐            │
                     │  │mod_rewrite│ │ mod_proxy  │            │
                     │  └───────────┘ └────────────┘            │
                     │        HTTP Server (Core)                │
                     │──────────────────────────────────────────│
                     │      BMMTM Extensible Agent               │ → Retrieves dynamic
                     │──────────────────────────────────────────│    content from
                     │            Application Server            │    Application Server
                     └──────────────────────────────────────────┘
```
*(Figure 13.4 equivalent)*

### Functional Components

- **HTTP Client**: browser or software that initiates requests to the Apache server, asking for web pages/files/other resources.
- **HTTP Server (Core)**: the core module that handles HTTP(S) requests and responses, interfacing with modules such as `mod_ssl`, `mod_rewrite`, `mod_proxy`, and `mod_auth` to provide additional functionality.
  - **`mod_auth`**: manages user authentication, ensuring only authorized users can access specific web resources based on the configured credentials.
  - **`mod_ssl`**: provides SSL/TLS encryption to secure communication between the server and clients.
  - **`mod_rewrite`**: enables URL rewriting, customized URLs, and redirection based on specified rules.
  - **`mod_proxy`**: functions as a proxy and gateway, forwarding requests to other servers and load balancing.
- **BMMTM Extensible Agent**: intercepts HTTP(S) transaction data; enhances monitoring and performance analysis by providing insights into interactions between clients and servers.
- **Application Server**: executes backend applications, processes data, and generates dynamic content that the web server then serves. Used to run applications written in PHP, Java, Python, etc.

### Table 13.1 — Apache Server Vulnerabilities

| Vulnerability | Description |
|---|---|
| **HTTP response splitting** | Occurs when improperly validated input allows attackers to inject malicious headers into HTTP responses, potentially leading to cross-site scripting (XSS), cache poisoning, or sensitive information disclosure. |
| **HTTP/2 DoS by memory exhaustion on endless continuation frames** | Attackers send continuous HTTP/2 headers, leading to excessive memory consumption and a potential DoS. Attackers exploit this by sending specially crafted requests that trigger the over-read, potentially revealing sensitive information stored in adjacent memory locations. |
| **`mod_macro` buffer over-read** | Occurs when the `mod_macro` module improperly handles macro expansion, causing it to read beyond the buffer's end. |
| **DoS in HTTP/2 with initial window size 0** | This vulnerability arises when an attacker sets the HTTP/2 initial window size to 0, which blocks the server from sending data. Attackers exploit this by sending the initial window size to 0 for window size updates, leading to a denial of service (DoS). |
| **HTTP/2 stream memory not reclaimed right away on RST** | This vulnerability occurs when memory allocated for a stream reset is not immediately freed upon receiving a stream reset (RST) frame. |
| **Insecure default configuration** | Arises from insecure default admin credentials, leading to remote code execution (RCE). Attackers exploit this by using the default credentials to gain admin access and execute arbitrary code. |
| **Improper authorization** | Arises from improper authorization mechanisms within the server's core components. Attackers can exploit this by exploiting the faulty checks to gain unauthorized access or escalate their privileges to access and perform restricted actions. |
| **DNS rebinding in import functionality** | Occurs because of inadequate input validation in the import functionality of Apache Allura. It allows attackers to manipulate DNS responses and access internal services, potentially exposing sensitive information. |
| **Environment variable injection** | Arises from improper handling of environment variables, allowing attackers to override configurations such as `ZEPPELIN_INTP_CLASSPATH_OVERRIDES` in Apache Zeppelin. Attackers leverage this by injecting malicious code or commands into these variables, leading to arbitrary code execution on the server. |
| **Code injection** | Arises from connecting to a MySQL database via the JDBC driver in Apache Zeppelin. Attackers can inject sensitive configuration or malicious code during the database connection setup, leading to remote code execution. |
| **Improper certificate validation** | Arises from improper certificate validation in FTP_TLS connections of Apache Airflow. Attackers can leverage this by intercepting and manipulating FTP traffic, potentially leading to man-in-the-middle (MITM) attacks. |
| **Cross-site scripting (XSS)** | Arises due to improper input handling which allows attackers to leverage this by injecting malicious scripts into task logs. Attackers can insert harmful data into task logs, enabling arbitrary script execution in a victim's browser. |
| **Path-traversal vulnerability** | Arises due to improper limitation of a pathname to a restricted directory, allowing attackers to access files and directories outside the intended directory in Apache OFBiz. Attackers can leverage this vulnerability to potentially execute arbitrary code or navigate to unintended directories. |
| **SQL injection** | Caused by improper neutralization of special elements in SQL commands of Apache Submarine Server Core. Allows attackers to execute arbitrary SQL queries for unauthorized access, data retrieval, or modification of the database. |

*Source: https://httpd.apache.org*

---

## 6. IIS (Internet Information Services) Web Server Architecture

IIS is a Windows web server application developed by Microsoft. It runs on and responds to browser requests, and supports **HTTP, HTTP Secure (HTTPS), File Transfer Protocol (FTP), FTP Secure (FTPS), Simple Mail Transfer Protocol (SMTP), and Network News Transfer Protocol (NNTP)**. Its ASP.NET application uses HTML for the user interface and compiled Visual Basic code for processing. IIS is flexible and easy-to-manage for web hosting.

```
                    Kernel mode                          User mode
 ┌─────────────┐    ┌───────────────┐         ┌─────────────────────────────────┐
 │ HTTP Client │───>│  HTTP.sys     │────────>│  Windows Activation Service (WAS)│
 │  (browser)  │<───│  (HTTP.sys)   │<────────│  WWW Service                     │
 └─────────────┘    └───────────────┘         │        │                        │
                                               │        ▼                        │
                                               │  Worker Process (W3WP.exe)      │
                                               │  ┌──────────┬─────────────────┐ │
                                               │  │Web Server│  Application    │ │
                                               │  │  Core    │  Pool           │ │
                                               │  │(Native   │ (Native Modules,│ │
                                               │  │ Modules) │  Managed Modules│ │
                                               │  │          │  Pure           │ │
                                               │  │          │  Authentication)│ │
                                               │  └──────────┴─────────────────┘ │
                                               └─────────────────────────────────┘
```
*(Figure 13.5 equivalent)*

### IIS Components

- **Protocol listeners** (known as HTTP.sys)
- **World Wide Web Publishing Service** (known as WWW service)
- **Windows Process Activation Service** (WAS)

### Responsibilities of the IIS Components

- Listening to requests coming from the server
- Managing processes
- Reading configuration files

### How IIS Processes a Request (step by step)

1. An HTTP request for a resource is sent from the client browser to the web server; the request is intercepted by **HTTP.sys**.
2. `HTTP.sys` communicates with **WAS** to collect data from `ApplicationHost.config`, the root file in the configuration system in the IIS web server.
3. **WAS** raises a request for configuration information, such as the site and application pool, which is then sent to the **WWW Service**.
4. The **WWW Service** uses the configuration information obtained to configure `HTTP.sys`.
5. A worker process (`w3wp.exe`) is initiated by WAS for the application pool to which the request is intended.
6. The request is then processed by the worker, and the response is returned to `HTTP.sys`.
7. The client browser receives the response.

IIS depends on a group of DLLs that work collectively with the main server process (`inetinfo.exe`), capturing different functions such as content indexing, server-side scripting, and web-based printing.

### Table 13.2 — IIS Vulnerabilities

| Vulnerability | Description |
|---|---|
| **Trust boundary violation vulnerability** | Results from inadequate separation of privilege boundaries, allowing an unauthenticated entity to access restricted functionality in the Telerik Report Server. Exploiting this flaw may lead to unauthorized server operations manipulation. |
| **Authentication bypass vulnerability** | Occurs due to specific issues in the implementation of the authentication process where an insecure endpoint allows unauthenticated access to restricted server functionality. Attackers can leverage this vulnerability to circumvent authentication and execute arbitrary code on the server. |
| **CRLF cross-site scripting vulnerability** | Arises due to misconfigurations in the SiteMinder Web Agent for IIS Web Server. Attackers can execute arbitrary JavaScript code in a client's browser by exploiting this vulnerability. |
| **CCURE passwords exposed to administrators** | Arises due to improper handling and logging of sensitive information within the C•CURE 9000 Web Information Server (IIS) while hosting the C•CURE 9000 Web Server. Attackers can exploit this vulnerability and access these logs to retrieve sensitive Windows credentials. |
| **Arbitrary file path access vulnerability** | Occurs due to the default configuration of the Aquaforest TIFF Server, which improperly restricts access to file paths. Attackers can exploit this vulnerability to access, enumerate, or traverse directories and files, potentially bypassing authentication or accessing restricted files. |
| **Windows IIS server elevation of privilege vulnerability** | Occurs due to the server's improper handling of specific requests in Windows IIS Server. Attackers can leverage this vulnerability to obtain unauthorized access and take control of the server. |
| **File and directory permissions vulnerability** | Arises due to incorrect default permissions in Hitachi JP1/Performance Management software on Windows. Attackers can leverage this vulnerability to manipulate files and directories and access sensitive information. |
| **TYPO3 cross-site scripting (XSS) vulnerability** | Unfiltered use of the server environment variable `PATH_INFO` in the `GeneralUtility::getIndpEnv()` component of the TYPO3 Content Management Framework. Attackers exploit this by injecting malicious HTML code into unpatched pages, potentially affecting other visitors. |
| **Multibyte XSS in password manager** | Occurs due to improper handling of file paths in certain mail server contexts. Allows authenticated mail users to add files with unsanitized content in public folders where the IIS server has permission to write, potentially leading to arbitrary code execution. |
| **MailEnable vulnerability** | Occurs due to improper neutralization of user-controllable input within the `/isapi/PasswordManager.dll` `ResultURL` parameter. Attackers can exploit this vulnerability to inject malicious scripts and steal sensitive information. |
| **XSS in password manager** | (See "Multibyte XSS in password manager" above — related class of vulnerability affecting the MailEnable password manager component.) |

*Source: https://cve.mitre.org*

---

## 7. Nginx Web Server Architecture

Nginx is a high-performance, scalable web server, **reverse proxy, and load balancer** that operates on a master-worker architecture. It employs a single-threaded, event-driven, asynchronous, and non-blocking model to efficiently manage multiple connections. The core of Nginx's architecture comprises a **master process** that oversees multiple **worker processes** responsible for handling client requests.

```
                      ┌───────────────┐
   Clients  ────────> │ Master Process│
                      └───────┬───────┘
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼
      ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
      │Worker Process│  │Worker Process│  │Worker Process│
      └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
             │  HTTP / FastCGI │                │
             └────────┬────────┴────────┬───────┘
                       ▼                 ▼
                 ┌──────────┐      ┌───────────┐
                 │  Cache    │      │ Memcache  │
                 │ (Proxy    │      │           │
                 │  Cache)   │      └───────────┘
                 └─────┬─────┘
                       ▼
                  ┌──────────┐
                  │ Backend  │
                  └──────────┘
```
*(Figure 13.6 equivalent — includes Cache Loader and Cache Manager sub-components)*

### Components

- **Master Process**: reads and validates HTTP server configuration; creates, binds, and closes sockets; manages worker processes and ensures they are properly configured and run correctly.
- **Worker Processes**: handle client requests by accepting connections, reading/writing data, and communicating with upstream servers. Each single-threaded worker uses non-blocking I/O to handle over 1000 concurrent connections simultaneously.
- **Proxy Cache**: the proxy cache store composes cached content of served content, reduces backend server load, and speeds up response times by serving frequently accessed content directly from the cache memory.
  - **Cache Loader**: loads cache metadata into memory at Nginx startup, ensuring the cache is ready to immediately serve requests. It scans the cache directories and initializes the in-memory cache structures.
  - **Cache Manager**: periodically checks the cache for expired content and removes old/unused cache entries into free space, ensuring the cache does not grow beyond its configured size.
- **Web Server**: the web server component of Nginx handles HTTP requests sent by clients, serving static content and forwarding requests to the application servers.
- **Application Server**: processes requests from clients by running server-side scripts/applications and delivering dynamic content to clients.
- **Memcache**: serves as a caching layer that stores data in memory for the rapid retrieval of frequently accessed data, reducing the need for repeated database queries.

### Table 13.3 — Nginx Vulnerabilities

| Vulnerability | Description |
|---|---|
| **NULL pointer dereference in HTTP/3** | Occurs due to a NULL pointer dereference in Nginx's QUIC module when handling HTTP/3 requests, allowing attackers to cause servers to terminate. |
| **Excessive memory usage and CPU exhaustion in HTTP/2** | This vulnerability allows attackers to cause improper memory handling and excessive CPU usage in HTTP/2, flooding the server with HTTP/2 requests to consume memory and CPU, disrupting normal operations. |
| **Server-side request forgery (SSRF) vulnerability** | Occurs due to a Server-Side Request Forgery (SSRF) vulnerability in the upload link feature of `mintplex-labs/anything-llm`. Attackers can exploit this by hosting a malicious website, allowing them to perform internal port scanning, access non-public web applications, execute arbitrary file deletion, and carry out local file inclusion. |
| **Remote code execution vulnerability** | Arises due to the exposed configuration settings via Nginx-UI. Attackers can exploit this to perform remote code execution, privilege escalation, or information disclosure. |
| **Improper certificate validation** | Occurs due to the improper validation of user input in the Import Certificate feature of Nginx-UI. Attackers can exploit this vulnerability to perform arbitrary file writes. |
| **SQL injection vulnerability** | Occurs due to improper neutralization of special SQL elements, allowing unsanitized user-controlled parameters to be appended to SQL queries. Attackers can exploit this vulnerability to execute arbitrary SQL queries for unauthorized access or data breaches. |
| **Unauthenticated private keys access** | Arises from the reliance on `.htaccess` for security, which fails to work on Nginx servers that don't support `.htaccess` files. Attackers can leverage this vulnerability to read private keys by accessing the site on a server that does not support `.htaccess` files. |
| **SQL injection vulnerability (nginxWebUI)** | See "SQL injection vulnerability" above — same class affects `nginxWebUI` specifically. |
| **OS command injection in nginxWebUI** | Occurs due to improper handling of file arguments in the upload feature. Attackers can exploit this vulnerability to manipulate arguments to inject and execute OS commands remotely on the server. |
| **Default file permissions vulnerability** | Occurs because the Nginx Management Suite sets default file permissions that allow authenticated modification of sensitive files. Attackers can leverage this vulnerability to modify sensitive files on the Nginx Instance Manager and Nginx API Connectivity Manager. |

*Source: https://cve.mitre.org*

---

**Next:** [02 — Web Server Attack Techniques →](02-web-server-attack-techniques.md)
