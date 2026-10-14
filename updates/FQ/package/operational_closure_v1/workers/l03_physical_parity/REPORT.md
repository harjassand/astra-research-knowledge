# Physical status of the parity-doubled renewal model

15 October 2026 (Australia/Brisbane). **Disposition: generalized detailed balance is a real equilibrium possibility when the branch is a measured odd mechanical variable; the generator by itself is only a mathematical lift. A literal erasing reset without its parity-conjugate reverse jump is incompatible with finite-temperature equilibrium.** This report is a physical-interface audit and proposed experiment. No device was built and no lab measurement was made.

## Exact stochastic statement

Let $X$ be a finite irreducible CTMC with rates $k_{xy}$ and stationary distribution $\pi$. Its stationary time-reversed rates are

\[
k^R_{xy}=\frac{\pi_y k_{yx}}{\pi_x},\qquad x\ne y.
\]

On $(x,s)$, $s\in\{+,-\}$, put $k$ on the $+$ branch, $k^R$ on the $-$ branch, and stationary mass $\mu(x,s)=\pi_x/2$. With $\theta(x,s)=(x,-s)$, every within-branch edge obeys

\[
\mu(x,+)k_{xy}=\mu(y,-)k^R_{yx},
\]

and the corresponding identity holds after swapping the branches. A same-position velocity flip is self-conjugate under $\theta$, so its rate ratio contributes zero to the path log-ratio. Equal $+\to-$ and $-\to+$ rates are a simple sufficient choice when the other transitions are paired, though the full generator must still have parity-matched escape rates and stationary weights. For the doubled within-branch chain, the escape rates match automatically: $\lambda^R_x=\sum_{y\ne x}\pi_y k_{yx}/\pi_x=\lambda_x$ by stationarity of $\pi$; symmetric same-position flips add the same rate to both branches. Once every state-changing reset/flip edge also has its parity-conjugate partner at the required rate, the endpoint and jump factors telescope and the holding-time factors cancel. The stationary log path ratio against $\theta$-reversed paths is then zero. Stationary time reversal plus a branch label therefore establishes a *formal* generalized-detailed-balance model.

It becomes an equilibrium phase-space model only if $s$ denotes an actual odd coordinate, such as the sign of a measured velocity, and the edge pairing is physically present. For a physical state $i=(q,v,\ldots)$, the equilibrium condition is

\[
\theta(q,v,\ldots)=(q,-v,\ldots),\quad
\rho_{\rm eq}(q,v,\ldots)=\rho_{\rm eq}(q,-v,\ldots),\quad
\rho_{\rm eq}(i)k_{i\to j}=\rho_{\rm eq}(\theta j)k_{\theta j\to\theta i}.
\]

Thus the physical reverse of a jump $(q,v)\to(q',v')$ starts at $(q',-v')$ and returns to $(q,-v)$. A local one-dimensional hop must be kinematically consistent with the measured velocity; its conjugate reverses the displacement and both endpoint velocities. If an edge has positive rate, this conjugate edge must have positive rate too. For one equilibrium bath and a state energy $E_i=E_{\theta i}$, local detailed balance requires

\[
\log\frac{k_{i\to j}}{k_{\theta j\to\theta i}}
=-\beta(E_j-E_i)
\]

when no particles or work are exchanged. For a channel exchanging particles with reservoir $\nu$, with $N_{a,j}-N_{a,i}$ species $a$ gained by the system, the corresponding condition is

\[
\log\frac{k^\nu_{i\to j}}{k^{\bar\nu}_{\theta j\to\theta i}}
=-\beta_\nu\left[(E_j-E_i)-\sum_a\mu_{\nu a}(N_{a,j}-N_{a,i})\right].
\]

The stationary weights of the abstract lift can be represented by $E_x=-k_BT\log\pi_x+\mathrm{const}$, equal for the $+/-$ pair. For each positive conjugate rate pair, a shared transition-state barrier and attempt prefactor can reproduce both rates because their ratio is the Boltzmann weight ratio. This is a constructive thermodynamic embedding of a finite rate network at the rate-equation level; it does not establish that a proposed geometry, velocity, jump mechanism, or reservoir realizes those rates.

## The reset constraint is decisive

If the “orientation flip at reset” is a transition \((x,+)\to(r,-)\) that changes or resets the even state, its time-reversed parity-conjugate event is \((r,+)\to(x,-)\), not the same reset. At equilibrium the channel rates must satisfy

\[
\pi_x k_{(x,+)\to(r,-)}
=\pi_r k_{(r,+)\to(x,-)}.
\]

The half factors cancel. More generally, the reverse channel must carry the appropriate reservoir/chemical-potential term in local detailed balance. A one-way reset which erases the pre-reset state and has no reverse “unreset” transition cannot be an equilibrium operation at finite energy and finite temperature. A same-position velocity flip $(q,+v)\leftrightarrow(q,-v)$ is self-conjugate, so its path-rate ratio is one. Choosing equal rates in both directions is a simple sufficient choice when the other transitions are parity matched; “the branch flip probabilities are symmetric” alone does not repair a one-way state reset.

