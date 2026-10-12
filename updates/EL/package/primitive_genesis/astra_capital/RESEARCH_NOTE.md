# Occupation probes for certifying a frozen sequential predictor

Status: internally reconstructed mathematical candidate; historical originality, independent correctness and physical realization remain UNKNOWN. No theorem is imported merely because Astra has a card for it. The operation below builds on the full original N718 product-completion argument, whose source status remains unreviewed. It is not a claim of a foundational breakthrough already achieved.

## The capability question

Can one certify the whole visible path predicted by a frozen controller/world-model pair, without reconstructing its hidden generator, knowing the number of hidden states, or supplying a hidden deployment-density bound?

The positive answer below is conditional on a concrete active experiment: restart the same controller, stop it at an independently sampled occupation time, retain the actual hidden state, then apply a small library of product-compatible kinetic probes. This is stronger than the N718 future-prediction interface in one specific respect: the source requires deployed hidden marginals to be bounded by a supplied multiple of a training preparation. Here the controller itself prepares the distribution to which the certificate applies. It also permits a frozen predictor depending on the entire visible history, rather than only a finite-state Markov model. It does not certify a new policy without new experiments, and it can conservatively reject a correct observed predictor when its hidden instantaneous rates remain variable conditional on visible history.

The immediate mathematical operation is an experimentally acquired squared instantaneous-rate error. Its implications are simultaneous guarantees for every bounded visible-path functional: survival, thresholds, hitting events, multi-time correlations and any reward of the same frozen feedback policy.

## 1. Source reconstruction and the first failed attack

Pinned Astra revision: `5fc72a144d77c31b400efc0768afd7833c702362` of `harjassand/astra-research-knowledge`.

I read `00_START_HERE.txt`, the relevant dossiers and gates, all 428 lines of the original N718 proof, and the decisive N713 original proof sections, rather than treating the cards as premises. Source hashes and read ranges are in `SOURCE_RECEIPTS.json`.

The full N718 argument has three decisive steps. For a bounded hidden row generator Q, visible indicators e_a, a possibly nonstationary preparation nu, and actual probe gains g_u, product settings supply the positive form

    E_a(w) = sum_(i!=j) nu_i q_ij [sum_u w_u g_u(i,j) - (e_a(j)-e_a(i))/2]^2.

With selective probes, all within-label gains equal one and sum(w)=0. Alternatively, a counter must report all modeled microscopic jumps, not merely label changes. Define the signed mathematical operator

    V_a = [Q D_a - D_a Q - diag(Qe_a)]/2.

Then the exact nonstationary identity is

    <Qe_a,Qe_b>_nu = nu Q D_a Qe_b - nu D_a Q^2e_b - 2nu V_a Qe_b.

The first term cannot be dropped without stationarity. These formulas are independently rederived in Section 4 below. N718 subsequently bounds the whole path of a finite action library using a supplied hidden-density domination constant C. That is the gate attacked here.

### Failed stronger claim: small training residual certifies future deployment without coverage

This fails even for three hidden states, balanced visible preparation, the same deployment start as training, one action and a bounded generator. Let

    Q = [[-1,1,0], [0,-1,1], [0,0,0]],
    labels = (A,A,B),
    nu_delta = ((1-delta)/2, delta, (1-delta)/2),  0<delta<1.

The training-averaged reduced rate is l_delta = 2delta/(1+delta) from A to B. The N718 residual trace is exactly

    tr Gamma_nu = 2delta(1-delta)/(1+delta),

which tends to zero. The two visible masses tend to 1/2; rare visible labels are not the problem. The first A state moves internally to the second A state, whose B rate is one. At time T, the true B probability is

    1 - exp(-T) [delta + ((1-delta)/2)(1+T)],

whereas the reduced B probability is

    1 - ((1+delta)/2) exp[-2delta T/(1+delta)].

Their difference tends, as delta decreases to zero, to

    [1-(1+T)exp(-T)]/2.

At T=4 this is approximately 0.45421. Thus no bound tending to zero with the training residual alone can hold. Full microscopic support and visible balance do not fix the problem. The internal A transition moves probability onto a state that training had almost missed. This counterexample killed the first universal-transfer attack.

## 2. Changed attack: let the controller prepare its own occupation law

