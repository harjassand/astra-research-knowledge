"""Deterministic algebra/numerical regression tests, NOT statistical source evidence."""
import json
import numpy as np
from pathlib import Path
I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex); Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1,-1]).astype(complex)
def tr(a):return float(np.trace(a).real)
def positive(a):
    w,v=np.linalg.eigh(a);return (v*np.maximum(w,0))@v.conj().T

def pair(A,B):
    w,v=np.linalg.eigh(A-B);P=(v*(w>0))@v.conj().T
    yy=B+positive(A-B)
    return tr(P@A+(I-P)@B),P,yy

def best(ss):
    ans=(-np.inf,None,None,None)
    for a in range(len(ss)):
        for b in range(a,len(ss)):
            f,p,y=pair(ss[a],ss[b])
            if f>ans[0]:ans=(f,(a,b),p,y)
    return ans

def pure(v):return (I+v[0]*X+v[1]*Y+v[2]*Z)/2
out={"seed":20261029,"scope":"Deterministic fixtures and random coefficient perturbations; no physical acquisition or rigorous interval certificate"}
eps=.02;eta=1e-6
ss=[(1-2*eps-eta)*pure([0,0,1]),(eps+eta)*pure([0,0,1]),eps*pure([0,0,-1])]
fstar=1-eps-eta;top=pair(ss[0],ss[1])[0];bb=best(ss)[0]
assert abs(top-(2*fstar-1)-eta)<1e-12 and abs(bb-fstar)<1e-12
out['top_prior_sharp_family']={'epsilon':eps,'eta':eta,'Fstar':fstar,'top_prior_binary':top,'state_aware_binary':bb}
for name,vs,F,expected in [('trine',[[np.cos(2*np.pi*k/3),np.sin(2*np.pi*k/3),0] for k in range(3)],2/3,(2+np.sqrt(3))/6),('tetrahedron',np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/np.sqrt(3),.5,(1+np.sqrt(2/3))/4)]:
    ss=[pure(v)/len(vs) for v in vs]; bb=best(ss)[0]
    assert abs(bb-expected)<1e-12 and bb<F
    out[name]={'Fstar_exact':F,'best_binary':bb,'expected':expected}
high=[]
for q in [.1,.02,.01]:
    c=.5;P0=1-2*q;s0=np.sqrt(1-c*c)
    zz=P0*(P0-q)/(2*P0-q*(1-c));yy=P0-zz;R=yy-q/2;uz=-(zz+q*c/2)/R
    ss=[P0*pure([0,0,1]),q*pure([s0,0,-c]),q*pure([-s0,0,-c])]
    mm=[(-2*uz/(1-uz))*pure([0,0,1]),pure([q*s0/(2*R),0,uz])/(1-uz),pure([-q*s0/(2*R),0,uz])/(1-uz)]
    U=yy*I+zz*Z
    assert np.linalg.norm(sum(mm)-I)<1e-12
    assert all(np.linalg.eigvalsh(m)[0]>-1e-12 for m in mm)
    assert all(np.linalg.eigvalsh(U-v)[0]>-1e-12 for v in ss)
    score=sum(tr(m@v) for m,v in zip(mm,ss));binary=best(ss)[0]
    assert abs(score-tr(U))<1e-12 and score>binary
    high.append({'q':q,'c':c,'Fstar_primal_dual':score,'best_binary':binary,'strict_gap':score-binary})
out['high_fidelity_nonbinary']=high
rng=np.random.default_rng(out['seed']);max_regret=0.;max_dual_violation=0.
for k in range(1000):
    m=int(rng.integers(2,15));ps=rng.dirichlet(np.ones(m));ss=[]
    for p in ps:
        v=rng.normal(size=3);v=v/np.linalg.norm(v)*rng.uniform(.1,1);ss.append(p*pure(v))
    delta=float(rng.uniform(.001,.05));hh=[]
    for s in ss:
        h=rng.normal(size=(2,2))+1j*rng.normal(size=(2,2));h=(h+h.conj().T)/2;h*=delta/np.linalg.norm(h,2)*rng.uniform(0,1);hh.append(s+h)
    oracle=best(ss)[0];fh,(a,b),P,yy=best(hh);actual=tr(P@ss[a]+(I-P)@ss[b]);regret=oracle-actual
    assert regret<=4*delta+1e-12
    slack=max(0.,max(np.linalg.eigvalsh(h-yy)[-1] for h in hh));U=yy+slack*I
    viol=max(np.linalg.eigvalsh(h-U)[-1] for h in hh);max_dual_violation=max(max_dual_violation,float(viol))
    assert viol<1e-12 and abs(tr(U)-fh-2*slack)<1e-12
    # Independent true dual upper bound: U+delta I dominates true coefficients.
    assert max(np.linalg.eigvalsh(s-U-delta*I)[-1] for s in ss)<1e-12
    assert tr(U)+2*delta-actual<=4*delta+2*slack+1e-12
    max_regret=max(max_regret,regret)
out['random_tests']={'cases':1000,'max_binary_regret':max_regret,'max_dual_feasibility_roundoff':max_dual_violation,'all_passed':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
