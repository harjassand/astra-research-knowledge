# FLAG-XOR plus fast noisy verifier: direct generator and code-frame derivation

2026-11-01, derived after the parent's new FLAG-XOR proposal. This is a different architecture from the phase-disabled plan verifier. The earlier rearm counterexample does NOT refute it: this construction uses small verifier-energy weights and fast repair rates, not a demand that each wrong actuation be individually downhill.

## 1. Explicit physical registers and commuting potential

Let W be the already accepted Tanner-witness potential, whose arguments are commuting actual code stabilizers S and witness Z-basis variables a. For every fixed candidate witness-flip mask x_j introduce a PHYSICAL flag qubit b_j. Define
 F_flags=product_(j,i:x_j(i)=1) CNOT(b_j -> a_i),
 y=a XOR sum_j b_j x_j,
 W_v=F_flags W F_flags†=W(S,y).
All flag-controlled witness flips commute. The number of candidate masks, masks per witness, total flag count, and interaction incidence must be counted; they can be enormous fixed code-degree constants. The flags are noisy gauge registers, not a reliable classical history.

For every candidate j, f_j(S,y) is a Boolean permission: if true, flipping mask x_j strictly lowers W by at least1. Construct finite-fan-in Boolean DAGs evaluating these permissions from physical a,b and actual stabilizers. XOR computations of y are part of the DAG, not free input wires. Use physical wire qubits; the terminal wire is c_j. An actual stabilizer input S_v is represented by a physical syndrome-input wire t_v with its own consistency constraint. Do not assume it is correct.

For every gate/input-copy i, let e_i be the projector onto an incorrect output. For a two-input gate, e_i=[z_i != f_i(z_parents)]. For a stabilizer-input wire, e_i=[t_v != syndrome(S_v)]. All e_i, W_v, and physical wire/flag Z operators commute. Choose positive weights recursively backwards through the DAG,
 w_i >= 1+sum_(k direct child of i) w_k,
counting each affected child once or more conservatively. Let E=sum_i w_i e_i, w_max=max_i w_i, and
 Q=W_v+epsilon E.
This is a positive sum of commuting local terms on the actual physical registers. 'Local' initially means bounded support on the stated Tanner graph, not Euclidean short range.

## 2. Native classical repairs; quantum input primitive exposed

At rate gamma, overwrite each gate output by its function of current parent bits. Implement this using one jump per parent pattern, each mapping the incorrect target bit to the correct value. At most one jump per gate is enabled in any basis state. Two-input gates therefore require at most THREE physical qubits. A violated gate is corrected, at most its direct children become newly violated, and no root a or b changes. Thus
 Delta E <= -w_i+sum_child w_k <= -1,
 Delta W_v=0.
Since sum_i e_i >= E/w_max,
 L_repair^* Q <= -(gamma epsilon/w_max) E.

A quantum syndrome-input repair is instead
 L_(v,s)=sqrt(gamma) Pi_(S_v=s) tensor |s><1-s|_(t_v).
It nondestructively overwrites the cached syndrome and has support weight(S_v)+1. Its rate, imperfect implementation, data backaction and all associated apparatus must be charged. THIS IS NOT A THREE-QUBIT NATIVE OPERATION when S_v has high weight. The generator proof below includes it explicitly and does not claim that the full strictly few-qubit hardware gate has been closed. Compiling it into a timed QND circuit requires a further implementation theorem, not just a circuit diagram.

## 3. Wrong permissions are controlled by real violated gates

Compare current c_j with the ideal DAG evaluated on the actual roots (S,a,b). If an output is wrong, at least one ancestor gate/input-copy violates its local equation: otherwise induction in topological order makes it correct. Let R bound the number of permission outputs downstream of any single violated gate. Then
 N_false_positive <= R sum_i e_i <= R E,
 N_false_negative <= R E.
R is fixed only if the actual circuit family has bounded per-location size/fanout; explicitly enumerate and charge it for the chosen selector/mask layout.

Assume the accepted witness theorem provides at least c W_v true permissions in the safe virtual basin. This is valid for one chosen improving mask per original location, or all masks with permissions that include that chosen branch. Additional masks increase hardware/rates and are not free. Therefore
 N_correct_enabled >= c W_v - R E.
This inequality is useful even if its right side is negative.

## 4. Two-qubit actuation and full mean generator bound

For each candidate use
 L_act,j=sqrt(kappa) X_(b_j) tensor |1><1|_(c_j).
This is a TWO-QUBIT jump; it toggles one physical flag and thereby the whole virtual witness mask. There is no consume/rearm phase and no finite history buffer. A stale c_j can immediately toggle it back; that reverse mistake is deliberately included as false-positive activity.

Let D bound |Delta W_v| for every flag toggle, and B bound |Delta E| for one flag toggle. B is the sum of weights of all actual constraint terms whose inputs change, including XOR preprocessing; it is finite but potentially enormous. Choose
 a0=1-epsilon B>0,  A0=D+epsilon B.
Every correctly enabled actuation has Delta Q<=-a0; every falsely enabled one has Delta Q<=A0. Hence
 L_act^* Q <= -kappa a0 c W_v + kappa R(a0+A0) E,
