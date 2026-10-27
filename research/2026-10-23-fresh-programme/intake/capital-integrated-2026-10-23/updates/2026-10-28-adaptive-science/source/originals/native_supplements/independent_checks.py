"""Independent algebra/law checks; all numerical integrations are diagnostics.

No programme state, other chat, live producer or external scientific source is
read. Packet functions are imported only to count/test the actual interfaces.
"""
from pathlib import Path
from fractions import Fraction as F
import contextlib
import csv
import importlib.util
import io
import json
import math
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "deps"))
import numpy as np
import scipy
import sympy as sp
from scipy.integrate import quad
from numpy.polynomial.hermite_e import hermegauss
from numpy.polynomial.legendre import leggauss

results = {}

def module_at(label, rel):
    spec = importlib.util.spec_from_file_location(label, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[label] = mod
    spec.loader.exec_module(mod)
    return mod

def gaussian_rule(n):
    x, w = hermegauss(n)
    return x, w / math.sqrt(2 * math.pi)

# Independently differentiate u; do not start from the packet residual formula.
x, z, mu = sp.symbols("x z mu", real=True)
K, h, S = sp.Function("K")(x), sp.Function("h")(x), sp.Function("S")(x, z)
u = S * (h + z - mu) - K * sp.diff(S, x) - sp.diff(S, z)
residual = K * sp.diff(u, x) + sp.diff(u, z) + S * (1 + K * sp.diff(h, x)) + K * sp.diff(h, x)
residual = residual.subs(sp.diff(K, x), x * K - (h - mu))
expected = (2*S + z*sp.diff(S,z) - sp.diff(S,z,2)
            + (1+2*S)*K*sp.diff(h,x)
            + K*(z*sp.diff(S,x)-2*sp.diff(S,x,z))
            + 2*sp.diff(S,x)*K*(h-mu)
            - (x*sp.diff(S,x)+sp.diff(S,x,2))*K**2
            + sp.diff(S,z)*(h-mu))
assert sp.expand(residual - expected) == 0
results["full_scalar_residual_independent_differentiation"] = "PASS"

# A genuinely nonsymmetric form still has the required energy identity.
tau = sp.Matrix([[2, 1], [0, 2]])
Sm = sp.Matrix([[1, 2], [2, -1]])
Tm = sp.Matrix([[0, 1], [1, 1]])
inner = lambda A, B: sp.trace(A.T * B)
assert inner(Sm*tau, Sm) == sp.trace(Sm**2*(tau+tau.T)/2)
asymmetry = inner(Sm*tau, Tm) - inner(Tm*tau, Sm)
assert asymmetry != 0
assert inner(Sm*tau, Sm) >= F(3,2)*inner(Sm, Sm)
results["nonsymmetric_form_example"] = {"antisymmetric_difference": int(asymmetry), "coercive_energy": int(inner(Sm*tau,Sm))}

# Independently reconstruct the unnormalized finite-chaos inverse and its norms.
chaos_cases = 0
for lam, a in [(F(3,5),F(4,5)), (F(5,13),F(12,13))]:
    for n in range(121):
        coeff = [-1/(2*a)]
        for j in range(1,n+1):
            coeff.append(-lam*(n-j+1)*coeff[-1]/(a*(j+2)))
        assert coeff == [-(-lam/a)**j*F(math.comb(n,j),(j+1)*(j+2))/a for j in range(n+1)]
        weights = [F(math.factorial(n-j)*math.factorial(j),math.factorial(n)) for j in range(n+1)]
        nj = sum(c*c*w for c,w in zip(coeff,weights))
        nd = sum(c*c*w*(j+1)**2 for j,(c,w) in enumerate(zip(coeff,weights)))
        assert nj >= a**(-2*n-2)/((n+1)**2*(n+2)**2)
        assert nd >= a**(-2*n-2)/(n+2)**2
        assert a**(2*n)*nd <= 1/(4*a*a)
        chaos_cases += 1
results["exact_chaos_cases_two_distinct_channels"] = chaos_cases

# Nonconstant legal scalar source, arbitrary S, and full weak cancellation with
# the residual term retained. This tests the complete formula, not a fitted basis.
xx, zz = sp.symbols("xx zz", real=True)
kk = F(1,5)*xx/(1+xx**2)
hh = F(1,5)*(1-2/(1+xx**2)**2)
ss = F(1,100)*(1+xx*zz+zz**2)
mm = hh+zz
uu = ss*mm-kk*sp.diff(ss,xx)-sp.diff(ss,zz)
rr = kk*sp.diff(hh,xx)
ee = sp.simplify(kk*sp.diff(uu,xx)+sp.diff(uu,zz)+ss*(1+rr)+rr)
# f(y)=y^4/4+3y^2/2, Lf=y^4-3, f''=3y^2+3, f'''=6y.
integrand = mm**4-3+4*mm**3*uu-ee*(3*mm**2+3)-rr*6*mm*uu
fn = sp.lambdify((xx,zz),integrand,"numpy")
weak_errors = []
for order in (80,128,192):
    nodes, weights = gaussian_rule(order)
    weak_errors.append(float(weights @ fn(nodes[:,None],nodes[None,:]) @ weights))
results["nonconstant_weak_cancellation_GH_residuals"] = weak_errors
# The first reviewer run used an over-tight GH192 tolerance for a rational
# integrand with poles at +/-i. Preserve that failure in logs; integrate Z
# exactly and use adaptive one-dimensional quadrature instead of silently
# treating GH stability as a certificate.
z_integrated = sum(coef * (sp.factorial2(degree[0]-1) if degree[0] else 1)
                   for degree,coef in sp.Poly(sp.cancel(integrand),zz).terms()
                   if degree[0] % 2 == 0)
g_only = sp.lambdify(xx,z_integrated,"numpy")
adaptive_value,adaptive_error = quad(lambda t: float(g_only(t))*math.exp(-t*t/2)/math.sqrt(2*math.pi),
                                     -np.inf,np.inf,epsabs=2e-12,limit=300)
assert abs(adaptive_value) < 2e-11
results["nonconstant_weak_cancellation_exact_Z_adaptive_G"] = {"signed_residual":adaptive_value,"integration_error_estimate":adaptive_error}

# Q17 projected inverse: directly integrate the one-residual-value estimator for
# a residual with source, noise, cross, and first-chaos components.
lam, a = .6, .8
def R(g,zz): return g*g-1+2*g*zz+3*(zz*zz-1)+g
def jfun(X): return -(3.24*(X*X-1)/4+.6*X/3)/a
def jprime(X): return -(3.24*X/2+.6/3)/a
nv, wv = gaussian_rule(7)
lv, lw = leggauss(40)
angles, wa = (lv+1)*math.pi/4, lw/2
max_conditional_error = 0.
max_source_centering_error = 0.
for g,zz in [(-1.2,.3),(0.,0.),(.7,-.9),(2.,1.1)]:
    X = lam*g+a*zz
    numerical = 0.
    for theta, weight in zip(angles,wa):
        s,c = math.sin(theta),math.cos(theta)
        xp = s*X+c*nv[:,None]
        gp,zp = lam*xp+a*nv[None,:],a*xp-lam*nv[None,:]
        val = -math.pi/(2*a)*s*(c*zz-a*s*nv[:,None])*R(gp,zp)
        numerical += weight*float(wv @ val @ wv)
    exact = zz*jfun(X)-a*jprime(X)
    max_conditional_error = max(max_conditional_error,abs(numerical-exact))
assert max_conditional_error < 2e-12
# Integrate the full second moment independently in four Gaussian variables.
g,zz,v,w = np.meshgrid(nv,nv,nv,nv,indexing="ij")
weights4 = wv[:,None,None,None]*wv[None,:,None,None]*wv[None,None,:,None]*wv[None,None,None,:]
moment = 0.
for theta, weight in zip(angles,wa):
    s,c = math.sin(theta),math.cos(theta)
    xp = s*(lam*g+a*zz)+c*v
    value = -math.pi/(2*a)*s*(c*zz-a*s*v)*R(lam*xp+a*w,a*xp-lam*w)
    moment += weight*float(np.sum(weights4*value**2))
exact_moment = math.pi**2*(1+3*a*a)/(32*a*a)*25
assert abs(moment-exact_moment) < 2e-11
results["projected_residual_estimator"] = {"max_conditional_mean_error":max_conditional_error,"second_moment_direct":moment,"second_moment_formula":exact_moment,"R_L2_squared":25}

# A nonseparable two-dimensional conservative source, checked from endpoint
# values. Both source directions are coupled to coordinates, not coordinatewise
# unrelated scalar fixtures. P_r is used only by the truth evaluator.
v = np.array([1.,2.]); w = np.array([2.,-1.]); offset = np.array([.3,-.4])
def ff(x):
    return offset + np.sin(x@v)[...,None]*v/5 + .3*np.cos(x@w)[...,None]*w/5
def pf(r,x):
    return offset + math.exp(-2.5*(1-r*r))*(np.sin((r*x)@v)[...,None]*v/5+.3*np.cos((r*x)@w)[...,None]*w/5)
nodes, wn = gaussian_rule(24)
t1,t2,u1,u2 = np.meshgrid(nodes,nodes,nodes,nodes,indexing="ij")
tt = np.stack([t1,t2],axis=-1).reshape(-1,2)
ut = np.stack([u1,u2],axis=-1).reshape(-1,2)
wg = (wn[:,None,None,None]*wn[None,:,None,None]*wn[None,None,:,None]*wn[None,None,None,:]).ravel()
lam = .5
telescope_errors = []
for X in [np.array([.2,-.4]),np.array([1.1,.7]),np.array([-2.,1.])]:
    Xp = lam*lam*X+math.sqrt(1-lam**4)*tt
    for cap in (0,1,4,7):
        actual = pf(lam,X).copy()
        for idx in range(cap):
            r = lam**(2*idx+1)
            A = r*X+math.sqrt(1-r*r)*ut
            B = r*Xp+math.sqrt(1-r*r)*ut
            actual -= wg @ (ff(A)-ff(B))
        telescope_errors.append(float(np.max(abs(actual-pf(lam**(2*cap+1),X)))))
assert max(telescope_errors) < 3e-11
results["nonseparable_vector_endpoint_telescope_max_error"] = max(telescope_errors)

# Exact hazard law comparison, including zero/one endpoints and horizon zero.
grid = [F(0),F(1,20),F(1,4),F(3,5),F(1)]
hazard_cases = 0
for p in grid:
    for q in grid:
        for H in range(21):
            pm = [p*(1-p)**i for i in range(H)]+[(1-p)**H]
            qm = [q*(1-q)**i for i in range(H)]+[(1-q)**H]
            actual = sum(abs(s-t) for s,t in zip(pm,qm))/2
            lo,hi = sorted([p,q])
            exact = max((1-lo)**k-(1-hi)**k for k in range(H+1))
            assert actual == exact
            hazard_cases += 1
results["independent_exact_censored_hazard_cases"] = hazard_cases

# Solve Q52's Bellman system ourselves; verify endpoint monotonicity symbolically.
lo,hi,e,delta = sp.symbols("lo hi e delta", positive=True)
gamma = 1-delta
U0,U1 = sp.symbols("U0 U1")
sol = sp.solve([U0-gamma*(hi-lo+lo*U1+(1-hi)*U0),U1-gamma*(e+(1-e)*U0)],(U0,U1))
num = gamma*(hi-lo)+gamma**2*lo*e
formula = num/(delta*(1+gamma*lo)+num)
assert sp.factor(sol[U0]-formula) == 0
results["rare_mode_independent_Bellman_solution"] = "PASS"

# Actual code interface accounting, without editing the packet implementation.
four = module_at("independent_four", "replay_Q52/archive_science/gaussian_challenge/check_four_query_correction.py")
global_calls = [0]
old_call = four.CountingOracle.__call__
def counted_call(self,x):
    global_calls[0] += 1
    return old_call(self,x)
four.CountingOracle.__call__ = counted_call
with contextlib.redirect_stdout(io.StringIO()) as captured:
    four.main()
(ROOT/"logs"/"Q52_all_four_query_calls.stdout.txt").write_text(captured.getvalue())
assert global_calls[0] == 248000
results["rational_family_script_all_source_calls"] = global_calls[0]
gm = module_at("independent_gm", "replay_Q17/gaussian_mean/check_and_sample.py")
total_g_calls = [0]
old_g_call = gm.CountedOracle.__call__
def counted_g_call(self,x):
    total_g_calls[0] += 1
    return old_g_call(self,x)
gm.CountedOracle.__call__ = counted_g_call
trials, _ = gm.query_and_symmetry_checks()
results["Q17_query_symmetry_replay"] = {"outputs":trials,"total_whole_vector_calls":total_g_calls[0],"worst_case_cap":3}

# Refit variability is recorded, never substituted for the frozen certificate.
orig = ROOT/"owned_Q52/archive_science/coercive_audit/galerkin_S_rational.csv"
refit = ROOT/"refit_Q52/archive_science/coercive_audit/galerkin_S_rational.csv"
original_rows,refit_rows = list(csv.DictReader(orig.open())),list(csv.DictReader(refit.open()))
diff = []
for left,right in zip(original_rows,refit_rows):
    if left != right:
        diff.append({"G_degree":int(left["hermite_G_degree"]),"Z_degree":int(left["hermite_Z_degree"]),"frozen_numerator":int(left["numerator"]),"refit_numerator":int(right["numerator"]),"denominator":int(left["denominator"])})
(ROOT/"refit_coefficient_differences.json").write_text(json.dumps(diff,indent=2)+"\n")
results["refit_different_coefficient_rows"] = len(diff)
results["refit_max_absolute_coefficient_difference"] = max([abs(d["frozen_numerator"]-d["refit_numerator"])/d["denominator"] for d in diff] or [0.])
results["environment"] = {"python":sys.version,"numpy":np.__version__,"scipy":scipy.__version__,"sympy":sp.__version__}
(ROOT/"INDEPENDENT_RESULTS.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))
