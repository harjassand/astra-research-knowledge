# Primary-source gate: one-port response of a chemically biased Markov ring

## Finding

At the level of an ideal calibrated port, a negative dissipative response is already a direct measurement of work delivered by the system: for a state energy \(E_i(h)=-h f_i\), the protocol work into the system is
\[
  \dot W_{\rm on}(t)=-\dot h(t)\,\langle f\rangle_t.
\]
Thus, with a sinusoidal open-loop drive and the convention \(h(t)=\Re(h_\omega e^{i\omega t})\), an observed conjugate response \(\delta\langle f\rangle=\Re[\chi_{fh}(\omega)h_\omega e^{i\omega t}]\) gives
\[
  \overline{\dot W}_{\rm on}=-\frac{\omega |h_\omega|^2}{2}\,\Im\chi_{fh}(\omega).
\]
Positive \(\Im\chi_{fh}\) therefore certifies output at this port; no hidden-state labels or fitted generator are needed for that **port-work** claim if \(h\), \(f\), and their calibration are trusted. It does not identify the chemical source or establish net efficiency. Those require independent fuel/affinity bookkeeping and actuator/load losses.

Do not substitute generic FDT violation or negative differential mobility for this sign test. FDT violation is a correlation/response mismatch, and negative differential mobility is a negative slope of a steady current versus bias; neither by itself fixes the sign of cycle work at the proposed energy port.

## Exact check in the proposed fixed-affinity load class

Take an \(N\)-state ring \(i\to i+1\) (clockwise) with baseline clockwise/counterclockwise rates \(k_+,k_->0\), and column-generator convention \(q_{ij}\) means source \(j\to i\). Set
\[
q_{ij}(h)=q_{ij}(0)\exp[\beta h(f_i-f_j)/2],\qquad E_i(h)=-h f_i.
\]
Every rate is finite and positive for finite \(h\), and the cycle affinity is fixed: \(\mathcal A=N\log(k_+/k_-)\), since all conservative increments telescope. The zero-field stationary distribution is uniform. For a real Fourier mode \(f_j=\cos(\theta j)\), \(\theta=2\pi m/N\), define
\[
A=(k_++k_-)(1-\cos\theta),\qquad D=(k_--k_+)\sin\theta.
\]
Linearizing the master equation at \(h=0\), the source is \((\partial_h L)p_{\rm ss}=\beta A f/N\); the two Fourier eigenvalues of \(L\) are \(-A\pm iD\). Direct resolvent evaluation gives
\[
\chi_{fh}(\omega)=\frac{\beta A}{4}\left[\frac{1}{A+i(\omega-D)}+\frac{1}{A+i(\omega+D)}\right],
\]
and hence
\[
\Im\chi_{fh}(\omega)=-\frac{\beta A\omega}{2}
 \frac{A^2+\omega^2-D^2}
 {[A^2+(\omega-D)^2][A^2+(\omega+D)^2]}.
\]
So this exact model has a negative-work band precisely when \(D^2>A^2+\omega^2\). It is impossible for the first Fourier mode of a 3- or 4-state ring under this symmetric load rule (the maximal \(|D|/A\) is respectively \(1/\sqrt3\) or \(1\)); it is possible for a sufficiently biased ring with at least five states. Example in rate units: \(N=5\), \(m=1\), \(k_+=9\), \(k_-=1\), \(\omega=1\) gives \(A\simeq6.910\), \(|D|\simeq7.608\), and \(\Im\chi\simeq2.84\times10^{-3}\,\beta\) (for the unnormalized cosine observable above). This is a strict linear-response witness. Since the rates and periodic stationary solution are analytic near zero amplitude, strict negativity persists for a sufficiently small but nonzero finite sinusoidal amplitude; it is not an infinite-time reset construction. The actual finite-amplitude work must still be evaluated directly from the periodic solution.

For this homogeneous ring, the baseline cycle current is \(J=(k_+-k_-)/N\), so fuel power under local detailed balance is \(T\mathcal A J=T(k_+-k_-)\log(k_+/k_-)\). The example consumes about \(17.58\,k_BT\) per unit time at baseline. Its small-signal output scales as \(|h_\omega|^2\) and is tiny near zero amplitude; a negative response is not an efficiency claim.

## Closest primary sources and exact scope

