# Autonomous momentum logic: constructed clock, failed hardware transfer

3 November 2026. Independent route, not an extension of the chiral-fermion work. **No civilisation-changing computing capability or same-resource advantage was obtained.** This pass built the central clock/gate mechanism rather than substituting a bibliography. It isolates an exact mathematical repair and the physical interaction that remains unearned. Novelty is not established.

## Intended capability and contract

The desired outcome was sustained reliable reversible classical computation at useful throughput with less TOTAL energy per useful operation than the strongest energy-recovery implementation at the SAME temperature, fabrication/interaction capabilities, device count, reliability, and rate. Below-Landauer work for a non-erasing gate is already allowed and is not the target breakthrough. Count preparation, clock distribution and stabilization, finite damping, refrigeration, read/write, fanout, reset and error-correction entropy. A single ideal NOT does not supply universal composable hardware.

The attempted missing operation was replacing an externally timed momentum-logic pulse by a finite-energy autonomous clock, while explicitly retaining backreaction of the gate on that clock. The main exact constructions are classical Hamiltonian models. No quantum computing advantage is claimed.

## Decisive primary source and present Astra check

Ray, Boyd, Wimsatt and Crutchfield, Physical Review Research 3,023164 (2021), https://journals.aps.org/prresearch/pdf/10.1103/PhysRevResearch.3.023164, pp.2–3, constructs NOT from a half-period harmonic rotation and Fredkin from commensurate normal-mode rotations. Its ideal pulse changes potentials and thermal coupling at externally specified times. The finite-damping simulation is not a physical account of a self-contained controller. This is the precise transfer attempted here; the source's logical construction itself is not new work by us.

Astra HEAD was pinned to d2eeaa1a421bd1f75748403ccc85e50351140ccb. A bounded current-record search located U1299-hamiltonian-clock-and-tube-constraint; its current packet and exact governing PROOF.md are saved. That source explicitly distinguishes formal Hamiltonian embedding from a physical clock and useful computation. Its near-harmonic Lyapunov/tube constraint is not a theorem about the clock below, and was NOT imported as one. No directly applicable momentum-logic operation was acquired from the searched record phrases. This was a phrase/operation check, not exhaustive semantic retrieval.

## 1. Built mechanism: an ordinary finite-mass traveling clock

Use a canonical target action-angle pair (I,phi), I>=0, and a clock position/momentum (s,P). The intentionally favorable autonomous Hamiltonian is

    H = P^2/(2M) + g(s) I.

The pulse g has compact support. Outside the pulse this model freezes the target; that favorable effective coupling is already stronger than an ordinary oscillator with fixed kinetic energy. It is therefore NOT a fabricated device model. On a transmitted positive-P trajectory with total energy E and E-Ig(s)>0,

    I_out = I_in,
    P_out = P_in,
    Phi(E,I) = sqrt(M/2) integral g(s)/sqrt(E-Ig(s)) ds.

Thus the clock returns its energy but acquires a data/action-dependent traversal time and produces an action-dependent rotation. Zero final clock work is not zero control disturbance.

### Unavoidable curvature for this architecture

At fixed E,

    dPhi/dI = sqrt(M/2)/2 integral g(s)^2/[E-Ig(s)]^(3/2) ds > 0

for any nonzero pulse. Signed pulse lobes cannot cancel this derivative. This is an exact model-level obstruction to an amplitude-independent phase rotation at finite E. It is NOT a no-go theorem for reliable digital gates: their acceptance regions have finite width, and increasing clock reserve can make errors small.

In physical time, dPhi/dI = integral g^2/(2K) dt, K=E-Ig. Cauchy-Schwarz gives

    dPhi/dI >= Phi^2 / [2 integral K dt].

The multichannel version H=P^2/(2M)+sum_j g_j(s)I_j has response matrix

    dPhi_j/dI_k = integral g_j g_k/(2K) dt,

which is positive semidefinite. Pulse shaping cannot remove every diagonal response while keeping a nonzero phase. Independent dummy loads can equalize a distribution but do not give a uniform cancellation for arbitrary realized actions.

### Numerical stress test, with all limitations explicit

`test_mechanism.py` uses exact top-hat scattering, not time-stepping, with 500,000 samples. Target q is initialized near +/-2 with Gaussian width 1/8 and p has unit Gaussian variance. This is the local harmonic approximation to a source-like double well, NOT its exact Gibbs law. Clock P=sqrt(2E0)+N(0,1), M=kT=g=1; pulse length is calibrated at mean action 2.50875. Reflections count as failures. Wrong output signs occur at rates 0.147242, 0.050506, 0.009724, 0.001044 and 0.000042 for E0=10,20,40,80,160. At E0>=320 no failures were seen: this only gives an approximately 6e-6 95% zero-count upper bound, not a high-reliability certificate. The derivative quadrature agrees with an independent finite difference to about 5e-14 absolute.

Stored E0 is NOT dissipation. Perfect Hamiltonian clock energy can be reused. Any claimed energy price must instead include damping, preparation, control/readout and reset. This calculation supplies no reason that a high-quality shared clock cannot amortize its stored energy.

## 2. Stronger actual repair: finite-reserve isochronous clock

Let a clock have action J>=0 and angle theta. Let chi(J) be smooth, zero for J<=1/2 and one for J>=1. Choose g(theta)>=0 smooth and periodic, and

    H = omega J + chi(J) g(theta) I.