The full microscopic bookkeeping also matters. A generator formed by summing several channel rates can look balanced even while parallel channels carry opposing chemical currents. Every channel must have its own conjugate and reservoir account. Distinct temperatures, chemical potentials, fuel/waste reservoirs, external work, or an unlogged controller can supply nonzero cycle affinity and dissipation hidden from the binary signal. In an equilibrium realization, all closed-cycle affinities vanish after reservoir exchanges are included, stationary velocity occupancy is parity symmetric pointwise, and net heat/work/chemical flux is zero. At a fixed magnetic field or other time-reversal-odd control, the comparison must also reverse that field/control; holding it fixed changes the physical reversal.

## What ordinary physical assumptions permit

There is no general physical prohibition on the parity construction. A particle with position even and velocity odd can have equilibrium phase-space probability currents: a trajectory advancing at $+v$ is reversed by one retreating at $-v$. The currents cancel under the correct phase-space reversal, even though either branch by itself can look directional. Spinney and Ford give a discrete position/velocity telegraph model: at its symmetric parameter value, the stationary probabilities for the two velocities are equal and their stated generalized detailed-balance relation pairs a right-moving jump with the velocity-reversed left-moving jump. Their asymmetric-velocity case instead has a nonzero mean entropy-production rate. This is an established equilibrium-compatible *model class*, not evidence that the present hidden branches correspond to velocity in a real apparatus.

Accordingly, the doubled chain is not “just relabeling” once all of the following are independently specified and measured: a physical even position/configuration $q$; a genuine odd velocity $v$ that reverses under time reversal and is kinematically consistent with the jumps; parity-symmetric equilibrium weights; every paired reverse transition, including reset reversals; channel-resolved local detailed balance; and no unaccounted drive or reservoir flux. Without these data, naming the duplicate index $v=\pm$ is just a choice of labels. In an overdamped description where velocity has been eliminated, the missing odd coordinate cannot be reinstated as an accounting trick.

## Why the binary renewal trace cannot decide

If the observed output is $Y=f(X)$ and discards branch, position phase, transition channel, and reset history, its dwell-time law does not determine which microscopic reversal is physical. A stationary alternating-renewal binary process can be compatible with both a parity-reversible phase-space model and an all-even driven hidden-state model. The same observed dwell distribution therefore cannot certify zero dissipation or prove the existence of physical velocity. This is an identifiability issue, not a defect in fitting the binary renewal law. Primary work on partially observed Markov networks shows why waiting-time/transition measurements can expose hidden cycles and why the correct time reversal depends on the physical state description.

An exact hidden-dissipation stress test is available for any proposed all-even realization: append an independent three-state all-even cycle $z\in\{0,1,2\}$ with clockwise rate $a$ and counterclockwise rate $b$, where $a>b>0$, and let the binary sensor ignore $z$. The binary path law is unchanged, while the added stationary entropy-production rate is $k_B(a-b)\log(a/b)>0$: each of the three edges carries net current $(a-b)/3$ and affinity $\log(a/b)$. This is an identifiability counterexample, not a proposed device. It shows why the additional observable must include the hidden phase/cycle or its energy/chemical exchange, not merely another statistic of the same binary trace.

## Decisive experiment within a declared state/channel boundary

Keep the binary sensor, but add a synchronized measurement of the actual even coordinate $q(t)$, signed velocity $v(t)$, the internal transition/reset marker, and any exchange channel available to the device. Use a high-speed position tracker plus a calibrated direction-sensitive velocity readout (for example, Doppler or two-sided transit timing); tag reset channels with a non-invasive marker where possible. First establish the stationary histogram and verify $\rho(q,v)=\rho(q,-v)$ within uncertainty. Then estimate the conditional jump hazards from measured state exposures and compare, edge by edge,

\[
\widehat J^{\theta}_{ij}
=\widehat\rho_i\widehat k_{i\to j}
-\widehat\rho_{\theta j}\widehat k_{\theta j\to\theta i}.
\]

For every equilibrium candidate edge this parity-conjugate flux difference must vanish. In particular, for each reset $(x,+)\to(r,-)$, record exposure in $(r,+)$ and test for the predicted reverse $(r,+)\to(x,-)$, with the rate fixed by the measured equilibrium weights and forward rate. If no such reverse event appears and the Poisson upper bound on its rate lies below the detailed-balance prediction, the reset-based equilibrium realization is falsified. Observing the paired event is necessary but not sufficient: measure channel-resolved heat, work, chemical exchange, and any controller power to rule out a hidden driven cycle.

In parallel, use the all-even candidate's complete hidden-state map to compute its ordinary reversed-path log likelihood. A driven cycle has

