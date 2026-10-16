# Vulnerability Handling Demo: SBOM, Triage, VEX, Fix, Advisory

A hands-on self-study exercise covering the full vulnerability handling cycle
required for manufacturers by the EU Cyber Resilience Act (CRA, Annex I Part II).

The product is fictional: a small Python **cloud gateway** for a networked
controller ("RC-100"). It reads a local config, renders a status page and
sends telemetry over HTTPS (`gateway/gateway.py`).

## Results at a glance

| Stage | Findings | What happened |
|---|---|---|
| 1. Scan of SBOM (v1.0) | 21 (1 critical, 8 high, 12 medium) | CycloneDX SBOM generated and scanned with Trivy |
| 2. Triage + VEX | 18 | 3 findings documented as *not affected* in OpenVEX |
| 3. Fix (v1.1) | 0 | Libraries updated, new SBOM re-scanned |

## Triage: does the CVE really affect our product?

| CVE | Library | Severity | Decision | Reason |
|---|---|---|---|---|
| CVE-2020-14343 | PyYAML | Critical | Not affected | Only `yaml.safe_load` is used; the vulnerable full loader is never called |
| CVE-2020-28493 | Jinja2 | Medium | **Affected** | Operator text from the web UI reaches the `urlize` filter → ReDoS / denial of service |
| CVE-2024-22195 | Jinja2 | Medium | Not affected | No template uses the `xmlattr` filter |
| CVE-2024-35195 | requests | Medium | Not affected | TLS verification is never disabled (`verify=False` not used) |
| CVE-2023-32681 | requests | Medium | Not affected by default; updated | No proxy in code, but requests reads system proxy settings, so a customer-configured proxy could expose it |

**Key lesson:** the only *critical* finding was not exploitable, while a *medium*
one was. Severity (CVSS) alone does not decide; reachability and deployment context do.

## Files

| File | Content |
|---|---|
| `gateway/` | Demo product: code, template, dependencies (fixed version) |
| `gateway-sbom.cdx.json` | CycloneDX SBOM of v1.0 (vulnerable versions) |
| `gateway-vex.json` | OpenVEX statements for the 3 *not affected* findings |
| `gateway-sbom-fixed.cdx.json` | CycloneDX SBOM of v1.1 (fixed versions) |
| `ADVISORY.md` | Security advisory for the affected finding |

## Further lessons
- **Zero findings does not mean secure.** A first scan of an image based on an
  end-of-life OS (Alpine 3.8) showed 0 findings, because no security data is
  published for it anymore, and software compiled from source did not appear in the SBOM.
- **"Not affected" is not "ignored".** It is documented (VEX), the library is
  still updated in the next regular release, and the decision is re-checked when the code changes.

## Link to the Cyber Resilience Act
- Annex I Part II: identify components (SBOM), address vulnerabilities without
  delay, publish information on fixed vulnerabilities (advisory).
- Article 14: actively exploited vulnerabilities must be reported within
  24 hours (early warning), 72 hours (notification) and 14 days (final report).
  No active exploitation was known here, so no report was required.

## Reproduce
```
trivy fs --format cyclonedx --output gateway-sbom.cdx.json gateway
trivy sbom gateway-sbom.cdx.json
trivy sbom --vex gateway-vex.json gateway-sbom.cdx.json
```
| `CRA & IEC 62443 Gap Analysis – Networked Refrigeration Controller.pdf` | Self-study gap analysis of a fictional networked controller against the CRA and IEC 62443 |
