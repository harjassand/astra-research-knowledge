# Fixed-window geometric clock preparation: outer times and QQ marks

Status: candidate replacement of two clock operations in the checked sharp assembly. It uses ordinary product geometric distributions and paid classical angle preparation. It does NOT supply a free exponential clock conditional on an arbitrary coherent remaining duration, and it does NOT replace the still-acquired off-diagonal bridge sampler.

## 1. Exact bin law and an actual circuit

Fix a known positive rate q, a per-physical-call CLASSICAL window tau>0, B>=0, M=2^B and Delta=tau/M. Write z=e^{-q Delta}. Conditional on an exponential wait being less than tau, its integrated bin probabilities are

    Pr(m)=(1-z) z^m/(1-z^M), m=0,...,M-1.

The binary bits of m are independent, with bit-j probability

    p_j=z^{2^j}/(1+z^{2^j})
       =e^{-q Delta 2^j}/(1+e^{-q Delta 2^j}).

Indeed product_j(1+z^{2^j})=(1-z^M)/(1-z), and the product bit probabilities are z^m divided by that product. A draw therefore uses exactly B one-qubit preparation rotations (controlled on a mixture label if required), not a coherent inverse CDF. Increasing exponential density is obtained by reflecting the bin index; q=0 is uniform Hadamards. B=0 is the single-bin limit.

For an UNCENSORED waiting clock with a censor at tau, add a Bernoulli tail flag of probability e^{-q tau}. On its complement use the preceding conditional bin state. The tail sentinel means the true wait is at least tau. Its exact value is unnecessary whenever the subsequent comparison threshold is at most tau. All seed registers remain available and are reversed after SELECT. No label or coin is erased by a many-to-one map without retaining the input seed.

Angles are computed CLASSICALLY from the fixed q,tau before the physical first-event circuit call, at the requested tolerance. The physical private event/time measurement may determine the next call's classical window; that is allowed adaptive simulation, not a real-time hardware latency claim. All classical arithmetic, compilation, angle descriptions, controlled gates and inverses are paid. There is no table over all coherent remaining times. Within a call, the same q,tau angle list can be reused for all coherent QQ draws.

Evaluate e^{-x}/(1+e^{-x}) with nonpositive exponentials. If an amplitude is clipped, use a probability cutoff of order the SQUARE of its allocated rotation error. Small q Delta uses expm1 or interval Taylor arithmetic; the limiting bit probability is1/2. Certify all rotation angles directly to their operator-error budgets. No tiny probability is divided by. The classical work and number of bits are polynomial in input lengths, B and log(1/error); no q tau iterations are needed.

## 2. Outer three-exponential proposal, with no uniform endpoint strips

Receive the sharp proposal

    w(t)=alpha_L² mu [a² e^{2st}+2a b1 e^{-delta t}+b1² e^{-2dt}],

and its exact component masses on [0,tau]. Prepare the atom/component/zero-arm label using those masses and the fixed whole normalizer A. Each event component is sampled with its exact integrated bin probabilities from Section1 (reflection for the increasing component). Its finite timestamp is the bin midpoint. The inner block on EVERY component remains J K0(t)/sqrt(w_total(t)), not division by a component density. Mixture labels stay private orthogonal Kraus coordinates.

In the ERROR PROOF only, extend each finite bin label with a private variable distributed according to the exact conditional continuous component density inside that bin. The exact and finite constructions then share this Hilbert space; their times differ by at most Delta/2. Since the normalized event operator has received derivative bound Lout, the base-block L2 error is at most Lout Delta/2: the sum of proposal masses divided by A² is at most one. The exact counter-augmented continuation changes by at most Lphys Delta/2. The label/bin embeddings may depend on the fixed classical tau; this does not expose their timestamps to the consumer.

Thus choose, for example,

    Delta_out <= min(tau, beta/[100(1+Lout)],
                    e_step/[100 Lphys]).

No outer inverse-uniform endpoint strips, sigma, or associated t0 is needed for this replacement. The physical short-remaining-window rule x_min stays unchanged. Internal conditioned bridge durations can approach or round to zero; the separately checked stable hierarchical source supplies their limiting bridge and does not need an endpoint floor. If using the older endpoint-floor bridge instead, its old floors must still be retained; this note alone does not remove them.

The continuum versus finite timestamp distributions are NOT close in TV. Only the common conditional-bin Kraus embedding and the private-future channel are compared. Every artificial component/bin variable stays inaccessible to the physical consumer, while the actual source and physical jump color are retained.

Prepare component weights and B rotations with total circuit operator error <=beta/100, and subdivide by their actual operation count. Numerical masses/angles and midpoint multiplication by the known tau are paid. With tau an arbitrary finite dyadic, forming (m+1/2)tau/M may require actual reversible constant multiplication, not merely a free bit shift.

## 3. QQ Poisson marks by sequential censored waiting draws

