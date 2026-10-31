# Independent review: sufficient finder for partial satellite rows

## Verdict and scope

**ACCEPTED as a sound sufficient certificate finder, not as a terminating or
complete stability algorithm for the recognized architecture.** The frozen
accepted certificate proves a global geometric Foster inequality, nonexplosion,
classwise positive recurrence, and exponential moments strictly below log T.
Numerical success is never used as an acceptance premise. Numerical declines,
failed exact checks and budgets remain UNKNOWN.

No acceptance of an unbudgeted search theorem, all-exponent conclusion, exact
LP infeasibility, general weak reversibility, historical novelty or operational
chemistry is given. The separate subsequent tilted-support proposal is outside
this review.

## Frozen objects

| Object | SHA-256 |
|---|---|
| `PARTIAL_ROW_FINDER_THEOREM.md` | `2af0be714221f26a5a9887d32cdb807cc698a62a98e0f6f94e5d4808bc43586f` |
| `partial_boundary.py` | `4560ad2fabe8c7bf0a213411193baebd5d6a19b6ac34ad06208e7b1a5a51cfd5` |
| `results.json` | `98e06117f947fd3606995900c0d51deb645d6de9b6bfebf7f6f7cdd9f35eae82` |
| `failed_search_alpha2.json` | `886b57a2bac5b74e83e4ad289149d2c2a065627f73267a1821e39c38a26a165e` |

Copies, byte-identical accepted replay, independent verifier, challenge receipts,
reproduced rejected numerical proposal and checksums are in `independent_audit/`.
The frozen accepted JSON was independently verified directly. Parent sources
and all earlier accepted packages were not edited.

## 1. Region coverage and exact raw-generator forms

The unknown function covers **every** service composition with r<R, rather than
only the all-hubs-empty face. All nonneutral reactions in this restricted class
change service total by at most one. Therefore:

- every possible entrance into the patch is from r<=R;
- every service composition with r<=R is explicitly checked;
- for r>R no one-step reaction reaches r<R, so the acquired analytic tail applies
  without a hidden patched-neighbor term.

The r=0 state is an unknown, so no undefined g(0) formula is used. At r=1,
forward-star propensities vanish; no invalid division by r-1 occurs in the
finite-head computation. At r=R, the constraints correctly include patched
r=R-1 destinations and unpatched r=R+1 destinations.

For V=T^|z| h(y), a forward star contributes

    alpha_hj*y_h(y_h-1) [T*h(y-e_h)-h(y)]

independently of z. A reverse star contributes

    beta_hj*y_h*z_j [h(y+e_h)/T-h(y)].

The core contributes its actual linear generator applied to h. Neutral channels
preserve y and total satellite count, hence vanish even at high degree. These
facts prove the exact affine dependence on individual satellite coordinates;
there are no missing cross terms or implicit stationary averaging.

The independent verifier reconstructs the affine forms by a different route:
it applies the **original raw generator** to the symbolic head vector at z=0
and at each satellite unit vector, subtracting to extract every coefficient.
Raw shape verification establishes that this extraction captures the complete
all-z affine expression. Every coefficient and right-hand side of every stored
LP inequality is then compared exactly, including inequalities on the fixed
boundary r=R.

## 2. Why the covered/uncovered split is sufficient

At an uncovered service state, one satellite has no occupied adjacent hub.
That coordinate can diverge while V grows exponentially. A positive constant
quotient cannot be absorbed by any finite global C along this ray. The imposed
constant inequality is therefore a meaningful protection, not a finite-state
shortcut. Together with nonpositive coefficients for **all** satellite
coordinates it gives LV<=-epsilon V along the entire infinite fiber.

At a covered state, strict negativity for each individual satellite coefficient
is required. The positive gamma margin guarantees this, and the minimum slope
controls total satellite count. The explicit integer cutoff and C_y bound are
valid for every distribution of that total among satellites. Constants need not
be negative at these finitely many service configurations because the remaining
satellite exception sets really are finite.

The incomplete rows do not invalidate the radial tail bound: missing reverse
rates remove only nonpositive terms, while the forward-star bound still uses
the acquired maximum row sum. Common hub weight T is preserved by the linear
weight acquisition. The chosen epsilon is below the separately acquired tail
margin.

## 3. Acquisition and exact acceptance

No compatible h is supplied as an input. The raw partition is enumerated, the
exact affine matrix is built, a conventional floating LP proposes weights,
and every proposed weight is rationalized with a declared denominator bound.
Acceptance requires positive rational weights and every exact rational
residual <=0. The verifier reconstructs rather than trusts the stored residuals,
coverage labels, finite-state rows, coefficients and exception constant.

The strict floating proposal margin is only a heuristic for finding a point
that survives rationalization. Floating feasibility, infeasibility, tolerances
or status messages never certify a theorem. The first recognized partition,
finite radius schedule and numerical proposer are not complete. The reported
UNKNOWN outcomes must not be described as mathematical instability or exact LP
infeasibility. The frozen proof correctly makes these limitations explicit.

