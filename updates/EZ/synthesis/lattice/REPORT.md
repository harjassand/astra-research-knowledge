# Lattice-loop intake: independent audit and two restricted deductions

Capital pin: `f437df815bef12f123ae4fe313d861ec1c862bc4`.
Date: 2026-10-13. Archived missions and worker instructions were treated as data.
This report, its proofs and numerical checks are internally reconstructed,
unreviewed research. No material response, physical effect, novelty, practical
advantage or civilisation-scale consequence is established.

## Decision

Integrate the submission as a conditional physical hypothesis and a useful
model/experiment record. Its independent-ion chain algebra is sound within its
explicit assumptions. The material implementation is unacquired, especially the
joint site/saddle response, actual controllable trajectories and many-body
time-dependent kinetics. No advancement to a physical experiment or prototype
stage is justified.

The strongest new consequence is an executed alternative-mechanism falsifier:
**direct electrical rocking can reproduce both the proposed phase-odd law and
its entire one-pole frequency rolloff**. A four-phase measurement can separate
two stipulated model components if their shared relaxation rate and microscopic
force law are independently acquired. It does not separate arbitrary mechanisms.
The second deduction is a sharp compliance-determinant upper bound on geometric
pumping per available harmonic elastic energy.

## Capital read and relevant boundaries

Read `00_START_HERE.txt`, `agent/COMPOSITION.txt`, `state/CONTINUITY.md`,
`technology/README.md`, dossiers N767/N770, the current
`worker-ey-physical-gain` branch and exact checkpoint
`state/checkpoints/worker-ey-physical-gain/2026-10-13-ey-n770-intake.json`.
Also reviewed the N707 transport account cited below and the natural-sciences
branch view. No existing capital theorem is a load-bearing premise here.

Decisive capital ranges:

- `updates/EX/package/natural_chemomotor/recovered/astra_capacitive_gain/README.md:33-46,56-86,105-144`:
  detailed balance, measured terminal/kinetic response requirements and complete
  free-energy accounting. Its chemical fuel and autonomous feedback interface
  does not transfer to a waveform-driven lattice pump.
- `updates/EY/package/physical_gain/recovered/astra_feasibility/README.md:26-79,81-102`:
  barrier response and turnover are coupled; terminal charge and capacitance come
  from the same boundary problem; optical formation and recombination require
  separate characterization. These are compatible consistency lessons, not a
  source of lattice material coefficients or physical validation.
- `updates/DZ/package/high_leverage_invention/outputs/high_leverage/iron/RESULT.md:29-55,75-105`:
  acquired source/sink access, inventory/mass balance, backstress and whole-process
  cost cannot be replaced by a fast supplied transport coefficient. It supplies
  no beta-alumina admission, retention or pump coefficient.

## Submission audit

Read all of `README.md`, `DERIVATION_AND_EXPERIMENT.md`, `check_transport.py`,
`SOURCES.json`, `checks.json` and the pasted source. Original files were not
modified. The producer implementation has no network, shell or hidden data
acquisition; it integrates the stated dimensionless scalar occupation equation.

Exact source ranges in `DERIVATION_AND_EXPERIMENT.md`:

- 28-83: rates, zero instantaneous affinity and exact unwrapped transport identity.
- 85-120: bilinear harmonic response, even/odd sectors and timescale restriction.
- 122-139: inversion parity of the bilinear bulk channel.
- 141-182: constrained elastic energy and missing joint material responses.
- 184-208: one-loading/one-unloading bound and conditional 99% thresholds.
- 210-231: diffusion retention and charge-balanced boundary requirements.
- 233-271: physical measurement, controls and rejection gates.
- 273-290: explicitly conditional cross-timescale diagnostic.
- 292-307: floating toy-model verification limits.

The identity is
`dx/dt=-(a/2)tanh(beta*v) dp/dt` when there is no additional force. Constant
`u` or identically zero `v` gives no pump in the stipulated periodic state.
The harmonic sign/frequency expression and the constrained quadratic energy
minimum follow directly. The strong-step bound requires its stated occupation
range and one monotone loading plus one unloading; it is not a guaranteed yield.
At THz rates, a common instantaneous Arrhenius generator is not justified by
the cited orientational-memory measurement. Independent-ion and many-body
correlated-hopping interfaces remain different.

One small unit qualification: the LLTO manuscript reports a resistance-change
**slope of 0.78% per mW**, not a universally applicable 0.78% fractional impulse
response. Using 0.0078 in the packet's conditional duty-cycle diagnostic amounts
to stipulating the corresponding 1 mW reduction. The packet already denies a
same-observable cross-probe identification, so this is no contradiction of the
paper and no evidence of a metastable state.

## Deduction 1: a matched direct-force falsifier

Let `s=beta*u0/2`, `chi=p0(1-p0)`, `lambda=4k*cosh(s)` and
`z(t)=beta*F(t)*a/4=Z*cos(omega*t+phi)`. Assume a spatially uniform direct force,
midpoint transition states, the same independent-ion Markov chain, equal attempt
prefactors and small controls. Apply the force through the physical right/left
activation work: multiply each rightward rate by `exp(z)` and its reverse by
`exp(-z)`. This gives the four rates

