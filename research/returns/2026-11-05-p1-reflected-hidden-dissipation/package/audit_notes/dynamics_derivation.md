# Three-time reflection detects driving invisible to every two-time law

Research derivation by the dynamics branch, 5 November 2026. This is an internally derived mathematical candidate, not a priority or external verification claim.

## 1. Exact model, notation, and scope

Let X be a stationary, finite, irreducible continuous-time Markov chain (CTMC), in row-generator convention, with generator Q and strictly positive stationary probability row vector pi. Every microscopic variable is taken to be even under the **physical** time reversal. Its reverse generator is

    Q* = D_pi^{-1} Q^T D_pi.

Set Boltzmann's constant to one. The mathematical stationary path irreversibility rate is

    sigma = sum_{i<j} (pi_i Q_ij - pi_j Q_ji)
                         log[(pi_i Q_ij)/(pi_j Q_ji)].

Under the usual local-detailed-balance thermodynamic model this is the physical entropy-production rate. A unidirectional microscopic edge gives infinite sigma and the lower bounds below are then automatic. The proof concerns finite sigma; no bound on hidden state count, rates, topology, or relaxation time is used.

The observable is a deterministic finite-alphabet label Y_t = h(X_t). Observation does not intervene in the dynamics. Stationarity is an explicit premise, not inferred merely from a short observed record.

Fix a half-window length t > 0. A bounded function g may depend on the observed half-path (Y_s:0<=s<=t), or on any fixed finite set of snapshots in that half-window. Let R=osc(g)=sup(g)-inf(g)>0. Let w(Y_0) be any specified number in [0,1]. Define

    F = w(Y_0) g((Y_{-s})_{0<=s<=t}) g((Y_s)_{0<=s<=t}),
    C = E F,                    p = E w(Y_0).

The same function g is applied to the past read outward from time zero and to the future read outward from time zero. An arbitrary additive constant in g is allowed. Conditional on X_0, the two halves are independent, including when g also uses the deterministic central label Y_0.

## 2. Direct entropy-production theorem

**Theorem.** For the model above,

    sigma >= 8 [-C]_+ / (R^2 t).                                    (1)

If C<0 and p>0, set

    eta = -4 C / (p R^2).

Necessarily 0<eta<=1, and the sharper statement is

    sigma >= (2p/t) sqrt(eta) artanh(sqrt(eta)).                     (2)

At eta=1 the right side is interpreted as infinity. In particular, equilibrium requires C>=0 for every such g,w,t.

### Proof of the linear bound

Let P_i and P_i* be the laws of the full hidden future half-path, starting at i, under Q and Q*. Put

    u_i = E_{P_i} g(h(X)),       v_i = E_{P_i*} g(h(X)).

The stationary past, read outward from time zero and conditioned on X_0=i, has law P_i*. Conditional independence of past and future therefore gives

    C = sum_i pi_i w(h(i)) u_i v_i.

Use the pointwise algebraic identity

    u_i v_i = ((u_i+v_i)/2)^2 - ((u_i-v_i)/2)^2
            >= -(u_i-v_i)^2/4.

The difference of expectations of an R-range observable is at most R times total variation. Pinsker then gives

    (u_i-v_i)^2 <= R^2 TV(P_i,P_i*)^2
                  <= (R^2/2) D(P_i || P_i*).

Thus

    C >= -(R^2/8) sum_i pi_i D(P_i||P_i*).

Starting the two path laws in the same pi, the initial-law relative entropy is zero. Q and Q* have the same exit rate at every state. The standard CTMC likelihood-ratio formula therefore yields exactly

    sum_i pi_i D(P_i||P_i*) = t sigma.

This proves (1). This derivation does **not** use additive reversibilization or a quadratic distance to the equilibrium class. Its linear dependence on the negative reflection defect is stronger than that generic route near equilibrium.

### Proof of the nonlinear refinement

Write v_i^TV=TV(P_i,P_i*). For any pair of probability laws P,Q with total variation v,

    D(P||Q)+D(Q||P) >= 4 v artanh(v).                              (3)

To prove (3), coarse-grain to the set on which dP>dQ. The resulting Bernoulli parameters differ by v. For a fixed difference, their Jeffreys divergence is minimized by parameters (1+v)/2 and (1-v)/2, yielding (3).

