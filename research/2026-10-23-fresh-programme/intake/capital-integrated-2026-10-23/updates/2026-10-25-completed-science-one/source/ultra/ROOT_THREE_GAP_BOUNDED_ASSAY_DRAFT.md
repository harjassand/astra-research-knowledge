# Three-gap curvature with arbitrary bounded odd readout

25 October 2026. Root construction, independent review pending. The aim is
to remove the clipped-linear detector approximation from the bounded assay.
No physical device, priority or better-than-all-methods claim is made. Finite
differences, pointer correlation and sequential testing are conventional tools.
The proposed new operation must pass the checks below before use.

## 1. Predeclared physical experiment

Keep the existing true-coordinate host, constant unknown Delta, finite
translation pulses and fresh centered ZERO-QP Gaussian pointers. The two
tag shapes/areas are the same in three geometries, with free gaps

    T_0=T, T_1=T+h, T_2=T+2h, h>0.

Choose a geometry uniformly and independently before each trial. Pad every
trial to one common duration/read clock; preserve the actual detached pointer
quadratures during storage. Use fresh independent coupling signs and signed
raw product W, as in BOUNDED_DIFFERENTIAL_ACTUATOR. They extract an effective
real ODD response F_j of each pointer even with unknown electronic offsets.
Assume only |F_j|<=R_j. There is NO linear-response or clipped-linear
approximation to F_j in this construction. Set R=R_1 R_2.

The current response curves/pointer parameters may depend on the PAST, but
must be common to the three current counterfactual geometries. The starting
spin/host state is common too, by fresh randomization. Within-trial asymmetry,
storage loss, QP/phase defects and current-geometry-dependent electronics are
not removed by this assumption and require actual error budgets.

For a given trial define the unknown contrast product

    M=m_1 m_2,
    m_j=E_Gaussian F_j(Q_j+ell_j).

It is predictable and |M|<=R. We do not supply it to the estimator or assume
a positive per-trial lower bound. An END-OF-PROTOCOL average-contrast gate
will require a predeclared M_req>0.

The first-Delta cancellation for bounded odd readouts is exact as in
ROOT_ANALOG_POINTER_MOMENTS Section4. Hence each actual correlation has

    C_r(Delta)=M+c_2,r Delta^2+Rem_r,
    |Rem_r|<=R L_3(|Delta|tau_r),
    L_3(z)=exp(z)-1-z-z^2/2<=z^3 exp(z)/6.              (1)

Here tau_r is the total active trial duration for its transverse Dyson
expansion. The bound counts both ket and bra vertices. Transverse dynamics
after detachment need not be included if they commute with the stored record.
All actual meter durations and free gaps BEFORE detachment are included.

## 2. The host-free reference has an exact nuisance polynomial

For analysis only, use the reference with H_G spin independent and no
longitudinal host force/bias, retaining the SAME finite pointer dynamics.
This is not a supplied physical switch. Delta remains on during the tags.
At Delta=0 a tag's odd-weighted instrument has diagonal weights(+m,-m)
and zero offdiagonal weight: the Gaussian product kernel is real/even and
the response is odd. Thus its weighted map is exactly

    J_F(rho)=m{sigma_z,rho}/2.                           (2)

For two vertices BOTH in the free gap, the zero-transverse finite tags
therefore give M cos(Delta T). Their contribution to c_2(T) is -M T^2/2,
for any initial spin state. Two tag-internal vertices give a gap-independent
coefficient; one vertex in the free gap and one inside a tag gives a term
linear in T. The unperturbed reference has no other T dependence. Hence

    c_2,ref(T)=-M T^2/2+A T+B.                          (3)

The unknown A,B include all finite-tag shape/backaction effects and are
common across the three geometries. This ordered-word decomposition is the
central claim to reconstruct independently; it does not drop the actual
transverse evolution during a tag.

With v=(-1,2,-1), equations(3) give

    sum_r v_r M=0,
    sum_r v_r c_2,ref(T_r)=M h^2.                       (4)

Thus the curvature contrast preserves the bare Delta^2 signal while killing
both unknown tag nuisance coefficients, as well as the unknown zero baseline.

## 3. A deliberately conservative host comparison

