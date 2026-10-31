# Whole two-state bridges from a last refresh: finite-clock receiving construction

Status: NEW candidate, not an amendment of frozen ledgers. This uses ordinary rank-one refresh structure, geometric clocks and bounded-gap singular-value amplification. It is not a general Markov bridge oracle, an implementation of the quantum circuit, or a practical advantage claim.

## 1. Received interfaces and notation

Receive the sharp complete instrument in SHARP_COMPLETE_FIRST_EVENT_ASSEMBLY.md, the fixed-window geometric clock, and the coherent truncated clock. The binding manifest at the end supplies their exact hashes. All physical jump outputs, private source memory, prescribed controls, operator encodings, word phases, count caps and complete-instrument amplification remain those of the sharp construction.

For clarity the base scalar has positive c, r>=8c, delta=r-2c, nu=sqrt(delta^2+8c^2), d=(nu+delta)/2, s=2c^2/d. The Doob chain has rates q_0=s and q_1=d; nu=s+d. Its stationary probabilities are pi_0=d/nu and pi_1=s/nu. The same proof permits distinct off-diagonal c and diagonal QQ coefficient, provided the previously certified positive two-state majorant and separation hold. This note does not substitute parameters silently into a resource table.

The known real scalar rates, thresholds and fixed coin probabilities are acquired classically to certified accuracy. Tiny positive s is not replaced by zero. Certified zero-coupling cases use the existing separate branch. Times are private; there is no total-variation assertion comparing a continuous timestamp to a grid timestamp.

## 2. Exact last-refresh disintegration

The two-state generator is nu(Pi-I), where Pi redraws a label from pi. Thus it can be realized by a rate-nu Poisson refresh process, ignoring refreshes that leave the current label unchanged. Ignoring them yields precisely the visible flip rates q_i=nu*pi_(1-i).

Fix initial i, final j and duration t>0. The event of no refresh has probability exp(-nu*t), and then the endpoint is i. Conditional on at least one refresh, the last refresh label is independent with distribution pi. Its backward gap Y has density nu exp(-nu*y)/(1-exp(-nu*t)), 0<y<t. Conditional on its time u=t-Y and last label j, the process before u is an UNCONDITIONED copy of the original chain started at i: independent Poisson increments and marks prove this directly.

Consequently an entire endpoint bridge is sampled as follows.

* If i differs from j, draw Y as above, run the unconditioned visible-flip chain until u=t-Y, set the last refresh label to j, and remain at j until t.
* If i=j, first choose no refresh with probability

    a_i(t)=z/[pi_i+(1-pi_i)z], z=exp(-nu*t).

  On no refresh return the empty visible word. Otherwise use the preceding last-refresh construction.

Only actual visible flips are Hamiltonian insertion events. At the last refresh append one flip if and only if the preceding label differs from j. If they agree, omit that refresh from the word AND merge the adjacent residence intervals. In particular it creates neither a factor (-i), nor an additional factor-2 Q-dwell normalization. Subsequent QQ Poisson insertions are generated over the maximal visible Q residences, including the final gap. This bookkeeping is essential to recover the exact Dyson word.

At t=0 the same-endpoint word is empty. The different-endpoint conditional limit is one instantaneous required flip, followed by termination; its outer endpoint weight is zero at an exactly zero-duration physical branch. QQ count is zero. These branches bypass conditional-clock division and amplification. The limiting convention is also used if a positive remaining duration rounds to zero.

This construction never enumerates the potentially nu*t invisible refreshes. It simulates only the visible flips and later QQ insertions, stopping and selecting zero at the existing total virtual-word cap K. The aggregate complete-instrument tail already earned in the sharp construction, not a conditional endpoint rejection probability, pays this overflow.

## 3. A bounded-success no-refresh coin without online exponentials

For i=j precompute t_i*=log(1/pi_i)/nu. All constants here are classical. The following fair-branch Bernoulli races have acceptance probability at least 1/2 and, conditional on acceptance, output NO REFRESH with probability a_i(t).

