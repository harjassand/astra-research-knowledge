# Morrey campaign as evidence about Astra's discovery process

Bounded source assessment, 22 October 2026 Brisbane. This does not resume the halted campaign. No scientific computation, optimization or source modification was performed. The reading window began at 17:09:18 UTC on 21 October; exact final time is in COSTS.json.

## Main conclusion

The Morrey work is a counterexample to the diagnosis that Astra only becomes better at producing exclusions. Its strongest supplied artifacts contain constructive, general mathematical mechanisms: a global quadratic anchor for every minimal positive circuit; a gluing argument that accepts arbitrary positive-semidefinite subtractions; a full-skew calibration that rescues a family excluded by the previous restricted calibration; and laminate/Jensen certificates for nontrivial actual gradient families. These are internally supported restricted results, not the full conjecture, historical novelty, formal verification or external acceptance.

The most productive pattern in the inspected record is **turning a failure of a representation into a better representation, then using it to prove a family result and retire the corresponding search space**. Counting the number of agents does not explain that pattern. Forty workers were configured, but there is no matched smaller-team run or complete cost accounting from which to infer the causal return to forty.

## Scientific capital actually visible in original arguments

### 1. A nonlinear family problem became finite convex geometry

`work/ws05/elliptic_universal/lead/MINIMAL_POSITIVE_CIRCUIT_QUADRATIC_ANCHOR_THEOREM.md` is an actual proof, not just a summary. For spanning vectors v_i, m=r+1, with a one-dimensional strictly positive kernel, it constructs probability weights theta_i such that S=sum theta_i v_i v_i^T is positive semidefinite and z^T S z <= sum (v_i.z)_-^2 for every z.

The decisive representation is the support body K=-N B_+ and the identity K intersect (-K)=intersection_i E_(A-v_i v_i^T). This converts the nonlinear global inequality to finitely many PSD inequalities. A D-optimal design W=sum omega_i v_i v_i^T then supplies theta_i=1-r omega_i; first-order optimality gives both nonnegativity of the theta and the required PSD caps. This is a genuine connection between convex design/ellipsoid machinery and the variational certificate problem. It replaces a hunt for special coefficient weights with one structural construction valid in every allowed rank.

I read the proof and the separate body-geometry and D-optimal audits. The two audits have complementary scopes and do not merely repeat a verdict. The body proof includes singular S, and the design audit handles zero weights and boundary optima. The resulting QC consequence still uses the named K generator, quadratic determinant completion, the gluing argument and background extension; it does not cover arbitrary overlapping circuits.

### 2. Complementary work had to change an interface, not merely concatenate results

`work/root_math/psd_negative_update_quadratic_anchor_bridge.md` replaces a rank-one negative update by arbitrary S>=0. Its Schur-complement/inertia calculation yields a PSD block and the translated touching minorant even with kernels and dependent factors. This matters because the D-optimal anchor is generally not rank one. The two contributions therefore fit only after the receiving theorem's admissible object was generalized.

The source attributes the decisive block-inertia argument to WS04 and root, and the anchor construction to WS05. The final combination genuinely expands the theorem's scope to all one-minimal-circuit networks in up to four matrix coordinates, including affine offsets via a separate argument. The attributions and chronology are producer records; this review observes the complementary proof dependencies, not the original conversations.

This is a more consequential form of knowledge reuse than copying a proof or retaining a filename: one investigator's result changed the input class another construction could accept. A transfer assessment should ask whether the composition removes an actual frontier assumption.

### 3. A restricted certificate failure was followed by a successful representation extension

`work/ws05/nullity_two/continuation/lead/EXACT_PROFILE_AND_CONTRACTIVE_MODE_OBSTRUCTION.md` supplies a rational stationary four-cut member excluding every homogeneous graph-vanishing single-K choice. Its proof uses incompatible exact lower/upper requirements on kappa. It carefully does not infer non-QC from this obstruction.

`work/root_math/full_skew_graph_k_criterion.md` subsequently permits h=k.u+v.z, rather than imposing v=0. Its PSD/range/pseudoinverse conditions are necessary and sufficient for that architecture, including singular blocks. `work/root_math/optimal_tilt_four_cut_universal.md` chooses the optimal tilt xi=beta/(1+lambda0), producing an exact nonnegative residual and handling signed beta and the singular endpoint directly. The member that defeated the earlier architecture is now included in the stated QC family.

This sequence is unusually useful meta-evidence. The earlier exclusion was scientifically correct but not decisive about the object. The gain came from identifying that graph-vanishing was an extra representation restriction, not an essential constraint. More numerical resolution within the excluded architecture could not have supplied this extension.

The record also states that root and WS05 obtained the tilt independently and simultaneously. Thus some parallel work was duplicative rather than complementary. That provides redundancy and checking, but it is not evidence of a proportional discovery gain from parallelism.

### 4. Exact examples became whole-law theorems and removed wasted search directions

`work/ws10/strip_exchange/full_flow/ACTUAL45_FULL_LAW_R1C_JENSEN_THEOREM.md` covers every finite global R1C test on one actual 45-triangle law, all affine backgrounds. The exact constructive object is 39 positive root children, binary rank-one trees, exact terminal mass recovery and determinant-zero roots. The proof explains why the roots need not themselves be assembled by a pairwise rank-one binary tree.

The earlier 1,967-column partial allocation was infeasible. The expanded 13,970-column dictionary produced an exact 39-root support; only that small verified support is needed for the theorem. The resource log records that later negative probes on this actual law were withdrawn. This is an observable shift from repeated integrand testing to a universal certificate for the fixed field. It does not make the failed partial dictionary useless, nor does its failure show a nonlaminate law.

