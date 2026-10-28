# Contract frozen before the response experiment

This wave does not extend the quartic programme. Initial reasoning and source
screening were independent of the capability-inversion worker.

Hidden assumption: two O(1) simulated responses must each be resolved to
O(eta) absolute error before their O(eta) difference can be certified.
Candidate operation: evolve the perturbation-normalized response directly.
This could serve transport, reliability, linear control and network-response
tasks, but the required generator is supplied, not inferred from a device.

Input: an EXPLICIT rational sparse row-stochastic P, lambda>0, Q=lambda(P-I),
diagonal D with entries0 or1, b>=0, c a coordinate readout, t>=0, eta>0 with
P-eta D/lambda>=0 entrywise, and normalized absolute tolerance eps. All
model rows, perturbation, input and readout are equally available to every
method. Output: rational bounds of width<=eps for

    r_eta=c^T[e^(tQ)-e^(t(Q-eta D))]b/eta.

The actual response difference is eta*r_eta. This is a normalized absolute
accuracy contract, not relative accuracy when r_eta may approach zero.
Reading, validating, storing and propagating the full explicit model is
charged. Unknown-system model identification, noise calibration and physical
execution are outside this contract and remain unacquired.

Proposed construction: u'=Qu, z'=(Q-eta D)z+Du, u(0)=b,z(0)=0; output c^Tz.
Compute it by positive uniformization with exact integer propagation and
rational Poisson-tail bounds, so floating cancellation/solver status carries
no proof weight. eta is a rational input; big-integer bit growth is charged.
No arithmetic-cost independence of the bit length of eta is assumed.

Primary comparator screen already finds that the central operation is prior:
Van Loan1978 Theorem1 computes precisely the block-triangular convolution;
Al-Mohy2025 arXiv2410.03575v2 treats the general unequal-diagonal-block
operator and an off-diagonal-norm-independent backward-error algorithm.
Al-Mohy--Higham2011 supplies sparse exponential action. These are credited
before testing; neither a stable implementation nor a gain over subtraction
would establish a new scientific operation.

Strong ordinary methods:

1. The same general Van Loan block exponential, implemented as an explicitly
   assembled2n-state sparse integer recurrence, with the SAME rigorous tail.
2. The ordinary Frechet derivative at eta=0 plus rigorous second-order
   remainder: 0<=r_0-r_eta<=eta ||b||inf ||D||inf^2 t^2/2. Use it whenever
   that remainder fits the requested budget, otherwise use the exact block
   method. Charge precondition checks and derivative computation. No reuse is
   free; each fresh-query measurement recomputes it.
3. Separate exact uniformizations to illustrate the hidden conditioning cost;
   this is not the sole or decisive comparator.

Predeclared cases: n=64,512,4096; eta=10^-2,10^-8,10^-14,10^-20; eps=10^-12;
lambda=2,t=4. P has row weights(1,4,2,1)/8 at offsets(0,+1,-1,+11), cyclic;
b_i=(8+i mod7)/8; D_i=1 at0,1,floor(n/3),floor(n/2), zero elsewhere; c=e_0.
This is12 supplied-model synthetic cases, not empirical system validation.
Retain every case, failed precision test, setup cost and input byte count.

Promotion gate: a consequential new capability requires advantage over the
strong ordinary block/derivative methods, not only over separately evaluated
responses. Algebraic equivalence to the ordinary block method decisively
closes the generic novelty claim for this construction even before timings.
