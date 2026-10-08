"""Exact all-mixed star check using four explicitly attainable Spin(11) seeds."""
import json
from itertools import combinations
from pathlib import Path
import sympy as sp
from math import gcd
HERE=Path(__file__).parent
D=json.loads((HERE/'spin11_fullstar_blocks.json').read_text())
# Moments of |0^5> and (|0^5>+|1^h 0^(5-h)>)/sqrt(2), h=3,4,5.
# The h=1,2 two-weight seeds give the same vector as |0^5>.
SEEDS=[(1,5,5,10,10),(0,2,7,8,14),(1,1,1,14,14),(0,0,5,10,16)]
VERT=[sp.Matrix(v) for v in SEEDS]
TRACE=sp.Matrix(D['trace_coefficients'])

def prim(q):
 den=sp.ilcm(*(x.q for x in q)); z=[int(x*den) for x in q]; g=0
 for x in z:g=gcd(g,abs(x))
 return tuple(x//g for x in z)

def rays(w):
 rows=[sp.eye(5).row(i) for i in range(5)]
 rows += [(VERT[w]-VERT[j]).T for j in range(len(VERT)) if j!=w]
 out=set()
 for inds in combinations(range(len(rows)),4):
  M=sp.Matrix.vstack(*(sp.Matrix(rows[i]) for i in inds))
  if M.rank()!=4:continue
  ker=M.nullspace()
  if len(ker)!=1:continue
  q=ker[0]
  if all((row*q)[0]>=0 for row in rows):pass
  elif all((row*(-q))[0]>=0 for row in rows):q=-q
  else:continue
  out.add(prim(q))
 return out

def mat(a):return sp.Matrix([[sp.Rational(x) for x in row] for row in a])

def main():
 cones=[rays(i) for i in range(len(VERT))]; allr=set().union(*cones)
 failures=[];unknown=[]; records=[]
 for ray in sorted(allr):
  a=sp.Matrix(ray); scores=[(v.T*a)[0] for v in VERT]; support=max(scores); bound=(TRACE.T*a)[0]+support
  rec={'ray':list(ray),'seed_scores':[str(x) for x in scores],'support':str(support),'bound':str(bound),'blocks':[]}
  for key,o in D['blocks'].items():
   G=mat(o['gram']); Bs=[mat(x) for x in o['bilinear_H']]
   H=sum((a[k]*Bs[k] for k in range(5)),sp.zeros(G.rows)); gap=sp.simplify(bound*G-H)
   mins=[]
   for n in range(1,gap.rows+1):
    for ix in combinations(range(gap.rows),n):
     val=sp.factor(gap.extract(ix,ix).det());mins.append((ix,val))
   neg=[(ix,v) for ix,v in mins if v.is_negative is True]
   und=[(ix,v) for ix,v in mins if v.is_nonnegative is None]
   if neg:failures.append({'ray':ray,'block':key,'negative_minors':[(list(ix),str(v)) for ix,v in neg]})
   if und:unknown.append({'ray':ray,'block':key,'undecided_minors':[(list(ix),str(v)) for ix,v in und]})
   rec['blocks'].append({'block':key,'gap':[[str(sp.factor(gap[i,j])) for j in range(gap.cols)] for i in range(gap.rows)],'principal_minors':[{'indices_0_based':list(ix),'determinant':str(val)} for ix,val in mins],'psd':not neg and not und})
  records.append(rec)
  state='FAIL' if any(x['ray']==ray for x in failures) else ('UNDECIDED' if any(x['ray']==ray for x in unknown) else 'PASS')
  print(f'ray {ray}: support={support}, bound={bound}, blocks={len(rec["blocks"])} {state}',flush=True)
 iso=[];x=sp.symbols('x')
 for key,o in D['blocks'].items():
  G=mat(o['gram']); Bs=[mat(z) for z in o['bilinear_H']]; H=sum(Bs,sp.zeros(G.rows))
  cp=sp.factor((x*G-H).det())
  gap=1054*G-H
  bad=[]
  for n in range(1,gap.rows+1):
   for ix in combinations(range(gap.rows),n):
    q=sp.factor(gap.extract(ix,ix).det())
    if q.is_negative is True or q.is_nonnegative is None:bad.append((ix,str(q)))
  iso.append({'block':key,'charpoly':str(cp),'gap_1054_psd':not bad,'bad_minors':bad})
 status='PASS' if not failures and not unknown and all(x['gap_1054_psd'] for x in iso) else ('FAIL' if failures else 'INCOMPLETE')
 out={'status':status,'scope':'Spin(11) exact full-mixed star versus support of an attainable 4-seed canonical-EB subset',
      'seed_moments':SEEDS,'trace_coefficients':D['trace_coefficients'],'cone_ray_counts':[len(x) for x in cones],
      'cone_rays':[[list(x) for x in sorted(c)] for c in cones],'distinct_rays':len(allr),'ray_certificates':records,
      'failures':failures,'unknown':unknown,'isotropic_top':1054,'isotropic_blocks':iso,'verification_costs':{'full_triple_dimension':32768,'isotypic_swap_blocks':11,'cone_ray_checks':len(allr)*11,'principal_minor_checks':sum(len(b['principal_minors']) for rec in records for b in rec['blocks'])}}
 (HERE/'spin11_seed_support_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
 print('cone ray counts',list(map(len,cones)),'distinct',len(allr),'block-ray checks',len(allr)*11,'status',status,flush=True)
 if status=='PASS':print('CERTIFICATE PASS: all exact support-cone rays, all 11 swap/isotypic blocks, and isotropic top=1054.',flush=True)
if __name__=='__main__':main()