Let X be a finite hidden pure-jump process. Its actual action J_t belongs to a finite library {1,...,s}; action j has unknown generator Q^j. The controller is a fixed, well-posed, predictable function of the visible label history H_t and its exogenous randomness. Every deployed and probed generator has a supplied exit-rate bound R>0. Let Y_t=ell(X_t) have k labels. The initial hidden preparation is repeatable. No stationary law, hidden-state count, full support or mixing claim is assumed.

Fix a horizon T and freeze a candidate predictor. Given the same visible history, the candidate supplies nonnegative off-diagonal hazards lambda_b(t,H_t), b != Y_t, with total exit rate at most R. The controller and predictor must be frozen before validation; a policy changed after validation requires another preparation experiment. Define the k-vector

    vhat_b(t,H_t) = lambda_b(t,H_t),             b != Y_t,
    vhat_(Y_t)(t,H_t) = -sum_(b != Y_t) lambda_b(t,H_t).

The candidate can use arbitrary stored visible history and computation. Computing it is a charged operation. There is no claim that an arbitrary history-dependent model is efficiently executable or learnable.

Choose U independently and uniformly on [0,T]. Run the actual controller to U, record H_U and its current action J_U, retain X_U without observing it, and branch into a probe trial. Define the action occupation submeasures

    omega_j(i) = (1/T) E int_0^T 1{J_t=j,X_t=i} dt.

They are not normalized distributions. Their masses m_j sum to one. Some action masses and some visible masses may be zero. No division by any of them is performed.

The branch is a counterfactual *distribution* interface. Every raw nodal mean uses a fresh independent reset/replay and an independently randomized stop, so that its pre-probe joint law of (X_U,H_U,J_U) is identical. The chosen probe must have no effect before the stop; its identity is randomized after the stop or kept causally isolated beforehand. A hidden state is not cloned, observed or restarted from a recorded microscopic configuration. Reusing the same physical trial after a probe without restoring the preparation would break the proof. If the available experiment cannot reproduce the unprobed controller law before each branch, the certificate does not apply.

The quantity to acquire is

    D = (1/T) E int_0^T || Q^(J_t)E(X_t,:) - vhat(t,H_t) ||_2^2 dt.

This is a true nonnegative scalar. It has units of rate squared. The occupation procedure acquires D against precisely the states, actions and histories visited by this controller, not an unrelated training law.

### Theorem A: whole-path certificate with no hidden coverage constant

Let P be the actual visible path law on [0,T]. Let Phat be the path law generated by the frozen predictor hazards, the same controller map and the same initial visible law. Then

    TV(P,Phat) <= min{1, T sqrt((k-1)D)}.                         (A)

There is no minimum visible-rate denominator, minimum label probability, hidden-state count or hidden-density domination constant in (A).

**Proof.** At a hidden state i of visible label a and action j, put r_ib^j = sum_(l:ell(l)=b) q_il^j for b != a. Construct a comparison hidden process which retains within-label rates and rescales rates toward each other visible label to total lambda_b(t,H_t). If r_ib^j=0 but lambda_b>0, distribute the added comparison rate over any hidden states of label b. An empty fiber can be supplied with an extra comparison-only dummy state; the true process has zero mass and zero incoming rates there, so D is unchanged. The comparison process has exactly the predictor's visible intensities, even though its microscopic dynamics depend on history. Its exit rate is at most 2R, which suffices for nonexplosion; that comparison process is never a requested physical probe.

Couple true and comparison processes with their common rates until the first discrepancy. While their histories agree, their controller choices and predictor evaluations agree. The discrepancy intensity is at most

    sum_(b != a) |r_ib^j-lambda_b(t,H_t)|.

Integrating its expectation under the true process bounds the probability of a coupling discrepancy, and therefore bounds visible-path TV. Cauchy-Schwarz first over destinations and then over occupation time gives

    E int_0^T sum_(b != Y_t) |r_(X_t)b^(J_t)-lambda_b| dt
       <= sqrt(k-1) E int_0^T ||Q^(J_t)E(X_t,:)-vhat||_2 dt
       <= T sqrt((k-1)D).

The diagonal coordinate only enlarges the squared norm used on the right. Bounded rates give nonexplosion and the comparison construction. This proves (A).

