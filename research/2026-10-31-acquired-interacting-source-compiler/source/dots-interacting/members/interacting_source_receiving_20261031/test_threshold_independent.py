import copy,json,random
from fractions import Fraction as F
from acquire_threshold_source import ThresholdSource,verify_spec,ceil_log2_positive
rng=random.Random(31011120)
results={'random_models':0,'exact_columns':0,'malformed_specs':0,'dyadic_cases':0}
for trial in range(80):
 n=1+trial%5
 u=[[F(rng.randrange(1,12),rng.randrange(1,12)) for _ in range(2)] for _ in range(n)]
 e=[[[F(rng.randrange(1,12),rng.randrange(1,12)) for _ in range(2)] for _ in range(2)] for _ in range(n-1)]
 saved=copy.deepcopy((u,e));s=ThresholdSource(u,e);assert (u,e)==saved
 p=[s.probability(x) for x in range(1<<n)]
 assert sum(p)==1 and min(p)==s.pi_min
 for x in range(1<<n):
  rows=s.column(x);assert sum(v['probability'] for v in rows)==1
  forward={}
  for f,c in enumerate(s.colors): forward[s.map(f,x)]=forward.get(s.map(f,x),F(0))+c.delta/s.R
  backward={}
  for row in rows:
   backward[row['y']]=backward.get(row['y'],F(0))+row['probability']
   if row['probability']:assert s.map(row['color'],row['y'])==x
  for y in set(forward)|set(backward):assert forward.get(y,0)==backward.get(y,0)
  pp=s.first[x&1]
  for i in range(1,n):pp*=s.conditional[i-1][(x>>(i-1))&1][(x>>i)&1]
  assert pp==p[x];results['exact_columns']+=1
 for mask in range(1<<n):assert s.parity_mean(mask)==sum(p[x]*(-1 if (mask&x).bit_count()%2 else 1) for x in range(1<<n))
 rec=s.specification(range(1<<n));assert verify_spec(rec) and verify_spec(json.loads(json.dumps(rec)))
 results['random_models']+=1
s=ThresholdSource([[1,2]]*3,[[[3,2],[2,3]]]*2); rec=s.specification([0,1,7])
for key in rec:
 for v in [None,True,False,0,1,0.0,[],{},'not-canonical']:
  x=copy.deepcopy(rec);x[key]=v
  if json.dumps(x,sort_keys=True)==json.dumps(rec,sort_keys=True):continue
  if key=='parity_means' and v=={}:
   assert verify_spec(x) # valid omission of optional requested outputs, not a false value
   continue
  assert not verify_spec(x),(key,v);results['malformed_specs']+=1
for bad in [None,[],1,True,'x']:
 assert not verify_spec(bad);results['malformed_specs']+=1
for key in ['00','+0','0.0','-1','8']:
 x=copy.deepcopy(rec);x['parity_means'][key]='0';assert not verify_spec(x);results['malformed_specs']+=1
for b in range(1,250):
 for x in [F(1<<b),F((1<<b)-1),F((1<<b)+1),F((1<<b)*19-1,19),F((1<<b)*19+1,19)]:
  if x<1:continue
  l=ceil_log2_positive(x);assert 2**l>=x and (l==0 or 2**(l-1)<x);results['dyadic_cases']+=1
# Large numerical dynamic range is paid in bits, not a probability inverse loop.
s=ThresholdSource([[F(1,1<<1000),1],[1,F(1,1<<800)]],[[[1,F(1,1<<500)],[F(1,1<<300),1]]])
for x in range(4):assert sum(r['probability'] for r in s.column(x))==1
assert verify_spec(s.specification([0,1,2,3]))
results['extreme_factor_bits']=1001
# Symbolic nonadmission remains a valid law record, not a recurrence rejection.
s=ThresholdSource([[1,1]]*3,[[[100,1],[1,100]]]*2)
assert s.return_m is None and verify_spec(s.specification())
results['valid_unadmitted_record']=True
s=ThresholdSource([[1,1]]*128,[[[11,10],[10,11]]]*127)
assert len(s.colors)<=1024 and verify_spec(s.specification([0,1,(1<<128)-1]))
results['symbolic_n128']={'colors':len(s.colors),'return_m':s.return_m,'pi_min_bits':s.pi_min.denominator.bit_length()}
print(json.dumps(results,indent=2))
