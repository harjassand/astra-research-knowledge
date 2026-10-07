#!/usr/bin/env python3
"""Reproducible finite diagnostics; NOT an implementation of the Chen--Liu FPRAS.

Uses exact rational/symbolic arithmetic for local identities and small tensor
contractions. Dense floating-point diagonalization checks the cooling estimates.
Run: python checks/check_results.py (from the checkpoint root).
Dependencies: Python 3, numpy, scipy, sympy. No network calls.
"""
from __future__ import annotations
import itertools, json, math, platform
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.linalg import expm, eigh

ROOT = Path(__file__).resolve().parents[1]
results: dict[str, object] = {"scope": "Finite identity and small-instance diagnostics, not a general FPRAS or formal proof", "tests": {}}

def record(name: str, value: object) -> None:
    results["tests"][name] = value

# Q Hess(log Q) criterion for arbitrary nonnegative bivariate coefficients.
u,v,A,B,C,D = sp.symbols('u v A B C D', nonnegative=True)
Q = A+B*u+C*v+D*u*v
grad = sp.Matrix([sp.diff(Q,z) for z in (u,v)])
M = Q*sp.hessian(Q,(u,v))-grad*grad.T
factor = (2*B*C-A*D+B*D*u+C*D*v+D**2*u*v)*(A*D+B*D*u+C*D*v+D**2*u*v)
assert sp.expand(M.det()-factor)==0
assert sp.expand(M[0,0]+(B+D*v)**2)==0
assert sp.expand(M[1,1]+(C+D*u)**2)==0
record('bivariate_hessian_factorization', 'exact symbolic pass; log concave iff AD <= 2BC for nonzero nonnegative Q')

# Fibre Hessian of the most general real symmetric two-qubit generator.
s1,s2,z1,z2 = sp.symbols('s1 s2 z1 z2', real=True)
p,f,g0,g1,h0,h1 = sp.symbols('p f g0 g1 h0 h1', real=True)
a00,a01,a10,a11 = sp.symbols('a00 a01 a10 a11', real=True)
u1,v1,u2,v2 = (s1+z1)/2,(s1-z1)/2,(s2+z2)/2,(s2-z2)/2
qA = (a00*v1*v2+a01*v1*u2+a10*u1*v2+a11*u1*u2
      +p*(1+u1*u2*v1*v2)+f*(u1*v1+u2*v2)
      +(1+u1*v1)*(g0*v2+g1*u2)+(1+u2*v2)*(h0*v1+h1*u1))
F = sp.hessian(qA,(z1,z2))
Delta=a00-a01-a10+a11
expected=sp.Matrix([
 [-p*(s2**2-z2**2)/8-f/2-(g0*v2+g1*u2)/2,
  Delta/4+p*z1*z2/4-(g1-g0)*z1/4-(h1-h0)*z2/4],
 [Delta/4+p*z1*z2/4-(g1-g0)*z1/4-(h1-h0)*z2/4,
  -p*(s1**2-z1**2)/8-f/2-(h0*v1+h1*u1)/2]])
assert all(sp.expand(x)==0 for x in F-expected)
record('infinitesimal_fibre_hessian', 'exact symbolic pass for all ten real-symmetric matrix parameters')

# EPR* positive decomposition, critical eight-vertex boundary, and Pfaffian representation.
x=sp.symbols('x1:5'); a,c,d=sp.symbols('a c d',positive=True); b=a+c+d
P=d*(1+sp.prod(x))+a*(x[0]*x[1]+x[2]*x[3])+b*(x[0]*x[2]+x[1]*x[3])+c*(x[0]*x[3]+x[1]*x[2])
R=a*(x[0]+x[3])*(x[1]+x[2])+c*(x[0]+x[1])*(x[2]+x[3])+d*(1+x[0]*x[2])*(1+x[1]*x[3])
assert sp.expand(P-R)==0
record('EPR_star_three_connection_decomposition', 'exact symbolic pass on b=a+c+d')

# Local tensor mapping: output bits then complemented input bits in reverse order.
def local_poly(F: sp.Matrix) -> dict[tuple[int,...],sp.Expr]:
    ans={}
    for out in range(4):
        for inp in range(4):
            if F[out,inp]:
                bits=((out>>1)&1,out&1,1-(inp&1),1-((inp>>1)&1))
                ans[bits]=F[out,inp]
    return ans
