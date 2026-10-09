"""Check the stronger, exactly fixed-reference, coherent lower construction.
Floating point diagnostic. The Schur-complement positivity/reference identities
are symbolic in the companion proof; this script is not their certification.
"""
from pathlib import Path
import json
import numpy as np
from quantum_choi_formula_probe import apply_blocks, ptrace_blocks

def cross_bkm(c,b,tau,p):
    vals,u=np.linalg.eigh(c)
    mask=vals>1e-12
    vals=vals[mask];u=u[:,mask]
    nu,v=np.linalg.eigh(tau)
    entries=u.conj().T@b@v
    q=1-p
    x=q*vals[:,None]; y=p*nu[None,:]
    diff=np.log(x)-np.log(y)
    divided=diff/(x-y)
    return float(2*p*q*np.sum(np.abs(entries)**2*divided))

if __name__=='__main__':
    data=np.load(Path(__file__).with_name('quantum_choi_formula_probe.npz'))
    c,b,dd=data['c'],data['b'],data['d']
    n,d=4,2; tau=np.eye(2)/2
    nc=apply_blocks(c,n,d,.5); nb=apply_blocks(b,n,d,.5)
    vals=[]
    for p in [1e-2,1e-5,1e-10,1e-20,1e-40,1e-80]:
        gi=cross_bkm(c,b,tau,p);go=cross_bkm(nc,nb,tau,p)
        vals.append({'p':p,'fixed_reference_BKM_ratio':go/gi})
    # Check a pair of actual states, with exactly unchanged marginal analytically.
    p=.03;t=.2;q=1-p
    def state(t):return np.block([[q*c,t*np.sqrt(p*q)*b],[t*np.sqrt(p*q)*b.conj().T,p*(t*t*dd+(1-t*t)*tau)]])
    plus,minus=state(t),state(-t)
    out={'status':'NUMERICAL ONLY','target':.375,'asymptotic_ratios':vals,
      'minimum_pair_eigenvalue':float(min(np.linalg.eigvalsh(plus)[0],np.linalg.eigvalsh(minus)[0])),
      'pair_reference_difference_norm':float(np.linalg.norm(ptrace_blocks(plus,d)-ptrace_blocks(minus,d))),
      'pair_trace':float(np.trace(plus).real)}
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