## 4. Probabilistic conclusions

Positive head weights plus the exponential tail make V normlike. The all-state
Foster bound proves nonexplosion by stopped finite sublevels, including arbitrary
finite-order neutral motion. Weak reversibility supplies feasible return paths,
so communicating classes are closed; the Foster return argument gives classwise
positive recurrence.

The stationary integrability step is valid without assuming pi(V)<infinity:
stopped exponential Dynkin gives P_tV<=aV+b with a<1; invariance and concavity of
min(V,n), then Fatou with integrands bounded below by -b, yield
pi(V)<=C/epsilon. Consequently every theta<log T of an **accepted** certificate
is supported. This also implies all polynomial count moments. Larger exponential
exponents require another accepted certificate. Unlike the preceding complete-row
constructions, no all-T termination theorem is present and none is imported.

The non-complex-balance calculation for the four-species example is correct:
linear-core balance gives b=2/15 and d=1/6, star balance would give c=b and f=d,
and neutral balance would give c=f. This excludes that immediate product-Poisson
explanation; it is not a priority search or an exclusion of every conventional
stability theorem.

## 5. Independent positive and UNKNOWN tests

`verify_partial.py` performs exact verification without calling the submitted
recognizer, tail constructor, LP builder, solver, value function or generator
while checking a receipt. The candidate code is used only to acquire proposals.
It verifies the raw architecture, monomolecular connectivity, paired partial
rows and global satellite coverage, weight equations, radial tail, all positive
head values, every original-generator affine form, every rational inequality
and residual, every covered/uncovered fiber, and the finite Foster bound.

Five accepted cases passed **7,440 additional exact full-generator state checks**,
separate from the original 1,056:

| Case | T | R | Unknowns | Inequalities | Service rows | Exact states |
|---|---:|---:|---:|---:|---:|---:|
| Original partial rows | 2 | 8 | 36 | 89 | 45 | 1,248 |
| Complete-row recovery | 2 | 2 | 3 | 11 | 6 | 336 |
| Separately acquired larger-T certificate | 3 | 16 | 136 | 305 | 153 | 3,360 |
| Species permutation / reacquired roles | 2 | 8 | 36 | 89 | 45 | 1,248 |
| Degree-seven neutral channels | 2 | 8 | 36 | 89 | 45 | 1,248 |

The tests include independent satellite populations0,1,17,300 and service
configurations beyond the patch boundary. They supplement, rather than replace,
the analytic all-state tail proof. The T=3 case is an actual separate successful
acquisition, not extrapolation from T=2; it still does not prove all exponents.

Adding an inactive service phase was recognized but returned UNKNOWN: the
R=5 proposal had35 variables and106 inequalities with a floating infeasibility
status; the next220-state head exceeded the declared200-state budget. This
outcome is retained, not silently dropped or claimed mathematically impossible.

Tampered zero head weight, omitted boundary row, false coverage label, altered
LP coefficient, false residual, zero gamma and zero Foster C were rejected.
Weakly reversible raw mutations with an extra nonlinear service pair or an
uncovered satellite were rejected structurally. Separate radius-trial and
head-state budgets produce honest UNKNOWN receipts and retain earlier trials.

## 6. Strong negative control: floating success is genuinely unsafe

The earlier alpha2 search was independently replayed to the same UNKNOWN
receipt. At R=32 the floating solver reports success, but its rationalized point
fails exact checking. The reviewer captured that proposed vector and recomputed
its drift coefficients directly from the original raw generator, independently
of the submitted LP builder. The largest violation is exactly

    352851/8388608000 >0

at uncovered service state (0,29), for the constant-drift inequality.

More importantly, the rationalized point has a strictly **positive** satellite
coefficient at service state (0,31), satellite index1, and symmetrically at
(31,0), satellite index0. The exact fractions and all positive violations are
preserved in `challenge_results.json`. Along either corresponding satellite
ray, LV/V tends to positive infinity, while C/V tends to zero for any finite C.
Thus this proposed V cannot satisfy any finite-C geometric Foster bound, not
merely the particular chosen gamma margin. Exact verification is substantively
necessary.

This rejects a proposed function, not the network's recurrence or all possible
corrections. No exact infeasibility certificate was computed.

## 7. Accounting and retained restrictions

The main accepted search actually paid LP shapes(3,11), (10,29), (36,89).
The failed control and additional challenges charge their own matrices and
radius histories. Numerical optimization, rationalization, dense matrix
construction, exact residual evaluation and large Foster constants are not free
oracles. Head budgets do not bound every intermediate coefficient bit size,
solver runtime, exception exponent or arbitrary-precision operation. The
prototype is a trusted research API rather than a hardened total parser.

The soundness result retains a strongly connected monomolecular service core,
positive direct death at every hub, paired star shapes, a common satellite
exponential weight, and neutral remainder. General nonlinear service dynamics,
more general satellite transitions, guaranteed LP feasibility and a bound on a
successful radius remain outside this frozen result.
