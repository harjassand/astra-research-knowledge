# Independent whole audit: homogeneous kinetic lift and clamped-energy CDF

## Verdict and frozen binding

**PASS for the complete declared-model proof/code/receiving conjunction.** No frozen source correction was required. This is a finite executable acceptance separate from the earlier theorem-only receipt and separate from the previously accepted robustness/conductance package.

Exact inputs:

- `radial_kinetic_service_20261031/FROZEN_SHA256.json`: 6,768 bytes, SHA256 `edb99e8bc6284fd7bd18a6248cec114ecca83e5b5771d0748193460d81dc81ad`.
- `receive_kinetic.py`: `b4b75f4eb063e13a8c4fe49a34af5c55f182df87317a1cde4c0c14b3aefdf8cb`.
- Current theorem `EXACT_KINETIC_LIFT_CANDIDATE.md`: `7d9841aa8604523aa44f921c90c4da986a5932755408351da161affe890a9242`.
- `check.py`: `6300f5599393ade62589c3dee624f82ee0def4196c35390a4e992fc30813d008`.

All **26 manifest files** match their exact sizes and hashes. I read the current mathematical argument, executable, author tests, arithmetic/cost record, scope judgment, README, and source-bound theorem review. The earlier sign/citation versions and theorem-check snapshots remain historical evidence, not current source substitution. `CONSTRUCTION_NOTES.md` is outside the 26-file freeze and is not promoted to accepted current claims. The earlier robustness archive also matches its recorded 720,934 bytes and SHA256 `b1595d4fe992de16fc4662264008ba11b4fa4f7bcc36b23d6c0e6eb8c11abf73`.

Accepted finite operation: a **terminal energy CDF with requested absolute interval width under a fixed externally declared finite clamp protocol**, for the raw homogeneous energy and the declared divergence-form radial-plus-complete-pair-tangent generator. It is not the earlier constant-SPD/Euclidean process, an autonomous hitting-time calculation, adaptive control, full-state trajectory service, angular equilibrium sampler, empirical generator acquisition, or physical actuation.

## Actual replay and independent results

The clean copied-tree author suite completed **988 checks**, including actual recomputation of all four saved cases and the noncentral-energy case. Its regenerated report is **byte-identical** to frozen `check_results.json`. Wall time was 2.219s, a diagnostic rather than a controlled benchmark. Runtime production uses only the Python standard library; SymPy and SciPy appear in the author test suite, with SciPy explicitly a non-proof diagnostic.

The independent suite passed **1,152 checks**. It uses a separately implemented unscaled exact rational exponential series with a geometric remainder, direct factorial noncentral-Gamma mixture references with full remainder bounds, independent protocol product/sum formulas, exact initial polynomial evaluation, every proof-bearing field attack, malformed and oversized raw inputs, and exact resource boundaries. It also:

- replays the standalone saved raw/certificate pair, not included in the author's four-row loop;
- reconstructs all four original external tasks literally from the source's declared protocol/threshold/initialization, rather than allowing the submitted certificate to choose its task;
- directly recaptures exact saved acquisition, parameters, CDF, moments and work counters;
- verifies the ordinary Gaussian comparator is not handicapped.

The two m=512,p=4 cases read 1,023 energy monomials and **523,776 exponent entries** each. With initial z=e1, beta=kappa=1, clamp positions (-1,0,1/2), durations (1/3,1/2,2/3), and threshold64, both return EXACTLY the same rational CDF interval, displayed as

    [0.09834889399763794, 0.09834889400961049].

Its exact width is below the requested 10^-10. The cases differ in interaction coefficient 20 versus 10^100 and tangent weight 1 versus 10^80. Their raw hashes and coefficient acquisition differ and are separately bound; equal scalar output does not mean those costs were skipped. Each has 1,799 guarded products, seven exponential calls, 283 Taylor terms and 16 total Poisson-mixture iterations. The separate u0=256 author replay pays 842 Poisson iterations and 6,659 guarded operations, so large noncentrality is not hidden as constant work.

## 1. The actual kinetic model and global lift

The mathematical generator is not determined by a potential alone. Its transverse tensor is

    M(z) = zz^T/(p^2 U(z)) + T(z),

with matched divergence-form drift `-M grad(vU) + beta^-1 div M`. Omitting the divergence drift changes the energy process. The source explicitly declares this engineered tensor and the complete-pair tangent program; the finite consumer authenticates that program syntax, not an unknown physical device or a previously supplied Euclidean process.

