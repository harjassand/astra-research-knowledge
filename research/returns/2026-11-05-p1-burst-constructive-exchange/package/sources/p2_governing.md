# Local thermal intervention without global equilibration

## Question and status

Can a retained continuously thermal nonlinear apparatus supply a causally randomized local input when its hidden environment has not equilibrated and the input cannot be reset by an actuator? The construction prepares an approximately fair two-arm momentum intervention by classifying natural thermal fluctuations. Its ideal comparison preserves the hidden marginal and old classical reference. No response model is acquired. Direct momentum reset is simpler if physically supplied. Conditional Gaussian log-Sobolev and entropy dissipation are established ingredients; historical priority and a laboratory implementation are not claimed.

## 1. Physical class and excess preparation resource

Let S=(p,z), H=p²/(2M)+V(z), where z includes conjugate position x and all hidden variables. The well-posed baseline Markov process preserves the normalized Gibbs probability pi(dp,dz)=G_sigma(dp)pi_z(dz), sigma²=M/beta, with actual thermostat

    dx=(p/M)dt,
    dp=F(S)dt−gamma p dt+sqrt(2 gamma sigma²)dW, gamma>0.

The conservative dynamics preserves the Gibbs law and phase volume. Other thermostats may dissipate entropy relative to pi. Nonlinear interactions, nonmixing hidden variables and arbitrary hidden dimension are allowed when the process and entropy identities are well defined. Kinetic factorization is essential; arbitrary momentum-dependent interactions are not covered. Thermostat Brownian noise is not observed.

For any old classical reference R, including prior retained records, supply

    D(rho_SR || pi_S tensor rho_R) <= D_0 < infinity.        (1)

This is excess free energy plus shared information, not total thermal energy. An omniscient copy of continuous microscopic coordinates may violate the finite bound. A Gibbs start followed by a fixed Hamiltonian protocol that returns to the reference Hamiltonian gives D_0<=beta W when its work/heat accounting justifies that free-energy bound; reference/measurement information is separately priced. The operation does not infer that preparation or D_0 from a quiet trace.

With h_t=d rho_SR,t/d(pi tensor rho_R), I_p(t)=E|partial_p log h_t|², the actual thermostat gives

    −D'(t) >= gamma sigma² I_p(t).                         (2)

The conservative part vanishes by integration by parts; the local Ornstein-Uhlenbeck part contributes the displayed Dirichlet form. Use its integrated weak version for finite-entropy initial laws.

## 2. Local replacement lemma

Let C replace p by an independent G_sigma sample while leaving the joint (z,R) marginal unchanged. Disintegrating over (z,R), the conditional Gaussian log-Sobolev inequality gives

    J(t):=D(rho_SR,t || C rho_SR,t) <= (sigma²/2) I_p(t).

The p derivative of log h_t is exactly the derivative of the conditional density ratio rho(p|z,R)/G_sigma(p). Averaging its fiber inequality and combining with (2) proves

    integral_0^infinity J(t)dt <= D_0/(2 gamma).             (3)

No hidden-space coercivity, spectral gap or mixing rate is used. Global rho may stay far from pi forever.

Let T be a private independent trigger with density g and sup g<=C_g. A fixed meter duration or independent latency can be added without increasing the density cap. Entropy chain rule gives

    D(law(T,S_T,R) || law(T) C rho_SR,T)
        = integral g(t)J(t)dt <= C_g D_0/(2 gamma).

With TV(P,Q)=(1/2)||P−Q||_1,

    TV(law(T,S_T,R), law(T) C rho_SR,T)
       <= delta_th:=sqrt(C_g D_0/(4 gamma)).                (4)

This controls the full hidden/reference joint state. It is averaged over T and old history, not conditional on every realized time or rare record. Coarse timestamping or discarding T only decreases TV.

## 3. Finite trigger resource

A private independent Poisson arrival port of calibrated rate r supplies a clock. Accept its first arrival by H and otherwise report timeout. Conditional on arrival,

    g(t)=r exp(−rt)/(1−exp(−rH)), 0<=t<=H,
    C_g=r/(1−exp(−rH)), P(timeout)=exp(−rH).                 (5)

