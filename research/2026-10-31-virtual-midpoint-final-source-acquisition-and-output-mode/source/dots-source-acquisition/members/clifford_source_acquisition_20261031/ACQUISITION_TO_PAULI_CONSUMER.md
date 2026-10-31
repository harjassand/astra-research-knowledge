# Receiving a known Clifford source program into reusable non-Clifford simulation

31 October 2026. Specification and proof of the acquisition-to-consumer interface. This does not alter the frozen pure-return compiler. The source finder is a separately reviewed research prototype; its regression tests and code receipt are not a full simulation implementation. No source learning, practical advantage, or priority claim is made.

## 1. Input, admission and reusable output

The executable frontend currently accepts n>=1 source qubits, e>=0 fresh |0> environment qubits, and an explicit gate list over H, S, S-dagger, X, Z, CX and SWAP. It retains the first n output wires and discards the environment. Other specified pure stabilizer ancillary preparations and wire conventions must first be compiled into this gate/wire interface, with their gates charged. Arbitrary stochastic mixtures, postselection and non-Clifford source programs are not admitted merely because their components are individually familiar.

For the actual supplied program U, let W be its acquired Stinespring isometry. Run the exact Pauli-image filtration and purity check, and verify its certificate against the program digest. Only status `accepted_pure_return` enters this consumer. The mathematical admission proof is `INDEPENDENT_ACQUISITION_PROOF.md`, SHA256 997140547b36e1edfe75e012d5da22306b733ee8e1b1113626b003cfa1867bae. It proves that the output certificate supplies:

* an integer 1<=m<=2n with Phi^m=Reset_psi on every input, including reference correlations;
* n independent signed stabilizers of the pure fixed state psi;
* an explicit Clifford preparation V_psi and its inverse;
* the actual W circuit, its unitary extension, controls and inverse;
* a phase-consistent preparation of c satisfying W psi=c tensor psi;
* a circuit for reflecting about P=|psi><psi|, using V_psi, the all-zero reflection and V_psi-dagger.

The image iteration is M_(j+1)=F(M_j intersect S), starting with all binary Pauli labels. A nonzero plateau rejects eventual forgetting; zero image with mixed output rejects the pure-return interface. Neither rejection says that a general channel is unstable or unsimulable. Exact signed tableau arithmetic, rather than dense state enumeration, supplies the accepted data in polynomial time.

The c preparation is important: prepare psi on clean source work, apply the original W with its original ancillary preparation, then V_psi-dagger on the source output. The source work returns to |0>, leaving the actual c, with the phase inherited from U. A separately synthesized stabilizer ray for c is not substituted. Reusing the same acquired phase-safe circuit makes A=(<c| tensor I)W fix psi exactly, and gives A^m Q=0, Q=I-P.

This package can be cached once and reused across future couplings without repeating acquisition. Changing the source program invalidates its digest and requires verification again. No square-root stationary-distribution oracle or exponential Kraus table is acquired or needed.

## 2. Exact sparse-Pauli centering is an acquired operation

Suppose a future user supplies an explicit polynomial-length Hermitian term list

    K = sum_(j=1)^J theta_j S_j tensor P_j,

where theta_j are real exactly represented rationals, S_j are Hermitian Pauli strings on the system, and P_j are Hermitian Pauli strings on the source. More general supplied system operators can be handled with their real encodings and normalizations, but this specification uses Pauli strings for a fully explicit consumer.

Precompute Gaussian-elimination membership data for the unsigned labels of psi's n signed stabilizers g_1,...,g_n. For each P_j:

1. If its label is not in their binary span, set mu_j=0. A pure-state stabilizer group is maximal isotropic, so some stabilizer anticommutes with P_j; conjugation by that stabilizer proves its expectation vanishes.
2. Otherwise solve for the generator product G with that label. Multiply the SIGNED Paulis, keeping phases modulo 4, and set mu_j=+1 if P_j=G and mu_j=-1 if P_j=-G.

