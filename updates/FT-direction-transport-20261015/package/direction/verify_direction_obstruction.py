"""Exact finite checks for the direction-field audit.

These check algebra, not compactness, Sobolev embeddings, lower
semicontinuity, the implicit-function theorem, or the general analytic proofs.
No numerical optimizer, prior output, or downloaded theorem is an input.
Run with Python 3 and SymPy. Output: verification.json next to this file.
"""
from __future__ import annotations
from pathlib import Path
import json
import math
import sympy as sp

ROOT = Path(__file__).resolve().parent
checks: list[dict[str, object]] = []

def zero(expr: sp.Expr) -> None:
    if sp.cancel(sp.expand(expr)) != 0:
        raise AssertionError(sp.factor(expr))

def passed(name: str, **details: object) -> None:
    checks.append({'name': name, 'status': 'PASS', **details})
    print('PASS:', name, flush=True)

# 1. Reconstruct the homogeneous vectorial Picone algebra independently.
x = sp.symbols('x0:4')
y = sp.symbols('y0:4')
monomials = []
for a in range(5):
    for b in range(5-a):
        for c in range(5-a-b):
            d = 4-a-b-c
            monomials.append(sp.prod(z**e for z,e in zip(x,(a,b,c,d))))
assert len(monomials) == 35
for f in monomials:
    grad = [sp.diff(f,z) for z in x]
    zero(sum(g*z for g,z in zip(grad,x))-4*f)
    shifted = f.subs(dict(zip(x,[z+h for z,h in zip(x,y)])), simultaneous=True)
    zero(shifted-sum(g*(z+4*h) for g,z,h in zip(grad,x,y))/4
         -(shifted-f-sum(g*h for g,h in zip(grad,y))))
passed('All-35 homogeneous Euler/Picone identities', monomials=35)

# 2. Exact lower quartic remainder used in the scalar row problem.
A,L,C = sp.symbols('A L C', nonzero=True)
zero(A+L+C-A/3 - (3*(L+4*A/3)**2/(8*A)+C-3*L**2/(8*A)))
mu,t = sp.symbols('mu t', positive=True)
d = 4*mu*t**3/3
zero(d*t-mu*t**4/3 - sp.Rational(3,4)*d*t)
passed('Rank-one quartic remainder and residual-dual constant')

# 3. Actual second variation of the circular mass-constrained energy.
k = sp.symbols('k', positive=True)
a,b,c,s = sp.symbols('a b c s', real=True)
# The n=1 mode suffices for the exact nonconvexity certificate.
rho = 1+a*c
rho_y = -a*s
phase_y = k+b*c
integrand = rho*phase_y**4 + rho_y**2*phase_y**2/(8*rho) + rho_y**4/(256*rho**3)

def avg_circle(poly: sp.Expr) -> sp.Expr:
    result = sp.Integer(0)
    for (i,j),coef in sp.Poly(sp.expand(poly), c,s).terms():
        if i % 2 or j % 2:
            continue
        h,l = i//2,j//2
        moment = sp.Rational(math.factorial(2*h)*math.factorial(2*l),
                             4**(h+l)*math.factorial(h)*math.factorial(l)*math.factorial(h+l))
        result += coef*moment
    return sp.simplify(result)
H = sp.Matrix(2,2,lambda i,j:avg_circle(sp.diff(integrand,[a,b][i],[a,b][j]).subs({a:0,b:0})))
assert H == sp.Matrix([[k*k/8,2*k**3],[2*k**3,6*k*k]])
reduced = sp.factor(H[1,1]-H[1,0]**2/H[0,0])
assert sp.simplify(reduced-(6*k*k-32*k**4)) == 0
assert reduced.subs(k,1) == -26
passed('Genuine density/phase Hessian and eliminated n=1 mode',
       Hessian=str(H), reduced=str(reduced), at_k_1=-26)

# 4. General p quadratic form and square completion (all coefficients symbolic).
p = sp.symbols('p', positive=True)
zprime,theta,theta_prime = sp.symbols('zprime theta theta_prime', real=True)
Q = k**(p-2)/p*zprime**2 - 2*p*k**(p-1)*zprime*theta + p*(p-1)*k**(p-2)*theta_prime**2
Qsplit = k**(p-2)/p*(zprime-p**2*k*theta)**2 + p*(p-1)*k**(p-2)*theta_prime**2-p**3*k**p*theta**2
zero(Q-Qsplit)
passed('General-p reduced spectral square completion')

