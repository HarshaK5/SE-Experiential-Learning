"""Teaching example for calculating income tax under two tax regimes."""

import re
import secrets
from typing import Mapping

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from defusedxml import ElementTree


STANDARD_DEDUCTION_NEW = 75000
STANDARD_DEDUCTION_OLD = 50000
REBATE_LIMIT_NEW = 1200000
CESS = 0.04
PAN_KEY = secrets.token_bytes(32)
NEW_SLABS = (
    (400000, 0.00),
    (800000, 0.05),
    (1200000, 0.10),
    (1600000, 0.15),
    (2000000, 0.20),
    (2400000, 0.25),
    (float("inf"), 0.30),
)
OLD_SLABS = (
    (250000, 0.00),
    (500000, 0.05),
    (1000000, 0.20),
    (float("inf"), 0.30),
)


def calculate_slab_tax(taxable_income: float, lower_limit: float,
                       slabs: tuple[tuple[float, float], ...]) -> float:
    """Calculate progressive tax for income above the exemption limit."""
    tax = 0.0
    previous_limit = lower_limit
    for upper_limit, rate in slabs:
        taxable_at_rate = max(
            0.0, min(taxable_income, upper_limit) - previous_limit
        )
        tax += taxable_at_rate * rate
        previous_limit = upper_limit
        if taxable_income <= upper_limit:
            break
    return tax


def new_regime_tax(salary: float) -> int:
    """Return tax under the new regime, including cess."""
    taxable = max(0.0, salary - STANDARD_DEDUCTION_NEW)
    if taxable <= REBATE_LIMIT_NEW:
        return 0
    tax_amount = calculate_slab_tax(taxable, 0, NEW_SLABS)
    return int(tax_amount * (1 + CESS))


def basic_exemption(age: int) -> int:
    """Return the old-regime basic exemption based on taxpayer age."""
    if 60 <= age < 80:
        return 300000
    if age >= 80:
        return 500000
    return 250000


def old_regime_tax(salary: float, age: int,
                   deductions: Mapping[str, float]) -> int:
    """Return tax under the old regime, including deductions and cess."""
    taxable = max(
        0.0,
        salary - STANDARD_DEDUCTION_OLD - sum(deductions.values()),
    )
    tax_amount = calculate_slab_tax(taxable, basic_exemption(age), OLD_SLABS)
    return int(tax_amount * (1 + CESS))


def better_regime(salary: float, age: int,
                  deductions: Mapping[str, float]) -> str:
    """Return the regime with the lower tax liability."""
    new_tax = new_regime_tax(salary)
    old_tax = old_regime_tax(salary, age, deductions)
    return "new" if new_tax < old_tax else "old"


def is_valid_pan(pan: str) -> bool:
    """Return whether a value has the expected PAN format."""
    return bool(re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", pan))


def encrypt_pan(pan: str) -> str:
    """Encrypt a PAN with authenticated encryption and a fresh nonce."""
    nonce = secrets.token_bytes(12)
    ciphertext = AESGCM(PAN_KEY).encrypt(nonce, pan.encode(), None)
    return (nonce + ciphertext).hex()


def signing_key() -> rsa.RSAPrivateKey:
    """Generate a signing key using a currently recommended RSA size."""
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def parse_form16(xml_text: str) -> tuple[int, int]:
    """Read salary and TDS values from a safely parsed Form 16 document."""
    root = ElementTree.fromstring(xml_text)
    salary = root.findtext("salary")
    tds = root.findtext("tds")
    if salary is None or tds is None:
        raise ValueError("Form 16 must contain salary and tds elements")
    return int(salary), int(tds)


def main() -> None:
    """Print representative calculator results."""
    deductions = {"80C": 200000, "80D": 30000}
    print("New regime, salary 12,75,000:", new_regime_tax(1275000))
    print("New regime, salary 18,00,000:", new_regime_tax(1800000))
    print("Old regime, salary 18,00,000:",
          old_regime_tax(1800000, 35, deductions))
    print("Better regime:", better_regime(1800000, 35, deductions))
    print("Basic exemption at age 80:", basic_exemption(80))
    print("PAN 'ABCDE1234F' valid?", is_valid_pan("ABCDE1234F"))
    print("PAN encryption produces unique ciphertexts:",
          encrypt_pan("ABCDE1234F") != encrypt_pan("ABCDE1234F"))
    print("Form 16:", parse_form16(
        "<form16><salary>1800000</salary><tds>150000</tds></form16>"
    ))
    print("Signing key size:", signing_key().key_size)


if __name__ == "__main__":
    main()
