# 01 — Web Application Concepts

> Foundational knowledge: what a web application actually is, how it is put together, and why every layer of that stack is a potential point of failure. Everything later in this repo (threats, methodology, tools, defenses) builds on the mental model in this file.

## Table of Contents
- [What Is a Web Application?](#what-is-a-web-application)
- [How a Web Application Works — Request Lifecycle](#how-a-web-application-works--request-lifecycle)
- [Web Application Architecture](#web-application-architecture)
- [Web Application Components](#web-application-components)
- [Web 2.0 and Modern Web Applications](#web-20-and-modern-web-applications)
- [Web Services: SOAP vs REST](#web-services-soap-vs-rest)
- [The Vulnerability Stack](#the-vulnerability-stack)
- [Why Web Applications Are High-Value Targets](#why-web-applications-are-high-value-targets)

---

## What Is a Web Application?

A web application is server-side (and increasingly client-side) software that is reached through a web browser over HTTP/HTTPS, rather than being installed locally. Instead of shipping a compiled binary to a user's machine, the logic lives on a server; the browser only renders the interface and executes whatever script (usually JavaScript) the server hands it.

Key characteristics:
- **Runs inside a browser sandbox** — the client-side portion is constrained by the browser's execution environment (same-origin policy, DOM sandboxing, etc.).
- **Statelessness of HTTP, statefulness of the app** — HTTP itself has no memory of previous requests, so applications bolt state on top using cookies, sessions, tokens, or server-side session stores.
- **Dynamic content generation** — pages are frequently assembled on the fly from a database, template engine, or API response rather than served as static files.
- **Multi-language, multi-tier by nature** — a typical stack mixes HTML/CSS/JavaScript on the client with a server-side language (PHP, Java, Python, Node.js, C#/.NET, Ruby, Go) and a backend datastore (SQL or NoSQL).

Because so many moving, independently-developed parts are glued together, a web application's attack surface is larger than almost any other kind of software — and that's exactly why this module (and this repo) exists.

## How a Web Application Works — Request Lifecycle

A minimal but complete request/response cycle looks like this:

```
[ Browser ]  --HTTP GET /login.aspx?id=6329-->  [ Firewall ]  -->  [ Web Server ]
                                                                        |
                                                                        v
                                                              [ Web App Server / Runtime ]
                                                                        |
                                                            (executes application logic,
                                                             makes OS system calls)
                                                                        |
                                                                        v
                                                                  [ Database / DBMS ]
                                                          SELECT * FROM news WHERE id = 6329
                                                                        |
                                                                        v
[ Browser ]  <-- HTML/JSON response -------------------  [ Web Server ] <-- result set
```

Step by step:
1. The **user** submits a request through a browser — usually by clicking a link, submitting a form, or the browser itself constructing a request (AJAX/fetch).
2. The request traverses the **network/firewall** and reaches the **web server** (e.g., Apache, IIS, Nginx, LiteSpeed).
3. The web server hands dynamic requests to a **web application server / runtime** (PHP-FPM, Tomcat, Node.js process, .NET runtime, uWSGI, etc.), which executes the application's business logic.
4. That logic frequently needs to make **OS system calls** (reading files, spawning processes) and talks to a **DBMS** (MySQL, PostgreSQL, MSSQL, Oracle, MongoDB) to fetch or store data.
5. The result is formatted (HTML, JSON, XML) and sent back through the same chain to the browser, which renders it.

Every arrow in that diagram is a place an attacker can sit, intercept, or tamper: the browser (client-side attacks), the network path (MITM), the web server (misconfig, outdated software), the app runtime (business logic flaws, injection), and the database (SQL injection, excessive privileges).

## Web Application Architecture

Most modern web applications follow some variant of an **N-tier architecture**, splitting responsibilities into independent layers so each can scale, be secured, and be updated separately.

**Classic 3-tier model:**

| Tier | Responsibility | Common Technologies |
|---|---|---|
| **Presentation tier** (client) | Rendering UI, capturing input, client-side validation | HTML, CSS, JavaScript, React/Angular/Vue |
| **Logic tier** (application/middleware) | Business rules, session handling, orchestration, API endpoints | Java (Spring), .NET, Node.js/Express, Python (Django/Flask), PHP (Laravel) |
| **Data tier** | Persistent storage, queries, transactions | MySQL, PostgreSQL, MSSQL, Oracle, MongoDB, Redis |

Larger enterprise systems extend this into an **N-tier** design by adding:
- A **reverse proxy / load balancer** tier in front of the web servers (Nginx, HAProxy, F5, AWS ELB).
- A **caching tier** (Redis, Memcached, CDN edge caches) between the app and data tiers.
- A **web services / API gateway** tier that exposes internal functionality to other applications (Kong, AWS API Gateway, Apigee).
- A **message queue** tier for asynchronous processing (RabbitMQ, Kafka, SQS).

**Why the architecture matters to an attacker (and a defender):** each additional tier is both a defense-in-depth opportunity and a new component with its own CVEs, default credentials, and misconfiguration risks. A reverse proxy that forwards the wrong headers, a cache that stores authenticated pages for unauthenticated users (web cache poisoning), or an API gateway with an open admin endpoint can each single-handedly undo the security of every tier behind it.

## Web Application Components

A production web application typically bundles together:

- **Web server software** — Apache HTTP Server, Microsoft IIS, Nginx, LiteSpeed, Cherokee. Handles raw HTTP, TLS termination, virtual hosting, and static file serving.
- **Application/runtime layer** — executes the business logic: PHP, ASP.NET, JSP/Servlets, Node.js, Python WSGI/ASGI apps, Ruby on Rails.
- **Database Management System (DBMS)** — Oracle, MySQL/MariaDB, MSSQL, PostgreSQL, MongoDB, Redis. Stores everything from user credentials to transaction history.
- **Third-party components / libraries** — front-end frameworks, open-source packages (npm, pip, Maven/Gradle, NuGet), analytics SDKs, payment widgets. These are frequently the weakest link (see [Using Components with Known Vulnerabilities](./02-owasp-top-10-and-web-threats.md)).
- **Web services / APIs** — SOAP or REST endpoints that let other applications (mobile apps, partners, internal microservices) talk to the system programmatically.
- **Authentication/session infrastructure** — identity providers, SSO (SAML/OAuth/OIDC), session stores, MFA services.
- **Security appliances** — WAF, reverse proxy, IPS/IDS, RASP agents sitting in front of or embedded within the stack.

## Web 2.0 and Modern Web Applications

"Web 2.0" describes the shift from static, document-style websites to interactive, user-generated, API-driven applications: social networks, wikis, blogs, SaaS dashboards, single-page applications (SPAs). Characteristics that matter from a security standpoint:

- **Heavy client-side logic** — SPAs (React, Angular, Vue) push a large amount of application logic into the browser, expanding the client-side attack surface (DOM-based XSS, client-side routing bypass, exposed API keys in bundled JS).
- **AJAX / asynchronous communication** — pages update in the background via `XMLHttpRequest`/`fetch`, meaning traditional "view source" analysis alone won't reveal all functionality; passive/active spidering with a proxy is required.
- **Mashups and third-party integrations** — a single page may pull content and scripts from multiple origins, increasing reliance on those third parties' security postures (supply-chain risk).
- **User-generated content (UGC)** — comments, reviews, profile fields, uploaded files. Every UGC input point is a candidate injection point (stored XSS being the classic example).
- **Rich Internet Applications** — heavier use of client-side storage (localStorage, IndexedDB, cookies), WebSockets, and Service Workers, each with its own security model to understand.

## Web Services: SOAP vs REST

Web applications frequently expose functionality to other systems as **web services**. The two dominant styles:

| Aspect | SOAP | REST |
|---|---|---|
| Message format | Strict XML envelope (Header/Body) | Typically JSON, sometimes XML |
| Transport | Usually HTTP, but transport-agnostic | HTTP only, uses verbs (GET/POST/PUT/DELETE) |
| Contract | WSDL (Web Services Description Language) | OpenAPI/Swagger (optional, informal) |
| State | Can support stateful operations (WS-* extensions) | REST is meant to be **stateless** |
| Typical attacks | XML injection, XML External Entity (XXE), SOAPAction spoofing, WS-Address spoofing, oversized/recursive payload DoS | Injection via JSON/query params, broken object-level authorization (BOLA/IDOR), mass assignment, rate-limit bypass |

**Six REST constraints** (worth knowing because deviations from them often indicate a security gap):
1. **Client-Server** separation
2. **Statelessness** — every request must contain all information needed to process it (no server-side session reliance)
3. **Cacheability** — responses declare whether they can be cached (mislabeling this enables web cache poisoning)
4. **Uniform interface** — consistent resource-based URLs and standard HTTP verbs
5. **Layered system** — client cannot tell if it's talking directly to the server or through intermediaries (proxies, gateways)
6. **Code on demand** (optional) — server can extend client behavior by transmitting executable code (e.g., JavaScript)

REST and SOAP attacks are covered in depth in [07 — Web Services, API & Webhook Attacks](./07-web-services-api-and-webhook-attacks.md).

## The Vulnerability Stack

A web application is only as strong as its *weakest layer*, and CEH's "vulnerability stack" model is a useful way to reason about where a compromise can originate. From bottom to top:

| Layer | Element | Typical Weak Points |
|---|---|---|
| Layer 1 | **Security** | Missing/misconfigured IPS/IDS, no WAF, weak firewall rules |
| Layer 2 | **Network** | Unpatched routers/switches, flat network with no segmentation |
| Layer 3 | **Operating System** | Unpatched Windows/Linux/macOS host, weak service hardening |
| Layer 4 | **Database** | Default DB creds, excessive privileges, unpatched Oracle/MySQL/MSSQL |
| Layer 5 | **Web Server** | Outdated Apache/IIS, verbose banners, directory listing enabled |
| Layer 6 | **Third-Party Components** | Vulnerable open-source or commercial libraries/plugins |
| Layer 7 | **Custom Web Application** | Business logic flaws, injection points, broken access control |

An attacker only needs **one** exploitable layer to get a foothold; a defender has to secure **all seven** simultaneously. A concrete example of Layer 6 risk: a merchant site's core code (Layer 7) may be solid, but if it redirects to a third-party payment gateway (Layer 6) for checkout, an attacker who compromises that third party can pivot back into the primary site's trust relationship — exactly the mechanism behind [Magecart-style attacks](./08-other-web-app-attacks.md#magecart-attack).

## Why Web Applications Are High-Value Targets

- **Direct exposure to the internet** — unlike internal systems, most web apps are reachable by anyone, anywhere, with no need for prior network access.
- **Data concentration** — a single application often centralizes credentials, PII, payment data, and business logic in one place.
- **Complex, fast-moving codebases** — frequent releases, many contributors, and third-party dependencies mean the attack surface is constantly shifting.
- **Business impact of downtime or breach** — reputational damage, regulatory fines (GDPR, PCI-DSS, India's DPDP Act), and direct financial loss.
- **Low barrier to initial reconnaissance** — most of the information needed to start an assessment (technology stack, exposed endpoints, third-party integrations) is visible from the outside with basic tooling — see [03 — Footprinting & Reconnaissance](./03-footprinting-and-recon.md).

---

**Next:** [02 — OWASP Top 10 & Web Application Threats →](./02-owasp-top-10-and-web-threats.md)