The weighted reflection deficit obeys

    -C <= (R^2/4) sum_i pi_i w_i (v_i^TV)^2.

Both stationary path KL directions have mean t sigma, because reversing Q exchanges every stationary edge flux pair. Hence

    2 t sigma = sum_i pi_i [D(P_i||P_i*)+D(P_i*||P_i)]
              >= 4 sum_i pi_i w_i v_i^TV artanh(v_i^TV).

The function H(s)=sqrt(s) artanh(sqrt(s)) is increasing and convex on [0,1):

    H(s)=sum_{n>=1} s^n/(2n-1).

Jensen with weights pi_i w_i/p now proves (2). Its first-order term is exactly (1), because H(eta)>=eta.

### Generality and boundary

The proof only requires a stationary two-sided Markov process, conditional independence of the two halves given the complete present state, the ordinary even-variable reverse, and finite stationary half-path KL equal to t sigma. It therefore suggests a direct extension to other Markov processes satisfying these precise hypotheses. The finite CTMC version is fully proved here; no unproved diffusion regularity is used.

The argument is not a universal thermodynamic theorem for hidden odd variables, nonstationary preparation, or an observer with unmodelled dynamical memory. Those are substantive changes to the model.

## 3. The four-state construction

Let a>0 and 0<epsilon<a/2. Define column vectors

    1=(1,1,1,1)^T,
    f=(1,1,-1,-1)^T,
    h=(1,-1,1,-1)^T,
    k=(1,-1,-1,1)^T=f*h.

They are orthonormal in the stationary inner product <u,v>=(u^T v)/4. Take

    Q = -a(I - 11^T/4) + (epsilon/4)(h f^T + f k^T).              (4)

Explicitly,

    Q = [ -3a/4+epsilon/2,   a/4,        a/4-epsilon/2,  a/4             ]
        [  a/4,              -3a/4-epsilon/2, a/4,       a/4+epsilon/2  ]
        [  a/4,               a/4+epsilon/2, -3a/4,      a/4-epsilon/2  ]
        [  a/4-epsilon/2,     a/4,        a/4+epsilon/2, -3a/4            ].

All off-diagonal rates are positive. Rows and columns sum to zero, so pi=(1/4,1/4,1/4,1/4) and the chain is irreducible. Observe only

    Y_t = f(X_t) in {+1,-1}.

In the centered basis,

    Q f = -a f + epsilon h,
    Q h = -a h,
    Q k = -a k + epsilon f.                                      (5)

Thus the propagator acts as

    P_t f = e^{-at}(f+epsilon t h),
    P_t h = e^{-at} h,
    P_t k = e^{-at}(k+epsilon t f+(epsilon t)^2 h/2).               (6)

### All one-time and two-time laws agree with an equilibrium telegraph process

The stationary mean is zero. From (6),

    E[Y_0 Y_t] = <f,P_t f> = e^{-at}.                             (7)

For binary mean-zero outputs the entire two-time law is determined by this correlation:

    P(Y_0=u,Y_t=v) = (1+uv e^{-at})/4,   u,v in {+1,-1}.          (8)

These are exactly the laws of the reversible symmetric two-state chain with flip rate a/2. Consequently all one-time observables and all their two-time correlations agree with that equilibrium process, at every lag. No test using only the complete collection of such population laws can distinguish the two.

The output Y is nonetheless not a Markov chain: its higher-order laws differ.

### The entire observed path law is time-reversal symmetric

Let R be the permutation swapping hidden states 3 and 4 and fixing 1 and 2. It fixes f and 1 and exchanges h and k. Directly,

    Q^T = R Q R.

Every observation projector D_y commutes with R. For an arbitrary observed word with arbitrary positive gaps, transpose its stationary matrix-product probability and use P_t^T=R P_t R, R1=1, and R D_y=D_y R. All R factors cancel. The result is precisely the probability of the reversed word with reversed gaps.

Therefore the visible process has zero forward-versus-reversed path KL on every finite time window. This is stronger than merely having zero two-time current. Every visible time-arrow estimator vanishes in the infinite-data limit.

### The three-time law and its reflection obstruction

