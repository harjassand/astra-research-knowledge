# Independent whole pivot-star review

31 October 2026. Reviewer: challenge_graph_profile_compiler. **Scoped mathematical and trusted-input research-constructor PASS.** Non-operational stochastic count-process mathematics only. This review is independent of the other helper's receipt; it does not accept the separate terminal-gap compiler by association.

## Frozen source and execution bindings

Full-read sources, hashes independently checked:

- `PIVOT_STAR_THEOREM.md`: `24166432f3f19f9fbb4891c20896b1c2c3e340d70420a7187592264f412b12cc`.
- `pivot_lift.py`: `69408dd5cf0235d4a92947696e5db505857062b42703e9cfbf1c1fdf2c91e519`.
- `pivot_lift_results.json`: `6880adc44888c88d67b706c2af6662bdcd361a9d175e11e450a05c56f16c1008`.

I ran the frozen demonstration independently into `/tmp`, preserving the author's artifact. Its entire JSON reproduced the saved hash exactly, including the 6,760 rational grid challenges. I also wrote and ran `check_pivot_independent.py`, with results in `pivot_independent_checks.json`. These challenge one-species cores with no stars, empty cores, fifth-order cores, no-zero cores, asymmetric positive rates, three rational t values, finite-layer and tail-boundary states, and rejection of unauthorized satellite immigration. They are finite checks, not the all-population proof.

## 1. Exact scope and graph acquisition

The theorem requires a separately weakly reversible non-null one-species core on the acquired pivot, both direct star channels for every satellite, and a residual list preserving BOTH pivot count and total population. Full reaction-graph weak reversibility is separately checked. A reaction is never classified solely from a desired drift sign. Null channels can be deleted, and parallel star rates are correctly aggregated.

The raw-list recognizer tries every coordinate and classifies every remaining channel. Its finite reachability routine checks return reachability of each complex edge. For a reaction enabled at a population state, any complex return path can be executed with the same nonnegative spectator population. Hence population transitions are reversible by actual directed paths, every reachable communication component is closed, and no lattice-only irreducibility claim is needed.

An empty non-null core makes total population conserved, so every reachable class is finite. With a nonempty weakly reversible core, the maximum source M is also the maximum of all complexes; at source M every non-null target is strictly lower. M cannot be zero in this case.

## 2. Corrector and boundary faces

For a>=1, the recurrence g(a+1)/g(a)=a/(a+c) is positive and rational at every integer. The harmonic-sum bound gives g(a)>=exp(-c)a^(-c), while g(a)<=1. Together with the independently positive g(0), this makes t^N g(a) normlike. For any t' strictly between 1 and t, exponential growth dominates the polynomial loss uniformly over a<=N, so V_t dominates a positive constant times (t')^N. The a=0 case is handled separately by g(0), not by evaluating a negative power of zero.

For a>=2, the forward-star ratio minus one is c/(a-1), producing c alpha a. The reverse-star ratio minus one is -c/(a+c), producing -[c a/(a+c)] sum_j beta_j b_j. At a=1 the forward channel is disabled and must be omitted. The source does omit it. At a=0 both star directions are disabled; choosing g(0) strictly larger than every t^v g(v) makes every enabled inflow contribution negative, uniformly in all satellite counts.

If no inflow exists, weak reversibility excludes any non-null core edge into zero as well. The face a=0 cannot leave through a star channel and all its remaining reactions preserve N. Its classes are finite, even if neutral reactions move satellite coordinates. The drift inequality is then used on a>=1 only. The frozen code's zero-face flag has this meaning, not an assertion that the whole face is one finite set or an absorbing singleton.

## 3. Exact all-population tail and finite layers

For a>M, the core ratios are finite rational products with positive denominators and limit one. At M>=2 the leading coefficient of P(a) is sum_{M->v} kappa [t^(v-M)-1], strictly negative. The added star term is only linear. At M=1, c is chosen so the linear coefficient remains at most -mu(1-1/t)/2 when satellites are present. With no satellites its coefficient is already strictly negative. Thus H(a) tends to minus infinity in both cases.

After rational cancellation, normalize the denominator's leading sign. Since H+1 is negative eventually and the denominator has positive leading coefficient, the numerator has negative leading coefficient. Every derivative of a nonzero polynomial eventually has its leading sign. Consequently doubling R eventually makes every shifted numerator coefficient nonpositive and every shifted denominator coefficient nonnegative, with positive denominator constant. This proves H(a)<=-1 for every real a>=R, not merely tested integers. Exact SymPy rational polynomial arithmetic constructs this witness; no floating root finder or empirical tail inference is involved.

For each of the finitely many layers 1<=a<R, the satellite drift coefficient d_a is strictly positive when satellites exist. The chosen integer B_a bounds the total satellite count for the exceptional layer. When B_a=-1 the whole layer is already controlled. With no satellites only one state per pivot layer remains, and B_a=0 is a harmless convention. The displayed C bounds V(H_a+epsilon) on every exceptional state, since N<=a+B_a there and the omitted satellite contribution is nonpositive. Therefore the global drift inequality is valid on the nonconservative part, with epsilon also limited by the actual zero-face quotient if inflow exists.

