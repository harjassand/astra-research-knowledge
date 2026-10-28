#!/usr/bin/env python3
"""Independent exact IC/complete-kernel and small full-CPTP certificates.
No author check imported; no sampled episodes or generic QE/SDP optimization.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,itertools,json
import sympy as s

HERE=Path(__file__).resolve().parent
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
def adj(A):return A.conjugate().T
def eq(A,B):return s.simplify(A-B)==s.zeros(*A.shape)
def ic(n):
    bs=[]
    for j in range(n):
        v=s.eye(n)[:,j];bs.append(v*v.T)
    for j in range(n):
        for k in range(j+1,n):
            v=s.eye(n)[:,j]+s.eye(n)[:,k];bs.append(v*adj(v)/2)
            v=s.eye(n)[:,j]+s.I*s.eye(n)[:,k];bs.append(v*adj(v)/2)
    assert len(bs)==n*n
    return bs
def gramdual(bs):
    G=s.Matrix([[s.trace(a*b) for b in bs] for a in bs]);Gi=G.inv()
    dual=[sum((Gi[i,j]*bs[j] for j in range(len(bs))),s.zeros(bs[0].rows)) for i in range(len(bs))]
    assert all(s.simplify(s.trace(dual[i]*bs[j]))==int(i==j) for i in range(len(bs)) for j in range(len(bs)))
    return dual,G
def psd_exact(A):
    for size in range(1,A.rows+1):
        for ix in itertools.combinations(range(A.rows),size):
            assert s.simplify(A.extract(ix,ix).det())>=0

ic_dimensions=[]
for n in range(1,5):
    bs=ic(n);ds,G=gramdual(bs);assert G.det()!=0
    eff=[a/(2*n*n) for a in bs]
    rem=s.eye(n)-sum(eff,s.zeros(n));psd_exact(rem-s.eye(n)/2)
    ic_dimensions.append({'dimension':n,'basis_size':len(bs),'gram_determinant':str(G.det())})

# Different source from the author: mixed coherent memory, rational complex
# interactions and input-dependent native outcome probabilities.
rho=s.Matrix([[s.Rational(2,3),s.I/6],[-s.I/6,s.Rational(1,3)]])
assert rho.det()==s.Rational(7,36)
CNOT=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
SWAP=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
Q=s.Rational(3,5)*I-s.I*s.Rational(4,5)*Y
P=s.diag(1,s.I)
U=CNOT*s.kronecker_product(Q,P)
V0=SWAP*s.kronecker_product(P,Q)*CNOT
V1=s.kronecker_product(Q,P)*SWAP*CNOT
for G in [U,V0,V1]:assert eq(adj(G)*G,s.eye(4))
filters=[s.kronecker_product(s.diag(s.Rational(3,5),1),I),
         s.kronecker_product(s.diag(s.Rational(4,5),0),I)]
actions=[[B*V for B in filters] for V in [V0,V1]]
for ks in actions:assert eq(sum((adj(K)*K for K in ks),s.zeros(4)),s.eye(4))

def embed_pair(G,first,second,n=3):
    out=s.zeros(2**n)
    for inp in itertools.product(range(2),repeat=n):
        for a,b in itertools.product(range(2),repeat=2):
            dest=list(inp);dest[first]=a;dest[second]=b
            oi=sum(x*2**(n-1-i) for i,x in enumerate(dest))
            ii=sum(x*2**(n-1-i) for i,x in enumerate(inp))
            out[oi,ii]=G[2*a+b,2*inp[first]+inp[second]]
    return out

def process_kernel(K):
    # Independent parallel-slot Choi construction on M,A1,A2; then reorder
    # (A1ref,A2ref,B1,B2) to (A1ref,B1,A2ref,B2).
    G=embed_pair(K,0,2)*embed_pair(U,0,1)
    J=s.zeros(16)
    for mi,ni,mf in itertools.product(range(2),repeat=3):
        A=s.Matrix(4,4,lambda out,inp:G[4*mf+out,4*mi+inp])
        B=s.Matrix(4,4,lambda out,inp:G[4*mf+out,4*ni+inp])
        va=s.Matrix([A[o,i] for i in range(4) for o in range(4)])
        vb=s.Matrix([B[o,i] for i in range(4) for o in range(4)])
        J+=rho[mi,ni]*va*adj(vb)
    order=[8*a+4*c+2*b+d for a,b,c,d in itertools.product(range(2),repeat=4)]
    return s.simplify(J.extract(order,order))

def induce(K,sigma,prep,effect):
    out=K*s.kronecker_product(sigma,prep)*adj(K)
    return s.Matrix(2,2,lambda m,n:s.simplify(sum(effect[c,b]*out[2*m+b,2*n+c]
                  for b,c in itertools.product(range(2),repeat=2))))

preps=ic(2);effects=[p/8 for p in preps]
bi=[p.T for p in preps];di,_=gramdual(bi);de,_=gramdual(effects)
local=[s.kronecker_product(a,b) for a in bi for b in effects]
dual=[s.kronecker_product(a,b) for a in di for b in de]
tensor_duals=[s.kronecker_product(a,b) for a in dual for b in dual]
kernels={};born_cases=0
for action,ks in enumerate(actions):
    for outcome,K in enumerate(ks):
        W=process_kernel(K);assert eq(W,adj(W))
        reconstructed=s.zeros(16)
        for u,v,u2,v2 in itertools.product(range(4),repeat=4):
            prob=s.simplify(s.trace(induce(K,induce(U,rho,preps[u],effects[v]),preps[u2],effects[v2])))
            assert prob>=0
            basis=s.kronecker_product(local[4*u+v],local[4*u2+v2])
            assert s.simplify(s.trace(W*basis)-prob)==0
            reconstructed+=prob*tensor_duals[(4*u+v)*16+4*u2+v2]
            born_cases+=1
        assert eq(reconstructed,W)
        kernels[action,outcome]=W

# Coherent caller memory C is retained and can be entangled with the payload.
Caller=s.kronecker_product(Q,P)*CNOT
T=Caller[:,[0,2]] # B1 -> A2,C, with C initialized in |0>.
assert eq(adj(T)*T,I)
L=[s.diag(1,s.Rational(4,5)),s.Matrix([[0,s.Rational(3,5)],[0,0]])]
assert eq(sum((adj(a)*a for a in L),s.zeros(2)),I)
def link(W,T):
    out=s.zeros(8)
    for i,b,c,j,d,e in itertools.product(range(2),repeat=6):
        val=sum(T[2*a+c,q]*s.conjugate(T[2*z+e,r])*W[8*i+4*q+2*a+b,8*j+4*r+2*z+d]
                for q,r,a,z in itertools.product(range(2),repeat=4))
        out[4*i+2*b+c,4*j+2*d+e]=s.simplify(val/2)
    return out
def direct_endpoint(K,Filt=I):
    G=embed_pair(K,0,1)*embed_pair(Caller,1,2)*embed_pair(s.kronecker_product(I,Filt),0,1)*embed_pair(U,0,1)
    out=s.zeros(8)
    for mi,ni,mf in itertools.product(range(2),repeat=3):
        A=s.Matrix(4,2,lambda bc,a:G[4*mf+bc,4*mi+2*a])
        B=s.Matrix(4,2,lambda bc,a:G[4*mf+bc,4*ni+2*a])
        va=s.Matrix([A[bc,a] for a in range(2) for bc in range(4)])
        vb=s.Matrix([B[bc,a] for a in range(2) for bc in range(4)])
        out+=rho[mi,ni]*va*adj(vb)/2
    return s.simplify(out)
coherent=[];adaptive=[]
for o,K in enumerate(actions[0]):
    ans=link(kernels[0,o],T);assert eq(ans,direct_endpoint(K));coherent.append(ans)
for record in range(2):
    for o,K in enumerate(actions[record]):
        ans=link(kernels[record,o],T*L[record]);assert eq(ans,direct_endpoint(K,L[record]));adaptive.append(ans)
for law in [coherent,adaptive]:
    J=sum(law,s.zeros(8));assert s.trace(J)==1
    assert s.Matrix(2,2,lambda a,b:sum(J[4*a+c,4*b+c] for c in range(4)))==I/2

# Rectangular p=2,q=3 actual channel, reconstructed from 36 ordinary scalars.
P3=ic(3);E3=[a/18 for a in P3];de3,_=gramdual(E3)
A=s.Matrix([[1,0],[0,1],[0,0]])*s.Rational(3,5)
B=s.Matrix([[0,1],[0,0],[1,0]])*s.Rational(4,5)
assert adj(A)*A+adj(B)*B==I
vs=[s.Matrix([C[b,a] for a in range(2) for b in range(3)]) for C in [A,B]]
Jrect=sum((v*adj(v) for v in vs),s.zeros(6));rec=s.zeros(6)
for i,j in itertools.product(range(4),range(9)):
    state=A*preps[i]*adj(A)+B*preps[i]*adj(B)
    prob=s.simplify(s.trace(E3[j]*state))
    assert s.simplify(s.trace(Jrect*s.kronecker_product(preps[i].T,E3[j]))-prob)==0
    rec+=prob*s.kronecker_product(di[i],de3[j])
assert eq(rec,Jrect)

# Exact all-CPTP diamond-epigraph certificates on a nontrivial channel family.
vi=s.Matrix([1,0,0,1]);vx=s.Matrix([0,1,1,0]);PI=vi*vi.T/2;PX=vx*vx.T/2
decoder_cases=0;regret_cases=0
for pp in range(11):
    p=s.Rational(pp,10);flip=p>s.Rational(1,2);b=1-p if flip else p
    CR=(vx*vx.T) if flip else (vi*vi.T)
    assert s.Matrix(2,2,lambda a,c:sum(CR[2*a+j,2*c+j] for j in range(2)))==I
    JD=2*b*(PX-PI);ZZ=2*b*(PX+PI);tt=2*b
    psd_exact(ZZ-JD);psd_exact(ZZ+JD)
    assert s.Matrix(2,2,lambda a,c:sum(ZZ[2*a+j,2*c+j] for j in range(2)))==tt*I
    decoder_cases+=1
    for qq in range(11):
        q=s.Rational(qq,10);chosen_flip=q>s.Rational(1,2)
        error=1-p if chosen_flip else p;opt=min(p,1-p)
        assert error-opt<=2*abs(p-q)
        regret_cases+=1

# Explicit incomplete calibration alphabet attack, including all real matrices.
a,b,c,x,y,z=s.symbols('a b c x y z',real=True)
rr=s.Matrix([[a,b],[b,c]]);ee=s.Matrix([[x,y],[y,z]])
UP=s.diag(1,s.I);UM=s.diag(1,-s.I)
assert s.expand(s.trace(ee*UP*rr*adj(UP))-s.trace(ee*UM*rr*adj(UM)))==0
vp=s.Matrix([1,0,0,s.I]);vm=s.Matrix([1,0,0,-s.I]);assert (adj(vp)*vm)[0]==0

# Rational acquisition bounds and loose complete-port constant dominance.
budget_cases=0
for d,p,q,b,H,n,C,K in itertools.product([1,2,3],[1,2],[1,3],[1,2],[0,1,7],[1,2],[1,3],[1,7]):
    eta=F(1,5);B=p*q*b;M=d*(1+B*H);w=F(1,2)
    while 4*C*K*w*w*M**(2*n)>eta**(2*n):w/=2
    assert 4*C*K*w*w*M**(2*n)<=eta**(2*n)
    # sqrt(d/2)<=d and d sqrt(B/2)<=d B, exact squared tests.
    assert d<=2*d*d and B<=2*B*B
    budget_cases+=1

out={'status':'PASS_INDEPENDENT_EXACT_IC_PORT_KERNEL_CONTROLLER_AND_DECODER_CERTIFICATES',
 'source_sha256':hashlib.sha256((HERE/'IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY.md').read_bytes()).hexdigest(),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'IC_dimension_cases':ic_dimensions,'exact_two_slot_scalar_coefficients':born_cases,
 'mixed_memory_native_instrument_kernels_reconstructed':len(kernels),
 'coherent_retained_quantum_memory_branches':len(coherent),'adaptive_retained_record_branches':len(adaptive),
 'rectangular_ordinary_coefficients':36,'exact_full_CPTP_diamond_certificates':decoder_cases,
 'exact_model_selected_regret_cases':regret_cases,'exact_integer_dyadic_budget_cases':budget_cases,
 'incomplete_real_alphabet_attack':'Exact symbolic real 2x2 input/effect equality and orthogonal Bell outputs',
 'source_calls':0,'episode_starts':0,'rng_draws':0,'sampled_outcomes':0,
 'generic_modulus_QE_executed':False,'physical_candidate_fit_executed':False,'generic_recovery_optimizer_executed':False,
 'gate_synthesis_or_hardware_executed':False,
 'evidence_scope':'Exact symbolic/fraction finite fixtures. Small supplied recovery solutions have exact primal/dual-style certificates; no claim of running the generic optimizer.'}
(HERE/'ic_port_independent_complete_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
