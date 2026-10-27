"""Same fresh-count comparison of full-data and held-out certificates."""
import json,math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from residual_validation import Oracle,mat,mul,inv,ab,add,sub,eye,maxrowsum,minimum,serialize,tvbox,GRID
from learner import frozen_spectral_bound

ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'residual_counts.json').read_text());q=Oracle(data['tables'])
H=q.H();Hz={(a,o):q.Hz(a,o) for a in range(2) for o in range(2)}
w=F(303,100000) # exact: confidence failure 36 exp(-9.1809)< residual method failure
dH=mat([[0,0],[w,w]]);dHz=mat([[w,w],[w,w]])
results=[]
for s in GRID:
    S=mat([[1+s,-s],[-s,1+s]])
    V=mul(H,S);U=inv(V);dV=mul(dH,ab(S));A=mul(ab(U),dV)
    if maxrowsum(A)>=1:continue
    M=mul(inv(sub(eye(),A)),ab(U))
    W={z:mul(mul(U,v),S) for z,v in Hz.items()}
    E={z:mul(M,add(mul(dHz,ab(S)),mul(dV,ab(W[z])))) for z in W}
    margin=min(minimum(sub(W[z],E[z])) for z in W)
    if margin<0:continue
    t=max(tvbox([W[a,o][i][j] for o in range(2) for i in range(2)],
                [E[a,o][i][j] for o in range(2) for i in range(2)]) for a in range(2) for j in range(2))
    results.append({'s':s,'margin':margin,'local_tv':t,'one_macro_tv':3*t/(2+3*t)})
best=min(results,key=lambda r:(r['local_tv'],-r['margin']))
N=min(t['shots'] for t in data['tables']);exponent=2*N*w*w
out={'same_fresh_dataset':True,'no_additional_shots':True,
     'full_data_width':w,'full_data_confidence_failure':36*math.exp(-float(exponent)),
     'full_data_selected':best,
     'held_out_selected':json.loads((ROOT/'residual_certificate.json').read_text())['selected'],
     'spectral':frozen_spectral_bound(np.array(H,dtype=float),np.array(dH,dtype=float),
        {z:np.array(v,dtype=float) for z,v in Hz.items()},
        {z:np.array(dHz,dtype=float) for z in Hz})}
(ROOT/'variant_comparison.json').write_text(json.dumps(serialize(out),indent=2)+'\n')
print(json.dumps(serialize({k:out[k] for k in ['full_data_confidence_failure','full_data_selected','spectral']}),indent=2))
