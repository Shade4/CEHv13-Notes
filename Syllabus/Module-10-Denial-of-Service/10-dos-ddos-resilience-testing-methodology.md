# 10 — DoS/DDoS Resilience Testing Methodology

> 🧩 **This file is supplementary** — it is not part of the CEH v13 Module 10 slide deck, but is
> added here (per the "add extra detail" brief) as the natural next step once you understand the
> individual attack techniques (`04`–`05`) and defenses (`07`–`09`): how do you actually *verify*,
> in a controlled and authorized way, that your countermeasures work? This mirrors how DDoS
> resilience/"chaos" testing is run in real infrastructure and red-team engagements.

---

## 10.0 Before Anything Else: Authorization and Safety

**Never run any traffic-generation tool from this repo against a system you don't own or lack
signed authorization to test — including "just a quick test" against a production system.** A
resilience test that goes even slightly wrong can cause the exact outage you were trying to
verify protection against, with real business impact. At minimum you need:

- [ ] A signed **Statement of Work (SOW)** and **Rules of Engagement (RoE)** naming the exact
      systems, IP ranges, and time windows in scope
- [ ] Written sign-off from **everyone** who owns infrastructure in the traffic path — including
      any upstream ISP, CDN, or cloud provider, since a large enough test can look identical to a
      real attack from their side and trigger their *own* automated mitigations or abuse reports
- [ ] A **kill switch** / abort procedure agreed with the target system's operations team before
      you start
- [ ] Testing scheduled during a **low-traffic maintenance window**, never during peak production
      hours, unless the specific goal is to test peak-hour behavior with full stakeholder sign-off
- [ ] Legal/compliance review — many cloud providers' Acceptable Use Policies require **advance
      notice** before any load test above a certain traffic volume, even against your *own* hosted
      resources (AWS, Azure, and GCP all have specific policies and notification procedures for
      this)

If any of the above is missing, don't run the test.

---

## 10.1 Load Testing vs. Stress Testing vs. DDoS Simulation

These three terms get used loosely, but they answer different questions:

| Type | Question it answers | Typical tools |
|---|---|---|
| **Load testing** | "How does the system perform under *expected* peak traffic?" | Apache Bench (`ab`), `wrk`, JMeter, Locust, k6 |
| **Stress testing** | "Where is the breaking point, and how does the system fail — gracefully or catastrophically?" | Same tools as above, pushed well past expected capacity |
| **DDoS simulation** | "Does our actual DDoS mitigation stack (WAF, scrubbing service, rate limits, TCP intercept, etc.) detect and correctly respond to attack-shaped traffic?" | Purpose-built, contracted DDoS-simulation vendors; controlled use of attack tools from `06` *only* inside an isolated lab replica of production |

Most organizations should do the first two regularly as part of normal capacity planning, and
reserve the third — actual DDoS-shaped simulation — for a periodic, formally contracted exercise,
often run *with* your DDoS-protection vendor's cooperation so they can validate their own
detection systems too.

## 10.2 Phase 1 — Scoping

Define exactly what you're testing against, mapped to the attack categories in `04`–`05`:

| In scope? | Category | Reference |
|---|---|---|
| ☐ | Volumetric capacity (bandwidth saturation point) | `04.2` |
| ☐ | Protocol/connection-table exhaustion (SYN flood behavior) | `04.3` |
| ☐ | Application-layer resilience (HTTP flood, Slowloris-style slow connections) | `05.1`–`05.3` |
| ☐ | Mitigation-stack validation (does the WAF/scrubber correctly detect and respond?) | `09` |

Set measurable success criteria before starting: target requests-per-second the system should
sustain, maximum acceptable latency degradation, time-to-detection by your monitoring, and
time-to-mitigation by your defensive stack.

## 10.3 Phase 2 — Baseline

Capture normal-traffic baselines *before* testing, so you have something to compare against:

```bash
# Baseline current connection/request rates (example, adjust to your stack)
# nginx access log request-rate snapshot
tail -n 100000 /var/log/nginx/access.log | awk '{print $4}' | uniq -c

# Baseline current bandwidth utilization on an interface (Linux)
sar -n DEV 1 60
```

## 10.4 Phase 3 — Execution (Authorized Lab / Approved Window Only)

### Legitimate Load-Testing Tools

```bash
# Apache Bench — simple HTTP load test: 10,000 requests, 100 concurrent
ab -n 10000 -c 100 https://staging.example.com/

# wrk — modern HTTP benchmarking tool: 30-second test, 12 threads, 400 connections
wrk -t12 -c400 -d30s https://staging.example.com/

# hping3 — controlled SYN flood against YOUR OWN lab host, to test SYN-cookie/TCP-intercept config
# (run only against systems you own, on an isolated lab network)
sudo hping3 -S -p 80 --flood --rand-source 10.10.1.50

# hping3 — controlled ICMP flood test against your own lab host
sudo hping3 --icmp --flood 10.10.1.50
```

### Application-Layer / Slow-Connection Testing

```bash
# Simulate Slowloris-style slow-header connections against your OWN staging server,
# to verify your web server's connection-timeout hardening actually works
slowhttptest -c 1000 -H -i 10 -r 200 -t GET -u https://staging.example.com/ -x 24 -p 3
```

### Monitoring During the Test

Run these in parallel on the target/mitigation stack throughout the test window:

```bash
# Live connection-count snapshot
watch -n1 'ss -s'

# Live per-source packet-rate snapshot (helps validate rate-limiting rules from 08.2 are working)
sudo tcpdump -i eth0 -n | awk '{print $3}' | cut -d. -f1-4 | sort | uniq -c | sort -rn | head
```

Confirm whether your countermeasures (SYN cookies, TCP intercept, rate limiting, WAF rules, cloud
scrubbing) actually engaged, and how quickly — this is the real deliverable of the exercise, not
just "did it fall over."

## 10.5 Phase 4 — Reporting

Structure findings around the metrics defined in scoping:

1. **Executive summary** — did the system meet its target availability/latency SLOs under the
   tested load, in plain business language.
2. **Breaking point (if reached)** — at what traffic level did degradation begin, and what
   specifically failed first (a specific service, a specific connection-table limit, a specific
   upstream link)?
3. **Mitigation validation** — for each control listed in
   [`08-countermeasures-and-mitigation.md`](08-countermeasures-and-mitigation.md) that was in
   scope, did it trigger, how fast, and did it correctly distinguish attack traffic from
   legitimate traffic during the test?
4. **Detection validation** — did the techniques from
   [`07-detection-techniques.md`](07-detection-techniques.md) (or your commercial platform's
   equivalent) alert your team, and how long did that take end-to-end (detection → human
   awareness → mitigation engaged)?
5. **Remediation roadmap** — prioritized list of gaps found, mapped to specific fixes (a
   configuration change, a capacity upgrade, a new WAF rule, an escalation-process fix).
6. **Retest plan** — schedule a follow-up test after remediation to confirm the gap is actually
   closed.

---

**Related files:** [`04-volumetric-and-protocol-attacks.md`](04-volumetric-and-protocol-attacks.md) ·
[`08-countermeasures-and-mitigation.md`](08-countermeasures-and-mitigation.md) ·
[`cheatsheets/tools-and-commands.md`](cheatsheets/tools-and-commands.md)