Every common visible-path functional F in [0,1] consequently satisfies |E_P F-E_Phat F| <= the right side of (A). This concerns the whole path, including jump times. It is not a uniform statement over untested controllers.

If the predictor uses a different initial visible law muhat, add delta_init=TV(mu_actual,muhat). This is directly estimable from the reset's initial visible labels; it is not a hidden-state coverage assumption. With simultaneous per-label empirical errors <=theta, a valid upper bound is half the empirical l1 discrepancy plus k theta/2. Initial visible-law estimation must be charged unless the preparation fixes that label exactly.

## 3. The acquisition identity for an arbitrary frozen predictor

Normalize generators, hazards and time by R for the remainder of the acquisition proof. Every microscopic exit rate and predicted exit rate is then at most one. Write tau=RT for the normalized deployment horizon. Restore physical D by multiplying normalized D by R^2.

For each action j and each visible target a use actual nonnegative probe gains g_ju, u=0,...,p-1, with baseline gain one, and actual product settings whose off-diagonal rates are

    (K_(j,u odot v))_il = q_il^j g_ju(i,l) g_jv(i,l).

A product setting is a simultaneous actuator composition. A temporal sequence of K_ju followed by K_jv does not supply this identity. Either all within-label gains equal one, with synthesis coefficients summing to zero, or an activity sensor measures all modeled microscopic jump events. The rate bound must include product settings.

Use omega_j in place of the source's normalized preparation. This merely weights every raw mean by the observed action tag 1{J_U=j}. Conditional rejection sampling and rare-action division are unnecessary.

Define the directed flux measure nu_j(i,l)=omega_j(i)q_il^j. The observable H_j,b_ja,c_ja and their positive synthesis error are

    H_(j,uv) = sum nu_j g_ju g_jv,
    b_(j,a,u) = sum nu_j g_ju (e_a(l)-e_a(i))/2,
    c_(j,a) = sum nu_j [(e_a(l)-e_a(i))/2]^2,
    E_(j,a)(w) = w^T H_j w - 2 b_ja^T w + c_ja.

In selective mode the sums for H are cross-label only; unobserved internal terms vanish because sum(w)=0. In activity-complete mode H includes all microscopic edges. Product-setting initial activity measures H. Ordinary label changes measure b and c. Expanding the square proves exactly

    E_(j,a)(w) = sum nu_j [w dot g_j - (e_a(l)-e_a(i))/2]^2 >= 0.

Choose w_ja with l1 norm at most W and put W_ja=sum_u w_ja,u K_ju. For the signed mathematical V_ja defined in Section 1,

    | omega_j (W_ja-V_ja) Q^j e_b |
       <= 2 sqrt(m_j E_(j,a)).                              (3.1)

Indeed, the expression is a flux-weighted inner product of the gain error with Q^je_b(l)-Q^je_b(i). The latter has magnitude at most two and the flux mass is at most m_j. This proves (3.1) by Cauchy-Schwarz.

The measured time jets are

    C2_(j,aa) = omega_j D_a (Q^j)^2 e_a,
    T_(j,aa) = omega_j Q^j D_a Q^j e_a,
    Z_(j,u,a) = omega_j K_ju Q^j e_a.

T is obtained from the mixed derivative of E[1{J_U=j} e_a(Y_(U+s))e_a(Y_(U+s+t))] under Q^j. Z uses K_ju first and Q^j second. The initial action tag is held fixed during the probes; the controller is suspended during the probe. These sequential pulses acquire mixed derivatives and are distinct from product settings.

Rearranging 2V_ja Q^je_a gives, with no stationarity assumption,

    G = sum_(j,a) omega_j (Q^je_a)^2
      = sum_(j,a) [T_(j,aa)-C2_(j,aa)-2omega_j V_ja Q^je_a].

The synthesized Gtilde substitutes sum_u w_ja,u Z_(j,u,a) for omega_j V_ja Q^je_a. Therefore

    |Gtilde-G| <= 4 sum_(j,a) sqrt(m_j E_(j,a))
                <= 4 sqrt(k sum_(j,a) E_(j,a)),             (3.2)

because sum_j m_j=1. This is a scalar trace bound, avoiding the source's stronger full-matrix acquisition when only a path certificate is wanted.

