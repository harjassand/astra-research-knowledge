# Independent review of recurrence and closed reservoir noise

Reviewer: `recurrent_bath_purity`. Date: 21 October 2026.

## Disposition

The proposed Hilbert–Schmidt argument is correct in the maximally mixed reference model. Its finite spectral cutoffs propagate exactly under the unchanged physical unitary, for arbitrary external inputs and correlations. The resulting finite-dimensional description can be time dependent after identifying the moving reservoir subspaces.

A simpler and stronger route to the principal exclusion is also available: purification, finite-rank normal-state tails, and the Schmidt spectrum establish asymptotically perfect discrimination from every nonunitary IID channel for **any faithful finite-dimensional reference input**. No finite entropy, bounded energy, or return of an external purification is required. This stronger route is proved below.

These are independent internal mathematical checks. This review does not establish historical priority or external certification. No numerical campaign was run.

An additional requested check establishes a positive coding consequence in the maximally mixed recurrence model: there exist collective block codes with log dimension at least n log(d) - 8 sqrt(n) and full diamond recovery error tending to zero. The low-Kraus-rank code construction is inherited greedy/Tverberg machinery; the substantive application here is the normal-state spectral approximation under recurrence. See Sections 7–8.

## 1. Model and notation

Let S be a d-dimensional Hilbert space, E a separable Hilbert space, and U a fixed unitary on S tensor E. The initial reservoir state tau is a normal trace-class density operator. Every use acts with U on a fresh external input S and the same reservoir E. All degrees of freedom of the closed device that persist or absorb discarded information belong to E. In particular, there is no uncounted fresh ancillary environment or per-call discard.

For a fixed input density eta on S, define

    Phi_eta(X) = Tr_S[ U (eta tensor X) U* ],
    tau_n = Phi_eta^n(tau).

Trace-norm recurrence means that a sequence n_j tending to infinity satisfies ||tau_(n_j) - tau||_1 -> 0. The half-trace return distance is delta_n = ||tau_n - tau||_1 / 2.

The complete external process is distinguished from an ordinary output stream produced by unpurified reference inputs. The theorem below permits reference-entangled input tests and retains the full joint output/reference state.

## 2. The maximally mixed purity lemma

Write U = sum_(i,j) |i><j| tensor A_ij and K_ij = A_ij / sqrt(d). With eta = I/d,

    Phi(X) = sum_a K_a X K_a*,
    sum_a K_a* K_a = I,
    sum_a K_a K_a* = I.

Both identities follow from unitarity of U. There are d^2 Kraus operators, so every operator sum below is finite. Phi is trace preserving on trace-class operators and unital on bounded operators.

### Exact defect identity

For every Hilbert–Schmidt operator X, putting Y = Phi(X),

    sum_a ||K_a X - Y K_a||_2^2
      = ||X||_2^2 - ||Y||_2^2.                         (1)

Proof: the first squared term sums to Tr(X* X) by sum K_a* K_a = I. The second squared term sums to Tr(Y*Y) by sum K_a K_a* = I. The mixed inner product is

    sum_a Tr(X* K_a* Y K_a)
      = Tr( Phi(X*) Y ) = Tr(Y*Y).

All products under the trace are trace class, because each product contains two Hilbert–Schmidt factors and bounded Kraus factors. Thus cyclicity here is legitimate. Expanding the squared norms gives (1). This also proves Hilbert–Schmidt contraction directly.

### Recurrence saturates contraction at every step

Every density tau is Hilbert–Schmidt, regardless of its von Neumann entropy. The sequence ||tau_n||_2 is nonincreasing. Trace-norm recurrence implies Hilbert–Schmidt recurrence because ||Z||_2 <= ||Z||_1. A nonincreasing sequence that returns arbitrarily late to its initial value is constant. Hence

    ||tau_n||_2 = ||tau||_2 for all n.

Equation (1), applied to X = tau_n, yields

    K_a tau_n = tau_(n+1) K_a for every a,n.

Returning to the blocks of U gives

    U (I tensor tau_n) = (I tensor tau_(n+1)) U,

and therefore

    U (I tensor tau_n) U* = I tensor tau_(n+1).         (2)

No entropy difference or subtraction of infinite quantities occurs.

