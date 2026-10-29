# Local operations that select collective transport

## The physical consequence chosen

The completed construction couples two systems' net transport while allowing
their spatial densities to relax independently. It retains a common current
that can carry work against a load. Local reciprocal memory dynamics supplies
the connection, without an event-wide selector, initially correlated distant
memory, or an external switching clock in this new architecture.

The result is proved for specified harmonic native systems. It includes their
nonflat density histories and joint current large-deviation law. It does not
assert a device, nonlinear particle-system generality, practical speedup, or
historical priority.

The strongest next attack changed the target again: with density-dependent
mobility, a force-only current constraint generally changes rare density
histories. Preserving those histories requires a different actual port. The
saved nonlinear partial theorem and conventional transformer comparison make
that frontier concrete.

## 1. The operation and its actual resources

Two separate periodic carrier rings have signed harmonic densities x_1,x_2,
unknown positive resistances r_1,r_2 constant within each ring, fixed positive
inertia tau, and independent matched thermal baths. Their actual current is

    tau dv=-(B*x+Rv+gq)dt+fdt+sqrt(2R)dW,    dx=Bvdt.

The new local memory dynamics is

    dq=(gv-aA*p)dt,
    dp=(aAq-gamma AA*p)dt+sqrt(2gamma)A dV,
    A=[[B_N,0],[0,-B_N],[I,I]].

The signed ladder connects neighboring memory cells and colocated cells
across the rings. It leaves one protected direction
h=(1_N,-1_N)/sqrt(2N), giving the exact trajectory identity

    J_1,tot(t)-J_2,tot(t)=sqrt(2N)/g [h*q(t)-h*q(0)].

The common current has no endpoint restriction. Unlike pointwise gearing,
the operation does not freeze x_1-x_2: the wave transports the counter memory.
The useful scaling is

    kappa_N=g_N^2 ->0,       N^2 kappa_N ->infinity.

All local coefficients, ranges and degrees are bounded. The product thermal
auxiliary preparation, weak reciprocal tap, conservative relative damping,
matched noise and physical force port are real supplied operations. The
displacement counter q/g pays range/compliance or gain precision. Gaussian
amplitudes are unbounded. Fixed inertia gives finite native response, while
the voltage-noise model remains white. This is not a hard bandwidth or
amplitude guarantee for hardware.

## 2. The complete transport law

From two specified smooth nonflat initial profiles, each density obeys its
native macroscopic heat equation, rho_(a,t)=r_a^(-1)rho_(a,xx). More strongly,
the complete density histories in the stated weak continuous-path topology
are exponentially equivalent at speed N to the two independent native heat
histories. Finite-N microscopic density processes remain coupled.

On physical time N^2t,

    (J_1,tot,J_2,tot)(N^2t)/N^(3/2) => (Z_t,Z_t),
    Z_t=sqrt[2/(r_1+r_2)] W_t.

The common Brownian channel is independent of both limiting density fields.
The difference current is superexponentially small at the macroscopic N^2
scale over the whole observation horizon. The full speed-N joint rate is

    I=sum_a (r_a/4) int dt dx [j_a+r_a^(-1)rho_(a,x)]^2

on continuity, the specified initial profiles, and
`int j_1 dx=int j_2 dx` almost everywhere; it is infinite otherwise.
Contracting over current leaves the two ordinary independent density actions.

The proof combines a corrected-momentum identity, a forward/backward
additive-functional estimate needing no hidden mixing, passivity, and the
actual Gaussian path law. It does not infer an action from a non-Gaussian CLT.

For actual uniform native forces f_(a,i)(s)=F_a(s/N^2)/N, the common current is

    I_0(t)=[F_1(t)+F_2(t)]/(r_1+r_2).

The initial charging transient is included. Its forced common rate is
`(r_1+r_2)int(I-I_0)^2dt/4`, with minimum zero. For F_1>0>F_2 and positive
sum, system 1 drives transport against system 2's load. This is ordinary
tight-coupling work at the declared native interface, not a new efficiency law.

The complete theorem is `SELECTIVE_TRANSPORT_COUPLING_AND_ACTION.md`. Its
actual-file review in `physical_mechanism/receiving_review` accepts the
corrector, Gaussian whole-path argument, full action, force normalization and
work accounting without correction.

## 3. Unknown hidden linear memory can be retained

The general receiver permits an unknown causal passive impedance, including
noncommuting linear hidden memory, with warranted in-band coercivity and norm
bounds. A finite hidden model need not first be identified. The local
controller approaches the native impedance restricted to the allowed current
subspace. Mean response and the complete stationary Gaussian noise spectrum
approach that target together.

