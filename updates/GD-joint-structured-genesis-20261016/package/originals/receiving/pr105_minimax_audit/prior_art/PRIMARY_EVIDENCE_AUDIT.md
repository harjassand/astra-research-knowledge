# Bounded primary-art verification

Checked 2026-10-16 against live primary HTML. Scope: the three specified papers only; no historical-priority clearance or independent verification of every theorem in those papers.

## Viola–Knill

Source: https://arxiv.org/html/quant-ph/0511120
Title: Random decoupling schemes for quantum dynamical control and error suppression. The page identifies PRL 94, 060502 (2005).

- Setting, source lines 40–47: arbitrary time-dependent drift; logical frame follows a known random control path; recorded control history permits returning to the physical frame.
- Theorem 1, lines 57–67: uniform random control, independence beyond a correlation interval, and a uniform spectral-norm drift bound yield mean pure-state error O(T Δt k²). The discrete realization uses equally spaced random bang-bang group pulses.
- Open-system setting and Theorem 2, lines 68–82: one joint system/environment evolution; the interaction Σ J_a(t)⊗B_a is uniformly norm-bounded. Its mean pure-state error is O(T Δt λ²). No repeated bath reset is assumed. The environment is purified for the pure-system-input error definition.
- Limits: this is a worst-input, control-averaged state-error bound, not an exact finite-action sector-endpoint minimax or selected-subset effect theorem. The formal irreducibility premise and later selective-decoupling discussion must not be silently equated with every two-sector interface.

## Santos–Viola

Source: https://arxiv.org/html/quant-ph/0511121
Title: Dynamical control of qubit coherence: Random versus deterministic schemes.

- Section II, lines 123–125: R protocol selects a π pulse or identity fairly at each prescribed equally spaced slot, including an initial random slot.
- Section III.1.1, Eqs. (11)–(17), lines 153–187: logical-frame tracking and cumulative toggle-parity signs.
- Section III.1.3, lines 239–243: the known control history permits deterministic frame return.
- Section II, Eqs. (1)–(3), and V.5: explicit time-dependent couplings to a retained quantum bosonic environment are studied.
- Limit: the detailed environment is a pure-dephasing bosonic model, not itself the arbitrary bounded joint-coupling theorem. That general bounded-coupling premise is verified in Viola–Knill above.

## Wang v2: precise correction needed

Source: https://arxiv.org/html/2610.01521v2
Metadata: https://arxiv.org/abs/2610.01521v2
Title: Continuous-Process Randomized Compilation for Quantum Process Tensors.

Sections III.2/IV.1 and Appendix I establish pointwise-covariant instruments, independent fixed-node frames and retained environment propagation. Section V.2, Eqs. (24)–(29), specifies H_E=0, H_SE=g Z_S⊗|1><1|_E, and a static bath mixture with weight 0<ϖ<1. Starting from |+>, it measures X after every cell and retains all outcomes. Equation (29) gives complete-record TV error ε_K=ϖ[1−cos^(2K)(gh)]. Unit prefactor is a ϖ=1 boundary specialization; the stated correlated-memory example has 0<ϖ<1.

Inference from that model: terminal wrong-X probability is instead ϖ{1−[cos(2gh)]^K}/2, because two flips can cancel. Therefore its retained-record survival expression is not an endpoint minimax theorem. Theorem 2 also already provides a general integrable-envelope complete-record upper bound; “uniform envelope bound” alone is too broad a delta claim.

## Actual delta in the local packet

Reading FIXED_REFRESH_MINIMAX.md, the proposed additional result is specifically:

1. An exact finite-action singleton wrong-sector endpoint minimax, Q=1−∏_k cos²(min(a_k,π/2)), under a known time-dependent odd-coupling envelope and exact fixed pinches.
2. A time-dependent finite sink-bath construction that makes every first mismatch permanent, turning the no-mismatch survival complement into actual terminal error and saturating Q. Bath dimension m+1 is sufficient for m gaps; smaller fixed dimensions are not covered by this attainment claim.
3. Optimization of Q at equal envelope actions, plus the separately qualified singleton Walsh-effect interface.

This delta is a comparison of statements in this bounded source set, not a novelty or priority certificate. It does not establish finite-width control, hardware feasibility, or a universal finite-action product bound for multiple selected coordinates sharing a bath.

## Recommended correction to PRIMARY_PRIOR.md

Replace the unqualified Wang sentence with: “Its static-bath benchmark has complete retained-record error ϖ[1−cos^(2K)(gh)] for 0<ϖ<1; the unit-prefactor expression is its fully active-bath boundary specialization. This is a history-record observable, rather than the terminal wrong-sector observable optimized here.”

No source files or repository code were changed.
