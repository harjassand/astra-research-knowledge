# Cost ledger and informative failures

This note reads the frozen author reports. It does not add an independent
review claim or treat a tiny synthetic fixture as a practical capability.

## 1. Exact rational rank was not enough

In the preceding exact-input experiment, retained randomized range found an
admitted rank-five model but its retained query rationals reached 33,081 bits
and 23,128,058 serialized bytes. This lost to the retained full-space method.
The rank-four ordinary Krylov fixture was much better, but was not a new
learner and did not establish a broad strong-baseline advantage.

The finite-observation continuation actually executes a common-denominator
integer backend. All methods now round after each small matvec and choose
their own smallest admitted query precision. It is not a favorable fixed
precision imposed only on the proposed model.

## 2. Identical imperfect observations, strong retaining methods

The 12-state, two-generator fixture has no common stationary law. The learner
sees only outward entry enclosures. Eight- and twelve-bit observations fail
the paid uncertainty budget; at sixteen bits rank three fails and rank four
passes. Its center-compression error is about 7.77e-6; observation error is
105/32768 = 0.00320435. Query rounding then uses the available remaining budget.

Forty horizon-30 words share the same 1,032 retained prefixes. Every method
gets those same observations and may retain prefix states:

| Retained ordinary method | State dimension | Query fractional bits | Total certified error | Query time (illustrative) |
|---|---:|---:|---:|---:|
| Full stochastic center | 12 | 12 | 0.007111 | 0.01635 s |
| Bidirectional Krylov | 4 | 15 | 0.009494 | 0.00384 s |
| Randomized joint-normal range | 5 | 16 | 0.007574 | 0.00518 s |
| Pooled-normal spectral | 6 | 16 | 0.006837 | 0.00644 s |

The last three require approximately 0.226, 0.812 and 0.400 seconds of
acquisition, plus grid tuning and another 0.054, 0.114 and 0.116 seconds of
exact certificate verification, respectively. **All lose after acquisition on
this 40-query batch.** Query savings alone are not the requested result.
Amortization depends on actual future distinct work, prefix overlap and memory,
not an assumed stream of infinitely many fresh equally expensive queries.

The integer state budgets are 13, 16, 17 and 17 bits including the grid
denominator. Stored common-denominator coefficients use at most 20 bits for
the full center and 27 for these reduced models. Actual integer accumulator
maxima are reported, including final output dot products. Reduced certificate
payloads are 4--6 kB and include rationals as large as 929 bits; the random
basis itself reaches 390-bit entries. Thus online fixed precision does not
erase offline exact arithmetic or archive costs.

Construction-image MVPs, per-candidate certificate-image MVPs and dense center
projection counts are separated. A construction counter is not falsely
reported as all verification work. Geometry solving, PSD tests, unsuccessful
candidates and exact arithmetic are in acquisition wall time. Peak
intermediate bit operations are not fully instrumented, so no complete
bit-level empirical ledger is claimed. The proof instead gives a conservative
common-denominator bit-complexity construction.

## 3. Full-entry statistical acquisition can dwarf every saving

The executed interval fixture uses a mock certified precision oracle. It does
NOT establish the cost of getting those enclosures from physical samples.
For scale, substitute the elementary full-entry Hoeffding frontend with
n=12, m=2, failure probability 0.001, and rounds p=8,12,16. Use halfwidth
rho=2^(-p-1), round confidence delta/2^(k+1), and the conservative integer
logarithm bound in the proof. Required cumulative draws per row are

* p=8: 2,752,512;
* p=12: 738,197,504;
* p=16: 197,568,495,616.

Across 24 rows the final count is **4,741,643,894,784 transitions**. These are
calculated sufficient budgets, not executed experiments, optimal bounds, or
a claim that the resulting random centers would give the identical learned
basis. They show why a sound interval interface alone does not earn cheap
scientific acquisition. Ordinary direct Monte Carlo and retained row learning
must remain competitors; sharper confidence methods may greatly improve this
deliberately conservative budget.

## 4. Task-weighted acquisition avoids a supplied probe set, not acquisition cost

The separate sparse experiment starts with only initial label 17 in a
billion-label universe, access to row sampling, the task's bounded terminal
observable, horizon 12, and tolerance 0.1. A Bellman overapproximation chooses
which row to refine. It acquires seven center states and 28 nonzero center
entries through 84 row updates. The record charges **15,778,976 iid draws**,
including all training and fresh validation batches. On the simultaneous
event of probability at least 0.999 its observation error is at most 3/32.
This executable's `risk/2` applies to observable range width at most one.
The general theorem includes `osc(b)`. Coverage assumes nonanticipating row,
support and validation-batch-size selection with fresh data. A transcript
verifier does not authenticate that timing or establish validity under
optional, outcome-dependent stopping of a validation batch.

All 4,096 binary words of length 12 are tested only AFTER acquisition; this
enumeration is not used to find probes or establish the certificate. The
maximum error in that synthetic realization is about 0.0008384. Small
empirical error is not substituted for the 0.09375 certified bound.

The composed stable replay is admitted at total error 0.0938263, but its rank
is **seven**, the entire acquired center graph. Therefore it has no additional
rank advantage over ordinary retained sparse center evaluation. The successful
operation is uniform, finite-data admission without presupposing the graph,
metric or probes. The mechanism is established model-based exploration plus
the stated error decomposition, not a historically new general learner.

## 5. Hard limits kept in the record

* Fixed entry precision cannot identify two absorbing kernels whose length-L
  answers differ by more than 2 epsilon. Worst-case observation precision must
  scale at least on the order epsilon/L in that example.
* A zero-output null task on K accessible test leaves still costs
  Omega(K log(1/delta)/epsilon) samples for uniformly successful admission.
  Small rank alone gives no acquisition guarantee. A lazy interface that only
  ever needs D leaves can legitimately be much cheaper; it is a strong
  retaining baseline, not something excluded from comparison.
* A learned geometry need not approximate a true common stationary law. Bad
  geometry is allowed by the theorem but can yield a useless large bound.
* Stable-H replay can incur bias even at full dimension for general
  non-common-equilibrium families. A failed reduction is INCONCLUSIVE, not a
  reason to deny the original stochastic center's cheap infinity-norm replay.
* No initial-state feedback policy equivalence, unbounded-horizon admission,
  new-observable transfer, drifting-law guarantee, measurement provenance, or
  physical-model verification is claimed.

The tested mathematical principle survives imperfect observations and finite
execution. The north-star claim of a new, consequential acquisition-to-later-
computation advantage over strong existing retained methods remains open.
