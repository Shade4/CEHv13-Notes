# Lab 05 — Local Reconnaissance Lab

## Objective

Practice reconnaissance without touching a real third-party target.

## Suggested architecture

Run a deliberately vulnerable or test application locally:

```text
Your machine
   |
   +-- Local VM / container
         |
         +-- Test web application
         +-- Test DNS
         +-- Test mail data
```

## Workflow

### Step 1 — Scope

```text
Target: 127.0.0.1 / local VM
Purpose: training
Authorization: owner-controlled
```

### Step 2 — DNS

Create a test domain or local DNS zone and practice:

- A
- AAAA
- MX
- NS
- TXT
- SOA
- PTR

### Step 3 — Web

Observe:

- Headers
- Technology indicators
- Public pages
- Error handling

### Step 4 — Path

Use traceroute/tracert where meaningful in your local environment.

### Step 5 — Documentation

Create a complete footprint report.

## Expected outcome

The learner should be able to move from raw observations to a defensible security report.
