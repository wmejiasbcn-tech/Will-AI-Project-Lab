import hashlib
import tempfile
import unittest
from pathlib import Path

from apply_p1_patch import (
    OLD_HASH, OLD_SIZE, OLD_WRITE, build_patched_bytes, apply_patch
)

FIXTURE = '''        doc_hash = hashlib.sha256(content_text.encode("utf-8")).hexdigest()
        timestamp = datetime.now(timezone(timedelta(hours=2))).isoformat()

        # Store document
        corpus_file = os.path.join(self.corpus_dir, f"{normative_type.lower()}_{doc_uuid}.txt")
        os.makedirs(self.corpus_dir, exist_ok=True)
        with open(corpus_file, "w", encoding="utf-8") as f:
            f.write(content_text)

        # Register in index
        entry = {
            "size_bytes": len(content_text.encode("utf-8")),
        }
'''


class PatchTests(unittest.TestCase):
    def test_lf_patch_uses_binary_write_and_rechecks_disk_hash(self):
        result = build_patched_bytes(FIXTURE.encode("utf-8")).decode("utf-8")
        self.assertNotIn(OLD_HASH, result)
        self.assertNotIn(OLD_WRITE, result)
        self.assertNotIn(OLD_SIZE, result)
        self.assertIn('content_bytes = content_text.encode("utf-8")', result)
        self.assertIn('with open(corpus_file, "wb") as f:', result)
        self.assertIn('with open(corpus_file, "rb") as f:', result)
        self.assertIn("stored_hash != doc_hash", result)
        self.assertIn('"size_bytes": len(content_bytes)', result)

    def test_crlf_source_style_is_preserved(self):
        raw = FIXTURE.replace("\n", "\r\n").encode("utf-8")
        result = build_patched_bytes(raw)
        self.assertIn(b"\r\n", result)
        self.assertNotIn(b"\n", result.replace(b"\r\n", b""))

    def test_patch_fails_closed_when_source_has_drift(self):
        with self.assertRaises(ValueError):
            build_patched_bytes(b"class Unknown: pass\n")

    def test_patch_is_idempotent(self):
        first = build_patched_bytes(FIXTURE.encode("utf-8"))
        self.assertEqual(first, build_patched_bytes(first))

    def test_apply_creates_backup_and_verifies_source_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "dike_auditora.py"
            target.write_bytes(FIXTURE.encode("utf-8"))
            outcome = apply_patch(target)
            self.assertTrue(outcome["changed"])
            self.assertTrue(Path(str(target) + ".before-p1-crlf-lf.bak").exists())
            self.assertEqual(
                hashlib.sha256(target.read_bytes()).hexdigest(),
                outcome["patched_sha256"],
            )


if __name__ == "__main__":
    unittest.main()
