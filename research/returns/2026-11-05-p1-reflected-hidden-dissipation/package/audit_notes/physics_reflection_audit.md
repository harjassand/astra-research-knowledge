# Adversarial physics audit: reflection certificates and one-record inference

Internal audit for the selected research result, 2026-11-05. No separate research endpoint is proposed here.

## Verdict

The population linear and nonlinear bounds, the four-state construction, the equilibrium moment-generating-function bound, and the proposed no-mixing quantitative confidence inversion all check out under the stated assumptions. The strongest restrictions are stationary initialization, ordinary reversal of even microscopic states, deterministic instantaneous observation, and a prespecified witness and record length.

The organizing idea of detecting dissipation through negative reflected past–future covariance is already present in a public October 2026 unrefereed manuscript. The increment that survives this source check is the direct linear-in-violation Q-versus-Q* bound for arbitrary bounded half-record tests, the explicit three-snapshot construction whose entire visible path law is reversible and whose every two-time law is an equilibrium telegraph law, and the proved finite-record operation with no hidden mixing assumption. Priority is not established by this bounded search.

## 1. Population bound audit

Let Q be a finite irreducible CTMC generator in row convention, with stationary distribution pi. All microscopic states are even under physical time reversal. Put Q*=D_pi^{-1}Q^T D_pi. Let Y=h(X) for a deterministic finite-alphabet observation map.

For a fixed half-window length t, let g be a real measurable functional of a half-record, with range length R, and let 0<=w(Y_0)<=1. Apply the same g to the future [0,t] and to the reflected past [0,-t]. Define

    C = E[w(Y_0) g(reflected past) g(future)].

Conditioned on X_0=i, the reflected past and future are independent and distributed as Q* and Q respectively. If u_i and v_i are their conditional g means, then

    C = sum_i pi_i w_i u_i v_i
      >= -(1/4) sum_i pi_i w_i (u_i-v_i)^2.

For the two conditional half-path laws P_i and P_i*,

    |u_i-v_i| <= R TV(P_i,P_i*)
               <= R sqrt(D(P_i||P_i*)/2).

Since w_i<=1 and sum_i pi_i D(P_i||P_i*)=t sigma(Q),

    sigma(Q) >= 8[-C]_+/(R^2 t).

The KL identity is exact: stationarity makes Q and Q* have equal exit rates at each state, so the holding-time terms cancel; averaging the jump log-likelihood over pi gives the stationary entropy production. Missing reverse transitions may make sigma infinite, in which case the lower bound remains valid but uninformative.

### Nonlinear improvement

Let p=Ew>0 and eta=4[-C]_+/(pR^2). Set d_i=|u_i-v_i|/R. The symmetric-divergence bound

    D(P_i||P_i*)+D(P_i*||P_i) >= 4 d_i atanh(d_i)

follows from the sharp total-variation/symmetric-KL inequality and d_i<=TV. Both averaged one-sided KLs equal t sigma. The function F(z)=sqrt(z) atanh(sqrt(z)) is increasing and convex on [0,1), as follows directly from its positive power series. Hence

    2t sigma >= 4 sum_i pi_i w_i F(d_i^2)
             >= 4p F(sum_i pi_i w_i d_i^2/p)
             >= 4p F(eta),

or

    sigma(Q) >= (2p/t) sqrt(eta) atanh(sqrt(eta)).

Its small-violation leading term is exactly the linear bound. It is not a sharp characterization of the least possible entropy production for all data. Eta=1 forces infinite cost or a failure of the finite-cost premises; eta>1 is incompatible with the bounded-score population assumptions.

## 2. Four-state construction audit

Take f=(1,1,-1,-1)^T, h=(1,-1,1,-1)^T, k=f*h=(1,-1,-1,1)^T and

    Q = -a(I-J/4) + (epsilon/4)(h f^T + f k^T),
    0 < epsilon < a/2,

where J is the all-ones matrix. Row and column sums vanish and all off-diagonal rates are positive. In particular, the perturbation matrix before its factor epsilon/4 is

    [[ 2, 0,-2, 0],
     [ 0,-2, 0, 2],
     [ 0, 2, 0,-2],
     [-2, 0, 2, 0]].

