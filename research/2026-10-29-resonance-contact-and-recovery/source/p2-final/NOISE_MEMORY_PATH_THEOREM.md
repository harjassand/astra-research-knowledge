# Gaussian measurement noise and causal quantum memory

Author: `producer-workspace/measurement_frontier`, 29 October 2026 Australia/Brisbane.

Status: constructed theorem and exact special cases; independent review pending. This extends the accepted passive receiver compiler, whose proofs and reviews in `p2_mediator/` remain unchanged. It is a measurement-synthesis result under a specified receiver contract. Historical priority is not established.

## 1. The operation and receiver contract

Finite bosonic batches arrive in a fixed order, with one-particle feature columns `f_(i,t)` for `i=1,...,n`. Use the accepted convention

    Phi(f)=Re(f)^T Q+Im(f)^T P, [Q_j,P_k]=2i delta_jk,
    W(f)=exp(i Phi(f)), Omega_t=Im Gram(f_t).

The desired reported Gaussian POVM has operator characteristic function

    Mhat(u)=W(direct_sum_t sum_i u_i f_(i,t)) exp(-u^T N u/2),       (1)

for every real u. The real symmetric matrix N is the added measurement covariance. The input field may be any normal state and may be correlated with an arbitrary reference. No Gaussian input assumption is made. If `sum_t Omega_t=0`, (1) is the sharp joint quadrature measurement convolved with classical Gaussian noise N. For nonzero total commutator, (1) is an approximate joint Gaussian observable; it must satisfy the usual global Gaussian-observable positivity condition.

Receivers use deterministic calibrated passive interferometers, fresh independent vacuum ancillary modes, destructive homodyne, classical storage and fixed linear processing of outcomes. Classical affine displacements can be removed into the recorded frame and do not change the result. There is no outcome-dependent choice of interferometer or measurement axis in the necessity claim. Every quantum mode or delay line crossing the cut after batch t counts toward q_t. Preshared entangled ancillas and non-Gaussian operations are not free resources in this contract. Ancillas introduced before the first input may be deferred to batch 1, and their surviving modes then count normally.

The reported n-vector can be a linear coarsening of a larger raw homodyne record. The theorem preserves the complete reference assemblage for that **reported** POVM; it does not identify the raw refinement with the smaller record, or assert a source-erasure identity for a noisy POVM. The compiler saves the raw record and its linear reporting map, so any later full-record claim can use the actual refinement.

## 2. Exact feasibility theorem

Let S_0=S_T=0 be real skew matrices, and for t=1,...,T define

    Gamma_t = S_t-S_(t-1)-Omega_t.                               (2)

**Theorem.** The Gaussian POVM (1) is realizable by the stated receiver class with at most q_t retained canonical modes after each batch if and only if there are real symmetric matrices N_t such that

    rank(S_t) <= 2 q_t,
    N_t+i Gamma_t >= 0,
    sum_t N_t = N.                                               (3)

The semidefinite inequality is Hermitian. In particular N_t is positive semidefinite on real vectors. Extra independent classical Gaussian output noise can be included in any N_t as a real positive matrix, so an equivalent formulation permits `sum N_t <= N` in the real positive-semidefinite order.

For a supplied feasible path the construction uses `rank(N_t+i Gamma_t)` fresh vacuum modes at batch t, followed by the accepted passive compression lemma. It retains exactly `rank(S_t)/2` modes after that batch. A sufficient live width is

    rank(S_(t-1))/2 + m_t + rank(N_t+i Gamma_t).                   (4)

The bound counts fresh detector resources as well as input capture. It does not bound photon number, total storage time, precision or apparatus bandwidth.

### Sufficiency

Factor the positive matrix `H_t=N_t+i Gamma_t` as a complex Gram matrix of ancillary feature columns g_(i,t), using `rank(H_t)` independent vacuum modes. Define enlarged features

    h_(i,t)=f_(i,t) direct_sum g_(i,t).

Their prefix imaginary Gram is

    sum_(s<=t) Im Gram(h_s)
      = sum_(s<=t)(Omega_s+Gamma_s)=S_t.

Their global imaginary Gram vanishes. The accepted passive compiler therefore measures a commuting refinement of all `Phi(direct_sum_t h_(i,t))`, with the stated retained count and physical chronology. Its classical linear reporting map gives their joint values.

The ancillary modes start in a product of independent vacua, so tracing them from the operator characteristic function gives

    W(Fu) product_t <0|W(g_t u)|0>
       = W(Fu) exp[-sum_t ||g_t u||^2/2]
       = W(Fu) exp[-u^T(sum_t N_t)u/2].                           (5)

This is exactly (1). The characteristic-function identity determines the POVM and, by normal linearity, the full reference assemblage for its reported record. The original field need not have finite energy. Ancillary g are coefficients in a detector measurement; this construction does **not** apply controlled source displacements to the ancillas.

