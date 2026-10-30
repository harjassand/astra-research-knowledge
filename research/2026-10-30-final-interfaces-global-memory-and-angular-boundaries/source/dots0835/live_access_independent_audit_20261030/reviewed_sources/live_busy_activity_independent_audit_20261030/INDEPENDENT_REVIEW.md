# Independent review: direct singleton BUSY moment on the actual native memory
2026-10-30. Reviewer: `challenge_live_busy_energy`.

## Verdict and exact source
**Scoped PASS for the direct full-Hilbert singleton-activity moment and the reference-stable, pointwise-in-time uniform exponentially small BUSY-density tail, on the SAME accepted unified native physical apparatus.**

Root source reviewed and copied verbatim into `reviewed_sources/`:

- `producer-workspace/DIRECT_SINGLETON_DERIVATION_V1.md`
- SHA-256 `3ecabba158a1c4457dd5bbba0b0cc0ec278eeb970674062ac5f779de4dd05658`.

The completing independent derivation is

- `CONSTANT_SINGLETON_BUSY_MOMENT.md`
- SHA-256 `4a7faab68ba000ef1a57a08c75bfae59ee9a518f6da821f75737ccf37e63eecc`.

The weaker fully inherited pair/singleton route is also independently derived in

- `DIRECT_FULL_HILBERT_BUSY_MOMENT.md`
- SHA-256 `72ab2a7ecfd48afbb98f5ca350b86c7fc54bfea3235d5df9dda8e4db135f1eae`.

This verdict covers the root source through its `Continuous joint noise and moment` section using the COARSE O(eta) noise bound. The root's optional O(delta eta) refinement is not needed and is not certified by this receipt. The final operational-use paragraph is conditional on its separately stated canonical-memory/forest-prefix/physical-handoff modules; this receipt does not by itself accept the full bare-DATA/readout composition.

## 1. Why the original proposal was needlessly difficult
The earlier root history-weighted candidate used controller-only history-pinched Xbar_h, guarded activity gates, a history exponential, and T_B. Its dirty drift needed new clean/dirty surgery and precise O(delta^2) versus O(delta) source control. That candidate is neither used nor retroactively certified here.

The accepted ORIGINAL full-Hilbert X_h already obeys cP_h<=X_h<=CP_h, L0*X_h<=-P_h, and commutes EVERY BUSY projector. Its possible DATA dependence on malformed histories is harmless when the raw factor is I. History pinching and DATA conditional expectation existed only to permit multiplication by a different DATA potential. Removing those unnecessary operations makes the direct physical activity theorem available without a transfer across dirty normalization.

I independently read the full activity receipt, the native manuscript, the unified-generator interface and the actual dirty owner-algebra sources rather than infer this from the accepted DATA-memory theorem. Dependency hashes are in `DEPENDENCY_SHA256.txt`.

## 2. Same physical coefficients are established, not assumed
The unified interface section 8 explicitly identifies the global BUSY L0 as setting only the first epsilon edge to zero while retaining later acquisition at the chosen fixed positive zeta, all NEW Ai-to-Q0 aborts, fast cleanup, the actual payload, and the full finite monitor generator. The polynomial X_h is constructed from this actual L0. The native manuscript section 5 restates the full-Hilbert witness BEFORE pinching.

The word `halted` in the root's L0 description is an analytical splitting, not a physical stop command. Actual evolution remains L_native=L0+epsilon V. The activity delta is an independent mathematical gate strength; it does not have to equal delta_mem=d_mem epsilon^2 in the DATA proof. A common sufficiently small physical epsilon and the minimum of the two permitted physical-noise thresholds satisfy both proofs. No later-zeta, abort, cleanup, or monitor parameter is retuned between observables.

## 3. Noncommuting product and the load-bearing fast remainder
The maskwise singular-value argument is valid and yields

    2c delta M <=logG<=2C delta M,
    M=sum_h P_h,

with full singleton coverage. It does not claim that Y is positive or replace log of a noncommuting product by a sum.

The fast remainder is NOT a generic O(delta^2)N estimate. Under exact finite-depth congruence the linear term is 2delta sum L0*X_h<=-2delta M. Every nonzero higher multiplication-superoperator word remains in the intersection of the active corners associated to its gate factors: the actual fast generator preserves these corner algebras. Locality makes each remainder cone finite, and incidence bounds how many cones contain a given anchor. Consequently the full second/higher-order remainder is bounded in Loewner order by C_F delta^2 M. A fixed sufficiently small delta absorbs it. The independent supplement states the finite-cone and corner argument in full.