Now record vhat(U,H_U) at the stop and hold that vector fixed while probing. Under target Q^(J_U), the single first derivative

    Bpred = d/dh E[ vhat_(Y_(U+h))(U,H_U) ] at h=0
          = E sum_b vhat_b(U,H_U) Q^(J_U)e_b(X_U)

is observable. The raw statistic has magnitude at most one. The zero-order mean

    Cpred = E ||vhat(U,H_U)||_2^2

has magnitude at most two. Thus

    D = G - 2Bpred + Cpred.                                (3.3)

There is no density ratio, hidden-state reconstruction, normalization by label/action masses, or enumeration of possible histories in (3.3). The predictor must be frozen during each short probe: rerunning it on the post-probe history would differentiate a different object.

## 4. A certificate valid for coefficients fitted from the same observations

Suppose every acquired moment entry has absolute error at most theta, simultaneously. For each action set

    Hplus_j = sym(Hhat_j) + p theta I.

Then Hplus_j-H_j is PSD. For every feasible coefficient vector of l1 norm <=W,

    E_(j,a)(w) <= U_(j,a)(w)
       := w^T Hplus_j w - 2 bhat_ja^T w + chat_ja + 2theta W + theta.

This holds uniformly for fitted coefficients. The noisy quadratic upper problem is convex on the confidence event; an implementation which finds Hplus non-PSD returns inconclusive. A feasible vector and its evaluated upper certificate suffice for validity; optimizer accuracy only affects success. The source's comparison estimate reconstructs directly:

    U_(j,a)-E_(j,a) <= [(p+1)W^2+4W+2] theta.               (4.1)

Let Utotal=sum_(j,a) max(0,U_(j,a)) and define Dhat by (3.3), using Gtilde and measured Bpred,Cpred. A valid scalar upper bound is

    Dcert = max{0, Dhat + 4sqrt(k Utotal)
                        + [2sk(1+W)+3]theta}.              (4.2)

The last bracket accounts respectively for T,C2,Z and for -2Bpred+Cpred. Uniform l1 bounds make it valid after fitting the w's. An implementation must also add its numerical optimizer/evaluation error. The returned path certificate is

    epsilon_cert = min{1, delta_init + tau sqrt((k-1)Dcert)}. (4.3)

If Utotal is too large or the propagated error is unhelpful, the result is inconclusive. A numerical zero never establishes exact closure.

For a useful success guarantee, let xi be a desired additive precision for D. Put Cw=(p+1)W^2+4W+2 and K=2sk(1+W)+3. It suffices that true feasible syntheses have total error <=xi^2/(512k), and that

    theta <= min{xi^2/(512 s k^2 Cw), xi/(4K)}.

Then Utotal<=xi^2/(256k), synthesis and statistical contributions are each <=xi/4, and Dcert<=D+xi, up to charged optimization errors. No conditioning assumption on H or small-mass division is needed.

## 5. Second changed attack: acquire time jets with spectral interpolation

The original N718 finite-difference construction is valid as a conservative interface, but its common short time h proportional to the squared desired operator accuracy gives roughly accuracy^-12 samples. That cost is not intrinsic to a bounded generator. I changed the acquisition attack to fixed-interval analytic interpolation.

This is established spectral differentiation used in a new measurement interface, not a claimed invention in numerical analysis. A self-contained bound follows.

For a scalar endpoint statistic f(t)=eta exp(tK)g with total variation norm of eta <=1, ||g||_infinity<=1 and ||K||_infinity<=2, truncate its Taylor series at degree n. On [0,1] the remainder obeys

    ||r_n||_infinity <= exp(2) 2^(n+1)/(n+1)!.

Use the shifted Chebyshev-Lobatto nodes t_j=(1-cos(j pi/n))/2, j=0,...,n. The discrete cosine representation of the interpolating polynomial has coefficients bounded in magnitude by twice the maximum nodal datum. Since

    |d/dt T_m(2t-1)|_(t=0) = 2m^2,
    |d^2/dt^2 T_m(2t-1)|_(t=0) = (4/3)m^2(m^2-1),

the l1 norms of the endpoint derivative weights obey the sharper identities

    ||w_first||_1 = 2n^2,
    ||w_second||_1 = (4/3)n^2(n^2-1).

