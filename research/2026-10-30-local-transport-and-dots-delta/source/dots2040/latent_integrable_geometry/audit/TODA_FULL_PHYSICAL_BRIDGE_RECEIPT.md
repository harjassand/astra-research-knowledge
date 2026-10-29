# Actual positive Toda input → local Abel initialization → doubling → full state

**2026-10-29. Numerical implementation receipt, not a certified algorithm theorem.**

Artifacts: `toda_full_physical_bridge.py`, `.json`, `.log`; reused arithmetic
`rounded_relative_doubling.py`. The exact input is `a=(1,2,3)`, `b=(0,1,-1)`;
`C=6`, `p=x³−15x+8`, `F=p²−144`. The original curve is fixed throughout.
The endpoint table is the saved prototype's high-precision isolation of that F.

## A discovered convention error, caught before running time evolution

With the governing transfer convention
`T_i=[[(x-b_i)/a_i,−a_(i−1)/a_i],[1,0]]` and `M=T3 T2 T1`, the vector
`(psi1,psi0)=(1,0)` maps to `(psi4,psi3)`. At a Dirichlet root `psi3=0`,
**the multiplier is M11, not M22**. The two are reciprocal there.

The finite initial block is `[[0,1],[1,1]]`, hence `G=x²−x−1` and
`mu=(1±sqrt5)/2`. Exact symbolic transfer multiplication gives

- `M22=−3(x−1)/2`;
- `M11 mod G=−2x/3`;
- correct `y=12*M11−p mod G=5x−9`.

Using M22 instead produces the conjugate divisor, which decodes to
`a=(1,3,2), b=(1,0,−1)`, not the requested initial state. This negative regression
is preserved in JSON. With the correct sheets, the initial decoder error norm is
`1.5493111145e−98`. Both the monodromy and initial sheet polynomial were derived
symbolically rather than guessed from an ODE trajectory.

## Initialization and full inverse-spectral decoder

The initializer solves only the short local equation
`A(theta0+h)−A(theta0)=(0,−2*tau)`, `tau=1/64`, on the original F.
It uses fixed-J iteration, numerically evaluated local one-dimensional Abel
integrals, and the signed-angle Jacobian. It never evolves physical a,b to obtain
an initial spectral point and never replaces F with a numerically recomputed curve.

Fifty iterations attain residual `1.4162755617e−71`. The final angle displacement
norm is about `0.22731`; the maximum observed fixed-J iteration derivative Frobenius
norm at iterates is `0.08430`. These are numerical observations, not a certified
whole-neighborhood contraction bound or satisfaction of the deliberately conservative
all-input collar radius in `LOCAL_FLOW_INITIALIZATION.md`.

The decoder uses stable reciprocal evaluation of kappa, then
`a3²=−C sum 1/(kappa_j G'(mu_j))` and positive normalized weights
`W_j=−C/(a3² kappa_j G'(mu_j))`. For the two-site finite block,
`b1=sum W_j mu_j`, `a1²=sum W_j(mu_j−b1)²`, `b2=sum mu_j−b1`.
Finally `a2=C/(a3*a1)` and `b3=−sum mu_j`. Every decoded a_i is positive.
Decoded initialized physical coordinates agree with independent DOP853 to
`4.4408920985e−16`.

## Arithmetic, target times, and comparator

Each call performs relative doubling about the **original** fixed divisor D0,
not about the previous point. Matrix rounding uses 256 bits and prescribed-point
perturbation scale `2^-44`. Each call must pass both separated-zero matching below
one quarter of input separation and one-residual-point-per-gap checks before its
output can enter the next call. Failed admission raises an error rather than
returning an apparent physical success. Direct-Abel error is compared with
`A(D(t))−A(D0)−(0,−2t)` modulo the independently numerically computed real periods.
The period matrix is used for diagnostics, not for the local initializer or
section-based group operation.