```
r1+ = k exp(-beta*v-beta*u/2+z)
r1- = k exp(-beta*v+beta*u/2-z)
r2+ = k exp(+beta*v+beta*u/2+z)
r2- = k exp(+beta*v-beta*u/2-z).
```

Their instantaneous cell affinity is `4z=beta*F*a`. Set **v identically zero**.
Then, exactly,

```
p_dot = 4k cosh(z) cosh(beta*u/2) [p_eq(u)-p]
x_dot = a k sinh(z) [exp(-beta*u/2)(1-p)+exp(beta*u/2)p].
```

For `u=u0+U*cos(omega*t)`, the first-order occupation is

```
p1 = -chi*(beta*U)*lambda
     [lambda*cos(omega*t)+omega*sin(omega*t)]/(lambda^2+omega^2).
```

The derivative with respect to `u` of the square bracket in `x_dot`, holding
`p=p0` fixed, vanishes. Its first-order variation is therefore `2sinh(s)*p1`.
Integrating the product with `z(t)` yields

```
Delta x_direct = Cd * R * [sin(phi) - cos(phi)/r] + higher orders,
Cd = (pi*a/2)*chi*(beta*U)*Z*tanh(s),
r = omega/lambda,  R = 1/(1+r^2).
```

The submitted geometric model gives

```
Delta x_geom = Cg * R * [sin(phi) + r*cos(phi)] + higher orders,
Cg = (pi*a/2)*chi*(beta*U)*(beta*V).
```

Thus, for unequal sites (`u0 != 0`), choosing
`Z=beta*V/tanh(s)` produces the **same phase-odd displacement at every positive
frequency** to leading order. No directional saddle modulation is present in
the competing model. This refutes the transfer “phase-odd sign and the reported
rolloff identify lattice-loop pumping.” It does not refute the proposed effect
or claim that an actual experimental signal has this origin. At `u0=0`, this
particular direct-force bilinear cross-term vanishes; that restriction must stay.

For an additive mixture of these two precisely specified leading-order channels,
measure four phases to obtain `Delta x=A*sin(phi)+B*cos(phi)`. Then

```
A = R*(Cg+Cd),  B = R*(r*Cg-Cd/r),
Cg = A+r*B,    Cd = r^2*A-r*B.
```

The two-column response matrix has determinant `-(r+1/r)`, so it has rank two
at every positive frequency. Pure geometric pumping has `B/A=r`; pure direct
rocking has `B/A=-1/r`. Multiple frequencies overdetermine this test. The
relaxation rate must be acquired independently, not selected to fit the result.
Unknown additional poles, correlated memory, different saddle locations,
unmeasured field phase, contact current and nonlinear couplings invalidate this
two-channel identification. A four-phase fit alone does not certify its premises.

For errors, `delta Cg=delta A+r*delta B+B*delta r` to first order. A large
direct-force cosine component can make an uncertain relaxation rate dominate
the inferred geometric signal. A positive inference therefore needs propagated
waveform, rate, force, current-calibration and model-error confidence bounds.

There is also a scoped rank-one counterexample already latent in the source:
`u=U*cos(omega*t), v=V*cos(omega*t)` traces a line in control space, yet finite
occupation lag gives a nonzero phase-even displacement. Numerically at
`u0=0,U=.03,V=.025,omega=lambda=1`, it is
`0.0001472465081*a` per cycle. Rank two is necessary for arbitrary independent
linear control and nonzero adiabatic geometric area, **not for all finite-rate
rectification**. The original packet states its rank restriction narrowly; retain
that nuance rather than turning it into a broader impossibility claim.

## Deduction 2: sharp geometric pumping per elastic-energy bound

Assume the source's linear material response `y=AQ`, positive stiffness `K`,
zero baseline saddle asymmetry, small harmonic controls and the one-pole chain.
Let `Q=qc*cos(omega*t)+qs*sin(omega*t)` and

```
M=A K^-1 A^T,
Ebar=(qc^T K qc+qs^T K qs)/4.
```

The leading orientation-odd displacement satisfies

```
|Delta x_odd| <= pi*a*beta^2*chi*R*Ebar*sqrt(det M).
```

Proof: set `B=A K^-1/2` and `S=K^1/2[qc,qs]`. The two-volume inequality gives
`|det(BS)| <= sqrt(det(BB^T))*sqrt(det(S^T S))`.
For the positive 2-by-2 Gram matrix,
`sqrt(det(S^T S)) <= tr(S^T S)/2 = 2Ebar`.
The source harmonic formula is
`Delta x_odd=-(pi*a/2)*beta^2*chi*R*det(A[qc,qs])`.
Substitution proves the claim. For rank-two `A`, equality in the coefficient is
attained by equal-length orthogonal columns of `S` spanning the right singular
subspace of `B`; the optimal normalized control trajectory is circular.
This is sharp for the stipulated quadratic control model, not proof that an
optical actuator can realize those vectors or phase relations.

