from __future__ import annotations
import json,time
from pathlib import Path
from itertools import combinations
import numpy as np
from scipy.linalg import expm,block_diag
from certificates import thermal_statistics,coherence_budget,histogram_interval,confidence_interval
OUT=Path(__file__).resolve().parent
rng=np.random.default_rng(932174); checks=0; worst=0.0
for trial in range(160):
    k=int(rng.integers(2,6)); dims=rng.integers(1,7,size=k); n=int(sum(dims))
    labels=np.repeat(np.arange(k),dims); off=np.r_[0,np.cumsum(dims)]; blocks=[]
    for d in dims:
        a=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)); blocks.append((a+a.conj().T)*.35)
    D=block_diag(*blocks); T=np.zeros((n,n),complex); g=np.zeros((k,k))
    for i in range(k):
        for j in range(i+1,k):
            a=rng.normal(size=(dims[i],dims[j]))+1j*rng.normal(size=(dims[i],dims[j]))
            a*=rng.uniform(.001,.25)/np.linalg.norm(a,2)
            T[off[i]:off[i+1],off[j]:off[j+1]]=a
            T[off[j]:off[j+1],off[i]:off[i+1]]=a.conj().T
            g[i,j]=g[j,i]=np.linalg.norm(a,2)
    beta=float(rng.uniform(.2,2)); H=D+T
    z=np.array([np.trace(expm(-beta*a)).real for a in blocks]); EH=expm(-beta*H)
    c=np.array([np.trace(EH[off[i]:off[i+1],off[i]:off[i+1]]).real for i in range(k)])
    u=np.diag(expm(np.diag(np.log(z))+beta*g)).real
    assert min(c-z)>-1e-8 and min(u-c)>-1e-8, ('block bound',trial)
    C,eta=coherence_budget(g,beta); assert c.sum()<=C*z.sum()+1e-8
    F,p=thermal_statistics(H,beta,labels,k)
    for _ in range(4):
        v=rng.uniform(-4,4,size=k); Fv,_=thermal_statistics(H+np.diag(v[labels]),beta,labels,k)
        lo,hi=histogram_interval(p,v,beta,C); slack=min(Fv-F-lo,hi-(Fv-F)); worst=min(worst,slack)
        assert slack>-1e-9, ('reweighting',trial,lo,Fv-F,hi)
        checks+=1
print('random block tests',checks,'passed',flush=True)

# Eight-site 2x4 repulsive Hubbard implementation control, canonical Nup=Ndown=3.
# This is not a measured material or a hard-system speedup benchmark.
start=time.perf_counter(); L=8; Nu=Nd=3; U=8.; weak=.025; beta=2.; bias=-2.
masks=[sum(1<<i for i in c) for c in combinations(range(L),Nu)]
basis=[(u,d) for u in masks for d in masks]; lookup={s:i for i,s in enumerate(basis)}
n=len(basis); H=np.zeros((n,n)); labels=np.array([u&1 for u,d in basis],dtype=int)
edges=[]
for y in range(2):
    for x in range(4):
        i=4*y+x
        if x<3: edges.append((i,i+1))
        if y<1: edges.append((i,i+4))
for col,(up,dn) in enumerate(basis):
    H[col,col]=U*(up&dn).bit_count()+bias*(up&1)
    for spin in (0,1):
        mask=(up,dn)[spin]
        for i,j in edges:
            amp=weak if spin==0 and 0 in (i,j) else 1.
            for a,b in ((i,j),(j,i)):
                if (mask>>b)&1 and not (mask>>a)&1:
                    mid=((1<<max(a,b))-1)^((1<<(min(a,b)+1))-1)
                    sign=-1 if (mask&mid).bit_count()%2 else 1
                    new=mask^(1<<a)^(1<<b)
                    state=(new,dn) if spin==0 else (up,new)
                    H[lookup[state],col]+=-amp*sign
assert np.max(abs(H-H.T))<1e-14
F,p=thermal_statistics(H,beta,labels,2)
kappa=(2*weak**2)**.5; C=np.cosh(beta*kappa); eta=1-1/C
# Counterfactual onsite design and independently declared scalar reference cost.
v=np.array([.3,-.7]); H1=H+np.diag(v[labels]); F1,p1=thermal_statistics(H1,beta,labels,2)
interval=histogram_interval(p,v,beta,C)
assert interval[0]-1e-9<=F1-F<=interval[1]+1e-9
Nshots=30000; observed=rng.multinomial(Nshots,p); phat=observed/Nshots
stat_error=.01; ci=confidence_interval(phat,stat_error,v,beta,C)
# This seeded draw happens to be within the specified intervals; coverage is analytic.
assert np.max(abs(phat-p))<stat_error
assert ci[0]-1e-9<=F1-F<=ci[1]+1e-9
output={'random_block_matrices':160,'random_reweighting_checks':checks,'worst_negative_slack':worst,
 'hubbard_control':{'geometry':'2x4 open rectangle','sites':L,'N_up':Nu,'N_down':Nd,
 'Hilbert_dimension':n,'U_over_bulk_hopping':U,'beta_times_bulk_hopping':beta,
 'weak_up_hopping':weak,'reference_up_site0_potential':bias,'local_hybridization_norm_bound':kappa,
 'C':C,'coherent_weight_budget':eta,'reference_free_energy':F,'target_free_energy':F1,
 'reference_label_histogram':p.tolist(),'target_label_histogram':p1.tolist(),
 'counterfactual_shifts':v.tolist(),'true_free_energy_change':F1-F,
 'exact_histogram_analytic_interval_numerically_evaluated':list(interval),
 'simulated_shots':Nshots,'simulated_counts':observed.tolist(),'per_bin_error_bound':stat_error,
 'Hoeffding_failure_upper_bound':float(2*np.exp(-2*Nshots*stat_error**2)),
 'statistical_interval_numerically_evaluated':list(ci),'seconds_including_two_full_diagonalizations':time.perf_counter()-start},
 'warnings':['Random and Hubbard results use double precision.','Histogram acquisition was simulated from exact diagonalization, not performed experimentally.','The eight-site control is not a scalability or scientific-discovery benchmark.']}
(OUT/'diagnostics.json').write_text(json.dumps(output,indent=2))
print(json.dumps(output,indent=2),flush=True)

# An adaptively selected reference cost makes the information gain explicit.
# Same histogram coverage applies to the entire diagonal design family.
obj=json.loads((OUT/'diagnostics.json').read_text()); h=obj['hubbard_control']
base=h['true_free_energy_change']; exact=h['exact_histogram_analytic_interval_numerically_evaluated']
h['adaptive_design_after_threshold_calculation']={
    'declared_cost':0.975,
    'true_free_energy_change':base+0.675,
    'Gibbs_upper_from_exact_reference_histogram':0.975-h['reference_label_histogram'][1],
    'Golden_Thompson_lower_from_exact_reference_histogram':exact[0]+0.675,
    'new_exact_histogram_interval':[x+0.675 for x in exact],
    'not_an_independently_selected_material_benchmark':True}
(OUT/'diagnostics.json').write_text(json.dumps(obj,indent=2))
