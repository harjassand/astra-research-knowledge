"""Matrix-valued telescopic divergence completion.
Core i: B_i(g)=sum_p A_(i,p) q_(i,p)^g, |q|<1.
Each constructed flux retains the original TT bond dimensions exactly.
All contractions below sum the infinite coordinate domains rationally.
"""

if not __debug__:
    raise RuntimeError('Do not run with Python -O: certificate checks must execute.')
import sympy as sp
from fractions import Fraction as F
import random,time,json
from pathlib import Path

def rat(x):return sp.Rational(x.numerator,x.denominator) if isinstance(x,F) else sp.Rational(x)
def core_value(core,n):
    if n<0:return sp.zeros(*core[0][0].shape)
    return sum((A*q**n for A,q in core),sp.zeros(*core[0][0].shape))
def total(core):return sum((A/(1-q) for A,q in core),sp.zeros(*core[0][0].shape))
def value(cores,g):
    x=sp.ones(1,1)
    for core,n in zip(cores,g):x=x*core_value(core,n)
    return x[0]
def mass(cores):
    x=sp.ones(1,1)
    for core in cores:x=x*total(core)
    return x[0]
def fluxes(cores,refs):
    m=len(cores);means=list(map(total,cores));out=[]
    for i in range(m):
        packet=[]
        for j,core in enumerate(cores):
            if j<i:packet.append(core)
            elif j>i:packet.append([(means[j]*(1-refs[j]),refs[j])])
            else:
                p=[(-A*q/(1-q),q) for A,q in core if q]
                if refs[j]:p.append((means[j]*refs[j],refs[j]))
                if not p:p=[(sp.zeros(*means[j].shape),sp.Rational(0))]
                packet.append(p)
        out.append(packet)
    return out

def routed_fluxes(cores,refs):
    """All legal-path payloads, each with TT ranks at most twice the input.
    A triangular block automaton sums F_i for i>=j without a rank-m direct sum.
    """
    m=len(cores);means=list(map(total,cores));out=[]
    hs=[];ds=[]
    for i,core in enumerate(cores):
        h=[(-A*q/(1-q),q) for A,q in core if q]
        if refs[i]:h.append((means[i]*refs[i],refs[i]))
        if not h:h=[(sp.zeros(*means[i].shape),sp.Rational(0))]
        hs.append(h);ds.append([(means[i]*(1-refs[i]),refs[i])])
    for j in range(m):
        result=[]
        for i,core in enumerate(cores):
            if i<j:result.append(core);continue
            nr,nc=means[i].shape;items=[]
            poles=set(q for C in (core,hs[i],ds[i]) for A,q in C)
            for q in sorted(poles):
                B=sum((A for A,Q in core if Q==q),sp.zeros(nr,nc))
                H=sum((A for A,Q in hs[i] if Q==q),sp.zeros(nr,nc))
                D=sum((A for A,Q in ds[i] if Q==q),sp.zeros(nr,nc))
                block=B.row_join(H).col_join(sp.zeros(nr,nc).row_join(D))
                if i==j:block=block[:nr,:]
                if i==m-1:block=block[:,nc:]
                if block!=sp.zeros(*block.shape):items.append((block,q))
            if not items:
                shape=(nr if i==j else 2*nr,nc if i==m-1 else 2*nc)
                items=[(sp.zeros(*shape),sp.Rational(0))]
            result.append(items)
        out.append(result)
    return out

def inner(a,b):
    x=sp.ones(1,1)
    for ac,bc in zip(a,b):
        shape=(ac[0][0].rows*bc[0][0].rows,ac[0][0].cols*bc[0][0].cols)
        K=sum((sp.kronecker_product(A,B)/(1-q*r) for A,q in ac for B,r in bc),sp.zeros(*shape))
        x=x*K
    return x[0]

def run():
    start=time.perf_counter();rng=random.Random(123013);checks=0;routechecks=0;rows=[]
    for m,r in [(2,2),(3,2),(5,3)]:
        dims=[1]+[r]*(m-1)+[1];cores=[]
        for i in range(m):
            core=[]
            for p in range(2):
                A=sp.Matrix(dims[i],dims[i+1],lambda a,b:sp.Rational(rng.randint(-3,3),5))
                q=sp.Rational(rng.randint(0,3),5);core.append((A,q))
            cores.append(core)
        refs=[sp.Rational(1,3)]*m;fs=fluxes(cores,refs);routes=routed_fluxes(cores,refs);mb=mass(cores)
        for _ in range(12):
            g=[rng.randrange(5) for i in range(m)];div=0
            for i,fi in enumerate(fs):
                h=list(g);h[i]-=1;div+=value(fi,g)-value(fi,h)
            target=value(cores,g)-mb*sp.prod((1-refs[i])*refs[i]**g[i] for i in range(m))
            assert div==target;checks+=1
            for j in range(m):
                assert value(routes[j],g)==sum(value(fs[i],g) for i in range(j,m));routechecks+=1
        assert all([c[0][0].shape for c in packet]==[c[0][0].shape for c in cores] for packet in fs)
        energy=sum((min(i,j)+1)*inner(fs[i],fs[j]) for i in range(m) for j in range(m))
        assert energy>=0
        assert sum(inner(w,w) for w in routes)==energy
        assert all(c[0][0].rows<=2*r and c[0][0].cols<=2*r for packet in routes for c in packet)
        rows.append(dict(dimension=m,bond_dimension=r,fluxes=m,max_poles=max(len(c) for f in fs for c in f),
             routed_rank_bound=2*r,routed_energy=str(energy),energy_float=float(energy)))
    return dict(exact_pointwise_checks=checks,exact_automaton_checks=routechecks,routed_rank_factor=2,bond_dimensions_preserved=True,infinite_contractions=True,
         rows=rows,seconds=time.perf_counter()-start,
         scope='TT completion of b-mass(b)*reference; mean-zero sources are repaired exactly')
if __name__=='__main__':
    out=run();Path('tt_completion_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