The uniform law is stationary. On the orthogonal Hadamard basis, Q sends k to -ak+epsilon f, f to -af+epsilon h, and h to -ah. Thus

    e^{tQ} f = e^{-at}(f+epsilon t h),
    e^{tQ^T} f = e^{-at}(f+epsilon t k).

Since f is orthogonal to h and k, the observed binary process Y=f(X) has correlation e^{-at}. Every stationary two-time joint law is therefore exactly that of the equilibrium symmetric telegraph process with flip rate a/2. This is a statement about two-time laws, not about equality of full visible process laws.

Let R be the permutation swapping hidden states 3 and 4. It fixes f, swaps h and k, and satisfies RQR=Q^T. Consequently the entire stationary observed process Y is time-reversal invariant. Every visible-path forward/reverse KL statistic is zero, regardless of record order or temporal resolution.

Condition on Y_0=-1. Then k=-h, and h is conditionally equally likely to have either sign. Therefore

    Cov(Y_{-t},Y_t | Y_0=-1) = -epsilon^2 t^2 e^{-2at}.

With g(y)=y+e^{-at} and w(y)=1{y=-1}, the unconditional reflected score is

    C = -(1/2) epsilon^2 t^2 e^{-2at}.

Here R_range=2, yielding sigma>=epsilon^2 t e^{-2at}. Directly summing the five asymmetric edge-pair contributions gives

    sigma(Q) = (epsilon/2) log[(a+2epsilon)/(a-2epsilon)].

### Important strongest-method comparison

The family is not invisible to methods with continuous dwell-time access. A symbolic calculation gives mean dwell 2/a in each observed label and

    CV_A^2 = (2a^2+epsilon^2)/(2a^2-epsilon^2) > 1,
    CV_B^2 = (2a^2-epsilon^2)/(2a^2+epsilon^2) < 1.

Thus the established Skinner–Dunkel waiting-time criterion detects the family. The earned access distinction is that only three discrete state snapshots per score are needed here; no uninterrupted visit must be reconstructed. Do not claim superiority over estimators given richer waiting-time data.

The score g uses a. In an actual unknown-system experiment, a must be independently calibrated, or a prespecified set of offsets must be tested with the corresponding selection correction. Choosing a score after examining the same record invalidates the fixed-witness confidence argument unless a separate proof controls that choice. More generally, replacing e^{-at} by a fixed c0 changes C to

    C = (1/2)[(c0-e^{-at})^2-epsilon^2 t^2 e^{-2at}],

which quantifies the calibration tolerance needed to retain negativity.

## 3. One stationary record: equilibrium MGF without mixing

This section proves a new operational addition within the selected endpoint. It does not assume the successive triples are independent.

Fix n, t, a bounded endpoint score g, and a central weight w in [0,1] before observing the record. Put G=||g||_infinity, B=G^2, T=2t. The record contains 2n+1 snapshots at times 0,t,...,2nt. Set

    Z_r = w(Y_{(2r-1)t}) g(Y_{(2r-2)t}) g(Y_{2rt}),
    r=1,...,n.

Adjacent blocks share one boundary snapshot. They may be strongly dependent.

Under any finite hidden stationary reversible CTMC, lift g and w to microscopic states and write P=e^{tQ}. Work in L^2(pi), so P is a self-adjoint Markov contraction. For theta>=0 define the tilted block kernel

    K_theta(i,k) = sum_j P(i,j) P(j,k)
                  exp[-theta w_j g_i g_k].

Its exact series is

    K_theta = sum_{m>=0} (-theta)^m A_m/m!,
    A_m = M_{g^m} P M_{w^m} P M_{g^m}.

Each A_m is positive semidefinite:

    A_m = (M_{w^{m/2}} P M_{g^m})^*
          (M_{w^{m/2}} P M_{g^m}).

Also ||A_m||<=G^{2m}=B^m, while A_0=P^2<=I. Absolute convergence follows from bounded g,w. Dropping the negative odd terms in the Loewner order gives

    K_theta <= sum_{m even} theta^m A_m/m!
             <= cosh(theta B) I.

