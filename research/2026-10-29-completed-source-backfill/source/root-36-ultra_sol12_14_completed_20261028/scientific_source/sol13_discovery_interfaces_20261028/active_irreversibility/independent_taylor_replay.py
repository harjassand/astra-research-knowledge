"""No producer import: rebuild rates and exp(tQ) via direct signed Taylor.

Also consumes rational kernels to build the twelve-state parity comparator.
This is a second code path by the same worker, not a peer audit.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time
START=time.monotonic();OUT=Path(__file__).resolve().parent
raw=json.loads((OUT/'CONTINUOUS_CERTIFICATE.json').read_text())
a,b,c,g,d=[F(raw['parameters'][k]) for k in ['a','b','c','gamma','d']]
x=[-3,-1,1,3];u=[1,-1,-1,1];v=[1,-3,3,-1];labels=[0,0,0,0,1,2]
I=[[F(i==j) for j in range(6)] for i in range(6)]
def mul(A,B):return [[sum(y*z for y,z in zip(row,col)) for col in zip(*B)] for row in A]
def generate(circ,field):
    A=[[F(0) for j in range(6)] for i in range(6)]
    for i in range(4):
        for j in range(4):
            if i!=j:A[i][j]=c+circ*(u[i]*v[j]-v[i]*u[j])
        A[i][4]=(a+b*x[i])*field;A[4][i]=(a+b*x[i])/field
        A[i][5]=A[5][i]=a-b*x[i]
    for i in range(6):A[i][i]=-sum(A[i])
    return A
def taylor(A,t,K=80):
    power=I;coef=F(1);R=[r[:] for r in I]
    for k in range(1,K+1):
        power=mul(power,A);coef=coef*t/k
        R=[[z+coef*y for z,y in zip(row,p)] for row,p in zip(R,power)]
    eta=t*max(sum(abs(z) for z in r) for r in A)
    coef=F(1)
    for k in range(1,K+2):coef=coef*eta/k
    err=coef/(1-eta/(K+2))
    assert all(sum(r)==1 for r in R) and min(z for r in R for z in r)>0
    return R,err
def probability(matrices,pi,word,lab):
    r=[p*int(y==word[0]) for p,y in zip(pi,lab)]
    for M,y in zip(matrices,word[1:]):
        r=[sum(r[i]*M[i][j] for i in range(len(r)))*int(lab[j]==y) for j in range(len(r))]
    return sum(r)
out={};signed={}
for name,circ in [('target',g),('ordinary',F(0))]:
    kernels={};errs={}
    for field,tt in [(F(1),F(1,4)),(d,F(1,4)),(d,F(1,2))]:
        A=generate(circ,field)
        if field==1:assert A==[[F(z) for z in row] for row in raw['Q' if name=='target' else 'S']]
        kernels[field,tt],errs[field,tt]=taylor(A,tt)
    keys=[(F(f),F(t)) for f,t in zip(raw['fields'],raw['durations'])]
    mats=[kernels[k] for k in keys];err=sum(errs[k] for k in keys);word=raw['word'];pi=[F(1,6)]*6
    pf=probability(mats,pi,word,labels);pr=probability(mats[::-1],pi,word[::-1],labels)
    lo,hi=pf-pr-2*err,pf-pr+2*err
    if name=='target':assert -F(700390315,10**16)<lo<hi<-F(700390314,10**16)
    else:assert pf==pr
    oldlo,oldhi=map(F,raw['outcomes'][name]['difference_interval'])
    assert max(lo,oldlo)<min(hi,oldhi)
    out[name]={'difference_interval':[str(lo),str(hi)],'display_difference':float(pf-pr)}

# Exact parity lift of each saved normalized uniformization kernel. The
# stationary adjoint is formed from its known Gibbs law, not a new query.
lifted=[];liftlabels=labels*2
for field,tt in zip(map(F,raw['fields']),map(F,raw['durations'])):
    pi=[F(1)/(5+field*field)]*4+[field*field/(5+field*field),F(1)/(5+field*field)]
    P=[[F(z) for z in r] for r in raw['kernel_queries'][f'target:{field}:{tt}']['kernel']]
    adj=[[pi[j]*P[j][i]/pi[i] for j in range(6)] for i in range(6)]
    R=[[P[i][j] if i<6 and j<6 else adj[i-6][j-6] if i>=6 and j>=6 else F(0) for j in range(12)] for i in range(12)]
    theta=lambda i:(i+6)%12
    hat=pi*2
    assert all(hat[i]*R[i][j]==hat[theta(j)]*R[theta(j)][theta(i)] for i in range(12) for j in range(12))
    lifted.append(R)
lf=probability(lifted,[F(1,12)]*12,raw['word'],liftlabels)
lr=probability(lifted[::-1],[F(1,12)]*12,raw['word'][::-1],liftlabels)
pf,pr=map(F,[raw['outcomes']['target']['forward_approximation'],raw['outcomes']['target']['reverse_approximation']])
assert lf==lr==(pf+pr)/2
result={'status':'INDEPENDENT_SIGNED_TAYLOR_REPLAY_PASSED','degree':80,'outcomes':out,
        'twelve_state_comparator':{'forward_equals_reverse_equals_target_average':'EXACT','reducible':True,
                                   'physical_parity_or_sector_preparation_acquired':False},
        'seconds':time.monotonic()-START,
        'scope':'Same-worker independent code path, not independent peer or physical validation.'}
(OUT/'INDEPENDENT_TAYLOR_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'seconds':result['seconds'],'comparator':result['twelve_state_comparator']},indent=2))
