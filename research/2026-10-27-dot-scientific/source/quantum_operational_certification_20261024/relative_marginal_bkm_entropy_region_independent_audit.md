# Independent receipt: relative-marginal BKM entropy region

27 October 2026. PASS for relative_marginal_bkm_entropy_region_theorem.md, with nonmutating exact scalar-certificate replay. This is the original-source relative band m EX<=X<=M EX, not entropy whitening or arbitrary two-state contraction.

The support reduction is exact: positivity and zero marginal on a reference subspace force X to vanish on the corresponding full physical product subspace. The WH output also vanishes there. On the retained finite support tau is faithful; m>0 makes both source/output paths faithful. The zero source is trivial. No lower spectral bound on tau uniform in dimension or conditioning is required.

E(D)=0 implies TrD=TrD log tau=0 since log tau belongs to the fixed marginal algebra. Exact second-order Taylor integration gives the two relative entropies with weight1-s and no missing factor of two. N fixes tau, preserves the marginal and trace, so Delta=D(X||tau)-2D(NX||tau) is the original deficit.

The noncommuting base-order argument is valid: for0<P<=Q, Q^T tensor Q-P^T tensor P=(Q^T-P^T) tensor Q+P^T tensor(Q-P)>=0. Applied to vec(K), this orders Tr K* P K P without falsely ordering P² against Q². Resolvent integration proves BKM antitonicity; substituting t=cu proves exact inverse scaling in the base. Thus the two changing-base costs in equation(5) have the stated, opposite directions. Positivity of N transmits the actual relative source inequalities to the output path.

At the product marginal, partial physical transpose is a linear Hilbert-Schmidt isometry commuting with left/right multiplication by the reference-only resolvent. Since E(D)=0, ND=-D^(Tphysical)/2 and hence Htau(ND)=Htau(D)/4 exactly. This is not asserted at a changing nonproduct base; those costs are separately controlled by order.

Integrating gives input>=I(M)H and output<=I(m)H/4. The subtraction coefficient I(M)-I(m)/2 is correct. For the contraction assertion, input>=I(M)H implies H<=input/I(M), so eliminating H indeed gives the required upper bound, not an inequality reversal. The positive metric makes equality force X=tau when the coefficient is strictly positive; no equality characterization is asserted at a zero coefficient.

Independently received the scalar antiderivative, continuous valueI(1)=1/2, half-to-two band coefficients and the rational atanh lower bound log2>842/1215. In that band the actual gap is at least(3log2-2)Htau(D), and the source-specific contraction coefficient is below1/2. Arbitrarily ill-conditioned reference examples constructed by congruence satisfy the relative order bounds and marginal identity, but congruence is not applied to entropy itself. Scope excludes unrestricted WH3 VALUE and arbitrary mutual-information/relative-entropy contraction claims.
