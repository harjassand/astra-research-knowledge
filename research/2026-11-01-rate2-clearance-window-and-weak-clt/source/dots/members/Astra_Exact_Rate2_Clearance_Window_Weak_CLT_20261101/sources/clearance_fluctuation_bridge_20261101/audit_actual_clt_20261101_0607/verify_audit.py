#!/usr/bin/env python3
"""Read-only audit verification; regenerated checker outputs live in temporary dirs.
Default is self-contained snapshot/replay verification. --original-root also
checks all 38 original paths and all 63 separately received parameter pins.
"""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
here=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--original-root',type=Path);args=p.parse_args()
manifest=json.loads((here/'AUDIT_SHA256.json').read_text());n=0
for entry in manifest['files']:
 q=here/entry['path'];data=q.read_bytes()
 assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'],q
 n+=1
sources=json.loads((here/'SOURCE_READBACK.json').read_text())['files']
for entry in sources:
 data=(here/'snapshot'/entry['path']).read_bytes()
 assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256']
 if args.original_root:
  data=(args.original_root/entry['path']).read_bytes()
  assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256']
parameter_n=0
if args.original_root:
 for block in json.loads((here/'PARAMETER_BINDING_READBACK.json').read_text())['manifests']:
  data=(args.original_root/block['manifest']).read_bytes();assert hashlib.sha256(data).hexdigest()==block['sha256']
  for entry in block['files']:
   data=(args.original_root/entry['path']).read_bytes()
   assert len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256']
   parameter_n+=1
with tempfile.TemporaryDirectory(prefix='clt_independent_readonly_') as tmp:
 tmp=Path(tmp)
 shutil.copy2(here/'independent_check.py',tmp/'independent_check.py')
 result=subprocess.run([sys.executable,str(tmp/'independent_check.py')],check=True,capture_output=True,text=True)
 actual=(tmp/'INDEPENDENT_CHECK_RESULTS.json').read_bytes()
 assert actual==(here/'INDEPENDENT_CHECK_RESULTS.json').read_bytes()
 independent=json.loads(actual)['checks']
 shutil.copy2(here/'author_replay/check_tail_envelopes.py',tmp/'check_tail_envelopes.py')
 subprocess.run([sys.executable,str(tmp/'check_tail_envelopes.py')],check=True,capture_output=True,text=True)
 actual=(tmp/'TAIL_CHECK_RESULTS.json').read_bytes()
 assert actual==(here/'author_replay/TAIL_CHECK_RESULTS.json').read_bytes()
 assert actual==(here/'snapshot/clearance_fluctuation_bridge_20261101/TAIL_CHECK_RESULTS.json').read_bytes()
 author=json.loads(actual)['checks']
print(json.dumps({'status':'PASS_IMMUTABLE_BINDINGS_AND_EXACT_ISOLATED_REPLAYS','audit_payloads':n,'snapshot_sources':len(sources),'original_sources_checked':len(sources) if args.original_root else 0,'original_parameter_pins_checked':parameter_n,'independent_exact_assertions':independent,'author_exact_assertions':author,'numerical_parameter_solvers_rerun':False},indent=2))