Thus mu_j=<psi|P_j|psi> is exactly 0 or +/-1. Binary membership alone does not determine its sign. In the executable convention i^p X^x Z^z, multiplication is

    (p,x,z)(q,u,v)=(p+q+2 z dot u mod 4, x xor u, z xor v).

Since the input Paulis are Hermitian, the final equal-label phase difference is 0 or 2. After polynomial preprocessing, each new term requires polynomial(n) bit operations; a simple elimination implementation uses O(n^2) per term. Identity strings and negative signed generators are included.

Compute and combine equal system strings in

    Hbar = sum_j theta_j mu_j S_j,
    Kc = K - Hbar tensor I_source.

Then P Kc P=0 exactly, where P acts on the source. No Monte Carlo estimation, state tomography or assumption about a future task distribution is involved. The cached membership data remains useful for new supplied Pauli lists. This is ordinary stabilizer expectation evaluation used to discharge a real compiler input promise.

## 3. Actual block encodings and the nonzero mean cost

Let beta=sum_j |theta_j|. A direct finite LCU gives K normalization beta. Its SELECT applies the supplied system/source Pauli strings and the coefficient sign; coefficient-state preparation is synthesized from the explicit J-entry list. A conservative gate implementation scans that list, polynomial in J, the register lengths and precision; no free QRAM is assumed.

For the centered operator use the original J terms plus the nonzero subtraction terms. A known normalization is

    alpha_c = sum_j |theta_j|(1+|mu_j|) <= 2 beta.

For Hbar a known normalization is alpha_mean<=sum_j |theta_j mu_j|<=beta; combining duplicate strings can improve it. Zero lists are handled as exact zero operations. These are actual acquired upper bounds, not an oracle for the exact operator norm. Controlled SELECT, PREPARE, their inverses and all real synthesis costs are included. Expectations are exact even when the coefficient rotations are numerically synthesized.

Crucially the original generator is IDENTICALLY

    -i[Hsys + sqrt(lambda) Hbar + sqrt(lambda) Kc, .]
       + lambda(Phi-I).

The receiving compiler uses H0'=Hsys+sqrt(lambda)Hbar and the centered Kc. It must not erase Hbar, average it away, or pretend the source rate is the only rate-dependent resource. The ordinary system-action bound includes

    T(alpha_Hsys + sqrt(lambda) alpha_mean).

Consequently a nonzero mean can destroy an overall polylogarithmic-rate bound even though the source overhead remains logarithmic. A separately proved fast implementation of this system term may improve its cost; it is not granted here. A scalar identity part is the sole trivial exception: its commutator vanishes, so it may be removed exactly. For general noncommuting mean terms, neither a change of frame nor a cheap phase oracle is implicit.

Use the nominal exact centered operator in the theorem. If its implemented block differs by eta, the physical Hamiltonian discrepancy is at most sqrt(lambda) eta; allocating eta=O(epsilon/[T sqrt(lambda)]) prices its channel error by the ordinary Duhamel bound. Thus exact centering is not falsely inferred from rounded rotations. Coefficient arithmetic, including sqrt(lambda), gains the corresponding logarithmic precision bits. Lambda=0 and T=0 use the previously bound degenerate branches.

## 4. Full receiving statement and its limits

With a verified positive frontend certificate, the finite Pauli list, supplied Hsys access, target time/error and p prescribed instruments, all input operations of the accepted pure-return compiler are acquired. Invoke its arbitrary-source-input addendum for arbitrary joint source/system/reference input, retain the source between segments, and charge each supplied instrument's own implementation separately. The error is the accepted uniform joint-channel/controlled-process error, with private simulator emission/time records. No normalization of a postselected state is used.

The reusable source-acquisition cost is polynomial in n, e and raw gate-list length. Per future term-list acquisition is polynomial in J, n, system register length and coefficient bits. Execution costs are those of the accepted compiler with m<=2n, acquired b=alpha_c (or a separately certified accessible tighter upper bound), B=b^2 T and the actual H0' action above; they include the real W/c/reflection/LCU circuit costs. This is a resource substitution, not a claim that the complete quantum compiler has been implemented by the certificate-finder Python program.

