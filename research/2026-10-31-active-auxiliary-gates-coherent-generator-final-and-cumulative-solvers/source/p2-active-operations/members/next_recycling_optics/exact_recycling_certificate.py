"""Exact rational certificate for the recycled spin-one optical complement.

The 3-state block uses the nonorthonormal coordinates S=diag(sqrt(3),1,
sqrt(2)); all coefficients and positive-principal-minor checks are rational.
No numerical eigensolver or external symbolic package is required.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent


def zero(): return np.full((3, 3), F(0), dtype=object)


def mul(z, w):
    return (z[0]*w[0]-z[1]*w[1], z[0]*w[1]+z[1]*w[0])


def abs2(z): return z[0]**2+z[1]**2


def leading_principal_minors(x, y):
    # x is symmetric and y antisymmetric, so x+i y is Hermitian.
    a, b, c = x[0, 0], x[1, 1], x[2, 2]
    u, v, w = (x[0, 1], y[0, 1]), (x[0, 2], y[0, 2]), (x[1, 2], y[1, 2])
    triple = mul(mul(u, w), (v[0], -v[1]))
    return [a, a*b-abs2(u), a*b*c+2*triple[0]-a*abs2(w)-b*abs2(v)-c*abs2(u)]


def certificate():
    hp = np.array([[F(0), F(1), F(0)],
                   [F(3), F(40, 3), F(-40, 3)],
                   [F(0), F(-20, 3), F(20, 3)]], dtype=object)
    vp = zero(); vp[0, 1] = F(1); vp[1, 0] = F(3)
    metric = zero()
    for j, k in enumerate([3, 1, 2]): metric[j, j] = F(k)
    decay = zero(); decay[1, 1] = decay[2, 2] = F(1)
    x = zero(); y = zero()
    for j, k in enumerate([F(2127753, 208384), F(2035657, 625152), F(30743, 4884)]):
        x[j, j] = k
    for (i, j), a, b in zip([(0, 1), (0, 2), (1, 2)],
                            [F(-135, 407), F(-8265, 13024), F(-175, 1776)],
                            [F(-1, 2), F(-3175, 3256), F(4195, 26048)]):
        x[i, j] = x[j, i] = a
        y[i, j] = b; y[j, i] = -b
    real = -hp.T@y+y@hp-(decay@x+x@decay)*F(1, 2)
    real[1, 1] += x[0, 0]*F(1, 3)  # ALL r->b recycling, not a no-jump model
    imag = hp.T@x-x@hp-(decay@y+y@decay)*F(1, 2)
    residual = list((real+metric).flat)+list(imag.flat)
    assert all(z == 0 for z in residual)
    cr = -vp.T@y+y@vp
    ci = vp.T@x-x@vp
    # The second drive quadrature is Vy=i(v-v^dagger). In the transformed
    # coordinates Vy'=iW, W=[[0,-1,0],[3,0,0],[0,0,0]].
    wp = zero(); wp[0, 1] = F(-1); wp[1, 0] = F(3)
    cyr = wp.T@x+x@wp
    cyi = wp.T@y+y@wp
    checks = {
        "P3_minus_I": leading_principal_minors(x-metric, y),
        "9over2_I_minus_P3": leading_principal_minors(F(9, 2)*metric-x, -y),
        "8over5_I_minus_C": leading_principal_minors(F(8, 5)*metric-cr, -ci),
        "8over5_I_plus_C": leading_principal_minors(F(8, 5)*metric+cr, ci),
        "13over10_I_minus_Cy": leading_principal_minors(F(13, 10)*metric-cyr, -cyi),
        "13over10_I_plus_Cy": leading_principal_minors(F(13, 10)*metric+cyr, cyi),
    }
    assert all(t > 0 for values in checks.values() for t in values)
    # The remaining five complement modes have P=1 (three modes), and
    # P=1+P_bb (the two excited |xz>,|yz> modes which recycle into bright).
    pbb = x[0, 0]/3
    extra_upper_margin = F(9, 2)-(1+pbb)
    assert extra_upper_margin > 0
    return {
        "basis": "b,r,q = g_z,e_zz,(e_xx+e_yy)/sqrt(2)",
        "coordinate_change": "S=diag(sqrt(3),1,sqrt(2)); Pprime=S^dagger P S",
        "Pprime_real": [[str(z) for z in row] for row in x],
        "Pprime_imag": [[str(z) for z in row] for row in y],
        "poisson_equation_exact_zero_residual": True,
        "strict_positive_leading_principal_minors":
            {k: [str(z) for z in values] for k, values in checks.items()},
        "extra_mode_upper_margin": str(extra_upper_margin),
        "conclusion": "I <= Pfull <= (9/2)I and ||i[V,Pfull]|| < 8/5",
        "gain_domain": "Hermitian ||G-I||<=1/4, arbitrary common H_E(t)",
        "operator_inequality": "L_t^*(Pfull tensor I) <= -(3/5)I <= -(2/15)(Pfull tensor I)",
        "survival_bound": "Pr(transient at t) <= (9/2) exp(-2(t-s)/15) Pr(transient at s)",
        "complex_gain_domain": "A=I+B with ||B||<=1/4; Re B and Im B need not commute",
        "complex_gain_operator_inequality": "L_t^*(Pfull tensor I) <= -(11/40)I <= -(11/180)(Pfull tensor I)",
        "complex_gain_survival_bound": "Pr(transient at t) <= (9/2) exp(-11(t-s)/180) Pr(transient at s)",
    }


if __name__ == "__main__":
    result = certificate()
    (ROOT/"exact_recycling_certificate.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
