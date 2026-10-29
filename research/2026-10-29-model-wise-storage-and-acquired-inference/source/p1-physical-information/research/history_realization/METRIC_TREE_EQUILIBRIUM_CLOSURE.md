# Metric-tree compatibility and the closure of hidden equilibrium

Research construction, 29 October 2026. Written by the complementary history-realization agent for Astra. This is a mathematical proof draft, not an external validation or a historical-priority claim.

## 1. Result and exact scope

Let A be a finite observation alphabet. Let p be a stationary probability law on A indexed by the rational time line. The following are equivalent:

1. p belongs to the rational-cylinder closure of stationary finite reversible continuous-time Markov chain observations with deterministic memoryless emissions.
2. The path marginals of p extend to probability laws on every finite unrooted tree with positive rational edge lengths, consistently under graph isomorphism, leaf deletion, and subdivision of an edge into two edges whose lengths sum to the original length.

Every finite portion of condition 2 is a linear feasibility problem over finite probability tables. Thus this is a complete convex feasibility hierarchy for the specified closure. It has no hidden-state, clock-rate, stationary-mass, or irreducibility cap.

If p is stochastically continuous, the construction also gives an exact realization by a stationary reversible, strongly continuous Markov semigroup on a standard Borel probability space. This conclusion is not an exact finite-state CTMC realization, a finite-rate pure-jump realization, a Hunt-process construction, or a càdlàg hidden-path theorem.

The essential additional information is consistent branching at more than one vertex, together with edge-subdivision compatibility. CP reflected-history data give positive factors at a cut; they do not supply this whole structure.

### Existing ingredient and collision

The uncolored infinite-degree-tree representation is classical. Aldous, *Exchangeability and related topics*, Saint-Flour 1983 lectures, published in LNM 1117 (1985), Theorem 13.5, pp. 111–114, proves that an invariant tree process is a coordinatewise observation of an invariant Markov tree process. The proof uses branch directing measures and their independence of the labeling scheme. The countably colored version used below follows by the same argument with one exchangeable family per edge color; it is proved here to state the needed interface. No claim that this representation argument is new is made.

Primary source: https://www.stat.berkeley.edu/~aldous/Papers/me22.pdf

The proposed addition in this note is the assembled metric-tree criterion, its semigroup implication, and its finite-CTMC closure bridge. Priority for that assembled statement remains unverified. The finite graph connection-algebra literature is an additional relevant antecedent, not evidence of priority.

## 2. What the extension requires

A finite metric tree T consists of a finite connected acyclic graph with a positive rational length on each edge. For each such T, introduce a probability vector

    q_T(y), y in A^{V(T)}.

Require:

- Isomorphism: relabeling vertices without changing edge lengths relabels q_T accordingly.
- Leaf deletion: summing the label of a leaf gives the law for the tree with that leaf and its incident edge removed.
- Subdivision: replace an edge of length s+t by two edges of lengths s and t and a new degree-two vertex. Sum over the new vertex's label. The result must equal q_T, for every assignment of all remaining labels and every collection of other branches attached to the endpoints.
- Path data: if T is a path with successive lengths t_1,...,t_k, its label law equals p at times 0,t_1,t_1+t_2,...,t_1+...+t_k.

The one-vertex probability vector is the one-time law of p. Leaf deletion implies consistency on every connected subtree. Unobserved interior vertices are handled by summing their labels; they are not deleted with a changed metric except through the subdivision rule.

There are countably many variables and constraints. Each individual constraint involves finitely many variables and is affine with rational coefficients, except for the supplied path probabilities on its right-hand side. All unknowns lie in [0,1].

The extension variables are mathematical witnesses. A passive source does not supply independent branches, hidden-state resets, or preparations. An inference procedure may optimize over q_T without physically acquiring a branching experiment.

## 3. Countably colored tree representation

Let C be a finite or countable set of edge colors. Take a countable tree U in which every vertex has countably infinitely many incident edges of each color. Every finite C-colored tree embeds in U. A consistent isomorphism-invariant family q_T produces an Aut(U)-invariant label process Y on U by Kolmogorov consistency.

