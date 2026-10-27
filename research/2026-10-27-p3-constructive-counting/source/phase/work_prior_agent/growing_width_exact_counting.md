# Uniform growing-width exact counting

27 October 2026. Conditional on the supplied OpenAI ETH manuscript. A quantitative extension, not general CircuitSAT or a practical speedup. Sparsification at the scale (k/epsilon)^(3k) is established prior work (Cygan et al., 2012).

## Main conclusion

Put lambda=ceil(log_2 n), nu=ceil(log_2 lambda), a=k^3 nu/lambda. One deterministic algorithm with absolute polynomial exponents counts an explicitly described k-CNF of bit length L on its original n declared variables in

    (L+n)^O(1) 2^[O(n sqrt(a) (log_2(2/a))^(3/2))]

for 2<=k and a<=1/16, with polynomial space in L+n. Bounded exceptional sizes use exhaustive search. In particular the time is polynomial description length times 2^o(n) for k=o((log n/log log n)^(1/3)).

The changes to the supplied construction are counting-preserving sparsification with explicit growing-k constants, and optimization of the actual binomial tail instead of the fixed-beta specialization in Lemma 4.8.

## Factorial sparsification

Keep Appendix A's branching and normalization, but set theta_j=M^j(j!)^2, j>=0, M>=2. Child A requires some literal of the common set H true; child B requires all of H false and retains the petals. This remains a disjoint partition. Select smallest clause width c, then largest |H|.

Lemma A.2's proof needs only theta_{j-i}, not geometric multiplicativity. Its insertion recurrence therefore remains

    T1<=2n;
    Tj<=4n theta_{j-1}+2 sum_{i<j}theta_{j-i}Ti.

Tj counts all insertions, including later-deleted clauses, excluding input clauses. Induction gives

    Tj<=16n M^(j-1)((j-1)!)^2.

Separate i=1 and divide the recurrence by nM^(j-1)((j-1)!)^2. The bound is 8+32 sum_{b=1}^{j-2}binom(j-1,b)^(-2)<=16. Each internal binomial coefficient binom(m,b)>=m, so the sum is <=(m-1)/m^2<=1/4; the empty case also holds.

A B-step of petal width j inserts >=theta_j clauses, so occurs <=16n/(Mj^2) times. Since sum j^(-2)<2, there are <=32n/M B-choices along a path. Depth is <=Cn, with

    C=16 sum_{j=0}^{k-2}M^j(j!)^2<=32M^(k-2)((k-2)!)^2.

For M>=32, the source's path encoding bounds nodes by (Cn+1)^2 2^[(32n/M)log_2(4CM)]. Choose the first power of two M>=32 with 32ceil(log_2(4CM))<=sigma M. If h0=ceil(log_2(4k/sigma)), a power of two in [2048kh0/sigma,4096kh0/sigma) suffices: log_2 M<=5h0, ceil(log_2(4CM))<=9kh0, while sigma M>=2048kh0. Hence

    M=O((k/sigma)log(2k/sigma)),
    B=2 sum_{j=0}^{k-1}theta_j<=4M^(k-1)((k-1)!)^2,
    log B=O(k log(2k/sigma)).

B,C are computed integers. Leaf solution sets are disjoint.

For a uniform implementation, enumerate subsets only of clauses actually present, using canonical sorted keys. Never allocate all n^k clauses. Each clause has <=2^k subsets and each current formula has <=m_input+Cn clauses. Per-node work and depth-first storage are polynomial in L+n+C+2^k+k+log M with absolute exponents. Under the parameters below C,2^k=n^o(1), so these are fixed polynomial factors in L+n. Before materializing arrays, the algorithm checks C,B,2^k,D0<=n and the explicit polynomial-size parameter bounds; failure invokes exhaustive search. Uniform estimates below imply these guards fail at only bounded exceptional sizes in the theorem range. This ensures a global polynomial-space algorithm even before the asymptotic regime.

## Parity systems and preprocessing

Take sigma=1/ceil(sqrt(lambda)). For k<=lambda^(1/3), log B,log C=O(k nu). Each leaf has m_G<=Bn clauses. Put mu=floor(log_2 m_G)+1=O(lambda) and use Section 6.1:

    P=20000B^2 mu^2; D0=320000B^2 mu^3.