Let B_host bound the unconditional state L2 norm of the longitudinal
frequency (2lambda Y_G(u)+epsilon)/hbar in the HOST-FREE reference applied
to the actual old state, averaged over its earlier records. H_G evolves
that host independently of all spin/pointer operations. Reference sigma_x
insertions and finite tags therefore leave this host marginal unchanged.
The actual linear-host source formula with the entire old bounded-force/
mechanical-meter history retained supplies the Y_G bound; it is not a
conditional Gaussian or conditional-energy assertion. The host force after
the trial start is removed only in this mathematical comparison. Direct
meter bias is retained exactly in both references and is NOT part of B_host.

For a unit hybrid ket vector, Duhamel comparing host-full and host-free
longitudinal propagation gives state error at most B_host tau_r/2. The same
applies to the bra, so a bounded observable matrix element changes by at most
R B_host tau_r. The total TWO-transverse-vertex ket/bra integration weight
is tau_r^2/2. Therefore the claimed unconditional coefficient bound is

    E_past |c_2,r-c_2,ref,r|<=R B_host tau_r^3/2.         (5)

This avoids claiming a Gaussian host or a uniformly bounded conditional
energy. Its independent check must confirm the hybrid state-moment comparison,
not replace state norms by an unbounded operator norm. A sharper quadratic
host-phase bound is possible but not needed for this proposed operation.

Combining(1),(4),(5), define

    C_b=(R/2)B_host sum_r |v_r| tau_r^3
            +(R/6)|Delta_max| sum_r |v_r|tau_r^3 exp(Delta_max tau_r).

Then the proposed randomized curvature mean mu_X satisfies

    E_past |mu_X-M Delta^2 h^2|<=Delta^2 C_b.             (6)

All constants are known coarse caps, not calibrated fine contrasts. Fixed
minimum pulse durations/range/phase or a large B_host can make this sufficient
bound unusable; return UNKNOWN rather than presume arbitrary control speed.

## 4. Same-record average-contrast acquisition

From each actual signed raw product W report

    X=3 v_geometry W,             |X|<=6R,
    Y=3 1_(geometry0) W,          |Y|<=3R.

Their conditional means are the curvature contrast and C_0 respectively.
The first-Delta cancellation and bounded Dyson terms give, for ANY input,

    |C_0-M|<=R L_2(Delta_max tau_0), L_2(z)=exp(z)-1-z.

For N trials, martingale Hoeffding therefore encloses the ACTUAL RANDOM
bar M=N^-1 sum_j M_j by

    M_-=bar Y-eps_Y-R L_2(Delta_max tau_0),
    M_+=bar Y+eps_Y+R L_2(Delta_max tau_0),
    eps_Y=R sqrt(18log(2/delta_Y)/N).                    (7)

Check consistency and require M_->=M_req>0 only at the END. No precise
baseline, linear detector gain, independent denominator or Gaussian
postselected bath is inferred. The same records may supply X and Y.

For d=Delta^2 h^2 bar M, (6) and Markov give

    Pr(|bar mu_X-d|>eta d AND bar M>=M_req)
                         <=C_b/(eta h^2 M_req).         (8)

This is a joint event bound; no division by unknown return probability is
made. Hoeffding for X gives radius

    eps_X=R sqrt(72log(2/delta_X)/N).

On the joint events, if bar X+eps_X<=0 return UNKNOWN. Otherwise

    |Delta|_lo^2=(bar X-eps_X)_+/[(1+eta)h^2 M_+],
    |Delta|_hi^2=(bar X+eps_X)/[(1-eta)h^2 M_-].           (9)

Total failure is <=delta_X+delta_Y+C_b/(eta h^2 M_req), plus all separately
acquired model/control/pointer-box failures. With true bar M<M_req, false
acceptance already requires failure of(7). No uniform nonzero-contrast
completion guarantee, optional-stopping or iid-bath claim is made.

## 5. Actual proposed interface change

If correct, this uses bounded arbitrary odd detector functions, exact
finite tags and a coarse empirical CONTRAST product, rather than an assumed
linear detector with a small tail-approximation error. The price is three
random geometries, a larger bounded score and a conservative host/Delta
remainder gate. Statistical relative acquisition still costs Delta^-4
at fixed quality; it does not beat the restricted noisy-record exponent.

Exact centered zero-QP Gaussian inputs, shared within-trial counterfactual
instrument law, stable actuator, fresh random bits and two fresh pointers
remain premises/resources. Nonzero unresolved phase/asymmetry floors may
swamp the quadratic signal. Full hardware, preparation/readout, storage,
control and source costs persist. This draft has no numerical execution;
the nuisance-polynomial and all-hybrid moment comparison require independent
whole reconstruction before acceptance. It changes no accepted earlier file.
