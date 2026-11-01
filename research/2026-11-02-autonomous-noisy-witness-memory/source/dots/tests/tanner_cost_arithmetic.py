"""Reproduce conservative proof-cost arithmetic, NOT validate code instances."""
import math,json

def entropy(x):
    return -x*math.log2(x)-(1-x)*math.log2(1-x)

def inverse_entropy(y):
    lo,hi=1e-300,0.5
    for _ in range(200):
        mid=(lo+hi)/2
        if entropy(mid)<y:lo=mid
        else:hi=mid
    return (lo+hi)/2

rho=.25; delta=.03; epsilon=1/12
rob=.5*min(.25*inverse_entropy(rho/8)*inverse_entropy((1-rho)/8),
           inverse_entropy(rho*(1-rho)/8))
A=1+1/(rob*(1-epsilon)); alpha=delta**2*epsilon**2/1024
out={'warning':'Illustrative substitutions only; no finite Delta code verified.',
     'rho':rho,'delta':delta,'epsilon':epsilon,'source_robustness':rob,
     'A':A,'alpha':alpha,
     'one_conservative_large_degree_comparison':8192/(3*alpha**3*rob**2*epsilon**2),
     'rows':[]}
for D in (16,32,100,1000):
    d0=D*D; K=8*d0*d0+2*d0+1
    r=2**-12*delta**2*epsilon**3*rob/(4*A*D**3*(1+2*d0))
    w=r/(8*d0); bnoise=4*(d0+1)
    out['rows'].append({'unverified_Delta':D,'basin_fraction':r,
       'boundary_potential_density':w,'linearized_noise_rate_scale':w/(5*K*bnoise),
       'lookup_entries_log2':d0,'candidate_codewords_log2':13*d0/16})
print(json.dumps(out,indent=2))
