# Direct complete-MMSE-order falsification with all-trial accounting

Status: elementary derivation and arithmetic tests; external mathematical review and historical priority remain open. This is a proposed prospective experiment, not an acquired apparatus result.

## 1. Exact task and source comparator

Retain the measured-POVM packet's definitions, local preparation rotations, and scores. In particular, the hidden label is L in {-1,+1}, equiprobable; i in {-1,+1} is an independent equiprobable preparation coin;

    sigma_i = (I+b Z+i b X)/2,          b=9 sqrt(2)/20,
    tau_(L,i) = (I+L i r X+z Z)/2,    r=6/11, z=9/11,
    rho_L = (1/2) sum_i sigma_i tensor tau_(L,i).

The exact frozen local product unitary conjugates rho_L. Its two stereographic vectors and scores are read without alteration from `frozen_design.json`. Scores are

    s = (-719,646,-270,149)/1000.

For an all-trial experiment, add failure outcome 0 and freeze its score to zero. Every attempted preparation belongs to the denominator. The receiver gets only the specified quantum systems and fixed control, with no unintended classical access to L or i. The source gets i only on its independent reveal branch and has the same quantum-reference access as the mathematical comparator. A biased label schedule requires explicit reweighting and additional drift assumptions, below.

The ideal source reveals i with probability q. In the revealed branch its reference average state is B=(I+zZ)/2 and label-weighted state is H=i r X/2. The Hermitian estimator A=i r X solves

    (B A+A B)/2 = H.

Completing the square, or the standard SLD/binary-MMSE identity, gives optimal squared-error risk 1-r^2. In the erase branch the reference is B for both labels, so its optimal score is zero and risk is one. Therefore the unrestricted source optimum, with its reference retained, is exactly

    R_source(q)=1-q r^2,      g_source(q)=q r^2.

A common local reference rotation conjugates its optimal estimator and leaves this value unchanged. No artificial source-estimator restriction is introduced. For q=9/20, g=81/605; for q=43/100, g=387/3025. These are separate source experiments and must be chosen before new evaluation.

## 2. A directly observable witness, with complete denominators

For each attempt, record the hidden label after measurement and the frozen receiver outcome K. Define

    Z=2 L s_K-s_K^2 = 1-(L-s_K)^2.

Thus target risk is 1-E Z, without any detector tomography. A valid lower confidence bound G_low for E Z exceeding q r^2 proves that this target estimator beats the optimal ideal source on this particular binary task, provided the state/interface contract holds. One strict task witness falsifies the claimed complete ordinary MMSE dominance. One successful task cannot prove a complete order in the other direction, and this operation does not establish stochastic decoding, physical channel simulation, or a capacity advantage.

All-trial recording absorbs outcome-dependent efficiencies and selection into the actual observed law. A four-outcome success-conditioned model alone cannot supply this statistic. Failure score zero is a chosen estimator, so it supplies a sufficient witness; an informative failure outcome may admit a better score, but must be modeled and frozen independently.

## 3. Preparation uncertainty has an exact paid allowance

Let intended rho_L and actual rho_tilde_L obey trace distance

    (1/2)||rho_tilde_L-rho_L||_1 <= eta_L.

For every complete physical POVM, including its failure effect, put A_L=sum_k z_(L,k) F_k, where z_(L,k)=2 L s_k-s_k^2. Positivity and completeness imply

    min_k z_(L,k) I <= A_L <= max_k z_(L,k) I.

For trace-zero D=rho_tilde_L-rho_L and an observable aI<=A<=bI, shifting by (a+b)I/2 and applying trace-norm duality gives

    |Tr A D| <= (b-a) (1/2)||D||_1.

Consequently the intended and actual balanced gains differ by at most

    B_prep=(R_- eta_-+R_+ eta_+)/2,
    R_-=526071/200000=2.630355,
    R_+=565929/200000=2.829645.

If both trace distances are at most eta, B_prep=2.73 eta. A confidence-valid sufficient acceptance rule is

    G_low - B_prep > q*36/121.

If the preparation bound has simultaneous coverage 1-gamma and the statistical lower bound has coverage 1-alpha, the resulting decision has error at most alpha+gamma by the union bound. The program does not establish either apparatus calibration or preparation coverage from a declaration. These must come from independent defensible evidence. It returns `PREPARATION_UNCALIBRATED` when no preparation bound is supplied.

This allowance protects the intended ideal task against target preparation mismatch. It is not a formula for the optimum source risk under arbitrary noisy preparations, nor evidence of a hardware source being ideal. A fully physical matched-arm comparison requires its own source model or a separate source-risk bound.

## 4. A drift-aware pooled confidence rule

Use fresh equiprobable hidden labels and preparation coins on every trial. Let the receiver POVM at t be predictable from past history, with no extra access to the current label/coin. Write mu_t=E[Z_t | past]. The pooled observation range is

    a=-1.954961, b=0.921039, R=b-a=2.876.

Conditional Hoeffding's lemma gives

    E[exp(lambda*(Z_t-mu_t)) | past] <= exp(lambda^2 R^2/8).

Multiplying these conditional bounds and applying Markov's inequality yields, at a predeclared horizon N,

    P[(1/N)sum_t mu_t < mean(Z)-R sqrt(log(1/alpha)/(2N))] <= alpha.

Thus this lower bound is valid for the average predictable gain without an IID apparatus assumption. If the same intended states are prepared each time, averaging the predictable POVMs still gives a physical POVM. After paying valid per-trial or average preparation allowances, strict excess over q r^2 therefore supplies a common intended-task witness. It does not guarantee future performance or stability.

