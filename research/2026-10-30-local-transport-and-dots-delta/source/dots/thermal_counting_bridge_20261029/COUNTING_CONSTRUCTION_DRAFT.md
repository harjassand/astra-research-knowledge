# Candidate: subexponential-volume thermodynamics without a sign restriction
2026-10-29. Root working construction, independent review pending. Conditional on the cited fixed-width exact-counting theorem and completion of the uniform thermal product-formula bridge. No historical novelty or practical-runtime claim.

## Target and why this is not another recovery extension
Input: an explicitly given bounded-degree k-local Hamiltonian H=sum_e h_e on n qubits, with fixed k, each qubit in at most Delta terms, and ||h_e||<=J for fixed J. Terms are rational-complex Hermitian matrices. Graphs need not have geometric separators; bounded-degree expanders are allowed. For fixed beta>0 and eps>0, compute free-energy density f=-(beta*n)^-1 log Tr exp(-beta H) within eps in 2^{o(n)} time and polynomial space. No stoquasticity, commuting terms, spectral gap, low entanglement, supplied Gibbs sampler, or acquired environment inverse is assumed.

A sufficiently large beta=O(1/eps) would also approximate ground-energy DENSITY to additive eps. This is not inverse-polynomial total-energy accuracy, not a general QMA collapse, not Gibbs-state preparation, and not a practical polynomial-time algorithm. The purpose is to change the generic many-body computational boundary; constants in eps and beta may be enormous.

## Thermal bridge being separately checked
Color the term-overlap graph into c<=k(Delta-1)+1 matchings. For delta=beta/r, Q(delta) is the ordered product of all local exp(-delta h_e/2), grouped in these c disjoint layers. P(delta)=Q(delta)^dagger Q(delta)>0. The needed statement is
  ||log P(delta)+delta H|| <= C n delta^2,
with C depending only on k,Delta,J and a fixed upper bound on delta, not n. Then
  |log Tr P(beta/r)^r - log Tr exp(-beta H)| <= C n beta^2/r.
A proposed proof uses R=Q exp(delta H/2): R'R^-1=Q'Q^-1+(1/2)QHQ^-1. This contains only finite-depth local conjugations. Its value at0 is0; bounded-degree support expansion should bound its norm by C n delta. Singular-value Gronwall gives a relative Loewner comparison, and operator monotonicity of log gives the stated estimate. The independent worker owns checking constants and all noncommutative steps. Ordinary additive operator-norm Trotter error alone would NOT suffice.

## Remove precision-dependent path width by changing the nearby Hamiltonian
Do not approximate every gate of a long tensor contraction to error1/n. Instead round LOCAL positive exponentials to exact rational matrices, and interpret them as exact exponentials of a nearby Hamiltonian.

Let A_e=exp(-delta h_e/2), with lambda_min(A_e)>=a=exp(-delta J/2). Round its real/imaginary entries Hermitian-symmetrically to a common dyadic grid, producing G_e with ||G_e-A_e||<=eta<=a/2. Define h'_e=-(2/delta)log G_e. Then G_e>0 and the operator-log integral yields
  ||h'_e-h_e|| <= 4eta/(delta a).
Choose eta<=delta*a*eps/(16Delta). Since m<=nDelta, ||H'-H||<=n eps/4. Ordered eigenvalue comparison implies |f(H')-f(H)|<=eps/4, with no gap or phase assumption. Also ||h'_e||<=J+1 for eps<=1.

The needed grid bit depth B depends only on beta,r,eps,k,Delta,J, not n. Matrix dimension is fixed; certified local exponentiation and rounding cost polynomial in the supplied bit length, with constants depending on these fixed parameters. The matrices h'_e need not be rational or explicitly diagonalized: exact rational G_e define them mathematically. Use the thermal bridge with norm bound J+1, and choose r so its contribution to free-energy error is <=eps/4.

## Exact signed tensor sum is two fixed-width #SAT counts
The rational positive matrix product P'=Q_G^dagger Q_G, raised to r, contains M=2mr=O(n) local gates. Its trace has a path expansion using at most n+kM binary wire variables. The final wire of each qubit is identified with its initial wire to close the trace. Every local matrix entry has form (u+iv)/2^B, with integer |u|,|v|<=W for a fixed W independent of n.

For each gate introduce one component bit choosing u or v, and a constant-width selector z in[0,2^ceil(log2(W+1))). Impose z<the absolute value of the selected integer. This supplies exactly its magnitude as multiplicity, including zero weights. Its phase is one of {1,i,-1,-i}. A two-bit running phase register adds these phases modulo4. All transitions are deterministic, so they introduce no extra multiplicity.

A fixed local truth table enforces each gate's allowed wire/component/selector/phase transition. Its scope is constant (depending on k,B,W), so listing forbidden patterns gives a constant-width CNF with O(n) variables and clauses. Initial phase is0. Make two formulas selecting final phase0 and phase2, and count them exactly as C0,C2. Then
  Tr[(Q_G^dagger Q_G)^r]=(C0-C2)/2^(BM).
The imaginary part is exactly zero, and C0-C2 is strictly positive because the matrix is positive definite. No Monte Carlo average-sign assumption or division by an estimated tiny quantity occurs. Counts have O(n) bits; their subtraction is exact. Computing the logarithm of this positive rational to additive O(beta*n*eps) costs polynomial bit work.

Apply the fixed-width #SAT theorem (OpenAI, The Exponential Time Hypothesis is False, October25 2026, governing main_full_version.tex; acquired blob f7af85e623b58e0ca9f4b9416916d442defa963a). For fixed physical/accuracy parameters, N=O(n) Boolean variables and constant clause width give poly(input length)*2^{o(n)} time and polynomial space. This is a conditional use of that released counting theorem, not a new proof or independent acceptance of it.

## Comparators and unclosed obligations
Geometric block cutting already gives easy density approximation on families with small separators; it is not the claimed target. Generic exact diagonalization remains exp(n). A direct circuit reduction with a variable for every high-precision gate can lose the subexponential bound; the nearby-log-Hamiltonian argument is intended to avoid that mistake. Strong primary quantum partition-function algorithms and all current counting consequences still need a direct comparison before novelty is asserted.

Remaining: full review of the volume-uniform thermal estimate; actual exact signed-count compiler checks; explicit finite rounding constants; comparison against known thermodynamic-density algorithms. No executable full asymptotic #SAT solver has been supplied by this note, and no benchmark superiority is claimed.