Direct physical integration is an independent comparator, never a producer. It
integrates all six original Toda ODE variables with DOP853 at two tolerances,
`2e−12` and `2.3e−14`, recording refinement differences and energy/product drift.
Comparisons are requested at tau, 1/32, 1, 16 and 32.

## Evidence boundary

Exact: original F, transfer multiplication, initial Dirichlet polynomial,
normalized rational kernels of rounded matrices, polynomial norms, gcds,
squarefree multiplicity and rational isolating intervals inside the reused arithmetic.

Noncertified: transcendental evaluations, local quadrature, fixed-J iteration,
rounding-error bounds as evaluated in floating point, selecting the numerical sheet
in the inherited genus-two prototype, root midpoint conversion, zero matching,
physical projection, decoding, periods and ODE reference. The tested q/eps schedule
is empirical; the conservative theorem schedule and rigorous interval decisions
are not implemented here. This is neither raw-equation recognition nor a general
fast-forwarding or comparative speedup result. It specifically checks that an
actual initial state can traverse the fixed-curve initialization/arithmetic/full-state
interfaces without silently changing the sheet, origin, curve or flow velocity.

## Completed baseline run

All eleven calls through `T=32` passed both arithmetic admission and the numerical
cumulative direct-error budget. At `T=16` and `T=32`, direct-Abel errors were
`1.9401042636e−11` and `3.8817762053e−11`, respectively.

Independent direct-ODE max-step refinement is preserved in
`toda_direct_ode_reference.py/.json/.log`. It uses no spectral code. Restricting
DOP853 to max steps `1/256` and `1/512` gives endpoint differences of `9.13e−14`
at T16 and `5.19e−13` at T32. Against the smaller-step reference, maximum error
across **all six physical coordinates** is `2.9358450393e−10` at T16 and
`2.9258062639e−10` at T32. These errors are well above the observed reference
step-refinement differences, so this baseline exhibits a measurable arithmetic
perturbation error rather than merely matching an inaccurate comparator.

## Completed precision refinement

`toda_full_physical_refinement.py/.json/.log` repeats the full initialization and
physical chain, changing only arithmetic rounding to 288 bits and perturbation
scale to `2^-52` (256 times smaller). All eleven refined calls also passed admission
and cumulative direct-error checks. `toda_physical_comparison_summary.py/.json`
joins both completed runs with the independent step-refined ODE and verifies source
hashes, matching admissions, and fixed-curve equality.

| Target | Baseline max physical error | Refined max physical error | Direct-Abel error reduction |
|---|---:|---:|---:|
| T=16 | 2.93585e−10 | 1.14565e−12 | 256.00000000002× |
| T=32 | 2.92581e−10 | 1.09268e−12 | 256.00000000002× |

Physical errors are relative to the float64 max-step `1/512` ODE reference, not
certified upper bounds. Its step-halving variation is `9.13e−14` at T16 and
`5.19e−13` at T32. In particular the refined T32 physical error is close enough to
this reference floor that its physical reduction factor (about268) should not be
interpreted as accurately distinct from256. The separately computed direct-Abel
reduction tracks the deliberately imposed perturbation scaling cleanly.

As a full-output consistency check, reconstruct the coefficients of the N3
monodromy numerator from every decoded state:

`p=x³−(b1+b2+b3)x²+(b1b2+b1b3+b2b3−a1²−a2²−a3²)x`
`  −b1b2b3+a1²b3+a2²b1+a3²b2`.

Their deviations from `(1,0,−15,8)`, together with `|a1*a2*a3−6|`, are below
`7.63e−34` for the baseline and `5.85e−34` for refinement. This is consistent with
the saved 35-digit coordinate strings; it does not prove phase accuracy by itself.

**Outcome:** the requested actual-state, unchanged-curve, local-flow initialization,
relative arithmetic, and full physical decoder interfaces now have a completed
numerical bridge and an informative precision-refinement check. The implementation
also exposed and corrected a real multiplier-index/sheet error before time evolution.
It remains a noncertified finite-instance experiment, not the outstanding uniform
finite-precision theorem or evidence of novelty.
