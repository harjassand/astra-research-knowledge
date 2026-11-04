# Independent adversarial proof audit: positive latent-Ising compiler

2026-11-04. Reviewer: independent thermal-memory/compiler worker. Reviewed PROOF.md and SOURCES.md in the parent directory, and independently inspected Feng–Guo–Wang's published mixing theorem and equation(33). No Python or numerical experiment was used for this audit.

## Verdict

The mathematical compiler is justified within its declared generic, strictly positive rank-two CP / balanced ferromagnetic / consistent-field class. I found no counterexample to its recognition completeness, strong-edge bound, or original-variable sampling lift. The arbitrary-weight polynomial-bit claim is repairable as stated below; two implementation joins must be explicit, and an expected-time coin routine should not silently be described as worst-case polynomial time.

This is a scoped composition of existing methods, not a new Ising tractability class, not certification of a production implementation, and not an independently established novelty or practical speed advantage.

## 1. Local acquisition and recognition completeness

Let A=T0+tT1. Its determinant is a degree-at-most-two polynomial in t. Nonzero hyperdeterminant rules out an identically singular pencil, so at least one of t=0,1,-1 works. On a real simple spectrum choose eigenvectors U of T1 A^{-1}, and put V^T=U^{-1}A. Then
T1=U diag(mu0,mu1)V^T,
T0=U diag(1-t mu0,1-t mu1)V^T.
This directly proves the displayed CP reconstruction, without relying on a numerical tensor fit.

For a positive rank-two decomposition with invertible legs, the two projective first-leg ratios are distinct. The eigenvectors therefore identify the two component directions uniquely. The remaining factors are then fixed up to nonzero column scalings and a simultaneous swap. Equivalently, the three Kruskal ranks are all2, meeting the rank-two uniqueness condition. Normalizing each column by its coordinate sum removes those scalings. A sum-zero direction cannot be rescaled into a strictly positive column. A mixed-sign normalized column cannot be made positive by changing its sign. Once normalized, the coefficient sign is also fixed. Consequently the tests are complete for the stated strictly-positive generic rank-two class.

The scope restriction matters: rejection does not rule out nonnegative boundary representations, higher latent dimension, non-diagonal holographic transformations, or another tractable formulation. No objection to the paper's explicit restriction.

## 2. Global labels and fields

For an edge W=B_u^T B_v, positivity is immediate and det W=det B_u det B_v is nonzero. Swapping one endpoint's two latent labels changes its determinant sign. Thus the XOR constraints are necessary and sufficient for all edges to have positive determinant. A connected balanced graph has exactly two such labelings, related by a common spin flip.

Independently checking the symmetrization gives
r_u r_v W00=W11,
r_u W01=r_v W10.
Solving gives exactly the ratios in PROOF.md. The two diagonal entries are a=W11, both off-diagonal entries b=r_u W01, and a>b follows from det W>0. Since W=D_u^{-1} H D_v^{-1}, a spin-zero endpoint contributes r_v^{-1}. Therefore d_v(0)=c_v(0)/g_v and d_v(1)=c_v(1), proving the stated lambda and prefactor C.

Positive diagonal symmetrization has unique ratios; multiplying both entries of an endpoint diagonal by a common scalar changes only a global scalar. Hence it cannot rescue opposing fields. After balancing, only a global flip per connected component remains, which sends every lambda to its reciprocal and multiplies the partition prefactor by the product of the previous lambdas. The componentwise common-field test is complete for this representation class.

## 3. Strong-edge lemma and finite-range reduction

Expand all edges except e as 1+(beta_f-1)1[equality]. For each fixed expansion graph, either e's endpoints are connected and cannot disagree, or they belong to distinct clusters with activities a,b in(0,1]. Summing their spins gives equality weight beta_e(1+ab) and disagreement weight a+b. Since
1+ab-a-b=(1-a)(1-b)>=0,
Pr(disagree | expansion graph) <=1/(beta_e+1).
The expansion graph is sampled with its actual nonnegative reweighted mass, so averaging preserves the bound. No independence of that graph from e is required. The lemma is valid, including nonuniform consistent fields; it is not valid for arbitrary opposing fields.

