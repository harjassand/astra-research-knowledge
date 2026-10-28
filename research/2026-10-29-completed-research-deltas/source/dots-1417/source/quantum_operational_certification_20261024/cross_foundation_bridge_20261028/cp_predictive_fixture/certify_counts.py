"""Exact count-only replay. Reads no generator, plant maps or reference probabilities."""
import json, math
from pathlib import Path
import numpy as np
import sympy as s
root=Path(__file__).parent
D=json.loads((root/'counts.json').read_text());N=D['shots_per_setting'];eta=s.Rational(D['radius'])
r=4;H=s.ones(r,r);DH=s.ones(r,r)*eta
for j in range(r):DH[0,j]=0
for x in D['base']:H[x['test'],x['prep']]=s.Rational(x['counts'][0],N)
Hz={};Dz={}
for a,k in D['actions'].items():
    for o in range(k):
        key=(a,o);Hz[key]=s.zeros(r);Dz[key]=s.ones(r)*eta
        if k==1:
            for j in range(r):Hz[key][0,j]=1;Dz[key][0,j]=0
for x in D['shift']:
    for o in range(D['actions'][x['action']]):
        key=(x['action'],o);Hz[key][x['test'],x['prep']]=s.Rational(x['counts'][2*o],N)
        if x['test']==1 and D['actions'][x['action']]>1:
            Hz[key][0,x['prep']]=s.Rational(sum(x['counts'][2*o:2*o+2]),N)
F=[s.eye(2),s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
t=s.Matrix([[2,0,0,0]])
def ab(A):return A.applyfunc(abs)
def choi(W):
    J=s.zeros(4)
    for m in range(4):
        for n in range(4):J+=W[m,n]*s.kronecker_product(F[n].T,F[m])/2
    assert J==J.conjugate().T
    return J

def rational_sqrt_up(x,scale=10**8):
    k=math.isqrt(int(s.floor(x*scale*scale)))
    if s.Rational(k*k,scale*scale)<x:k+=1
    z=s.Rational(k,scale);assert z*z>=x
    return z

def exact_lower(J):
    # Numerical eigensolve only proposes a rational witness; exact minors decide.
    v=float(np.linalg.eigvalsh(np.array(J.evalf(),dtype=complex))[0])
    m=s.Rational(math.floor(v*100000)-1,100000)
    if m<=0:return None
    B=J-m*s.eye(4)
    assert all(s.simplify(B[:k,:k].det())>0 for k in range(1,5))
    return m

def rec(x):return {'exact':str(x),'float':float(x)}
results=[]
for qstr in D['candidate_bloch_radii']:
    q=s.Rational(qstr)
    P=s.Matrix([[s.Rational(1,2)]*4,[0,q/2,0,0],[0,0,q/2,0],[0,0,0,q/2]])
    S=P.inv();assert s.ones(1,4)*S==t
    rho0=sum((P[i,0]*F[i] for i in range(4)),s.zeros(2));assert rho0==s.eye(2)/2
    V=H*S;U=V.inv();DV=DH*ab(S);A=ab(U)*DV
    anorm=max(sum(A[i,j] for j in range(4)) for i in range(4));assert anorm<1
    M=(s.eye(4)-A).inv()*ab(U)
    fit={z:U*h*S for z,h in Hz.items()}
    for a,k in D['actions'].items():assert t*sum((fit[(a,o)] for o in range(k)),s.zeros(4))==t
    rows={};Eall={};passed=True
    for z,w in fit.items():
        # V*w = H_z*S exactly; no repair residual is hidden.
        assert V*w==Hz[z]*S
        E=M*(Dz[z]*ab(S)+DV*ab(w));Eall[z]=E
        kappa=rational_sqrt_up(sum(e*e for e in E));m=exact_lower(choi(w))
        if m is None or kappa>m:passed=False
        rows[f'{z[0]}:{z[1]}']={'kappa':rec(kappa),'choi_lower':None if m is None else rec(m),
                                    'epsilon':None if m is None else rec(kappa/m)}
    x={'q':qstr,'pass':passed,'inverse_neumann_norm':rec(anorm),'branches':rows}
    if passed:
        eps=max(s.Rational(v['epsilon']['exact']) for v in rows.values())
        local=max(sum(s.Rational(rows[f'{a}:{o}']['kappa']['exact']) for o in range(k)) for a,k in D['actions'].items())
        # d=2: half diamond <= d/2 sum kappa = sum kappa.
        local=min(s.Integer(1),local,eps);delta=s.Rational(2,5);gamma=1-delta
        clock_add=min(s.Integer(1),gamma*local/delta);clock_mix=gamma*eps/(delta+gamma*eps)
        w=fit[('rotate',0)];E=Eall[('rotate',0)]
        trace_lower=s.trace(w)-s.trace(E)
        trsq_upper=s.trace(w*w)+2*sum(abs(w[i,j])*E[j,i] for i in range(4) for j in range(4))+s.trace(E*E)
        separator=trace_lower**2-4*trsq_upper
        assert trace_lower>0 and separator>0
        x.update({'epsilon':rec(eps),'local_half_diamond_bound':rec(local),'clock_additive':rec(clock_add),
                  'clock_common_cp':rec(clock_mix),'no_four_state_hmm_witness_gap':rec(separator)})
    results.append(x)
passing=[x for x in results if x['pass']]
assert passing
best=min(passing,key=lambda x:s.Rational(x['local_half_diamond_bound']['exact']))
summary={'method':'rational interval inversion, rational Choi principal-minor witnesses, rational domination and spectral witness',
         'counts_only':True,'plant_imports':False,'candidates_checked':len(results),'selected_q':best['q'],
         'failure_probability_upper':312*math.exp(-2*N*float(eta)**2),
         'represented_resets':D['represented_resets'],'represented_native_calls':D['represented_native_calls'],
         'selected':best,'candidates':results}
(root/'certificate.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['candidates','selected']},indent=2))
print(json.dumps({k:v for k,v in best.items() if k!='branches'},indent=2))
