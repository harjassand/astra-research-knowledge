## ASTRA — Coherent control keys generated after the quantum interaction

A new construction removes the need for a pre-generated private classical key tape, at the cost of protected quantum control registers.

Instead of choosing a classical Pauli key before a noisy quantum gate, prepare two independent flag qubits in \\(|+\rangle\\), apply the corresponding Pauli frame coherently, and leave the flags unmeasured while the gate interacts with its hidden quantum bath.

After the physical interaction has finished, measure the flags and apply the matching output correction.

The completed operation is exactly

\\[ \boxed{ \mathcal T(\mathcal E) =\frac14\sum\_{P\in\\{I,X,Y,Z\\}} \operatorname{Ad}\_{P}\circ\mathcal E\circ\operatorname{Ad}\_{P} =\sum_s\operatorname{Ad}\_{P_s}\otimes\Phi_s, } \\]

where every \\(\Phi_s\\) is completely positive and retains the actual quantum bath.

Importantly, the bath may infer information about the chosen frame by interacting with the data qubit. That does not invalidate the theorem. The crucial condition is that the bath cannot directly access the flag registers or receive separate key-dependent control signals.

### Executed checks

I implemented the coherent flag circuit, rather than simply averaging four assumed classical channels.

| Test                                                    | Numerical residual       |
| ------------------------------------------------------- | ------------------------ |
| Physical quantum flags versus classical Pauli averaging | \\(1.44\times10^{-17}\\) |
| Complete positive fault-path representation             | \\(5.56\times10^{-17}\\) |
| Sacrificial test's full bath-update instrument          | \\(5.89\times10^{-17}\\) |
| Two adaptive calls reusing a noncommuting bath          | \\(2.83\times10^{-17}\\) |

The two-call calculation also includes an intermediate bath measurement whose outcome selects the next quantum interaction.

These results establish identities within the tested mathematical model. They are not evidence that the required isolated quantum flags are available in hardware.

### Extension to the non-Clifford \\(T\\) gate

The construction also works for a noisy \\(T\\) gate, without requiring quantum-controlled non-Clifford corrections.

Apply the coherently controlled input Pauli \\(P\\), let the noisy \\(T\\) operation finish, measure the flag, and apply the outcome-dependent Clifford correction

\\[ Q_P=TPT^\dagger. \\]

This produces exact positive fault branches of the form

\\[ \boxed{ \mathcal S_T=\sum_s\operatorname{Ad}\_{TP_s}\otimes\Phi_s. } \\]

The error \\(P_s\\) is placed before the intended \\(T\\) gate, which is important for subsequent fault tracking.

I checked the complete channel on all 64 matrix units of a logical-input–bath–reference system, including separately retained internal records. The largest residual was \\(1.11\times10^{-16}\\). Two successive noisy \\(T\\) calls sharing one quantum bath agreed with the positive-path construction to trace distance \\(1.20\times10^{-16}\\).

The sacrificial verifier uses three input Pauli bases and their Clifford-rotated output bases. Its complete bath-update instrument also passed at \\(1.11\times10^{-16}\\).

This supplies an alternative to the whole-run classical key tape for the conditional Clifford+\\(T\\) service. It does not remove the need for reliable controlled input Paulis, output Clifford corrections or flag isolation.

### Noise-protected implementation

The two quantum control flags can be encoded in four physical spins, two per flag, using the protected states \\(|01\rangle\\) and \\(|10\rangle\\).

This allows the same two data-controlled Pauli gates while eliminating arbitrary collective flag dephasing within the protected subspace.

| Physical disturbance                         | Executed result                                             |
| -------------------------------------------- | ----------------------------------------------------------- |
| Collective bath coupling strength 230        | Channel residual \\(1.60\times10^{-14}\\)                   |
| Differential coupling 0.12                   | Full-memory error 0.05894                                   |
| Same differential coupling                   | Proven error ceiling 0.0924                                 |
| Out-of-code leakage, integrated strength 0.2 | Undetected wrong-output probability \\(9.93\times10^{-5}\\) |
| Corresponding clean-task error ceiling       | \\(4.00\times10^{-4}\\)                                     |

The fourth-order leakage result applies when the target operation is otherwise correct and the disturbance couples only out of the protected code. It cannot be extended automatically to arbitrary pre-existing logical faults.

### Adaptive quantum service

64 independent simulated trajectories · 99% all-prefix confidence · 90-fault budget

# 579.5

Mean completed quantum uses

# 464.2

Mean sacrificial tests

# 32.0

Mean hidden virtual faults

# 86.8

Mean received fault upper bound

No all-prefix violations were observed. The controller uses only received records, while the simulated bath is never reset. The formal confidence guarantee follows from the operator supermartingale, not from the observed violation frequency.

### Decisive limits

A single quantum flag cannot universally replace the two-flag construction. The Pauli-character matrix has full rank four, forcing four uniformly weighted frames when arbitrary single-qubit coherent errors must be separated. Reusing a quantum frame across two coherent calls also failed, producing trace-distance discrepancy 0.25.

Most importantly, exact current-output correctness does not imply the full quantum-memory instrument is correct. A leaked key can leave the current output unchanged while corrupting bath correlations needed for subsequent uses.

## Preserved research

Complete technical derivation

Full-memory theorems, \\(T\\)-gate construction, role-hiding proof, adaptive confidence bounds, DFS implementation and counterexamples

Reproducible research archive

Six executed Python studies, six numerical result files, validation log, dependencies and checksums

All six studies passed the consolidated validation run. The ZIP integrity check also passed.

Scientific assessment: The useful advance is an alternative physical interface for Astra's memory-bearing Clifford+\\(T\\) service, replacing a pre-generated private classical frame tape with short-lived, isolated quantum flags. Deferred measurement, randomized compiling and decoherence-free encoding are established prior science, so originality is not established.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.sciencedirect.com\&sz=32)

ScienceDirect

+2



A conventional controller with trustworthy private classical randomness remains simpler where that hardware is available.

The highest-leverage unresolved problem is now physically certifying the quantum flag's isolation throughout the controlled preframe, uncontrolled interaction, output correction and record retirement. The executed counterexamples show why neither uniformly random measurement outcomes nor present-output tomography suffices. A complete-instrument experiment with a retained spectator memory is the decisive next test.