# ASTRA | Radiative-rank, finite-time return, and loss-speed constraints

27 October 2026. Foundational-physics continuation. Mathematical derivations and actually executed source files in `astra_bridge_topology/`. The Hamiltonians, controls, preparation assumptions, and numerical scopes below are deliberately separate. These are *constructed-model* results; there is no experimental measurement, Maxwell-complete realization, or historical priority claim.

## I. Research decision and independently informed alternative

The incumbent low-exposure bridge uses a buffer `a`, lossy intermediate `e`, and storage `b`, with a single 2-edge chain and `sqrt(g(t)^2+J(t)^2) <= Omega`. It exactly transfers one photon and can make intermediate population arbitrarily small by allowing a longer transfer. However, low loss in `a` and `b` eventually limits that approach. The question is not another numerical pulse improvement: **what exact physical resource permits final emitted radiation to vanish at finite time?**

Two independent alternatives are studied against that same contract: (1) a third, complex `a-b` control edge implementing counterdiabatic dark transfer; (2) two intermediate emitters whose antisymmetric superposition is dark to one *collective* radiation bath, using only real 2-edge hoppings. Both preserve positive one-body operators, with a permanent, explicitly positive and gapless radiation Jacobi bath. Each architecture makes a different additional resource available; neither is silently assigned to the original 2-edge interface.

Counterdiabatic STIRAP, dark-state transfer, speed-cost tradeoffs, and collective subradiance have strong prior art. Relevant direct antecedents include Chen and Muga, PRA 86 033405 (2012); Giannelli and Arimondo, PRA 89 033419 (2014); Baksic, Ribeiro and Clerk, PRL 116 230503 (2016); and experimental superconducting three-level transfer (2019). The current work is the conditional finite-time **radiation-kernel/entire-Fourier theorem**, unconditioned loss-speed comparison, positive gapless-bath completion, and independently executed full joint-state operations, with their exact interface scope.

## II. All-protocol loss-speed inequality (new no-occupancy-cap proof)

Let `P=span{|a>,|b>}`, `Q=P^perp` and a normalized one-photon trajectory solve a self-adjoint, possibly time-dependent Hamiltonian on `P+Q`. The local `PHP` dynamics is diagonal in `a,b` (so no bypass), and `||P H(t) Q|| <= Omega` at all times. The initial and final states are `|a>` and `exp(i alpha)|b>`. Write `q(t)=||Q psi(t)||^2` and `A=int_0^T q(t) dt`.

Remove the independent `P` local phases by the unitary propagator of `PHP`. The remaining two-component `x(t)` satisfies `||dot x|| <= Omega sqrt(q)`. The two endpoints are orthogonal unit vectors even after their local phase rotations; hence

    sqrt(2) <= ||x(T)-x(0)|| <= Omega int_0^T sqrt(q(t)) dt
             <= Omega sqrt(T A).

Therefore

    A T >= 2 / Omega^2.                                          (1)

This result needs **no maximum-occupation assumption**. It is weaker than the previous Fubini-Study `pi^2(1-epsilon)/(4 Omega^2)` inequality when `max q<=epsilon` is small, but is valid for arbitrary occupancy of any-dimensional `Q`.

Let both `P` modes have weak Markov loss rate `kappa_p>0`, and suppose `Q` has loss rate at least `kappa_e>kappa_p` for every normalized `Q` excitation. The *ideal-unitary trajectory* has integrated leading-order emission hazard

    L = int_0^T [kappa_p (1-q(t)) + kappa_e q(t)]dt
      = kappa_p T + (kappa_e-kappa_p) A.

Using (1) and minimizing over `T>0` gives

    L >= 2 sqrt[2 kappa_p (kappa_e-kappa_p)] / Omega.             (2)

For unequal `a,b` loss, (2) remains valid with `kappa_p` replaced by `min(kappa_a,kappa_b)` if the mediator loss operator is bounded below by `kappa_e I_Q`. **Do not** interpret (2) as an exact radiation bound for an arbitrary frequency-dependent *closed* continuum: coherent radiation is spectrally nonlocal in time. Its precise meaning is the ideal-path Markov loss functional / first term in weak-decay expansion.

### Exact near-saturating path and optimization

The existing three-stage 2-edge transfer (one positive common onsite shift `mu >= Omega+1` makes every instantaneous 3x3 matrix positive) uses a parameter `0<phi<pi/2`. It has

    T(phi) = pi/[2 Omega tan(phi)] + 2 phi/Omega,
    A_e(phi) = [pi sin(phi)cos(phi)/2 + phi - sin(2phi)/2]/Omega,
    A_a(phi) = A_b(phi)
             = [phi/2 + sin(2phi)/4 + pi cos^3(phi)/(4 sin(phi))]/Omega.