For s,t>0,

    E[Y_0 Y_s Y_{s+t}] = <f,P_s D_f P_t f>
                        = epsilon^2 s t e^{-a(s+t)}.             (9)

At equal gaps set r=e^{-at}, m=r^2(epsilon t)^2. The complete triple law is

    P(Y_{-t}=u,Y_0=v,Y_t=w)
       = [1+r(uv+vw)+r^2 uw+m uvw]/8.                           (10)

It is explicitly symmetric under u<->w, as it must be.

Conditioning on the central symbol Y_0=-1 gives

    E[Y_{-t}|Y_0=-1] = E[Y_t|Y_0=-1] = -r,
    E[Y_{-t}Y_t|Y_0=-1] = r^2-m,
    Cov(Y_{-t},Y_t | Y_0=-1) = -m < 0.                          (11)

Under any stationary reversible all-even hidden Markov model this conditional covariance must be nonnegative: given the hidden present state the two observations are independent draws from the same conditional distribution; their covariance after conditioning only on the central visible symbol is the variance of their common conditional mean.

For the explicit bounded witness choose

    w(Y_0)=1{Y_0=-1},    g(Y_t)=Y_t+r.

It has p=1/2, R=2, and

    C = E[1{Y_0=-1}(Y_{-t}+r)(Y_t+r)] = -m/2.                  (12)

Therefore **every compatible all-even hidden CTMC**, regardless of hidden architecture and rates, obeys

    sigma >= m/t = epsilon^2 t e^{-2at}.                         (13)

The nonlinear form is

    sigma >= epsilon e^{-at} artanh(epsilon t e^{-at}).           (14)

The linear expression (13) is optimized over t at t=1/(2a), yielding epsilon^2/(2ae). The actual generator's entropy-production rate is

    sigma(Q) = (epsilon/2) log[(a+2epsilon)/(a-2epsilon)].         (15)

As epsilon/a -> 0 this is 2epsilon^2/a + O(epsilon^4/a^3). At the optimal lag the linear certificate is a fraction 1/(4e) of the actual leading-order dissipation. No claim is made that (13), (14), or Q is the globally sharp cost over compatible architectures.

For an arbitrary fixed shift c (useful for avoiding data-dependent tuning),

    E[1{Y_0=-1}(Y_{-t}+c)(Y_t+c)]
       = [(c-r)^2-m]/2.                                        (16)

Consequently a shift error |c-r|<sqrt(m) preserves a strict certificate. A learned shift should be selected on independent calibration data or handled by a simultaneous confidence procedure.

## 4. Numerical instance requested by root

Take a=1, epsilon=0.4, t=0.5. Then

    Q = [[-0.55, 0.25, 0.05, 0.25],
         [ 0.25,-0.95, 0.25, 0.45],
         [ 0.25, 0.45,-0.75, 0.05],
         [ 0.05, 0.25, 0.45,-0.75]].

Computed by scipy.linalg.expm and independent enumeration of all eight triple probabilities:

    r                         = 0.6065306597126334
    m                         = 0.014715177646857697
    C                         = -0.0073575888234288485
    conditional covariance    = -0.014715177646857697
    sigma actual              = 0.43944491546724396
    sigma linear lower bound  = 0.029430355293715394
    sigma nonlinear bound     = 0.029576001029894584
    chi-square(P_eps || P_0)   = 0.0005419150197415458

All eight triple probabilities from matrix multiplication agree with (10) to at most 5.6e-17 in double precision. These numerical checks support the algebra and are not a replacement for the proof.

| (Y_-t,Y_0,Y_t) | probability |
| --- | ---: |
| (+,+,+) | 0.3244569922804459 |
| (+,+,-) | 0.0771756726477125 |
| (+,-,+) | 0.017512868012414723 |
| (+,-,-) | 0.08085446705942692 |
| (-,+,+) | 0.07717567264771251 |
| (-,+,-) | 0.02119166242412915 |
| (-,-,+) | 0.08085446705942693 |
| (-,-,-) | 0.3207781978687314 |

A convenient exact alternate instance is a=1, epsilon=1/4, t=log 2, c=1/2. Its Q is rational, C=-(log 2)^2/128, linear floor=(log 2)/64, nonlinear floor=(1/8)artanh((log 2)/8), actual cost=(log 3)/8.

