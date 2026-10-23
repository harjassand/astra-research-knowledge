# Current available scientific operations

23 October 2026. These are source-reported internal conclusions, with their
original limitations. This integration checked source identities and routing;
it did not independently prove the theorems or repeat the experiments. Read the
governing source before using a result. Historical priority and external
acceptance remain unknown unless supported separately in that source.

## Pro1: recurrent communication, entropy and bath-depth cost

Read the Cycle11 [whole-bath theorem](cycle-11/pro1/ENTROPY_DRIFT_AND_DEPTH_COST.tex),
[complete inherited proofs](cycle-11/pro1/COMPLETE_SOURCE_PROOFS.txt),
[results](cycle-11/pro1/RESULTS.txt), [resources](cycle-11/pro1/RESOURCE_RECORD.json)
and [failed routes](cycle-11/pro1/FAILED_ROUTES.md).

For the unchanged recurrent tree device, initially independent input and normal
bath initializer, the new entropy–displacement inequality retains the actual
root and permits arbitrary input correlations. With b=beta² its entropy
ceiling is c(b)=log2[2 sqrt(2)(1-b)+3b]. A finite-error arbitrary-code
rate–depth inequality charges final mean bath displacement. The inherited
actual encoder is shown to have O_beta(log N) final mean depth at tau_pi,
uniformly over logical states and retained references.

Consequently the excess of the explicitly **sublinear-final-mean-depth**
capacity Q_sub is Theta(beta²), for fixed 0<beta<=1/32, between the inherited
lower `(ln 2)/2^20 * beta²` and `log2[1+(3/(2 sqrt(2))-1)beta²]` above 3/2.
Unrestricted capacity is still open. Final mean depth is neither maximum
intermediate depth nor trace-norm bath return. Initial input–bath independence
is essential. Pure push gives linear depth but only logarithmic complementary
entropy; it does not exhibit a high-rate code.

The older finite-angle lower bounds remain usable: the Cycle9 clipping
certificate beats Cycle10 at beta=1/512. Input dimension 3^k with
k=floor[1/(256 beta²)] and enormous cutoff constants prevent an efficient
finite-horizon claim. The remaining owner question is reference leakage for
escape-compatible high-entropy inputs and general logical encoders. Its
proposed lower bound is unproved. This new converse is not a feedback or
unrestricted-capacity converse.

## Pro2: four original noisy actions with arbitrary bridges

Read the Cycle11 [proof](cycle-11/pro2/PROOF.md), [result](cycle-11/pro2/RESULT.md),
[implementation](cycle-11/pro2/src/bridge_recovery.py),
[fixed sources](cycle-11/pro2/sources/), [receiving checks](cycle-11/pro2/verification/),
[costs](cycle-11/pro2/COSTS.md) and [failure](cycle-11/pro2/FAILED_APPROACHES.md).
The full [Cycle5 predecessor](cycle-05/pro2/) is present, not replaced by a
partial cache; all predecessor ZIP identities are in the export bindings.

Every finite chordless graph of treewidth<=2 and maximum degree<=4, including
arbitrary bridge forests, isolated vertices and disconnected components, has
a constructive coordinate q=4 design with canonical least-squares inverse:

`||Dhat-D||op <= ||Dhat-D||F <= 3 sqrt(2) ||E||F`.

The support is known before design; D is an arbitrary real symmetric matrix
with a free diagonal, each whole query row has norm<=1, and E is arbitrary
absolute Frobenius action noise. All original vertices/actions remain. The
stronger bridgeless constant sqrt(3+sqrt(5)) survives. Preparation costs
O(n+m log m) arithmetic plus a charged fixed certificate load; action, bit,
precision, residual and output costs are additional.

The new root qualification, both bridge resets and quantitative pendant-leaf
bound are essential. Omitting the same-entry outgoing prohibition fails on a
chain of triangles. Exact saved receivers establish only their native inputs;
the all-size result depends on the proof and inherited semantic certificate.
The coordinate lower count four is not an arbitrary-real lower on this
subclass. The full nonchordless degree-four partial-two-tree q=4 question
remains open; its strong conventional q=5 control and applicable q=3 forest
controls remain. No molecular/NIST, AD, physical or runtime advantage is
established. The next owner question is a realizable quantitative two-vertex
separator interface in a nonchordless block.

