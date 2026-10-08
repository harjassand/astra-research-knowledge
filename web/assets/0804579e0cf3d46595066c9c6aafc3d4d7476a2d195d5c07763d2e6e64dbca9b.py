#!/usr/bin/env python3
"""Run bundled checks in a temporary copy without changing archived results.

Default: standard-library checks. --optional also runs SymPy/SciPy diagnostics
when those packages are already installed. Nothing is installed or downloaded.
Finite exact tests and floating-point diagnostics are not asymptotic proofs.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--optional',action='store_true')
a=p.parse_args()
source=Path(__file__).resolve().parent
scripts=[
 ('contact_audit/independent_audit.py',None),
 ('contact_audit/audit_nanson.py',None),
 ('entropy_audit/independent_checks.py',None),
 ('proof_mining/check_char2_support.py',None),
 ('hf_audit/test_encoding.py',None),
]
if a.optional:
 scripts.extend([
  ('contact/test_diagonal_determinant.py','sympy'),
  ('frontier/check_factorial_grouped_entropy.py','scipy'),
 ])
report={'python':sys.version.split()[0],'checks':[]}
with tempfile.TemporaryDirectory(prefix='astra-reproduction-') as td:
 target=Path(td)/'record'
 shutil.copytree(source,target)
 for rel,dep in scripts:
  item={'script':rel}
  if not (target/rel).is_file():
   item['status']='not included'
  elif dep and importlib.util.find_spec(dep) is None:
   item.update(status='skipped',reason='Optional dependency is not installed: '+dep)
  else:
   started=time.monotonic()
   r=subprocess.run([sys.executable,str(target/rel)],cwd=target,capture_output=True,text=True)
   item.update(status='passed' if r.returncode==0 else 'failed',exit_code=r.returncode,seconds=round(time.monotonic()-started,3),stdout=r.stdout,stderr=r.stderr)
  report['checks'].append(item)
  print(rel+': '+item['status'],file=sys.stderr)
print(json.dumps(report,indent=2))
sys.exit(1 if any(x['status']=='failed' for x in report['checks']) else 0)
