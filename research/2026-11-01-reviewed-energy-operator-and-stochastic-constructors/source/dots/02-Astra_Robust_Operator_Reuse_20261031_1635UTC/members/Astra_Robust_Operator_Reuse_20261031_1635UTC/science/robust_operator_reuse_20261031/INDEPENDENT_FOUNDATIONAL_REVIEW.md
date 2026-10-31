# Independent review: task-sensitive stable operator reuse

Verdict: scoped mathematical and research-prototype PASS for the frozen exact-input construction. The uniform scalar certificate, common-metric acquisition, finite-horizon validation barrier, saved modular witness and repaired executable verifier check out. This is ordinary retained bidirectional Krylov/model reduction with an observable-sensitive certificate, not a demonstrated advantage over equally informed retained methods or a limitation on learning generally. No imperfect-observation extension is included in this receipt.

Review date: 2026-10-31. Both proof bodies and all frozen code listed in the binding table were read in full. Author files and saved reports were not edited by the reviewer. Tests that write relative files were run in a temporary working directory; comparison reruns imported their functions without replacing frozen reports.

## 1. Acquired metric and contraction

The raw interface is a finite explicit family of rational row-stochastic matrices and rational task vectors. The stationary vector is not supplied as privileged information: the program solves the stationary nullspace of A0, requires uniqueness and strict positivity, normalizes it, and checks stationarity for every other generator. Failure means this route is inconclusive, not that no compression exists. Rational input inspection and linear algebra, including the conditioning/bit cost of a small pi_min, are real work.

Jensen's inequality and common stationarity establish contraction in H=diag(pi). Stochasticity alone does not establish Euclidean contraction; the code and tests correctly keep that distinction. H^{-1}A^T H is the actual weighted adjoint and a contraction in the same metric. Nonreversibility is allowed.

Including the constant vector in the learned span is essential to the minorization proof. The acquired d=min A_ij/pi_j lies in [0,1]. Subtracting d times the stationary reset kernel and dividing by 1−d produces another stationary stochastic contraction when d<1. Every Q vector has zero stationary mean, yielding ||QAQ||_H<=1−d. At d=1 it is the complement dynamics that vanishes, not necessarily the complementary vector space. At d=0 the quadratic-in-length certificate remains valid. No spectral-gap oracle is assumed.

## 2. Uniform two-sided observable bound

P is the H-orthogonal projection onto the rational learned space containing b and c. For the full contractive word trajectory, ||p_t||_H<=||b||_H. The complement recursion therefore gives ||q_t||_H<=e_in||b||_H sum_{j<t}alpha^j. The lifted compressed trajectory remains in P; subtracting its recurrence from that of p_t leaves the P-block propagation plus PAQ q_{t−1}. Since the P block is contractive, summing and pairing with c proves exactly

    |c^T H A_w b − v^T G B_w u|
       <= ||b||_H ||c||_H e_in e_out S_l(alpha).

No positive two-sector comparison exponential is needed. The empty/one-letter cases have S_l=0 and are exact for this task. S_l(1)=l(l−1)/2, S_l(0)=max(l−1,0), and the gap bound S_l(alpha)<=(l−1)/(1−alpha) is correct for alpha<1 and l>=1.

The executable residual sums are weighted-coordinate Frobenius upper bounds on the actual block operator norms. They are computed from all basis directions and all generators, including adjoints; they are not random-probe norm estimates. The AGM product bound k=(in2+out2)/2 is sound, and its squared admission test is exact rational arithmetic. It is conservative, not optimal: an equally informed method could directly use in2*out2 in a squared product certificate, or an acquired PSD/operator-norm bound. No claim that the chosen stopping rule is best follows.

The two-dimensional symmetric-contraction example has the stated eigenvalues and fixed-length leading error e^2 S_l(1−g). It demonstrates the quadratic coefficient and horizon limitation for the contraction theorem. It is explicitly not a row-stochastic example with a retained constant mode. The certificate is uniform over every word within the declared horizon, so later adaptive choices among those words do not create a statistical failure probability. Aggregating many scalar errors into a different consumer objective would still require its own error accounting.

## 3. Actual acquisition and executable verifier

The learner starts from 1,b,c, removes exact dependencies, and retains both forward and weighted-adjoint images of each new basis vector. Exact H-orthogonalization and rational rescaling preserve the span and metric identities. A failed certificate with nonzero residual can append a new independent direction; full dimension gives zero residual. Thus there are at most n basis columns. The claimed 2mr generator/adjoint vector products for final rank r is correct for the learner's retained-image path, but does not count repeated residual arithmetic, metric acquisition, orthogonalization or verification as free.

