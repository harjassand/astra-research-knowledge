#!/usr/bin/env python3
"""Replay author diagnostics in isolation; never overwrite author originals."""
from pathlib import Path
import hashlib, shutil, subprocess, sys, tempfile

HERE = Path(__file__).resolve().parent
names = ["ic_port_complete_kernel_check.py", "IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY.md"]
before = {n: hashlib.sha256((HERE / n).read_bytes()).hexdigest() for n in names}
tmp = Path(tempfile.mkdtemp(prefix="ic_port_author_replay_"))
for name in names:
    shutil.copy2(HERE / name, tmp / name)
proc = subprocess.run([sys.executable, str(tmp / names[0])], capture_output=True, text=True)
(HERE / "ic_port_author_independent_replay.log").write_text(proc.stdout + proc.stderr)
assert proc.returncode == 0, proc.stderr
assert before == {n: hashlib.sha256((HERE / n).read_bytes()).hexdigest() for n in names}
shutil.copy2(tmp / "ic_port_complete_kernel_check.json",
             HERE / "ic_port_author_independent_replay.json")
print("PASS isolated author-code replay; this is reproducibility, not new independent fixtures.")
