"""Exact finite diagnostics for the separate analytic transfer-current proof.

Python standard library only; this does not establish its universal quantifiers.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
import random


def solve(a,b):
    n=len(b)
    m=[list(row)+[value] for row,value in zip(a,b)]
    for i in range(n):
        p=next(k for k in range(i,n) if m[k][i])
        m[i],m[p]=m[p],m[i]
        z=m[i][i];m[i]=[v/z for v in m[i]]
        for k in range(n):
            if k!=i:
                z=m[k][i];m[k]=[v-z*t for v,t in zip(m[k],m[i])]
    return [row[-1] for row in m]


def main():
    rng=random.Random(20261015);records=[]
    for case in range(36):
        n=3+case%6;s,t=0,n-1
        edges={(i,i+1):Q(rng.randint(1,9),rng.randint(1,7)) for i in range(n-1)}
        for i in range(n):
            for j in range(i+2,n):
                if rng.random()<.3:edges[i,j]=Q(rng.randint(1,9),rng.randint(1,7))
        w=[Q(rng.randint(1,20),rng.randint(1,9)) for _ in range(n)]
        L=[[Q(0) for _ in range(n)] for _ in range(n)]
        for (i,j),c in edges.items():L[i][i]+=c;L[j][j]+=c;L[i][j]-=c;L[j][i]-=c
        I=list(range(1,n-1));K=[[L[i][j] for j in I] for i in I];b=[-L[i][s] for i in I]
        h=solve(K,b);N=w[s]+sum(w[i]*hi for i,hi in zip(I,h))
        distances=[None]*n;distances[s]=distances[t]=Q(0)
        pending=set(range(n))
        while pending:
            i=min((i for i in pending if distances[i] is not None),key=lambda i:distances[i]);pending.remove(i)
            for (j,k),c in edges.items():
                other=k if j==i else j if k==i else None
                if other in pending:
                    v=distances[i]+1/c
                    if distances[other] is None or v<distances[other]:distances[other]=v
        B=sum(w[i]*distances[i] for i in I)
        for lam in [Q(1,100),Q(1),Q(10)]:
            Kl=[row[:] for row in K]
            for j,i in enumerate(I):Kl[j][j]+=lam*w[i]
            hl=solve(Kl,b);Nl=w[s]+sum(w[i]*v for i,v in zip(I,hl))
            # Direct off-diagonal Schur entry of the actual augmented graph.
            KI=[-lam*w[i] for i in I];v=solve(Kl,[-L[i][s] for i in I])
            g=lam*w[s]-sum(k*vi for k,vi in zip(KI,v))
            assert g/lam==Nl and Nl<=N<=w[s]+(1+lam*B)*(Nl-w[s])
            records.append({'case':case,'lambda':str(lam),'N':str(N),'N_lambda':str(Nl),'B':str(B),'g_as':str(g)})
    out={'status':'PASS','exact_fixtures':len(records),'records':records,'scope':'Finite rational diagnostics; universal analytic proof separately stated, historical priority and performance advantage UNKNOWN.'}
    Path(__file__).with_name('TRANSFER_CURRENT_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],out['exact_fixtures'])


if __name__=='__main__':main()