### Finite spectral cutoffs propagate exactly

For a positive threshold a, let P_n = 1_[a,infinity)(tau_n). These projections have finite rank because tau_n is compact. Functional calculus in (2) gives

    U (I tensor P_n) U* = I tensor P_(n+1).            (3)

Consequently, the ranks of P_n agree, and Tr(P_n tau_n) is independent of n. To obtain arbitrary small tails, choose thresholds tending to zero through gaps of the initial spectrum. If tau has finite rank, one threshold below its least positive eigenvalue suffices.

The word "spectral cutoff" here means a union of complete positive-eigenvalue eigenspaces. Arbitrarily cutting a degenerate eigenspace need not give (3).

Equation (3) maps S tensor P_n E onto S tensor P_(n+1) E. Tensoring it with any external reference identity shows that the same support statement holds for arbitrary correlated inputs, adaptive testers, and conditional branches of external measurements. It is not restricted to the reference input experiment.

For a fixed cutoff rank r, choose isometries V_n from C^r onto P_n E. Then

    W_n = (I tensor V_(n+1)*) U (I tensor V_n)

is a unitary on S tensor C^r. The W_n may depend on n. This gives a finite-memory representation for proof purposes, not a fixed finite-dimensional physical simulator.

### Consequence for a finite-rank initial truncation

Let epsilon = 1 - Tr(P_0 tau) and tau^P = P_0 tau P_0/(1-epsilon). Since P_0 commutes with tau,

    ||tau - tau^P||_1 = 2 epsilon.

The complete n-slot processes differ by at most 2 epsilon in full strategy distance, uniformly in n. With pure reference-entangled inputs in all slots, the external state from tau^P has rank at most r^2: its initial reservoir rank is at most r, its final reservoir dimension is r, and the joint evolution is unitary. This gives the usual fixed-rank spectral comparison against IID mixed output states.

### Scope warning

The maximally mixed assumption is necessary for this particular bistochastic proof. For eta non-maximally-mixed, let E=S, U=SWAP, tau=eta. The reservoir is stationary under Phi_eta, but U(I tensor tau)U* = tau tensor I, which generally differs from I tensor tau. Thus the intertwining conclusion cannot simply be asserted for a general faithful eta. The next proof avoids that invalid extension.

## 3. Stronger theorem for every faithful reference input

### Statement

Assume the closed unitary model above, with arbitrary normal tau and faithful eta. Suppose tau is trace-norm recurrent under Phi_eta. Let N be any channel on S that is not unitary. Let omega_n be the joint state of all n external outputs and their retained input references when each input is prepared as a fresh purification of eta. Put

    theta = (N tensor id)(|sqrt(eta)><sqrt(eta)|).

Then

    ||omega_n - theta^(tensor n)||_1 -> 2.             (4)

In particular, the complete process cannot equal the IID process N in every slot, and its full strategy distance from that IID process tends to its maximal value 2.

The argument also applies to a prescribed sequence of unitaries U_n on the same reservoir, provided the corresponding reference trajectory has the stated recurrence. No such extension is needed for the fixed-device claim.

### Purify the initial reservoir

Choose a purification |Psi>_(ER) of tau, with R inert throughout. This is a mathematical reference, not an additional return requirement. Its marginal tau_R remains fixed automatically because nothing acts on R.

The external inputs are prepared independently as purifications of eta. After n interactions the total state on external outputs, input references, E and R is pure. Write sigma_n for its ER marginal and omega_n for its external output/reference marginal. Their nonzero spectra coincide by the Schmidt decomposition.

The E marginal of sigma_n is exactly tau_n, and its R marginal is tau_R.

### Normal-state tails produce a finite joint projection

For any epsilon > 0, choose a rank-r spectral projection P on E containing all but epsilon of the probability of tau, and the matching rank-r projection Q on the Schmidt reference R. Thus

    Tr(P tau) >= 1-epsilon,
    Tr(Q tau_R) >= 1-epsilon.

At arbitrary n,

    Tr[(P tensor Q) sigma_n]
      >= Tr(P tau_n) + Tr(Q tau_R) - 1
      >= 1 - 2 epsilon - delta_n.                     (5)

The first inequality is the commuting-projection union bound. The second uses the effect-probability inequality

    |Tr P(tau_n-tau)| <= ||tau_n-tau||_1/2.

