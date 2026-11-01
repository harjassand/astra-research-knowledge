"""Independent exact-power/refined-Darboux reference, no candidate imports.
Every point is evaluated as an exact rational power, then independently enclosed
at 4096 dyadic bits before accumulation. The complete nominal analytic tail is
added, not sampled away. Refinement is twice the actual received grid.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time
H=Path(__file__).resolve().parent;rows=json.loads((H/'robust_well_kinetics_20261031/results.json').read_text());start=time.perf_counter();Q=1<<4096;N=65536;a=128;points=0;checks=[]
def ok(x,label):assert x,label;checks.append(label)
def point(y,e,kind):
 global points
 x=y*y;v=1+(1-x)**2;b=v+e*x*(1-x)**2/(1+x)
 q=(1/b if kind=='mass'else 4/(4-b))**a
 z,rem=divmod(q.numerator*Q,q.denominator);points+=1
 return z,z+(rem!=0)
def integrate(l,r,e,kind):
 h=(r-l)/N;prev=point(l,e,kind);low=high=0
 for j in range(1,N+1):
  cur=point(l+j*h,e,kind);low+=min(prev[0],cur[0]);high+=max(prev[1],cur[1]);prev=cur
 return h*F(low,Q),h*F(high,Q)
tail=F(2,4*a-1)/9**a;refs={}
for e in [F(0),F(1,1000)]:
 l,h=integrate(F(1,2),F(1),e,'mass');ll,hh=integrate(F(1),F(2),e,'mass');p,q=integrate(F(0),F(1,2),e,'resistance');refs[str(e)]={'mass':(l+ll,h+hh+tail),'resistance':(2*p,2*q)}
# R_v is integrated exactly as the polynomial (2-2 y²+y⁴)^alpha.
coef=[1]
for _ in range(a):
 out=[0]*(len(coef)+2)
 for j,x in enumerate(coef):
  for k,y in enumerate([2,-2,1]):out[j+k]+=x*y
 coef=out
Rv=sum((F(x,2**(2*j)*(2*j+1))for j,x in enumerate(coef)),F(0))
for row in rows:
 c=row['certificate'];e=row['original_defect'];ok(c['N']*2==N and c['T']=='2','actual grid and complete tail interface')
 for key,val in [('nominal_basin_mass',refs['0']['mass']),('lower_density_basin_mass',refs[e]['mass']),('robust_slab_resistance',refs[e]['resistance'])]:
  l,h=map(F,[c[key]['lower'],c[key]['upper']]);rl,rh=val;ok(l<=rl<=rh<=h,'actual '+key+' contains independent exact-power refined-Darboux enclosure')
 ok(F(c['nominal_resistance']['lower'])<=Rv<=F(c['nominal_resistance']['upper']),'actual nominal resistance contains independent exact polynomial integral')
 ok(F(c['tail_upper'])>=tail,'actual full-infinity majorant outward')
report={'status':'PASS','checks':len(checks),'tests':checks,'exact_rational_points':points,'independent_grid_per_segment':N,'dyadic_accumulation_bits':4096,'reference':{e:{k:{'lower':str(l),'upper':str(h)}for k,(l,h)in d.items()}for e,d in refs.items()},'seconds_diagnostic':time.perf_counter()-start}
(H/'independent_scalar_reference_results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='reference'},indent=2))
