# Response-completed closure: active information, predictive autonomy, and a kinetic-access obstruction

## Status

This is a mathematical research candidate developed in the present conversation. The proofs below are self-contained finite-state arguments. They have not been independently reviewed or formally verified. Historical priority for the combination of operational Gram recovery, the controlled path certificate, the finite-field acquisition protocol, and the access obstruction is unresolved.

The following ingredients are NOT claimed as new: strong and weak lumpability; orthogonal projection residuals; nonequilibrium linear response; positivity of a Gram matrix; Markov-chain time change; relative-entropy comparison on path space; polynomial interpolation; Hoeffding/Bernstein bounds. The candidate contribution is their particular operational combination: measure an otherwise hidden closure residual using visible, calibrated experiments, and use it to certify complete future controlled-path error without reconstructing the microscopic model.

This is NOT a universal method for identifying hidden generators, a universally optimal experimental design, or a proof that a laboratory system obeys the assumed intervention rule. The exact population zero test and finite-confidence approximate test are different statements.

## 1. Model and notation

Let Q be the row generator of an irreducible finite continuous-time Markov chain X, with stationary distribution pi_i>0. All rate sums are finite. The number n of microscopic states is unrestricted and need not be known to the experimenter. The observed label is Y=ell(X) in {1,...,k}; every label has positive stationary probability mu_a. Write e_a(i)=1_{ell(i)=a}, E=[e_1 ... e_k], R=diag(pi), M=diag(mu), and use the real inner product <f,g>_pi=f^T R g.

The orthogonal conditional-expectation projection onto functions of the label is

    P = E M^{-1} E^T R.

Let

    A = E^T R Q E,
    L = M^{-1} A,
    B = (I-P) Q E = Q E - E L,
    Gamma = B^T R B.

L is a valid k-state generator and mu^T L=0. For i in label a and b!=a, let r_ib=sum_{j:ell(j)=b} q_ij. Then (QE)_ib=r_ib off the source label, while its source-label coordinate is minus the total rate of leaving that label. Gamma is the weighted covariance of these aggregate rates around their source-label conditional averages L_ab.

The dimension-free resource statements assume a supplied upper bound Lambda on all microscopic exit rates. They do not claim to infer such a bound from an arbitrary observation record.

A geometric label-potential intervention g in R^k acts as

    q_ij^{h,g} = q_ij exp[h(g_{ell(j)}-g_{ell(i)})/2], i!=j,

with adjusted diagonal. This is a prescribed microscopic rate rule. It holds symmetric kinetic prefactors fixed. Local detailed balance alone does not imply it.

## 2. Exact operational recovery of Gamma

Measure the stationary two-time joint probabilities

    C_ab(t) = E[e_a(X_0)e_b(X_t)].

For the pulse g=e_a, started from the SAME unperturbed stationary law, define

    chi_ab(t) = d/dh E_h[e_b(X_t)] at h=0.

All derivatives below are finite-state derivatives at time zero. Put X2_ab=chi_ab''(0) and C2=C''(0). Then

    Gamma = -2 X2 - C2 - A^T M^{-1} A,             (2.1)
    A = C'(0).

In particular, the right side is symmetric positive semidefinite despite its apparently nonsymmetric components.

### Proof

Let Q* = R^{-1} Q^T R, S=(Q+Q*)/2, and V_a=dQ^{h,e_a}/dh at zero. Direct differentiation of off-diagonal rates, followed by stationarity, gives

    pi^T V_a g = -<S e_a,g>_pi.

Duhamel's formula and pi^T exp(sQ)=pi^T yield

    chi_ab(t) = -int_0^t <S e_a, exp(sQ)e_b>_pi ds.

Thus X2_ab=-<S e_a,Qe_b>_pi, while C2_ab=<e_a,Q^2 e_b>_pi=<Q*e_a,Qe_b>_pi. Consequently

    -2 X2_ab-C2_ab = <Qe_a,Qe_b>_pi.

Subtracting the Gram matrix of P Q E, which is A^T M^{-1} A, leaves B^T R B. This proves (2.1).

