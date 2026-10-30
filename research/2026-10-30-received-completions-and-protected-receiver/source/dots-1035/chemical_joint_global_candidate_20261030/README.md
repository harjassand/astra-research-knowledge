# Coupled chemical recurrence: global candidate for separate whole-proof review

Prepared 2026-10-30, approximately10:02 UTC. Ordinary local research bundle; no external publication.

## Result and exact status
The complete construction passed the existing child review. It claims nonexplosion, positive recurrence of every closed communicating class, and every exponential population moment for ONE explicit rank-three, deficiency-two stochastic mass-action network. Separate whole-proof review and novelty verification remain outstanding. Filenames beginning INDEPENDENT are historical child-audit names; they do NOT denote an independent external or separate whole-project review.

Network: 0→A+B→3A+4B→0 with unit constants, plus the reversible chain 3C+4B↔A+2C+4B↔2A+C+4B↔3A+4B, increasing-A constants6,1,7 and decreasing-A constants12,1,1. Its fast composition dynamics is multistable. It is not complex balanced at the listed rates: balance along the leaf-attached fast chain would require A/C simultaneously1/2,1,7.

## Read first
1. proofs/JOINT_GLOBAL_FOSTER_CANDIDATE.md — full construction and domain partition.
2. audits/INDEPENDENT_JOINT_GLOBAL_FOSTER_AUDIT.md — child end-to-end check, including stopped-process and moment issues.

The key advance is not a new fixed strip fixture: two complementary infinite backgrounds are eliminated using finite-head algebra plus genuine infinite-tail estimates. Their stopped-cost values are then coupled with an exact low-phase function into a global Foster function. Neither noncompact trace target is assumed recurrent.

## Dependency order
- proofs/FRACTIONAL_FACTORIAL_BULK.md and the primal paragraph in proofs/PRIMAL_AND_EXACT_CORNER_TRANSFER.md. Historical 'awaiting audit' headers in old dependencies are superseded by the accompanying child audits, not by an external review.
- proofs/EXACT_LOW_PHASE_FORCING_CLOSURE.md: one globally defined F, actual low-B Poisson correction, true clearing-return feedback, and the preserved positive balanced ray showing F alone fails.
- proofs/INFINITE_PHASE_FIRST_EXIT_CONTRACTION.md: controlled r=N−h_B trace. Its positive lower-rate premise is explicit; unrestricted physical first-up control is explicitly falsified at A=0,B=3.
- proofs/KILLED_SHELL_FAST_BOUNDARY_SCALE.md: actual conservative-shell absorption N^(−9/4), not mixing.
- proofs/COMPLEMENTARY_ACTUAL_COMPOSITION_TRACE.md: actual s=B−g_N trace, with summable infinite-composition tail.
- proofs/ROBUST_PHASE_INFINITE_FIBER_LIFT.md supplies the elementary finite affine policy-improvement context used in the first trace. Its broader source-complete global corollary is not a dependency of the present network theorem.
- proofs/GENERAL_SUMMABLE_KILLED_FIBER_LEMMA.md is a NEW, UNREVIEWED structural generalization of one analytic ingredient. It is not used in the global candidate and must not be treated as reviewed capital.

## Exact algebra checks
From checks/ run:

    python check_first_residual_all_exit_degrees.py
    python check_composition_head_exit_degrees.py

Compare with the corresponding JSON files. The first proof uses only the fixed B<=12 head; its maximum up/tail exponents are−1/−2. The second uses only the fixed N<=8 head (45 states); maxima are−1/−3. These are exact positive-Schur degree calculations, not eigenvalue numerics. The extra widths are checks, not the proof of an infinite-width limit.

check_exact_primal_feedback.py is only a numerical corroboration of the analytically positive balanced ray of F. It is not used to certify recurrence.

## Explicit exclusions
- General weakly reversible recurrence is NOT proved.
- No assumed fast equilibration, cone invariance, global recurrence, or closed truncated corner is used.
- Earlier frozen/mapped joint-matrix numerics had genuine endpoint failures; the present proof changes representation and does not relabel those tests as passed.
- No efficiency bound or novelty claim is made.
- Audit hashes refer to versions reviewed before minor status/docstring updates; SHA256SUMS.txt records this bundle's current files.

## Primary comparison already checked
Anderson–Kim arXiv1904.08967 concerns specified single-linkage subclasses, including binary hypotheses, not an automatic arbitrary-order theorem. Anderson–Cappelletti–Kim–Nguyen arXiv1808.05328 gives strongly-endotactic recurrence subclasses and cautions against treating strong endotacticity alone as sufficient. The ConStRAINeD project publicly claims general two-species recurrence; the present network has three independent species. Current arXiv2610.31550 separates planar bulk criteria from compatible boundary estimates. These comparisons do not establish novelty of the present explicit result or mechanism.
