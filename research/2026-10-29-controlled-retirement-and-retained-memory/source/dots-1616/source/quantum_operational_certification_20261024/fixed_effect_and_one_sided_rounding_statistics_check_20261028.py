#!/usr/bin/env python3
"""Independent finite algebra checks, no quantum-source queries or random draws."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
import itertools,json,math
import sympy as S
import mpmath as mp
mp.mp.dps=110
Q=S.Rational; I=S.I
simp=lambda a:a.applyfunc(S.simplify)
def eq(a,b):return simp(a-b)==S.zeros(*a.shape)
def tr(a):return S.simplify(S.trace(a))
def psd(a):
    a=simp(a);assert eq(a,a.H)
    for n in range(1,a.rows+1):
        for ix in itertools.combinations(range(a.rows),n):
            assert S.simplify(a.extract(ix,ix).det())>=0
    return True
def block(a,b,c,d):return a.row_join(b).col_join(c.row_join(d))
def quat(t):
    r=sum(z*z for z in t);z=[(1-r)/(1+r)]+[2*v/(1+r) for v in t]
    a=z[0]+I*z[1];b=z[2]+I*z[3]
    return S.Matrix([[a,b],[-S.conjugate(b),S.conjugate(a)]])
def embed(U,k,i,j):
    ans=S.eye(k)
    for a,x in enumerate([i,j]):
        for b,y in enumerate([i,j]):ans[x,y]=U[a,b]
    return ans
U=quat([Q(1,4),Q(1,5),Q(-1,7)]);V=quat([Q(-1,6),Q(1,8),Q(1,3)])
assert eq(U.H*U,S.eye(2)) and eq(V.H*V,S.eye(2))
fixed=[]
for singular in [False,True]:
    Ar=S.diag(0 if singular else Q(3,5),Q(4,5));Dr=S.diag(1 if singular else Q(4,5),Q(3,5));A=Ar*Ar
    L=S.eye(2) if singular else U;R=S.eye(2) if singular else V
    D=S.diag(0 if singular else Q(1,7),Q(1,11))
    M=L*D*R.H
    W10=S.diag(0,Q(25,12))*D if singular else Dr.inv()*M*Ar.inv()
    # Correct singular inverse only acts on the supported second coordinate.
    assert eq(Dr*W10*Ar,M)
    c=1+tr(W10.H*W10);W=block(c*S.eye(2),W10.H,W10,c*S.eye(2));psd(W)
    m0=Q(1,2**30);m=S.simplify(m0+tr(W[:2,:2]*A+W[2:,2:]*(S.eye(2)-A))-2*tr(D));assert m>=m0
    Hs=[S.zeros(2),S.Matrix([[Q(1,8),Q(1,9)+I/13],[Q(1,9)-I/13,Q(-1,7)]]),S.diag(Q(1,2),Q(-1,2))]
    for H in Hs:
        psd(S.eye(2)/4-H*H)
        for sign in [-1,1]:
            v=S.eye(2)-2*H*H+sign*I*H
            assert eq(S.eye(2)-v.H*v,3*H*H-4*H**4);psd(S.eye(2)-v.H*v)
            B=-Ar*R*v*L.H*Dr;C=block(A,B,B.H,S.eye(2)-A);psd(C)
            assert eq(C[:2,:2]+C[2:,2:],S.eye(2))
            cost=S.simplify(m0+tr(W*C));assert cost==S.simplify(m+4*tr(D*H*H))
            fixed.append({'singular_A':singular,'sign':sign,'cost':str(cost),'exact_TP_PSD':True})
# Non-normal contraction: real/imaginary inequality without commutation.
N=S.Matrix([[Q(1,3),I/4],[0,Q(-1,5)]])
psd(S.eye(2)-N.H*N);X=(N+N.H)/2;H=(N-N.H)/(2*I);E=S.eye(2)-X
assert not eq(X*H,H*X)
assert eq(X*X+H*H,(N.H*N+N*N.H)/2);psd(2*E-H*H)
# Exact finite rational Jacobi steps, including a repeated-eigenvalue input.
jacobi=[]
for diagonal in [S.diag(Q(1,4),Q(1,4),Q(1,32)),S.diag(Q(1,2),Q(1,64),Q(1,256))]:
    k=3;Q0=embed(U,k,0,1)*embed(V,k,1,2);rho=simp(Q0*diagonal*Q0.H)
    eta=Q(1,32);dc=eta**2/(128*k**3);bits=80;den=2**bits;rot=S.eye(k);cur=rho;steps=0
    cap=k*k*math.ceil(math.log2(32*k/float(eta**2)))
    while True:
        energy=S.simplify(sum(cur[i,j]*S.conjugate(cur[i,j]) for i in range(k) for j in range(k) if i!=j))
        if energy<=eta**2/16:break
        assert steps<cap
        i,j=max(((i,j) for i in range(k) for j in range(i+1,k)),key=lambda ij:abs(complex(S.N(cur[ij[0],ij[1]],25))))
        mat=mp.matrix([[mp.mpc(str(S.N(S.re(cur[x,y]),105)),str(S.N(S.im(cur[x,y]),105))) for y in [i,j]] for x in [i,j]])
        vals,u=mp.eighe(mat);det=u[0,0]*u[1,1]-u[0,1]*u[1,0]
        u[0,1]/=det;u[1,1]/=det
        if mp.re(u[0,0])<0:u=-u
        qq=[mp.re(u[0,0]),mp.im(u[0,0]),mp.re(u[0,1]),mp.im(u[0,1])]
        tt=[Q(int(mp.nint(z/(1+qq[0])*den)),den) for z in qq[1:]]
        r=quat(tt);assert eq(r.H*r,S.eye(2));whole=embed(r,k,i,j)
        nxt=simp(whole.H*cur*whole)
        en=S.simplify(sum(nxt[a,b]*S.conjugate(nxt[a,b]) for a in range(k) for b in range(k) if a!=b))
        assert en<=(1-Q(2,k*k))*energy+eta**2/(64*k*k)
        cur=nxt;rot=simp(rot*whole);steps+=1
    assert eq(rot.H*rot,S.eye(k))
    diag=S.diag(*[cur[i,i]+eta/2 for i in range(k)])
    bar=simp(rot*diag*rot.H)
    psd(bar-rho);psd(rho+eta*S.eye(k)-bar);psd(S.eye(k)-bar)
    jacobi.append({'repeated_eigenvalue':diagonal[0,0]==diagonal[1,1],'steps':steps,'cap':cap,'exact_unitarity_energy_and_sandwich':True})
# Deterministic covariance coefficients with distinct scales and complex cross-blocks.
k=3
basis=[S.diag(Q(1,2),Q(1,16),Q(1,64)),S.Matrix([[0,Q(1,32),0],[Q(1,32),0,0],[0,0,0]]),S.Matrix([[0,0,0],[0,0,I/256],[0,-I/256,0]])]
rho=sum((g*g for g in basis),S.zeros(k));psd(S.eye(k)/2-rho)
T=S.Matrix([[1,I/3,Q(1,5)],[Q(1,7),1,I/4],[I/6,Q(1,8),1]]);W=T.H*T
ops=[S.Matrix([[0,1,0],[1,0,0],[0,0,0]]),S.Matrix([[0,0,0],[0,0,I],[0,-I,0]]),S.diag(1,-2,3)]
def n(a):return S.simplify(sum(tr(o*a)**2 for o in ops))
a=max(1,sum(tr(o.H*o) for o in ops));s=sum(n(g) for g in basis);m=Q(1,2**20);q=tr(W*rho)
delta=min(Q(1,16),s/(64*a*k));eta=min(Q(1,8),m/(8*(1+tr(W))));bar=rho+eta*S.eye(k)/2
bands={}
for i in range(k):
    if bar[i,i]<delta:continue
    j=0
    while bar[i,i]<=Q(1,4)**(j+1):j+=1
    bands.setdefault(j,[]).append(i)
bs=[]
for j,idx in bands.items():
    P=S.zeros(k)
    for i in idx:P[i,i]=1
    bs.append((Q(1,4)**j,P))
ell=len(bs);K=ell*(ell+1)//2;P=sum((x[1] for x in bs),S.zeros(k));keep=sum(n(P*g*P) for g in basis)
assert keep>=s/4
comps=[]
for pp,Pi in bs:
    gs=[Pi*g*Pi for g in basis];ss=sum(n(g) for g in gs);bb=pp*(m+tr(W*Pi));comps.append(('diag',pp,Pi,None,gs,ss,bb,0))
for u,v in itertools.combinations(bs,2):
    (pi,Pi),(pj,Pj)=sorted([u,v],key=lambda x:x[0]);gs=[Pi*g*Pj for g in basis];ss=sum(n(g+g.H) for g in gs);tt=sum(tr(W*g*g.H) for g in gs);bb=pj*m+2*pj*tr(W*Pj)+48*tt
    comps.append(('off',pj,Pi,Pj,gs,ss,bb,tt))
qb=tr(W*bar);assert sum(c[6] for c in comps)<=(8*ell+56)*(m+qb)
assert max(c[5]/c[6] for c in comps)>=(s/(m+q))/(8*K*(8*ell+56))
R0=2*math.ceil(math.sqrt(math.ceil(math.log2(192*max(2,k)))))
completion_cases=0;cross_cost_nondiagonal=0
for typ,pp,Pi,Pj,gs,ss,bb,tt in comps:
    for coeff in itertools.product([-1,0,1],repeat=len(gs)):
        G=sum((c*g for c,g in zip(coeff,gs)),S.zeros(k))
        numer=n(G if typ=='diag' else G+G.H)
        if ss==0 or numer<ss/2:continue
        # These deterministic points meet the event; no probability is estimated.
        psd(R0**2*pp*S.eye(k)-G.H*G)
        if typ=='off':assert tr(W*G*G.H)<=48*tt
        if typ=='diag':
            TT=G/(2*R0*S.sqrt(pp));outs=[(Pi+TT)/2,(Pi-TT)/2]
        else:
            B=G/(4*R0*S.sqrt(pp));base=2*B*B.H+Pj-2*B.H*B;outs=[base+B+B.H,base-B-B.H]
        ratios=[]
        for A in outs:
            psd(A);psd(S.eye(k)-A)
            cost=m+tr(W*A);ratios.append(n(A)/cost)
            if typ=='off':
                diagcost=tr(W*(Pi*A*Pi+Pj*A*Pj));assert tr(W*A)<=2*diagcost
                if tr(W*A)!=diagcost:cross_cost_nondiagonal+=1
        assert max(ratios)>=ss/(256*R0**2*bb)
        completion_cases+=1
assert cross_cost_nondiagonal>0
# Rational finite-precision and probability/cost constants at extreme scales.
scalar=0
for den in [1,2**20,2**80]:
    mm=F(1,den)
    for ss in [F(1,den),F(1),F(den)]:
        for aa in [F(1),F(2**10)]:
            dg=ss/(32*(1+ss)*aa)
            assert dg*dg*2*aa<=ss/16
            dw=mm/(16*(1+mm)*aa)
            assert dw*dw*aa<=mm/16
            scalar+=1
assert F(1,12)-F(1,48)-F(1,48)-F(1,96)==F(1,32)
for k in range(1,101):
    R=2*math.ceil(math.sqrt(math.ceil(math.log2(192*max(2,k)))))
    # Stronger rational tail using e>=2: 2k exp(-R²/2)<=2k 2^(-R²/2).
    assert F(2*k,2**(R*R//2))<=F(1,48)
root=Path(__file__).resolve().parent
sources={'ordinary_fixed_effect_decoder_positive_cost_geometry_20261028.md':'433e0b0ce9b0361968d73cb7de060fae7f24dda7c03f410d466876d105c31077','ordinary_one_sided_effect_finite_positive_cost_rounding_20261028.md':'8b5859b44e398d5d97d5b14580041bd9232b9fe59188a9c090634d6a4dbab0b6'}
for f,h in sources.items():assert sha256((root/f).read_bytes()).hexdigest()==h
out={'status':'PASS_EXACT_SOURCE_DISABLED_CHECKS','source_calls':0,'random_draws':0,'source_acquisition_simulations':0,'source_sha256':sources,'fixed_slice_completion_cases':len(fixed),'fixed_slice_cases':fixed,'noncommuting_real_imaginary_case':True,'exact_rational_Jacobi_cases':jacobi,'retained_bands':ell,'retained_components':len(comps),'actual_effect_completion_cases':completion_cases,'nonzero_W_cross_cost_checks':cross_cost_nondiagonal,'extreme_precision_cases':scalar,'rational_Gaussian_tail_constant_cases':100,'scope':'Exact deterministic algebra and certified rational rotation residuals. No sampled Gaussian confidence test, SDP execution or quantum source experiment.'}
(root/'fixed_effect_and_one_sided_rounding_statistics_check_20261028.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='fixed_slice_cases'},indent=2))
