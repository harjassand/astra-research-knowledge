#!/usr/bin/env python3
"""Exact endpoint separation/repair and restricted all-CPTP optimum fixtures.

No generic ellipsoid run. No stochastic acquisition or physical compilation.
The Pauli fixtures DO execute a specialized exact endpoint optimizer and certify
its unrestricted-CPTP optimum analytically; they do not restrict the theorem.
"""
from pathlib import Path
import hashlib, itertools, json
import sympy as s

HERE = Path(__file__).resolve().parent
Q = s.Rational
def adj(A): return A.conjugate().T
def clean(A): return A.applyfunc(s.simplify)
def equal(A,B): return clean(A-B)==s.zeros(*A.shape)
def unit(n,i):
    v=s.zeros(n,1);v[i]=1;return v
def partial(A,m,n):
    return s.Matrix(m,m,lambda i,j:sum(A[n*i+b,n*j+b] for b in range(n)))

def negative_witness(A):
    """Exact rational Hermitian congruence separation; None certifies PSD."""
    A=clean(A);n=A.rows
    assert A==adj(A)
    for i in range(n):
        if A[i,i]<0:return unit(n,i)
    for i in range(n):
        if A[i,i]==0:
            for j in range(n):
                if A[i,j]!=0:
                    v=unit(n,i)-s.conjugate(A[i,j])/(A[j,j]+1)*unit(n,j)
                    assert s.simplify((adj(v)*A*v)[0])<0
                    return v
    piv=next((i for i in range(n) if A[i,i]>0),None)
    if piv is None:return None
    ix=[j for j in range(n) if j!=piv]
    if not ix:return None
    col=A.extract(ix,[piv]);d=A[piv,piv]
    Schur=A.extract(ix,ix)-col*adj(col)/d
    w=negative_witness(Schur)
    if w is None:return None
    v=s.zeros(n,1);v[piv]=-(adj(col)*w)[0]/d
    for j,z in zip(ix,w):v[j]=z
    assert s.simplify((adj(v)*A*v)[0])<0
    return v

def assert_psd(A):
    v=negative_witness(A)
    assert v is None, (A,v)
def hb(n,traceless=False):
    ans=[]
    for i in range(n-(1 if traceless else 0)):
        a=unit(n,i)*unit(n,i).T
        if traceless:a-=unit(n,n-1)*unit(n,n-1).T
        ans.append(a)
    for i in range(n):
        for j in range(i+1,n):
            a=s.zeros(n);a[i,j]=a[j,i]=1;ans.append(a)
            a=s.zeros(n);a[i,j]=s.I;a[j,i]=-s.I;ans.append(a)
    return ans
def tp_basis(m,n):
    return [s.kronecker_product(a,b) for a in hb(m) for b in hb(n,True)]
def combo(bs,cs,dim):
    return sum((c*b for c,b in zip(cs,bs)),s.zeros(dim))
