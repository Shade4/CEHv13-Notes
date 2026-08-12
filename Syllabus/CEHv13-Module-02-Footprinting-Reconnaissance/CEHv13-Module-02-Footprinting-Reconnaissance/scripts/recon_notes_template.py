#!/usr/bin/env python3
"""Create a small structured reconnaissance note template."""

from datetime import datetime, timezone
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("target")
args = parser.parse_args()

record = {
    "target": args.target,
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "",
    "source": "",
    "observation": "",
    "evidence": "",
    "confidence": "low|medium|high",
    "passive_or_active": "passive|active",
    "security_relevance": "",
    "validated": False,
    "notes": "",
}

print(json.dumps(record, indent=2))