Euler's identities give

    div M_rad = (m+1-p)z/(p^2 U),
    M_rad grad U = z/p,
    grad U^T M_rad grad U = U,
    (div M_rad).grad U + M_rad:Hess(U) = m/p.

For the full tangent component, `T grad U=0` identically implies both zero direct energy noise and

    (div T).grad U + T:Hess(U) = 0.

No conditional average or mixing limit appears. The explicitly chosen radial Brownian motion gives energy noise sqrt(2u/beta), independent of the longitudinal Brownian motion. Thus the full projected generator is exactly

    beta^-1 f_yy - v'(y)u f_y
      + (alpha/beta-v(y)u) f_u + (u/beta)f_uu,
    alpha=m/p.

The all-start path-law conclusion is justified by local strong uniqueness and the global join, not merely a formal equality of stationary densities. It applies to every positive-energy initial full state and laws with the same (y,U) pushforward. Hidden angular histories need not mix.

For c=2kappa+1, W=1+y^2+cu obeys

    GW <= (2+c alpha)/beta-u,

because yv'>=-kappa and v>=1. Coercivity controls |z| by u; an upper spherical bound on homogeneous U, together with positive lower u, keeps z away from zero on stopped compact sets. Local regularity then excludes a separate angular explosion. The adapted transform Q=exp(integral v)u and time change ds=exp(integral v)dt/beta yield `dQ=alpha ds+sqrt(2Q)dB`, so 2Q is squared Bessel of dimension2alpha. The scale functions log Q at alpha=1 and Q^(1-alpha) above one exclude hitting zero. Combining the lower-bound stops with W excludes finite-time infinity escape. This includes the critical alpha=1 case, but not alpha<1.

The homogeneous energy pushforward has density proportional to u^(alpha-1); hence the projected Gibbs density is proportional to `u^(alpha-1) exp(-beta v(y)u)`. Its y marginal has integrable |y|^-4alpha tails when alpha>=1. Local divergence-form symmetry, the global conservative diffusion and finite Gibbs mass support stationarity, including the degenerate T=0 case. No mixing, ergodicity, bounded actuator or uniform ellipticity follows.

For fixed clamped segments the scalar CIR process similarly stays positive and nonexplosive; finitely many deterministic clamp switches do not change u instantaneously. The work at a switch is `(v_new-v_old)u`. The program does not perform that actuation or hide it as free heat.

## 2. Complete raw grammar, coercivity, rank and tangent certificate

The code scans the complete supplied energy list, every length-m exponent vector and canonical rational coefficient. It enforces:

- strict dimension and resource integers, excluding BOOL/float aliases;
- exponents from {0,2,4}, common total degree p in {2,4}, no duplicates;
- strictly positive listed coefficients, with zero terms omitted;
- a pure degree-p monomial for every transverse coordinate;
- exact bounded Fraction initial coordinates and exact computed positive initial U;
- the actual complete-pair tangent schema and a nonnegative canonical rational weight.

Thus every atom is nonnegative, and

    U >= d_min sum |z_i|^p >= d_min m^(1-p/2) ||z||^p.

This is precisely the corrected theorem premise. Positive pure terms alone would not protect against negative mixed terms; the parser rejects those. Nonhomogeneous, rotated/odd-exponent, missing-coercivity or unsupported positive forms can soundly return Unknown. The code acquires p and alpha and refuses alpha<1. Its CDF backend further refuses noninteger alpha; that is an implementation restriction, not a theorem restriction.

There is **no axis/basis finder here**. The distinguished macro clamp coordinate is externally declared, and the raw polynomial is the transverse U. This service does not inherit the prior robustness receiver's quadratic-null-axis acquisition claim or acquire a general physical mobility matrix.

For g=grad U, the complete-pair formula is

    T=c_t (||g||^2 I-gg^T),
    div T=c_t[Hess(U)g-(Delta U)g].

It follows from all X_ij=(partial_j U)e_i-(partial_i U)e_j. Those fields are tangent and divergence-free; the summed divergence expression and cancellation are correct. Euler gives z.g=pU>0 away from zero. For c_t>0, T has kernel span(g), and the radial term is nonzero on that kernel, so M is SPD at every z!=0. When c_t=0 the code explicitly reports `transverse_SPD_away_origin=False`; it admits the valid rank-one lift, not a false full-SPD claim. Arbitrarily small positive tangent weights do not supply a uniform ellipticity bound.

