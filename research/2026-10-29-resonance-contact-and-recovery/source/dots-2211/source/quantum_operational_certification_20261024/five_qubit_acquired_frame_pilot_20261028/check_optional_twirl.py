#!/usr/bin/env python3
"""Exact post hoc algebra check; no new samples or executed deployment."""
from pathlib import Path
import json,hashlib
import sympy as s
p=Path(__file__).parent
out={'scope':'Exact algebra on saved logical channels; no new experiment','banks':[]}
chars=[s.diag(1,1,1,1),s.diag(1,1,-1,-1),s.diag(1,-1,1,-1),s.diag(1,-1,-1,1)]
for N in [4096,16384]:
 src=p/f'exact_channels_N{N}.json';M=s.Matrix([[s.Rational(x) for x in row] for row in json.loads(src.read_text())['logical_PTM']]);T=sum((C*M*C for C in chars),s.zeros(4))/4
 assert T==s.diag(*M.diagonal()) and T[0,0]==1
 x,y,z=[T[j,j] for j in [1,2,3]]
 probs=[(1+x+y+z)/4,(1+x-y-z)/4,(1-x+y-z)/4,(1-x-y+z)/4]
 assert all(v>=0 for v in probs) and sum(probs)==1
 Fe=(1+sum(M[j,j] for j in [1,2,3]))/4
 assert Fe==probs[0]
 out['banks'].append({'calibration_N':N,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'exact_pauli_probabilities':list(map(str,probs)),'reference_complete_half_diamond_posthoc':float(1-probs[0]),'entanglement_fidelity_invariant':True,'certificate_bound_not_score':'.001 conditional on validated simultaneous event and nominal twirl implementation'})
out['source_sha256']=hashlib.sha256((p/'OPTIONAL_LOGICAL_TWIRL_COROLLARY.md').read_bytes()).hexdigest()
(p/'optional_twirl_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='banks'},indent=2))