Arbitrary future non-Clifford dynamics are allowed only through their acquired coupling/operation interface. Continuous Pauli Hamiltonian rotations with generic coefficients are already non-Clifford; accepting a Clifford source does not make the entire driven evolution a stabilizer circuit. Conversely this does not prove classical hardness or superiority over an equally retaining conventional compiler.

A succinct arbitrary Boolean diagonal operator is not a sparse Pauli list. For psi=|+>^n and B_f=diag_h((-1)^f(h)), its exact mean is 1-2 #f/2^n. Computing every such mean from an arbitrary Boolean program would compute its satisfying-assignment count. This source frontend does not supply that operation. Expanding B_f into exponentially many Paulis is not polynomial acquisition. A separately refreshed fair sign can center a DIFFERENT physical model; it does not silently simulate the original noncentered model.

The addendum permits arbitrary prescribed quantum source instruments as a quantum task. It does not turn them into classical-source observations. Any classical-source interpretation additionally needs the separately verified outcome-retaining diagonal-algebra condition; public sparse source-label snapshots are different from disclosure of the simulator's artificial emission path.

## 5. Primary comparison and scientific meaning

[Aaronson and Gottesman, Improved Simulation of Stabilizer Circuits](https://arxiv.org/abs/quant-ph/0406196), already supplies efficient stabilizer simulation, canonical circuit forms, inner products and mixed-state extensions. Signed Pauli expectation evaluation and Clifford state preparation are standard consequences of that machinery, not new learning operations.

[Yashin et al., Further improvements to stabilizer simulation theory](https://arxiv.org/abs/2511.05478), develops efficient quadratic-form representations and composition for stabilizer operations/Clifford channels, distinguishing CSS simplifications from general frames. It is a direct ordinary representation comparator.

[Looi and Griffiths, Tripartite Entanglement in Qudit Stabilizer States and Application in Quantum Error Correction](https://arxiv.org/abs/1107.1761), characterizes a class of stabilizer-code channels through tripartite structure. Only its accessible primary abstract is used here; no restricted publisher/full-text access was attempted. Its existence rules out presenting channel normal forms as an unexplored idea; its abstract alone does not establish every implementation detail of this exact frontend.

The useful conjunction is that raw known-program analysis now emits a checkable return certificate and phase-consistent executable inputs, and those cached inputs also compute sparse-Pauli centering for later consumers. It removes supplied promises within a precisely admitted class. It is not raw-data source learning, unrestricted latent-representation discovery, or a demonstrated advantage over a strong compiler using the same retained tableau and program.

## 6. Binding provenance

Bound repaired frontend: acquire_clifford_source.py SHA256 d838ceb019302861375671da683467ab82514cd45e6eff6e86a5990e8664b1f0. Its separate executable receipt is EXECUTABLE_ACQUISITION_INDEPENDENT_REVIEW.md SHA256 fe91016db2174e5d18576dc66aa22b5c86dbbc6623c0ec6268c1ffbcffe73fdf. That audit found and repaired a forged-persistence certificate defect in the earlier ca74 version: a zero-only list was incorrectly treated as a nonzero space. Canonical-basis validation now rejects it, and the original failure is preserved. This consumer binds only the repaired code; it does not replace the audit or assert that all future edits preserve admission.

Accepted execution base: pure_return_source_20261031/PURE_RETURN_FULL_FINITE_BIT_RECEIVING.md SHA256 1a097458af52e4b89746b2f5e38e8ba4ea9f8a835db731daef39b8e9ea71e032. Arbitrary-input addendum SHA256 39cfffcb2c38bf13da46a380760a994787caada7ecc99f43cc93e6953fc95069. Their existing receipts and restrictions remain binding.
