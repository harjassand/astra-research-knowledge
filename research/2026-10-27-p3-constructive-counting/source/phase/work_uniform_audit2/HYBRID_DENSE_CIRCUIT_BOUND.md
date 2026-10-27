# A hybrid contraction bound for dense AND/OR circuits

27 October 2026. Conditional on the pinned OpenAI manuscript. This is a quantitative extension, not a claim to solve general CircuitSAT, historical priority, or practical speed.

## Main result

Let an explicitly given acyclic Boolean circuit have n independent inputs, g noninput AND/OR gates of arbitrary fan-in, signed wires, W wires, and prescribed target values on any designated outputs. Let L be its bit description length and N=n+g. A deterministic exact counter follows from the governing manuscript with time

    (L+N)^O(1) 2^[O(N sqrt(log log N)/(log N)^(1/4))]

and polynomial space. Constants in the polynomial and exponential bounds are absolute. Small sizes use exhaustive search. Gate values are uniquely determined by the original inputs, so the count is the original target-preimage count, with no multiplicity correction. There is no depth, fan-in, wire-density, or supplied-decomposition promise. In particular, W may be Theta(N^2) after duplicate-wire normalization.

The time is subexponential in the original n when

    g=o(n (log n)^(1/4)/sqrt(log log n)).

The theorem still charges for g gate bits. It does not resolve the main arbitrary-many-state target. Its qualitative conclusion for g=O(n) is already a routine consequence of fixed-width counting and a width split. The contribution here is the explicit uniform rate, with the dense binary part compiled separately from the few long clauses. This improves the earlier 1/5-power quantitative rate, and does not depend on that earlier growing-width theorem.

## 1. The hybrid counting lemma

Write lambda=ceil(log_2 N), nu=ceil(log_2 lambda), for N sufficiently large. Let

    F = B AND C,

where B is an arbitrary explicitly listed 2-CNF on the N declared variables and C is an arbitrary explicitly listed CNF with H literal incidences. The two lists may share variables in any way. The direct clause list C is not expanded into a monomial list or included in the sparsification of B.

The count of F is computable in

    (L+N+H)^O(1) 2^[O((N nu+H)/sqrt(log_2(N nu+H)))]

bit operations and polynomial space, conditional on the source. This is useful even when B has quadratic literal incidence. For the application below, H<=kM<=kN with k a fixed power of log N, but the construction does not require that bound.

### 1.1 Manufacturing the binary summaries

Apply Appendix A's disjoint sparsification only to B, using clause width 2 and sigma=1/ceil(sqrt(lambda)). Each leaf B_j has at most B_0 N clauses, where B_0 is bounded by a fixed power of lambda. The leaf solution sets partition B's solutions, so the counts of B_j AND C add to the desired count. The number of leaves is polynomial times 2^[O(N/sqrt(lambda))]. Keep all N declared variables at every leaf, including fixed variables represented by unit clauses.

For each B_j, run Section 6's manufactured parity-test procedure on B_j alone. This constructs a system A_j of at most 6N equations over F_2, each of degree at most 2 and with a fixed polylogarithmic number of monomials. Every solution of B_j passes A_j. The greedy procedure proves that the two counts are equal. Therefore their sets of Boolean solutions are equal, not merely equinumerous:

    {x:B_j(x)=1} = {x:A_j(x)=0}.

Consequently the same replacement is valid after conjunction with C. This set-equality step is necessary; arbitrary count-preserving substitutes could not be used under a further observable.

All parity rows are actually selected by the manuscript's unweighted candidate counts. No summary, satisfying-count value, or useful matrix is assumed as input. Since the sparsification width is the fixed constant 2, Section 6 and Appendix D.2/D.3 bound the construction cost by

    poly(L+N) 2^[O(N nu/sqrt(lambda))]

plus 2^[poly(log N)] preprocessing. The latter is absorbed in the displayed exponent for sufficiently large N. Using the older Section 5 counter instead would still be lower order in the final circuit bound.

### 1.2 The sparse-test half of the tensor network

Use the incidence-polynomial encoding of Appendix D.3 for A_j. Its ring is

    R = (Z/2^(N+1)Z)[V]/(V^(N+1)).

