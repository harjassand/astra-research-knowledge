"""Exact rational checks for the strongly-endotactic local inward certificate.
No simulation and no claim to verify N35's probability theorem.
"""
from fractions import Fraction as F

q = F(101,100)
eps = F(1,10000)
ell = eps/F(1000)
gamma = F(4,5)*eps

# Conservative absolute Hessian bounds on [.99,1.01]^2.
hessian_bounds = [20*q+144*q**6, 20*q+192*q**6, 144*q**6,
                  30*q+192*q**6, 30*q+256*q**6, 192*q**6]
assert max(hessian_bounds) < 310

# Expanded ambient collars, including ell in each tangential direction.
umax = F(7,5)*eps+ell
vmax = eps+ell
remainder = F(310,2)*(umax+vmax)**2
upper_a = -F(6,5)*eps+66*ell+remainder
upper_b = -F(7,5)*eps+83*ell+remainder
assert upper_a <= -gamma
assert upper_b <= -gamma
assert F(1)-umax > 0 and F(1)-vmax > 0
assert F(1)-umax > F(99,100) and F(1)+umax < q
assert F(1)-vmax > F(99,100) and F(1)+vmax < q
print('PASS: exact ambient collar drift bounds')
print('epsilon=',eps,'ell=',ell,'gamma=',gamma)
print('max Hessian conservative bound=',max(hessian_bounds))
print('remainder / epsilon=',remainder/eps)
print('upper a drift / epsilon=',upper_a/eps)
print('upper b drift / epsilon=',upper_b/eps)
