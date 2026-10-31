# Independent cross-mobility review

Date: 2026-10-31. Reviewer: independent child `review_cross_family`.

## Decision and scope

**Mathematical construction: PASS.** The fixed analytic potential, full-fiber
basins, normalized invariant law, each actual constant-SPD generator, and exact
smooth boundary patch are all received. The capacity limit is genuine, not the
energy of a boundary-violating shear. No empirical mixing assumption, physical
implementation, new variational principle, or generic hardness claim is earned.

**Finite receiver: PASS.** `receive.py` was read and independently replayed.
Its exact rational formulas, parsed-object schema validation, matrix derivation,
SPD/Schur checks, capacity enclosure, conductance factors, and condition-number
enclosure match the theorem. Separate replay covered all four supplied
certificates, 73 additional valid models, and 17 additional malformed objects.
The hardened parser/resource update also passes: three duplicate raw-key cases
(including an escaped equivalent key), eight invalid/insufficient budget cases,
and two exact budget boundaries. Huge `k` is rejected before expanded powers.

## Checks with consequential content

1. `v>=1` and `v>=y^4/2` give `3<Z<16`. In particular the noncoercive zero-energy
   line does not obstruct normalizability. Infinite stationary second moments do
   not invalidate the stopped Lyapunov proof.
2. For **every** fixed constant SPD `D`, not only the special family,
   `V=1+x^T D^-1 x` satisfies
   `LV=4-[6(y^2-2/3)^2+4/3]z^2<=4`. Coercivity is valid separately for each `D`.
   Local strong existence, stopped Ito, and the displayed exit-probability bound
   exclude finite-time explosion from every initial point.
3. The killed-domain symmetry/exhaustion argument is a sufficient receiving
   argument for invariance and reversibility. The use of nonexplosion to obtain
   `P_t 1=1` matters: formal stationary integration by parts alone would not have
   closed this step.
4. The smooth step construction has `||u'||<6`; the cutoff has `||chi'||<24`.
   Its use of absolute value is harmless because it is locally constant at zero.
   The blended trial is in `[0,1]`, smooth, and identically correct on **all** of
   each basin. Finite-energy spatial cutoffs justify weighted-form admissibility;
   these approximations are a domain argument, not replacement capacity trials
   with truncated basin values.
5. On the patch, `grad h=(a+p,-alpha a)` and its exact energy is
   `epsilon a^2+2 epsilon a p+p^2`. Thus the bound `900` is valid for either sign
   of `p`. Every nonzero derivative requires `|z|>=k/[8(1-epsilon)]>=k/8`.
   Total patch width is `1/4`, not `1/8` or `1/2`. The unnormalized tail cost
   `3600 exp(-k^2/128)/k` and normalized `1200` constant are correct.
6. The central-mass/shoulder comparison correctly proves `mu(A)>=1/4`, giving
   the factor `4` for capacity/mass conductance. This is not a claim about an
   arbitrary-start hitting time.
7. Schur completion and tilted-line Cauchy-Schwarz both preserve the full-fiber
   traces. They give the two strictly positive lower bounds for every actual
   SPD member. Weighted local Sobolev regularity/ACL and density justify their
   extension beyond smooth functions.
8. The eigenvalue/condition-number bounds correctly expose both diverging fast
   mobility and collapsing conditional mobility. Keeping `D_yy=1` does not keep
   all physical noise or metric resources bounded.

## Stronger geometry boundary independently obtained

The integer/rational restrictions are useful for the finite receiver, but are
not needed for the analytic boundary theorem. For any

    D = [[1,b],[b,c]],   c>b^2,   delta=1-b^2/c,

with real `b!=0`, put `alpha=b/c`. The same trial and patch argument work with
either sign of `b`, because

    (1,-alpha)^T D (1,-alpha)=delta,
    |alpha|=(1-delta)/|b|,
    |z|>=1/(8|alpha|)>=|b|/8.

Consequently the universal upper bound in this **specific 2D fixed-potential,
full-basin family** is

    cap_D <= 36 delta + (1200/|b|) exp(-b^2/128).

The two lower bounds are

    cap_D >= delta sqrt(pi)/Z,
    cap_D >= sqrt(pi/2) exp(-b^2/2)/Z.

They prove the exact sequential classification

    cap(D_n) -> 0  iff  delta_n -> 0 AND |b_n| -> infinity.

The forward implication uses both positive lower bounds; the reverse implication
uses the upper bound. For `b=0`, `delta=1` and the first lower bound rules out
collapse, so occasional zero cross entries cause no loophole. This is stronger
than saying that the construction is possible along one specially tuned family.
Neither condition alone suffices, but **jointly they do suffice here**. This
classification is not asserted for arbitrary potentials or higher-dimensional
geometries.