Exactly `2 A_a+A_e=T`. This verifies the occupation accounting across all three stages; the earlier note only gave `A_e`. The dose is `kappa_p(2A_a)+kappa_e A_e`, which can be optimized by a one-dimensional scalar minimization without approximating the trajectory.

At `Omega=10`, `kappa_p=10^-6`, `kappa_e=2x10^-5` (in binding-energy units), the executed optimum is

    phi = 0.22803531760
    T = 0.72246461939,
    A_e = 0.03537314531,
    A_a = A_b = 0.34354573704,
    L_exact_ideal = 1.39455438036e-6,
    universal_lower = 1.23288280059e-6,
    ratio = 1.13113296713.

For `kappa_p/kappa_e ->0`, the optimal small-`phi` asymptotics give `phi ~ sqrt[kappa_p/(kappa_e-kappa_p)]` and `L ~ pi sqrt[kappa_p(kappa_e-kappa_p)]/Omega`. The universal-to-constructive factor tends to `pi/(2 sqrt 2)=1.11072...`: this simple chain construction is within about 11.1% of the universal lower bound in the high-loss-contrast regime. This is an **asymptotic within-factor result**, not a claim of globally exact loss-optimal control.

### Weak-loss state-vector error, with an explicit remainder

For one excitation and a time-dependent Markov no-jump generator `-iH(t)-Gamma/2`, assume `0<=Gamma<=kappa_max I`. Let `psi_0` be the ideal trajectory and `psi_nj` the no-jump trajectory, initially identical. With mutually orthogonal environmental photon outputs, the complete one-photon-plus-environment pure-state error satisfies

    epsilon^2 = P_jump + ||psi_nj(T)-psi_0(T)||^2.

Duhamel gives `||psi_nj(t)-psi_0(t)||<=kappa_max*t/2`. Comparing actual and ideal jump-rate integrals yields

    |epsilon^2 - int_0^T <psi_0,Gamma psi_0>dt|
       <= (3/4)(kappa_max T)^2 + (1/12)(kappa_max T)^3.         (3)

Equation (3) explains precisely when (2) bounds a physical state-vector error to leading order. It is not an invocation of postselection or a ratio of successful shots.

For two optimized transfers plus a `pi` storage hold with `kappa_b=kappa_p`, the complete executed no-jump output gives

    total local-gate time = 4.586521892,
    first-order dose = 5.930701414e-6,
    root-0 full-state error = 0.002435301315,
    root-1 full-state error = 0.002435301341,
    rigorous absolute remainder allowance on error^2 = 6.31e-9.

Photon production, original Jacobi capture/release and memory-flag preparation are *not* included in this local-gate comparison and must be added separately.

## III. A stronger continuum theorem: emitted radiation cannot all return at finite time

Consider a fixed radiation Hilbert space `H_rad = L^2(I,domega) tensor K`, with free Hamiltonian multiplication by `omega`, initially vacuum in the one-photon sector. Suppose finite-dimensional emitter amplitudes `q(t)` couple to the bath through

    (W q)(omega) = v(omega) R q,

where `R:C^d -> K` is time independent, and `|v(omega)|>0` almost everywhere on some nonempty open interval `I0 subset I`. The internal Hamiltonian may be arbitrary and time dependent; assume only that the total evolution is well-defined, the coupling is bounded/finite-energy, and the transfer takes finite time `T`.

The exact radiation amplitude at the end is

    psi_rad(omega,T) = -i v(omega)e^{-i omega T}
                          int_0^T e^{i omega t} R q(t) dt.       (4)

Each component of the Fourier integral in (4) is an **entire** function of complex `omega`, since `R q(t)` has support in the finite interval `[0,T]`. If the final radiation sector is *exactly vacuum* across a nonzero frequency interval, the identity theorem for holomorphic functions and uniqueness of the Fourier transform require

    R q(t) = 0  for almost every t in [0,T].                    (5)

This is stronger than the instantaneous condition for remaining radiation-vacuum at every time: **even coherent reabsorption at the final time cannot perfectly erase broadband radiation unless the emitter trajectory is in the common radiative kernel throughout.**

In particular, if `R` has full column rank, then `q(t)=0` a.e.; with no `a-b` bypass, exact finite-time `a->b` transfer and exact final radiation vacuum cannot both occur. If `ker R` is nonzero, (5) gives a necessary condition, not an automatic controllability theorem. A factorized shared-bath example below supplies sufficiency at this interface.

