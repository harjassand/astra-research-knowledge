# Four one-sided fixture readings can qualify intrinsic loss

Parent continuation of the completed reciprocal-loss construction. This removes
the perfect-block/direct-velocity prerequisite from one finite qualification
operation. It does not remove the intrinsic visible-core/tail promise, actual
metrological bounds or operating/rating conditions. No experiment was performed.

At each calibration frequency, let the specified passive fixture have known
impedance Z_f with Re Z_f>0. For the unknown passive electrically terminated
module impedance Z_s, reciprocity gives

    K_f=F_fixture/V_terminal=-Z_f H/(Z_s+Z_f),
    |H| >= (Re Z_f/|Z_f|) |K_f|.

The completed peer construction proved this pointwise law. Its finite-fixture
transfer K_f need not have the cubic-core form, since it also depends on unknown
reactive mechanics. **It is unnecessary to fit or interpolate K_f.**

Suppose the intrinsic transfer has H=H_core+E, |E|<=epsilon throughout the band,
and q_core(x)=x²/|H_core(i sqrt(x))|² is a polynomial of degree<=3. Four
pointwise fixture readings and fixture factors give |H(x_j)|>=g_j>epsilon.
Consequently the unknown cubic's values obey

    0 <= q_core(x_j) <= x_j²/(g_j-epsilon)² = U_j.

For the cubic Lagrange basis ell_j(x),

    q_core(x) <= sum_j max(ell_j(x),0) U_j.

This is a finite band upper bound even though there are **no upper gain
observations**. Negative Lagrange weights multiply the known lower value0.
With uncertain, disjoint node intervals, interval arithmetic gives the same
valid outer bound; subdividing the protected band controls numerical enclosure
width. If it proves x²>G² q_upper(x), the actual intrinsic gain is >=G-epsilon
and its loss is >=omega_min R_min(G-epsilon)². Only the intrinsic transfer needs
the cubic/tail promise. The pointwise fixture factors require qualification at
the measured nodes, not a cubic model of the loaded fixture response.

## Executed construction

`finite_fixture.py` reuses the peer's reviewed exact rational interval primitive
and implements this new one-sided interpolation. The synthetic measurement
centres come from the published Pope nominal core plus a **supplied** pure
viscous100000 Ns/m fixture, at195,197,199,201 rad/s. These are not published
laboratory readings or an acquired fixture specification.1% magnitude and1ppm
frequency intervals are illustrative requirements. The node data alone, without
carrier mass, a measured mechanical phase, or loaded-fixture model coefficients,
give the following exact interval results over31–32 Hz:

| Intrinsic promise | Actual gain floor | Mechanical loss floor | Sufficient cells for1% |
|---|---:|---:|---:|
| Exact cubic core |17 N/V |95692.3 N/m |4 (bound.0089524) |
| Uniform visible tail<=.5 N/V |15.5 N/V |79550.4 N/m |5 (bound.0085589) |

The two cases each close with20 interval leaves, maximum depth5. The greater
cell count pays for the weaker, one-sided information. The known chain uses
the source25000 N/m+25 Ns/m connectors, the existing25501 N/m per-edge/base
norm budget and the conservative loss-minus51002 comparison margin. Cell count
changes total mass and static series stiffness; these are not matched-resource
isolator performance contests. A finite current **upper** rating is not obtained
from this one-sided operation.

This completes a conditional information reduction: loss qualification does not
require a perfect mechanical block, direct velocity measurement, a full reactive
mechanical model, or a finite-order promise for the loaded fixture transfer.
It still needs the calibrated dissipative fixture factor, actual terminal force/
voltage intervals, same-loop reciprocity, operating resistance lower bound,
settling/amplitude control, and the intrinsic visible-core/tail structure.
Unknown series or extra mechanical ports remain outside this scalar promise.
Durable operation also needs its separate input/time/thermal/lifetime rating.
These physical inputs are unacquired. Historical priority and practical full-cost
advantage remain open; no new hardware or civilisation-level result is claimed.