## 4a. Four hidden states are minimal for this precise separation

**Lemma (proposed by root, independently audited here).** A stationary finite CTMC with at most three hidden states and a nonconstant binary deterministic output cannot simultaneously have an exactly single-exponential centered autocovariance and a non-Markov output process. Consequently four states are minimal for the exact separation constructed above.

**Proof.** Normalize the centered binary output f to unit norm in L^2(pi). The mean-zero subspace has dimension at most two. If it has dimension one, f is automatically a generator eigenfunction. Otherwise choose an orthonormal basis beginning with f. The generator's matrix on this invariant subspace has the form

    A=[[-a,b],[c,d]],

because the first derivative of <f,e^{tQ}f>=e^{-at} at zero is -a. Its second derivative is a^2+bc, which must equal a^2. Hence bc=0. If c=0 then Qf=-af; if b=0 then Q*f=-af.

For a binary output an eigenfunction relation Qf=-af makes the total rate from a hidden state into the other output block depend only on its current output label. This is strong lumpability, so the observed process is a two-state CTMC. If instead Q*f=-af, the stationary reversed observed process is a two-state CTMC. Every stationary two-state CTMC is reversible, so the original output is the same Markov process. This proves the lemma.

The minimality statement is only for a nonconstant binary label with an exactly single-exponential autocovariance at every lag. It makes no claim about the smallest system for arbitrary hidden dissipation, multiexponential correlation, other observation alphabets, or other inference targets.

## 5. Statistical operation and paid access

The inference theorem is a population statement. A complete finite-data operation is available with the following explicitly specified access: N independent realizations, each initialized in its own stationary distribution, observed at 0,t,2t. Equivalently one has N independent stationary windows of length 2t. The cost is N preparations/independent copies, 3N recorded symbols, and total sequential observation time 2tN, plus the real preparation/reset cost supplied by that access. Storage and arithmetic for a fixed score are O(1) working memory and O(N) updates.

This access must **not** be silently replaced by arbitrary adjacent windows from one unknown slow hidden process. Stationarity and independence are substantive experimental resources. A single-record guarantee requires a declared mixing/concentration bound or a separate valid dependent-data argument.

For a prespecified c in [-1,1], score

    F_j=1{Y_t^{(j)}=-1}(Y_0^{(j)}+c)(Y_{2t}^{(j)}+c)

has range width L=2(1+|c|). Hoeffding gives, with probability at least 1-delta,

    C <= F_bar + L sqrt[log(1/delta)/(2N)].

The theorem yields a valid one-sided confidence certificate

    sigma >= (2/t) max{0, -F_bar - L sqrt[log(1/delta)/(2N)]}.     (17)

For the family with c=r, choose N>=8L^2 log(1/alpha)/m^2 and reject equilibrium if

    F_bar < -L sqrt[log(1/alpha)/(2N)].

The false-positive probability is at most alpha for every hidden equilibrium model under the stated independent stationary sampling access. The alternative's false-negative probability is at most alpha. This is O(epsilon^{-4} log(1/alpha)) for fixed a,t.

The root independently derived the matching fixed-lag lower bound. To record it here: for the eight-outcome triple law (10), relative to epsilon=0,

    chi-square(P_epsilon || P_0) = m^2/(1-r^2)^2.                 (18)

Since KL<=chi-square and N independent triples have additive KL, any test with both errors <=alpha<1/4 requires

    N >= [(1-r^2)^2/m^2] log[1/(4alpha)]                         (19)

by the standard Bretagnolle-Huber testing inequality. The power epsilon^{-4} is therefore optimal in this explicitly fixed-lag independent-triple access model. This does not prove an optimum for continuous trajectory access, arbitrary adaptive timing, or interventions.

## 5a. A single-record equilibrium test without a null mixing bound

The independent-window inference certificate above can be supplemented by a stronger sampling result for **testing equilibrium**. It controls the null error on one uninterrupted stationary trajectory, even when the unknown equilibrium model mixes arbitrarily slowly.

Fix the gap t, a real function g of one visible snapshot, and a weight w in [0,1], in advance. Write |g|<=G and osc(g)<=R. Sample Y_n=Y_{nt} for n=0,...,N+1, and form

    F_n=w(Y_n) g(Y_{n-1})g(Y_{n+1}),  n=1,...,N.

