"""Exact finite witness: measured grid separation does not guarantee100W savings.
All- NO case z=0 is admitted by four-species envelope. Construct continuous
nondecreasing curves through all digitized central points; make target power gap
arbitrarily small by steep unresolved segments near500W.
"""
from pathlib import Path
from fractions import Fraction as F
import json
D=Path(__file__).resolve().parent;r=json.loads((D/'digitized.json').read_text());v={(x['configuration'],x['reported_power_W']):F.from_float(x['center_fraction']) for x in r['rows']};target=F('0.01135');assert v['intrinsic',500]<target<v['forced',500];assert v['forced',400]<target<v['intrinsic',600]
rows=[]
for e in [F(1),F(1,100),F(1,1000000)]:
 f=[(F(400),v['forced',400]),(F(500)-e,v['forced',400]),(F(500),v['forced',500]),(F(600),v['forced',600]),(F(700),v['forced',700])]
 b=[(F(400),v['intrinsic',400]),(F(500),v['intrinsic',500]),(F(500)+e,v['intrinsic',600]),(F(600),v['intrinsic',600]),(F(700),v['intrinsic',700])]
 def crossing(knots):
  assert all(y<=z for (_,y),(_,z) in zip(knots[:-1],knots[1:]))
  for (p,y),(q,z) in zip(knots[:-1],knots[1:]):
   if y<=target<=z and z>y:return p+(q-p)*(target-y)/(z-y)
 pf,pb=crossing(f),crossing(b);assert pf<500<pb
 rows.append({'epsilon_W':str(e),'forced_crossing_W_exact':str(pf),'baseline_crossing_W_exact':str(pb),'gap_W_exact':str(pb-pf),'gap_W':float(pb-pf),'forced_knots':[[str(x),str(y)] for x,y in f],'baseline_knots':[[str(x),str(y)] for x,y in b]})
out={'scope':__doc__,'target_fixedN_per_feed_mole':str(target),'witnesses':rows,'proof':'The exact power gap is a positive constant times epsilon. Hence its infimum over continuous nondecreasing data-consistent curves is0. Distinctive report-power ordering is possible, but no uniform positive savings magnitude follows from continuity/monotonicity alone. These steep curves are mathematical counterexamples, not proposed plasma response.','physical_claim':False}
(D/'ordering_proof.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
