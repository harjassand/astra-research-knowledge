#!/usr/bin/env python3
"""Exact prescribed-matrix checks. No source sampler, RNG, or source calls."""
import hashlib, itertools, json
from pathlib import Path
import sympy as s
R=s.Rational
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
pa=[I,X,Y,Z]
K=lambda *a:s.kronecker_product(*a)
def clean(A): return A.applyfunc(s.expand)
def tr(A): return s.expand(s.trace(A))
def zero(A): return clean(A)==s.zeros(*A.shape)
def partial(A,keep,n=4):
    keep=tuple(keep); drop=tuple(i for i in range(n) if i not in keep)
    out=s.zeros(2**len(keep));
    for a,b in itertools.product(range(2**len(keep)),repeat=2):
        aa=[(a>>(len(keep)-1-i))&1 for i in range(len(keep))]
        bb=[(b>>(len(keep)-1-i))&1 for i in range(len(keep))]
        for z in range(2**len(drop)):
            zz=[(z>>(len(drop)-1-i))&1 for i in range(len(drop))]
            av=[0]*n; bv=[0]*n
            for i,p in enumerate(keep): av[p]=aa[i];bv[p]=bb[i]
            for i,p in enumerate(drop): av[p]=bv[p]=zz[i]
            ia=sum(v<<(n-1-i) for i,v in enumerate(av));ib=sum(v<<(n-1-i) for i,v in enumerate(bv))
            out[a,b]+=A[ia,ib]
    return clean(out)
P0=s.diag(1,0)
p=[R(7,10),R(1,10),R(1,10),R(1,10)]
a=[R(1,20),R(1,20),R(1,40),R(1,40)]
T=[K(Z,X),K(X,I),K(Y,Z),K(Z,Z)]
G=[K((p[k]*s.eye(4)+a[k]*T[k])/4,P0) for k in range(4)]
assert all(p[k]>=a[k] for k in range(4))
Gsum=sum(G,s.zeros(8));assert tr(Gsum)==1
chi={j:[1]+[1 if j==k else -1 for k in (1,2,3)] for j in (1,2,3)}
H={j:sum((chi[j][k]*G[k] for k in range(4)),s.zeros(8)) for j in (1,2,3)}
kappa=R(1,4)
# Analytic Pauli triangle certificate for H_j-kappa G >=0, including zero spectator eigenvalues.
margin={j:sum((chi[j][k]-kappa)*p[k] for k in range(4))-sum(abs(chi[j][k]-kappa)*a[k] for k in range(4)) for j in (1,2,3)}
assert all(x>0 for x in margin.values())
assert not zero(G[1]*G[2]-G[2]*G[1])
assert not zero(Gsum*H[1]-H[1]*Gsum)
U2=(3*s.eye(4)+4*s.I*K(X,X))/5*(5*s.eye(4)+12*s.I*K(Z,Z))/13
U=K(U2,s.eye(4));assert zero(U.H*U-s.eye(16))
B={j:clean(U*K(pa[j],s.eye(8))*U.H) for j in (1,2,3)}
rho=clean(U*K(I/2,Gsum)*U.H)
Rp={j:clean(U*K(I/2,H[j])*U.H) for j in (1,2,3)}
contrast={j:clean(B[j]*Rp[j]) for j in (1,2,3)}
rstates={(j,sgn):clean(rho+sgn*contrast[j]) for j in (1,3) for sgn in (-1,1)}
assert zero(B[3]*contrast[1]*B[3]+contrast[1])
assert zero(partial(contrast[1],(2,3)))
Blocal=partial(B[1],(0,1))/4
Xlocal=partial(contrast[1],(0,1))
assert tr(Blocal*Xlocal)==tr(H[1])==R(3,5)

