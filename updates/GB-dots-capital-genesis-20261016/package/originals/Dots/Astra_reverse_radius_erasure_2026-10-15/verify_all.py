"""Verify integrity and run portable exact research checks."""
from pathlib import Path
import hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parent
for line in (ROOT/'SHA256SUMS').read_text().splitlines():
    expected,name=line.split('  ',1)
    if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=expected:
        raise SystemExit('SHA-256 mismatch: '+name)
print('PASS: SHA-256 manifest',flush=True)
checks=sorted((ROOT/'checks').glob('*.py'))
for script in checks:
    print('Checking '+script.name,flush=True)
    subprocess.run([sys.executable,str(script)],check=True)
print('PASS: '+str(len(checks))+' exact check scripts',flush=True)
