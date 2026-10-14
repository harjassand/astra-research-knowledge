# Three-snapshot certification with a matched random clock

15 October 2026, Australia/Brisbane. Root construction. Status: internally derived theorem, independently scrutinized by same-team agents; externally unreviewed, novelty UNKNOWN, no physical experiment. This is a scientific inference operation, not an energy or manufacturing technology.

## Exact operation and assumptions

Let X be a stationary irreducible finite continuous-time Markov chain with generator Q and stationary distribution pi. All microscopic variables are even under physical time reversal. Define sigma = sum_{i<j}(pi_i Q_ij-pi_j Q_ji) log[(pi_i Q_ij)/(pi_j Q_ji)] in nats per unit time. This is a mathematical path-irreversibility rate; physical entropy production additionally needs the physical reversal and local-detailed-balance interpretation.

Take three binary snapshots Y_-,Y_0,Y_+. Deterministic labels are allowed. More generally, conditional on microscopic states, the three detector outputs may be independent Bernoulli variables with any fixed unknown probabilities b_i in [0,1]. The detector must not change the specimen dynamics, retain correlated memory, or add an unaccounted driven hidden system. No full-path or uninterrupted-residence observation is required.

Choose r in (0,1) before the test. Let the left and right gaps be independent draws from the SAME distribution rho, independent of specimen and readout, with finite known mean m>0. A fixed gap is a special case. Record

    W = Y_0 (Y_- - r)(Y_+ - r),     c = r(1-r).

If its true stationary mean is -D<0, then every compatible finite all-even hidden CTMC, with no state-count/rate/activity cap, satisfies

    sigma >= -log(1-D/c)/m.                                      (1)

The data must have 0<D<c for a finite-cost compatible model; D>=c excludes every such finite-cost model. The theorem is a lower certificate, not the minimum compatible sigma.

## Proof, including the physical-access change

If sigma is infinite the conclusion is automatic. Otherwise forward and reverse flux supports agree. On a window of duration T define P as the stationary hidden path law and P^R as its ordinary time reverse. The stationary adjoint is Q*_ij=pi_j Q_ji/pi_i, and Q*_ii=Q_ii. Let nu have path density sqrt(dP dP^R). Its initial distribution is pi and its path generator is the possibly killed operator

    G_ij = sqrt(Q_ij Q*_ij) (i!=j),     G_ii=Q_ii.

AM-GM gives row sums at most zero. G is self-adjoint in the pi inner product. Its path mass A is the Hellinger affinity, not a normalized equilibrium path law. No stationarity of the killed semigroup is asserted.

For fixed gaps s,t, integrating the three independent detector emissions gives

    integral W dnu = sum_i pi_i b_i [exp(sG)(b-r1)]_i
                                      [exp(tG)(b-r1)]_i.

Averaging INDEPENDENT IDENTICALLY DISTRIBUTED gaps makes this a sum of nonnegative squares. For unequal deterministic gaps or correlated gap pairs the square argument is unavailable; approximate equality is not silently assumed.

Let mu=(P+P^R)/2, including the same clock and detector kernels. Its observable W expectation equals the forward expectation because W is invariant under exchanging endpoints and the clock law is exchangeable. Pathwise AM-GM gives mu>=nu. Since W>=-c,

    -D = integral W dmu >= -c(1-A).

The stationary path entropy S=log(dP/dP^R) has E S=T sigma. Jensen yields A_T=E_P exp(-S/2)>=exp(-T sigma/2). Averaging the clock and applying Jensen again gives A>=exp(-m sigma). Thus D/c<=1-exp(-m sigma), proving (1).

This improves the existing N512 generic range transfer for this particular reflected-square statistic by using positivity under the KILLED geometric path measure. N512 and the October 3 hidden-dissipation predecessor already supply the general path-affinity idea. The inequality is developed here as a scoped specialization; no historical priority is asserted.

## Independently reproducible target

Use the specified three-state ring Q=[[-21/20,1,1/20],[1/20,-21/20,1],[1,1/20,-21/20]], with uniform pi and label B={1,2}. Its complete binary observed path law is time-reversal invariant. Choose r=9/10. Exact rational uniformization of exp(tQ), followed by exact interval logarithms, evaluates (1) for fixed t=3/10 and iid gaps in {1/5,2/5}, each with probability 1/2. The checker also verifies all eight observable triplet probabilities, equilibrium controls and a parity-reversible six-state countermodel. These are calculations on supplied mathematical generators, not empirical observations.