The complete-pair formula is legitimate succinct generator input, not a secretly precomputed m-by-m matrix. Actual gradients, Hessian/divergence, noise projection, stiffness and full-state actuation remain real costs outside this scalar query. The full raw polynomial and tangent program are hashed. Here energy-list order is part of the program hash: reordering an identical polynomial preserves exact U but changes the bound raw program. This is stricter representation binding, not mathematical inconsistency.

## 3. Fixed protocols and finite Gamma-Poisson enclosure

The scalar autonomous Y/u dynamics do NOT have a frozen-y transition at finite time steps. The executable correctly restricts its protocol to a finite list of exact rational positions and strictly positive durations, with no adaptive/state-dependent callback or feedback field. Each v_j=1+kappa(1-y_j^2)^2 is positive.

Ordinary CIR semigroup composition gives

    E_new=e_j E_old,
    B_new=e_j B_old+(1-e_j)/(beta v_j),
    e_j=exp(-v_j t_j),

and terminal Laplace transform

    (1+B theta)^(-alpha) exp[-E u0 theta/(1+B theta)].

The mean and variance are E u0+alpha B and 2EBu0+alpha B^2. The direct Poisson-Gamma mixture has lambda=E u0/B and integer shape alpha+N. These are standard noncentral-Gamma/chi-square formulas, not a new stochastic engine. The independent protocol check uses the closed product E and sum of each segment's b times all subsequent e factors, rather than merely repeating the implementation recurrence.

At dyadic scale S=2^P, every positive interval product or rational scaling is rounded outward by integer division. For exp(-x), the implementation reduces to 0<=r<=1/2, encloses a positive Taylor sum for exp(r), and stops only when the next term upper is at most1/S. Because subsequent term ratios are at most1/2, adding2/S encloses the entire remainder. Reciprocal endpoints are reversed correctly, and each scaling square retains all interval error. Clipping exp(-x) to [0,1] is sound. No floating transcendental value contributes to a proof endpoint.

The outward propagated E/B intervals give

    lambda in [Elo*u0/Bhi, Ehi*u0/Blo],
    x in [threshold/Bhi, threshold/Blo].

The mixture CDF decreases with lambda by Poisson-increment plus exponential-summand coupling, and increases with x by CDF monotonicity. Hence evaluating (lambda_hi,x_lo) below and (lambda_lo,x_hi) above is sound even though E and B are correlated. Positive B lower and positive Poisson seed lower are required; underresolution is Unknown rather than an implicit exact zero.

For a fixed corner, the code's gamma prefix initially contains terms0 through alpha-1. After mixture term n, updating the prefix by term alpha+n correctly produces the next shape. All Poisson/Gamma terms and products are outward, nonnegative, and clipped using valid probability bounds. If mass_lo is the sum of retained Poisson lower weights, then

    true omitted mixture <= true omitted Poisson mass <= 1-mass_lo.

This is a rigorous full tail, not an empirical convergence heuristic. The two corner tails each satisfy the requested-width/8 cutoff, while the final **entire CDF interval** is separately required to have absolute width at most the external request. Protocol uncertainty, all rounding and truncation are retained in this final test. The independent noncentral reference uses direct rational factorial sums and separately bounded exact exponentials, including its complete omitted probability mass.

## 4. Error and cost scope

This is absolute probability accuracy only. The independent tests confirm a sufficiently rare threshold can legitimately produce lower endpoint zero while satisfying the requested absolute width. That is not a relative rare-event guarantee or an informative positive lower probability claim. Large noncentrality, poor fixed precision or a tight final width can force Unknown.

The raw scan is O(number of terms times m), and hashing scans the raw program again. Initial U evaluation uses at most p support multiplications plus one sum per term; identifying the support still reads every exponent. Positive raw coefficient bits, tangent-weight bits, initial-coordinate bits, protocol segments and task rational sizes are bounded. The aggregate energy-coefficient ledger excludes the separately individually bounded tangent weight and initial coordinates; it should not be read as all serialized input bits.

`RationalBudget` guards initial-energy products/additions conservatively. The fixed engine counts/guards products before executing them. `largest_guarded_product_bits` is a product-operand proxy, not peak process memory or a universal bound on every addition, denominator, division, low-degree protocol calculation, reciprocal, final moment, or serialization intermediate. This limitation is explicit in the source costs; ordinary Fraction/serialization work is not omitted from the scope merely because it is not in that counter.

