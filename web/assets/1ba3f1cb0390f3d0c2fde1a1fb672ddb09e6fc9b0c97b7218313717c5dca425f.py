"""Independent exact exposed witness audit; no originator script imports."""
from itertools import product
from pathlib import Path
import json
from sympy import Matrix, Rational as Q, I, eye, sqrt, zeros, simplify, kronecker_product as kron

J=[Matrix([[0,0,0],[0,0,-I],[0,I,0]]),
   Matrix([[0,0,I],[0,0,0],[-I,0,0]]),
   Matrix([[0,-I,0],[I,0,0],[0,0,0]])]
I3=eye(3)
def simp(A): return A.applyfunc(simplify)
def Jn(n): return sum((n[i]*J[i] for i in range(3)),zeros(3))
def pvm(n):
    K=Jn(n)
    ps=[(K*K+K)/2,(K*K-K)/2,I3-K*K]
    assert simp(sum(ps,zeros(3))-I3)==zeros(3)
    for p in ps:
        assert p.H==p and simplify(p.trace())==1 and simp(p*p-p)==zeros(3)
    return ps
def canonical(ensemble,A):
    return simp(3*sum((p*r*(r*A).trace() for p,r in ensemble),zeros(3)))

# Derive the real-sphere canonical channel from seven explicit pure atoms.
real_ensemble=[]
for i in range(3):
    v=eye(3)[:,i]
    real_ensemble.append((Q(2,15),v*v.T))
for signs in [(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)]:
    v=Matrix(signs)/sqrt(3)
    real_ensemble.append((Q(3,20),v*v.T))
assert sum(p for p,r in real_ensemble)==1
assert sum((p*r for p,r in real_ensemble),zeros(3))==I3/3
for p,r in real_ensemble: assert r*r==r and r.trace()==1 and r.H==r and p>0
for i,j in product(range(3),repeat=2):
    E=zeros(3);E[i,j]=1
    assert canonical(real_ensemble,E)==(E.trace()*I3+E+E.T)/5
print('PASS seven explicit real pure atoms: probabilities axes2/15, tetrahedron3/20; canonical map exact on all9 matrix units.',flush=True)

u=Matrix([0,0,1]);v=Matrix([sqrt(3)/2,0,Q(1,2)])
Rot=Matrix([[Q(1,2),0,sqrt(3)/2],[0,1,0],[-sqrt(3)/2,0,Q(1,2)]])
assert Rot.T*Rot==I3 and Rot.det()==1 and Rot*u==v
c=(u.T*v)[0];h=(u+v)/sqrt(2+2*c)
pin=pvm(u);pout=[simp(Rot*r*Rot.T) for r in pin]
for r in pout: assert r.H==r and r.trace()==1 and simp(r*r-r)==zeros(3)
assert simp(sum(pout,zeros(3)))==I3
def phi(A): return simp(sum((q*(p*A).trace() for p,q in zip(pin,pout)),zeros(3)))
ph=pvm(h)
local_ensemble=[(c/3,p) for p in ph]+[((1-c)*p,r) for p,r in real_ensemble]
assert len(local_ensemble)==10
assert sum(p for p,r in local_ensemble)==1
assert simp(sum((p*r for p,r in local_ensemble),zeros(3)))==I3/3
def psi(A): return canonical(local_ensemble,A)
assert phi(I3)==I3 and psi(I3)==I3
for i,j in product(range(3),repeat=2):
    E=zeros(3);E[i,j]=1
    assert simplify(phi(E).trace()-E.trace())==0
    assert simplify(psi(E).trace()-E.trace())==0

# Explicit normalized legal broadcast Choi state, PSD by pure projectors.
R=sum((kron(p.T,q,q)/3 for p,q in zip(pin,pout)),zeros(27))
assert R.H==R and R.trace()==1 and simp(R*R-R/3)==zeros(27)
states=list(product(range(3),repeat=3));idx={s:i for i,s in enumerate(states)}
def marginal(axis):
    result=zeros(3);others=[i for i in range(3) if i!=axis]
    for a,b in product(range(3),repeat=2):
        for o in product(range(3),repeat=2):
            left=[0,0,0];right=[0,0,0];left[axis]=a;right[axis]=b
            for i,x in zip(others,o): left[i]=right[i]=x
            result[a,b]+=R[idx[tuple(left)],idx[tuple(right)]]
    return simp(result)