1. Aaron Beyen, Francesco Casini, and Christian Maes, [“A Rayleigh criterion for mechanical instability: inducing activity by chemo-mechanical coupling,” arXiv:2605.06543v2 (2026)](https://arxiv.org/abs/2605.06543), DOI [10.1088/1742-5468/ae898f](https://doi.org/10.1088/1742-5468/ae898f). This is the closest finite-state chemical primary: a three-state driven CTMC at one temperature, cycle affinity \(\Delta\mu=3w\) (Eqs. 2–6), coupled semi-reciprocally to a slow mechanical probe. Its reduced probe friction is Eq. (11); the explicit leading-order \(\nu(x)\) is Eqs. (20)–(24), where a frenetic term can overpower positive entropic friction. The derivation assumes probe/chemistry time-scale separation and weak coupling (\(\lambda\ll1\)); they compare reduced and full simulations in Fig. 5 and show nonlinear velocity saturation. Crucial mismatch: the chemical transition *reactivities* depend on probe position (Eqs. 7, 14, 17), and the probe is a dynamical coordinate, not a prescribed one-field drive/load port. They establish chemical energy injection into motion, not a calibrated one-port power-harvesting device or its net fuel efficiency.

2. Ji-Hui Pei and Christian Maes, [“The induced friction on a probe moving in a nonequilibrium medium,” Phys. Rev. E 111, L032101 (2025), arXiv:2407.09989](https://arxiv.org/abs/2407.09989), DOI [10.1103/PhysRevE.111.L032101](https://doi.org/10.1103/PhysRevE.111.L032101). Eq. (10) explicitly allows a discrete-state Markov-jump medium and splits friction into a force-correlation (entropic) contribution and a sign-indefinite frenetic term. Its showcased negative-friction calculations are rotating run-and-tumble and sheared Brownian media (Secs. III–IV), not a chemical ring. This is primary support that nonequilibrium probe friction need not be positive, but it is not the target exact rate/control construction.

3. Robert Wulfert, Michael Oechsle, Thomas Speck, and Udo Seifert, [“Driven Brownian particle as a paradigm for a nonequilibrium heat bath: Effective temperature and cyclic work extraction,” Phys. Rev. E 95, 050103(R) (2017), arXiv:1705.00877](https://arxiv.org/abs/1705.00877). They couple an oscillator to a driven Brownian particle in a periodic potential and use its frequency-dependent FDR temperature as a NESS bath. Their four-stroke stiffness cycle extracts work when \(T_2/T_1>\Omega^2\) (Eq. 18), with an example efficiency about 0.071. It is an established open-loop cyclic extraction analogue, but not a chemical CTMC or a single sinusoidal conjugate port. They explicitly say the energy cost of maintaining the driven thermostat is neglected (pp. 4–5); this is a strong warning against equating load-side work with net efficiency.

4. Saar Rahav, Jordan Horowitz, and Christopher Jarzynski, [“Directed Flow in Nonadiabatic Stochastic Pumps,” Phys. Rev. Lett. 101, 140602 (2008)](https://doi.org/10.1103/PhysRevLett.101.140602). Their Eqs. (11a,b) imply the no-pumping theorem for cyclic detailed-balanced Arrhenius dynamics: with fixed barrier energies/branching fractions, cyclic well-depth changes give zero integrated excess link current (pp. 2–3). This does **not** rule out extraction from a driven chemical NESS: their theorem assumes detailed balance at every protocol value, while here \(\mathcal A\ne0\). It is a theorem about integrated probability current, not a general passivity result for measured work at a driven port. A one-parameter quasi-static loop also has no geometric excess-current area; that statement does not settle finite-frequency dissipative work.

## Decision / falsifier

The closest literature contains (i) chemical CTMC-induced negative friction and (ii) open-loop cyclic work extraction from a nonequilibrium bath, but the exact fixed-cycle-affinity, single-conservative-port condition is not the setup of those examples. The ring calculation above is a direct source-independent check that the proposed class itself admits a finite-rate, small-amplitude output witness once the ring is sufficiently large and biased. The decisive operational test is to apply sinusoidal \(h(t)\), measure calibrated \(f(t)\), and integrate \(-f\dot h\) over steady cycles. If its mean is nonnegative after controller/load calibration, the port-level harvesting claim fails for that operating point. Any efficiency claim additionally requires counted chemical cycle turnovers and affinity, including the ongoing baseline fuel burn.
