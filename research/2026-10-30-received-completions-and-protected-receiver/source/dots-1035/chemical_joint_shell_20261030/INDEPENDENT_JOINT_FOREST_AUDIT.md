# Independent audit: joint-shell positive-forest transport

Reviewer: finite_phase_drift_challenge, 2026-10-30. Internal mathematical review. Reviewed JOINT_SHELL_FOREST_TRANSPORT.md, check_joint_endpoint_support.py, imported reaction definitions/height tables, and JOINT_ENDPOINT_SUPPORT.json.

## Verdict

The polynomial core-to-core Green transport proof passes after one general-setting correction: for possibly negative offsets, require L+min_j h_j≥D_A (where D_A bounds A source orders), not merely L≥D_A. This guarantees a common valid core and unchanged A-enabling away from eliminated endpoints. The concrete recorded heights are nonnegative, with D_A=3 and L≥3, so the test cases already satisfy the corrected condition.

No polynomial-to-near-identity upgrade is justified. The result is a genuine killed-kernel comparison under checked finite support conditions, not recurrence or global feedback control.

## 1. Exact endpoint elimination and supports

For core C and endpoint E, the eliminated generator is

    Q_eff=Q_CC+Q_CE(-Q_EE)^−1 Q_EC.

Reachability of core or killing makes Q_EE transient. The effective off-diagonal rates are nonnegative; effective killing is

    k_eff=k_C+Q_CE(-Q_EE)^−1 k_E.

Self-return excursions are incorporated in the diagonal and are not spurious new jumps. These quantities are rational functions of R because the endpoint block has fixed size and all its rates are polynomials in R. Positive forest expressions certify which entries are strictly positive. For two equal nonzero supports, corresponding positive rational functions have upper/lower polynomial ratio bounds eventually. No assumption that their expanded coefficients in R are all positive is necessary.

Only core states within the maximum fixed C-jump distance of the cut can enter the endpoint. There are finitely many such states over the fixed phase alphabet. All Schur-altered rows and possible new endpoint-mediated destinations therefore have fixed cardinality. Their support comparison is genuinely finite after expressing coordinates relative to the cut.

## 2. Forest numerator argument

For a transient killed finite generator, det(-Q_eff) has a positive cemetery-rooted forest expansion. A Green-entry cofactor has a positive two-root forest expansion, with the starting state assigned to the tree rooted at the occupation target. Every nonzero term uses at most one outgoing transition/killing rate from each vertex. Matching effective supports matches these forest supports, including the zero pattern of inverse entries.

On unaltered rows, adding one A particle leaves C unchanged and gives each nonzero source monomial a ratio between one and

    1+D_A/(A-D_A+1).

Positive sums retain these bounds. With the corrected L condition, A-D_A+1≥1 on the whole common core. Over each fixed phase, A runs through a consecutive integer interval, so the sum of logarithmic ratio bounds is O(D_A log R). The finitely many altered rows add only fixed polynomial factors from their rational rate comparisons. Thus every denominator or numerator forest term has a two-sided polynomial comparison, uniformly in the selected entry. Positive summation and division preserve a possibly larger polynomial exponent. Finally, block inversion identifies the full Green restrictions with the exact Schur inverses.

This validates the numerator argument, not merely a determinant or inverse-norm estimate.

## 3. Exact script verification and what its signatures certify

Re-ran check_joint_endpoint_support.py from the artifact directory. Output matches JOINT_ENDPOINT_SUPPORT.json byte-for-byte: 15 cases, all equal signatures, and no trapped states in either endpoint block.

The reaction formulas agree with the rank-three network. The first three entries respectively change N=A+C by +1,+2,-3 and B by +1,+3,-4; their residual jump is deltaN-h_target+h_source. Fast composition jumps change C by ±1 and preserve N,B. Falling factorials are evaluated as exact integers; no eigenvalue or floating-point sign test enters the certificate.

For these reactions, the ONLY core-to-endpoint entries are fast C-increasing edges from (cut,b) to (cut+1,b), b≥4. At L≥3 and the recorded nonnegative heights, their A source count is L+h_b≥3, making every such edge strictly positive. No b<4 entry exists because (b)_4=0. Endpoint-to-core exits can only land at (cut,b'). Hence the stored destination set for each entry phase b=4,...,K determines every Schur-created off-diagonal and killing support. A return to the same b contributes only a self-return correction; recording it does not create an extra off-diagonal.

Direct core supports match: all A orders are enabled throughout the common core, C is unchanged, and phase/residual eligibility is independent of R. Thus the equal signatures genuinely imply the full effective support equality, rather than checking an incomplete subset of boundary channels.

The endpoint coordinates relative to cut form fixed finite sets. Their A counts are fixed integers for each of the old/new blocks, and their C counts are R plus fixed offsets. Once R≥L+3, all positive-degree C factors needed here are positive. Therefore the graph is independent of R beyond that bound. Evaluating it at R=100 certifies this exact stable topology; it is not an asymptotic numerical extrapolation. The JSON records entry-to-exit signatures and trap tests, while the script supplies the full graph construction.

## 4. Whole-shell transience

Immigration is enabled at every state. Each immigration either changes residual R and kills immediately, or preserves R and increases phase B by one. In at most K+1 such firings it exits the phase alphabet or encounters a nonzero residual jump. Every proposed intermediate neutral immigration is physically enabled and remains a valid shell state. Thus every shell state reaches killing, proving finite killed-shell transience independently of full-network recurrence. The same observation also certifies endpoint reachability of killing for these test graphs.

## Limits retained

The bounds apply to common-core Green entries only. Low-A endpoint entries are not compared directly. Fixed phase width is essential to the finite endpoint size and polynomial forest exponent. This proof supplies no 1+O(1/R) shifts, no uniform constants as phase width grows, and no absorption of global connector feedback. Majority-coordinate insertion and its required support/leading-degree checks remain outside this audit.
088f8629674802adc44b8000dfe64f04c689975f9d397c5c3ec73617397b01aa  producer-workspace/JOINT_SHELL_FOREST_TRANSPORT.md
07409871c1a00ce1fa36eba34ff433ef28f7cdf8af920f002b2521a6504be49e  producer-workspace/check_joint_endpoint_support.py
d44382f630979e84373537cc471d99d35d31421e15720966f60954f391f71c69  producer-workspace/JOINT_ENDPOINT_SUPPORT.json
740bd5a0ce00d0f5f625ba6cdb54cbbf4a0c41b07aa467d363993f669da25998  producer-workspace/tree_residual_matrix.py
da80c7556cf43465d589664dd7918bcc0357514e3b972e26ec2e21796a9737e7  producer-workspace/joint_matrix.py
