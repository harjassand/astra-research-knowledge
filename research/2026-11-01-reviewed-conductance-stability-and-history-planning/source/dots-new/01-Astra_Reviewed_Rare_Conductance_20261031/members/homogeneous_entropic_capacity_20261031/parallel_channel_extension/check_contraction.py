from fractions import Fraction as F
from pathlib import Path
import json, random, hashlib
rng=random.Random(20261031);checks=0
for k in [F(1,10000),F(1,10),F(1),F(10),F(10000)]+[F(rng.randrange(1,1000),rng.randrange(1,1000)) for _ in range(200)]:
 a=1+k;d=7*k/(16*a);eta2=7/(8*(1+d))
 assert 0<eta2<1;checks+=1
 assert 1/eta2==(16+23*k)/(14*(1+k));checks+=1
 assert 1/eta2<=F(23,14);checks+=1
 for j in range(101):
  y=F(j,200);delta=k*y*y*(2-y*y);contracted=k*eta2*y*y*(2-eta2*y*y)
  assert delta/a<=d;checks+=1
  assert contracted<=delta/(1+d)<=delta/(1+delta/a);checks+=1
  assert 1-contracted/a>=1/(1+delta/a);checks+=1
p=Path(__file__).with_name('PARALLEL_CHANNEL_CANDIDATE.md')
out={'status':'PASS','exact_rational_checks':checks,'scope':'pointwise contraction inequalities only, not independent whole proof','proof_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
Path(__file__).with_name('contraction_checks.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
