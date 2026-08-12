# Lab 04 — Email Header Analysis

## Objective

Learn to extract security-relevant information from a legitimate email header.

## Use

Use an email you own, a synthetic training email, or a header supplied by your course.

Do not upload private correspondence to public analysis services without permission.

## Header fields to inspect

- `Received`
- `From`
- `To`
- `Date`
- `Message-ID`
- `Reply-To`
- `Return-Path`
- SPF result
- DKIM result
- DMARC result

## Method

1. Preserve the original header.
2. Identify each `Received` hop.
3. Read the timestamps.
4. Identify mail systems and domains.
5. Check authentication results.
6. Separate confirmed information from assumptions.
7. Remove personal information from your notes if it is not necessary.

## Report

```text
Source:
Date:
Mail path:
Authentication:
Interesting infrastructure:
Confidence:
Security relevance:
```