Each candidate system has <=6n equations of degree <=k, with <=2^kD0 monomials per equation. The actual scope is <=kD0, because each row uses <=D0 clauses. The 2^k expansion factor is unnecessary in the scope bound. Total incidence N0<=6nkD0.

Fix variables in more than b0=ceil(N0/n)ceil(sqrt(lambda)) scopes. At most n/sqrt(lambda) bits are fixed, so there are <=2^[n/sqrt(lambda)] disjoint branches and >=n/2 free variables. Add neutral factors. The remaining maximum incidence b<=b0+1 and scope w<=max(kD0,1) satisfy log b,log w=O(k nu). Monomial descriptions have n exp(O(k nu)) entries and polynomial bit length.

The initial code search is bounded by poly(n,B,mu)2^[O(B^3mu^6)]. The shift search exponent is <=D0log_2(2m_G); a local matrix has c_Gd_G<=D0^2/(8B)+D0 bits. Even checking all local words fits the bound. Greedy selection makes <=3n(2m_G)^P candidate counts, exponent O(B^2mu^3+log n). Expansion costs polynomial in n,2^k,D0. These preprocessing exponents are exp(O(k nu))lambda^O(1)=n^o(1), uniformly for k<=lambda^(1/3). Every candidate count is actually computed; the answer and useful parity summary are not supplied.

## Optimized replacement parameters

