#!/usr/bin/env python3
"""Exact rank-two determinant update expansion checks on small block examples."""
from itertools import combinations, permutations
import json
from pathlib import Path


def det(A):
    n=len(A)
    if n==0: return 1
    z=0
    for p in permutations(range(n)):
        inv=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=-1 if inv%2 else 1
        for i,j in enumerate(p): term*=A[i][j]
        z+=term
    return z

def sub(A,I,J): return [[A[i][j] for j in J] for i in I]
def blockdiag(bs):
    n=sum(len(B) for B in bs); A=[[0]*n for _ in range(n)]; o=0
    for B in bs:
        for i in range(len(B)):
            for j in range(len(B)): A[o+i][o+j]=B[i][j]
        o+=len(B)
    return A

def rank_update_expansion(G,X,Y,I,J):
    k=len(I); r=len(X[0]) if X else 0; total=0
    for p in range(min(k,r)+1):
        for Apos in combinations(range(k),p):
            R=[I[a] for a in Apos]
            irest=[I[a] for a in range(k) if a not in Apos]
            for Bpos in combinations(range(k),p):
                C=[J[b] for b in Bpos]
                jrest=[J[b] for b in range(k) if b not in Bpos]
                rem=det(sub(G,irest,jrest))
                for S in combinations(range(r),p):
                    xminor=det([[X[i][s] for s in S] for i in R])
                    yminor=det([[Y[j][s] for s in S] for j in C])
                    sign=-1 if (sum(Apos)+sum(Bpos))%2 else 1
                    total+=sign*xminor*yminor*rem
    return total

def main():
    blocks=[[[1,2],[0,1]],[[0,1],[2,-1]]]
    G=blockdiag(blocks); n=len(G); r=2
    X=[[1,0],[0,1],[1,-1],[2,1]]
    Y=[[0,1],[1,1],[-1,0],[2,-1]]
    F=[[G[i][j]+sum(X[i][s]*Y[j][s] for s in range(r)) for j in range(n)] for i in range(n)]
    fixtures=0
    for k in range(n//2+1):
        for I in combinations(range(n),k):
            si=set(I)
            for J in combinations([j for j in range(n) if j not in si],k):
                direct=det(sub(F,I,J)); expanded=rank_update_expansion(G,X,Y,I,J)
                assert direct==expanded,(k,I,J,direct,expanded)
                fixtures+=1
    result={"status":"PASS exact integer rank-two minor expansion","n":n,"r":r,"minor_fixtures":fixtures,
            "scope":"Verifies the matrix-minor/Cauchy-Binet expansion on this input only; does not implement the block transfer DP or sampler."}
    Path(__file__).with_name("rank2_minor_expansion_check.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__": main()
