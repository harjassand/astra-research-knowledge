from fractions import Fraction as F
import json
from pivot_lift import recognize, construct, exact_generator, weak_reversible

def reaction(n,u,v,k=1):
 return ((u,)+(0,)*(n-1),(v,)+(0,)*(n-1),F(k))
def stars(n):
 out=[]
 for j in range(1,n):
  aa=(2,)+(0,)*(n-1); ab=tuple(1 if i in (0,j) else 0 for i in range(n))
  out.extend([(aa,ab,F(j+1,j+2)),(ab,aa,F(j+2,j+1))])
 return out
cases=[(1,[(0,1),(1,0)]),(1,[(0,5),(5,0)]),
 (2,[(0,1),(1,0)]),(2,[(0,5),(5,0)]),
 (2,[(1,3),(3,1)]),(2,[(2,5),(5,2)]),
 (3,[(0,2),(2,5),(5,0)]),(3,[(1,4),(4,2),(2,1)])]
checks=0; summaries=[]
for n,edges in cases:
 rs=[reaction(n,u,v,F(i+1,i+2)) for i,(u,v) in enumerate(edges)]+stars(n)
 rec=recognize([str(i) for i in range(n)],rs); assert rec['accepted']
 for t in [F(11,10),F(3,2),F(3)]:
  cert=construct(rec,t); assert all(F(x)<=0 for x in cert['shifted_numerator_coeffs'])
  assert all(F(x)>=0 for x in cert['shifted_denominator_coeffs'])
  assert F(cert['shifted_denominator_coeffs'][-1])>0
  points=list(range(9))+[cert['R'],cert['R']+1]
  for av in points:
   for bv in ([0,1,7] if n>1 else [0]):
    x=(av,)+(bv,)*(n-1)
    V,LV=exact_generator(rec,cert,x)
    if av==0 and cert['zero_face_conservative']: assert LV==0
    else: assert LV<=-cert['epsilon']*V+cert['foster_C'],(n,edges,t,x)
    checks+=1
  summaries.append({'n':n,'core':edges,'t':str(t),'R':cert['R']})
for n in [1,2,3]:
 rec=recognize([str(i) for i in range(n)],stars(n))
 assert rec['accepted'] and construct(rec)['finite_shells'];checks+=1
assert weak_reversible([(0,1),(1,2),(2,0)])
assert not weak_reversible([(0,1),(1,2)])
checks+=2
bad=stars(3)+[reaction(3,0,1),reaction(3,1,0),((0,0,0),(0,1,0),F(1)),((0,1,0),(0,0,0),F(1))]
assert not recognize(['A','B','C'],bad)['accepted'];checks+=1
# Constructor is not a hardened typed verifier: document rather than promote.
r=recognize(['A'],[reaction(1,0,1),reaction(1,1,0)])
c=construct(r,2.0)
assert isinstance(c['t'],float)
print(json.dumps({'checks':checks,'cases':summaries,'float_parameter_accepted':True,'scope':'Finite exact challenges, not proof; float acceptance documents trusted API limitation.'},indent=2))
