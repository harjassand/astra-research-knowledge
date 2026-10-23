"""Exact small diagnostics for the P3 conditional-odds and cubic constructions."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math


def bern_product(params, bits):
    return math.prod(p if b else 1-p for p,b in zip(params,bits))


def r(theta,q):
    return theta*theta/q+(1-theta)**2/(1-q)


def minimax_checks():
    intervals=[(F(1,10),F(3,10)),(F(4,5),F(9,10)),
               (F(1,5),F(4,5)),(F(2,3),F(3,4))]
    q=[(a+b)/2 for a,b in intervals]
    d=[(b-a)/2 for a,b in intervals]
    ks=[1+dd*dd/(qq*(1-qq)) for dd,qq in zip(d,q)]
    mix=[F(1,2)+dd*(2*qq-1)/(4*qq*(1-qq)) for dd,qq in zip(d,q)]
    assert all(0<=w<=1 for w in mix)
    states=list(product([0,1],repeat=len(q)))
    qmass=[bern_product(q,x) for x in states]
    k=math.prod(ks)
    endpoints=[]
    for theta in states:
        pars=[intervals[i][theta[i]] for i in range(len(q))]
        mass=[bern_product(pars,x) for x in states]
        risk=sum((p*p/qq for p,qq in zip(mass,qmass)),F(0))
        assert risk==k
        endpoints.append(mass)
    for ix,x in enumerate(states):
        mix2=sum((bern_product(mix,theta)*pm[ix]**2
                  for theta,pm in zip(states,endpoints)),F(0))
        assert mix2==k*qmass[ix]**2
    # A nonproduct positive proposal, chosen arbitrarily for a falsification test.
    pert=[F(1)+F(1,5)*(1 if x[0]==x[1] else -1) for x in states]
    raw=[qq*t for qq,t in zip(qmass,pert)];total=sum(raw,F(0))
    qcor=[v/total for v in raw]
    risks=[sum((p*p/qq for p,qq in zip(pm,qcor)),F(0)) for pm in endpoints]
    assert max(risks)>=k
    return {'joint_minimax_exact':str(k),'joint_minimax_float':float(k),
            'endpoint_risks_all_equal':True,'least_favourable_identity_exact':True,
            'arbitrary_correlated_proposal_worst_risk':float(max(risks))}


def transpose_mv(A,x):
    return [sum((A[i][j]*x[i] for i in range(len(x))),F(0)) for j in range(len(x))]


def trajectory_score(bits,d,T,rho,kappa,sigma,A,b):
    x=[F(0)]*d;s=F(0)
    for t in range(T):
        z=[sum((A[i][j]*x[j] for j in range(d)),F(0)) for i in range(d)]
        x=[rho*x[i]+kappa*z[i]**3+sigma*(2*bits[t*d+i]-1) for i in range(d)]
        assert all(-1<=v<=1 for v in x)
        s+=sum((b[i]*x[i] for i in range(d)),F(0))
    return s


def cubic_checks():
    d=2;T=4;rho=F(1,2);kappa=F(1,20);sigma=F(9,20)
    A=[[F(3,4),F(1,4)],[F(1,4),F(3,4)]];b=[F(1,20),F(1,15)]
    upper=[[rho*(i==j)+3*kappa*A[i][j] for j in range(d)] for i in range(d)]
    vl=list(b);vu=list(b);lo=[None]*T;hi=[None]*T
    for t in range(T-1,-1,-1):
        lo[t]=[2*sigma*v for v in vl];hi[t]=[2*sigma*v for v in vu]
        vl=[b[i]+rho*vl[i] for i in range(d)]
        step=transpose_mv(upper,vu);vu=[b[i]+step[i] for i in range(d)]
    low=[v for row in lo for v in row];high=[v for row in hi for v in row]
    states=list(product([0,1],repeat=d*T))
    scores=[trajectory_score(x,d,T,rho,kappa,sigma,A,b) for x in states]
    minima=[];maxima=[];comparisons=0
    for j in range(d*T):
        mask=1<<(d*T-1-j)
        diffs=[scores[ix^mask]-scores[ix] for ix,x in enumerate(states) if x[j]==0]
        mn=min(diffs);mx=max(diffs)
        assert low[j]<=mn<=mx<=high[j]
        minima.append(mn);maxima.append(mx);comparisons+=len(diffs)
    # Floating diagnostic of estimator variance; the log-ratio proof above is exact.
    endpoints=[(1/(1+math.exp(-float(a))),1/(1+math.exp(-float(bb))))
               for a,bb in zip(low,high)]
    q=[(a+bb)/2 for a,bb in endpoints]
    k=math.prod(max(r(a,qq),r(bb,qq)) for (a,bb),qq in zip(endpoints,q))
    target_raw=[math.exp(float(s))/len(states) for s in scores]
    Z=sum(target_raw)
    mass=[v/Z for v in target_raw]
    qm=[float(bern_product(q,x)) for x in states]
    risk=sum(v*v/qq for v,qq in zip(mass,qm))
    assert risk<=k+1e-12
    return {'d':d,'T':T,'paths':len(states),'exact_ratio_comparisons':comparisons,
            'all_log_ratio_bounds_hold_exactly':True,
            'compiler_lower':[str(x) for x in low],
            'compiler_upper':[str(x) for x in high],
            'observed_lower':[str(x) for x in minima],
            'observed_upper':[str(x) for x in maxima],
            'R_float_diagnostic':risk,'K_float_diagnostic':k}


if __name__=='__main__':
    result={'minimax':minimax_checks(),'cubic':cubic_checks()}
    path=Path(__file__).with_name('minimax_cubic_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    compact={**result,'cubic':{k:v for k,v in result['cubic'].items()
                              if k not in ['observed_lower','observed_upper']}}
    print(json.dumps(compact,indent=2))