## Independent executed checks

Run:

    python independent_check.py

The script performs exact SymPy checks of the Lyapunov SOS identity, SPD
algebra, patched-gradient energy, Schur completion, and tilted-line decomposition.
It also executes finite diagnostics for full-fiber boundary samples including
very large `|z|`, 2,500 randomly chosen patch points, smooth-step derivative bound,
and normalizing/basin integrals. These diagnostics do not replace the proof and
no PDE capacity solver is used.

Executed result: **PASS**. Diagnostic values are `Z≈10.1179089112` and
`mu(A)≈0.4086402529`; the smooth step's actual maximum derivative is about
`3.31428`. `independent_check_results.json` preserves the output. Rational
examples use `e^{-x}<=2^{-floor(x)}` and exact arithmetic thereafter.

## Finite receiver replay and resource boundary

Run:

    python independent_receiver_check.py

Executed result: **PASS**, preserved in `independent_receiver_results.json`.
All expected outputs were recalculated independently with rational arithmetic.
Tests include `epsilon` very close to zero and one and nontrivial exact
numerator/denominator sizes. Boolean/float/string rationals, absent/extra fields,
and noncanonical fractions were rejected.

The receiver truthfully discloses output integer sizes of order `k^2` and now
checks a configurable expanded-power budget **before** the power allocations.
The default is 1,000,000. Insufficient budget explicitly rejects this execution,
not the theorem. Tests cover exact acceptance/rejection boundaries and a huge
`k` that must fail without power allocation. This is an expansion budget, not a
claim that arbitrary input byte lengths or all runtime memory are bounded.

`strict_json_loads` now rejects duplicate raw keys at every object level,
including escaped keys that decode to the same string. The CLI uses this strict
loader. The earlier two optional engineering observations are therefore closed
at their stated scope.

## Higher-dimensional Gaussian corollary

**`HIGH_DIMENSIONAL_COROLLARY.md`: PASS.** The extension is valid for every
integer fiber dimension `m>=1`:

- Gaussian fiber integration gives marginal `v^{-m/2}` with integrable `y^{-2m}`
  tails. The same quadratic Lyapunov has trace term `2(m+1)` and unchanged
  nonpositive drift coefficient multiplying `||z||^2`.
- The trial depends only on `(y,z_1)`, so its energy computation is unchanged.
  Conditional `z_1` variance is `1/v(y)<=1`. Gaussian Chernoff gives the uniform
  tail probability `2 exp(-k^2/128)`, hence normalized patch energy at most
  `1800 exp(-k^2/128)` without a dimension-dependent normalizer.
- Raising the shoulder/central comparisons to exponent `m/2` leaves their
  length ratio intact, proving `mu_m(A)>=1/4`.
- The optimal `y`-only capacity is exactly `1/(Q_m R_m)`. Since `v>=1`,
  `Q_m<=Q_1<8`; since `v<=2` on the unit-width slab, `R_m<=2^{m/2}<=2^m`.
  Thus `C_free,m>1/(8*2^m)` is correct.
- With `epsilon_m=2^{-3m-10}` and `k_m=16m`, multiplying the capacity bound by
  `8*2^m` gives precisely H3's coefficients and exponents. The first H3 term
  decreases by factor `1/4` per dimension; the second decreases by
  `2^{-4m-1}<=1/32`, proving the limit. The condition-number cost has the stated
  order `m^2*2^{3m}`.

`python independent_highdim_check.py` passes exact symbolic dimension/Euler/
Lyapunov checks and exact rational H3 consequences at dimensions 1, 2, 4, 8, 16.
Results are in `independent_highdim_results.json`. For example the certified
relative upper bound at `m=4` is `4833/4194304` (about 0.00115228). The small-`m`
bounds can exceed 1 and are not advertised as sharp.

This extension does not assert one fixed finite-dimensional potential as `m`
changes: at each dimension the potential is fixed across its mobility family.
It rules out a dimension-uniform relative guarantee once the stated cross
mobilities are allowed. It adds no physical implementation or hidden fast-mixing
assumption.

## Explicit remaining limitations

- The present review is of a fixed analytic mathematical model, not evidence
  that a physical system has constant reversible mobility or this potential.
- Every finite SPD member is valid; a singular limiting diffusion is neither
  needed nor silently received.
- Bounded cross amplitude prevents collapse even with loss of uniform ellipticity.
  Therefore the construction does not say that every cross term destroys the
  no-cross theorem's useful conclusion.
- No independent actual-capacity numerical estimate is claimed. The inequalities
  alone prove existence and the exact collapse criterion.
