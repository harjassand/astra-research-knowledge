# Proper-MPS periodic/GNS gap identification: provisional extension

2026-11-05. A standalone extension, kept separate from the previously packaged LTI-hierarchy proof.

## Outcome

The proposed proof identifies the limiting finite-periodic gap with the infinite-chain GNS gap for translation-invariant, positive, finite-range **proper primitive-MPS parent Hamiltonians**, with uniform open-chain gap and unique large-ring ground state. It establishes existence of the periodic limit and the one-sided estimate Delta_GNS <= Delta_N + O(log N/N). The exact assumptions are in `PROOF.md`; no matching two-sided convergence rate is claimed.

The mathematical proof has two internal independent reviews, not external or formal verification. A separate literature-priority audit supplies exact source anchors and is not a third proof audit. No matching full theorem was located, but novelty remains unresolved: the original FNW 1992 full article could not be inspected beyond a preview/security-check barrier. The earlier LTI proof and its archive have not been edited. If both candidates are accepted, the nearest-neighbor LTI hierarchy converges to the GNS gap on its stated proper-parent class.

## Central operation

Project a low-energy translation-eigen periodic excitation onto the exact MPS ground space of a quiet buffer. Uniform MPS conditioning produces a local operator of bounded norm representing that vector. Transfer-matrix mixing compares its norm, mean and energy with the infinite MPS uniformly even as the operator's support grows. This excludes periodic low-energy states that would be missed by assuming fixed-support convergence alone.

`check_embedding.py` constructs the whole operation, including the periodic excitation, buffer projection, explicit local operator, and infinite-state energy and variance. It checks 12 cases: AKLT and a generic complex MPS at N=6,8, plus a complex nonprojector positive interaction with the same local MPS kernel. It imports no earlier proposal code. The second independent audit separately tests the uniform finite-rank inequalities on 60 cases with core lengths up to 1000.

## Strong prior and limitations

- Bachmann–Dybalski–Naaijkens Proposition 5.4 and Nachtergaele–Sims–Young Theorem 7.4 already provide the one-sided finite-gap-to-GNS comparison. The reverse inequality is not obtained by relabeling those theorems.
- Haegeman et al. PRL 111,080401 (2013) already explicitly describes the finite-boundary local excitation embedding. Its selected-quasiparticle approximation theorem assumes uniform momentum-sector isolation and nonzero local spectral weight, which this buffer proof does not assume.
- Haegeman–Osborne–Verstraete PRB 88,075133 (2013), Table I, reports much stronger AKLT variational estimates: K=1 gives 10/27, K=2 gives 0.350634581086138, and K=12 gives 0.350124157337687. The present best small construction-check quotient is approximately 0.432, so there is no numerical gap-bound improvement or new variational capability.
- These are floating-point construction tests, not interval-certified upper bounds. The numerical routine has exponential physical Hilbert-space cost and is not a proposed efficient solver.
- Merely having a unique infinite injective/product MPS ground state is not enough for this proof. Weak-parent boundary modes, closing open gaps, frustrated chains, and higher dimensions are excluded.
- No new best AKLT lower bound, no hardware proposal, no experimental dataset and no external action are involved.

Exact primary sources, assumptions and priority distinctions appear in `LITERATURE_PRIORITY_AUDIT.md`, `independent_periodic_gns_audit.md` and the second proof audit. The standard direction is explicitly Nachtergaele-Sims-Young Theorem 7.4, equations (7.26)-(7.29), with its local-vector core in Section 7.2. `PROOF.md` Section 7 adds citations without altering the previously reviewed Sections 1-6; `CITATION_UPDATE.json` records both hashes and the verifier checks that provenance.

## Reproduce

Requirements: Python 3.12, NumPy 2.3.5 and SciPy 1.17.0 were used. No solver package, GPU or network access is needed to rerun the tests.

From the archive's extraction directory:

    python mps_gns_gap_extension_20261105/verify_package.py
    python mps_gns_gap_extension_20261105/verify_package.py --run-tests

The manifest is checked before tests run. Tests regenerate result JSON files, so use a fresh extraction for a later manifest check. The final extraction test record is outside the archive to avoid a self-hash cycle.

## Relation to the earlier candidate

The earlier archive remains `lti_gap_completeness_20261105/compact_reproduction.zip`, SHA256 `ceba3efefed82e575b73ae06db7f39d71d17ee28f002d9694219561d558b42a6`. Its natural nearest-neighbor hierarchy starts at n>=3; its projected Appendix D extension starts at n>=4 and has a separately reviewed level shift. None of those scope qualifications are altered by this extension.