### Observable Krylov interpretation

Decompose functions into the observed space and its orthogonal complement. In this decomposition Q has blocks

    Q = [ L   C_hidden ]
        [ B_hidden  D_hidden ].

Passive two-time jets involve L^2+C_hidden B_hidden, and higher jets involve directed return products such as C_hidden D_hidden^j B_hidden. A large B_hidden can be concealed by cancellation, one-sided coupling, or long return paths.

The response completion replaces the directed return product by B_hidden* B_hidden. Positivity prevents cancellation from making this product zero unless B_hidden itself is zero. The Gram residual is a standard object; its acquisition from the specified visible interventions is the operational step here.

## 3. A finite-amplitude extraction; no infinitesimal-field oracle

For an indicator pulse e_a set z=exp(h/2). Its generator is Laurent-linear:

    Q_a(z)=Q+(z-1)K_a^+ +(z^{-1}-1)K_a^-,

where K_a^+ contains transitions into label a with the corresponding diagonal correction and K_a^- contains transitions out. Hence

    F_ab(z)=pi^T Q_a(z)^2 e_b

is a Laurent polynomial with powers -2,-1,0,1,2. The linear functional

    D[F] = -(F(2)-F(1/2))/6
           +9(F(3/2)-F(2/3))/10                 (3.1)

equals (1/2)F'(1) on this five-dimensional space. This is checked on the five monomials, or by solving for the two antisymmetric coefficients. Since d/dh=(z/2)d/dz,

    X2_ab = D[F_ab].                             (3.2)

Only the four fixed multipliers 2, 1/2, 3/2, and 2/3 are needed. Every microscopic rate changes by a factor between 1/2 and 2. The field strengths h=2 log z are fixed numbers, not quantities tending to zero with the requested accuracy.

This exact statement concerns time curvature, not the entire finite-time response: exp(tQ_a(z)) is not generally Laurent-polynomial of degree two. Section 7 bounds the finite-time curvature approximation explicitly.

## 4. Exact autonomous controlled state criterion

The following are equivalent:

1. Gamma=0.
2. (I-P) Q P=0: the observed function space is Q-invariant.
3. For every i in label a, r_ib=L_ab for every b!=a (strong lumpability).
4. For every initial microscopic law, the observed process is the Markov chain L; after any known label-dependent rate multiplication c_ab(t,observed history), its observed conditional rates are c_ab L_ab.

Here c_ab are positive bounded predictable multipliers, and the feedback policy is well posed and has no hidden-state access. Randomized policies are allowed by conditioning on their exogenous seed. Multipliers for internal same-label transitions can also be allowed; they do not affect the aggregate off-diagonal rates.

### Proof

Gamma=0 iff each column of B vanishes, since pi_i>0. This is exactly the aggregate-rate condition. That condition specifies the observed conditional jump intensities independently of the hidden conditional distribution. Multiplication by c_ab preserves it, even with observation-dependent feedback. Conversely, use a point mass as the initial microscopic law and inspect first jump intensities. This forces the aggregate-rate condition.

### Important distinction

Gamma=0 tests strong, intervention-compatible state autonomy. It is NOT equivalent to the observed stationary path alone being Markov. A stationary observed Markov process may have Gamma>0. Section 6 gives a whole class of such processes.

## 5. Quantitative full-path prediction

Let d=tr Gamma. Let ell_min be the smallest positive off-diagonal entry of L. Entries L_ab=0 cause no problem: all corresponding r_ib are zero, since they are nonnegative and have conditional average zero.

Start the true chain in pi. Let P_Q^{u,T} be its observed path law under a predictable label-dependent multiplier policy with

    exp(-H) <= c_ab(t,history) <= exp(H).

Let P_L^{u,T} be the k-state controlled Markov path law using c_ab L_ab and initial mu.

Suppose the true controlled microscopic marginal obeys

    Law(X_t=i) <= C_T pi_i for 0<=t<=T.          (5.1)

Then

    KL(P_Q^{u,T} || P_L^{u,T})
        <= C_T exp(H) T d / ell_min,             (5.2)