This is where full versus half trace norm enters. The joint ER state is not assumed to return, to decouple, or to preserve its correlations with R.

### Compare the Schmidt spectra

The projection P tensor Q has rank r^2. By the Ky Fan variational principle, (5) implies that the sum of the largest r^2 eigenvalues of sigma_n is at least 1 - 2 epsilon - delta_n. The same is true of omega_n because their nonzero spectra agree.

Let Pi_n project onto the largest min(r^2,dim omega_n) eigenspaces of omega_n, using any rank-r^2 maximizing projection when the dimension allows. Then

    Tr(Pi_n omega_n) >= 1 - 2 epsilon - delta_n.

Faithfulness of eta makes theta an invertibly filtered normalized Choi state. Its rank equals the Kraus rank of N. A channel between equal d-dimensional spaces has Choi rank one exactly when it is unitary. Thus theta is mixed and lambda = ||theta||_infinity < 1.

It follows that

    Tr(Pi_n theta^(tensor n)) <= r^2 lambda^n,

and binary testing gives

    ||omega_n - theta^(tensor n)||_1
      >= 2 [1 - 2 epsilon - delta_n - r^2 lambda^n]_+. (6)

If r^2 exceeds the external dimension for a small n, the same bound remains valid; it may simply be nonpositive before the positive-part operation.

Along recurrence times n_j, delta_(n_j) -> 0 and lambda^(n_j) -> 0. For each fixed epsilon, (6) gives limiting distance at least 2(1-2 epsilon). Letting epsilon decrease to zero gives distance tending to 2 along the recurrence subsequence.

Finally, the family omega_n is prefix consistent. Future interactions on the reservoir and new inputs cannot change the marginal of previously emitted outputs and retained input references. The ideal tensor-power family is also prefix consistent. Contractivity under deleting the last slot makes the distance in (4) nondecreasing in n. A nondecreasing bounded sequence with a subsequence tending to 2 tends to 2. This proves (4).

### What the proof establishes operationally

The finite-rank spectral projector Pi_n supplies an existential distinguishing measurement on the collected output/reference record. It is not asserted to be efficiently computable or experimentally convenient. No exponential discrimination rate uniform in tau, no effective recurrence time, and no finite spectral-tail bound have been established for an arbitrary normal infinite-dimensional reservoir.

Only one admissible nonadaptive purified-input experiment is needed for the lower bound. Therefore the conclusion automatically applies to the stronger distance obtained by optimizing over complete causal testers.

## 4. Exact IID noise forces reservoir mass to escape

There is a complementary theorem needing no recurrence hypothesis.

Suppose the complete closed-device process is exactly IID N for every horizon, with N nonunitary and eta faithful. Then omega_n = theta^(tensor n). By purity of the total state, sigma_n has largest eigenvalue lambda^n, where lambda < 1 as above.

Choose a rank-r Q on R with Tr(Q tau_R) >= 1-epsilon. For any rank-m projection P on E,

    Tr(P tau_n)
      <= Tr[(P tensor Q) sigma_n] + epsilon
      <= m r lambda^n + epsilon.                     (7)

Taking rank-one P and the supremum gives

    ||tau_n||_infinity <= r lambda^n + epsilon.

Since epsilon is arbitrary and its required r is fixed before n tends to infinity,

    ||tau_n||_infinity -> 0,
    Tr(tau_n^2) -> 0.

For every fixed normal density sigma on E, choose a finite-rank P capturing all but epsilon of sigma. Equation (7), or the operator-norm conclusion, gives Tr(P tau_n) -> 0. Therefore

    ||tau_n - sigma||_1 -> 2.                         (8)

Exact indefinitely repeated memoryless nonunitary noise thus forces maximal eventual separation from every fixed normal reservoir state under the faithful reference experiment. This rules out recurrence and gives a stronger statement than a dimension-only finite-bath obstruction.

## 5. Necessary scope distinctions and exact examples

### Ordinary stationary output statistics are insufficient

Let E=S be finite dimensional, U=SWAP, and tau=eta faithful. For unpurified independent input states eta, the output stream is exactly eta^(tensor n), and the reservoir remains eta. This might look like IID replacement noise if only those output statistics were examined.

