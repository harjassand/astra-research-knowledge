#!/usr/bin/env python3
"""Independent deterministic checks. Does not import/execute the author script."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parent
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]]); Z=s.diag(1,-1)
P=[X,Y,Z]
qs=[(1,0,0,0),(0,1,0,0),(F(1,2),)*4,(F(3,5),F(4,5),0,0),(F(1,3),F(2,3),F(2,3),0)]
def rat(x): return s.Rational(x.numerator,x.denominator) if isinstance(x,F) else s.Rational(x)
def unit(q): return rat(q[0])*I-s.I*sum((rat(q[j+1])*P[j] for j in range(3)),s.zeros(2))
def bloch(U): return s.Matrix(3,3,lambda a,j:s.simplify(s.trace(P[a]*U*P[j]*U.conjugate().T)/2))
def Kmat(M):
    xx,yy,zz=M[0,0],M[1,1],M[2,2]
    return s.Matrix([[xx+yy+zz,M[2,1]-M[1,2],M[0,2]-M[2,0],M[1,0]-M[0,1]],
      [M[2,1]-M[1,2],xx-yy-zz,M[0,1]+M[1,0],M[0,2]+M[2,0]],
      [M[0,2]-M[2,0],M[0,1]+M[1,0],-xx+yy-zz,M[1,2]+M[2,1]],
      [M[1,0]-M[0,1],M[0,2]+M[2,0],M[1,2]+M[2,1],-xx-yy+zz]])

moment_cases=born_terms=mean_cases=rotation_identity_cases=channel_cases=0
V=I.col_join(s.zeros(2))
for q in qs:
    U=unit(q); assert s.simplify(U.conjugate().T*U)==I
    H=s.zeros(2).row_join(U.conjugate().T).col_join(U.row_join(s.zeros(2)))
    assert s.simplify(H*H)==s.eye(4)
    for degree in range(25):
        assert s.simplify(V.T*(H**degree)*V)==(I if degree%2==0 else s.zeros(2))
        moment_cases+=1
    for Pj in P:
        for sg in [-1,1]:
            rho=(I+sg*Pj)/2;encoded=V*rho*V.T
            A=s.Rational(4,5)*s.eye(4)-s.I*s.Rational(3,5)*H
            B=s.Rational(4,5)*s.eye(4)+s.I*s.Rational(3,5)*H
            out=(A*encoded*A.conjugate().T+B*encoded*B.conjugate().T)/2
            expected=s.diag(s.Rational(16,25)*rho,s.Rational(9,25)*U*rho*U.conjugate().T)
            assert s.simplify(out-expected)==s.zeros(4)
            channel_cases+=1
    R=bloch(U); assert R.T*R==s.eye(3) and R.det()==1
    for p in [s.Rational(0),s.Rational(1,7),s.Rational(1,2),s.Rational(1)]:
        mean=s.zeros(3);second=s.Rational(0);total=s.Rational(0)
        for j in range(3):
            for sg in [-1,1]:
                rho=(I+sg*P[j])/2
                for a in range(3):
                    for b in [-1,1]:
                        pr=s.simplify(p*s.trace((I+b*P[a])/2*U*rho*U.conjugate().T)/18)
                        assert pr>=0
                        obs=s.zeros(3);obs[a,j]=9*sg*b
                        mean+=pr*obs;second+=pr*81;total+=pr;born_terms+=1
        assert s.simplify(mean-p*R)==s.zeros(3)
        assert second==81*p and total==p
        assert s.trace((p*R).T*(p*R))==3*p*p
        mean_cases+=1
    for q2 in qs:
        U2=unit(q2);R2=bloch(U2)
        t2=s.trace((R2-R).T*(R2-R))
        assert s.simplify(1-abs(s.trace(U2.conjugate().T*U))**2/4-t2/8)==0
        rotation_identity_cases+=1

# Exact all-CPTP lower witness: the I/X-average Choi is a separable X-basis state.
phi=s.Matrix([1,0,0,1])/s.sqrt(2);bell=phi*phi.T
IX=s.kronecker_product(I,X)
dephased=(bell+IX*bell*IX)/2
plus=s.Matrix([1,1])/s.sqrt(2);minus=s.Matrix([1,-1])/s.sqrt(2)
pp=s.kronecker_product(plus,plus);mm=s.kronecker_product(minus,minus)
assert s.simplify(dephased-(pp*pp.T+mm*mm.T)/2)==s.zeros(4)

# Deterministic general-d Weyl twirl on all matrix units.
weyl_cases=0;max_weyl_error=0.
for d in range(2,7):
    shift=np.roll(np.eye(d),1,axis=0)
    phase=np.diag(np.exp(2j*np.pi*np.arange(d)/d))
    ws=[np.linalg.matrix_power(shift,a)@np.linalg.matrix_power(phase,b) for a in range(d) for b in range(d)]
    for i in range(d):
        for j in range(d):
            e=np.zeros((d,d),complex);e[i,j]=1
            out=sum((w@e@w.conj().T for w in ws))/d**2
            target=np.eye(d)/d if i==j else np.zeros((d,d))
            err=float(np.max(abs(out-target)));max_weyl_error=max(max_weyl_error,err)
            assert err<1e-13;weyl_cases+=1

# Independent exact finite rational Jacobi fitting at the modified scale 64.
fit_results=[];risk_curvature_cases=0
for M,N in [(s.zeros(3),1),(s.diag(1,0,0),7),
             (s.Matrix([[3,-1,2],[0,2,-1],[1,0,3]]),17),
             (s.Matrix([[0,3,0],[-2,0,1],[1,0,-3]])/2,128)]:
    delta=s.Rational(1,N);eta=delta/32
    K=Kmat(M);A=K/64+s.eye(4)/4;Q=s.eye(4)
    assert s.trace(A)==1 and s.trace(M.T*M)<=81
    cap=16*math.ceil(math.log2(float(128/(eta*eta))))
    steps=0
    def energy(B): return sum((B[i,j]**2 for i in range(4) for j in range(4) if i!=j))
    while energy(A)>eta**2/16:
        old=energy(A)
        i,j=max(((i,j) for i in range(4) for j in range(i+1,4)),key=lambda ij:abs(A[ij[0],ij[1]]))
        angle=.5*math.atan2(float(2*A[i,j]),float(A[i,i]-A[j,j]))
        t=s.Rational(round(math.tan(angle/2)*2**60),2**60)
        c,ss=(1-t*t)/(1+t*t),2*t/(1+t*t)
        T=s.eye(4);T[i,i]=T[j,j]=c;T[i,j]=-ss;T[j,i]=ss
        assert T.T*T==s.eye(4)
        A=T.T*A*T;Q=Q*T;steps+=1
        assert energy(A)<=(1-s.Rational(2,16))*old+eta**2/(64*16)
        assert steps<=cap
    assert Q.T*Q==s.eye(4)
    D=Q.T*K*Q
    residual2=sum((D[i,j]**2 for i in range(4) for j in range(4) if i!=j))
    assert residual2<=delta**2/4
    col=max(range(4),key=lambda j:D[j,j]);q=Q[:,col]
    assert (q.T*q)[0]==1
    U=unit(q);assert s.simplify(U.conjugate().T*U)==I and s.simplify(U.det())==1
    R=bloch(U)
    assert s.simplify(s.trace(R.T*M)-(q.T*K*q)[0])==0
    for true_q in qs:
        Rtrue=bloch(unit(true_q));t2=s.trace((R-Rtrue).T*(R-Rtrue))
        assert s.simplify(s.trace(R.T*M)-s.trace(Rtrue.T*M)+delta)>=0
        for p in [s.Rational(1,100),s.Rational(1,3),s.Rational(1)]:
            E=M-p*Rtrue;err2=s.trace(E.T*E)
            assert s.simplify(4*err2/(p*p)+4*delta/p-t2)>=0
            risk_curvature_cases+=1
    bits=max(max(abs(x.p).bit_length(),int(x.q).bit_length()) for x in Q)
    fit_results.append(dict(N=N,steps=steps,cap=cap,quaternion_max_bits=bits,
                            residual_bound=float(s.sqrt(residual2)),delta=float(delta)))

# A retained Bell probe and causal history-controlled entangling operations:
# evaluate all branch densities, comparing I and X on the no-leak branch.
cnot=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
adaptive_cases=0
for N in [1,2,3,4]:
    for p in [s.Rational(1,7),s.Rational(1,2)]:
        noleaks=[]
        for W in [I,X]:
            states={():bell}
            for n in range(N):
                nxt={}
                for hist,rho in states.items():
                    U=unit(qs[(n+sum(hist)+2)%len(qs)])
                    ctl=cnot*s.kronecker_product(U,I)
                    rho=ctl*rho*ctl.conjugate().T
                    for f,weight in [(0,1-p),(1,p)]:
                        act=s.kronecker_product(I,W if f else I)
                        nxt[hist+(f,)]=weight*act*rho*act.conjugate().T
                states=nxt
            assert s.simplify(sum(s.trace(rho) for rho in states.values()))==1
            noleaks.append(states[(0,)*N])
        assert noleaks[0]==noleaks[1]
        assert s.simplify(s.trace(noleaks[0])-(1-p)**N)==0
        adaptive_cases+=1

lower_cases=0
for N in range(1,257):
    p=F(1,N+1);lower=p*(1-p)**N/2
    assert lower>=F(1,12*N)
    assert F(81,2*N)+F(1,2*N)==F(41,N)
    lower_cases+=1

receipt=json.loads((ROOT/'ordinary_onsite_two_axis_frozen_memory_recovery_statistics_receipt_20261028.json').read_text())
for path,h in receipt['sha256'].items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,path
source=ROOT/'compressed_moments_hidden_orientation_bridge_20261028.md'
out=dict(status='PASS_INDEPENDENT_ORIENTATION_BRIDGE_ALGEBRA_AND_FINITE_CONTROLS',
 source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
 script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 exact_moment_cases=moment_cases,exact_born_terms=born_terms,exact_mean_cases=mean_cases,
 exact_random_sign_channel_cases=channel_cases,exact_fit_risk_curvature_cases=risk_curvature_cases,
 exact_rotation_loss_identities=rotation_identity_cases,
 general_dimension_weyl_matrix_unit_cases=weyl_cases,max_weyl_error=max_weyl_error,
 exact_rational_fit_cases=fit_results,exact_adaptive_no_leak_cases=adaptive_cases,
 exact_lower_budget_cases=lower_cases,received_fit_manifest_entries=len(receipt['sha256']),
 source_calls=0,rng_draws=0,sampled_source_outcomes=0,
 scope='Independent finite algebra, exact rational fitting, deterministic Born distributions and small coherent-probe/adaptive branch maps. No acquisition samples, production gate synthesis or hardware.')
(ROOT/'compressed_moments_hidden_orientation_independent_check_20261028.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
