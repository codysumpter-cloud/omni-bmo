# Security Policy

## Reporting a vulnerability

Please do **not** open a public issue for sensitive problems such as:

- token or credential leaks
- remote command-execution bypasses
- transport or pairing bypasses
- private-data exposure
- unsafe operator-control paths

Instead, gather the minimum reproducible details and report the issue privately to the maintainer.

## Secrets and sensitive material

Never commit:

- live bearer tokens
- `.env` files with secrets
- private bridge endpoints with embedded credentials
- raw logs containing secrets or personal identifiers

## Safe defaults

- use placeholders in docs and examples
- redact screenshots and logs
- rotate any secret immediately if exposure is possible
