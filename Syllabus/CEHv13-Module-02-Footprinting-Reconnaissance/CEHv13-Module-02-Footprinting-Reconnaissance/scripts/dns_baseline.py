#!/usr/bin/env python3
"""
Minimal DNS baseline collector.

Purpose:
    Collect common DNS records for a domain in an authorized assessment.

This script performs DNS queries only. It is not a port scanner.
"""

import argparse
import socket

try:
    import dns.resolver
except ImportError:
    raise SystemExit(
        "Install dnspython first: python -m pip install dnspython"
    )

RECORDS = ["A", "AAAA", "MX", "NS", "TXT", "SOA", "CNAME"]

def query(domain: str, record_type: str):
    resolver = dns.resolver.Resolver()
    try:
        answers = resolver.resolve(domain, record_type)
        return [str(answer) for answer in answers]
    except Exception as exc:
        return [f"[no result / error: {exc}]"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="Authorized domain to query")
    args = parser.parse_args()

    domain = args.domain.rstrip(".")
    print(f"DNS baseline for: {domain}")
    print("=" * 60)

    for record_type in RECORDS:
        print(f"\n[{record_type}]")
        for value in query(domain, record_type):
            print(value)

if __name__ == "__main__":
    main()