Here is an elementary sign proof, avoiding a hidden condition-number assertion. If ell_j is the Lagrange cardinal polynomial at node t_j, then ell_j'(0) has sign (-1)^(j+1), including j=0. For j>=1, ell_j''(0) = -2ell_j'(0) sum_(l!=0,j) 1/t_l, and ell_0''(0)>0; thus second derivative signs are (-1)^j for n>=2. The nodal values of T_n(1-2t) are (-1)^j. Applying either endpoint derivative functional to this polynomial therefore sums the absolute weights and gives the displayed identities. In particular the tensor mixed-derivative weight l1 norm is exactly 4n^4.

The Taylor remainder has zero first and second derivative at zero when n>=2. Therefore derivative bias is bounded by those weight norms times the remainder. For mixed jets F(s,t)=eta exp(sK)D exp(tQ)g, rectangular Taylor truncation has remainder at most

    2 exp(4) 2^(n+1)/(n+1)!

on [0,1]^2, and its mixed derivative at (0,0) is zero. A safe common bias envelope for the first, second and mixed jets is

    B_n = 8 exp(4) n^4 2^(n+1)/(n+1)!.

Choose n>=2 with B_n<=theta/2, and acquire every raw nodal mean to

    beta <= theta/(8n^4).

Then each required derivative has error <=theta. Such n is O(log(e/theta)); the factorial bound is stronger than needed. Each probe duration is at most 1/R, or two such pulses. The shortest positive node is of order 1/(R n^2), rather than a power of the target accuracy. Endpoint activity bits have the same analyticity property: their no-jump probability is a mixture of exp(-r_i t), r_i<=1.

One conservative number of scalar moment families, with p probes per action, is

    M = s [p(p+1)/2 + 2pk + 3k] + k + 2.

The terms account for H, b/Z, c/C2/T, initial visible masses and Bpred/Cpred. Initial labels can be recorded during the same reset/replay trials. The number of raw nodal means is at most L=M(n+1)^2, overcounting one-dimensional and zero-order families. With the exponential-clock implementation below every raw statistic has magnitude at most four. For each nodal mean it therefore suffices to use

    N_node = ceil[32 beta^-2 log(2L/zeta)]

independent preparations, by Hoeffding. The total bound is L*N_node, or

    O(M (n+1)^2 beta^-2 log(M(n+1)^2/zeta))

independently prepared observations. More explicitly the logarithmic degree factor here is O(n^10), because beta^-2=64n^8 theta^-2. Fixed predictor evaluations add their actual computational cost. The previous theta choice gives xi^-4 times polynomial factors and logarithms for unknown-gain completion, and xi^-2 if the V syntheses are known exact and no fitted norm acquisition is required. For a path tolerance epsilon, xi of order epsilon^2/tau^2 gives conservative epsilon^-8 tau^8 and epsilon^-4 tau^4 dependence, respectively. These are sufficient bounds, not minimax claims or modest numerical budgets.

Rational approximations to the Chebyshev times and weights have charged bit cost. During the probes, bounded generator norms make raw means Lipschitz in each pulse length with a universal constant. Node errors O(beta/R) and appropriately bounded switching/model errors fit the raw-mean budget. Weight evaluation at polynomial precision must be included; the displayed l1 bounds prevent an exponentially ill-conditioned differentiation oracle from being hidden here.

## 6. Preparing random occupation times is an actual interface

Restarting every trial and rerunning the controller to the stop costs at most T per accepted preparation, plus the original preparation cost and the probe time. Prefix sampling is not free. An initial preparation bias alpha causes a raw-mean bias of at most a constant times alpha, independent of hidden count; to claim the concentration guarantee it must fit the beta budget.

A finite digital grid of stopping times does not approximate arbitrary feedback policies automatically. A controller can switch on a set that a grid misses. One may supply a justified timing regularity bound, or realize continuous stopping with an independent calibrated exponential clock of rate 1/T. Condition its ring time S on S<=T and weight every tagged raw statistic by

    w_time(S) = (1-exp(-1)) exp(S/T),

which lies between 1-exp(-1) and e-1. The conditional density times this weight is exactly 1/T on [0,T]. The positive flux form and all moment identities therefore recover uniform occupation. Rejection of S>T costs only the constant factor 1/(1-exp(-1)). The clock must be independent of hidden dynamics and controller randomness, and its calibration and readout accuracy are charged. Approximate weights and clock-density errors add bounded raw bias. The controller's actual action tag is recorded at the ring; it is not guessed from a rounded time.

