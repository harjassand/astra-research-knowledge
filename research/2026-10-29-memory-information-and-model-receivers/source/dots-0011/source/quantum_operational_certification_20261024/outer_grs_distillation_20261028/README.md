# Explicit conventional outer distillation wrapper — 2026-10-28

This package closes the outer coding implementation obligation for conditional inner/outer distillation. It does not establish a new quantum capacity or an advantage over conventional pure-state concentration.

## What is supplied

- `GOVERNING_WRAPPER_v1.md`: characteristic-two weighted GRS duality, [[B,B−4t,2t+1]] CSS code, total syndrome-only Berlekamp–Welch recovery, exact bilateral decoding/measurement/correction, and costs.
- `TWIRL_FREE_ADDENDUM_v1.md`: the same corrected-span guarantee applies without actually twirling. Product inner states with individual m-ebit fidelity at least 1−epsilon0 yield output infidelity at most Pr[Bin(B,epsilon0)>t]. Nonidentical blocks are allowed; correlated blocks require their own good-subspace-weight bound.
- Small-field stripes make field construction deterministic polynomial in B, with no stripe union factor. Output payload is floor(m/h) h (B−4t), h=max(1,ceil(log2 B)).
- Exact finite-field and binary Clifford-label programs/data, including total failure fallback. No hardware data or dense noisy quantum simulation is claimed.

## Reproduce

With ordinary Python 3 and no third-party dependencies:

    python grs_wrapper_v1.py
    python check_field_and_gates_v1.py

Programs write their corresponding JSON results beside themselves. Preserve received data before rerunning if comparing bytes. `AUTHOR_MANIFEST_v1.json` binds frozen author source/data. Independent review directories contain separately authored scope and receipts; acceptance is limited to their stated checks.

## Scope and dependencies

An inner method must independently supply fixed payload, fidelity, independently prepared block states, and paid acquisition/control. The outer construction provides no such inner promise. Its ideal local Clifford gates/measurements must be implemented; a physical vanishing-error claim additionally needs vanishing total implementation error or a separate fault-tolerant mechanism.

For the motivating near-pure source composition, impurity decreases with growing sample size. This is not fixed-positive-noise distillation. The same outer method is available to ordinary smaller-block pure-state concentration, so the qualitative dilute asymptotic capability is not exclusive to the Schur construction. Governing inner claims and their comparator correction remain separate dependencies.

No earlier source is superseded. The twirl-free addendum removes an unnecessary operation from the twirled v1 protocol while preserving its fidelity conclusion. CSS/GRS and one-way distillation are credited conventional ingredients; the work here makes this particular interface and decoder explicit.
