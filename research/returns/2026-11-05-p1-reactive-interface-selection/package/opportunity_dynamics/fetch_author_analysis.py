"""Fetch the externally maintained author-analysis dependency, verify, then save.
This script downloads only; it does not execute the downloaded program.
"""
from pathlib import Path
import hashlib,urllib.request
url='https://raw.githubusercontent.com/cwlindeman/shear-cell-data/master/trackParticlesAndStrains.py'
expected='119e47aa1057a062d83be67aa7aeb5aa9f47b02c0f10ee231e1f2528d1b0cf88'
with urllib.request.urlopen(url,timeout=45) as r:data=r.read()
if hashlib.sha256(data).hexdigest()!=expected:
    raise RuntimeError('Author source changed; recover the recorded revision before reproduction.')
p=Path(__file__).resolve().parent/'trackParticlesAndStrains.py'
p.write_bytes(data)
print(p)
