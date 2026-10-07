#!/usr/bin/env python3
"""Exact rank-two tagged transfer-network check for a 4-site block example."""
from itertools import combinations
from collections import defaultdict
import json
from pathlib import Path


def det(A):
    n=len(A)
    if n==0: return 1
    from itertools import permutations
    total=0
    for p in permutations(range(n)):
        inv=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=-1 if inv%2 else 1
        for i,j in enumerate(p): term*=A[i][j]
        total+=term
    return total

def sub(A,I,J): return [[A[i][j] for j in J] for i in I]
def blockdiag(bs):
    n=sum(len(B) for B in bs); A=[[0]*n for _ in range(n)]; off=0
    for B in bs:
        for i in range(len(B)):
            for j in range(len(B)): A[off+i][off+j]=B[i][j]
        off+=len(B)
    return A

def tags(n,r):
    out=[]
    for p in range(r+1):
        for R in combinations(range(n),p):
            for C in combinations(range(n),p):
                for S in combinations(range(r),p): out.append((R,C,S))
    return out

def local_configs(B, off):
    b=len(B); out=[]
    for state in range(3**b):
        x=state; I=[]; J=[]
        for j in range(b):
            q=x%3; x//=3
            if q==1: I.append(off+j)
            elif q==2: J.append(off+j)
        out.append((tuple(I),tuple(J)))
    return out

def transfer_sum(blocks,X,Y,tag,tag2,k):
    R,C,S=tag; R2,C2,S2=tag2
    n=len(X); r=len(X[0]); G=blockdiag(blocks)
    coef=det([[X[i][s] for s in S] for i in R])*det([[Y[j][s] for s in S] for j in C])
    coef2=det([[X[i][s] for s in S2] for i in R2])*det([[Y[j][s] for s in S2] for j in C2])
    dp={(0,0,0,0):1}; off=0
    for B in blocks:
        b=len(B); nxt=defaultdict(int); configs=local_configs(B,off)
        Rt=tuple(i for i in R if off<=i<off+b); Ct=tuple(j for j in C if off<=j<off+b)
        R2t=tuple(i for i in R2 if off<=i<off+b); C2t=tuple(j for j in C2 if off<=j<off+b)
        for (ri,cj,pr,pc),val in dp.items():
            for I,J in configs:
                il=set(I); jl=set(J)
                if not set(Rt)<=il or not set(Ct)<=jl or not set(R2t)<=il or not set(C2t)<=jl: continue
                lr=len(I); lc=len(J)
                if lr-len(Rt)!=lc-len(Ct) or lr-len(R2t)!=lc-len(C2t): continue
                li=[i-off for i in I]; lj=[j-off for j in J]
                posI={off+x:q+1 for q,x in enumerate(li)}
                posJ={off+x:q+1 for q,x in enumerate(lj)}
                local_exp=sum(posI[i] for i in Rt)+sum(posI[i] for i in R2t)+pr*(len(Rt)+len(R2t))
                local_exp+=sum(posJ[j] for j in Ct)+sum(posJ[j] for j in C2t)+pc*(len(Ct)+len(C2t))
                d=det(sub(B,[i-off for i in I if i not in Rt],[j-off for j in J if j not in Ct]))
                d2=det(sub(B,[i-off for i in I if i not in R2t],[j-off for j in J if j not in C2t]))
                w=(-1 if local_exp%2 else 1)*d*d2
                nr,nc=ri+lr,cj+lc
                if nr<=k and nc<=k:
                    key=(nr,nc,(pr+lr)%2,(pc+lc)%2)
                    nxt[key]+=val*w
        dp=nxt; off+=b
    raw=dp.get((k,k,k%2,k%2),0)
    return coef*coef2*raw

def direct_c(F,k):
    n=len(F); total=0
    for I in combinations(range(n),k):
        si=set(I)
        for J in combinations([j for j in range(n) if j not in si],k):
            d=det(sub(F,I,J)); total+=d*d
    return total

def main():
    blocks=[[[1,2],[0,1]],[[0,1],[2,-1]]]
    G=blockdiag(blocks); n=len(G); r=2
    X=[[1,0],[0,1],[1,-1],[2,1]]
    Y=[[0,1],[1,1],[-1,0],[2,-1]]
    F=[[G[i][j]+sum(X[i][s]*Y[j][s] for s in range(r)) for j in range(n)] for i in range(n)]
    T=tags(n,r); results=[]
    for k in range(n//2+1):
        via=0
        for t in T:
            for u in T: via+=transfer_sum(blocks,X,Y,t,u,k)
        direct=direct_c(F,k)
        assert via==direct,(k,via,direct)
        results.append({"k":k,"tag_count":len(T),"ordered_tag_pairs":len(T)**2,"coefficient":direct})
    result={"status":"PASS exact tagged tensor transfer","n":n,"r":r,"blocks":[2,2],"results":results,
            "scope":"Finite exact integer check of local transfer signs, block factorization, and tag-pair contraction only; no general implementation or sampler."}
    Path(__file__).with_name("rank2_block_tensor_check.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
if __name__=="__main__": main()