The final verifier independently recomputes the metric, Gram matrix, positive orthogonal basis, inclusion of 1,b,c, reduced matrices, leakage sums, gap and error bounds. It now REQUIRES caller-supplied expected_length and expected_tolerance and compares the record against them. A record for an easier task is no longer accepted as admission for the requested task. Matrix rational pairs use exact integer types, positive denominators and reduced fractions; bool/float aliases are rejected there. Zero observables are now admitted as trivial scalar tasks. Malformed ordinary inputs tested by the suites return rejection rather than being treated as a certificate.

The verifier intentionally does not certify timing, ledger counters, discovery history or optimality. Its conclusion is the mathematical property for the supplied exact matrices/task, not truth of an empirical physical model. It uses ordinary Python/SymPy exact arithmetic with assertions enabled; the reviewed execution is not Python −O and is not a hardened resource-limited network parser. Exact future queries return rationals; any later decimal approximation needs its own output-rounding budget.

Two review findings were repaired before freeze: the original verifier only certified the task declared by the record, and the modular routine lacked an unrestricted overflow guard. The original default modular fixture was safe, but general input size/prime was not automatically safe. The final API binds the external task; the final witness routine validates primality and d(p−1)^2<=int64_max before its modular products. Denominators must be invertible modulo p. The representation-bit field was also corrected: max_representation_entry_bits is distinct from the scan of serialized rational fields, and neither is claimed to instrument every intermediate allocation.

## 4. Full-algebra witness and separate uniform-validation barrier

The saved perturbed fixture's witness has 121 independent word matrices modulo prime 1,000,003 on the 11-dimensional mean-zero restriction. I independently replayed every word and elimination using unbounded Python integers, rather than relying on NumPy int64. All 121 pivots were present. Invertible rational denominators and full modular rank imply full rational rank. This is full M_11 on the mean-zero space, NOT full M_12: the stochastic constant direction is retained. Failure to find full rank is not promoted to a general negative certificate.

The barrier proof concerns a DIFFERENT input language: general nonnegative column-substochastic matrices, a unary horizon, and universal scalar validation against a zero-output candidate. It does not prove hardness inside the common-positive-stationary-metric class above.

The 3SAT construction correctly encodes each assignment as a length-h word and its scalar as q^h times the fraction of satisfied clauses. With q=1−1/(2h), Bernoulli gives q^h>=1/2. The threshold separates SAT and UNSAT by gamma=q^h/(2m)>=1/(4m). A violating word is a polynomial-size witness with polynomial rational bit growth, so the coNP-completeness statement is justified in that language. Scaling the observable/tolerance scales the gap; the proof correctly avoids claiming fixed-relative-error hardness.

Contractive telescoping gives perturbation error at most h zeta. The convex perturbations toward distinct diagonal D and positive rank-one X remain nonnegative contractions and change each matrix by at most 2rho. At rho=1, the N^2 matrices D^i X D^j are independent by two Vandermonde factors and nonzero entries of X. Their vectorized determinant is a nonzero rational polynomial of degree at most N^2(2N−1). Testing that degree plus one distinct positive rational points in the admitted interval must find full algebra. Exact elimination has polynomial bit cost in this explicit finite input, although a high polynomial and all failed tests are paid. The chosen eta ensures 2h rho<=gamma/4, retaining the robust decision gap.

Thus small perturbations can preserve stable finite-task behavior while changing exact algebra closure. This does not make on-demand word evaluation hard, solve schedule optimization, establish general learning impossibility, or show that every useful retained abstraction is hard to acquire. The local leakage certificate is an incomplete sufficient route and may honestly fall back to full dimension.

## 5. Executed checks and finite resources

I reran the final author suite: 167 checks, including 127 exhaustive short words and 12 full-horizon holdouts. The three exact barrier examples passed. I added and executed independent_reuse_checks.py: 150 checks, including nonuniform stationary measures, genuinely nonreversible kernels, both gapless and positive-minorization cases, 126 exhaustive words, malformed/alias/task-substitution rejection, zero tasks, unsafe modular parameters, and the saved rank-121 witness replay. Both saved main acquisition records independently verify against the raw fixture JSON and its externally supplied horizon/tolerance: quadratic rank 4 and first-order-state rank 12.

I also reread and reran strong_comparison.py. All methods receive the same raw kernels/task and retain prefix work. The ordinary retained bidirectional Krylov method is the acquisition under review, not a separate novel competitor. The retained randomized joint-normal-range method receives the same quadratic certificate and pays its failed trials and verification actions. It admits rank 5 after its power ladder. Rank alone is not an arithmetic-cost guarantee: the recorded randomized-range future-query entries reach 33,081 bits and about 23.1 MB of rational state payload, versus 2,095 bits/about 1.10 MB for the rank-4 Krylov path and 685 bits/about 1.51 MB for retained full-space prefixes. My rerun reproduced those exact payload/bit counts and 536 retained prefixes; wall-clock values are illustrative and machine-dependent.

