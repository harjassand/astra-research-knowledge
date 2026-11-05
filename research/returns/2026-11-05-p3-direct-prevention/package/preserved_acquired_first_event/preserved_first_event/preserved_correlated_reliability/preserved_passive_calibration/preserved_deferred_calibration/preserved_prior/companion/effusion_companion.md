# Finite-temperature rate acquisition by isotropic forcing

Internal constructive companion, 2026-11-05. This is a completed mathematical construction for the stated ideal classical transport model, not an experimental demonstration, not a general law of materials failure, and not an established novelty claim. It is deliberately narrower than generic force spectroscopy.

## 1. The physical model and actually supplied ports

A maintained dilute classical reservoir injects particles into an unknown finite or countable collection of straight, separable, collisionless guides. Guide j has direction v_j in S^2, coordinate x in [0,L], particle mass m, and an unknown nonnegative longitudinal potential U_j(x). A successful transmission is the event of interest. The guide ends at an absorbing detector. Failed particles are removed or rethermalized; they never affect later injected particles. The source is a stationary Poisson thermal-flux source. The individual incident rates nu_j and their sum can be measured upstream or bounded by the injector, but no positive lower bound on any nu_j is needed.

For the equilibrium Maxwell distribution, incident flux is weighted by positive normal velocity: density proportional to v exp(-beta m v^2/2)dv. With E=mv^2/2, the incident longitudinal energy is exactly Exp(beta). This is a flux distribution, not the unweighted bulk kinetic-energy distribution. Thus classical transmission across a fixed conservative guide occurs exactly when E exceeds the maximum longitudinal potential. No small-temperature or Kramers approximation is used.

The physical controls are (i) a calibrated force vector f with norm at most F, contributing potential -x f.v_j, (ii) an input shutter, and (iii) a clearing/reset port that removes every in-flight particle between force blocks. The only inference output needed is a count of transmitted particles. Directions and channel identities need not be measured. Finite mouth size, imperfect field geometry, missed events, collisions and clearing failure need explicit bounds; they are not inferred from zero exit observations.

The global geometry promise is a thin barrier shell. Put I=[ell-w,ell+w] subset [0,L]. Every U_j is zero outside I and has maximum B_j>=B_min, with B_min>F L. More generally it is enough to have a certified height margin greater than F L between the global maximum and every point outside I. This is a construction/geometric premise about *every* route to the detector. It cannot be established by seeing only a few successful paths.

An electric force on charged classical particles, or a mechanically imposed generalized force on a calibrated guided coordinate, is one realization. The reservoir and guide mouths must be shielded or maintained so that the incoming thermal flux is independent of f. Otherwise a bounded multiplicative change in nu_j must be included in the error budget. Collisions, quantum tunnelling and inelastic wall scattering are outside this ideal model unless separately bounded.

## 2. Exact rate law with saddle motion already included

Write h=f.v_j and

    B_j(f)=max_{0<=x<=L} [U_j(x)-h x].

Because B_j>F L, a maximizing point stays in I and B_j(f)>0. Therefore

    |B_j(f)-B_j+ell f.v_j| <= F w.

This follows directly by taking maxima of functions differing by -h(x-ell), whose magnitude on I is at most Fw. It allows arbitrary movement or exchange of the maximizing saddle within I; no Hessian or prefactor derivative has been assumed small.

Poisson thinning gives the exact completed-transmission rate

    k_j(f)=nu_j exp[-beta B_j(f)],
    a_j=k_j(0)=nu_j exp(-beta B_j),

and hence

    exp(-beta Fw) a_j exp(beta ell f.v_j)
      <= k_j(f) <=
    exp(beta Fw) a_j exp(beta ell f.v_j).

For w=0 this is an exact Bell-form response derived from finite-temperature ballistic mechanics. It is not an assumed generic Bell law. Unknown barrier heights, incident fluxes and channel count remain unrestricted except for finite total flux.

## 3. Isotropic intervention and total-rate inference

Define s=beta F ell and

    Gamma_d(s)=E_{u uniform on S^(d-1)} exp(s u_1)
              = 0F1(;d/2;s^2/4).

In three dimensions Gamma_3(s)=sinh(s)/s, with Gamma_3(0)=1. Averaging f=F u over all directions gives, for Lambda=sum_j a_j,

    exp(-beta Fw) Gamma_3(s) Lambda
      <= mean_u sum_j k_j(Fu) <=
    exp(beta Fw) Gamma_3(s) Lambda.