The kernel K_theta is entrywise nonnegative and self-adjoint. In finite dimension, Perron–Frobenius therefore makes its spectral radius equal to its largest eigenvalue; every eigenvalue has absolute value no larger than that eigenvalue. Thus

    ||K_theta|| <= cosh(theta B).

The Markov property, retaining every shared boundary, gives the exact moment-generating function

    E_eq exp[-theta sum_{r=1}^n Z_r]
      = <1,K_theta^n 1>_pi
      <= cosh(theta B)^n.

No hidden state count, spectral gap, mixing time, or independent-triples approximation enters. Stationarity is still necessary for this formulation.

### Exact Chernoff tail

Let Gamma=-(1/n)sum_r Z_r. For 0<=gamma<=B define

    I(x) = kl((1+x)/2 || 1/2)
         = [(1+x)log(1+x)+(1-x)log(1-x)]/2,

with the continuous endpoint convention. Optimizing theta gives

    P_eq(Gamma>=gamma) <= q_gamma
                       := exp[-n I(gamma/B)]
                       <= exp[-n gamma^2/(2B^2)].

At gamma=B the optimized bound is 2^{-n}. This is a uniform equilibrium-rejection guarantee for a fixed witness and fixed n. It is not itself an e-process or an optional-stopping guarantee.

### Extension to general bounded half-record tests

For a half-record functional g with |g|<=G, define the signed transfer operator

    T_m(i,j)=E_i[g(half-record)^m 1{X_t=j}].

By conditional Cauchy–Schwarz and stationarity, ||T_m||<=G^m. Reversal of the left half under equilibrium turns its transfer into T_m^*, so the expansion has A_m=T_m^* M_{w^m}T_m. The same PSD and norm argument applies. The left-half test must be the temporal reflection of the same functional used on the right, and boundedness is essential to the displayed exponential bound.

## 4. No-mixing quantitative entropy-rate confidence bound

The proposed confidence inversion is valid. It is conservative and has a different limiting scale from the strong population bound.

For an arbitrary stationary Q with finite sigma, define its additive reversibilization

    S=(Q+Q*)/2.

It has the same stationary law and the same escape rate at each microscopic state. For a pair of stationary fluxes x=pi_i q_ij, y=pi_j q_ji, the corresponding Q-versus-S relative-entropy-rate contribution is

    x log[2x/(x+y)] + y log[2y/(x+y)].

It is at most one quarter of the entropy-production edge cost:

    x log[2x/(x+y)] + y log[2y/(x+y)]
      <= (1/4)(x-y)log(x/y).

To check the constant, put z=(x-y)/(x+y). After cancelling positive factors, the inequality is

    (1+z)log(1+z)+(1-z)log(1-z) <= z atanh(z).

Both sides are even. For z>=0, the derivative of RHS-LHS is z/(1-z^2)-atanh(z)>=0, and the difference vanishes at zero.

Consequently, for the full stationary path on [0,nT],

    D(P_Q || P_S) <= nT sigma(Q)/4.

The same inequality holds for the observed snapshot record by data processing. No estimate of S is needed; it is a comparison model in the proof.

Fix a desired error probability delta in (0,1). For 0<gamma<=B define

    L_delta(gamma) = 4 kl(delta||q_gamma)/(nT), if q_gamma<delta;
                     0, otherwise.

Set L_delta(gamma)=0 for gamma<=0. Then

    P_Q{ L_delta(Gamma) > sigma(Q) } <= delta.

### Fixed-threshold proof

For A_gamma={Gamma>=gamma}, write p=P_Q(A_gamma) and q_actual=P_S(A_gamma). The null MGF gives q_actual<=q_gamma. Binary data processing gives

    kl(p||q_actual) <= nT sigma/4.

If p>delta and q_actual<=q_gamma<delta, monotonicity of binary KL yields

    kl(p||q_actual) >= kl(p||q_gamma) > kl(delta||q_gamma).

Therefore sigma<L_delta(gamma) implies p<=delta.

### Why plugging in the observed Gamma is legitimate