An analog detector with independent finite latency preserves the cap by convolution. All later meter and control schedules have finite duration relative to this trigger. Exact event time need not be digitally read or stored. The actual independent bounded-density timing law is a supplied physical resource; a predictable PRNG does not establish it. Clock-law discrepancy eta_clock in TV adds eta_clock to the final error.

For timeout alpha_c and thermal error delta_th, sufficient settings are

    r<=4 gamma (1−alpha_c) delta_th²/D_0,
    H=log(1/alpha_c)/r.                                    (6)

Maximum occupancy is H plus finite metrology and latency. Expected clock occupancy, including timeout, is (1−exp(−rH))/r.

The integral estimate alone does NOT justify a finite grid of point times: an integrable function can concentrate at those points. This is a proof boundary, not a no-go for every specific digital Langevin system. A digital clock needs a proved time-regularity bound or actual independent continuous dither. The preceding finite-slot energy argument does not automatically supply it.

A possible clock resource is coherent-light photon counting with finite power and efficiency, under its actual Poisson and detector contracts. For detection efficiency eta_det and carrier frequency omega, flux Phi=r/eta_det and power hbar omega Phi suffice in the ideal count model. Maximum emitted optical energy is hbar omega r H/eta_det. Dark counts, afterpulses, latency, timing correlation and leakage into the plant require calibrated bounds. A private autonomous timer with the same density/independence contract is equally suitable. This specifies and prices a finite resource; it does not certify a desired photon source from its name.

## 4. The two-arm intervention instrument

Choose a known Lipschitz a(p) in [0,1] with integral a dG_sigma=1/2. Assign A=+ with probability a(p), otherwise A=−. Both arms are used. Define

    q_+(dp)=2a(p)G_sigma(dp),
    q_−(dp)=2[1−a(p)]G_sigma(dp).                           (7)

On the ideal replaced state the exact output law is:

    A is fair and independent of (T,z,R);
    p|A is distributed as q_A independently of (T,z,R).     (8)

Thus it equals a randomized do-intervention: choose a fair arm, prepare its known local momentum law, preserve the hidden/reference marginal from the passive evolution. The real operation classifies naturally occurring momenta; it applies no momentum kick or momentum-reset actuator. Applying the same classification to (4) preserves its TV bound. Any subsequent common physical experiment, nonlinear dynamics, controller and recorded outcome is a stochastic channel and cannot increase that error. There is no future-horizon factor in this state-level comparison; actually running that future experiment still costs its actuation, observations, computation, work and occupancy.

A fully explicit partition is

    a(p)=[1+eta sin(p/sigma)]/2, 0<eta<=1.                   (9)

It has Lipschitz constant eta/(2sigma), exactly balanced arms, and

    E_q+ p= eta sigma exp(−1/2),
    E_q− p=−eta sigma exp(−1/2),
    E_q+ p²=E_q− p²=sigma².                               (10)

Likelihood ratios are bounded by 1+eta<=2. The arm's mutual information about p is at most log 2. These directed finite-amplitude thermal input ensembles are known without identifying the nonlinear response. They do not deliver free work: measurement, memory, detector reset and the stochastic clock have their own physical costs.

A single acceptance function with ideal success p_a instead prepares q=aG_sigma/p_a. If joint preselection TV error is delta, success differs from p_a by at most delta and conditional-state TV is at most delta/p_a. Proof: for any event, conditional TV is at most unconditional TV divided by the larger of its two probabilities; here one probability is p_a. Rare thermal targets pay that acceptance cost. The balanced two-arm operation avoids rejection by retaining both complementary input ensembles.

## 5. What is retained and discarded

Current fine position/momentum-estimation readings must be discarded from the claimed prepared output. They reveal p and its prelaunch history, so a fresh momentum cannot be independent of those same readings. Retain old history/reference R, the trigger record, arm A and future outputs. Fine current preparation readings are temporary instrument workspace, isolated after classification and reset at a paid cost. Retaining them requires specifying a larger ideal instrument and is a different claim.