No polynomial bit-complexity claim follows from this terminating search. Large molecularity, small rates, large R, coefficient growth, and the finite-layer enumeration are paid.

## 4. Nonexplosion, recurrence, and stationary moments

The normlike drift bound implies LV<=C. Stopped Dynkin up to finite sublevel exit bounds its probability before any fixed time by a constant divided by the exit-level lower bound. Finite reaction lists have bounded increments and finite rates at every state; rates are uniformly bounded on finite sets. Thus explosion cannot occur either by escaping every sublevel or while remaining inside one. Arbitrarily high-degree neutral rates do not invalidate this argument: they contribute zero to LV and cannot create infinitely many jumps in a fixed finite sublevel.

Enlarging the finite set makes LV<=-1 outside it, giving a finite expected hitting time by the stopped argument. Within each closed irreducible reachable class, the finite-set recurrence criterion gives positive recurrence. Finite conservative classes are handled directly. Nothing here claims a single global irreducible class or uniform recurrence constants over all rate choices.

The exponential-moment conclusion does not use the invalid formal step integral LV=0 before establishing integrability. Localization of exp(epsilon t)V and Fatou gives P_T V<=rV+b, r<1. For phi_n(v)=min(v,n), invariance, Jensen, and this semigroup inequality imply integral[phi_n(V)-phi_n(rV+b)]<=0. These differences are bounded below by -b. Fatou then proves (1-r)pi(V)<=b, hence pi(V)<=C/epsilon. Taking a larger t than any desired exp(theta) and using the coercive comparison proves all finite exponential total-count moments on each invariant class. The no-inflow finite face has them automatically.

## 5. Executable scope and caught interface limitation

The program faithfully implements these identities on its declared trusted exact input contract: integer complexes and int/Fraction rates, rational t>1, and the constructor's own unmodified recognition result. Its helper `exact_generator` uses falling factorials, tests enabled channels, and compares exact rational values. Independent reruns found no arithmetic or orientation failure on that contract.

It is NOT a hardened public input parser or an independently supplied certificate verifier. In particular, `construct(rec,t=2.0)` is accepted and leaves a float parameter; `Fraction` can convert floating input rates rather than rejecting them, and the constructor trusts a mutable recognition record. I tested and reported this distinction. The author explicitly confirmed the trusted rational API scope and did not claim hostile-certificate validation. Python assertions must remain enabled for the research checks. No security, malformed-input rejection completeness, or provenance certification is granted by this receipt. A future external validator would need strict types and recomputation of recognition and witnesses.

The separate `compile_recurrence.py` dispatches to another terminal-gap route. I inspected its dispatcher for context only; this receipt does not verify that other theorem or route. A negative pivot recognition result means outside this sufficient recognition class, not nonrecurrence.

## 6. Strong ordinary comparison

The deficiency-zero baseline has the standard complex-balanced product-Poisson explanation. The concrete witness has incompatible complex-balance requirements: 0<->A requires pivot concentration one, while the leaf 3A requires two. That establishes non-complex-balance, not historical novelty or absence of all product-form/decomposition methods.

I directly inspected Hoessly's accessible primary Theorem 3 in *Stationary distributions via decomposition of stochastic reaction networks*, https://link.springer.com/article/10.1007/s00285-021-01620-3 . It requires component stationary factors that agree up to proportionality on shared species. Such compatibility is not acquired automatically from this raw pivot-star grammar. Hoessly--Mazza's primary abstract at https://arxiv.org/abs/1809.07361 confirms broad existing non-weakly-reversible product-form work; I do not infer its detailed applicability from the abstract alone. No exhaustive literature or novelty verdict is made.

The useful proved delta is a sufficient all-population rational Lyapunov construction without requiring stationary factors or a fast-fiber mixing oracle. It is still ordinary Foster--Lyapunov machinery once the correction is acquired. It proves neither general weak-reversibility recurrence nor a practical simulation advantage.

## Verdict

PASS for the exact restricted mathematical closure, classwise nonexplosion/positive recurrence/all exponential stationary moments, and trusted-rational research constructor. Keep the explicit boundary treatment, non-formal stationary-integrability argument, input-contract limits, and ordinary-method comparison attached to any downstream use.

Independent supplementary challenge binding: 666 checks; `check_pivot_independent.py` SHA-256 `d155c8217c8afb62259081125ea21f22521495f05fb75cfa3e824805e09f5eab`; `pivot_independent_checks.json` SHA-256 `70537b0c00190b650c02216e2322f61423bf7f2bf7be55bf9f19be51a194d65f`. Float acceptance is recorded as an interface limitation, not counted as an exact-arithmetic proof check.
