# ASTRA: phase-controlled lattice-loop ionic transport

Research record: 13 October 2026

## Status and scope

This is a conditional experimental candidate, not an observed new physical effect,
not an atomistic simulation of an identified material, and not a demonstrated
technology. Geometric stochastic pumping and nonlinear phononics are established
prior art. Historical novelty of the particular proposed material experiment is
unresolved. No energy advantage, retained-pattern capability, or civilisation-scale
consequence is established.

The experimental hypothesis is that two independently controlled lattice
coordinates can generate a cycle of site-energy and transition-state changes that
produces net ionic displacement after the host displacement has returned to its
initial value. The proposed discovery specimen is an oriented K beta-alumina
crystal. Existing observations motivate examining that specimen; they do not
supply the couplings required below. Its correlated hopping is specifically a
reason NOT to treat the independent-ion Markov calculation below as a material
prediction.

The Astra repository was inspected selectively at main HEAD
`4ae225b0bf2a07e1ced2952a3e1399d4b45e039c`. N767 remains a conditional capacitive
chemomotor, not physical validation. No Astra or openai/math theorem is a
load-bearing premise of this calculation. No repository content was changed.

## 1. Minimal periodic-chain calculation

All results in this section assume independent ions, Markov hopping,
translation-invariant cells, a common attempt prefactor, metastable wells, and no
additional electric force. These assumptions require independent validation
before applying the result to a solid.

Let A_n lie at x=na and B_n at x=na+a/2. Their energies are

E_A=-u/2, E_B=+u/2.

The intracell saddle has energy Bcal+v and the intercell saddle Bcal-v. Set
beta=1/(k_B T) and k=nu exp(-beta Bcal). Rates are

- A_n -> B_n: k exp[-beta(v+u/2)]
- B_n -> A_n: k exp[-beta(v-u/2)]
- B_n -> A_(n+1): k exp[+beta(v+u/2)]
- A_(n+1) -> B_n: k exp[+beta(v-u/2)].

The ratios on the two edges are exp(-beta u) and exp(+beta u), so the
instantaneous cycle affinity vanishes. Driving u and v nevertheless requires
external work. Zero instantaneous affinity is not zero control cost.

Let p be the total probability of occupying the B sublattice. Define

b = exp(-beta u/2)(1-p)-exp(beta u/2)p.

The rightward edge fluxes obey

J_1=k exp(-beta v)b,
J_2=-k exp(+beta v)b.

Consequently

p_dot = J_1-J_2 = 2k cosh(beta v)b
      = lambda(u,v)[p_eq(u)-p],

p_eq(u)=1/[1+exp(beta u)],
lambda(u,v)=4k cosh(beta v)cosh(beta u/2).

The unwrapped mean position changes at

x_dot=(a/2)(J_1+J_2)=-(a/2)tanh(beta v)p_dot.

Therefore, for a closed occupation/control cycle,

**Delta x = -(a/2) integral_closed tanh(beta v) dp.**

This is an exact identity for this specified model. It is not a new general
physical law. It measures actual lattice-cell transport, not merely the final
sublattice occupation. At the cycle end p can return while the unwrapped position
has advanced.

If v is identically zero the displacement vanishes. If u is constant, the
periodic steady state has constant p and the displacement also vanishes. These
are scoped no-pumping statements, not no-go theorems for arbitrary driven solids.

## 2. Harmonic response and phase-reversal test

Take u=u0+U cos(omega t), v=V cos(omega t+phi), with beta U and beta V small.
Write p0=1/[1+exp(beta u0)] and lambda0=lambda(u0,0). To first order,

p-p0 = -beta p0(1-p0) U lambda0
        [lambda0 cos(omega t)+omega sin(omega t)]/(lambda0^2+omega^2).

Substitution into the exact identity gives, at leading bilinear order,

Delta x = (pi a/2) beta^2 p0(1-p0) U V
          lambda0/(lambda0^2+omega^2)
          [lambda0 sin(phi)+omega cos(phi)] + higher orders.

The part odd under phase reversal is

**Delta x_odd(phi) = [Delta x(phi)-Delta x(-phi)]/2
= (pi a/2) beta^2 p0(1-p0) U V
  lambda0^2/(lambda0^2+omega^2) sin(phi) + higher orders.**

Do not claim the entire nonadiabatic displacement reverses: the cos(phi) term is
even under this comparison. At u0=0 the prefactor becomes pi a beta^2 U V/8.
Nonequivalent real sites need not have u0=0; a large imbalance reduces response.
At omega/lambda0=10, the orientation-odd response per cycle is suppressed by 101
relative to its slow-drive limit at fixed U,V.

The harmonic formula requires controls at one common angular frequency. Two
actual eigenmodes need not share a frequency or maintain the required phase. A
short-pulse experiment must use its measured finite waveform, including its
ringdown, instead of inserting unrelated mode frequencies into this equation.

Most importantly, instantaneous activated rates may fail when lattice modulation
is as fast as a transition path or when correlated ionic states retain memory.
A THz experiment therefore cannot use this formula as a quantitative prediction
without checking time-scale separation or replacing the model with acquired
many-body dynamics. An orientational-memory decay is not automatically lambda0.