At a vertex v and a color c, enumerate its c-neighbors. The full label arrays in the corresponding components of U minus v form an exchangeable sequence, conditionally over Y_v. There is one random directing measure D_{v,c} per color. Joint separate exchangeability implies that all the branches, across all colors, are conditionally independent given

    G_v = sigma(Y_v, D_{v,c}: c in C).

One way to see the joint assertion is to average a product of finitely many branch-cylinder functions over independent permutations of the finitely many involved color families. The empirical means converge to the corresponding directing integrals. Conditional expectation against every bounded function of the directing records and Y_v then gives the product formula. Countably many colors require only these finite-family assertions.

The directing record is unchanged when finitely many branches of any color are removed. Consequently, if w lies in one component after v is deleted, G_w is measurable using labels entirely within that component: in defining every directing measure at w, omit its single branch leading back toward v. This is the locality step that makes neighboring hidden records conditionally independent across a cut.

The labels used to identify rooted branches must not become a hidden orientation or parity variable. This can be handled by the same labeling-independence argument as in Aldous's Lemma 13.6 and proof of Theorem 13.5. Equivalently, choose the hidden record X_v as Y_v together with the conditional probabilities of all finite rooted colored label patterns, conditional on G_v. There are countably many such patterns. Automorphisms supported inside one branch leave G_v unchanged, since the other infinitely many branches still determine its directing measure. Rooted isomorphism types therefore give common versions of the record. A countable subgroup mapping all finite patterns and all directed colored edges suffices to remove exceptional-set issues.

These pattern coordinates generate G_v modulo null sets: conditional expectations of cylinder functions generate any sub-sigma-field of this countably generated label space, and every finite cylinder is a marginal of a finite rooted tree cylinder. Hence X_v takes values in a standard Borel space X and generates G_v. It is carried to X_{gv} by every required color-preserving automorphism g, with no extra state involution.

The branch locality and conditional independence now imply the tree Markov property for X. All X_v have one marginal mu. Across an edge of color c, their joint distribution is symmetric, because a color-preserving automorphism interchanges the endpoints. Disintegrate that joint law to obtain a mu-reversible Markov kernel K_c. Every colored path law, and indeed every colored tree law q_T, is generated by these kernels and the deterministic readout Y_v = g(X_v).

### The dense branch algebra

For each finite rooted colored label pattern T, let f_T(x) be its conditional probability given the root state x. Include patterns with an unobserved root. Their functions are bounded in [0,1].

Conditional independence of distinct root branches shows that f_T f_U is the function of the rooted tree obtained by gluing the roots while placing their branches in disjoint slots. Conflicting prescribed root labels give zero. The linear span B of these functions is therefore a unital algebra. It contains the observation indicators and is invariant under each K_c: add an unobserved new root joined to the old root by an edge of color c.

By the definition of X_v, the functions f_T generate its sigma-field. The bounded monotone-class theorem therefore makes B dense in L2(mu). This density is needed below; merely using the linear span of unbranched future-word features would not suffice.

## 4. Subdivision forces one semigroup

Apply Section 3 with colors C = positive rationals, interpreted as edge lengths.

Fix rooted patterns T and U, with conditional functions f and g. Connect their roots by an edge of length s+t. Its observed probability is

    <f, K_{s+t} g>_mu.

Subdivide the connecting edge into lengths s and t, leaving the new middle vertex unobserved. The tree Markov representation gives

    <f, K_s K_t g>_mu.

The subdivision constraint makes these equal for every such f,g. Density of the branch algebra and boundedness of the operators imply

    K_{s+t} = K_s K_t,  s,t > 0 rational.                 (1)

Set K_0 = I. Each K_t is selfadjoint and Markov. In addition, K_t = K_{t/2}^2 is positive semidefinite as a Hilbert-space operator. Let A_1 = K_1. Unique positive operator roots give

    K_{m/n} = A_1^{m/n}, m,n positive integers.            (2)

The spectrum of A_1 lies in [0,1]. Formula (2) defines K_t for every positive real t by spectral calculus, with 0^t interpreted as zero. Strong limits from rational times preserve positivity on functions, the constant one, stationarity, and selfadjointness. Thus these are reversible Markov operators.

