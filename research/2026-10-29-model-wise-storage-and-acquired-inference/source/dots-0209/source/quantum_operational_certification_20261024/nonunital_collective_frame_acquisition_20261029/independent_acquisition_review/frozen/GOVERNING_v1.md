# Physical frame acquisition for nonunital collective channels with retained memory
2026-10-29. New extension, pending independent review. No random-unitary or training-reset premise is used below.

## Common structural promise: completeness, not model-free soundness
Fix unknown local rotations V_i and their twisted permutation operators. Every complete acquisition source operation on data and retained apparatus memory has Kraus operators commuting with these SAME twisted permutations. Thus, for every conditional current bath state and every pair i,j, the full reduced adjoint channel fixes the twisted swap S_ij. The physical source can be nonunital, globally entangling and history dependent. Probe inputs are fresh and independent of the current bath; all current random settings/signs are private through the source call, with a common native port/time boundary.

This is a structural promise for successful frame identification. It is not inferred by fitting data. The separate sequential weighted guard is model-free for soundness of an accepted finite operation and can abort safely for a bad candidate frame. Failure of excitation/identifiability can prevent acquisition completion or yield; no generic learning theorem for arbitrary channels is asserted.

## Rectangular pair-adjoint defect
For each pair define the current pair channel by inserting maximally mixed spectator qubits and tracing them at output. Let P_0=I,P_1=X,P_2=Y,P_3=Z. For correlation-output column(a,b), a,b∈{1,2,3}, and full input row(p,q), p,q∈{0,1,2,3}, define
 T[(p,q),(a,b)]=(1/4)Tr[(P_p⊗P_q) N_pair†(P_a⊗P_b)].
T is real16×9. Let J be the fixed inclusion of the nine correlation coordinates into these16 Hermitian coordinates, J[(p,q),(a,b)]=1[p=a,q=b], and M=T−J.

Write C_ij=O_i O_j^T, where O_i=Ad(V_i)∈SO(3). The twisted swap is
S_ij=(I+Σ_ab C_ij,ab P_a⊗P_b)/2.
The pair adjoint fixes S_ij and, since it is unital, fixes I. Therefore M vec(C_ij)=0. This does not assume N_pair is unital in the Schrödinger picture. Retaining all16 rows explicitly accounts for identity and one-body terms generated in N_pair† of a correlation observable. A unit eigenvector of a random-unitary9×9 block is no longer the governing object.

At call r, conditional on past history, let M_r be this matrix for the current bath state. The true C_ij lies in EVERY kernel. Consequently it lies in the actual predictable occupation average Mbar_m=(1/m)Σ_r M_r. The occupation average is random and history dependent; it need not be the channel at any future time.

## One common randomized physical bank: all edges and all entries
On EVERY call, independently for EACH site choose an input axis c∈{1,2,3} uniformly and sign u∈{−1,+1} uniformly, and prepare its ordinary Pauli eigenstate ρ=(I+uP_c)/2. After the source call, independently choose each output measurement axis z∈{1,2,3} uniformly, and record its sign y∈{−1,+1}. Output choices may be made after source isolation. Prepare and measure all n sites. All sites/signs/settings are independent fresh private coins before conditioning on current outcomes.

Define input features f_0=1 and f_p=3u·1[c=p] for p=1,2,3. Directly,
E[f_p ρ]=P_p/2.
For star pair(i,1), set
 X_r[(p,q),(a,b)]=9·1[z_i=a,z_1=b]·y_i y_1·f_p(i)f_q(1).
Then E[X_r|past]=T_r, entry by entry. Other sites average to I/2 because their independent signs are unweighted. This remains true for an arbitrary global channel, even if the pair output depends on ALL spectator inputs before averaging. The same shot contributes to every star edge, with arbitrary cross-edge correlations.

Crucially, all144 entries use the SAME chronological bank. Acquiring separate deterministic entry blocks under a changing bath would average different channels in different columns and could destroy the common-kernel argument. The old all-leaves pure +c schedule relied on product-unitary marginal structure and is not imported here.

