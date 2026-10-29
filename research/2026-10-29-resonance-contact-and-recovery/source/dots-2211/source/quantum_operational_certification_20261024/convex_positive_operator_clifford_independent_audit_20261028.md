# Independent review: convex channel proposal for acquired Pauli-algebra recovery

2026-10-28. Reviewer producer-workspace/review_trace_class_synthesis. PASS at the precise scope/version in the receipt. This review is separate from the received positive-operator feasibility theorem and does not modify it.

## 1. Choi conventions and full convex optimality

With K=sum_rs |r><s| tensor Phi(|r><s|), unitality is Tr_aux K=I_d, NOT trace over output; TrK=d. Pauli expansion gives K=(I tensor I+sum sigma_j^T tensor A_j)/2. Direct contraction gives TrHK=sum Tr C_j A_j, with no missing2 or d factor.

Set D_j=sigma_j^T tensor I−I tensor B_j. Expanding one-half sum D_j(I tensor T_jk)D_k gives I tensor sum T_jj−H. Symmetry of operator blocks cancels each off-diagonal Pauli anticommutator in BOTH factors. Cross terms use commutation only with true B, never with unknown candidate A. The block quadratic form is positive for arbitrary vectors, including noncommuting coefficient entries. The true embedding is primal feasible and attains Tr sum T_jj; hence it is optimal over the entire unital-CP set, not merely exact representations.

For T>=tau I, Q dominates tau(3I−sum sigma_j^T tensor B_j). Multiplication by a PSD feasible K and tracing gives tau(3d−sum Tr A_j B_j). Unital positivity implies each Hermitian A_j is a contraction; sum Tr A_j²<=3d. The stated Frobenius curvature and noisy empirical-optimum bound follow. This proof includes unital CP maps with nonunitary/nonrepresentation Pauli images.

## 2. Finite convex step and actual scope of efficiency

The affine parameterization by three Hermitian matrices is exact and has a known interior. In ordinary real diagonal/off-diagonal coordinates, a Euclidean radius1/4 around A=0 gives ||K−I/2||op<=1/4. Every feasible A has coordinate radius <=sqrt(3d)<=2d for d>=2. Thus explicit rational inner/outer bounds are available; the established rational PSD-separation/weak-optimization machinery applies without a hidden Slater or conditioning oracle. The received endpoint source supplies that general finite machinery, not the present dual proof.

The repair Kphys=(K+eta I)/(1+2eta) is exactly unital and PSD when the unrepaired affine K has spectral floor−eta. Its Pauli images are A/(1+2eta). To check the displayed repair bound even when original K is not CP, observe that repaired images are contractions, so ||A_j||op<=1+2eta. Therefore the absolute objective displacement is at most6d(1+a)eta. Weak optimization and repair errors must jointly fit zeta.

The polynomial finite convex-optimization claim concerns the local SDP, in dimension2d, coefficient precision and requested objective error. It is NOT a blanket polynomial end-to-end bit complexity claim for arbitrary symbolic spectral field representations, gate output or the exponentially width-dependent acquisition bill. No actual generic SDP run is claimed in this receipt.

## 3. Physical rounding and observed positive-fit guard

Unital-CP output images need not satisfy Pauli algebra relations. Rounding is therefore essential. For X=sign(A_X), Zodd=(A_Z−X A_Z X)/2 exactly anticommutes with X. If Zodd is invertible, its sign also anticommutes, and X's positive/negative eigenspaces are balanced. Consequently Y=iXZ completes the correctly handed physical triple.

If ||A_X−B_X||<=epsilon_x and ||A_Z−B_Z||<=epsilon_z, nearest-unitary sign projection yields ||X−B_X||<=2epsilon_x. Odd projection then gives ||Zodd−B_Z||<=epsilon_z+2epsilon_x, and its sign gives ||Z−B_Z||<=2epsilon_z+4epsilon_x. These bounds demonstrate completion as the SDP error vanishes; gaps approach one. Soundness ultimately uses the RECEIVED acquired positive-fit residual, not these unknown-error estimates.

Exact anticommutation must not be inferred from floating residuals or independent approximate diagonalizers. The source now retains a common representation: diagonalize X, extract the off-diagonal block of Zodd, take its polar unitary, and use one common basis for the whole triple. Exact algebraic nominal matrices or a rigorously synthesized common-unitary representation preserve physicality; actual finite gate errors are paid separately. Norm/positivity/residual certificates must include numerical uncertainty. The subsequent fit certificate then handles any physical candidate, even a suboptimal numerical SDP result.

## 4. Physical-source scope retained

The parent source's private current coins, actual local ordinary preparations/readouts, predictable-history contrast means, one fixed global V, symmetric positive operator blocks, acquired support and retained-memory transfer remain load-bearing. This upgrade provides candidate generation; it does not prove those premises from finite data. Under a persistent true positive block gap, shrinking data and SDP errors yields convergent images, physical rounding, positive fitted block and eventual acceptance. Finite caps can abstain. Fixed-inverse comparison, known-code composition and the actual3n-gate telescope remain distinct from optimal-noise correction or a fault-tolerance threshold.

## 5. Independent evidence

convex_clifford_channel_independent_check_20261028.py imports only this reviewer's earlier noncommuting fixture, not root author code. It verifies the complete8-by-8 Choi factorization, true embedding optimum and dual annihilation exactly. Nine exact mixtures of distinct unital physical embeddings verify Choi objective normalization and both curvature inequalities. Three exact negative-spectral-boundary repair cases verify unitality and objective allowance. Nine floating rounding illustrations check spectral gaps, anticommutation and the derived approximation bounds; those floating examples do not themselves certify exact nominal gates. Source calls, generic SDP executions and hardware operations are zero.

Received: exact convex dual/curvature upgrade, finite rational SDP candidate mechanism, physical rounding with the stated arithmetic/control obligations, and transfer through the already received acquired fit certificate. Not received: generic solver execution, polynomial end-to-end hardware runtime, statistical/hardware advantage, unrestricted noise identifiability or historical novelty. Conventional recovery SDPs and local-operator sewing are credited; the new scoped claim is the positive-block dual and its certified acquisition use.
