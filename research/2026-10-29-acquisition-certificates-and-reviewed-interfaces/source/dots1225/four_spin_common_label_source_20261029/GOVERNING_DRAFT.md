# One finite four-spin source with the same star-label law
2026-10-29. Separate unreviewed construction; not folded into the accepted two-qubit receipt.

Let G be the24 orientation-preserving signed permutation matrices in SO(3), and choose SU(2) lifts u_g. The exact second moment is

 (1/24)sum_g (g_ca g_db)=delta_cd delta_ab/3.

If a=b, nonzero products require c=d and a random permutation sends column a to row c with probability1/3. If a!=b, the two nonzero rows differ; averaging the four even diagonal sign flips kills their product. This proves the formula without an approximate design or Haar integration.

On four physical spins choose unknown local V_0,...,V_3 and W=tensor_j V_j. Define a SINGLE source

 T_W(X)=(1/24)sum_g [W u_g^{tensor4} W†] X [W u_g^{tensor4} W†]†,
 N_W^eta=(1-eta)T_W+eta D_16, 0<=eta<=1.

It has24 known-form random-unitary Kraus operators and256 depolarizing matrix-unit Kraus operators, with unknown W not provided to the learner. This defines a finite memoryless source family; it is not a laboratory implementation. T_W is a TP, unital, self-adjoint group twirl. It is NOT asserted to equal the full four-spin SU(2) Haar twirl: only the exact pair second moment below is needed.

For each star edge (j,0), let P_ab^(j)=sigma_a^(j)sigma_b^(0), with identities on the other spins. These nine operators are orthonormal under Tr(A†B)/16. Their collective signed-permutation transfer is the rank-one projector onto vec(I3)/sqrt3. Local conjugation sends this vector to

 (c_j)_ab=(R_j R_0^T)_ab/sqrt3,

where V_j sigma_b V_j†=sum_a(R_j)_ab sigma_a. Thus the same source, on every edge, has transfer |c_j><c_j| and commutator Gram

 H_j=sum_l Tr([K_l,P_a^(j)]†[K_l,P_b^(j)])/(2*16)
    =I9-(1-eta)|c_j><c_j|.

Run the same controlled nine-label commutator instrument with all FOUR source carriers initialized maximally mixed. The minus amplitudes have factor1/(2sqrt9), so its output is H_j^T/18, independent of the carrier dimension. Therefore every edge has minus probability(8+eta)/18 and normalized state

 sigma_j=[P_(c_j perpendicular)+eta|c_j><c_j|]/(8+eta).

Records from fresh calls to this memoryless source are independent conditional on their selected edges; same-edge records have the identical isotropic pollution x=eta/(8+eta). This is not an assumption of independent physical pair sources or independent simultaneous records from one call. Adaptive edge choice must retain its usual causal/record accounting.

## Protected carrier and full-rank boundary
Every u_g^{tensor4} acts as identity on the two-dimensional total-spin-zero sector P0 (up to irrelevant lift phases). Hence T_W is exactly identity on all encoded states/operators in W P0, including arbitrary logical reference correlations. This gives one common protected FOUR-spin source port at eta=0, not just an entanglement-breaking two-spin example. Depolarization destroys exact protection for eta>0; its source Choi floor is eta I256/16. The previous full-rank exact-variable-gate boundary therefore applies to this family too.

The common source does not supply a free unknown-frame unitary oracle. Constructing, storing, extracting or approximately applying its label program still requires the separately checked interfaces. Acquisition calls use maximally mixed carriers; service calls use the protected encoded logical carrier, under the declared common-map boundary. Known controls/storage and finite mixtures remain paid assumptions. No practical yield, historical novelty, generic correlated-noise or capacity claim is made.