The largest absolute estimator value is81. For a fixed entry, E[X_r²|past] is at most81: output-axis importance has second moment9, and each nonidentity input feature has second moment3. Also |T_r entry|≤1 because N_pair† maps a Pauli unitary to a Hermitian contraction. Therefore the martingale difference obeys |X_r−T_r|≤82 and conditional variance≤81.

A scalar martingale Bernstein bound gives, for0<eta≤1,
Pr(|That−Tbar|≥eta)≤2 exp[−m eta²/(2(81+82eta/3))].
One may derive this from the conditional exponential-series bound for a centered variable of bounded magnitude; no independence across source calls is assumed. Hence
m≥220 eta^(−2) log[288(n−1)/delta]
suffices by union bound for all144(n−1) entries to have error≤eta with probability≥1−delta. Alternatively plain bounded-difference Hoeffding gives a looser explicit bound. The16×9 operator error is then≤12eta on every star edge.

Each observation is ONE full n-qubit source call, with n ordinary preparations and n ordinary measurements. Counters update only four input rows for one output column per edge, so bookkeeping is O(n) per shot and memory O(n) constant-size matrices. Source/bath reset is NOT required. Calibration of these physical product preparations/readouts is required and not learned from this calculation.

## Observed gap, rounding and abstention
Let e=12eta. Compute a unit smallest right-singular vector of Mhat=That−J. Under the structural promise, s1(Mhat)≤e. Let gL=min_star_edges[s2(Mhat)−e], where s1≤s2≤... are the nine singular values. If gL>0, Weyl's inequality certifies that each occupation-average Mbar has a one-dimensional kernel and its second singular value is≥gL, on the concentration event. This uses the already promised true kernel; it is not an empirical proof of the noise model.

The earlier residual argument applies to rectangular matrices: ||Mbar vhat||≤2e, giving distance≤2sqrt(2)e/gL from the normalized true vector up to sign. Reshape sqrt(3)vhat and round to the nearer of ±SO(3). If2sqrt(6)e/gL<1, the correct sign branch is separated and
||Chat−C||F≤4sqrt(6)e/gL.
Set the root frame to identity and use star-relative frames; the common unknown global frame is irrelevant to singlet encoding.

Use fresh geometrically growing epochs and confidence allocations delta_j summing to delta for an adaptive procedure. Each epoch's predictable occupation average still has the common kernel. Stop only when its observed gL and error ratio meet the desired frame target; otherwise continue to a declared budget and return inconclusive. A stable positive occupation gap eventually permits completion with sufficient data. Arbitrary dynamics can cancel excitation or stay near identity, so no universal termination or finite gap-free runtime is promised. An obvious residual failure s1>e may reject the structural model at the chosen confidence but small residual is not model certification.

## Transfer to the already derived memory service
If deployment ALSO satisfies the same full joint collective-algebra promise, the reviewed twirled frame-variance theorem applies to the rounded local frames. Its bound is halfdiamond≤24π² n e²/gL², uniformly in storage horizon for the specified retired-key logical service. Thus a numerical-gap lower bound g0>0 would yield O(n g0^(−2) epsilon^(−1) log(n/delta)) full-array acquisition calls, with larger conservative constants from the randomized estimator. An observed-gap stopping rule can use24π² n e²/gL²≤epsilon instead of a supplied g0. Compiler and control errors remain separate.

If the structural promise is false, no frame-correctness or uniform-memory conclusion follows. However the sequential model-free guard remains valid for ANY fixed candidate frame at its own source/control interface. These two logically separate guarantees are not conflated.

## Concrete nonunital example
`check_exact_nonunital_v1.py/.json` uses n=4, random unknown local frames and the Lindblad generator with jump V(Σ_i |0><1|_i)V†. The global channel is strongly nonunital: ||N(I)−I||F≈3.94759. Its rectangular pair defect has exactly one null direction and second singular value≈0.354780; the recovered relative frames match to≈1e−15. The omitted lower-degree coefficient rows have Frobenius norm≈0.623382, so their presence is not cosmetic. This is a finite-dimensional mathematical channel calculation, not reconstruction of the environment or a hardware experiment. Full Kraus commutation follows because the collective Lindblad generator and its dilation respect permutations; no random-unitary representation is asserted.
