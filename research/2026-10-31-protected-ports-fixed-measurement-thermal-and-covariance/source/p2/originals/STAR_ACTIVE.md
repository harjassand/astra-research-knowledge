# STAR: active force, rectified charge response, and supplied local gates

Working derivation complementary to the root STAR representation calculation. This note does not claim a qualified device, a full gauge reset, or an arbitrary-energy robust bosonic gate. The original neutral-block files are unchanged.

## 1. What the prior architecture already supplies

The four-spin STAR is the SAGE geometry of Foulk, Hoffman, Laubscher and Das Sarma, *Singlet-only Always-on Gapless Exchange Qubits with Baseband Control*, arXiv:2501.18589, DOI 10.1103/j1hn-k5m8. Its center is site 1 and its leaves are sites 2, 3 and 4. In one standard spin-singlet basis the exchange Hamiltonian is

\[
 H_q={J_{14}\over4}(\sqrt3X+Z)
      -{J_{13}\over4}(\sqrt3X-Z)-{J_{12}\over2}Z.
\]

Equal exchanges therefore produce a degenerate logical doublet. SAGE supplies baseband rotations through unequal exchanges and a perturbative interblock-exchange entangler. The original paper gives a representative 785 ns interblock gate at J0=20 MHz and Jc=4 MHz, about 99.8% intrinsic fidelity, and four local gates in its complete CNOT construction. Those are results in its stated exchange and quasistatic-noise model, not an arbitrary-memory bound. Its spin-blockade readout is explicitly restricted to an unleaked qubit. Initialization uses spin relaxation or cold-electron injection from a reservoir.

The root construction adds a different question: if a physical resonator shifts the central potential equally relative to all three leaves, can the entire **idle Hubbard response** be logical-scalar, while symmetry-breaking modulation activates a useful force? Exact S3 symmetry is stronger than the exchange-order cancellation. On the standard-isotypic component, an invariant Hamiltonian has the form I_L tensor H_gauge. The root representation calculation supplies that statement; it must not be re-described as a new SAGE encoding.

The active gate still requires the relevant charge gauge to be qualified. One-edge hopping is not generally Z_L tensor a scalar on all charge-gauge states. It can couple different charge copies and other S3 irreducible sectors. The source calculation treats gauge renewal separately.

Primary source: https://arxiv.org/abs/2501.18589

## 2. Microscopic model and the active low-energy axis

Let

\[
 H=U\sum_i n_{i\uparrow}n_{i\downarrow}
   +x(n_1-1)
   -\sum_{j=2}^4 t_{1j}\sum_\sigma
       (c^\dagger_{1\sigma}c_{j\sigma}+\mathrm{h.c.}),
 \quad |x|<U.
\]

All particles and both spins are retained. Set t13=t14=q and t12=p. The outer transposition 3↔4 is preserved even when p differs from q. In the isolated low-energy singlet doublet its two parities are the fixed logical Z axis. Thus a single-edge modulation does not acquire an uncontrolled transverse logical axis within this doublet merely because its charge dressing changes. That statement does not eliminate transitions out of the doublet.

At exchange order,

\[
 J_j(x)={4t_j^2U\over U^2-x^2},\qquad
 H_{\rm eff}=-\sum_jJ_j(x)P_s^{1j}.
\]

Write e=epsilon0/U, s=v/U, Q=a+a†, F(e)=1/(1-e²), and modulate

\[
 t_{12}^2(t)=t^2+b\cos\omega_dt,
 \qquad t_{13}=t_{14}=t,
 \qquad x=\epsilon_0+vQ.
\]

The modulation parameter b has units of energy squared. It is called `a` in some root calculations; here b avoids confusion with the bosonic annihilation operator. An exact squared-hopping waveform requires

\[
 t_{12}(t)=\sqrt{t^2+b\cos\omega_dt},\qquad |b|<t^2,
\]

and hence a calibrated conversion from barrier voltage to hopping. A sinusoidal barrier voltage is not automatically this waveform.

Ignoring scalar terms, the exchange-order logical drive is

\[
 H_d=-{2b\over U}F(e+sQ)\cos\omega_dt\,Z.
\]

At a drive frequency close to the resonator frequency, the leading rotating-wave force is

\[
 H_{\rm force}=G Z(a+a^\dagger),\qquad
 G=-{b\over U}sF'(e),
 \quad F'(e)={2e\over(1-e^2)^2}.
\]

This requires nonzero central detuning. At e=0 this force vanishes. Moving toward |e|=1 increases it while reducing the charge gap and increasing nonlinear corrections.

