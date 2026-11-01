#!/usr/bin/env python3
"""Independent finite-fiber controls; no floating point or candidate imports.
These exact finite tests supplement MECHANISM_REVIEW_PENDING.md, not its proof.
"""
from fractions import Fraction as F
from math import prod
import json

def compositions(m,n):
    if n==1:
        yield (m,)
    else:
        for k in range(m+1):
            for z in compositions(m-k,n-1):
                yield (k,)+z

def ff(x,u):
    if any(a<b for a,b in zip(x,u)):return 0
    return prod(prod(range(a-b+1,a+1)) for a,b in zip(x,u))

def solve(A,B):
    n=len(A);m=len(B[0]);a=[list(map(F,row))+list(map(F,b)) for row,b in zip(A,B)]
    for j in range(n):
        k=next(k for k in range(j,n) if a[k][j])
        a[j],a[k]=a[k],a[j];q=a[j][j];a[j]=[z/q for z in a[j]]
        for k in range(n):
            if k==j or not a[k][j]:continue
            q=a[k][j];a[k]=[z-q*y for z,y in zip(a[k],a[j])]
    return [row[n:n+m] for row in a]

def top_support(raw):
    n=len(raw[0][0]);p=max(sum(u)for u,v,k in raw);traces=[]
    for i in range(n):
        support={i};steps=[]
        while 0 not in support:
            found=False
            for index,(u,v,k) in enumerate(raw):
                if sum(u)!=p or any(u[j] and j not in support for j in range(n)):continue
                new={j for j in range(n)if v[j]}-support
                if new:
                    steps.append([index,sorted(new)]);support|=new;found=True;break
            if not found:break
        traces.append({'initial':i,'steps':steps,'terminal':sorted(support),'reaches_seed':0 in support})
    return traces

def run(label,raw,maxmass):
    n=len(raw[0][0]);p=max(sum(u)for u,v,k in raw);C=max(F(1),p**3*sum(k for u,v,k in raw));T=1/(4*C)
    traces=top_support(raw);assert all(z['reaches_seed']for z in traces)
    kmin=min(k for u,v,k in raw if sum(u)==p);ell=F(3,4*n)
    for _ in range(n):ell=min(ell,T*kmin*ell**p/(4*n))
    delta=ell;K0=64*n*C*T/delta**2;K=K0+2/delta
    lam=F(2,3);mu=F(7,5);rows=[];normalization=0;drifts=0;brackets=0;linear_rows=0
    for M in range(maxmass+1):
        states=list(compositions(M,n));index={x:i for i,x in enumerate(states)};q=[[F(0)]*len(states)for x in states]
        for i,x in enumerate(states):
            full=(x[0]+1,)+x[1:]
            for u,v,k in raw:
                us=(u[0]+1,)+u[1:]
                assert k*ff(full,us)==full[0]*k*ff(x,u);normalization+=1
                rate=k*ff(x,u)
                if rate:
                    target=tuple(a-b+c for a,b,c in zip(x,u,v));j=index[target]
                    q[i][j]+=rate;q[i][i]-=rate
            if M>=p:
                z=tuple(F(a,M)for a in x)
                for j in range(n):
                    b=sum(k*ff(x,u)*(v[j]-u[j])/M**p for u,v,k in raw)
                    vv=sum(k*prod(a**b for a,b in zip(z,u))*(v[j]-u[j])for u,v,k in raw if sum(u)==p)
                    assert abs(b-vv)<=C/M;drifts+=1
                    bracket=sum(k*ff(x,u)*(v[j]-u[j])**2/F(M**(p+1))for u,v,k in raw)
                    assert bracket<=C/M;brackets+=1
        killing=[mu+lam/(1+x[0])for x in states]
        mat=[[-q[i][j]+(killing[i]if i==j else 0) for j in range(len(states))]for i in range(len(states))]
        rhs=[[lam/(1+x[0]),mu*int(x[0]==0),mu*int(x[0]>0),F(1,1+x[0])]for x in states]
        ans=solve(mat,rhs)
        for i,x in enumerate(states):
            up,loss,down,hseed=ans[i];assert 0<=up<=1 and 0<=loss<=1 and 0<=down<=1 and up+loss+down==1
            holding=hseed+loss/lam;assert F(1)/(lam+mu*(M+1))<=holding<=1/mu+1/lam
            for j in range(4):
                assert sum(mat[i][k]*ans[k][j]for k in range(len(states)))==rhs[i][j]
                # Undo time change: A*Q and physical kill mu*A+lambda.
                assert (1+x[0])*sum(mat[i][k]*ans[k][j]for k in range(len(states)))==(1+x[0])*rhs[i][j]
                linear_rows+=1
            for t in [F(65,64),F(2),F(100)]:
                actual=t*up+loss+down/t
                assert actual==1/t+(t-1/t)*up+(1-1/t)*loss
                assert actual<=1/t+(t-1/t)*(up+loss)
            if M>=p and M>=8*C*T/delta:
                assert up<=lam*(T+K/mu)/M and loss<=(mu*T+K)/M
        extremes=[]
        for j in range(n):
            x=tuple(M*int(i==j)for i in range(n));up,loss,down,hseed=ans[index[x]]
            extremes.append({'coordinate':j,'p_up':str(up),'p_loss':str(loss),'physical_cycle_mean':str(hseed+loss/lam)})
        if M:
            x=(M,)+(0,)*(n-1);up,loss,down,hseed=ans[index[x]]
            assert up==lam/(lam+mu*(M+1)) and loss==0
        rows.append({'M':M,'fiber_states':len(states),'pure_states':extremes})
    return {'label':label,'order':p,'support_traces':traces,'C':str(C),'T':str(T),'delta':str(delta),
            'finite_fiber_results':rows,'seed_normalization_identities':normalization,
            'scaled_drift_error_checks':drifts,'bracket_rate_checks':brackets,
            'exact_killed_equation_rows':linear_rows,
            'large_mass_asymptotic_bound_used_as_proof_not_numerical_evidence':True}

def main():
    BB=(0,2,0);BC=(0,1,1);CC=(0,0,2);rB=(1,1,0)
    raw=[(BB,BC,F(1)),(BC,BB,F(1)),(BC,CC,F(2)),(CC,BC,F(1)),(BC,rB,F(1)),(rB,BC,F(1))]
    cubic=[]
    for u,v,k in raw:
        for j in range(3):
            cubic.append((tuple(a+int(i==j)for i,a in enumerate(u)),tuple(a+int(i==j)for i,a in enumerate(v)),k))
    multiplier=0
    for M in range(3,13):
        for x in compositions(M,3):
            for u,v,k in raw:
                assert sum(ff(x,tuple(a+int(i==j)for i,a in enumerate(u)))for j in range(3))==(M-2)*ff(x,u);multiplier+=1
    bad=top_support(raw[:4]);assert not all(z['reaches_seed']for z in bad)
    print(json.dumps({'cases':[run('opposing_pure_ray_quadratic_Q',raw,8),run('catalyzed_cubic_Q',cubic,7)],
                      'catalytic_generator_multiplier_identities':multiplier,'missing_restoration_support_rejected':bad,
                      'scope':'Pending mechanism controls only; no frozen constructor or finite-test stability claim.'},indent=2))

if __name__=='__main__':main()