and

    TV(P_Q^{u,T},P_L^{u,T})
        <= sqrt(C_T exp(H) T d/(2 ell_min)).     (5.3)

A rate-floor-free alternative is

    TV <= C_T exp(H) T sqrt((k-1)d).             (5.4)

These bounds concern the entire path, not merely endpoint distributions or one selected observable. They apply simultaneously to every policy obeying the stated bounds, with the same constants.

### Acquired sufficient regularity conditions

With no control, C_T=1.

For any finite generator with exit rates <=Lambda, all the allowed controls obey

    C_T <= exp(2 Lambda T sinh H).              (5.5)

This dimension-free bound can be exponentially large in the controlled horizon; it is not silently treated as polynomial.

A stronger explicit class has

    lambda pi_j <= q_ij <= Lambda pi_j for i!=j, (5.6)

where 0<lambda<=Lambda are supplied bounds. This includes arbitrary internal nonreversibility, unknown state count and nonuniform pi, but requires a globally mixing background and an upper comparability bound. It is a real restriction, not inferred from the observed measurements. For this class,

    C_T <= (Lambda/lambda) exp(2H),             (5.7)

uniformly over time and feedback, and ell_min>=lambda min_a mu_a. Thus

    TV <= sqrt((Lambda/lambda) exp(3H) T d/(2 ell_min)). (5.8)

No lower bound on individual microscopic stationary probabilities appears. A sufficient physical example is a bounded-rate system with sufficiently strong resetting plus the stated upper rate comparability; arbitrary local-interaction physics is not automatically covered.

### Proof of path comparison

Construct a hidden comparison generator Qbar. Within a label retain all rates. For i in label a, b!=a and r_ib>0, put

    qbar_ij = q_ij L_ab/r_ib for ell(j)=b.

When r_ib=0<L_ab, distribute total L_ab among states of label b arbitrarily. This introduces no forward-support problem for KL from Q to Qbar. Set diagonals to zero row sums. Then Qbar E=EL, so Qbar is strongly lumpable. Apply the same multipliers c to Qbar; its observed law is exactly P_L^{u,T}.

For x>=0,y>0 define Psi(x,y)=x log(x/y)-x+y, with the continuous convention at x=0. The continuous-time likelihood formula gives, after summing destinations within a label,

    KL(hidden controlled Q || hidden controlled Qbar)
      = E_Q int_0^T sum_{b!=Y_t} c_{Y_t,b} Psi(r_{X_t,b},L_{Y_t,b}) dt.

The policies are the same functions of the recorded history in the two laws. Therefore their rate multipliers agree at a common path argument, which is what the likelihood formula requires.

Use Psi(x,y)<= (x-y)^2/y, marginal domination (5.1), and c<=exp(H). The cross-label squared residuals are at most tr Gamma; the diagonal residual squares only increase that trace. Data processing to observed paths and Pinsker prove (5.2)-(5.3).

For (5.4), couple the two hidden chains until their first different jump using common rates. At a shared state i their rate of a failed coupling is at most sum_{b!=a} c_ab |r_ib-L_ab|. Integrate its expectation under the true process. Cauchy-Schwarz gives E_pi sum_{b!=a}|r_ib-L_ab|<=sqrt((k-1)d). No KL denominator is needed.

### Proof of marginal bounds

For (5.5), put v_i(t)=Law(X_t=i)/pi_i. At a component attaining the maximum of v, stationarity gives

    d/dt max_i v_i <= Lambda(exp(H)-exp(-H)) max_i v_i.

The same inequality holds for feedback because each conditional rate stays inside the specified pointwise interval. Starting at v=1 and applying Gronwall proves (5.5).

For (5.6), writing p_j(t)=Law(X_t=j), the bounds hold pathwise even under feedback and imply

    p'_j <= Lambda exp(H) pi_j(1-p_j)
             -lambda exp(-H)(1-pi_j)p_j
          <= Lambda exp(H)pi_j -lambda exp(-H)p_j.

Comparison with this scalar ODE proves (5.7).