## 3. A physically tied fourth-order on-state error

Define DeltaE=E(code0)-E(code1), continuously following the two isolated low-energy singlet branches. A fourth-order expansion in hopping gives

\[
 \Delta E=-{4(p^2-q^2)\over U}F(e)
  +{A(e)p^4+B(e)p^2q^2+C(e)q^4\over U^3}
  +O(t^6/U^5),
\]

where

\[
\begin{split}
 A(e)&={16(1+e^2)\over(1-e^2)^3},\\
 B(e)&={4(1+8e^2-e^4)\over(1-e^2)^3},\\
 C(e)&={-4(5+12e^2-e^4)\over(1-e^2)^3}.
\end{split}
\]

The identity A+B+C=0 is necessary for exact degeneracy at p=q and is satisfied. With p²=t²+b cos(omega_d t), the fourth-order difference is

\[
 \Delta E^{(4)}={ (A-C)t^2b\cos\omega_dt
                  +A b^2\cos^2\omega_dt\over U^3}.
\]

Consequently the cycle-averaged instantaneous splitting contains

\[
 \overline{\Delta E}^{(4)}={A(e)b^2\over2U^3}.
\]

The off state is exactly neutral under the qualified symmetry. The on state has a real, nonzero rectified response. Its c-number part can be calibrated as a local phase; its dependence on Q cannot be removed by naming that phase.

The logical Hamiltonian is DeltaE Z/2. Expanding the rectified term in sQ and using the rotating-wave number component of Q² gives

\[
 H_{\rm dc}\supset {\chi_{\rm on}\over2}Zn,
 \qquad \chi_{\rm on}={b^2s^2\over2U^3}A''(e),
\]

\[
 A''(e)={64(2+17e^2+5e^4)\over(1-e^2)^5}.
\]

With the alternative convention H_force=(g/2)ZQ, g=2G, this yields