for axis in range(3): assert marginal(axis)==I3/3
Swap=zeros(27)
for s,i in idx.items(): Swap[idx[(s[0],s[2],s[1])],i]=1
assert simp(Swap*R*Swap.T-R)==zeros(27)
print('PASS exact legal nonsymmetric spin1 EB broadcaster: rank3 Choi, tracial single marginals, equal output swap.',flush=True)

E=[sqrt(Q(3,2))*r for r in J]
T=Matrix(3,3,lambda i,j:simplify((E[i]*phi(E[j])).trace()/3))
P=Matrix(3,3,lambda i,j:simplify((E[i]*psi(E[j])).trace()/3))
assert T==v*u.T and simp(P-c*h*h.T)==zeros(3)
local=simp(I3+P-T-T.T)
g=(v-u)/sqrt(2-2*c);n=Matrix([0,1,0])
assert simp(local-Q(3,2)*g*g.T-n*n.T)==zeros(3)
print('PASS entire local vector-span C2 residual: exact 0,1,3/2 eigenvalues from orthonormal h,g,n decomposition.',flush=True)

Eu=sqrt(Q(3,2))*Jn(u);Ev=sqrt(Q(3,2))*Jn(v)
den=sqrt(2*(1+c*c))
A=(kron(Eu,Eu)+kron(Ev,Ev))/den
phiA=(kron(phi(Eu),phi(Eu))+kron(phi(Ev),phi(Ev)))/den
psiA=(kron(psi(Eu),psi(Eu))+kron(psi(Ev),psi(Ev)))/den
norm=simplify((A*A).trace()/9)
score_phi=simplify((A*phiA).trace()/9)
score_psi=simplify((A*psiA).trace()/9)
excess=simplify(norm-score_psi-2*(norm-score_phi))
assert norm==1 and score_phi==Q(5,8) and score_psi==Q(9,40) and excess==Q(1,40)
print('PASS exact naive product failure: norm1, broadcast5/8, comparator9/40, C2 excess1/40.',flush=True)

# The theorem's two-product repair on this same example.
def Du(A):return simp(sum((p*(p*A).trace() for p in pin),zeros(3)))
pv=pvm(v)
def Dv(A):return simp(sum((p*(p*A).trace() for p in pv),zeros(3)))
repairA=(kron(Du(Eu),Du(Eu))+kron(Du(Ev),Du(Ev))+kron(Dv(Eu),Dv(Eu))+kron(Dv(Ev),Dv(Ev)))/(2*den)
score_repair=simplify((A*repairA).trace()/9)
assert score_repair==Q(5,8)
right=u*u.T;left=v*v.T;total=kron(T,T)
u2=kron(u,u);v2=kron(v,v)
assert simp(kron(right,right)+kron(left,left)-total-total.T-(v2-u2)*(v2-u2).T)==zeros(9)
print('PASS two-product repair: comparator score5/8; tensor polar residual exact positive outer product.',flush=True)

Path(__file__).with_name('EXPOSED_WITNESS_CHECKS.json').write_text(json.dumps({
    'schema_version':1,'all_pass':True,'real_canonical_atoms':7,'local_skew_comparator_atoms':10,
    'normalized_legal_choi_rank':3,'single_marginals':'I3/3',
    'local_residual_eigenvalues':['0','1','3/2'],
    'naive_product':{'norm':str(norm),'broadcast_score':str(score_phi),'comparator_score':str(score_psi),'excess':str(excess)},
    'two_product_repair_score':str(score_repair),
    'status':'Exact scoped identities and pure-projector constructions; universal theorem proved in texts, no parameter grid.'
},indent=2)+'\n')