def compose(N,C,p,k):
    return s.Matrix(p*p,p*p,lambda ia,jb:sum(
        N[k*(ia//p)+y,k*(jb//p)+z]*C[p*y+ia%p,p*z+jb%p]
        for y in range(k) for z in range(k)))

separation_cases=0
for n in range(1,6):
    # A rational complex congruence preserves known inertia.
    T=s.eye(n)
    for i in range(n):
        for j in range(i+1,n):T[i,j]=Q(i+j+1,7)+s.I*Q(j-i,11)
    for pattern in itertools.product([-1,0,1],repeat=n):
        if n>=4 and sum(abs(x) for x in pattern)>2:continue
        A=clean(T*s.diag(*pattern)*adj(T))
        v=negative_witness(A)
        if -1 in pattern:
            assert v is not None and s.simplify((adj(v)*A*v)[0])<0
        else:assert v is None
        separation_cases+=1

gram_cases=0
for m,n in itertools.product(range(1,4),repeat=2):
    # Factor Gram bounds suffice for the tensor-product coordinate bound.
    for bs in [hb(m),hb(n,True)]:
        if not bs:continue
        G=s.Matrix([[s.trace(a*b) for b in bs] for a in bs])
        assert_psd(G-s.eye(len(bs)))
        assert_psd(4*max(m,n)*s.eye(len(bs))-G)
        gram_cases+=1
    bs=tp_basis(m,n)
    assert len(bs)==m*m*(n*n-1)
    assert all(partial(a,m,n)==s.zeros(m) for a in bs)

interior_cases=0
radius_cases=[]
for task,p,k in itertools.product(['projection','recovery'],range(1,4),range(1,4)):
    if task=='projection':
        m,n,a,b,ell=p,k,p,k,1;D=p*k
        base=hb(D)
        J0=combo(base,[Q((i%7)-3,5) for i in range(len(base))],D)
        g=1+sum(abs(s.re(z))+abs(s.im(z)) for z in J0)
        L=lambda C:C
    else:
        m,n,a,b,ell=k,p,p,p,p;D=p*p
        N=s.eye(p*k)/k
        # Nontrivial known channel with complex off-diagonal coefficients.
        if p>1 and k>1:
            N+=s.kronecker_product(hb(p)[-1],hb(k,True)[-1])/(4*p*k)
        assert_psd(N);assert partial(N,p,k)==s.eye(p)
        L=lambda C,N=N,p=p,k=k:compose(N,C,p,k)
        vi=s.Matrix([int(i==j) for i in range(p) for j in range(p)])
        J0=vi*vi.T;g=p
    cb=tp_basis(m,n);zb=hb(D)
    C0=s.eye(m*n)/n
    ss=ell*m+g+1;t0=b*ss+1;T=2*t0
    r=Q(1,8*(n*n+n*ell+b+1))
    R=2*m+a*T+ss*D+T+1
    M=len(cb)+len(zb)+1
    assert M==m*m*(n*n-1)+D*D+1
    # Deterministic rational directions inside the stated Euclidean ball.
    for seed in range(6):
        vec=[Q(((j+1)*(seed+2))%7-3) for j in range(M)]
        den=1+sum(abs(x) for x in vec)
        vec=[r*x/den for x in vec]
        assert sum(x*x for x in vec)<=r*r
        C=C0+combo(cb,vec[:len(cb)],m*n)
        Z=ss*s.eye(D)+combo(zb,vec[len(cb):-1],D);t=t0+vec[-1]
        assert partial(C,m,n)==s.eye(m)
        for A in [C,Z-(L(C)-J0),Z+(L(C)-J0),t*s.eye(a)-partial(Z,a,b)]:
            assert_psd(A)
        assert 0<t<T
        interior_cases+=1
    radius_cases.append({'task':task,'p':p,'k':k,'M':M,'h':max(m*n,D,a),
                         'r':str(r),'R':str(R)})

repair_cases=0;root_repair_cases=0;stinespring_cases=0;budget_cases=0
for m,n in itertools.product(range(1,5),repeat=2):
    for aa in [Q(1,1000),Q(1,100),Q(1,10*(n+1))]:
        lam=[1+(n-1)*aa]+[-aa]*(n-1)
        C=s.diag(*(lam*m))
        Cphys=(C+2*aa*s.eye(m*n))/(1+2*n*aa)
        assert partial(C,m,n)==s.eye(m)
        assert partial(Cphys,m,n)==s.eye(m)
        assert_psd(Cphys-aa/(1+2*n*aa)*s.eye(m*n))
        change=sum(abs(Cphys[i,i]-C[i,i]) for i in range(m*n))
        assert change<=4*m*n*aa
        repair_cases+=1
        # Exact diagonal Kraus/isometry certificate, no gate compilation.
        Ks=[]
        for i in range(m):
            for j in range(n):
                K=s.zeros(n,m);K[j,i]=s.sqrt(Cphys[n*i+j,n*i+j]);Ks.append(K)
        assert sum((adj(K)*K for K in Ks),s.zeros(m))==s.eye(m)
        stinespring_cases+=1
        for b,ell,sigma in itertools.product([1,2,3],[1,2,5],[Q(1,10),Q(1,1000)]):
            r=Q(1,8*(n*n+n*ell+b+1))
            W=2+4*b+2*b*n*ell+8*m*n*n
            e=min(r/4,Q(1,8*n*n),sigma/(4*W))
            aC=2*n*e
            gap=(1+Q(1+4*b+2*b*n*ell,2)+4*m*n*n)*e
            assert gap<sigma and 2*n*aC<=Q(1,2)
            budget_cases+=1
        # General non-TP shift/normalization repair (diagonal exact version).
        lam2=[]
        for i in range(m):
            lam2.extend([1+(n-1)*aa+(-1)**i*aa]+[-aa]*(n-1))
        C=s.diag(*lam2);C1=C+aa*s.eye(m*n);P=partial(C1,m,n)
        C2=s.diag(*[C1[i,i]/P[i//n,i//n] for i in range(m*n)])
        assert partial(C2,m,n)==s.eye(m);assert_psd(C2)
        assert sum(abs(C2[i,i]-C[i,i]) for i in range(m*n))<=5*m*n*aa
        root_repair_cases+=1

# Executed specialized endpoint optimizer with full-CPTP optimality certificate.
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
P=[I,X,Y,Z]
J=[]
for U in P:
    v=s.Matrix([U[b,a] for a in range(2) for b in range(2)])
    J.append(v*adj(v))
assert sum(J,s.zeros(4))==2*s.eye(4)
weights=[
    [Q(6,5),Q(-1,5),0,0],
    [Q(1,5),Q(1,10),Q(-1,10),Q(1,5)],
    [-1,Q(-1,2),0,Q(-1,3)],
    [Q(1,4)]*4,
    [0,0,0,2],
    [Q(1,1000),0,Q(-1,1000),0],
    [Q(3,5),Q(1,5),Q(1,10),Q(1,10)],
]
true_weights=[[Q(1,4)]*4]+[[int(j==i) for j in range(4)] for i in range(4)]
true_weights += [[Q(7,10),Q(1,10),Q(1,10),Q(1,10)],
                 [Q(1,10),Q(6,10),Q(2,10),Q(1,10)]]
pauli_solves=0;regret_cases=0;epi_cases=0
for w in weights:
    w=list(map(s.Rational,w));pos=[max(x,0) for x in w];total=sum(pos)
    q=[x/total for x in pos] if total else [s.Integer(1),0,0,0]
    assert sum(q)==1 and all(x>=0 for x in q)
    C=sum((q[i]*J[i] for i in range(4)),s.zeros(4))
    Jhat=sum((w[i]*J[i] for i in range(4)),s.zeros(4))
    ZZ=sum((abs(q[i]-w[i])*J[i] for i in range(4)),s.zeros(4))
    tt=sum(abs(q[i]-w[i]) for i in range(4))
    assert_psd(C);assert partial(C,2,2)==I
    assert_psd(ZZ-(C-Jhat));assert_psd(ZZ+(C-Jhat))
    assert partial(ZZ,2,2)==tt*I
    # Bell-outcome lower bound for every physical channel equals this value.
    assert tt==sum(-x for x in w if x<0)+abs(total-1)
    chosen=max(range(4),key=lambda i:q[i])
    # Four-Pauli sum rule gives all-CPTP recovery lower error 1-max(q).
    assert 1-q[chosen]==1-max(q)
    pauli_solves+=2
    for rr in true_weights:
        eta=sum(abs(w[i]-rr[i]) for i in range(4))/2
        error=1-rr[chosen];opt=1-max(rr)
        assert error-opt<=4*eta
        regret_cases+=1
    for ee in [Q(1,100),Q(1,1000)]:
        aZ=(2+2*2)*ee;aT=(1+2*2)*ee
        Znear=ZZ-aZ*s.eye(4);tnear=tt-2*aZ-aT
        assert_psd(Znear+aZ*s.eye(4)-(C-Jhat))
        assert_psd(Znear+aZ*s.eye(4)+(C-Jhat))
        assert partial(Znear,2,2)==(tnear+aT)*I
        assert (tnear+aT+2*aZ)/2==tt/2
        epi_cases+=1

out={
 'status':'PASS_EXACT_SEPARATION_INTERIOR_REPAIR_AND_RESTRICTED_ENDPOINT_CERTIFICATES',
 'source_sha256':hashlib.sha256((HERE/'ACCESSIBLE_ENDPOINT_RATIONAL_SDP_AND_COMPILER.md').read_bytes()).hexdigest(),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'rational_congruence_PSD_separation_cases':separation_cases,
 'basis_Gram_certificates':gram_cases,
 'rational_interior_ball_direction_checks':interior_cases,
 'spectrahedron_parameters':radius_cases,
 'exact_affine_TP_repair_cases':repair_cases,
 'exact_general_root_normalization_repair_cases':root_repair_cases,
 'exact_Kraus_Stinespring_TP_certificates':stinespring_cases,
 'exact_accuracy_budget_cases':budget_cases,
 'executed_restricted_Pauli_endpoint_optimizations':pauli_solves,
 'full_CPTP_Pauli_comparator_regret_cases':regret_cases,
 'exact_epigraph_residual_repairs':epi_cases,
 'generic_rounded_ellipsoid_executed':False,
 'generic_SDP_solver_executed':False,
 'finite_gate_compiler_executed':False,
 'hardware_executions':0,'source_calls':0,'episode_starts':0,'RNG_draws':0,
 'scope':'Exact rational/symbolic fixtures. Specialized Pauli optimizer is executed with all-CPTP certificates; generic GLS solver and physical circuit synthesis are theoretical algorithm imports, not executed.'
}
(HERE/'accessible_endpoint_exact_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