The Beigel--Tarui evenness lift uses one shared V-order budget, as in Lemma 5.2. The retained incidence-monomial degree is at most K_0=2(a+2N)=O(N), where a<=6N is the number of equations. The inputs remain the original Boolean variables.

As in Appendix D.3, fix the values of variables whose test incidence is above a polylogarithmic threshold. There are at most N/sqrt(lambda) such variables. Branches are disjoint. Substitute these bits into both A_j and C. This operation only decreases H. No heavy-variable estimate involving the direct-clause incidence H is needed.

Partition the tests and free variables into J=ceil(N^(1/4)) groups. For each array of selected-incidence counts d_(u,v), of total at most K_0, use ceil(log_2 binom(E_(u,v),d_(u,v))) wires to index a selected subset of incidences between a test group and a variable group. Here E_(u,v) counts only the sparse-test incidences, not the clauses in C. Exactly as in equation (D.3), these wires total O(N nu). The degree-array count is 2^[O(sqrt(N) log N)], which is lower order.

At a test group, the tensor entry is the product of the indicated multilinear coefficients of its lifted equations. These entries are computed by the source's Boolean Möbius inversion, in 2^[poly(log N)] time and polynomial space. Their computation and degree accounting are unchanged by C.

### 1.3 Attaching the direct clauses

For each free variable that occurs in C, add one Boolean port to its variable-group tensor. Route this bit to all occurrences in C through an equality tree. Each common external bit extends uniquely through a tree, so no multiplicity is introduced. Variables not occurring in C need no added port. The total number of equality-tree edges and clause ports is O(N+H).

A direct clause gets its ordinary 0/1 satisfaction tensor. If the clause is too large to meet Theorem D.1's maximum-degree hypothesis, realize its OR by a binary tree of ternary Boolean OR tensors, fixing the output to 1. Each assignment to its literal ports has exactly one internal OR trace, contributing one precisely when the clause is satisfied. Signed literals are handled in the leaf-port tensors. This uses O(clause width) edges and degree at most three. Empty clauses terminate the branch with count zero. Hence no large-arity tensor is being assumed cheap or admissible.

For an assignment of the monomial-index wires, let b_v be the number of selected test incidences for free variable v. The variable-group tensor sums the Boolean x_v subject to the values q_v on its newly attached ports:

    product over variables with a direct port of q_v^(b_v)
      times product over variables with no direct port of
               (2 if b_v=0, else 1).

Use 0^0=1. This expression is the exact local sum of product x_v^(b_v), with each directly used variable pinned to its exposed bit. A port consistency check is unnecessary at the group because each variable has only one exposed port; its external equality tree enforces all copies. Evaluating this tensor takes polynomial time. It preserves the dependence on C exactly, rather than replacing it by a scalar count.

Summing the physical direct-clause bits and the coded monomial indices therefore gives, in R, the source's parity-lift product multiplied by the Boolean indicator of C and summed over the original variables. Sum the V-coefficients after contracting, then reduce modulo 2^(N+1). The source congruence gives #F, since the true count lies in [0,2^N].

If necessary subdivide every network edge once by an equality tensor to make the network bipartite. This is a constant-factor increase and preserves the contraction.

### 1.4 Costs and admissibility

Put s=N nu+H. Each resulting network has O(s) Boolean edges and polynomially many vertices. Its test and variable groups have maximum degree at most N^(3/4) poly(log N), plus at most N^(3/4) newly exposed variable bits. The equality and OR trees have constant degree. Thus the degree is at most s^(9/10) for all sufficiently large N, uniformly in H. Both ring precision and truncation order are N+1=O(s).

The group-entry procedures use at most poly(L+s) 2^[poly(log N)] time and polynomial space, uniformly in the port assignment. This meets Theorem D.1 with fixed constants A,b, since s>=N and any fixed polylogarithmic exponent is eventually below s^(9/10). All tensor descriptions and degree-array counters have polynomial bit length. Apply Theorem D.1 to obtain 2^[O(s/sqrt(log s))] bit operations per network. The sparsification branches, heavy-variable branches, degree arrays, parity-summary construction, and direct-constraint normalization are absorbed in that bound. All enumerations can be traversed sequentially, with polynomial space.