Thus the *total* baseline hazard is inferred from pooled accelerated counts. No channel catalogue, transition-state search, per-channel prefactor estimate, observed direction, or minimum attempt frequency is required. If channels share an exact radius and the ideal physics holds, all hidden channels are accelerated by the same averaged factor.

The baseline output process in stationarity is Poisson of intensity Lambda, so the waiting time from a stationary observation start to the next output has mean 1/Lambda. For an initially empty apparatus whose source turns on at time zero, let M_empty be the first detection mean. There is also a uniform exact initial-state correction:

    1/Lambda <= M_empty <= 1/Lambda + L sqrt(pi m beta/2).

Indeed the first successful launch time is exponential of mean 1/Lambda; the first detected arrival is no earlier than that launch, and no later than that launch plus its own transit delay. Conditional on transmission, the excess energy above the maximum is again Exp(beta), and transit time is at most L sqrt[m/(2 excess)]. Its mean is bounded by L sqrt(pi m beta/2). Thus the cold initially empty mean has a completely paid additive transit correction without an equilibrium or exponential-exit assumption for the full apparatus. The finite protocol below also starts each force block empty.

## 4. Explicit finite force set, with no rapid switching

Choose a spherical quadrature exact on polynomials of degree t. A constructive choice in dimension three is Gauss-Legendre quadrature in z=cos(theta), with n_z=ceil((t+1)/2) nodes, crossed with n_phi=t+1 equally spaced azimuths. The resulting positive weights sum to one and there are q=n_z*n_phi force settings.

Taylor truncation proves, uniformly in every unknown v in S^2,

    |sum_r w_r exp(s u_r.v)-Gamma_3(s)|
       <= 2 exp(s) s^(t+1)/(t+1)!.

Choose t=O(s+log(1/eta_q)) so the right side is at most eta_q. Since Gamma>=1 this is also a relative error bound. For eta_q<=1/2, one may use log-quadrature error alpha_q=2 eta_q. Thus q=O((s+log(1/eta_q))^2), with positive known dwell weights. No infinite switching or unknown angular distribution enters the construction.

Inject at force r for actual source-open exposure T w_r. The force is held constant throughout the subsequent transit/flush period. Digital timing and force-vector errors can be included as multiplicative calibration errors. The force field need not be rapidly rotated while a particle is in flight.

## 5. Finite transit time without a saddle-curvature assumption

A near-threshold trajectory can take arbitrarily long, so using an uncharged infinite settling time would be invalid. Choose an energy margin zeta>0. If E>=B_j(f)+zeta, kinetic energy is at least zeta everywhere and transit time is at most

    tau_f = L sqrt(m/(2 zeta)).

Among all transmitted energies, the fraction with this margin is exactly exp(-beta zeta). After an injection block of duration T_r, close the source shutter and keep f unchanged for tau_f, continuing to count. Then clear all remaining particles before the next force block. The count from that block is Poisson with mean between

    exp(-beta zeta) T_r sum_j k_j(f_r)

and

    T_r sum_j k_j(f_r).

The delayed near-threshold events contribute only a bounded multiplicative detection deficit. This statement does not need an upper bound on their individual delays. Clearing failure would permit later force blocks to pump or transmit leftover particles and must be bounded by the actual reset operation.

## 6. Complete statistical interval

Let a detector detect every transmitted particle independently with probability in [d_-,d_+], uniformly over paths and energies. Take d_+=1 when convenient. Suppose other calibrated log-rate effects are at most alpha_c. For independent force blocks totaling source-open time T, the pooled count N is Poisson with unknown mean mu satisfying

    A_- T Lambda <= mu <= A_+ T Lambda,

where

    A_- = d_- Gamma_3(s) exp[-beta Fw-alpha_q-beta zeta-alpha_c],
    A_+ = d_+ Gamma_3(s) exp[ beta Fw+alpha_q+alpha_c].

Take any exact (1-delta) Poisson mean interval [mu_L(N),mu_U(N)], for example Garwood's chi-square interval. Then

    Lambda in [mu_L/(A_+T), mu_U/(A_-T)],
    M=1/Lambda in [A_-T/mu_U, A_+T/mu_L].

