#!/usr/bin/env python3
"""Run the bundled finite checks. Python 3.10+; standard library only."""
import subprocess
import sys
from pathlib import Path
if sys.version_info < (3, 10):
    raise SystemExit("Python 3.10 or newer is required.")
root = Path(__file__).resolve().parent
names = ("check_explicit_tableau_grammar.py", "check_folded_machine.py",
         "check_final_constants.py", "check_fk_merger_algebra.py")
for name in names:
    print("\n=== " + name + " ===", flush=True)
    subprocess.run([sys.executable, str(root / "checks" / name)], check=True, cwd=root)
print("\nAll bundled finite checks passed. See MANUSCRIPT.md for the infinite-volume proof.")