All ancilla preparation is causal: the modes realizing H_t enter at batch t, and every one that survives this stage is included in S_t's physical retained modes. No uncounted future entangled resource is introduced.

### Necessity

A fixed passive network with destructive homodyne and linear reporting can be represented by a common linear-optical dilation and commuting real linear observables Y_i on the original field and every independent vacuum ancilla. Deferred-measurement notation is an operator description; it does not grant extra physical storage. Early measured modes are never acted on again.

The reported characteristic function on arbitrary original input states determines its original-field Weyl coefficients uniquely. They must be F=(f_1,...,f_T) from (1). Partition the final observables' ancillary coefficients by the batch in which the corresponding fresh vacuum modes were introduced; denote them g_t. Their Gram matrices are

    H_t=Gram(g_t)=N_t+i Gamma_t >=0.

Independence of the vacuum modes gives `sum_t N_t=N` exactly by the Gaussian factor in (1). Final commutativity gives `sum_t(Omega_t+Gamma_t)=0`.

At cut t, the part of each final Y_i supported on already arrived original inputs and ancillas can be reconstructed from past commuting records and the retained register's quadratures. Future input or fresh ancillary variables have no coefficient in that past support. Thus, for some real matrices,

    Y_(past,t)=B_t y_(past)+L_t R_(memory,t).

Past records commute with one another and with the surviving memory. Taking commutators yields

    S_t=sum_(s<=t)(Omega_s+Gamma_s)=L_t J_(q_t) L_t^T,

and hence `rank(S_t)<=2q_t`. This is a consequence of the receiver's linear measured-observable representation, not an assumed reconstruction premise for arbitrary non-Gaussian or adaptive receivers. It proves (2)-(3).

## 3. The sharp noise cost for a prescribed path

Let W be a positive-definite real weight matrix on the reported observables. For a fixed S path, (3) separates by batch. Its exact minimum is

    min Tr(W N) = sum_t Tr |i W^(1/2) Gamma_t W^(1/2)|.          (6)

It is attained by

    N_t = W^(-1/2) |i W^(1/2) Gamma_t W^(1/2)| W^(-1/2).         (7)

Proof: put A=W^(1/2)Gamma_t W^(1/2), a real skew matrix, and transform N similarly. An orthogonal change of coordinates gives 2x2 skew blocks gamma_j J and a zero radical. Positivity of each principal block `N'+i gamma_j J` implies that the sum of its two diagonal entries is at least `2|gamma_j|`; radical diagonal entries are nonnegative. Summing gives `Tr N'>=Tr|iA|`. The proposed `N'=|iA|` attains the bound because `|iA|+iA` is positive semidefinite. Each nonzero skew block needs only one vacuum ancilla at this optimum.

Consequently the memory-constrained optimization is a rank-constrained path problem:

    inf_(S_0=S_T=0, rank S_t<=2q_t)
      sum_t ||i W^(1/2)(S_t-S_(t-1)-Omega_t)W^(1/2)||_1.          (8)

This is an exact characterization and constructive compilation rule, not a claim that global rank-constrained optimization is computationally easy. For `C_t=S_t-K_t`, where `K_t=sum_(s<=t)Omega_s`, the objective is the weighted total variation of C_t. This identifies the temporal cost that a per-cut singular-value threshold misses.

With zero retained memory, S_t=0 and (6) reduces to the exact cost `sum_t Tr|i W^(1/2)Omega_t W^(1/2)|`. With unconstrained memory and globally isotropic target, S_t=K_t gives zero added noise and recovers the accepted exact theorem.

## 4. Exact two-batch tradeoff

For two batches with Omega_1=K and Omega_2=-K, only one intermediate matrix S is free. Put `A=W^(1/2)K W^(1/2)` and let its positive skew singular values be `kappa_1>=...>=kappa_r>0`, one per 2x2 block. Then

    minimum Tr(WN) with q stored modes = 4 sum_(j>q) kappa_j.    (9)

Indeed the objective is `2||i W^(1/2)(K-S)W^(1/2)||_1`. Rank is invariant under the invertible congruence. The singular-value tail lower bound for any rank-2q approximation gives `4 sum_(j>q)kappa_j`; keeping the q largest skew blocks attains it and remains real skew. This is a complete optimum within the declared receiver/noise objective. It is not an optimum channel-error theorem or an unrestricted quantum-memory lower bound.

For completeness, the trace-norm tail bound follows from singular-value interlacing under a rank-k perturbation: `s_(j+k)(A)<=s_j(A-B)` when `rank B<=k`. The min-max characterization of singular values proves this by restricting the minimizing subspace to the kernel of B, costing at most k dimensions. Summing over j gives `sum_(j>k)s_j(A)<=||A-B||_1`. Here each positive kappa occurs twice and k=2q.

