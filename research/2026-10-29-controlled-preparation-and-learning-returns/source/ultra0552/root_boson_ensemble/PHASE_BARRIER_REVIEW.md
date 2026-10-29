# Root review of the local phase-law obstruction

29 October 2026. Full mathematical review of
`a_independent/canonical_overlap/PHASE_LAW_BARRIER.md` and full read of
`compile_bound_and_condition.py`. Accepted at the precise representation and
estimator scope below. This is not a physical hardness or novelty receipt.

I independently reconstructed the following load-bearing arguments:

* The mean uses only physically required Fourier moments. The second moment
  does not; splitting h_K^2 into a low core and remainder is essential.
* The low core's squared norm has nonnegative known moments and keeps its
  zero-frequency sum of squared composition-pair counts. Symmetric unimodal
  coefficient averaging and the restricted r32 composition ensemble give
  the stated exponential lower bound after the exact integer inequality.
* For site laws, a cross monomial has at most one uncontrolled coordinate.
  Its compensating known coordinates pay exp[-4(K+1)^2/(M-1)], including the
  entire coefficient mass D^4. Positivity alone does not make that cross
  term nonnegative; the quantitative suppression pays the issue.
* For fixed-size correlated blocks, the core has <=2R particles per block;
  M>=16R pays the remaining compensating Gaussian energy. Two uncontrolled
  blocks cannot occur in a monomial with total degree 2K. The theorem's
  exact divisibility/size threshold is retained.
* Exact product-block HS identities force the needed moments up to a common
  phase by the three-block charge functional equation. Required moments are
  nonzero, so the divisions used there are legitimate. Removing the common
  phase leaves |h_K| unchanged.
* The iid relative-MSE consequence and constant-envelope rejection consequence
  follow from exact variance and E W^2<=esssup(W) E W. Neither is a lower
  bound for all estimators, importance measures, or correlated field chains.
* The O(M)-bit perturbation argument pays product-moment telescoping and
  coefficient mass; it does not certify a PRNG as ideal randomness.

The ordinary difference-vector DP counts each physical occupation pair once:
given d=alpha-beta with positive and negative masses p=n, common occupations
have total K-p and binomial(K-p+M-1,M-1) possibilities. There is no local cap.
The tail D^2 exp[-4(Ecut+1)] and energy-moment bound 2K^2 times that tail are
conservative and valid. The required comparison is the SAME diagonal t4,
K=M physical input, not a distinct easy model substituted afterward.

Root read-only replay ran the M64 compiler/DP without invoking its writing
main. It reproduced 2100 maximum states, 437414 integer updates, the stated
rational enclosure and sample lower bound. An additional root-only full
occupation enumeration for M=K=3 (100 pairs) lay inside its independent
rational DP bounds. These are implementation controls, not the premises of
the all-size proof. Producer timing is not converted into an end-to-end
machine-independent performance claim.

Decision: optimizing independent finite phase alphabets or fixed-size block
laws alone is a ruled-out uniform direct-sampling remedy in this class.
Globally correlated proposals, conditional integration, field MCMC,
nonunitary HS factors and different estimators remain live. Noncommuting
frustrated hopping is not solved by the diagonal ordinary DP.