For a branch with N>=n/2 free variables put lambda'=ceil(log_2 N), nu'=ceil(log_2 lambda'), a'=k^3nu'/lambda'. These differ from the original parameters by bounded factors. Compute from actual scopes

    r=floor(sqrt(lambda'/(k^3nu'))),
    t=ceil(log_2 r), Q=floor(lambda'/(128t)),
    tau=1/(r lambda'), D=r^(2Q),
    A=ceil(log_2(2br^2lambda')),
    R=ceil(sqrt(8QA))+32.

Check r>=2,Q>R,R>=32,6R<=Q, both Lemma 4.7 balance conditions and interval endpoints. The R-point interval about the binomial mean contains every integer within R/4. Hoeffding and e>=2 give the exact certificate

    Pr[W outside I]<=2exp(-R^2/(8Q))
                   <=2exp(-A)<=2^(1-A)
                   <=1/(br^2lambda')=tau/(rb).

No floating-point tail estimate is required. As t=O(log(2/a'))=O(nu') and log b=O(k nu'),

    A=O(k nu'),
    R/Q=O(sqrt(k nu' t/lambda'))+O(t/lambda').

Also D<=2^(lambda'/64)<=(2N)^(1/64), b,w=exp(O(k nu'))=N^o(1), and therefore 2(b+w)D^2<=N<=total incidence for sufficiently large N uniformly. The condition 2Qr^2<=N follows from a polynomial bound in lambda'. R/Q tends uniformly to zero over the stated a' range with r>=2 and k<=lambda'^(1/3), so 6R<=Q and interval containment eventually hold. The guarded algorithm falls back to exhaustive search only at bounded exceptional sizes in the uniform theorem.

## Counting and exact arithmetic

Use original precision ell=n+1. With <=6n equations, Lemma 5.2 gives d<=8kn<=16kN. Retain q=floor(dR/Q) perturbation variables and J=q+1 Taylor coefficients. Then

    q/N=O(sqrt(a' log(2/a'))).

For q<=N/2, the cost Cq=sum_{j<=q}2^j binom(N,j) obeys log_2 Cq<=N[H_2(q/N)+q/N], hence O(Nsqrt(a')(log(2/a'))^(3/2)). For the remaining bounded-a' range, Cq<=3^N is absorbed after increasing the absolute constant. Measurement and group enumeration each cost exponent O(N/r)=O(Nsqrt(a')); indeed tau log(2D+1)=O(1/r).

Every input list, replacement array, factor coefficient array, measurement matrix and Hermite matrix is polynomial-size in L+n. For example D<=(2N)^(1/64), Q,R,r<=poly(log N), ell=n+1, J=O(kn), and S=n exp(O(k nu)) is polynomial. The row denominator is (R-1)!Q!, logarithmic size O(Qlog Q). Proposition 5.3 and Appendix B have fixed-polynomial bit costs in their explicit parameters n,ell,k,Q,log D,log S. Exponential enumeration contributes only its logarithm to coefficient bit length. Thus the bound is in bit operations.

Traverse all trees, candidates, measurement tuples and subset pairs sequentially. Rational Hermite reconstruction, coefficient summation and reduction modulo 2^(n+1) give each exact count. Disjoint branch counts add with n+1 bits. The exponents n sigma, n/sqrt(lambda), and n^o(1) preprocessing are absorbed by the main term. Space remains polynomial.

## Width removal with only a bound on initially long clauses

Let F be an arbitrary CNF on N declared variables, bit description length L, with at most M clauses whose width exceeds a chosen k>=2. There may be arbitrarily many clauses of width at most k. At a node, simplify clauses under the accumulated partial assignment. If C is a remaining long clause, choose k distinct literals P from C. Partition the solutions into A: replace C by the clause P, requiring some literal of P true; B: fix every literal of P false, retain C, and simplify the formula.

These cases are disjoint and exhaustive. Child B fixes k distinct free variables, so a path has at most floor(N/k) B choices. Child A permanently makes one formerly long clause short. Simplification only shortens or deletes clauses, so a path has at most M A choices regardless of the number of initially short clauses. With D=M+floor(N/k), depth is at most D. A deterministic branch rule makes each node specified by its depth and B positions. Thus the number of nodes is at most

    (D+1) sum_{j=0}^{floor(N/k)} binom(D,j)
      <= poly(M+N) 2^[O((N/k)log_2(2+Mk/N))].

For N/k<=M, apply the binomial-sum bound with B fraction at most 1/2; for M<N/k, use 2^D. If M=0 there is no branching. Normalize tautologies and repeated literals first. Contradictions terminate immediately. At every leaf, retain the original N declared variables and add the accumulated fixed bits as unit clauses. The leaf count is exactly its branch count, with no missing factor for fixed bits, and all clauses have width at most k. The leaf description is polynomial in L+N. Depth-first traversal uses polynomial space.

For a=k^3 ceil(log_2 ceil(log_2 N))/ceil(log_2 N)<=1/16, the full bit-time bound is

    (L+N)^O(1) 2^[O((N/k)log_2(2+Mk/N)
                 +N sqrt(a)(log_2(2/a))^(3/2))].

This is subexponential in N if k tends to infinity, k^3 log log N=o(log N), and log(2+M/N)=o(k). It covers M=O(N) without restricting the number of initially short clauses.

For M=O(N), put lambda=ceil(log_2 N), nu=ceil(log_2 lambda), and choose integer k of order lambda^(1/5)/nu^(2/5). Both exponent contributions are

    O(N nu^(7/5)/lambda^(1/5)).

Small N uses k=2 or enumeration. The same expression holds for M=N(log N)^c, fixed c, with a constant depending on c. In particular, unrestricted-width CNF with O(N) clauses can have quadratic literal incidence and needs no internal variables. The partition itself is elementary; its use here removes fixed width using the rigorously uniform counter.

## Raw unbounded-fan-in circuit consequence

Consider an explicit acyclic Boolean circuit with n independent inputs, g noninput AND/OR gates of arbitrary fan-in, negations on wires, W wires, and prescribed target values on designated outputs. Let L include gate kinds, signed source indices, and output targets. Compute a topological order in polynomial time. Delete repeated literals; complementary literals make the gate the appropriate constant. Empty gates have their standard constant values.

Introduce one variable y per gate, so N=n+g. For y=AND(l_1,...,l_t), add the t binary implications (not y OR l_i) and one reverse clause (y OR not l_1 OR ... OR not l_t). For an OR gate add (y OR not l_i) for every input and one reverse clause (not y OR l_1 OR ... OR l_t). Output targets are units. Negated edges need no additional variables; constants and unary gates only add short clauses. For each original input assignment there is exactly one satisfying gate-variable assignment, its topological evaluation. Thus the encoding preserves the original target-preimage count exactly.

The CNF has O(W+g+number_of_targets) clauses and polynomial bit length in L+N, but at most g possibly long clauses. Every other clause has width at most two. Applying width removal with M<=g<=N gives deterministic exact counting in

    (L+n+g)^O(1)
       2^[O((n+g)(log log(n+g))^(7/5)/(log(n+g))^(1/5))]

bit operations and polynomial space. Constants in both exponents are absolute. For g=O(n), this is subexponential in the ORIGINAL independent-input count n, without restrictions on circuit depth, fan-in, output locality, or decomposition. After duplicate-wire normalization W can still be Theta(n^2). A direct fan-in-two expansion would introduce Theta(W) internal variables and fail to retain subexponential dependence on n on such dense circuits.

The displayed bound is also 2^o(n) times polynomial description length when g=o(n(log n)^(1/5)/(log log n)^(7/5)); this sufficient condition gives log(n+g)=Theta(log n). Counting is per requested target. A complete histogram still incurs its output-size cost. Conditional counting gives inversion and exact sampling with polynomially many calls, as already in the source; these are consequences, not additional new mechanisms.

## Raw many-output growing-locality circuits

Another consequence needs no trace variables. Compute syntactic input supports by set unions through a circuit DAG. If every designated output has support at most k, evaluate its 2^k local assignments and forbid each assignment giving the wrong target. Supports may overlap arbitrarily. The k-CNF has exactly the original n variables, at most t_out 2^k clauses, and O(t_out 2^k k log n) bits; construction costs poly(L+n)2^k. The growing-width theorem gives subexponential original-input exact preimage counting for k=o((log n/log log n)^(1/3)), independently of the number of intermediate gates. Fan-in-two depth d implies support at most 2^d, giving a growing-depth range; arbitrarily deep small-support outputs are also allowed.

This is a quantitative extension of the source's fixed-locality corollary. The unbounded-fan-in result is stronger as a representation consequence because it removes a locality restriction rather than merely increasing its bound.

## Scientific status and limits

The argument is conditional on the supplied OpenAI manuscript. It is a uniform quantitative extension and a class of raw dense circuits, not a generic program or circuit solver and not a polynomial-time SAT algorithm. The circuit compiler introduces g uniquely determined state bits; sufficiently large g erases the original-input gain. No practical speed advantage has been established. Accompanying programs execute structural transformations and finite exact consistency checks, not the full asymptotic counting algorithm.

The useful shared summary is manufactured by the source's parity-selection and replacement-form procedures. No small width or easy decomposition is assumed in the unbounded-fan-in theorem: the disjoint tree manufactures width with its entire cost included. The modified thresholds and concentration parameters expose the width dependence absent from the stated fixed-k theorem. The sparsification dependence itself is established prior art, so it is not claimed as a separate discovery. Moreover, qualitative subexponential counting for M=O(N) initially long clauses already follows from this elementary width split and the supplied fixed-k theorem: for each desired exponential rate choose a sufficiently large constant k, then use its subexponential counter (or effective diagonalization). The distinctive result proved here is the explicit uniform rate, fixed polynomial exponent, growing-width admissibility, and consequent quantitative superlinear gate range. The qualitative dense linear-gate corollary alone is not presented as the requested breakthrough.

## Sources

1. OpenAI, The Exponential Time Hypothesis is False, revision 25 October 2026, Sections 3--6 and Appendices A, B, D. Pinned governing source: https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf
2. Cygan et al., On Problems as Hard as CNF-SAT (2012), for the established quantitative sparsification scale c(k,epsilon)=(k/epsilon)^(3k): https://cseweb.ucsd.edu/~paturi/myPapers/pubs/CyganDellLokshtanovMarxNederlofOkamotoPaturiSaurabhWahlstrom_2012_ccc.pdf

## Executed finite checks

The accompanying check_uniform_width_bounds.py uses exact integers and rational numbers. It verified 396 insertion-recurrence inequalities (j=2,...,100 for four M values) and 35 explicit parameter-cap choices (seven k values and five rational sigma values); all assertions passed. uniform_width_bound_checks.json contains the complete results. These finite checks support implementation of the repaired inequalities; the induction and asymptotic argument above supply the proofs. They do not test the full counting algorithm or establish a practical speed claim.