This theorem is about a stationary, freely propagating continuum with frequency-separable `v(omega) R`. For general nonfactorizable `W(omega)`, simultaneous spectral-kernel properties need their own analysis; in particular, on-shell scattering cancellation need not imply a time-independent dark state. A finite discrete bath is a decisive counterexample to careless generalization: a two-state emitter/radiation Rabi system returns all radiation to vacuum after `pi/g` despite fully populating that radiation mode transiently.

### A crucial quantitative limitation

Strict positive radiation leakage does **not** imply a uniform lower bound proportional to emitter population-time when the control phase/frequency is unrestricted. In the scalar continuum `|v|^2=eta^2>0` on `[0,W]`, take

    q_M(t)=sin(pi t/T) exp(-i M t),  0<=t<=T.

Every `q_M` has the *same* occupation-time `T/2`. Yet its entire Fourier transform is explicitly

    F_M(omega)=a[1+exp(i(omega-M)T)]/[a^2-(omega-M)^2],
    a=pi/T.

For `M>W+a`,

    P_rad(T) <= eta^2 W [2a/((M-W)^2-a^2)]^2 = O(M^-4).        (6)

Therefore a meaningful *quantitative* radiation floor requires an additional bound on control energies, modulation bandwidth, smoothness, or temporal control dimension. The shift `M` is an ever-increasing **physical frequency/control resource**; (6) is not a free no-loss device.

In any **fixed finite-dimensional** temporal control subspace, the radiation Gram operator formed from (4) is strictly positive definite because a nonzero finite-time Fourier transform cannot vanish on a full frequency interval. The smallest Gram eigenvalue is therefore a valid subspace-dependent leakage certificate. Its value can approach zero as the control family becomes richer. Executed sine-basis quadrature yields minimum eigenvalues `2.56e-2` (dimension 1), `2.88e-5` (dimension 3), and `5.11e-10` (dimension 5), at `eta=.1`, `T=1`, `W=4`. Values for larger bases become roundoff-sensitive and are not reported as rigorous numerical lower bounds.

## IV. Two distinct physical escapes, each with declared extra resources

### A. Three-edge counterdiabatic bypass — exact zero emitter/radiation at all times

Let `|D(theta)> = cos(theta)|a> + sin(theta)|b>`. On the 3-mode subspace set

    H_chain = g(theta)(|a><e|+h.c.) + J(theta)(|e><b|+h.c.),
    g=Omega sin(theta), J=-Omega cos(theta),
    H_cd = i dot(theta) (|b><a|-|a><b|).

The chain annihilates `|D>`, and `H_cd |D>= i d|D>/dt`. Thus for an arbitrary smooth `theta(0)=0`, `theta(T)=pi/2`,

    psi(t) = exp(-i mu t)|D(theta(t))>

solves the exact Schrödinger equation for `H=mu I+H_chain+H_cd`. Its intermediate emitter occupation is **identically zero**, not merely of order `1/T`. For a permanently coupled radiation continuum, the emitter-to-radiation source is identically zero as well, so the complete radiation state remains vacuum *for any value of its coupling* compatible with the positive Hamiltonian.

For a smooth profile `theta(t)=pi[1-cos(pi t/T)]/4`, `max|dot theta|=pi^2/(4T)`. The instantaneous 3x3 off-diagonal spectrum is `{0,+sqrt(Omega^2+dot theta^2),-sqrt(Omega^2+dot theta^2)}` (the complex third edge has a nontrivial Peierls phase). A common onsite shift

    mu >= sqrt[Omega^2 + (pi^2/(4T))^2] + 2 eta^2/w + delta

makes the system strictly positive, even when `e` is permanently coupled with strength `eta` to a positive Jacobi radiation half-line of onsite energy `w` and hopping `w/2`. The radiation endpoint inverse at zero is `2/w`; the resulting lower Schur margin is at least `delta`.

For `Omega=10`, `T=.5`, `w=11`, `eta=.0074162`, the executed controls have

    max counterdiabatic direct hopping = 4.93480220,
    common onsite mu = 12.16134502,
    proved local Schur margin >1.0099.

The **full finite photon+gapless-radiation calculation** retained 64 signal sites, 24 radiation sites, source support 16 sites, exact Jacobi capture and release, both conditional-storage phase branches, and permanent radiation coupling. It returned

    full two-root conditional-sign error = 1.86e-10,
    max final radiation+intermediate population = 1.16e-20,
    full operation time = 9.00936.

The nonzero residuals reflect finite source truncation and numerical integration. Exact zero radiation in the ideal transfer follows *analytically* from the invariant subspace and persists in the infinite radiation half-line.