# 5. Rigorous rational trial upper bound, with positive density.
e = sp.Rational(1,100)
dmin = 1-16*e
assert dmin == sp.Rational(21,25)
first = avg_circle((1-16*e*c)*(1+e*c)**4)
assert first == 1-29*e**2-sp.Rational(189,8)*e**4
second_num = avg_circle(32*e**2*(1-c*c)*(1+e*c)**2)
third_num = avg_circle(256*e**4*(1-c*c)**2)
assert second_num == 16*e**2+4*e**4
assert third_num == 96*e**4
upper = first+second_num/dmin+third_num/dmin**3
assert upper == sp.Rational(2467145694157,2469600000000)
assert upper < 1
passed('Exact amplitude-minimized nonconvexity upper certificate',
       epsilon=str(e), density_lower=str(dmin), upper=str(upper),
       strict_deficit=str(1-upper))

# 6. Optional exact value of that trial: not the minimized value.
z = sp.symbols('z'); amp=16*e; cc=(1-z)/amp
trial = sp.expand(z*(1+e*cc)**4+32*e**2*(1-cc*cc)*(1+e*cc)**2/z
                  +256*e**4*(1-cc*cc)**2/z**3)
moment={-1:1/sp.sqrt(1-amp*amp),
        -2:(1-amp*amp)**(-sp.Rational(3,2)),
        -3:(2+amp*amp)/(2*(1-amp*amp)**sp.Rational(5,2))}
