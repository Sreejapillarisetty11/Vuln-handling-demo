# Security Advisory SA-2026-001: Denial of service in RC-100 gateway status page

**Published:** 16 October 2026
**Affected product:** RC-100 cloud gateway (demo), version 1.0
**Fixed in:** version 1.1
**CVE:** CVE-2020-28493 (Jinja2, urlize filter)
**Severity:** Medium (CVSS 3.1 base score 5.3)

## Description
The gateway status page passes operator notes to the Jinja2 urlize filter.
Jinja2 2.11.2 is vulnerable to a regular expression denial of service (ReDoS)
in this filter. A specially crafted text can cause high CPU load.

## Impact
An attacker with access to the notes field can make the status page
unresponsive. No data is disclosed or modified. The telemetry function
is not affected.

## Solution
Update to version 1.1, which uses Jinja2 3.1.6.

## Workaround
Until you update, restrict access to the web interface to trusted networks.

## CRA note
No active exploitation is known, so no early-warning report under
Article 14 of the Cyber Resilience Act is required.