\[
 \left|{\chi_{\rm on}\over g}\right|
 ={ |b|s\over4U^2}\left|{A''(e)\over F'(e)}\right|.
\]

This is the usable improvement over a generic single-curvature longitudinal source. In that source, g=J''v epsilon_d/2 and chi=J''v², so chi/g=2v/epsilon_d. Here the zero-drive logical curvature vanishes by symmetry, and the displayed on-state contribution is additionally suppressed by b/U²=modulation_depth times (t/U)². The improvement is a derived scaling law, not an independently assigned small residual. There are also off-resonant rectified linear-Q terms, higher hopping orders, and finite-frequency corrections.

The fourth-order correction to the linear force can already be substantial:

\[
 G=-{bs\over U}F'(e)
   +{bt^2s\over4U^3}(A-C)'(e)+\cdots,
\]

\[
 (A-C)'(e)={8e(43+30e^2-e^4)\over(1-e^2)^4}.
\]

At e=.4 this predicts a relative fourth-order correction of about 16.9% when t/U=.05. Root exact numerical response finds about 15.2% in its stated example. At t/U=.1 the leading exchange formula substantially overestimates the acquired force. Use the acquired microscopic G and its uncertainty, or a sufficiently weak regime with a controlled remainder. Do not use the nominal exchange formula as if it were already a calibrated pulse rate.

### Finite drive frequency is another rectification mechanism

The formula above concerns the instantaneous spectrum. At finite drive frequency the virtual denominators also depend on drive photons. Even an exact sinusoid in squared hopping therefore does not remove all second-order cycle-averaged differential exchange.

For |b|/t² small, the Fourier coefficients of the actual hopping are

\[
 t_0=t-{b^2\over16t^3}+O(b^4/t^7),\qquad
 t_{+1}=t_{-1}={b\over4t}+O(b^3/t^5).
\]

Define S(z)=1/(U+epsilon0+z)+1/(U-epsilon0+z). Second-order Floquet perturbation theory gives the additional differential quasienergy

\[
 \Delta E_{\rm dc,freq}
 =-{b^2\over8t^2}\left[S(\omega_d)+S(-\omega_d)-2S(0)\right]
 +O((b/t^2)^4t^2/U).
\]

Here hbar=1, and the expansion also requires that the relevant virtual denominators stay away from resonance. For omega_d much smaller than U-|epsilon0|,

\[
 \Delta E_{\rm dc,freq}
 =-{b^2\omega_d^2\over2t^2U^3}
 {1+3e^2\over(1-e^2)^3}+O(\omega_d^4).
\]

Its magnitude relative to the displayed instantaneous fourth-order DC term is approximately

\[
 {\omega_d^2\over t^2}\,{1+3e^2\over16(1+e^2)}.
\]

It can dominate when the bus frequency is large compared with the tunnel coupling, even while the bus remains well below the charging energy. It also produces Q-dependent corrections. A static Fourier derivative of the exact low-band energy is not yet the acquired dynamical force in the driven spin-plus-bus system. This frequency dependence must be retained in the actual effective model or bounded by a controlled time-dependent reduction.

### Direct periodic-density acquisition of the microscopic force

Within the two selected periodic singlet modes, central density remains diagonal in the outer-swap parity axis. Write its branch difference as d0(t)-d1(t)=C1 cos(omega_d t)+S1 sin(omega_d t)+.... To first order in the bus voltage, the resonant in-phase force is G=v C1/4. The branch **sum** also matters: it supplies an induced logical-scalar force f_induced=v(C1,0+C1,1)/4. A physical classical source can compensate that force or incorporate it in the intended geometry.

At leading weak hopping and modulation, the finite-frequency force is

\[
 G_{\omega}={bv\over2}\left[
 {1\over(U+\epsilon_0)^2-\omega_d^2}
 -{1\over(U-\epsilon_0)^2-\omega_d^2}\right].
\]

This follows by computing the central-density harmonic of the periodic virtual charge amplitudes sqrt(2)t_m/(U±epsilon0+m omega_d). It reduces to the static formula as omega_d tends to zero. It is not a substitute for exact response when hopping is too strong for the leading expansion.

`star_floquet_force.py` constructs the full 20-dimensional S=0 periodic propagator, selects each branch by its overlap with the corresponding instantaneous low singlet state at the initial drive phase, and integrates the periodic central-density harmonic. For t/U=.1, b/U²=.005, epsilon0/U=.4, omega_d/U=.05 and v/U=.005:

| Midpoint steps per drive period | G/U |
|---|---:|
| 512 | -1.53308343655e-5 |
| 1024 | -1.53309081962e-5 |
| 2048 | -1.53309266571e-5 |

The final change is 1.8461e-11 U. At 2048 steps, f_induced/U=-1.72636290320e-5; it differs from G at this hopping strength. The Floquet quasienergy difference is Omega/U=.000267189032. The minimum within-period overlaps with the respective instantaneous branches are .9999847917 and .9999998360; the minimum instantaneous S=0 charge gap is .599336515 U. The force is about .621% stronger than the static microscopic response at the same parameters, and substantially weaker than the leading hopping expansion.

These are convergent floating-point calculations without rounding enclosures. They select periodic dressed modes; closeness to instantaneous branches does not supply a loading ramp. There is no oscillator, damping, preparation or readout in this calculation. It is first order in v only and omits the root positive-capacitance model's counterterm proportional to v²(n1-1)²/omega_r. It therefore does not certify a complete spin-bus gate.

The periodic Hellmann--Feynman identity gives dOmega/depsilon0 as the period-averaged density difference. A separate finite-difference check, preserved in `star_floquet_curvature.py` and its result file, gives d²Omega/depsilon0² approximately .0030653163/U. Its adiabatic DC number-shift estimate is chi=v²d²Omega/depsilon0² approximately 7.66329e-8 U, or chi T/2 approximately .00392588 radians per photon per ideal loop. This is a static-detuning susceptibility of the driven module. The second-order response to a resonant quantum oscillator can differ, and is not certified by this number. It shows that the active bus response remains material even if the cold-port error is strongly filtered.

`FLOQUET_PORT.md` and `star_floquet_port.py` subsequently retain all twenty periodic modes in the weak-coupling central-electrode bath calculation. They test the full drive-assisted escape channel, in addition to the projected diagonal dephasing; their scope remains separate from a full oscillator-mediated gate.

### Derivation and executable preservation

In each outer-swap parity sector the zero-hopping spin-singlet state is nondegenerate. For R=Q_charge H0^(-1) Q_charge and hopping V,

\[
 E^{(2)}=-\langle VRV\rangle,
 \quad
 E^{(4)}=-\langle VRVRVRV\rangle
          +\langle VR^2V\rangle\langle VRV\rangle.
\]

On a STAR, all relevant four-hop paths have one doublon. Their first and last charged denominators are U±x; an intermediate charge-transfer state has denominator U. Independent leaf phase changes exclude odd powers of any edge hopping. Particle-hole symmetry makes the coefficients even in x. After bringing them over (1-e²)³ their numerators have degree at most four. Exact rational calculations at three distinct e² values therefore determine the coefficients; two extra rational points and additional (p,q) values check them.

`star_active.py` executes those rational checks without a symbolic-algebra dependency, then compares to the full N=4, S=0 Hubbard spectrum. `star_active_results.json` preserves the output. Fourth-order residuals scale as sixth order on the tested weak-hopping sequence. For e=.35, b=.3t², the exact static-cycle averaged splitting at t/U=.02 is 1.8870e-7 U, versus the fourth-order prediction 1.9138e-7 U; at t/U=.01 the values are 1.19190e-8 U and 1.19613e-8 U. Separate driven Hubbard Floquet checks retain the finite-frequency shift and double midpoint resolution twice. These are numerical checks without interval rounding enclosures; the driven calculation contains no oscillator and is not a qualification of a noisy physical gate.

## 4. Resonant cubic force and bus-energy qualification

The Q² term of the first-order modulation has no static resonant part in the near-resonant rotating frame: its components rotate at frequencies near omega_r and 3 omega_r. This does not make it absent; it produces off-resonant motion and higher-order effects.

The Q³ term has a resonant component. Since the resonant annihilation part of Q³ is 3 a n, a transition from |n> to |n-1> receives a fractional leading correction

\[
 {s^2F'''(e)\over2F'(e)}n
 ={6s^2n(1+e^2)\over(1-e^2)^2},
 \qquad F'''(e)={24e(1+e^2)\over(1-e^2)^4}.
\]

Thus increasing the bus occupation changes the force, rather than only adding an irrelevant phase. A finite occupation or tail qualification is required. A mean-energy bound can control tails and residual displacements, but is not the same assumption as a hard Fock cutoff.

Any nonzero branch-dependent final displacement has operator norm distance 2 from identity on the unrestricted oscillator Hilbert space. Exact ideal loop closure can be bus-state independent; generic finite errors cannot be uniformly small at unlimited bus energy. The preceding alternatives note gives an explicit coherent-state witness and energy-constrained replacement bounds.

## 5. The charge gap and scalar bus loading

At a fixed c-number central detuning, the zero-hopping charge energy outside the singly occupied sector is at least U-|x|. The one-particle STAR hopping matrix has eigenvalues plus/minus sqrt(sum_j |t_j|²), 0, 0 per spin. Therefore the N=4 hopping operator has norm

\[
 \|V\|=2\sqrt{\sum_j|t_j|^2}.
\]

Within S=0, interlacing with the charge block gives the conservative charge gap

\[
 \Delta_{\rm charge}\ge U-|x|-2\sqrt{\sum_j|t_j|^2}.
\]

For the modulation above, a sufficient lower bound throughout the waveform is U-|x|-2sqrt(3t²+|b|). This is a sufficient gap for the two low singlet branches, not a small-error bound on a rapidly driven pulse.

It is also not a global ground-state gap. With equal antiferromagnetic exchange, under H=-J sum Ps, the code has energy -3J/2 while an S=1 state with outer spin 3/2 has energy -2J. A spin-preserving electric gauge-cooling operation can respect the code; arbitrary thermal spin relaxation does not.

For a bosonic bus,

\[
 H_{\rm bus}=\omega_r n+v(n_1-1)Q,
\]

completing the square lowers a charged-sector threshold by as much as v²/omega_r. Occupied bus energy and the hopping norm must also be included in any spectral-window argument. An unrestricted oscillator has no global separation between all nominal spin/bus states and charge excitations.

Even when the gauge stays in its low band, the scalar idle response loads the bus:

\[
 E_{\rm idle}(Q)=-{6t^2\over U}F(e+sQ)+O(t^4/U^3).
\]

Its rotating-wave quadratic component shifts the resonator frequency by

\[
 \delta\omega_r=-{6t^2\over U}s^2F''(e),
\]

and its Q⁴ component gives an n² coefficient

\[
 -{3t^2\over2U}s^4F^{(4)}(e),\qquad
 F^{(4)}(e)={24(1+10e^2+5e^4)\over(1-e^2)^5}.
\]

The common linear force also shifts the equilibrium. These scalar loads sum over connected modules. They may be included in the acquired physical bus model when the gauge is qualified. They cannot be discarded merely because they are logical-scalar: active loop closure depends on the bus dynamics. Gauge excitations and leaked neighboring modules can alter that dynamics. Exact idle logical opacity is not a proof of arbitrary-history active-gate robustness.

## 6. Local gates from the same force and an actual classical drive

A DC exchange imbalance would add a logical photon-number shift already at exchange order. Local gates can instead use the same resonant force primitive plus a phase-controlled classical resonator drive. This is an additional physical source, not a free logical rotation. The physical one-edge modulation itself generates a scalar force. Consequently f below is the **total** scalar force; the external source must produce f minus the sum of the acquired induced scalar forces.

In the ideal harmonic rotating model, let

\[
 H=\Delta n+Q A,\qquad
 A=f I+\sum_jG_j Z_j.
\]

Here f is the total calibrated in-phase scalar drive amplitude, and each Z_j denotes the fixed logical axis selected by that module's physical edge. This expression first sets aside acquired local quasienergy terms Omega_j Z_j/2, restored below. At T=2pi/|Delta|, completion of the square gives, for positive Delta,

\[
 U(T)=\exp\left({i2\pi\over\Delta^2}A^2\right)\otimes I_{\rm bus}.
\]

This identity holds on arbitrary bus/reference states under the ideal Hamiltonian. It supplies both operation types:

| Operation | Settings | Logical action, apart from a scalar |
|---|---|---|
| Entangler | Two modules, G1=G2=G, f=0, Delta=4|G| | exp(i pi Z1 Z2/4) |
| Local phase | One module, force G, f=±G, Delta=4|G| | exp(±i pi Z/4) |

Both take

\[
 T={\pi\over2|G|}.
\]

An actual driven module also has the local term Omega Z/2. It commutes with the displayed ideal force Hamiltonian, so a one-qubit loop instead has phase

\[
 \theta={4\pi fG\over\Delta^2}-{\Omega T\over2}
 \quad(\bmod\ \pi).
\]

The source can supply the corresponding f if Omega has been acquired accurately. At the displayed Floquet point, Omega T/2 is approximately 13.69 radians; it is not negligible. Phase wrapping keeps the needed f of order G. Identical modules' local shifts can be compensated by a common drive; unequal modules need appropriately supplied local compensation. These acquisitions and corrections must be included in a complete operation. The simple table describes the Omega-compensated ideal setting.

For an arbitrary phase exp(i theta Z), use f=theta Delta²/(4pi G). Choosing different physical edges gives the nonparallel SAGE axes; finite ordinary single-qubit synthesis from two nonparallel axes therefore supplies arbitrary local operations. This uses the same force calibration and microscopic restrictions as the entangler. A phase-controlled microwave source, routing to the bus, pulse envelopes and local synthesis duration remain resources.

For the two displayed Omega-compensated settings, ||A||=2|G| and the maximum ideal coherent excursion is 2||A||/|Delta|=1. If the initial bus has mean occupation at most N, including arbitrary reference correlations, then during the ideal loop

\[
 \langle n(t)\rangle\le(\sqrt N+1)^2.
\]

If scalar-force compensation also absorbs an unremoved Omega phase, use the actual ||A|| and the bound (sqrt(N)+2||A||/|Delta|)². A source amplitude chosen without accounting for that extra excursion can invalidate the bus-energy qualification.

The root acquired example |G|=6.0080737e-6 U gives T U approximately 261447 in units hbar=1. The example |G|=1.5236283e-5 U gives T U approximately 103099. These are interaction-loop times, excluding ramps, classical-source settling, gauge/bus renewal, preparation, readout and holding. A physical conversion uses the actual qualified U/hbar. Comparing these times to SAGE or QUEX counts alone does not establish an advantage.

Finite-frequency charge corrections, nonlinear forces, rectified on-state response, bus loss and source errors must bound the difference from this ideal model. Closing the final bus trajectory does not erase information already lost into a damping channel. Repeated use needs a maintained energy qualification: small residual displacements can accumulate and invalidate a one-gate energy bound unless renewal, damping or another supplied operation controls them.

## 7. Scope of the resulting improvement

The concrete improvement is a symmetry-protected off state with a drive-selected active logical force, plus a way to obtain local gates from that same force. It removes the ordinary model's static logical curvature and logical-state-dependent idle bus loading. It does not remove gauge dependence, nonlinear bus dynamics, charge excitation, symmetry mismatch, or source requirements.

The strongest comparisons should give ordinary longitudinal gates the same acquired force, resonator spectrum, energy bound and physical source operations. SAGE remains a strong baseband comparator with no resonator requirement; QUEX supplies a distinct singlet-only charge/cavity proposal. Neither the exact STAR off-state theorem nor its gate segment count alone proves a complete physical advantage.

Primary comparisons:

- SAGE: https://arxiv.org/abs/2501.18589
- SAGE extended charge-noise study: https://arxiv.org/abs/2604.15419
- Longitudinal spin-resonator gate: https://arxiv.org/abs/1801.04858
- Sweet-spot curvature/resonator analysis: https://arxiv.org/abs/2010.01233
- QUEX: https://arxiv.org/abs/1807.10471

