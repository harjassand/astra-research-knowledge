# Native quantum cancellation investigation: closed without an invention

## Outcome

No new tractable many-body simulation class was obtained. Three independently proposed mechanisms were screened before literature checking (`00_mechanisms_before_search.md`). The most concrete was developed through an exact construction and a decisive failure test. The alternatives also failed their native-access gates. No novelty is claimed for the identities, hardness embedding, or elementary counterexamples below.

The intended capability was classical computation of relative-error thermal partition functions or additive-error bounded-support thermal observables from the actual bounded-degree, fixed-locality Pauli coefficients, with polynomial cost in physical system size, coefficient bit length, inverse temperature, and inverse error. No decomposition, fast sampler, mixing oracle, rank certificate, or uncharged exponential preprocessing was allowed. This investigation does not establish the requested capability, even for a newly delimited useful class.

## 1. Selected mechanism: cancel complete ordering orbits before sampling

Write H = sum_i h_i P_i, and let A_ij be 1 when the Hermitian Pauli terms anticommute. For a multiplicity vector c, replace every word with those multiplicities by its exact signed sum S(c) times the canonically ordered product U(c) = product_i P_i^{c_i}. Appending the final letter gives the native recurrence

S(0)=1,
S(c)=sum_{i:c_i>0} (-1)^{sum_{j>i} A_ij c_j} S(c-e_i).

Hence H^m = sum_{|c|=m} (product_i h_i^{c_i}) S(c) U(c), exactly. The operation performs cancellation before absolute values or Monte Carlo. The hoped-for further step was to fuse local cancellation cells and thereby keep a polynomial number of effective sectors.

For a star with center A, mutually commuting leaves B_j, and {A,B_j}=0, put D=sum_j b_j B_j and R²=a²I+D². Then R² is central in that star algebra and

exp[-beta(aA+D)] = cosh(beta R) I - [sinh(beta R)/R](aA+D).

The ratio is interpreted by its continuous value at zero. Fixed-size stars are exactly resumable from their coefficients. This is elementary functional calculus, not a new algorithm by itself.

### Native cost that cannot be discarded

For one vector c, direct recurrence uses up to product_i(c_i+1) states; square-free c already permits 2^L states for L terms. S(c) has at most O(m log m) bits because its magnitude is bounded by the number of words. Coefficient rational arithmetic also has polynomial bit cost for polynomial order m after clearing denominators. The missing cost is the number of states, not unbounded-size scalar arithmetic.

The anticommutation graph does not determine the physical trace. One must also retain the full binary Pauli-product map and its phases: a canonical word contributes to the trace only when its physical product is scalar. These native linear relations can be found efficiently; summing all their weighted sectors cannot consequently be assumed easy. Exact disconnected cancellation components need not describe independent physical subsystems.

### Minimal decisive construction, with locality checked

Start with a simple cubic graph G on n vertices and m=3n/2 edges. Put one data qubit at each vertex and two ancillas a(e,s), s=+1,-1, at each edge e=(u,v). Define

H0 = sum_{e=(u,v)} sum_{s=±1} [X_a + s Z_a + Z_a Z_u - Z_a Z_v].

This is genuinely **2-local**; it uses Z_a(Z_u-Z_v), not the earlier exploratory 3-local term Z_a Z_u Z_v. All coefficients are ±1. There are N=n+2m=4n qubits and 8m Pauli terms. The physical interaction graph has degree 6 at data qubits and 2 at ancillas. For each ancilla, X_a anticommutes with its three mutually commuting Z-type terms. Different ancilla blocks commute. Thus the Pauli anticommutation graph is exactly 2m disjoint claws K_(1,3).

Every block can be summed perfectly. At fixed data assignment z, its eigenvalues are ±sqrt[1+(s+z_u-z_v)²]. Tracing the ancillas gives exactly

Z0(beta) = w0^m sum_z r^{cut_G(z)},
w0=4 cosh(beta sqrt(2))²,
r=cosh(beta sqrt(10))/cosh(beta sqrt(2)).

