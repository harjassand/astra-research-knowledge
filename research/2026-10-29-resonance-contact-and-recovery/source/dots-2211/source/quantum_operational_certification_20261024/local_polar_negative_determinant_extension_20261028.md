# Physical handedness correction for every nonsingular local qubit channel

28 October 2026. Root candidate addendum, separately reviewed before use. The received positive-determinant source remains unchanged. This removes its determinant-sign restriction by changing the canonical residual convention, not by implementing a transpose.

## 1. Exact construction

For each nonsingular real Bloch matrix T of a genuine qubit CPTP channel, let T=O S be the right polar decomposition, S>0 and O orthogonal. Set s=det O in {+1,-1}, D=diag(1,s,1), and O_eff=O D. Then det O_eff=1. A physical unitary U_eff implements O_eff, and

    E_eff=Ad_(U_eff dagger) composed E

is CPTP with Bloch contraction D S and affine translation O_eff^T t. If s=-1, D S need not be positive or symmetric. That does not invalidate physicality, which follows from actual unitary composition. No physical map implementing D alone is requested.

For the product-channel/local-mixer family define V_eff=V(tensor_i U_eff,i). The actual reduced source factors exactly as Ad_(V_eff) composed (tensor_i E_eff,i). The local algebra supports are unchanged. The goal is the inverse of this canonical mixer, not noise removal or recovery of an unidentifiable original V.

## 2. What the acquired contrasts determine

Use the same common-positive-spectator-factor contrasts, but allow any invertible T:

    C_j=sum_a T[a,j] B_a R,
    R>=0, [R,B_a]=0, R>0 on the containing envelope.

With c=Tr R^2, the Gram matrix is G=c T^T T=c S^2. Thus whitening gives

    F_j=sum_k C_k [G^(-1/2)]_kj
       =B_(O e_j) R/sqrt(c).

The signs A_j=sign(F_j)=B_(O e_j) are physical reflections. Orthogonality makes A_X and A_Z anticommute regardless of det O. Set the target logical generators

    B_eff,X=A_X, B_eff,Z=A_Z,
    B_eff,Y=i A_X A_Z=s A_Y.

These are exactly the conjugated Pauli axes of O_eff. The actual extraction circuit uses only X and Z, so it does not need to determine s before execution. A finite acquired Y matrix remains useful for estimating the orientation or residual channel, but no antiunitary gate is used.

The scalar Gram normalization remains valid even at negative determinant: Tr|F_j|=Tr R/sqrt(c), and for the stationary product family Tr R=1 gives S=Tr|F_j| sqrt(G). For residual parameters the physical Y expectation must use i B_eff,X B_eff,Z, not the uncorrected acquired Y sign. Applying an SPD residual formula without the D factor would be wrong.

## 3. Finite certificates and restrictions

The finite perturbation proof for Gram inverse square root depends on positivity of G, not positivity of T. The sign proof depends on positive R and fixed orthogonal O, not its orientation. Therefore a version of the three-axis learner whose fixed contract is arbitrary invertible T can certify the same X/Z operator approximations, and the same three-reflection receiver telescope targets V_eff dagger. This transfer requires separate review of the modified contract and guards; the original SPD receipt is not silently broadened.

If finite X/Z approximations do not exactly anticommute, the actual extraction circuit remains a physical unitary sequence as in the original construction. Its analysis compares to the true exact Clifford pair. Do not set an imperfect i S_X S_Z as a Hermitian measured observable without symmetrization or a separate physical construction. For a residual Y expectation, one may instead use the Hermitian commutator (i/2)(S_X S_Z-S_Z S_X), whose operator error is at most the sum of the two X/Z errors; its known matrix can be contracted against ordinary shadow estimates.

Singular T remains excluded: lost contrast directions make G singular, and finite guards may abstain. Variable T correlated with changing spectator factors remains excluded by the separate pooled-whitening counterexample. Conditioning may be arbitrarily poor. Full physical preparation/readout, source validity, bounded mixer locality, unknown-payload timing, control errors and complete-memory transfer retain their actual costs and assumptions.

The polar gauge is invariant under replacing V by V W and E by Ad_(W dagger) E for a local unitary W: O becomes W^T O, det O is unchanged, and V W (W^T O D)=V O D in Bloch notation. This is a conventionally fixed observable target, not identification of the microscopic placement of rotations.

No historical novelty, efficient code discovery, hardware threshold, or universal arbitrary correlated-noise recovery claim is made. The exact algebra opens the same local acquisition target to all nonsingular product qubit channels, subject to a separate finite acquisition proof.
