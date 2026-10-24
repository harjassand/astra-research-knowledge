#!/usr/bin/env python3
"""Standard-library replay of one finite-invariant continuum upper bound.

The numerical solver is not imported or trusted.  Candidate dyadic dual
weights are checked for sign; exact rational coefficient rows are rebuilt;
certified scalar intervals widen every continuum constraint; and an outward
rounded interval LDL^T test proves positivity of the repaired dual slack.
See the accompanying central derivation for the continuum inclusion.
"""
from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "luna_single_port"))
from fixed_interval_ldlt import FixedInterval, certify_spd

BITS = 192
SCALE = 1 << BITS
SCALAR_BITS = 100


def frac(x):
    return F(*x)


def pair(x):
    return [x.numerator, x.denominator]


def lower(x, bits=SCALAR_BITS):
    s = 1 << bits
    return F((x.numerator*s)//x.denominator, s)


def upper(x, bits=SCALAR_BITS):
    return -lower(-x, bits)


def read_interval(x):
    a, b = frac(x["lower"]), frac(x["upper"])
    assert a <= b
    return a, b


def square_interval(a):
    lo, hi = a
    return (F(0) if lo <= 0 <= hi else min(lo*lo, hi*hi),
            max(lo*lo, hi*hi))


def product_interval(a, b):
    ps = [x*y for x in a for y in b]
    return min(ps), max(ps)


def sqrt_bounds(q, bits=SCALAR_BITS):
    assert q >= 0
    s = 1 << bits
    k = math.isqrt((q.numerator*s*s)//q.denominator)
    lo = F(k,s)
    hi = lo if lo*lo == q else F(k+1,s)
    assert lo*lo <= q <= hi*hi
    return lo, hi


def point(x):
    return FixedInterval((x.numerator*SCALE)//x.denominator,
                         -((-x.numerator*SCALE)//x.denominator))


def add(a,b):
    return FixedInterval(a.lo+b.lo, a.hi+b.hi)


def mul(a,b):
    ps = [x*y for x in (a.lo,a.hi) for y in (b.lo,b.hi)]
    return FixedInterval(min(ps)//SCALE, -((-max(ps))//SCALE))


def times(a,q):
    x,y = ((a.lo,a.hi) if q>=0 else (a.hi,a.lo))
    return FixedInterval((x*q.numerator)//q.denominator,
                         -((-y*q.numerator)//q.denominator))


def add_outer(matrix, row, weight):
    """Add weight * row row^T with enclosing fixed-point arithmetic."""
    if not weight:
        return
    r = [point(x) for x in row]
    ids = [j for j,x in enumerate(row) if x]
    for p,i in enumerate(ids):
        for j in ids[p:]:
            a = times(mul(r[i],r[j]),weight)
            matrix[i][j] = add(matrix[i][j],a)
            if i != j:
                matrix[j][i] = matrix[i][j]


def add_symmetric_cross(matrix, row, other, weight):
    """Add weight*(row other^T+other row^T), including diagonal twice."""
    if not weight:
        return
    rr,oo = [point(x) for x in row],[point(x) for x in other]
    ids = [j for j,(x,y) in enumerate(zip(row,other)) if x or y]
    for p,i in enumerate(ids):
        for j in ids[p:]:
            a = add(mul(rr[i],oo[j]),mul(oo[i],rr[j]))
            matrix[i][j] = add(matrix[i][j],times(a,weight))
            if i != j:
                matrix[j][i] = matrix[i][j]


def complex_mul(a,b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]


def kernel_values(u,c):
    dx,y = u[0]-c,u[1]
    d = dx*dx+y*y
    inv = dx/d,-y/d
    aa = c*inv[0],c*inv[1]
    ap = complex_mul(u,complex_mul(inv,inv))
    return aa,ap


def make_rows(rhat,q0,n):
    dim = 2*n
    z = [F(0)]*dim
    z[0] = F(1)
    us = [[F(0)]*dim for _ in range(n)]
    vs = [[F(0)]*dim for _ in range(n)]
    for i in range(1,n):
        us[i][i] = F(1)
    us[0][0] = q0/rhat[0]
    for i in range(1,n):
        us[0][i] = -rhat[i]/rhat[0]
    for i in range(n):
        vs[i][n+i] = F(1)
    return z,us,vs


def main():
    cand_path = HERE / "rational_candidate.json"
    scalar_path = HERE / "root_scalar/scalar_enclosures.json"
    scalar_source = HERE / "root_scalar/certify_scalars.py"
    assert hashlib.sha256(scalar_source.read_bytes()).hexdigest() == \
        "f250fcb8ab3e879946423b7ea0ac9781f4c5eafed71b5397097445d440c8ed5f"
    assert hashlib.sha256(scalar_path.read_bytes()).hexdigest() == \
        "35beea2cfc8948ac8972317aec5b991545a4a7bf1a404c7b8a5beba93ff872fa"
    d = json.loads(cand_path.read_text())
    ss = json.loads(scalar_path.read_text())
    los,his = [frac(x) for x in d["cell_lo"]],[frac(x) for x in d["cell_hi"]]
    rhat = [frac(x) for x in d["normalizations"]]
    q0 = frac(d["q0"])
    n = len(rhat)
    assert n == 36 and d["eliminated_cell"] == 0
    assert los[0] == -1 and his[-1] == 1
    assert all(his[i] == los[i+1] for i in range(n-1))
    assert d["signs"] == [1]*24+[-1]*12 and all(r>0 for r in rhat)
    h = [b-a for a,b in zip(los,his)]
    c = [(a+b)/2 for a,b in zip(los,his)]
    rplus,bb,j2 = [],[],[]
    for i,cell in enumerate(ss["cells"]):
        assert cell["i"] == i
        assert frac(cell["lo"]) == los[i] and frac(cell["hi"]) == his[i]
        assert frac(cell["true_center"]) == c[i]
        rplus.append(upper(read_interval(cell["r"])[1]))
        bb.append(upper(read_interval(cell["int_R2"])[1]))
        j2.append(upper(read_interval(cell["J2"])[1]))
    assert len(rplus) == n and all(x>0 for x in rplus+bb+j2)
    qlo,qhi = read_interval(ss["q"])
    assert qlo > 0  # hence A_plus>A_minus and B=2*A_minus
    assert read_interval(ss["A_plus"])[0] > read_interval(ss["A_minus"])[1]
    am = read_interval(ss["A_minus"])
    assert read_interval(ss["B"]) == (2*am[0],2*am[1])
    charge_quadrature_error = upper(max(abs(qlo-q0),abs(qhi-q0)))
    seed_radius = frac(d["seed_l1_radius"])
    assert seed_radius >= 0
    # The correction is the vector q0*z-D0_initial.  It need not be axial:
    # every norm and objective estimate uses only its Euclidean norm bound.
    dq = charge_quadrature_error+seed_radius
    N = [upper((rplus[i]+(dq if i==0 else 0))**2/rhat[i]**2) for i in range(n)]
    K = [upper((h[i]*bb[i]+(2*rplus[i]*dq+dq*dq if i==0 else 0))/rhat[i]**2)
         for i in range(n)]
    assert all(0<x<=2 for x in N+K)
    trace_actual = 1+sum(N[1:])+sum(K)/3
    trace_upper = frac(d["trace_upper"])
    assert trace_actual <= trace_upper == 100
    identity_repair = frac(d["identity_repair"])
    assert identity_repair > 0
    z,us,vs = make_rows(rhat,q0,n)
    dim = 2*n
    zero = FixedInterval(0,0)
    slack = [[zero for _ in range(dim)] for _ in range(dim)]
    duals = {k:frac(v) for k,v in d["scalar_duals"].items()}
    assert len(duals)==2*n+4*7 and all(y>=0 for y in duals.values())
    y0 = frac(d["dual_H00"])
    mismatch = read_interval(ss["prescribed_sign_mismatch_objective_upper"])[1]
    obj_const_upper = upper(sum(rplus)/2+dq/2+mismatch)
    bound = obj_const_upper+y0+trace_upper*identity_repair
    # The charge-eliminated objective is -q0 H00/2 plus
    # sum_{minority} rhat_i H0i.  Subtract it in the dual slack.
    slack[0][0] = add(slack[0][0],point(y0+q0/2))
    for i in range(24,n):
        v = point(-rhat[i]/2)
        slack[0][i] = add(slack[0][i],v)
        slack[i][0] = slack[0][i]
    for i in range(n):
        yn = duals[f"u_norm_le_1_{i}"]
        yb = duals[f"bessel_{i}"]
        add_outer(slack,us[i],yn+yb)
        add_outer(slack,vs[i],3*yb)
        bound += yn*N[i]+yb*K[i]
    pole_records = []
    for j,p in enumerate(d["poles"]):
        u = frac(p[0]),frac(p[1])
        es = ss["ell"][j]
        assert frac(es["pole_re"])==u[0] and frac(es["pole_im"])==u[1]
        re = [F(0)]*dim
        im = [F(0)]*dim
        e = F(0)
        M = F(0)
        uabs_up = sqrt_bounds(u[0]*u[0]+u[1]*u[1])[1]
        for i in range(n):
            aa,ap = kernel_values(u,c[i])
            for k in range(dim):
                re[k] += rhat[i]*(aa[0]*us[i][k]+ap[0]*h[i]*vs[i][k]/2)
                im[k] += rhat[i]*(aa[1]*us[i][k]+ap[1]*h[i]*vs[i][k]/2)
            closest = min(max(u[0],los[i]),his[i])
            dist_lo = sqrt_bounds((u[0]-closest)**2+u[1]**2)[0]
            assert dist_lo>0
            mid_dist2 = (u[0]-c[i])**2+u[1]**2
            e += upper(uabs_up*j2[i]/(mid_dist2*dist_lo))
            M += upper(rplus[i]*max(abs(los[i]),abs(his[i]))/dist_lo)
        aa0,_ = kernel_values(u,c[0])
        e = upper(e+sqrt_bounds(aa0[0]**2+aa0[1]**2)[1]*dq)
        M = upper(M)
        er,ei = read_interval(es["re"]),read_interval(es["im"])
        ell_abs_up = sqrt_bounds(max(abs(er[0]),abs(er[1]))**2
                                 +max(abs(ei[0]),abs(ei[1]))**2)[1]
        # |v/(u-v)|<=1/Im(u) on [-1,1].  The initial L1 discrepancy
        # propagates into each conserved bilinear square by this bound.
        rho = seed_radius/u[1]
        seed_square_error = upper(rho*(2*ell_abs_up+rho))
        error = upper(e*(2*M+e)+seed_square_error)
        er2,ei2 = square_interval(er),square_interval(ei)
        rr = er2[0]-ei2[1],er2[1]-ei2[0]
        cross = product_interval(er,ei)
        ii = 2*cross[0],2*cross[1]
        re_lo,re_hi = lower(rr[0]-error),upper(rr[1]+error)
        im_lo,im_hi = lower(ii[0]-error),upper(ii[1]+error)
        yl,yh = duals[f"pole_re_lo_{j}"],duals[f"pole_re_hi_{j}"]
        zl,zh = duals[f"pole_im_lo_{j}"],duals[f"pole_im_hi_{j}"]
        wr,wi = yh-yl,zh-zl
        # Re(c c^T)=re re^T-im im^T;
        # Im(c c^T)=re im^T+im re^T (bilinear, no conjugate).
        add_outer(slack,re,wr)
        add_outer(slack,im,-wr)
        add_symmetric_cross(slack,re,im,wi)
        bound += yh*re_hi-yl*re_lo+zh*im_hi-zl*im_lo
        pole_records.append({"e_upper":pair(e),"M_upper":pair(M),
                             "seed_square_error_upper":pair(seed_square_error),
                             "square_error_upper":pair(error),
                             "re_slab":[pair(re_lo),pair(re_hi)],
                             "im_slab":[pair(im_lo),pair(im_hi)]})
    for i in range(dim):
        slack[i][i] = add(slack[i][i],point(identity_repair))
    proof = certify_spd(slack,precision_bits=BITS)
    assert proof.certified, proof.diagnostic
    claimed = frac(d["claimed_upper"])
    assert bound < claimed
    B_lo = read_interval(ss["B"])[0]
    assert B_lo > 0 and claimed <= F(95,100)*B_lo
    out = {
        "status":"PASS: exact scalar enclosures plus interval-LDL dual certificate",
        "scope":"fixed continuous Case-D G; fixed pointwise radius; explicit L1-small seeds; all homogeneous collisionless times",
        "candidate_sha256":hashlib.sha256(cand_path.read_bytes()).hexdigest(),
        "scalar_enclosures_sha256":hashlib.sha256(scalar_path.read_bytes()).hexdigest(),
        "scalar_source_sha256":hashlib.sha256(scalar_source.read_bytes()).hexdigest(),
        "ldlt_module_sha256":hashlib.sha256((HERE/"luna_single_port/fixed_interval_ldlt.py").read_bytes()).hexdigest(),
        "gram_dimension":dim,"cells":n,"moments_per_cell":2,"complex_probes":7,
        "fixed_interval_bits":BITS,"scalar_rounding_bits":SCALAR_BITS,
        "seed_l1_radius":pair(seed_radius),
        "charge_quadrature_error_upper":pair(charge_quadrature_error),
        "q_shift_upper":pair(dq),"objective_constant_upper":pair(obj_const_upper),
        "trace_actual_upper":pair(trace_actual),"trace_used":pair(trace_upper),
        "identity_repair":pair(identity_repair),"identity_repair_cost":pair(trace_upper*identity_repair),
        "dual_bound_upper_exact":pair(bound),"dual_bound_preview":float(bound),
        "claimed_upper":pair(claimed),"B_lower":pair(B_lo),
        "gap_lower":pair(B_lo-claimed),"gap_fraction_lower":pair(1-claimed/B_lo),
        "gap_fraction_preview":float(1-claimed/B_lo),
        "minimum_ldlt_pivot_lower":pair(min(proof.positive_pivot_lower_bounds)),
        "ldlt_pivots":[[pair(a),pair(b)] for a,b in proof.pivot_intervals],
        "N_rhs":[pair(x) for x in N],"K_rhs":[pair(x) for x in K],
        "pole_bounds":pole_records,
        "solver_status_used_as_proof":False,
    }
    (HERE/"verified_certificate.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({k:out[k] for k in ["status","dual_bound_preview","claimed_upper",
                     "gap_fraction_preview","minimum_ldlt_pivot_lower"]},indent=2))


if __name__ == "__main__":
    main()