This is a physical randomized-stop interface, not a claim that a finite-bit distribution is literally uniform in total variation against an atomless law. Existing continuous-time observation idealizations alone do not validate a particular clock or a nonperturbing pause/probe switch.

Likewise, observed label changes do not provide an all-microscopic-event counter. Selective neutrality or actual all-event access and the microscopic product law remain independent acquisition gates. Product flux errors xi_prod add xi_prod ||w||_1^2 to squared synthesis certificates, as in the reconstructed source. Unobserved internal actuation must be bounded or measured. The method does not infer these structural exclusions from its own visible endpoint data.

## 7. A matched passive obstruction and active consequence

This example demonstrates a possible capability separation under the explicit probe interface; it is not a claim that exponential active/passive separations are new. N709 already proposes a different stationary Walsh-ladder separation. The following lower-bound mechanism is the classical birthday obstruction in uniformity testing, embedded in a four-label continuous-time process. It needs no N709 theorem.

For integer m>=1 let N=2^m. An unknown distribution P on m-bit strings is implemented by a hidden prefix tree. At depth l<m the total exit rate is one and the next-bit transition probabilities are P(B_(l+1)=b | prefix). Zero-probability prefixes can be assigned arbitrary outgoing probabilities. The visible label is (depth parity,last bit), requiring four labels; the root has a fixed visible label. Parity changes at every jump, so every modeled tree jump is visible. After m bits, attach a four-state tail which flips parity at rate one and chooses a fresh fair bit. Its law is independent of P. The initial root is exactly restartable; stationarity and irreducibility are not assumed. The hidden dimension is O(2^m), and this is disclosed rather than claimed polynomial in m.

The candidate four-state predictor chooses the next bit fairly at total exit rate one. For P uniform on all strings the full visible path equals the candidate. For P uniform on any subset S of size N/2, their path TV on horizon T=4m is at least

    Pr(Poisson(4m)>=m)/2 >= [1-exp((log 4-3)m)]/2 > 0.4.

The distinguishing event is: at least m jumps occurred and the first m bits belong to S. The Poisson clock has the same law under both models and is independent of the bits. The last inequality uses exp(log 4-3)<0.2.

A full passive trial, even with exact jump times and unlimited processing, is a stochastic function of one P-distributed m-bit string and independent clocks/tail randomness. Consider a uniformly random half-size subset S. Conditional on r sampled strings all being distinct, the mixture alternative and the uniform null both give the uniform law on ordered distinct tuples. Collision probabilities are at most r(r-1)/N under the alternative and r(r-1)/(2N) under the null. Thus the TV distance between their r-trial experiments is at most

    3r(r-1)/(2N).

For bounded testing error, some half-support alternative therefore requires r=Omega(sqrt N)=Omega(2^(m/2)) independent passive restarts. This is the standard uniformity-testing/birthday lower bound, here proved in the needed scope.

The active occupation certificate is polynomial in m at constant confidence and accuracy. Supply the known geometric probes

    q_il^(a,+) = q_il 2^(e_a(l)-e_a(i)),
    q_il^(a,-) = q_il 2^(-e_a(l)+e_a(i)).

Their difference divided by three is exactly V_a, because Delta e_a is -1,0 or 1. Primitive gains are at most two, product gains at most four and their within-label gains are one. There are only finitely many probes per visible label; the common exit bound is R=4. This is a specified kinetic access law, not something passive data can guarantee.

The fair null has D=0 on its occupation law. Every half-support alternative has D bounded below by a constant times T^-2, by Theorem A and the >0.4 path discrepancy. Acquiring D to a sufficiently small constant multiple of T^-2 therefore accepts the null and cannot accept any alternative with a small path certificate. With the known exact geometric syntheses, the spectral acquisition bound uses polynomially many trials and polynomial total physical duration in m. Even unknown compatible gains retain a polynomial statement when the fixed finite completion budget succeeds. No microscopic tree reconstruction is performed.

This is a promise certificate/test with perfect-model completeness. It is not tolerant testing of all hidden realizations whose observed laws happen to equal the candidate: those can have D>0. Direct empirical estimation of a single chosen reward is also much cheaper than a universal path-law certificate. The claimed advantage concerns simultaneous control of all bounded path events in this specified hard family.

