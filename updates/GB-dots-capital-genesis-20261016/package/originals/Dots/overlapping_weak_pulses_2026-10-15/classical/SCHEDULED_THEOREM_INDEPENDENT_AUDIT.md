# End-to-end independent audit: scheduled finite-duration memory

2026-10-15 20:40 UTC. Reviewed SCHEDULED_FINITE_DURATION_MEMORY_THEOREM.md together with the global moment/locality proof, independent quantum subset audit, finite-duration proof and audit, and local-stochastic proof and independent audit.

## Verdict

PASS, conditional on the exact ideal-control, reserved-support, common-dilation/deletion-stability, initialization and deterministic timing premises, and the named original deterministic contour and memory imports. The composed argument does not require chronological Fourier labels, iid domination, commuting shared-bath channels, or an atomic post-error pulse. It concerns finite weak pulses under the specified qualified model and pointwise deterministic-time recovery.

The combined draft closes the earlier open *interface* gates for this restricted model: its additive/deletion-stable full dilation supplies uniform global-character subset effects, and its strict clean-patch premise supplies global completion-time support histories. This does not prove those premises for arbitrary hardware or arbitrary controllers. The separate norm-only restricted-amplitude route remains outside this theorem and open.

Two notational clarifications requested during review were verified resolved at 20:42 UTC: Section 3 now handles CSS sectors by separate estimates and a union bound, and Section 4B includes the independent unselected-seed averaging weights/records in the full Kraus notation. The draft also explicitly confines every bad attempt's memory action to its declared total interval, excluding uncharged delayed tails. No outstanding clarification remains from this audit.

## 1. Conditioning, randomization and actual channels

Fix a deterministic T. Condition on h containing only exogenous starts and noise. This fixes the geometric clean/completed set independently of quantum input and generated outcomes. Fourier-transform only the independent seeds attached to that set. Fix the other independently sampled seeds during the uniform quantum calculation and average them afterward. Pending wrappers are not completed or assigned small-action characters.

For a selected set S, the full-joint inequality is

    sum_(chi nonzero on S, alpha) K_(h,chi,alpha)^dagger K_(h,chi,alpha)
      <= a^(2|S|) I.

Here alpha includes ordinary physical/dilation outcome indices, and either includes unselected-seed mixture weights or is accompanied by their explicit independent average. Applying a CPTP final decoder and summing its index does not change this effect. Fixing an unnormalized alpha is permissible in the support algebra, but no normalized endogenous branch is used for this probability inequality.

Taking expectation in any joint input density operator gives the microscopic subset probability hypothesis conditional on h, with p=a^2. On nonselected starts define the mark to be zero. A subset containing such a start has probability zero; an all-selected subset obeys the displayed bound. Averaging unselected seeds preserves it. Consequently it is a uniform full-primitive subset bound for all finite subsets of the canonically indexed parent starts, including h-measurable subsets.

This is an instrument on the full experiment's averaged channel, not an online measurement protocol. Final Fourier labels must remain unavailable to physical control. The independent frame initialization and common deletion-stable dilation are essential; an inaccessible seed register alone would not excuse hidden frame-dependent control.

## 2. Why the support certificate matches these global records

Only bath-independent clean correction gates are moved to starts. Joint commutation is valid because their data and private ancillas are disjoint from every intervening operation, and they act as identity on the shared bath. Their exact completed C_i action includes the inactive branch, and their private outputs are discarded/reset as stipulated.

For the finite weak pulses, no joint channel is moved. Within a chronological Dyson/Pauli expansion, memory factors belonging to a clean pulse commute past intervening memory factors on disjoint full supports. Their bath coefficients remain in their original chronological order. After collecting just the memory factors at that pulse's completion, global Fourier projection fixes the product Pauli's character. Equal-character patch Paulis differ by a stabilizer because detection is complete and the patch has no logical Pauli. On each definite-syndrome orbit this stabilizer contributes a scalar, so a fixed representative suffices. The trivial representative is identity.

This gives one legal local support record per global character tuple, simultaneously for every term and all physical Kraus indices. Arbitrary bad gates remain local Pauli expansions. Continuous bad interactions, when admitted, are handled termwise by their locally supported, convergent finite-horizon Dyson expansion; no bad overlap component is contracted. The same guard excludes every possible bad birth time in an attempt's interval, so no gate-count multiplier is needed.

The full reserved duration includes correction, frame insertion, weak pulse, and completed removal. The reservation includes entire check and randomizer support, not just the nominal error patch. An uncharged memory coupling in H_0, or a correction projector touching a clean patch from outside its reservation, would break this argument. Section 2.3 of the draft explicitly excludes that loophole.

Skipped reference starts perform only the atomic envelope map sat_S composed with F. The physical chain does not receive a fictitious correction. This envelope map dominates its old input, so omissions do not invalidate support containment or retained-rate clock certificates. Physical topology changes only through actual bounded-support terms and exact corrections.

## 3. Probability constants and parameter order

For a guarded slab, original parent starts are counted before selecting clean attempts. The candidate count mean is at most

    mu=kappa N(Delta+2tau).

