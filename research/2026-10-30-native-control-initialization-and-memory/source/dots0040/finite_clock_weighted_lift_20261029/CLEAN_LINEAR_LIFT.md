# Exact finite-rate CLEAN linear Poisson lift; robust-noise obstruction remains
2026-10-29. Candidate derivation for independent audit, not a completed physical noise theorem.

Work in the exact dressed independent-set clock range. Write d_h=-Delta_h V>=0, with Delta_h=Phi_h^*-I, and the actual joint generator
L*=i[H_clock,.]+kappa sum_j[a_j^* Phi_j^*(.) a_j - {n_j,.}/2].
The overlap graph must include FULL channel/read supports, not merely changed checks. Rates here are uniform for notation.

## 1. Positive clock-only Poisson solutions
Let T_t be the hard-core clock semigroup. Use the full-qubit high-reset coefficient contraction with lambda=kappa/2-C_D g>0, restricting afterwards to the independent-set range. Let omega be its unique invariant state and p_h=omega(n_h). Define
A_h^0=-kappa integral_0^infinity [T_t(n_h)-p_h I]dt.
Then L_clock^* A_h^0=kappa(n_h-p_h I). Coefficient contraction gives ||T_t(n_h)-p_hI||<=2exp(-lambda t), hence ||A_h^0||<=2kappa/lambda. Set
A_h=A_h^0+(2kappa/lambda)I.
Thus 0<=A_h<=M I, M=4kappa/lambda, uniformly in volume. The stationary local no-emission lower-progress theorem yields p_h>=p_min>0 uniformly: for any fixed T, c(D,g,kappa,T)<=P_omega(N_h(T)>=1)<=kappa p_h T.

These A_h are quasi-local, not strictly local. Weighted coefficient contraction gives spatial tails; their scalar shift is not small. Existence alone is sufficient for the clean calculation below.

## 2. A stronger disjoint-move animal inequality
For two disjoint full channel supports h,j, accepted choices and acceptance statuses do not change under the other channel. On a syndrome x where both are active, write u_h(A)=theta^{d_h(A)}-1 for the scalar relative animal increment (here d_h(A) is local removed-minus-added count, NOT the decrement observable).
Then Delta_j Delta_h V=sum_A f_A u_h(A)u_j(A).
A negative term has exactly one positive u. Complete the corresponding increasing flip, e.g. B=A union D_h. This is connected, makes u_h(B)<0, and leaves u_j unchanged because D_h and D_j are disjoint. The original one-move charging estimate, multiplied by |u_j(A)|=|u_j(B)|, applies unchanged. Each positive target can receive charges from both orientations. Strengthen the original per-move ratio requirement to
R_D>=2^{|D|+2}/(1-theta^{d_D}).
Each orientation then consumes at most one quarter of its positive target. Therefore
Delta_j Delta_h V>=0, equivalently Delta_j d_h<=0.
Inactive cases give zero. This is NOT vanishing of disjoint cross terms: the sign is favorable. It requires the full untruncated animal sum.

## 3. Local overlap estimate to check against concrete SSF footprints
For every adjacent pair j,h there is a uniform constant C_loc such that
Delta_j d_h<=C_loc d_j.
Here is the charging proof/interface. If j does nothing, the left side is zero. Otherwise all changed local decisions/animal factors lie in a bounded connected check patch K_jh containing D_j and every possible changed-check set at h before/after j. In the difference Delta_j d_h, untouched animal terms cancel. Any remaining source animal intersects K_jh. Complete it to B=A union K_jh. The size added is uniformly bounded, the weight ratio is bounded below by theta^{(1-c)|K_jh|} times a bounded correction for the flip j, and the number of preimages is <=2^{|K_jh|}. Each scalar difference factor has a fixed bound because the flip sizes are bounded. The completed B contains D_j, so the strict per-move decrement lower bound for d_j pays for it. This proves the displayed estimate with a geometric constant provided the SSF channel is deterministic syndrome update and its full local decision footprint is included in the overlap graph. For more general CPTP channels, this interface is NOT automatic.

## 4. Exact joint drift identity and absorption
Define
Vcorr=V+epsilon sum_h A_h tensor d_h.
Each summand is positive, so Vcorr>=V>0. No clock/data factorization of states is assumed. Exact product-generator algebra gives
L*Vcorr=-(1-epsilon)kappa sum_h n_h d_h
         -epsilon kappa sum_h p_h d_h
         +epsilon kappa sum_{j,h} (a_j^* A_h a_j) tensor Delta_j d_h.
The Hamiltonian acts only on clocks. The last term is the reset/data cross term; it must NOT be omitted.
For disjoint supports, it is nonpositive by section 2 and positivity of a_j^*A_h a_j. For overlapping supports, section 3 and a_j^*A_h a_j<=M n_j bound it by epsilon kappa C_loc M Dbar sum_j n_j d_j, where Dbar includes the diagonal h=j. The h=j case also admits the same bounded-patch argument.
Choose epsilon=[2(1+C_loc M Dbar)]^{-1}. Then
L*Vcorr<=-(kappa/2)sum_h n_h d_h-epsilon kappa p_min sum_h d_h.
Combining the actual weighted SSF coverage proves
L*Vcorr<=-epsilon kappa p_min (1-theta)/(2C1) W + b N.
This is an exact finite-rate operator drift on the clean dressed range and small-component data basin. It has no effective-Poisson approximation and no time-growing simulation error.

## 5. Why this does not close the generic physical-noise theorem
Uniformly, sum_h d_h is only O(W), not O(V). Thus Vcorr can behave like W. A local data perturbation changes each distant d_h involving the same large animal; summing over local perturbations may cost W2=sum_A |A|^2 f_A. The clean negative drift above controls W, not W2. A polynomial factor cannot be silently absorbed with an N-independent constant. Quasi-local clock tails introduce another obligation, but do not cure the basic extra animal-size factor.
The physical full-Hilbert extension is also absent: the positive d_h algebra and exact clock/data generator only hold in the clean dressed range; arbitrary perturbations exit it.
A multiplicative per-animal clock dressing, or a closed entire moment hierarchy, is needed to retain local orbit control without this loss. This note is genuine clean service progress, NOT a full robust controller lift.