The logical intervention time is the end of the momentum-estimation window. Finite subsequent coin evaluation, waveform loading and workspace erasure may occur while the source continues to evolve. Include those delays as the same physical channel in both real and ideal experiments. The theorem does not pretend that the output momentum is still a product state after arbitrary latency; it compares the complete delayed experiment to an ideal intervention at the stated time. Reset apparatus must not re-enter the plant except through separately priced backaction.

## 6. Finite momentum metrology from position boxes

The operation does not assume an instantaneous momentum oracle. Supply local passive-process moment bounds, uniform over the entropy ball at the start of a trial:

    E p(t)² <= P_*²,
    E |F(S_t)−gamma p(t)|² <= B_*²,
    E x(t)² <= X_*², if an unbounded position meter is used.

A bounded-angle or differential-position instrument can replace the last bound with its own range/unwrap contract. Such local bounds can be obtained without hidden dimension: if equilibrium obeys E_pi exp(c F²)<=L_F, entropy variational inequality gives E_rho F²<=(D_0+log L_F)/c. Similarly the Gaussian p factor gives P_*²=4sigma²[D_0+(log 2)/2]. A known bounded force gives a simpler B_* bound. These are additional metrology premises, not consequences of factorization alone.

Following the trigger, take two finite position means of width b>0, starting at 0 and ell>0. Let their calibrated errors have mean-absolute bias at most e_x each and independent Gaussian white-noise density nu_x. At t_*=ell+b define

    p_hat=M(Y_1−Y_0)/ell.

The noiseless finite-box estimator equals a positive normalized average of p over [0,t_*]:

    M/(ell b) integral_0^b [x(s+ell)−x(s)]ds
       = 1/(ell b) integral_0^b integral_s^(s+ell) p(u)du ds.

The SDE and Minkowski inequality give

    ||p(t)−p(s)||_L2 <= B_*|t−s|+sqrt(2gamma sigma²|t−s|).

Consequently a sufficient mean-absolute error is

    e_p = B_*t_* + sqrt(2gamma sigma²t_*)
          + 2M e_x/ell + M sqrt(2nu_x/(b ell²)).             (12)

Finite sensor response, integration, time normalization, tracking and ADC errors belong in e_x. For a positive sensor kernel with mean delay tau_m, the local velocity moment gives position RMS lag at most P_*tau_m/M; its startup transient must be cleared or bounded. Finite range overflow is separately charged. For a box mean, Markov bounds its squared magnitude by X_*²; Gaussian detector tails and a finite ADC range complete a finite failure allowance. More efficient range bounds can use supplied exponential moments.

For Lipschitz constant L_a, use the same independent coin to couple the actual arm probability a(p_hat) and ideal a(p(t_*)). Label disagreement is at most L_a e_p, plus numerical/coin error and overflow. If a mean-square metrology bound is supplied, the same argument controls squared conditional bias by conditional Jensen. The comparison uses the momentum at the END of the second box; it does not insert a hidden instantaneous measurement.

### 6.1 Native direct-port metrology

If a native meter supplies a finite average of p itself, differentiation of position is unnecessary. Let p_hat=(1/b) integral_0^b p(s) ds + detector error, and launch at b. For calibrated mean-absolute bias e_0 and independent white readout noise density nu_p,

    E|p_hat-p(b)| <= B_* b + sqrt(2 gamma sigma² b)
                       + e_0 + sqrt(nu_p/b).               (13)

This is a different supplied readout interface, not a supplied momentum reset. For example, an electrical capacitive port has charge p, capacitance M=C, conjugate flux x and voltage p/C. A resistor at the port gives gamma=1/(RC) and classical Johnson current noise sqrt(2 gamma C/beta); the rest of the network may have an arbitrary nonlinear potential energy in flux/hidden variables, subject to the factorization and force contracts. A finite voltage readout then measures the local momentum directly. Meter loading and backaction remain priced below. Classical white-noise and Gibbs descriptions are valid only within a declared frequency/temperature band; demanding shorter b outside that band is not permitted.

