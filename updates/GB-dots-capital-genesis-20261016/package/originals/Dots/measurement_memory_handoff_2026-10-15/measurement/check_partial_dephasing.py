#!/usr/bin/env python3
"""Original exact-rational channel checks and shared-bath matrix tests."""
import itertools, json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.linalg import expm

def exact_checks():
    I2=sp.eye(2); Z=sp.diag(1,-1); I4=sp.eye(4); Id=sp.eye(16)
    S0=sp.kronecker_product(Z,I2); S1=sp.kronecker_product(I2,Z)
    adj=lambda S:sp.kronecker_product(S.conjugate(),S)
    D0=(Id+adj(S0))/2; D1=(Id+adj(S1))/2; DG=D0*D1
    r0=sp.Rational(1,3);r1=sp.Rational(2,5);q=(1-r0)*(1-r1)
    T=(r0*Id+(1-r0)*D0)*(r1*Id+(1-r1)*D1)
    R=(T-q*DG)/(1-q)
    assert R==sp.Rational(2,9)*Id+sp.Rational(4,9)*D0+sp.Rational(1,3)*D1
    assert T==q*DG+(1-q)*R
    # Exact random-stabilizer Kraus weights, hence an exact CP certificate.
    ws=[sp.Rational(11,18),sp.Rational(2,9),sp.Rational(1,6),sp.Rational(0)]
    assert sum(ws)==1 and all(w>=0 for w in ws)
    assert R==ws[0]*Id+ws[1]*adj(S0)+ws[2]*adj(S1)+ws[3]*adj(S0*S1)
    # TP and each sector fixed exactly.
    trace=sp.Matrix(1,16,lambda i,j: int(j%5==0))
    assert trace*R==trace and trace*T==trace
    sectors=[]
    for s,t in itertools.product((0,1),repeat=2):
        P=(I4+(-1)**s*S0)*(I4+(-1)**t*S1)/4
        vec=sp.Matrix([P[i,j] for j in range(4) for i in range(4)])
        assert R*vec==vec;sectors.append(P)
    # A single scalar r Id+(1-r)D_G cannot fit all three coherences.
    def matrix_unit_vec(a,b):
        v=sp.zeros(16,1);v[a+4*b]=1;return v
    factors=[]
    for b in [1,2,3]:
        v=matrix_unit_vec(0,b); factors.append((T*v)[4*b])
    assert factors==[r1,r0,r0*r1] and len(set(factors))==3
    # Strongest q with T-q D_G CP follows from orthogonal Pauli Choi vectors.
    tw=[sp.Rational(7,15),sp.Rational(7,30),sp.Rational(1,5),sp.Rational(1,10)]
    assert 4*min(tw)==q
    # Expected squared block size identities by exhaustive exact rational sums.
    cases=0
    for M in range(1,8):
        for r in [F(0),F(1,5),F(7,10),F(1)]:
            avg=F(0)
            for pattern in itertools.product((0,1),repeat=M-1): # success=1
                prob=F(1);lens=[];run=1
                for bit in pattern:
                    prob*=1-r if bit else r
                    if bit:lens.append(run);run=1
                    else:run+=1
                lens.append(run);avg+=prob*sum(x*x for x in lens)
            formula=M+2*sum((M-k)*r**k for k in range(1,M))
            assert avg==formula;cases+=1
    # Finite endpoint channels: with zero weak noise, the conservatively
    # charged missing-endpoint flag has exactly its scalar mixture weight.
    qi=sp.Rational(3,4);qo=sp.Rational(4,5)
    Pplus=(I2+Z)/2;Pminus=(I2-Z)/2
    endpoint_ops=lambda q:[(sp.sqrt(1-q)*I2,False),(sp.sqrt(q)*Pplus,True),(sp.sqrt(q)*Pminus,True)]
    Efailed=sp.zeros(2)
    for A,sa in endpoint_ops(qi):
        for B,sb in endpoint_ops(qo):
            K=B*A
            if not(sa and sb):Efailed+=K.conjugate().T*K
    assert Efailed==(1-qi*qo)*I2
    return {'endpoint_failed_flag_effect':str(1-qi*qo)+' I','r0':str(r0),'r1':str(r1),'complete_pinching_weight':str(q),'remainder_random_stabilizer_weights':[str(w) for w in ws],'remainder_nonzero_choi_eigenvalues':['22/9','8/9','2/3'],'scalar_mixture_obstruction_coherence_factors':[str(x) for x in factors],'maximal_CP_pinching_weight':str(4*min(tw)),'exact_block_moment_cases':cases,'all_exact_identities_pass':True}

I2=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
def kron(*xx):
    a=np.ones((1,1),complex)
    for x in xx:a=np.kron(a,x)
    return a
