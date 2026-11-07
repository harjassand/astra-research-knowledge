# Physical nucleation: residence certificates and a waiting-time law

**Latest lifecycle and availability, 7 November Brisbane:** all three current same-warm successors are POSTED ONCE/START CONFIRMED by separate dispatcher receipts: P14be18304, P2e0144bad and P3ce8eed3e. Exact1967-character P1 and2524-character P3 visible bodies matched. P1 begins current-source review/endpoint selection with no final question visible; P3 begins lower-cost calibration acquisition/maintenance with physical output retained. Starts are not new science or policy gains. Both completed returns retain NEW provisional correctness-assumed70–80, earlier frontier75–85 unchanged. P1's ZIP remains transfer-unconfirmed/held, no retry; P3's broader control programme remains unfinished. No scientific handoff is pending. Both traces/prior captures are staged; Stickies uncertainty is cleanup only. Capital sends no prompt/recovery; all source/N1683/Sol/Dots/team/resource holds remain.






**Availability correction:** matching expanded user-visible activity is now staged: [trace](activity/p2_nucleation_law_20261107_return.visible-activity.txt), [updated return](P2_NUCLEATION_LAW_20261107_RETURN.txt) and [pre-recovery capture](P2_NUCLEATION_LAW_20261107_RETURN.pre-recovery.txt). Earlier missing-activity/locked-access descriptions below refer to the original handoff. This correction does not revise scientific scope, assessment or credit. [Recovery index](../2026-11-07-visible-activity-recovery/README.md).









The finite-temperature two-dimensional Ising phase-switch predictor remains **UNRESOLVED**. This return supplies a quantitative connection from physical residence certificates to the complete normalized waiting-time law, a rational certificate processor, and explicit counterexamples to two proposed shortcuts. Physical capacity and global residence acquisition are still missing. The supplied **NEW provisional correctness-assumed consequence is55–65**, for the specialized weighted-residence-to-full-law bridge, conditional rational CDF processor and scoped local-histogram obstruction. Generic NBUE/equilibrium-transform/Stein exponential approximation is classical and receives its primary credit. Earlier completed chain70–80, effective-law75–85 and global programme frontier75–85 remain unchanged. Scores are ordinal/nonadditive, with no activity/source-availability penalty, no loss of accepted science and no90+ claim.

Read the [complete proofs and costs](package/RESEARCH_REPORT.txt), [continuing endpoint](package/ENDPOINT.json), [failure families](package/FAILURE_OBJECTS.json), and [exact prompt, full response and opening explanation](P2_NUCLEATION_LAW_20261107_RETURN.txt). The [original ZIP](original/Nucleation_Law_20261107.zip) and all ten members are published unchanged. [Source provenance](SOURCES.json) records publication scope and lifecycle receipts.

## Governing endpoint

The requested operation predicts the physical first-passage time from all-minus to nonnegative magnetization for heat-bath dynamics on an explicitly counted square torus. Rational factors `u=exp(-2 beta J)`, `v=exp(-2 beta h)`, `0<u<=1/4096`, `u^2<v<1` specify the rates. Each site has its own rate-one proposal clock. The weak-field scale is `R=log(u)/log(v)=J/h`, with `C R <= ell <= R^p` in the stated nonempty volume regime. Target membership is directly tested; its exponentially many configurations are not supplied as a list.

The desired total cost is polynomial at each fixed admissible temperature in explicit input size, inverse accuracy, log inverse failure probability and binary query-time length, avoiding an exponential-in-R wait at fixed accuracy. Temperature dependence must be paid; fixed-temperature polynomiality does not imply uniform polynomiality in an arbitrary temperature encoding. The [earlier chain kernel and explicit finite-target construction](../2026-11-07-p2-rare-event-chain/README.md) does not supply the missing two-dimensional kernel or target representation.

## Completed construction, with conditional inputs

For a finite killed chain with `T=E_a tau_B` and the maximal-mean-start premise `E_x tau_B<=T`, define `d=1-E_a[tau_B^2]/(2T^2)`. The report derives Wasserstein distance at most `2d` and uniform normalized-CDF error at most `min(1,2 sqrt(d))` from Exp(1). The physical occupation identity is