Deleting edges with beta<1+eta changes every weight by a factor within[1,(1+eta)^m]. Conditioning all beta>M edges to agree changes total variation by exactly the excluded-event probability, at most m/(M+1). Every internal edge of a contracted component, not just originally strong edges, must be collected as a constant beta factor. Fields multiply. This preserves the conditional law and its partition identity.

There is no need to merge parallel remaining edges. For t=beta+sqrt(beta^2-1), an auxiliary unbiased spin yields
sum_z t^{1[s_u=z]+1[z=s_v]} = 2t beta^{1[s_u=s_v]}.
The two cases are t^2+1=2t beta and2t. Thus the expanded partition is (product_e 2t_e) times the old partition. IMPORTANT: recovering the old partition requires division by this product. The source's instruction to 'collect this known prefactor' is ambiguous, not an algebraic failure, but must specify the reciprocal.

Every edge receives its own auxiliary vertex, so parallel edges become a simple graph. Since beta<=M, t<=2M; and t>=beta>=1+eta. Isolated vertices or a graph with no remaining edges are sampled and counted directly, without invoking an edge-based mixing theorem.

## 4. Bit complexity and two necessary implementation clarifications

Each local pencil uses only a quadratic extension of rational input. Bounded degree of the original graph is essential: an edge depends on two local fields; a vertex field depends on only a constant number of local fields and square roots. The algebraic degree is therefore bounded independently of graph size. Rational-input height grows polynomially in L under these fixed-size operations. Standard root separation bounds then give polynomial-size isolating descriptions, exact sign tests, and polynomial logarithmic bounds on nonzero local quantities.

The product C may have exponential algebraic degree. The proposed factorwise numerical evaluation avoids that problem. With N=O(n+m) positive factors and logarithmic error at most d on each, the product's logarithmic error is at most Nd. Likewise each configuration weight in a rounded model changes by at most exp(plus-or-minus Nd), and normalized probabilities by at most exp(plus-or-minus2Nd). Choosing d proportional to epsilon/N suffices. Positivity prevents cancellation in this global product.

Strong contraction multiplies already-rationalized fields; numerators and denominators gain additive bit length, hence polynomial size even when the resulting field is exponentially small. Tiny lambda does not invalidate the general consistent-field backend: its random-cluster weights are1+product(lambda), bounded between1 and2.

**Clarification A: a second algebraic step occurs after initial rationalization.** The edge-subdivision t contains a square root even when beta was rounded to a rational. One cannot then literally claim every sweep uses rational coins unless t is rationalized again. Repair: approximate each t to relative/logarithmic error O(epsilon/m), maintain t>=1+eta/2, and allocate a second global perturbation budget on the enlarged graph. Approximate the corresponding reciprocal normalization factors separately. All these square roots have degree2 and polynomial height. Alternatively use certified algebraic coins with a separately analyzed accuracy/runtime budget. This is an omitted accounting step, not a superpolynomial obstruction.

**Clarification B: runtime convention.** Exact rejection-based rational Bernoulli generation has polynomial expected bit cost, not a finite deterministic worst-case stopping time. For the usual worst-case polynomial randomized-algorithm formulation, cap retries and allocate the exponentially small cap-exceedance probability among the polynomially many coin calls; output a failure/fallback on that event. This adds arbitrarily small total-variation or counting-failure error while making the runtime bound explicit. An expected-polynomial statement is also valid if labeled as such.

Arbitrary algebraic input numbers are NOT covered without an encoding/degree promise. What is covered is arbitrary-bit-size rational raw tensors and bounded-degree algebraic quantities derived from their constant-size neighborhoods. The proof does not claim a generic algorithm polynomial in the size of unrestricted nested algebraic expressions.

## 5. Backend and counting verification

I inspected the published Feng–Guo–Wang PDF, Theorem1.1 and its equation(33):
https://doi.org/10.1016/j.ic.2023.105066
https://www.pure.ed.ac.uk/ws/portalfiles/portal/370864187/Swensden_Wang_FENG_DOA27062023_VOR_CC_BY.pdf

