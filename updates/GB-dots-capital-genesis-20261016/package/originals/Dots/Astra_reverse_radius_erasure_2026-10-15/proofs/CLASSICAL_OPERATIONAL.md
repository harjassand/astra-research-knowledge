# Exact complete binary-MMSE erasure threshold and signed observable compiler

Status: internally derived and independently reconstructed. Historical novelty has NOT been established. This is an operational theorem; it does not identify the fixed-reference-dimension SLD coefficient with the fixed-dimension RLD coefficient.

## Statement and conventions

Let T be an n-output, m-input classical channel, realized as measurement in a fixed classical input basis. Let E_q reveal that input with probability q and otherwise output one erasure symbol. Both channels leave an arbitrary finite-dimensional quantum reference untouched.

Let C(T) be the exact small-SDP value proved in CLASSICAL_THEOREM.md. Then the following are equivalent:

1. q >= C(T).
2. For every input encoding of a binary real label into joint input/reference states, the optimal quantum-measurement mean-square risk after E_q is no greater than after T.
3. The same holds for every real label ensemble with finite second moment.
4. For every faithful baseline and Hermitian tangent, E_q has no smaller SLD Fisher quadratic form than T, allowing arbitrary finite reference systems.

For positive nonconstant T, every q<C(T) has a faithful binary witness of reference dimension at most min(m,n). For arbitrary zero-entry channels, dimension m suffices. These are sufficient bounds, not minimal-memory assertions. They arise from the RLD vector frame dimension plus ONE coherent flag. We do not transfer the earlier fixed-r RLD formula to fixed-r SLD/MMSE.

The compiler below is a signed linear observable map. It is not a stochastic decoder, a channel simulation, a general decision-problem comparison, or a capacity statement.

## 1. The normalized radius and compiler

First assume T>0, C=C(T)<1. At an optimal free center u, the dual identity gives

    Σ_y u_y = 1−C,       w=u/(1−C) ∈ Δ_n.

Equivalently,

    min_{w∈Δ_n} max_i χ²(w||t_i) = C/(1−C),
    χ²(w||t_i)=Σ_y (w_y−T_yi)²/T_yi.

For 0<q<1 and q>=C define an n-by-(m+1) real matrix D by

    D(:,erase)=w,
    D(:,i)=[t_i−(1−q)w]/q.

Every column sums to one and DE_q=T exactly. Entries of the revealed columns may be negative; this is essential in some examples.

The per-input second-moment defect is

    M_i=diag(t_i)−D diag(E_q(:,i)) D^T
       =V_i−[(1−q)/q](t_i−w)(t_i−w)^T,
    V_i=diag(t_i)−t_i t_i^T.

Because v=t_i−w has zero sum and t_i>0,

    v^T V_i^+ v = Σ_y v_y²/T_yi = χ²(w||t_i).

The rank-one subtraction criterion therefore gives

    M_i>=0 iff χ²(w||t_i)<=q/(1−q).

All M_i are positive at q>=C. The q=1 endpoint is ordinary averaging on the revealed symbol; q=0 is possible only when T has identical columns and one averages on the erasure symbol. For zero-entry channels with C<1 the same proof applies on supports: w is supported on the common positive output rows, and the divergence is finite. If there are no common positive rows then C=1 and only q=1 suffices.

## 2. Reference-assisted observable lifting

Take ANY family of Hermitian target reference observables A_y, with no commutativity assumption. Upon observing source symbol a, measure

    B_a=Σ_y D_ya A_y.

The B_a are Hermitian. Their first-moment operator at each input i agrees exactly with that of the target family:

    Σ_a E_q(a|i)B_a=Σ_y T_yi A_y.

Their second-moment defect is

    Σ_y T_yi A_y²−Σ_a E_q(a|i) B_a²
       =Σ_yz M_i,yz A_y A_z >=0.

To see the last inequality, factor the real PSD matrix M_i as F_i^T F_i. The expression becomes Σ_k(Σ_y F_i,ky A_y)², a sum of squares of Hermitian operators. This is the step that makes the scalar covariance certificate valid with arbitrary quantum side information.

For any label x and any positive reference block ρ_{x,i}, the cross term in expected (estimate−x)² is preserved by the first-moment identity, while the estimate-square term decreases by the operator inequality. Summing over inputs and labels proves that this compiled estimator has no larger risk. An optimal target estimator therefore yields the complete MMSE comparison. The lift is independent of the state ensemble and of the reference dimension.

General POVMs offer no better quadratic-risk optimum than a Hermitian observable: if a POVM with reported values a has first moment A, its second moment satisfies Σ_a a²M_a>=A²; the spectral measurement of A has these first and second moments A,A². Thus the observable formulation covers unrestricted quantum measurement and estimation.

## 3. Exact MMSE–SLD dictionary

Define L_B(X)=(BX+XB)/2 and g_B(H)=Tr[H L_B^{-1}(H)] on faithful baselines. Completing the square gives

    g_B(H)=sup_{A=A*} {2Tr HA−Tr BA²}.

For a centered label ensemble, let B be its average output state and H its label-weighted average output state. The optimal mean-square risk is Var(label)−g_B(H). With classical output blocks, the g-values add over those blocks.

In particular, for the equiprobable binary pair ρ_±=B±tH with label ±1, the MMSE is exactly 1−t²g_B(H). This is an exact finite-state identity once both ρ_± are positive, not a local asymptotic expansion. It also establishes the SLD quadratic comparison from the binary MMSE comparison by taking sufficiently small t. The measured chi-square variational quantity uses this SLD metric, not the Petz/RLD trace metric; their equality of COMPLETE erasure thresholds requires the next construction.

