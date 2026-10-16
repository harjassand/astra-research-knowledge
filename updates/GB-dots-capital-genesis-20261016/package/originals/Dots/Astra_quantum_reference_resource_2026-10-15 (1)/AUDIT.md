# Independent exact reconstruction of the finite reference law

## Verdict

The mathematical argument in THEOREM.md passed an independent internal reconstruction of every inequality and a nontrivial symbolic sharpness example. This is not external peer review.

For m>=2, reference dimension at most r>=1, k=min(r,m-1), and 0<=lambda<=1, the sharp conditional RLD/standard-Petz chi-square excess coefficient is

c_(m,r)(lambda)=lambda²/[lambda+((1-lambda)/m)(k+1)/k].

It is equivalently the sharp reveal threshold for m-ary erasure dominance over the classical m-ary symmetric measurement channel in reference-dimension-restricted standard Petz-D2 order. Faithful state pairs may have unequal reference marginals. Exact-dimension and at-most-dimension suprema agree. This does not assert multiplicative contraction of logarithmic D2 or historical novelty.

## Projection lemma independently checked

For a rank-r orthogonal projection P on a block direct sum and a unit w in ker P, let p_i=||w_i||², and for nonzero w_i let u_i=w_i/sqrt(p_i) be block supported and q_i=<u_i,P u_i>. Set q_i=0 when p_i=0. Then sum p_i=1, sum q_i<=rank P=r, and 0<=q_i<=1-p_i. The final inequality follows from P<=I-ww*, since ran P is orthogonal to w.

The scalar identity

r²p+q-(r+1)²pq=(rp-q)²+(1-p-q)(r²p+q)

is exact; it was also checked symbolically. Hence sum p_i q_i<=r/(r+1), proving the compression inequality for the block pinching of P on ker P. No common eigenbasis or block-size hypothesis is needed.

For positive R_i summing to I_r, let A=[sqrt(R_1),...,sqrt(R_m)], P=A*A, and w_i=R_i^-1/2 z_i. Then AA*=I, P is a rank-r orthogonal projection, P_ii=R_i, and sum z_i=0 gives Aw=0. Directly E=||w||² and N=<w,diag(P_ii)w>. The projection lemma yields E>=(r+1)N/r. Combining it with the separately audited alphabet bound E>=mN/(m-1) gives E>=(k+1)N/k.

The existing spectral Jensen proof then supplies the asserted coefficient. Applying the vector inequality to z_i=Z_i xi for each xi proves operator order. The physical identity Z_i=H_i-R_i K, K=sum H_i, remains exact for Hermitian tangents. Whitening preserves the reference dimension. Crucially, the proof obtains an operator inequality before undoing whitening and taking trace; it does not incorrectly assume that the scalar ratio is invariant under congruence.

## Sharpness and admissibility

Use a k-dimensional reference and k+1 active symbols carrying the regular-simplex rank-one frame R_i^0=(k/(k+1))P_i. Set all other baseline blocks zero. Take H_i=h_i R_i^0 on active symbols with real sum h_i=0 and unequal h_i, and H_i=0 on inactive symbols. Then every Z_i is supported on the corresponding rank-one range, the collection is nonzero by the Hermitian nonorthogonal-eigenvector argument, and its conditional ratio is exactly the asserted bound in the boundary limit.

Faithful regularization R_i(epsilon)=(R_i^0+epsilon I)/(1+m epsilon) makes every block strictly positive, including inactive ones, while retaining sum R_i=I. Keeping H_i fixed is valid: it is supported on R_i^0, so each input inverse cost has a finite limit; target baselines remain uniformly positive for 0<lambda<1. The conditional reference term K² is fixed. The scalar total tangent trace is zero. Normalize by k and choose a sufficiently small pair perturbation; this gives faithful normalized state pairs with the same strict violation whenever erasure reveal q lies below the claimed coefficient.

For an exact reference dimension r>k, direct-sum a faithful baseline on the additional dimensions with all tangents zero. Both defects vanish on the added summand and the scalar ratio is preserved after normalization. This justifies the exact-dimension assertion as well as the at-most-dimension one. No general vector-to-Hermitian-tangent conversion is being assumed: the lower construction already has Hermitian H_i.

The lower construction generally has nonzero reference tangent K, so allowing unequal reference marginals is essential to the stated scope. The theorem does not establish the same formula under an additional equal-reference-marginal restriction.

## Independent symbolic example

checks/check_finite_reference.py uses m=4, r=2, lambda=1/2, three active trine projectors and one inactive symbol. It independently derives, for the stated epsilon regularization and fixed H=(R_0^0,-R_1^0,0,0),

input excess = 2(13epsilon+2)/[3(3epsilon+2)],
target excess = 8(52epsilon²+12epsilon+1)/[3(8epsilon+1)(24epsilon+11)].

Their ratio tends exactly to 4/11, between the scalar threshold 1/3 and unrestricted threshold 3/8. The script verifies the normalized baseline identity, tangent trace zero, and projection scalar identity. The reproducible fixture is checks/finite_reference_check.json.

The general proof is algebraic; this exact symbolic example is an independent consistency check, not its justification. Historical priority and implementation performance were not assessed.
