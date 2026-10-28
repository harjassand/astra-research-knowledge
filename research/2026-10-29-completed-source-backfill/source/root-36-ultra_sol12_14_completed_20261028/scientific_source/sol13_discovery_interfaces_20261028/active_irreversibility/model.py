"""Explicit rational six-state controlled model, no experimental input."""
from fractions import Fraction as F
x=[-3,-1,1,3];u=[1,-1,-1,1];v=[1,-3,3,-1]
n=6;labels=[0,0,0,0,1,2]
S=[[F(0) for j in range(n)] for i in range(n)]
for i in range(4):
    for j in range(4):
        if i!=j:S[i][j]=F(1)
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
def tick(A,tau=F(1,16)):
    P=[[F(i==j)+tau*A[i][j] for j in range(n)] for i in range(n)]
    assert min(t for row in P for t in row)>=0
    return P
def controlled_word(matrices,pi,w):
    r=[p*int(a==w[0]) for p,a in zip(pi,labels)]
    for A,a in zip(matrices,w[1:]):
        r=[sum(r[i]*A[i][j] for i in range(n))*int(labels[j]==a) for j in range(n)]
    return sum(r)

def make_family(a,b,c,circulation):
    """Parameters are rational rates; all off-diagonal rates are positive
    when a>3|b| and c>6|circulation|."""
    A=[[F(0) for j in range(6)] for i in range(6)]
    for i in range(4):
        for j in range(4):
            if i!=j:A[i][j]=c+circulation*(u[i]*v[j]-v[i]*u[j])
        A[i][4]=A[4][i]=a+b*x[i]
        A[i][5]=A[5][i]=a-b*x[i]
    for i in range(6):A[i][i]=-sum(A[i])
    return A