At fixed intervention strength eta and target label error epsilon, b=O(epsilon²/gamma) and nu_p=O(sigma² epsilon^4/gamma) suffice when the force term is subordinate and e_0=O(sigma epsilon). The two-position scheme instead requires roughly e_x=O(epsilon³) and nu_x=O(epsilon^8) after fixing dimensional parameters. Neither scheme gives arbitrary precision at fixed detector noise, fixed bandwidth or a fixed backaction floor.

### 6.2 Finite parameter and arithmetic choice

For desired mean momentum error E_m>0 in the two-position implementation, choose t_*>0 satisfying B_*t_*<=E_m/4 and sqrt(2 gamma sigma² t_*)<=E_m/4, put b=ell=t_*/2, require e_x<=ell E_m/(8M), and require nu_x<=b ell² E_m²/(32M²). Equation (12) then gives e_p<=E_m. For a direct meter, choose b satisfying its first two terms <=E_m/4 each, e_0<=E_m/4 and nu_p<=b E_m²/16. All durations and precision requirements are explicit and finite for positive error and a meter family that actually reaches these contracts.

Digitize within a finite range, charging overflow to eta_overflow. Evaluate a on this finite alphabet by a precomputed table to absolute error eta_num. A fresh uniform L-bit word implements the Bernoulli coin with probability error at most 2^(-L). Piecewise interpolation and the known Lipschitz constant give a finite table construction without an exact real-number oracle. A table with spacing delta_p has O(range/delta_p) entries; direct indexing costs O(log(range/delta_p)) bit operations plus the chosen probability precision. Table preparation, random-bit generation, comparator time, memory protection and reset are physical resources. Their latency is included after the logical intervention time.

## 7. Meter backaction and the complete one-shot error

Suppose the actual meter adds a predictable force u to the same momentum equation, with pathwise integral u(t)^2 dt <= Q² during its measurement window. The unobserved Langevin Brownian noise still has variance rate 2 gamma sigma². Assume the standard absolute-continuity/Novikov conditions. Change measure in this noise coordinate while retaining the same independent detector seeds, clock and old reference. Girsanov gives the actual-versus-passive joint-path KL bound

    D(P_meter || P_passive) <= Q²/(4 gamma sigma²),
    TV(P_meter,P_passive) <= Q/(2 sqrt(2 gamma sigma²)).     (14)

The force may depend causally on past detector readings. More generally Q² may upper-bound the actual expected action, provided the absolute-continuity and exponential-integrability conditions hold. Other disturbance coordinates require a separately established comparison, and a fixed nonzero Q imposes an error floor. A device with an unknown backaction law does not satisfy this contract by being called noninvasive.

Compare in three steps: replace the measured plant by its passive counterpart using (14); replace its finite estimate by p at the end of the window, coupling the arm coins; replace that momentum by a Gaussian independent of the contemporaneous hidden/reference state using (4). Discard temporary fine readings as specified above. Any common delayed future operation then contracts TV. With a finite ADC and coin, the resulting complete law obeys

    epsilon_one <= sqrt(C_g D_0/(4 gamma)) + L_a e_p
       + eta_num + 2^(-L) + eta_overflow + eta_clock
       + Q/(2 sqrt(2 gamma sigma²)).                       (15)

Timeout is a separately heralded event of probability alpha_c. Parameter calibration and model-discrepancy allowances, if present, add their own proved law errors; they are not absorbed invisibly. The output comparison includes arm, retained clock record, old reference, hidden state and all subsequently declared observations. The ideal intervention is inserted at the end of the passive meter window. Its hidden marginal is the passive waiting/window marginal, not the unknown marginal of a disturbance-free state at some other time.

The earlier single-arm statement also implements an externally requested arm C: accept with probability a_C(p), where a_+=a and a_-=1-a. Ideal success is 1/2, actual success differs by at most epsilon_one, and the accepted intervention is within 2 epsilon_one in TV. Failed attempts consume their actual preparation and readout occupancy. Random labeling of every trial remains the main two-arm interface; it does not freely set an arbitrary momentum value.

