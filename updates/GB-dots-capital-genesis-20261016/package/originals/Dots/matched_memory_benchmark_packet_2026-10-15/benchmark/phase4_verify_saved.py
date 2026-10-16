from independent_audit import *
import hashlib
rows=json.loads((ROOT/'phase4_readout_results.json').read_text())
for line in (ROOT/'PHASE4_ENDPOINT_SHA256SUMS').read_text().splitlines():
 digest,name=line.split();assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest
for method in ('sweep','toom'):
 data=json.loads((ROOT/f'phase4_endpoint_{method}.json').read_text());L=data['L']
 assert data['format']=='4d-memory-endpoint-v1' and (L,data['alpha'],data['T'],data['seed'])==(32,.001,5,101)
 E={decode_id(i,L,2) for i in data['E']};S={decode_id(i,L,1) for i in data['S']};assert bd(E,L)==S
 for policy in range(3):
  r=json.loads((ROOT/f'phase4_recovery_{method}_D{policy}.json').read_text());D={decode_id(i,L,2) for i in r['R']};assert bd(D,L)==S
  C=E^D;assert not bd(C,L);h=hom(C);mask=sum(1<<ORI.index(a) for a in h)
  row=next(v for v in rows if v['method']==method and v['policy']==f'D{policy}');assert mask==row['logical_bits'] and len(D)==row['recovery_faces'] and len(C)==row['residual_faces']
  for cut in (1,L-1):assert hom(C,cut)==h
res={'status':'PASS','saved_endpoint_boundaries':2,'saved_recovery_boundary_and_score_checks':6,'content_hashes':'all matched','homology_cuts':[0,1,31]}
(ROOT/'phase4_saved_independent_verification.json').write_text(json.dumps(res,indent=2));print(json.dumps(res))