### Estimated, rather than exact, reduced rates

If a valid reconstructed generator Lhat satisfies

    max_a sum_{b!=a}|Lhat_ab-L_ab| <= delta_L,

then an additional coupling error at most T exp(H) delta_L must be added, along with the error in the initial observed law. If ||Gammahat-Gamma||_op<=eta, use max(0,tr Gammahat+k eta) as a certified upper bound for d. A finite dataset never certifies an exact population zero merely by numerical rounding.

## 6. Information unavailable from passive observation, even at infinite time

Consider the class satisfying the reverse-invariance condition

    P Q(I-P)=0.                                (6.1)

Equivalently, Q* is strongly lumpable on the observed partition. Started in stationarity, Y is exactly the k-state Markov chain L. This follows by reversing the strongly lumpable stationary Q* chain; equivalently, propagate any stationary label-cylinder probability in the Q*-invariant observed subspace. All finite-dimensional distributions agree, and therefore the full path laws agree.

Condition (6.1) does not imply (I-P)QP=0. Thus Gamma may be positive. For a fixed observed stationary chain there can be models with Gamma=0 and models with Gamma bounded away from zero that have EXACTLY the same complete passive law.

### A large positive class, not a long nilpotent ladder

For uniform pi, let J be uniform averaging, P the block-averaging projection for any nontrivial partition, and Z an arbitrary real matrix. Put

    Q = J-I + epsilon (I-P) Z (I-J),            (6.2)

with epsilon small enough that all off-diagonal entries remain positive. Then Q1=0, pi^TQ=0, and P Q(I-P)=0. Every such model has the same observed refresh generator

    L = 1 mu^T-I.

Z can alter both the observed-to-hidden coupling and the internal hidden dynamics. No nilpotence, special spectrum, long word cancellation, or symmetry pairing is required. The passive equivalence class contains relatively open sets inside the linear constraints defining (6.1), with a positive rate margin. Gamma varies continuously and is generically nonzero when the partition has hidden degrees of freedom.

Therefore no passive estimator can consistently distinguish the hypotheses Gamma=0 and tr Gamma>=g over a class containing one matched pair, at ANY observation horizon. The two probability laws of all passive data coincide. In contrast, Section 7 gives a finite active test with polynomial resources whenever a positive gap g and the stated access/regularity bounds are provided.

This is a minimax impossibility. It does NOT say every nearby perturbed model remains individually difficult for passive observation.

### Four-state witness

Take f=(1,-1,1,-1)^T, d=(1,-1,-1,1)^T, pi uniform, epsilon=1/4, and

    Q=J-I+epsilon d f^T/4.

In ordinary coordinates,

    Q=(1/16) [ -11  3   5   3
                3 -11  3   5
                3   5 -13  5
                5   3   5 -13 ].

Use the labels of f. Its entire stationary observed law is the symmetric two-state chain of flip rate 1/2. Nevertheless,

    Gamma=(1/64) [ 1 -1; -1 1 ].

A pulse of the sign observable f has

    chi(t)=1-exp(-t)
           -(epsilon^2/2)[1-(1+t)exp(-t)].

The equilibrium two-state realization has chi_eq(t)=1-exp(-t). No passive experiment distinguishes these two realizations, while calibrated active experiments do.

### The certificate is not a full controlled realization

In the preceding example replace Q by

    Q_beta=J-I+epsilon d f^T/4+beta d d^T/4,

with |epsilon|+|beta|<1. All these models have the same entire passive law AND the same Gamma, while their finite-time controlled responses differ: Q_beta d=-(1-beta)d, and the third time derivative of the f-pulse susceptibility is 1+epsilon^2(1-beta/2). Thus Gamma certifies closure and bounds approximation error when small; it does not encode all controlled dynamics when large.

## 7. Finite samples, sensor noise, time, and calibration

Scale time so that the supplied maximum exit-rate bound is one. To restore units, multiply Gamma by Lambda^2 and divide trial durations by Lambda.

