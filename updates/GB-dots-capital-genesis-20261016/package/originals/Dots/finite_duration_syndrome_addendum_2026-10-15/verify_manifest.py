from pathlib import Path
import hashlib
r=Path(__file__).resolve().parent
n=0
for line in (r/'SHA256SUMS').read_text().splitlines():
 h,name=line.split('  ',1); p=(r/name).resolve()
 if not p.is_relative_to(r): raise RuntimeError('Unsafe manifest path')
 if hashlib.sha256(p.read_bytes()).hexdigest()!=h: raise RuntimeError('Hash mismatch: '+name)
 n+=1
print('PASS:',n,'manifest entries verified')
