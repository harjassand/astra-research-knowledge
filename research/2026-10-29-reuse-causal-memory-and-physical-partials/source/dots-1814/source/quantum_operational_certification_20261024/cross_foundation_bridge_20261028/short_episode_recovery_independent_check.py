#!/usr/bin/env python3
"""Independent deterministic rational diagnostics; no source sampling or RNG.
Checks the new recovery bridge, not a replacement for its general proof.
Also checks the separately proposed depth-enabled Bell-probe minimax formula.
"""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from math import gcd, lcm
import json
import sympy as s

HERE = Path(__file__).resolve().parent
OUT = HERE / 'short_episode_recovery_independent_check.json'
SOURCES = ['SHORT_EPISODE_ONE_USE_RECOVERY_LOWER_BOUND.md',
 'PHYSICAL_QUADRATIC_DISTINGUISHING_LENGTH.md',
 'PHYSICAL_QUADRATIC_LENGTH_INDEPENDENT_RECEIPT.md',
 'PHYSICAL_QUADRATIC_LENGTH_INDEPENDENT_RECEIPT.json']
lam = F(1,4)
c, t = F(1,2)-lam/4, lam/4
cases=[]
for q in (2,3,4,5,7,8,9,16):
    d=q+1; r=q*q+q+1; kstar=r-2
    alpha=1-F(1,2*r); A=alpha**kstar
    v=A*F(r,8*d*d); Delta=(1-lam)*v
    p=lambda j,k: F(1,2)+F(1,4*d)+alpha**k*F(r*int((k+j)%r==0)-1,8*d*d)
    mu=(p(1,kstar)+p(2,kstar))/2
    assert mu==F(1,2)+F(1,4*d)+A*F(r-2,16*d*d)
    shift=F(1,2)-mu
    feig=(F(1,2)+shift,F(3,4)+shift)
    assert min(feig)>=F(1,4) and max(feig)<=F(3,4)
    f1,f2=p(1,kstar)+shift,p(2,kstar)+shift
    assert (f1,f2)==(F(1,2)-v/2,F(1,2)+v/2)
    ftau=F(1,2)+F(1,4*d)+shift
    assert ftau==F(1,2)-A*F(r-2,16*d*d)
    early=0
    for k in range(r-2):
        assert p(1,k)==p(2,k)
        f=p(1,k)+shift
        # Full Pauli-transfer matrices match, not just one classical outcome.
        T1=(1,1-lam,(1-lam)*(1-2*f),(1-lam)*(1-2*f))
        g=p(2,k)+shift
        T2=(1,1-lam,(1-lam)*(1-2*g),(1-lam)*(1-2*g))
        assert T1==T2
        early+=1
    # In the effect eigenbasis every memory-input/output block has these
    # four exact eigenvalues. Multiplicity of the orthogonal effect is d-1.
    floor=lam/F(2*d)
    spectra=[]
    for fe, mult in ((feig[0],d-1),(feig[1],1)):
        ev=(floor,floor,floor+2*(1-lam)*(1-fe)/d,
            floor+2*(1-lam)*fe/d)
        assert min(ev)==F(1,8*d)
        assert sum(ev)*d==2  # tracing whole Q Choi block, Q input dim=2
        spectra.append({'effect':str(fe),'multiplicity':mult*d,
                        'choi_eigenvalues':[str(x) for x in ev]})
    w1=(c+Delta/2,c-Delta/2,t,t)
    w2=(c-Delta/2,c+Delta/2,t,t)
    assert sum(w1)==sum(w2)==1
    assert w1[0]>max(w1[1:]) and w2[1]>max(w2[0],w2[2],w2[3])
    assert Delta/2>=F(9,512)
    Lstar=1-c-Delta/2
    # All simplex extremal decoder scores. The equal I/X correction achieves
    # common Bell and half-diamond regret Delta/2.
    assert max((w1[i]+w2[i])/2 for i in range(4))==c
    mixed_identity=(w1[0]+w1[1])/2
    assert 1-mixed_identity-Lstar==Delta/2
    cases.append({'q':q,'d':d,'r':r,'early_full_channel_equalities':early,
       'mu':str(mu),'v':str(v),'Delta':str(Delta),
       'oracle_loss':str(Lstar),'minimax_short_regret':str(Delta/2),
       'v_float_supplement':float(v),'regret_float_supplement':float(Delta/2),
       'F_eigenvalues':[str(x) for x in feig],
       'use_choi_floor':str(floor),'forward_choi_floor':str(F(1,2*r*d)),
       'use_spectrum_blocks':spectra})