av,bv,cv,dv=sp.symbols('a b c d')
Fe=sp.Matrix([[av,0,0,dv],[0,bv,cv,0],[0,cv,bv,0],[dv,0,0,av]])
poly=sum(w*sp.prod(xx**bb for xx,bb in zip(x,bits)) for bits,w in local_poly(Fe).items())
assert sp.expand(poly-(dv*(1+sp.prod(x))+av*(x[0]*x[1]+x[2]*x[3])+bv*(x[0]*x[2]+x[1]*x[3])+cv*(x[0]*x[3]+x[1]*x[2])))==0
record('physical_port_labeling', 'exact pass, including reversed complemented input ports')

# Exact signed-swap triangle: all three connections are individually nonnegative.
def signed_swap(n: int, i: int, j: int) -> sp.Matrix:
    ans=sp.zeros(2**n)
    for inp in range(2**n):
        bits=[(inp>>k)&1 for k in range(n)]
        bits[i],bits[j]=1-bits[j],1-bits[i]
        out=sum(bb<<k for k,bb in enumerate(bits));ans[out,inp]=1
    return ans
U01,U02,U12=(signed_swap(3,*e) for e in ((0,1),(0,2),(1,2)))
triangle=U12*U02*U01
assert sp.trace(triangle)==0
assert all(sum(triangle[i,j] for i in range(8))==1 for j in range(8))
# Remove spin flips, leaving ordinary swaps: the same word has two permutation cycles.
def plain_swap(n: int,i: int,j: int)->sp.Matrix:
    ans=sp.zeros(2**n)
    for inp in range(2**n):
        bits=[(inp>>k)&1 for k in range(n)];bits[i],bits[j]=bits[j],bits[i]
        ans[sum(bb<<k for k,bb in enumerate(bits)),inp]=1
    return ans
plain=plain_swap(3,1,2)*plain_swap(3,0,2)*plain_swap(3,0,1)
assert sp.trace(plain)==4
record('frustrated_triangle', {'signed_trace':0,'unfrustrated_loop_count':4,'order_applied':[[0,1],[0,2],[1,2]],'matrix':np.array(triangle,dtype=int).tolist()})

# EPR* conservation-law obstruction, all local axes, exact symbolic calculation.
I=sp.eye(2); X=sp.Matrix([[0,1],[1,0]]);Y=sp.Matrix([[0,-sp.I],[sp.I,0]]);Z=sp.diag(1,-1)
beta,si,sj=sp.symbols('b si sj',real=True)
K=(sp.kronecker_product(X,X)+beta*sp.kronecker_product(Y,Y)-sp.kronecker_product(Z,Z))/2
charge=si*sp.kronecker_product(Y,I)+sj*sp.kronecker_product(I,Y)
comm=K*charge-charge*K
claim=sp.I*(si+sj)*(sp.kronecker_product(Z,X)+sp.kronecker_product(X,Z))
assert all(sp.expand(z)==0 for z in comm-claim)
record('EPR_star_charge_obstruction', 'exact commutator pass; for |b|<1 the singular-axis argument forces opposite Y charges on every edge')

# Exact small-network coefficient contraction, with nonhomogeneous one-qubit factors.
def embed_rational(n:int, F:sp.Matrix, sites:tuple[int,...])->sp.Matrix:
    ans=sp.zeros(2**n)
    for inp in range(2**n):
        bits=[(inp>>(n-1-k))&1 for k in range(n)]
        sub=sum(bits[k]<<(len(sites)-1-j) for j,k in enumerate(sites))
        for outsub in range(2**len(sites)):
            if not F[outsub,sub]:continue
            ob=bits.copy()
            for j,k in enumerate(sites):ob[k]=(outsub>>(len(sites)-1-j))&1
            out=sum(bb<<(n-1-k) for k,bb in enumerate(ob))
            ans[out,inp]+=F[outsub,sub]
    return ans

