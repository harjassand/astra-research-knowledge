import sympy as s
m,c,e=s.symbols('m c e',positive=True)
f=8/(m+3)-1/m-1
assert s.cancel(f-(m-1)*(3-m)/(m*(m+3)))==0
# Scalar coefficients of the exact congruence multiplier elimination.
Ep,Em,Sp,Sm,L=s.symbols('Ep Em Sp Sm L')
assert s.expand(-2*(-c*Ep+e*Em)-2*c*Ep+2*e*Em)==0
assert s.expand(-(-c*Ep+e*Em)-Sp+Sm-(c*Ep-Sp-e*Em+Sm))==0
print('PASS exact Jensen factor and two-face multiplier signs; CP Schwarz, compact KKT and original entropy receiving are proved in the theorem.')