The residual sum is an antiferromagnetic Ising cut polynomial. Cubic MaxCut is NP-hard [Alimonti–Kann, 2000](https://www.sciencedirect.com/science/article/pii/S0304397598001583).

For completeness, the approximation target also fails: set beta=n+2, let C be the maximum cut and L=log r. Then r^C <= sum_z r^{cut(z)} <= 2^n r^C and L >= (n+2)(sqrt(10)-sqrt(2))-log 2. A 25%-relative partition estimate determines C by rounding log(Zestimate/w0^m)/L to the nearest integer. The worst-case rounding interval lies strictly inside (-1/2,1/2).

Adding Heta=H0-eta sum_u X_u, eta=1/[100n(n+2)], connects the entire anticommutation graph for connected G and breaks each individual conserved Z_u. The eigenvalue perturbation bound gives |log Zeta-log Z0| <= beta n eta=0.01, still safely within the same rounding margin. This does not assert that every symmetry disappears. Coefficients require O(log n) bits, beta is O(n), and log Z is O(n²); stable log-cosh arithmetic makes postprocessing polynomial-bit-cost.

**Exact conclusion:** perfect local Pauli cancellation and star resummation do not supply efficient global thermal access. A deterministic polynomial guarantee on this whole family implies P=NP; a bounded-error randomized guarantee implies NP is contained in BPP. Both H0 and Heta are locally gauge-stoquastic (conjugate by Z on every ancilla). This is deliberately an obstruction from residual sector aggregation, not an intrinsic sign-problem theorem, not a real-time simulation obstruction, and not a claim that every more restrictive new class is impossible.

## 2. Reflection fusion: positivity did not acquire sampling access

The exact identity Z=||exp(-beta H/2)||_F² supplies nonnegative global weights. It does not supply their values or conditional probabilities. The attempted additional operation was to fuse reflected local blocks and preserve positive, small boundary kernels.

The simplest proposed shortcut, a positive mixture of product positive operators across spatial pieces, fails on two spins. For H=XX+YY+ZZ, the normalized Gibbs state's partial transpose has minimum eigenvalue

[3-exp(4 beta)]/[2(exp(4 beta)+3)],

which is negative for beta>log(3)/4. No such positive product-operator decomposition exists there. This only rules out that shortcut; scalar path positivity is not equivalent to separability. Keeping entangled boundary operators instead leaves the boundary representation/contraction problem unresolved. No new closure rule or polynomial bound was found.

Thermal purification and imaginary-time thermal-state sampling already have established tensor-network realizations: [Verstraete–García-Ripoll–Cirac, 2004](https://arxiv.org/abs/cond-mat/0406426) and [White, 2009](https://arxiv.org/abs/0902.4475). Restating global positivity or assuming efficient preparation of the half-evolved states would not be the requested invention.

## 3. Adaptive gauge plus elimination: no new locality-preserving operation

A diagonal phase transformation preserves the product of hopping phases around each basis-state cycle. Three positive hopping amplitudes around a triangle therefore cannot all become negative by such a gauge. This triangle is natively realized in the one-excitation sector of a three-spin 2-local XY Hamiltonian. More general basis changes are not ruled out by this observation.

Exact elimination then produces the usual energy-dependent Feshbach–Schur term H_PQ(E-H_QQ)^(-1)H_QP. This is established machinery, not a new operation; see [Dusson–Sigal–Stamm, 2021](https://arxiv.org/abs/2105.02058). Local Pauli sparsity is not preserved: for E>sum_j lambda_j>0, the resolvent (E-sum_j lambda_j Z_j)^(-1) has all 2^q Z-subset coefficients strictly positive. The Neumann expansion proves this because the coefficient for subset S already has the positive contribution |S|! product_{j in S}(lambda_j)/E^{|S|+1}.

That example itself is easy and may be stored as a compact unevaluated expression. It is a failure of the proposed sparse local representation, not a hardness proof. Retaining a short inverse expression does not establish cheap observable evaluation; using separator contractions is ordinary variable elimination/tensor-network machinery. No different exact closure or controlled approximation beyond those frameworks was acquired.

## 4. Primary-literature boundary

The selected route overlaps existing free-mode algebra, rather than extending it:

- [Chapman–Flammia, 2020](https://quantum-journal.org/papers/q-2020-06-04-278/): graph characterization of generalized free-fermion mappings.
- [Elman–Chapman–Flammia, arXiv:2012.07857v2](https://arxiv.org/abs/2012.07857v2): even-hole/claw-free frustration-graph constructions and independent-set charges.
- [Chapman–Elman–Mann, arXiv:2305.15625](https://arxiv.org/abs/2305.15625): claw-free graphs with a simplicial clique and commuting cycle symmetries.
- [Fukai–Vona–Pozsgay, 2026](https://doi.org/10.21468/SciPostPhys.21.1.011): specially related couplings can give free fermions even with claws and even holes. Merely finding a claw is not evidence of an interacting computational breakthrough.
- [Troyer–Wiese, 2005](https://arxiv.org/abs/cond-mat/0408370): generic sign-problem hardness is a necessary boundary. It does not preclude genuinely new restricted classes, nor does sign freedom alone prove efficient sampling.

No claim is made that the gadget refutes these free-fermion constructions. Physical sector access, allowed representations, multiplicities, and computational output must be checked separately from formal algebraic solvability.

## Reproduction and stopping point

Run `OPENBLAS_NUM_THREADS=1 python verify_native_cancellation.py`.

Verified: 10 exact power-expansion orders; square-free star sums through 7 leaves; 12 direct dense thermal traces (largest dimension 512); 6 bounded-degree graph cut recoveries including adversarial 25% relative errors and the perturbation allowance; connected perturbed graph; three thermal partial-transpose checks; eight exact rational resolvent expansions; the triangle gauge obstruction. Maximum direct trace discrepancy in log Z was 1.07e-14. These tests check identities, not large-system speed or new physics.

All work used included tools and modest native CPU. No paid jobs, external uploads, publication, contact, or physical experiments occurred. The three mechanisms are closed as invention claims. A new attempt would need a genuinely different acquired operation, not a hidden sector-sum oracle, boundary-rank promise, sampler, or uncharged symbolic evaluation.
