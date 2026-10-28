"""Independent literal-matrix check of the SAME N32 scalar interface.

Exact arithmetic only; no thermal trajectory, device record or new source
case. This checks implementation identities, not scientific novelty or
an independently implemented stochastic likelihood.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time

HERE=Path(__file__).resolve().parent;r=json.loads((HERE/'INTERFACE.json').read_text())
start=time.perf_counter();n=r['N']
k=[[F(3 if i==j else -1 if abs(i-j)==1 else 0) for j in range(n)] for i in range(n)]
aug=[row+[F(i==j) for j in range(n)] for i,row in enumerate(k)]
pivots=[];updates=0
for i in range(n):
 pivot=aug[i][i];assert pivot>0;pivots.append(pivot)
 aug[i]=[x/pivot for x in aug[i]]
 for j in range(n):
  if j!=i and aug[j][i]:
   scale=aug[j][i];aug[j]=[x-scale*y for x,y in zip(aug[j],aug[i])];updates+=2*n
inv=[row[n:] for row in aug]
assert all(aug[i][j]==F(i==j) for i in range(n) for j in range(n))
inv2=[[sum((inv[i][z]*inv[z][j] for z in range(n)),F(0)) for j in range(n)] for i in range(n)]
mu=sum((inv[i][i] for i in range(n)),F(0));var=sum((inv2[i][i] for i in range(n)),F(0))
g=F(r['g']['exact']);rho2=F(r['rho_squared_upper']['exact'])
assert inv[0][-1]==g
assert inv[0][0]==F(r['b_equals_d']['exact'])
assert inv2[0][0]==F(r['R2_pp']['exact'])
assert mu==F(r['C_long_exposure_interface']['travel_mean']['exact'])
assert var==F(r['C_long_exposure_interface']['travel_variance']['exact'])
for j,expected in [(n-1,g*(61*mu-12)),(n-2,g*(183*mu-97))]:
 assert 35*inv2[0][j]+6*inv2[1][j]+inv2[2][j]==expected
v0,v1=inv2[0][-2],inv2[0][-1]
c00,c01,c11=inv2[-2][-2],inv2[-2][-1],inv2[-1][-1]
spectral0=(c11*v0*v0-2*c01*v0*v1+c00*v1*v1)/((c00*c11-c01*c01)*inv2[0][0])
assert 0<=spectral0<=rho2<=1
out={'status':'EXACT_SAME_SOURCE_MATRIX_IDENTITIES_PASS','N':n,'checks':['Literal rational inverse matches g,d','Literal square inverse matches R2_pp','Literal traces match travel mu,var','Both spectral U constants match61/183 formulas','Exact omega0 canonical correlation below global certified upper'],'omega0_rho_squared':str(spectral0),'global_rho_squared_upper':str(rho2),'rational_elimination_pivots':len(pivots),'elimination_scalar_row_updates':updates,'new_source_case':False,'trajectories':0,'data_readouts':0,'seconds_after_imports':time.perf_counter()-start}
(HERE/'CONSTANT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['omega0_rho_squared','global_rho_squared_upper']},indent=2))
