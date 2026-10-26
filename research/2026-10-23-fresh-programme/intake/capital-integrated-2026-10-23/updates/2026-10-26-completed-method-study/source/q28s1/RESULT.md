# Q28 stage 1 result

**A complete candidate binary-channel comparison theorem was constructed, together with an exact counterexample to an index-only extension. The civilisation-changing scientific capability target is NOT_ACHIEVED. Historical novelty and independent correctness review remain UNKNOWN.**

The initial question was whether the sharp full-matrix reset law could extend to hybrid classical/quantum memories with nonuniform reset weights. Three materially different mechanisms were considered before the main construction: selective assembly, continuously repaired atom arrays, and hybrid dissipative-memory mathematics. Their demonstrated operations, missing bridges and strong incumbents are preserved in `RESEARCH_NOTES.md`. Physical recognition or a new compatible detector was not silently assumed.

The actual constructed claim is broader than a biased-reset formula. For any pair K,L of finite-output classical channels with a **binary input**, define

\[
G_K(t)=\sum_y\frac{(k_{y0}-k_{y1})^2}{t k_{y0}+(1-t)k_{y1}},\qquad 0<t<1.
\]

For every finite quantum reference R and arbitrary classical-quantum hypotheses rho,sigma, including unequal reference marginals, the sharp coefficient in

\[
D(K\rho\Vert K\sigma)-D(\rho_R\Vert\sigma_R)
\le c\,[D(L\rho\Vert L\sigma)-D(\rho_R\Vert\sigma_R)]
\]

is `sup_t G_K(t)/G_L(t)`, provided L is informative; an infinite supremum means there is no finite coefficient. Undefined infinity-minus-infinity differences are excluded. Ordinary classical hypotheses attain every sharpness limit. Thus quantum reference engineering cannot improve the optimum in this exact class.

The construction is an operator identity, not a numerical conjecture. The BKM Hessian is written as an integral of inverse left/right multiplication superoperators. The two input superoperators, after congruence by their sum, become Q and I-Q. They commute without requiring commuting reference states. Completing the conditional quadratic form gives the scalar function G_K evaluated at Q. Functional calculus and affine-path integration establish the all-reference relative-entropy result. Scalar nearby hypotheses prove sharpness. The complete derivation, boundary regularization, CMI consequence, and all-finite-product less-noisy consequence are in `binary_channel_proof.md`.

For a binary-output channel `[[a,b],[1-a,1-b]]`, the resulting exact coefficient is `(sqrt(a(1-b))-sqrt(b(1-a)))²`. The ordinary scalar formula is an antecedent, not the novelty claim. Applied to p=(1/4,3/4), retention 1/2, it gives

\[
\eta=(19-\sqrt{105})/32=0.2735327885637626\ldots.
\]

The weighted commutative reset expectation has complete index 4, but transplanting the full-matrix index formula gives 0.375. The proposed transplant is therefore decisively false. The trace/domain have changed explicitly; this does not refute the public N967 theorem.

The strongest ordinary comparator is exact classical KL/chi-square channel comparison, with competent one-variable model optimization. It uses the same channel matrices, probabilities and channel uses. The construction produces the **same optimum**, with a broader guarantee covering arbitrary quantum conditioning. It does not show a smaller acquisition cost, faster numerical optimizer, memory recovery, or a hardware advantage. Existing scalar comparison and CMI machinery are credited below. No universal-program copying objection is needed: there simply is no demonstrated physical or algorithmic performance gain here.

Executed validation is saved in `NUMERICAL_VERIFICATION.md` and `numerical_results.json`: seven channel comparisons; 2,800 finite-state pairs with reference dimensions 1,2,3,5,8 and both marginal regimes; and 168 local Hermitian-tangent optimizations with an explicitly recorded numerical-null-space threshold. All tested ratios stay below the computed scalar comparison values within stated tolerances. The general-channel scalar optima are numerical estimates, not certified global optima. Four rational comparison bounds additionally have exact polynomial/Sturm certificates in `EXACT_CERTIFICATES.md` and `exact_certificate_results.json`. Run the saved Python scripts to reproduce them. These are local calculations, not source measurements.

The binary boundary is tested rather than hidden. The known three-label uniform-reset simplex witness gives a metric ratio 0.3165666475 at epsilon=0.01, exceeding its ordinary classical optimum 0.3 and tending toward 1/3. This is pre-existing N967 input, independently reproduced as a negative control. The lifting does not extend by the same argument to three input labels because normalized input superoperators need no longer commute.

The theoretical consequence is a way to certify every finite-output binary classical channel comparison against arbitrary quantum side information using an ordinary one-variable certificate, with sharp conditional-mutual-information comparisons and product-register ordering at every finite blocklength. This is a general mathematical unit rather than a one-fixture score improvement. Its exact historical novelty is unresolved; a targeted literature pass is not proof of priority. It is not presently justified to describe its scientific reach as civilisation-changing.

The precise unresolved scientific operation is an analogous complete comparison mechanism for three or more superselection labels, where the normalized positive operators form a noncommuting POVM rather than Q,I-Q. A complete-index scalar cannot supply the general law. A physically improved memory additionally needs an implemented encoding, recovery, sensing and correction cycle with matched resources; none was constructed here. The assignment's broad capability mission therefore remains unfulfilled despite the completed mathematical object.

## Primary sources and versions

- Hirche, George, Nuradha and Wilde, *Conditional contraction coefficients and their applications to quantum networks*, arXiv:2608.27171v1: https://arxiv.org/html/2608.27171v1 . This supplies the pre-existing conditional-contraction/CMI framework. Relevant definitions, equivalence and channel-order sections were inspected.
- Makur and Polyanskiy, *Comparison of Channels: Criteria for Domination by a Symmetric Channel*, arXiv:1609.06877v3 / IEEE TIT (2018): https://arxiv.org/html/1609.06877v3 ; https://doi.org/10.1109/TIT.2018.2839743 . Classical KL/chi-square ordering and its scalar matrix criteria are established.
- Hirche, Rouze and Stilck Franca, *On contraction coefficients, partial orders and approximation of capacities for quantum channels*, arXiv:2011.05949v3, published as Quantum 6,862: https://arxiv.org/html/2011.05949v3 ; https://doi.org/10.22331/q-2022-11-28-862 . Quantum metric/relative-entropy comparison and complete channel orders are antecedents. Version v3 was the retrieved full text; v4 exists.
- Hirche and Shaya, *Partial orders and contraction for BISO channels*, arXiv:2504.16726v2: https://arxiv.org/html/2504.16726v2 . This is a strong ordinary binary-channel comparison antecedent, including BSC/BEC extremality and extension discussion; it is not being claimed as this trial's invention.
- Polyanskiy and Wu, *Strong data-processing inequalities for channels and Bayesian networks*, arXiv:1508.06025v2: https://arxiv.org/html/1508.06025v2 . Classical information-contraction, erasure comparison and network methods are established.
- Astra N967 frozen packet: https://raw.githubusercontent.com/harjassand/astra-research-knowledge/0aecbbdb1fa289741c1f1ed96366610d13d37486/knowledge/current/packets/N967.json . Governing proof: https://raw.githubusercontent.com/harjassand/astra-research-knowledge/0aecbbdb1fa289741c1f1ed96366610d13d37486/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-25-dots-ultra-selected-sources/source/dots/general_inclusion_sharpness.md . The full-matrix result and its simplex construction are pre-existing, with the packet's own scope and internal acceptance preserved.

All executable work and outputs are in this Q28 stage1 directory. No other trial, private key/evaluator/reviewer folder, programme chat, subagent, paid service, equipment or model API was used.
