from fractions import Fraction as F
import runpy, contextlib, io, math
from pathlib import Path
root=str(Path(__file__).resolve().parent.parent/'certified_control_escape')+'/'
for file,h_floor,error_ceiling in [('worked_example.py',F('0.19739'),F('0.011827')),('reciprocal_example.py',F('1.25357'),F('0.027424'))]:
 with contextlib.redirect_stdout(io.StringIO()): r=runpy.run_path(root+file)
 H,a,HH,aa,iv=r['H'],r['a'],r['HH'],r['aa'],r['iv']
 assert all(HH[i][j].l<=H[i][j]<=HH[i][j].h for i in range(3) for j in range(3))
 assert all(aa[i].l<=a[i]<=aa[i].h for i in range(3))
 margin=min(H[i][i]-sum(abs((H[i][j]+H[j][i])/2) for j in range(3) if j!=i) for i in range(3))
 assert margin==(F(1,5) if file.startswith('worked') else F(13,10))
 assert r['h']==margin-r['deltaH'] and r['h']>h_floor
 assert r['bound']<error_ceiling
 # Verify all exact gauge-related choices and original true matrix scalar response.
 if file.startswith('worked'):
  assert len(r['keep'])==1
  Hstar=[[H[j][i]*a[j]/a[i] for j in range(3)] for i in range(3)]
  for u in ([0,0,0],[1,0,0],[F(1,3),0,F(2,3)],[1,1,1]):
   z1=r['response'](H,a,u); z2=r['response'](Hstar,a,u)
   assert z1.l==z1.h==z2.l==z2.h
 print(file,'exact inclusion, Gershgorin, robust h, bound PASS',float(r['h']),float(r['bound']))
N=1588; M=14; sigma=1e-7; radius=1e-8
failure_upper=2*M*math.exp(-N*radius**2/(2*sigma**2))
assert failure_upper<.01 and N*M==22232
print('Gaussian union upper bound',failure_upper,'N total',N*M)

# Exact rational verification of the Gaussian union probability bound.
x=F(397,50); term=F(1); exp_lower=term
for k in range(1,41):
 term=term*x/k; exp_lower+=term
assert F(28)/exp_lower < F(1,100)
print('Exact rational Gaussian union-bound check PASS')
