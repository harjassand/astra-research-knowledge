"""Exact rational sign certificate for the phonon dual.
No floating-point sign test is used in the assertions.
"""
from fractions import Fraction as R
from decimal import Decimal, getcontext
from pathlib import Path
import json
getcontext().prec=35

def exp_bounds(x,N=80):
    x=R(x); assert x>=0 and x<N+2
    term=R(1); total=term
    for n in range(1,N+1):
        term*=x/n; total+=term
    nextterm=term*x/(N+1)
    # Successive remaining Taylor ratios are at most x/(N+2).
    return total,total+nextterm/(1-x/R(N+2))

def h_bounds(w):
    w=R(w)
    el,eu=exp_bounds(2*w)
    # E+1/E-2 strictly increases for E>1.
    den_l=el+1/el-2
    den_u=eu+1/eu-2
    return 4*w**3/den_u,4*w**3/den_l

def g_bounds(w):
    hl,hu=h_bounds(w)
    return hl/w,hu/w

h1=h_bounds(1);h2=h_bounds(2)
mu=((h1[0]-h2[1])/6,(h1[1]-h2[0])/6)
lam=((-4*h1[1]+h2[0])/3,(-4*h1[0]+h2[1])/3)
assert lam[1]<0<mu[0]

def F_bounds(w):
    w=R(w);h=h_bounds(w)
    return h[0]+lam[0]+2*mu[0]*w*w,h[1]+lam[1]+2*mu[1]*w*w

f4=F_bounds(4);f5=F_bounds(5)
assert f4[1]<0<f5[0]
clo,chi=R(17,4),R(427,100)
assert F_bounds(clo)[1]<0<F_bounds(chi)[0]
def bracket_bounds(n):
    den=(2*n+2)*(2*n+1)
    return 2*mu[0]+4*lam[0]/den,2*mu[1]+4*lam[1]/den
assert bracket_bounds(3)[1]<0<bracket_bounds(4)[0]

# Exact finite Riemann bound proves positive conductance improvement.
# c in (4.25,4.27), and cancellation leaves
# int_1^2 g - int_(c/2)^c g.
# g is decreasing; enlarge the second interval to (2.125,4.27).
N=32
lower=R(0)
for j in range(1,N+1):
    w=R(1)+R(j,N)
    lower+=g_bounds(w)[0]/N
a,b=clo/2,chi
for j in range(N):
    w=a+(b-a)*R(j,N)
    lower-=(b-a)*g_bounds(w)[1]/N
assert lower>0

def dec(x):
    return str(Decimal(x.numerator)/Decimal(x.denominator))
def bounds_dec(x): return list(map(dec,x))
out=dict(method="exact Fraction Taylor bounds; N80; geometric remainder",
         lambda_bounds=bounds_dec(lam),mu_bounds=bounds_dec(mu),
         F4_bounds=bounds_dec(f4),F5_bounds=bounds_dec(f5),
         c_coarse_bracket=[str(clo),str(chi)],
         coefficient_n3_bounds=bounds_dec(bracket_bounds(3)),
         coefficient_n4_bounds=bounds_dec(bracket_bounds(4)),
         rigorous_Jrigid_minus_Jstar_lower_bound=dec(lower),
         riemann_subintervals=N,
         status="PASS: all sign assertions and strict improvement use exact rational arithmetic")
p=Path(__file__).resolve().parent/"phonon_dual_exact_certificate.json"
p.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))

