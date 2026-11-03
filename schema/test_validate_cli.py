"""CLI regressions for requested signature verification (issue #172).

Uses the published tokens and import blocker from the issue reproduction.
Run from the repository root with:
    python3 -m unittest discover -s schema -p 'test_validate_cli.py' -v
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate.py"
MANIFEST = json.loads((HERE / "vectors" / "manifest.json").read_text(
    encoding="utf-8"))
PUBLIC_KEY = MANIFEST["public_key"]
VALID = "vectors/positive/allow-read.json"
ALTERED = "vectors/negative/bad-signature.json"

# A fresh interpreter prevents a cached module from bypassing the finder.
# Block the package and every submodule, as in the published reproduction.
BLOCK_IMPORT = """
import runpy
import sys

blocked = sys.argv[1]
assert not any(n == blocked or n.startswith(blocked + ".") for n in sys.modules)

class Block:
    def find_spec(self, name, path=None, target=None):
        if name == blocked or name.startswith(blocked + "."):
            raise ImportError(f"No module named {name!r}")
        return None

sys.meta_path.insert(0, Block())
sys.argv = sys.argv[2:]
runpy.run_path(sys.argv[0], run_name="__main__")
"""


class ValidateCLITests(unittest.TestCase):
    def run_cli(self, *args: str, block: str | None = None):
        command = [sys.executable]
        if block is not None:
            command += ["-c", BLOCK_IMPORT, block]
        command += [str(VALIDATOR), *args]
        result = subprocess.run(command, cwd=HERE, capture_output=True,
                                text=True, encoding="utf-8", timeout=30)
        self.assertEqual(result.stderr, "", result.stderr)
        return result

    def assert_unavailable(self, token: str):
        result = self.run_cli("--key", PUBLIC_KEY, token, block="cryptography")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(f"ERROR  {token}: [no-verifier]", result.stdout)
        self.assertIn("pip install cryptography", result.stdout)
        self.assertNotIn("INVALID", result.stdout)
        self.assertNotRegex(result.stdout, r"(?m)^\s*ok\s")
        self.assertNotIn("signature: verified", result.stdout)

    def test_valid_signature_verified(self):
        result = self.run_cli("--key", PUBLIC_KEY, VALID)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn(f"ok  {VALID}; signature: verified against supplied key",
                      result.stdout)
        self.assertIn("warning: platform SOFTWARE", result.stdout)

    def test_altered_signature_invalid(self):
        result = self.run_cli("--key", PUBLIC_KEY, ALTERED)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(f"INVALID  {ALTERED}: [signature]", result.stdout)
        self.assertNotIn("ERROR", result.stdout)
        self.assertNotRegex(result.stdout, r"(?m)^\s*ok\s")

    def test_valid_signature_unavailable(self):
        self.assert_unavailable(VALID)

    def test_altered_signature_unavailable(self):
        self.assert_unavailable(ALTERED)

    def test_signature_not_requested(self):
        for token in (VALID, ALTERED):
            for blocked in (None, "cryptography"):
                with self.subTest(token=token, blocked=blocked):
                    result = self.run_cli(token, block=blocked)
                    self.assertEqual(result.returncode, 0, result.stdout)
                    self.assertIn(
                        f"ok  {token}; signature: not requested (no --key)",
                        result.stdout)
                    self.assertNotIn("signature: verified", result.stdout)

    def test_empty_or_malformed_key_is_an_error(self):
        for key in ("", "not-hex", "00", "00" * 33):
            with self.subTest(key=key):
                result = self.run_cli("--key", key, VALID)
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn(f"ERROR  {VALID}: [bad-key]", result.stdout)
                self.assertNotIn("INVALID", result.stdout)
                self.assertNotRegex(result.stdout, r"(?m)^\s*ok\s")

    def test_missing_structural_validator_is_an_error(self):
        result = self.run_cli("--key", PUBLIC_KEY, VALID, block="jsonschema")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(f"ERROR  {VALID}: [no-validator]", result.stdout)
        self.assertNotIn("INVALID", result.stdout)
        self.assertNotRegex(result.stdout, r"(?m)^\s*ok\s")

    def test_earlier_semantic_failure_remains_invalid(self):
        token = "vectors/negative/tree-size-too-small.json"
        result = self.run_cli("--key", PUBLIC_KEY, token, block="cryptography")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn(f"INVALID  {token}: [tree-size]", result.stdout)
        self.assertNotIn("no-verifier", result.stdout)

    def test_multiple_tokens_continue_and_preserve_failure(self):
        result = self.run_cli("--key", PUBLIC_KEY, VALID, ALTERED, VALID)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertEqual(result.stdout.count(
            f"ok  {VALID}; signature: verified against supplied key"), 2)
        self.assertEqual(result.stdout.count(
            f"INVALID  {ALTERED}: [signature]"), 1)

    def test_multiple_unavailable_tokens_are_reported(self):
        result = self.run_cli("--key", PUBLIC_KEY, VALID, ALTERED,
                              block="cryptography")
        self.assertEqual(result.returncode, 1, result.stdout)
        for token in (VALID, ALTERED):
            self.assertIn(f"ERROR  {token}: [no-verifier]", result.stdout)
        self.assertNotIn("INVALID", result.stdout)
        self.assertNotRegex(result.stdout, r"(?m)^\s*ok\s")

    def test_published_vectors(self):
        result = self.run_cli("--vectors")
        expected = sum(len(MANIFEST.get(group, []))
                       for group in ("positive", "negative", "canonical"))
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn(f"{expected} passed, 0 failed", result.stdout)

    def test_vectors_do_not_treat_unavailable_as_rejection(self):
        result = self.run_cli("--vectors", block="cryptography")
        self.assertEqual(result.returncode, 1, result.stdout)
        affected = [entry["file"] for entry in MANIFEST["positive"]]
        affected.append("negative/bad-signature.json")
        for token in affected:
            with self.subTest(token=token):
                lines = [line for line in result.stdout.splitlines()
                         if token in line]
                self.assertEqual(len(lines), 1, result.stdout)
                self.assertIn("FAIL", lines[0])
                self.assertIn("cannot evaluate", lines[0])
                self.assertIn("[no-verifier]", lines[0])
        self.assertNotIn("ACCEPTED", result.stdout)

    def test_canonical_mode_does_not_claim_signature_verification(self):
        result = self.run_cli("--canonical", "--key", PUBLIC_KEY, VALID,
                              block="cryptography")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("canonical bytes", result.stdout)
        self.assertIn("signing input", result.stdout)
        self.assertNotIn("signature:", result.stdout)
        self.assertNotRegex(result.stdout, r"(?m)^\s*ok\s")


if __name__ == "__main__":
    unittest.main()