## Pro3: the native finite critical phase law

Read the Cycle11 [path-composition theorem](cycle-11/pro3/NATIVE_PATH_COMPOSITION_THEOREM.md),
[report](cycle-11/pro3/REPORT.md), [comparator](cycle-11/pro3/COMPARATOR.md),
[contract](cycle-11/pro3/INFORMATION_AND_COST_CONTRACT.md), [recorded evidence](cycle-11/pro3/evidence/)
and [reviews](cycle-11/pro3/reviews/).

The formerly open arbitrary-geometry phase gap is internally closed for the
finite native contract: positive pi,q; q initialization; one population
D(pi||q)<=K; fixed lazy mixture alpha; target-independent reciprocal
row-stochastic proposal; and the unchanged two-stage correction. Parameters
and proposal stay fixed during each run. In the strict zero-attenuation
critical regime d>d_star, with c(d)u_n=loglog n+s+o(1),

`(log n) R_n = max{K, (1-exp(-K)) exp[-s-Psi({u_n/d})]} + o(1)`.

Definitions of c, d_star and Psi and all other regimes are in the governing
proof. The unrestricted liminf now matches the phase lower bound; it need
not equal the limsup. The path bridge retains actual diagonals, signed local
progress, proposal cycles/merging, global hits, and post-hit returns. Its
reverse reference is not a Markov chain; the explicit (3/2)^N defect is paid.
No free absorbing operation or additional KL budget is supplied.

Ordinary independence MH remains the strong same-information comparator and
has amplitude K. The hybrid can be worse; this is not an acceleration claim.
The new 16,401 tagged-path check is a finite K=24 diagnostic, not a K=1
critical-scale experiment. The old admitted 32-state and failed-K=1
5,462-state fixtures remain unchanged. The theorem is exact-real, not a
floating-point sampler certificate. The selected standard-Borel extension,
including singular proposals and an actual atomless realization, remains open.

## Ultra: pooled recovery priced by inventory entropy

Read the immutable Cycle11 [principal proof](cycle-11/ultra/PROOF.txt),
[status](cycle-11/ultra/STATUS.json), [comparator](cycle-11/ultra/COMPARATOR.json),
[costs](cycle-11/ultra/COSTS.json), and the subsequently completed
[access supplement](cycle-11/ultra-access-supplement/PROOF.txt).

For the declared complete queue source and **known finite prior** p on K,
fixed finite D,L, then r->infinity, the target is a deterministic fixed Bell
rank on every branch, decoupled from the complete actual residual. Initial
apparatus is local product and independent; no hidden clock record or
entangled aid is supplied. With B=E[K]ln D and H=H(K), the source reports

`max{0,(H-c(D^-2))/2} <= B-R(p) <= H+kappa_D`.

Thus growing prior entropy gives Theta_D(H(K)) loss; bounded entropy gives
bounded loss regardless of support diameter. This does not assert a Theta(H)
law near zero entropy. Partial breeding, compression, hashing, and seed
recycling are established machinery; the proof pays their actual resource
and whole-block error. Typical-set decoding can be exponential. No efficient
quantum compiler or useful blocklength is supplied.

Under matched conventions R(p) equals ordinary two-way distillable
entanglement of the actual rho_p. An equally informed conventional source
can use the same receiver. Older periodic receivers can win at finite sizes;
there is no formation or computational advantage claim. The old pointwise
per-queue profile task is different and remains closed at its original scope.
The remaining principal owner question is whether broad-prior deficit can
reach H(K)/2+O_D(1), or a stronger converse separates that coefficient.

The additive supplement proves that a fixed positive **global** erasure
outage preserves the zero-aid reliable fixed-rank capacity, while iid
per-queue reveal/erase records can increase it even with matched specified
entropy/mutual-information summaries and record dimensions. It corrects a
mean-information generalization, preserves the principal proof, and supplies
no experimental hidden-clock readout or compiled quantum code.

## Dots: a measured ordinary dilute finishing benchmark

