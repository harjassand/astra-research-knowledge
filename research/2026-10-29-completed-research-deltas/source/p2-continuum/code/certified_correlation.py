"""Outward interval consequence of the certified two-kick record receipt."""
from pathlib import Path
import json,hashlib
from certified_continuum_kicks import I
r=Path(__file__).resolve().parent.parent
p=r/'data/certified_continuum_kicks.json'
d=json.loads(p.read_text())
a={k:I(*v['physical_exact_probability']['zero']) for k,v in d['records'].items()}
p1=a['only1']+a['both']; p2=a['only2']+a['both']
indep=p1*p2; cov=a['both']-indep
result={'source_receipt_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'input':'source |0>','port1_probability':p1.out(),'port2_probability':p2.out(),
 'actual_both_probability':a['both'].out(),'product_of_marginals':indep.out(),
 'covariance':cov.out(),'scope':'outward arithmetic consequence of certified exact-model intervals; no physical device claim'}
(r/'data/certified_joint_record_correlation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
