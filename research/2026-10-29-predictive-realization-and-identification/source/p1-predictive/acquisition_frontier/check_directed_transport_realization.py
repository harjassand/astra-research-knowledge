#!/usr/bin/env python3
"""Rational KKT, state-cost and full directed-realization controls; no sampling."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def solve(a,b):
    n=len(b);a=[list(map(F,row))+[F(z)] for row,z in zip(a,b)]
    for j in range(n):
        p=next(i for i in range(j,n) if a[i][j]);a[j],a[p]=a[p],a[j]
        z=a[j][j];a[j]=[x/z for x in a[j]]
        for i in range(n):
            if i!=j:
                z=a[i][j]
                if z:a[i]=[x-z*y for x,y in zip(a[i],a[j])]
    return [row[-1] for row in a]

def ceil(x):return -(-x.numerator//x.denominator)

def certify(name,flow,r,l,M,alpha,beta):
    m=len(r)
    assert all(sum(flow[i][j] for j in range(m))==sum(flow[j][i] for j in range(m)) for i in range(m))
    assert [sum(row) for row in M]==r
    assert [sum(M[i][j] for i in range(m)) for j in range(m)]==l
    objective=F(0);slacks=[]
    for i in range(m):
        for j in range(m):
            assert M[i][j]>=0
            if i!=j and flow[i][j]==0:
                assert M[i][j]==0;continue
            gradient=F(0) if i==j else 2*M[i][j]/flow[i][j]
            slack=gradient-alpha[i]-beta[j]
            assert slack>=0 and M[i][j]*slack==0
            slacks.append(slack)
            if i!=j:objective+=M[i][j]**2/flow[i][j]
    return {'name':name,'ports':m,'J_star':str(objective),'positive_M_channels':sum(x>0 for row in M for x in row),'kkt_allowed_positions':len(slacks),'strictly_positive_kkt_slacks':sum(x>0 for x in slacks)},objective

def full_nine_state_realization():
    weights=[F(1),F(2)];edges=[]
    def path(i,j,flow,holds):
        previous=i
        for hold in holds:
            new=len(weights);weights.append(flow*hold);edges.append((previous,new,flow));previous=new
        edges.append((previous,j,flow))
    # Optimizer diag(1,1), offdiag M01=1. Diagonal flow8, mean1/8.
    path(0,0,F(8),[F(1,16),F(1,16)])
    path(1,1,F(8),[F(1,16),F(1,16)])
    # Mean1 channel01, second moment13/8 by a rational mixture.
    path(0,1,F(3,4),[F(1,2),F(1,2)])
    path(0,1,F(1,4),[F(1)])
    edges.append((1,0,F(1)))
    n=len(weights);assert n==9
    L=[[F(0) for _ in range(n)] for _ in range(n)]
    for i,j,f in edges:L[i][i]+=f;L[i][j]-=f
    assert all(sum(row)==0 for row in L)
    assert all(sum(L[i][j] for i in range(n))==0 for j in range(n))
    Q=[[-L[i][j]/weights[i] for j in range(n)] for i in range(n)]
    assert all(Q[i][j]>=0 for i in range(n) for j in range(n) if i!=j)
    assert any(weights[i]*Q[i][j]!=weights[j]*Q[j][i] for i in range(n) for j in range(n))
    I=list(range(2,n));C=[[L[i][j] for j in I] for i in I]
    wi=[weights[i] for i in I];h=solve(C,wi)
    ht=solve([list(row) for row in zip(*C)],wi)
    bR=[weights[i]-sum(L[i][I[k]]*h[k] for k in range(len(I))) for i in range(2)]
    bL=[weights[i]-sum(L[I[k]][i]*ht[k] for k in range(len(I))) for i in range(2)]
    c=sum(x*y for x,y in zip(wi,h));S=[[F(0)]*2 for _ in range(2)]
    M=[[F(0)]*2 for _ in range(2)]
    for j in range(2):
        x=solve(C,[L[i][j] for i in I])
        y=solve(C,[wi[k]*x[k] for k in range(len(I))])
        for i in range(2):
            S[i][j]=L[i][j]-sum(L[i][I[k]]*x[k] for k in range(len(I)))
            M[i][j]=sum(L[i][I[k]]*y[k] for k in range(len(I)))
    assert S==[[F(1),F(-1)],[F(-1),F(1)]]
    assert bR==[F(3),F(3)] and bL==[F(2),F(4)] and c==1
    assert M==[[F(1),F(1)],[F(0),F(1)]] and sum(wi)==3
    means=[]
    for target in [(0,),(1,),(0,1)]:
        live=[i for i in range(n) if i not in target]
        hv=solve([[L[i][j] for j in live] for i in live],[weights[i] for i in live])
        actual=sum(weights[i]*hv[k] for k,i in enumerate(live))/sum(weights[i] for i in live)
        R=[i for i in range(2) if i not in target]
        term=F(0)
        if R:
            z=solve([[S[i][j] for j in R] for i in R],[bR[i] for i in R])
            term=sum(bL[i]*z[k] for k,i in enumerate(R))
        compressed=(c+term)/(sum(weights)-sum(weights[i] for i in target))
        assert actual==compressed
        means.append({'target_ports':list(target),'mean':str(actual)})
    return {'states':n,'hidden_states':n-2,'b_R':list(map(str,bR)),'b_L':list(map(str,bL)),'c':str(c),'record_and_three_means_exact':True,'nonreversible':True,'means':means}

def main():
    F2=[[F(0),F(1)],[F(1),F(0)]]
    M2=[[F(1),F(1)],[F(0),F(1)]]
    c2,J2=certify('two_port_unbalanced',F2,[F(2),F(1)],[F(1),F(2)],M2,[F(2),F(0)],[F(-2),F(0)])
    F3=[[F(0),F(1),F(1,10)],[F(1),F(0),F(1)],[F(1,10),F(1),F(0)]]
    M3=[[F(1),F(5,6),F(1,6)],[F(0),F(1,6),F(5,6)],[F(0),F(0),F(1)]]
    c3,J3=certify('three_port_split_optimum',F3,[F(2),F(1),F(1)],[F(1),F(1),F(2)],M3,[F(10,3),F(5,3),F(0)],[F(-10,3),F(-5,3),F(0)])
    cycle=[[F(0),F(1),F(0)],[F(0),F(0),F(1)],[F(1),F(0),F(0)]]
    Mb=[[F(1),F(0),F(0)],[F(0),F(2),F(0)],[F(0),F(0),F(0)]]
    cb,Jb=certify('balanced_nonreciprocal_core',cycle,[F(1),F(2),F(0)],[F(1),F(2),F(0)],Mb,[F(0)]*3,[F(0)]*3)
    assert (J2,J3,Jb)==(F(1),F(5,3),F(0))
    # Hall cut on the directed-cycle support proves empty transportation set.
    r=[F(1),F(0),F(0)];l=[F(0),F(0),F(1)];witnesses=[]
    for count in range(1,4):
        for rows in combinations(range(3),count):
            neighbors={j for i in rows for j in range(3) if i==j or cycle[i][j]>0}
            if sum(r[i] for i in rows)>sum(l[j] for j in neighbors):
                witnesses.append({'rows':list(rows),'neighbor_columns':sorted(neighbors),'supply':str(sum(r[i] for i in rows)),'capacity':str(sum(l[j] for j in neighbors))})
    assert witnesses
    exact=[];approx=[]
    for label,J,M in [('two',J2,M2),('split_three',J3,M3),('balanced',Jb,Mb)]:
        c=F(1);delta=(2*c-J)/2;D=J+delta;k=ceil(D/(2*c-D));c0=(1+F(1,k))*D/2
        assert 0<D<2*c and c0<=c
        exact.append({'fixture':label,'J':str(J),'c':str(c),'delta':str(delta),'k':k,'c0':str(c0)})
        for exponent in [1,4,16,64]:
            c=J/2+F(1,2**exponent)
            for eta in [F(1),F(1,4),F(1,16)]:
                delta=eta*c/2;D=J+delta;k=ceil(4/eta);c0=(1+F(1,k))*D/2;cp=max(c,c0)
                assert c<=cp<=(1+eta)*c
                assert c0<c*(1+eta/4)**2
                m=len(M);bound=m+k*m*m+1
                approx.append({'fixture':label,'slack_exponent':exponent,'eta':str(eta),'k':k,'state_bound':bound,'c_ratio':str(cp/c),'exact_state_lower':str(J/(2*c-J))})
    # Hyperexponential calibration, rational even at high second moments.
    hyper=0
    for mu in [F(1,7),F(3,2),F(5)]:
        for factor in [F(2),F(5,2),F(7),F(100)]:
            q=factor*mu*mu;a=mu/2;d=q/mu-mu;p=(d-mu)/(d-a)
            assert 0<=p<1 and a>0 and d>0
            assert p*a+(1-p)*d==mu and 2*(p*a*a+(1-p)*d*d)==q;hyper+=1
    sharp=[]
    for k in [1,2,4,16,64]:
        J=F(50,27);c=(1+F(1,k))*J/2
        assert J/(2*c-J)==k
        sharp.append({'hidden_states':k,'J':str(J),'c':str(c),'lower_bound_attained':True})
    out={'status':'PASS','scope':'Exact supplied-record controls; zero source observations and no claim of a native acquisition experiment.','kkt_certificates':[c2,c3,cb],'empty_transport_hall_witnesses':witnesses,'exact_calibrations':exact,'approximate_calibrations':approx,'hyperexponential_moment_checks':hyper,'sharp_state_lower_controls':sharp,'full_directed_realization':full_nine_state_realization()}
    (HERE/'DIRECTED_TRANSPORT_REALIZATION_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','kkt_optima':3,'empty_transport_witnesses':len(witnesses),'approximation_controls':len(approx),'hyperexponential_checks':hyper,'full_realization_states':out['full_directed_realization']['states']}))

if __name__=='__main__':main()
