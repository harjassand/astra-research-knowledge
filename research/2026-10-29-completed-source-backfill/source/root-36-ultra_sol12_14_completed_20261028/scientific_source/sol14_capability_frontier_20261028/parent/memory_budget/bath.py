"""Actual singular noncommuting bath, after the whole-white proof is paid."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,time
sys.set_int_max_str_digits(0)
START=time.perf_counter();HERE=Path(__file__).resolve().parent
PRIOR=HERE.parents[2]/'sol12_structural_capability_20261028'/'quantum_independent'
sys.path.insert(0,str(PRIOR));import frame as f
source=json.loads((HERE/'SOURCE.json').read_text())
white=json.loads((HERE/'WHOLE_WHITE.json').read_text())
assert white['status']=='EXACT_WHOLE_WHITE_CURVE_ADMITTED'
X=[[(F(z[0]),F(z[1]))for z in row]for row in source['X']]
U=[[F(1,2)]*2 for _ in range(2)];V=[[F(1),F(0)],[F(0),F(0)]]
Z=f.zeros(36)
for i in range(18):
 for j in range(18):
  for u in range(2):
   for v in range(2):
    Z[2*i+u][2*j+v]=f.add(f.scale(X[i][j],U[u][v]),f.z(int(i==j)*V[u][v]))
assert f.trace(Z)==f.z(1054)
assert all(Z[2*i+1][2*j+1]==f.scale(X[i][j],F(1,2))for i in range(18)for j in range(18))
assert all(f.total(Z[12*i+k][12*j+k]for k in range(12))==f.z(F(1054,3)if i==j else 0)for i in range(3)for j in range(3))
gap=F(white['h0_interval']['lower'])/F(2108)
assert gap>F(36,1000)
out={'status':'PAID_COMMON_BATH_RECEIVER','source_dimension':36,'source_rank':28,
 'reference_dimension':12,'antisymmetric_extension_dimension':108,'source_trace':1054,
 'CMI_excess_lower':str(gap),'CMI_excess_lower_display':float(gap),
 'proof':'Whole-white curve plus inherited atom qprime(0+)=1/2; remaining measure nonnegative.',
 'normalized_physical_qutrit_marginal':'I3/3','normalized_reference_marginal':'not asserted flat',
 'bath_U':[[str(v)for v in row]for row in U],'bath_V':[[str(v)for v in row]for row in V],
 'seconds':time.perf_counter()-START,'physical_implementation':False,'priority':'UNKNOWN'}
(HERE/'BATH.json').write_text(json.dumps(out,indent=2)+'\n')
(HERE/'BATH_SOURCE.json').write_text(json.dumps({'field':'Q[sqrt(-3)]','Z':[[[str(z[0]),str(z[1])]for z in row]for row in Z]},indent=2)+'\n')
print(json.dumps({k:out[k]for k in ['status','CMI_excess_lower_display','seconds']},indent=2))