The analytic successor in `work/root_math/four_fans_and_three_interior_vertices.md` covers arbitrary vector nodal values on admissible nested triangular layers and triangular meshes with at most three interior vertices. Its boundary accounting is substantive. A four-face fan laminates at its own mean, but replacing it by the mean affine map would erase a nonaffine quadrilateral boundary trace. The supplied convex-test counterexample defeats universal degree-four physical coarsening. The proof explicitly avoids that invalid composition.

## Failures that discriminate competing diagnoses

1. **Wrong representation versus insufficient compute.** The graph-vanishing no-go and successful full-skew rescue directly separate these explanations for one family. The resource record does not support the claim that more optimization in the old family was needed.

2. **Formal admissibility versus favourable local data.** Negative conditional packets coexist with globally Jensen-positive actual parent maps. Determinant moments and finite laws alone are not actual gradients. This is the mathematical analogue of a component response that cannot be assembled into an operating physical system, but the mathematical obstruction concerns boundary/compatibility, not experimental access.

3. **Review can retract a real inference.** `work/ws04/hsharp_transport/RELAXED_ZERO_GAP_ACTIVE_CORE.md` preserves a withdrawn traceless-active-core conclusion. The algebra admitted same-endpoint tails of both relevant signs, so a zero integrated moment did not eliminate them. Valid joint identities were retained. This is not evidence that every review works; it is a specific correction to a nontrivial inference.

4. **Finite failure remains finite.** `work/ws06/hessian/TWO_CORE_ROUND_REPORT.md` has an actual compatibility-preserving, 137-parameter C1Q2 test with a far-tail and negative-density region forced into every feasible potential. The 640-iteration run reduced a positive gap from about .419 to .249, had nonzero final projected gradient, and established no optimum. The chosen method seriously attacked the correct boundary, but more iterations are not justified by these numbers alone.

5. **Finite exactness is not universal resolution.** WS07's all-real-amplitude line has 85 exact quadratic pieces and global line minimum zero. Its full four-dimensional span avoids earlier trivial exclusions, so it is not merely an easy sanity check. Still, one line does not settle QC. The source pointwise floor -1/3 is correctly distinguished from a negative Jensen gap.

6. **Success does not settle the parallelism question.** The campaign combined root synthesis, independent lemma work, numerical discovery, counterexamples and exact replay. It has 40 configured agents, all fresh initial forks, repeatedly reused. There is no controlled warm/fresh or small/large-team contrast. The successes refute 'large parallel campaigns cannot produce substantive results'; they do not prove that forty was efficient or necessary.

## Resource and trace limits

The package records 10 gpt-6.1-sol/max and 30 gpt-6-luna/max accepted configurations and zero additional spawns. One Luna was reassigned to CPU/process management. I counted 95 saved host snapshots, from 10:57:23 to 16:30:25 UTC, plus a 69,842-byte manager status file. Many samples show no active scientific compute and substantial CPU idle time; unrelated applications sometimes constrained headroom. This is not evidence that agents were idle: proofs and model inference are not measured by local Python CPU usage.

The detailed manager history preserves source-guard, metadata, report-key and numerical-control failures. Some repairs were consequential, including an ill-conditioned float reference formula and a checker wrongly demanding equality with a deliberately coarse bound. Others were transport/metadata overhead. These records establish real integration cost, but do not meter total model tokens, researcher reasoning time or opportunity cost. No valid all-in cost-per-discovery or team-size speedup can be computed.

The audit read selected original arguments and independent checks, not all 6,325 payload paths. It did not rerun exact scripts or optimizers, contact authors, refresh literature or inspect hidden reasoning. Historical novelty and external correctness remain unknown. The repository pin and manifests provide provenance rather than proof certification.

## Recommended difficult meta-research experiment

Use the **historical pre-anchor obligation**, not a new Morrey continuation. Freeze a self-contained seed containing spanning v_1,...,v_(r+1), the strictly positive one-dimensional dependence, and the desired global anchor inequality. Require a construction and proof for arbitrary rank, singular anchor and boundary support; numerical examples do not pass. The original theorem is held out only as a grading reference. The identical seed and ordinary tools go to both arms, so no necessary mathematical premise is withheld from the baseline.

Strong baseline: a capable fresh agent with unrestricted choice of mathematical methods and a fixed substantive time budget. Treatment: the same model/budget/information, with an explicit initial obligation to identify the representational restriction, seek an exact alternative representation, and state what failure in the chosen representation would and would not establish. Do not supply 'D-optimal design' or the body identity only to treatment: those would give away the substantive solution rather than test a research strategy.

Measure the strongest verified uniform theorem and gaps, not verbosity, activity or confidence. Charge the representation phase inside the same budget. Independently inspect proof dependencies and boundary cases before scoring. If both solve it, the task is saturated and provides no strategy evidence; if neither does, do not infer equal long-term ability. A single historical example can be overfit, so any apparent gain needs a different obligation and later independent owner use before adoption as a system-wide rule.

An optional harder endpoint is composing the anchor with the supplied PSD bridge to prove all-background QC, but that mixes two obligations and should not quietly alter the first endpoint after observing results.

## Recommendation to the parent evaluator

Treat Morrey as evidence that Astra can create connected mathematical capital and generalize across representations, while its most important conjecture remains open. Preserve its halted status. Do not score it as zero because the main conjecture is unsolved, or as transformative because many audited partial theorems exist. The most promising general research-process hypothesis is that explicitly separating an object's constraints from a certificate's restrictions can prevent premature retirement and expose a reusable structural operation. That hypothesis deserves a controlled test, not blanket compulsory process overhead.