## 8. Reuse on one retained apparatus

Let R_j be all retained history before trial j. Define the actual joint entropy budget

    B_j >= D(rho_{S,R_j} || pi tensor rho_{R_j})
        = E_{R_j} D(rho_{S|R_j} || pi).                    (16)

This is an average over realized histories. It is not a uniform bound on every posterior. Trial j uses a private clock independent of the source conditional on R_j, with a deterministic cap C_j on its conditional density, and the finite instrument above. Conditioning on R_j, applying the local replacement proof and averaging gives the same one-shot formula with D_0 replaced by B_j. History-dependent controller policies are permitted; all their effects and records must fit the following ledger.

Passive evolution cannot increase the budget. Fresh private clock/coin randomness carries no initial source information. Carry a sampled clock variable as part of the reference from its generation: independence gives no initial increase, and every conditionally deterministic passive time leaves pi invariant. Thus recording a private trigger is not charged as source information merely because it is later correlated with the plant. For a newly retained finite report Y with at most 2^b values, exact chain rule gives

    D(rho_{S,R,Y} || pi tensor rho_{R,Y})
      = D(rho_{S,R} || pi tensor rho_R) + I(S;Y|R)
      <= preceding budget + b log 2.                     (17)

Include arm and future output bits in b. Do not double-count an arm computed entirely from an already retained report plus fresh randomness. Temporary fine preparation readings are discarded and isolated; they incur reset costs but do not enter R_j. An unbounded-precision continuously retained output path is not automatically covered by a finite information budget.

For a force u acting through the thermostatted momentum coordinate, compare the controlled joint path with the uncontrolled stationary process carrying the same fixed initial reference. At a deterministic endpoint, or an endpoint fixed by independent clock/reference randomness, Girsanov and data processing give

    D_after <= D_before + E integral u²/(4 gamma sigma²).  (18)

This assumes absolute continuity and a finite declared action. A direct entropy/Young estimate gives the conservative alternative E integral u²/(2 gamma sigma²) while retaining half of the Fisher dissipation. Fixed Hamiltonian protocols may admit a sharper beta-work accounting, but arbitrary feedback is not silently assigned beta times its mechanical work. Forces outside the supplied noise range need their own entropy bound.

Equation (18) is not a claim about a state-dependent stopping time: the uncontrolled stopped endpoint need not be Gibbs. A measurement-triggered experiment can stop applying control early and then run passively to a fixed precommitted deadline; apply (18) at that padded endpoint. A horizon selected from already retained history is allowed conditionally on that history. This distinction is essential.

A usable deterministic ledger is consequently

    B_j = D_0 + sum_{i<j} [A_i + b_i log 2],
    A_i >= E integral_trial_i u²/(4 gamma sigma²),          (19)

with all physical disturbances included in u and all extra preparation/measurement effects priced. If only the safer entropy estimate is supplied, replace 4 by 2. Conditional uniform bounds imply (19); unconditional expected action bounds also suffice for the average budget, including when control depends on the retained history.

### 8.1 Complete adaptive campaign comparison

Let A_j and I_j denote the actual and ideal trial kernels, including the same waiting policy, finite later latency, experiment and retained outcomes. I_j inserts an exact Gaussian momentum replacement and fair q-arm at the stated meter-end time. Suppose the actual input to trial j has budget B_j and the resulting one-trial error is epsilon_j. Then

    TV(A_j P_actual, I_j P_ideal)
      <= TV(A_j P_actual, I_j P_actual)
         + TV(I_j P_actual, I_j P_ideal)
      <= epsilon_j + TV(P_actual,P_ideal).

Induction gives full adaptive history/state-law TV at most sum_j epsilon_j. This orientation applies entropy bounds only to actual histories; it makes no unjustified transfer of a posterior bound to an ideal campaign. Clocks and future controls may depend on each process's own history through the same declared policy. Comparing both kernels on the actual input is the decisive quantifier.