If t>=t_i*, put x=exp[-nu(t-t_i*)]. The two race weights are x and 1-pi_i*x. Their ratio is x/[1+(1-pi_i)x]=a_i(t). A survival comparison of a fixed Exp(nu) clock supplies x; the second weight is the complement of a known pi_i coin AND that survival event.

If t<t_i*, put y=exp[-nu(t_i*-t)]. The weights are 1 and y-pi_i. The latter is exactly the interval event t_i*-t<=Exp(nu)<t_i*. Their ratio is 1/[1-pi_i+y]=a_i(t).

The sum of weights is at least one in both regimes. Choose the branch fairly, then accept its bounded coin. Keep all branch/coin/clock seeds and flags. A bounded-gap preparation normalizes the accepted race; it is not an indefinitely repeated postselection. The accepted branch is the required Bernoulli result. The two formulas coincide at the threshold.

The exact posterior is well conditioned as a probability: |a_i'(t)|<=nu. The race weights themselves have derivatives bounded by a constant times nu, including at the threshold. Thus changing t or the precomputed threshold by h changes the raw race law by O(nu*h), and normalization costs only the constant success lower bound, never 1/pi_i. Clamping a rounded interval endpoint to its valid interval costs the same bound.

## 4. Event input-sector weights from a second bounded race

The event arm needs initial-sector P with probability

    p(t)=E_QP/(E_QP+E_QQ)
        =c(1-z)/[c+s+(d-c)z], z=exp(-nu*t).

Set a0=(c+s)/d<1, t*=log(1/a0)/nu. The inequality follows from the high-rate separation. Precompute both and the constants c/(c+s), s/(c+s).

For t<t*, y=exp[-nu(t*-t)], use weights

    wP=c/(c+s)*(y-a0),
    wQ=1+s/(c+s)*y.

For t>=t*, x=exp[-nu(t-t*)], use

    wP=c/(c+s)*(1-a0*x),
    wQ=s/(c+s)+x.

Each weight divided by two is a valid coin. Choose P or Q fairly and use that coin; the total acceptance is (wP+wQ)/4>=1/4. In the early regime y-a0 is the interval event t*-t<=Exp(nu)<t*. In the late regime 1-a0*x is the complement of a known a0 coin AND an exponential survival comparison. A coin of weight wQ/2 is a fair mixture of its two displayed terms. No coherent ratio, exponential or square root of E_Qi is evaluated.

Algebraically, in the early regime wP+wQ equals [c+s+(d-c)z]/(d*z); in the late regime it equals that denominator divided by c+s. Both accepted P ratios are exactly p(t). At the threshold they agree. Differentiating gives p'(t)=c*nu^2*z/[c+s+(d-c)z]^2; the high-rate bounds imply |p'|<=2nu. Alternatively the bounded raw coin derivatives and acceptance>=1/4 give a slightly looser constant. Again there is no rare-endpoint denominator.

No-event endpoint weights are evaluated classically at the current classical window endpoint and prepared with their paid rotations. Event endpoint choices use this race because the event time is coherent.

The event race prepares E_Qi/S1, S1=E_QP+E_QQ. The associated conditional word average supplies JK0/(alpha_L*sqrt(mu)*S1). The already acquired outer proposal has density w=(alpha_L*sqrt(mu)*S1)^2. Its normalization cancels this denominator algebraically. The circuit need not calculate S1, sqrt(w), or E_Qi online. The three outer exponential component labels stay private, orthogonal Kraus coordinates with their existing normalized common-density interpretation.

## 5. Finite clocks and actual normalization

