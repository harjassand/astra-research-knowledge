from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
count=0
for line in (root/'SHA256SUMS').read_text().splitlines():
    expected,name=line.split('  ',1)
    p=(root/name).resolve()
    if not p.is_relative_to(root): raise RuntimeError('Unsafe manifest path')
    if hashlib.sha256(p.read_bytes()).hexdigest()!=expected: raise RuntimeError('Hash mismatch: '+name)
    count+=1
print('PASS:',count,'manifest entries verified')