The complete process is instead a one-slot delay: the first output is the initial reservoir state, and each later output is the previous input. Retained input references reveal that distinction. Hence replacing complete-process equality by equality of the ordinary stationary output stream would make the exclusion false.

### A nonfaithful reference can make an IID reset reservoir stationary

Let E be the incomplete bilateral infinite tensor product of qubits with vacuum |0> at each site. Equivalently, E has an orthonormal basis indexed by finite subsets of the integers, recording finitely many excitations. This is a separable Hilbert space. Its all-zero vacuum |Omega> is a normal pure state.

Let U first SWAP S with site 0 and then shift all reservoir sites one place to the right. The shift and the SWAP are genuine unitaries on this fixed space. On the vacuum initial state, every use outputs |0>, while the incoming input is stored at the next positive site. Thus the full external process is exactly the IID reset channel for all inputs and every finite horizon. Every reservoir site was present initially; no new ancillary system is added after initialization.

For the pure reference eta=|0><0|, the reservoir remains the vacuum, so it is exactly stationary. Faithfulness is therefore necessary to infer mixed theta from a nonunitary channel.

For eta=diag(1-p,p) with 0<p<1, the reservoir after n uses stores the independent input mixture on n sites. Its vacuum probability is (1-p)^n and

    ||tau_n - |Omega><Omega|||_1
       = 2[1-(1-p)^n] -> 2.

This is an exact example of the mass-escape alternative under a faithful reference.

### Normality and closed-unitary accounting are substantive

The finite-rank tails in (5) and (7) use normal trace-class initial states. No conclusion here is asserted for singular states or a different non-type-I algebraic reservoir model.

The proof also requires a closed unitary dilation on the counted reservoir. An uncounted fresh environment or a per-call irreversible discard can supply ordinary IID noise with a stationary retained register. Such a model is outside the theorem.

### No entropy-return or purification-return assumption

The initial reservoir may have infinite von Neumann entropy. All estimates use finite-rank probability mass, Hilbert–Schmidt norms, or finite-dimensional eigenvalue bounds. R is inert only as a mathematical purification device; its joint state with E may change arbitrarily. Returning an external purification is not part of the contract.

## 6. Recommended integration

Use Section 3 as the main general theorem and Section 4 as its complementary mass-escape statement. The original Hilbert–Schmidt lemma remains a valid stronger structural refinement for maximally mixed inputs, giving uniformly propagating finite spectral cutoffs and a finite-rank process approximation at every horizon.

Keep the operational limits explicit: complete-process distinguishability, normal type-I reservoir, faithful input reference, and closed unitary accounting. Do not infer a useful finite-horizon rate without a known spectral tail and a return schedule. Do not identify the result with R1's entanglement expenditure law; this argument uses no relative entropy of entanglement, Bell stock, LOCC assumption, or logarithmic resource expansion.

## 7. Checked low-Kraus-rank exact coding lemma

### Statement and inherited mechanism

Let M be a channel from a D-dimensional input to a D-dimensional output, with a Kraus representation A_1,...,A_k. Let

    S = span_C { A_i* A_j : 1 <= i,j <= k }.

This is a self-adjoint complex operator space containing I. Let m be its complex dimension, equivalently the real dimension of its Hermitian part. Then 1 <= m <= k^2, and M has an exactly correctable subspace of dimension at least

    q = ceil(D/m^2) >= ceil(D/k^4).                   (9)

The proof is the greedy diagonalization plus convex partition method already present in Knill, Laflamme and Viola, *Theory of Quantum Error Correction for General Noise*, Theorems 3–4, arXiv:quant-ph/9908066, subsequently Phys. Rev. Lett. 84, 2525 (2000). The displayed bound uses the affine dimension m-1 after removing the constant identity expectation. This straightforward refinement is not a claimed new coding mechanism or historical-priority result.

The sole nontrivial convex-geometric input is the affine Tverberg theorem: any (q-1)(p+1)+1 indexed points in R^p can be partitioned into q nonempty sets whose convex hulls have a common point. There is no prime-power restriction for this affine theorem. The p=0 case is immediate. Coincident points are permitted, by the usual indexed formulation or by a perturbation/compactness argument.

