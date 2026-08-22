# Appendix B: Ethical Hacking Essential Concepts – II
## Part 2 — Network Segmentation Concepts

[← Back to Part 1: Information Security Controls](01-information-security-controls.md) | [Next: Network Security Solutions →](03-network-security-solutions.md)

---

## Table of Contents

1. [Network Segmentation](#network-segmentation)
2. [Network Security Zoning](#network-security-zoning)
3. [Network Segmentation Example: DMZ](#network-segmentation-example-dmz)
4. [Network Virtualization (NV)](#network-virtualization-nv)
5. [Virtual Networks](#virtual-networks)
6. [VLANs](#vlans)
7. [Quick-Reference Summary](#quick-reference-summary)

---

## Network Segmentation

**Network segmentation** is the practice of splitting a network into smaller network segments and separating groups of systems or applications from each other.

It defeats the drawback of the traditional **flat network**, where all network resources (servers, workstations) sit on the same network. If an attacker manages to penetrate a flat network through perimeter defense, they can move around it with relative ease. In a **segmented** network, groups of systems or applications with no need to interact are placed in different network segments — so even if an attacker breaches one segment's security, they still can't reach network resources sitting in other segments.

### Security Benefits of Network Segmentation

- Improved Security
- Better Access Control
- Improved Monitoring
- Improved Performance
- Better Containment

### Example Segmented Architecture

A typical layout separates **Internal Zone** (user workstations, internal servers) from two **DMZ zones** — one holding proxy/email/web servers facing the internet through a firewall, and another holding application/database servers — with a firewall mediating traffic between all zones and the internet.

---

## Network Security Zoning

**Network security zoning** is a mechanism that lets an organization manage a secure network environment by selecting the appropriate security levels for different zones of internet and intranet networks. It helps effectively monitor and control inbound and outbound traffic.

### Examples of Network Security Zones

| Zone | Description |
|---|---|
| **Internet Zone** | An uncontrolled zone outside the boundaries of an organization |
| **Internet DMZ** | A controlled zone that provides a barrier between internal networks and the internet |
| **Production Network Zone** | A restricted zone that strictly controls direct access from uncontrolled networks |
| **Intranet Zone** | A controlled zone with no heavy restrictions |
| **Management Network Zone** | A secured zone with strict policies |

---

## Network Segmentation Example: DMZ

A **Demilitarized Zone (DMZ)** is a computer subnetwork placed between an organization's private network (such as a LAN) and an outside public network (such as the internet) — acting as an additional security layer.

**Contains the servers that need to be accessed from an outside network:** web servers, email servers, DNS servers.

### DMZ Configurations

- Both internal and external networks can connect to the DMZ
- **Hosts** in the DMZ can connect to external networks
- But hosts in the DMZ **cannot** connect to internal networks

A typical setup places the DMZ network behind a **three-legged firewall**, with the internal network sitting behind that same firewall on a separate leg — keeping the DMZ, internal network, and internet each isolated from one another except through firewall-mediated paths.

---

## Network Virtualization (NV)

**Network Virtualization** is the process of combining all available network resources and allowing network administrators to share those resources among network users using a single administrative unit.

This is done by splitting available bandwidth into **independent channels**, which can be assigned or reassigned to a particular server or device in real time. This lets each network user access all available network resources (files, folders, computers, printers, hard drives, or other resources) from their own computer.

### Why Network Virtualization?

- Efficient, flexible, scalable usage of the network
- To logically segregate the underlay administrative domain from the overlay domain
- To accommodate the dynamic nature of server virtualization
- To provide security and isolation of traffic and network details from one user to another
- To cope with virtualization techniques in other areas (compute and storage)

---

## Virtual Networks

**Virtual networks** are the end product of network virtualization. Virtual network software is used for virtual networking, and can be placed either outside a virtual server (external) or inside a virtual server, depending on the size and type of the virtualization platform.

A typical architecture stacks separate virtual networks (e.g., "Virtual Network Finance," "Virtual Network Engineering") on top of a shared **Virtualization Layer**, which itself sits on top of the actual **Physical Network**.

---

## VLANs

**VLANs (Virtual Local Area Networks)** are logical groupings of workstations, servers, and network devices that behave as if they're on a single, isolated LAN — regardless of their actual physical location.

The purpose of a VLAN is to create a **simple network with improved security** and better traffic management. Multiple VLANs (e.g., Virtual LAN A, B, C) can share the same physical LAN segment and switch/hub hardware, kept logically separate, and interconnected across switches (e.g., Cisco 2950 switches) using **802.1Q trunk** links.

---

## Quick-Reference Summary

- **Network segmentation** splits a flat network into isolated segments, containing breaches and improving security/access-control/monitoring/performance
- **5 named security zones**: Internet, Internet DMZ, Production Network, Intranet, Management Network
- **DMZ**: a buffer subnetwork holding internet-facing servers (web/email/DNS); DMZ hosts can reach external networks but not the internal network
- **Network virtualization** combines and shares network resources via independent, dynamically-assignable bandwidth channels
- **Virtual networks** are the output of that virtualization, sitting on a Virtualization Layer above the physical network
- **VLANs** logically group devices regardless of physical location, using trunk links (802.1Q) to interconnect across switches while staying logically isolated

---

*Part of the CEH Appendix B study series — continues in [Part 3: Network Security Solutions](03-network-security-solutions.md).*
