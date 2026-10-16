# Independent audit of the coherent-fault bridge

## Verdict and scope

The proposed bridge is valid for ideal stabilizer-frame randomization of a fresh, frame-independent, memory-only local unitary, with the explicitly refined completed correction channel. The proof is on the entire physical input algebra, hence remains valid with an untouched reference. It does not establish the same claim for the unrefined completed channel, gate/frame-dependent noise, exposed frame records with later feedback, or an arbitrary persistent bath. The general persistent-bath theorem can be used downstream only after the independent rare-fault representation has actually been established in its required joint-channel scope.

## Definitions and covariance

Let S be an abelian stabilizer group, and let C(X)=sum_j Q_j Pi_j X Pi_j Q_j† be a CPTP completed correction, where the Pi_j form an orthogonal resolution of identity and are stabilizer functions, and every Q_j is Pauli. For any g in S, g commutes with Pi_j and commutes or anticommutes with Q_j. The signs cancel in each Kraus channel, so C Ad_g = Ad_g C on every operator.

If P is Hermitian Pauli and some g in S anticommutes with P, averaging the two framed implementations for U=exp(-i theta P) gives exactly cos²(theta) C + sin²(theta) Ad_P C. This conclusion uses a common U independent of the selected frame.

## Local groups and refinement

Fix a bounded patch A supporting U. Assume every Pauli supported in A that centralizes S belongs to S modulo phase (no local logical Pauli). Choose commuting Hermitian generators M_i for the subgroup of stabilizers supported in A. Their joint projectors R_r are supported in A; each generator has bounded support even if its expression as a product of original checks is long. This is an ideal direct measurement assumption, not a claim that these measurements already exist in the original hardware or jump list.

Let D(X)=sum_r R_r X R_r and C_ref=C D. Since each Q_j permutes the joint M eigenspaces and Pi_j commutes with them, D C_ref=C_ref. Refinement ordering before correction is therefore safe: the output eigenvalue need not equal the input eigenvalue, but it is definite for each Kraus Q_j Pi_j R_r.

For a geometrically local bounded-degree stabilizer presentation, the original checks intersecting A generate a group G whose union of supports lies in a bounded neighborhood of A. Its commutation characters distinguish exactly the global syndromes of Paulis supported in A: checks disjoint from A add no information. Uniform independent sampling of its generators produces uniform sampling of G, also with generator dependencies. Merely saying that individual checks are local is insufficient without bounded degree/number and bounded geometry.

## Full-input CP proof

Write the stabilizer-frame twirl of the unitary channel as T_U=sum_chi Ad_{U_chi}, where U_chi is the character-Fourier component of U under conjugation by G. These are operators supported in A. The trivial-character part U_0 is, by the no-local-logical assumption, a linear combination of the M subgroup, so U_0 R_r=a_r R_r on every physical eigensector, not just the code sector.

Let delta=||U-I||<1. Unitarity and character orthogonality give sum_chi U_chi† U_chi=I. If E denotes operator twirling, then

sum_(chi != 0) U_chi† U_chi = E((U-I)†(U-I)) - (U_0-I)†(U_0-I) <= delta² I.

Thus U_0†U_0 >= (1-delta²)I, and |a_r|² >= 1-delta² on every nonzero R_r. Consequently

T_U D - (1-delta²) D

has Kraus contributions sqrt(|a_r|²-1+delta²) R_r for the zero-character terms, and U_chi R_r for chi != 0. This is an explicit CP decomposition on the full physical input space. It proves Choi positivity without assuming that diagonal entries or a projected Choi block control the entire Choi matrix.

For q=delta²>0, define F_A=[T_U D-(1-q)D]/q. The difference has trace q Tr(X), so F_A is CPTP, supported in A. Since D C_ref=C_ref,

T_U C_ref=(1-q) C_ref+q F_A C_ref.

This also keeps the rare fault support at A, rather than enlarging it by the correction support. For q=0, U=I and there is no fault branch; no division by q is used. The same identity holds after tensoring an arbitrary reference identity channel.

## Exact failure without refinement

Use three qubits with stabilizers Z_1,Z_2 and logical qubit 3. Let C reset qubit 1 using Kraus P_(Z1,+) and X_1 P_(Z1,-), leaving qubits 2 and 3 unchanged. Let A={2} and U=exp(-i theta Z_2). A contains no logical Pauli. Stabilizer twirling leaves U unchanged, but C does not dephase Z_2.

Restrict inputs to qubit 1 fixed at zero and qubit 3 fixed. The purported positive difference reduces to Ad_U-lambda Id on qubit 2, where lambda=1-delta²>0. In the |00>,|11> Choi subspace its matrix is

[[1-lambda, exp(-2i theta)-lambda], [exp(2i theta)-lambda, 1-lambda]].

Its determinant is -4 lambda sin²(theta), strictly negative for nontrivial small theta. Thus CP domination fails exactly, despite locality, no local logical operators, covariance, and small operator-norm noise. Refinement D_(Z2) repairs this case. More generally a distinct rank-one unitary Choi operator cannot dominate any positive multiple of the identity-channel Choi operator.

## Ideal trajectory and process assumptions

For every definite Pauli orbit E V of the full code, each M_i has one eigenvalue independent of the logical state. Therefore D fixes E V X V† E†, including reference-entangled logical operators. The refined correction has the same action as the original completed correction on all such ideal/Pauli trajectories. It is nevertheless a different channel on general coherent physical inputs, and the coherent theorem must explicitly use it.

For exogenous independent Poisson proposals and fresh independent inaccessible frames, the exact channel mixture admits independent Bernoulli marks of probability q, yielding independent thinned proposal processes of rates (1-q)kappa and q kappa. Location-dependent fixed q is allowed with the corresponding rates; a common upper bound can be used by adding harmless fault branches. Each bad mark applies F_A after C_ref. If the classical argument treats good and bad correction streams separately, its nominal good correction rate is reduced to (1-q)kappa and this bookkeeping must be retained. One cannot assert that the bad stream is independent of the unsplit parent correction clock.

The random-unitary extension is safe for independently sampled memory-only U satisfying a uniform delta bound, after averaging the displayed CP identities. A general fresh CPTP channel needs its own proved CP decomposition or a stated random-unitary realization; being close to identity alone does not imply this quadratic rare-fault representation. Frame-dependent noise, feedback through stored random frame records, correlations among proposals, and unmodeled continuous bath interactions are not covered by the marginal channel calculation.

No historical novelty, experimental feasibility, noisy-frame robustness, or hardware claim is implied.

### Support/rate bookkeeping clarification

The local factor F_A has support A, but it is applied after the correction at every bad proposal. To fit an interface requiring a separate independent ideal-correction stream and a separate independent arbitrary-fault stream, use the good stream of rate (1-q)kappa and regard the entire bad channel F_A C_ref as the fault. Its support is A union the bounded correction patch. Alternatively, retaining the smaller fault support A requires a certificate that explicitly allows a bundled simultaneous correction at that bad proposal. Both routes are bounded-patch constructions, but they must not be conflated.
