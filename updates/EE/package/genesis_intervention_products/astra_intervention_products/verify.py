#!/usr/bin/env python3
"""Exact falsification checks for intervention-product completion.

No stochastic data or experimental results are fabricated. All exact checks use
rational finite matrices. Floating finite-time checks are explicitly diagnostic.
"""
from __future__ import annotations
import json
import random
from pathlib import Path
from typing import Sequence
import sympy as S
import numpy as np
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parent
checks: list[str] = []

def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    checks.append(name)

def eq(A: S.Matrix, B: S.Matrix) -> bool:
    return A.shape == B.shape and all(S.cancel(x) == 0 for x in A-B)

def generator(off: S.Matrix) -> S.Matrix:
    n = off.rows
    Q = off.copy()
    for i in range(n):
        Q[i,i] = -sum(Q[i,j] for j in range(n) if j != i)
    return Q

def controlled(Q: S.Matrix, gains: S.Matrix) -> S.Matrix:
    return generator(Q.multiply_elementwise(gains))

def indicators(labels: Sequence[int]) -> S.Matrix:
    k = max(labels)+1
    return S.Matrix([[int(a == b) for b in range(k)] for a in labels])

def geo(Q: S.Matrix, labels: Sequence[int], a: int) -> S.Matrix:
    n = Q.rows
    return generator(S.Matrix(n,n,lambda i,j: S.Rational(1,2)*Q[i,j]*(int(labels[j]==a)-int(labels[i]==a)) if i != j else 0))

def direct_residual(Q: S.Matrix, nu: S.Matrix, E: S.Matrix) -> S.Matrix:
    R = S.diag(*list(nu))
    M = S.diag(*list(nu*E))
    A = E.T*R*Q*E
    B = Q*E-E*M.inv()*A
    return B.T*R*B

def cross_moments(Ps: list[S.Matrix], products: list[list[S.Matrix]], nu: S.Matrix, labels: Sequence[int], full_activity: bool=False):
    p, n, k = len(Ps), Ps[0].rows, max(labels)+1
    H = S.zeros(p,p)
    b = S.zeros(k,p)
    c = S.zeros(k,1)
    for u in range(p):
        for v in range(p):
            H[u,v] = sum(nu[i]*products[u][v][i,j] for i in range(n) for j in range(n) if i!=j and (full_activity or labels[i]!=labels[j]))
        for a in range(k):
            b[a,u] = sum(nu[i]*Ps[u][i,j]*S.Rational(int(labels[j]==a)-int(labels[i]==a),2) for i in range(n) for j in range(n) if i!=j)
    Q=Ps[0]
    for a in range(k):
        c[a] = sum(nu[i]*Q[i,j]*S.Rational((int(labels[j]==a)-int(labels[i]==a))**2,4) for i in range(n) for j in range(n) if i!=j)
    return H,b,c

def minimize_exact(H: S.Matrix, b: S.Matrix, c: S.Expr, zero_sum: bool=True):
    """Minimize w'Hw-2b'w+c using exact normal equations.

    This verifier has no l1-budget optimizer. The production theorem uses a
    budgeted convex quadratic program and a posteriori certificates.
    """
    p=H.rows
    U=S.zeros(p,p-1) if zero_sum else S.eye(p)
    if zero_sum:
        for j in range(p-1):
            U[0,j]=-1
            U[j+1,j]=1
    K=U.T*H*U
    h=U.T*b
    sol,params=K.gauss_jordan_solve(h)
    sol=sol.subs({z:0 for z in params})
    w=U*sol
    err=S.cancel((w.T*H*w)[0]-2*(b.T*w)[0]+c)
    return w,err

def moment_residual_direct(Q: S.Matrix, gains: list[S.Matrix], nu: S.Matrix, labels: Sequence[int], a: int, w: S.Matrix, full: bool=False):
    n=Q.rows
    ans=0
    for i in range(n):
        for j in range(n):
            if i==j or (not full and labels[i]==labels[j]):
                continue
            target=S.Rational(int(labels[j]==a)-int(labels[i]==a),2)
            gain=sum(w[u]*gains[u][i,j] for u in range(len(gains)))
            ans += nu[i]*Q[i,j]*(gain-target)**2
    return S.cancel(ans)

def recovered_gram(Q: S.Matrix, Ps: list[S.Matrix], nu: S.Matrix, labels: Sequence[int], weights: list[S.Matrix]) -> S.Matrix:
    E=indicators(labels); R=S.diag(*list(nu)); M=S.diag(*list(nu*E)); A=E.T*R*Q*E
    k=E.cols
    G=S.zeros(k,k)
    for a in range(k):
        Da=S.diag(*list(E[:,a]))
        W=sum((weights[a][u]*Ps[u] for u in range(len(Ps))),S.zeros(Q.rows))
        for b in range(k):
            g=E[:,b]
            G[a,b]=(nu*Q*Da*Q*g-nu*Da*Q*Q*g-2*nu*W*Q*g)[0]
    return G-A.T*M.inv()*A

