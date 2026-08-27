# 07 — Detection Techniques

> Exam objective: *Explain DoS/DDoS attack countermeasures* (detection subset)

Early detection is what makes every other countermeasure in
[`08-countermeasures-and-mitigation.md`](08-countermeasures-and-mitigation.md) possible — you
can't throttle, drop, or reroute an attack you haven't noticed yet. Detecting a DoS/DDoS attack
is genuinely tricky: the detector needs to reliably tell a genuine traffic spike apart from a
malicious one, which isn't always possible with full confidence. It's also computationally
impossible to deeply inspect every single packet at line rate on a busy network, so all
practical detection techniques rely on **statistical analysis of deviation** rather than
packet-by-packet inspection — they define an attack as an **abnormal, noticeable deviation** from
a threshold of normal network traffic statistics.

There are three main detection techniques:

## 7.1 Activity Profiling

**Activity profiling** is based on the *average packet rate* for a network flow — a flow being a
sequence of consecutive packets sharing similar header fields (source/destination IP, ports,
transport protocol). Activity profiles are built by continuously monitoring network packet-header
information.

**An attack is indicated by:**
- An increase in activity levels among the network-flow clusters
- An increase in the overall number of distinct clusters (more typical of a *distributed* attack)

The underlying insight: for a higher average packet rate or activity level, the time between
consecutive matching packets shrinks. **Randomness in activity level is measured using an entropy
calculation** — if a network is under attack, entropy across network activity levels tends to
*increase*, since attack traffic often introduces more varied/unusual flow patterns into what was
previously a fairly predictable baseline.

**Main challenge:** raw traffic volume. This is mitigated by **clustering packet flows with
similar characteristics** — because DoS attack traffic tends to be highly repetitive and similar
packet-to-packet, an increase in average packet rate *or* an increase in the diversity of distinct
flows can both be independent indicators of an attack underway.

## 7.2 Sequential Change-Point Detection

This technique filters network traffic by **IP address, targeted port number, and communication
protocol**, then stores the resulting traffic-flow data as a time series (flow rate vs. time).
**Change-point detection algorithms** scan that time series for sudden, statistically significant
shifts in traffic flow rate — a drastic change is treated as a possible sign that a DoS attack is
underway.

The classic implementation uses the **CUSUM (Cumulative Sum) algorithm**, which calculates the
deviation between the *actual* and *expected* local average within the traffic time series. Beyond
flagging DoS attacks, this same technique is also effective at identifying the typical scanning
behavior of network worms (see the scanning methods discussed in
[`02-botnets-and-cybercrime-ecosystem.md`](02-botnets-and-cybercrime-ecosystem.md)) — since worm
propagation also produces a distinctive, sudden shift in traffic patterns.

## 7.3 Wavelet-Based Signal Analysis

Wavelet analysis describes an input signal in terms of its **spectral components** — it divides
the incoming signal into different frequency bands and analyzes each one separately. Analyzing
the **energy of each spectral window** reveals the presence of anomalies: these techniques check
which frequency components are present at a given time and describe them, and an unfamiliar
frequency component showing up is treated as a signal of suspicious network activity.

Practically, a network traffic signal is a combination of a time-localized data-flow signal and
background noise. Wavelet-based analysis **filters the anomalous traffic-flow signal out from
that background noise**. Normal network traffic tends to sit in the **low-frequency** range;
during an attack, the **high-frequency components** of the overall signal increase noticeably —
that shift toward high-frequency energy is the anomaly signature this technique is built to catch.

---

## Summary Comparison

| Technique | What it measures | Best at catching |
|---|---|---|
| Activity Profiling | Average packet rate & flow-cluster entropy | Broad volumetric increases; distributed attacks (more clusters) |
| Sequential Change-Point Detection | Sudden shifts in flow rate over time (CUSUM) | Sharp-onset attacks; also detects worm-scanning behavior |
| Wavelet-Based Signal Analysis | Frequency-domain energy distribution | Subtle anomalies buried in noisy traffic; frequency-signature shifts |

None of these techniques is perfect in isolation — real-world DDoS protection platforms (see
[`09-protection-tools-and-services.md`](09-protection-tools-and-services.md)) typically combine
several detection approaches plus machine-learning-based anomaly detection to reduce both false
positives (blocking legitimate traffic) and false negatives (missing a real attack).

---

**Next:** [`08-countermeasures-and-mitigation.md`](08-countermeasures-and-mitigation.md) →