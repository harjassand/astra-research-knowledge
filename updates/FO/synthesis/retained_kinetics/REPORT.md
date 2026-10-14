# Phase-selective structural writing with finite retention

**Disposition.** A non-melting route is mathematically possible, but an optical population contrast does not establish one. A small phase-odd excitation can select and retain a structural polarity over a finite, specified horizon if (i) the sample has two experimentally identified symmetry-related variants, (ii) phase reversal changes the *structural transition kernel* in the corresponding odd direction, and (iii) the pulse moves an existing boundary or nucleates/grows a selected variant faster than field-free reverse transitions erase it. Detailed balance permits this during a driven pulse; removal of the drive restores symmetric kinetics; for an irreducible finite chain, long-time dynamics eventually erase ensemble polarity. The missing physical control is a measured, phase-reversible retained structural kernel under matched heat and direct-field controls, not another carrier-contrast number.

Separately, the incoming physical phase-rewriting source record (`work/FM-sources/physical/RESEARCH_RECORD.md`) derives an impulsive complete-melting contrast threshold C > 0.4484916 only under its equal-mole, fixed-composition, equilibrium complete-melting energy-partition assumptions. This conditional enthalpy calculation is not an N777 result and is not a general lower bound for structural switching. A real optical ferroelectric domain-switching experiment shows that wall-mediated structural switching can be written without melting an entire domain: in freestanding BaTiO3, 391 nm light switches an upward region downward while a measured imprint selects the downward state and photoexcitation lowers the wall-motion barrier. The paper estimates only 0.25–0.5 K heating in a COMSOL model and reports above-bandgap-only switching; it also reports optical-write/electrical-reset cycles. The cycle documents a structural write followed by reset under that protocol, but is not a controlled post-light-off retention curve over a declared hold interval. This is a useful non-bulk-melt precedent, but the direction is selected by the built-in imprint, not a coherent phase-odd selector.

This analysis is a conditional model and primary-literature audit. It does not establish a new capability, favorable material rates, novelty, cost superiority, or any transfer to GaAs, hBN, BaTiO\(_3\), Te, or another material.

## Exact symmetry result: mobility alone cannot write a polarity

Let a finite configuration space \(\Omega\) have an involution \(\iota\) that exchanges the actual two variants, \(\iota^2x=x\). Let \(M(\iota x)=-M(x)\) be a signed structural order parameter. A time-dependent continuous-time Markov generator \(Q_t\) is variant-symmetric when

\[
 Q_t(\iota x,\iota y)=Q_t(x,y)\quad\text{for all }x,y,t.
\]

If the initial distribution is symmetric, \(p_0(\iota x)=p_0(x)\), then \(p_t(\iota x)=p_t(x)\) for all finite \(t\). To see this, define \(\tilde p_t(x)=p_t(\iota x)\). The generator identity makes \(\tilde p_t\) solve the same forward equation as \(p_t\); uniqueness and equal initial data imply equality. Consequently \(\mathbb E[M_t]=0\), and the positive- and negative-variant probabilities are equal (apart from a symmetry-invariant tie class). This holds for any symmetric temperature history, any symmetric nucleation/migration/regrowth network, and any common mobility change.

In particular, if \(Q_t=a(t)Q_0\) with \(a(t)>0\), then

\[
 p_t=p_0\exp\!\left(Q_0\int_0^t a(s)\,ds\right).
\]

The multiplier changes the clock and can accelerate coarsening, but it cannot create a signed bias from a symmetric ensemble. This is the common-generator-multiplier result already present in the N811 kernel. If the finite chain is irreducible and the field is removed, its symmetric field-free stationary distribution is the long-time limit; finite-horizon retention and asymptotic symmetry are compatible.

The theorem depends on the *actual* variant involution and symmetric initial state/kernel. It must not be applied by simply assigning signs to translational antiphase domains. Such domains need not be inversion-related or have opposite nonlinear susceptibility. Nor does it say asymmetric seed populations cannot yield net output: then the asymmetry is an input that must be mapped, costed, and included in the baseline.

