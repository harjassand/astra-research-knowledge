# Paid acquisition, planner and reuse scope

Let a fixed partition attempt have n states, m actions, r blocks, N episodes per
state/action, cap K, rational gamma with numerator/denominator bit length b_g.
Let c_src denote the actual cost of one forward source call at its prepared row;
if costs vary, use their sum rather than a claimed unit-cost simulator.

- **Native task input:** read n feature rows and construct equal-feature groups.
  This costs input size; arbitrary unique features can give r=n immediately.
- **One acquisition attempt:** nmN episodes; <=nmN(K+1) forward calls,
  expectation nmN[1+gamma(1-gamma^K)/(1-gamma)]. Multiply by actual source work.
  State/endpoint mapping costs O(1) word access only after an n-entry map has
  been acquired/stored; each label has ceil(log2 n) bits. Counts require
  log2(N+1) bits, and every increment/coin/map operation is paid.
- **Stopping coins:** exact integer rejection uses O(b_g) expected random bits
  and bit operations per coin (with standard integer arithmetic), not a free
  geometric oracle. Actual prototype bit requests and source CDF scans are
  separately instrumented in the protocol result.
- **Retained evidence:** nmr integer counters, the actual partition, count design,
  source identity and all failed attempt records. Full microscopic paths are
  available to every method; retaining them costs their actual number of labels.
  Endpoint counters alone need O(nmr log(N+1)) bits plus the partition/map.
- **Receiving:** O(nmr) rational counter processing plus max-row L1 comparisons.
  Uniform-block averages may have unequal block denominators; exact common
  denominator construction and bit growth are paid. No O(r)-only acquisition
  verification is claimed. The root radius uses a b-bit dyadic rational;
  truncation gamma^(K+1) has O(K b_g) bits. A conservative polynomial bit bound
  suffices; no arbitrary-denominator sum is counted as constant-bit arithmetic.
- **Refinement:** pairwise connected-component proposal is O(m n^2 r) rational
  arithmetic per attempt. The exact reference implementation additionally forms
  a dense resolvent; this is analysis/testing code with exact matrices, not the
  forward-observation learner. Statistical proposals require a FRESH endpoint
  batch after each partition change. All attempts and confidence budgets count.
- **Retained core:** O(mr^2) rational Bhat entries, hhat, radii, hashes and design
  scalars. Map and full counts remain separate. Ordinary block-compatible goals
  then cost input reading, O(mr^2) LP assembly, an r-variable O(mr)-constraint
  rational LP, exact primal/dual/candidate checking, and r output action labels.
  Standard polynomial LP bit complexity is available; the actual prototype's
  rational simplex runtime is recorded and not declared polynomial worst case.
- **Finite precision:** no computed inverse of R or reduced spectral condition
  number is needed. Core coefficients/LP certificates have their exact rational
  lengths counted. The code's maximum-entry field covers inputs/outputs, NOT
  every internal pivot/intermediate or measured peak memory.
- **Repeated receiving:** a trusted previously checked core digest can be reused;
  its per-goal hash scans only the small core. A new independent full audit pays
  all nmr counter work. Neither digest nor signatures prove physical iidness.
- **Deployment:** retain n ceil(log2 r) map bits (plus representation overhead),
  an actual current-state sensor/simulator label each step, policy-table lookup
  and the source's execution cost. Infinite stationary policy description is
  finite; executing infinitely many steps is not free. J-step implementation
  incurs all J operations and normalized tail error <=gamma^J.

The conservative sufficient schedule in PROOF section 9 scales polynomially in
n,m,r, inverse accuracy and 1/(1-gamma), not necessarily in the bit length of
gamma alone. It is not a lower bound and may be far worse than a strong
variance-aware or goal-specific learner. No real acquisition-amortization or
hardware advantage is established here. The source interface itself must exist;
arbitrary physical microscopic row preparation or state sensing is not granted.

A useful qualitative distinction is earned conditionally: full-kernel or
block-Markov predictive learning can fail on the same process for which these
control-specific moments yield a small later LP. But strong ALP/SF methods using
the same certificate receive that benefit too. The source-bound ingredient,
its historical status, and an important economically favorable workload remain
the criteria for a larger capability claim.