rng=random.Random(7102026)
random_cases=[]
for case in range(18):
    n=4+case%3; k=2+case%2
    labels=[i%k for i in range(n)]
    Q=generator(S.Matrix(n,n,lambda i,j: S.Rational(rng.randint(1,9),64) if i!=j else 0))
    nv=[rng.randint(1,7) for _ in range(n)]; nu=S.Matrix([[S.Rational(x,sum(nv)) for x in nv]])
    E=indicators(labels); R=S.diag(*list(nu)); M=S.diag(*list(nu*E)); A=E.T*R*Q*E
    G=S.zeros(k,k)
    for a in range(k):
        Da=S.diag(*list(E[:,a])); V=geo(Q,labels,a)
        for b0 in range(k):
            f=E[:,b0]
            G[a,b0]=(nu*Q*Da*Q*f-nu*Da*Q*Q*f-2*nu*V*Q*f)[0]
    check(f'nonstationary_completion_{case}',eq(G,E.T*Q.T*R*Q*E))
    check(f'nonstationary_residual_{case}',eq(G-A.T*M.inv()*A,direct_residual(Q,nu,E)))
    gains=[S.ones(n)]
    for u in range(3):
        gains.append(S.Matrix(n,n,lambda i,j: 1 if labels[i]==labels[j] else S.Rational(rng.randint(2,9),5)))
    Ps=[controlled(Q,g) for g in gains]
    products=[[controlled(Q,g.multiply_elementwise(h)) for h in gains] for g in gains]
    H,b,c=cross_moments(Ps,products,nu,labels)
    for a in range(k):
        w,err=minimize_exact(H,b[a,:].T,c[a])
        direct=moment_residual_direct(Q,gains,nu,labels,a,w)
        check(f'positive_moment_identity_{case}_{a}',err==direct and err>=0)
        W=sum((w[u]*Ps[u] for u in range(len(Ps))),S.zeros(n))
        Lam=max(-Q[i,i] for i in range(n))
        for bb in range(k):
            val=(nu*(W-geo(Q,labels,a))*Q*E[:,bb])[0]
            check(f'kinetic_energy_bound_{case}_{a}_{bb}',S.cancel(val**2-4*Lam**3*err)<=0)
    random_cases.append({'case':case,'n':n,'labels':k,'nonstationary':not eq(nu*Q,S.zeros(1,n))})