For the smallest positive eigenvalue lambda of A*A, a diffusive band
Omega=O(lambda) permits lambda<<kappa<<1. Choosing kappa of order sqrt(lambda)
gives an O(sqrt(lambda)) response bound with fixed positive wave speed and
warranted native bounds. The observer's band lies below the controller's
communication frequency. This controls a native metric constraint, not an
arbitrary numerical conductivity independent of native kinetics.

A finite measurement-vector TV bound additionally needs the actual sensing
noise/precision and complete force/filter interface. Review caught a missing
out-of-band premise: finite-duration filters can see an unmeasured resonance.
The accepted correction requires global coercivity or an outside spectral
envelope, or zero outside filter mass. A noiseless exact constraint record
can remain singular even when in-band response error is small.

Read `LOCAL_PASSIVE_LAW_REALIZATION.md` together with its separate correction.

## 4. Prepared covariance and fresh response are different resources

For bounded local linear dynamics, the remote response to a fresh force is
bounded by a matrix-exponential tail. Before time proportional to physical
distance, it is exponentially small in that distance. Arbitrary prepared
covariance cancels from the forced-versus-unforced mean comparison under the
same preparation and future bath law.

On the fixed ring/ladder metric, the ideal collective constraint responds
remotely at once; a local realization needs order-N startup communication.
Diffusive time N^2 leaves room for that communication. This explains why the
long-scale law is attainable without treating prepared correlation as a new
communication channel.

The proof concerns its bounded linear generator and every actual physical
link. It is not a hard light cone or a frequency-domain minimax theorem. Its
original, geometry/gain clarification and actual review are preserved.

## 5. The nonlinear attack changed the next operation

An actual exclusion hop accompanied by a local Gaussian-field shift, with
energy-consistent Metropolis rate, gives product invariance and a collective
current counter without a global event bit. With an actual exp(CN) initial
density ceiling and bounded event rate, the whole-horizon current tail is
superexponentially small at speed N when N^2 kappa_N diverges. This is a
non-Gaussian theorem.

The nonlinear density/action receiver remains unproved. The broad reciprocal
hidden-rate class first needs a warranted native hydrodynamic interface.
Even for ordinary exclusion, the Gaussian independent-density objective needs
revision. For native mobility M and protected directions H, a force-only
constraint gives

    M_c=M-MH(H*MH)^(-1)H*M.

Density noise is unchanged exactly when BMH=0. Density-dependent mobility
generally fails that condition even though BH=0 and typical heat survives.
An explicit traveling-profile calculation gives a strictly positive extra
density-history cost when the two freely optimal circulating currents differ.

A conventional two-sided transformer instead gives Q M Q, with Q removing
the protected directions. Since BQ=B, it preserves density response and noise.
But transforming an apparatus output does not change the original native
carrier current: actual flow interposition or additional carrier transport
is required. Ordinary transformer machinery already solves the task when
that stronger port is supplied.

The root identifies the extra matched current channel explicitly:

    Q M Q-M_c=U U*,       U=QMH(H*MH)^(-1/2).

It has rank at most the number of protected directions. Supplying its native
transport, reciprocal response and matched noise restores the stronger density
objective for constant mobility. Only MH enters this compensation, suggesting
a focused acquisition target. Neither that acquisition nor the generally
extended actuator has been supplied for the nonlinear particle system.

Read `MOBILITY_GEOMETRY_AND_OPERATION_CHOICE.md`, the independent variational
calculation in `record_geometry`, and the actual two-sided transformer
comparison in `physical_mechanism`. Their source and receiving records make
clear that the projection/order machinery has direct predecessors, including
the shorted operator. A sharper counter endpoint does not supply the missing
port or nonlinear receiver.

## 6. Evidence, credit and preserved boundaries

Executed root code checks a full hidden-state realization against eliminated
response/noise formulas, the selective two-ring receiver and marked particle
balance. The maximum full-resolvent discrepancy is about 3.90e-9; the thermal
noise identity residual is below 1.71e-15. These are population checks.
`VALIDATION.md` records exact outputs, commands, reviews and corrections.

Passive RLC networks, robust integral control, constrained Langevin methods,
Gaussian path large deviations, classical propagation bounds and local
particle-field counters have close primary predecessors. The ordinary
reciprocal wave alternative changed the original attack; Maggs--Levrel
preempted a broad particle-field novelty claim. The candidate addition is
the explicit local operation/receiver/resource composition. Priority remains
unresolved. `PRIMARY_CONSTRUCTION_COMPARISON.md` records the actual reads.

All previous scientific assets, actual reviews, accepted dependencies and
failures are preserved unchanged. Retained-record conditioning must preserve
the complete future law. A calibration failure probability is not promoted to
a rare-history certificate; later preparation does not supply first baseline
calibration. No end-to-end acquisition budget, manufactured apparatus or
practical speedup has been established.
