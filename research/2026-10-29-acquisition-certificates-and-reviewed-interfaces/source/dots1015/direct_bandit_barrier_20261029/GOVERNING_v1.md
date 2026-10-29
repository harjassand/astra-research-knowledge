# Finite first-order bandit acquisition using direct star witnesses

2026-10-29. Author construction, receiving review requested. The rational floor sampler and first-order derivation were developed jointly with `producer-workspace/sharpen_noreset_acquisition_certificate`. This is a materially different fallback to the full-information quartic controller; it is not a claim of historical novelty or practical superiority over conventional channel-adapted bandit control.

## Physical interface and scope
For each of m=n−1 star edges use the direct twisted-swap Bell witness in `direct_star_witness_20261029/GOVERNING_v1.md`. A selected frame C gives Bernoulli flip Y with mean ell_t(C)=delta_t(C)/2 in [0,1]. Prepare a uniform Bell eigenstate of its twisted swap and maximally mixed remaining carriers; measure the same swap. This requires candidate-dependent rotations, Bell preparation/readout and routing. It does NOT supply full-information feedback for other frames.

Each edge has a finite rational stereographic SO(3) net of M arms. Independently draw one arm per edge from its learner, forming a globally consistent star frame (root frame identity, other frames the relative rotations). The current joint source map must be fixed before fresh arm and role randomness, on the actual conditional memory history. On a private witness role choose an edge uniformly. Write rho for each edge's resulting observation probability, e.g. rho=p_w/m. Observe that edge's Bernoulli flip. Other roles may perform service/validation but must not alter the current map according to hidden current choices. No-reset source memory is allowed; comparison is evaluated on actual learner-induced histories, not counterfactual policy histories.

## Ideal barrier probabilities, implemented rational distribution
Fix horizon T>=1, eta=rho/4, and barrier R(p)=−sum_i log p_i. Starting cumulative estimated losses L_i=0, the ideal FTRL point is
 p_i*=1/(c_i+nu), c_i=eta(L_i−min_j L_j),
where sum_i 1/(c_i+nu)=1. Since min c_i=0, the unique root satisfies nu in [1,M]. The ideal point is only an analysis device.

Set D=8MT. Exact rational bisection brackets nu in [lo,hi] with width<=1/D, using a public fixed number of iterations. Let lower_i=1/(c_i+hi), k_i=floor(D lower_i), w_i=k_i+2, W=sum_i w_i, and IMPLEMENT q_i=w_i/W.

The derivative of 1/(c_i+nu) has magnitude<=1 on the bracket, so 0<=p_i*−lower_i<=1/D. Hence Dp_i*−2<=k_i<=Dp_i*, D<=W<=D+2M, and
 q_i >= a p_i*, a=D/(D+2M),
 q_i >= 2/(D+2M).
Consequently p_i*/q_i<=1+1/(4T)<=5/4, and TV(q,p*)<=1−a<=1/(4T). Integer weights give an exact finite weighted sampler, not an algebraic-probability oracle.

On the observed edge/arm j update L_j by Y/(rho q_j); no other coordinate changes. This is conditionally unbiased for the vector of current expected arm losses. The probe signal is nonnegative; the signed product-probe estimator cannot substitute for it in the following argument.

## First-order regret proof
For a nonnegative coordinate update g e_j, move continuously along that update in the ideal barrier solution. Differentiating the KKT equations gives
 −d p_j/ds = eta g p_j(s)^2 [1−p_j(s)^2/sum_i p_i(s)^2],
so p_j is nonincreasing and
 <p_t*−p_(t+1)*, g e_j> <= eta (p_t,j*)^2 g^2.
The standard FTRL telescoping inequality follows directly from convex minimization at each step:
 sum_t <p_t*−u, g_t> <= [R(u)−R(uniform)]/eta + sum_t <p_t*−p_(t+1)*,g_t>.
For clarity, it can be obtained by bounding each increment of min_p[R(p)/eta+L_t.p] between its gradients before and after the update, then using the final minimum <= R(u)/eta+L_T.u. No numerical optimization theorem is assumed.

