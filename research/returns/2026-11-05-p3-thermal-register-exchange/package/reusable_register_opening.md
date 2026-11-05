# Reusable thermal register: working theorem

Status: derived in this exchange. Operational strengthening of the accepted P1 thermal loader. This is not a constant-noise hardware threshold, and does not reproach the accepted BDL lifetime proof.

## Contract

In a stabilizer code's protected frame, V_s = F_s^dagger V_0 identifies each valid syndrome sector with a common logical subsystem. The Hamiltonian is scalar E(s) on that sector. Let pi(s) be its Gibbs syndrome law. For the specified energy-resolved one-site Pauli Davies bath, a jump a at syndrome s has rate q_a(s), changes the syndrome to s+d_a, and acts on the logical subsystem by the Pauli ell_a(s)=V_(s+d_a)^dagger P_a V_s. The no-jump evolution is scalar on the logical subsystem. The autonomous syndrome chain has stationary distribution pi.

Define b(s)=sum_a q_a(s) 1[ell_a(s) is nonidentity modulo global phase], and lambda_L=sum_s pi(s)b(s). If s is stable against all elementary Paulis, b(s)=0. With cN jump channels of rate at most Gamma, lambda_L<=c Gamma N pi(unstable).

Active instruments act on logical registers, ports, and references in the SAME way in each syndrome sector. They preserve the syndrome. They may depend on all retained classical information, including observed syndromes. The bath is isolated during active operations, or its effects are included in the operation's implementation error. Adaptive passive holding intervals have total duration almost surely bounded by T. Separate independently held blocks have their own passive clocks and exposure bounds.

## Theorem and proof

Initialize the syndrome once with p satisfying TV(p,pi)<=epsilon_init. The joint memory/reference state is block diagonal in that classical syndrome. Allow arbitrary logical/reference entanglement conditional on the sampled syndrome, using a common conditional preparation in the two comparisons. Compare an arbitrary compatible classically timed adaptive experiment to an ideal experiment with the SAME syndrome path and logical instruments, but every holding jump's logical Pauli replaced by the identity. The trace distance of the complete final quantum state and retained records is at most

epsilon_init + T lambda_L + sum_j epsilon_control,j.

The comparison is uniform over compatible classically scheduled adaptive strategies, and so is a process guarantee. It does not include coherent quantum control of the holding clock or bath coupling. The ideal does not assert that successive thermal syndrome reports are independent. The guarantee is unconditional on the retained records: conditioning on a rare accepted record requires the usual division by its acceptance probability. A canonical TFD coherent across syndrome sectors is a separate preparation capability, not an allowed initial state of this trajectory proof.

Proof: syndrome-block-diagonal states remain block diagonal under the specified bath. Each jump's probability and waiting time depend only on the syndrome, because energy projectors are syndrome scalars and the elementary Pauli is unitary. Couple actual and ideal experiments to the same autonomous syndrome trajectory, jump labels and instrument realizations. They coincide, including arbitrary entangled references, until a nonidentity logical Pauli occurs. In accumulated passive time, ideal active operations only pause the syndrome trajectory; they never change its value. Extend the trajectory to deterministic duration T if the strategy stops earlier. Since its starting law is pi, the expected count of nontrivial logical jumps up to T is T lambda_L. The probability of at least one is no larger. Coupling p to pi costs TV(p,pi) once. A standard channel hybrid over faulty active instruments contributes the sum of uniform diamond errors. No uniform rare-posterior stability claim is required.

## Executable reusable interface

Measure the commuting checks to obtain s, apply F_s, and invert the ground-state Clifford encoder. The stored unknown logical state is now on designated ports. Apply a logical instrument or swap in a new unknown input; re-encode and apply F_s^dagger. Every ideal branch returns exactly the same syndrome s. Measuring s is nondisturbing on the stipulated block-diagonal state. Reversible syndrome extraction and decoder evaluation give a coherent implementation if required, but ordinary measurement and classical evaluation suffice here.

The original Gibbs sample is reused. It is unnecessary to draw a fresh sample and reset the thermal background after each logical read/write. Ancilla reset, classical memory protection, port storage, gate compilation/routing, bath isolation, precision, energy and active time remain charged.

## BDL consequence and limits

The accepted BDL/historical compiler gives pi(unstable)<=C exp(-c N^eta) and polynomial preparation and frame evaluation at its stipulated low temperature. Therefore the complete campaign error is at most

epsilon_init + sum_j epsilon_control,j + C' Gamma N T exp(-c N^eta).

The number of active operations enters their actual costs and implementation errors; it does not separately multiply the initial sample error or passive exposure term. Sum bounds over multiple independently held blocks. A suitable power of log(total requested exposure / target error) suffices asymptotically for each block size, subject to the large actual family constants.

This supplies a reusable quantum register under the declared Hamiltonian and bath contract. It does not supply independent syndrome samples, generic noncommuting fabrication robustness, constant-rate noisy gates, a finite-bath derivation valid for exponential time, or a bridge to the classical burst-loss or P2 momentum-replacement models.