## 8. Limits, criticism and next decisive gate

The new conceptual step is occupation-conditioned validation, including a frozen history-dependent predictor. The coupling inequality, response algebra, product Gram construction, spectral differentiation and birthday lower bound each have established antecedents. The exact combination and its historical priority have not been searched exhaustively. It is a credible mathematical capability candidate, not an established fundamental discovery.

The construction is on-policy. It certifies no new start distribution, action library, controller, horizon beyond T or counterfactual policy for free. Optimizing policies over an untested class can still require exponential exploration. A finite tested policy library costs its actual validation budget and a union bound. If policy selection uses validation data, independent final validation or a justified simultaneous finite-library procedure is necessary.

There is no nonzero-residual infinite-horizon guarantee. Because the bound includes tau and active experiments must rerun the actual policy, very long-horizon certification can remain expensive. Unknown-gain moment cancellation also requires more statistical precision than direct reward estimation. The source's physical composition, activity access, rate calibration and resetting gates survive intact.

The candidate is conservative: D decomposes into the squared error of the true visible conditional hazard and a nonnegative conditional variance of the hidden instantaneous rates given history. A perfect observed predictor can therefore fail the certificate. Removing that variance without state access or paired conditional preparations is a separate unresolved question; nothing here establishes it can be done.

A concrete exact fixture makes this limitation visible. On four hidden states with uniform preparation and labels (0,0,1,1), let J be uniform averaging, h=(1,-1,0,0)^T, f=(1,1,-1,-1)^T and Q=J-I+h f^T/16. All off-diagonal rates are positive and the uniform law is stationary. The transpose Q^T is strongly lumpable with the symmetric two-label rate 1/2, so the entire stationary observed law is exactly that Markov law. Nevertheless the squared hidden-rate error of this perfect predictor is D=1/64. The exact verifier checks both assertions' algebraic premises. This excludes a silently stronger claim of complete certification of every good observed predictor.

The nearest decisive next gate is an independently implemented random-stop assay on an unknown hidden simulator, using only the allowed labels/probes, empirical nodal means and the noisy positive certificate. It should include the three-state coverage failure and the prefix-tree testing family, source-clock false probes, deliberately broken product composition, finite readout/timing errors and a correct observed predictor with positive hidden-rate variance. The present verifier checks exact algebra and marked numerical interpolation diagnostics; it is not that complete noisy experimental assay.

## 9. Primary-source comparison and source receipts

The Astra sources are pinned original research capital, with their unresolved statuses preserved. N718's full original argument was used for the product-flux norm, signed response operator and nonstationary identity; the occupation/history-dependent validation and spectral acquisition argument were reconstructed here. N713's original controlled path proof supplies a comparator for the coupling architecture. N709 was inspected only to avoid falsely claiming a new active/passive separation phenomenon; its theorem is not a premise.

External primary comparisons consulted on 2026-10-12:

- Hilder and Sharma, [Quantitative coarse-graining of Markov chains](https://arxiv.org/abs/2201.10256), published in SIAM J. Math. Anal. 56 (2024), 913–954, [DOI](https://doi.org/10.1137/22M1473996). The abstract verifies that quantitative effective-dynamics bounds without explicit scale separation are prior work. This note does not claim that subject is new and does not import their quantitative theorem without reading its full proof.
- Xie, Wang and Zhao, [On Exponential Convergence of Gegenbauer Interpolation and Spectral Differentiation](https://arxiv.org/abs/1109.5509). Exponential spectral differentiation for analytic functions is established. Section 5 supplies its own deliberately loose elementary bound for the exact endpoint/mixed jets needed here.
- Paninski, [A Coincidence-Based Test for Uniformity Given Very Sparsely Sampled Discrete Data](https://www.columbia.edu/cu/neurotheory/pdfs/Paninski_2008.pdf), IEEE Trans. Inf. Theory 54 (2008), 4750–4755. The square-root support-size uniformity-testing barrier is prior work; Section 7 gives the particular random-half-support proof used in the embedding.

The related nonequilibrium response and uncertain-lumpability sources listed in the original N718 note have not all been reopened in full. No first-ever, optimality, empirical or physical readiness claim is made.
