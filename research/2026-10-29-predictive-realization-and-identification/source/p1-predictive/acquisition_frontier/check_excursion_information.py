#!/usr/bin/env python3
"""Exact Schur/clock controls and conventional forest relative-error controls."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def inverse(a):
    n=len(a)
    x=[list(map(F,row))+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        p=next(i for i in range(j,n) if x[i][j])
        x[j],x[p]=x[p],x[j]
        pivot=x[j][j]
        x[j]=[v/pivot for v in x[j]]
        for i in range(n):
            if i!=j:
                c=x[i][j]
                x[i]=[u-c*v for u,v in zip(x[i],x[j])]
    return [r[n:] for r in x]

def sub(a,inds): return [[a[i][j] for j in inds] for i in inds]
def matvec(a,b): return [sum((x*y for x,y in zip(r,b)),F(0)) for r in a]
def quad(a,b): return sum((x*y for x,y in zip(b,matvec(a,b))),F(0))

def counter_controls():
    out=[]
    for e in [F(1,16),F(1,64),F(1,1024),F(1,2**16),F(1,2**32),F(1,2**64)]:
        lap=[[1+e,F(-1),-e],[F(-1),F(1),F(0)],[-e,F(0),e]]
        L=[[v/3 for v in r] for r in lap]
        S=[[L[i][j]-L[i][2]*L[2][j]/L[2][2] for j in [0,1]] for i in [0,1]]
        b=[F(1,3)-L[i][2]/L[2][2]/3 for i in [0,1]]
        c=F(1,9)/L[2][2]
        assert S==[[F(1,3),F(-1,3)],[F(-1,3),F(1,3)]]
        assert b==[F(2,3),F(1,3)] and c==F(1,3)/e
        h=matvec(inverse(sub(lap,[0,2])),[F(1),F(1)])
        assert h==[F(2),F(2)+1/e]
        T=sum(h)/2
        assert T==2+F(1,2)/e
        P=[[e/(1+e),1/(1+e)],[F(1),F(0)]]
        s=[(1+e)/(2+e),1/(2+e)]
        d=[1/(1+e),F(1)]
        mu=[1/(1+e),F(0)]
        mu2=[2/(e*(1+e)),F(0)]
        w=[s[i]*d[i] for i in range(2)]
        bb=[s[i]*(d[i]+mu[i]) for i in range(2)]
        cc=sum(s[i]*mu2[i] for i in range(2))/2
        Z=(2+e)/3
        assert bb==[v/Z for v in b] and cc==c/Z
        edge=s[0]*P[0][1]
        D=w[0]+sum(s[i]*mu[i] for i in range(2))
        assert (cc+bb[0]**2/edge)/D==T
        assert sum(bb)==1/Z
        T2=2+F(1,4)/e
        assert T/T2>=F(5,3)
        out.append({"epsilon":str(e),"mean":str(T),"c":str(c),"boundary_start_mean":str(h[0]),"mean_ratio_to_double_epsilon":str(T/T2),"all_exact_checks":True})
    return out

def forest_degree_controls():
    """Verify every killed inverse entry, not merely one selected mean."""
    k=F(11,10); rows=[]; checked=0
    for fixture in range(4):
        weights=[F(1),F(2),F(3),F(5)]
        q=[[F(0) for _ in weights] for _ in weights]
        for i in range(4):
            for j in range(i+1,4):
                cond=F(1+((i+3*j+fixture)%7),2+fixture)
                q[i][j]=cond/weights[i]; q[j][i]=cond/weights[j]
        qhat=[[F(0) for _ in weights] for _ in weights]
        for i in range(4):
            for j in range(4):
                if i!=j:qhat[i][j]=q[i][j]*(k if (i+2*j+fixture)%3 else 1/k)
        for a in [q,qhat]:
            for i in range(4):a[i][i]=-sum(a[i])
        worst=F(1)
        for r in range(1,4):
            for target in combinations(range(4),r):
                transient=[i for i in range(4) if i not in target]
                n=len(transient); fac=k**(2*n-1)
                true=inverse([[-q[i][j] for j in transient] for i in transient])
                prop=inverse([[-qhat[i][j] for j in transient] for i in transient])
                for a in range(n):
                    for b in range(n):
                        assert true[a][b]/fac<=prop[a][b]<=true[a][b]*fac
                        if true[a][b]:worst=max(worst,prop[a][b]/true[a][b],true[a][b]/prop[a][b])
                        checked+=1
        rows.append({"fixture":fixture,"worst_observed_entry_factor":str(worst),"general_bound":str(k**5)})
    return {"fixtures":rows,"exact_killed_entries_checked":checked,"all_passed":True}

def main():
    result={"three_state_countermodel":counter_controls(),"forest_relative_rate_controls":forest_degree_controls(),"method":"exact rational arithmetic; zero source observations; mathematical supplied-source controls"}
    path=HERE/'EXCURSION_INFORMATION_EXACT_CHECKS.json'
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({"status":"PASS","countermodels":len(result['three_state_countermodel']),"entries":result['forest_relative_rate_controls']['exact_killed_entries_checked'],"output":str(path)}))

if __name__=='__main__':main()