# Exact heterogeneous-gain acquisition. The estimator sees only moments.
Q=S.Matrix([[-11,3,5,3],[3,-11,3,5],[3,5,-13,5],[5,3,5,-13]])/16
labels=[0,1,0,1]; E=indicators(labels); nu=S.Matrix([[S.Rational(1,10),S.Rational(2,10),S.Rational(3,10),S.Rational(4,10)]])
z=S.ones(4)
for i in range(4):
    for j in range(4):
        if labels[i]!=labels[j]:
            z[i,j]=([S.Rational(1,2),S.Rational(2,3)] if labels[i]==0 else [S.Rational(3,2),S.Integer(2)])[(i+j)//2%2]
D=4
gains=[z.applyfunc(lambda x:x**j) for j in range(D+1)]
Ps=[controlled(Q,g) for g in gains]
products=[[controlled(Q,g.multiply_elementwise(h)) for h in gains] for g in gains]
H,b,c=cross_moments(Ps,products,nu,labels)
weights=[]; errors=[]
for a in range(2):
    w,err=minimize_exact(H,b[a,:].T,c[a]); weights.append(w); errors.append(err)
    check(f'heterogeneous_zero_certificate_{a}',err==0)
    W=sum((w[u]*Ps[u] for u in range(D+1)),S.zeros(4))
    check(f'heterogeneous_actual_synthesis_{a}',eq(W,geo(Q,labels,a)))
Ghat=recovered_gram(Q,Ps,nu,labels,weights); Gtrue=direct_residual(Q,nu,E)
check('heterogeneous_observed_recovery',eq(Ghat,Gtrue))

# Deliberately omit the nonstationary correction: this must fail here.
R=S.diag(*list(nu)); M=S.diag(*list(nu*E)); A=E.T*R*Q*E
naive=S.zeros(2)
for a in range(2):
    Da=S.diag(*list(E[:,a])); V=geo(Q,labels,a)
    for bb in range(2):
        naive[a,bb]=(-nu*Da*Q*Q*E[:,bb]-2*nu*V*Q*E[:,bb])[0]
naive-=A.T*M.inv()*A
check('stationary_formula_fails_off_stationarity',not eq(naive,Gtrue))

# Gain collision: a single scalar gain used for both directions cannot synthesize
# opposite target signs, regardless of the available polynomial degree.
zcol=S.Matrix(4,4,lambda i,j:1 if labels[i]==labels[j] else 2)
gcol=[zcol.applyfunc(lambda x:x**j) for j in range(3)]
pc=[controlled(Q,g) for g in gcol]
ppc=[[controlled(Q,g.multiply_elementwise(h)) for h in gcol] for g in gcol]
Hc,bc,cc=cross_moments(pc,ppc,nu,labels)
wc,ec=minimize_exact(Hc,bc[0,:].T,cc[0])
flux=sum(nu[i]*Q[i,j] for i in range(4) for j in range(4) if labels[i]!=labels[j])
mean=bc[0,0]/flux
conditional_variance=S.cancel(cc[0]-flux*mean**2)
check('collision_residual_matches_conditional_variance',ec==conditional_variance and ec>0)

# Source clocks satisfy product composition but violate internal neutrality.
# Cross-only calibration wrongly reports zero residual. The full activity
# version detects the missing information.
uniform=S.ones(1,4)/4
zclock=S.Matrix(4,4,lambda i,j:2 if labels[i]==0 else S.Rational(1,2))
gclock=[zclock.applyfunc(lambda x:x**j) for j in range(3)]
pclock=[controlled(Q,g) for g in gclock]
ppclock=[[controlled(Q,g.multiply_elementwise(h)) for h in gclock] for g in gclock]
Hk,bk,ck=cross_moments(pclock,ppclock,uniform,labels)
ww=[]
for a in range(2):
    w,e=minimize_exact(Hk,bk[a,:].T,ck[a]); ww.append(w)
    check(f'clock_false_cross_zero_{a}',e==0)
wrong=recovered_gram(Q,pclock,uniform,labels,ww)
actual=direct_residual(Q,uniform,E)
check('clock_demonstrates_neutrality_is_essential',not eq(wrong,actual))
Ha,ba,ca=cross_moments(pclock,ppclock,uniform,labels,True)
wa,ea=minimize_exact(Ha,ba[0,:].T,ca[0],False)
check('activity_complete_clock_residual_positive',ea>0)
check('activity_complete_moment_identity',ea==moment_residual_direct(Q,gclock,uniform,labels,0,wa,True))

# Exact statistical/model-error envelope for perturbed product moment matrices.
for case in range(5):
    w=weights[0]; xi=S.Rational(case+1,10000)
    perturb=S.Matrix(H.rows,H.cols,lambda i,j:xi*(1 if (i+j)%2 else -1))
    observed=H+perturb
    est=(w.T*observed*w)[0]-2*(b[0,:]*w)[0]+c[0]
    W=sum(abs(x) for x in w)
    check(f'product_calibration_error_envelope_{case}',S.cancel(est+xi*W**2)>=0)

# Floating finite-time mixed derivatives are diagnostic, not exact evidence.
Qf=np.array(Q,float); nuf=np.array(nu,float); Ef=np.array(E,float)
float_checks=[]
for j in [1,2,4]:
    Pf=np.array(Ps[j],float)
    exact=float((nu*Ps[j]*Q*E[:,0])[0])
    for h in [1e-3,2e-4]:
        val=float(((nuf@expm(h*Pf)@expm(h*Qf)@Ef[:,0]-nuf@expm(h*Pf)@Ef[:,0]-nuf@expm(h*Qf)@Ef[:,0]+nuf@Ef[:,0])/h**2).item())
        float_checks.append({'setting':j,'h':h,'value':val,'exact_jet':exact,'absolute_error':abs(val-exact)})

out={
 'status':'internally checked research candidate; no external review or physical data',
 'exact_assertion_count':len(checks),
 'random_nonstationary_cases':random_cases,
 'heterogeneous_example':{
    'Q':[[str(Q[i,j]) for j in range(4)] for i in range(4)],
    'nu':[str(x) for x in nu],
    'labels':labels,
    'unknown_gain_matrix':[[str(z[i,j]) for j in range(4)] for i in range(4)],
    'degree':D,
    'weights':[[str(x) for x in w] for w in weights],
    'coefficient_l1':[str(sum(abs(x) for x in w)) for w in weights],
    'measured_residuals':[str(x) for x in errors],
    'Gamma':[[str(Gtrue[i,j]) for j in range(2)] for i in range(2)],
    'naive_stationary_formula':[[str(naive[i,j]) for j in range(2)] for i in range(2)],
 },
 'collision_residual':str(ec),
 'source_clock':{
   'cross_only_reconstruction':[[str(wrong[i,j]) for j in range(2)] for i in range(2)],
   'actual_Gamma':[[str(actual[i,j]) for j in range(2)] for i in range(2)],
   'full_activity_minimum_residual':str(ea),
 },
 'floating_diagnostic_count':len(float_checks),
 'floating_diagnostics':float_checks,
 'exact_checks':checks,
}
(ROOT/'verification_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['exact_assertion_count','floating_diagnostic_count','heterogeneous_example','collision_residual','source_clock']},indent=2))