This Hamiltonian is nonnegative. In Cartesian oscillator coordinates J=(Q^2+P^2)/2, the cutoff removes the angle singularity near the origin. In the operating annulus chi=1,

    theta_dot = omega,
    I_dot = 0,
    J_dot = -g'(theta) I,
    phi_dot = g(theta).

Starting at g(theta0)=0, choose J0 >= 2 + Imax max(g)/omega. For every 0<=I<=Imax,

    J(theta) = J0 - I g(theta)/omega >= 2,
    Delta phi = (1/omega) integral_cycle g(theta) dtheta,
    J_out = J0.

For omega=1 and g=(1-cos theta)/2, one cycle implements EXACT (q,p)->(-q,-p) for every target action in the admitted range; clock action and phase modulo 2pi return. This construction has finite reserve and bounded-below energy: it does not silently use H=P with unbounded negative momentum. Numerical integration at I=.1,1,5,20 verifies phase pi to <2e-11 and action restoration to <3e-11. The proof, not these finite samples, establishes the stated annular result.

An initial clock phase offset does not affect the integrated rotation over a full cycle, but identifying completion and retaining an output are separate interfaces. The gate repeats each cycle. The favorable target Hamiltonian freezes the target at zeros of g only instantaneously for this profile; a smooth zero plateau can be supplied, but physical stable storage and bath switching remain absent. Thermal distributions with unbounded action require a tail budget, never a finite all-state reserve.

This same action-angle trick can formally autonomize a supplied finite-energy time-periodic gate Hamiltonian on a bounded operating region: the clock action absorbs work while its angle advances uniformly. That is formal classical mechanics, not a new physical computer.

### Why the repair does not yet transfer to hardware

The interaction must depend on clock angle but NOT clock amplitude across a finite annulus. In oscillator coordinates it depends on normalized quadratures, e.g.

    cos(theta) = Q/sqrt(Q^2+P^2).

It therefore requires a nonlinear momentum-dependent coupling, not ordinary coordinate coupling. For a natural mechanical coupling V(Q,z), at fixed theta,

    partial_J V = [Q/(2J)] partial_Q V.

Requiring this to vanish for every J and theta in an open annulus forces the nontrivial clock-coordinate coupling to vanish there (up to special isolated points). This rules out exact implementation by that restricted coupling class, NOT by all circuits, magnetic interactions or effective Hamiltonians. A measured phase detector plus feedback cannot simply be declared free; its noise, power and delays must enter the same resource ledger.

The physical coupling that eliminates the curvature has thus NOT been acquired. No material/circuit with the required normalized-quadrature interaction and full energy/noise budget was built or identified in this pass.

## 3. Same-resource strongest comparison

The fair incumbent includes shared resonant AC power clocks and energy recovery, not an independent dissipative clock per bit or mandatory kT ln2 per reversible gate.

* Takeuchi, Yamanashi and Yoshikawa (2017), https://www.nature.com/articles/s41598-017-00089-9.pdf, explicitly models reversible QFP gates, gate-to-gate interactions, buffer stages and sub-Landauer dissipation as frequency falls. This already defeats novelty claims based only on reversibility or small ideal gate work.
* Chen et al. (2019), https://www.nature.com/articles/s41598-019-46595-w.pdf, uses shared multiphase AC excitation for both power and timing and provides circuit-level synthesis and gate energy modeling. Its historical performance forecasts are not assumed to be a current wall-plug benchmark.
* Herr, https://arxiv.org/html/2504.04284v1, explicitly treats interconnected-gate backaction and copy/termination mechanisms. Its device/error estimates are source-reported model claims, not measurements acquired here.
* Tang, Ray and Crutchfield, https://arxiv.org/abs/2602.07683, is an additional modern momentum-computing incumbent using coupled flux-parametron circuits. We did not reproduce its full simulation and do not claim to beat it.

For a resonant clock with energy Eclock, quality factor Qclock and N useful gates per cycle, an indicative loss allocation is 2pi Eclock/(Qclock N), before wiring, gate loss, cooling and correction. Both incumbent and candidate may share and reuse clocks. The candidate supplies neither physical Qclock nor an implementation cost for its angle-only coupling, so no numerical advantage ratio is warranted. In a fully ideal Hamiltonian comparator both can have zero dissipation; adding a formal clock cannot strictly improve on zero. At fixed nonzero temperature/damping, the candidate currently has no complete device specification to compare.

## Initial stop and next stronger operation

The parent then supplied a magnetic guiding-center bridge. Its additional construction and full Coulomb tests are in GUIDING_CENTER_TRANSFER.md. That follow-up earns an explicit approximate spatial action coupling, not the exact angle-only coupler or a same-resource advantage. The initial stopping analysis below applies to the direct oscillator implementation.

**Close this pass as a failed hardware transfer with an explicit mathematical central mechanism, not as an achieved new capability.** The finite-mass clock obstruction was repaired formally, but the repair moves the indispensable operation into a normalized-quadrature interaction and usable storage/read/write interfaces. Neither has been earned. More toy fidelity points would not settle that.

A justified reopening operation is concrete: construct a bounded passive circuit or mechanical/magnetic Hamiltonian realizing the angle-only interaction over a declared finite annulus, derive its actual Langevin/shot-noise dynamics and terminal I/O, then compare an entire repeated gate block with a shared-clock RQFP/adiabatic implementation at matched temperature, throughput, error probability, component count and wall-plug energy. A synthesized feedback controller must be counted, not treated as an oracle. If no such physical interaction is available, reject this opening rather than extending the formal embedding.