and the entire ideal generator satisfies
 L_ideal^* Q <= -kappa a0 c W_v
   -[gamma epsilon/w_max-kappa R(a0+A0)] E.
Choose gamma epsilon/w_max > kappa R(a0+A0). All constants can be fixed independently of total memory size, provided the actual code-degree/circuit constants are fixed. This is a DIRECT extensive drift inequality, not a mean completion probability.

## 5. Exact exponential-potential bound; no exponential-order trap

All ideal jumps act as injective partial permutations of the joint stabilizer/register labels, with actual syndrome projectors for quantum input repairs. For F=exp(alpha Q), compute their weighted exponential increments directly. The pointwise identities lift to operator inequalities because F and jump source projectors are jointly diagonal in the commuting label algebra; quantum coherences in the state are not discarded.

A gate repair reduces Q by at least epsilon, a correct actuation by at least a0, and an incorrect actuation increases it by at most A0. Therefore
 F^(-1/2) L_ideal^*(F) F^(-1/2)
 <= -kappa c(1-exp(-alpha a0)) W_v
 +{ kappa R[(1-exp(-alpha a0))+(exp(alpha A0)-1)]
    -gamma(1-exp(-alpha epsilon))/w_max } E.

For any sufficiently small fixed alpha>0 and sufficiently large fixed gamma, the E coefficient is strictly negative. Write the two negative coefficients as u>0 and v>0. Since Q=W_v+epsilon E,
 L_ideal^* F <= -min(u,v/epsilon) Q F.
This supplies the extensive exponential drift needed by the parent's rare-event route. Additional arbitrary coherent Hamiltonian and local bath noise is NOT assumed classical; it must be admitted using the parent's local weighted-conjugation perturbation bounds with all new support, incidence, energy-weight, flag and wire counts included. No global T-times-microscopic-error approximation is used.

## 6. Exact verifier-frame unitary, ground space and distance

There is an explicit reversible circuit U_DAG. In topological order, XOR each gate function into its dedicated output qubit; for a stabilizer-input wire, XOR the actual syndrome via its spectral projector. The function controls may be many-body at this ANALYTIC encoding step, but every support is bounded in the code family. U_DAG leaves all root variables and all actual stabilizers unchanged.

Apply its inverse in reverse topological order to an ARBITRARY assignment of wire bits. When a wire is processed, its parent bits still have their original values; its output becomes exactly its original constraint-violation bit. Thus
 E = U_DAG (sum_i w_i n_i) U_DAG†.
Also U_DAG commutes with W_v. Consequently the exact potential identity is
 Q = U_DAG F_flags [W + epsilon sum_i w_i n_i] F_flags† U_DAG†.

This is stronger than merely guessing the kernel. Let K_old be the accepted protected-plus-gauge zero space of W. Then
 ker Q = U_DAG F_flags (K_old tensor H_flags tensor |0...0>_wires).
Every flag configuration is a legitimate gauge degree of freedom after decoding; every verifier wire is fixed in the decoded frame. There is no reliable-metadata premise. The protected logical algebra is conjugated by this explicit unitary (and by the old witness frame).

If U_total=U_DAG F_flags has a bounded-depth, bounded-support, bounded-incidence implementation as an ANALYTIC local circuit, let C be its maximum backward light-cone expansion for arbitrary supported operators. Then any operator on r new physical qubits decodes to support at most C r on the old system plus gauge/initialized auxiliaries. Thus subsystem distance satisfies d_new>=d_old/C. This argument uses operator support, not a false claim that the nonlinear Boolean circuit is Clifford. All circuit depths, expanded supports and C can be huge constants and must be supplied for a useful instance.

The parent's full protected-component/boundary interface must still be transported through this finite-depth frame and checked, especially because a physical Pauli need not decode to one Pauli under U_DAG. Finite-support operator expansion rather than Clifford-only reasoning is required. The exact ground/distance identities alone are not a completed lifetime proof.

## 7. Scope and comparison

This proposal succeeds at the proposed generator inequality and exact ground mapping. It removes classical clocks, transaction rearming and ownership locks from the W-drift mechanism, conditional on the explicitly supplied quantum syndrome-input repair primitive. All selector wires and flags are physical noisy qubits. Wrong actuation is paid by fast repair, not forbidden by trusted metadata.

It does NOT yet synthesize high-weight QND syndrome-input repair from native two-/three-qubit Hamiltonians and simple reservoirs. The ordinary active Tanner decoder receives exactly the same syndrome primitive, graph connectivity, flags/wires, local gates, reset resources and rates. If the primitive is granted, the candidate new capability is time-independent noisy-classical-controller drift under the parent's stronger coherent-noise admission, not an asserted practical resource advantage.

## 8. Independent finite check

`check_flag_verifier.py` enumerates all 4096 physical configurations of a two-witness, three-flag, seven-wire Boolean-DAG example. It checks the actual mean and exponential generator inequalities, including stale permissions and reverse toggles, and verifies that the reverse-topological circuit maps every arbitrary wire assignment to its violation bits. All checks passed; output is in `check_flag_verifier_results.txt`. This checks the commuting algebra and bookkeeping, not native quantum-syndrome synthesis or a lifetime theorem.
