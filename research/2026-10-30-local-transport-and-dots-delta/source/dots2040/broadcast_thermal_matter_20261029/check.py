"""Independent rational local-force replay; no stochastic/physical validation."""
from fractions import Fraction as F
from itertools import product
import json

def network(n):
    t=2*n+1; m=2*t+n
    c=[F(10)]*t+[F(40)]*t+[F(13)]*n
    g=[F(1)]*t+[F(2)]*t+[F(1)]*n
    b=[F(0)]*m; b[0]=-10;b[t-1]=10
    J=[[F(0)]*m for _ in range(m)]
    def edge(i,j,w):J[i][j]=J[j][i]=F(w)
    for i in range(t-1):edge(i,i+1,-10)
    for i in range(t):edge(i,t+i,-4*(-1)**i)
    for j in range(n):edge(2*j+1,2*t+j,1);edge(2*j+2,2*t+j,1)
    return t,m,c,g,b,J

def run(word):
    n=len(word);t,m,c,g,b,J=network(n);s=[F(-1)]*m
    events=[(F(-51,4), list(range(2,t,2)),1),(F(25,4),[0],1),(F(53,4),list(range(2*t,m)),1),(F(89,4),list(range(t,2*t)),1),(F(-25,4),[0],-1),(F(-53,4),list(range(2*t,m)),-1)]
    for j,bit in enumerate(word):
        events.append((F(29,4),[2*j+1],1))
        if bit:events.append((F(45,4),[2*t+j],1))
        events.append((F(-29 if bit else -21,4),[2*j+2],-1))
    stable=[]; drive=[]
    for H,ids,d in events:
        for i in ids:
            assert all(J[i][j]==0 for j in ids)
            f=g[i]*H+b[i]+sum(J[i][j]*s[j] for j in range(m))
            drive.append(d*f-c[i])
            assert drive[-1]>0
        for i in set(range(m))-set(ids):
            # Exact min over ALL simultaneous intended coordinates [-1,1].
            a=c[i]+s[i]*(g[i]*H+b[i]+sum(J[i][j]*s[j] for j in range(m) if j not in ids))-sum(abs(J[i][j]) for j in ids)
            stable.append(a);assert a>0
        for i in ids:s[i]=F(d)
    assert [int((x+1)/2) for x in s[2*t:]]==list(word)
    return min(stable),min(drive),len(events)

out=[]
for n in range(1,8):
    data=[run(w) for w in product([0,1],repeat=n)]
    out.append(dict(n=n,words=len(data),min_stable=str(min(x[0] for x in data)),min_drive=str(min(x[1] for x in data)),max_events=max(x[2] for x in data)))
print(json.dumps(out,indent=2))