# Test arbitrary CPTP, non-Pauli decoders by exact Kraus calculations.
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]); Y=s.Matrix([[0,-s.I],[s.I,0]])
Z=s.diag(1,-1); Ps=(I,X,Y,Z)
Ksets={
 'identity':[I], 'X':[X],
 'rational_Y_rotation':[s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],
                                [s.Rational(4,5),s.Rational(3,5)]])],
 'amplitude_damping_9_25':[s.diag(1,s.Rational(4,5)),
                          s.Matrix([[0,s.Rational(3,5)],[0,0]])],
 'reset_zero':[s.Matrix([[1,0],[0,0]]),s.Matrix([[0,1],[0,0]])],
 'Z_dephasing':[s.diag(1,0),s.diag(0,1)],
}
kraus=[]
Delta=F(cases[0]['Delta'])
w1=tuple(map(s.Rational,(c+Delta/2,c-Delta/2,t,t)))
w2=(w1[1],w1[0],w1[2],w1[3])
for name,Ks in Ksets.items():
    assert sum((K.conjugate().T*K for K in Ks),s.zeros(2))==I
    a=tuple(s.simplify(sum(abs(s.trace(K*P))**2 for K in Ks)/4) for P in Ps)
    assert sum(a)==1 and all(x>=0 for x in a)
    score1=sum(x*y for x,y in zip(w1,a)); score2=sum(x*y for x,y in zip(w2,a))
    assert score1<=max(w1) and score2<=max(w2)
    assert (score1+score2)/2<=s.Rational(c)
    kraus.append({'decoder':name,'a_P':[str(x) for x in a],
                   'world_scores':[str(score1),str(score2)]})

# Explicit full QM Choi and TP checks in a memory-effect eigenbasis at d=3.
# Matrix-unit outputs factor tau, hence this identity extends to any reference.
d=3; N=2*d; tau=s.eye(d)/d
feig=list(map(s.Rational,cases[0]['F_eigenvalues']))
Fdiag=[feig[1]]+[feig[0]]*(d-1)
outputs={}; units=0
for a in range(N):
 for b in range(N):
    qi,mi=divmod(a,d); qj,mj=divmod(b,d)
    EQ=s.zeros(2); EQ[qi,qj]=1
    Tout=s.zeros(2)
    if mi==mj:
        Tout=s.Rational(1-lam)*((1-Fdiag[mi])*EQ+Fdiag[mi]*X*EQ*X)
    if a==b: Tout+=s.Rational(lam)*I/2
    output=s.kronecker_product(Tout,tau)
    assert s.trace(output)==int(a==b)
    outputs[(a,b)]=output; units+=1
J=s.zeros(N*N)
for (a,b),output in outputs.items():
 for h in range(N):
  for k in range(N): J[a*N+h,b*N+k]=output[h,k]
# Exact eigenvalues and multiplicities of the 36x36 full-algebra Choi.
eigs=J.eigenvals()
assert sum(eigs.values())==N*N and min(eigs)==s.Rational(1,8*d)
assert all(x>=s.Rational(1,8*d) for x in eigs)

# Exact finite-n Bell-label decision. Integer recurrence avoids sampling.
p=c+Delta/2; m=c-Delta/2; z=2*t
den=lcm(p.denominator,m.denominator,z.denominator)
P,M,Z0=[int(x*den) for x in (p,m,z)]
D={0:1}; finite=[]
for n in range(65):
    if n in (0,1,2,4,8,16,32,64):
        scale=den**n
        assert sum(D.values())==scale
        err=F(sum(count for v,count in D.items() if v<0),scale)+F(D.get(0,0),2*scale)
        # swapping I/X reflects D exactly, so TV reduces to this statistic.
        tv=F(sum(abs(D.get(v,0)-D.get(-v,0)) for v in range(-n,n+1)),2*scale)
        assert err==(1-tv)/2
        if n==0: assert err==F(1,2)
        if n==1: assert tv==Delta
        finite.append({'n':n,'Bayes_error':str(err),'TV':str(tv),
           'minimax_regret':str(Delta*err),
           'Bayes_error_float_supplement':float(err),
           'regret_float_supplement':float(Delta*err)})
    new={}
    for v,count in D.items():
        for dv,weight in ((1,P),(-1,M),(0,Z0)):
            new[v+dv]=new.get(v+dv,0)+count*weight
    D=new

out={'status':'PASS deterministic independent checks',
 'source_sha256':{f:sha256((HERE/f).read_bytes()).hexdigest() for f in SOURCES},
 'source_calls':0,'episode_starts':0,'rng_calls':0,'hardware_executions':0,
 'generic_QE_executed':False,'environment_tomography_performed':False,
 'cases':cases,'non_Pauli_CPTP_decoder_checks':kraus,
 'QM_matrix_units_checked':units,
 'full_use_choi_exact_spectrum_d3':{str(k):v for k,v in eigs.items()},
 'finite_n_constructive_checks':finite}
OUT.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'cases':len(cases),
  'early_full_channel_equalities':sum(z['early_full_channel_equalities'] for z in cases),
  'non_Pauli_CPTP_checks':len(kraus),'QM_matrix_units':units,
  'finite_n_cases':len(finite),'output':str(OUT)},indent=2))