**Explicit new resource:** an independently controllable complex `a-b` edge, with a gauge-invariant nontrivial loop phase. If the two original bridge edges and onsite potentials are all real and the instantaneous dark state is real, exact finite-speed following of that moving state is impossible without a suitable imaginary tangent generator. Counterdiabatic direct coupling is known prior physics, not newly invented here. The original two-edge lower bound is not contradicted because the bypass violates its `PHP` no-mixing condition.

### B. Two radiating intermediates, one dark collective mode — no direct bypass

Replace `e` by `e1,e2`, and let the radiation bath couple to the symmetric state `e+=(e1+e2)/sqrt2`. Use opposite-signed, **real** source and storage hoppings to address `e-=(e1-e2)/sqrt2` only. The controlled Hamiltonian in the invariant subspace `span{a,e-,b}` is exactly the previous two-edge bridge, while the radiation bath sees **only** the orthogonal bright state `e+`. Thus there is exact transfer with nonzero `e-` occupation but exactly zero radiation, at any finite operation time admitted by the hopping bound. The positive onsite shift covers the collective-bath Schur term.

Executed smooth protocol: `Omega=10`, `Phi=.23`, `T=1.788985245`, strong common radiation coupling `eta=2` to a 28-site approximation of a gapless Jacobi bath `[0,22]`. The calculated final common-radiation population was `2.69e-32`, despite peak population of about `5.2%` in the mediator dark superposition. The full state-transfer error was `2.67e-11`, and the Schur positive margin at least `1.1`.

This protection **does not survive truly independent radiation**. If each emitter also couples to a separate bath with amplitude `.2`, the full-system radiation probability after a single transfer was `4.99e-4` and state-transfer error `0.02234`. If source-coupling asymmetry is `1%` but the radiation coupling remains exactly symmetric, common-radiation leakage was `7.39e-7`, with additional coherent-transfer error.

The conceptual distinction is the **radiative rank** of the fixed spectral source map `R`:

- A shared bath supplies `R proportional (1,1)`, with nontrivial kernel `span(1,-1)`; exact emission-free mediation is possible because that kernel is dynamically invariant.
- Adding independent radiation supplies extra linearly independent rows; `R^*R` becomes strictly positive, and the exact finite-time no-radiation theorem excludes a perfect two-edge transfer without a bypass or further shielding.
- Frequency-dependent which-emitter information can also destroy a common spectral kernel, even if each individual frequency channel looks rank-deficient.

The two-mediator construction requires **correlated loss**, phase-opposed couplings and matching local energies. It does not eliminate ordinary independent free-space emission.

## V. Physical claim boundary and next strongest attack

1. **Proved for declared Hamiltonians:** unconditional two-edge Markov exposure inequality, exact three-stage occupation integrals, continuum unique-continuation/no-perfect-return theorem, exact complex-bypass and collective-dark constructions, positive-energy completion and resulting all-particle nonbinding capacity under the prior conserved-memory assumptions.
2. **Executed numerical, not proved hardware fidelity:** near-saturation and no-jump errors; finite-site full photon/radiation propagation; symmetry-breaking and independent-bath diagnostics. The exact radiation-dark identities do not rely on finite-site numerics.
3. **Important counterexamples:** finite discrete radiation permits coherent complete return, so continuum support matters; high-frequency control can suppress radiation arbitrarily without changing occupation-time, so quantitative loss floors need an additional energy/bandwidth contract; collective darkness fails under independent radiation.
4. **Unacquired interfaces:** a physically realizable complex direct hopping (and its phase/drive costs), or nearly perfectly collective microscopic radiation for two accessible mediators; full Maxwell modes and correlated loss, lossless input source, finite-temperature populations, calibrated conditional storage interaction, and all control slew/work. Neither architecture proves superiority over existing STIRAP/quantum-memory practice.

The meaningful next physics problem is to derive the *radiative source matrix* `W(omega)` from one realistic electromagnetic or solid-state platform, quantify its smallest singular direction over the photon bandwidth, and prove a lower bound on leakage **with the actual accessible control-energy/bandwidth constraints**. That decides whether either topology offers a physical capability beyond ideal-model controls.

## VI. Reproducibility and source scope

Executed in the current container with NumPy/SciPy. Scripts and JSON in `astra_bridge_topology/`:

- `loss_frontier.py`, `loss_frontier_results.json`: exact loss-speed optimizer, comparison across loss contrasts, independent no-jump whole-state check and rigorous remainder.
- `counterdiabatic_bypass.py`, `counterdiabatic_bypass_results.json`: analytic time-dependent dark identity, real-space positive Schur bound, full finite-signal-plus-permanent-radiation complete conditional photon operation.
- `radiative_rank_bridge.py`, `radiative_rank_results.json`: shared-radiation dark mode, strong gapless coupling, broken symmetry and independent radiation counter-tests, radiative Gram eigenvalues.
- `continuum_no_echo.py`, `continuum_no_echo_results.json`: explicit complete radiation Fourier transform and `O(M^-4)` bound, discrete-bath Rabi revival counterexample.
- `temporal_radiation_gram.py`, `temporal_radiation_gram_results.json`: time-domain Fourier-Gram diagnostic and precision warning.

Source basis: `ASTRA_BRIDGE_EXPOSURE_TRADEOFF_20261027.md`, `ASTRA_FINITE_TIME_JACOBI_FLAG_GATE_AND_LOSS_20261026.md`, and the source scripts in `astra_bridge_transfer/`. No permanent research repository mutation or experimental assertion is made.

## VII. Next executed attack: free-space vector-dipole compatibility

The exactly shared-radiation two-emitter mechanism must not be interpreted as an ordinary pair of separated electric dipoles: at any finite separation, the free-space electromagnetic field acquires which-emitter phase information. Moreover, its real Green tensor produces a coherent dipole-exchange shift that the abstract dark model previously left tunable independently.

In the usual point-dipole, Born-Markov, rotating-wave free-space model, let `x=k0 L`, `c2=cos^2(angle between dipole and separation)`, `Gamma` be the **single-atom population decay rate**, `Gamma12` the cooperative decay, and `Omega12` the coherent dipole exchange. The standard vector Green tensor gives

    Gamma12/Gamma = (3/2)[(1-c2)sin(x)/x
                           +(1-3c2)(cos(x)/x^2-sin(x)/x^3)],
    Omega12/Gamma = (3/4)[-(1-c2)cos(x)/x
                          +(1-3c2)(sin(x)/x^2+cos(x)/x^3)].

The antisymmetric mode has population decay `Gamma_dark = Gamma-Gamma12`. At small separation:

    perpendicular dipoles: Gamma_dark/Gamma = x^2/5+O(x^4),
                           Omega12/Gamma = 3/(4 x^3)+O(1/x),
    parallel dipoles:      Gamma_dark/Gamma = x^2/10+O(x^4),
                           Omega12/Gamma = -3/(2 x^3)+O(1/x).

Thus suppressing independent radiation by shrinking the pair **necessarily increases the coherent near-field exchange as x^-3**. Equivalently the product `(Gamma_dark/Gamma)^(3/2) * |Omega12|/Gamma` approaches the strictly positive orientation-dependent constants

    perpendicular: 3/[4*5^(3/2)] = 0.067082..., 
    parallel:      3/[2*10^(3/2)] = 0.047434....

This is a physical control **tradeoff**, not a universal no-go: the coherent exchange might be compensated by detunings or incorporated into a dressed Hamiltonian, with its magnitude and calibration counted.

For the existing *smooth* two-transfer bridge, `A_dark,total = 0.07007067328/B`. As a model-specific first-order necessary loss-only condition for 1% coherent full-state error, require `Gamma_dark * A_dark,total < 10^-4`. Setting `Gamma/B=1`, the executed exact Green-function formulas give

    perpendicular: k0 L <= 0.08448895, |Omega12|/B >= 1239.13;
    parallel:      k0 L <= 0.11949303, |Omega12|/B >=  885.41.

For `Gamma/B=.1`, the corresponding exchange magnitudes drop to `3.78B` and `2.95B`. These are *conditional* scale examples. They exclude buffer and storage loss, capture/release, preparation, emitter frequency noise, finite-pulse corrections and the actual Maxwell waveguide structure; the weak-Markov target is not an independently certified complete 1% device.

`free_space_dipole_tradeoff.py` evaluates the complete trigonometric expressions at 60-digit precision and saves `free_space_dipole_tradeoff_results.json`. This is the substantive new physical constraint on the collective-dark proposal. It also explains why the earlier real-3-site Hamiltonian with a perfectly shared bath does not yet establish an experimental interface for ordinary separated emitters.

Relevant established source: Lehmberg-type cooperative decay and coherent exchange for two free-space electric dipoles; see the independently published formulas in Scientific Reports 11, 2021, article 99449 and the 2025 *Light: Science & Applications* electromagnetic Green-tensor treatment. The formulas, and subradiance itself, are prior physics; their quantitative role as a constraint on the specific Astra bridge is the scoped inference here.
