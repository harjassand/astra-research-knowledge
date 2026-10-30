# Blinded mathematical assessment

None of the six returns resolves the full exceptional ROC/QC question. All six retain substantive correct results at the scopes described below. I found no blocking error in their checked main arguments. The important differences are a smaller sufficient QC coefficient, a broader all-means positive theorem, a compatible-field guarantee at the original ROC boundary, and an obstruction to a specified proof method. These are distinct accomplishments.

## Exposure and scope of this assessment

I had no inherited constructor conversation and no previous exposure to these mathematical artifacts before this assignment. I read the common frozen `MATH_TASK.md`, the two assigned checkpoints, their relevant scientific proofs, and the six assigned scientific returns and proof/code artifacts. I did not consult mapping/design files, context or procedure prompts, production history, memory files, network sources, coordinator conclusions, or scientific reports outside these assigned copies and the permitted common mathematical packet. I have not inferred or assigned coordination-policy labels. Labels are masked, but writing style, implementation choices and provenance-bearing paths may permit inference; this is not a claim of perfect blinding.

This is a source-exposed internal mathematical assessment, including exact replays and targeted independent algebra. Internal results are accepted on their mathematical substance at their actual scope; external validation is not an extra acceptance gate. This is not an exhaustive historical-novelty audit or a proof-assistant formalization.

Throughout, use the common normalization

\[
P=3p=F+C_M+Q,\quad F=|w|^4+2|z|^2|w|^2,\quad C_M=z^TM\nu(w).
\]

For `Q=λ(|z|²+|w|²)`, the inherited exact ROC threshold is

\[
\lambda_{\rm ROC}(M)=\frac{2\sigma_1(M)^2+\sigma_2(M)^2}{16}.
\]

For `M=I`, write `P₀` for the member at `λ=3/16`, and set

\[
\lambda_H=\frac{3+\sqrt3}{24}=0.197168783648703\ldots>3/16.
\]

These definitions, the normal form, the acoustic kernel count and the general compatible moment-Schur reduction are inherited capital, not new contributions of these returns. The fixed task is explicit about this distinction: [MATH_TASK.md, lines 7–22](producer-workspace/MATH_TASK.md:7).

## Block 1

The checkpoint already has the full evaluated ROC criterion and finite full-Q classifier, the sharp singular-value threshold, non-polyconvexity of `P₀`, and the obstruction to **every polynomial closed-form correction** making its ordinary-heat density pointwise PSD. Repeating those facts earns no new credit. See [checkpoint capsule, lines 5–23](producer-workspace/CAPSULE.md:5) and [checkpoint proof, lines 119–179](producer-workspace/PROOF.md:119).

| Masked return | Correct new contribution relative to this checkpoint | Exact limitation and blocking-error assessment |
|---|---|---|
| `result_8bee532` | **An actual boundary-field theorem:** `P₀` satisfies the QC inequality for every background, amplitude and phase of every characteristic-polarized noncollinear resonant three-wave gradient. The map is constructed explicitly, and resonant third moments and the Schur correlation need not vanish. It also classifies the complete characteristic locus, proves uniqueness of a null rank-one line at each characteristic background, shows `b=0 ⇒ r=0` for actual periodic gradients, and identifies the fourth-order cusp degeneracy. | This is not global QC of `P₀`: output polarizations are prescribed and unrestricted multimode interactions remain. The characteristic/cusp geometry is structural information, not itself a QC theorem. No blocking error found. The determinant proof uses the inherited nonnegative Schur diagonal blocks correctly; a determinant alone without those blocks would not suffice. |
| `result_b8f8b00` | **The broadest all-means QC construction in this block:** `F+C_M+Q` is QC if `Q(a,b)≥||M||²_F/4` on the two unit circles. For `Q=αr+βt`, this is `α+β≥||M||²_F/4`; it equals the exact ROC condition whenever `rank M≤1`, including equality and determinant lineality. A tunable certificate further proves QC for the conformal modes at `λ≥λ_H`, and supplies improved sufficient bounds for general `M`. | Sharpness is established for the isotropic rank-one-M subfamily, not for arbitrary admitted Q with rank-one M. The original full-rank boundary `P₀` remains open. No blocking error found: the explicit polynomial primitive and square identities are identities on all compatible Hessians, so heat flow and Stokes prove a genuine all-fields/all-means inequality. |
| `result_f715a2c` | **A correct all-means QC construction with weaker constants:** exact rational 18×18 Grams prove the conformal and anticonformal slices at `99/500` and `27/100`. Scaling, proper rotations and an optimized convex combination give its stated all-M sufficient class, including arbitrary ROC quadratic residuals. Separately, for every `M=σO` and every Q admitted by the sharp ROC criterion, it proves the QC inequality at every conformal mean `(z₀,0)`, including the original lower boundary. | Neither the rational-primitive fit nor the unsuccessful searches prove a theorem or a counterexample. The safe-mean result covers all test fields but a restricted plane of means. It is not global QC for those lower tails. No blocking error found in the rational Gram construction or the independent safe-mean completion. |

