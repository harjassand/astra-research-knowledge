"""An exact finite projective 2-design outside the SIC convex-order class.

All entries are in Q[sqrt(2),sqrt(5),sqrt(7),i]. Sparse mask arithmetic
checks the actual48 rank-one projectors and every second-moment entry.
The obstruction is to full convex order, NOT to the entropy inequality.
"""
from fractions import Fraction as Q
from pathlib import Path
from time import perf_counter
import json,sys
import exact_entropy as e
sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent
BASES=[2,5,7,-1]
def clean(x):return{k:Q(v)for k,v in x.items()if v}
def f(x=0,mask=0):return clean({mask:Q(x)})
def add(a,b):
 c=a.copy()
 for k,v in b.items():c[k]=c.get(k,Q(0))+v
 return clean(c)
def scale(a,x):return clean({k:v*x for k,v in a.items()})
def conj(a):return clean({k:(-v if k&8 else v)for k,v in a.items()})
def mul(a,b):
 out={}
 for i,x in a.items():
  for j,y in b.items():
   factor=1
   for bit,p in enumerate(BASES):
    if i&j&(1<<bit):factor*=p
   mask=i^j;out[mask]=out.get(mask,Q(0))+x*y*factor
 return clean(out)
def total(xs):
 out=f()
 for x in xs:out=add(out,x)
 return out
def zeros(n):return[[f()for _ in range(n)]for _ in range(n)]
def mm(a,b):return[[total(mul(x,y)for x,y in zip(row,col))for col in zip(*b)]for row in a]
def trace(a):return total(a[i][i]for i in range(len(a)))
def weighted(weights,gs):return[[total(scale(g[i][j],w)for g,w in zip(gs,weights))for j in range(3)]for i in range(3)]

def build_design():
 one=f(1);ii=f(1,8)
 rays=[([one,f()],1),([f(),one],1),([one,one],2),([one,f(-1)],2),([one,ii],2),([one,scale(ii,-1)],2)]
 phases=[one,ii,f(-1),scale(ii,-1)]
 projectors=[];weights=[];radii=[]
 for y,wy in[(Q(2,9),Q(9,11)),(Q(5,6),Q(2,11))]:
  for v,norm in rays:
   # sqrt(y(1-y)/norm), represented by the indicated square-free mask.
   cross={(Q(2,9),1):f(Q(1,9),5),(Q(2,9),2):f(Q(1,9),4),
          (Q(5,6),1):f(Q(1,6),2),(Q(5,6),2):f(Q(1,12),3)}[y,norm]
   assert mul(cross,cross)==f(y*(1-y)/norm)
   for phase in phases:
    s=zeros(3);s[0][0]=f(y)
    for a in range(2):
     s[a+1][0]=mul(cross,mul(phase,v[a]));s[0][a+1]=conj(s[a+1][0])
     for b in range(2):s[a+1][b+1]=scale(mul(v[a],conj(v[b])),(1-y)/norm)
    assert trace(s)==one and mm(s,s)==s
    assert all(s[i][j]==conj(s[j][i])for i in range(3)for j in range(3))
    projectors.append(s);weights.append(wy/24);radii.append(y)
 assert len(projectors)==48 and sum(weights)==1
 literal_keys=[tuple(tuple(tuple(sorted(cell.items()))for cell in row)for row in s)for s in projectors]
 assert len(set(literal_keys))==48
 assert weighted(weights,projectors)==[[f(Q(1,3)if i==j else 0)for j in range(3)]for i in range(3)]
 return projectors,weights,radii

def main():
 start=perf_counter();projectors,weights,radii=build_design()
 checks=0
 for i in range(3):
  for j in range(3):
   for k in range(3):
    for l in range(3):
     value=total(scale(mul(s[i][j],s[k][l]),w)for w,s in zip(weights,projectors))
     assert value==f(Q(int(i==j and k==l)+int(i==l and k==j),12));checks+=1
 mean=sum(w*y for w,y in zip(weights,radii));second=sum(w*y*y for w,y in zip(weights,radii))
 assert mean==Q(1,3)and second==Q(1,6)
 hinge=sum(w*max(2*y-1,0)for w,y in zip(weights,radii))
 assert hinge==Q(4,33)and hinge-Q(1,9)==Q(1,99)
 high=[w if y==Q(5,6)else Q(0)for w,y in zip(weights,radii)]
 c=weighted([9*w for w in high],projectors)
 assert c==[[f(Q(15,11)if i==0 else Q(3,22))if i==j else f()for j in range(3)]for i in range(3)]
 # A positive entropy control deliberately does not certify the full bad design.
 hp=e.entropy([e.iv(Q(5,6)),e.iv(Q(1,12)),e.iv(Q(1,12))])
 control=e.add(e.sub(e.logq(Q(11,2)),e.scale(e.logq(3),2)),e.scale(hp,2))
 assert control[0]>0
 out={'status':'PASS','d':3,'actual_weighted_projectors':48,'distinct_projectors':48,
 'rank_one_Hermitian_idempotence_checks':48,'second_moment_components':checks,
 'radial_law':{'2/9':'9/11','5/6':'2/11'},'hemisphere_value':e.serial(hinge),
 'pair_score_hinge_value':'1/9','strict_convex_order_violation':'1/99',
 'selected_C_spectrum':['15/11','3/22','3/22'],'selected_mass_m':'18/11','transport_edge_cut_violation':'1/11',
 'uniform_distinct_variant':{'n':264,'high_radius_phase_grid':8,'low_radius_phase_grid':36,
  'qubit_base_rays':6,'proof':'DESIGN_OBSTRUCTION.md, exact phase-character sums'},
 'one_positive_entropy_control':e.record(control),'all_preparation_entropy_status':'NOT_DECIDED by this mechanism obstruction',
 'SIC_convex_hull':'Strictly outside even the weakly closed convex hull of qutrit SIC design measures, separated by the continuous hemisphere test at e0.',
 'seconds':perf_counter()-start,'prior_priority':'UNKNOWN'}
 (HERE/'DESIGN_OBSTRUCTION.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
