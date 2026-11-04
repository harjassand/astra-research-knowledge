# Independent audit of the direct endpoint correction

4 November 2026. Refers to the original PROOF.md, SHA256 fb5d4f943cf79c863019eb820f57f5c13683f1b6adc2b683f5c12fb6bab20314. Original proof and audit are unchanged. This auditor also read and verified CORRECTION.md, SHA256 80b7fc407d2487a83b459f5eaf028b9cf31156a0d1575b69f08cefd1d5962407. Its algebra, biconnected scope, finite symmetric-factor compatibility test, and conservative ratio-error bound B=2 eta/r+2 eta/r^2 for eta<r/2 are correct. Its endpoint-gap requirement g>2B is sufficient; arithmetic error must be included as stated.

**Verdict:** The direct maximum-principle reconstruction is correct. I independently approve the spanning biconnected extension of the exact generator-identification theorem. The earlier three-connected theorem remains true, but graphic reconstruction and state-label alignment are unnecessary. The endpoint principle has direct published prior; this correction should reduce, not inflate, the novelty assessment.

## Independent derivation

For a nonzero finite response d=pi'−pi on an unknown pair {a,b}, stationarity gives Wd=alpha(e_b−e_a), with alpha nonzero. Put h_i=d_i/pi_i and L=W diag(pi). Since Wpi=0, L has zero row sums and nonnegative off-diagonal entries. At every nontarget state,

0 = sum_{j != i} W_ij pi_j (h_j−h_i).

Thus h is harmonic off the target pair. Assume alpha>0. State b cannot be a maximum because (Lh)_b>0; state a cannot be a minimum because (Lh)_a<0. Irreducibility and propagation of equality in the harmonic equation place a at a maximum and b at a minimum.

If the baseline contains a spanning bidirected biconnected selected graph, any nontarget state has a path to b avoiding a. A nontarget maximum would propagate along this path, forcing b to be a maximum, contradiction. Similarly no nontarget can share b's minimum. For alpha<0, the endpoint roles reverse. Therefore the unique maximum and minimum of d_i/pi_i identify the unordered physical target pair in a linear scan. Extra positive directed rates do not spoil the argument.

With those endpoints known, solve 1^T K=0, Kpi=0, and require Kd_e to vanish outside each recovered pair. A spanning biconnected graph has connected cycle matroid. The original cycle-rigidity argument now applies directly in physical state coordinates and gives K=cW. Choosing the generator sign and one clock normalization finishes the reconstruction. No unknown permutation or graph-recognition algorithm remains. This covers triangles and four-cycles as well.

## Independent exact checks and scope

For the four-cycle with clockwise rates 2 and anticlockwise rates 1, pi=(1,1,1,1)/4. Doubling pair {0,1} gives pi'=(22/105,29/105,4/15,26/105), hence h=(-17,11,7,-1)/105. The extrema identify the pair although the graph is not three-connected.

Some condition preventing endpoint plateaus is real. For a biased triangle on states 0,1,2 with clockwise rates 2, anticlockwise rates 1, and a symmetric unit-rate pendant connection 0–3, pi is again uniform. Doubling pair {0,1} gives h=(-5,7,3,-5)/45: the pendant state ties target 0 at the minimum. An arbitrary argmin is unsafe outside the sufficient assumptions. Biconnectivity is not asserted necessary for all identifiable cases.

With coordinate estimation error eta and pi_min>eta, let R=max_i(pi'_i/pi_i). Then

||hhat−h||_infinity <= eta(1+R)/(pi_min−eta).

If twice this bound is less than both endpoint-to-runner-up extremum gaps, the target pair is recovered exactly. The later singular-value requirement for reconstructing W still applies. This replaces the matroid rank-margin requirement, but does not create a uniform finite-sample guarantee or eliminate rare-state and mixing costs.

## Verified prior and significance

I independently downloaded and inspected J. J. Hunter (2002), *Stationary Distributions and Mean First Passage Times of Perturbed Markov Chains*, Research Letters in the Information and Mathematical Sciences 3, 85–98. Corollary 4.1.2, equations (4.7)–(4.8), and page 93 explicitly establish that relative-response extrema occur at the two perturbed destinations. The model changes two entries of one row of a discrete-time transition matrix. The present finite edge intervention differs physically but produces the same two-coordinate stationary forcing. This is a strong direct predecessor for the endpoint principle.

Primary PDF: https://mro.massey.ac.nz/server/api/core/bitstreams/8b373271-6b75-456d-84ab-1ecfd6b7cd19/content

Hunter is not being claimed to contain the entire blind generator-reconstruction theorem. The corrected result combines an established response extremum property with the labelled cycle-rigidity construction. No priority clearance, new general maximum principle, or exceptional experimental capability is established. The earlier audit checked the correctness of the more elaborate route but missed this substantially simpler same-data baseline; that assessment is now corrected.

A longer independent derivation and explicit generator matrices are preserved separately in ENDPOINT_AUDIT_ADDENDUM.md.
