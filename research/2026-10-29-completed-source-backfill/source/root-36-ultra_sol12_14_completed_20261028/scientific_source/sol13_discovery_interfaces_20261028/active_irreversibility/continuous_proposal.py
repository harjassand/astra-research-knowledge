"""Four charged floating proposals; none is a certificate."""
from model import F,labels
from pathlib import Path
import json,time
START=time.monotonic()
import numpy as np
from scipy.linalg import expm
a=F(1);b=F(33,100);c=F(1,3);g=F(11,200);d=F(5,2)
x=[-3,-1,1,3];u=[1,-1,-1,1];v=[1,-3,3,-1]
def make(circulation):
    A=[[F(0) for j in range(6)] for i in range(6)]
    for i in range(4):
        for j in range(4):
            if i!=j:A[i][j]=c+circulation*(u[i]*v[j]-v[i]*u[j])
        A[i][4]=A[4][i]=a+b*x[i];A[i][5]=A[5][i]=a-b*x[i]
    for i in range(6):A[i][i]=-sum(A[i])
    return A
def tilted(A,D):
    w=[F(1)]*4+[D,F(1)]
    B=[[A[i][j]*w[j]/w[i] if i!=j else F(0) for j in range(6)] for i in range(6)]
    for i in range(6):B[i][i]=-sum(B[i])
    return np.asarray(B,dtype=float)
def prob(mats,word):
    r=np.asarray([float(F(1,6))*int(x==word[0]) for x in labels])
    for P,y in zip(mats,word[1:]):r=(r@P)*np.asarray([int(x==y) for x in labels])
    return r.sum()
rows=[];word=[1,0,0,0,0,2];fields=[F(1),d,F(1),d,F(1)]
for t in [.1,.25,.5,1.]:
    durations=[t,t,t,2*t,t];record={}
    for name,A in [('target',make(g)),('ordinary',make(F(0)))]:
        kernels=[expm(tilted(A,D)*tt) for D,tt in zip(fields,durations)]
        f=prob(kernels,word);r=prob(kernels[::-1],word[::-1]);record[name]={'forward':float(f),'reverse':float(r),'difference':float(f-r)}
    rows.append({'t':t,**record})
out={'proposals':rows,'parameters':list(map(str,[a,b,c,g,d])),'seconds':time.monotonic()-START,
     'scope':'Floating proposals only. Actual continuous-time exp(tQ), not discrete ticks.'}
(Path(__file__).resolve().parent/'CONTINUOUS_PROPOSAL.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
