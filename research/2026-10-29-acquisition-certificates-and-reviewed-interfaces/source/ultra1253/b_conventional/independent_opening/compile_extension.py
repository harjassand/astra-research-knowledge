"""Exact algebra/global majorants plus a finite analytic evaluator.

One compatible analytic input family, two equally informed constructions.
No dynamics, sampled Hessian proof, isometry oracle or physical data.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import time

START = time.perf_counter()
import sympy as s
import mpmath as mp

HERE = Path(__file__).resolve().parent
x, y, z, d, u = s.symbols("x y z delta u", real=True)
coords = (x, y, z)
zz = s.symbols("zz", nonzero=True)
I = s.I


def rat_string(a):
    a = s.Rational(a)
    return str(a.p) if a.q == 1 else f"{a.p}/{a.q}"


def factorial_majorant(poly):
    p = s.Poly(s.expand(poly), u)
    assert all(c >= 0 for c in p.all_coeffs())
    return sum(c * s.factorial(k[0]) for k, c in p.terms())


def extension_bound(delta):
    """Literal Eq(11)--(14), with rational overpayments throughout."""
    delta = s.Rational(delta)
    M = 4 + 4 * delta
    F = 17 * delta**2 / 4
    U, U1 = 34 * delta**2, 128 * delta**2
    assert 0 < U < 1
    G = (12 * delta + (4 + 16 * delta) * U / (1 - U)
         + (4 + 8 * delta) * U1 / (2 * (1 - U)**2))
    cs = [s.factorial(j) * 128**j for j in range(4)]
    Fs = [cs[j] * F for j in range(3)]
    As = [cs[j] * G + cs[j + 1] * F for j in range(3)]
    R1, R2 = 1 + cs[1] * M, cs[2] * M
    b0 = Fs[0] + u * As[0]
    db = Fs[1] + R1 * As[0] + u * As[1]
    ddb = Fs[2] + R2 * As[0] + 2 * R1 * As[1] + u * As[2]
    b1 = db + 2 * R1 * u * b0
    b2 = ddb + 4 * R1 * u * db + (4 * R1**2 * u**2 + 2 * R1**2 + 2 * R2 * u) * b0
    v = u + M
    p0, p1, p2 = 2 * v**2 + v**4, 4 * v + 4 * v**3, 4 + 12 * v**2
    H = s.Poly(s.expand(p0 * b2 + 2 * p1 * b1 + p2 * b0), u)
    assert H.degree() <= 7
    return factorial_majorant(H.as_expr()), (M, F, G), H


def laurent_dict(expr):
    expr = s.expand(expr)
    ans = {}
    for term in s.Add.make_args(expr):
        k = int(term.as_powers_dict().get(zz, 0))
        c = s.simplify(term / zz**k)
        ans[k] = s.simplify(ans.get(k, 0) + c)
    return {k: v for k, v in ans.items() if v != 0}


# Acquire the entire finite rational source family and compatibility, not
# just a numerical trajectory or a pre-supplied force table.
Q = s.Matrix([x, y, d * (x*x-y*y)])
Qp = s.Matrix([-y, x, -4*d*x*y])
Qpp = s.Matrix([-x, -y, -4*d*(x*x-y*y)])
v2 = 1 + 16*d*d*x*x*y*y
v2p = 32*d*d*x*y*(x*x-y*y)
A = Qpp/v2-Qp*v2p/(2*v2*v2)
g = -A-Q
f = -d*d*(x*x-y*y)**2/2
df = s.Matrix([s.diff(f, a) for a in coords])

# Circle reduction checks are exact polynomial division by x^2+y^2-1.
circle = s.Poly(x*x+y*y-1, x, y, z, d)
compat_num = s.together((Qp.dot(g)-df.dot(Qp))).as_numer_denom()[0]
assert s.rem(s.Poly(compat_num,x,y,z,d), circle).is_zero
assert s.rem(s.Poly(s.together(Qp.dot(Qp)-v2).as_numer_denom()[0],x,y,z,d), circle).is_zero

# Strong ordinary construction: a real-algebraic defining ideal directly
# supplies conormals; all global rational denominators remain >=1.
res1, res2 = x*x+y*y-1, z-d*(x*x-y*y)
g1 = g-df
beta = g1[2]
alpha = (x*g1[0]+y*g1[1]+2*d*(x*x-y*y)*beta)/2
Braw = f+alpha*res1+beta*res2
for j in range(3):
    err = s.together(s.diff(Braw,coords[j])-g[j]).as_numer_denom()[0]
    err = s.rem(s.Poly(err,z,x,y,d),s.Poly(res2,z,x,y,d)).as_expr()
    assert s.rem(s.Poly(err,x,y,d),s.Poly(res1,x,y,d)).is_zero

origin_factor = 2*(x*x+y*y)-(x*x+y*y)**2
BB = s.cancel(origin_factor*Braw)
SS = res1**2+res2**2
S1 = [s.diff(SS, a) for a in coords]
ordinary_entry_constants = []
for i in range(3):
    row=[]
    for j in range(3):
        hh = s.cancel(s.diff(BB,coords[i],coords[j])
                      -s.diff(BB,coords[i])*S1[j]
                      -s.diff(BB,coords[j])*S1[i]
                      +BB*(S1[i]*S1[j]-s.diff(SS,coords[i],coords[j])))
        num, den = s.fraction(hh)
        # SymPy's cancelled denominator is a positive constant times
        # v2^p; prove that exact factorization, rather than guessing it.
        factors = s.factor_list(den)
        den_constant = factors[0]
        assert den_constant > 0
        for fac, exponent in factors[1]:
            assert s.expand(fac-v2)==0 and exponent >= 0
        major=0
        for powers, coeff in s.Poly(num,x,y,z,d).terms():
            ax, ay, az, ad = powers
            assert ad >= 1  # retained cancellation at delta=0 is essential
            major += abs(coeff/den_constant)*(3*u+2)**(ax+ay+az)
        row.append(factorial_majorant(major))
    ordinary_entry_constants.append(row)
Cordinary = max(sum(row) for row in ordinary_entry_constants)

# Select one literal source from the declared family. This is a constructor
# smallness gate, not a native-model parameter grid or statistical scan.
bits = max(8, int(Cordinary.p).bit_length()+20)
delta = s.Rational(1,2**bits)
ours, native_bounds, H = extension_bound(delta)
assert d not in ours.free_symbols
assert ours < s.Rational(1,100)
assert delta * Cordinary < s.Rational(1,100)

# Finite numerator for g(z)/v2(z)^2, using a single Laurent variable.
cx=(zz+zz**-1)/2
sy=(zz-zz**-1)/(2*I)
sub={x:cx,y:sy,d:delta}
numerators=[laurent_dict(s.expand((-Qpp[i]*v2+Qp[i]*v2p/2-Q[i]*v2*v2).subs(sub))) for i in range(3)]


def mprat(a):
    a=s.Rational(a)
    return mp.mpf(int(a.p))/mp.mpf(int(a.q))


def mpcomplex(a):
    return mp.mpc(mprat(s.re(a)), mprat(s.im(a)))


def shifted_ray(k, Z, Zbar, rr, aa, bb):
    """E[z^k/v2^2], positive/negative geometric rays, no Fourier cutoff."""
    N=max(0, (-k+3)//4)
    ans=mp.mpc(0)
    for m in range(N):
        ans+=rr**m*(aa+bb*m)*Zbar**(-k-4*m)
    t=rr*Z**4
    ans+=rr**N*Z**(k+4*N)*((aa+bb*N)/(1-t)+bb*t/(1-t)**2)
    NN=max(1,(k+3)//4)
    for m in range(1,NN):
        ans+=rr**m*(aa+bb*m)*Z**(k-4*m)
    t=rr*Zbar**4
    ans+=rr**NN*Zbar**(4*NN-k)*((aa+bb*NN)/(1-t)+bb*t/(1-t)**2)
    return ans


mp.mp.dps=max(160,bits//3+70)
dd=mprat(delta)
root=mp.sqrt(1+4*dd*dd)
rr=2*dd*dd/(1+2*dd*dd+root)
cc=(1+2*dd*dd+root)/2
aa=(1+rr*rr)/(cc*cc*(1-rr*rr)**3)
bb=1/(cc*cc*(1-rr*rr)**2)
assert 0 < rr < 1
num_mp=[{k:mpcomplex(c) for k,c in p.items()} for p in numerators]


def candidate(xx, yy, z3):
    w=mp.mpc(xx,yy)
    ee=mp.exp((1-xx*xx-yy*yy)/2)
    Z=w*ee
    Zbar=mp.conj(Z)
    eq=[mp.re(Z),mp.im(Z),dd*mp.re(Z*Z)]
    ef=-dd*dd*(1+mp.re(Z**4))/4
    jx=ee*mp.mpc(1-xx*xx,-xx*yy)
    jy=ee*mp.mpc(-xx*yy,1-yy*yy)
    gradf=[-dd*dd*mp.re(Z**3*jx),-dd*dd*mp.re(Z**3*jy),mp.mpf(0)]
    eg=[]
    for co in num_mp:
        val=sum(c*shifted_ray(k,Z,Zbar,rr,aa,bb) for k,c in co.items())
        assert abs(mp.im(val)) < mp.mpf(10)**(-mp.mp.dps+15)
        eg.append(mp.re(val))
    rv=[xx-eq[0],yy-eq[1],z3-eq[2]]
    av=[eg[j]-gradf[j] for j in range(3)]
    rad=xx*xx+yy*yy
    W=(2*rad-rad*rad)*mp.exp(-sum(a*a for a in rv))*(ef+sum(rv[j]*av[j] for j in range(3)))
    return (xx*xx+yy*yy+z3*z3)/2+W


ordinary_fn=s.lambdify((x,y,z,d),(x*x+y*y+z*z)/2+s.exp(-SS)*BB,"mpmath",cse=True)
source_point=[mp.mpf(3)/5,mp.mpf(4)/5,-7*dd/25]
force_fn=s.lambdify((x,y,d),-A,"mpmath",cse=True)
force=force_fn(source_point[0],source_point[1],dd)
ours_grad=[mp.diff(lambda t:candidate(*(source_point[:j]+[t]+source_point[j+1:])),source_point[j]) for j in range(3)]
ordinary_grad=[mp.diff(lambda t:ordinary_fn(*(source_point[:j]+[t]+source_point[j+1:]),dd),source_point[j]) for j in range(3)]
err=max(abs(ours_grad[j]-force[j]) for j in range(3))
err_ord=max(abs(ordinary_grad[j]-force[j]) for j in range(3))
assert err < mp.mpf(10)**(-mp.mp.dps//2)
assert err_ord < mp.mpf(10)**(-mp.mp.dps//2)
assert abs(candidate(*source_point)-mp.mpf(1)/2) < mp.mpf(10)**(-mp.mp.dps//2)

point=[mp.mpf(1)/3,mp.mpf(2)/5,mp.mpf(1)/7]
source_output={
    "status":"EXACT_COMPATIBILITY_AND_GLOBAL_CONVEXITY_GATES_PASS",
    "scope":"One entire declared input family symbolically qualified; one literal finite-expression analytic potential and equally informed ordinary potential evaluated. No universal simulator, isometry or dynamics executed.",
    "delta":"1/2^"+str(bits),
    "eta":"1/100",
    "source_dimension":1,"configuration_dimension":3,
    "exact_checks":["Laurent/circle unit-speed identity","Cleared compatible value/force jets","Ordinary defining-equation jets","Positive global denominator factorization","Numerator vanishes to delta order for every ordinary Hessian entry","Positive-coefficient Gaussian bounds for both whole-space Hessians"],
    "global_hessian_bounds":{
        "fourier_constructor":rat_string(ours),
        "fourier_decimal_display":str(s.N(ours,15)),
        "ordinary_defining_equations":rat_string(delta*Cordinary),
        "ordinary_decimal_display":str(s.N(delta*Cordinary,15)),
        "ordinary_unit_delta_constant_bits":int(Cordinary.p).bit_length(),
        "fourier_majorant_degree":H.degree()},
    "native_norm_bounds":dict(zip(["Q","f","g"],[rat_string(v) for v in native_bounds])),
    "finite_expression":{"special_operations":["one positive algebraic square root","exponential","rational operations"],"rays_per_component":[2*len(c) for c in numerators],"numerator_monomials":[len(c) for c in numerators],"global_real_denominator_floor":"1-r > 0; no pole on real input"},
    "numerical_diagnostics_only":{
        "mpmath_decimal_precision":mp.mp.dps,
        "source_circle_coordinates":["3/5","4/5","-7 delta/25"],
        "candidate_value_error":mp.nstr(abs(candidate(*source_point)-mp.mpf(1)/2),12),
        "candidate_force_error":mp.nstr(err,12),
        "ordinary_force_error":mp.nstr(err_ord,12),
        "off_curve_point":["1/3","2/5","1/7"],
        "candidate_off_curve_value":mp.nstr(candidate(*point),70),
        "ordinary_off_curve_value":mp.nstr(ordinary_fn(*point,dd),70)},
    "random_draws":0,"trajectory_steps":0,
    "execution_seconds_including_imports":time.perf_counter()-START,
    "compiler_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "priority":"UNKNOWN","physical_acquisition":"NOT_PERFORMED",
    "practical_or_trajectory_advantage":"NOT_ESTABLISHED"}
(HERE/'RESULT.json').write_text(json.dumps(source_output,indent=2)+"\n")
print(json.dumps({"status":source_output["status"],"delta":source_output["delta"],"bounds":[source_output["global_hessian_bounds"]["fourier_decimal_display"],source_output["global_hessian_bounds"]["ordinary_decimal_display"]],"seconds":source_output["execution_seconds_including_imports"]},indent=2))
