# Astra: autonomous quantum memory with noisy witnesses

## What this package establishes

A qualified mathematical construction of quantum memory in a fixed, graph-local open-system model. Finite noisy witness registers replace an assumed reliable classical decoder. An extensive restoring-potential bound and a corrected quantum boundary argument give an exponentially long storage lifetime at fixed admitted local noise/control ratios.

A second construction replaces the ideal conditional correction jumps with an exact finite-rate Hamiltonian/ancilla-reset model. Its positive current-corrected Lyapunov observable controls rare boundary occupation directly. It does not take an infinite-reset-rate limit or transfer a finite-time approximation over an exponentially long memory interval. Data, witnesses and added ancillas all enter the stated noise budgets.

The whole mathematical joins have passed separate independent INTERNAL reviews. Governing quantum Tanner code/decoder theorems remain imported primary premises. This is not external peer review, a hardware demonstration, or a claim of historical priority.

## Why it could matter

The intended capability is quantum information that protects itself without a reliable external timing/decoder service. The contribution here is a constructive route to finite noisy decoder witnesses and finite-rate protection, including coherent perturbations. Ordinary autonomous decoder auxiliaries and stored Pauli frames are established prior ideas; they are not claimed as inventions of this package.

This is a foundational component toward reliable quantum technology, not the civilisation-level north star reached. Memory is proved, not universal computation or an energy/work advantage.

## The essential cost gate was checked early

The present proof does NOT establish a useful operating regime:

- No useful finite Tanner-code instance is certified.
- The guaranteed asymptotic constants are extraordinarily pessimistic. Small-degree numerical substitutions are explicitly UNVERIFIED diagnostics, not physical thresholds.
- Conditional operations and Hamiltonian couplings have bounded-but-high body order; straightforward local selectors have exponential dependence on the fixed code degree.
- Expander graph locality is not fixed-density, short-range3D locality. Communication infrastructure, delays and noise must be paid.
- Finite reset reservoirs, native few-body synthesis, noisy input encoding and noisy terminal readout are not constructed.

These limitations are not proof that physical performance must be as poor as the sufficient bounds. They do prevent a practical or same-resource advantage claim. Further refinements of these tiny constants alone would have limited additional consequence. The next promotion gate is a concrete finite-code/native-interaction regime, not another large theoretical budget.

## Conditions that must travel with the theorem

Use only the specified LZ-family hypotheses, actual local projectors and extensive move-count bound. The safe component is confined using minimum syndrome representatives; global low energy alone is not sufficient. Protected logical information is a SUBSYSTEM: witnesses may be coherently noisy gauge degrees of freedom.

General dissipators require a TWO-STEP boundary shell. The original one-step claim was false; its counterexample and superseded author draft are retained in history/ and tests/.

The ideal-jump model has5n qubits. The finite-dilation model has5n+M_anc, M_anc<=L0 n, potentially with enormous L0. All added noise, rates and preparation costs must use the latter count. Warm ancillary preparation is admitted only with the explicit small-excitation moment and truncation charge. Arbitrarily hot or correlated preparations are not supplied.

With fixed independent bath initialization the result has a restricted-code channel interpretation. Initially correlated baths instead use the stated joint-state/output bound. The terminal consumer is explicit but IDEAL: the two-layer frame Clifford, followed by the original efficient Tanner decoder, with the additional radius shrink. No minimum-weight oracle is needed; no fault-free physical readout is inferred.

## Read order

1. FINITE_DILATION_JOIN_DRAFT.md: strongest proposed whole-model statement, accepted at its exact hash by the corresponding receipt.
2. JOINED_TANNER_MEMORY_DRAFT.md and controller/TANNER_WITNESS_DOWNHILL_CONTROLLER.md: ideal-jump instance and its code/gauge construction.
3. ANCILLA_CURRENT_HYPOCOERCIVE_LIFT.md: exact current and exponential-potential mechanism.
4. independent_audit/ and controller_audit/: the actual independent scopes, corrections and source bindings.
5. costs/ and priors/: early physical gate and strong conventional comparisons.

Author filenames containing DRAFT are preserved to maintain receipt hashes; current acceptance is governed by the matching receipts, not by a renamed historical header.

## Checks and reproduction

The scripts check finite algebra, source-constant arithmetic and the actual one-shell counterexample. They do NOT simulate a scalable Tanner memory or establish a hardware threshold.

From tests/, run:

    python check_constants.py
    python check_clifford.py
    python check_current_signs.py
    python two_step_counterexample.py
    python tanner_cost_arithmetic.py

Python, NumPy and SymPy are used as indicated by the scripts. No physical experiment or external publication was performed. The complete proof, costs, comparisons and informative failure are preserved here rather than replacing the scientific target with a convenient smaller claim.
