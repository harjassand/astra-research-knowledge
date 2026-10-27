"""An explicit finite-decimal positive cell, strictly inside both budgets.

No transcendental tuning oracle: masses and springs are rational decimals.
Endpoints are enclosed from their exact characteristic polynomials. This is a
near-optimal feasible construction, not the exact optimal root of JOINT_PROOF.
"""
from fractions import Fraction as F
from pathlib import Path
from certify import I,band,endpoints,conductance

m2=F('0.000513557966');m1=1-m2
k1=F('19.98226783251');k2=F('0.03763216749')
C=m1*m1/k1+m2*m2/k2
kap=k1+k2
assert C<F(1,20) and kap<F('20.02')
B2=(k1+k2)*m1*m2+k1*m2+k2*m1
al_sum=B2/(m1*m2);al_prod=2*k1*k2/(m1*m2)
disc=I(al_sum*al_sum-4*al_prod).sqrt()
a1=(I(al_sum)-disc)/2;a2=(I(al_sum)+disc)/2
co=[F(1),-(B2+4*m1*m2)/(m1*m2),
    (2*k1*k2+4*(k1*m2+k2*m1))/(m1*m2),-4*k1*k2/(m1*m2)]

def poly(x):
    v=F(0)
    for c in co:v=v*x+c
    return v

def root(lo,hi):
    lo=F(lo);hi=F(hi);fl=poly(lo);fh=poly(hi)
    assert fl*fh<0
    for _ in range(210):
        md=(lo+hi)/2;fm=poly(md)
        if fl*fm<=0:hi=md;fh=fm
        else:lo=md;fl=fm
    return I(lo,hi)

b0=root(1,3);b1=root(41,44);b2=root(70,80)
assert b0.pos() and (a1-b0).pos() and (b1-a1).pos() and (a2-b1).pos() and (b2-a2).pos()
e=[b0.sqrt(),a1.sqrt(),b1.sqrt(),a2.sqrt(),b2.sqrt()]
J=band(0,e[0])+band(e[1],e[2])+band(e[3],e[4])
Jp=conductance(endpoints(40))
assert (Jp-J).pos()
lines=['# Explicit rational positive cell inside both resource caps','',
       f'backbone mass = 1',f'side mass 1 = {m1}',f'side mass 2 = {m2}',
       f'intercell spring = 1',f'side spring 1 = {k1}',f'side spring 2 = {k2}',
       f'total spring sum = {kap}',f'CM compliance exact fraction = {C}',
       '', 'The three disjoint beta-root intervals each contain a root by exact signs.',
       'A cubic has only three roots, so these intervals exhaust its full spectrum.',
       'The positive alpha roots use their exact quadratic.','']
for n,v in [('C_CM',I(C)),('compliance margin',I(F(1,20)-C)),('spring sum',I(kap)),
            ('spring margin',I(F('20.02')-kap)),('p',e[0]),('r',e[1]),('s',e[2]),('u',e[3]),('v',e[4]),
            ('J_rational_cell',J),('optimized_pendant_minus_cell',Jp-J)]:
    lines.append(n+' = '+v.fmt())
lines+=['','PASS: finite decimal parts, exact strict budget margins, full endpoint isolation,',
        'strict positive interlacing and certified all-band gain over the optimized pendant.','']
out='\n'.join(lines);Path(__file__).with_name('RATIONAL_CELL.md').write_text(out);print(out)