Read the Cycle11 [report](cycle-11/dots/REPORT.md),
[sampling and dose identity](cycle-11/dots/calculations/SAMPLING_AND_DOSE_PROOF.md),
[endpoint implementation](cycle-11/dots/calculations/endpoint_ledger.py),
[independent endpoint review](cycle-11/dots/independent_endpoint/REVIEW.md),
[decision](cycle-11/dots/DECISION.txt),
[failures](cycle-11/dots/CORRECTIONS_AND_FAILURES.txt),
and [source attribution/licenses](cycle-11/dots/SOURCE_LICENSES.txt). The actual
deposited workbook, extracted numerical inputs and recorded outputs are present.
The completed Cycle11 archive was recovered at the final source checkpoint;
its exact identity is in the registry. No calculation was repeated for this merge.

Yang et al., DOI10.1038/s41467-025-60696-3, and the deposited source data
DOI10.6084/m9.figshare.28210994.v1 supply separate nitrite/nitrate measurements
for an ordinary dark H2O2 batch at nominal 0.5mM nitrite, 1mM peroxide, pH3,
298K. This is a published model solution, not an actual captured plasma-liquid
matrix or a new experiment by Astra. The workbook remains unchanged. The
adoption of mM despite a microM sheet header is an explicitly documented source
interpretation based on the SI axis/caption and identical main-figure values.

Initial nitrate is nonzero. Reported means give 99.6112% nitrite conversion,
97.8455% net nitrate per initial nitrite, and 98.2275% net nitrate per nitrite
lost. These denominators differ. For a well-mixed unreplenished batch the
ledger is `P_net=(V0-sum vi)ct+sum(vi ci)-V0 c0`; a final aliquot only partitions
that inventory. Under the **declared** 100mL initial volume and four exactly
1mL pre-endpoint samples, including time zero, it gives 45.8891 micromol net
nitrate in remaining plus analytically sampled liquid and 0.458891 mol per
nominal mol peroxide charge. Omitting the time-zero withdrawal gives 0.463539.
Those are conditional point reconstructions, not certified yield intervals.
Analytical exports are not isolated saleable product, and nominal charge is
not measured consumption or independently standardized delivered dose.

The new source supplies a useful conventional finishing operation with measured
product amplitude. It does not establish complete original-N attribution,
peroxide-caused nitrate increment without a nitrate blank, complete calibration
and sampling uncertainty, reagent recovery, fertilizer quality or plant economy.
The source SD box is sensitivity, not a confidence or guaranteed interval.
Dark treatment supplies no positive photon denominator. The photochemical
search did not recover a qualified matched absolute product/delivered-dose
comparison; an OH or initiation yield is not a nitrate yield.

The [Cycle11 evaluator observation proof](cycle-11/evaluator/reviews/empirical_observation_countermodel.md)
and [Max corrections](cycle-11/max/CORRECTIONS.json) supply a separate narrow
identification argument: calibrated net original-N product and positive dose
can determine their quotient without every gas species. Dots accepts that
correction; the stronger metrological dose contract is still not established
by this source. Full gas/emissions claims require their own observations.
The next owner question is effectiveness in an actual captured-liquid matrix
with product, reagent charge/residual and collection history established.

The [Cycle10 photon/inventory comparison](cycle-10/dots/photon_independent/matched_photon_proof.md)
and the positive nitrate observations survive at their original scope. The
ordinary chemical benchmark is not compared with a 532nm initiation-energy
floor as if both were measured nitrate efficiencies. Nitrite finishing does
not itself fix new atmospheric nitrogen. No new kinetic trajectory or hardware
operation is selected by this integration, and T3.1/T4.1 remain untouched.

## Evaluation and integration boundaries

[Cycle11 evaluator](cycle-11/evaluator/REPORT.txt) and
[Max operation ledger](cycle-11/max/OPERATIONS.json) govern their own assessment
of **Cycle10**, not the new Cycle11 owner proofs above. Their retrospective
proof-budget comparison and countermodels retain their stated controls,
initial errors/corrections and missing costs. The result is not an agent trial
or evidence of a learned inventor, recursive self-amplification, normalization
alone as a causal mechanism, or programme-wide advantage. Earlier scoped CPU
gains remain at their actual workload and information boundary.

Every cycle's native cost and failed-attempt records remain beside its source.
Unknown inference, discovery, review, total runtime or memory costs stay unknown;
short replay times are not substituted for them. No active job, resource booking,
pending background collection or external scientific acceptance is inferred from
a dated handoff. Further scientific work returns to its named owner.
