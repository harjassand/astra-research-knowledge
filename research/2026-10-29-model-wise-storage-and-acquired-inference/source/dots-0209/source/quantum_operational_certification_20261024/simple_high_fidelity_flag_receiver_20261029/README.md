# Simple high-fidelity flag receiver — 2026-10-29

New scoped construction, author checks only; independent review pending.

- Exact two-outcome qubit Helstrom receiver uses no Naimark ancilla.
- Top-prior pair gives F>=2F*-1; this rule's bound is asymptotically sharp.
- State-aware empirical pair search removes the prior-estimation penalty: F>=B*-4delta>=2F*-1-4delta, before numerical/control costs.
- A directly checked dual slack gives full-oracle regret <=4delta+2s without a general SDP. This extends the existing compact pilot's certificate workflow; it is not a new discrimination principle.
- A biased three-state family has strictly nonbinary optimum at arbitrarily high fidelity. Exact two-outcome optimality is not automatic in the high-fidelity regime.

`THEOREM_v1.md` governs all claims and assumptions. `check_binary_receiver_v1.py` reproduces deterministic sharpness fixtures and 1,000 perturbation tests; its JSON is diagnostic floating-point output, not physical observations or an interval certificate. This package changes no earlier result. It depends on the received compact flag recovery theorem in the sibling directory; old sources remain intact. No new source calls, hardware experiments, historical novelty or advantage over equally informed conventional binary discrimination is claimed.

The actual substantive obstacle removed is a general flag-POVM/Naimark implementation when controlled additive loss or a small dual slack is sufficient. It does not remove the accessible-flag, Bell-reference, calibrated-control, stationary-source or full-CPTP-comparator restrictions. Morrey is untouched.