# Includes a non-anticommuting learned raw pair and a completely disjoint gauge decoder.
pairs=[('true',B[1],B[3]),('non_anticommuting',R(3,5)*B[1]+R(4,5)*B[3],B[3]),('disjoint',K(I,I,X,I),K(I,I,Z,I))]
rows=[];Ds={}
for name,x,z in pairs:
    assert zero(x*x-s.eye(16)) and zero(z*z-s.eye(16))
    P=(s.eye(16)+z)/2;Q=s.eye(16)-P
    V=P.col_join(x*Q);assert zero(V.H*V-s.eye(16))
    A={j:clean(V.H*K(pa[j],s.eye(16))*V) for j in (1,2,3)}
    assert zero(A[3]-z) and zero(A[1]-(x-z*x*z)/2)
    t={j:tr(rho*B[j]*A[j]) for j in (1,2,3)}
    ell=clean(s.Matrix([[(3-sum(t.values()))/4]]))[0]
    # Direct channel action and normalized Choi, independent of diagonal-t formula.
    blocks=[]
    for aa in range(2):
        block=[]
        for bb in range(2):
            e=s.zeros(2);e[aa,bb]=1
            source=clean(U*K(e,Gsum)*U.H)
            vsource=clean(V*source*V.H)
            output=s.Matrix(2,2,lambda u,v:tr(vsource[u*16:(u+1)*16,v*16:(v+1)*16]))
            block.append(output/2)
        blocks.append(block)
    J=blocks[0][0].row_join(blocks[0][1]).col_join(blocks[1][0].row_join(blocks[1][1]))
    assert tr(J)==1 and zero(J-J.H)
    bell=(J[0,0]+J[0,3]+J[3,0]+J[3,3])/2
    assert s.expand(ell-(1-bell))==0
    g=sum((1-tr(contrast[j]*A[j]))/4 for j in (1,3))
    gstar=sum((1-tr(H[j]))/4 for j in (1,3))
    excess=s.expand(g-gstar)
    assert excess>=kappa*ell/2 and excess<=ell
    assert 2*ell<=sum(1-t[j] for j in (1,3))<=4*ell
    Ds[name]=(A,ell,excess)
    rows.append({'name':name,'ell0':str(ell),'excess':str(excess),'bell_loss_direct':str(1-bell)})
comparisons=[]
for aa,bb in itertools.combinations(Ds,2):
    A,ea,ra=Ds[aa];C,eb,rb=Ds[bb]
    mean=second=s.S(0)
    for j in (1,3):
        for sign in (-1,1):
            h=sign*(C[j]-A[j])/2
            mean+=tr(rstates[j,sign]*h)/4
            second+=tr(rstates[j,sign]*h*h)/4
    mean=s.expand(mean);second=s.expand(second)
    formula=sum(tr(rho*(A[j]-C[j])**2) for j in (1,3))/8
    assert mean==ra-rb and s.expand(second-formula)==0
    assert second<=2*(ea+eb)<=4*(ra+rb)/kappa
    comparisons.append({'a':aa,'b':bb,'mean':str(mean),'second_moment':str(second)})
# Uniform constant inequalities, exact rational bounds (no floating confidence computations).
# sqrt(1/524288)<1/512, so finite spectral bias+variance+range <1/96 of t.
assert R(1,4096)+R(1,512)+R(1,384)<R(1,96)
assert R(154,2**17)<R(1,640)
assert 2*R(154,2**17)+R(1,320)<R(1,160)
assert R(8)*(2*R(154,2**17)+R(1,320))<R(1,20)
assert R(1)-R(1,8)-R(1,16)==R(13,16)
assert R(1,8)+R(1,16)==R(3,16)
result={'status':'PASS','kind':'exact deterministic prescribed-matrix and rational-constant checks; no source sampling','source_calls':0,'physical_qubits':4,'true_interval':[0,1],'disjoint_interval':[2,3],'gauge':'noncommuting, correlated, rank deficient','relative_margin_certificates':{str(j):str(v) for j,v in margin.items()},'decoder_cases':rows,'comparison_cases':comparisons,'coarse_disjoint_contrast_exactly_zero':True,'true_patch_contrast_trace_norm':'3/5','coarse_score_constants':'13/16 versus 3/16','finite_spectral_Bernstein_additive_certificate':'1/4096+1/512+1/384<1/96','all_checks_passed':True}
path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