Choose one global time mesh h for a physical first-event call, rounding it DOWN to a power of two. Choose a classically certified window W that is a power of two, at least max(tau_max, t_0*, t_1*, t*) plus two mesh units. Then W/h is an integer power of two, exactly as required by the uncensored product-clock circuit. Arrange outer timestamps on this same h-grid: for example the outer bin mesh is 2h or an even integer multiple of h, so its midpoints lie on the h-grid; round classical window endpoints to the same grid with the separately charged physical-time error. The N=0 bypass remains explicit. Fixed Exp(q) clocks for q in {s,d,nu,2*c_diag} are prepared on [0,W] with the exact integrated geometric-bin probabilities and a tail atom. Their binary rotation angles depend only on q,h,W and are precomputed, with certified numerical error. Conditional last-gap sampling on coherent t=N*h uses the already acquired leading-bit envelope M=2^ceil(log2 N), followed by the m<N flag. Its success is at least 1/2. It does not use an endpoint transition probability.

All comparisons, integer additions/subtractions, leading-bit computation and flag erasures are reversible. A clock bin is coupled in the proof to its exact conditional continuous value. The returned time differs by at most h. Uncensored clocks are compared to the coherent remaining duration; the tail atom is beyond every relevant threshold. Events at rounded equal times retain the known chronological word order and create zero intervals, rather than swapping operators.

There are at most three bounded conditional factories per whole event bridge: endpoint race, same-endpoint no-refresh race, and last-gap clock. Controlled absent branches skip the factory. A no-event bridge needs at most the last two. The unconditioned visible prefix uses at most K+1 waiting draws before its overflow flag. QQ generation uses at most 2K+2 waiting draws. Thus there are O(K) fixed-clock draws, not O(K) conditional bridge factories. Loops are padded to their caps, and overflow selects zero without renormalization.

For a fully safe source-vector implementation use the received rectangular polar polynomial with singular interval bounded below by 1/2 (race success>=1/4). Its degree is O(log(1/eta)), phase/good-polynomial approximation is O(eta^2), and total subsequent circuit synthesis error is O(eta). The additional real-part/signal ancilla is paid. The polynomial coefficients and phase preprocessing are finite, paid classical operations. This already closes the construction without an exact acceptance oracle.

A less stringent, separately scoped internal-MEAN variant is also valid. For success amplitude x>=1/2 the polynomial

    p_l(x)=x sum_(k=0)^l [binom(2k,k)/4^k]*(1-x^2)^k

is bounded by one on [-1,1] and has 1-p_l(x)<=4*(3/4)^(l+1). Choose the tail <=eta/100 and approximate the GOOD polynomial to eta/100 with strict boundedness margin. Its failed probability is O(eta), though its failed amplitude can be O(sqrt(eta)). The circuit subsequently SELECTS ZERO on this failure and unprepares the same source. Therefore only failed probability enters the selected mean block. On success the target conditional law is unchanged; a success phase depending on the preserved input labels cancels between PREP and PREP dagger. Fresh flags and all seeds must remain present until unpreparation, and SELECT must be diagonal in these history labels. Actual full-circuit synthesis error is still allocated in operator norm. This variant does NOT claim an eta-close public source isometry and does NOT weaken the outer complete physical instrument amplification requirement.

One may instead use ordinary fixed-point search with the same constant success gap. No optimal phase-count claim is needed here. The three-PREP alternative plus actual scalar P(t) arithmetic remains a legitimate comparator; neither option is declared cheaper without an actual gate audit.

## 6. Finite-grid error proof without endpoint floors or tie deletion

The following is a conservative explicit allocation, not an optimized precision ledger. Let eta be the allowed inner selected-mean error, let K be the already fixed aggregate virtual cap, and put

    Qrate=1+nu+2*c_diag,
    Lword=1+alpha_0*T+mu*(alpha_H+1),
    D=K+4.

Choose h<=eta/[10^7 * D^3 * (Qrate+Lword)]. Classically acquired rates/coin probabilities/thresholds are approximated so that their total raw-law perturbation over the capped construction is <=eta/100. For instance rate errors <=eta/[10^7*D^3*(1+W)] and threshold errors <=h suffice, with corresponding fixed rotation accuracies. Comparisons use grid integers, not an exact-real branch oracle. Branch formulas have an overlap interpretation at a rounded threshold; either neighboring branch differs by O(nu*h).

