# Uniform 3-CNF compilation and vanishing density error
2026-10-29. Root addendum to COUNTING_CONSTRUCTION_DRAFT.md; independent receiving in progress.

The fixed-accuracy proof need not use growing-width truth tables. Let each local numerator have real/imaginary integer parts bounded by W and let B_w=ceil(log2(W+1)). A bounded-fanin Boolean circuit takes the fixed 2k wire bits and component bit, looks up the B_w magnitude bits and sign, compares an unrestricted B_w-bit selector z with that magnitude, and adds the selected phase to a two-bit running accumulator. Each output magnitude bit is a truth table on only 2k+1 bits and takes O_k(1) Boolean gates. Binary comparison takes O(B_w) gates, phase addition O(1). Hence each physical gate costs O_k(B_w) Boolean inputs/auxiliaries/gates.

Use one Tseitin variable for each Boolean gate output and its exact equivalence clauses, not one-way implication clauses. Pin every constant and final constraint. Each satisfying free path/component/selector assignment has exactly ONE auxiliary extension. All clauses have width at most3, with O(1) clauses per Boolean gate. Therefore N=O_k(n+mr B_w) variables and O_k(N) clauses, uniformly even when precision and r vary. The density constant depends on fixed locality k, not B_w,r or epsilon. This is important because the sharp external sparse #3SAT bound has constants depending on clause density.

## Explicit ground-density schedule
Fix k,Delta,J. Remove scalar terms and track their known energy shift. Let eps in(0,1], beta=4/eps (qubits). Set J0=J+1, q<=k(Delta-1)+1 and M=sum_{l=1}^q k^l. Choose a fixed rational constant C satisfying
 C>=4J0 M and C^2>=64 e Delta J0^3 M^2/3.
A rational upper bound e<3 suffices to choose C without an exact transcendental comparison. Put r=ceil(C eps^(-3/2)). Integer comparisons using rational eps determine this ceiling without a real oracle. Then delta=beta/r=Theta(sqrt eps), with constants depending only on the fixed local parameters.

Choose local rational positive gates so that ||G_e-exp(-delta h_e/2)||<=eta, where eta<=delta exp(-delta J/2) eps/(16Delta). A certified rational lower bound on exp(-delta J/2) suffices. The resulting nearby Hamiltonian changes free-energy density by at most eps/4. The symmetric physics bound makes the remaining Trotter free-energy error at most eps/4. Gate entries require B_w=O(log(1/eps)) bits because delta=Theta(sqrt eps), all original local norms are bounded, and the desired eta is Theta(eps^(3/2)). Polynomial bit evaluation uses rational enclosures; rounded matrices are Hermitian and positive definite.

Thermal entropy gives E0/n in[f_beta,f_beta+ln2/beta], with ln2/beta<eps/4. Evaluate the exact positive rational product trace logarithm to a further eps/8 free-energy-density error and return its corresponding energy interval or midpoint. The accumulated interval gives additive eps ground-energy-density accuracy with slack.

The resulting sparse3-CNF has
 N=O(n eps^(-3/2) log(2/eps)).
Its source-input and construction bit length is polynomial in the supplied Hamiltonian bit length, n,1/eps. Conditional on the external sparse exact-counting theorem, total time is
 poly(input length,n,1/eps) * 2^{O(N/sqrt(log(N+2)))}
and polynomial space in those parameters.

In particular define ell=ceil(log2(n+2)), t=ceil(ell^(1/4)) by integer fourth-power comparisons, and eps_n=1/t. Then
 N=O(n (log n)^(3/8) loglog n),
 time=poly(input length,n)*2^{O(n loglog n/(log n)^(1/8))}.
This is subexponential in n for polynomial/subexponential input length and yields error O((log n)^(-1/4)) in ground-energy density. More generally eps=(log n)^(-a) works for every fixed a<1/3, with computable rational rounding. The endpoint a=1/3 does NOT follow from these bounds.

## Limits and comparison
The accuracy vanishes only logarithmically. This is not inverse-polynomial TOTAL-energy accuracy, not a polynomial-time algorithm, not quantum-state preparation, and not an assertion that finite-size implementations beat numerical many-body methods. The released sparse counting theorem is an imported premise; its full solver has not been executed here. A stronger baseline than exact diagonalization is Le Gall, ESA2025/arXiv2410.21833v2, which gives unguided density-scale ground-energy approximation in randomized2^{O(n)} time and polynomial space. Full historical novelty remains unchecked.