## Conditional phase-odd drive theorem and detailed balance

For a polarity-like order parameter (M(x)), take the explicit effective free energy

\[
 F_h(x)=F_0(x)-hM(x),\qquad F_0(\iota x)=F_0(x).
\]

For single-site heat-bath/Glauber transitions, or any locally detailed-balanced transition pair,

\[
 \frac{q_h(x,y)}{q_h(y,x)}=\exp[-\beta(F_h(y)-F_h(x))].
\]

Thus a real conjugate field changes the forward/reverse ratio; it can bias pair nucleation, boundary migration, and regrowth rather than only multiplying every rate. A hypothetical coupling proportional to the relative optical phase cosine reverses sign when the phase is shifted by pi. Exact inversion covariance then requires that phase reversal exchange the complete driven structural law. The coupling strength, sign, spatial range, and size relative to heat/direct-field effects are material parameters that must be acquired. Optical interference establishing a carrier term does not provide them.

For pulse duration t_p, zero-field retention horizon \(\tau\), and initial symmetric law \(p_0\), the full finite-time structural distribution is

\[
 p_{\pm}^{\rm ret}=p_0 e^{Q_{\pm h}t_p}e^{Q_0\tau},\qquad
P_{\pm}(A)=\sum_{x\in A} p_{\pm}^{\rm ret}(x).
\]

For time-varying pulse waveforms, use the time-ordered propagator. No equilibrium approximation is made during the pulse or hold. A candidate is polarity-selective only if a predeclared structural endpoint A, such as positive-variant majority or retained boundary advance, has a reproducible phase-odd response at the stated post-drive horizon.

In a seedless three-dimensional isotropic nucleation approximation, a spherical domain with bulk free-energy advantage \(\Delta f=2h\) has

\[
 \Delta G(R)=4\pi R^2\sigma-\frac{4\pi}{3}R^3\Delta f,
 \quad R_*=\frac{2\sigma}{\Delta f}=\frac{\sigma}{h},
 \quad \Delta G_* = \frac{16\pi\sigma^3}{3\Delta f^2}=\frac{4\pi\sigma^3}{3h^2}.
\]

This conditional classical estimate makes the near-coexistence obstacle explicit: as \(h\to0\), the critical radius and barrier diverge. An existing, mapped, weakly pinned boundary can bypass the *bulk nucleation* barrier; it does not bypass pinning, reverse events, defects, heating, or the need to measure a transition kernel. No \(\sigma\), h, nucleation prefactor, wall mobility, or pinning distribution is assigned to a real material here.

## Exact finite-state countermodel with nucleation, migration, regrowth, and removal

`ising_retention.py` enumerates all 256 states of a periodic eight-site inversion-related \(s_i\in\{-1,+1\}\) ring. Its model free energy and one-site heat-bath flip rates are

\[
 F(s;h)=-J\sum_i s_i s_{i+1}-h\sum_i s_i,\qquad
 q_h(s,s^{(i)})=\frac{\nu}{1+\exp(\beta[F(s^{(i)};h)-F(s;h)])}.
\]

Each flip obeys detailed balance exactly. Starting from the exact \(h=0\) Gibbs law, a +h pulse permits pair-domain nucleation, wall migration, domain growth/regrowth, and eventual whole-ring reversal; then h is set to zero and the full chain is evolved for the retention interval. Matrix exponentials give full probability distributions, not Monte Carlo estimates. Phase reversal, detailed balance, and mass conservation are checked in code.

At dimensionless \(\beta J=1\), \(\beta h=0.3\), \(\nu t_p=40\), and \(\nu\tau=2\), all *illustrative only*, the plus pulse gives mean polarity 0.81388, positive-majority probability 0.92466, and all-plus probability 0.74693 after the drive is off. The phase-reversed pulse gives the exact inverted result to numerical precision. Waiting \(\nu\tau=1000\) returns mean polarity to zero and positive/negative majority probabilities to 0.47417 each.

