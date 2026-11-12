"""Build six small review repositories; keep evaluation answers outside them."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import textwrap


def source(text: str) -> str:
    return textwrap.dedent(text).lstrip("\n")


CASES = [
    {
        "category": "clean-change",
        "requirements": "Add counts by SKU. Combine repeated SKUs and return an empty mapping for no rows. Input rows contain a string SKU and a nonnegative integer quantity.",
        "base": {
            "inventory.py": "def total_units(rows):\n    return sum(row['quantity'] for row in rows)\n",
            "test_inventory.py": source("""
                import unittest
                from inventory import total_units

                class InventoryTests(unittest.TestCase):
                    def test_total(self):
                        self.assertEqual(total_units([{'sku': 'A', 'quantity': 2}]), 2)
            """),
        },
        "head": {
            "inventory.py": source("""
                def total_units(rows):
                    return sum(row['quantity'] for row in rows)

                def counts_by_sku(rows):
                    counts = {}
                    for row in rows:
                        counts[row['sku']] = counts.get(row['sku'], 0) + row['quantity']
                    return counts
            """),
            "test_counts.py": source("""
                import unittest
                from inventory import counts_by_sku

                class CountsTests(unittest.TestCase):
                    def test_repeated_sku(self):
                        self.assertEqual(counts_by_sku([
                            {'sku': 'A', 'quantity': 2}, {'sku': 'A', 'quantity': 3}
                        ]), {'A': 5})

                    def test_empty(self):
                        self.assertEqual(counts_by_sku([]), {})
            """),
        },
        "probe": "from inventory import counts_by_sku; print(counts_by_sku([{'sku':'A','quantity':2},{'sku':'B','quantity':4},{'sku':'A','quantity':3}]))",
        "result": "{'A': 5, 'B': 4}",
        "expected_findings": [],
    },
    {
        "category": "intentional-behavior",
        "requirements": "Add a username validator for the legacy export. Accept 1 to 12 ASCII letters or digits; reject all other values with ValueError. Approved exclusions: Unicode names, punctuation, case normalization, and transliteration. Preserve accepted spelling and case.",
        "base": {"users.py": "def export_name(name):\n    return name\n"},
        "head": {
            "users.py": source("""
                def export_name(name):
                    if not isinstance(name, str) or not (1 <= len(name) <= 12):
                        raise ValueError('username must contain 1 to 12 ASCII letters or digits')
                    if not name.isascii() or not name.isalnum():
                        raise ValueError('username must contain 1 to 12 ASCII letters or digits')
                    return name
            """),
            "test_users.py": source("""
                import unittest
                from users import export_name

                class UserTests(unittest.TestCase):
                    def test_spelling(self):
                        self.assertEqual(export_name('AbC12'), 'AbC12')

                    def test_rejections(self):
                        for name in ('', 'x' * 13, 'Zo\u00eb', 'a_b', 'abc ', None):
                            with self.subTest(name=name), self.assertRaises(ValueError):
                                export_name(name)
            """),
        },
        "probe": "from users import export_name; print(export_name('AbC12'))",
        "result": "AbC12",
        "expected_findings": [],
        "false_positive_trap": "Do not demand Unicode support or normalization contrary to approved exclusions.",
    },
    {
        "category": "handled-edge-case",
        "requirements": "Change the public summarize API from a total to an arithmetic mean. Inputs are lists of finite numeric observations. Empty input must still raise ValueError. metrics.py contains private helpers used only through api.py.",
        "base": {
            "metrics.py": "def _summarize(values):\n    return sum(values)\n",
            "api.py": source("""
                from metrics import _summarize

                def summarize(values):
                    if not values:
                        raise ValueError('at least one observation is required')
                    return _summarize(values)
            """),
            "test_api.py": source("""
                import unittest
                from api import summarize

                class ApiTests(unittest.TestCase):
                    def test_empty(self):
                        with self.assertRaises(ValueError):
                            summarize([])
            """),
        },
        "head": {
            "metrics.py": "def _summarize(values):\n    return sum(values) / len(values)\n",
            "test_mean.py": source("""
                import unittest
                from api import summarize

                class MeanTests(unittest.TestCase):
                    def test_mean(self):
                        self.assertEqual(summarize([2, 4, 6]), 4)
            """),
        },
        "probe": "from api import summarize; print(summarize([2, 4, 6]))",
        "result": "4.0",
        "expected_findings": [],
        "false_positive_trap": "The public caller already rejects empty input; private helper division by zero is unreachable through the supported API.",
    },
    {
        "category": "pre-existing-bug",
        "requirements": "Append the currency code USD to the shipping receipt, retaining two decimal places. Keep the existing shipping calculation unchanged in this change. The established rate contract is $5 up to and including 10 kg, and $10 above 10 kg; callers provide positive integer weights.",
        "base": {
            "shipping.py": "def fee(weight_kg):\n    return 5 if weight_kg < 10 else 10\n",
            "receipt.py": "from shipping import fee\n\ndef receipt(weight_kg):\n    return f'{fee(weight_kg):.2f}'\n",
            "test_shipping.py": source("""
                import unittest
                from shipping import fee

                class ShippingTests(unittest.TestCase):
                    def test_rates(self):
                        self.assertEqual(fee(5), 5)
                        self.assertEqual(fee(11), 10)
            """),
        },
        "head": {
            "receipt.py": "from shipping import fee\n\ndef receipt(weight_kg):\n    return f'{fee(weight_kg):.2f} USD'\n",
            "test_receipt.py": source("""
                import unittest
                from receipt import receipt

                class ReceiptTests(unittest.TestCase):
                    def test_currency(self):
                        self.assertEqual(receipt(5), '5.00 USD')
            """),
        },
        "probe": "from shipping import fee; print(fee(10))",
        "base_result": "10",
        "result": "10",
        "expected_findings": [],
        "false_positive_trap": "The boundary bug exists in the base, remains unchanged and is not worsened. An explicitly separate historical observation is not a blocking finding against this change.",
    },
    {
        "category": "fixed-in-working-tree",
        "requirements": "Add an integer percentage discount to subtotal_cents. Inputs are a list of nonnegative integer prices in cents and a discount integer from 0 through 100. Round the discounted total down to integer cents. Preserve the old result when the discount is omitted.",
        "base": {"pricing.py": "def subtotal_cents(prices):\n    return sum(prices)\n"},
        "head": {
            "pricing.py": "def subtotal_cents(prices, discount_percent=0):\n    return sum(prices) - discount_percent\n",
            "test_pricing.py": source("""
                import unittest
                from pricing import subtotal_cents

                class PricingTests(unittest.TestCase):
                    def test_discount(self):
                        self.assertEqual(subtotal_cents([1000, 500], 20), 1200)

                    def test_rounding_and_default(self):
                        self.assertEqual(subtotal_cents([101], 50), 50)
                        self.assertEqual(subtotal_cents([]), 0)
                        self.assertEqual(subtotal_cents([101]), 101)
            """),
        },
        "staged": {"pricing.py": "def subtotal_cents(prices, discount_percent=0):\n    return sum(prices) * (100 - discount_percent)\n"},
        "working": {
            "pricing.py": "from rounding import apply_discount\n\ndef subtotal_cents(prices, discount_percent=0):\n    return apply_discount(sum(prices), discount_percent)\n",
            "rounding.py": "def apply_discount(cents, percent):\n    return cents * (100 - percent) // 100\n",
        },
        "probe": "from pricing import subtotal_cents; print(subtotal_cents([1000, 500], 20))",
        "head_result": "1480",
        "result": "1200",
        "expected_findings": [],
        "false_positive_trap": "HEAD and index each contain a bug; the final working tree fixes it using the relevant untracked rounding.py helper.",
    },
    {
        "category": "cross-file-regression",
        "requirements": "Add formatted dollar prices to the catalog. Preserve the payment payload contract: amount_cents is an integer number of cents, including when ordering multiple units. Supported SKUs are coffee and tea; quantities are nonnegative integers.",
        "base": {
            "catalog.py": "PRICES = {'coffee': 250, 'tea': 175}\n",
            "totals.py": "from catalog import PRICES\n\ndef total_cents(items):\n    return sum(PRICES[sku] * quantity for sku, quantity in items)\n",
            "checkout.py": "from totals import total_cents\n\ndef payment_payload(items):\n    return {'amount_cents': int(total_cents(items)), 'currency': 'USD'}\n",
            "test_checkout.py": source("""
                import unittest
                from checkout import payment_payload

                class CheckoutTests(unittest.TestCase):
                    def test_empty(self):
                        self.assertEqual(payment_payload([]), {'amount_cents': 0, 'currency': 'USD'})
            """),
        },
        "head": {
            "catalog.py": source("""
                from decimal import Decimal

                PRICES = {'coffee': Decimal('2.50'), 'tea': Decimal('1.75')}

                def display_price(sku):
                    return f'${PRICES[sku]:.2f}'
            """),
            "test_catalog.py": source("""
                import unittest
                from catalog import display_price

                class CatalogTests(unittest.TestCase):
                    def test_display(self):
                        self.assertEqual(display_price('coffee'), '$2.50')
                        self.assertEqual(display_price('tea'), '$1.75')
            """),
        },
        "probe": "from checkout import payment_payload; print(payment_payload([('coffee', 3)])['amount_cents'])",
        "base_result": "750",
        "result": "7",
        "expected_findings": [{
            "id": "price-unit-regression",
            "severity": "Important",
            "paths": ["catalog.py", "totals.py", "checkout.py"],
            "scenario": "Three coffees must produce amount_cents=750, but changing PRICES from integer cents to Decimal dollars makes checkout send 7.",
            "acceptable_severities": ["Critical", "Important"],
        }],
    },
]


def run(args: list[str], directory: Path) -> str:
    environment = os.environ.copy()
    if args[:2] == ["git", "commit"]:
        # Synthetic history is identical in independently built comparison sets.
        environment.update(GIT_AUTHOR_DATE="2026-11-12T00:00:00+0000", GIT_COMMITTER_DATE="2026-11-12T00:00:00+0000")
    result = subprocess.run(args, cwd=directory, env=environment, text=True, encoding="utf-8", capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{args!r} failed in {directory}:\n{result.stdout}{result.stderr}")
    return result.stdout.strip()


def write_files(directory: Path, files: dict[str, str]) -> None:
    for name, contents in files.items():
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(contents, encoding="utf-8", newline="\n")


def check_probe(directory: Path, code: str, expected: str) -> str:
    actual = run([sys.executable, "-B", "-c", code], directory)
    if actual != expected:
        raise AssertionError(f"{directory.name}: expected {expected!r}, got {actual!r}")
    return actual


def build(destination: Path) -> Path:
    destination = destination.resolve()
    # Refuse merges or overwrites, including any pre-existing empty directory.
    destination.mkdir(parents=True, exist_ok=False)
    manifest = {"schema_version": 1, "cases": []}
    for index, case in enumerate(CASES, 1):
        directory = destination / f"case-{index:02d}"
        directory.mkdir()
        run(["git", "init", "--quiet", "--initial-branch=main", "--template="], directory)
        for key, value in {
            "user.name": "Review Fixture",
            "user.email": "fixture@example.invalid",
            "commit.gpgsign": "false",
            "core.autocrlf": "false",
            "core.hooksPath": ".git/no-hooks",
            "core.fsmonitor": "false",
        }.items():
            run(["git", "config", "--local", key, value], directory)
        write_files(directory, {
            ".gitignore": "__pycache__/\n*.pyc\n.opencode/\n",
            "AGENTS.md": "# Repository checks\n\nUse Python standard-library tools. Run `python -B -m unittest discover -v` for the available tests.\n",
            "docs/specs/change-design.md": f"# Requested change\n\nStatus: Approved\n\n{case['requirements']}\n",
            **case["base"],
        })
        run(["git", "add", "."], directory)
        run(["git", "commit", "--quiet", "-m", "Initial implementation"], directory)
        base_sha = run(["git", "rev-parse", "HEAD"], directory)
        verification = {}
        if "base_result" in case:
            verification["base_probe"] = check_probe(directory, case["probe"], case["base_result"])
        write_files(directory, case["head"])
        run(["git", "add", "."], directory)
        run(["git", "commit", "--quiet", "-m", "Implement requested change"], directory)
        head_sha = run(["git", "rev-parse", "HEAD"], directory)
        if "head_result" in case:
            verification["head_probe"] = check_probe(directory, case["probe"], case["head_result"])
        if "staged" in case:
            write_files(directory, case["staged"])
            run(["git", "add", "."], directory)
        write_files(directory, case.get("working", {}))
        verification["final_probe"] = check_probe(directory, case["probe"], case["result"])
        tests = subprocess.run(
            [sys.executable, "-B", "-m", "unittest", "discover", "-v"],
            cwd=directory, text=True, encoding="utf-8", capture_output=True,
        )
        if tests.returncode:
            raise AssertionError(f"Fixture tests failed in {directory}:\n{tests.stdout}{tests.stderr}")
        verification["test_output"] = tests.stdout + tests.stderr
        verification["test_command"] = "python -B -m unittest discover -v"
        verification["python_version"] = sys.version.split()[0]
        status = run(["git", "status", "--short", "--untracked-files=all"], directory)
        if case.get("working"):
            if "MM pricing.py" not in status or "?? rounding.py" not in status:
                raise AssertionError(f"Expected index/working-tree/untracked layers, got {status!r}")
        elif status:
            raise AssertionError(f"Unexpected dirty fixture {directory}: {status}")
        manifest["cases"].append({
            "id": directory.name,
            "category": case["category"],
            "directory": str(directory),
            "spec": "docs/specs/change-design.md",
            "base_sha": base_sha,
            "head_sha": head_sha,
            "status": status,
            "source_sha256": {
                path.relative_to(directory).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in sorted(directory.rglob("*"))
                if path.is_file() and ".git" not in path.relative_to(directory).parts
            },
            "expected_findings": case["expected_findings"],
            "false_positive_trap": case.get("false_positive_trap"),
            "verification": verification,
        })
    manifest_path = destination / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="New scratch directory outside the source repository")
    args = parser.parse_args()
    destination = args.destination.resolve()
    repository = Path(__file__).resolve().parents[3]
    if destination == repository or repository in destination.parents:
        parser.error("destination must be outside the source repository")
    for name in ("OneDrive", "OneDriveConsumer", "OneDriveCommercial"):
        if os.environ.get(name):
            excluded = Path(os.environ[name]).resolve()
            if destination == excluded or excluded in destination.parents:
                parser.error("destination must be outside OneDrive")
    print(build(destination))


if __name__ == "__main__":
    main()
