# 02 — Botnets and the Cybercrime Ecosystem

> Exam objective: *Summarize DoS/DDoS concepts* (botnets subset) & *Demonstrate different
> DoS/DDoS attack techniques* (propagation subset)

## 2.1 What Is a Botnet?

The term **"bot"** is a contraction of **"robot"** — software applications that run automated
tasks over the Internet. A **botnet** ("roBOT NETwork") is a group of computers infected by bots;
while bots can be used for benign purposes (web spidering, data collection), as a hacking tool a
botnet is a huge network of compromised systems the attacker can command at will. Even a
relatively small botnet of **1,000 bots** can have combined bandwidth larger than that of most
corporate networks.

Common bot families used for benign purposes include **Internet bots**, **IRC bots**, and
**chatter bots** — well-known IRC bots include Cardinal, Sopel, Eggdrop, and EnergyMech. The
*malicious* repurposing of the same underlying bot concept is what powers the modern DDoS
economy.

## 2.2 What Attackers Use Botnets For

Botnets form the core of the cybercriminal activity center, linking and uniting the various parts
of the cybercriminal world. Beyond DDoS, attackers use botnets to:

| Use | How it works |
|---|---|
| **DDoS attacks** | Consume the victim's bandwidth and overload the system, destroying network connectivity |
| **Spamming** | Attackers use a SOCKS proxy for spamming after harvesting email addresses from web pages/other sources |
| **Sniffing traffic** | A packet sniffer on a compromised machine observes and steals sensitive data (credit card numbers, passwords); can even be used to steal from *other* botnets |
| **Keylogging** | Records keystrokes on infected machines to harvest login credentials (e.g., PayPal) |
| **Spreading new malware** | Botnets can be used to distribute and grow new bot infections |
| **Installing ad-ons for click fraud** | Automates clicks to perpetrate "click fraud" |
| **Google AdSense abuse** | Automates ad clicks on sites showing AdSense to fraudulently inflate ad revenue |
| **Attacks on IRC chat networks ("clone attacks")** | A master agent instructs each bot to link to thousands of clones within an IRC network, flooding it — functionally similar to a DDoS attack |
| **Manipulating online polls/games** | Every bot has a unique address, letting the botnet cast many "unique" votes/moves |
| **Mass identity theft** | Send large volumes of email impersonating a reputable organization (e.g., eBay) to phish for identity data |
| **Credential stuffing** | Automated login attempts using stolen credentials across many websites at scale |
| **Cryptocurrency mining** | Installs mining software on compromised machines, stealing their CPU/GPU cycles without consent |

### Botnet-Based DDoS Attack — Full Flow

```
 1. Attacker sets a bot C&C handler
 2. Attacker infects a machine (creating the first "bot"/victim)
 3. That bot looks for other vulnerable systems and infects them too — growing the botnet
 4. Bots connect to the C&C handler and wait for instructions
 5. Attacker sends commands to the bots through the C&C
 6. Bots (zombies) attack the target server, in unison
```

## 2.3 Organized Cyber Crime: The Business Behind Botnets

Cybercriminals increasingly operate like organized crime syndicates with a predefined
revenue-sharing model — essentially a corporation offering criminal services, from malware
development and bank-account hacking to renting out massive DDoS capability for a price.

> **Example:** An organized crime syndicate might launch a DDoS attack against a bank specifically
> to *divert the bank's security team's attention* while a separate crew drains accounts using
> stolen credentials elsewhere — DDoS as a diversion tactic, not just an end in itself.

### Cybercrime Hierarchical Structure

```
                         Criminal Boss
                    (business entrepreneur —
                     never commits crimes directly)
                              │
                              ▼
              Underboss (Trojan provider & manager
                 of Trojan Command & Control)
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
  Campaign Manager      Campaign Manager      Campaign Manager
        │                     │                     │
        ▼                     ▼                     ▼
 Affiliation Network   Affiliation Network   Affiliation Network
        │                     │                     │
        ▼                     ▼                     ▼
 Stolen Data Reseller  Stolen Data Reseller  Stolen Data Reseller
```

- **Criminal Boss** — the head of the organization; acts purely as a business entrepreneur and
  never commits crimes personally.
- **Underboss** — sets up the C&C server and crimeware toolkit database; manages attack
  implementation and supplies Trojans.
- **Campaign Managers** — each runs their own affiliation network to implement attacks and steal
  data.
- **Stolen Data Resellers** — monetize the stolen data at the bottom of the chain.

### The Botnet Ecosystem

The wider botnet ecosystem links several specialized "markets":