Inside a given fast residence of duration ell<=tau, the QQ process has fixed rate q=2c. Instead of a finite Poisson-CDF scan followed by sorting, draw independent censored Exp(q) waits using the same per-call fixed-window circuit of Section1. Compare the waiting time to the COHERENT remaining residence. If it exceeds that residence, stop this residence. Otherwise emit one QQ insertion, subtract the wait and repeat. A tail sentinel always exceeds the residence and stops it. This is an unconditioned clock followed by a comparison, not an exponential conditioned to fall before ell.

Cap TOTAL virtual insertions at K and select the zero word on overflow, exactly as in the aggregate-tail proof. There are at most K accepted QQ marks and at most K+1 residences requiring a final censored wait. Therefore 2K+2 clock draws per path PREP is a safe fixed cap. Unused draws may be coherently prepared and ignored, then unprepared. The coherent cost is that cap, not the expected number of draws.

Before discretization the procedure is the ordinary exponential-wait construction of a Poisson process and gives exactly the same independent residence-conditional QQ law as the received source. Marks are chronological by construction, so no sorting is needed. Keep the fixed off-diagonal residence order and all boundary operators; a numerical equality creates a zero interval, not a reordering of noncommuting boundary operations.

## 4. Finite clock coupling, including termination decisions

Couple every finite bin draw to its exact conditional exponential time within that bin; a non-tail draw differs by <=Delta_QQ/2. Tail draws are compared only with thresholds <=tau, so their precise value is irrelevant. Given past history, a new exact exponential wait is independent and has density at most q. If the current remaining durations differ by e, a different stop/continue decision can occur only within a boundary strip of width O(e+Delta_QQ), with conditional probability <=2q(e+Delta_QQ). Comparison arithmetic on the finite registers is exact or receives its usual allocated timing error.

After j matched accepted marks, accumulated residence-time error is at most its inherited off-diagonal error plus j Delta_QQ. Summing over at most 2K+2 draws gives a conservative mismatch bound

    O(q K² Delta_QQ)+O(q K² h_off),

where h_off is the separately earned skeleton rounding scale. Matching absolute mark times differ by O(K(Delta_QQ+h_off)). The operator word error is therefore

    O([Hs+mu(alpha_H+1)](K+1)²(Delta_QQ+h_off)).

One sufficient choice, with the inherited off-diagonal budget unchanged, is

    Delta_QQ <= min(tau,
      eta/[10^6(1+q)(K+1)²],
      beta/[10^6(1+Hs+mu(alpha_H+1))(K+1)²]).

Round all finite times monotonically within the residence and keep the hierarchical order. If a remaining duration rounds to zero, its QQ count is zero; the discrepancy from an exact small positive duration is bounded by q times that duration. No inverse endpoint probability or minimum-spacing assumption is used.

For numerical clock preparation, let N_draw=2K+2. Allocate the sum of all clock PREP/PREP† rotation errors <=eta/100 (or a smaller base-block allocation), by assigning each of the O(N_draw(B_QQ+1)) rotations its actual budget. Classical angle errors then perturb the joint finite draw law and the coherent selected-word block by the standard unitary hybrid. Scalar rate arithmetic is included by certifying the angles as functions of the exact acquired rates. The subsequent comparisons and subtractions use actual finite registers. No exponentiation or logarithm of a coherent remaining duration is needed in these QQ clocks.

## 5. What this does not replace

An off-diagonal bridge component needs a truncated exponential conditioned on a coherent remaining t. Preparing a tau-window clock and rejecting waits beyond t would cost 1/(1-e^{-qt}), potentially unbounded. This is NOT licensed here. The checked three-call conditional bridge preparation remains the explicit solution for those operations, with its scalar acceptance and arithmetic costs. A later bounded-ratio dyadic conditional-clock construction would need its own normalization/precision proof.

Nor does this note remove scalar arithmetic from the actual positive outer masses, endpoint weights or inner conditioned source; only quantities depending on the per-call classical tau can be compiled into the fixed rotation lists here. No free QRAM, branch-dependent uncharged preprocessing, hidden physical resets, or physical timestamp output is assumed.

## 6. Execution accounting and receiver

Outer product preparation uses O(3B_out) controlled single-qubit rotations plus the constant branch register and finite timestamp formation. QQ clocks use at most (2K+2)(B_QQ+1) such rotations per path PREP, and twice that for PREP plus inverse, plus finite comparisons/subtractions and seed/work registers. All rates are fixed within a physical call; angle acquisition can be reused within that call but is charged again if its classical tau changes.

The complete first-event normalizer, sharp amplification degree, aggregate word cap, physical count/window caps, actual jump-stack output and final controlled-process scope remain unchanged. Add the stated new clock errors to their existing beta/e_step budgets; ample subdivisions may be tightened without changing the formula's logarithmic rate/precision dependence. The revised operation list is more explicit than inverse CDF/CDF/sort oracles, but these are still rotation/arithmetic counts, not final hardware gates. A separate same-fixture ledger is needed before any numerical resource assertion. No practical crossover or novelty claim follows.