The matched unbiased thermal kernel gives zero mean polarity. More directly, from a uniform random domain mosaic at equal elapsed time t=1/ν, multiplying every field-free flip rate by ten lowers the mean number of domain walls from 1.08820 to 0.43713, while mean signed polarity remains zero to 1e-14. This is the exact finite-state countermodel for “faster unbiased coarsening” versus selected writing. The conditional small per-site-field, coarse two-variant witness uses \(N=100\) and \(\beta h=0.01\) per site (total \(N\beta h=1\)): with a *hypothetical* whole-domain attempt rate and pulse/hold, its selected probability is 0.87322 after drive removal. This demonstrates an extensive bias can accumulate across a cooperative volume; the assumed rate is not material evidence.

The model's finite-time on/off work is also explicit. For a sudden pulse from h=0 to h and back, starting from \(\pi_0\), the pathwise work in kBT units is

\[
 \beta W=\beta h\,[M(s_{\rm end})-M(s_{\rm start})],
 \quad
 \Pr(W=w)=\sum_{x,y:\,\beta h[M(y)-M(x)]=w}
 \pi_0(x)[e^{Q_ht_p}]_{xy}.
\]

The field-free hold does no work in this bookkeeping but contributes to the retained output/noise distribution. The full 256-state retained probability vector and discrete on/off work histogram are serialized in `ising_results.json`. For the illustrative eight-site run, mean work is 2.0990 \(k_BT\), variance 4.6391 \((k_BT)^2\), final nonequilibrium free energy is 0.5421 \(k_BT\), and mean dissipated work above that free energy is 1.5569 \(k_BT\). The three-outcome (+ majority, − majority, tie) readout entropy is 0.31525 nats, so a degenerate memory reset would cost at least 0.31525 \(k_BT\) per recorded outcome in the reversible Landauer idealization. Reset is conditional on recording this result; it is not charged to an open-loop pulse. These dimensionless values are model output, not device costs.

## Noisy interface model and its finite-time cost

`continuum_wall.py` gives the complementary analytic limit: a *pre-existing flat interface*, with no bulk nucleation or pinning, translating as a Brownian coordinate. For

