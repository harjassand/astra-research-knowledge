# Physical permutation orbit: complete n=6 subcode instance
2026-10-29. Author: review_actual_logical_comparator. New construction; independent receiving review requested separately. The all-n proof is owned by derive_matching_survival_bound and is not replaced by these floating checks.

## What changes
The fixed logical subcode Q of dimension4 sits in the dimension5 six-qubit singlet sector P. Encode into Q, apply a uniformly random physical permutation of the six qubits, execute the source, undo that same permutation, then apply the complete Q decoder. The source does not receive the current permutation through an extra setting/control side channel. Retire the random permutation after undoing it. No logical Pauli pad is used in this instance.

Because the singlet representation of S6 occurs once in the full64-dimensional physical output, permutation averaging can remove coherent scalar/residual Kraus cross terms even when the source leaks out of the singlet sector. This is stronger than merely averaging a logical error score. The implementation tests the claimed exact joint decomposition
T_orbit = identity_P tensor B_good + T_bad,
where T_bad is CP and T_bad*I = I_P tensor H_bad. Restriction to Q and complete CPTP decoding preserve the good branch. Bad probability is a memory-only effect, not dependent on the logical payload, including initially correlated logical-memory input. The all-n proof supplies the matching-survival bound Tr(H_bad rho_M) <= C_full q with C_full=(n+2)/(n-1); at n6 it is8/5, without the fixed-subcode factor d/K.

## Exact counterexample shows why the orbit is necessary
Let |M0> be one of the15 product-of-three-singlets matching states. Choose Q to contain |M0>, and use the physical reflection U=I-2|M0><M0| with trivial bath coupling. Q has dimension4, so fixed-Q entanglement fidelity is |(4-2)/4|²=1/4 and Bell loss3/4.

For a uniformly sampled matching, squared overlap with M0 is1 for the identical matching,1/4 for the six matchings sharing one pair, and1/16 for the remaining eight matchings. Therefore E[p]=1/5 and E[p²]=3/32. Survival under the reflection is(1-2p)², giving q=4(1/5-3/32)=17/40. Thus C_full q=(8/5)(17/40)=17/25, which is strictly below3/4. Simply deleting d/K from the old fixed-subcode bound is false.

The full-P scalar is Tr_P(U)/5=3/5, so orbit bad probability is1-(3/5)²=16/25, below17/25. For the explicit Gram–Schmidt Q and logical-zero reset used in this program, the actual orbit-averaged Q Bell loss, including reset of Q-complement output, is99/160=0.61875. This precise reset-completed value need not hold for every Q/reset orientation. The program evaluates Fe for each orbit vector w with s=||Q*w||² as (1-2s/K)²+4(1-s)|w0|²/K². A logical Pauli twirl would leave the old fixed-Q Bell loss3/4 unchanged; the new physical permutation orbit is a different operation. The new randomized-code orbit changes the operation; it does not repair the invalid fixed-Q claim by relabelling its constants.

## Implemented tests
orbit_instance.py constructs all15 matching vectors, an orthonormal five-dimensional singlet basis, all720 physical permutations as actual64-coordinate index rearrangements and their exact restricted5x5 representations. It retains the complete64-dimensional output. The source-memory register has dimension2. The Q decoder consists of Q* plus a separate reset Kraus for every vector orthogonal to Q, preserving and tracing genuine leakage/bath correlations rather than dropping leakage.

Three source families are executed:
1. The exact matching-state reflection counterexample.
2. A seeded joint physical-system/memory unitary with nonzero leakage.
3. The same unitary followed by physical amplitude damping, giving a nonunital two-Kraus source with nonzero leakage.

For each, the program checks source TP, averages the actual conjugated Kraus matrices, constructs CP residual branches, tests the bad effect I_P tensor H_bad, applies the full channel and both split branches to a correlated Q-memory input, then checks the complete decoded split. Maximum recorded residual is below1e-14. Coherent and nonunital fixtures have physical singlet leakage approximately0.28975 and0.42337 respectively. These are numerical matrix checks, not interval-certified equalities or physical measurements. They accompany the exact representation proof, rather than establish its generality.

## Required controls and comparison scope
A uniform physical permutation can be sampled by Fisher-Yates with exact bounded integer sampling. Naive rejection from unbiased bits has expected finite cost but no finite worst-case bit cap; a finite cap and failure event must be charged if required. Merely taking random fixed-width integers modulo an uneven range is biased.

With arbitrary pairwise SWAP access, each permutation needs at most n-1 SWAPs, hence pre/post permutation together at most2(n-1), or at most6(n-1) CNOTs using standard three-CNOT SWAPs. At n6 these upper bounds are10 SWAPs or30 CNOTs. On a line, adjacent inversion sorting can require n(n-1)/2 SWAPs per direction, hence at most n(n-1) total and an average n(n-1)/2 total for uniform permutations. These are ideal gate counts; routing time, calibration and storage are not free. Pad variable-duration controls if the source can otherwise infer the current permutation or role. Noise during these operations must either be included in a proved complete boundary or paid as an implementation-error budget.

This construction still requires the fixed Q encoder and its CPTP decoder on service calls. It does not discover a good frame or guarantee low bad probability under arbitrary noise. It improves the certification interface and removes a subcode coefficient under the stated extra randomized physical operation. It does not establish a gate-cost advantage over full logical two-design testing or a hardware threshold.

The exact good/bad decomposition is after forgetting the private random permutation. Retaining it in an output register, leaking it during the source call, or later releasing it to a continuing source is not covered by the same averaged joint-channel statement. Source may have arbitrary retained quantum memory within the declared role-independent source port; controls and temporary key storage remain trusted.

## Run
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 orbit_instance.py
This regenerates orbit_instance.json and prints the same data. Python3.12.14, NumPy2.3.5 and SciPy1.17.0 were used. No inherited research modules or hidden source arrays are imported.
