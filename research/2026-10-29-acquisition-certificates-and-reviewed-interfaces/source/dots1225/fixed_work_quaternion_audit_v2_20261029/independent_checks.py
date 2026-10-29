from fractions import Fraction as F
from pathlib import Path
import sys,random,copy,json
sys.path.insert(0,str(Path(__file__).parent/'replay'))
import bounded_sos_oracle_v2 as b
import fixed_work_oracle_v2 as w
from dyadic_gap_counter import Counter
rng=random.Random(41291)
assert len(w.exps)==35 and len(w.ze)==10
identity_cases=0
for active in w.exps:
 f={e:F(e==active) for e in w.exps};G,ns=w.gram(f);assert len(ns)==20
 for e,grp in w.groups.items():
  assert sum(a*G[i][j] for i,j,a in grp)==f[e]
  assert all(sum(a*N[i][j] for i,j,a in grp)==0 for N in ns)
 identity_cases+=1
repair_cases=0
for k in range(40):
 G=[[F(0) for _ in range(10)] for _ in range(10)]
 for i in range(10):
  for j in range(i,10):G[i][j]=G[j][i]=F(rng.randrange(-100,101),rng.randrange(1,30))
 V=[[F(int(i==j)) for j in range(10)] for i in range(10)]
 if k%2:V=[[F(rng.randrange(-2,3)) for j in range(10)] for i in range(10)]
 if k==0:V=[[F(0) for _ in range(10)] for _ in range(10)]
 delta,V=b.repair(G,V)
 D=[[w.qdiag[i]*int(i==j) for j in range(10)] for i in range(10)]
 A=b.congruence(G,V);B=b.congruence(D,V)
 assert delta>=0
 assert all(B[i][i]>sum(abs(B[i][j]) for j in range(10) if j!=i) for i in range(10))
 assert all(A[i][i]+delta*B[i][i]>=sum(abs(A[i][j]+delta*B[i][j]) for j in range(10) if j!=i) for i in range(10))
 repair_cases+=1
cases=[{}, {(4,0,0,0):1}, {(4,0,0,0):F(-1,10**100)}, {e:F(rng.randrange(-4,5),3) for e in w.exps}]
for raw in cases:
 c=b.solve(raw);assert b.verify(raw,c)
 assert c['line_cholesky_slots']==2304 and c['jacobi_pair_slots']==540
 wc=w.solve(raw);assert w.verify(raw,wc)
 assert wc['objective_evaluations']==100 and wc['gram_scores']==541
rejections=[]
raw={(4,0,0,0):1};c=b.solve(raw)
for name,key,value in [('negative_scale','scale','-1'),('noncanonical_scale','scale','2'),('extra_quaternion_coordinate','quaternion',c['quaternion']+['0']),('short_gram','rational_gram',c['rational_gram'][:-1]),('short_basis','rational_basis',c['rational_basis'][:-1])]:
 cc=copy.deepcopy(c);cc[key]=value
 try:b.verify(raw,cc)
 except (AssertionError,ValueError):rejections.append(name)
 else:raise AssertionError(name)
for malformed in [{(4.,0,0,0):1},{(4,):1},{(5,-1,0,0):1}]:
 try:b.verify(malformed,c)
 except ValueError:rejections.append(str(malformed))
 else:raise AssertionError('accepted malformed exponent')
counter_cases=0
for bits in [0,1,7,39]:
 for cap in [F(0),F(2),F(340050)]:
  ctr=Counter(bits,cap);exact=F(0)
  for _ in range(100):
   gap=cap*F(rng.randrange(1001),1000);rounded=ctr.add(gap);exact+=gap
   assert gap<=rounded<=gap+F(1,2**bits)
  assert exact<=F(ctr.units,ctr.den)<=exact+F(100,2**bits)
  counter_cases+=1
out={'monomial_identity_cases':identity_cases,'repair_cases':repair_cases,'new_solver_cases_each':len(cases),'rejected_invalid_mathematical_inputs':rejections,'counter_cases_100_reports_each':counter_cases,'scope':'Exact rational mathematical checks and finite floating proposal executions; no physical measurements or clock isolation claim'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