## 4. Necessity: one coherent flag converts a vector RLD witness to SLD

Suppose q<C(T). The previous theorem supplies a faithful r-dimensional POVM R_i>0 and zero-sum vectors z_i such that

    N=Σ_y z_y* A_y^{-1} z_y > q E,
    E=Σ_i z_i*R_i^{-1}z_i,
    A_y=Σ_i T_yiR_i, z_y=Σ_iT_yi z_i.

Choose a_i>0 with Σa_i=1 and δ>0. On a reference of dimension r+1 set

    B_i(δ)=diag(R_i,δa_i),
    H_i=[[0,z_i],[z_i*,0]].

The tangents are Hermitian, traceless and sum to zero. A direct off-diagonal Lyapunov solution gives the EXACT formula

    g_{B_i(δ)}(H_i)=4 z_i*(R_i+δa_i I)^{-1}z_i.

For target output y replace R_i,z_i,a_i by A_y,z_y,b_y=Σ_iT_yi a_i. These expressions converge to 4E and 4N as δ→0. Hence for some finite positive δ the target SLD cost exceeds q times the input cost. The erased tangent is exactly zero, while homogeneity gives the revealed cost g_{qB_i}(qH_i)=qg_{B_i}(H_i). Therefore the erasure output has strictly smaller total SLD cost than the target.

All baseline blocks are faithful. Divide all B_i,H_i by r+δ to normalize the total trace. Choose t>0 small enough that B_i±tH_i>0 for every i. Explicitly the block Schur condition is

    t² z_i*R_i^{-1}z_i < δa_i,

so such a t always exists. The resulting equiprobable encoded binary states are faithful, and their reference marginals are IDENTICAL because ΣH_i=0. The exact MMSE dictionary now gives a strict operational reversal: MMSE(E_q)>MMSE(T).

For positive T, the frame theorem supplies r<=min(m,n)−1; adding the flag costs one, so min(m,n) reference dimensions suffice. For channels with zeros, r<=m−1 and m dimensions suffice. The construction is separable across the classical input/reference split. Its reference advantage comes from noncommuting conditional states, not input/reference entanglement.

## 5. Exact non-symmetric benchmark and faithful operational counterexample

For the cyclic 3-by-3 channel from CLASSICAL_THEOREM.md, C=2/11 and w=(1/3,1/3,1/3). At q=C the compiler is exactly

    D=[[5/4,−7/12,1/3,1/3],
       [1/3,5/4,−7/12,1/3],
       [−7/12,1/3,5/4,1/3]],

where the fourth column is erasure. DE_q=T, and each covariance defect is PSD of rank one. Its three diagonal entries are a permutation of (1/8,2/9,1/72); all its 2-by-2 and 3-by-3 principal minors are zero.

The exact script verify_operational.py also constructs a faithful reference-dimension-three binary witness at q=1/6<C, using frame regularization ε=1/1000, flag weight δ=1/1000, and binary tangent amplitude t=1/1000. It obtains

    target SLD / input SLD = 2012025024009/11096264288108
                          ≈0.1813245405631976 >1/6.

Every encoded state is proved positive by exact rational Schur complements. The exact positive risk difference is

    MMSE(E_q)−MMSE(T)
      =978813513513838/33372098093433565458243
      ≈2.9330295948831382·10^−8.

The small absolute gap is reported honestly; no claim of a large one-shot estimation advantage is implied by a large threshold separation. The verification runner prints the exact operational results.

## 6. Scope and established signed-lift prior art

The signed complete variance lift and its observable-estimation compiler are ALREADY an established framework. Zhu–Wang, *Quantum Incapacity beyond No-Cloning and PPT Mechanisms*, arXiv:2607.24693v2, Definition 3.3 introduces reference-complete variance-dominating signed lifts, Proposition 3.4 gives the CP-defect certificate, and Remark 3.8 explicitly interprets the lift as unbiased observable estimation with no larger variance, including a joint reference. Primary text: https://arxiv.org/html/2607.24693v2 . It also distinguishes this from simulating a POVM distribution.

Hirche, *Quantum estimation, channel orders, and private capacity*, arXiv:2610.03706v1, Definition 3.1 and Theorem 3.2 relate signed lifts and complete measured chi-square order. The general converse in Appendix A.1 concerns HERMITIAN-SMOOTHED measured order; ordinary complete measured order is a weaker node of its hierarchy. Proposition 2.1 gives the measured/SLD chi-square–binary-MMSE relation. Primary text: https://arxiv.org/html/2610.03706 . Its separately named quantum chi-square in Section 3.2 is BKM, not standard Petz/RLD.

Accordingly, Sections 1–2 above are the erasure specialization of an established framework, not an invented signed-lift theory or new operational interpretation. The explicit small radius yields its exact erasure threshold. The separate step proved in Section 4 is necessity for ORDINARY, UNSMOOTHED complete SLD/binary-MMSE order via a paid coherent flag; this does not follow automatically from the general smoothed-order equivalence. Neither checked source explicitly stated this erasure formula, but bounded searches do not establish historical novelty.

The compiler is an observable compiler, not a POVM-distribution simulator or arbitrary decision-problem dominance. Joint observables require access to the retained reference. No finite-memory equality between the RLD and SLD resource laws is asserted.
