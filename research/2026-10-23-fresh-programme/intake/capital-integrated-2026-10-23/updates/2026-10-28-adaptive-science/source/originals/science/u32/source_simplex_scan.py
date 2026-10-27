"""Count-only finite gauge scan of the exact pinned original qubit fixture."""
import json,sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'source_counts'))
from finite_predictive_learner import learn,CountOracle

data=json.loads((ROOT/'source_counts/calibration_counts.json').read_text())
model=learn(data);q=CountOracle(data);ps=model['preparations'];fs=model['tests'];H=model['H']
dH=np.array([[q.cell(p,f)[1] for p in ps] for f in fs]);Hz={};dHz={}
for a in range(4):
    for o in range(2):
        z=((a,o),)
        Hz[a,o]=np.array([[q.cell(p,f,z)[0] for p in ps] for f in fs])
        dHz[a,o]=np.array([[q.cell(p,f,z)[1] for p in ps] for f in fs])
results=[]
for k in [.5,.75,1,1.25,1.5,2,3,4,6,8,12]:
    S=k*np.eye(4)+(1-k)*np.ones((4,4))/4
    V=H@S;U=np.linalg.inv(V);dV=dH@abs(S);A=abs(U)@dV
    rho=max(abs(np.linalg.eigvals(A)))
    W={z:U@v@S for z,v in Hz.items()};raw_margin=min(v.min() for v in W.values())
    margin=None
    if rho<1:
        M=np.linalg.solve(np.eye(4)-A,abs(U))
        E={z:M@(dHz[z]@abs(S)+dV@abs(W[z])) for z in W}
        margin=min(np.min(W[z]-E[z]) for z in W)
    c=np.linalg.solve(S,np.array([1.,0,0,0]))
    results.append(dict(expansion=k,raw_margin=float(raw_margin),
       certified_margin=None if margin is None else float(margin),
       initial_min=float(c.min()),inverse_radius=float(rho)))
out={'source_fixture':'Frozen original qubit counts, no new acquisition',
     'candidates':results,'governing_confidence':model['certificate']}
(ROOT/'source_simplex_scan.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passing_candidates':sum(c['certified_margin'] is not None and c['certified_margin']>=0 and c['initial_min']>=0 for c in results),
                  'best_raw_margin':max(c['raw_margin'] for c in results)},indent=2))
