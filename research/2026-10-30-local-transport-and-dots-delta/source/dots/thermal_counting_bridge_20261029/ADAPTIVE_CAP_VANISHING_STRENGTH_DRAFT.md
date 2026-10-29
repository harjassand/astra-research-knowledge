# Vanishing density accuracy under bounded local energy strength
2026-10-29. Root working bridge, separate review pending. It changes the adaptive degree cap and imports the separately checked local-strength product-formula estimate. It is NOT covered by the older fixed-accuracy sparsifier receipt.

## Objective
Remove the bounded GRAPH-degree premise from logarithmically vanishing energy-density approximation. Keep fixed locality k and a bounded actual per-site interaction-norm sum. The explicit rational envelope construction in LOCAL_STRENGTH_SPARSIFICATION_DRAFT.md makes this a checked input contract rather than a hidden norm oracle. Original terms may form a dense, nongeometric, noncommuting interaction graph. This is not arbitrary Coulomb chemistry without an extensive local-norm bound.

Use one internal rational parameter tau in(0,1]. Let L,g,q and J_s=L/q be as in the received sampling argument, with sparsification parameter tau. In the nontrivial branch L>tau*n/4, put
 lambda=q*g/L=g/J_s,
 D=ceil(9lambda)+ceil(log2(200g/tau)).
The logarithm ceiling is computed by rational comparisons; 200g/tau>50 here. This cap uses the ACTUAL lambda, not the older coarse upper bound Lambda. Every binomial-tail step of the older proof applies with lambda because mu_v<=lambda. The same >.97 success probability and ||Htilde-H||<=tau*n/2 remain valid.

## The weak sampled couplings cancel the large degree
Since q=ceil(512L^2/(tau^2 n)) and L>tau*n/4,
 tau^2/(528g)<=J_s<tau/128.
The upper ceiling factor528 is valid because 512L^2/(tau^2n)>32n>=32. Also g>tau/4. Therefore
 D J_s <=9g+J_s[log2(200g/tau)+2] <10g.
For an elementary bound, set x=tau/g<4. Then x log2(200/x)+2x<=32+1+8=41<128, using log2(200)<8 and x log2(1/x)<=1. The retained overlap graph has a coloring into c<=kD disjoint layers, giving cJ_s<=10kg.

This does NOT make D bounded as tau shrinks. It bounds the integrated LOCAL STRENGTH of the colored pulse sequence, which is the physical approximation parameter in PHYSICS_LOCAL_STRENGTH_THEOREM.md.

## Rounding and relative-generator approximation
Set theta=tau/(4g)<1. Round each retained local exponential A_e=exp(-delta h_e/2) to a Hermitian rational G_e so that ||G_e-A_e||<=eta=delta*theta*J_s/16. Choose the SMALLEST sufficient common dyadic bit depth B with 2^-B<=eta/(2*2^k). With the schedule below, lambda_min(A_e)>1/2, eta<1/4, and the operator-log integral proves that h'_e=-(2/delta)logG_e satisfies ||h'_e-h_e||<=theta J_s. Thus
 ||H'-Htilde||<=theta L<=n tau/4,
 ||h'_e||<=2J_s, and sum_e ||h'_e||<=2ng.

The layer-strength constant in the new physics theorem is
 K=k sum_j max_(e in layer j)||h'_e|| <=k c(2J_s)<=20k^2 g=:Kbar.
Choose beta=4/tau, and the LEAST positive integer satisfying
 r>=max{2Kbar beta,(8/3)Kbar beta sqrt(g/tau),1}, delta=beta/r.
Square rational comparisons determine the root ceiling. Then Kdelta<=1/2 and the received geometric-tail product-formula bound gives free-energy-density Trotter error<=tau/4, equivalently ||-(r/beta)logP-H'||<=n tau/4. The norm bounds also imply delta*J_s<1, justifying the simple local exponential eigenvalue floor. No extensive operator norm occurs in an exponential estimate.

For fixed k,g and tau tending to0: q=O(n tau^-2), r=O(tau^-3/2), delta=Theta(sqrt tau), theta=Theta(tau), J_s>=const*tau^2. Hence B=O(log(2/tau)). The uniform unique-extension3-CNF compiler produces
 N=O(n tau^-7/2 log(2/tau))
variables and O(N) clauses. All classical preprocessing, term indices, coefficient bit lengths and capped random sampling are charged polynomially.

## Consequences and exact access meaning
The effective A=-(r/beta)logP obeys ||A-H||<=n tau on the successful sparsification event. Its explicitly described positive mixed state sigma=P^r/Tr(P^r) then satisfies
 Tr(Hsigma)-E0(H)<=2n tau+n ln2/beta<9n tau/4.
Taking tau=epsilon/4 gives energy-density error<epsilon with slack. Its exact evaluated energy is ALWAYS an upper bound on E0(H), even when sparsification missed its norm target, because sigma is a valid density operator. The randomness affects near-optimality, not positivity or the upper-bound interpretation. Repeating and choosing the least exactly evaluated witness energy boosts success by ordinary independent trials, with all counting calls charged.

Conditional on the released sparse#3SAT bound, fixed k,g and
 epsilon_n=1/ceil((ceil log2(n+2))^(1/8))
give N=O(n(log n)^(7/16)loglog n) and expected/capped-randomized total time
 poly(input length,n)*2^{O(n loglog n/(log n)^(1/16))}=2^{o(n)}
apart from input reading. Space is polynomial. More generally the displayed bound admits logarithmic exponents a<1/7; no endpoint improvement is asserted. Product-Pauli measurement sampling of sigma retains its previously stated EXPECTED-time, distinct-site, nonphysical-preparation scope. Evaluating the original H uses polynomially many local trace queries, even if the original term list is dense.

This is NOT exact Gibbs sampling, spectral-gap simulation, ground-state trace-distance approximation, a polynomial-time classical witness, or practical algorithm superiority. The new original-source counting theorem remains an imported premise for runtime, not for the quantitative reduction itself. Standard matrix concentration, Hamiltonian term sampling, short imaginary-time locality and Boolean counting ingredients must remain credited.