For every finite stationary reversible hidden CTMC,

    P[sum_{n=1}^N F_n <= -u]
        <= 2 exp[-u^2/(2N G^2 R^2)].                            (20)

Thus the prespecified test

    reject equilibrium if F_bar < -GR sqrt[2 log(2/alpha)/N]      (21)

has false-positive probability at most alpha uniformly over all hidden state counts, rates, and mixing times. It uses only N+2 snapshots and chronological duration (N+1)t, plus stationarity preparation. It does not supply an entropy-rate confidence interval or an alternative-power guarantee by itself.

### Proof

Let P=e^{tQ}, let X_n be the full hidden sampled chain, abbreviate g_n=g(h(X_n)), w_n=w(h(X_n)), and let h_n=(Pg)(X_n). Under equilibrium, P is reversible. Decompose exactly

    F_n = w_n h_n^2 + A_n + B_n,
    A_n = w_n g_{n-1}(g_{n+1}-h_n),
    B_n = w_n h_n(g_{n-1}-h_n).

A_n is a forward martingale difference when revealing X_{n+1} after X_0,...,X_n. B_n is a backward martingale difference when revealing X_{n-1} after X_n,...,X_{N+1}; reversibility and stationarity give its conditional mean zero. The conditional range length of each increment is at most GR. The sum of w_n h_n^2 is nonnegative. Therefore a score sum below -u forces either sum A_n<-u/2 or sum B_n<-u/2. Applying the conditional-range form of Hoeffding-Azuma in each time direction and a union bound gives (20).

The proof does not require the observer to know or estimate the hidden function h_n; it is used only to establish the calibration. No independence between the two martingales is assumed. g,w and the schedule must be prespecified, or their selection must be controlled by a separate valid multiple-testing or calibration argument.

For the explicit alternative, a known spectral/mixing bound or another model-specific concentration argument can supply power. The symmetric part of its hidden generator has gap a-epsilon/sqrt(2)>0. A claim of optimal single-record sample complexity needs its own lower and upper proofs; the independent-triple lower bound (19) must not be silently transferred to this richer access model.

## 6. Essential parity boundary

The same four-state Q satisfies generalized detailed balance under the involution R that swaps 3 and 4:

    pi_i Q_ij = pi_{Rj} Q_{Rj,Ri},
    pi_i=pi_{Ri},    Q_ii=Q_{Ri,Ri}.

If this R is the **physical** time reversal, then the full hidden process has zero physical entropy production. The observed label f is even under R, so all observed data are exactly unchanged.

Thus the very same visible process has:

* a strictly positive architecture-independent dissipation floor among ordinary all-even Markov realizations;
* an explicit finite zero-physical-dissipation realization when a hidden odd parity is allowed.

Parity cannot be determined from these data. It must come from the physical model of the hidden variables. Merely assigning an arbitrary mathematical involution to an actual apparatus does not erase its dissipation; the involution has to describe its real microscopic reversal. This boundary is central to interpreting the theorem and prevents an overbroad ‘data alone always reveals heat’ claim.

## 7. Prior-art comparison and novelty limits

The following are primary papers or primary-source manuscripts inspected through their abstracts/full text. No exhaustive priority claim is justified by this bounded search.

0. Jorgensen, Neeb, and Olafsson, **Reflection Positive Stochastic Processes Indexed by Lie Groups**, SIGMA 12, 058 (2016).
   https://sigma-journal.com/2016/058/
   https://arxiv.org/abs/1510.07445
   Reflection positivity of symmetric Markov processes is established mathematics, with older roots in Osterwalder-Schraders' framework. The nonnegative equilibrium conditional-square identity itself is not claimed new. The present novelty candidate is its quantitative dissipation-defect conversion, explicit observational separation, and inference operation.

1. Skinner and Dunkel, **Estimating Entropy Production from Waiting Time Distributions**, PRL 127, 198101 (2021).
   https://math.mit.edu/~dunkel/Papers/2021SkDu_PRL.pdf
   They already infer dissipation from time-symmetric waiting statistics without visible currents, including full-law optimization as a conceptual optimum and a numerically obtained waiting-variance bound. This work must not be described as discovering that time-symmetric observations can contain dissipation information.

