# 07 — OT/ICS Concepts and Architecture

> Learning Objective 4: *Explain OT Concepts and Attacks* (concepts half).

## Table of Contents

- [What is OT?](#what-is-ot)
- [Industrial Network vs. Business Network](#industrial-network-vs-business-network)
- [Introduction to ICS](#introduction-to-ics)
- [Essential ICS Terminology](#essential-ics-terminology)
- [Open, Closed, and Manual Control Loops](#open-closed-and-manual-control-loops)
- [Components of an ICS](#components-of-an-ics)
- [Safety Instrumented Systems (SIS)](#safety-instrumented-systems-sis)
- [IT/OT Convergence (IIoT)](#itot-convergence-iiot)
- [The Purdue Model](#the-purdue-model)
- [OT Technologies and Protocols per Purdue Level](#ot-technologies-and-protocols-per-purdue-level)

---

## What is OT?

**Operational Technology (OT)** is the combination of hardware and software designed to detect or cause changes in physical industrial processes, through direct monitoring and/or control of physical devices such as valves, pumps, sensors, motors, conveyors, elevators, and heating/cooling systems.

OT is used across nearly every heavy-industry vertical:

- Manufacturing
- Mining
- Healthcare
- Building management
- Transportation
- Oil and gas
- Defense
- Utility sectors (electricity, water, gas)

OT systems employ different approaches to design hardware and protocols than IT, so **supporting older versions of software and hardware makes OT systems very difficult to patch or upgrade** — a plant may run a PLC firmware from a decade ago because replacing it means a costly, scheduled shutdown of a production line, not a routine patch-Tuesday reboot.

### Devices Connected to an OT Network — By Sector

| Sector | Representative Devices |
|---|---|
| **Utility Sector** | Water pumps, electricity grid controls, gas-flow controls |
| **Healthcare Industry** | Building HVAC, patient-monitoring infrastructure tied into facility control |
| **Traffic Signal / Transportation** | Traffic-light controllers, rail-signaling systems, surveillance |
| **Office Building** | HVAC, elevators, access control, fire safety |

At the center of all of these, the same core OT components recur: **DCS, SCADA, RTU, PLC** — covered in detail below.

---

## Industrial Network vs. Business Network

An OT network generally consists of a collection of automated control systems networked together to achieve a shared industrial objective. It's typically organized into two logically separate networks that need controlled, monitored interconnection:

- **Industrial Network** — the network of automated control systems and devices (SCADA, DCS, PLC, RTU, sensors) directly involved in running the physical process.
- **Business Network** — the corporate IT network used for enterprise applications, email, ERP, and other business functions.

### Industrial Protocols

Most OT systems use proprietary protocols (Modbus, OPC, CIP, SRTP, and others) or non-proprietary protocols. Protocols are generally selected based on the specific application, and can also be adapted for communication over standard Ethernet and Internet Protocol (IP) when systems require it.

### Network Perimeter / Electronic Security Perimeter (ESP)

The network perimeter is the outermost boundary of assets, acting as a logical or physical division between the interior of a security zone and the outside world. Cybersecurity controls act as the boundary between secure and insecure areas of the network.

### Critical Infrastructure

Critical infrastructure refers to a collection of physical and logical systems and assets whose failure or destruction would severely impact public health, safety, and the economy.

---

## Introduction to ICS

An **Industrial Control System (ICS)** is an essential part of every industrial and critical infrastructure facility. A typical ICS represents the various control systems that support all segments of industrial process handling, distribution, and automation — from manufacturing lines to utility grids.

The control task performed by an ICS is primarily focused on the **output**. Control of the output is defined by the system's process loop, which is configured in one of three modes:

- **Open Loop** — output has no effect on the input required to achieve the desired result.
- **Closed Loop** — output does have an effect on the input, in order to maintain the desired objective (a feedback loop).
- **Manual Loop** — the system is entirely under human control.

---

## Essential ICS Terminology

| Term | Definition |
|---|---|
| **Assets** | The different components of an ICS environment — sensors, actuators, network devices, PLCs, and ICS workstations. Most components are represented graphically to display process flow, program logic, and process parameters. |
| **Zones and Conduits** | A network-segmentation technique used to isolate networks and assets. A **zone** groups assets that share common security requirements; a **conduit** is the pathway through which traffic is allowed to flow between zones, enabling controlled and monitored cross-zone traffic. |

---

## Open, Closed, and Manual Control Loops

### Open Loop
The controller output has no effect on the acquired input required to achieve compliance with the desired specification. In an open-loop system, generally the tools include closed loops, HMIs, and the remote-management and diagnostics component. The remote-management and diagnostics component monitors and reports the ICS system's status back to a central hub for effective coordination between the distributed ICS systems.

### Closed Loop
The output has an effect on the input to maintain the desired objective. A classic closed-loop diagram:

```
   Set Point            Error                 Final                Process
      │                    │                Control Element         Variable
      ▼                    ▼                      │                    │
   ┌──────┐   Error    ┌────────────┐             ▼             ┌──────────┐
   │  ──  │──────────► │ Controller │───────► [Control Valve] ──►│  Process │
   └──────┘            └────────────┘                            │  (Temp   │
      ▲                                                            │  flow)  │
      │                                                            └────┬─────┘
      │              ┌───────────────┐                                 │
      └──────────────│  Transmitter   │◄───── Primary Element ◄────────┘
       Process Variable└───────────────┘        (Transducer)
```

*(Illustrated in the module as Figure 18.77 — "BPCS architecture".)*

### Manual Loop
The system is completely under human control — the controller (control room, HMI operator) is primarily responsible for maintaining compliance with the desired specifications. Generally, ICS control systems include control loops, HMIs, and the remote-diagnostics/maintenance tooling used to keep the distributed systems' terminology and configuration synchronized.

---

## Components of an ICS

```
                     ┌─────────────────────────────┐
                     │  Industrial Control System    │
                     │           (ICS)               │
                     └──────────────┬────────────────┘
                                    │
     ┌───────────────┬─────────────┼─────────────┬───────────────┐
     ▼                ▼             ▼             ▼               ▼
   SCADA             DCS          BPCS           SIS            (HMI / RTU / PLC / IED
(Supervisory     (Distributed  (Basic Process (Safety           embedded throughout)
Control & Data    Control       Control        Instrumented
Acquisition)      System)       System)        System)
```

*(Figure 18.72 — "Components of an ICS".)*

### Distributed Control System (DCS)

A DCS is used to control production systems within the same geographic location. Such systems are used for large, complex process plants — refineries, chemical/nuclear plants, pulp/paper plants, and other automated manufacturing sites — where a centralized supervisory control loop coordinates a group of localized controllers distributed throughout the plant, each handling part of the overall production process.

A DCS achieves the process control by using various feedback and feedforward control loops. Operators using a graphical HMI can monitor and control the entire process, from a central location, in real time.

**DCS Architecture:** A **Main Supervisory Control Server** coordinates several **Redundancy Servers** (for fault tolerance), each managing separate **Process** segments — each with its own PLC/RTU, temperature/pressure sensors, and actuators/valves feeding back into an HMI-equipped control room.

### Supervisory Control and Data Acquisition (SCADA)

A SCADA system is a centralized supervisory control system used for monitoring industrial facilities/infrastructure at scale — measuring trends in real time and detecting/correcting deviations from process norms. SCADA is used across a wide geographical area for critical processes: oil/gas pipelines, water/wastewater treatment, power grid transmission, and public transportation systems.

SCADA architecture consists of hardware (sensors, cables, telephone lines, radios) and communication devices, along with an array of field devices consisting of PLCs and other pieces of automated industrial equipment. SCADA software is typically split into two layers:

- The **field devices** collect and transmit data to a control room.
- The **SCADA MTU (Master Terminal Unit)** communicates the field data back to the operator, in a graphical/tabular format, and enables the operator to remotely monitor and control the system in real time.

Devices connected to a SCADA network — including cameras, radios, telephone lines, sensors, and PLCs/RTUs — are typically field-controlled either through direct control by the operator or by the control server/HMI. Notably, **SCADA systems are fault-tolerant systems with redundant components**, meaning a component failure may not necessarily be visible from outside the system — which can complicate detecting a live compromise.

### Programmable Logic Controller (PLC)

A PLC is a real-time digital computer used for industrial automation. PLCs are considered more than capable computers in industrial control systems due to their extraordinary feature-set: ease of programming, execution of programming logic, ease of hardware use, timers/counters, and reliable control capabilities. They are built to survive severe industrial environments.

**PLC Architecture** consists of three main modules:

1. **CPU Module** — The CPU comprises a central processor and its supporting memory component. The processor is responsible for receiving the required input, performing the required computations, and producing outputs to control connected devices. Program memory typically consists of RAM and ROM memories: RAM stores user-written programs, schemas, drivers, and system data; ROM typically stores boot firmware. Application programs are generally stored in non-volatile memory to survive a power cycle, since PLCs don't usually run a keyboard/monitor and reprogramming the processor whenever power fails would be operationally infeasible.
2. **Power Supply Module** — Supplies the necessary voltage required for PLC modules. Depending on the model, this is essentially the AC-to-DC conversion circuitry that lets a plant run PLCs off a standard 24V or 5V DC bus.
3. **I/O Modules** — The input and output modules connect the sensors and actuators of the target system for sensing and producing real-time value inputs/outputs. Three types:
   - **Digital I/O Module** — used for switching devices ON/OFF, in nature digital (on/off relays and switches). These modules handle multiple digital inputs and outputs and support both AC and DC voltages.
   - **Analog I/O Module** — used for sensors and actuators that provide analog electric signals. This module includes analog-to-digital converters for input data, and digital-to-analog converters for output signals — this module processes analog data.
   - **Communication I/O Module** — used for exchanging information between a communication network and a CPU located at a remote location.

### Basic Process Control System (BPCS)

The main purpose of a PLC is to make machinery and systems work automatically without human intervention — therefore, a PLC is very important, as it's responsible for the growth of all manufacturing, production, etc.

A **BPCS** is responsible for performing process control and monitoring for industrial infrastructure. It's a system that responds to input signals from processes and associated equipment operated by other devices to generate output signals that allow the associated equipment to operate in a desired, appropriately-adjusted manner. BPCS systems are dynamic in nature and are highly adaptable to changing production conditions.

BPCS is applicable to all sorts of control systems, including the temperature, pressure, flow, feedback, and feedforward control loops used in industries such as chemical, oil and gas, and food and beverage.

The use of BPCS is crucial in industrial automation as they act as the first layer of protection against any unsafe or hazardous condition to the desired performance of any industrial infrastructure. BPCS systems are often used to push the performance limits to attain the desired performance. However, they can also make lack diagnostic capabilities in terms of security, as they lack diagnostic components related to security, so they may need coordination alongside dedicated safety systems for security-related failures. However, when a BPCS makes a manual intervention required to attain the desired plant operation quality, it can complement other layers of protection.

Some of the important functions BPCS offers:

- Offers trending and alarm/event-logging facilities
- Provides an interface from which an operator can monitor and control a system using an operator console (HMI)
- Controls the processes that in turn optimize the plant operation to enhance the quality of the product
- Generates production data reports
- Manages the sequencing, timing, and coordination of various process steps running in batches, ensuring consistent quality and efficiency

---

## Safety Instrumented Systems (SIS)

A **Safety Instrumented System (SIS)** is an automated control system designed to safeguard the manufacturing process in case of any hazardous incident in industry. It monitors and performs "specific control functions" to shut down the monitored system or bring it to a predefined safe state to reduce the adverse impacts of an incident.

SIS functions independently of other control systems to prevent operation exceeding pre-established boundaries of the critical process from reaching an unsafe operating condition. Typical examples of SIS practices include fire and gas systems, emergency shutdown systems, safety shutdown systems, etc.

SIS includes critical safety interlocks or features that prevent the operation of certain equipment under unsafe personnel/environment conditions, thereby protecting both the equipment and personnel.

SIS also handles the storage and retrieval of recipes — including formulas, process steps, and production parameters — for easy replication of batch processes.

The functional requirements of the work performed by a SIS should also be determined from Hazard and Operability Studies (HAZOP), Layers of Protection Analysis (LOPA), risk graphs, etc. SIS functionality works independently from other control systems. It consists of sensors, logic solvers, and final control elements that maintain safe operation of the process by following the functions:

- **Field sensors** — collect information to determine and measure process parameters such as temperature, pressure, flow rate, etc. Different types of sensors are available, such as pneumatic, electric switches, smart transmitters, etc.
- **Logic solvers** — helpful in deciding the necessary action to be taken based on the gathered information they provide. Logic solvers provide actions for both fail-safe and fault-tolerant situations to avoid incidents.
- **Final control elements** — implement the actions determined by the logic controller by bringing the system to an activated off/on state; these generally comprise process-activated shutoff valves controlled by the SIS.

As no component in a system can be completely immune to failure, it's essential to conduct security testing of the SIS to determine how it should be integrated into the smooth operation of a plant's cybersecurity environment. The main aim of assessing the workings of the SIS is to guarantee safety and integrity of the SIS so that it remains at its actual design levels.

**Layers of protection provided by SIS systems** (outermost/latest response to innermost/first response):

```
Community Emergency Response  ← Mitigation
Plant Emergency Response      ← Mitigation
Physical Protection           ← Prevention
Post-Release Protection       ← Prevention
Safety Instrumented System    ← Prevention
Critical Alarms + Operator    ← Prevention
Supervision                   ← Prevention
Basic Controls, Process       ← Prevention
Alarms, and Supervision
Process Design                ← Prevention
```

**SIS architecture** flows: **Sensor → Logic Solver → Final Control Element** — a sensor detects an abnormal condition, the logic solver evaluates it against configured thresholds, and the final control element (e.g., a shutoff valve) is triggered to bring the process to a safe state.

---

## IT/OT Convergence (IIoT)

**IT/OT convergence** is the integration of information technology (IT) computing/networking systems with operational technology (OT) systems used to monitor events, processes, and devices, and to make adjustments in enterprise and industrial operations. Historically OT teams and IT teams operated fully independently, using different technologies, terminologies, and safeguarding methods; convergence requires both teams to co-operate with each other to improve security, efficiency, quality, and productivity.

Benefits of merging IT with OT (i.e., **IIoT**, the Industrial Internet of Things):

- **Enhancing Decision Making** — decisions can be enhanced by integrating OT data into business intelligence tooling.
- **Enhancing Automation** — business flow and industrial control operations can improve automation and interoperability once systems are integrated.
- **Expedite Business Output** — the pay-off between OT and IT teams can organize technological and operational overheads to accelerate business output.
- **Minimizing Expenses** — merging these two systems reduces overall operational costs, since teams and infrastructure are no longer duplicated, improving reliability and reducing well-siloed spending.
- **Increased Agility** — integrated systems with unified conditions/operations are more responsive to change, since dependencies across conditions/operations are digitally applied rapidly, in a unified way.
- **Predictive Maintenance** — IT systems can pull data from OT to predict equipment failures before they happen, reducing downtime and helping schedule maintenance appropriately.
- **Better Quality Control** — integrating IT systems with OT processes allows more rigorous monitoring and control of quality standards across production lines, leading to higher product quality and consistency.
- **Compliance and Reporting** — IT/OT convergence simplifies compliance with regulatory requirements by providing tools for improved data collection, analysis, and reporting.
- **Scalability** — Unified IT and OT systems are easier to scale up or down based on business needs, supporting growth and adaptation without the need for extensive infrastructure changes.

---

## The Purdue Model

The **Purdue Model** (formally, the Purdue Enterprise Reference Architecture — PERA) is a widely accepted model that describes the internal connections and dependencies of important components in ICS networks — the "reference map" every OT security professional uses to describe where a device or a threat sits.

The Purdue Model consists of three zones: the **manufacturing zone** (OT), the **enterprise zone** (IT), and a **demilitarized zone (DMZ)** that sits between the OT and IT zones. The intention behind adding this DMZ is to strictly control the interaction between network or system components that are otherwise untrusted.

The three zones are further divided into several operational levels, each associated with a well-described level of the architecture:

```
┌──────────────────────────────────────────┐
│  IT Systems      Level 5   Enterprise Network  │
│  (Enterprise     Level 4   Business Logistics  │
│   Zone)                    Systems              │
├──────────────────────────────────────────┤
│         Industrial Demilitarized Zone (IDMZ)     │
├──────────────────────────────────────────┤
│  OT Systems      Level 3   Operation Systems/    │
│  (Manufacturing              Site Operations     │
│   Zone)          Level 2   Control Systems/      │
│                              Supervisory Controls │
│                  Level 1   Basic Controls/        │
│                              Intelligent Devices  │
│                  Level 0   Physical Process        │
└──────────────────────────────────────────┘
```

*(Figure 18.81 — "Purdue model".)*

| Zone | Level | Description |
|---|---|---|
| **Enterprise Network (IT Systems)** | Level 5 | Enterprise network — corporate IT, business intelligence, general internet connectivity. |
| **Enterprise Network (IT Systems)** | Level 4 | Business logistics systems — ERP, scheduling, business planning tied to plant data. |
| — | *Industrial DMZ* | Buffer zone between IT and OT, brokers data flow, hosts jump servers/historian mirrors. |
| **Manufacturing Zone (OT Systems)** | Level 3 | Operation systems / site operations — plant historian, MES, batch management. |
| **Manufacturing Zone (OT Systems)** | Level 2 | Control systems / supervisory control — SCADA, HMI, engineering workstations. |
| **Manufacturing Zone (OT Systems)** | Level 1 | Basic controls / intelligent devices — PLCs, RTUs, drives (VFDs). |
| **Manufacturing Zone (OT Systems)** | Level 0 | The physical process itself — sensors, actuators, motors, valves. |

**Enterprise systems** (Level 4–5) generally include cloud/internet connectivity, networks, storage, and data-processing infrastructure, plus general PC/Java/Python-class application software.

**OT systems** (Level 0–3) are further divided:

- **Level 3 (Operational Systems/Site Operations)** — All the devices, networks, control, and monitoring systems inside a single plant fall under this zone. It manages the production process for that specific plant floor and integrates level-0-through-2 systems, laboratory information systems (LIMS), historians, servers, supervising systems, email/print clients, etc.
- **Level 2 (Control Systems/Supervisory Controls)** — Supervising, monitoring, and controlling the physical process is carried out at this level. The control systems used are DCSs, SCADA software, Human-Machine Interfaces (HMIs), real-time software, and other real-time control system tooling such as engineering/monitoring workstations and PLC line control.
- **Level 1 (Basic Controls/Intelligent Devices)** — Analysis and alteration of the physical process is done at this level via control outputs — "smart valves," "smart sensors," "move valves," etc. Level-1 devices include Intelligent Electronic Devices (IEDs), PLCs, RTUs, Proportional-Integral-Derivative (PID) controllers, and Variable Frequency Drives (VFDs) — VFDs are used to automate tasks at the plant level, as they modify the frequency and voltage supplied to a motor to control its speed.
- **Level 0 (Physical Process)** — At this level, the actual physical process is defined, and the product is manufactured. Higher levels and their monitoring equipment are located at this level; this layer is referred to as the Equipment Under Control (EUC). Level-0 devices carry out the manufacturing/monitoring of plant operations.

- **Industrial Demilitarized Zone (IDMZ)** — A barrier between the manufacturing zone and enterprise zone that creates a shared network zone where any communication between IT and OT can be inspected before continuing. This is where production is not allowed to continue if the IDMZ itself is compromised. IDMZ hosts include Microsoft domain controllers, database replication servers, and proxy servers.

---

## OT Technologies and Protocols per Purdue Level

Industrial network protocols and zones deployed across the ICS network vary widely by Purdue level. Understanding which protocol lives at which level tells a security assessor immediately what kind of traffic/tooling to expect there.

### Protocols used at Level 4 and 5

| Protocol | Description |
|---|---|
| **DCOM** (Distributed Component Object Model) | Microsoft's proprietary technology enabling software components to communicate directly over a network, reliably and securely. |
| **FTP/SFTP** | File Transfer Protocol establishes a connection for the specific server (or, if encrypted, SFTP), and the identity of the client and server is established beforehand. |
| **GE-SRTP** (Service Request Transport Protocol) | Developed by GE Fanuc/Emerson Automation Platforms, used to transfer data from PLCs to HMIs, RTUs, and various other types of GE PLCs. |
| **IPv4/IPv6** | Foundational networking protocols used for packet-switched networks in devices; IPv6 offers vastly expanded address space over Wi-Fi networks. |
| **OPC UA** (OPC Unified Architecture) | Ensures secure, reliable, and platform-independent communication protocols for the interconnection of data across manufacturing devices and enterprise systems. |
| **TCP/IP** | The suite of communication protocols for interconnecting networking devices on the internet. |
| **SMTP/HTTP/HTTPS** | Standard internet protocols used for email transfer, file transmission, and browsing across a wireless local area network (LAN) or WAN. |
| **Wi-Fi** | The most common Wi-Fi standard used in industrial deployments provides an extended range, and most commonly the 802.11b standard delivers a maximum speed of 600 Mbps and a range of approximately 50 m. |

### Protocols used at Level 3

| Protocol | Description |
|---|---|
| **ISA/IEC 62443** | Provides a flexible framework for addressing and mitigating current and future security vulnerabilities in industrial automation and control systems. |
| **Modbus** | A serial communication protocol used with PLCs — enables communication between many devices connected to the same network. |
| **NTP** (Network Time Protocol) | Used for clock synchronization between computer systems over packet-switched, variable-latency data networks. |
| **Profinet** | A communication protocol used to exchange data between controllers like PLCs and devices like RFID readers. |
| **SuiteLink** | Based on TCP/IP, runs as a service on Windows operating systems — mostly used in industrial applications that value time, quality, and high throughput. |
| **Tase-2** (also IEC 60870-6) | An open communication protocol that enables exchange of time-critical information between control systems through WAN and LAN. |
| **ControlNet** | A real-time control protocol used to collect data from and send instructions to field devices; provides high-speed transmission and is particularly robust in noisy environments. |
| **Profibus PA/DP** | Used to automate tasks at the plant level. Profibus decentralized peripherals (DP) operate sensors and actuators via a central controller; Profibus process automation (PA) monitors measuring equipment through a process control system. |
| **Omron FINS** | Used by PLC programs for transferring data and monitoring other services with remote PC servers via various industrial control ICSs (RS-232 or common TCP/IP ports). |
| **PCWorx** | PCWorx is a proprietary automation protocol that ties many controllers together, so they make automation and factory automation seamless. |
| **Profibus** | More complex than Modbus and is designed for addressing interoperability issues; employed in process automation and factory automation fields. |
| **Sercos III** | The serial real-time communication system (Sercos II) is compliant with an interface appropriate for use in industrial machines, and is used in complex motion-control applications with high-specification demands. |
| **S7 Communication** | S7 Communication is a Siemens proprietary protocol between programmable logic controllers (PLCs) of the Siemens S7-300/400 family, used in PLC programming and for accessing PLC data from SCADA. |
| **WiMax** | Worldwide interoperability for microwave access (WiMax) is a wireless metropolitan-area networking standard; it operates at frequencies between 2.5 GHz and 5.8 GHz with a transfer range of up to 40 miles. |
| **FOUNDATION Fieldbus** | This network protocol is used for building automation control systems. It's a particularly common protocol in digital communication infrastructure that links field instruments such as actuators and sensors to control systems. |
| **Remote-management protocols** | Industrial sites use remote-management protocols such as RDP, VNC, and SSH. Once the attacker compromises and gains access to the OT network, they can perform further exploitation to understand and manipulate the configuration and working of the equipment. |

### Protocols used at Level 2 and 0/1

| Protocol | Description |
|---|---|
| **6LoWPAN** | IPv6 over Low-Power Wireless Personal Area Networks — a communication protocol used between smaller and lower-power devices with limited processing capacity, mainly for home and building automation. |
| **DNP3** (Distributed Network Protocol 3) | A communication protocol used to interconnect components within process automation systems — very common in electric/water utility SCADA. |
| **DNS/DNSSEC** | Domain Name System Security Extensions provide a way to authenticate DNS response data and secure information provided by DNS. |
| **FTE** (Fault Tolerant Ethernet) | Designed to provide rapid network redundancy — each node is connected twice to a single LAN through dual network interfaces. |
| **HART-IP** | Used to integrate WirelessHART gateways and HART multiplexers tightly and efficiently for sending and receiving digital information. |
| **IEC 60870-5-101/104** | An extension of the IEC 101 protocol with modifications in transport, network, link, and physical layer services; enables communication between the control station and substation over standard TCP/IP. |
| **SOAP** (Simple Object Access Protocol) | A messaging protocol containing a strict set of rules that administrates data transfer between client and server using XML message format. |
| **DeviceNet** | Used to connect simple industrial devices such as sensors and actuators with higher-level devices such as PLCs; runs on Controller Area Network (CAN) technology. |
| **AS-Interface (AS-i)** | A simple, cost-effective network designed to connect binary devices such as actuators and sensors in automation applications. |
| **BACnet** (Building Automation and Control network) | A data communication protocol designed for building automation and control networks — implements ASHRAE, ANSI, and ISO 16484-5 standards. |
| **EtherCAT** | Ethernet for Control Automation Technology — an Ethernet-based fieldbus system suited for both hard and soft real-time computing needs in automation. |
| **CANopen** | A high-level communication protocol based on the CAN (Controller Area Network) protocol — used for embedded networking applications like vehicle networks. |
| **Crimson** | The common programming platform used for various Red Lion products, such as G3 and G3 Kadet series HMIs, Data Station Plus, Modular Controller, and the Productivity Station. |
| **DeviceNet (CIP variant)** | Another variant of the Common Industrial Protocol (CIP) used in automation to interconnect control devices to exchange data. |
| **Zigbee** | A short-range communication protocol based on the IEEE 203.15.4 standard, used for devices that transfer data intermittently at a low data rate within a restricted area (10–100 m). |
| **ISA SP100** | A committee establishing the industrial wireless standard ISA100 — used for the industrial manufacturing environment and process automation industry. |
| **MELSEC-Q** | Provides an open, seamless network environment integrating different levels of automation networks such as CC-Link IE, high-speed, and large-capacity ethernet-based integrated open networks. |
| **Niagara Fox** | A building-automation protocol used between Niagara software systems developed by Tridium. |

---

**Previous:** [06 — IoT Countermeasures and Security](06-iot-countermeasures-and-security.md)
**Next:** [08 — OT Attacks and Threats](08-ot-attacks-and-threats.md)
