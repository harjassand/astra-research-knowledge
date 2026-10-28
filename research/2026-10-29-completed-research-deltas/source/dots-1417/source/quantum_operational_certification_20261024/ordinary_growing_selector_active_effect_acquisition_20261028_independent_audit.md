# Independent full-source review: growing-selector active effect acquisition

28 October 2026. Auditor: `producer-workspace/audit_algebra_extraction`.

**Received source:** `ordinary_growing_selector_active_effect_acquisition_20261028.md`, SHA-256 `136c4f8a83c81ad28f097f3f35adaf1299b0113d4435e860be119ca0668ed202`.

**Verdict:** received for the actual reset Bernoulli quadratic interface and the explicitly stated common-algebra composition. No unresolved mathematical or finite-protocol gap remains. The exact-sqrt alternative and any later matrix-Bernstein/rate improvements are NOT substituted into this received protocol.

## Independent canonical derivation

`growing_sphere_loewner_selection_independent_derivation_20261028.md` gives the complete independent proof. It uses the manuscript's rational BINOMIAL C, actual normalized-Cz input and s=||Cz||^2 weight; it does not mix them with exact-B^(-1/2) query definitions.

1. The basis/sign mixture has the required real projective second/fourth moments and can be sampled without enumerating its exponentially large formal support. T(z) satisfies E[(z^TFz)T]=F and ||T||F^2=L_m=m^3(m+3)/4.
2. The finite rational series gives0<C<=B^(-1/2), tail<=1/16,49I/64<=CBC<=I, and C^(-2)<=2B. C is a polynomial in B, so the commutation needed for these bounds is actual, not assumed for an arbitrary approximate inverse. The matrix floor is chosen by the learner, not imposed on the source or on A.
3. With actual Bernoulli y at normalized Cz, E[y s T]=CAC exactly in the finite-control reference model. On a good prior envelope, its centered Frobenius variance is at most L_m/tau. This is the essential inverse-tau rather than inverse-tau-squared variance bound.
4. Batch size ceil[2304L_m/(tau c^2)] gives radius c/12 failure at most1/16. The FIRST batch mean with a strict-majority2r-neighborhood, including itself, is within3r=c/4 whenever a majority is good. All tests use exact rational squared distances; no numerical boundary separation is assumed. With the displayed odd b, adaptive first-failure union bounds cost at most beta.
5. Exact rational reconstruction and largest-dyadic whole-update rounding give A+(c/4)B+tau_next I<=Bnext<=A+(7c/4)B+tau_next I. The looser2c coefficient closes A+tau I<=B<=aA+2tau I with a=1/(1−2c). Exact PSD accept/abort tests are physical on every history and pass on every good history. Rounding resets stored bit length; rational Schur elimination can test PSD in polynomial time without enumerating all principal minors.
6. The final gap-free Rayleigh slack tau_J/2 gives p<=a lambda_min(A)+(3/2)tau_J, with a<=1+gamma/7. The count sum is at most b[J+9437184L_m/(gamma^2 epsilon)]. Aborted histories may stop early but no executed observations are erased.

The original concern about bad learned-whitening fixed points is resolved by this UNIFORM Loewner invariant, starting from the known global effect bound A<=I. It is not resolved merely by finding a stable empirical sign or by assuming a narrow good region has been explored. The result depends essentially on the known PSD-quadratic family over the entire real sphere.

## Native controls and bit accounting

The source fixes the largest permissible dyadic grid explicitly. C's degree is O(tau^(-1)log(1/tau)); this classical work is paid rather than described as logarithmic. Its rational coefficients, products and inverse have polynomial bit complexity because every accepted B has a bounded dyadic representation and C has a known positive floor. Selected batch means obey a deterministic all-history norm cap, so failed statistical histories do not cause unbounded numerical work.