### Step 1: an H-diagonal family

Choose a Hermitian basis H_1=I,H_2,...,H_m of S. There are at most k^2 independent Hermitian generators: the k diagonal A_i*A_i, together with the Hermitian real and imaginary parts of each off-diagonal pair A_i*A_j. This proves m <= k^2 without confusing real and complex dimensions.

Construct unit vectors v_1,...,v_N, where N=ceil(D/m), satisfying

    <v_a,H_j v_b> = 0  whenever a != b, for every j.  (10)

Start with any unit vector. If t vectors have been selected, exclude the complex span of {H_j v_a: j=1,...,m; a=1,...,t}. Its dimension is at most tm. Therefore another unit vector exists whenever tm<D. Hermiticity supplies both orientations of (10), and H_1=I gives ordinary orthogonality. Since (N-1)m<D, the induction reaches N vectors.

### Step 2: convex partition removes diagonal dependence

For each a define

    x_a = (<v_a,H_2 v_a>,...,<v_a,H_m v_a>) in R^(m-1).

Put q=ceil(N/m). Then (q-1)m+1 <= N, so Tverberg gives disjoint nonempty groups G_1,...,G_q and nonnegative weights p_(g,a) summing to one in each group, such that

    sum_(a in G_g) p_(g,a) x_a = x

is independent of g. If Tverberg is applied to only the required number of points, the unused points are simply discarded. Define

    w_g = sum_(a in G_g) sqrt(p_(g,a)) v_a.

The w_g are orthonormal because the groups are disjoint. Equation (10) kills all cross terms, both within the weighted diagonal expectation and between different groups. Thus

    <w_g,H_j w_h> = c_j delta_(g,h)

with c_j independent of g. If V is the isometry with columns w_g, then

    V* A_i* A_j V = alpha_(i,j) I_q.                 (11)

These are the exact Knill–Laflamme conditions. The integer identity

    ceil(ceil(D/m)/m) = ceil(D/m^2)

finishes the dimension count. One way to verify it is that an integer b satisfies bm >= ceil(D/m) exactly when bm^2 >= D.

### Step 3: exact recovery, explicitly

The matrix alpha in (11) is positive semidefinite and has trace one. Change Kraus representation by a unitary mixing that diagonalizes alpha, obtaining F_l with

    V* F_l* F_h V = p_l delta_(l,h) I_q,
    p_l >= 0, sum_l p_l = 1.

For p_l>0, W_l=F_l V/sqrt(p_l) is an isometry. The ranges of the W_l are pairwise orthogonal. Let Pi=sum_(p_l>0) W_l W_l*. For any fixed logical density omega_0, the map

    R(X) = sum_(p_l>0) W_l* X W_l
           + Tr[(I-Pi)X] omega_0

is completely positive and trace preserving. Direct substitution gives

    R o M o Enc = id_q,
    Enc(rho) = V rho V*.

This is exact channel recovery, including inputs entangled with an arbitrary reference. It is not merely a statement about average fidelity.

### Primary-source check

The KLV manuscript was opened and its Theorems 3–4 and proof inspected. The greedy exclusion and square-root convex weights above are the same mechanism. KLV retains an ambient real dimension m rather than the affine m-1 used here; its published-style bound is already enough for the asymptotic application.

The affine Tverberg statement was checked in the author's own later proof, H. Tverberg, *A generalization of Radon's theorem II*, Bulletin of the Australian Mathematical Society 24 (1981), 321–325. Its point count q(p+1)-p is the same as (q-1)(p+1)+1. The original paper is H. Tverberg, *A Generalization of Radon's Theorem*, Journal of the London Mathematical Society s1-41 (1966), 123–128.

Primary links:

- KLV original manuscript and Theorems 3–4: https://arxiv.org/pdf/quant-ph/9908066
- KLV publication: https://doi.org/10.1103/PhysRevLett.84.2525
- Original Knill–Laflamme criterion: https://doi.org/10.1103/PhysRevA.55.900
- Tverberg's original paper: https://doi.org/10.1112/jlms/s1-41.1.123
- Tverberg's own second proof: https://doi.org/10.1017/S0004972700004858

## 8. Recurrence yields asymptotically full-rate block recovery

