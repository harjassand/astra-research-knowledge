if not __debug__:
    raise RuntimeError("Run without -O / PYTHONOPTIMIZE; validation assertions are required")
from fractions import Fraction as Q
import math,re
import exact_intervals as c
u=Q(1,2**53)
s=open('coefficients.h').read();cs=re.findall(r'0x[0-9a-f.]+p[+-]\d+',s);assert len(cs)==53
refs=[Q(2,2*j+1) for j in range(20)]+[Q(1,math.factorial(j)) for j in range(33)]
for st,q in zip(cs,refs):assert abs(Q(float.fromhex(st))-q)<=u*q
l2=c.logpoint(2);l=Q(float.fromhex('0x1.62e42fefa39efp-1'));assert max(abs(l-Q(l2.l,c.S)),abs(l-Q(l2.h,c.S)))<u
assert Q(2,3**41)/(41*Q(8,9))<Q(2,10**21)
assert Q(2,2**33*math.factorial(33))<Q(3,10**47)
e=Q(13,10**15)
for k in range(7):e=(2+e)*e+u*(1+e)**2
assert e<Q(2,10**12)
assert 5000*2**48<2**64
print('Exact coefficient, remainder, squaring-error and accumulator checks passed.')