\[
\Sigma_{\rm even}(\omega)
=\log\frac{\rho(i_0)}{\rho(i_T)}
+\sum_{m}\log\frac{k_{i_m i_{m+1}}}{k_{i_{m+1}i_m}},
\]

and positive stationary mean when its cycle current and affinity are nonzero. The parity model instead tests the path against \(\theta\omega\), including position reversal, velocity sign reversal, and the reverse reset. If a passive full-state trace still leaves the fitted models overlapping, randomize a small calibrated impulse that reverses velocity while holding (q) fixed, with sham trials and measured impulse work. The parity model predicts the velocity-reversed conjugate transition/hitting-time statistics; an all-even driven cycle predicts persistence of its hidden cycle orientation. The impulse is a diagnostic perturbation, not a free operation, and its energy and disturbance must be logged.

This is decisive only relative to the declared observable state and channel boundary. No finite record can exclude an arbitrarily weak unmeasured reservoir or hidden cycle. A reported equilibrium verdict must state which physical states, reverse channels, and reservoirs were actually resolved and give rate confidence intervals; missing channels keep the verdict **UNKNOWN**.

## Costs, comparator, and limits

The strongest comparator receives the same binary record, the same position/velocity/transition data, the same calibration samples, and the same perturbation budget. Compare likelihoods for (i) the parity-conjugate equilibrium model with explicit reverse resets and (ii) the all-even renewal mechanism with its driven cycle. Charge fabrication and sensor loading, velocity/position calibration, timestamp resolution, channel tagging, independent stationary preparation, repeated velocity-reversal pulses, thermal/chemical calorimetry, controller and readout power, lost/failed records, and resets. The exact required reverse-reset rates follow the flux identity above; no hardware-specific numerical rates, power, accuracy, or scaling are claimed because the device and generator parameters were not supplied.

The principal practical risks are that resolving velocity disturbs it, the detector labels a bookkeeping branch rather than mechanical momentum, rare reverse resets evade finite sampling, and multiple physical channels are lumped into one rate. A clean binary dwell fit, a balanced aggregate generator, or a hash/verification receipt cannot resolve those risks. The main claim is therefore conditional: **equilibrium is physically possible if parity is real and all conjugate channels close; the current generator alone does not establish that condition.**

| Measurement | Parity-equilibrium realization | All-even dissipative realization |
|---|---|---|
| Binary dwell law | Matches the stipulated law | Matches the same stipulated law |
| Full resolved path | Probability matches its position-reversed, velocity-flipped path | Ordinary state-reversed path has positive mean log likelihood ratio when a driven cycle is resolved |
| Reset traffic | Each reset has its parity-conjugate reverse flux at the required rate | Reset/current asymmetry or a hidden driven channel remains measurable |
| Energy and reservoirs | No stationary net heat, work, or chemical flux | Positive cycle affinity is paid by heat, fuel, work, or another declared resource |

## Primary sources inspected

1. Ian J. Ford and Richard E. Spinney, “Entropy production from stochastic dynamics in discrete full phase space,” *Physical Review E* 86, 021127 (2012), [arXiv full text](https://arxiv.org/html/1204.4822v2), [journal DOI](https://doi.org/10.1103/PhysRevE.86.021127). Inspected the definition of the position/velocity-reversed path and its path-probability ratio (Sec. II, Eqs. 3–5); the telegraph model's position/velocity rates and stationary probabilities (Sec. III, Eqs. 13 and surrounding text); and the equilibrium conjugacy at its symmetric parameter value (lines 111–119 of the HTML). It explicitly models discrete position and velocity; it does not validate the assigned device.
2. Jann van der Meer, Benjamin Ertel, and Udo Seifert, “Thermodynamic Inference in Partially Accessible Markov Networks: A Unifying Perspective from Transition-Based Waiting Time Distributions,” *Physical Review X* 12, 031025 (2022), [journal article](https://doi.org/10.1103/PhysRevX.12.031025), [arXiv](https://arxiv.org/abs/2203.12020). Inspected abstract and popular summary: transition-based waiting-time ratios can detect hidden cycles and yield full entropy production for unicyclic networks or lower bounds for more complex networks; the paper emphasizes the correct physical time reversal. This supports the new measurement choice, not an apparatus-specific guarantee.
3. Massimiliano Esposito, “Stochastic thermodynamics under coarse graining,” *Physical Review E* 85, 041125 (2012), [journal article](https://doi.org/10.1103/PhysRevE.85.041125). Inspected abstract: when microstates inside observed mesostates remain out of equilibrium, extra entropy-balance contributions survive coarse-graining. This supports retaining channel/reservoir observables and not inferring full thermodynamics from an aggregate generator.

The rate identities and reset test above are direct derivations for the assigned construction. No novelty, physical implementation, or empirical equilibrium claim is made.
