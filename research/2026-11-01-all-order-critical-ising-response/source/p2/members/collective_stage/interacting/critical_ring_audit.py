"""Independent tests of the finite-ring positive-defect response theorem.

Rational identities are checked against full physical Gibbs configurations.
Finite physical response comparisons use full-state symmetric CG. The closed
bound for large n stores no configurations; it is a floating evaluation of
the exact rational theorem, with stable expm1 formulas.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import math
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import time
import numpy as np
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import LinearOperator, cg


def scalar_formulas(n,t,eta,nu=1):
    gamma=2*t/(1+t*t)
    v=(1+t)/(1-t)*(1-t**n)/(1+t**n)
    alpha=(2*t+t**(n-2)-t*t-2*t**(n-1))/(1-t**n)
    kappa=nu*(1-gamma*(1+eta)+eta*alpha)
    q=(1-t*t)**2/(1-t**(2*n))*(1-t**(2*n-4)+2*t**(n-3)*(1-t*t))
    lower=n*v/kappa
    delta=eta*eta/(1-abs(eta))*(q/v)*F(n-2,n)/(gamma*(kappa/nu))
    return dict(gamma=gamma,v=v,alpha=alpha,kappa=kappa,q=q,lower=lower,delta=delta,upper=lower*(1+delta))


def exact_identities(n):
    """Full Gibbs state sums use integer physical weights R^aligned, R=n."""
    t=F(n-1,n+1);gamma=2*t/(1+t*t)
    spins=[[2*((x>>i)&1)-1 for i in range(n)] for x in range(1<<n)]
    weights=[n**sum(s[i]==s[(i+1)%n] for i in range(n)) for s in spins]
    z=sum(weights)
    @lru_cache(None)
    def moment(mask):
        total=0
        for s,w in zip(spins,weights):
            v=1
            for i in range(n):
                if mask>>i&1:v*=s[i]
            total+=w*v
        return F(total,z)
    def mask(sites):
        ans=0
        for i in sites:ans^=1<<(i%n)
        return ans
    variance_per_site=sum(moment(mask([0,i])) for i in range(n))
    def mt(a,b):
        return sum(moment(mask([i,0,a,a+b])) for i in range(n))
    alpha=mt(1,1)/variance_per_site
    formulas=scalar_formulas(n,t,F(2,5))
    checks={'magnetization_variance':variance_per_site==formulas['v'],
            'contact_projection':alpha==formulas['alpha'],
            'all_gap_projections':True,'all_covariance_rows':True,
            'positive_contact_maximum':True,'polynomial_supersolution':True}
    largest=F(0);smallest=None
    for a in range(1,n-1):
        for b in range(1,n-a):
            c=n-a-b
            corrmt=mt(a,b)
            al=(t**a+t**b+t**c-t**(a+b)-t**(b+c)-t**(c+a))/(1-t**n)
            checks['all_gap_projections'] &= corrmt==al*variance_per_site
            tt=sum(moment(mask([i-1,i,i+1,0,a,a+b])) for i in range(n))
            q=tt-alpha*corrmt
            qform=(1-t*t)**2/(1-t**(2*n))*sum(t**(x+y-2)*(1-t**(2*zz))
                    for x,y,zz in [(a,b,c),(b,c,a),(c,a,b)])
            checks['all_covariance_rows'] &= q==qform
            checks['positive_contact_maximum'] &= 0<q<=formulas['q']
            largest=max(largest,q);smallest=q if smallest is None else min(smallest,q)
            h=F(a*b*c,n)/gamma
            hs=[]
            for i,j in [(0,1),(1,0),(0,2),(2,0),(1,2),(2,1)]:
                gaps=[a,b,c];gaps[i]+=1;gaps[j]-=1
                hs.append(F(gaps[0]*gaps[1]*gaps[2],n)/gamma if min(gaps)>0 else F(0))
            Hh=3*h-gamma/2*sum(hs)
            checks['polynomial_supersolution'] &= Hh==1+3*(1-gamma)*h
    return dict(n=n,checks=checks,all_exact=all(checks.values()),
                q_min=float(smallest),q_max=float(largest),q_contact=float(formulas['q']))


def physical_response(n,eta):
    t=(n-1)/(n+1);gamma=(n*n-1)/(n*n+1)
    size=1<<n;ids=np.arange(size)
    spins=2*((ids[:,None]>>np.arange(n))&1)-1
    aligned=(spins==np.roll(spins,-1,axis=1)).sum(axis=1)
    logp=aligned*np.log(n);prob=np.exp(logp-logp.max());prob/=prob.sum();g=np.sqrt(prob)
    M=spins.sum(axis=1);f=g*M
    rows=[];cols=[];values=[];diagonal=np.zeros(size)
    for i in range(n):
        left=spins[:,(i-1)%n];right=spins[:,(i+1)%n]
        rate=.5*(1+eta*left*right)*(1-gamma/2*spins[:,i]*(left+right))
        to=ids^(1<<i)
        diagonal+=rate
        rows.append(ids);cols.append(to);values.append(-rate*g/g[to])
    rows.append(ids);cols.append(ids);values.append(diagonal)
    K=coo_matrix((np.concatenate(values),(np.concatenate(rows),np.concatenate(cols))),shape=(size,size)).tocsr()
    K=(K+K.T)/2
    operator=LinearOperator((size,size),matvec=lambda x:K@x+g*(g@x))
    count=[0]
    def callback(x):count[0]+=1
    u,status=cg(operator,f,M=diags(1/(diagonal+prob)),rtol=1e-12,atol=0.,maxiter=10000,callback=callback)
    truth=float(f@u)
    form=scalar_formulas(n,F(n-1,n+1),F(str(eta)))
    lower=float(form['lower']);upper=float(form['upper'])
    return dict(n=n,eta=eta,response=truth,lower=lower,upper=upper,
                relative_width=float(form['delta']),actual_relative_correction=truth/lower-1,
                enclosure_pass=bool(lower<=truth*(1+1e-10) and truth<=upper*(1+1e-10)),
                solver_status=int(status),iterations=count[0],
                relative_residual=float(np.linalg.norm(operator@u-f)/np.linalg.norm(f)))


def stable_large(n,eta):
    # Exact critical-family identities avoid subtraction in gamma and lambda.
    logt=math.log1p(-2/(n+1));tn=math.exp(n*logt)
    gamma=1-2/(n*n+1);lam=2/(n*n+1)
    omt2=4*n/(n+1)**2;t2=1-omt2
    v=n*(-math.expm1(n*logt))/(1+tn)
    mobility=1-eta*t2+eta*math.exp((n-2)*logt)*(-math.expm1(4*logt))/(-math.expm1(n*logt))
    kappa=lam*mobility
    q=omt2**2/(-math.expm1(2*n*logt))*(-math.expm1((2*n-4)*logt)+2*math.exp((n-3)*logt)*omt2)
    delta=eta**2/(1-abs(eta))*(q/v)*((n-2)/n)/(gamma*kappa)
    lower=n*v/kappa
    return dict(n=n,eta=eta,lower=lower,upper=lower*(1+delta),relative_width=delta,
                width_times_n=delta*n,kappa=kappa,magnetization_variance=n*v,
                nonlinear_residual_variance=n*q)


def odd_excursion_identities():
    def h(gaps):
        k=len(gaps)
        return F(sum(gaps[i]*gaps[j]*gaps[l]
                     for i,j,l in combinations(range(k),3)
                     if (j-i)%2 and (l-j)%2 and (k-l+i)%2),sum(gaps))
    records=[]
    for k in [3,5,7,9,11,13]:
        gaps=list(range(2,k+2));base=h(gaps);drift=F(0)
        for i in range(k):
            for direction in [-1,1]:
                y=gaps.copy();y[i]+=direction;y[(i+1)%k]-=direction
                drift+=(base-h(y))/2
        boundary=True
        for i in range(k):
            # Rotate the vanishing collision gap to zero for an explicit merge.
            y=gaps[i:]+gaps[:i];y[0]=0
            reduced=[y[-1]+y[1]]+y[2:-1]
            boundary &= h(y)==h(reduced)
        records.append(dict(defects=k,exact_drift=str(drift),expected_drift=str(F(k-1,2)),
                            drift_pass=drift==F(k-1,2),all_collision_merges_exact=boundary))
    return records


def run():
    start=time.perf_counter()
    exact=[exact_identities(n) for n in [3,4,5,7,9]]
    physical=[physical_response(n,eta) for n in [3,7,11,15] for eta in [-.4,.3,.6]]
    large=[stable_large(n,.6) for n in [31,127,511,2047,8191,32767,1000000]]
    excursion=odd_excursion_identities()
    out=dict(all_pass=all(x['all_exact'] for x in exact) and all(x['enclosure_pass'] and x['solver_status']==0 for x in physical)
                     and all(x['drift_pass'] and x['all_collision_merges_exact'] for x in excursion),
             exact_physical_gibbs_checks=exact,full_physical_response_checks=physical,
             general_odd_defect_excursion_checks=excursion,
             closed_formula_large_instances=large,seconds=time.perf_counter()-start,
             numerical_scope='The identities are exact Fraction comparisons against all physical Gibbs states. Full response comparisons and large-n endpoints are floating evaluations, not directed interval arithmetic.')
    Path(__file__).with_name('critical_ring_audit_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':run()
