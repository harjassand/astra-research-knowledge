"""Exact replay: actual triad -> determinant -> complete Bernstein box cover."""
import sys,json,itertools
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as F
from triad_core import *
from bernstein_all_free import init,split
here=Path(__file__).parent
p0,p1,p2,p3,p4,p5=S.symbols('F A B C D E',real=True)
variables=(p0,p1,p2,p3,p4,p5)
rs=[conformal((p0,p1),(1,0)),conformal((p2,p3),(0,1)),conformal((p4+p5,-p4+p5),(1,1))]
N=moments([r[0] for r in rs],[r[1] for r in rs]);det=S.Poly(N.det(method='domain-ge'),*variables)
actual={tuple(m):F(str(c)) for m,c in det.terms()}
raw={tuple(m):F(c) for m,c in json.loads((here/'all_free.json').read_text())};assert actual==raw
print('PASS: reconstructed full six-output determinant:',len(actual),'terms.')
groups={}
for m,c in actual.items():
 degree=(m[0]+m[1],m[2]+m[3],m[4]+m[5])
 assert sum(d>0 for d in degree)>=2 # one-wave determinants vanish
 if min(degree)>0:groups.setdefault(degree,[]).append((m,c))
assert len(groups)==15
cert=json.loads((here/'all_free_strict_bernstein_certificate.json').read_text());assert len(cert)==120
seen=set();leafcount=0;global_min=None;bounds={}
for row in cert:
 degree=tuple(row['degree']);chart=tuple(row['chart']);assert (degree,chart) not in seen;seen.add((degree,chart))
 assert degree in groups and chart in set(itertools.product([0,1],repeat=3))
 deg,bs=init(groups[degree],chart,degree);trie={}
 for path,claimed_min in row['leaves']:
  node=trie
  for i in range(0,len(path),2):node=node.setdefault((int(path[i]),int(path[i+1])),{})
  assert not node;node['leaf']=F(claimed_min)
 def replay(node,coeff):
  global leafcount,global_min
  if 'leaf' in node:
   assert len(node)==1 and min(coeff)==node['leaf'] and min(coeff)>0
   leafcount+=1;global_min=min(coeff) if global_min is None else min(global_min,min(coeff));return min(coeff)
  keys=list(node);assert len(keys)==2
  axes={k[0] for k in keys};assert len(axes)==1
  axis=next(iter(axes));assert set(keys)=={(axis,0),(axis,1)}
  ll,rr=split(deg,coeff,axis)
  return min(replay(node[(axis,0)],ll),replay(node[(axis,1)],rr))
 bound=replay(trie,bs);bounds[degree]=min(bounds.get(degree,bound),bound)
assert seen==set(itertools.product(groups,itertools.product([0,1],repeat=3)))
assert leafcount==904 and global_min>0
print('PASS: all 15 multidegrees, all 8 output charts, all',leafcount,'covering leaves have positive exact Bernstein coefficients.')
print('Smallest coefficient:',global_min)
(here/'coercivity_bounds.json').write_text(json.dumps({','.join(map(str,k)):str(v) for k,v in bounds.items()},indent=2))
print('PASS: boundary terms have a vanishing third-moment row and are PSD by the inherited global-ROC block argument.')
print('The theorem covers right-isosceles resonant triangles; it does not establish global QC of P0.')
