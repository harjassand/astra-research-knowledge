# Root construction: a Liouville-space boundary lift for classical channels

24 October 2026, 14:41 UTC. Candidate theorem; independent check requested. No historical priority or external acceptance claimed.

Let K(y|x) be any finite classical stochastic channel, acting on a classical register with arbitrary finite quantum reference. Define eta_c,D by same-reference-marginal hypotheses and eta_Delta,D by reference-subtracted relative entropies. Claim: these two Umegaki coefficients are equal for EVERY such K. This does not say that either equals the scalar classical coefficient, and does not assert equality for arbitrary quantum transmitted channels.

## Complete SLD to complete BKM lift

Take faithful subnormalized r-by-r blocks sigma_x with sum of traces one, Hermitian tangent blocks H_x, and sum_x H_x=0. Let Omega_s(X)=(sX+Xs)/2. Its positive matrix on Hilbert-Schmidt space C^(r^2) has trace r Tr(s). Define Gamma_x=Omega_(sigma_x)/r, so sum Tr Gamma_x=1.

Fix any full-support probability vector q_x. On reference C^(r^2) direct-sum C, define faithful blocks
S_x(epsilon)=(1-epsilon) Gamma_x direct-sum epsilon q_x,
T_x=|vec H_x><vac|+|vac><vec H_x|.

Each T_x has trace zero, and sum T_x=0, so S +/- tT are normalized hypotheses with identical reference marginals, positive for sufficiently small t at every fixed epsilon>0. Moreover K maps Gamma_x exactly to Gamma'_y=Omega_(sum_x K(y|x)sigma_x)/r and T_x exactly to the lift of H'_y=sum_x K(y|x)H_x. The vacuum coefficient becomes epsilon q'_y. Discard identically zero output rows; all remaining q'_y>0 and sigma'_y faithful.

For a fixed positive Gamma and vector h, the BKM quadratic form of this off-diagonal tangent at ((1-epsilon)Gamma) direct-sum epsilon q is
2 <h, [log((1-epsilon)Gamma)-log(epsilon q) I] [ (1-epsilon)Gamma-epsilon q I ]^(-1) h>.
The continuous divided difference is used at coincident eigenvalues. Dividing by 2 log(1/epsilon) and taking epsilon down to zero gives <h,Gamma^(-1)h>.

Consequently the input limit is r sum_x Tr H_x Omega_(sigma_x)^(-1)(H_x), and output is the analogous r sum_y expression. The factor r cancels. Every complete SLD tangent quotient is approached by complete BKM tangent quotients with reference dimension r^2+1, and hence by finite same-marginal Umegaki state-pair quotients (epsilon fixed first, then t down to zero).

This is a state construction, not a claimed physical channel taking arbitrary unknown reference states to Liouville space. In a vectorization convention Omega_s=(I tensor s+s^T tensor I)/2. The transpose term does not license a universal completely positive physical preparation map. Known finite hypotheses can nevertheless be prepared in principle as ordinary positive matrices.

The reverse coefficient inequality eta_c,BKM <= eta_c,SLD follows from the untouched-qubit SLD integral representation of BKM, with the reference including that qubit. Thus the optimized complete coefficients agree, although the metrics do not agree pointwise.

## Conditional versus complete

At any cq baseline sigma and tangent H, put L=Omega_(sigma_R)^(-1)(H_R), and H0_x=H_x-Omega_(sigma_x)(L). Sum H0_x=0. The exact SLD gauge identity is
sum_x g_(sigma_x)(H0_x)=sum_x g_(sigma_x)(H_x)-g_(sigma_R)(H_R).
K preserves the reference sum and maps Omega_(sigma_x)(L) to Omega_(sigma'_y)(L), so the same identity holds at output. Thus every conditional SLD quotient is bounded by the complete SLD coefficient.

Integrating the untouched-qubit SLD representation gives the same bound for conditional BKM differences, and integrating along the affine hypothesis segment gives the conditional Umegaki inequality. Therefore eta_Delta,D <= eta_c,SLD = eta_c,D. The opposite inequality follows immediately from the same-marginal subclass. This proves the claimed equality, subject to independent verification of the standard integral/support extensions already used in the predecessor theorem.

All reductions use arbitrary finite quantum reference dimensions. The lift enlarges memory and uses singular limits, so no uniform finite-precision bound or finite optimizer follows. Faithful states suffice for the supremum via the usual support approximation; undefined infinity-minus-infinity cases are excluded by the coefficient definition.

## Why this does not prove the all-quantum-channel conjecture

For a classical channel, mixing positive reference blocks commutes with the linear map sigma -> Omega_sigma. A channel on a genuinely quantum input does not in general act as that same channel on the left/right Liouville factors simultaneously. The original physical input dimension and one-use channel action must be retained. No such commuting physical implementation has been established here.