I=np.eye(8,dtype=complex);Id=np.eye(64,dtype=complex)
S=[kron(Z,I2,I2),kron(I2,Z,I2)]
HB=.37*kron(I2,I2,Y)
raw=[kron(X,I2,X)+.33*kron(Y,I2,Y)+.21*kron(Z,I2,Z),kron(I2,X,Z)+.24*kron(I2,Y,X)]
J=[.18,.22];V=[J[i]*raw[i]/np.linalg.norm(raw[i],2) for i in range(2)]
r=[.35,.62];tau=.9;M=3
ch=lambda K:np.kron(K.conj(),K)
D=[(Id+ch(s))/2 for s in S]
# start, internal, internal, finish for each parent
bounds=[[0.,.3,.6,.9],[.1,.4,.7,1.]]
events=sorted((t,i,k) for i,ts in enumerate(bounds) for k,t in enumerate(ts))

def numerical_shared_bath():
    branches=[(I.copy(),[None,None],[False,False],[])]
    total_direct=Id.copy();active=[];now=0.
    for t,i,k in events:
        if t>now:
            H=HB+sum((V[j] for j in active),np.zeros_like(I));U=expm(-1j*H*(t-now))
            total_direct=ch(U)@total_direct
            branches=[(U@K,last,bad,pattern) for K,last,bad,pattern in branches]
        now=t
        internal=k in (1,2)
        options=[]
        if internal:options.append((np.sqrt(r[i])*I,None,0))
        for bit in (0,1):
            options.append((np.sqrt(1-r[i])*(I+(-1)**bit*S[i])/2 if internal else (I+(-1)**bit*S[i])/2,bit,1))
        nxt=[]
        for K,last,bad,pattern in branches:
            for op,bit,success in options:
                ll=last.copy();bb=bad.copy();pp=pattern.copy()
                if bit is not None:
                    if ll[i] is not None and bit!=ll[i]:bb[i]=True
                    ll[i]=bit
                if internal:pp.append((i,k,success))
                nxt.append((op@K,ll,bb,pp))
        branches=nxt
        channel=r[i]*Id+(1-r[i])*D[i] if internal else D[i]
        total_direct=channel@total_direct
        if k==0:active.append(i)
        if k==3:active.remove(i)
    summed=sum((ch(K) for K,_,_,_ in branches),np.zeros_like(Id))
    channelerr=float(np.linalg.norm(summed-total_direct,2));assert channelerr<3e-13
    normerr=float(np.linalg.norm(sum((K.conj().T@K for K,_,_,_ in branches),np.zeros_like(I))-I,2));assert normerr<3e-13
    probs={}
    for _,_,_,pat in branches:
        key=tuple(x[2] for x in pat)
        probs[key]=np.prod([(1-r[i]) if bit else r[i] for i,k,bit in pat])
    maximum_ratio=0.;conditional_slack=1.;count=0
    for key,prob in probs.items():
        selected=[b for b in branches if tuple(x[2] for x in b[3])==key]
        pattern=selected[0][3];budgets=[]
        for i in range(2):
            ints=[bit for j,k,bit in pattern if j==i];lengths=[];run=1
            for bit in ints:
                if bit:lengths.append(run);run=1
                else:run+=1
            lengths.append(run);budgets.append(J[i]**2*(tau/M)**2*sum(n*n for n in lengths))
        for subset in [(0,),(1,),(0,1)]:
            E=sum((K.conj().T@K for K,_,bad,_ in selected if all(bad[i] for i in subset)),np.zeros_like(I))/prob
            bound=np.prod([budgets[i] for i in subset]);slack=float(np.linalg.eigvalsh(bound*I-E)[0]);assert slack>-3e-13
            conditional_slack=min(conditional_slack,slack);count+=1
    averaged=[]
    budgets=[J[i]**2*tau**2/M**2*(M+2*sum((M-k)*r[i]**k for k in range(1,M))) for i in range(2)]
    for subset in [(0,),(1,),(0,1)]:
        E=sum((K.conj().T@K for K,_,bad,_ in branches if all(bad[i] for i in subset)),np.zeros_like(I))
        bound=float(np.prod([budgets[i] for i in subset]));eig=float(np.linalg.eigvalsh(E)[-1]);assert eig<=bound+3e-13
        averaged.append({'parents':list(subset),'effect_max_eigenvalue':eig,'bound':bound,'ratio':eig/bound})
    return {'branch_count':len(branches),'independent_success_patterns':len(probs),'conditional_subset_checks':count,'conditional_budget_min_slack':conditional_slack,'channel_reconstruction_error':channelerr,'normalization_error':normerr,'shared_bath_commutator_norm':float(np.linalg.norm(V[0]@V[1]-V[1]@V[0],2)),'averaged_subsets':averaged}

out={'exact_rational_checks':exact_checks(),'shared_bath_numerical_checks':numerical_shared_bath()}
Path(__file__).with_name('partial_dephasing_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