At zero the strong limit is the spectral support projection

    P = 1_{(0,1]}(A_1).                                  (3)

It need not equal I without a continuity assumption. This possible instantaneous loss of state information is not silently identified with finite-rate motion.

## 5. Stochastic continuity removes the instantaneous projection

Assume now that the observed process p is stochastically continuous. Write e_a = 1_{g=a}. Then

    <e_a, K_t e_a> = Pr(Y_0=a,Y_t=a) -> Pr(Y_0=a)

as rational t decreases to zero. Contractivity implies

    ||K_t e_a-e_a||_2^2
    <= 2[||e_a||_2^2-<e_a,K_t e_a>] -> 0.

Hence P e_a = e_a.

The range of P is closed under products of bounded functions. Indeed P is a positive, unital, stationary orthogonal projection. For bounded f with Pf=f, Markov Jensen gives P(f^2) >= f^2. Both sides have the same integral, so equality holds almost surely. Polarization gives closure under products.

For every t>0, K_t f belongs to the range of P. Every rooted-pattern function is recursively obtained from observation indicators by applying K_t and multiplying branch functions. It therefore belongs to the range of P. Density of B forces P=I.

Consequently K_t is strongly continuous at zero, and hence at all times. It is a reversible Markov semigroup on the standard Borel probability space. Positive, stationary Markov operators on this space admit regular kernels; their integrated semigroup identities define the stationary hidden finite-dimensional distributions. The observation has exactly p's rational-time law.

This establishes a semigroup realization. It does not specify a regular hidden topology, pure-jump paths, finite activity, or a particular laboratory state representation.

## 6. Approximation by finite reversible CTMCs

This step applies even when P in (3) is not I.

For positive rational delta, define the bounded generator

    B_delta = (K_delta-I)/delta.

It is a conservative reversible jump generator on the abstract state space: its semigroup is the Poisson mixture

    exp(t B_delta)
    = exp(-t/delta) sum_{m>=0} (t/delta)^m K_delta^m/m!.

For every t>0, spectral calculus gives strong convergence

    exp(t B_delta) -> K_t as delta decreases to zero.     (4)

For a spectral value lambda>0 this is the scalar limit

    exp[t(lambda^delta-1)/delta] -> lambda^t.

For lambda=0, the left-hand side is exp(-t/delta), which also tends to zero. Dominated convergence proves (4). No uniform generator bound is inferred.

Choose finite measurable partitions F_n of X which refine the observation partition, increase with n, and generate the hidden sigma-field modulo mu-null sets. Let E_n be conditional expectation onto F_n. Then E_n converges strongly to I. Define the finite transition matrix

    T_{delta,n}(i,j)
    = mu(A_i)^{-1} integral_{A_i} K_delta(x,A_j) mu(dx).

Discard zero-mass cells. T_{delta,n} is stochastic and reversible for the cell masses. The finite generator

    Q_{delta,n} = (T_{delta,n}-I)/delta                  (5)

has nonnegative off-diagonal entries, zero row sums, and maximum escape rate at most 1/delta.

For fixed delta, the lifted bounded operators E_n K_delta E_n converge strongly to K_delta and have norm at most one. Their exponential series therefore show that the finite semigroups in (5), embedded in L2(mu), converge strongly to exp(t B_delta). The harmless orthogonal-complement part can be assigned generator -I/delta; its contribution disappears because E_n tends to I.

Observation multipliers commute with E_n because the partitions refine the sensor. A finite word probability is an inner product of a finite product of observation multipliers and transition operators. Uniform boundedness and successive strong convergence give convergence of every finite list of word probabilities.

For a specified finite cylinder list and accuracy, first choose delta small enough in (4), then n large enough for the compression approximation. Diagonalization over the countable rational-cylinder list gives finite reversible CTMC outputs converging to p.

This is an existence proof with the full preparation interface visible: it requires the abstract kernels K_delta and sensor-refining conditional expectations. It is not an acquisition algorithm from a finite passive record. The proof supplies no useful rate of convergence, dimension bound, precision cost, or mixing guarantee.

## 7. The opposite implication