The upper lifetime endpoint is infinite when mu_L=0. For zero counts a one-sided statement is

    Lambda <= log(1/delta)/(A_-T),
    M >= A_-T/log(1/delta).

The same bound applies to the *total unseen-channel rate* after freezing a discovered channel list and using fresh validation exposure, provided a detector can distinguish novel marks. No union bound over unknown channels is needed. For total-hazard inference no channel labels are needed at all.

To attain relative interval width 1+epsilon, the ratio A_+/A_- itself must be at most 1+O(epsilon); statistical exposure cannot remove an inaccurate geometric or physical extrapolation. Expected accelerated counts of order epsilon^-2 log(1/delta) are sufficient, using doubling exposure or a valid confidence sequence when Lambda is initially unknown.

## 7. Full cost and remaining exponential burden

Let n=Theta(epsilon^-2 log(1/delta)), assuming the systematic error budget is small enough. The characteristic required source-open time is

    T = Theta(n/[Gamma_3(s) Lambda]).

It is an acceleration by a proved factor, not an unconditional lifetime-free algorithm. For a single barrier B and attempt rate nu,

    T ~ (2s n/nu) exp[beta(B-F ell)]

at large s, up to declared error factors. Unknown barriers substantially above the allowed work, or an extremely small incident prefactor, retain an actual exposure cost. The restriction B_min>FL prevents quietly driving barriers negative, where the exponential response clips at the incident flux.

The serial physical time per complete design is

    T_wall <= T + q(tau_f + tau_clear + tau_slew),

where tau_clear and tau_slew are bounds from actual hardware. If destructive specimens are used instead of a reusable flux source, their preparation/reset time and number must be added; this protocol does not supply those preparations for free. The source also pays approximately nu_total*T incident particles, not just n transmitted ones. Particle kinetic-energy supply, field holding power, switching energy, detector dead time and background counts must be charged if an engineering cost is claimed. Known additive background can be handled by a joint count interval, but no relative bound is possible when uncalibrated background dominates the signal.

Calibration s=beta F ell requires absolute error O(epsilon), because |d log Gamma/ds|<=1. Consequently relative precision of F, ell, beta is O(epsilon/s). The shell-width tolerance obeys beta Fw=O(epsilon), i.e. w/ell=O(epsilon/s). Strong acceleration demands proportionally tighter geometric and thermometric control.

That thermometry statement concerns uncertainty in Gamma when the *same fixed bath* defines both the baseline and forced rates. Actual temperature drift changes the unknown barrier rates and is a separate error. No finite bound on individual barrier heights was assumed. If nu_total is known and the individual nu_j remain fixed, an exact aggregate correction is available. Write lambda_o=sum nu_j exp(-beta_o B_j), r=beta_target/beta_o. Jensen's inequality for Z=exp(-beta_o B) under weights nu_j/nu_total gives, when r>=1,

    nu_total^(1-r) lambda_o^r <= lambda_target <= lambda_o,

and when 0<r<=1,

    lambda_o <= lambda_target <= nu_total^(1-r) lambda_o^r.

Thus maintaining relative rate precision requires relative temperature stability O(epsilon/log(nu_total/lambda_o)), not just O(epsilon/s). This is a logarithmic-rarity metrology cost. For a natural fixed-density Maxwell reservoir, the known common beta^(-1/2) flux factor must first be divided out; if flux changes are not controlled or bounded, this correction does not apply.

Numerically Gamma_3(10)=1101.32328747, Gamma_3(20)=12129129.8852, Gamma_3(30)=178107909692. A conservative Taylor remainder <=0.01 uses respectively 722, 2738, 6050 explicit quadrature settings. These are mathematical values, not experimental performance predictions.

## 8. Exact minimax statement and its boundary

In the exact sharp-shell rate family, among all distributions of *static* forces of magnitude at most F, the best worst-direction acceleration is exactly Gamma_d(s). Achievability is isotropic forcing. For any other design pi,

    average_v E_{f~pi} exp(beta ell f.v)
        = E_{f~pi} Gamma_d(beta ell |f|)
        <= Gamma_d(s),

