# Finite-rate control: what remains obstructed

Date: 2026-10-16. Internally proved method obstructions; no impossibility of quantum memory is asserted.

## 1. Every finite memory-only randomizer leaves missing bath Choi directions

Let A be a finite memory patch and B a finite persistent bath. Let R_A be ANY memory-only linear superoperator, including an arbitrarily strong but finite GKLS randomizer, dephaser, or full depolarizing dissipator. Consider the proposed finite-rate uniformization

    N_r = Id_AB + [R_A tensor Id_B - i[H_AB,.]]/r,

where r is finite and positive. Work after removing any permitted bath-only Hamiltonian into the baseline. Write normalized vectorization |X>=(X tensor I)|Omega_AB>, and set u=|I>. Let E be the vector subspace consisting of all |M_A tensor I_B>. The Choi matrix of Id_AB+R_A tensor Id_B/r is supported wholly in E.

If v_0=P_(E perpendicular)|H_AB> is nonzero, put v=v_0/||v_0||. Then v is orthogonal to u, and

    <v|J(N_r)|v> = 0,
    <u|J(N_r)|v> = i ||v_0||/r.

The commutator Choi matrix is -i|H><I|+i|I><H|. The compression to span{u,v} therefore has determinant

    -||v_0||^2/r^2 < 0.

Consequently N_r is not CP for ANY finite r, irrespective of the finite strength or choice of memory-only randomizer. A positive matrix must have zero cross entries to any vector with zero quadratic form; the Hamiltonian creates precisely a forbidden cross entry.

For H=J Z_A tensor Z_B on two qubits, ||v_0||=|J|. The same 2x2 determinant is -J^2/r^2 even if R_A includes every memory Pauli dissipator at arbitrary rates. The authored symbolic checker verifies this compression exactly.

This generalizes N881's specific depolarizing-floor counterexample to all memory-only finite randomizer generators. It does NOT show that the full continuous semigroup is unphysical: the Hamiltonian-plus-GKLS generator is valid. It does NOT refute the new finite-time Poisson-syndrome bound. It refutes the exact step converting this continuous joint generator into a sparse finite-rate CPTP proposal process by memory-only uniformization. Paid joint jump directions covering |H> can repair the Gram-range condition, under the separate N881 theorem.

## 2. Privacy and covariance are not calibration consequences

The supplied randomizer-control packet has an exact two-qubit example: every intended data flip X_D is accompanied by X_B on a bath qubit, while H=J Z_D Z_B. The corrected data controls are perfect in every reduced-data gate metric, but the joint flips commute with H and no randomization-rate suppression occurs. Winick et al. gives the same underlying frame-leakage mechanism in established randomized compiling.

The supplied qualified-core packet also has a compiler-following coherent drive error whose entire Fourier weight lies in the zero character. Small action plus additive private dependence is not sufficient: actual full-support conjugation covariance is needed to equate a zero character with ideal memory action. A tiny coherent unitary has no nonzero exact-ideal CP branch; ordinary infidelity does not identify a stochastic contamination parameter.

These are existing supplied obstructions, not new examples invented in this file. They remain decisive for interpreting the sharp endpoint theorem. Exact finite-rate Markov dephasing is a substantial operation premise. It is not implied by reduced detector tomography, small readout error, endpoint gate equality, or a formally chosen stochastic unraveling of an unrelated process.

## 3. Exact Markov freshness has a process-level dimension cost

Let G be an independent Pauli stabilizer group of size d_G=2^m and consider the isolated full-pinch Markov protector lambda(D_G-Id). Over an interval Delta>0 its channel is

    E_Delta = r Id+(1-r)D_G,  r=exp(-lambda Delta).

Its orthogonal random-unitary Choi weights are

    w_I = [1+(d_G-1)r]/d_G,
    w_g = (1-r)/d_G for g != I.

For lambda Delta>0 it has Choi rank d_G. Suppose a physical controller/environment is initially pure, has dimension D, receives no fresh systems or randomness, and is never reset. If it claims to realize the full Markov PROCESS for N such intervals under arbitrary intermediate interventions, apply the following legitimate tester: feed one half of a fresh maximally entangled pair into each interval and swap the output into an external store. Exact Markov behavior makes the stored state the tensor product of N normalized Choi states. Its rank is d_G^N and its entropy is N H(w).

The complete unitary evolution of controller plus tester starts pure; the rank of the stored reduced state is at most D. Therefore

    D >= d_G^N,  log_2 D >= m N,
    S(controller output) = N H_2(w) <= log_2 D.             (1)

For a mixed initial controller of rank R, rank is at most D R; alternatively count its purifier among the resources. External classical seeds, discarded outputs and reservoir modes are also resources. They cannot be called a finite closed controller and omitted from D.

This is a standard Stinespring-rank argument applied to the claimed refresh primitive. It proves an exact full-process freshness cost, NOT a hardware energy bound or a lower bound on the resources of the restricted fixed Astra circuit. Approximate processes can compress low-probability histories; no approximate lower bound is supplied here. A finite reservoir can mimic all single-time reduced dephasing channels while failing the Markov multi-time interface. The usual CNOT followed by a second CNOT illustrates why marginal dephasing calibration does not certify non-returning information.

At fixed finite temporal resolution, finite N requires finite but exponentially growing exact joint environment rank. Requiring the exact Markov process at every arbitrarily fine intervention grid requires unbounded fresh modes even on a fixed time interval. A continuous GKLS model normally represents that ideal reservoir; its finite coefficient lambda is not a finite total environment claim.

## 4. Detector support remains a separate gate

The full-footprint condition for a weak patch A and check group G is

    Pauli(A) intersect Centralizer(G) subset phase times S_code.

The measurement packet proves that expanding A to the complete detector data footprint D, while requiring every check to be supported in D and preserving this same zero-good-support rule against all Paulis on D, forces D to be a fixed pure stabilizer factor. Thus the new effect theorem cannot qualify arbitrary detector/ancilla faults by relabeling their whole support as the weak patch. A broader space-time support certificate or a separately qualified restricted fault family is still necessary.

## 5. Answer to the actual continuous-control question

Finite rate does remove the inflation B-to-epsilon and gives a rigorous simultaneous-Hamiltonian endpoint effect under the EXACT specified Markov randomizer. It does not remove the missing joint Choi directions, obtain the Markov primitive from finite/noisy controls, protect controller records, or close the detector-footprint support gap. The useful advance is a sharper receiving interface and a sharper target for a physical model; actual autonomous continuous shared-bath/control capability remains NOT_ESTABLISHED.
