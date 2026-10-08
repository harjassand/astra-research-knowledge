"""Fresh small-system diagnostic for Astra N109/N110: not a proof.
Computes spectral gaps and the positivity/amplitude-floor implication.
"""
import json
import numpy as np
from itertools import combinations
from scipy.linalg import eigh

X=np.array([[0,1],[1,0]],float)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.]); I=np.eye(2)

def op(n, sites):
    out=np.array([[1.]],complex)
    for i in range(n):
        out=np.kron(out, sites.get(i,I))
    return out

def instance(n,rng):
    edges=[]
    H=np.zeros((2**n,2**n),complex)
    V=0.; c=0.
    for i,j in combinations(range(n),2):
        if rng.uniform()<0.65:
            f=float(10**rng.uniform(-1.2,0.8))
            d=f*float(rng.uniform(-1.,1.))
            H+=.5*d*op(n,{i:Z,j:Z})-.5*f*(op(n,{i:X,j:X})+op(n,{i:Y,j:Y}))
            V+=f+max(d,0.); c+=abs(d)/2
            edges.append([i,j,f,d])
    g=np.array([10**rng.uniform(-1.5,0.35) for _ in range(n)])
    h=np.array([rng.uniform(-2,2) for _ in range(n)])
    for i in range(n):
        H+=h[i]*op(n,{i:Z})-g[i]*op(n,{i:X})
        V+=2*abs(h[i])+g[i]; c+=abs(h[i])
    return H,V,c,g,h,edges

def run(seed=20261008):
    rng=np.random.default_rng(seed)
    trials={2:30,3:30,4:30,5:30,6:15}
    minimum_ratio=float('inf'); maximum_viol=0.; worst=None
    for n, count in trials.items():
        for r in range(count):
            H,V,c,g,h,edges=instance(n,rng)
            values,vs=eigh(H)
            Delta=float(values[1]-values[0]); rmin=float(g.min())
            ratio=Delta/(2*rmin)
            u=vs[:,0]; u=np.real_if_close(u).real
            if u.sum()<0: u=-u
            gamma=2**(-n/2)*(rmin/V)**n
            A=c*np.eye(2**n)-H.real
            if min(np.ravel(A)) < -1e-12:
                raise RuntimeError('Generator negative coefficient')
            if min(u)<-1e-9: raise RuntimeError('Ground not PF positive')
            if ratio < minimum_ratio: minimum_ratio=ratio; worst={'n':n,'trial':r,'gap':Delta,'gmin':rmin,'ratio':ratio,'V':V,'edges':len(edges)}
            if min(u) +1e-13 < gamma: raise RuntimeError('Hypercube PF floor violated')
            maximum_viol=max(maximum_viol, max(0., gamma-min(u)))
    return {'seed':seed,'number_of_trials':sum(trials.values()),'trial_count_by_qubits':trials,'gap_ratio_min':minimum_ratio,'worst_gap_case':worst,'generator_positivity_and_PF_floor':'all checks passed','max_positive_floor_deficit':maximum_viol,'limitations':'Random finite-dimensional tests only; no proof of spectral gap or complexity theorem.'}
if __name__=='__main__':
    outcome=run()
    print(json.dumps(outcome,indent=2))
    with open('quantum_checks.json','w') as f: json.dump(outcome,f,indent=2)
