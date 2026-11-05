"""Independent geometry and two-particle LTI marginal padding checks.
Every output of the local interaction is enumerated; no excitation truncation.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
from pathlib import Path
from itertools import product,combinations
from collections import Counter
import math,json,hashlib,time
import numpy as np

OUT=Path(__file__).resolve().parent
SOURCE=OUT.parent/'lti_2d_product_extension_20261105'/'interaction.npy'


def orient(z):
    for x in z:
        if x:return z if x>0 else tuple(-a for a in z)
    return z


def geometry(p,R,L):
    A=list(product(range(L),repeat=p));u=L+R-1
    Y=[y for y in product(range(-R+1,u),repeat=p) if not all(0<=a<L for a in y)]
    clamp=lambda y:tuple(max(0,min(L-1,a)) for a in y)
    assigned={y:clamp(y) for y in Y};mult=Counter(assigned.values())
    P=(2*R-1)**p;T=P*(6*R-1)**p;s=len(Y)
    assert s==(L+2*R-2)**p-L**p
    assert s<=2*p*(R-1)*3**(p-1)*L**(p-1)
    for y,a in assigned.items():
        for yy,aa in zip(y,a):
            assert max(yy,0)>=aa and min(yy+R-1,u-1)<=aa+R-1
    assert max(mult.values(),default=0)<=P
    core=Counter(orient(tuple(b-a for a,b in zip(x,y))) for x,y in combinations(A,2))
    for z,n in core.items():assert n==math.prod(L-abs(a) for a in z)
    cross=Counter()
    for y,a in assigned.items():
        for x in A:
            if max(abs(xx-aa) for xx,aa in zip(x,a))>=R:
                cross[orient(tuple(aa-xx for xx,aa in zip(x,a)))]+=1
    assert max(cross.values(),default=0)<=2*s
    far=Counter();near_count=Counter()
    for y,z in combinations(Y,2):
        a,b=assigned[y],assigned[z]
        if max(abs(x-w) for x,w in zip(a,b))<3*R:
            near_count[y]+=1;near_count[z]+=1
        else:
            assert max(abs(x-w) for x,w in zip(y,z))>=R
            far[orient(tuple(x-w for x,w in zip(a,b)))]+=1
    assert max(near_count.values(),default=0)<=T
    assert max(far.values(),default=0)<=2*P*s
    return dict(p=p,R=R,L=L,boundary_terms=s,maximum_assignment_multiplicity=max(mult.values(),default=0),
                far_unordered_pairs=sum(far.values()),max_far_displacement_multiplicity=max(far.values(),default=0),
                all_support_counting_checks_passed=True)


def dicke(n,j):
    a=1/math.sqrt(math.comb(n,j))
    return {sum(1<<i for i in x):a for x in combinations(range(n),j)}


def weight(n_total,n_local,J,j):
    if not (0<=j<=n_local and 0<=J-j<=n_total-n_local):return 0.
    return math.comb(n_local,j)*math.comb(n_total-n_local,J-j)/math.comb(n_total,J)


def add(a,b):
    for x,v in b.items():a[x]=a.get(x,0)+v


def inner(a,b):return sum(np.conj(v)*b.get(x,0) for x,v in a.items())


def terms_action(states,terms,h):
    out={}
    for sites in terms:
        clear=sum(1<<i for i in sites)
        patterns=[sum((1<<s) for j,s in enumerate(sites) if mask>>j&1) for mask in range(16)]
        for state,amp in states.items():
            inp=sum(((state>>s)&1)<<j for j,s in enumerate(sites))
            if inp==0:continue
            rem=state&~clear
            for mask in range(1,16):
                x=rem|patterns[mask]
                out[x]=out.get(x,0)+amp*h[mask,inp]
    return out


K=[(0,0),(1,0),(0,1),(1,1)]


def pair_moment(h,n_total,J,z=None,squared=False):
    other=[] if z is None else [(x+z[0],y+z[1]) for x,y in K]
    pts=sorted(set(K+other));idx={x:i for i,x in enumerate(pts)}
    t0=[[idx[x] for x in K]]
    t1=None if z is None else [[idx[x] for x in other]]
    total=0.
    for j in range(1,min(J,len(pts))+1):
        w=weight(n_total,len(pts),J,j)
        if not w:continue
        psi=dicke(len(pts),j);a=terms_action(psi,t0,h)
        if squared:val=inner(a,a).real
        elif z is None:val=inner(psi,a).real
        else:val=2*inner(a,terms_action(psi,t1,h)).real
        total+=w*val
    return total


def moments(h,L,J):
    n_total=(2*L)**2;u=L+1;nu=u*u
    energy=pair_moment(h,n_total,J)
    a=pair_moment(h,n_total,J,squared=True)/energy
    v=a;disjoint=0.
    for z in product(range(-L+1,L),repeat=2):
        if z==(0,0):continue
        b=pair_moment(h,n_total,J,z=z)/energy
        v+=b/2
        if max(abs(x) for x in z)>=2:
            assert b>=-1e-12;disjoint+=b/2
    points=list(product(range(-1,u+1),repeat=2));idx={x:i for i,x in enumerate(points)}
    inside=list(product(range(u),repeat=2));inbits=[idx[x] for x in inside]
    maskU=sum(1<<x for x in inbits)
    A=list(product(range(L),repeat=2))
    Y=[x for x in product(range(-1,u),repeat=2) if x not in A]
    term=lambda anchor:[idx[(anchor[0]+x,anchor[1]+y)] for x,y in K]
    core_terms=[term(x) for x in A];boundary_terms=[term(x) for x in Y]
    Ecore=Etotal=S_core=S_boundary=cross=0.
    max_states=0
    for j in range(1,min(J,nu)+1):
        w=weight(n_total,nu,J,j)/energy
        if not w:continue
        psi={sum(1<<inbits[i] for i in c):1/math.sqrt(math.comb(nu,j)) for c in combinations(range(nu),j)}
        core=terms_action(psi,core_terms,h);boundary=terms_action(psi,boundary_terms,h)
        Ecore+=w*inner(psi,core).real;Etotal+=w*(inner(psi,core)+inner(psi,boundary)).real
        S_core+=w*inner(core,core).real;S_boundary+=w*inner(boundary,boundary).real
        cross+=2*w*inner(core,boundary).real
        max_states=max(max_states,len(core)+len(boundary))
    M=float(np.linalg.eigvalsh(h)[-1]);c=float(np.linalg.eigvalsh(h)[1]);kappa=M/c
    overlap_J=4;P=9;T=P*11**2;s=len(Y);C0=2*M*overlap_J*2
    assert abs(Ecore-L*L)<1e-9
    assert disjoint<=v+2*M*overlap_J+1e-10
    assert S_core<=L*L*v+C0*L+1e-9
    assert cross<=s*(2*kappa*disjoint+P*M*(1+kappa))+1e-9
    assert S_boundary<=s*(M*kappa*(1+T)+2*kappa*kappa*P*disjoint)+1e-9
    # A concrete counterexample to factoring compression for nearby crossing terms.
    psi={1<<i:1/math.sqrt(nu) for i in inbits}
    outputs=[terms_action(psi,[t],h) for t in boundary_terms]
    projected=[{x:v for x,v in o.items() if x&~maskU==0} for o in outputs]
    defects=[abs(inner(outputs[i],outputs[j])-inner(projected[i],projected[j]))
             for i,j in combinations(range(len(Y)),2)]
    defect=float(max(defects,default=0))
    assert defect>1e-6
    return dict(L=L,total_window_sites=n_total,global_Dicke_particles=J,
                normalized_dual_objective=float(v),positive_disjoint_moment_sum=float(disjoint),
                core_first_moment=float(Ecore),padded_first_moment=float(Etotal),
                core_second_moment=float(S_core),seam_second_moment=float(S_boundary),
                mixed_moment=float(cross),padding_correction_times_L=float((S_core+S_boundary+cross-L*L*v)/L),
                maximum_sparse_output_count=max_states,
                maximum_near_compression_factorization_error=defect,
                all_claimed_moment_inequalities_passed=True)


def main():
    start=time.perf_counter();h=np.load(SOURCE)
    geom=[geometry(*args) for args in [(1,1,3),(1,3,11),(2,2,8),(2,3,11),(3,2,7)]]
    states=[moments(h,L,2) for L in (2,3,4)]
    result=dict(interaction_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                geometry=geom,correlated_LTI_tests=states,elapsed_seconds=time.perf_counter()-start,
                interpretation='Full-LTI Dicke marginals, including nonzero far cross moments; finite checks support the algebra, not SDP-optimum or universal proof claims.')
    (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
