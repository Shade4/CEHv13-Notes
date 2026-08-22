# Appendix B: Ethical Hacking Essential Concepts – II
## Part 5 — Data Backup Process

[← Back to Part 4: Data Leakage Concepts](04-data-leakage.md) | [Next: Risk Management Concepts and Frameworks →](06-risk-management.md)

---

## Table of Contents

1. [Data Backup](#data-backup)
2. [RAID (Redundant Array of Independent Disks) Technology](#raid-redundant-array-of-independent-disks-technology)
3. [Advantages and Disadvantages of RAID Systems](#advantages-and-disadvantages-of-raid-systems)
4. [The RAID Levels](#the-raid-levels)
5. [Selecting an Appropriate Backup Method](#selecting-an-appropriate-backup-method)
6. [Choosing the Backup Location](#choosing-the-backup-location)
7. [Data Recovery](#data-recovery)
8. [Quick-Reference Summary](#quick-reference-summary)

---

## Data Backup

Data is the **heart** of any organization; data loss can be costly and have real financial impact. **Backup** is the process of making a duplicate copy of critical data that can be used for restore and recovery purposes when the primary copy is lost or corrupted, either accidentally or on purpose. Data backup plays a **crucial role** in maintaining business continuity by helping organizations recover from IT disasters such as hardware failures, application failures, security breaches, human error, and deliberate sabotage.

### Backup Strategy or Plan

- Identify critical business data
- Select backup media
- Select backup technology
- Select appropriate RAID levels
- Select an appropriate backup method
- Choose the backup location
- Select the backup types
- Choose the right backup solution
- Conduct a recovery drill test

---

## RAID (Redundant Array of Independent Disks) Technology

**RAID** is a method of combining multiple hard drives into a single unit and writing data across several disk drives — offering **fault tolerance** (if one drive fails, the system can continue operations).

Placing data on RAID disks enables I/O operations to overlap in a balanced way, improving system performance, simplifying storage management, and protecting against data loss. RAID represents a portion of computer storage that can divide and replicate data among several drives, working as **secondary storage**.

RAID has six commonly used levels — **RAID 0, RAID 1, RAID 3, RAID 5, RAID 10, and RAID 50** — each built from combinations of three underlying storage techniques:

- **Striping**
- **Mirroring**
- **Parity**

---

## Advantages and Disadvantages of RAID Systems

| Advantages | Disadvantages |
|---|---|
| Offers **hot-swapping/hot-plugging** — system component replacement (in case a drive fails) without affecting network functionality | Not compatible with some hardware components and software systems (e.g., system imaging programs) |
| Supports **disk striping**, improving read/write performance as the system fully utilizes processor speed | Data is **lost if drives fail one after another** — e.g., in RAID 5, a drive exclusive for parity can't recreate the first drive if a second drive also fails |
| Increased RAID **parity checks** prevent system crashes or data loss | Cannot protect data or offer performance boosts for all applications |
| Increased data **redundancy** helps restore data if a drive fails | RAID configuration is difficult |
| Increases **system uptime** | |

---

## The RAID Levels

### RAID Level 0 — Disk Striping

Splits data into blocks written evenly across multiple hard drives. Disk striping improves I/O performance by spreading the I/O load across many channels and disk drives.

- Data recovery is **not possible** if a drive fails
- Requires a minimum of **two drives**
- Does **not** provide data redundancy

### RAID Level 1 — Disk Mirroring

Multiple copies of data are simultaneously written to multiple drives, providing data redundancy by duplicating the drive data on multiple drives.

- If one drive fails, **data recovery is possible**
- Requires a minimum of **two drives**

### RAID Level 3 — Disk Striping with Parity

Data is striped at the **byte level** across multiple drives. One drive per set is dedicated to parity information.

- If a drive fails, **data recovery and error correction** are possible using the parity drive in the set
- The parity drive stores information about multiple drives

### RAID Level 5 — Block Interleaved Distributed Parity

Data is striped at the byte level across multiple drives, and parity information is **distributed among all member drives** (rather than dedicated to one drive, as in RAID 3).

- The data-writing process is **slow**
- Requires a minimum of **three drives**

### RAID Level 10 — Blocks Striped and Mirrored

A combination of **RAID 0 (striping)** and **RAID 1 (mirroring)** — requires a minimum of **four drives**.

- Has the same fault tolerance as RAID level 1, and the same mirroring overhead as RAID 0
- Stripes data across **mirrored pairs**: mirroring provides redundancy and improved performance; striping provides maximum performance

### RAID Level 50 — Mirroring and Striping Across Multiple RAID Levels

A combination of **RAID 0 striping** and the **distributed parity of RAID 5**.

- **More fault tolerant** than RAID 5, but uses twice the parity overhead
- Requires a minimum of **6 drives**. A drive from each segment can fail and the array will recover; if more than one drive fails within a single segment, the array stops functioning
- Offers greater reads/writes compared to RAID 5, and the highest levels of redundancy and performance among the levels covered here

---

## Selecting an Appropriate Backup Method

Select the backup method according to the organization's requirements, based on cost and ability.

| Method | Description | Advantage | Disadvantage |
|---|---|---|---|
| **Hot Backup (Online)** | Backs up data while the application, database, or system is **running** and available to users. Used when no downtime is allowed | Immediate data backup switchover is possible | Very expensive |
| **Cold Backup (Offline)** | Backs up data while the application, database, or system is **not running** (shut down) and unavailable. Used when scheduled downtime and a full backup are allowed | Least expensive | Switching over the data backup requires additional time |
| **Warm Backup (Nearline)** | A combination of both hot and cold backup | Less expensive than a hot backup; switchover takes less time than a cold backup (but more time than a hot backup) | Less accessible than a hot backup |

---

## Choosing the Backup Location

| Location | Description | Advantages | Disadvantages |
|---|---|---|---|
| **Onsite Data Backup** | Storing backup data only at onsite storage | Easily accessed and restored; less expensive | Greater risk of data loss |
| **Offsite Data Backup** | Storing backup data in remote locations, in fire-proof, indestructible safes | Data secured from physical threats such as fire or floods | Problems maintaining a regular data-backup schedule |
| **Cloud Data Backup** | Storing backup data on storage provided by an online backup provider | Data is encrypted and free from physical security threats; data can be freely accessed | No direct control over the backup data; more time needed for backup |

---

## Data Recovery

**Data recovery** is the process of recovering data that may have been accidentally or intentionally deleted or corrupted. Deleted items can include files, folders, and partitions from electronic storage media — hard drives, removable media, optical devices, and other storage media.

The majority of lost data is **recoverable**; however, there are situations where the damage to data is permanent and irreversible. When attempting to recover data from a target, a variety of data recovery tools can be used.

---

## Quick-Reference Summary

- **Backup strategy** spans 9 steps: identify critical data → select media/technology → choose RAID level → pick backup method → pick location → pick backup type → pick solution → test recovery
- **RAID** = fault tolerance via striping/mirroring/parity, across 6 common levels
- **RAID 0** (striping, no redundancy, 2+ drives) → **RAID 1** (mirroring, redundant, 2+ drives) → **RAID 3** (byte-level striping + dedicated parity drive) → **RAID 5** (byte-level striping + distributed parity, 3+ drives, slower writes) → **RAID 10** (striping + mirroring combined, 4+ drives) → **RAID 50** (striping + distributed parity combined, 6+ drives, highest redundancy/performance of the six)
- **3 backup methods by availability**: Hot (online, expensive, zero downtime) / Cold (offline, cheap, requires downtime) / Warm (nearline, a middle ground)
- **3 backup locations**: Onsite (cheap, fast, riskier) / Offsite (physically secure, scheduling friction) / Cloud (encrypted, accessible, less direct control)
- **Data recovery**: mostly possible, but not always — permanent/irreversible loss can happen

---

*Part of the CEH Appendix B study series — continues in [Part 6: Risk Management Concepts and Frameworks](06-risk-management.md).*
