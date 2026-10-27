"""Full-spectrum rigorous improvement, with an additional stiffness budget.

All fractions, algebraic endpoint enclosures, exponential sums and positive
infinite-series remainders are rigorous. The printed decimal bounds are
outward roundings of exact rational intervals.
"""
from fractions import Fraction as Q
from pathlib import Path
from intervals import I,sqrt,isolate,full_conductance

HERE=Path(__file__).resolve().parent
mass_h,mass_b=Q(1,20),Q(19,20)
H,k=Q(5),Q(1805,99)
C=mass_h**2/H+mass_b**2/k
assert C==Q(1,20) and H+k==Q(2300,99) and H+k<24

trace0=H*(1+1/mass_h)+k*(1+1/mass_b)
pair0=2*H*k/(mass_h*mass_b)
tracepi=trace0+4
pairpi=pair0+4*(H/mass_h+k/mass_b)
detpi=4*H*k/(mass_h*mass_b)
assert [trace0,pair0]==[Q(14100,99),Q(380000,99)]
assert [tracepi,pairpi,detpi]==[Q(14496,99),Q(427200,99),Q(760000,99)]

# Exact characteristic polynomials derived from the positive star matrices.
# D0: t*(99*t^2-14100*t+380000)/99.
# Dpi: (99*t^3-14496*t^2+427200*t-760000)/99.
alpha=[I(0),isolate([99,-14100,380000],36,37),
       isolate([99,-14100,380000],106,107)]
beta=[isolate([99,-14496,427200,-760000],1,2),
      isolate([99,-14496,427200,-760000],37,38),
      isolate([99,-14496,427200,-760000],106,107)]
assert alpha[0].hi<beta[0].lo<beta[0].hi<alpha[1].lo
assert alpha[1].hi<beta[1].lo<beta[1].hi<alpha[2].lo
assert alpha[2].hi<beta[2].lo
edges=[sqrt(beta[0]),sqrt(alpha[1]),sqrt(beta[1]),sqrt(alpha[2]),sqrt(beta[2])]
J=full_conductance(edges)

# Optimized legal one-pendant comparator: k in [20,24], optimal k=20.
# Its unconstrained optimum k*=2.729... is below 20; supplied theorem proves
# j'(r)>0 beyond its unique global minimum. No grid establishes this fact.
r=sqrt(40);d=sqrt(101)
ordinary_edges=[sqrt(22-2*d),r,sqrt(22+2*d)]
Jone=full_conductance(ordinary_edges)
gain=Jone-J
assert gain.lo>Q(2449590878,10**14)
assert gain.hi<Q(2449590880,10**14)

main_edges=[sqrt(5)-1,2*sqrt(2),sqrt(5)+1]
Jmain=full_conductance(main_edges)
Jrig=full_conductance([sqrt(2)])
lines=['PASS: positive rational 3-mass/2-pendant construction.',
       f'Masses [1, {mass_h}, {mass_b}]; springs [{H}, {k}]; K=1.',
       f'Exact C_CM={C}; exact total internal stiffness={H+k}<24.',
       'Full candidate positive frequency edges (alternating stop/start):']
lines += [x.decimal() for x in edges]
lines += ['J_two '+J.decimal(), 'J_one '+Jone.decimal(),
          'J_one-J_two '+gain.decimal(),
          'Main C=1/4 optimum J '+Jmain.decimal(),
          'Rigid J '+Jrig.decimal(),
          'Main J/J_rigid '+(Jmain/Jrig).decimal(),
          'All optical bands included. No truncation without remainder.',
          'Integral computed by pi^2/6 minus positive exponential tail sums;',
          'Machin atan series, Taylor exp tails, and geometric integral tail',
          'are enclosed by exact rational interval arithmetic.']
text='\n'.join(lines)+'\n'
(HERE/'CERTIFIED_FINITE_NETWORK.txt').write_text(text)
print(text)
