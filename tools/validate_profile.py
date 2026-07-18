#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

REQUIRED_TEXT = (
    "# Arun Kumar Duraipandian",
    "Principal-level SRE | Distributed SaaS Platforms | AI-Assisted Reliability Engineering",
    "Site Reliability Engineering Professional at IBM",
    "large-scale distributed SaaS platforms spanning Kubernetes/OpenShift",
    "portfolio-wide resilience review across alerting",
    "critical production workload",
    "avoiding critical upgrade downtime",
    "20% MTTR improvement",
    "over one thousand engineering hours",
    "six-figure estimated annual productivity value",
    "## Technical focus",
    "## Recognition",
)

PROHIBITED_PATTERNS = {
    "customer count": r"\b\d+ customers\b",
    "rounded cluster count": r"\b100\+ clusters\b",
    "rounded VSI count": r"\bthousands of virtual server instances\b",
    "rounded monitoring-control count": r"\b1,000\+ observability controls\b",
    "exact SLO duration": r"\b12 consecutive months\b",
    "exact upgrade rate": r"\b95% upgrade success\b",
    "exact productivity hours": r"\b1,040 engineering hours\b",
    "exact productivity dollars": r"\$104K\+",
    "exact support-case count": r"\b3,200\+?\b",
    "exact incident count": r"\b76\s+(?:CIE\s+)?incidents\b",
    "support-case wording": r"\bsupport cases\b",
    "exact cluster count": r"\b150 clusters\b",
    "exact VSI count": r"\b2,500 virtual server instances\b",
    "exact monitoring-control count": r"\b1,400 monitoring controls\b",
    "exact alert/synthetic split": r"\b(?:584 alert|816 synthetic)\b",
    "named customer": r"\b(?:Kaiser Permanente|BNPP|Prudential|Geico)\b",
    "flagship tenant wording": r"\bflagship tenant\b",
    "business automation SaaS wording": r"\b(?:BA SaaS|Business Automation SaaS|IBM Software Business Automation)\b",
    "specific IBM product portfolio": r"\b(?:CP4BA|CP4BAaaS|Cloud Pak for Business Automation|FileNet|Business Automation Workflow|Operational Decision Manager|Datacap|Content Manager OnDemand)\b",
    "unofficial IBM title": r"\b(?:Staff SRE|Principal SRE|SRE Manager) at IBM\b",
    "internal project name": r"\b(?:SRE CortexAI|SREFlow|BA SaaS Metrics Portal)\b",
    "IBM internal URL": r"https?://[^\s)]+\.ibm\.com\b",
    "badge wall": r"img\.shields\.io|github-readme-stats",
    "decorative HTML": r"<(?:div|table|img)\b",
    "placeholder": r"\b(?:TBD|TODO|coming soon)\b",
}


def validate(text: str) -> list[str]:
    failures: list[str] = []

    for required in REQUIRED_TEXT:
        if required not in text:
            failures.append(f"missing required text: {required}")

    for label, pattern in PROHIBITED_PATTERNS.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            failures.append(f"contains prohibited {label}")

    if len(re.findall(r"^# [^#].*$", text, flags=re.MULTILINE)) != 1:
        failures.append("README must contain exactly one H1 heading")

    links = dict(re.findall(r"\[([^]]+)]\(([^)]+)\)", text))
    expected_links = {
        "GitHub": "https://github.com/akdur",
        "LinkedIn": "https://linkedin.com/in/arunkduraipandian/",
        "Email": "mailto:arukdpn@gmail.com",
    }
    for label, url in expected_links.items():
        if links.get(label) != url:
            failures.append(f"missing or incorrect {label} link")

    if len(text.splitlines()) > 125:
        failures.append("README exceeds the 125-line profile limit")

    if len(text.split()) > 900:
        failures.append("README exceeds the 900-word profile limit")

    return failures


def main() -> int:
    if not README.exists():
        print(f"Profile validation failed: missing {README}", file=sys.stderr)
        return 1

    text = README.read_text(encoding="utf-8")
    failures = validate(text)
    if failures:
        print("Profile validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    checks = len(REQUIRED_TEXT) + len(PROHIBITED_PATTERNS) + 6
    print(f"Profile validation passed ({checks} checks).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