```text
d = T^-2 E_a integral_0^tau_B [T-E_(X_s) tau_B] ds.
```

The attractive Ising process from all-minus has the stronger stochastic maximality needed in the source comparison. Two moments of an arbitrary distribution would not suffice. The report also gives the reverse convergence criterion, residual-life and factorial-moment bounds. Classical equilibrium-transform/Stein machinery receives its primary credit.

For an actual thermal core A and a clock of rate kappa active there, the accepted soft-source quantities are `C=kappa sum_A w(1-psi)`, `N=sum_(B^c) w psi`, `Q=N/C`, `Z_A=sum_A w`. Given valid certificates for core mean deficit D0, `C/Z_A<=U<kappa`, and the **global weighted exterior residence** `sum_(B^c outside A) w psi/N<=eta`, write `s=U/kappa`. The new sufficient bound is

```text
d <= min(1, eta + kappa D0 + U D0 (2-s)/(1-s)^2).
```

The accepted affine comparison `Q<=T<=(1+kappa D0)Q+D0` remains valid for every positive kappa. A bounded-lobe contribution does not certify the global eta; an unconditional Gibbs probability cannot replace weighted physical residence. The source clock choice `kappa=epsilon^2/(16D0)` has polynomial waiting scale when D0 is polynomial, **if** the corresponding capacity and global residence certificates are earned. For D0=0, the separate stated case applies.

[residence_law.py](package/residence_law.py) accepts already-valid rational Q bounds, D0, U, kappa and eta, and constructs mean bounds and a reusable CDF enclosure. It evaluates the exponential terms with rational intervals. The conservative processor bound is `2^40(B_enc+b+2)^12` bit operations, including certificate/query encoding and output precision. Binary time length is charged; it does not simulate to the query time. Joint validity probability transfers from the input certificates to the whole reusable enclosure without a union bound over queries. Additive CDF bounds do not promise relative rare-tail or instantaneous-hazard accuracy. The quantile formula is proved, but no separate quantile routine was executed.

The report also specifies a fully costed high-accuracy simulation fallback **conditional on future global exponential shape and mean bounds**. It pays discretization, truncation, finite-bit randomness and confidence. This auxiliary branch was proved, not implemented or run. It does not acquire those global bounds.

## Explicit failure families

The [failure objects](package/FAILURE_OBJECTS.json) preserve two distinct limitations:

- A three-state reversible birth-death family has vanishing capacity and zero core mean deficit, but two rare waiting stages. Its normalized law tends to a scaled shape-two Erlang law rather than Exp(1); global exterior residence remains non-negligible. No Ising embedding is claimed.
- For every radius r and repetition count j, explicit stripe pairs on side `ell=10(2r+1)j` have identical complete radius-r spin-pattern histograms and plus density 2/5, but different transition rates. The difference is `(m-2)j ell u^4 v/(1+u^4 v)`, where `m=2r+1`. The proof includes finite-time separation. This refutes exact strong Markov lumpability by those histograms. It gives no all-minus first-passage lower bound, significant-nucleation-current claim, impossibility of richer or memory-bearing representations, or unrestricted runtime lower bound.

## What the producer executed

[VALIDATION.json](package/VALIDATION.json) records standard-library exact rational checks from [validate_exact.py](package/validate_exact.py). A 3x3 torus is fully enumerated (512 states), reduced only by actual graph automorphisms to 13 transient orbits. Detailed balance, moment and source equations, occupation identities, affine mean comparison and defect bounds were checked. The two means are approximately 732.304 and 377405.714; their exact-moment defects are approximately 0.00350318 and 0.00000668670. The latter gives normalized-CDF error below 0.00518 using its **exact moments**; the soft-source certificates are looser. Both fixtures lie outside the governing large-volume weak-field scaling. Exact enumeration is not a scalable acquisition method.

The producer also checked several stripe radii/repetitions, the two-stage family and an exactly exponential case at query time `2^4096`. General scope comes from the supplied proofs. These are producer checks, with no Capital scientific replay, independent audit, physical run or practical advantage established.