Timeout can be included as a common heralded abort branch. A campaign with prechosen timeout budgets alpha_j has abort probability at most sum alpha_j. If one conditions on all clocks succeeding, any unconditional law comparison must also pay that conditioning factor unless success probabilities are proved equal and independent of every earlier branch. The clean contract reports the heralded abort separately.

For n rounds and fixed total path-law accuracy epsilon, allocating comparable per-round error epsilon/n gives worst-case clock occupancy proportional to

    n² [sum_j B_j] log(n/alpha_clock)/(gamma epsilon²).

If each round adds at most c entropy units, sum_j B_j <= n D_0+c n(n−1)/2. The resulting n³/n⁴ cost is real. It should not be concealed under the phrase reusable preparation. A single scalar causal estimate can be substantially cheaper than a full n-round path-law certificate.

### 8.2 A direct causal estimate without a stationary hidden ensemble

For the actual pretrial retained history H_j, let theta_j(H_j) be the ideal intervention contrast for the future bounded outcome Y_j in [0,1], using the passive waiting/window hidden marginal of that actual history and the same post-arm policy. This target is generally history-dependent. It is not the stationary-environment response. Define Z_j=2 A_j Y_j with A_j in {-1,+1}. Under the ideal fair-arm operation, its conditional mean is theta_j(H_j). For the actual operation the conditional bias beta_j obeys E|beta_j|<=4 epsilon_j. Also Z_j lies in [-2,2].

For any eta,alpha in (0,1), Markov's inequality and the bounded martingale difference inequality imply, with probability at least 1−eta−alpha,

    | n^(-1) sum Z_j − n^(-1) sum theta_j(H_j) |
      <= 4 [n^(-1) sum epsilon_j]/eta
         + sqrt(8 log(2/alpha)/n).                         (20)

Timeouts are separate heralded outcomes or are charged by their declared allowance. This inference does not require independently equilibrated specimens or a common response curve. A sharper posterior contract can improve the preparation-bias term, but an average entropy bound alone must not be mislabeled uniform conditional accuracy. For an arm-invariant future policy, ordinary continuous weighting by the known score s(p)=2a(p)−1 is a stronger statistical comparator than randomized one-bit marking; the latter earns a physical downstream arm/branch interface rather than a variance advantage for that special observable-only task.

## 9. Complete resource and initialization contract

The apparatus is retained throughout waiting and later trials. It stays connected to its physical thermostat; continuous thermal noise is not counted as an unbudgeted preparation defect because the Gibbs law is the reference. The finite resource is excess entropy/free energy and retained source information. A driven nonequilibrium steady state, unknown heating or a thermostat with uncalibrated fluctuation-dissipation parameters is a different premise.

For each trial the execution bill includes the following quantities.

| Resource | Required contract / actual bill |
| --- | --- |
| Plant and thermostat | Actual factorized kinetic Gibbs law; known sigma, gamma>0 or robust certified bounds; continuously occupied source and bath over the full waiting plus experiment deadline |
| Excess preparation | Supplied D_0 and reference-information ledger; a valid preparation/work protocol or another justified upper bound |
| Private trigger | Independent density cap C_g, timeout probability, finite detector latency and law error; maximum H and expected clock occupancy stated above |
| Readout | Local force/moment/range contracts; actual finite b, ell, bandwidth, e_x/nu_x or e_0/nu_p; sensor startup/clearing; overflow probability |
| Backaction | Measured or derived L2 force budget Q and action contribution to later entropy; a meter imprecision/backaction pair that the chosen device can realize jointly |
| Calibration | Temperature, friction, readout gains/noise, force-family bounds, clock and backaction bounds acquired at their own physical exposures and confidence; this theorem does not make those costs disappear |
| Digital control | Finite ADC range/bits, lookup or approximation table, L fresh random bits, comparator and arm-routing latency; elementary gate count and aggregate gate error |
| Temporary memory | Finite fine-readout, coin and arithmetic workspace; isolated after arm production and reset at a stated error, energy and time cost |
| Retained history | Arm plus finite future reports; b_j bits enter entropy ledger and must be protected throughout later waiting periods |
| Future experiment | Its own actuation/action, metrology, record precision, deterministic/padded deadline, computation and occupancy; common future-channel errors may be included in the ideal comparator, while target-specific implementation errors are charged |

