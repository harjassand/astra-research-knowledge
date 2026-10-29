"""Bounded independent arithmetic/identity intake of the nonradial extension.

No kinetics, random samples, optimizer, or all-speed rebuild is run.  A single
previously admitted interval is replayed through the producer's pure certifier;
this replay is explicitly not an independent implementation of quadrature.
The jet algebra, tail/cover/mixture checks and receipt are owned by this review.
Producer files and bytecode are never written.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib
import json
import sys
import time

sys.dont_write_bytecode = True
from flint import arb, ctx, fmpq

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "t_nonradial_completion"
ctx.prec = 200


def a(q):
    if isinstance(q, arb):
        return q
    q = F(q)
    return arb(fmpq(q.numerator, q.denominator))


def rat(x):
    m, e = map(int, x.man_exp())
    return F(m * 2**e) if e >= 0 else F(m, 2**(-e))


def interval(x):
    return {"lo": str(rat(x.lower())), "hi": str(rat(x.upper())),
            "display": float(x)}


def digest():
    return {str(p.relative_to(SOURCE)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in SOURCE.rglob("*") if p.is_file() and "__pycache__" not in p.parts}


class Jet:
    """Independent second-order forward-mode automatic differentiation."""
    def __init__(self, x, d=0, dd=0):
        self.x, self.d, self.dd = map(a, (x, d, dd))

    @staticmethod
    def cast(other):
        return other if isinstance(other, Jet) else Jet(other)

    def __add__(self, other):
        b = self.cast(other)
        return Jet(self.x+b.x, self.d+b.d, self.dd+b.dd)

    __radd__ = __add__

    def __neg__(self):
        return Jet(-self.x, -self.d, -self.dd)

    def __sub__(self, other):
        return self + (-self.cast(other))

    def __rsub__(self, other):
        return self.cast(other) + (-self)

    def __mul__(self, other):
        b = self.cast(other)
        return Jet(self.x*b.x, self.d*b.x+self.x*b.d,
                   self.dd*b.x+2*self.d*b.d+self.x*b.dd)

    __rmul__ = __mul__

    def __truediv__(self, q):
        return self * (1/a(q))

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        z = Jet(1)
        for _ in range(n):
            z = z*self
        return z

    def exp(self):
        e = self.x.exp()
        return Jet(e, e*self.d, e*(self.dd+self.d*self.d))


def jet_second(point, axis, co, force_branch=None):
    v, r, u = [Jet(x, int(j == axis)) for j, x in enumerate(point)]
    aa, bb, cc = map(a, co)
    x = v*v+r*r-2*v*r*u
    # Points at a join may use either one-sided polynomial.  The first
    # derivatives agree there.  Box interpolation only needs essential bounds.
    middle = force_branch if force_branch is not None else 4 <= float(x.x) <= 25
    ph = 1+4*((x-4)*(25-x))**2/194481 if middle else Jet(1)
    e0 = (-v*v/2-a(F(3,4))*r*r/2+a(F(3,4))*v*r*u).exp()
    e1 = (-a(F(3,4))*r*r/2+a(F(3,4))*v*r*u-v*v*u*u/2).exp()
    p = aa+bb*(v-r*u)+cc*x
    g = ph*(4*r*e1-(r**3+r*r*p)*e0)
    return g.dd


def main():
    start = time.perf_counter()
    before = digest()
    certificate = json.loads((SOURCE/"NONRADIAL_CERTIFICATE.json").read_text())
    scalar = json.loads((SOURCE/"STATIC_CERTIFICATE.json").read_text())
    manifest = json.loads((SOURCE/"FINAL_RECEIPT.json").read_text())
    for item in manifest["manifest"]:
        assert before[item["path"]] == item["sha256"]
    assert scalar["row_certificate_sha256"] == before["NONRADIAL_CERTIFICATE.json"]
    assert certificate["status"] == "PASS_FULL_CONTINUUM"
    rows = sorted(certificate["admitted"], key=lambda row: F(*row["v_interval"][0]))
    end = F(0)
    for row in rows:
        lo, hi = [F(*x) for x in row["v_interval"]]
        assert lo == end < hi
        assert F(*row["row_upper"]) < F(199,200)
        assert all((F(*x).denominator & (F(*x).denominator-1)) == 0 for x in row["controls"])
        end = hi
    assert end == 8 and len(rows) == 47
    margin = F(199,200)-max(F(*row["row_upper"]) for row in rows)
    # The polynomial bump is C1 at both joins and has its only interior maximum
    # at x=29/2; h there is 441/4, hence phi=5/4 exactly.
    assert 1+4*F(441,4)**2/194481 == F(5,4)
    for x in (F(4), F(25)):
        h = (x-4)*(25-x)
        assert h == 0 and 8*h*(29-2*x)/194481 == 0

    # Independent scalar budgets at higher precision than the producer receipt.
    beta, d, eta = a(F(3,4)), a(F(1,10000)), a(F(199,200))
    pi = arb.pi()
    zb = (2*pi)**a(F(3,8))*beta**a(F(-3,2))
    cb = zb/beta.sqrt()
    assert cb < 4
    assert F(199,200)+4*F(25,4)*F(1,10000) == F(399,400)
    pq = d*a(F(45,16))*cb
    factory_c = 2+64/(1-pq)
    factory_e = 1-eta/(1-pq)
    assert factory_c < 67 and factory_e > a(F(3,1000))
    assert a(F(19,2))*factory_c/factory_e < 213000
    v = a(8)
    tail8 = a(F(5,4))*(4/(beta*(1-beta)*v*v)
               +beta**a(F(-3,2))*(-(1-beta)*v*v/2).exp()
               *(1+2*(2/(pi*beta)).sqrt()/v))
    assert tail8 < a(F(*certificate["tail_row_upper"])) < eta
    # Exact Gaussian-tail positive-part integral: no floating cancellation.
    def clipping(L):
        rr = (2*((2*pi)**a(F(-3,8))/L).log()/(1-beta)).sqrt()
        def surv(z):
            return (2/pi).sqrt()*z*(-z*z/2).exp()+(z/arb(2).sqrt()).erfc()
        bias = L*zb*surv(beta.sqrt()*rr)-surv(rr)
        assert bias > 0
        return rr, bias/(1+bias)
    rr, tv = clipping(d)
    claimed = scalar["continuous_clipping_pointwise_sharp"]["normalized_TV_bound"]
    assert a(F(*claimed["lower"])) < tv < a(F(*claimed["upper"]))
    assert tv < a(F(3574,10**18))
    assert (2*pi)**a(F(-3,8))*(-a(F(25,8))).exp() > a(F(1,8000))

    # Native gain-envelope Jacobian and completing-square identities, symbolic
    # polynomial equality avoids numerical density checks.
    import sympy as s
    r, v, u, be, c = s.symbols("r v u beta c", real=True)
    assert s.expand(be*(1-be)*r*r+(v*u-be*r)**2
                    -(be*r*r-2*be*v*r*u+v*v*u*u)) == 0
    assert s.expand(-be*(r-c)**2/2-(1-be)*c*c/2
                    +be*r*r/4-be*v*v/2
                    -(-be*(r-2*c)**2/4+(be-s.Rational(1,2))*c*c-be*v*v/2)) == 0
    # Rayleigh(alpha)*normal*azimuth, t=V cos(theta): E_G cancels alpha*V.
    assert s.cancel(4/(be*(1-be)*v)*(be*(1-be)*v)-4) == 0

    # Read-only local actual-code derivative admission against independent jets.
    sys.path.insert(0, str(SOURCE))
    builder = importlib.import_module("certify_nonradial")
    ctx.prec = 160
    test_boxes = [
        ((F(0),F(1,4)), (F(0),F(1,4)), (F(-1),F(1))),
        ((F(7,4),F(2)), (F(0),F(1,8)), (F(-1),F(1))),
        ((F(2),F(9,4)), (F(0),F(1,8)), (F(-1),F(1))),
        ((F(19,4),F(5)), (F(0),F(1,8)), (F(-1),F(1))),
        ((F(5),F(21,4)), (F(0),F(1,8)), (F(-1),F(1))),
        ((F(55,16),F(7,2)), (F(1),F(2)), (F(-1,2),F(1,2))),
        ((F(31,4),F(8)), (F(15),F(16)), (F(-1),F(1))),
        ((F(0),F(1,4)), (F(31,16),F(33,16)), (F(-1),F(1))),
        ((F(0),F(1,4)), (F(79,16),F(81,16)), (F(-1),F(1))),
    ]
    checks = 0
    from itertools import product
    for vbox, rbox, ubox in test_boxes:
        row = next(z for z in rows if F(*z["v_interval"][0]) <= vbox[0]
                   and F(*z["v_interval"][1]) >= vbox[1])
        co = list(map(lambda q:F(*q), row["controls"]))
        bounds = builder.derivatives(*(builder.interval(*z) for z in (vbox,rbox,ubox)), co)
        # producer returns derivatives in r,u,V order; jets use V,r,u order.
        for point in product(*[(z[0],(z[0]+z[1])/2,z[1]) for z in (vbox,rbox,ubox)]):
            x = point[0]**2+point[1]**2-2*point[0]*point[1]*point[2]
            branches = (False,True) if x in (4,25) else (None,)
            for axis, bound in zip((1,2,0), bounds):
                for branch in branches:
                    assert abs(jet_second(point,axis,co,branch)) <= bound
                    checks += 1

    # One existing worst-margin interval, fixed exact controls, no fit/grid.
    hardest = max(rows, key=lambda row:F(*row["row_upper"]))
    lo, hi = map(lambda q:F(*q), hardest["v_interval"])
    co = list(map(lambda q:F(*q), hardest["controls"]))
    ctx.prec = 112
    tick = time.perf_counter()
    replay = builder.Integrator(lo,hi,co).run(max_cells=6000)
    replay_seconds = time.perf_counter()-tick
    assert replay["status"] == "PASS"
    assert replay["row_upper"] == hardest["row_upper"]
    assert replay["box_evaluations"] == hardest["box_evaluations"]
    after = digest()
    assert before == after
    out = {"status":"PASS_BOUNDED_INDEPENDENT_EXTENSION_INTAKE",
           "producer_files_unchanged":True,"producer_manifest_files":len(manifest["manifest"]),
           "closed_speed_cover":[0,8],"exact_intervals":len(rows),
           "minimum_certified_margin_below_199_over_200":str(margin),
           "independent_jet_point_derivative_checks":checks,"derivative_boxes":len(test_boxes),
           "nonnegative_tail_at8":interval(tail8),
           "pointwise_clipping_radius":interval(rr),"pointwise_clipping_TV":interval(tv),
           "read_only_actual_certifier_replay":{
               "v_interval":hardest["v_interval"],"row_upper":replay["row_upper"],
               "box_evaluations":replay["box_evaluations"],"seconds_after_imports":replay_seconds,
               "independent_quadrature_implementation":False},
           "exact_native_gain_polynomial_identities":3,
           "kinetic_or_stochastic_or_optimizer_runs":0,
           "total_seconds_after_imports":time.perf_counter()-start,
           "producer_inputs":before}
    (ROOT/"REPLAY.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:v for k,v in out.items() if k!="producer_inputs"},indent=2))


if __name__ == "__main__":
    main()
