# 01 — IoT Concepts and Architecture

> Learning Objective 1 of Module 18: *Explain IoT Concepts and Attacks* (concepts half).

## Table of Contents

- [What is IoT?](#what-is-iot)
- [How IoT Works](#how-iot-works)
- [IoT Architecture](#iot-architecture)
- [IoT Application Areas and Devices](#iot-application-areas-and-devices)
- [IoT Technologies and Protocols](#iot-technologies-and-protocols)
- [IoT Communication Models](#iot-communication-models)
- [IoT Operating Systems](#iot-operating-systems)
- [Challenges of IoT](#challenges-of-iot)
- [Threat vs. Opportunity](#threat-vs-opportunity)

---

## What is IoT?

The **Internet of Things (IoT)** — also called the *Internet of Everything (IoE)* — is the network of physical objects ("things") that are embedded with sensors, software, and network connectivity, allowing them to collect and exchange data with each other and with centralized systems over the internet, largely without direct human intervention.

Four primary technology building blocks make an IoT deployment work:

1. **Sensing Technology** — Sensors embedded in the device that sense changes in the surrounding environment: temperature, location, vibration, moisture, ambient light, or a patient's vital signs. This is the "eyes and ears" layer of any IoT system.
2. **IoT Gateways** — Bridge devices that sit between low-power IoT endpoints (which usually can't speak IP directly, or speak it inefficiently) and the wider internet/cloud. The gateway aggregates traffic from many sensors, may do protocol translation (e.g., Zigbee → IP), and forwards data upstream.
3. **Cloud Server / Data Storage** — Once data leaves the gateway it is transmitted (usually over the internet) to a cloud backend where it's processed, stored, and made available for analytics or triggering further automated actions.
4. **Remote Control via Mobile App** — The end-user's interface. A mobile or web app talks to the cloud API, letting the user monitor sensor data and issue control, configuration, or data-request commands back down to the physical device.

### Illustrative end-to-end flow

A worked example that ties the four pieces together — a smart home security setup:

1. A smart security system is installed in a home and connected to the internet via the home's Wi-Fi/router (the home's internet gateway).
2. The system's sensors continuously collect information about the home's environment (motion, door/window state, camera feed) and send it, via the internet connection, to a cloud server.
3. Data stored in the cloud includes the device's ID and the timestamps/values of everything the sensors have reported.
4. From a mobile phone anywhere in the world, the user opens the companion app, which authenticates to the cloud with the device's credentials and pulls the latest state, or pushes a new command (e.g., "arm the alarm").
5. The cloud validates the request; if the credentials/session are invalid the request is rejected and (ideally) an alert is generated. If valid, the command is relayed back down to the device over its established connection.

This "sensor → gateway → cloud → app" pattern recurs throughout almost every IoT product, and it's the pattern attackers target at every hop (see [02 — IoT Attack Surface and Vulnerabilities](02-iot-attack-surface-and-vulnerabilities.md)).

---

## How IoT Works

At a mechanical level, IoT devices work through this repeating loop:

1. A sensor sensing an environmental change (temperature, motion, pressure, etc.)
2. The reading is converted into a digital signal
3. That signal is sent — usually over a low-power radio protocol — to a local gateway or hub
4. The gateway forwards the reading to the cloud, often over Wi-Fi, Ethernet, or cellular
5. Cloud-side software collects, logs, and (optionally) analyzes the reading, and can trigger automated actions or notify the end-user
6. The end-user or an automated rule sends a control command back down through the same chain

---

## IoT Architecture

IoT reference architectures are typically described as a 4- or 5-layer stack. From the bottom (closest to physical hardware) to the top (closest to the human user):

| Layer | Description |
|---|---|
| **Edge Technology Layer** | The lowest layer — the actual hardware: sensors, RFID tags, readers, and other endpoint devices that gather raw data from the physical world. |
| **Access Gateway Layer** | The first point where message routing, publish-subscribe handling, and initial data processing occurs. This is the bridge from constrained device protocols to standard networking. |
| **Internet Layer** | The critical layer that allows communication between endpoints, whether device-to-device, device-to-cloud, or device-to-gateway, and back-end data sharing. |
| **Middleware Layer** | Sits between the application layer and the hardware layer. It handles device management, data filtering, data aggregation, and provides an abstraction so applications don't need to know the specifics of every underlying device. |
| **Application Layer** | The top of the stack — delivers services and interfaces to the end-user: building/home automation dashboards, industrial monitoring consoles, healthcare portals, and so on. |

```
┌─────────────────────────────┐
│      Application Layer       │  ← dashboards, apps, industry-specific services
├─────────────────────────────┤
│      Middleware Layer         │  ← device management, information management
├─────────────────────────────┤
│      Internet Layer           │  ← connection between endpoints
├─────────────────────────────┤
│      Access Gateway Layer     │  ← protocol translation and messaging
├─────────────────────────────┤
│      Edge Technology Layer    │  ← sensors, RFID tags, readers, endpoint devices
└─────────────────────────────┘
```

---

## IoT Application Areas and Devices

IoT devices show up across almost every industry vertical. The table below (adapted from the module's device/sector breakdown) is a useful map when you're scoping an assessment — it tells you what kind of devices to expect in a given environment:

| Service Sector | Application Group | Example Locations | Example Devices |
|---|---|---|---|
| **Buildings** | Commercial/Institutional | Offices, education, retail, hospitality, healthcare, airports, stadiums | Heating/ventilation/AC (HVAC), transport, fire and safety, lighting, security, access |
| **Buildings** | Industrial | Process, clean room, campus | Process, clean room, and campus control systems |
| **Energy** | Supply/Demand | Power generation, transport, distribution, low voltage, power quality, energy management | Turbines, windmills, UPS, batteries, generators, meters, drills, fuel cells |
| **Energy** | Alternative | Solar, wind, co-generation, electrochemical | Solar and wind generation equipment |
| **Energy** | Oil/Gas | Rigs, derricks, heads, pumps, pipelines | Field monitoring & control equipment |
| **Consumer & Home** | Infrastructure | Wiring, network access, energy management | Digital cameras, power systems, MID e-readers, dishwashers, desktop computers, washing machines |
| **Consumer & Home** | Awareness/Safety | Security/alerts, fire safety, elderly/children monitoring | MRI machines, PDAs, implants, surgical equipment, telemedicine devices |
| **Consumer & Home** | Convenience/Entertainment | HVAC/climate, lighting, appliances, gaming | Consoles, alarms, TVs, MP3 players |
| **Healthcare & Life Science** | Care | Hospital, ER, mobile, POC clinic, labs, doctors' offices | Implants, surgical equipment, monitors, telemedicine |
| **Healthcare & Life Science** | In Vivo/Home | Implants, home monitoring systems | MRI machines, PDAs, home monitors |
| **Healthcare & Life Science** | Research | Drug discovery, diagnostics, labs | Research and diagnostic equipment |
| **Transportation** | Non-vehicular | Air, rail, marine | Vehicle-control/rail-signaling systems |
| **Transportation** | Vehicles | Commercial, construction, off-highway | Vehicle lights, signage, tolls |
| **Transportation** | Transport systems | Tolls, traffic management, navigation | Traffic-light and navigation systems |
| **Industrial** | Resource Automation | Mining, irrigation, agricultural, woodland | Pumps, valves, VATs, conveyors, fabrication, assembly, vessels/tanks |
| **Industrial** | Fluid/Process Industries | Petrochemicals, hydro/carbons, food/beverage | Assembly/packaging/warehousing |
| **Industrial** | Converting/Discrete | Metals, paper, rubber/plastic, metalworking, electronics, assembly/test | — |
| **Industrial** | Distribution | Pipelines, conveyance | — |
| **Retail** | Specialty | Fuel stations, gaming, casinos, discos, special events | POS terminals, tags, cash registers, vending machines |
| **Retail** | Hospitality | Hotels/restaurants, bars, clubs | POS terminals, cash registers |
| **Retail** | Stores | Supermarkets, shopping centers, single site, distribution centers | POS terminals |
| **Security/Public Safety** | Surveillance | Radar/satellite, environment, military security, unmanned devices | Weapons, vehicles, ships, aircraft, radar/satellite gear |
| **Security/Public Safety** | Equipment | Weapons, vehicles, ships, aircraft gear | — |
| **Security/Public Safety** | Tracking | Humans, animals, postal, food, health, baggage | Tanks, fighter jets, battlefields, jeeps, cars, ambulances |
| **Security/Public Safety** | Public Infrastructure | Water, treatment, building, environment, equipment, personnel/police/fire/regulatory | Ambulance, police, fire, homeland security |
| **Security/Public Safety** | Emergency Services | Ambulance, police, fire, homeland security | — |
| **IT & Networks** | Public | Services, e-commerce, data centers, mobile carriers, ISPs | Servers, storage, PCs, routers, switches, PBX systems |
| **IT & Networks** | Private | IT/data center office, privacy nets | Servers, storage, routers, switches, PBX systems |

*(Table 18.1 in the source courseware — reproduced here in condensed form for reference.)*

---

## IoT Technologies and Protocols

IoT relies on an unusually wide range of network technologies because "one radio for everything" doesn't work when some devices need to run for years on a coin-cell battery and others need to move video in real time. The module breaks the landscape into short/medium/long-range wireless, plus wired protocols.

### Short-range Wireless Communication

| Protocol | Notes |
|---|---|
| **Bluetooth Low Energy (BLE)** | A power-efficient variant of Bluetooth designed for periodic small data transfers — used heavily in wearables, security, and entertainment devices. |
| **Light-Fidelity (Li-Fi)** | Uses visible light (in the 224–800 THz spectrum) as the communication medium instead of RF. Bi-directional, high-speed. Common household LED bulbs can be adapted to carry Li-Fi data. |
| **Near-Field Communication (NFC)** | Very short-range (centimeters) magnetic-field-based communication between two electronics. Used for contactless payment, social networking, and document identification. |

### Medium-range Wireless Communication

| Protocol | Notes |
|---|---|
| **HaLow (802.11ah)** | A variant of the Wi-Fi standard purpose-built for IoT — extended range, lower data rates, and reduced power consumption compared to classic Wi-Fi. |
| **LTE-Advanced** | A mobile communication standard that boosts coverage, cell-edge performance, and capacity over standard LTE — used where IoT devices need wide-area cellular connectivity. |
| **6LoWPAN** (IPv6 over Low-power WPAN) | Lets low-power devices (e.g., 802.15.4 radios) speak IPv6 directly, so IoT sensor networks can be internet-routable. |

### Long-range Wireless Communication

| Protocol | Notes |
|---|---|
| **LPWAN** (Low-Power Wide-Area Network) | An umbrella category of protocols for long-range, low-power, low-bandwidth communication over telemetry networks. LoRaWAN and Sigfox are the two most common implementations. |
| **LoRaWAN** | A Long Range WAN protocol used for machine-to-machine and industrial IoT communication over long distances at low power. |
| **Sigfox** | A subscription network that uses narrow-band signaling to deliver low-power, long-range coverage — good for tiny, infrequent payloads. |
| **NB-IoT** (Narrowband-IoT) | A 3GPP-standardized LPWAN variant that operates over cellular spectrum, offering deep indoor penetration and long device battery life. |
| **Neul** | Uses "white-space" spectrum (unused TV broadcast frequencies) to deliver low-cost, high-coverage, low-power connectivity. |
| **VSAT** (Very Small Aperture Terminal) | A satellite-based communication protocol used for connectivity in remote areas without landline/cellular coverage. |
| **Cellular** (2G/3G/4G/5G) | Widely available, higher power consumption, but the only option in areas without other IoT-specific infrastructure. |
| **MQTT** (Message Queuing Telemetry Transport) | A lightweight publish/subscribe protocol used to send small, frequent telemetry messages over constrained or high-latency links. |
| **QUIC** | Multiplexes several UDP connections between two endpoints — functionally comparable to TCP/TLS but with lower connection-setup latency. |

### Wired Communication

| Protocol | Notes |
|---|---|
| **Ethernet** | The most widely deployed wired LAN protocol; used to physically wire together IoT gear inside a building. |
| **MoCA** (Multimedia over Coax Alliance) | Repurposes existing in-home coaxial cable to deliver network connectivity, avoiding new cable runs. |
| **Power-Line Communication (PLC)** | Piggybacks data onto existing electrical wiring — data and power share the same physical line, useful in automation and broadband-over-powerline scenarios. |

### IoT Application-layer Protocols

- **CoAP** (Constrained Application Protocol) — a lightweight, RESTful web-transfer protocol purpose-built for constrained M2M devices and networks.
- **Edge** — computing performed at, or very close to, the device generating the data, reducing round-trip latency to the cloud, improving caching, and reducing bandwidth.
- **UDP** — the low-overhead transport most of the above application protocols run over, since retransmission/ordering guarantees of TCP are often unnecessary or too costly for constrained links.

---

## IoT Communication Models

There are four canonical ways IoT devices are architected to talk to each other and to the outside world:

### 1. Device-to-Device

Two or more devices connect and communicate directly with each other rather than through an intermediary application server — e.g., a light bulb and a light switch made by different manufacturers, communicating over Bluetooth, Z-Wave, or Zigbee. Because there's no cloud broker in the loop, this model is fast and works offline, but it also means authentication and encryption are entirely up to the device firmware.

### 2. Device-to-Cloud

The device communicates directly with an internet cloud service to exchange data and control messages, bypassing any local hub. This is the most common pattern for consumer IoT (e.g., a smart thermostat talking straight to the manufacturer's cloud API).

### 3. Device-to-Gateway

An intermediary gateway device sits between the endpoint and the cloud application service provider (ASP). The gateway may run local software that provides security, protocol/data translation, or additional functionality before relaying data onward. Two illustrative examples:

- A **temperature sensor** paired to a **wireless network** connects through the gateway (over Bluetooth/Z-Wave/Zigbee) to the ASP over HTTP/TLS/DTLS/UDP/TCP/IP.
- A **carbon-monoxide sensor**, similarly, connects to a **local gateway** over Bluetooth/IEEE 802.11 (Wi-Fi)/IEEE 802.15.4 (LR-WPAN), and the gateway then talks to the cloud over CoAP, DTLS, UDP, IPv4/IPv6.

If a smartphone app is the "gateway" (e.g., using the phone as a Bluetooth-to-internet bridge for a fitness tracker), the same model applies — the phone runs a local app that pairs with the device and forwards data to the cloud over its own mobile-data or Wi-Fi connection.

### 4. Back-End Data-Sharing

This model extends the device-to-cloud model by allowing the data collected from a single device to be accessed and analyzed by multiple third parties simultaneously, rather than a single closed application server. The protocol stack typically layers CoAP/HTTP on top of an authentication mechanism (e.g., OAuth 2.0), letting data flow out to Application Service Provider #1, #2, #3, etc.

```
      Light Sensor
           │
    (CoAP or HTTP)
           │
           ▼
   Application Service Provider #1  ──OAuth 2.0──►  Application Service Provider #2
                                                              │
                                                              ▼
                                              Application Service Provider #3
```

---

## IoT Operating Systems

IoT hardware ranges from 8-bit microcontrollers with kilobytes of RAM to Raspberry-Pi-class SBCs, and the OS choice reflects that range:

| OS | Notes |
|---|---|
| **Windows 10 IoT** | Microsoft's family of OSes purpose-built for embedded devices. |
| **Amazon FreeRTOS** | An open-source, real-time OS for microcontrollers that makes low-power, battery-operated edge devices easy to secure, deploy, connect, and manage. |
| **Fuchsia** | Google's open-source, non-Linux-kernel OS designed for a range of devices from embedded to full computers. |
| **RIOT** | A free, open-source OS designed for low-power IoT devices — supports IPv6/6LoWPAN natively. |
| **Ubuntu Core** | A lightweight, containerized version of Ubuntu built for IoT gateways, robots, and edge devices. |
| **ARM Mbed OS** | Mostly used in low-power IoT devices that require Bluetooth connectivity. |
| **Zephyr** | A scalable RTOS supporting multiple hardware architectures, optimized for resource-constrained devices, built for security. |
| **Embedded Linux** | A stripped-down Linux build supporting the small memory/storage footprint of embedded devices. |
| **NuttX RTOS** | A real-time OS emphasizing standards compliance and small size, deployable on 8-bit and 32-bit microcontrollers. |
| **Integrity RTOS** | A commercial RTOS aimed at aerospace, defense, industrial, and automotive environments. |
| **Apache Mynewt** | An open-source RTOS supporting Bluetooth Low Energy from the kernel up. |
| **Tizen** | A Linux-based OS designed for a wide range of device classes: smartphones, wearables, TVs, and more. |

---

## Challenges of IoT

The module lists these recurring headaches that keep IoT security immature relative to traditional IT:

- **Lack of security and privacy** — most IoT devices ship with weak, inconsistent, or absent security policies because there's no industry-wide baseline.
- **Vulnerable web interfaces** — many devices expose a local or cloud-hosted web UI that inherits web-app vulnerability classes on top of embedded-device constraints.
- **Legal, regulatory, and rights issues** — regulation hasn't kept up with the rate of IoT deployment, so devices routinely ship with no legal requirement to patch or disclose vulnerabilities.
- **Default, weak, and hardcoded credentials** — cheap devices frequently ship with a fixed admin password baked into the firmware image itself.
- **Clear-text protocols and unnecessary open ports** — many devices leave debug/management services (Telnet, unauthenticated HTTP) exposed by default.
- **Coding errors (buffer overflow)** — resource-constrained firmware is often written in C without modern memory-safety mitigations, so classic memory-corruption bugs are common.
- **Storage issues** — the storage capacity on the device usually can't keep up with the volume of data collected and transmitted, leading to log truncation, weak retention, and lost forensic evidence.
- **Difficult-to-update firmware and OS** — it may be impractical (or the vendor never built in the capability) to push a security patch remotely; developers and manufacturers may refuse to fix vulnerabilities once a product line is out of active support.
- **Interoperability standards issue** — the sheer variety of vendors, protocols, and integration methods makes broad security testing labor-intensive.
- **Physical theft/tampering** — many IoT devices are physically accessible to attackers (a smart lock on the outside of a door, a parking sensor in the street), which enables hardware-level attacks that a server in a data center never has to worry about.
- **Lack of vendor support for fixing vulnerabilities** — firmware for legacy or budget-oriented devices is often abandoned quickly, before all vulnerabilities are patched.
- **Emerging economy and development issues** — every new market entrant reinvents insecure defaults rather than adopting hardened, vetted designs.
- **Handling of unstructured data** — the sheer volume and variety of connected-device data increases the difficulty of understanding and acting on it consistently.

---

## Threat vs. Opportunity

If a device or environment is **Misconfigured**, **Misapprehended** (poorly understood by its operators), and **Unprotected**, it should be treated by a defender as **Uncontrolled**, **Uncontained**, and **Unmonitored** — a live threat. The three biggest categories of threat this creates for organizations:

1. **Data, privacy, and safety** — an unprotected IoT device can leak personal, health, financial, or safety-critical information.
2. **Communications** — attackers can intercept, replace, or disrupt device-to-device or device-to-cloud channels.
3. **Delivery of services and standard of living** — because IoT increasingly underpins critical services (utilities, healthcare, transport), a compromise cascades into real-world service disruption.

### IoT Security Problems by Architecture Layer

| Layer | Security Issue |
|---|---|
| **Application** | Validation of the reported code, insufficient auditing, weak default passwords |
| **Network** | Firewall misconfiguration, insecure communication encryption, services, lack of automatic updates |
| **Mobile** | Insecure APIs, lack of communication-channel encryption, lack of storage-security interface |
| **Cloud** | Improper authentication, no encryption for storage/communications, insecure web interface |

> **IoT = Application + Network + Mobile + Cloud** — every one of these four layers must be independently hardened, because a compromise anywhere in the chain compromises the whole device.

---

**Next:** [02 — IoT Attack Surface and Vulnerabilities](02-iot-attack-surface-and-vulnerabilities.md)