# Enumerating incidence monomials and imposing wire disequality is exactly coefficient extraction.
# Gate tuples store (sites, matrix). This routine enumerates gate-local choices, not dense multiplication.
def coefficient_amplitude(n:int, gates:list, final:int)->sp.Expr:
    total=sp.Rational(0)
    def walk(k:int,bits:tuple[int,...],weight:sp.Expr)->None:
        nonlocal total
        if k==len(gates):
            if sum(bb<<(n-1-i) for i,bb in enumerate(bits))==final:total+=weight
            return
        sites,G=gates[k]; sub=sum(bits[i]<<(len(sites)-1-j) for j,i in enumerate(sites))
        for out in range(2**len(sites)):
            w=G[out,sub]
            if not w:continue
            new=list(bits)
            for j,i in enumerate(sites):new[i]=(out>>(len(sites)-1-j))&1
            walk(k+1,tuple(new),weight*w)
    # The all-ones boundary is the positive boundary polynomial product (1+x).
    for bits in itertools.product((0,1),repeat=n):walk(0,bits,sp.Rational(1))
    return total
n=3
edge=sp.Matrix([[1,0,0,0],[0,sp.Rational(6,5),sp.Rational(1,4),0],[0,sp.Rational(1,4),sp.Rational(6,5),0],[0,0,0,1]])
xgate=sp.Matrix([[1,sp.Rational(1,7)],[sp.Rational(1,7),1]])
zgate=sp.diag(sp.Rational(5,4),1)
gates=[((0,1),edge),((1,),xgate),((1,2),edge),((0,),zgate),((2,),xgate)]
Cmat=sp.eye(2**n)
for sites,G in gates:Cmat=embed_rational(n,G,sites)*Cmat
vec=Cmat*sp.ones(2**n,1)
for j in range(2**n):assert coefficient_amplitude(n,gates,j)==vec[j]
Znorm=(vec.T*vec)[0]
# Prefix rotation preparation with exact counts reproduces the target probabilities.
prefixes={}
for k in range(n+1):
    for pfx in itertools.product((0,1),repeat=k):
        val=sum(vec[j]**2 for j in range(2**n) if tuple((j>>(n-1-i))&1 for i in range(k))==pfx)
        prefixes[''.join(map(str,pfx))]=str(val)
for j in range(2**n):
    probability=sp.Rational(1); pref=''
    for k in range(n):
        bit=str((j>>(n-1-k))&1)
        probability*=sp.Rational(prefixes[pref+bit])/sp.Rational(prefixes[pref]);pref+=bit
    assert sp.simplify(probability-vec[j]**2/Znorm)==0
record('exact_nonhomogeneous_network', {'amplitudes_checked':8,'prefix_norms_checked':15,'normalizer':str(Znorm),'prefixes':prefixes,'backend':'exponential enumeration, not FPRAS'})

# Numerical vector-relative word approximation and cooling on genuinely noncommuting examples.
In=np.eye(2);Xn=np.array(X,dtype=float);Zn=np.array(Z,dtype=float);Yn=np.array(Y,dtype=complex)
def embed(n:int,M:np.ndarray,sites:tuple[int,...])->np.ndarray:
    return np.array(embed_rational(n,sp.Matrix(M),sites),dtype=complex)
def make_problem(n:int,edges:list[tuple[int,int,float,float]],hs:list[float],gs:list[float]):
    terms=[]; H=np.zeros((2**n,2**n),complex); shift=0.; V=0.
    for i,j,fv,dvalue in edges:
        H+=embed(n,(dvalue*np.kron(Zn,Zn)-fv*(np.kron(Xn,Xn)+np.kron(Yn,Yn)))/2,(i,j))
        Am=np.array([[max(-dvalue,0),0,0,0],[0,max(dvalue,0),fv,0],[0,fv,max(dvalue,0),0],[0,0,0,max(-dvalue,0)]])
        terms.append(embed(n,Am,(i,j)).real);shift+=abs(dvalue)/2;V+=fv+max(dvalue,0)
    for i,(hv,gv) in enumerate(zip(hs,gs)):
        H+=embed(n,hv*Zn-gv*Xn,(i,))
        if hv:terms.append(embed(n,abs(hv)*In-hv*Zn,(i,)).real)
        if gv:terms.append(embed(n,gv*Xn,(i,)).real)
        shift+=abs(hv);V+=2*abs(hv)+gv
    assert np.max(np.abs(sum(terms)-(shift*np.eye(2**n)-H)))<1e-12
    return H.real,terms,V