2. Martinez et al., **Inferring broken detailed balance in the absence of observable currents**, Nature Communications (2019).
   https://pmc.ncbi.nlm.nih.gov/articles/PMC6684597/
   Uses semi-Markov waiting-time asymmetry and visible path irreversibility. Our example's entire visible law is reversible, so arrow-based estimators are zero, but other full waiting-law estimators need not be zero.

3. Raux, Maier, and Seifert, **Lower bounds on entropy production from dynamical correlation functions**, arXiv:2608.03619 / accepted PRE (2026).
   https://arxiv.org/abs/2608.03619
   https://journals.aps.org/pre/accepted/10.1103/h28h-g7g7
   Uses asymmetry of two-time cross-correlations. Our binary observable's entire two-time law equals a reversible telegraph process and has zero asymmetry.

4. Aznagulov, **The Spectral Cost of Detecting Nonequilibrium at Finite Temporal Resolution**, arXiv:2609.37205v1 (2026).
   https://arxiv.org/html/2609.37205v1
   Supplies finite-resolution, hidden-equilibrium inference and additive-reversibilization comparisons, with a full-observation normal-network spectral law and antisymmetric-score tests. It is a close source and should not be ignored. Our direct linear reflection-defect bound and time-symmetric binary triple witness are different from the stated antisymmetry route. Full text searched for reflection without finding such a theorem; that is not proof of absence or priority.

5. Aznagulov, **Thermodynamic Realizability of Hidden Markov Processes: Attainment, Observable Certificates, and the Price of Architecture**, arXiv:2609.14623v1 (2026).
   https://arxiv.org/html/2609.14623v1
   Broad exact-law architecture optimization and observable certificate representation. It establishes a general variational framework, not the explicit triple certificate derived here. The present result does not solve its all-dimension optimum/nonattainment questions.

6. **Hidden dissipation without a known architecture**, Evidence Press / ipitchford candidate (October 2026).
   https://www.evidencepress.org/releases/hidden-dissipation-floor/
   https://github.com/ipitchford/hidden-dissipation-floor/blob/main/SOURCES.md
   This is an explicitly anonymous, unrefereed mathematical candidate, not authoritative empirical evidence. Its primary manuscript claims an all-dimension zero-floor classification for finite PH alternating-renewal laws and credits older equilibrium hyperexponential restrictions. It blocks any casual novelty claim for architecture-independent waiting-law floors. It is not a load-bearing premise of our proof.

7. Van der Meer et al., **Fluctuating entropy production on the coarse-grained level: Inference and localization of irreversibility**, PRR 6, 023175 (2024).
   https://doi.org/10.1103/PhysRevResearch.6.023175
   Explicitly treats odd-variable subtleties. Our parity boundary is consistent with that established caveat; it is an explicit construction, not the first recognition of it.

### Strongest applicable comparison, without overselling

The accomplished operation is an explicit, hidden-dimension-independent entropy floor from three time-symmetric snapshots and bounded scores, together with a family proving strict separation from the complete two-time law and from the complete observed time arrow. The proof gives a quantitative linear defect bound and a simple finite-data certificate under paid independent stationary-window access.

It does **not** dominate an optimal estimator using the full continuous observed path. In this four-state example the negative macrostate's dwell survival is already non-hyperexponential. Its transient matrix is

    T_-=[[-3a/4,a/4-epsilon/2],[a/4+epsilon/2,-3a/4]],

with stationary entrance alpha_-=((a-epsilon)/(2a),(a+epsilon)/(2a)). Set q=sqrt(a^2-4epsilon^2)/4 and B=(a+2epsilon^2/a)/sqrt(a^2-4epsilon^2)>1. Then

    S_-(s)=((1+B)/2)e^{-(3a/4-q)s}
            +((1-B)/2)e^{-(3a/4+q)s}.

The second coefficient is negative, so continuous dwell-law methods can also detect an obstruction. The novelty candidate is the representation, explicit three-snapshot operation, and its quantitative bound/cost/separation, not a claim that prior full-record methods have no signal.

No civilization-changing discovery is established merely by these mathematical facts. The theorem is a meaningful inferential capability in a specific physical model; its wider importance requires additional scientific applications and scrutiny.
