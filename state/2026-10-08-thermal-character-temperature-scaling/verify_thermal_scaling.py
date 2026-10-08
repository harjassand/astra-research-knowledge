"""Compute exact sector-summed trace distance to the fully mixed state.
This is an UPPER BOUND on distance to fully separable states, not that distance.
"""
import json
import numpy as np
from scipy.special import gammaln, logsumexp

def tv_to_fully_mixed(N, nu):
    assert nu>0
    beta=np.log1p(1./nu)
    twj=np.arange(N%2,N+1,2, dtype=float)
    j=twj/2
    k=((N-twj)/2).astype(int)
    log_binom=gammaln(N+1)-gammaln(k+1)-gammaln(N-k+1)
    log_w=2*np.log(twj+1)+log_binom-N*np.log(2)-np.log(N/2+j+1)
    w=np.exp(log_w-logsumexp(log_w))
    distances=[]
    for ji in j:
        mm=np.arange(-ji,ji+1)
        t=-beta*mm
        p=np.exp(t-logsumexp(t))
        distances.append(0.5*np.abs(p-1./len(mm)).sum())
    d=np.dot(w,distances)
    bound=0.25*np.sqrt(3*N)*beta
    return {'N':N,'nu':nu,'tv_to_fully_mixed':float(d),'proven_upper_bound':float(bound),'under_bound':bool(d<=bound+1e-9)}

if __name__=='__main__':
    rows=[tv_to_fully_mixed(N, N**alpha) | {'alpha':alpha} for N in (16,64,256,1024,4096) for alpha in (0.25,0.5,0.75)]
    if not all(x['under_bound'] for x in rows):raise RuntimeError('Analytic upper bound was violated in finite check')
    for alpha in (0.25,0.5,0.75):
        print(f'nu=N^{alpha}:', [(r['N'],round(r['tv_to_fully_mixed'],5)) for r in rows if r['alpha']==alpha])
    print('All 15 exact sector-summed checks obey beta sqrt(3N)/4 upper bound')
    with open('thermal_scaling_checks.json','w') as f:json.dump(rows,f,indent=2)