The last-gap conditional exponential quantile is 1-Lipschitz in its truncation duration under a shared uniform. Its binned output differs by <=h. Hence its endpoint u changes by at most the input duration error plus h. In the unconditioned visible prefix, couple identical exponential waiting times before discretization. After at most K draws, accumulated time displacement is <=O(D*h). A stopping decision can differ only when the next independent exponential lies within that displacement of the remaining horizon. Its density is <=q_state<=nu; a conditional union bound gives O(nu*D^2*h). No union over all possible coherent histories is taken. The same proof for QQ clocks gives O(2*c_diag*D^2*h), including the changes in maximal Q residence lengths caused by the prefix displacement. Extra polynomial slack in D covers the at most K residences.

On the coupled event, the word and its phase (-i)^V agree exactly, each event time moves by O(D*h), and total interval displacement is O(D^2*h). Contractive telescoping bounds the operator word error by O(Lword*D^2*h), using the actually acquired normalized fast-kernel derivative and ordinary H0 interval simulation. Retaining zero-length intervals preserves the word. The forced last refresh contributes no operator on a self refresh, as specified above. Thus the selected mean block differs by at most eta/10 with the displayed conservative h; bad-law mass is charged linearly because SELECT is a contraction and all its history labels are retained. There is no conversion of this particular mean-law estimate into a falsely linear source-vector estimate.

The bounded normalization factories contribute at most eta/10 after allocating eta/(100*D) to each actual factory and its controlled composition, using either the safe vector convention or the explicitly scoped selected-mean convention. Fixed rotation synthesis, reversible arithmetic, operator encodings and scalar parameter preprocessing use a further eta/10 total circuit budget divided by their ACTUAL circuit operation counts. The allocation is polynomial in log(1/eta), K, input bit lengths and log rates; computing W or its bit length does not require runtime proportional to W. Very small rates or stationary weights increase input/precision bits, not inverse-probability rejection runtime.

The outer geometric-bin coupling and exact capped-future channel hybrid remain separate: choose its mesh to charge both normalized outer operator variation and physical remaining-time Lipschitz error. It can share the smaller of its mesh and h. In particular include the full physical generator bound, not only Lword. No timestamp is released. Count overflow, window caps, actual jump output, source controls and their operation costs remain the previous complete proof.

## 7. Receiving allocation and consequence boundary

Let epsilon_step be the desired complete-instrument error and A the actual sharp amplifier normalization. Take beta=epsilon_step/(128*A). Keep the aggregate omitted-word error at its existing complete-instrument target; do not replace it by a conditional endpoint cap. Set eta=beta/10^4 for this source and subdivide all numerical/circuit errors as above. Sharp outer amplification then prices the new base error by at most 32*A times that error. The outer common-bin/time hybrid, count cap, prescribed-control composition and actual operation calls are unchanged and separately paid.

This removes conditional next-event CDF inversion and online event-weight exponentials, and reduces the number of conditional normalization factories from one per virtual flip to a constant per whole bridge. It does not remove O(K) visible-clock/operator slots, outer amplification, retained-memory execution, finite kernel synthesis, actual phase/rotation gates, or acquisition of the physical operators. No new numerical ledger or crossover is asserted by this note. The existing frozen three-call arithmetic ledger remains a valid alternative and a historical baseline.

## Binding manifest

Sharp complete assembly: 857672be623bc99c69c2995ec489c504df4fba9b6b5c4fd0ee56ad06f27ab07f.
Fixed-window geometric clock: 16335629791a1bfa6368171f39182fde71b61d957c87e2af0c26188684809500.
Coherent dyadic clock: 71a7d3ecb1cf66fb759a4048d7af027ef80dd2f75a9395baf62e181e724ed13a.
Their clock review: 6c8c13eeab09846e405659fd1336dec831be31f0312a0b055d407eb5b9fd5cfa.
The explicit bounded-polynomial realization uses the already bound real-polynomial rectangular QSVT convention, Gilyen et al. arXiv:1806.01838, Corollary18, and paid polynomial/phase preprocessing as in Haah arXiv:1806.10236, Section4.3. These are ordinary components, not new amplification claims.
