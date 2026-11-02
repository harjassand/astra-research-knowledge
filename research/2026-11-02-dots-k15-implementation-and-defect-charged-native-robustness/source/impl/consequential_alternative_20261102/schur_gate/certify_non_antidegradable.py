"""Rational PSD dual for Pauli-flag self-compatibility; intervals added when available."""
import json,os
from fractions import Fraction as F
import numpy as np
HERE=os.path.dirname(__file__)
a=next(x for x in json.load(open(HERE+'/non_antidegradable_dual_diagnostic.json')) if x['v']==.38 and x['r']==3 and x['K']==3)
u=np.array(a['dual_diagnostic']['r1'])+1e-6;v=np.array(a['dual_diagnostic']['r2'])+1e-6
ur=[[F(round(float(z)*10**10),10**10) for z in row] for row in u];vr=[[F(round(float(z)*10**10),10**10) for z in row] for row in v]
H=[[F(x,2) for x in row] for row in [[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]]]
allp=[]
for i in range(3):
 for j in range(3):
  W=[[sum(H[k][s]*vr[j][s]*H[s][l] for s in range(4))+(ur[i][k] if k==l else 0) for l in range(4)] for k in range(4)]
  for k in range(4):
   piv=W[k][k];assert piv>0,(i,j,k,piv);allp.append(piv)
   for x in range(k+1,4):
    for y in range(k+1,4):W[x][y]-=W[x][k]*W[k][y]/piv
c=sum(float(ur[i][j]+vr[i][j])*a['target'][i][j] for i in range(3) for j in range(4))
out=dict(status='exact rational positive-definiteness certificate; target probability functional still diagnostic until interval target substituted',u=[[str(x) for x in row] for row in ur],v=[[str(x) for x in row] for row in vr],H=[[str(x) for x in row] for row in H],all_ldl_pivots_positive=True,min_ldl_pivot_float=min(map(float,allp)),diagnostic_C=c,ldl_pivots=[str(x) for x in allp])
json.dump(out,open(HERE+'/non_antidegradable_rational_dual.json','w'),indent=2);print({k:v for k,v in out.items() if k not in ['u','v','H','ldl_pivots']})
# Exact dyadic interval endpoints from the physical lookup-partition integration certificate.
physical=next(x for x in json.load(open(os.path.dirname(HERE)+'/certified_repetition_quantizers.json')) if x['v']==.38)
def dyadic(x):
 sign,mant,e,bits=x
 return (-1 if sign else 1)*F(mant)*(F(2)**e)
upper=F(0);lower=F(0)
for i in range(3):
 for j in range(4):
  c=ur[i][j]+vr[i][j];end=physical['joint_mass_interval_dyadic'][i][j];lo=dyadic(end['lower']);hi=dyadic(end['upper'])
  upper+=c*(hi if c>=0 else lo);lower+=c*(lo if c>=0 else hi)
assert upper<0
out.update(status='CERTIFIED: all nine dual matrices are exactly rational positive definite, and dual functional upper bound is strictly negative for the interval-enclosed physical Gaussian lookup channel',physical_v=.38,physical_aspect=3,lookup_sha256=physical['assignment_sha256'],dual_C_lower_exact=str(lower),dual_C_upper_exact=str(upper),dual_C_bounds_float=[float(lower),float(upper)])
json.dump(out,open(HERE+'/non_antidegradable_rational_dual.json','w'),indent=2)
print('CERTIFIED physical C interval',float(lower),float(upper))
