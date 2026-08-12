# Lab 03 — Traceroute Analysis

## Objective

Understand network path observation.

## Linux

```bash
traceroute example.com
```

## Windows

```powershell
tracert example.com
```

## Record

| Hop | Host/IP | Latency | Provider clue | Notes |
|---:|---|---:|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

## Questions

- Which hops respond?
- Which hops do not respond?
- Where does the apparent provider change?
- Does the path remain stable across repeated tests?
- What information is uncertain?

## Important

A timeout does not necessarily mean the router is absent. It may simply filter or rate-limit traceroute traffic.
