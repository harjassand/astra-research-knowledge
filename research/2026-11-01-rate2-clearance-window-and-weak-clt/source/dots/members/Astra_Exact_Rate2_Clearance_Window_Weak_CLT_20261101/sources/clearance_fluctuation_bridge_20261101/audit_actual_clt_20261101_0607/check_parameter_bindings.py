from pathlib import Path
import hashlib,json
here=Path(__file__).resolve().parent;root=here.parents[1]
requests=[('inverse_clearance_clock_20261101/SCALAR_FREEZE.json','11c22f296fadc36a5374c5bfab2c7b214a3c2a77ea27f3a5910055f93027b4a5'),('audit_inverse_clock_certificate_20261101/RECEIPT_BINDINGS.json','e6d5fbaf44968a7096eac0abacfb27278247c2853ec8eec9ca327d6694fa5cab'),('inverse_clock_variance_20261101/VARIANCE_FREEZE.json','60636c65f720823168088f2b97760d5473f3fe5b51c6388369fedd1ada456129'),('audit_inverse_clock_variance_20261101/RECEIPT_BINDINGS.json','daaa7535453b6b4934143d4f186a200c5a3f2b3f32cc03a958371e5a57115076')]
checks=[]
for rel,expected in requests:
 p=root/rel;data=p.read_bytes();assert hashlib.sha256(data).hexdigest()==expected
 bound=[]
 for e in json.loads(data)['files']:
  q=p.parent/e['path'];d=q.read_bytes();assert hashlib.sha256(d).hexdigest()==e['sha256']
  if 'bytes' in e:assert len(d)==e['bytes']
  bound.append({'path':str(q.relative_to(root)),'sha256':e['sha256'],'bytes':len(d)})
 checks.append({'manifest':rel,'sha256':expected,'files':bound})
out={'status':'PASS_EXACT_PREVIOUS_DETERMINISTIC_FREEZE_AND_RECEIPT_BINDINGS','checked_payload_bindings':sum(len(x['files']) for x in checks),'manifests':checks,'scope':'Byte readback and mathematical identification of the same functional; previous deterministic numerical replay is received, not rerun or expanded to moments.'}
(here/'PARAMETER_BINDING_READBACK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'checked_payload_bindings':out['checked_payload_bindings']},indent=2))
