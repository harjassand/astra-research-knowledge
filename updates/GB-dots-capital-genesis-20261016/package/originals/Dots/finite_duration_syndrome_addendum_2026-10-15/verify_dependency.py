from pathlib import Path
import hashlib,json,sys
r=Path(__file__).resolve().parent
if len(sys.argv)!=2: raise SystemExit('Usage: python3 verify_dependency.py PRIOR_PACKET.zip')
d=json.loads((r/'DEPENDENCY.json').read_text()); b=Path(sys.argv[1]).read_bytes()
if len(b)!=d['size_bytes'] or hashlib.sha256(b).hexdigest()!=d['sha256']: raise RuntimeError('Dependency mismatch')
print('PASS: exact prior delivered packet verified')