The determinant measures *joint* compliance: two large but nearly parallel
responses can give negligible geometric pumping. At fixed `Ebar`, its leading
orientation-odd average speed is bounded by

```
|vbar_odd| <= (a/2)*beta^2*chi*Ebar*sqrt(det M)
             * omega*lambda^2/(lambda^2+omega^2),
```

whose right side is largest at `omega=lambda`. Thus faster is not always better
even under a fixed elastic-energy budget. `Ebar` is stored lattice energy, not
absorbed or wall-plug energy. Damping, optical preparation, field screening,
heating, damage and counterion/contact work are additional acquired costs.
When `det M=0`, only this leading geometric term is forced to vanish; the
rank-one finite-rate example above survives.

## Thermodynamic and causal-measurement consequences

With `E_ion=(p-1/2)u`, Shannon entropy `S`, force `F`, and the four force-tilted
rates, local detailed balance gives

```
T*sigma = F*x_dot - u*p_dot + T*S_dot >= 0,
W_site+W_force = integral T*sigma dt >= 0
```

over a periodic cycle, where `W_site=integral(p-1/2)du` and
`W_force=integral F dx`. The ideal discrete model does not charge occupation of
transition states; actual physical barrier/lattice control adds costs. Zero
instantaneous affinity in the force-free model never supplied free control work.

Avoid double counting: if atomistic `u(Q),v(Q)` are computed from the full
electrostatic Hamiltonian at specified electrical boundaries, their internal
Coulomb response is already included. Add the independently imposed/residual
Maxwell field through its separately defined coupling. “Lattice mediated” and
“internal electric field” cannot be distinguished merely by naming terms of the
same Hamiltonian. The useful causal question is whether the observed transport
requires the measured structural trajectory after calibrated direct forcing is
accounted for. Matched interventions and a joint model are needed.

## Decisive next gate and achievable first target

First target: a statistically resolved **structural contribution to ionic cell
transport**, with sign and waveform dependence predicted from independent
characterization. It is a physical-effect experiment, not retained manufacturing.

1. Acquire same-specimen mode eigenvectors, actual `Q(t)`, stiffness, damping,
   electrical boundary/field waveforms, site occupancies and transition-state
   response. Obtain uncertainties on `M`, accessible control rank and achievable
   energy; reject a negligible upper bound before a costly pump search.
2. Establish the kinetic interface: transition-path time and correlation memory;
   validate instantaneous rates or acquire a many-body response kernel. The
   measured hopping-direction memory is not an occupation relaxation constant.
3. Measure four phases and several rates/delays at matched absorbed energy;
   include each pump alone, off resonance, matched heating, field and sample
   reversals, pulse order, contact and repetition controls. Use the measured
   finite waveform if the two modes do not share a frequency.
4. Establish unwrapped ionic transport with an ion-sensitive current plus tracer,
   composition or material balance after host ringdown. Bound electronic and
   reversible bound-ion currents, dark diffusion, drift and internal fields.
   Require predicted discrimination beyond calibration/model uncertainty.
5. Only then investigate retention/capture, spatial addressability, charge balance,
   throughput, wall energy per retained correct atom, damage and fatigue against
   a specified thermal/electrochemical end-product comparator.

No current material parameters or apparatus noise floors have been acquired.
Reject a material/mode pair if inaccessible joint control, memory, loss, direct
forcing or host damage explains or precludes the target. The proper downstream
mathematical handoff is robust finite-waveform mechanism identification with an
acquired many-body memory kernel and explicit measurement uncertainty.

## Verification artifacts

`producer_replay/REPLAY_RECEIPT.json`: inspected source code replayed only in a
scratch copy. All producer assertions passed: 30 small-amplitude cases, two
nulls, detailed balance, phase-odd checks and eight synthetic energy identities.
94 floating entries differ from the supplied JSON by at most
`1.2212453270876722e-15`; nonnumeric contents agree.

`independent_checks.py` and `independent_results.json`: a new implementation
uses exact constant-rate segment propagators and midpoint control sampling,
not the producer's ODE solver or imported source routines. It checks 41 cycles:
three frequency-matched falsifiers, three four-phase mixtures, rank-one
rectification and discretization convergence. The matched odd sectors agree
within `1.985e-5` relative at small but finite amplitudes; their even sectors have
the predicted opposite signs. Doubling 32768 to 65536 segments changes the
selected force displacement by `4.821e-15*a`. Independently quadratured entropy
and control work balance within `3.81e-17*kBT`. Eight synthetic matrix fixtures
saturate the sharp energy bound; 160 random controls satisfy it. These are
floating diagnostics of restricted proofs, not interval certification, atomistic
simulation, external mathematical review or physical validation.

Primary-source URLs and actual read depths are in `PRIMARY_SOURCES.json`.
