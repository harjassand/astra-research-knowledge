"""Owner-reconstructed exact controls; never imports or executes producer programs."""
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
import json
from pathlib import Path


def main():
    checked = 0
    # The acquired audit gives the rational path expressions and a common
    # homogeneous denominator of degree12. Each cleared numerator has degree9.
    # Ten distinct nonpole x and y values therefore prove the epsilon=1
    # polynomial identity; homogeneity restores every nonzero epsilon.
    e = F(1)
    for x in map(F, range(2, 12)):
        for y in map(F, range(20, 30)):
            dx, dy = 1/(e-x), 1/(e-y)
            sx, sy = 1/(e+x), 1/(e+y)
            r = x+y
            cx, cy = 1/(e*e-x*x), 1/(e*e-y*y)
            kernel = 4*e*e*cx*cy*(x*cy+y*cx-1/r)
            ns = (dx*sy*sy+dy*sx*sx-sx*dy*dy-sy*dx*dx)/2
            zs = (dx*dy-sx*sy)/(2*e)
            ts = ((dx+dy)**2*(1/(2*e-r)-1/r)
                  -(sx+sy)**2*(1/r+1/(2*e+r))
                  +(dx-sx+dy-sy)**2/r)/2
            nc = sx*sy*sy+sy*sx*sx-dx*dy*dy-dy*dx*dx
            zc = -(dx*dy-sx*sy)/e
            tc = 4*e*e*(cx*cx+cy*cy)/r
            assert ns+zs+ts == kernel
            assert nc+zc+tc == -2*kernel
            checked += 2

    lo = F('1.7320508075688772')
    hi = F('1.7320508075688773')
    assert lo*lo < 3 < hi*hi
    a_lo, a_hi = 4-2*hi, 4-2*lo
    lower_bracket = 2*a_lo*a_lo-F(63, 28**2)
    assert lower_bracket > 0  # W>8 improves the denominator beyond28.
    w = F(12)
    lower = (2*a_lo*a_lo-F(63, (w*w-36)**2))/w
    upper = 2*a_hi*a_hi/w

    def outward(value, rounding):
        with localcontext() as context:
            context.prec = 16
            context.rounding = rounding
            return str(Decimal(value.numerator)/Decimal(value.denominator))

    def plus(a, b):
        return a[0]+b[0], a[1]+b[1]

    def distance(interval):
        return max(F(0), interval[0]-6, 6-interval[1])

    low, high = (F(9, 4), F(5, 2)), (F(7, 2), F(15, 4))
    upper_bath, lower_bath = (F(4), F(6)), (F(0), F(2))
    atom = (F(3), F(3))
    good = [plus(upper_bath, low), plus(low, low),
            plus(lower_bath, high), plus(high, high),
            plus(atom, low), plus(atom, high)]
    assert min(map(distance, good)) == F(1, 4)
    missed = plus(low, high)
    assert missed[0] < 6 < missed[1]
    assert distance(plus(upper_bath, low)) > 0
    assert distance(plus(upper_bath, high)) > 0

    eta = F(1, 9)
    assert 1-eta*(10-1) == 0
    total_p = F(3)
    source_delta, comparator_delta = F(1), F(3)
    assert (total_p*comparator_delta)/(total_p*source_delta) == 3

    output = {
        "scope": "Owner reconstruction of displayed algebra/support controls,not producer-script replay,experimental acquisition or finite-time gate validation.",
        "rational_kernel_identities_checked": checked,
        "kernel_proof_scope": "Two degree9 polynomial identities on a10x10 nonpole grid,with the stated common denominator and homogeneity argument; not a floating fit.",
        "positive_W8_lower_bracket": outward(lower_bracket, ROUND_FLOOR),
        "W12_t1_conservative_enclosure_of_symbolic_bounds":
            [outward(lower, ROUND_FLOOR), outward(upper, ROUND_CEILING)],
        "free_split_parity_external_gap": str(min(map(distance, good))),
        "same_parity_missed_cross_sum": [str(x) for x in missed],
        "support_scope": "Free g=0 support bookkeeping; exact-pole obstruction remains fixed small nonzero g,then small external lambda,as proved in its separate source.",
        "star_example": {"N": 10, "per_edge_eta": str(eta), "one_excited_energy": 0},
        "matched_comparator": {"P_over_g_squared": 3,
                               "source_abs_coefficient_over_ab": 3,
                               "comparator_abs_coefficient_over_ab": 9,
                               "ratio": 3,
                               "scope": "Leading ideal-model interaction; full-cycle costs and physical advantage remain unestablished."},
    }
    path = Path(__file__).resolve().parent / "evaluation/MATH_CONTROLS.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(output, indent=2)+"\n")
    print("Exact kernel/support/norm/comparator controls passed.")


if __name__ == "__main__":
    main()
