"""Calibration-fit prediction only; no new experiment or loss-aware certificate."""
import numpy as np,json,hashlib
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'data'
keys=['AA','AD','DA','DD']
E=np.array([np.loadtxt(p/f'figure4_dm_{k}.csv',delimiter=',',dtype=complex) for k in keys])
I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);b=np.sqrt(.405);r=6/11;z=9/11
# Columns: Phi+,Phi-,Psi+,Psi- in computational 00,01,10,11.
B=np.array([[1,1,0,0],[0,0,1,1],[0,0,1,-1],[1,-1,0,0]])/np.sqrt(2)
rhos=[sum(np.kron((I+b*Z+i*b*X)/2,(I+ell*i*r*X+z*Z)/2) for i in [-1,1])/2 for ell in [-1,1]]
P=np.array([[np.trace(e@B.T@rho@B).real for e in E] for rho in rhos])
a=np.array([b*r/(1+b*z),-b*r/(1+b*z),b*r/(1-b*z),-b*r/(1-b*z)])
risk=lambda a: sum(np.sum(P[k]*(a-ell)**2)/2 for k,ell in enumerate([-1,1]))
af=(P[1]-P[0])/P.sum(0)
result={'basis':['Phi+','Phi-','Psi+','Psi-'],'outcomes':keys,'conditional_probabilities_labels_minus_plus':P.tolist(),'ideal_fixed_scores':a.tolist(),'fixed_score_risk':float(risk(a)),'source_ideal_risk':524/605,'source_minus_fixed_risk':float(524/605-risk(a)),'calibration_refit_scores':af.tolist(),'calibration_refit_risk':float(risk(af)),'source_minus_refit_risk':float(524/605-risk(af)),'effect_eigenvalues':np.linalg.eigvalsh(E).tolist(),'completeness_operator_norm':float(np.linalg.norm(E.sum(0)-np.eye(4),2)),'hermiticity_max_abs':float(abs(E-E.conj().transpose(0,2,1)).max())}
(p/'welte_risk_prediction.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
r=json.load(open(p/'welte2021_record.json'))
checks={}
for f in r['files']:
 if (p/f['key']).exists():
  h=hashlib.md5((p/f['key']).read_bytes()).hexdigest();checks[f['key']]={'md5':h,'matches_archive':f['checksum']=='md5:'+h,'url':f['links']['self']}
(p/'welte_checksums.json').write_text(json.dumps(checks,indent=2))