\[
 F[m;h]=A\!\int\!\left[\frac{\kappa}{2}(m')^2+\frac{a}{4}(m^2-1)^2-hm\right]dx
\]

and overdamped dynamics \(\partial_t m=-\Gamma\,\delta F/\delta m+\eta\), projection onto a \(\phi^4\) kink of width \(\delta\) gives

\[
 I=\int(m')^2dx=\frac{4}{3\delta},\quad
 \mu=\frac{\Gamma}{AI},\quad
 |F_{\rm wall}|=2hA,\quad
 v=\mu |F_{\rm wall}|,\quad D=\mu k_BT.
\]

For a drive lasting `t_p` and field-free hold \(\tau\), target advance \(L\), and initial wall coordinate known, this conditional model gives

\[
 X_{t_p+\tau}\sim\mathcal N(vt_p,2D(t_p+\tau)),\quad
 P(X_{t_p+\tau}\ge L)=\Phi\!\left(\frac{vt_p-L}{\sqrt{2D(t_p+\tau)}}\right),
 \quad W=F_{\rm wall}(X_{t_p}-X_0)\sim\mathcal N(F_{\rm wall}vt_p,2F_{\rm wall}^2Dt_p).
\]

Its controlled-versus-uncontrolled path KL divergence during the pulse is \(v^2t_p/(4D)\), and Einstein consistency gives \(\beta\mathbb E W=4D_{\rm KL}\). Data processing bounds the KL divergence of any binary endpoint test by this path KL. In the script's dimensionless illustrative case, target advance probability is 0.94791 for +drive, 0.0005775 for reversed drive, and 0.20827 for unbiased motion after the hold. Mean drive work is 12 \(k_BT\), work variance 24 \((k_BT)^2\), path KL is 3 nats, and the sign-record reset floor is 0.04367 \(k_BT\). This construction isolates seeded wall drift; it must not be sold as a nucleation model or material rate.

These two models address different regimes. The finite Ising chain includes symmetric activation/nucleation and growth at its chosen lattice scale; the interface model conditions on an existing boundary and gives a continuum noise law. Neither substitutes for measured full-configuration kinetics.

## Why carrier or optical population contrast is underdetermined

Let the measurable carrier signal in an identified variant \(s\in\{-1,+1\}\) be

\[
 n_s(\phi)=n_0+s c\cos\phi.
\]

Consider two models with the same measured signal and identical fluence, frequency conversion, transmission, and reflection:

1. **No structural selection:** the auxiliary \(n_s\) is observed, but structural transitions follow the symmetric \(Q_0\), or a common multiplier \(a(\phi)Q_0\). This gives no mean polarity from a symmetric start; it may change coarsening time.
2. **Structural selection:** the same signal couples to an odd structural generalized force \(h(\phi)=g c\cos\phi\), and transitions follow \(Q_{h(\phi)}\). This gives phase-reversing selected migration/nucleation and finite-horizon retention in the examples above.

These models are observationally identical with respect to \(n_s(\phi)\) but imply different retained structural outputs. Thus carrier contrast alone does not identify \(g\), the variant-to-variant rate ratio, transition committor, or structural result. If optical phase changes only a scalar event rate, N811's clock-only result applies. State-dependent rates can alter endpoint selection, but then the same-configuration kernel and committor defect must be measured. An optical interferogram, photocurrent, or postprocessing optical anisotropy is not a substitute for a post-drive structural map.

## Baselines and complete cost boundary

The strongest direct baseline is an electric field conjugate to the same mapped structural polarity. If it induces the same \(F_h\) and rates \(Q_h\), optical and electric output distributions, work inside the material model, and retention are identical. An optical benefit must come from a measured advantage in access, geometry, spatial resolution, waveform, or total cost. A symmetric thermal pulse matched to local \(T(x,t)\), absorbed energy, and timing can accelerate coarsening but preserves the zero-sign theorem. To test a coherent phase-specific effect, compare \(\phi\) with \(\phi+\pi\), randomized phase, each color alone, non-overlapping pulses, and dose/temperature-matched controls.

The all-in comparison must charge both optical colors, harmonic generation and stabilization, source wall-plug energy, phase lock, actual absorbed-energy partition, heating/cooling or preheat, specimen/cap preparation, applied field/current and electrodes, readout and feedback, defect/damage/yield, material inventory loss, postdrive retention, reset if data are recorded, and output conditioning. Credit a return only if it is measured and reusable at the same declared boundary. Do not double count energy absorbed into the wall's structural free-energy change as both heat and work. N814's regenerative-work accounting is a cost-boundary discipline only; no molecular activation theorem is transferred to this solid-state system.

## Primary physical evidence and what it does not show

- Fraser et al. report that simultaneous fundamental and sum-frequency beams in a noncentrosymmetric medium produce interference between one- and two-photon transitions that modifies net absorption and can control carrier population. Their phased 1550/775 nm, 120 fs example is GaAs at 295 K. The result is a carrier/absorption control, not a retained structural transition. [Physical Review Letters 83, 4192 (1999), DOI 10.1103/PhysRevLett.83.4192](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.83.4192).
- Wahlstrand et al. measure phase-dependent carrier populations and photocurrent in GaAs and report geometry-dependent access to the effect and strong static-electric-field sensitivity. Their article is a direct reminder that a measured coherent signal can be confounded or enhanced by applied electrical fields. It is not evidence that a crystal variant or boundary is selected and retained. [Optics Express 19, 22563 (2011), DOI 10.1364/OE.19.022563](https://opg.optica.org/oe/abstract.cfm?uri=oe-19-23-22563).
- Horstmann et al. demonstrate coherent control of switching efficiency into a metastable metallic state in quasi-one-dimensional 1T-TaS\(_2\). This is a useful structural-transition precedent but the selected output is not an inversion-related retained polarity pair. [Nature 583, 232 (2020), DOI 10.1038/s41586-020-2440-4](https://www.nature.com/articles/s41586-020-2440-4).
- Pal et al. report subsecond optical switching of ferroelectric domains in a freestanding BaTiO3 membrane: 391 nm illumination at 0.63 W/cm^2 switches an upward region downward, while their measured negative imprint V_IMP = -0.55 V favors downward polarization; their interpretation couples that imprint to a lowered wall-motion barrier under illumination. They estimate a 0.25–0.5 K illumination-induced temperature increase in a COMSOL model, report above-bandgap-only switching, and show an optical-write/electrical-reset cycle. That documents an optical structural write followed by electrical reset under the reported protocol; it does not establish a controlled post-light-off retention curve over a declared hold interval. A phase-odd coherent polarity selector also remains unmeasured. The same material has direct electrical switching. [Nature Communications 16, 7940 (2025), DOI 10.1038/s41467-025-58592-x](https://www.nature.com/articles/s41467-025-58592-x).
- Kobayashi et al. report polarization-directed reorientation of the crystallographic \(c\)-axis in Te thin films. This is real post-growth structural orientation control but is not a polarity-writing experiment. The 2026 follow-up by Mitsuzuka et al. (arXiv:2606.26499v2, a preprint) measures pulse-number/fluence dependence and fits an Arrhenius model for linearly-dichroic, state-dependent heating and random reorientation. It therefore provides a cautionary photothermal alternative, not support for coherent phase-odd control. Their model assumes a melting-point-scale barrier and few-atom effective activation volume; those are model assumptions rather than a direct local temperature/map measurement. [Nano Letters 26, 104–110 (2026), DOI 10.1021/acs.nanolett.5c04774](https://pubs.acs.org/doi/10.1021/acs.nanolett.5c04774); [Mitsuzuka et al., arXiv:2606.26499v2](https://arxiv.org/html/2606.26499v2).

## Capital relationship and exact missing gate

- **N777:** the inherited result concerns common-committor/clock-selection: a common scalar generator multiplier changes the rate of traversal without changing autonomous path or committor selection. Its original report and `G-FA-N777-REVIEW` require same-specimen legal forcing/work and transition derivatives, direct-field discrimination, a configuration-level retained endpoint, and matched electrical/thermal controls with total energy and damage. The C > 0.4484916 complete-melting threshold belongs to the separate incoming physical phase-rewriting record described above, not N777. Neither source supplies the phase-odd retained structural kernel required here.
- **N783:** use the full configuration-level transition kernel plus terminal structural reward, damage, and cost as the correct evidence format. Its carrier-repair kernel and hBN context do not transfer to this structural problem.
- **N811:** a common positive generator multiplier changes time, not eventual reaction/endpoint selection. State-dependent policy can alter a committor, but a same-network mapped target/competitor, topology readout, and retained functional endpoint are required. This is the closest exact mathematical comparator for the symmetry/coarsening result.
- **N814:** retain the discipline of counting loading, losses, work return, reset, heat, throughput, and output at a matched boundary. Its molecular activation or renewal conclusions are not solid-state kinetic evidence.

The decisive next measurement is a **same specimen, same structural configuration, phase-reversed, field-free-retained transition map**. First establish the two actual variants and boundary topology structurally, including their symmetry relation; quantify the coherent carrier/heat/electric response in the chosen geometry and fluence. Then measure phase-conditioned forward/reverse nucleation and boundary rates or the full configuration transition kernel for \(\phi\) and \(\phi+\pi\), with a predeclared retention horizon after both light and applied fields are off. Use randomized phase, each colour alone, phase-averaged, dose/temperature-matched, and optimized direct-electric controls. Image the final structure and inventory independently of the control signal; include damage and functional output. If only mobility changes, stop at faster coarsening. If phase reversal changes the retained structural kernel but not the direct-field/thermal matched endpoint at lower total cost, the operation is real but not advantageous. No favorable rate should be inserted before measurement.

**Status of the physical question:** conditional theorem established in these models; primary examples show optical structural movement can occur without requiring whole-domain melting; the requested small phase-odd excitation-to-retained-polarity coupling, its finite-time material kernel, post-off durability, and practical advantage remain **UNKNOWN / unacquired**.
