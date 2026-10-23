#!/usr/bin/env python3
"""Independent high-precision arithmetic corroboration, not interval proof."""
from decimal import Decimal as D, localcontext
from fractions import Fraction
from pathlib import Path
import json,time

base=Path(__file__).resolve().parents[1]
result_path=base/'constructive_meta/RESULT.json'
if not result_path.exists():
    result_path=base/'audits/constructive_meta/RESULT.json'
saved=json.loads(result_path.read_text())
def dec_fraction(text):
    x=Fraction(text)
    return D(x.numerator)/D(x.denominator)
def contains(v, iv):
    return dec_fraction(iv['lo']) <= v <= dec_fraction(iv['hi'])
start=time.perf_counter()
with localcontext() as ctx:
    ctx.prec=100
    s=D(3).sqrt()
    pA=[D(1)/2,D(1)/6,D(1)/6,D(1)/6]
    qA=[D(1)/10,D(3)/10,D(3)/10,D(3)/10]
    pB=[D(1)/4,D(1)/4,D(1)/4+s/12,D(1)/4-s/12]
    qB=[D(1)/5,D(1)/5,D(3)/10-s/10,D(3)/10+s/10]
    entropies={name:-sum(x*x.ln() for x in xs) for name,xs in
               [('pA',pA),('qA',qA),('pB',pB),('qB',qB)]}
    for name,value in entropies.items(): assert contains(value,saved['entropy_nats'][name])
    for p,q in [(pA,qA),(pB,qB)]:
        assert all(abs(x*y-D(1)/20)<D('1e-95') for x,y in zip(p,q))
        assert abs(sum(p)-1)<D('1e-95') and abs(sum(q)-1)<D('1e-95')
    b=D(2047)/2
    a_low=b*min(entropies['pA'],entropies['qA'])
    b_low=b*min(entropies['pB'],entropies['qB'])
    separation=b_low-(a_low+D(2048).ln())
    assert separation > D(10)
    exact_supply=D(2049)/2*D(4).ln()
    assert contains(exact_supply,saved['shared_expected_exact_supply_per_copy_nats'])
    result={'status':'PASS','precision_decimal_digits':100,
      'entropies':{k:str(v) for k,v in entropies.items()},
      'separation_of_analytic_bounds_nats':str(separation),
      'expected_exact_supply_nats_per_copy':str(exact_supply),
      'scope':'Independent Decimal arithmetic corroborates the rational interval certificate; no matrix-state simulation, new capacity result or universal numerical certificate.',
      'wall_seconds':time.perf_counter()-start}
(Path(__file__).parent/'ROOT_QUEUE_ARITHMETIC.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
