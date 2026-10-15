# Binary-only scalar-resolvent learning: algorithmic prior-art audit

Date: 2026-10-15. Scope: primary-source public reading; no outreach or downloaded-code execution. Read the supplied generic binary theorem and measured-data gate. No claim of exhaustive literature coverage or novelty determination.

## Bottom line

I found no established polynomial-time exact learner for the unrestricted target g(S)=a_S^T(I+B_SS)^(-1)1 from Boolean subset responses alone. The strongest new comparator is the 2026 polynomial-time read-once determinant / black-box principal-minor-assignment algorithm. It does not close the gap: it learns a determinant polynomial from field-valued evaluations, whereas this oracle gives ratios of determinants only on Boolean inputs. The most directly implementable binary-only comparator remains nonlinear physical-model fitting, already experimentally demonstrated by Sol et al. A fixed iteration budget has polynomial computational cost; a polynomial-time global-recovery guarantee is a different, unestablished statement.

The generic response-field theorem remains useful as a query-complexity existence result. None of the sources below turns its field-membership/configuration-selection step into a polynomial-time operation for this interface.

## 1. Strongest exact comparator: 2026 read-once determinants

Aravind, Chatterjee, Ghosh, Gurjar, Raj, Saha, “Learning Read-Once Determinants and the Principal Minor Assignment Problem.” Primary full text: https://eccc.weizmann.ac.il/report/2026/035/download/ ; record: https://arxiv.org/abs/2603.04255 .

Theorem 1.1 assumes |F|>n^6, unit-cost field operations, and efficient square-root computation. It gives randomized polynomial-time proper learning of rank-one symbolic determinants and black-box det(A+diag(y)) learning. Theorem 1.4 separately reconstructs any property-R matrix from principal minors of order ≤4 in polynomial time. Algorithms 5, 7, 9 perform cut finding, no-cut reconstruction, and decomposition; pair/triple constraints produce quadratic candidates, checked using order-four minors. General matrices are reduced to property R using random diagonal shifts and inversion. Section 4.2, Lemma 4.3 explicitly evaluates at translated and inverted field inputs. Section 2.6 repairs zero inverses by univariate interpolation at d+1 distinct nonzero field values.

Transfer: the order-four reconstruction/cut algorithm is a concrete backend if the necessary principal-minor oracle can be constructed. Missing: neither determinant values nor arbitrary translated/inverted input evaluations are available from g(S). The generic property-R backend avoids arbitrary-field plant queries only after principal minors have been obtained. The theorem is exact algebraic learning, not a finite-noise guarantee or bit-complexity bound.

## 2. Quadratic-query exact/noisy principal-minor recovery

Brunel and Urschel (2024), “Recovering a Magnitude-Symmetric Matrix from its Principal Minors.” Primary full text: https://arxiv.org/html/2404.06302v2 ; DOI https://doi.org/10.1016/j.laa.2024.09.004 .

For real magnitude-symmetric matrices satisfying their four-cycle genericity Condition 1, Theorem 2 gives polynomial-time RecoverK using O(N²) principal-minor queries, possibly of order growing with graph invariant phi_G. It learns a principal-minor-equivalent representative, not necessarily the original matrix. Theorem 3 assumes bounded minors, edge separation alpha, additional margins beta/gamma, and absolute minor error delta < alpha min{alpha^(3 phi_G), beta^(3 phi_G/2), gamma}/100. It yields representative error at most 3 delta/(2 alpha), with O(N²) queries and polynomial runtime. Thus required precision can be exponentially severe in graph structure. The algorithm recovers magnitudes/edge charges from one- and two-minors, then signs through a positive-cycle basis.

Transfer: concrete graph-aware query selection and explicit separation/precision accounting. Missing: our scalar oracle does not provide these minors; arbitrary B is not magnitude-symmetric. Reciprocity of an original physical matrix does not by itself establish that a chosen normalized B, or an augmented response matrix, meets every hypothesis.

## 3. DPP learning is a different observation model

Urschel, Brunel, Moitra, Rigollet (2017), “Learning Determinantal Point Processes with Moments and Cycles.” Primary: https://proceedings.mlr.press/v70/urschel17a/urschel17a.pdf .

Independent random subsets Y drawn from a DPP give empirical inclusion moments P(S subset Y)=det(K_SS). The algorithm estimates diagonal/magnitude terms, recovers the graph, computes a short cycle basis, estimates cycle moments, and solves sign constraints. The advertised fixed-cycle-sparsity sample complexity contains an exponential-in-cycle-length term (C/alpha)^(2 ell), plus log(N)/(alpha² epsilon²); runtime is polynomial in sample count and N. Thus “polynomial time” does not remove the large precision/sample requirement for unbounded cycle length.

Transfer: use cycle complexity and entry separation as explicit model restrictions rather than genericity alone. Missing: querying our system on a chosen subset is not observing a DPP sample. Its scalar responses are neither probabilities nor inclusion moments. There is no legitimate empirical-moment estimator for principal minors from these responses without an additional reduction.

Related primary source: Brunel (2018), signed DPP learning, https://papers.nips.cc/paper/7966-learning-signed-determinantal-point-processes-through-the-principal-minor-assignment-problem.pdf . It treats K_ij=±K_ji; the 2024 result above is the more useful sparse/noisy comparator.

## 4. Older general PMAP

Griffin and Tsatsomeros (2006), “Principal minors, Part II: The principal minor assignment problem,” https://www.sciencedirect.com/science/article/pii/S0024379506002138 ; DOI https://doi.org/10.1016/j.laa.2006.04.009 .

