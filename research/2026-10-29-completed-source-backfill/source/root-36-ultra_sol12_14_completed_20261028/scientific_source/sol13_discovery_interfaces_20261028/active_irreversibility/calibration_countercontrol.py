"""Exact warning: odd-variable off-diagonal energy tilt need not preserve DB."""
from fractions import Fraction as F
from pathlib import Path
import json,time
START=time.monotonic();n=4;theta=[3,2,1,0];label=[0,1,1,0];d=F(2)
Q=[[F(0) for j in range(n)] for i in range(n)]
for i in range(n):Q[i][(i+1)%n]=1;Q[i][i]=-1
assert all(Q[i][j]==Q[theta[j]][theta[i]] for i in range(n) for j in range(n))
D=[d**y for y in label]
A=[[Q[i][j]*D[j]/D[i] if i!=j else F(0) for j in range(n)] for i in range(n)]
for i in range(n):A[i][i]=-sum(A[i])
gibbs=[z*z/sum(y*y for y in D) for z in D]
stationarity=[sum(gibbs[i]*A[i][j] for i in range(n)) for j in range(n)]
assert any(stationarity)
assert all(gibbs[i]*A[i][j]==gibbs[theta[j]]*A[theta[j]][theta[i]] for i in range(n) for j in range(n) if i!=j)
actual_weights=[1/(-A[i][i]) for i in range(n)]
actual=[w/sum(actual_weights) for w in actual_weights]
assert all(sum(actual[i]*A[i][j] for i in range(n))==0 for j in range(n))
result={'status':'OFFDIAGONAL_TILT_ALONE_FAILS','baseline_parity':theta,'labels':label,'field':'2',
        'baseline_common_parity_DB':True,'tilted_offdiagonal_pairing':True,'tilted_full_DB':False,
        'gibbs_candidate':list(map(str,gibbs)),'gibbs_stationarity_defect':list(map(str,stationarity)),
        'actual_stationary':list(map(str,actual)),
        'actual_label1_mass':str(sum(p for p,y in zip(actual,label) if y==1)),
        'gibbs_label1_mass':str(sum(p for p,y in zip(gibbs,label) if y==1)),
        'seconds':time.monotonic()-START,
        'scope':'Kinematic model countercontrol. No physical equilibrium apparatus is inferred from baseline parity.'}
(Path(__file__).resolve().parent/'CALIBRATION_COUNTERCONTROL.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
