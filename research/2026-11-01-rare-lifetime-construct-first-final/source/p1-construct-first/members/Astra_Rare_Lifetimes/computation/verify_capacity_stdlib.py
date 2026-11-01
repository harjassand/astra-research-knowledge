"""Exact rational finite checks; standard library only."""
from fractions import Fraction as F
from pathlib import Path
import json

def solve(a,b):
    n=len(b);z=[[F(x) for x in row]+[F(v)] for row,v in zip(a,b)]
    for k in range(n):
        p=next(i for i in range(k,n) if z[i][k]);z[k],z[p]=z[p],z[k]
        d=z[k][k];z[k]=[x/d for x in z[k]]
        for i in range(n):
            if i!=k:
                d=z[i][k];z[i]=[x-d*y for x,y in zip(z[i],z[k])]
    return [row[-1] for row in z]

def dot(x,y):return sum(a*b for a,b in zip(x,y))
def mv(a,x):return [dot(row,x) for row in a]
def wd(x,y,p):return sum(a*b*c for a,b,c in zip(x,y,p))

def generator(w,flow):
    n=len(w);q=[[F(0) for _ in w] for _ in w]
    for i in range(n):
        for j in range(n):
            if i!=j:q[i][j]=flow[i][j]/w[i]
        q[i][i]=-sum(q[i])
    assert all(sum(w[i]*q[i][j] for i in range(n))==0 for j in range(n))
    return q

def hit(q,w,A):
    n=len(w);pi=[x/sum(w) for x in w];B=[i for i in range(n) if i not in A]
    hB=solve([[-q[i][j] for j in B] for i in B],[F(1)]*len(B));h=[F(0)]*n
    for i,v in zip(B,hB):h[i]=v
    return pi,B,h,dot(pi,h),sum(pi[i] for i in A)

def check(q,w,A,delta,gap,reversible):
    n=len(w);pi,B,h,mu,p=hit(q,w,A);b=1-p
    K=[[(delta if i==j else 0)-q[i][j] for j in B] for i in B]
    eB=solve(K,[sum(q[i][j] for j in A) for i in B]);e=[F(1)]*n
    for i,v in zip(B,eB):e[i]=v
    m=dot(pi,e);S=delta*m;Rs=1/S-1/delta;M=mu/b
    J=sum(pi[i]*q[i][j] for i in A for j in B);qq=(S-delta*p)/J
    qlo=delta*gap*p*b/(J*(gap*p+delta));factor=1+delta/gap
    assert qq>=qlo
    assert Rs/(b*factor)<=M<=factor*Rs/b
    if reversible:assert Rs/b<=M
    qs=[[pi[j]*q[j][i]/pi[i] for j in range(n)] for i in range(n)]
    _,_,ha,mua,_=hit(qs,w,A);assert mu==mua
    h0=[1-x/mu for x in h];ha=[1-x/mu for x in ha];hs=[(x-m)/(1-m) for x in e]
    C0,Cs=1/mu,1/Rs
    assert Cs-C0==delta*wd(ha,hs,pi)
    assert wd(h0,[-x for x in mv(q,h0)],pi)==C0
    assert wd(ha,[-x for x in mv(qs,ha)],pi)==C0
    assert wd(hs,[delta*x-y for x,y in zip(hs,mv(q,hs))],pi)==Cs
    return dict(p=str(p),mean=str(M),Rs_over_b=str(Rs/b),screened_relative=str(Rs/mu),
                q=str(qq),q_lower=str(qlo),factor=str(factor),one_sided_valid=Rs<=mu,
                primal_adjoint_identity_exact=True)

def randcheck(n,seed,nonrev):
    w=[F(1+(7*i+seed)%9,1+(i+seed)%3) for i in range(n)]
    f=[[F(0) for _ in w] for _ in w]
    for i in range(n):
        for j in range(i):f[i][j]=f[j][i]=F(1+(5*i+11*j+seed)%7,5)
    # Domination of complete-refresh conductances certifies gap exactly.
    gap=min(f[i][j]*sum(w)/(w[i]*w[j]) for i in range(n) for j in range(i))
    if nonrev:
        for i in range(n):f[i][(i+1)%n]+=F(7,3)
    q=generator(w,f);A=[i for i in range(n) if (i+seed)%3==0] or [0]
    out=check(q,w,A,gap/13,gap,not nonrev)
    if not nonrev:
        fac=[F(15+(3*i+seed)%11,20) for i in range(n)];wh=[x*y for x,y in zip(w,fac)]
        fh=[[F(0) for _ in w] for _ in w];fs=[]
        for i in range(n):
            for j in range(i):
                t=F(15+(13*i+j+seed)%11,20);fs.append(t);fh[i][j]=fh[j][i]=f[i][j]*t
        _,_,_,muh,ph=hit(generator(wh,fh),wh,A);_,_,_,mu,p=hit(q,w,A)
        ratio=(muh/(1-ph))/(mu/(1-p));a,b,cl,cu=min(fac),max(fac),min(fs),max(fs)
        lo,hi=a*a/(b*cu),b*b/(a*cl);assert lo<=ratio<=hi
        out.update(transfer_ratio=str(ratio),transfer_lower=str(lo),transfer_upper=str(hi))
    return out

def heatbath(eps):
    states=[(0,0),(0,1),(1,0),(1,1)];w=[1-3*eps,eps,eps,eps]
    q=[[F(0) for _ in w] for _ in w]
    for i,x in enumerate(states):
        for site in range(2):
            y=list(x);y[site]=1-y[site];j=states.index(tuple(y));q[i][j]=w[j]/(w[i]+w[j])
        q[i][i]=-sum(q[i])
    out=check(q,w,[2,3],F(1,100),F(1,2),True);ss=eps/(1-2*eps)
    bad=(F(5,4)-ss+ss*ss)/(ss*(F(3,2)-ss));out['naive_indicator_ratio']=str(bad/F(out['mean']))
    return out

def main():
    n=7;w=[F(1)]*n;f=[[F(int(j==(i+1)%n)) for j in range(n)] for i in range(n)]
    directed=check(generator(w,f),w,[0],F(1,100),F(1,n*n),False)
    assert not directed['one_sided_valid']
    a,b,d=F(2,11),F(3,7),F(1,100)
    sharp=check([[-a,a],[b,-b]],[b,a],[1],d,a+b,True)
    assert F(sharp['q'])==F(sharp['q_lower'])
    assert F(sharp['screened_relative'])*F(sharp['factor'])==1
    out=dict(reversible=[randcheck(n,j,False) for n in range(3,8) for j in range(4)],
             nonreversible=[randcheck(n,j,True) for n in range(3,8) for j in range(4)],
             two_spin=[heatbath(F(1,2**k)) for k in [3,6,12,32,64,128]],
             sharp_two_state=sharp,directed_cycle_one_sided_failure=directed)
    path=Path(__file__).with_name('capacity_checks.json');path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(checks=48,all_passed=True,output=str(path),
        naive_ratio_2m128=float(F(out['two_spin'][-1]['naive_indicator_ratio'])),
        directed_Rs_over_mu=float(F(directed['screened_relative']))),indent=2))

if __name__=='__main__':main()