The same target is present in prior work. Comparing a larger certified floor with a previously exhibited floor compares two valid certificates, not two optima or complete experimental costs. Existing waiting-time, hidden-model optimization, reflected-moment and nonlinear inference methods are serious competitors.

### Best centering in this score family and an all-time consequence

Let c_uv=Pr(Y_-=u,Y_0=1,Y_+=v) for u,v in {0,1}. Direct expansion gives

    -E W_r/[r(1-r)] = c_01+c_10 - c_00 r/(1-r) - c_11(1-r)/r.

For positive c_00,c_11, AM-GM maximizes this ratio at r=sqrt(c_11)/(sqrt(c_00)+sqrt(c_11)), giving

    C = c_01+c_10-2 sqrt(c_00 c_11),
    sigma >= -log(1-C)/m,  if 0<C<1.                         (2)

This is the optimum within the W_r family, not over every statistic or hidden-model inference method. Boundary cases use limits. In physical estimation, optimizing r on test data requires simultaneous confidence bounds or a held-out calibration set; preregistering r=9/10 avoids this cost in the explicit fixture.

For the deterministic-label ring with clockwise rate 1 and reverse rate q in (0,1), p=2/3. At small fixed gap t, direct first-jump expansions at the middle B state give c_00=p q t^2+O(t^3), c_01=c_10=p(1+q)t/2+O(t^2), and c_11=p+O(t). Hence C/t tends to p(1-sqrt(q))^2. Inequality (2) holds for EVERY t>0 for every exact compatible finite all-even realization, so taking t down to zero in the target statistics proves

    V_infinity(P_q) >= (2/3)(1-sqrt(q))^2.

At q=1/20 this is (21-4sqrt(5))/30 > 2/5. The strict comparison follows from 9>4sqrt(5), equivalently 81>80. This is an analytic all-architecture bound for an exactly supplied path law. It does not give a finite-resolution experiment the t->0 information for free. The small-time negative score is O(t^2) for the near-optimal r, so shrinking the clock makes ordinary bounded-observation acquisition harder. No exact optimum or finite attaining realization is determined.

## Acquisition and error contract

For n INDEPENDENT stationary triplets and a predeclared r and clock law, W has range width R=max(r,1-r). At confidence 1-alpha, E W <= sample_mean + R sqrt(log(1/alpha)/(2n)). An independently justified total-variation discrepancy epsilon between the acquired triple law and ideal specimen/readout/clock law adds R epsilon. Insert the negative of this upper bound as D_lower in (1), only when positive. If only a mean-gap upper bound m_upper is justified, replace m by m_upper. Clock/state dependence, sample-adaptive selection without correction, unknown stationarity, readout memory and dependent windows are not covered by iid Hoeffding. Independent preparations or separately established dependence control are paid inputs.

A physical trial must measure a suitable binary state nondestructively, acquire the actual reversal/parity model, randomize matched clocks, check detector memory/back-action and prepare stationary independent trials (or justify mixing). The matched incumbent receives the same raw snapshot records, timing, calibrations and preparation budget. No such trial was executed.

The checker supplies two material falsifiers. Correlated gap pairs (1/10,1) and (1,1/10), equally likely, have identical left/right marginals but yield a negative score in a TWO-state equilibrium chain: exchangeability does not replace independence. In the supplied ring, 5 percent independent symmetric errors at all three readouts, with the explicitly tested r=43/50, make the score positive. The theorem still holds, but this noisy test returns no certificate. Noise tolerance of the inequality is not useful sensitivity at every error rate.

## Exact remaining obstruction and experiment

The same ring's complete binary law has a six-state irreducible lift whose generator uses Q in one orientation, Q* in the other, and symmetric orientation flips only at the singleton reset state. Parity swaps the orientations. The lift has zero PARITY-reversed path entropy production and exactly the same stationary observed law. Therefore binary snapshots or even the entire binary trajectory cannot establish the all-even physical premise. This does not refute (1), whose premise explicitly fixes ordinary reversal.

The decisive physical comparison must acquire an extra orientation/velocity observable or a calibrated intervention that distinguishes the two realizations, together with an independent energy/entropy ledger. An abstract parity-labelled generator is not a fabricated equilibrium device. If no such physical interface is obtained, the output remains an all-even model-class certificate, not a specimen heat measurement or a closed technological operation.

References: Astra N512, source proof modules and current gate records; https://www.evidencepress.org/releases/hidden-dissipation-floor/ (unrefereed candidate); https://arxiv.org/abs/2609.14623 (target); https://doi.org/10.1103/PhysRevLett.127.198101 (waiting-time incumbent). Exact source pins and inspection depths are in the campaign source ledger and worker reports.