The publisher abstract describes recursive reconstruction from principal submatrices and Schur complements, a sufficient success condition, and a polynomial-time variant exploiting overdeterminancy. This is a principal-minor-input algorithm, not a scalar-ratio learner. The 2026 paper explicitly distinguishes its property-R assumption from the older off-diagonal-full genericity assumption. I inspected the publisher abstract and that primary comparison, not the complete 2006 article; do not infer a stronger oracle guarantee from this entry.

## 5. Rational interpolation: two separate pitfalls

Grigoriev and Karpinski, “A Deterministic Algorithm for Rational Function Interpolation,” primary report: https://theory.cs.uni-bonn.de/ftp/reports/cs-reports/1985-1989/8526-CS.pdf . The stated polynomial/NC result is for t-sparse numerator and denominator with degree/coefficient bounds. The word “Boolean” in its complexity statement refers to Boolean parallel computation, not an oracle restricted to {0,1}^m. Generic determinant expansions have exponentially many monomials, despite a compact matrix representation. Sparsity-polynomial complexity therefore need not be polynomial in m.

Bshouty, Hancock, Hellerstein, “Learning Arithmetic Read-Once Formulas,” primary publication: https://doi.org/10.1145/129712.129747 . Its randomized substitution algorithm uses large/infinite fields; small-field results involve equivalence queries. A variable appearing once in a determinant matrix does not mean its polynomial has an arithmetic read-once formula. Neither that structural condition nor an equivalence oracle is supplied here.

I found no primary theorem in this targeted search that removes both the Boolean-input restriction and determinant-ratio difficulty for our class.

## 6. Binary metasurface fitting: strongest immediate practical comparator

Sol, Prod’homme, Le Magoarou, del Hougne (2024), “Experimentally realized physical-model-based frugal wave control in metasurface-programmable complex media.” Primary: https://pmc.ncbi.nlm.nih.gov/articles/PMC10987616/ .

This experiment uses 68 binary meta-atoms and a compact inverse-interaction-matrix model. Random configurations calibrate even a single complex S31 channel. Methods specify random parameter initialization, Adam, batch size 1000, initial step 10^-2, 8/9 training split, and validation-based stopping/restoration. Matrix inversions exploit block structure. The single-S31 result at 40,000 examples reports 23.4 dB prediction metric; the much smaller 398-configuration example uses the full scattering matrix and must not be advertised as scalar-only acquisition. Nonunique parameters are explicitly acknowledged. These are empirical predictive results, not a global polynomial-time identifiability theorem.

Transfer: direct rational forward-model fitting with independent heldouts and identical scalar/query budgets. Missing: raw data and independent calibration/noise records described in the supplied measured gate remain unavailable; fitting itself supplies no uniform exact/noisy recovery guarantee.

## 7. Exact algebraic interface audit (our derivation)

Let A=I+B, and introduce the (m+1)-square bordered matrix

    M = [ 0  a^T ; 1  A ].

For each S, its principal submatrix indexed by {0} union S satisfies

    det M_{0 union S} = -g(S) det A_S.

Thus the oracle gives a ratio of two linked families of principal minors, not either family separately. Alternatively, for X=diag(x),

    Q(x)=det(I+B X),
    R(x)=det(I+(B-1 a^T)X),
    1-g(S)=R(1_S)/Q(1_S).

Both Q and R are multilinear determinant polynomials. Their ratio on the cube is not a multilinear polynomial. Consequently, multilinear interpolation cannot extend g to arbitrary-field values. Even if Q/R were known on all vertices, choosing their structured off-cube extension is another identification issue.

A two-control example makes the missing information explicit. Set a=(1,1), B_12=b, B_21=c. Then

    g({1,2})=(2-b-c)/(1-bc).

The two choices (b,c)=(1/5,1/3) and (b,c)=(1/10,23/59) have identical singleton values and g({1,2})=11/7. Their determinants det A_{12}, however, are 14/15 and 567/590, respectively. All subset matrices are nonsingular and both directed edges are nonzero. Hence even the complete two-bit response table does not determine the original det A_{12}.

This rules out a universal operation that recovers the actual denominator-minor oracle from the response table. It does not rule out finding some equivalent response realization, nor a polynomial-time learner for larger generic m. A valid PMAP reduction must construct a compatible representative rather than assume its true minors were measured.

## 8. Actionable next operation, and honest stopping point

Practical: implement the normalized rational model directly. Baseline/singletons identify f0/a; optimize B against measured binary responses, with B_ii fixed to zero, multiple restarts, and independent random joint-support heldouts. For each S solve A_S x=1 and A_S^T y=a_S. Then

    partial g(S)/partial B_ij = -y_i x_j  (i,j in S, i!=j),

so one forward and one transpose solve supply the complete gradient for that observation. Complex data require the corresponding real-coordinate/Wirtinger treatment. A fixed-budget fit is implementable with polynomial work per iteration and predicts a target in O(m³), but convergence or heldout success is not a uniform theorem. Charge baseline/singletons, repeats, restarts, and heldouts honestly.

Theory: formulate a “linked principal-minor ratio assignment” problem for the bordered M above. The precise desired new operation is: from polynomially many ratios det M_{0S}/det M_S, construct in polynomial time any M' of the compatible border form whose ratios agree for every S. The 2026 cut/quadratic-candidate machinery is a plausible backend only after proving a ratio-to-compatible-minors step; the two-bit ambiguity explains why recovering the original minors is the wrong goal. No such step was found or proved in this review.

Do not replace this gap with arbitrary amplitudes, determinant access, DPP samples, an equivalence oracle, or exponential sparse-interpolation input size. The best present conclusion is a concrete experimental fitting baseline plus a sharply isolated algebraic subproblem, not a new certified binary acquisition algorithm.
