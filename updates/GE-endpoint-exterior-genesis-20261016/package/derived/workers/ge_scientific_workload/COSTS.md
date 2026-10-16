# Same-information cost accounting

This file gives constructive algorithmic comparisons, not new runtime benchmarks.
The source papers do not specify a finite-time absolute-TV tolerance on a full
permutation sampler; .05 belongs to the delivered mathematical fixtures and must
not be invented as an owner's scientific acceptance threshold.

## Actual cubic-lattice cycle workload

Let n=L^3, M=|E|<=3n, horizon beta, rate 1 on every edge, u=1. The supplied inputs
are geometry and beta, not measured material data. An explicit edge list costs
O(n) words; cubic coordinates can generate a uniformly indexed edge in O(1)
word operations after the boundary convention is fixed.

Exact ideal endpoint incumbent:

1. Draw N~Poisson(M beta).
2. Draw N independent uniform edge indices and apply their transpositions in
   sequence to an n-label array, starting from identity.
3. Scan permutation cycles in O(n), obtaining the complete shadow-length partition.

Superposition of independent edge Poisson processes proves this law is exact.
Event times are unnecessary because only their order and labels affect the
endpoint. No n! state enumeration, pair matrix, or density matrix is required.
Expected swaps are M beta<=3n beta. For the published beta=O(1) regime, expected
event work is O(n), as is an explicit full-permutation output and cycle scan.
Sorting cycle lengths, if required, adds the ordinary sorting cost; counting or
bucket forms can exploit integer lengths bounded by n. This is not a proof that
no constant-factor optimization exists. It removes the asserted stiff-event
bottleneck and supplies no asymptotic enabling gap for the certifier.

The exact static receipt retains both possible spatial boundary conventions.
For L=160, n=4,096,000 and the periodic edge count is 12,288,000; the open count
is 12,211,200. One pair vector has binomial(n,2)=8,388,605,952,000 entries, so even
8 bytes per entry means 67,108,847,616,000 bytes before other arrays. The current
dense physical-pair certifier is unsuitable at that scale. The delivered path/
cycle exterior implementation does not accept a branching cubic grid. Sparse
pair action or validated rational Krylov does not make the O(n^2) pair-vector
representation a preferable task here when the exact endpoint incumbent is O(n).

### A finite-bit constructive incumbent

Finite arithmetic and fair randomness are paid on both sides. An efficient
production Poisson generator should be given certified transcendental/rounding
and tail errors. The following simpler construction suffices to establish that
the exact endpoint method remains near output scale without a real-number oracle.
It is a derived algorithm specification, not executed acquired code.

Let mu=M beta be a supplied nonnegative rational, m=max(1,ceil(mu)), and x=mu/m<=1.
Partition the horizon into m equal intervals. Each interval has a Poisson(x)
number of uniform edge events. Choose integer K such that

    m/(K+1)! <= epsilon/4.

The falling-factorial Markov bound proves P(Poisson(x)>K)<=1/(K+1)!. Compute a
rational lower bound l for exp(-x) with exp(-x)-l<=delta<=epsilon/(12m), using
the alternating Taylor enclosure on [0,1]. Let Q=2^b>=4m(K+1)/epsilon and set

    a_k=floor(Q l x^k/k!), k=0,...,K.

Assign unused grid mass to count zero. A b-fair-bit integer samples this finite
CDF. Since sum_{k<=K} x^k/k!<3, the per-interval TV error is bounded by

    1/(K+1)! + (K+1)/Q + 3 delta.

Across m intervals it is <=3 epsilon/4. At most mK edge indices are needed.
For edge selection use ceil(log2 M) bits per attempt and rejection sampling,
capped at a attempts with 2^-a<=epsilon/(4mK); a fallback's union-bound mass
is <=epsilon/4. Total endpoint TV error is <=epsilon by coupling. M=0 and mu=0
are deterministic identity cases handled separately.

Count probabilities for k>=1 were only decreased, with all leftover assigned to
zero, so the approximate expected count is no greater than mu. Expected fair
bits are at most

    m b + 2 mu ceil(log2 M),

