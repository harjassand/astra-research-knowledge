import itertools,json
# Two identical check-basis views, deliberately permit conflicting baseline bits.
# Such a baseline is globally invalid but each local distance table is defined.
H=[1,2,3] # column binary check syndromes for a 3-qubit full-rank basis
synd=lambda x: __import__('functools').reduce(int.__xor__,(H[i] for i in range(3) if x>>i&1),0)
t={z:min(x.bit_count() for x in range(8) if synd(x)==z) for z in range(4)}
checks=0
for D in itertools.product(range(4),repeat=2):
 U=lambda y:sum(t[y^d] for d in D)
 choose=lambda y: 0 if U(y)==min(U(y^synd(f)) for f in range(8)) else next(f for f in range(8) if U(y^synd(f))==min(U(y^synd(g)) for g in range(8)))
 for y in range(4):
  f=choose(y); yy=y^synd(f)
  assert choose(yy)==0
  assert f==0 or U(yy)<U(y)
  assert abs(U(y)-2*t[y])<=3*sum(d.bit_count() for d in D)
  for g in range(8): assert abs(U(y^synd(g))-U(y))<=2*g.bit_count()
  checks+=1
print(json.dumps({'states_checked':checks,'globally_invalid_baselines_included':True,'idempotent_strict_improvement':True,'local_bandwidth':True,'original_energy_not_Hamming_example':{'syndrome':'11','local_distance':t[3],'Hamming':2}},indent=2))
