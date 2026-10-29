# Response-relative centrality: a normalization and a real obstruction
2026-10-29. New working derivation, not independently received. No approximate decoder theorem yet.

Let N be a qubit-input CPTP channel, Delta_a=N(sigma_a), K=sum Delta_a^2, and work on P=supp K. All inverses below are only mathematical support inverses: no source inverse, spectral gap, or executable normalization oracle is supplied.

## 1. Why absolute approximate centrality is inadequate
For N_r(rho)=N(rho) tensor I_r/r, the optimal recovery entanglement fidelity is exactly unchanged: discarding junk gives one direction, and any decoder on the enlarged output induces a decoder for N by attaching I_r/r. The response tuple, Gram operators and centrality commutators scale as
 Delta_a^(r)=Delta_a tensor I_r/r,
 B_ab^(r)=B_ab tensor I_r/r^2,
 [B_ab^(r),Delta_c^(r)]=[B_ab,Delta_c] tensor I_r/r^3.
Thus any fixed noncentral channel has arbitrarily small absolute operator-norm centrality defect after harmless junk dilution. This is not a no-go for a rank-paid theorem or a relative metric, nor a proof that the channel is far from every central approximation in every norm. It invalidates using a tiny raw defect alone as evidence of a simpler recovery task independent of junk rank.

## 2. Intrinsic bounded tuple
Put S=sqrt(K) and A_a=S^(-1/2) Delta_a S^(-1/2) on P. Since Delta_a^2<=K, operator monotonicity of square root gives |Delta_a|<=S. Therefore -I<=A_a<=I. Under maximally mixed junk replication, A_a^(r)=A_a tensor I_r: both its norm and its centrality defects are replication-invariant.

The exact fixed-point identity
 sum_a A_a S A_a=S
follows by expanding and using sum Delta_a^2=K=S^2. But in general sum A_a^2 is NOT I. It must not silently be treated as a normalized Clifford tuple.

## 3. An exact weighted Dirichlet identity
Let E=sum_a A_a^2-I_P. Direct trace expansion and the fixed-point identity give
 sum_a ||[A_a,S]||_F^2 = 2 Tr[S^2 E] >=0.
Indeed each squared commutator is 2Tr(S^2 A_a^2)-2Tr(S A_a S A_a), and the latter sum is Tr(S^2). Consequently
 sum_a ||[A_a,S]||_F^2 <= 2 ||E||_op Tr K.
No spectral gap or ambient-dimension factor enters this identity.

In particular E=0 forces every A_a to commute with S. If additionally [{A_a,A_b},A_c]=0, then Delta_a=S A_a and [{Delta_a,Delta_b},Delta_c]=S^3[{A_a,A_b},A_c]=0. Conversely exact central closure of Delta implies K commutes with every Delta, so E=0 and the normalized A have central anticommutators. Hence these TWO normalized conditions characterize the exact central class:
 (i) sum A_a^2=I_P;
 (ii) [{A_a,A_b},A_c]=0 for all indices.
Condition (ii) alone is not used as an equivalent promise.

## 4. What this does and does not open
This gives a scale-invariant candidate pair of approximate defects, and a quantitative, response-weighted commutation consequence of the first. It does not supply a nearby exact Clifford representation from the second, implement S^(-1/2), prove approximate joint-QPE behavior, or bound decoding regret. Those are the genuinely unresolved bridge. In particular measuring full K can disturb logical information when it does not commute with the responses; the general information-support filter only copies/uncomputes a threshold bit and does not license such a measurement.

The same continued-source and trusted-control qualifications as the exact streaming theorem would remain necessary for any collision-based implementation. No stronger access to the environment or a source inverse is introduced here.

## 5. Executed evidence
check_normalization.py constructs a generic noncentral qubit-to-qutrit CPTP map and five junk replicas r=1,2,3,5,9. It checks the r^-3 raw defect law, invariant normalized tuple/defect, axis contraction, exact fixed point, and the weighted Dirichlet identity numerically. These are diagnostics of the algebra, not an implemented recovery or finite acquisition of the defects.
