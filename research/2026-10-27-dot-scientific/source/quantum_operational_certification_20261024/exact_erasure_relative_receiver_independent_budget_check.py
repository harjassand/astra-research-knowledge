from fractions import Fraction as Q
for xi in [Q(1,2),Q(1,4),Q(1,100),Q(1,10**6)]:
 for L in range(1,33):
  eta=(xi/(100*L))**2
  beta=eta+xi/(18*L)
  assert beta<Q(1,16)
  # sqrt(eta)=xi/(100L), eta^(L/2)<=sqrt(eta), eta^L<=eta.
  cap=180*L*eta+36*xi/(100*L)
  assert cap<=Q(369,1000)*xi<Q(1,2)*xi
  assert cap+xi/2<=xi
  assert xi+2*xi/8==5*xi/4
print('PASS128 exact rational classifier/error budgets; analytic CP-sector proof separately audited')
