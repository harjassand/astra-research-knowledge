"""Exact all-odd-state audit of hopping, branching, and event-cost potentials."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from functools import lru_cache
import json


def potential(s,n):
    x=sorted(s);k=len(x)
    if k==1:return F(0)
    gaps=[(x[(i+1)%k]-x[i])%n for i in range(k)]
    return F(sum(gaps[i]*gaps[j]*gaps[l] for i,j,l in combinations(range(k),3)
                 if (j-i)%2 and (l-j)%2 and (k-l+i)%2),n)


def charge_potential(s,n):
    x=sorted(s)
    return sum(((-1)**(i+j))*(F((x[j]-x[i])**2,2)-F((x[j]-x[i])**3,3*n))
               for i,j in combinations(range(len(x)),2))


def higher_potentials(s,n):
    x=sorted(s);k=len(x)
    gaps=[(x[(i+1)%k]-x[i])%n for i in range(k)] if k>1 else [n]
    quintic=F(sum(__import__('math').prod(gaps[i] for i in ids)
                  for ids in combinations(range(k),5)
                  if all((ids[(j+1)%5]-ids[j])%k%2 for j in range(5))),n)
    def V(d):
        return F(d**5,60*n)-F(d**4,24)+F((n*n-1)*d**3,36*n)+F(d*d,24)
    U=sum((-1)**(i+j)*V(x[j]-x[i]) for i,j in combinations(range(k),2))
    return U,quintic,gaps


def quintic_cost_audit(n):
    b=F(1,3);gamma=F(n*n-1,n*n+1);d=gamma*(1-b)
    epsilon=(d-b)/3+2*b/n;u0=F((n-2)*(n-1),6*n);h0=F(n-2,n)
    checks=dict(U_nonnegative=True,Q_nonnegative=True,U_hop=True,Q_hop=True,
                U_branch=True,Q_branch_exact=True,Q_branch_upper=True,
                cost_superpotential=True,h_min=True,hop_ratio=True,branch_ratio=True)
    @lru_cache(None)
    def data(s):
        h=potential(s,n);u,q,g=higher_potentials(s,n)
        w=(3*u+2*q)/d+3*b*u0*h/(d*epsilon)
        return h,u,q,g,w
    for mask in range(1,1<<n):
        if mask.bit_count()%2==0:continue
        s=frozenset(i for i in range(n) if mask>>i&1);k=len(s)
        h,u,q,g,w=data(s)
        checks['U_nonnegative'] &= u>=0
        checks['Q_nonnegative'] &= q>=0
        dh=du=dq=dw=F(0);bu=bq=bw=F(0)
        for i in s:
            for direction in [-1,1]:
                nxt=s.symmetric_difference({i,(i+direction)%n})
                hn,un,qn,_,wn=data(nxt)
                du+=(u-un)/2;dq+=(q-qn)/2;dw+=(w-wn)/2
                if k>=3:checks['hop_ratio'] &= hn<=2*h
            nxt=s.symmetric_difference({(i-1)%n,(i+1)%n})
            hn,un,qn,_,wn=data(nxt)
            bu+=un-u;bq+=qn-q;bw+=wn-w
            if k>=3:checks['branch_ratio'] &= hn<=4*h
        quadratic=sum((F(j-i,2) if (j-i)%2==0 else F(k-j+i,2))*g[i]*g[j]
                      for i,j in combinations(range(k),2))
        predicted_bq=3*h-F(2,n)*quadratic+F(k-1,2)
        checks['U_hop'] &= du==h
        checks['Q_hop'] &= dq==F(k-3,2)*h
        checks['U_branch'] &= bu==k*u0-2*h
        checks['Q_branch_exact'] &= bq==predicted_bq
        checks['Q_branch_upper'] &= bq<=3*h
        if k>=3:
            checks['h_min'] &= h>=h0
            checks['cost_superpotential'] &= d*dw-b*bw>=k*h
    packed=frozenset([0,1,2]);w0=data(packed)[-1]
    return dict(n=n,all_exact=all(checks.values()),checks=checks,
                bounded_D_score_max=float(h0/epsilon),
                transformed_elementary_attempt_bound=float(w0/h0),
                predicted_bound=float(3*u0/d*(1+b*h0/epsilon)/h0))


def check(n):
    checks=dict(charge_equals_gaps=True,nonnegative=True,hop_drift=True,branch_drift=True,
                target_drift=True,event_superpotential=True)
    b=F(1,3);gamma=F(n*n-1,n*n+1);d=gamma*(1-b)
    aa=d/2+2*b/n;cc=d/2+b;epsilon=aa-cc/3
    count=0
    for mask in range(1,1<<n):
        if mask.bit_count()%2==0:continue
        s={i for i in range(n) if mask>>i&1};k=len(s);h=potential(s,n)
        checks['charge_equals_gaps'] &= h==charge_potential(s,n)
        checks['nonnegative'] &= h>=0
        hop=sum((h-potential(s.symmetric_difference({i,(i+direction)%n}),n))/2
                 for i in s for direction in [-1,1])
        branch=sum(potential(s.symmetric_difference({(i-1)%n,(i+1)%n}),n)-h for i in s)
        checks['hop_drift'] &= hop==F(k-1,2)
        checks['branch_drift'] &= branch==1-F(2*k,n)
        checks['target_drift'] &= d*hop-b*branch==aa*k-cc
        if k>=3:
            checks['event_superpotential'] &= d*hop-b*branch>=epsilon*k
        count+=1
    h3=F(n-2,n)
    return dict(n=n,odd_states=count,all_exact=all(checks.values()),checks=checks,
                event_expectation_bound=float((d+b)*h3/epsilon))


def check_three_cost(n):
    def h(a,b,c):return F(a*b*c,n)
    def u(a,b,c):return F(a*b*c*(a*b+b*c+c*a+1),12*n)
    checks=[]
    for a in range(1,n-1):
        for b in range(1,n-a):
            c=n-a-b;g=[a,b,c];value=u(*g);drift=F(0)
            for i,j in [(0,1),(1,0),(0,2),(2,0),(1,2),(2,1)]:
                y=g.copy();y[i]+=1;y[j]-=1
                drift+=(value-u(*y))/2
            checks.append(drift==h(*g))
    return dict(n=n,all_exact=all(checks),source_potential=float(u(1,1,n-2)),
                expected_h_transformed_time_at_gamma_one=float(u(1,1,n-2)/h(1,1,n-2)))


if __name__=='__main__':
    records=[check(n) for n in [3,4,5,7,9,11]]
    cost=[check_three_cost(n) for n in [5,9,17,33]]
    quintic=[quintic_cost_audit(n) for n in [4,5,7,9,11]]
    out=dict(all_pass=all(x['all_exact'] for x in records+cost+quintic),all_odd_state_checks=records,
             three_walker_cost_checks=cost,
             all_order_quintic_cost_checks=quintic,
             status='Exact Fraction evaluation over every odd subset; no sampling.')
    Path(__file__).with_name('positive_dual_potential_audit_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
