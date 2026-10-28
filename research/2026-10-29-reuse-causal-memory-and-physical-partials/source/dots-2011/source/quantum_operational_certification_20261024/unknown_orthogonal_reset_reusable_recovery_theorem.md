# Reusable recovery of unknown reversible mixed encodings with unknown orthogonal noise

27 October 2026. Local post-publication-cutoff assembly; component analytic receipts exist, whole assembly independent receiving requested. Historical novelty is unassessed.

## Capability and physical access
A stationary memoryless qutrit-input channel is promised to have the form
 E(rho)=p V(rho tensor sigma)V*+(1-p)Tr(rho)tau,
where V is an unknown isometry, sigma and tau are unknown density matrices, tau V=0, rank sigma<=a supplied integer r, and p>=a supplied p0>0. The finite output dimension s is known. Neither p nor any nonzero eigenvalue, noise spectrum, background, code basis, or inverse preparation operation is supplied.

For 0<nu<=1, ordinary classically labelled, unentangled training probes suffice to acquire a CLASSICAL reusable decoder Dhat. All source-dependent quantum training systems can be discarded. No calibration queries are needed for future data. Averaged over its one-time training, the complete unhalved diamond error obeys
 || E_training[Dhat E]-[p id+(1-p)erasure] ||_diamond <=nu p.
There is also a single good-training event on which each learned decoder satisfies the stronger relative bound below. This is recovery at actual source throughput p, not a small postselected success fraction.

The deterministic source-copy cap is
 N <= (4104 d/t) ceil[100 eps^-2 ln(4d(J+1)/beta)],
 d=3s, t=p0/r, eps=nu²/1000000, beta=nu p0/4,
 J+1<=ceil(log2(1/t))+2.
Thus N=O(sr/(p0 nu^4) polylog(sr/(p0 nu))). One independent source use per future datum is additional. Collective receiver-side measurements, classical matrix computations, register size and gate synthesis are NOT claimed ambient independent or computationally efficient.

## Acquired operator representation
The received labelled access preparation gives T=(J_Choi+3omega)/4 and omega=I3/3 tensor E(I3/3). One original source call prepares either receiver-local mixed program, with a known label preparation and no shared entangled sender reference.

Apply acquired_regularized_relative_operator_estimator.md separately to T and omega, using target eps, regularization t, failure beta/2. The two sample caps sum to the displayed N. The procedure learns all its whitening matrices from previous ordinary measurement outcomes; it does not use unknown physical whitening. On the common good event, each state estimate has Loewner error <=eps(state+tI).

Compute Hhat=4That-6omegahat, then the nine known A-Weyl conjugates. True omega is A-Weyl invariant. Writing H_j=J_j-3omega and A_j=J_j+3omega gives
 |relative error| <=eps(4T_j+6omega+10tI)<=10eps(A_j+tI).
This is an order bound, not an assertion that the matrices commute. Set eta=10eps=nu²/100000.

## Learned decoder and complete error
For each Hhat_j take the projector onto at most r largest positive eigenvalues. These are ordinary computed matrices, not the unknown exact Bell projectors. The deterministic proof in unknown_reset_relative_projector_receiver_root.md shows each positive-band risk L_j<=10eta p, without resolving tiny sigma eigenvalues.

Use the sequential retained-data Bell-projector receiver with known Weyl corrections and final erasure. Its complete error on the good event is bounded by
 p[18 sqrt(20eta)+1620eta] <0.271nu p <nu p/2.
The success-branch estimate uses reference-uniform instrument hybrids weighted by original signal mass. Reset acceptance is charged directly through an always-reject Stinespring comparison, rather than a square-root disturbance estimate that would lose relative throughput. On a declared abort, return erasure. An undetected bad-training event still runs the computed CPTP decoder; in either case worst complete error<=2. Thus failure adds at most2beta<=nu p/2, and total is strictly below nu p.

As with the imported continuous-outcome tomography model, this statement uses ideal mathematical measurement/matrix operations; it is not a bounded gate-complexity theorem. There is numerical slack for separately charged finite implementation error. Arbitrary many-data joint accuracy is NOT free: the good-event error accumulates at most linearly, while the bad-training event is a single shared event, not resampled independently for each datum.

## Worst-case comparison, not a universal noise lower
The independently received full_ambient_reset_compilation_lower_root.md supplies a matching-exponent worst-case subclass: flat rank-r flag, unknown Haar code, uniform unknown reset on its full ambient complement, s>3r. At fixed nu<=1/4 any classical deployment with arbitrary coherent adaptive pre-datum training requires
 n>=sr/[32{D_Ber(p||3r/s)+2p ln3}].
For p>=3r/s this implies n>=sr/[32p ln(3sp/r)]. Taking the known lower promise p0=p matches the acquired upper's rank/ambient/signal exponents up to logarithmic factors. This does not assert the same lower for every noise state, for p<3r/s, for online source calls, or for retained source-dependent quantum programs.

The consumed-program receiver remains a materially different comparator: it has fixed-accuracy sample scaling r²/p0² without raw ambient dependence, but consumes fresh calibration for each datum. Generic full-state infidelity tomography is another conventional reusable route; the new construction avoids paying full unknown-noise rank by learning relative operator contrasts and charging low-positive-rank risk. No claim that the field's strongest possible prior algorithm has been exhausted is made.

## Dependencies and boundaries
- acquired_regularized_relative_operator_estimator.md and root independent receipt; primary PSW debiased Keyl covariance theorem.
- unknown_reset_relative_projector_receiver_root.md and separate source audit/receipt.
- reusable_operator_learning_labelled_access.md and independent receipt.
- full_ambient_reset_compilation_lower_root.md and independent receipt.

The structural promise (stationarity, reversible mixed-success form, orthogonal reset, supplied rank and throughput bounds) is not certified merely by this learning theorem. Overlapping reset, entropy-only perturbation, unassisted quantum capacity, scalable gate implementation and historical priority remain separate questions. No source from the frozen merged PR240 is altered by this local theorem.