The rank-4 representation-entry maximum is 75 bits, while its serialized certificate rational maximum is 1,214 bits. The full-rank state-certificate serialized maximum is 9,447 bits. The corrected labels make clear that exact rational acquisition/query arithmetic and certificate storage can dominate a simple rank comparison. The prototype does not establish polynomial-in-log-horizon cost, optimized floating-point performance, or a fully instrumented intermediate-memory bound. Its S_L recurrence uses L iterations; rational output bit lengths and all future query arithmetic are paid.

## 6. Ordinary alternatives and scientific verdict

I inspected the primary records https://arxiv.org/abs/1404.6673 and https://arxiv.org/abs/1302.0221. The former explicitly provides stable weighted-automaton minimization and lossy bounded-error reduction; the latter provides switched-system model-reduction error bounds and Gramian methods. Their exact hypotheses and norms differ, so these abstract records alone do not establish that every displayed formula is already identical. They do establish strong ordinary retained-reduction baselines, consistent with the source's explicit credit.

A win over only the first-order state-error stopping criterion is not a win over equally informed Krylov, balanced, spectral, range or prefix-caching methods. They can use this same second-order scalar certificate. The current result is a sound, automatically acquired, uniformly certified finite-task reuse interface and a scoped exact-algebra/validation distinction. A new acquisition/transfer benefit beyond strong ordinary machinery, a noisy-data guarantee, or a consequential practical separation remains unearned.

## Exact frozen source/artifact binding

* `PROOF.md` — 11,644 bytes; SHA-256 `6c4f87bef1e45c22fcd3b0b42053bd55540690890751c9664b7f6a3ca570c6c4`.

* `UNIFORM_CERTIFICATION_BARRIER.md` — 6,302 bytes; SHA-256 `64cc05c2048efd7865556e1a535baba2f1ffcb701b1476de05ee940c7b3eade3`.

* `learn.py` — 8,363 bytes; SHA-256 `e274c04f20d81e478c033d606bfe9dd886a9a3f049a971e216575bb8c75b98ce`.

* `verify.py` — 3,469 bytes; SHA-256 `ed8dc7773c8728ce9d3a7432187684ce74be89c86e4533584f8c02483af61867`.

* `test_reuse.py` — 4,830 bytes; SHA-256 `bd189e1633e1ac8ab77c631183c958dd2694e90dfe4185b39613f884bc471a3a`.

* `algebra_witness.py` — 2,042 bytes; SHA-256 `3f2a28ddeeb8e078865c3e49ff5dcc58af47383b7e9640655b8136435be3230d`.

* `check_barrier.py` — 2,481 bytes; SHA-256 `9c37506c19ade478b0f4f7c97285ae80098281304fa68801a555fec8c487b202`.

* `strong_comparison.py` — 5,968 bytes; SHA-256 `f54211426ac6398c9db090f5dd94abd94b3e475eb7b8ee833ee5fe2403933281`.

* `acquisition_results.json` — 232,287 bytes; SHA-256 `36c79ab791e30c0e0a642051643a0305490f4e2a334a68f4573e9beb47be9fc3`.

* `tests_results.json` — 3,018 bytes; SHA-256 `7f50831183de33aa9cad6e6af4367ba326a4d1f5feacbfe4c4ec8ef849d288eb`.

* `algebra_witness.json` — 9,300 bytes; SHA-256 `b43b40bedc50173ae0ed9776a3d4c516ce1a1cb2bacdb53b1ad3cbd5e6459db5`.

* `barrier_checks.json` — 1,515 bytes; SHA-256 `ee4e8eb6219ac5a37dd1f6a4ea55d4055502056283ac7fd63de05810adb4cd9f`.

* `strong_comparison_results.json` — 3,529 bytes; SHA-256 `149ff419a658e956c8c9200c81aff4939ed24d0bb660af1d75f92f9aae2b16d0`.

* `fixture_input.json` — 18,144 bytes; SHA-256 `33dbbdf00da56eecdc24a76690e01ad9a08247b23fa751d1ba00f3e795bef683`.

* `independent_reuse_checks.py` — 3,873 bytes; SHA-256 `2cf4a903fa96db5971feb0104682ec908f759fb9b4a704ea2b3d8eb7e2e4e1a0`.

* `independent_reuse_checks.json` — 264 bytes; SHA-256 `7f15b658e77564c5a614024d4d72fda4ee86e21f36714f8a07d9f4bf6f76f7bc`.
