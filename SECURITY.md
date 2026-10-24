# Security policy

## Reporting a vulnerability

Report vulnerabilities privately through GitHub private vulnerability reporting:

https://github.com/getrefrain/refrain/security/advisories/new

Never open a public issue, pull request or Discussion for a vulnerability.

## Supported versions

No version has been released yet. Only the `main` branch is supported.

## What to expect

- We acknowledge your report within 3 business days.
- We aim to fix and disclose within 90 days of the report.

## Highest priority

These classes of issue matter most:

- **Cross-principal leakage**: one principal sees data, results or metadata that belong to another.
- **Cache scoping**: a cached result is served outside the scope it was stored for.
- **Data residency**: result data, SQL, sampled values or identities leave the customer's cloud.

Other issues are welcome too.
