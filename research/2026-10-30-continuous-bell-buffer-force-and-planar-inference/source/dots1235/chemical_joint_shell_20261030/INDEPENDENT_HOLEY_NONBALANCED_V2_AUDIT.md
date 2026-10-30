# Independent audit: non-complex-balanced holey-head v2

Reviewed 2026-10-30. This is a separate review of the doubled 3C->A+2C rate choice, not automatic acceptance from the all-unit fixture.

**Verdict: the new local actual head–tail construction and its stated matching premises pass this child-level audit.** No general-network theorem, novelty clearance, or separate whole-global-proof review is asserted.

## Changed reaction and non-complex-balance check

The helper implements doubling by including the (0,1) fast edge twice. Every rate construction sums over this list, so both the conservative absorption matrix and the head matrix receive exactly the intended doubled rate. Enabled supports, the inactive hole, and scalar first-up failure are unchanged.

For fast complex weights w0,w1,w3, stationarity is

    3w0=w1+w3,  2w1=2w0+w3,  2w3=w0+w1.

Thus w1/w0=5/3 and w3/w0=4/3. Positive mass-action monomials would require these to be a/c and (a/c)^3, which is impossible. In the full network, complex balance at the connector's zero and A+B complexes forces equal unit connector flows into and out of the shared 3A+4B junction. Hence the connector has zero net contribution there and cannot repair the fast incompatibility. The v2 non-complex-balance claim is correct. By contrast, the preserved all-unit fixture is complex balanced at (1,1,1), as acknowledged.

## Exact rerun

Ran `exact_holey_head_nonbalanced_slack.py` and reproduced `HOLEY_NONBALANCED_HEAD_EXACT.json` byte-for-byte. The leading Schur determinant is

    z^2 (3494/3653)(1-2/t).

The first six leading Cramer coefficients are 20/13; the seventh is 4480/3653+2280/(3653t). Also checked:

- full matrix dimension 21;
- entry Laurent t exponents remain in [-1,1];
- the leading active block is t-independent;
- its determinant is 78169235849950003200 > 0;
- its inverse is entrywise nonnegative.

Thus the same explicit alpha<1/43 two-scale bound applies, and all inactive profiles are positive asymptotic constants times r^2. The active recovery remains positive and O(r^2). This is exact algebra, not an inference from numerical eigenvalues.

## Actual shifts and tail feedback

The eta offsets, factor-two slack, and r^2 forcing are unchanged. They still convert the exact matrix solution into the suppressed-return physical head inequality; the birth-suppressed kernel remains an upper bound on the actual zero-birth return term.

Doubling an enabled fast coefficient does not invalidate shell reachability or the finite-graph bound. Every N>=4 shell reaches clearing, while the isolated N=3 hole remains inside the head. The true tail return and running-cost construction therefore has the same weighted bounds. All head-to-tail entrances still originate at active N=4 or5 with eta=0, rate O(s), and nonpositive original residual shift. The >=1-birth contribution is still O(s^{2alpha+o(1)}phi), absorbed by the earned s^2 phi active-phase margin. Inactive phases have no such entrance error. Tail running cost and nonexplosion are justified by the renewal argument detailed in `INDEPENDENT_HOLEY_HEAD_RETURN_AUDIT.md`.

## Modified graph boundary premise

Separately audited `HOMOGENEOUS_FAST_BOUNDARY_LIMIT.md`; see `INDEPENDENT_HOMOGENEOUS_BOUNDARY_AUDIT.md`. Its uniform simplex limit applies with the doubled coefficient, yielding endpoint values -3 and -2. Hence the required extreme-composition F margins remain valid, including zero/bounded minority counts. Low-B connector recursion, its actual clearing-return estimate, and the r-value depend only on the unchanged connector and preservation of N,B. Balanced high-B negativity follows from the same bulk lemma for this strongly connected graph after possibly decreasing alpha.

The polynomial tail-profile bound and B-s=g_N separation therefore retain the same cap-collar matching estimates. No unreviewed invariant-cap or equilibrium assumption is introduced by the changed rate.

## Artifact-label caveat

At review time the helper's comment still said “all rates one,” and the exact script docstring called the return “zero-birth.” These are misleading standalone labels: the implementation doubles one rate and uses the birth-suppressed upper kernel. The mathematical v2 document states both facts correctly. The author was asked to align the comments; this requires no computational change.

Reviewed hashes:
c88d2dda245fd7600c23f67375a5f6afd1ee65ffb1e524930c2ddb38e42a9124  chemical_joint_shell_20261030/HOLEY_HEAD_NONBALANCED_ACTUAL_CLOSURE_V2.md
d1ef85e20179297257bd455df83702eaf51209477521a02a225a4798c4d01d62  chemical_joint_shell_20261030/exact_holey_head_nonbalanced_slack.py
63c16d9aae9411d5fd462bea2af36f19011ebe8c8bea365b4260a305f2f03474  chemical_joint_shell_20261030/HOLEY_NONBALANCED_HEAD_EXACT.json
5c80a16914cb9575b276347bfba537d5ad522ba8a5c578b0cd01c58004fa748d  chemical_joint_shell_20261030/test_holey_head_nonbalanced.py

### Label verification

Re-read the current helper and exact script. Their standalone labels now correctly say birth-SUPPRESSED upper-return, and the doubled-edge comment is explicit. This resolves the nonmathematical caveat above. Current hashes after comment-only repair:
c88d2dda245fd7600c23f67375a5f6afd1ee65ffb1e524930c2ddb38e42a9124  chemical_joint_shell_20261030/HOLEY_HEAD_NONBALANCED_ACTUAL_CLOSURE_V2.md
d1ef85e20179297257bd455df83702eaf51209477521a02a225a4798c4d01d62  chemical_joint_shell_20261030/exact_holey_head_nonbalanced_slack.py
63c16d9aae9411d5fd462bea2af36f19011ebe8c8bea365b4260a305f2f03474  chemical_joint_shell_20261030/HOLEY_NONBALANCED_HEAD_EXACT.json
5c80a16914cb9575b276347bfba537d5ad522ba8a5c578b0cd01c58004fa748d  chemical_joint_shell_20261030/test_holey_head_nonbalanced.py
