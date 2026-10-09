#!/usr/bin/env python3
"""Replay exact stochastic-interface tests without changing saved results."""
from pathlib import Path
import subprocess,sys
if not __debug__: raise RuntimeError('Do not use Python -O; tests rely on assertions.')
root=Path(__file__).resolve().parent
result=subprocess.run([sys.executable,str(root/'stochastic_undecidability/verify_strengthening.py')],capture_output=True,text=True,check=True)
expected=(root/'stochastic_undecidability/verification_results.txt').read_text()
if result.stdout.strip()!=expected.strip(): raise RuntimeError('Replay output differs from saved record')
print(result.stdout,end='')
print('PASS: exact replay matches saved output. Analytic theorems are not proved by these toy checks.')