The known normalized rational directions can be prepared with finite paid amplitude-synthesis circuits. They are not supplied unknown states or free arbitrary rotations. Dimension m uses ceil(log2 m) selector qubits but generally O(m) known two-level rotations before routing/precision overhead. The finite sampler's rejection/abort coupling and all gate/input/transcript errors belong to one operational discrepancy budget allocated over a fixed complete horizon, including the final payload.

The displayed primitive random-bit formula counts only its own design draws. The final source correctly charges the additional m-anchor, logical-sign and global-Clifford randomness of full decoder acquisition separately within the SAME operational budget. No entangled reference is retained through the unknown source.

## Growing-anchor common-algebra composition

I checked Section7 independently rather than assuming the old four-anchor theorem is unchanged:

- For a positive real matrix-valued quadratic, scalarization gives G(x)<=m Gbar. The decoder regret multiplier is m, not4.
- This multiplier is genuinely sharp for actual Bell regret. With G(x)=|x><x| and identity logical noise, a gauge-controlled logical-Z decoder has maximum regret1 but anchor-average virtual loss1/m.
- In fixed-gauge nonnegative scalar quadratics, a perfect encoder yields at least1/m aggregate visibility; nonperfect visibility contributes its ACTUAL value divided bym. For general matrix-valued gauges, a perfect branch does not force a positive margin on other gauge sectors. The source keeps this distinction explicit.
- The margin and weighted proxy-tail assumptions are with respect to the NEW m-anchor rho. A former four-anchor weighted norm cannot be silently retained. The received state-independent unitary locality bound does imply the new weighted promise without a further gauge assumption.
- The selected eta=epsilon/(4096m q A_geom) gives statistical decoder regret225epsilon/8192<epsilon/20 and structural floor1980m q A_geom tau^2/kappa. Fine Bures tolerance mu=kappa^2 eta/512 and every inherited acquisition cap use this new eta.
- For the frozen receiver, the global ordinary test has p=[2^q/(2^q+1)]ell. Passing the primitive tolerance with this factor times epsilon/8 pays the Bell-loss conversion. Decoder failure<=epsilon/16, selector failure<=epsilon/16 and whole-process discrepancy<=epsilon/8 leave ample reserve in the stated final bound. The receiver is frozen before selector learning; A is then fixed conditionally even if acquisition history was random.
- The complete source ledger REPLACES the old selector learner by T_max, includes all decoder training and one final payload, and charges q logical plus ceil(log2 m) selector input qubits per call. For finite-time locality, replacing q by m q in the conservative width-cap logarithm is a safe (loose) transfer, retaining the resulting4^w. It is not a fixed-width or linear-m/q reliability claim.

The strongest equally informed conventional learner receives this same active effect-tomography method. This receipt makes no claim of quantum advantage, optimal m/gamma exponents, generic circuit-encoder optimization, empirical source-family validation or unknown-environment reconstruction.

## Exact checks and provenance

`growing_sphere_loewner_selection_independent_check_20261028.py` verifies exact design moments and rational-C laws for m=1,...,5, including noncommuting A/B cases. It checks54 prescribed rounded Loewner updates,51 noncommuting with A; five FIRST fixed-radius-majority cases; six dyadic-cap cases; exact PSD-guard examples; and sharp m-anchor regret fixtures. These are analytical matrix tests, NOT sampled or synthetic count-acquired performance claims.

A Python/SymPy Boolean-summation error while aligning the fixed-radius test was repaired by an exact Boolean-to-integer cast, without changing any matrix or threshold. The prior JSON was not used as evidence for the changed test. The preserved debug note documents this failure. The corrected script then completed twice under fail-fast shell execution and wrote byte-identical fresh JSON.

Zero source calls, RNG draws or acquisition simulations occurred. All bound manifests of the governing approximate-local and finite-time corollary receipts were reverified, as were the independently received current finite-controls bindings. The companion receipt binds this source, independent derivation, exact evidence, debug note and dependencies. It does not import the forthcoming statistics receipt, avoiding a circular dependency. Earlier received sources remain unchanged.