## Missing operation and retained credit

The governing endpoint still needs a constructed, normalized critical kinetic law covering all significant configurations and physical current/residence through growth to the actual magnetization target, at polynomial relative acquisition cost. Restricted regular contours and bounded-neck repairs do not establish unrestricted principal-contour coverage or global exterior residence. Neither the mean predictor nor the full CDF predictor for the growing two-dimensional class is constructed.

[SOURCE_SCOPE.json](package/SOURCE_SCOPE.json) credits Pekoz–Rollin exponential approximation, Hoeffding concentration, algorithmic Pirogov–Sinai equilibrium work, classical homogeneous nucleation and the stated biased-initialization phase-ordering results. Their hypotheses remain distinct from the missing finite-accuracy kinetic operation. No historical priority, generic rare-event solver, practical speedup or unrestricted QUBO resolution is claimed. The [nine predecessor identities](package/PREDECESSORS.json), accepted chain prediction, earlier elliptic/response results and their open boundaries retain credit. Those predecessor archives are listed as preserved by the producer; this ZIP does not contain nine new archive acquisitions.

## Source availability and publication

The exact prompt, complete response and opening explanation are staged. The expanded visible activity remains in the predecessor chat and was not staged while native access was locked. This is an availability gap, not a scientific verdict or score penalty. Displayed duration is not compute accounting.

All existing source-original and transfer holds remain binding. Capital did not recover held attachments, use alternate originals, unlock the Mac, contact researchers or dispatch a continuation. Sol remains closed/held, Dots protected/unmessaged, and the three-role/resource limits remain. Publication preserves original bytes and improves source navigation; the full generated retrieval corpus is **not rebuilt**. [Packet README](package/README.txt) and [member hashes](package/SHA256_MANIFEST.json) are unchanged source records.

## Supplied assessment and continuation decision

The new consequence is lower than the complete earlier chain predictor. It does not supply the missing critical kinetic representation, normalization/capacity, global physical residence or growth through the actual magnetization target. The rational processor requires already-valid Q bounds, D0, U, kappa and eta. The accepted affine source join holds for every positive kappa; the new specialized defect bound separately requires U<kappa. The conditional high-accuracy simulation closure was proved but not implemented/run. Exact3x3 checks lie outside the governing growing-nucleus regime. The stripe family excludes exact strong lumping, without excluding weak lumping under the all-minus law, richer geometry/memory, or unrestricted prediction algorithms; its significant-current contribution is unproved.

The current U1722 capacity source at content_version e6c057db retains the original-archive hold and the accepted positive-field thermal core, regular-family loop and bounded-residence capital. Those positive results and holds are unchanged. Classical Stein/NBUE, equilibrium contour algorithms, nucleation and phase-ordering work receive their actual credit; no new operative Zenodo premise or causal source-order winner is reported.

The coordinator continues the same warm P2 toward its explicitly owned full two-dimensional operation, with route/representation choice. The distributional bridge and failed compression make that continuation potentially useful; they do not establish tractability, improved returns or permission to renew conditional closures indefinitely. Later actual construction and opportunity cost remain decisive, without a fixed quota or easier fallback. The previous prompt's factual reminder about unresolved two-dimensional N1722 may have anchored question selection despite destination freedom. Chronology and causal effect remain unestablished; warm history, task, sources and unknown effort confound attribution. A broad programme label is not enough to establish identical-target continuity or policy efficacy.

The exact2860-character continuation, SHA25632ae2f1c81dc389cc6c53f98ee59f9067866816ab50b4b53536627559e98023c, was handed once to the existing dispatcher. Actual POSTED ONCE/START CONFIRMED is supplied, native d3da0a7c-73d8-40c6-8aa9-7c82b00ff21c, with exact visible body matched. The start is not a completed predictor or scientific effect. Capital did not send it or change scientific assignments.

Later supplied result: [conditional block transport and direct-simulation limits](../2026-11-07-p2-nucleation-block-transport/README.md). The full physical nucleation predictor stays unresolved; this is not a general algorithmic hardness result.