Conflict and external-noise flags use the full primitive windows and the enlarged patch geometry. Distinct points of one Poisson stream are included in the ordered-pair conflict estimate; self-pairing a point with itself is excluded. Pending flags are localized to each slab's candidate window intersecting [T-tau,T]. No global terminal event is reused across every slab.

Complete primitive packets can be colored using a fixed Q independent of L and b. On a separated color class, base indicators and candidate counts belong to independent packets, while mark probabilities are paid for jointly using the conditional subset effect. Within a packet, a base indicator need not be independent of its candidate count. The assignment expansion chooses one contribution per site, so it gives d0+a^2 mu per site without this false independence assumption. The largest color class supplies

    q=(d0+a^2 mu)^(1/Q).

The theorem uses the full-primitive, rather than clocks-only, hypothesis, so the stronger formula is justified. It does not use the earlier iid domination tolerance. The correct smallness test is d0+a^2 mu<=q_star^Q.

Set x=kappa tau and y=nu/kappa. The exact raw contribution beyond delta_ideal is

    F y(Cb+2x)+Nx[2D(Cb+2x)+1]+Na^2(Cb+2x).

For 0<=x<=1, the difference between A0 y+B0 x+C0 a^2 and that expression equals

    2(1-x)[F y+2NDx+Na^2]>=0.

Thus all three constants in Section 3 check exactly. delta_ideal must contain only slow and fast flags; external noise is already paid for in F nu. Cb>=1 and x<=1 ensure tau<=Delta, as required for the fixed spacetime packet degree.

Choose the coarse geometry, eroder/connectivity, Q and its contour tolerance before b. Fixed fine patch enlargements can be bounded by a fixed coarse enlargement for all b>=4. Increasing b then suppresses slow/fast errors without changing Q or the coarse rule. N and F may grow with the chosen b and are fixed afterward. This makes the order noncircular. It supplies existence constants, not useful numerical rates.

For fixed a,nu,tau, the displayed unconstrained optimum of the rate-dependent pair is correct. If a itself depends on tau in an implementation, that relation must be imposed when choosing physical parameters; the theorem does not treat such parameters as independently tunable hardware knobs.

## 4. CSS sectors, contours and torus transfer

A precise economical convention is to apply the same uniform LS estimate separately to each CSS sector, with per-sector slow/fast delta_ideal and conservative N,F including both sectors' interfering gadgets. Define success as both sector no-escape predicates. Union bounding their failure probabilities only changes the prefactor A. Their marks and primitive clocks may be correlated across sectors. Alternatively a sector-coordinate packet graph is valid after its degree and ideal-flag bookkeeping are explicitly adjusted. No cross-sector independence is needed.

For each sector, the correlated contour proof controls a disjoint contour family by the probability of its union of distinct sink deaths. The imported embedding property makes sinks distinct within each contour; disjoint image supports make them distinct across the family. The audited edge/support conversion ensures exponential enumeration in embedded support size even with noninjective non-sink embeddings. This replaces the relevant probability step of the contour-chain proof, rather than invoking the iid HT corollary for a correlated field.

The torus adapter copies actual coarse flags in a deterministic injective witness patch and sets all other flags to zero. This preserves LS. It need not reproduce a valid microscopic protocol outside that patch. Closed zero ancestry makes the witness persist in the copied cold process. The anchored bound and union over prospective anchors give the finite-horizon escape estimate. Whole-slab coverage and accumulated homology then apply to every supported history, including coherent sums via the common decoder.

## 5. Input-independent CP good map and final bound

For each h and final global character tuple chi, define G by the fixed robust no-escape support predicate (both sectors). It is independent of input state, bath coefficients, unselected-seed values, and any analysis coupling. Its permitted support record includes all bad-attempt patches and omitted starts. Every term of every K_(h,chi,alpha) with G=true is corrected by the same decoder.

Therefore every selected recovered Kraus operator is I_logical tensor a bath/auxiliary operator, and summing these actual Kraus maps gives Good=Id_logical tensor Lambda_g, with Lambda_g CP trace-nonincreasing. The complementary map Bad is CP. The classical bound holds uniformly over all joint input states, hence controls Bad's effect in operator order. Trace preservation forces that effect to have form I_logical tensor D_B. Completing Lambda_g by a CP bath map with effect D_B produces a CPTP comparison channel and diamond distance at most twice the failure bound.

This argument uses a complete Fourier-changed Kraus family for the actual averaged finite-horizon channel. It does not select signed expansion terms as outcomes or normalize the good map. It also does not assert a physical rare-error mixture.

The constants can absorb both the sector union and CP factor two. The bath comparison map may depend on L,T. The result is pointwise for each fixed deterministic T because the selected frame set and pending classification depend on T. It provides neither a simultaneous physical intermediate Pauli trajectory nor an adaptive stopping-time estimate.

## Final boundary

The theorem is a restricted scheduled model with exact completed corrections, exact private frames and resets, exogenous Poisson starts, fixed reservations, a qualified finite-dimensional additive common dilation, and ideal encoding/readout. Those are substantive retained premises. The audit establishes consistency of the mathematical composition under them; it does not establish autonomous timing hardware, noisy controls, arbitrary continuous-bath robustness, practical thresholds, novelty, or a physical Lindbladian realization.
