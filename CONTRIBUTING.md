# Contributing

Thank you for helping build an open, rigorous control-research commons.

## Before opening a pull request

1. Open an issue for architecture, protocol, safety-policy or real-plant integration changes.
2. Keep production connectivity disabled by default and make unsafe states fail closed.
3. Add tests for normal behavior, invalid input, timeout/failure and safety invariants.
4. Run `python -m unittest discover -s tests` and `ruff check .`.
5. Update the relevant safety case, threat model or architecture decision.

## Data and security rules

Do not commit real credentials, certificates, IP addresses, detailed network diagrams, proprietary DCS exports, unapproved plant tags, incident-sensitive data, personal information or export-controlled/restricted material. Use synthetic data unless you can document the right to redistribute the material and have removed operationally sensitive details.

Pull requests that add a live write path, bypass a safety layer or imply certification will be rejected.

By contributing, you agree that your contribution is licensed under Apache-2.0 and that you have the right to submit it.