Its general consistent-field mixing estimate has polynomial graph-size dependence and a coupling-range prefactor controlled by min(p_min,1-p_max), with p=1-1/beta. After preprocessing, this minimum is inverse-polynomial in m and1/epsilon. The use of that general theorem is justified; one need not assume fields stay uniformly away from1. The faster theorem with a field margin is not the arbitrary-weight fallback. The extracted PDF text reverses the expected sign in one beta-denominator expression; this could be a text-extraction issue. The preceding positive p-expression is unambiguous and is the one used here.

For counting, use the exact expanded-model identity with reciprocal subdivision constants. Start from the edge-free model with the same fields. Add each final edge with its first nontrivial weight min(2,t_final), then double up to t_final. Every nontrivial absolute edge strength is at least the final minimum margin or2, so these annealing stages do not reintroduce an arbitrarily small beta-1. Each ratio observable lies in[1,2], and the number of stages is O(m log M). Approximate independent draws with bias smaller than the per-stage target, followed by Hoeffding and a union bound, give a polynomial approximation scheme. No inconsistent-field pinning is required.

## 6. Original-variable lift

The joint positive weight q(x,s) has the advertised two marginals by independently distributing finite sums. Conditional on s, the original edge bits are independent, with precisely the two endpoint-factor product divided by W_e. This is a genuine stochastic kernel, not merely a linear gauge map. A latent distribution error contracts under this kernel. Approximate binary kernels with per-edge TV error eta can be coupled edge by edge; the probability of any mismatch is at most m eta. Therefore the lifted sample has error at most delta+m eta.

The kernel must be evaluated in the original positive-CP labels, after expanding contracted vertices, discarding subdivision spins, and undoing all recorded swaps. It can use certified approximations of the ORIGINAL factors independently of the rationalized Ising backend. Agreement need only be within the explicitly allocated errors; it does not require an exactly rational CP factorization.

## 7. Baseline and justified consequence

Nonnegative-rank-two tensor recognition and ferromagnetic Ising approximation are established methods. The same-resource comparator is local CP reconstruction followed by an established consistent-field Ising sampler and this latent-variable marginalization, not exponential raw contraction. The reviewed text appropriately disclaims a new tractability class and practical superiority. Generated examples validate identities but do not establish consequential workload frequency or novelty.

The justified output is a polynomial-bit, scoped recognition-and-approximate-sampling/counting compiler, with the normalization, second rationalization and runtime convention made explicit. No new physical interface, general tensor-network sampler, arbitrary mixed-field solution, or transformative computational advantage follows from this proof alone.

## Reviewed version identifiers
PROOF.md SHA256: 7a2074003245543f5f8d464657958f677245a826d7251ef0f95fb205b2a0823e
SOURCES.md SHA256: 751b9c38d127cb9f540bb5ddc84c309f2fc0d30fa0b2ab6594f9ea9e5d20fe6d
The audit applies to these read versions; later author revisions require a diff check.

## Follow-up verification of author repairs, 2026-11-04 02:22UTC
Re-read the revised Sections6–7 and quantitative implementation detail. Revised PROOF.md SHA256: 8ea93a3e3e6de48b68b215e77bf2d822009702339493ab81133a196d2b4182c7.

All three requested repairs are correctly present:
1. The expanded partition is explicitly divided by product(2t) on recovery.
2. New subdivision square roots are rationalized with their own logarithmic perturbation budget, preserving a polynomial lower interaction margin; normalization uses the original exact t identity and an independent numerical approximation.
3. The expected-time rational-coin statement is distinguished from capped rejection. With a polynomial number Q of calls and at least1/2 success per trial, a ceiling(log2(Q/gamma))+1 cap gives aggregate failure probability at most gamma. The fallback/failure is charged to TV or counting confidence.

The newly explicit annealing schedule retains an inverse-polynomial nontrivial coupling margin at every stage. The displayed conservative mixing and total sampling bounds are polynomial after substituting eta and M. Isolated/no-edge cases and the original-factor conditional kernels are also clarified.

No remaining blocker identified for delivery as a proof-only, scoped compiler theorem. This is not verification of an executable implementation, all literature priority, or a new practical computational advantage. The original audit's substantive scope restrictions remain in force.