Conditional on actual past, sampling probability q_j and edge observation probability rho, g_j=Y/(rho q_j). Thus expected stability is at most
 (eta/rho) sum_j q_j (p_j*/q_j)^2 ell_t(j)
 <= (25/64) sum_j q_j ell_t(j).
Also expected action mismatch <q−p*,g_t> equals <q−p*,ell_t> <= TV(q,p*) <=1/(4T). Sum these inequalities and take expectations. For any fixed arm j, use u=(1−1/T)e_j+(1/T)uniform. For T=1 this is uniform. Then R(u)−R(uniform)<= (M−1)log T and expected u loss <= expected j loss+1. Therefore, writing L_alg for cumulative expected true selected loss and L_j for that comparator's cumulative expected loss on the ACTUAL histories,
 (1−25/64)L_alg <= L_j + 5/4 + (4/rho)(M−1)log T,
and conservatively
 L_alg <= 2 L_j + 3 + (8/rho)(M−1)log T.

This is not hindsight selection over random adaptive loss paths. The fixed comparator can be chosen scientifically in advance (including a fixed unknown physical frame); no claim is made about counterfactual trajectories or arbitrary drifting comparators.

## Gap-free exact common-frame consequence
For an exact common hidden frame C*, the accepted commutator estimate gives delta(C)<= (9/2)||C−C*||_F^2. A stereographic grid with integer resolution r has M=(2r+1)^3 and covering radius <=2sqrt(6)/r, so its fixed comparator satisfies delta<=108/r^2. Multiplying the preceding normalized-loss inequality by two gives per-edge
 E sum_t delta_t(C_t) <= 216 T/r^2 + 6 + (16/rho)(M−1)log T.
For fixed m and rho, r of order (T/log T)^(1/5) gives cumulative O(T^(3/5)(log T)^(2/5)), hence vanishing average O((log T/T)^(2/5)). There is no positive excitation/singular-gap condition and no reconstruction of the complete environment. Identity/noise-unexcited rounds simply have zero flip loss. The rate is slower than the accepted full-information gap-free route but avoids its quartic optimizer and large signed coefficient estimator.

For a fixed approximate comparator, retain the explicit factor-two oracle inequality above. Combining the commutator triangle and aggregate Minkowski bound gives expected selected sum <=2(sqrt(Gamma)+sqrt(A))^2 + m[6+16(M−1)logT/rho], with A=(9/2)mT epsilon^2 and Gamma the expected fixed-frame defect on actual histories. This is only a sufficient symmetry-defect objective, not optimal encoder fidelity.

## Finite arithmetic, sampling and stops
`barrier_sampler.py` implements rational root bracketing and integer weights. Each importance update is W/(rho w_j), with W<=D+2M and w_j>=2. Cumulative rational magnitudes are polynomial in T,M,1/rho; storing sums of T such rationals has O(T log(D+M)+T bitlength(rho)) bits. Bisection uses O(log(MD)) exact rational operations and M terms per root test. Computing and storing M arms is charged; this is not a constant-storage/polylog-query controller.

Exact sampling chooses a uniform b-bit integer and rejects values >=W, with b=ceil(log2 W). Success probability is at least1/2. A public rejection cap K makes per-draw failure at most2^(−K). All candidate samplers and prospective role/edge/Bell keys must be scheduled as neutral pre-role preflight: their ranges depend only on the past, and rejection count is independent of the selected index. Any cap abort stops the physical protocol before the source call; analyze the stopped process with zero future losses. The comparator then also uses actual stopped history. A union bound pays the declared number of capped draws times2^(−K) in availability. There is no candidate-dependent post-role abort or assumed future continuation. A complete service/outer-code theorem still must combine the existing all-input transfer and private guard; this manuscript does not silently redefine that instrument.

## Evidence and limits
`check_barrier.py` checks 320 parameter/update cases against high-precision ideal normalization, relative domination, TV and derivative stability; exact rational arithmetic generates implemented q. Independent exact interval tests by the collaborating author are in `finite_barrier_sampler_checks_20261029`. These are controller diagnostics, not a physical bandit trajectory or independent receiving review. No native Bell-interface experiment, calibrated control model, outer-code yield simulation or practical constant claim has been executed here. Existing conventional full-path validation may dominate the direct-star witness at small ports.
