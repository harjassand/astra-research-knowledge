# Transactional arbitrary-CPTP-kick memory: conditional corollary of the spacetime-chain proof

2026-10-29. **Conditional synthesis, not a claim that all component audits are finished.** The precise required contracts are listed below. This theorem uses positive physical records and does not extend to arbitrary continuously acting coherent Hamiltonian or signed HP perturbations.

## 1. Required independently verified interfaces

### S: exact instrument and Pauli-branch semantics

The full-Hilbert local forest gauge places all unmarked owner good-range projectors on controller/workspace/lock registers only. For the actual separately recorded reset instruments, each unmarked good terminal is a correct current-syndrome SSF operation with the actual complete read footprint and reservation/serialization conditions. Clean intervening events are data identity in this representation. Marked or otherwise nonideal emissions and direct kicks are bounded-support data operations.

Every fixed actual physical record admits a data-Pauli expansion in which each term is a valid serial SSF history plus bounded-support Pauli bad events. Good-range inclusions hold coefficientwise because the projectors are data independent. Primitive marks, actual reset records, good-service certificates and the upper bound on bad-event mass are common to all Pauli terms. This is the interface in PAULI_BRANCH_INTERFACE.md and its independent gauge/decomposition audit, not a consequence of a stochastic Pauli noise assumption.

### D: deterministic one-sector D0/D1

Use exactly the D0/D1 contracts in SPACETIME_CPTP_MEMORY.md, applied independently to X and Z sectors. The finite-work constant C_seed is unconditional, and the good-block dichotomy must contain and root EVERY component at its target. Take a common cutoff ℓ below the code distance and each sector's small-component cutoff. Virtual boundary relabelings are by stabilizers only; no physical ideal recovery is performed between blocks.

### Q: fixed-set positive record fault-mass moment

All physical marks begin zero at the global initial time. For each fixed data set W of m sites and fixed physical block b, construct a deterministic set V_b(W) of physical anchor/time cells that contains every direct kick or marked emission which could contribute a branch bad event touching W. Bounded dressed support, incidence and constant block length must give |V_b(W)|<=κ_Q m.

A fixed constant multiple of the direct-plus-marked record mass must dominate the support-multiplicity charge Q_block(W) for EVERY Pauli branch. With those constants included, require the uniform positive moment

    E_ρ exp[θ Q_record(W,b)]
       <= exp[ε H_Q m (exp(B_Q θ)-1)] Tr ρ,   θ>=0.       (Q)

Here ρ is any allowed positive subnormalized initial joint state with the specified zero mark initialization; the budget is on the full retained quantum/controller/bath evolution. The target block may be arbitrarily late. Earlier kick ancestors are not discarded or freshly reset.

The candidate source for (Q) is MULTIPLICITY_AND_INITIAL_MARKS.md, equation (6), after bounded cell enlargement and multiplication by the maximum data support per emitted fault. The incidence/enlargement constants must actually be checked for the chosen gauge. This invocation does not assert that such emissions were independent primitive kicks.

### M: fixed-set positive actual-good-service moment

For each fixed W and window j, the conservative physical good-service miss count M_record(W,b,j) is over at most h0 m distinct candidate cells and majorizes the deterministic missed-opportunity count of EVERY compatible Pauli branch. Require

    E_ρ exp[θ M_record(W,b,j)]
       <= [1+q_good(exp θ-1)]^(h0 m) Tr ρ.              (M)

The candidate source is TWO_HALF_GOOD_SERVICE.md, Sections 7–8. It uses actual reset-shortfall/control-spoil records and exact fresh good terminals, not idealized independent hub clocks. Q and M may be correlated arbitrarily. Neither (Q) nor (M) may be obtained by renormalizing after a rare past or future record.

## 2. A terminal fresh-event tail without independence

The deterministic backward chain needs only one terminal fresh event, either Q_record>=m/(2C_seed) or Q_record+M_record>=m/C_bad. Put

    a0=min{1/(2C_seed),1/C_bad},
    B=max{B_Q,1},
    p=max{ε H_Q,q_good}.

For p<1 choose t=p^(-1/(4B)). Scalar Cauchy–Schwarz on the actual joint positive record measure, valid uniformly for every initial ρ, gives

    E_ρ t^(Q_record+M_record)
      <= exp[(ε H_Q m/2)(t^(2B_Q)-1)]
         [1+q_good(t^2-1)]^(h0 m/2) Tr ρ
      <= exp[((1+h0)/2)sqrt(p) m] Tr ρ.