Each finite reversible CTMC with stationary pi and generator Q defines a tree law by choosing a root with law pi and propagating exp(tQ) independently along edges of length t. Detailed balance makes this law independent of the chosen root. Its observed tree laws obey all four requirements in Section 2.

Suppose finite reversible CTMC output laws converge to p on rational cylinders. Enumerate the countably many finite rationally lengthed trees and their finite label tables. These tables lie in a compact product of simplices. A diagonal subsequence has a limit q_T for every T.

Normalization, isomorphism, leaf marginalization, and subdivision are finite linear identities and pass to the limit. The path marginals converge to the stipulated law p. Thus p has the required metric-tree extension.

Together with Section 6, this proves the closure equivalence in Section 1. Section 5 gives the additional exact strongly continuous semigroup when p is stochastically continuous.

## 8. Complete finite obstructions, without a complexity claim

Enumerate all variables and constraints in Section 2 and form increasing finite subsystems. Each is an LP over nonnegative probability tables. The full system is feasible if and only if every finite subsystem is feasible: all coordinates lie in [0,1], all constraints are closed, and compactness gives the finite-intersection implication.

Therefore a process outside finite reversible CTMC closure fails some finite LP. Farkas duality gives a linear inequality in finitely many supplied observed cylinder probabilities. Since all structural coefficients are rational, a separating dual can be chosen with rational coefficients after retaining a strict margin. Summing over a common observation-time grid turns the inequality into the expectation of one bounded finite-word statistic.

This is stronger in scope than enumerating capped hidden generators and solving a nonconvex model fit. It does not prove lower total computational or acquisition cost for any task. The tree tables grow rapidly, and positive instances need not have a finite stopping certificate. With approximate data, all input intervals must be propagated through the feasibility problem; selecting a witness from data requires valid held-out or simultaneous inference.

The branching variables are not additional samples. They are latent positive extension variables constrained by acquired path data. A failure is an observational inconsistency certificate; a feasible finite level is not a prepared simulator.

## 9. Finite-state realization is a further algebra condition

For a given compatible tree extension, form the root connection matrix

    M(T,U) = E[f_T(X) f_U(X)].

Its rank is the dimension of the branch algebra B in L2(mu). If this rank is finite r, B is a finite-dimensional unital algebra of bounded real functions. It is therefore the full algebra of functions constant on r measurable atoms, after null sets are discarded. The observation indicators belong to B and every K_t preserves B. They descend to reversible r-state stochastic matrices.

When p is stochastically continuous, Section 5 gives a continuous finite-dimensional semigroup, hence an ordinary finite CTMC generator. Thus finite branch-algebra rank of a compatible metric-tree extension is sufficient for exact finite-state realization, and a realization with N states has connection rank at most N.

This is connection-algebra machinery, closely related to classical graph-homomorphism representation arguments. It is not a claim that observed linear Hankel rank or reflected-history rank bounds the hidden state count. The extension itself is additional structure.

## 10. Astra collision and current status

Current Astra N507 already supplies a ten-state rational observed process with common ten-atom CP factorizations for every reflected-history table, while a finite observed inequality excludes every standard-Borel reversible hidden realization and its finite-dimensional-distribution closure. Its governing proof and current notices were fetched in full at revision 3e2cb7095bf53339c2249f35d182af62d324f95b.

N507 is source-reported and internally reviewed in its preserved record, not externally validated. Its principal proof uses a forward-invariant but nonreducing observable subspace and a dynamically impossible symmetric coupling of rigid positive feature points. The complete metric-tree hierarchy must reject it at a finite level; this note does not identify the first rejecting level or promise an efficient computation.

The earlier projective CP gluing lemma and infinite-mixture finite-state separation in the same source compilation are prior Astra constructions. They are retained at their actual scope. A separate simple ergodic bounded-rate countable-state example may clarify the finite-state boundary but does not replace the N507 obstruction.

Proof obligations checked in this draft: edge-color exchangeability, hidden-state locality, dense branch algebra, subdivision-to-semigroup implication, the possible zero-time projection, its removal by observed continuity, and two-stage finite-CTMC approximation. Independent root review remains necessary for new load-bearing uses. No physical experiment or source-access advantage has been asserted.
