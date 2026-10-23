"""Finite actual rank-three orbit test against ALL classical placements."""
import os
for k in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[k]="1"
import itertools,json,math,time
from fractions import Fraction
from pathlib import Path
import numpy as np
OUT=Path(__file__).resolve().parent;START=time.perf_counter();CPU=time.process_time()
rng=np.random.default_rng(2026102203);q=16;n=4;C=np.sqrt([.6,.3,.1]);m=math.log(2)
sites_list=[[0],[0,1],[2],[2,3]]

def classical_entry(x,y):
    val=Fraction(0)
    for sites in sites_list:
        if all(((x>>(3-j))&1)==((y>>(3-j))&1) for j in range(4) if j not in sites):
            val+=Fraction(1,2**len(sites))
    return val
A=[[classical_entry(x,y) for y in range(16)] for x in range(16)]
M=10**50
def root_interval(f):
    k=math.isqrt(f.numerator*M*M//f.denominator)
    return Fraction(k,M),Fraction(k+1,M)
roots=[root_interval(Fraction(18,100)),root_interval(Fraction(6,100)),root_interval(Fraction(3,100))]
def score_interval(triple):
    return tuple(Fraction(3,2)+2*sum((a*root[e] for a,root in zip(triple,roots)),Fraction(0)) for e in (0,1))
triples={};count=0
for placement in itertools.permutations(range(16),3):
    x,y,z=placement;triple=(A[x][y],A[x][z],A[y][z]);count+=1
    triples.setdefault(triple,placement)
best=max(triples,key=lambda t:score_interval(t)[0]);lo,hi=score_interval(best)
competitor_upper=max(score_interval(t)[1] for t in triples if t!=best)
assert lo>competitor_upper
best_placement=triples[best];classical=float(lo)

def E(X,sites):
    R=X.reshape([2]*8);left=4
    for j in sorted(sites,reverse=True):R=np.trace(R,axis1=j,axis2=j+left);left-=1
    R=R.reshape(2**left,2**left);rest=[j for j in range(4) if j not in sites]
    old=sites+rest;inverse=np.argsort(old)
    full=np.kron(np.eye(2**len(sites))/2**len(sites),R).reshape([2]*8)
    return full.transpose(list(inverse)+[j+4 for j in inverse]).reshape(16,16)
def energy(V):
    X=(V*C)@V.conj().T;L=sum((E(X,s) for s in sites_list),np.zeros_like(X))
    return float(np.vdot(X,L).real),X,L
records=[];best_actual=None
# Fixed eight random complex isometries, plus exact best classical state.
starts=[]
V=np.eye(16,dtype=complex)[:,best_placement];starts.append(("best_classical",V))
for k in range(8):
    V=np.linalg.qr(rng.normal(size=(16,3))+1j*rng.normal(size=(16,3)))[0]
    starts.append((f"random_isometry_{k}",V))
for name,V in starts:
    f,X,L=energy(V);initial=f;steps=0;grad_norm=0.0
    for iteration in range(220):
        if time.process_time()-CPU>8:break
        G=4*(L@V)*C
        inner=V.conj().T@G;G-=V@((inner+inner.conj().T)/2)
        grad_norm=float(np.linalg.norm(G))
        if grad_norm<1e-9:break
        eta=.25;accepted=False
        for backtrack in range(15):
            candidate=np.linalg.qr(V+eta*G)[0];nf,nX,nL=energy(candidate)
            if nf>=f+1e-4*eta*grad_norm**2:
                V,f,X,L=candidate,nf,nX,nL;accepted=True;steps+=1;break
            eta*=.5
        if not accepted:break
    rec=dict(start=name,initial_score=initial,final_score=f,score_excess_over_best_classical=f-classical,
             steps=steps,gradient_norm=grad_norm,unitarity_error=float(np.linalg.norm(V.conj().T@V-np.eye(3))))
    records.append(rec)
    if best_actual is None or f>best_actual[0]:best_actual=(f,V.copy(),X.copy())
np.savez_compressed(OUT/"RANK3_BEST_ACTUAL.npz",V=best_actual[1],X=best_actual[2],lambda_values=np.array([.6,.3,.1]))
result=dict(D=2,r=2,N=2,spectrum=[.6,.3,.1],classical_placements_enumerated=count,
            distinct_classical_coefficient_triples=len(triples),best_classical_placement=best_placement,
            best_cross_coefficients=list(map(str,best)),
            exact_best_score="3/2+2*("+"+".join(f"({a})*sqrt({p})" for a,p in zip(best,["18/100","6/100","3/100"]))+")",
            certified_best_interval=[str(lo),str(hi)],certified_positive_separation_from_other_triples=str(lo-competitor_upper),
            classical_score=classical,actual_orbit_search=records,
            maximum_observed_excess=best_actual[0]-classical,
            universal_domination="NOT_ESTABLISHED; no finite actual counterexample found by these bounded starts",
            body_wall_seconds=time.perf_counter()-START,body_CPU_seconds=time.process_time()-CPU,
            BLAS_threads=1)
assert result["body_CPU_seconds"]<10
(OUT/"RANK3_ROUTE_RESULT.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
