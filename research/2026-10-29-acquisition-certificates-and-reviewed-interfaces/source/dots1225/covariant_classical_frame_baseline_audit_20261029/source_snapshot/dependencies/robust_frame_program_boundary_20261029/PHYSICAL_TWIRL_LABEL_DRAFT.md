# An actual noisy source giving the isotropic almost-dark label

2026-10-29. Root derivation; receiving review requested.

The preceding label-pollution diagnostic can be realized by a concrete memoryless two-qubit source, rather than assumed as an independent corruption of quantum data.

Let T be the collective SU(2) Haar twirl: T(X)=P_s X P_s+Tr(P_t X)P_t/3, where P_s is the singlet projector and P_t=I-P_s. This is implementable as a channel using the known ten Kraus operators P_s and |t_i><t_j|/sqrt3, i,j=1,2,3. Here these Kraus matrices define the source family; the learner is NOT supplied its unknown local twist. No actual source hardware preparation is claimed.

In the nine-dimensional Pauli-product coefficient space P_ab=sigma_a tensor sigma_b, Hilbert--Schmidt inner product Tr(A†B)/4 makes this basis orthonormal. Let c=vec(I_3)/sqrt3. The twirl is the Hilbert--Schmidt orthogonal projection onto the collective commutant. Within this nine-dimensional subspace its transfer matrix is |c><c|, since T(P_ab)=delta_ab sum_j P_jj/3. The only other collective commutant direction is the identity, orthogonal to all nine products.

Using the accepted commutator Gram definition H_ab=Sum_l Tr([K_l,P_a]†[K_l,P_b])/8, unitality and self-adjointness give H=I-transfer(T)=I-|c><c|. Expanding the four commutator terms proves this directly; both diagonal terms contribute identity and both cross terms the self-adjoint transfer. A local conjugation W=V tensor I sends c to the corresponding real normalized rotation vector c_R, with conventions fixed by coefficient extraction Tr(P_ab W SWAP W†)/(2sqrt3). Thus H_R=I-|c_R><c_R|.

Now let N_R^eta=(1-eta)T_R+eta D_4, 0<=eta<=1, with D_4(X)=Tr(X)I_4/4. Depolarization has H_D=I_9, so linearity of the Gram in the channel gives
 H_R^eta=I_9-(1-eta)|c_R><c_R|.
The actual one-call commutator instrument's minus output is H^T/18. Since c_R is real, the minus probability is (8+eta)/18 and its normalized label state is
 sigma_R^eta=[P_(c_R perpendicular)+eta|c_R><c_R|]/(8+eta).
This is exactly the earlier IID label model with x=eta/(8+eta), a=1/(8+eta). Fresh calls to this specified memoryless source produce independent minus records. No marginal-to-independence inference is used.

For every eta>0 the source Choi matrix is positive definite with lower bound eta I_16/4, so the separate finite exact-frame-gate impossibility applies. Nevertheless approximate program operations remain possible. A1% SOURCE contamination eta=.01 corresponds to x=.01/8.01, NOT1% label pollution. Misidentifying these parameters would substantially misstate the noise threshold.

The script independently constructs Kraus operators and tests ten seeded unknown local twists and five eta values, including identity/full-depolarization endpoints. This is a floating algebra check supplementing the exact projection derivation, not acquired physical data. Source preparation, control noise, coherent-storage protection and subsequent extraction/purification resources remain separately paid.