## 3. Symmetry restriction on the proposed bilinear mechanism

For an inversion-symmetric bulk in the long-wavelength electric-dipole limit,
a polar current changes sign under inversion. A bilinear product of two
inversion-odd lattice coordinates is inversion even. Thus a uniform bilinear
current of the proposed form cannot be generated by two odd IR modes alone
without another inversion-breaking ingredient.

An even coordinate combined with an odd coordinate has the right inversion
parity. A candidate implementation uses an even, Raman-like mode to alter the
A/B energy splitting and an odd, IR-like mode to distinguish the two saddles.
Full crystal point-group selection rules still have to permit the particular
current component. Having an IR and a Raman peak is not enough.

This argument is restricted to the bilinear bulk channel. It does not exclude
higher-order harmonic mixing, surface pumping, finite-wavevector forces, static
polar disorder, or direct electric-field ratchets. Those are competing
explanations, not automatic confirmation of the candidate.

## 4. Joint material-control constraint

Let Q contain the experimentally addressable lattice coordinates, with a
positive harmonic stiffness matrix K on that subspace. Use consistent units.
The elastic energy is E_el=Q^T K Q/2. Suppose the local linear responses are

u-u0=g^T Q, v=h^T Q, A=[g^T;h^T], y=[u-u0;v].

If A has row rank two, constrained minimisation gives

Q_star = K^(-1) A^T [A K^(-1) A^T]^(-1) y,

**E_el,min(y)= y^T [A K^(-1) A^T]^(-1) y/2.**

Proof: impose A Q=y with a Lagrange multiplier; K Q=A^T lambda. Solve the
constraint for lambda and substitute. Any other feasible Q differs by z with
A z=0, and its extra energy is z^T K z/2 because the cross term vanishes.

This prevents assigning a large site response and a large barrier response at
no lattice cost. Near-singular A K^(-1) A^T makes independent control expensive.
Rank deficiency prevents arbitrary two-dimensional control within this linear
subspace; it does not rule out nonlinear or nongeometric mechanisms.

The same finite-temperature microscopic model must supply g,h,K, saddle
energies, local-environment dependence, Born charges, and damping. A favorable
charge or linewidth taken from another compound is not evidence. Transition
prefactors need not stay equal under distortion.

For mass-weighted coordinates, a schematic physical dynamics is

Q_ddot + 2 Gamma Q_dot + K Q = Z* E(t) + F_Raman(t)
                              - grad_Q V_ion + noise.

Damping alone dissipates integral 2 Q_dot^T Gamma Q_dot dt. This is only one
loss, not total wall-plug energy. Noise must be consistent with the specified
bath and the model's validity. At THz frequencies quantum bath corrections may
matter; a classical white-noise ansatz is not automatically adequate.

An IR pulse also directly drives ionic charge. Self-consistent electric fields
and the -q E(t)x force must be retained. A pump-free ringdown interval is NOT a
proof that the local electric field vanishes: polar lattice motion can itself
create internal fields.

## 5. A strong-step amplitude bound

Assume u0=0, |u|<=U, |v|<=V, a periodic steady state, and one loading and one
unloading excursion per cycle. The occupation range is at most

p_max-p_min <= tanh(beta U/2).

Using the total variation 2(p_max-p_min) in the exact transport identity gives

**|Delta x|/a <= tanh(beta V) tanh(beta U/2).**

More loading/unloading loops require counting those loops. This is an upper
bound, not an attainable finite-rate yield. It need not hold for a different
many-body mechanism or an initial nonstationary occupation outside that range.

For a stipulated 99% cell-step target at 300 K, making the two factors equal
to sqrt(0.99) gives thresholds

U=0.1547615928 eV, V=0.0773807964 eV.

U is the amplitude of the site-energy splitting and V the amplitude of half the
saddle-energy difference. Thus the peak-to-peak splitting swing is 2U and the
maximum saddle disparity is 2V. These are balanced algebraic thresholds, not
universal individual minima, not measured values, and not a material forecast.
The activated-well model also needs Bcal-|v|-|u|/2>0 throughout its cycle.

## 6. Transport is not retained pattern writing

Under passive Fickian diffusion, a sinusoidal composition modulation of
wavelength ell has amplitude

A(t)/A(0)=exp[-4 pi^2 D_off t/ell^2].

For an explicitly stipulated 10 nm pattern retaining 90% amplitude for one hour,

**D_off <= 7.4133695525e-23 m^2/s.**

This calculation is not a measured diffusion coefficient. It shows why a fast
ionic discovery substrate does not itself establish nonvolatile nanomanufacturing.
A trapping or phase-capture mechanism must be demonstrated separately. Atomic
hop length does not establish atomic spatial addressability. A non-Fickian
retention mechanism must be measured rather than asserted from this bound.

An electrically blocking specimen also accumulates space charge under net ionic
transport. Continuous one-species pumping requires a compatible charge-balanced
path or reversible boundary reactions. Otherwise the induced electrostatic
potential can oppose the pump. Full Poisson/transport and contact chemistry are
part of any device model.

