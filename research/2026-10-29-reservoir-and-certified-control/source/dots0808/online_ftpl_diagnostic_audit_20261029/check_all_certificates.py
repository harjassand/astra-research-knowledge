"""Independent exact rational verification of all acquired online oracle outputs."""
import json,itertools,math
from fractions import Fraction as F
from pathlib import Path
s=Path('producer-workspace/quaternion_oracle_controller_20261029');o=Path(__file__).parent
j=json.loads((s/'online_ftpl_result.json').read_text());pairs=list(itertools.combinations_with_replacement(range(4),2));z=[]
for a,b in pairs:
 e=[0]*4;e[a]+=1;e[b]+=1;z.append(tuple(e))
exps=sorted({tuple(a+b for a,b in zip(u,v)) for u in z for v in z});norm4={}
for i in range(4):
 for k in range(4):
  e=[0]*4;e[i]+=2;e[k]+=2;norm4[tuple(e)]=norm4.get(tuple(e),0)+1
N=0;maxgap=F(0)
for call in j['oracle_calls']:
 for row in call:
  c=row['certificate'];assert c['status']=='certified' and c['method']=='rational_SOS';a=list(map(F,row['query']));G=[list(map(F,r)) for r in c['gram']];scale=F(c['gram_scale']);lo=F(c['lower']);up=F(c['upper']);q=list(map(F,c['quaternion']))
  assert sum(x*x for x in q)==1
  assert sum(v*math.prod(x**k for x,k in zip(q,e)) for e,v in zip(exps,a))==up
  got={e:F(0) for e in exps}
  for i in range(10):
   for k in range(10):
    assert G[i][k]==G[k][i]
    got[tuple(x+y for x,y in zip(z[i],z[k]))]+=scale*G[i][k]
  assert all(got[e]==v-lo*norm4.get(e,0) for e,v in zip(exps,a))
  # Independent Schur-complement positivity, no imported LDL routine.
  R=[r[:] for r in G]
  for k in range(10):
   assert R[k][k]>0
   for i in range(k+1,10):
    for h in range(i,10):R[i][h]=R[h][i]=R[i][h]-R[i][k]*R[k][h]/R[k][k]
  assert 0<=up-lo==F(c['gap'])<=F(j['requested_gap']);maxgap=max(maxgap,up-lo);N+=1
assert N==3*j['actual_source_calls']==360
(o/'all_certificate_checks.json').write_text(json.dumps({'exact_rational_certificates':N,'max_actual_gap':str(maxgap),'requested_gap':j['requested_gap'],'all_quaternions_unit_and_upper_exact':True,'all_gram_identities_and_positive_schur_pivots':True,'scope':'All360 stored finite controller calls; not hardware or an all-input fast-oracle claim'},indent=2)+'\n');print(N,float(maxgap))