One explicit finite reset model is an isolated two-state memory cell coupled to its own bath at inverse temperature beta_m. At energy gap Delta, let its actual total relaxation rate be at least kappa_m. Choose

    Delta >= beta_m^(-1) log(2 b_tmp/delta_reset),
    tau_reset >= kappa_m^(-1) log(2 b_tmp/delta_reset).

The excited equilibrium probability is at most delta_reset/(2 b_tmp), and relaxation from an arbitrary initial bit adds at most exp(-kappa_m tau_reset). A union bound initializes b_tmp cells to zero with error at most delta_reset. Monotonically raising the gap costs at most b_tmp Delta in work, plus the chosen switching/driver costs. Finite ramp time, decoupling, protection during computation and the rate/gap range are supplied hardware contracts. A device with maximum available gap or rate has the corresponding nonzero reset/error floor. This construction is a finite upper bound, not an assertion that Landauer's lower bound is reached at finite time.

Reset and subsequent logic must be physically isolated from the retained plant; any residual coupling enters the force/action or a separate law-error budget. Fine records cannot be erased merely by declaring them absent while allowing their sensor to feed the plant later. The same cells can be reused, so temporary workspace need not scale with total trial count, but retained historical reports and their protection do scale as declared. Recording exactly one arm bit is useful when fine analog data cannot be retained, even though full readout weighting can be statistically superior when that richer record is available.

### 9.1 No timing channel from discarded fine records

Postmeter probability evaluation, comparison, routing and reset must use a fixed precommitted deadline, or a schedule depending only on retained arm/history and fresh randomness explicitly present in the ideal operation. Pad variable-time arithmetic to its worst-case time. Discarded fine momentum/position values must not choose the next launch time, influence control waveforms, or modulate sensor coupling after erasure. Otherwise their information re-enters the plant or future outputs through an undeclared side channel, and the simple independent-momentum intervention law is no longer the proved operation.

## 10. Consequence, alternatives and boundaries

The earned operation is a local randomized-ensemble intervention with a joint-law comparison including any old reference meeting the entropy budget, acquired from natural thermal fluctuations without a supplied momentum-overwrite actuator. The hidden subsystem need not equilibrate, be identifiable, be finite in a known dimension, or have a nonzero spectral gap. The reference law and excess entropy must nevertheless exist, and local metrology/clock contracts must be available. If D_0 grows with hidden volume, that growth remains in the preparation bill.

Ordinary global equilibration is a valid competitor when a useful mixing bound exists; the present guarantee has no such factor. Ordinary Gaussian momentum reset wins when the physical apparatus actually supplies it. Andersen resampling and molecular isoconfigurational/shooting ensembles are established computational operations with direct state-rewrite access. A physical impulse randomized independently of the plant is already an unconfounded additive-force intervention; it usually prepares a different momentum ensemble and retains old momentum/hidden correlations. None of these should be described as impossible.

For an arm-invariant future measurement, bounded weighting by s(p)=2a(p)−1 is preferable to adding a random label if the fine weight can be retained: the contrast is 2 E[s(p)Y], and Rao-Blackwellization reduces variance. The actual one-bit mark is useful when it routes a subsequent physical operation or when only the finite label interface is retained. Quantizing and retaining a weight changes the reference-information and memory bill and should be paid explicitly.

The construction is not a response simulator, an inverse-dynamics identification theorem, a sampler of the equilibrium hidden ensemble, or a rare-event accelerator. Since q_a/G<=1/w_a for any mixture G=sum_a w_a q_a, a rare event's conditional enhancement is paid by the arm probability. Equal kinetic energies do not erase the thermodynamic cost of correlations with the recorded label. A continuously driven nonequilibrium apparatus needs a separately bounded entropy input; finite excess entropy at one time does not cover later unbudgeted heating.

