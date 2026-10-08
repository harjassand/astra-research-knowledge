"""Enumerate vertices of the finite stationary-law LP for birth-death feedback."""
from itertools import combinations
from math import factorial


def solve(A, b, tol=1e-10):
    n=len(b)
    aug=[list(map(float,A[i]))+[float(b[i])] for i in range(n)]
    for c in range(n):
        r=max(range(c,n),key=lambda i:abs(aug[i][c]))
        if abs(aug[r][c])<tol:return None
        aug[c],aug[r]=aug[r],aug[c]
        z=aug[c][c]
        aug[c]=[x/z for x in aug[c]]
        for i in range(n):
            if i==c:continue
            z=aug[i][c]
            if z:
                aug[i]=[aug[i][j]-z*aug[c][j] for j in range(n+1)]
    return [aug[i][-1] for i in range(n)]


def lp_vertices(M,q,m,h):
    d=M+1
    eq=[[1.0]*d,[float(i) for i in range(d)]]
    rhs=[1.0,m]
    ineq=[] # each row means row dot pi >= rhs
    for n in range(d):
        row=[0.0]*d; row[n]=1.0
        ineq.append((row,0.0,('nonneg',n)))
    for n in range(M):
        row=[0.0]*d; row[n]=q; row[n+1]=-(n+1)
        ineq.append((row,0.0,('cap',n)))
    best=None; best_pi=None; feasible=0
    for idxs in combinations(range(len(ineq)),M-1):
        A=eq+[ineq[i][0] for i in idxs]
        b=rhs+[ineq[i][1] for i in idxs]
        pi=solve(A,b)
        if pi is None:continue
        if min(pi)<-1e-8:continue
        if abs(sum(pi)-1)>1e-7 or abs(sum(i*pi[i] for i in range(d))-m)>1e-7:continue
        if any(sum(a*x for a,x in zip(row,pi)) < val-1e-8 for row,val,_ in ineq):continue
        feasible+=1
        obj=sum(pi[:h])
        if best is None or obj<best:
            best,best_pi=obj,pi
    return best,best_pi,feasible


def threshold(M,q,m,h):
    def dist(k,alpha):
        if k==0: return [1.0]+[0.0]*M
        w=[q**n/factorial(n) for n in range(k)]
        if k<M: w.append(alpha*q**k/factorial(k))
        z=sum(w)
        pi=w+[0.0]*(M+1-len(w))
        return [x/z for x in pi]
    if m==0:return sum(dist(0,0)[:h]),dist(0,0),0,0
    for k in range(M+1):
        lo=dist(k,0.0); hi=dist(k,1.0) if k<M else lo
        ml=sum(i*lo[i] for i in range(M+1)); mh=sum(i*hi[i] for i in range(M+1))
        if ml-1e-9<=m<=mh+1e-9:
            if k==M or abs(m-ml)<1e-10:
                pi=lo; alpha=0.0
            else:
                a,b=0.0,1.0
                for _ in range(80):
                    mid=(a+b)/2
                    pi0=dist(k,mid); mm=sum(i*pi0[i] for i in range(M+1))
                    if mm<m:a=mid
                    else:b=mid
                alpha=(a+b)/2; pi=dist(k,alpha)
            return sum(pi[:h]),pi,k,alpha
    return None


def main():
    for M in [4,5,6]:
      for q in [1.5,2.5,4.0,7.0]:
        # attainable mean maximum under full cap at M
        maxm=q*sum(q**n/factorial(n) for n in range(M))/sum(q**n/factorial(n) for n in range(M+1))
        for frac in [0.25,0.5,0.75]:
          m=frac*maxm
          for h in range(1,M+1):
            o,pi,nv=lp_vertices(M,q,m,h)
            th=threshold(M,q,m,h)
            if th and o is not None and o < th[0]-1e-7:
              rates=[]
              for n in range(M):rates.append((n+1)*pi[n+1]/pi[n] if pi[n]>1e-12 else None)
              print('COUNTEREXAMPLE',dict(M=M,q=q,m=m,h=h,lp=o,threshold=th[0],support_policy=pi,rates=rates,threshold_k=th[2],alpha=th[3],vertices=nv))
              return
    print('No counterexample on this grid.')

if __name__=='__main__':main()