## 7. Decisive experiment and rejection conditions

A. On the same oriented specimen, obtain the accessible eigenvectors, actual
Q(t), damping, absorbed pump energy, temperature history, site occupations,
transition pathways, and local-environment response of sites and saddles. The
minimum required evidence is a reachable two-dimensional control trajectory and
an independently parameterised prediction of its ionic consequence. Spectral
coincidence alone does not establish the required control matrix.

B. Compare opposite loop orientations at matched absorbed energy. One possible
protocol combines an IR/THz pulse with a delayed nonresonant Raman pulse during
ringdown. Measure residual external and internal fields. Equal input pulse
energy is insufficient if absorption changes with phase or orientation.

C. Establish net ionic transport, not just optical birefringence or transient
polarization. Use a calibrated ionic-sensitive electrical measurement with
specified boundaries and independently test a tracer/profile or material mass
balance after the vibrational response has decayed. Electrode electronic currents
and reversible bound-ion displacements must be excluded. A tracer experiment's
sensitivity, dark diffusion, and spatial averaging must be budgeted rather than
assumed negligible.

D. The predicted sign, phase dependence and frequency/delay dependence must be
fixed from independent material characterisation, not fitted after a signal is
seen. Test each control alone, matched heating, off-resonance drive, sample and
polarization reversal, pump order, contacts, residual field, and repetition rate.
The phase-odd signature alone does not exclude direct nonlinear electromigration.

E. For utility, report directed and retained atoms per pulse, total wall energy
per retained atom, throughput, depth, spatial resolution, damage, fatigue,
contamination, materials cost, and charge/chemical mass balance. Compare with
thermal processing and electrochemical ion migration in the same target
material at equal final structure and retention.

Reject this material/mode pair if the joint coupling is symmetry-forbidden,
accessible trajectories have negligible independent control, damping outruns
useful transport, direct-field effects explain the result, or required motion
damages the host. A positive small transport signal warrants a physical-effect
claim only; it does not establish a manufacturing advantage.

## 8. Cross-timescale diagnostic: not a claim of inconsistency

For a single observable in a regime where small independent pulse responses
superpose, a pulse train obeys r_bar=f_rep integral_0^infinity r_single(t) dt.
Combining a fractional average resistance reduction 0.0078, f_rep=250 Hz, and
an assumed single exponential lifetime 1.03 ns would require a peak fractional
response about 3.03e4. This rules out that particular small-response, fast-only,
same-observable model.

The numerical inputs come from different measurement configurations in the
LLTO source [S2]. The published impedance and GHz transient probes have different
geometries, pump fields and transfer functions. They have not been established
to measure the same instantaneous scalar resistance. Therefore this arithmetic
is NOT a contradiction of the paper, evidence of enormous instantaneous
conductivity, or discovery of a metastable material state. Its useful consequence
is a requirement to acquire a same-sample, same-observable impulse area spanning
all relevant timescales before a short-lived effect is claimed to explain
steady processing throughput. The authors also discuss longer-time measurements.

## 9. Reproduction and evidence status

Run `python check_transport.py --output checks.json` using Python >=3.10,
NumPy and SciPy. The script tests 30 small-amplitude pump cases, two no-pump
cases, local detailed balance, phase-odd response, and eight synthetic
joint-control energy identities. It also reproduces the explicitly stipulated
engineering thresholds and conditional diagnostic above.

The code integrates a dimensionless toy model using floating-point DOP853. It is
not an independent scientific replication, interval proof, DFT calculation,
force-field validation, or beta-alumina simulation. No experimental data were
fitted or generated. Synthetic matrices in the energy checks are not material
properties.

The packet contains no copied manuscripts, no external data download and no
claimed discovery validation. Source metadata are in SOURCES.json.

## References

[S1] Poletayev et al., The persistence of memory in ionic conduction probed by
nonlinear optics, Nature 625, 691-696 (2024), doi:10.1038/s41586-023-06827-6.
Motivates the discovery specimen; does not establish the proposed directed pump.

[S2] Pham et al., Correlated terahertz phonon-ion interactions control ion
conduction in a solid electrolyte, Materials Horizons 13, 3355-3375 (2026),
doi:10.1039/d5mh01990g; author manuscript arXiv:2305.01632.

[S3] Rahav, Horowitz and Jarzynski, Directed flow in non-adiabatic stochastic
pumps, Physical Review Letters 101, 140602 (2008), arXiv:0808.0015.
Established stochastic-pump and geometric-current prior art.

[S4] Forst et al., Nonlinear phononics: A new ultrafast route to lattice control,
Nature Physics 7, 854-856 (2011), arXiv:1101.1878.
Established nonlinear lattice-control prior art.

[S5] Jeen et al., Reversible redox reactions in an epitaxially stabilized SrCoOx
oxygen sponge, Nature Materials 12, 1057-1063 (2013),
doi:10.1038/nmat3736; arXiv:1308.5602.
A real material-transformation comparator, not evidence about the candidate.