This proves the hybrid lemma. Its substantial bookkeeping advantage is that the direct C incidences cost H wires, not H log log N wires and not an increase of the sparse-test degree parameter. The binary density is compiled into the O(N log log N) part.

## 2. Manufacturing small direct-clause incidence

Suppose the original CNF has an arbitrary 2-CNF part B and at most M other clauses. Fix a cutoff k>=2. At a node, simplify under its partial assignment. For a remaining clause C of width greater than k, choose k distinct free literals P from C. Branch disjointly:

- A: replace C by P, requiring some literal of P true.
- B: require every literal of P false, retain C, and simplify.

A path has at most M A-steps, since a selected clause becomes short permanently. It has at most floor(N/k) B-steps, since each fixes k new free variables. A deterministic branch rule bounds the number of nodes by

    poly(M+N) 2^[O((N/k) log_2(2+Mk/N))].

For M>=N/k use the usual entropy bound on a binary path with at most N/k B-positions; for M<N/k the total-depth bound suffices. Retain all original N declared variables, adding fixed bits as units. At a leaf the direct list has at most M clauses, each of width at most k, so H<=kM. The binary part may be arbitrarily dense and includes the new units.

The hybrid lemma gives total time, for M<=N and k bounded by a fixed power of log N,

    poly(L+N) 2^[O((N/k) log_2(2+Mk/N)
                         +(N nu+kM)/sqrt(lambda))].

For M<=N choose the integer cutoff

    k = max(2, floor(lambda^(1/4) sqrt(nu))).

It can be constructed by integer comparisons, e.g. choose the greatest integer k with k^4<=lambda nu^2. Then log(2+k)=O(nu), and both dominant contributions are

    O(N sqrt(nu)/lambda^(1/4)).

The N nu/sqrt(lambda) term is lower order. This proves the claimed explicit rate for a 2-CNF plus at most N unrestricted clauses.

## 3. Compiling raw circuits and preserving outputs

Topologically sort the given circuit. Assign one trace variable to each gate, so N=n+g. For an AND gate y=AND(l_1,...,l_t), add its binary implications

    (not y OR l_i),  i=1,...,t,

and the single reverse clause

    (y OR not l_1 OR ... OR not l_t).

For an OR gate add the dual binary implications (y OR not l_i) and the one reverse clause (not y OR l_1 OR ... OR l_t). Prescribed outputs are unit clauses. Normalize repeated or complementary literals; constants and empty gates are immediate.

There are O(W+g) clauses, but only g possibly long reverse clauses. For each original assignment of the n independent inputs there is exactly one trace satisfying every gate relation, and the output units accept precisely the requested original outputs. Thus the full trace CNF is parsimonious. Applying Section 2 with M<=g<=N proves the main result. The description-size factor includes reading all W signed wire references; they are not treated as a free decomposition.

The conversion, disjoint clause tree, sparse binary summaries, tensor descriptions and reconstruction costs are all constructed and paid for. A histogram over all output strings would still incur its output-size cost. The theorem is for the count at a supplied target, and says nothing about polynomial-time SAT.

## 4. Scientific status

The mixed construction is conditional on the pinned source's Theorem D.1 and its exact parity-test manufacture. It is not an independently established refutation of ETH. Its raw circuit compiler is stronger quantitatively than the first growing-width route, but remains a composed extension of the governing machinery. Qualitative subexponential counting for dense linear-gate circuits is not claimed as new; it already follows by choosing a sufficiently large constant width before applying the fixed-width theorem.

The supplied checker executes exact finite parity-summary selection, the lift, Boolean Möbius coefficients, index round trips, and hybrid contractions. It uses exhaustive enumeration for finite counting and contraction. These checks validate the algebraic representation; they do not execute Theorem D.1's asymptotic algorithm or establish a practical speed advantage.

Source: OpenAI, *The Exponential Time Hypothesis is False*, pinned 25 October 2026 revision, Sections 5--6, Appendices A and D:
https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf
