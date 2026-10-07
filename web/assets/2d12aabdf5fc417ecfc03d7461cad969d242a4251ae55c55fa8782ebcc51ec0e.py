"""Exact rational closure certificate for the final sel:exponents contradiction."""
from fractions import Fraction as F

eps=F(1,100000)
beta=F(29,25)
# From b < H-alpha+Delta and near selection:
# dstar=alpha+b+y+H < 2H+y+Delta < 4z+5Delta.
# Hence Delta/z < 4eps/(1-5eps), and z>0 on a strictly selected unsafe bin.
delta_bar=4*eps/(1-5*eps)
# In H<=2c, far-energy and first unsafe inequality yield H+z+6alpha<8Delta.
assert 8*delta_bar<1
# In H>2c they instead yield H>z/2+3(alpha+c)-4Delta.
H_lower=F(1,2)-4*delta_bar
# Provided improved occupation is applicable, its far inequality and first unsafe
# inequality imply beta*y>H/3+z/3-(8/3)Delta. Near selection gives
# beta*y<(beta/2)(z+Delta)-beta*H/4 after dropping nonnegative alpha.
H_upper=((beta/F(2)-F(1,3))+(beta/F(2)+F(8,3))*delta_bar)/(F(1,3)+beta/F(4))
assert H_upper<H_lower
print('Delta/z bound:',delta_bar)
print('First energy branch impossible because 8*Delta/z <',8*delta_bar,'< 1')
print('Second branch H/z lower bound:',H_lower)
print('With improved occupation H/z upper bound:',H_upper)
print('Exact positive contradiction margin:',H_lower-H_upper)
print('Scope: final rational exponent contradiction once the improved-occupation window is established; no continuum occupation estimate is certified.')