The primitive Langevin model is an explicit physical/numerical contract. Its white-noise abstraction must be used within a validated regime. A colored-noise microscopic bath is not automatically covered by calling its long-time limit Langevin; in particular, continuous path-law TV between distinct diffusion models may be maximal. A microscopic-to-effective justification must bound the actual finite instrument/output laws, or prove an appropriate extended-state entropy-production statement. The present theorem does not silently provide that extra bath-limit result.

An explicit finite canonical-pointer realization of the position-box meter, including its joint imprecision/backaction relation and classical validity limit, is given in FINITE_POINTER_REALIZATION.md. It provides one concrete metrology architecture. The native electrical-port alternative is a separate available readout contract and must satisfy its own jointly attainable precision, loading and bandwidth law. A Hamiltonian measurement of p does not automatically disturb only p; applying the Girsanov contract requires the actual disturbance direction to be the noisy momentum coordinate.

## 11. Primary research and accepted-source placement

The following are existing machinery and close comparators, not results claimed here as newly discovered.

- Leonard Gross, "Logarithmic Sobolev Inequalities," American Journal of Mathematics 97 (1975), 1061–1083. Gaussian log-Sobolev inequality. DOI: https://doi.org/10.2307/2373688 .
- Laurent Desvillettes and Cedric Villani, "On the trend to global equilibrium in spatially inhomogeneous entropy-dissipating systems: The linear Fokker-Planck equation," Communications on Pure and Applied Mathematics 54 (2001), 1–42. Velocity entropy dissipation, local equilibria and global convergence machinery. https://onlinelibrary.wiley.com/doi/abs/10.1002/1097-0312(200101)54:1%3C1::AID-CPA1%3E3.0.CO;2-Q .
- Cedric Villani, "Hypocoercivity," arXiv:math/0609050 (2006). Degenerate kinetic diffusion and convergence to a stationary state. https://arxiv.org/abs/math/0609050 .
- Igor G. Vladimirov, "Position-momentum conditioning, relative entropy decomposition and convergence to equilibrium in stochastic Hamiltonian systems," arXiv:2312.09475 (2023). A particularly close treatment of conditional-momentum entropy for nonlinear Langevin systems. https://arxiv.org/abs/2312.09475 .
- Hans C. Andersen, "Molecular dynamics simulations at constant pressure and/or temperature," Journal of Chemical Physics 72 (1980), 2384–2393. Gaussian velocity resampling when a reset operation is supplied. https://doi.org/10.1063/1.439486 ; primary scan: https://users.wfu.edu/natalie/f23phy711/lecturenote/HCAndersen.pdf .
- Asaph Widmer-Cooper, Peter Harrowell and Heather Fynewever, "How Reproducible Are Dynamic Heterogeneities in a Supercooled Liquid?," Physical Review Letters 93 (2004), 135701. Isoconfigurational ensembles with independently randomized velocities. https://doi.org/10.1103/PhysRevLett.93.135701 .

The accepted acquired thermal-feedback simulator N1688 has a different endpoint: a future-record simulator acquired for its reciprocal thermal RC family, with its stated positive-exponential response, pulse/data precision, energy and occupancy contracts. The present operation neither reproves nor supersedes it. It constructs a local input law for an unknown nonlinear future experiment and then actually performs that experiment. Governing accepted source: https://github.com/harjassand/astra-research-knowledge/blob/626bf0fb5da19c8eb62964f0d7949bb19bc64799/research/2026-11-04-p2-acquired-thermal-feedback-simulator/source/p2/COMPLETE_VISIBLE_RESPONSE.txt .

The previous predictive-preparation theorem uses finite total energy, dissipation and private timing to suppress a deterministic hidden-state response; its finite grid construction and LTI plant assumptions are preserved. The current thermal statement uses excess relative entropy and an actual fresh Langevin port to decouple a local kinetic coordinate. They are distinct physical interfaces and neither is silently substituted for the other. Historical priority for their complete interface composition is not claimed from this bounded literature search.

