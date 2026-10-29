# Collective Schur extraction of unknown dark-direction programs

2026-10-29. Author construction, independent receiving review requested. This strengthens the rare eight-record exterior event by using all available label records coherently. It does not assume iid records for correctness; an explicitly separate iid example supplies a finite-call success bound.

## Input contract
Let V=C^d, here d=9, and let c be one fixed unknown unit vector. Put W=c-perp, dim W=d−1. N protected quantum records have an arbitrary joint positive state omega on V^tensorN tensor B, supported on W^tensorN tensor B. B includes retained bath, all earlier references and records, with arbitrary correlations. The accepted full-joint commutator acquisition supplies this support with c=vec(R)/sqrt(3), real up to phase, for a fixed unknown R in SO(3). Each record is an actual minus outcome; plus outcomes, source calls, protected storage and control are paid.

## 1. Partition measurement and a directly heralded program count
Apply the standard U(d)×S_N Schur transform to the records and measure the partition lambda. Keep the representation register Q_lambda and all multiplicity/reference registers as junk; no product-state assumption is made. Outcomes with more than d−1 rows have probability zero under the exact support promise. Define k=lambda_(d−1). The theorem is:

**There is a known isometry, depending only on lambda, that converts Q_lambda into k pure copies of |conj(c)> and junk, exactly decoupling those copies from B and all junk.** If k=0 it returns no program. The measured k is an actual program count, not an inferred spectral gap or a promise of future occupation.

## 2. Proof by nonnegative weights and inverse fundamental CG steps
First choose coordinates W=span(e1,...,e_(d−1)). In the polynomial tensor representation, the number operator N_d counting occurrences of basis vector e_d is nonnegative. The Schur transform acts equivariantly, so on the lambda block N_d acts only on Q_lambda. Its zero eigenspace is precisely Q_lambda(W), the polynomial U(d−1) irrep of shape lambda, provided lambda_d=0. This can also be seen from U(d)→U(d−1) interlacing: zero last-coordinate weight forces the restricted shape to have the same number of boxes, hence to equal the first d−1 rows. Arbitrary correlations with multiplicity and B do not alter this support statement.

Let rect=(k,...,k,0), with d−1 copies of k. It is a subdiagram of lambda. Choose a deterministic legal corner-removal path from lambda down to rect, never removing a box of rect. At each step use the inverse fundamental Clebsch–Gordan isometry
 Q_lambda_current -> Q_lambda_previous tensor V,
corresponding to the selected predecessor. This is a norm-preserving branch of the known CG UNITARY, specified by the predecessor label; it is not a postselected unknown map. Fundamental tensor products are multiplicity-free. The isometry intertwines U(d), so it preserves total N_d. Each output factor has nonnegative N_d. An input with N_d=0 therefore gives both the remaining representation and the peeled qudit zero N_d. Iterate. There are N−(d−1)k steps, at most N.

The surviving register lies in Q_rect(W). That U(d−1) representation is det(W)^k and has dimension one. Thus the full state factorizes on the surviving register, even if every input record was correlated with the bath. For general W use U(d) covariance; the surviving ray is the orbit of the canonical rectangle highest-weight ray.

## 3. Explicit rectangle-to-symmetric-dual conversion
As a U(d) representation,
 Q_(k^(d−1),0)(V) = det(V)^k tensor Sym^k(V*).
The determinant factor is a global phase. Under this known unitary identification the one-dimensional Q_rect(W) ray is |conj(c)>^tensork in the symmetric dual tensor space. No complex conjugation of an arbitrary supplied state is being performed: the conjugate ray was encoded in a different, known representation built from the records.

An efficient basis identification is explicit in the standard Gel'fand–Tsetlin gauge with positive simple-root matrix elements. The rectangle GT patterns have row j equal to (k repeated j−1 times, t_j), for1<=j<d, with k=t_0>=t_1>=...>=t_(d−1)>=t_d=0. Set occupation a_j=t_(j−1)−t_j, so a_j>=0 and sum a_j=k. Rectangle weights are k−a_j. Map the GT basis to symmetric occupation |a> with the known phase (−1)^(sum_j j a_j). The phase converts positive simple-root coefficients sqrt(a_j(a_(j+1)+1)) into those of the dual representation. This is a reversible integer relabeling plus a parity phase, not an unknown-frame operation. Finally apply inverse symmetric Schur encoding for partition(k), whose multiplicity is one, to produce k physical d-level program registers. On the surviving ray these are literally a product of k identical pure programs, decoupled from all other systems.

## 4. Known control implementation and its actual scope
Bacon–Chuang–Harrow's primary construction gives Schur and fundamental CG circuits; Eq32 of their full paper identifies inverse CG branches with normalized isometric intertwiners, and Eq33 gives the one-box rule. The present decoder uses the standard Schur transform, at most N inverse fundamental CG steps, reversible rectangle-basis arithmetic and a symmetric inverse Schur transform. It does NOT call a generic arbitrary-irrep tensor-product oracle, source inverse, controlled unknown channel, purification oracle or environment tomography.

