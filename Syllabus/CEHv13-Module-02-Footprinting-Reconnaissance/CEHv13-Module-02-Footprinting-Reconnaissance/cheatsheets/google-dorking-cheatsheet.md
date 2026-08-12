# Google Search Operator Cheat Sheet

## Common operators

```text
site:
filetype:
intitle:
inurl:
"exact phrase"
-term
```

## Examples

```text
site:example.com
site:example.com filetype:pdf
site:example.com intitle:"annual report"
site:example.com inurl:docs
site:example.com "security policy"
site:example.com filetype:txt -example
```

## Responsible use

Search operators should be used to understand **publicly indexed exposure** during authorized security work.

Do not treat search results as permission to access a system or bypass authentication.

## Investigation pattern

```text
Query
 ↓
Result
 ↓
Source
 ↓
Ownership validation
 ↓
Freshness check
 ↓
Security relevance
 ↓
Evidence
```
