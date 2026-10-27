"""Independent occupation-basis reference; imports no worker research code."""
import os
os.environ['OPENBLAS_NUM_THREADS']='2'
from itertools import product
from pathlib import Path
import json
import math
import time
import numpy as np

def compositions(n,m):
    if m==1:
        yield (n,)
    else:
        for k in range(n+1):
            for tail in compositions(n-k,m-1):
                yield (k,)+tail

def main():
    start=time.monotonic()
    m,n=3,3
    u1,u2,t,beta=1.,-.05,1.,1.
    single=list(compositions(n,m))
    states=list(product(single,repeat=2))
    ids={x:i for i,x in enumerate(states)}
    h=np.zeros((len(states),len(states)))
    for col,(a,b) in enumerate(states):
        h[col,col]=sum(u1*(a[i]-b[i])**2+u2*(a[i]+b[i])**2 for i in range(m))
        for flavor,occ in enumerate((a,b)):
            # Each undirected edge of the three-site triangle is counted once.
            for i in range(m):
                for j in range(m):
                    if i==j or occ[j]==0: continue
                    moved=list(occ); moved[i]+=1; moved[j]-=1
                    end=(tuple(moved),b) if flavor==0 else (a,tuple(moved))
                    h[ids[end],col]+=t*math.sqrt((occ[i]+1)*occ[j])
    assert np.array_equal(h,h.T)
    e=np.linalg.eigvalsh(h)
    weights=np.exp(-beta*e)
    z=float(weights.sum()); energy=float(weights@e/z)
    out={'scope':__doc__,'modes_per_flavor':m,'particles_per_flavor':n,
         'hilbert_dimension':len(states),'parameters':{'U1':u1,'U2':u2,'t':t,'beta':beta},
         'partition_function':z,'thermal_energy':energy,'ground_energy':float(e[0]),
         'elapsed_seconds':time.monotonic()-start,
         'boundary':'Floating-point full finite-sector diagonalization, not large-system QMC accuracy or advantage.'}
    Path(__file__).resolve().with_name('INDEPENDENT_REFERENCE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
