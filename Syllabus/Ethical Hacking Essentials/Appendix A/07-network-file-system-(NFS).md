# Appendix A: Ethical Hacking Essential Concepts – I
## Part 7 — Network File System (NFS)

[← Back to Part 6: Virtualization Concepts](06-virtualization.md) | [Next: Web Markup and Programming Languages →](08-web-markup-and-programming-languages.md)

---

## Table of Contents

1. [What Is NFS?](#what-is-nfs)
2. [NFS Security](#nfs-security)
3. [Host and File Level Security](#host-and-file-level-security)
4. [Quick-Reference Summary](#quick-reference-summary)

---

## What Is NFS?

The **Network File System (NFS)** is a **distributed file system protocol** that allows users to read, write, store, and access files across devices connected through a network — as if those remote files lived on local storage. NFS works on all **IP-based networks** and uses **TCP/UDP** for data access and delivery.

---

## NFS Security

NFS offers two types of security:

1. **Host level** — access control at the level of which hosts are permitted to connect at all
2. **File level** — operational restrictions on what an already-connected host can actually do to files

---

## Host and File Level Security

- **Host level security** refers to **restricting certain operations** when the remote user doesn't provide correct credentials
- **File level security** refers to **limiting actions** on the files within a mounted file system

### Methods of Securing Access Controls in NFS

| Method | What It Does |
|---|---|
| **Root Squashing** | The process of limiting superuser access privileges using identity authentication. To enforce restrictions on the superuser, administrators map the root's UID to the anonymous user in the NFS RPC credential structure |
| **nosuid** | Does not allow the SUID or SGID bits to take effect on the mounted filesystem. Uses the `nosuid` option to prevent execution of NFS-mounted user-identity executables on the host |
| **noexec** | Prevents the execution of files from the mounted partition. Uses the `noexec` option to prevent a user's identity from executing binaries |

---

## Quick-Reference Summary

- **NFS** = a distributed file system protocol for reading/writing/storing/accessing files across a network, running over IP using TCP/UDP
- **2 security levels**: Host (who can connect) and File (what they can do once connected)
- **3 access-control methods**: **Root squashing** (maps root's UID to an anonymous user), **nosuid** (blocks SUID/SGID from taking effect), **noexec** (blocks binary execution from the mounted partition)

---

*Part of the CEH Appendix A study series — continues in [Part 8: Web Markup and Programming Languages](08-web-markup-and-programming-languages.md).*