for j in range(6):
    moment[j]=sum(sp.binomial(j,2*h)*amp**(2*h)*sp.Rational(math.comb(2*h,h),4**h)
                  for h in range(j//2+1))
exact=0
for term in sp.Add.make_args(trial):
    power=int(term.as_powers_dict().get(z,0))
    exact += term/z**power*moment[power]
exact = sp.simplify(exact)
assert sp.simplify(exact-(sp.Rational(225257609,200000000)-sp.Rational(53731,10393600)*sp.sqrt(609))) == 0
passed('Exact trial energy, distinguished from the global minimum', value=str(exact))

# 6b. A genuinely two-dimensional phase example, minimized over all amplitudes.
# theta=y+e sin(x+y), rho=1-8e cos(x+y).
e2 = sp.Rational(1,100)
d2 = 1-8*e2
assert d2 == sp.Rational(23,25)
K2=1+2*e2*c+2*e2**2*c*c
first2=avg_circle((1-8*e2*c)*K2**2)
second2=avg_circle(16*e2**2*(1-c*c)*K2)
third2=avg_circle(64*e2**4*(1-c*c)**2)
assert first2==1-12*e2**2-sp.Rational(45,2)*e2**4
assert second2==8*e2**2+4*e2**4 and third2==24*e2**4
upper2=first2+second2/d2+third2/d2**3
assert upper2==sp.Rational(486519245657,486680000000) and upper2<1
# Fourier-mode quadratic form for k=(0,1), frequency=(1,1).
rho2=1+a*c
kappa2=1+2*b*c+2*b**2*c**2
grad_rho2_sq=2*a**2*s**2
integrand2=rho2*kappa2**2+grad_rho2_sq*kappa2/(8*rho2)+grad_rho2_sq**2/(256*rho2**3)
H2=sp.Matrix(2,2,lambda i,j:avg_circle(sp.diff(integrand2,[a,b][i],[a,b][j]).subs({a:0,b:0})))
assert H2==sp.Matrix([[sp.Rational(1,4),2],[2,8]])
assert H2[1,1]-H2[1,0]**2/H2[0,0]==-8
# Independently integrate the same rational trigonometric trial exactly.
amp2=8*e2
cz=(1-z)/amp2
kz=1+2*e2*cz+2*e2**2*cz**2
expr2=sp.expand(z*kz**2+16*e2**2*(1-cz*cz)*kz/z+64*e2**4*(1-cz*cz)**2/z**3)
mom2={-1:1/sp.sqrt(1-amp2*amp2),
      -2:(1-amp2*amp2)**(-sp.Rational(3,2)),
      -3:(2+amp2*amp2)/(2*(1-amp2*amp2)**sp.Rational(5,2))}
for j in range(6):
    mom2[j]=sum(sp.binomial(j,2*h)*amp2**(2*h)*sp.Rational(math.comb(2*h,h),4**h)
                for h in range(j//2+1))
exact2=0
for term in sp.Add.make_args(expr2):
    power=int(term.as_powers_dict().get(z,0))
    exact2 += term/z**power*mom2[power]
exact2=sp.simplify(exact2)
assert sp.simplify(exact2-(sp.Rational(50880491,40000000)-sp.Rational(7241,220800)*sp.sqrt(69)))==0
passed('Two-dimensional compatible reduced-energy nonconvexity certificate',
       epsilon=str(e2), density_lower=str(d2),
       upper=str(upper2), strict_deficit=str(1-upper2),
       exact_trial=str(exact2), eliminated_second_variation=-8)

# 7. Boundary-preserving translation chart and its actual gradient.
R,h,g,v = sp.symbols('R h g v', real=True)
gx,gy,hx,hy,vx,vy = sp.symbols('gx gy hx hy vx vy', real=True)
denom=R+g
q=v/denom
qx=vx/denom-v*gx/denom**2
qy=vy/denom-v*gy/denom**2
# u_R=(R+g+h, v+h*v/(R+g)).
second=v+h*q
for derivative, gv,hv,vv,expected in [
    ('x',gx,hx,vx,vx+q*hx+h*qx),
    ('y',gy,hy,vy,vy+q*hy+h*qy)]:
    actual=sp.diff(second,g)*gv+sp.diff(second,h)*hv+sp.diff(second,v)*vv
    zero(actual-expected)
assert second.subs(h,0) == v
# Parallelism with direction (R+g,v) is exact.
zero((R+g+h)*v-second*(R+g))
passed('Exact compatible translation chart, direction, and affine-boundary matching')

# 8. Every quartic energy perturbation is divisible by the small row error.
tau = sp.symbols('tau'); e0,e1=sp.symbols('e0 e1')
for f in monomials:
    shifted=f.subs({x[2]:x[2]+tau*e0,x[3]:x[3]+tau*e1},simultaneous=True)
    diff=sp.Poly(sp.expand(shifted-f),tau)
    assert diff.nth(0)==0 and diff.degree()<=4
passed('All-35 translation-chart polynomial error identities')

# 9. Fixed-fourth-mass constraint becomes a mean constraint.
a0,aref,eps = sp.symbols('a0 aref eps', real=True)
scaled_mass=(1+eps*a0)**4*(1+eps**2*v**2/(1+eps*g)**2)**2
scaled_ref=scaled_mass.subs(a0,aref)
series=sp.series((scaled_mass-scaled_ref)/(4*eps),eps,0,2).removeO().expand()
zero(series-(a0-aref+sp.Rational(3,2)*eps*(a0*a0-aref*aref)))
passed('Exact large-translation mass expansion', series=str(series))

# 10. Difference of radial variations at translated centers gives a Cartesian test.
u1,u2,eta,c1,c2,d1,d2 = sp.symbols('u1 u2 eta c1 c2 d1 d2')
rad1=sp.Matrix([eta*(u1+c1),eta*(u2+c2)])
rad0=sp.Matrix([eta*(u1+d1),eta*(u2+d2)])
assert sp.simplify(rad1-rad0-eta*sp.Matrix([c1-d1,c2-d2])) == sp.zeros(2,1)
passed('Translation-center stationarity identity')

# 11. The finite Schur square completion underlying the operator statement.
AA,CC,DD,xx,yy=sp.symbols('AA CC DD xx yy', nonzero=True)
zero(AA*xx**2+2*CC*xx*yy+DD*yy**2
     -(AA*(xx+CC*yy/AA)**2+(DD-CC**2/AA)*yy**2))
passed('Schur/inertia algebra; no positivity of the reduced block asserted')

payload={'status':'PASS','groups':len(checks),'checks':checks,
         'limits':'Finite algebra only. Analytic minimizer existence, spectral implicit function theorem, uniform energy bounds, compactness and all general variational claims require the written proofs. No negative quasiconvexity test is claimed.'}
(ROOT/'verification.json').write_text(json.dumps(payload,indent=2))
print(json.dumps({'status':'PASS','groups':len(checks)},indent=2))