- **Zero-Day Market** — buys/sells not-yet-patched vulnerabilities.
- **Botnet Market** — buys/sells access to existing botnets.
- **Malware Market** — buys/sells malware/bot code itself.
- The **Crimeware Toolkit Database** and **Trojan C&C Center** sit at the hub, feeding:
  - **DDoS-for-hire** and **extortion** services
  - **Data theft**, **phishing**, and **spam/mass mailing** (feeding stock fraud, scams, and
    fraudulent adverts downstream)
  - Exploitation of **client-side vulnerabilities** to redirect victims through **malicious
    sites**, harvesting **credit-card/e-commerce** data and **licenses/media (MP3, DivX)** for
    resale, and enabling **financial diversion**

## 2.4 Scanning Methods for Finding Vulnerable Machines

Before a botnet can grow, the malware needs a way to find new hosts to infect. Attackers use five
main scanning strategies:

| Method | How it works |
|---|---|
| **Random Scanning** | The infected machine probes IP addresses at random across the target network's IP range, checking each for vulnerability. Generates heavy traffic since many compromised machines probe the same addresses; propagation is fast early on and slows as available new IPs shrink. |
| **Hit-List Scanning** | The attacker first assembles a list of *known* potentially-vulnerable machines, then works through it. On compromising a machine, the list is split in half — the attacker keeps scanning one half while handing the other half to the newly-infected machine to scan. This halving repeats, so the number of scanners grows exponentially, infecting the entire hit-list very quickly. |
| **Topological Scanning** | Uses information already present *on* an infected machine (e.g., URLs/bookmarks/config on its hard drive) to find new targets. Accurate, and performs similarly well to hit-list scanning. |
| **Local Subnet Scanning** | An infected machine (often behind a firewall) looks for new vulnerable machines within its *own* local network, using locally-visible address information. Usually combined with one of the other techniques. |
| **Permutation Scanning** | All infected machines share a common pseudorandom permutation list of IP addresses (generated with a 32-bit block cipher and a preselected key). Each newly-infected host resumes scanning from just after the point where it was infected on the list; if it hits an already-infected machine, it restarts from a new random point. Scanning halts once a host encounters a set number of already-infected machines in a row, at which point a new permutation key is generated. **Advantages:** avoids reinfecting the same target repeatedly, and new targets are found at random for high scanning speed. |

## 2.5 How Malicious Code Propagates

Once a vulnerable machine is found, the attacker needs to actually get the attack toolkit onto it.
There are three propagation techniques:

### Central Source Propagation
```
Attacker ──1: Exploit──▶ Victim ──2──▶ Central Source ──3: Copy Code──▶ Victim ──4: Repeat──▶ Next Victim
```
The attacker places the attack toolkit on a central source; once a new vulnerable machine is
found, the central source transfers a copy of the toolkit to it, and the process installs
automatically via a scripting mechanism. The newly infected machine now searches for further
vulnerable machines, repeating the cycle. This technique commonly relies on **HTTP, FTP, and RPC**
protocols.

### Back-Chaining Propagation
```
Attacker ──1: Exploit──▶ Victim ──2──▶ Attacker (copies code back) ──3──▶ Victim ──4: Repeat──▶ Next Victim
```
The attacker places the toolkit on their *own* system, and the attack tools on the attacking
machine use special methods to accept a connection from the newly compromised system, then
transfer the toolkit *to* it. Simple port listeners, or even full intruder-installed web servers,
support this using the **Trivial File Transfer Protocol (TFTP)** for the back-channel file copy.

### Autonomous Propagation
```
Attacker ──1: Exploit AND Copy Code (simultaneously)──▶ Victim ──2: Repeat──▶ Next Victim
```
Unlike the two mechanisms above (which rely on an external file source), in autonomous
propagation the **attacking host itself** transfers the toolkit to the newly discovered
vulnerable system at the *exact moment* it breaks in — no separate transfer step needed.

## 2.6 Mobile Devices as Botnets for Launching DDoS Attacks

Android devices are a growing target for enlarging botnets because they are passively vulnerable
to Trojans, bots, and Remote Access Trojans (RATs) — frequently distributed through third-party
app stores and drive-by downloads. The typical attack chain:

1. The attacker binds a malicious server to an Android application package (**APK**) file.
2. The APK is encrypted, and unwanted features/permissions are stripped to avoid raising
   suspicion.
3. The trojanized package is distributed to a third-party app store (sometimes even slipping
   into stores like Google Play via disguised or drive-by-download infection methods).
4. A victim is tricked into downloading and installing the app, believing it's legitimate.
5. The attacker now has full control of the device, enslaving it into their mobile botnet to
   perform DDoS attacks, web injections, and other malicious activity.

➡️ Continue to real-world impact: [`03-real-world-case-studies.md`](03-real-world-case-studies.md)

---

**Next:** [`03-real-world-case-studies.md`](03-real-world-case-studies.md) →