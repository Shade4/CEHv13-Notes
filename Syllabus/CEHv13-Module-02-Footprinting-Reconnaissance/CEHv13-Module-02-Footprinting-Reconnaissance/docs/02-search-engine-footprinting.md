# 02 — Footprinting Through Search Engines

Search engines are powerful OSINT indexes.

## Why search engines matter

Search engines can reveal:

- Public pages
- Documents
- Cached/indexed content
- Technology references
- Employee pages
- Job advertisements
- Error pages
- Configuration fragments
- Public repositories
- Historical content

## Search operators

Operators vary by search engine. Common Google-style operators include:

| Operator | Purpose | Safe example |
|---|---|---|
| `site:` | Restrict results to a domain | `site:example.com security` |
| `filetype:` | Search for a file type | `site:example.com filetype:pdf` |
| `intitle:` | Search title text | `site:example.com intitle:security` |
| `inurl:` | Search URL text | `site:example.com inurl:docs` |
| `"..."` | Exact phrase | `"security policy"` |
| `-term` | Exclude a term | `site:example.com security -jobs` |

Use operators to understand what an organization has made searchable, not to bypass authentication.

## Google Hacking / Google Dorking

Google Hacking is the use of advanced search syntax to locate information that has already been indexed.

The important idea:

> The search engine is not necessarily breaking into the system. It may simply be showing information that was already exposed or indexed.

### Example

```text
site:example.com filetype:pdf
```

This can help an authorized tester inventory public PDF documents.

Another:

```text
site:example.com intitle:"annual report"
```

This focuses the search on pages whose titles contain the phrase.

## Google Hacking Database (GHDB)

GHDB is a categorized collection of search queries used for security research.

Categories can include:

- Files containing sensitive information
- Web server detection
- Error messages
- Network information
- Vulnerable services
- Various application-specific searches

A GHDB query is a **search pattern**, not proof of compromise.

## Search-engine methodology

1. Start broad.
2. Identify official domains.
3. Restrict with `site:`.
4. Search for document types.
5. Search technology terms.
6. Search historical or public references.
7. Record interesting results.
8. Validate ownership and freshness.
9. Remove false positives.

## Safe practice

Do not use search operators to collect private information that is not needed for the engagement.

Do not download or retain sensitive information merely because it is accessible.

## Shodan

Shodan indexes information about Internet-connected services.

Conceptually, Shodan can help identify:

- Publicly reachable services
- Service banners
- Ports
- Technology clues
- Organization/host relationships
- Geographic information
- Historical observations

Shodan is useful for defensive exposure management because organizations can search for their own Internet-visible infrastructure.

### Important distinction

A Shodan result means:

> "A service was observed and indexed."

It does **not** automatically mean:

> "The service is currently vulnerable."

Always verify within authorized scope.

## Other search resources

Depending on the engagement, useful sources can include:

- Search engines
- Public certificate transparency services
- Public code-hosting platforms
- Internet archives
- Security research databases
- Public documentation
- News databases

## Search-engine countermeasures

Organizations should:

- Review indexed public content
- Remove unnecessary sensitive documents
- Apply appropriate access controls
- Avoid publishing secrets
- Review metadata
- Use search-engine removal mechanisms where appropriate
- Monitor public exposure
- Periodically perform external attack-surface reviews