because each edge-selection rejection acceptance is at least 1/2. Worst-case bits
are m b + mK a ceil(log2 M). One rational CDF is precomputed and reused for every
interval, with its coefficient/rational-precision costs charged. K and b grow
polylogarithmically in m/epsilon; integer bit costs, including beta's input bits,
remain explicit. For beta=O(1), expected bits are O(n log(n/epsilon)) and event/
array operations remain O(n) up to bit arithmetic and finite-CDF lookup. Standard
better Poisson implementations are allowed the same information and may improve
this conservative construction.

## Pair/exterior certifier and averaging incumbent

The delivered accelerated sampler is conventional conditional-uniform averaging.
Any competitor given the same block, supplied rates, graph, horizon, tolerance,
and exact conditional permutation law may use exactly its boundary-event process
and final block shuffle. Online costs and fair-bit errors are then identical.
The comparison concerns the strength and cost of the error certificate, not a
new sampler mechanism. The certifier's precision and adaptive-quadrature work
cannot be treated as free.

For a fast block of s sites and boundary-attempt rate Gamma, the incumbent can
use component mixing/renewal bounds, exact dimer parity, exact quotient kernels
where small, spectral/functional inequalities, or validated exponential action.
The pair certificate may certify a block when one particular gap estimate fails;
that does not establish superiority over all these equally informed certificates.

The original reports give path setup O(n^3 m M(p)) integer-product bit work and
O(n^2 m p) bit storage, plus survival-node/ quadrature work, where m is scaling
depth, p integer precision, and M(p) multiplication bit cost. Dense general-pair
setup is O(n^6 m M(p)) with O(n^4 m p) storage. The adaptive node count has no
graph-uniform bound. Reuse across initial permutations/colors amortizes setup
only when graph, rates, horizon, partition, and tolerance remain covered by the
same certificate. A new beta query needs a valid time-dependent enclosure or
new setup, not automatic reuse.

For B samples, full accounting is C_acquire+C_cert+B(C_boundary+C_shuffle+
C_output+C_measure/reset). A claimed break-even B requires actual measurements
of these terms on the selected scientific workload. No such measured break-even
exists here. Once a cheaper same-information exact sampler is already O(n),
amortizing a much larger setup does not establish a new operation.

## Heat, duality, and validated matrix incumbents

One-point occupancy means and local quantum reduced states require an n-state
heat computation; k-point SSEP moments require the binomial(n,k)-state dual
exclusion computation. A full permutation TV certificate should not be billed
against a one-point query. For many repeated linear observables, heat-kernel/
spectral setup can also be reused without per-query Monte Carlo output noise.

Symmetric killed-pair and heat generators admit rational/shift-and-invert Krylov
incumbents with norm-independent approximation bounds. Costs are verified sparse
shifted solves, basis storage, scalar approximation errors, norm conversion, and
rounding/residual enclosure. A floating solver's failure on the synthetic graded
path does not refute this family. A valid comparison must include a fully
validated implementation at the actual required tolerance. None was implemented
or timed in this worker.

For an approximate heat/survival trajectory v(t) with defect d(t)=v'(t)+Hv(t),
substochastic contractivity gives the useful validation route

    ||v(t)-exp(-tH)1||_infinity
       <= ||v(0)-1||_infinity + integral_0^t ||d(s)||_infinity ds.

The integral must be enclosed over the entire interval, with the solve/projection/
interpolation errors included. Sampling residuals at nodes is insufficient.

## Quantum execution

For asymptotic symmetrization, drawing one exact uniform permutation already
implements the twirl; a finite-time CTMC trajectory is unnecessary. For a fixed
finite-time noise-channel emulation, the exact global Poisson sampler also first
compresses all swaps to one permutation, then executes/routes that permutation.
It must not be charged all microscopic quantum gates when the new method is
allowed to output only one final permutation.

Both methods pay the same resulting quantum routing and gate-accuracy obligations.
Both can use virtual wire relabeling when the downstream task allows it. An
accelerated classical event count proves neither faster physical evolution nor
fewer required routing gates. Rate acquisition, complete generator validation,
noise, reset, measurement repetitions, energy, and total execution costs remain
unmeasured for any actual quantum platform in this search.