Consequential source pointers:

- `8bee532`: [complete characteristic locus and Schur-boundary argument, proof lines 17–118](producer-workspace/PROOF.md:17); [all-triangle extension, lines 209–243](producer-workspace/PROOF.md:209); [determinant reconstructed from the actual polynomial, code lines 9–46](producer-workspace/triad_wedge.py:9); [exact Bernstein conversion, lines 7–31](producer-workspace/acute_test.py:7).
- `b8f8b00`: [universal compatible square identity, proof lines 88–178](producer-workspace/PROOF.md:88); [tunable improvement, lines 180–239](producer-workspace/PROOF.md:180); [exact identity receiver, lines 20–59](producer-workspace/verify_certificate.py:20).
- `f715a2c`: [global certificate and heat implication, proof lines 13–32](producer-workspace/PROOF.md:13); [all-M combination, lines 56–89](producer-workspace/PROOF.md:56); [all-admitted-Q safe conformal means, lines 91–114](producer-workspace/PROOF.md:91); [full coefficient identity and rational positive pivots, receiver lines 11–22](producer-workspace/receive.py:11).

**Comparison.** On the common all-means sufficient-construction axis, `b8f8b00` strictly improves `f715a2c`: `λ_H<99/500`, its pure anticonformal bound `1/4<27/100`, and it additionally resolves every isotropic rank-one-M boundary. Combining its two pure-mode certificates by the same convex-combination argument gives `(√λ_H a+b/2)²`, no larger than `f715a2c`'s `(√(99/500)a+√(27/100)b)²` for the same nonnegative signed-SVD coefficients a,b. Thus the latter's all-M all-means sufficient region is contained in mathematical consequences of the former's construction.

There is nevertheless no total containment of all stated theorems. `f715a2c` separately certifies all admitted orthogonal-M tails at conformal means, which `b8f8b00` does not claim. `8bee532` certifies arbitrary means for a restricted but genuinely resonant continuum of fields at the original full-rank `P₀` boundary, where neither global construction applies. The boundary-field and safe-mean statements are complementary restrictions of the QC quantifiers, not a resolution of the missing universal quantifiers.

**Still unresolved in this block:** global QC of `P₀`, the conformal interval `[3/16,λ_H)`, and the complete full-M/full-Q exceptional face. No separately admitted ROC polynomial has an actual compatible negative-energy witness in these returns.

## Block 2

The checkpoint already has the exceptional normal form, the evaluated full ROC inequality, a finite block-diagonal membership test, the sharp isotropic ROC threshold, QC for the conformal modes at `λ≥1/4`, and impossibility of improving `1/4` while the **primary leading heat correction is fixed**. That last qualification is essential. See [checkpoint capsule, lines 5–23](producer-workspace/CAPSULE.md:5) and [checkpoint report, lines 170–201](producer-workspace/REPORT.md:170).

| Masked return | Correct new contribution relative to this checkpoint | Exact limitation and blocking-error assessment |
|---|---|---|
| `result_7535b35` | **A better compatible QC constant and an additional method obstruction:** moving the leading exact heat primitive proves `λ≥λ_H` for the two conformal cubic modes, with all means and fields and the usual translated/ROC-quadratic extensions. It also proves that `λ_H` is optimal over closed polynomial two-forms of base degree at most two whose corrected density is an SOS of expressions affine in the base and linear in the Hessian. | This is not the sharp QC coefficient and does not reach `3/16`. The barrier is to the specified SOS class; nonnegative densities outside that class, nonpolynomial corrections and other proofs remain possible. No blocking error found. I checked the completeness of the invariant leading Gram family and the cubic coupling constraints, not just the positive identity. |
| `result_d6aa363` | **A broader positive theorem, stronger than QC:** for every M, `λ≥||M||²_F/8` gives an explicit global polyconvex lift through proved minor supports. It reaches the exact ROC boundary for every `rank M≤1`, so ROC=QC=PC is completely classified for their isotropic tails (and determinant lineality). It also proves the full-rank conformal ROC family non-PC for `λ=3/16+d`, `0≤d<d_*=(43−3√205)/288`. | The selector is explicit and its support inequality is globally proved; it is not a selector oracle. The non-PC interval excludes polyconvexity, not QC. The support-selector threshold is not claimed sharp for all PC representations at full rank. No blocking error found; the singular increments follow by continuity of the original polynomial support gap. |
| `result_f6b140e` | **The same better compatible QC constant:** its moving leading primitive and exact joint Gram completion prove `λ≥λ_H` for the same conformal modes, all means and fields, with the same natural extensions. It explicitly explains why the checkpoint's fixed-primitive obstructing jets lose their force. | Its optimization is only claimed within the displayed one-parameter completion bound. It does not establish the larger SOS-class obstruction proved in `7535b35`. It leaves the same QC gap and the other cubic directions. No blocking error found in the full compatible identity or heat-flow argument. |