so some hidden direction has acceleration no greater than Gamma_d(s). This proves optimality for arbitrary static-force mixtures, including unequal dwell allocations. With output-only observations, a single hidden Poisson channel supplies the corresponding no-event testing lower bound: total exposure T cannot uniformly exclude an unseen baseline rate a at confidence 1-delta until T is of order log(1/delta)/(a Gamma_d(s)).

Do not extend this exact minimax statement to arbitrary time-dependent forcing. Resonant or repeated forcing can pump additional work. A separate energy-budget comparison is available: if each injected particle receives at most W positive longitudinal work before crossing, then successful particles must have initial energy E>=B_j-W, so channel acceleration is at most exp(beta W), as long as B_j>W. At W=F ell and a thin shell, isotropic forcing gains exp(s)/(2s), within a factor approximately 2s of this broader work-limited upper bound. Removing the per-attempt work limit removes that comparison.

## 9. Relation to strong prior work

Temperature-accelerated dynamics already discovers unknown exits, extrapolates them using transition-state/Arrhenius machinery and uses a minimum prefactor in its stopping rule (Sorensen-Voter 2000; Aristoff-Lelievre 2014). TAMMBER already combines accelerated discovery, missing-rate uncertainty, Markov-model residence and adaptive resource allocation (Swinburne-Perez 2018). Hyperdynamics already constructs basin bias potentials that accelerate exits while preserving rate information (Voter 1997). Calling any of those ideas new would be incorrect.

The candidate addition here is the finite geometric force operation: all unknown shell channels become rate-equivalent under an explicit positive directional design, with exact finite-temperature derivation, finite flight/clearing cost and a static-design minimax law. It uses only a vector force rather than arbitrary configuration-dependent bias, and no individual barrier or prefactor needs to be acquired. It is not a proved global novelty claim; the literature search was targeted and incomplete. Ordinary direct counting, calibrated unidirectional force spectroscopy when a channel direction is already known, and temperature acceleration are the required experimental baselines. A known direction can use all force along that direction and achieve e^s, beating the spherical gain by roughly 2s; direction ignorance is a paid resource restriction.

Generic force spectroscopy does not satisfy the shell mechanics. Dudko-Hummer-Szabo explicitly show why generic kinetic extrapolation beyond Bell's formula needs attention to barrier shape and multidimensional effects. The present theorem avoids that issue only by constructing collisionless guides with a known localization envelope; it does not resolve arbitrary materials, ageing, hidden chemical states, common-cause device failures, or quantum tunnelling.

## 10. Primary sources consulted

- B. Cleuren, C. Van den Broeck, R. Kawai, *Fluctuation theorem for the effusion of an ideal gas*, Phys. Rev. E 74, 021117 (2006), DOI 10.1103/PhysRevE.74.021117, https://arxiv.org/abs/cond-mat/0606141 . Microscopic ideal-gas/Poisson effusion machinery; not the proposed force protocol.
- A. F. Voter, *Hyperdynamics: Accelerated Molecular Dynamics of Infrequent Events*, Phys. Rev. Lett. 78, 3908 (1997), DOI 10.1103/PhysRevLett.78.3908.
- D. Aristoff, T. Lelievre, *Mathematical Analysis of Temperature Accelerated Dynamics*, Multiscale Model. Simul. 12 (2014), DOI 10.1137/130923063, https://arxiv.org/abs/1305.6569 .
- T. D. Swinburne, D. Perez, *Self-optimized construction of transition rate matrices from accelerated atomistic simulations with Bayesian uncertainty quantification*, Phys. Rev. Materials 2, 053802 (2018), DOI 10.1103/PhysRevMaterials.2.053802, https://arxiv.org/abs/1803.05273 .
- O. K. Dudko, G. Hummer, A. Szabo, *Intrinsic Rates and Activation Free Energies from Single-Molecule Pulling Experiments*, Phys. Rev. Lett. 96, 108101 (2006), DOI 10.1103/PhysRevLett.96.108101; and *Theory, analysis, and interpretation of single-molecule force spectroscopy experiments*, PNAS 105, 15755-15760 (2008), DOI 10.1073/pnas.0806085105.
- Astra fixed P2 source, component calibration: https://github.com/harjassand/astra-research-knowledge/blob/5cfc803599d9f95cfa0a55896fb580e77567e162/research/returns/2026-11-05-p2-first-failure/component-calibration.md . This construction can supply accelerated local-rate acquisition in an engineered class; it does not itself infer P2 independence or topology.