For q_gamma<delta, L_delta is continuous and increasing in gamma. If sigma>=L_delta(B), overcoverage is impossible. Otherwise choose the limiting critical threshold gamma_* with L_delta(gamma_*)=sigma; for sigma=0 use the boundary q_gamma*=delta. The overcoverage event is {Gamma>gamma_*}. Its S-probability is at most q_gamma*. If its Q-probability were greater than delta, the preceding binary-KL argument would contradict the full-record KL upper bound. This proves the confidence statement, including discrete score distributions, with the strict overcoverage event displayed above.

This threshold inversion controls one prespecified statistic. It does not authorize arbitrary witness selection, varying n after seeing the data, or multiple uncorrected tests.

### Strength and limitation

For a fixed positive gamma and n tending to infinity,

    L_delta(gamma) -> 4 delta I(gamma/B)/T.

Indeed kl(delta||e^{-nI})=delta nI-H(delta)+o(1). Thus the no-mixing interval does not consistently recover the stronger linear population certificate from one arbitrary slowly mixing record. That is a substantive limitation, not a missing algebraic factor. Reliable estimation of the stationary mean C with vanishing error still requires paid independent preparation, a justified mixing/concentration condition, or another access mechanism.

The physical recording interval is nT=2nt and the endpoint implementation uses 2n+1 state snapshots. Stationary preparation is an explicit premise. If it is not already supplied, a preparation/mixing bill must be included before claiming a complete experimental cost.

## 5. Checks executed during this audit

1. Symbolic Hadamard-basis action verified the two-time law, the reflected covariance, the full generator, and the two dwell-time CV formulas.
2. For 135 random reversible generators of dimensions 2 through 10, with random positive stationary distributions, symmetric conductances, nonnegative weights and bounded scores, the exact tilted kernel was checked at theta=0.02,0.3,1.1. The largest L^2(pi) symmetry error was 6.67e-16. The maximum tested excess of its largest eigenvalue over cosh(theta B) was -4.93447e-5.
3. Exact finite-matrix MGF values for n=1,2,5,10 obeyed the claimed upper bound in every checked case; the maximum log-MGF excess was -4.93554e-5.

These are numerical implementation checks, not substitutes for the operator proof. No claim of external experimental validation or formal proof-assistant verification follows.

## 6. Physical and statistical caveats that must remain visible

* **Parity is essential.** The permutation R swapping states 3 and 4 makes RQR=Q^T. If R were the physical time-reversal involution, the same four-state model would obey generalized detailed balance and could have zero physical entropy production. The positive result is therefore about models whose microscopic variables are declared even, not all possible hidden physical mechanisms.
* **Physical interpretation needs local detailed balance.** Mathematically sigma is ordinary stationary path irreversibility. Interpreting it as thermodynamic dissipation requires the usual stochastic-thermodynamic identification; heat in watts additionally requires temperature and units, and multiple reservoirs require the proper entropy accounting.
* **Observation is instantaneous and noninvasive.** A sensor with its own memory, unknown delays, state-dependent dead time, or measurement back-action changes the model. Such sensor states may need to be included in the microscopic description with their reversal parity and dynamics.
* **Stationarity is not certified by the formulas.** Visible stationarity alone cannot guarantee a hidden stationary preparation. Arbitrarily slow hidden modes remain possible.
* **Prespecification matters.** g,w,t,n must be fixed before the tested record. An independently trained witness or a corrected finite prespecified family can be used, but no unrestricted data-adaptive validity has been proved here.
* **Three snapshots describes each score, not the total sample bill.** In the four-state family the negative mean is O(epsilon^2/a^2) at t=O(1/a), so the displayed bounded-score rejection budget scales at least as the sufficient O(a^4/epsilon^4) signal-to-noise expression, up to constants and log confidence factors. A complete power guarantee under the alternative still needs a proved dependence bound for that family. The null MGF alone controls false positives, not power.
* **No universal optimality claim.** The certificate is not proved to equal the least dissipation compatible with all observed statistics, or to dominate methods with richer observations.

## 7. Strongest relevant primary prior art inspected

### Skinner and Dunkel, PNAS 2021

*Improved bounds on entropy production in living systems*, PNAS 118(18), e2024300118, DOI 10.1073/pnas.2024300118.

Primary full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC8106300/

This explicitly detects positive entropy production even when observed trajectories are time symmetric, by minimizing dissipation over hidden Markov mechanisms consistent with measured transition statistics. It prevents any claim that the present work first infers dissipation from time-symmetric observations. Its concrete optimization uses successive coarse transitions, not the general bounded reflection-score formula proved here.