Consequential source pointers:

- `7535b35`: [moving primitive and global completion, report lines 32–172](producer-workspace/REPORT.md:32); [complete affine-base SOS class and dual inequality, lines 174–245](producer-workspace/REPORT.md:174); [receiver's null basis and general family, lines 60–101](producer-workspace/verify.py:60).
- `d6aa363`: [global minor supports and rational square identity, report lines 41–101](producer-workspace/REPORT.md:41); [non-PC cuts and optimized interval, lines 119–161](producer-workspace/REPORT.md:119); [exact support receiver, lines 9–67](producer-workspace/verify.py:9).
- `f6b140e`: [moving primitive, report lines 35–62](producer-workspace/REPORT.md:35); [full Gram identity, completion and heat implication, lines 64–222](producer-workspace/REPORT.md:64); [standalone exact receiver, lines 44–84](producer-workspace/verify.py:44).

**Comparison.** `7535b35` and `f6b140e` tie on the positive QC frontier. They use the same moving leading primitive after substituting `ρ=2k`, and have the same coefficient `(3+√3)/24`; different Gram coordinates and different rational specializations are not different positive theorems. `7535b35` adds a substantively stronger obstruction for the complete stated SOS class, whereas `f6b140e` limits its optimality claim to its one-parameter bound. Thus `7535b35` has an additional theorem over their common positive result.

`d6aa363` is incomparable with those returns on the central positive-theorem axis. It covers all four M modes, proves PC, and reaches a full isotropic boundary subfamily. The two heat returns reach strictly lower conformal coefficients: for `M=I`, the support construction needs `1/4`, while their compatible proof gives `λ_H`. Conversely, those heat returns do not prove the all-M PC theorem, the rank-one-M boundary classification, or the non-PC interval. Breadth/PC structure and a better conformal QC constant must not be collapsed into one scalar ranking.

**Still unresolved in this block:** QC of the conformal interval `[3/16,λ_H)`, including `P₀`, and the full arbitrary-M/admitted-Q task. The non-PC interval lies inside this still-undecided QC gap; it supplies no ROC/non-QC separation. The SOS obstruction also supplies no negative-energy gradient.

## Verification performed and limits

All execution used `python3 -B`; scripts that write output were copied into this review directory before execution. No source artifact was modified.

- The five final positive/certificate receivers plus the boundary-geometry receiver passed. Their individual stdout/stderr and exit statuses are retained in [replay_summary.json](producer-workspace/replay_summary.json).
- For `8bee532`, I reconstructed the determinant from `P₀`, not only from a stored coefficient list: 7,197 intermediate terms passed, followed by the 5,047 positive-coefficient shifted polynomial and 4,616 nonnegative Bernstein coefficients. The actual two-phase direct-energy implementation check also passed. See [triad replay summary](producer-workspace/replay_summary.json). The direct numerical check is implementation QA; the exact determinant and sign conversion prove the continuum assertion.
- For `7535b35`, I independently started with all 60 homogeneous quadratic two-form coefficients, imposed closure and coefficient matching against the complete symmetry-allowed null-bilinear SOS basis, and recovered exactly the stated three-parameter leading Gram family. Starting with all 24 linear two-form coefficients also recovered `e+k₁=0`, `k₂=0`, `f+k₃=1`. Together with the checked null-basis dimension and the Cauchy–Schwarz dual argument, this supports the claimed SOS-class lower bound. See [independent audit script](producer-workspace/check_sos_completeness.py) and [its output](producer-workspace/check_sos_completeness.log).

I also inspected the heat/Stokes passage, proper-rotation/scaling transport, the safe-conformal-mean completion, the finite-lift subgradient argument, and the determinant-to-Schur inference. I did not rerun every abandoned search or independently re-prove every inherited checkpoint theorem. Failed searches, rejected approximate primitives, new terminology and finite safe samples received no universal-theorem credit. The exact internal certificates establish the scoped mathematics described here; they do not establish historical priority or the unresolved full-face conclusion.
