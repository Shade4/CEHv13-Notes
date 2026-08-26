# Cheat Sheet — Cisco IOS / Juniper Sniffing-Defense Commands

Every switch/router hardening command from this module, consolidated by defense category. Cross-references point back to the topic file with full context and worked examples.

---

## 1. Port Security (defends: MAC flooding, switch port stealing, DHCP starvation)
Full context: [02 — MAC Attacks](../02-mac-attacks.md), [03 — DHCP Attacks](../03-dhcp-attacks.md)

```cisco
interface interface_id
switchport mode access
switchport port-security
switchport port-security maximum value
switchport port-security violation {restrict | shutdown}
switchport port-security limit rate invalid-source-mac
switchport port-security mac-address mac_address
switchport port-security mac-address sticky
switchport port-security aging time 2
switchport port-security aging type inactivity
end
show port-security address
show port-security address interface interface_id
snmp-server enable traps port-security trap-rate 5
```

---

## 2. DHCP Snooping (defends: rogue DHCP servers, MAC spoofing)
Full context: [03 — DHCP Attacks](../03-dhcp-attacks.md), [04 — ARP Poisoning](../04-arp-poisoning.md)

```cisco
ip dhcp snooping
ip dhcp snooping vlan number [number] | vlan {vlan range}
ip dhcp snooping vlan 4,104
ip dhcp snooping trust
ip dhcp snooping limit rate
end
show ip dhcp snooping
show ip dhcp snooping binding
no ip dhcp snooping information option
no ip dhcp snooping information option allow-untrusted
```

## 2a. MAC Limiting on Juniper switches
```
set interface ge-0/0/1 mac-limit 3 action drop
set interface ge-0/0/2 mac-limit 3 action drop
show
show ethernet-switching table
```

## 2b. DHCP Filtering (generic CLI, e.g. Dell/other vendors)
```
config
    <IP address> dhcp filtering
    exit
exit

config
    interface 0/11
        <IP address> dhcp filtering trust
        exit
    exit

show <IP address> dhcp filtering
```

---

## 3. Dynamic ARP Inspection — DAI (defends: ARP poisoning/spoofing)
Full context: [04 — ARP Poisoning](../04-arp-poisoning.md)

> Prerequisite: DHCP snooping (section 2) must already be enabled — DAI validates against the DHCP snooping binding table.

```cisco
ip arp inspection vlan 10
ip arp inspection vlan 10, 11, 12, 13
ip arp inspection vlan 10-13
ip arp inspection validate {src-mac | dst-mac | ip}
show ip arp inspection
```

---

## 4. VLAN Hopping Defense (switch spoofing + double tagging)
Full context: [05 — Spoofing Attacks](../05-spoofing-attacks.md)

```cisco
! Defend against switch spoofing
switchport mode access
switchport mode nonegotiate
switchport mode trunk
switchport mode nonegotiate

! Defend against double tagging
switchport access vlan 2
switchport trunk native vlan 999
vlan dot1q tag native
```

---

## 5. STP Attack Defense (BPDU Guard / Root Guard / Loop Guard / UDLD)
Full context: [05 — Spoofing Attacks](../05-spoofing-attacks.md)

```cisco
! BPDU Guard -- apply to all PortFast edge ports
configure terminal
interface gigabitethernet slot/port
spanning-tree portfast bpduguard

! Root Guard -- protects the root bridge
configure terminal
interface gigabitethernet slot/port
spanning-tree guard root

! Loop Guard -- protects against malfunctioning switches causing loops
configure terminal
interface gigabitethernet slot/port
spanning-tree guard loop

! UDLD -- detect and disable unidirectional links
configure terminal
interface gigabitethernet slot/port
udld { enable | disable | aggressive }
```

---

## 6. Promiscuous-Mode / Sniffer Detection
Full context: [08 — Countermeasures & Detection](../08-countermeasures-and-detection.md)

```bash
# Nmap NSE script to detect a NIC running in promiscuous mode
nmap --script=sniffer-detect [Target IP Address/Range of IP addresses]

# Example
nmap --script=sniffer-detect 10.10.1.19
```

---

## Quick decision table — "which command family do I need?"

| Symptom / Goal | Section |
|---|---|
| Attacker flooding CAM table with fake MACs | §1 Port Security |
| Rogue DHCP server on the network | §2 DHCP Snooping |
| Too many DHCP clients on one port | §2a MAC Limiting / §1 Port Security (max) |
| ARP cache poisoning / MITM via forged ARP replies | §3 Dynamic ARP Inspection |
| Unauthorized trunk / VLAN jumping | §4 VLAN Hopping Defense |
| Rogue switch trying to become STP root bridge | §5 STP Attack Defense |
| Need to confirm whether a host is sniffing | §6 Promiscuous-Mode Detection |