For optional stopping, use a valid confidence sequence. A deliberately simple explicit construction is to substitute alpha_N=6 alpha/(pi^2 N^2) in the fixed-N bound and union-bound over N. More efficient established mixture, stitched, and empirical-Bernstein confidence sequences are available; these statistical methods are prior art. A fixed-N bound cannot be repeatedly checked at level alpha without correction.

## 5. A cheaper stationary stratified rule and its planning cost

If a common stationary receiver applies to both label strata, collect fixed n_- and n_+ independent or appropriately concentrated trials and estimate the balanced gain by

    G_hat=(mean(Z|-)+mean(Z|+))/2.

Applying Hoeffding to the weighted observations gives

    V=(1/4)(R_-^2/n_-+R_+^2/n_+),
    G_low=G_hat-sqrt(V log(1/alpha)/2).

For fixed N=n_-+n_+, Cauchy-Schwarz minimizes V at n_+/N=R_+/(R_-+R_+)=0.51825, giving V=(2.73)^2/N before integer rounding. This allocation changes acquisition proportions while preserving the intended balanced risk by explicit reweighting. It does not justify ignoring receiver drift correlated with label stratum. Use the randomized pooled rule above when the common-stationary-receiver premise is unavailable.

For a true gain gap delta, a sufficient fixed-N test with type-I error alpha and power at least 1-beta is obtained by requiring

    N >= R_eff^2/(2 delta^2) * (sqrt(log(1/alpha))+sqrt(log(1/beta)))^2,

where R_eff is 2.73 for the stationary continuous optimal allocation, or 2.876 for the pooled rule. This follows by summing the upper-tail confidence radius and lower-tail alternative deviation radius. It is a sufficient worst-range budget for this elementary rule, not an information-theoretic lower bound or a best available statistical procedure. Round the stratum sizes and check V before preregistration.

At alpha=.05, beta=.20, with no paid preparation/failure loss and with the packet's deterministic positive gaps assumed to hold:

| Frozen source/box | delta | Stationary stratified sufficient N, approximately | Pooled sufficient N |
|---|---:|---:|---:|
| q=.45, component tolerance .0005 | .0002456917993 | 555,390,657 | 616,383,549 |
| q=.43, component tolerance .001 | .0046028993220 | 1,582,403 | 1,756,182 |

The smaller `center_crossing_trial_count` values in the JSON only put a confidence halfwidth below delta; they are not 80% power guarantees. Any preparation allowance or loss-inclusive gap reduction lowers usable delta and raises the cost. If preparation coverage consumes part of the desired total error, reduce alpha accordingly. Calibration confidence and control costs are absent from this prospective numerical calculation, so these numbers are not an apparatus-readiness claim.

## 6. A sharp flag-only efficiency gate, even for biased heralding

Consider any balanced binary label with any success outcomes and exactly one classical failure outcome f. Let success probability be s. No informative residual quantum or classical failure output is allowed in this theorem. For each output y put

    p_y=P(Y=y), m_y=E[L 1_(Y=y)].

The optimal posterior-mean squared-error gain is G=sum_y m_y^2/p_y. The constraints are |m_y|<=p_y and sum_y m_y=0. Let M=sum_success m_y=-m_f. Since the successful probabilities sum to s,

    sum_success m_y^2/p_y <= s,
    |M|<=min(s,1-s).

For 0<=s<=1/2,

    G <= s+s^2/(1-s)=s/(1-s).

For s>=1/2, G<=1. Hence the universal envelope is

    G <= min(s/(1-s),1).

For s<=1/2 it is sharp: give a perfectly identifying success only on label + with conditional probability 2s, and otherwise emit f. The success score is +1; the failure score is -s/(1-s). The exact gain is s/(1-s). For s>=1/2, split the successes into perfectly identifying label outcomes and make failure identify only one label, achieving gain one. These are classical sharpness examples, not realizability assertions for the packet's faithful quantum states.

It follows that a strict target improvement over source gain g=q r^2 requires

    s > g/(1+g).

The thresholds are 81/686≈.118076 at q=.45 and 387/3412≈.113423 at q=.43. In particular a .001 success probability permits at most 1/999 gain under this flag-only contract, even allowing optimal scores and label-biased heralding. The theorem fails if informative output is retained after failure: retaining the label as a second failure output yields gain one at arbitrarily small success probability. The same issue arises with an informative retained quantum reference. Welte's nondestructive architecture makes this caveat substantive; its normalized success-conditioned effects do not establish the needed failure instrument. No hardware-wide Welte no-go is claimed.

If the herald is label-independent and the entire success-conditioned law matches the modeled conditional task, score-zero failure gives exactly G_all=s G_cond. The packet's lower conditional gain bounds then yield the sufficient efficiencies

    s > .9981682560  (q=.45, .0005 box),
    s > .9652707784  (q=.43, .001 box).

These are paid engineering gates for that explicit fair-loss model. Neither the printed box nor a published coincidence fraction establishes their antecedents.

## 7. Same-information comparator and status

The strongest relevant incumbent is direct task-loss estimation on the same complete attempt records, with a suitable variance-aware or multinomial/likelihood confidence procedure, frozen in advance. It can use every observation used here. It may improve the Hoeffding planning cost. The proposed procedure introduces no additional observable information and has no established sample, runtime, hardware, or scientific-capability advantage over this incumbent.

The value of this derivation is the exact translation from the supplied mathematical witness to an all-trial, preparation-paid decision contract and explicit rejection gates. The source source-optimum calculation, posterior-mean risk identity, trace-distance bound, Hoeffding inference, and confidence-sequence machinery are established ingredients. Historical novelty of this combination or of the flag-only bound has not been established. No new physical operation has been acquired.