Assume each observed label probability is at least rho>0. Allow independent sensor corruption through a known full-rank confusion channel. Suppose corrected indicators phi_a(Z) satisfy

    E[phi_a(Z)|Y=b]=1_{a=b},    |phi_a|<=kappa,

where kappa>=1 is supplied. With a square invertible channel, the appropriate inverse matrix supplies these functions. Independent sensor noise at different observation times makes products of corrected indicators unbiased for two-time joint probabilities. A singular channel, arbitrary uncalibrated noise, or control acting on misidentified rather than actual labels is not covered.

### Explicit conservative acquisition protocol

Given desired normalized operator error 0<eta<=1 and failure probability zeta, put

    u=eta rho^2/(100 k^2),
    s=u/1000,
    beta=u s^2/100.                             (7.1)

Estimate mu, C(s), C(2s), and, for every label a and z in {2,1/2,3/2,2/3}, the terminal label means at times s and 2s after applying Q_a(z), starting from unperturbed stationarity.

Use

    Ahat=(Chat(s)-Mhat)/s,
    C2hat=(Chat(2s)-2 Chat(s)+Mhat)/s^2,

and use the functional (3.1) on

    [m_ab(z,2s)-2 m_ab(z,s)]/s^2

to estimate X2. The missing +mu_b term cancels because the field weights sum to zero. Finally form (2.1) and symmetrize.

If every raw scalar mean is accurate to beta, then every entry of A, C2, X2 and mu is estimated to at most u error. The following bounds establish this without a derivative oracle.

