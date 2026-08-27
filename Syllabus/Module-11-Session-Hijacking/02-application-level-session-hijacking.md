# 02 - Application-Level Session Hijacking

## Table of Contents
- [Overview](#overview)
- [Three Ways to Obtain a Session ID](#three-ways-to-obtain-a-session-id)
- [The 12 Ways to Compromise a Session Token](#the-12-ways-to-compromise-a-session-token)
- [Compromising Session IDs Using Sniffing](#compromising-session-ids-using-sniffing)
- [Predicting Session Tokens](#predicting-session-tokens)
- [Man-in-the-Middle / Manipulator-in-the-Middle](#man-in-the-middle--manipulator-in-the-middle)
- [Man-in-the-Browser / Manipulator-in-the-Browser](#man-in-the-browser--manipulator-in-the-browser)
- [Client-Side Attacks](#client-side-attacks)
- [Session Replay Attack](#session-replay-attack)
- [Session Fixation Attack](#session-fixation-attack)
- [Session Hijacking Using Proxy Servers](#session-hijacking-using-proxy-servers)
- [CRIME Attack](#crime-attack)
- [Forbidden Attack](#forbidden-attack)
- [Session Donation Attack](#session-donation-attack)
- [Comparison Table](#comparison-table-fixation-vs-donation-vs-replay-vs-csrf-vs-xss)

---

## Overview

Applicatoin-level session hijacking relies on HTTP sessions rather than the underlying TCP connection. The attacker steals or predicts a valid session token to gain unauthorized access to a web server, or to create a 
