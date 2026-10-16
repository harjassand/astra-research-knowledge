from pathlib import Path
import json,hashlib,sys
r=Path(__file__).resolve().parent
deps=json.loads((r/'DEPENDENCIES.json').read_text())['prior_packets']
if len(sys.argv)!=len(deps)+1:raise SystemExit('Provide all three older ZIPs in dependency-list order')
for p,d in zip(sys.argv[1:],deps):
 b=Path(p).read_bytes()
 if len(b)!=d['size_bytes'] or hashlib.sha256(b).hexdigest()!=d['sha256']:raise RuntimeError('Dependency mismatch: '+d['filename'])
 print('PASS:',d['filename'])