* At zero field, ||Q||_infty<=2; hence |C'''_ab(t)|<=8 and |C''_ab(t)|<=4. The forward second difference has bias <=8s and the first difference bias <=2s.
* Under the four fields, maximum exit rate is <=2, so ||Q_a(z)||_infty<=4 and |d^3m_ab(z,t)/dt^3|<=64. The field weights have total absolute value 32/15. Their time-curvature bias is at most (2048/15)s.
* Raw-mean error in X2 is at most (32/5) beta/s^2; in C2 at most 4 beta/s^2. These fit strictly inside u with (7.1).
* If each entry of Ahat-A and muhat-mu is <=u, each entry of Ahat^T Mhat^{-1} Ahat-A^T M^{-1}A is at most 8k u/rho^2. We used |A_ab|<=1, muhat>=rho/2, and u<=1.

Thus the final operator error is at most 11 k^2 u/rho^2<eta. Symmetrization does not worsen this bound.

The corrected raw scalar variables have absolute value at most kappa^2. Hoeffding and a union bound give a conservative total trial budget

    O(k^2 kappa^4 u^{-6} log(k/zeta)).           (7.2)

The constants are large and the bound is NOT practically optimized. The four fixed amplitudes avoid the extra statistical cost of shrinking a field toward zero. No claim of minimax-optimal sample complexity is made.

In the noiseless case, recording all three times 0,s,2s in each trial and estimating second differences directly exploits the fact that the difference vanishes unless the observed label jumps. Its variance is O(s), yielding an optional Bernstein improvement to O(u^{-5}) per fixed-size family of statistics. The supplied protocol code uses the simpler conservative noisy bound, not this improvement.

To test Gamma=0 against tr Gamma>=g, choose eta<g/(4k) and threshold the estimated trace between the separated ranges. This is a separated-hypothesis test, not exact equality recognition from finite data.

### Starts and waiting time are charged

Either a physical stationary reset is available, or a supplied bound

    sup_nu TV(nu exp(tQ),pi)<=M0 exp(-gamma t)

allows waiting gamma^{-1} log(4 M0 N_total/zeta) before each trial. Conditional coupling to independent stationary starts then costs at most zeta/4 over all trials. Under (5.6), M0=1 and gamma=lambda are available by the common-reset coupling. Thus total duration includes N_total times this wait, plus the pulse intervals. Hidden-state count and min_i pi_i do not enter this bound.

### Precision and systematic error

The designed times and field multipliers have bit lengths polynomial in log(1/eta), log(1/rho), log k, and the supplied numerical bounds. To make raw-mean bias <=beta/2, time and field-setting accuracy can be chosen polynomially small in beta using the bounded-rate Duhamel estimate. Calibration error in the sensor correction must also fit that raw-mean budget. This is an explicit accuracy requirement, not a claim that a physical instrument meets it.

A separate useful robustness bound concerns a finite-field kinetic calibration error. If each implemented generator differs from its geometric-field target by row operator norm at most delta_K, has exit rates <=3Lambda, and the unperturbed Q is unchanged, then each curvature F_ab changes by at most 10Lambda delta_K. The field functional therefore changes Gamma in operator norm by at most

    (128/3) k Lambda delta_K < 50 k Lambda delta_K. (7.3)

Higher time-derivative bounds use the actual supplied rate bound. Hence a nonzero leakage margin tolerates inverse-polynomial kinetic errors. With arbitrary unknown kinetic changes, no such recovery theorem holds; Section 8 gives an exact obstruction.

For an estimated valid macro generator, add the rate-estimation and initial-law errors stated after (5.8). The code returns raw L estimates and does not pretend that numerical projection establishes exact zero rates or exact autonomy.

## 8. A full adaptive access obstruction

Consider a DIFFERENT intervention rule with the same conservative forward/reverse rate ratios:

    q_ij^{u,clock}(t)=exp[-u_{ell(i)}(t,history)]q_ij. (8.1)

Every outgoing rate from a current label is multiplied by the same factor. This is an observable source-clock change.

For any fixed field vector u, both (8.1) and the geometric rule obey

    q_ij^u/q_ji^u = (q_ij/q_ji) exp(u_{ell(j)}-u_{ell(i)}). (8.2)

Their symmetric kinetic factors differ. Thus an energy change and local detailed balance do not specify the information content of an intervention.

### Time-change theorem

Suppose |u_a|<=H and the policy uses only observed history and independent randomness. Its entire controlled observed path through physical time T can be generated from an unforced observed path through operational time at most exp(H)T, together with the policy's random seed.

Proof: given an unforced path y(s), define operational time tau(t) by

    tau'(t)=exp[-u_{y(tau(t))}(t,controlled history)], tau(0)=0,

and set y_control(t)=y(tau(t)). The standard time-change calculation multiplies all outgoing microscopic intensities by tau'(t). Because tau' depends only on the observed history, constructing the transformed observed path does not require the hidden state. Boundedness gives tau(T)<=exp(H)T. For piecewise bounded predictable feedback with a well-posed closed loop this constructs a common Markov kernel from passive to active data.

Consequently, for ANY two hidden models and any such policy,

    TV(active_0 through T, active_1 through T)
      <= TV(passive_0 through exp(H)T, passive_1 through exp(H)T). (8.3)

No downstream statistical procedure, adaptive policy, or independent measurement noise can reverse this data-processing inequality. Fixed physical horizon is the resource being bounded; an unproved expected-stopping-time conclusion is not asserted.

If passive path laws are exactly identical, ALL these active source-clock experiments have exactly identical laws as well, at every horizon. Applied to the prior observation ladder, (8.3) preserves the exponential lower bound up to the acceleration factor exp(H). Amplitudes H=O(log r) only provide a polynomial clock speedup.

The linear-response version is also explicit: V_g=-diag(g)Q, so

    chi_clock,fg(t)=C_fg(0)-C_fg(t)

for every stationary Q, including irreversible ones. It can mimic the equilibrium-form relation without implying reversibility. This dependence on the kinetic implementation is known in nonequilibrium response theory; the all-policy path-information conclusion is proved here rather than inferred from a susceptibility calculation.

## 9. Why the old pointwise exponential separation cannot have a full polynomial-radius robustness neighborhood

Retain the old ladder operator A, sign f, first target d_1 and last source c_ell. Set

    E_short = |f><d_1| + |c_ell><f|,
    Q_r,rho = J-I+epsilon A+rho E_short,
    epsilon=1/(16r), 0<rho<=1/16.

In the physical state basis each E_short entry has absolute value <=2/n. Hence all off-diagonal rates remain >=3/(4n), the stationary law remains uniform, and the observation-reflection symmetry is preserved. The instantaneous observed macro generator also remains unchanged.

On span{f,d_1,c_ell}, put T=epsilon A+rho E_short. Then

    T f=epsilon d_1+rho c_ell,
    T d_1=rho f,
    T c_ell=epsilon f,
    T^2 f=2epsilon rho f.

Therefore the exact stationary autocorrelation is

    C_rho(t)=exp(-t) cosh(sqrt(2epsilon rho)t).

It violates the two-state Markov identity by

    C_rho(2t)-C_rho(t)^2
       =exp(-2t)sinh^2(sqrt(2epsilon rho)t)
       >=2epsilon rho t^2 exp(-2t).             (9.1)

At t=1 this is inverse-polynomial when rho is inverse-polynomial in r. Bounded pair statistics and the uniform mixing bound distinguish this process from any balanced two-state Markov law using O((epsilon rho)^{-2}) samples up to confidence and waiting logarithms.

This supplies arbitrarily small perturbations that preserve positivity, mixing, stationary masses, the instantaneous observed generator, and observed time symmetry, but destroy the pointwise exponential passive lower bound. It does NOT show that every perturbation does so. It rules out a uniform exponential lower bound for every model in any polynomial-radius unrestricted neighborhood of the old ladder.

The positive closure theorem does not require such a lower bound. It applies to the perturbed system itself, and statistical confidence is recalculated from its actual observations and responses.

## 10. Hidden dissipation: what the certificate can and cannot imply

Gamma>0 alone does not imply nonequilibrium. A reversible chain can have heterogeneous aggregate rates within a label and therefore positive Gamma. Conversely, Gamma=0 does not imply microscopic equilibrium: an invisible dissipative component can remain.

For a bounded real observable f, center its range so |f|<=M_f, and let

    C_f(t)=<f,exp(tQ)f>_pi,
    delta_f(t)=C_f(0)-C_f(t)-chi_f(t).

With K=(Q-Q*)/2,

    delta_f(t)=int_0^t <Kf,exp(sQ)f>_pi ds,
    delta_f''(0)=(||Qf||_pi^2-<f,Q^2f>_pi)/2.  (10.1)

For the ordinary all-even time-reversal convention, define stationary fluxes F_ij=pi_i q_ij and entropy production

    sigma=sum_{i<j}(F_ij-F_ji)log(F_ij/F_ji).

An absent positive reverse flux makes sigma infinite. For finite sigma, current conservation and Cauchy-Schwarz imply

    |<Kf,g>_pi| <= M_f sqrt(sigma E(g)),
    E(g)=-<g,Qg>_pi.

Indeed, the current form is (1/2)sum_{i<j}J_ij(f_i+f_j)(g_i-g_j),

    sum J_ij^2/(F_ij+F_ji) <= sigma/2,
    sum (F_ij+F_ji)(g_i-g_j)^2=2E(g).

Since exit rates of Q and Q* are <=Lambda, ||Q||_{2,pi}<=2Lambda. Also E(Qf)<=2Lambda||Qf||^2<=8Lambda^3 M_f^2. Thus

    sigma >= |delta_f''(0)|^2/(8 Lambda^3 M_f^4). (10.2)

For a balanced binary f, let lambda_obs=-C_f'(0),

    d_f=||(I-P)Qf||^2=f_labels^T Gamma f_labels,
    k_f=C_f''(0)-lambda_obs^2.

Then

    sigma >= (d_f-k_f)^2/(32 Lambda^3).          (10.3)

For a passive-equivalent reverse-lumpable system with reversible two-state observed chain, k_f=0. The active certificate then gives an architecture-independent positive dissipation floor for every hidden realization matching the full specified observation/intervention interface. It does not give such a floor from the passive path alone, which has a reversible two-state realization.

For general f one can use the finite-time response bound obtained by integrating the current inequality:

    |delta_f(t)|^2 <= (M_f^2 sigma t Var_pi(f))/2.

This inequality and response-based dissipation inference have substantial prior literature. They are not the principal novelty claim.

## 11. Scope of mathematical and computational evidence

The supplied verifier checks 24 rational nonreversible generators with nonuniform stationary laws; 10 relatively open passive-equivalent fiber examples; 6 genuinely strongly lumpable lifts; one exact four-state passive-equivalence witness; and shortcut algebra for r=1,...,8. The exact response-completion and finite-amplitude extraction identities are checked separately, using different expressions. There are 838 counted exact rational checks and 14 separately labelled floating diagnostics in the executed run.

No physical experiments were performed. The polynomial sample theorem is proved analytically; the large budget printed by protocol.py is not a claim that those samples have been acquired. Floating matrix exponentials are diagnostic only, not interval-certified. The exact four-state rational model and the general proofs do not rely on them.

The general results above do not import any claimed 2026 theorem from Astra or openai/math. Repository searches were selective; absence of a lexical search match is not evidence of novelty. The prior observation-ladder file is imported only for the scoped old-family comparison in Section 9 and the application of (8.3).

## 12. Prior-art and dependency boundary

1. Baiesi, Maes and Wynants, “Nonequilibrium linear response for Markov dynamics, I: jump processes and overdamped diffusions,” arXiv:0909.5306; and Baiesi, Boksenbojm, Maes and Wynants, “II: Inertial Dynamics,” arXiv:0912.0694. These establish the nonequilibrium response framework and its kinetic contribution. Formula (2.1) is derived explicitly above from that elementary finite-state mechanism.
2. Dembo and Deuschel, “Markovian perturbation, response and fluctuation dissipation theorem,” arXiv:0710.4394 (revised 2010). Response depends on the implementation of the perturbation; two different generic perturbations are studied. The mere kinetic-access distinction is therefore not claimed new.
3. Strong/weak lumpability and invariant subspace characterizations are classical. See also Feret et al., “Lumpability abstractions of rule-based systems,” arXiv:1011.0496, and Cardelli et al., “Lumpability for Uncertain Continuous-Time Markov Chains,” QEST 2021. The novelty candidate is not the aggregate-rate criterion itself.
4. Hilder and Sharma, “Quantitative coarse-graining of Markov chains,” arXiv:2201.10256; Katsoulakis and Plechac, “Information-theoretic tools for parametrized coarse-graining of non-equilibrium extended systems,” arXiv:1304.7700; Harmandaris et al., arXiv:1508.00289. Quantitative coarse-graining and path-space relative entropy predate this result.
5. Engbring et al., “A Nonlinear Fluctuation-Dissipation Test for Markovian Systems,” Physical Review X 13, 021034 (2023). Response-based tests of Markovian models are established. The present zero criterion concerns strong controlled autonomy and can be nonzero even when the unforced stationary observation is exactly Markovian.
6. Podhaisky et al., “Reliability of a nonlinear fluctuation-dissipation relation as a test of Markovianity,” Physical Review E 113, 044130 (23 April 2026). Finite-data uncertainty and field amplitude are substantive issues; they are not new concerns introduced here.

Historical priority for the specific complete acquisition-to-controlled-prediction theorem is not settled by these selective comparisons. No external scientific validation is claimed.

## 13. Remaining obligations and limitations

The most important remaining practical problem is acquiring or physically justifying the intervention's kinetic action. Merely observing energy differences, stationary populations, or local detailed-balance ratios cannot do this: the source-clock theorem gives a counterexample.

The result does not recover arbitrary hidden dynamics from Gamma, does not certify unbounded-horizon path accuracy for a fixed nonzero residual, does not eliminate rate/mixing/rare-visible-label/sensor conditioning costs, and does not prove that a particular physical device satisfies the finite-state and calibration assumptions. The sample upper bounds are conservative and noncompetitive constants may matter experimentally. Optimal finite-field schedules and tight minimax accuracy dependence remain unresolved.

Within the exact access contract, however, the mathematical obstruction is removed: unknown hidden dimension and passive return-word depth do not prevent acquiring a robust positive closure certificate, and that certificate controls all compatible future feedback experiments on the stated horizon.
