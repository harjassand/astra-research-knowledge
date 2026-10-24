"""Execute dependency-free static-browser cache regressions when Node is available."""
from pathlib import Path
import shutil
import subprocess
import unittest


NODE = shutil.which("node")
ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(NODE, "Optional Node.js browser-cache fixtures require node")
class WebCacheRegressions(unittest.TestCase):
    def test_dataset_updates_cache_recovery_and_request_races(self):
        result = subprocess.run([NODE, str(ROOT / "knowledge/test_web_cache.cjs")], cwd=ROOT,
                                capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("3 static web cache/epoch scenarios passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
