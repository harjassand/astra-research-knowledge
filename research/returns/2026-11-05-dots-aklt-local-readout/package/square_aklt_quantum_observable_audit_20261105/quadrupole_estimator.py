"""Distinct-site spin2 Qzz estimators from routed closed-loop samples.
Exact Fraction APIs preserve rational outputs; float wrappers are for plotting
and empirical summary statistics only.
"""
from collections import Counter
from fractions import Fraction

def loop_data(routes):
 visits=[Counter(route) for route in routes]
 total=Counter()
 for v in visits:total.update(v)
 return visits,total

def pair_estimator_exact(routes,i,j):
 if i==j:return Fraction(14,5)
 visits,total=loop_data(routes)
 num=2450*sum(v[i]*v[j] for v in visits);den=(2*total[i]+3)*(2*total[j]+3)
 assert num%den==0
 return Fraction(num//den,25)

def pair_estimator(routes,i,j):
 return float(pair_estimator_exact(routes,i,j))

def averaged_horizontal_estimators_exact(routes,side,separations):
 separations=tuple(separations)
 if side<=0 or any(not isinstance(r,int) or r<0 or r>=side for r in separations):
  raise ValueError('Require integer separations0 <= r < side and side > 0')
 visits,total=loop_data(routes);out={r:0 for r in separations}
 for v in visits:
  for (x,y),mi in v.items():
   for r in separations:
    if r==0:continue
    other=(x+r,y);mj=v.get(other,0)
    if mj:
     num=2450*mi*mj;den=(2*total[(x,y)]+3)*(2*total[other]+3)
     assert num%den==0
     out[r]+=num//den
 return {r:(Fraction(14,5) if r==0 else Fraction(z,25*(side-r)*side)) for r,z in out.items()}

def averaged_horizontal_estimators(routes,side,separations):
 return {r:float(x) for r,x in averaged_horizontal_estimators_exact(routes,side,separations).items()}
