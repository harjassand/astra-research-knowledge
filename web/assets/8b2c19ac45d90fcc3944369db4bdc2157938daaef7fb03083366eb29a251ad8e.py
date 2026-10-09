#!/usr/bin/env python3
"""One exact K=4 stationary/Petz/compatibility identity control; no scan."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import time

started=time.perf_counter()
K=4; d=K+2; w=F(1,K)
checks=[]
def check(cond,label):
    assert cond,label
    checks.append(label)

Z=sum(F(1,2**j) for j in range(K+1))
sigma=[1-w]+[w*F(1,2**j)/Z for j in range(K+1)]
rho=[1-w]+[w/F(K+1) for j in range(K+1)]
P=[[F(0) for j in range(d)] for i in range(d)]
P[0][0]=1
for j in range(1,K+1):P[j][j+1]=1
reset=[F(1,2**(i+1)) for i in range(K)]+[F(1,2**K)]
for i,r in enumerate(reset):P[i+1][1]=r
def action(M,x):return [sum(M[i][j]*x[j] for j in range(d)) for i in range(d)]
def product(A,B):return [[sum(A[i][k]*B[k][j] for k in range(d)) for j in range(d)] for i in range(d)]
def tv(x,y):return sum(abs(a-b) for a,b in zip(x,y))/2
check(sum(sigma)==sum(rho)==1,'faithful state normalizations')
check(min(sigma)>0 and min(rho)>0,'both actual states faithful')
for j in range(d):
    check(sum(P[i][j] for i in range(d))==1,f'column {j} TP')
    check(min(P[i][j] for i in range(d))>=0,f'column {j} positive preparation')
check(action(P,sigma)==sigma,'exact stationarity')
R=[[sigma[i]*P[j][i]/sigma[j] for j in range(d)] for i in range(d)]
for j in range(d):check(sum(R[i][j] for i in range(d))==1,f'Petz column {j} TP')
check(action(R,sigma)==sigma,'Petz exact stationarity')
S=product(R,P)
check(all(S[i][j]*sigma[j]==S[j][i]*sigma[i] for i in range(d) for j in range(d)),'symmetrization KMS detailed balance')
check(P[2][1]*sigma[1]!=P[1][2]*sigma[2],'original channel genuinely non-KMS')

# The actual broadcaster prepares each probability column tensor itself.
for j in range(d):
    joint=[[P[i][j]*P[k][j] for k in range(d)] for i in range(d)]
    check(sum(sum(row) for row in joint)==1,f'broadcast preparation {j} normalized')
    check([sum(row) for row in joint]==[P[i][j] for i in range(d)],f'broadcast marginal one {j}')
    check([sum(joint[i][k] for i in range(d)) for k in range(d)]==[P[k][j] for k in range(d)],f'broadcast marginal two {j}')
    post=[[sum(R[i][a]*joint[a][b]*R[k][b] for a in range(d) for b in range(d)) for k in range(d)] for i in range(d)]
    check([sum(row) for row in post]==[S[i][j] for i in range(d)],f'Petz-postprocessed actual marginal {j}')

b=tv(rho,action(P,rho));r=tv(rho,action(S,rho))
check(b==w*(1-F(1,2**K))/F(K+1),'exact forward half-error formula')
check(r==w*(K-1+F(1,2**K))/F(2*(K+1)),'exact Petz half-error formula')
check(b<=F(1,K*K),'b <= K^-2')
check(r>=F(1,6*K),'r >= (6K)^-1')
check(Z<K+1,'genuine entropy formula certifies D <= ln2/2')
root=Path(__file__).resolve().parent
result={'status':'PASS','K':K,'checks':len(checks),'check_names':checks,'forward_half_error':str(b),'Petz_half_error':str(r),'elapsed_seconds':time.perf_counter()-started,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'invocation':'python3 work/agents/tensor_frame_sol/cycle09_petz_symmetrization/check_reset_chain_exact.py','purpose':'exact finite identity control; analytic all-K and global classical proofs separate'}
(root/'reset_chain_exact_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','K','checks','forward_half_error','Petz_half_error','elapsed_seconds']}))