This section requires recurrence specifically under the maximally mixed reference input I/d, so that the exact spectral propagation of Section 2 holds. It is not asserted under general faithful-input recurrence alone.

Let Lambda_n be the actual n-use channel from S^n to the n collected outputs, with the reservoir initialized once in tau. For sufficiently large n, set

    a_n = exp(-sqrt(n)),
    P_0^(n) = 1_[a_n,infinity)(tau),
    r_n = rank(P_0^(n)),
    epsilon_n = 1 - Tr(P_0^(n) tau).

The cutoff includes complete eigenspaces. Its rank obeys

    1 <= r_n <= exp(sqrt(n)),

because every retained eigenvalue is at least a_n and the total trace is one. Normality and a_n decreasing to zero imply epsilon_n -> 0, with no entropy or rate assumption.

Normalize tau within P_0^(n), and denote the resulting n-use channel by Lambda_n^P. Section 2 shows that the bath stays inside moving rank-r_n subspaces at every intermediate time for every input, including inputs entangled across uses and with a reference. After choosing coordinates on these subspaces, the whole block is a unitary on C^(d^n) tensor C^(r_n), with an initial bath density of rank at most r_n and a final bath of dimension r_n.

Diagonalizing that initial bath state and then tracing its final basis gives at most

    k_n <= r_n^2

Kraus operators for Lambda_n^P. More explicitly, if the initial bath eigenvalues are s_b, the block unitary is W, and a is a final bath basis index, the Kraus operators are sqrt(s_b) <a|W|b>. No step resets or replenishes the bath. The W used in this proof is a block representation of the unchanged physical interaction; its time-dependent moving-subspace coordinates do not constitute a changed physical device.

Applying Section 7 with D=d^n gives an encoding Enc_n and a collective recovery R_n, acting only on the external block, such that

    R_n o Lambda_n^P o Enc_n = id_(q_n),
    q_n >= ceil(d^n / r_n^8),
    log(q_n) >= n log(d) - 8 sqrt(n).                (12)

All logarithms here are natural. The true and truncated initial bath states have full trace distance 2 epsilon_n. Their block channels therefore satisfy

    ||Lambda_n - Lambda_n^P||_diamond <= 2 epsilon_n.

This follows by applying the same unitary channel to the initial-state difference tensored with an arbitrary reference-entangled input, then using trace-norm contractivity. It does not accumulate a factor n. Composition with encoding and recovery gives

    ||R_n o Lambda_n o Enc_n - id_(q_n)||_diamond
        <= 2 epsilon_n -> 0.                        (13)

Thus full diamond recovery error is at most 2 epsilon_n; half-diamond error is at most epsilon_n. Equations (12)–(13) yield unassisted collective block transmission at asymptotic rate log(d) per use, the full input-dimension rate. If desired, restrict each q_n-dimensional code to its largest power-of-two subspace, losing less than one logical qubit.

### Scope and honest resource boundary

- This is an existence theorem for globally encoded input blocks and a collective decoder after collecting the output block. It does not supply a finite-depth, local, streaming, efficient, or uniformly computable encoder/decoder.
- The codes may depend on n, U and the spectral data of tau. They do not require access to the bath during transmission, communication of bath outcomes, per-use bath reset, or external preshared entanglement.
- The displayed rate overhead 8 sqrt(n) is explicit. The error tail epsilon_n has no uniform rate over all normal tau. Actual block length at a specified error target therefore depends on the reservoir's spectrum. No useful finite resource claim follows without those data.
- The maximally mixed recurrence hypothesis is essential to this proof's input-independent propagation of spectral subspaces. The faithful-reference no-IID theorem in Section 3 is more general, but its purification argument alone does not justify the coding conclusion.
- Normality of the initial bath alone does not control the block Kraus rank: the final bath support can grow with n, as the exact reset construction shows. Exact spectral propagation is the load-bearing additional fact.
- Fixed nonzero return error is not recurrence and has not been substituted for the limiting hypothesis.
- The finite-dimensional coding step is inherited from KLV/Tverberg. A minor denominator sharpening is not the scientific bottleneck or a reason to claim a new coding theorem. The significant extension under examination is the passage from recurrent normal, potentially infinite-entropy reservoir states to uniform finite-spectral process approximants and hence the block-recovery statement.
