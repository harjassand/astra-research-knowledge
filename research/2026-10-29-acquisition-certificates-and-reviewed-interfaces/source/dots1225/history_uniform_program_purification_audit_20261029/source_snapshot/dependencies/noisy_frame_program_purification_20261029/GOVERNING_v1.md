# Approximate frame programs from noisy acquired records
2026-10-29. Author draft, not received. This is a task-specific composition of established recursive SWAP purification, not a new purification algorithm.

## Interface and assumptions
Assume independent fresh batches from a memoryless source produce IID normalized label states sigma=x Pc+(1-x)PW/8, W=c-perp in C9, c=vec(R)/sqrt(3). Their minus-flag probability p_minus>0 and ordinary source-call costs are charged separately. This is a label-level model, NOT an automatic consequence of arbitrary channel depolarization. Exact trusted controls and protected storage remain assumptions. Root's exact absorption calculation gives an eventual growth output tau_0=(1-v_0)Pc+(v_0/8)PW, an expected normalized-label cost mu_0, and v_0≈0.2442 at x=.01. We require v_0<8/9 so c is the unique largest eigenvector. The unbounded process is used only as an analytic reference; finite deployment is capped below.

## Explicit purification operation
Acquire two independent copies of the same tau_j. Measure symmetric versus antisymmetric support with a controlled-SWAP and one flag. On symmetry, discard one copy and retain the other; on failure discard both and restart this level. The unnormalized retained state is (tau_j+tau_j^2)/2. Therefore
 D_j=2-2v_j+9v_j^2/8,
 p_j=D_j/2,
 v_(j+1)=v_j(1+v_j/8)/D_j.
This retains the isotropic family and unknown c without estimating c. Independence is essential; source-memory-correlated batches do not inherit this recurrence. For 0<v_0<8/9, v_j decreases to zero. With kappa=(1+v_0/8)/D_0<1, v_j<=v_0 kappa^j (the ratio increases with v on this interval). Thus a finite number of levels suffices at any positive error target. No finite level is exactly pure when x>0, consistent with the full-rank exact-gate obstruction.

Expected base-program cost C_0=1, C_(j+1)=2 C_j/p_j=4C_j/D_j. Expected ordinary calls are mu_0 C_j/p_minus. Expected counts follow independent restart/Wald accounting, not an assumption that record cost and output are independent. A depth-first recursion stores O(j) nine-dimensional programs, plus the eight-label growth workspace, one SWAP-test flag and known controls. Each four-qubit encoded program SWAP uses four controlled bit swaps. Acquisition and transducer controls are additional.

For v_0<1 (in particular .2442), define K=1/8+2/(1-v_0). Since
 C_(j+1)v_(j+1)/(C_j v_j)=4(1+v_j/8)/D_j^2 <=(1+v_j/8)/(1-v_j)^2,
 we obtain C_j v_j <= v_0 exp[K v_0/(1-kappa)]. Also v_(j+1)>=v_j/2. At the first level reaching v_j<=epsilon, C_j <= 2 v_0 exp[K v_0/(1-kappa)]/epsilon. This elementary bound is conservative; exact recurrence gives useful constants. It establishes O(1/epsilon) expected base programs for fixed v_0, in agreement with prior purification theory.

## Finite cap without postselection mistake
Let the ideal, always-eventually-terminating recursive protocol have expected ordinary-call count M. Stop at the public cap ceil(M/delta). Markov gives abort probability at most delta. DO NOT infer the capped successful output is exactly tau_j: growth runtime can correlate with output. Instead couple the capped and uncapped physical experiments until the cap. Their full output states, with abort flag retained, differ in trace norm by at most 2 delta after any fixed completion convention. Conditional on cap success, the retained state is within trace norm 2 delta/(1-delta) of tau_j. This explicit correction is charged when delivering a program. It is not a claim of IID capped outputs with the uncapped state law.

## Robust transfer to quaternion/Choi program
Two independent purified programs tau_j have trace-norm distance at most 4v_j from Pc tensor Pc. Use the independently accepted four-output transducer K, whose ideal success probability is p0=16/27 and ideal output is q tensor4. CP trace contraction bounds the unnormalized output difference by 4v_j and the success probability change by 2v_j (event distinguishability). Hence actual success is at least p0-2v_j, and its conditional four-program state differs from the ideal by at most 8v_j/(p0-2v_j) in trace norm. This deliberately conservative bound holds whenever 2v_j<p0. Discarding three programs and applying the fixed Bell-basis map gives one approximate Choi program with no greater error. Repeat independent complete batches for multiple programs; do not silently treat the four outputs of one noisy successful transducer as independent.

Cap error must be added to the input trace-norm budget before this normalization. A separate product-resource port-based teleportation analysis is owned by the comparator reviewer. No deterministic gate or many-gate fidelity claim is inferred here from one-outcome gate teleportation.

## Prior art and comparison
Childs et al., *Streaming quantum state purification*, arXiv:2309.16387v3, Sections 2–3, supplies the same recursive SWAP gadget and established inverse-error scaling. We independently derive the specific nine-dimensional recurrence and composition above. Watts et al., arXiv:2610.06737, supplies the generic antisymmetric growth predecessor. Neither mechanism is claimed novel.

At fixed dimension nine, conventional tomography/eigenvector estimation is a serious equally informed baseline; a classical estimate can be reused for arbitrarily many gates, whereas quantum programs are consumed. No advantage over that baseline, arbitrary-memory robustness, unknown spectral-gap removal, or practical implementation has been established. The opening is a concrete approximate-operation route under an explicit noisy IID model despite impossibility of finite exact heralding.

## Concrete physical model (dependent on root's separately reviewed derivation)
Root proposes N_eta=(1-eta)N_collective_twirl+eta D_4 on two carriers. Its commutator matrix is H=I-(1-eta)Pc, giving p_minus=(8+eta)/18 and x=eta/(8+eta). This identification is a dependency, not established by the recurrence code. `check_recurrence.py` evaluates the exact absorption formulas supplied in `robust_frame_program_boundary_20261029/check_growth_pollution.json` with this substitution and independently checks the symmetric-SWAP tensor identity on15 mixed states in dimensions2,3,9. At eta=.01, v_0=.03567419574 and the base expected call cost is292.0131. Nine purification levels give v≈7.5645e-5 at expected160843 calls per purified R program; sixteen give v≈5.9108e-7 at expected20.591 million calls. These are analytic ideal-model expectation evaluations, not executed million-call quantum trajectories; finite cap, two-program conversion and gate-processing costs are extra. Decimal numerical evaluations are not standalone interval certificates.