### Skinner and Dunkel, PRL 2021

*Estimating entropy production from waiting time distributions*, PRL 127, 198101, DOI 10.1103/PhysRevLett.127.198101.

Primary full text and supplement: https://arxiv.org/html/2105.08681v2

This derives the equilibrium exponential-mixture dwell restriction and constructs a universal waiting-variance/entropy curve through hidden-model optimization. The four-state example above has CV_B^2<1 and is therefore visible to this method with continuous waiting-time access. Its observation requirements differ from the present three-snapshot operation.

### Public October 2026 reflection-certificate candidate

Anonymous, *An architecture-independent dissipation floor for alternating-renewal observations*, version 1.1, 3 October 2026. Self-labeled unrefereed mathematical candidate; DOI 10.5281/zenodo.23118474.

Primary manuscript: https://github.com/ipitchford/hidden-dissipation-floor/blob/main/PAPER.tex

It already proves nonnegative equilibrium past–future covariance using conditional independence and identical reversed conditional laws. It converts negative persistence covariance into a dimension-independent entropy-production floor through additive reversibilization and a KL projection. Its fixed-window bound is sigma >= (2p/t) I(a_t,b_t), with I scaling quadratically in the covariance defect near zero, and it supplies a deterministic uncertainty-box extension. The root's direct Q-versus-Q* argument instead gives a linear-in-defect bound for general bounded half-record tests and the finite-snapshot implementation. The manuscript expressly does not construct a statistical confidence procedure. Its public status makes it relevant priority evidence even though peer review is not established.

### Aznagulov, spectral finite-resolution preprint, September 2026

*The Spectral Cost of Detecting Nonequilibrium at Finite Temporal Resolution*, arXiv:2609.37205v1.

Primary full text: https://arxiv.org/html/2609.37205v1

This gives a mixing-independent hidden-equilibrium MGF bound for antisymmetric current scores using tilted operators and Poissonized record length. It is close methodological prior art for a one-record uniform equilibrium test. The selected reflection score is time symmetric and may detect a visible process with no time-arrow information; its proof uses alternating PSD terms at fixed block count, rather than the prior's antisymmetric tilted-kernel relation and Poissonization. Do not present tilted-operator concentration or the general idea of uniform hidden-equilibrium testing as new.

### Aznagulov, thermodynamic realizability preprint, September 2026

*Thermodynamic Realizability of Hidden Markov Processes: Attainment, Observable Certificates, and the Price of Architecture*, arXiv:2609.14623v1.

Primary full text: https://arxiv.org/html/2609.14623v1

This considers exact hidden realization costs and dimension-priced globally calibrated finite-path certificates. Its general certificate representation is variational and does not by itself provide efficient calibration. No compactness claim from this source is needed as a premise for the present self-contained inequalities.

### Nitzan, Ghosal, and Bisker, 2023

*Universal bounds on entropy production inferred from observed statistics*, Phys. Rev. Research 5, 043251; preprint arXiv:2212.01783.

Primary record: https://arxiv.org/abs/2212.01783

This combines first- and second-order transition statistics and waiting-time moments in optimization-based bounds and explores simpler hidden topologies. It is relevant to the strongest applicable method comparison; a generic claim to outperform all hidden-model optimizations is not supported.

## Recommended defensible contribution statement

Under a stationary finite hidden CTMC model with ordinary even-variable reversal, a negative bounded reflected-record score yields an explicit entropy-production lower bound linear in its magnitude, independent of hidden dimension and topology. A four-state construction shows that three-time data can certify this obstruction when every two-time law is an equilibrium telegraph law and the entire visible path law is time symmetric. A fixed-score, fixed-budget tilted-operator argument provides a uniform one-record equilibrium test without a hidden mixing bound; additive reversibilization and binary-KL inversion give a conservative quantitative entropy-rate lower confidence bound under the same stationarity premise.

This is a mathematically substantive candidate result. It does not establish civilization-scale impact, worldwide priority, experimental applicability beyond its assumptions, or a complete solution to minimal thermodynamic realization.