rng=np.random.default_rng(8062026)
errors=[]; bound_checks=0
for trial in range(18):
    nn=2 if trial<9 else 3
    ed=[(i,i+1,float(rng.uniform(.2,1)),0.) for i in range(nn-1)]
    ed=[(i,j,ff,float(rng.uniform(-ff,ff))) for i,j,ff,_ in ed]
    hs=rng.uniform(-.5,.5,size=nn).tolist();gs=rng.uniform(0,.5,size=nn).tolist()
    H,terms,Vv=make_problem(nn,ed,hs,gs)
    tau=.4;alpha=.2
    k0=max(1,math.ceil(6*tau*Vv),math.ceil(nn/2)+math.ceil(math.log2(64/alpha)))
    mm=max(2*k0,math.ceil(8*k0*k0/alpha))
    sweep=np.eye(2**nn)
    for term in terms:sweep=(np.eye(2**nn)+tau*term/mm)@sweep
    va=np.linalg.matrix_power(sweep,mm)@np.ones(2**nn)
    vt=expm(tau*sum(terms))@np.ones(2**nn)
    er=float(np.max(np.abs(va/vt-1)));assert er<=alpha
    errors.append(er);bound_checks+=1
record('vector_relative_product_formula', {'random_seed':8062026,'instances':bound_checks,'max_relative_error':max(errors),'requested_bound':.2,'floating_point_diagnostic':True})

cooling=[]
fixtures=[
 (3,[(0,1,1.,.4),(1,2,.7,-.3)],[.2,-.4,.1],[.1,.2,.3]),
 (3,[(0,1,1.,-1.),(1,2,1.,-1.)],[0.,0.,0.],[0.,0.,0.]),
 (3,[(0,1,1.,1.)],[0.,0.,0.],[0.,0.,0.]),
]
for nn,ed,hs,gs in fixtures:
    H,terms,Vv=make_problem(nn,ed,hs,gs);w,U=eigh(H)
    mask=np.abs(w-w[0])<1e-9;rank=int(mask.sum())
    gap=float(np.min(w[~mask]-w[0])) if np.any(~mask) else 1.
    plus=np.ones(2**nn)/math.sqrt(2**nn);P0=U[:,mask]@U[:,mask].T
    overlap=float(plus@P0@plus);assert overlap+1e-10>=rank/(2**nn)
    target=P0@plus/math.sqrt(overlap);eps=.01
    tau=(nn*math.log(2)/2+math.log(8/eps))/gap
    filtered=U@(np.exp(-tau*(w-w[0]))*(U.T@plus));filtered/=np.linalg.norm(filtered)
    td=math.sqrt(max(0.,1.-float(np.dot(target,filtered))**2));assert td<=eps
    cooling.append({'n':nn,'ground_rank':rank,'gap':gap,'seed_overlap_squared':overlap,'lower_bound':rank/(2**nn),'tau':tau,'trace_distance':td})
record('degenerate_pure_ground_cooling',cooling)

# Numerical near-origin failure for the EPR* eight-vertex signature.
t=sp.Rational(1,20);bpar=sp.Rational(1,3)
vals={a:1,c:t*(1-bpar)/2,d:t*(1+bpar)/2}
Pe=sp.expand(P.subs(vals));ge=sp.Matrix([sp.diff(Pe,xx) for xx in x]);Me=Pe*sp.hessian(Pe,x)-ge*ge.T
at={xx:sp.Rational(1,10000) for xx in x}
eigs=np.linalg.eigvalsh(np.array(Me.subs(at),float));assert eigs[-1]>0
record('eight_vertex_direct_log_concavity_failure',{'t':'1/20','b':'1/3','all_variables':'1/10000','max_eigenvalue_of_q_squared_hessian_log':float(eigs[-1]),'scope':'direct local signature, not computational hardness'})

results['environment']={'python':platform.python_version(),'numpy':np.__version__,'sympy':sp.__version__}
results['status']='ALL CHECKS PASSED'
(ROOT/'checks'/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
