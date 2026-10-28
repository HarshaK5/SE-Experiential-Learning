# Static Analysis Issues

The table records the baseline findings from Pylint, Bandit, and Flake8. The
line numbers refer to the original `tax_calculator.py` before the fixes.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| CGI handler | Security - high | 92 | Bandit B412 flagged the use of `CGIHandler`, which is unsafe for an exposed application. | Removed the unused CGI entry point rather than retaining an unsafe integration. |
| XML external entity risk | Security - medium | 5, 86 | Bandit B408 and B318 flagged `minidom` parsing of untrusted XML. | Replaced `minidom` with `defusedxml.ElementTree` and validated required fields. |
| ECB encryption | Security - medium | 77 | Bandit B305 flagged ECB, which reveals repeated plaintext blocks. | Replaced AES-ECB and manual padding with AES-GCM and a fresh random nonce. |
| Weak RSA key | Security - medium | 83 | Bandit B505 flagged the 1024-bit RSA key as breakable. | Increased the key size to 2048 bits. |
| Hard-coded encryption key | Security | 10 | A fixed key was embedded in source code, so every deployment shared the same secret. | Generate a cryptographically random 256-bit key at process startup. A production service should load a persistent secret from a secret manager. |
| Incorrect rebate calculation | Correctness | 38-41 | Cess was calculated before the rebate reset the tax, producing tax for income at the rebate limit. | Apply the rebate before calculating cess and clamp taxable income at zero. |
| Incorrect age boundary | Correctness | 51 | Age 80 incorrectly received the under-60 exemption because the comparison used `> 80`. | Use `age >= 80` for the senior-most exemption. |
| Unused variables and imports | Quality | 2-4, 36 | Pylint and Flake8 reported unused imports, `bracket`, and `checked`. | Removed unused imports and simplified the tax calculation. |
| Bare exception | Quality | 73 | Flake8 E722 and Pylint flagged a bare `except`, which hid unrelated failures. | Removed the unnecessary exception; `re.fullmatch` safely returns `False` for invalid input. |
| Formatting violations | Style | Multiple | Flake8 reported long lines, missing blank lines, and multiple statements on one line. | Applied PEP 8 formatting and separated statements and functions. |

## Verification

After the fixes:

- Pylint: **10.00/10**
- Bandit: **0 issues**
- Flake8: **0 violations**