Primary source read: *The Quantum Schur Transform: I. Efficient Qudit Circuits*, https://arxiv.org/pdf/quant-ph/0601001 , especially sectionsIV–V, Eq32–33, and the explicit circuit-complexity statement in the introduction. Their approximate compiler has size N poly(d,log N,log(1/epsilon)); its known-unitary inverses have the same scope. We rely on these established primitives, not claim to invent the Schur transform.

The ideal exact isometries govern this theorem. Finite gate synthesis, all protected memory, preparation/routing/readout and calibration costs are required. A compiler approximation gives an additive JOINT instrument error by ordinary channel composition; conditioning on a rare output may enlarge normalized error. No exact finite Clifford+T realization of arbitrary algebraic CG coefficients, practical hardware gate count or noise tolerance is asserted. An actual native circuit for d9 and hundreds of records has NOT been executed here.

## 5. Correlated sources versus iid yield
For arbitrary correlated records the theorem guarantees correctness conditional on the observed k, not that k is positive. A source may repeatedly produce labels in a common smaller subspace, or identity may produce no minus labels at all. No reset, occupation gap, independent-copy premise or unconditional positive rate is hidden in the statement.

For an IID label state sigma supported on W, with nonzero eigenvalues p1,...,p_(d−1), Schur partition probability is f_lambda s_lambda(p). It is equivalently the RSK shape distribution of an iid word with those letter probabilities. This equivalence follows from the RSK bijection between words and a semistandard insertion tableau plus standard recording tableau: the weighted insertion-tableau sum is the Schur polynomial and the recording count is f_lambda.

For d−1=8, lambda8>=1 iff the word contains a strictly decreasing subsequence of length8, necessarily the full reversed alphabet. The waiting time for its greedy completion is a sum of eight independent geometric waiting times with parameters p8,...,p1. Thus its cumulative probability is exact. Completing k such full decreasing subsequences in succession is sufficient for lambda8>=k: the k disjoint subsequences have union size8k, and Greene's decreasing-subsequence invariant equals the sum of the first k column lengths, each at most8. This gives a rigorous, possibly conservative lower bound for k>1.

## 6. Exact finite-call example, no hidden waiting time
Use the memoryless two-axis collective source of the preceding kernel-program packet, with any fixed unknown local twist. H has spectrum{0,1/2×3,1×2,3/2×3}, and the minus probability is4/9. The conditional minus-state eigenvalues are {1,1,1,2,2,3,3,3}/16. Each ORDINARY source call therefore advances the next symbol in the greedy full-decreasing-subsequence process with probability {1,1,1,2,2,3,3,3}/36, including plus outcomes as no advancement. The source is memoryless only in this example; the unknown eigenbasis is irrelevant because partition probabilities are unitarily invariant.

`exact_renewal_bound.py` performs integer dynamic programming, not floating tail fitting. With a fixed576 source-call budget, the probability of at least TWO extracted programs is at least0.9737402949272663. At512 calls it is at least0.9280742951439552. At1024 calls, at least FOUR programs occur with probability at least0.9765548339473412. These bounds are on the ideal Schur protocol for this specified informative iid family, not arbitrary causal noise.

Using the separately checked two-program-to-four-quaternion contraction of the preceding packet would then give a one-use exact unknown-frame gate with additional probability(16/27)*(1/4), hence at least about0.14426 in576 calls if that extension and the present theorem are independently accepted. This is an ideal finite-call capability, not a practical resource advantage. All gate failures remain heralded and can damage an unknown input; full encoder/recovery composition must account for them.

## 7. Executed checks and unresolved obligations
`check_qutrit_collective_decoder.py` constructs the complete d3,N3,lambda(2,1) instrument using two orthogonal irrep copies. Its effect equals I−P_sym−P_antisym; it extracts a pure conjugate dark vector from arbitrary entangled bath fixtures, with IID rank2 success1/2. This is a dense nontrivial collective-decoder diagnostic, not an implementation of the entire d9 compiler.

`sample_iid_schur_counts.py` gives seeded RSK Monte Carlo (10000 trials/model) for IID rank8 and the two-axis spectrum; these samples are not quantum circuit executions. At128 minus records the two-axis sample has success frequency0.933 and mean program count2.21; at256 it has mean7.4773. Exact dynamic-programming bounds, not zero observed failures, govern any rigorous yield statement.

Remaining: independent representation/dual-phase/finite-control review; full d9 circuit compilation and joint error budgets; realistic protected-memory and coherence costs; extension beyond an exact shared dark direction; stronger equally informed quantum processing comparisons; historical novelty. The accepted gap-free classical controller remains a different fallback when no programs are produced.