Therefore the CP instrument of the terminal fresh event has diamond norm at most

    r0^m,
    r0=exp[((1+h0)/2)sqrt(p)] p^(a0/(4B)).              (12)

The effect bound is uniform, so it holds even when the actual event probabilities depend on the logical input. The estimate does not suppose an independent delay, controller clock, bath, or fault process after conditioning on quantum records.

## 3. The geometric proof is unchanged

Choose R so γ=c_R/(2C_seed)>1 and put

    K_vol=1+2C_seed/(1-1/γ).

The first-bad-block argument in SPACETIME_CPTP_MEMORY.md is pathwise on each valid Pauli history. The root can be an arbitrarily large component; only D0 is used there. All earlier blocks of that branch are good and admit D1. The backward chain must stop at a fresh event because the initial data error is empty. Its total connected spacetime volume V is at most K_vol times the terminal set size m, and V>=ℓ.

All physical records compatible with ANY bad Pauli branch consequently lie in the union of the corresponding fixed terminal-event certificates. The physical event may be checked against the complete record, but its norm is bounded unconditionally from the global initialization. No branch probabilities are assigned.

Let A_st be the bounded-degree spacetime-animal counting constant and

    r=A_st r0^(1/K_vol).

For L complete observed blocks, the uniform CP norm of the bad-record instrument in one sector is at most

    δ_sector <= min{1, L R N r^ℓ/(1-r)},    r<1.

Union-bounding the two sectors gives

    δ <= min{1, 2 L R N r^ℓ/(1-r)}.                    (13)

Only actual positive record-event instruments are union-bounded. There is no coherent Dyson-path union bound and no factor exponential in unrelated spacetime volume.

## 4. Quantum logical-memory conclusion

Initialize the dressed data in the exact encoded logical state, controllers in the specified globally good state, and a fixed bath state independent of the logical input. Logical reference entanglement is arbitrary. Keep the bath and controller records throughout the evolution.

Decode using the appropriate local forest frame F^dagger and the fixed sectorwise ideal syndrome recoveries R_X R_Z, followed by logical decoding. This is a statement about decoded logical memory, not bare physical data and not a free physical readout compiler.

On the complement of the bad-record event, every compatible Pauli-expanded term has the same correct logical action. The full good instrument, after tracing the fixed initial controller/bath and final ancillary outputs, therefore equals a scalar times the logical identity channel. The bad instrument is CP and has diamond norm at most δ uniformly over the input. Trace preservation then gives

    ||E_dec-id_L||_diamond <=2δ
       <=2 min{1, 2 L R N r^ℓ/(1-r)}.                  (14)

This conclusion does NOT require input-independent actual reset probabilities. It uses the uniform CP effect bound and common-correctable-span property. Nothing is measured merely to make formal Pauli labels classical.

If ℓ=c sqrt(N), and the fixed microscopic parameters can be chosen so p is sufficiently small that r<1, the bound permits an exponential-in-sqrt(N) logical lifetime up to the displayed polynomial factors. Constants may be extremely poor; no useful numerical threshold is asserted.

## 5. Scope, parameters, and unfinished obligations

* Physical noise here is bounded-rate exogenous local CPTP kicks with retained bath, as required by the mark/ancestor and good-service contracts. Arbitrary continuously acting coherent Hamiltonians do not have these positive primitive event records; this corollary does not settle that broader model.
* Choose R first for backward expansion; choose the fixed service-window duration sufficiently large to make reset-shortfall rare; then choose ε sufficiently small for robustness, control-spoil and fault-mass budgets. This order is compatible with the source contracts when their constants are finite and independent of N.
* The compiler semantics audit must confirm exact current-syndrome serial SSF, not only an intended abstract recovery channel or a good-range expectation estimate.
* The fault-mass audit must confirm the repeated-cell factorial moment and uniformly finite late-cell ancestry constants, and the dressed support/cell assignment used in (Q).
* The deterministic audit must confirm D0/D1, particularly the incoming-real-seed bound after virtual endpoint reduction and the component-rooting property.
* Final mathematical decoding includes the forest frame. Physical readout resources and any fixed-dimensional geometric routing remain separately charged.
* No arbitrary conditional restart, stationary marked-owner distribution, or invariant quantum residual-noise law is assumed. Initial marks are globally zero; their descendants in late blocks are accounted for by the unconditional source theorem.

This is the exact conditional composition theorem. It should be promoted only after the listed component contracts are audited, rather than by assuming a new quantum residual envelope.