This corner fact is the decisive difference between an earned constant-singleton theorem and the invalid shortcut of setting A=epsilon^{-2} in the old scaled-singleton theorem while ignoring its A-dependent constants.

## 4. Exact weak idle block and Young allocation
Each actual first-edge H_h has zero Ready_h/Ready_h block and commutes every other P_j. The full gate circuit commutes P_h, so the exact transformed contribution

    K_h=i[(Y H_hY^{-1})†-Y H_hY^{-1}]

has the same zero Ready_h diagonal. Bounded local cancellation gives ||K_h||<=C_W delta. Its BUSY_h diagonal, multiplied by epsilon, costs O(epsilon delta)P_h. Its cross block is paid by a fixed fraction of delta P_h and leaks only O(delta epsilon^2)(I-P_h). This is an exact block estimate, not an assumption of classical weak-transition rates.

After summing and choosing epsilon small,

    L_native*G <=[-a delta M+C delta epsilon^2 N]G.

There is no dirty flag term, no useful credit, no canonical safe-basin restriction, and no O(delta)N or O(delta^2)N scalar source. Full-Hilbert malformed DATA/workspace sectors are covered by the original witness and actual block algebra.

## 5. Noise, scalar moment and reference stability
The root's coarse noise estimate is valid via exact local congruence and its inverse, both CP but NONUNITAL. The transformed local map need not annihilate I; bound its cb norm directly. Finite-depth cancellation leaves only bounded cones, so the physical bounded-body incident-cb budget gives

    N_u*G <= C_noise eta N G.

The same argument retains the common bath and arbitrary reference: gates are system-only, joint local maps are bounded in cb norm, and bath-only terms annihilate the observable. The usual existence/normality assumptions on the actual CPTP dynamics remain required. This is not a representation-dependent bound on chosen Lindblad jump coefficients.

Set lambda=a/(2C), rho=C_native delta epsilon^2+C_noise eta. Then

    L_actual*G <=-lambda GlogG+rho NG.

For a normalized positive joint state, scalar spectral Jensen gives Tr(rho_u GlogG)>=x logx, x=Tr(rho_u G). No commutation with the state and no operator Jensen are required. All-ready initialization has x(0)=1, even with arbitrary DATA/reference/bath entanglement within that ready support. Hence

    logx(u)<=(rho/lambda)N,
    Pr(M>=beta N)<=exp{-[2c delta beta-rho/lambda]N}

at every u>=0. Taking epsilon and then the common permitted noise threshold sufficiently small yields a strictly positive exponent independent of N and elapsed time. The assertion is uniform at each time, not a bound on the event of any excursion during an infinite observation interval.

## 6. Independent diagnostics and evidentiary limit
`check_constant_singleton.py` and `constant_singleton_checks.json` preserve a 16-dimensional independent algebra fixture with three BUSY qubits and a shared auxiliary qubit. Its positive gate generators do not commute (commutator norm 0.18), but commute all BUSY masks. Across nine (delta,epsilon) choices:
- transformed weak idle-idle blocks and all-idle fast remainders are exactly zero numerically;
- the fast remainder divided by delta^2 M has norm about 9.53–10.42;
- weak norms divided by delta are about 5.54–5.57;
- the scalar remainder after reserving delta M, divided by delta epsilon^2 N, stays about 8.25–10.03;
- both maskwise exponential barriers hold to floating-point precision (worst approximately -2.3e-16).

These tests diagnose the algebra/scaling, not actual native absorption, a code family, or an experimentally validated device. The analytical verdict rests on the frozen accepted witness/block inputs and sections 2–5 above, completed by the independent supplement.

## 7. What is not accepted by this receipt
- No retrospective proof of the unnecessary guarded history/T_B drift.
- No need or claim to measure G physically; it is a proof observable.
- No assertion that every controller is idle, or that BUSY labels are independent.
- No infinite-time no-excursion claim.
- No automatic arbitrary-initialization bootstrap or arbitrary warm-state logical-memory theorem.
- No physical coupling/routing mechanism for quantum output, destructive-readout implementation, or live external-gate compatibility.
- No full bare-DATA decoding composition beyond the separately required canonical and prefix contracts.

The accepted controlled-retirement/readout constructions are preserved as fallbacks. This corollary removes the necessity of using a DATA-energy observable or a controller-erasure proof to establish sparse live BUSY masks; operational consequences must still use their stated output conditions.