The result is continuous as a small noncommuting feature vanishes, even though the exact zero-noise mode requirement jumps. A small covariance is an estimation-noise statement. It alone is not uniform total variation distance from a sharp measurement on unrestricted field inputs.

## 5. Multiple cuts: greedy spectral truncation fails

Let J1 and J2 be disjoint 2x2 skew blocks, W=I, and three arrival batches have prefixes

    K1=(3/2)J1+J2, K2=J1+(3/2)J2, K3=0.

Allow one retained mode. Keeping each cut's largest block chooses

    S1=(3/2)J1, S2=(3/2)J2, S3=0.

Its Gamma blocks are `(0,-1)`, `(-1,1)`, `(1,0)`, and its optimal trace noise is `2+4+2=8`.

Keeping the same plane instead chooses

    S1=(3/2)J1, S2=J1, S3=0.

Its Gamma blocks are `(0,-1)`, `(0,-1/2)`, `(0,3/2)`, with trace noise `2+1+3=6`. Both paths have the same allowed retained mode count. The second is strictly better. No claim that 6 is the global optimum is needed or made. This exact example rules out independent per-cut best-rank truncation as a general noise-optimal design rule.

`noise_memory_checks.py` checks the rational path identities, the two-batch formula's constructed values, and actual passive receiver synthesis for both paths. The Gram/path costs are exact rational results. The saved full passive matrices and reconstruction residuals are floating diagnostics; their numerical accuracy is not a physical noise certificate.

The actual objective matters even after a feasible path is chosen. In the example, the fixed-plane covariance is `diag(0,0,3,3)`, while the greedy covariance is `2 I_4`. Apply the same real orthogonal Hadamard matrix H/2 to all source-coordinate features, where H has rows `(1,1,1,1)`, `(1,-1,1,-1)`, `(1,1,-1,-1)`, `(1,-1,-1,1)`. The trace costs remain 6 and 8. But the sign-alphabet quantity `max_(z_i=+-1) z^T N z` becomes 12 for the fixed-plane design and remains 8 for the greedy design. A sign vector maps entirely into the two noisy directions and attains 12. This is an exact reversal between a covariance-trace objective and root's complete-erasure **sufficient-bound** objective; it is not a lower bound on actual corrected-channel error. Rotating feature coordinates defines another supplied source-coupling family and is not asserted to be a free physical change of qubit basis.

## 6. Scope and connection to erasure

The new operation is a causal Gaussian measurement with a certified noise covariance and quantum-storage schedule. Fresh detector vacuum and refined/coarsened classical records replace some coherent retention. The no-noise endpoint is the accepted exact receiver. Ordinary simultaneous-quadrature measurement and Gaussian Naimark ancillas are established constituents; the proposed new bridge is their compatible causal noise/memory path and exact receiver synthesis.

Root has proposed a separate complete-record erasure lift using this receiver. Its comparison family applies hypothetical controlled Weyl displacements also to the independent detector ancillas; the actual hardware does not. The enlarged features are exactly erased by the same physical receiver. Because original and ancillary sectors are orthogonal, no comparison Weyl phase appears. The vacuum overlap can then bound the full corrected actual-record instrument uniformly over arbitrary original field states. That is root's construction, not an independently authored part of this theorem; it requires its own statement and review. Equation (6) must not be promoted to optimality of that complete-channel error bound.

Actual operation additionally needs calibrated feature acquisition, available collection/capture, passive control delivery, independent vacuum supplies and detector performance. A passive interferometer does not amplify total photon number, but may concentrate energy into its retained mode. Storage loss, duration, source coherence, missed ports and fresh-ancilla supply costs remain distinct. No previous bath certificate transfers automatically.

## 7. Primary ancestry and source boundary

Holevo, *The structure of general quantum Gaussian observable*, arXiv:2007.02340, Section 2 (especially the Gaussian characteristic function and positivity inequality) and Theorem 1, supplies the standard noise cone and Naimark-extension ancestry. This theorem uses those established ingredients with a causal resource constraint; it does not claim to invent them.

Guo, Mueller and Liu, *Memory-Optimal Sequential Synthesis of Multimode Gaussian Transformations*, arXiv:2609.05250, concerns a prescribed full symplectic transformation, fixed output-emission order and flexible input injection. The present objective allows destructive measurements and linear reported statistics, with fixed input arrival and explicit added-noise allocation. Its full-transformation memory theorem is a close conventional starting point, not a theorem about this noise-constrained POVM objective.

Astra N939's current capsule still preserves its source-specific cross-response correction, adverse matched comparison and unacquired native-output interface. No N939 physical performance number is imported into this construction. The local accepted receiver proofs and their actual reviews are the mathematical dependency. Broader Astra search returned no clearly applicable new premise; candidate absence is not an impossibility or priority result. Acquisition details are saved separately.
