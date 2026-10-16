from pathlib import Path
import hashlib,json,sys
r=Path(__file__).resolve().parent
if len(sys.argv)!=3: raise SystemExit('Usage: verify_dependencies.py COHERENT_PACKET.zip FINITE_DURATION_PACKET.zip')
for p,d in zip(sys.argv[1:],json.loads((r/'DEPENDENCIES.json').read_text())['prior_delivered_packets']):
 b=Path(p).read_bytes()
 if len(b)!=d['size_bytes'] or hashlib.sha256(b).hexdigest()!=d['sha256']: raise RuntimeError('Dependency mismatch: '+d['filename'])
 print('PASS:',d['filename'])
