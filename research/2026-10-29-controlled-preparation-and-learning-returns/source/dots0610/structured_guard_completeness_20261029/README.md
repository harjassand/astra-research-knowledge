# Structured guarded completeness — 2026-10-29

New material: a full-physical Bell-loss extension of the received singlet-frame variance proof; a finite matching/orbit guard whose acceptance is provably high under a fixed unknown full-joint collective algebra and sustained occupation gap; an explicit four-spin block isometry and exact unitary completion; and a bath-coupled excitation subclass with exact gap one.

Governing statement: `GOVERNING_v1.md`. The load-bearing extension and theorem are under independent review. `FOUR_SPIN_IMPLEMENTATION_v1.md` gives an exact finite construction, NOT a verified elementary-gate netlist. `EXCITATION_WITNESS_v1.md` supplies an explicit nonempty family for the identifiability premise, not a technique to enforce it on arbitrary noise.

Run:

    python check_construction.py
    python check_excitation_witness.py

SymPy checks the isometry, collective invariance, unitary completion, and octahedral moment exactly. Guard tail probabilities and parameter comparisons use exact rational arithmetic; logarithmic training-cap and exponential-rate numerical examples are labelled floating diagnostics. The proof supplies the analytic inequalities independently.

Scope: source-call/sample complexity is polynomial in block size and inverse occupation gap, without learning the complete environment. Current local control, private settings, memory retirement, complete-call boundaries and source common-algebra assumptions remain explicit dependencies. No hardware demonstration, total circuit-time advantage, threshold or historical novelty claim is made. Arbitrary noise has only soundness and may always abort.

IMPORTANT comparator: an equally informed direct fixed-subcode full-path two-MUB/endpoint-Pauli guard also has a polynomial structured-family completeness route. The matching/orbit result must not be advertised as the first or unique polynomial route; its contribution is the matching-only model-free interface for a proper subcode with no d/K penalty. Independent reviewer is preparing the detailed comparison.

Quantitative caution: the displayed uniform bound at B2048 requires about1.6 trillion training calls for gap.35 and failure budget.05. The limiting1/48 physical-exposure ratio at fixed gap/confidence is only asymptotic and excludes endpoint control/storage. Exponentially small acquisition failure instead increases the single-block calibration cost and destroys that constant-rate conclusion absent amortization.

Dependencies: the original nonunital no-reset estimator, matrix confidence packet, received twirled variance proof, permutation-orbit guard and finite-field outer compiler. No original proofs or data were overwritten. This packet is additive, not a replacement for the actual1m model benchmark or its weaker certified frame margins.