All relevant loops are finite: raw terms/dimension, protocol segments, exponential scaling/Taylor budgets, alpha-dependent prefix length bounded by the admitted dimension, Poisson series limit and product-operation cap. The cdf engine costs O(alpha+retained mixture terms) per corner plus exponentials/protocol operations, with bit complexity and precision retained. It is not constant-cost in noncentrality, arbitrary precision, or arbitrary physical accuracy.

## 5. Receiving, adversarial checks and API boundary

`verify` recomputes from the raw model and original external task. It strictly binds schema, complete task, complete acquisition, operation, exclusions, mixture law and total duration; every exact terminal CDF/mean/variance endpoint; and every segment's v,duration,E,B endpoints. Independent attacks tested all these fields, not merely selected headlines. A different tangent program or energy input cannot reuse a certificate even when the scalar law would match. Certificate-supplied tolerances cannot override the original request.

Work counters, seconds, display values and extra outer fields are deliberately not authenticated proof fields. The independent suite recaptures the saved work by actual execution rather than interpreting verifier acceptance as authentication of arbitrary submitted diagnostics. Consumers must use exact bound fields, not modified displays or extras.

This is a Python callable interface, not a hostile-stream JSON service. Missing mandatory arguments or unsupported keyword names have ordinary Python argument-binding errors outside the signature; admitted malformed raw/task/certificate values fail with Unknown rather than false PASS. Resource failure is a refusal, not a proof of physical impossibility. Fixed-precision inability to resolve a positive Poisson seed and insufficient operation/series/bit budgets were exercised.

## 6. Comparisons, corrections and excluded upgrades

The strongest ordinary comparator gets the same raw model, protocol and scalar numerical engine. Gaussian energy already closes under an appropriate constant isotropic mobility; independent checks reproduce exactly the same scalar CDF for Gaussian/quartic inputs with matching alpha,u0. The source retains ordinary thermostat, pointwise Markov-function closure, tangent metric-design and noncentral-Gamma machinery. There is no asserted new CIR algorithm, generic projection theorem, priority conclusion or independent algorithmic separation.

The real limitation of Euclidean kinetics is correctly demonstrated: for U=z1^4+16z2^4+z3^4+z4^4, e1 and e2/2 both have energy1 but |grad U|^2=16 versus64 and Delta U-|grad U|^2=-4 versus-16. Their ordinary Euclidean instantaneous energy laws differ. The engineered mobility is substantive new model information, not a free consequence of known energy or Gibbs data.

The first theorem's missing mixed-coefficient sign restriction and the v3/v4 citation mismatch were corrected before this freeze and preserved. The final source points to the separately checked v4 covariance-design passage. This audit relies on the self-contained mathematics and trusted source-bound prior receipt; no external source retry or new historical-priority search was needed.

The theorem's all-start projected path-law identity does not by itself compute autonomous first-passage probabilities or mean hitting times. Nor does the fixed-clamp Laplace transform extend unchanged to random state-dependent protocol parameters. No feedback-control robustness, physical field acquisition, physical clamp, full dynamics simulation, chemical/biological operation, equipment, publication, outreach or purchase occurred. Earlier conductance and latency packages retain their own exact scopes.

## 7. Preservation and reproducibility

Receipt directory: `audit_kinetic_service_whole_20261031_2153/`.

- Run `python -B check.py` in `clean_replay/` for the complete author replay; it writes only that copied report.
- Run `python -B independent_audit.py` for the 1,152-check independent audit and actual saved-case recapture.
- `hash_verification.json`, `final_input_recheck.json` and `earlier_archive_preservation.json` bind untouched inputs.
- `initial_command_scope_error.json` records one resolved launch error exactly: a mistaken cwd made `../author_replay_stdout.txt` target `producer-workspace/author_replay_stdout.txt`, and the filesystem rejected that out-of-workspace redirection before Python could execute. Only hash verification/copy creation had completed. The denied target was not retried or escalated; the intended in-workspace clean-replay directory and logs were then used successfully. There is no remaining blocker or uncertain execution.

The audit manifest binds this review, tests, results, original-input recheck and logs. Frozen originals, corrected-history artifacts and the earlier robustness archive remain unchanged.

**Conclusion:** the exact homogeneous engineered kinetic lift now feeds a genuinely finite, outward, externally received fixed-clamp energy-CDF operation. Its mathematical success does not authenticate the special tensor in an unknown physical system or solve autonomous latency, adaptive control, or relative rare-event accuracy.
