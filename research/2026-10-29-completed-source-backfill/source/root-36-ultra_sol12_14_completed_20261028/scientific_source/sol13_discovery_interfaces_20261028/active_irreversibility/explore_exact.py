"""Small exact constructive test; not a physical acquisition."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,time
START=time.monotonic();OUT=Path(__file__).resolve().parent
x=[-3,-1,1,3];u=[1,-1,-1,1];v=[1,-3,3,-1]
n=6;labels=[0,0,0,0,1,2]
S=[[F(0) for j in range(n)] for i in range(n)]
for i in range(4):
    for j in range(4):
        if i!=j:S[i][j]=1
    S[i][4]=S[4][i]=1+F(x[i],4)
    S[i][5]=S[5][i]=1-F(x[i],4)
for i in range(n):S[i][i]=-sum(S[i])
K=[[F(u[i]*v[j]-v[i]*u[j],12) if i<4 and j<4 else F(0) for j in range(n)] for i in range(n)]
Q=[[S[i][j]+K[i][j] for j in range(n)] for i in range(n)]
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def mv(A,v):return [sum(a*b for a,b in zip(row,v)) for row in A]
def tilt(A,d):
    D=[F(1)]*4+[F(d),F(1)]
    out=[[A[i][j]*D[j]/D[i] if i!=j else F(0) for j in range(n)] for i in range(n)]
    for i in range(n):out[i][i]=-sum(out[i])
    pi=[z*z/sum(y*y for y in D) for z in D]
    return out,pi
def word(A,pi,w):
    r=[p*int(a==w[0]) for p,a in zip(pi,labels)]
    for a in w[1:]:r=[sum(r[i]*A[i][j] for i in range(n))*int(labels[j]==a) for j in range(n)]
    return sum(r)
def tick(A,tau):return [[F(i==j)+tau*A[i][j] for j in range(n)] for i in range(n)]
assert all(sum(row)==0 for row in Q) and all(sum(Q[i][j] for i in range(n))==0 for j in range(n))
results=[]
for d in [F(2),F(4),F(1,2)]:
    A,pi=tilt(Q,d);B,_=tilt(S,d)
    assert all(sum(pi[i]*A[i][j] for i in range(n))==0 for j in range(n))
    assert all(pi[i]*B[i][j]==pi[j]*B[j][i] for i in range(n) for j in range(n))
    tau=1/(2*max(-A[i][i] for i in range(n)));P=tick(A,tau)
    pair=None;power=[[F(i==j) for j in range(n)] for i in range(n)]
    for k in range(1,21):
        power=mm(power,P)
        for a,b in product(range(3),repeat=2):
            diff=sum(pi[i]*power[i][j]-pi[j]*power[j][i] for i in range(n) for j in range(n) if labels[i]==a and labels[j]==b)
            if diff:pair={'lag':k,'a':a,'b':b,'difference':str(diff),'display':float(diff)};break
        if pair:break
    found=None
    for length in range(2,9):
        for w in product(range(3),repeat=length):
            z=word(P,pi,w)-word(P,pi,w[::-1])
            if z:found={'length':length,'word':w,'difference':str(z),'display':float(z)};break
        if found:break
    results.append({'d':str(d),'tau':str(tau),'pair':pair,'word':found})
    print(results[-1],flush=True)
(OUT/'EXPLORATION.json').write_text(json.dumps({'results':results,'seconds':time.monotonic()-START},indent=2)+'\n')
