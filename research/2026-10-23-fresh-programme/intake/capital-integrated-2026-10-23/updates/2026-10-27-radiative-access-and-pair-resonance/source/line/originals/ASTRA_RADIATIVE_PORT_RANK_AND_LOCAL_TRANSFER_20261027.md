# Radiation-port rank, bounded-rate transfer, and a positive local waveguide construction

27 October 2026 — Astra interim foundational-physics research. Independently derived from the radiative-cut handoff and executed source code. The numerical transfer figures are full-state **model** diagnostics, not experiments or machine-checked interval certificates. All energy units use `B=1`.

## 1. Scientific choice and comparison

The incumbent four-emitter Fourier-null sources cancel terminal radiation algebraically, but the particular histories fail the strictly local Schrödinger equation because fixed broadband backaction drives inactive nodes. The previous weak-coupling no-bypass theorem bounds twelve-time-unit transport to at most about 0.518% probability. The question is whether a *real local waveguide bus*, rather than an artificial internal storage-to-storage bypass, supports coherent transfer while preserving spectral positivity and explicitly including an environmental continuum.

A genuinely different alternative is a time-dependent *chiral* continuum. Its single output channel removes the reciprocal two-port radiation-rank obstruction, but requires a direction-selective physical interface; contemporary giant-atom and dispersion-engineered proposals already explore such interfaces (Diekmann et al., PRX Quantum 7, 043013 (2026), DOI 10.1103/6wcb-nj42; Kuang et al., PRL 137, 103605 (2026), DOI 10.1103/m2md-rxkv). Both alternatives are pursued here, with the finite local Jacobi waveguide selected as the stronger physical-topology result.

## 2. An exact terminal-radiation rank theorem

Consider `n` dynamically controlled radiating sites and `M` independent continuum output channels. On an open positive-frequency interval `I`, assume the frequency-domain coupling matrix `V(omega)` is continuous, fixed in spectral shape, and may be multiplied by arbitrary bounded time-dependent scalar control envelopes at its individual source sites. Let the *effective* source amplitudes `q_j(t)` be integrable and supported in `[0,T]`. The final field from initially empty continua is, up to a nonzero scalar factor,

    xi(omega,T) = exp(-i omega T) V(omega) Q(omega),
    Q_j(omega)= integral_0^T exp(i omega t) q_j(t) dt.

**Theorem (full-column-rank obstruction).** If `V(omega)` has column rank `n` almost everywhere on a nonempty open subinterval of `I`, exact radiation vacuum at `T` implies `q_j(t)=0` almost everywhere for all `j`.

**Proof.** `V(omega)Q(omega)=0` almost everywhere by the terminal-vacuum hypothesis. Full rank gives `Q(omega)=0` almost everywhere on a subinterval. Each `Q_j(z)` is an entire function of exponential type at most `T` (integrate the compactly supported source against `exp(i z t)`). By continuity and the identity theorem it vanishes identically. Fourier inversion gives `q_j=0`. This is a **source necessary condition**; a nontrivial Fourier-null source in a rank-deficient interface must still satisfy the full local Schrödinger equations.

For exactly two distinct emitters at `x_1 != x_2`, coupled to both reciprocal directions with the same nonzero spectral envelope,

    V(omega) ~ [[exp(+i k(omega)x1), exp(+i k(omega)x2)],
                [exp(-i k(omega)x1), exp(-i k(omega)x2)]].

Its determinant is proportional to `sin(k(omega)(x2-x1))`. Provided the propagation phase is not identically constant at an integer multiple of pi over an open band, the determinant is nonzero almost everywhere there. **No nontrivial finite-duration pair of effective sources can exactly return *both* continua to vacuum.** This holds even with arbitrary onsite or coupling-envelope control, under the fixed spectral-port assumptions. It does *not* preclude arbitrarily accurate approximate transfer, extra emitters, mirrors, a genuine discrete cavity bus, or chiral coupling.

For contrast, one chiral direction has only one radiation equation. Two separated ports can have `Q_R(omega)=-exp(i omega tau)Q_L(omega)` in a linear-dispersion model; in time this is the permitted shifted cancellation history `q_R(t)=-q_L(t-tau)`. A nonzero history must fit inside the available time window. These algebraic histories alone do not guarantee physical local excitation dynamics.

## 3. A bounded-rate chiral construction and its limitation

The standard ideal chiral Markov *one-photon* cascade has source amplitude `a(t)`, receiver amplitude `b(t)`, separation time `tau`, and controllable rates `0 <= gamma_j(t) <= Gamma`. Up to a calibrated propagation phase,

    a'(t)= -gamma_L(t) a(t)/2,
    b'(t)= -gamma_R(t) b(t)/2
            -sqrt(gamma_R(t) gamma_L(t-tau))a(t-tau).

Take `A=x/Gamma`, `gamma_L(t)=Gamma/(1+exp(-Gamma t))` on `[-A,A]` and zero outside, and `gamma_R(t)=Gamma/(1+exp(Gamma(t-tau)))` on `[-A+tau,A+tau]` and zero outside. Starting with the left excitation, the *exact* final amplitudes/probabilities are

    b(A+tau)= -(1-exp(-x)),             (propagation phase suppressed)
    P_L=exp(-x),
    P_R=(1-exp(-x))^2,
    P_waveguide=exp(-x)-exp(-2x),
    ||psi_target-psi_actual||=sqrt(2 exp(-x)).

Derivation: `a(t)=sqrt((1+exp(-x))/(1+exp(Gamma t)))` on the sender window. Insert into the receiver's integrating-factor solution; the remaining integral is the exact derivative of `exp(Gamma t)/(1+exp(Gamma t))` and gives `b=-(1-exp(-x))`.

This gives a bounded-control, complete-output, reference-compatible near-perfect *one-way* transfer with duration `2x/Gamma+tau`. But **perfect** finite-time transfer is impossible at bounded rates even in this favorable ideal Markov interface: the left population obeys `P_L' >= -Gamma P_L`, so `P_L(T) >= exp(-Gamma T)`. An error target `epsilon` consequently needs `T >= (2/Gamma) log(1/epsilon)` (a necessary, not sufficient, duration).

### Positive-frequency completion (finite-band continuum; independent check)

Choose bath energies `0<omega<2E0` and hybridization profile

    h(omega)=[1-((omega-E0)/E0)^2]^2,
    W_L(omega,t)=sqrt(gamma_L(t)h(omega)/(2pi)),
    W_R(omega,t)=sqrt(gamma_R(t)h(omega)/(2pi))exp(-i omega tau).

The complete Hamiltonian acts on `C^2 + L^2(0,2E0)` with internal diagonal energy `E0` and bath multiplication energy `omega`; there is no sender-receiver Hamiltonian edge. This is a mathematically exact, semibounded *one-channel chiral Fano model*, **not** an acquired local 1D chiral electromagnetic channel. Because

    integral_0^(2E0) h(omega)/omega d omega =4/3,

its zero-energy emitter Schur complement obeys

    S(0) >= [E0 - 2(gamma_L+gamma_R)/(3pi)] I
         >= [E0 - 4 Gamma/(3pi)] I.

Thus the complete positive-frequency Hamiltonian remains nonnegative during the whole controlled operation. The bath is genuinely gapless and coupled at each time with nonzero rates.

An executed Gauss-Legendre spectral discretization plus independent adaptive Schrödinger evolution at `E0=24, Gamma=.3, x=11.5, tau=2.5` gives:

- total duration 79.1667;
- final receiver probability `0.9999643063`;
- full one-photon state-vector error after known phase correction `0.00597445`;
- sender probability `9.15e-6`, continuum output probability `2.65e-5`;
- analytic emitter Schur margin `>23.8726`.

The 1000, 1400, and 1750 spectral-node calculations agree at the displayed precision; this is numerical convergence, not interval certification. These pulses have abrupt changes at window boundaries; the *local* construction below uses smooth switching. A strictly one-way finite-band branch cannot be the only Bloch band of a static finite-range 1D translation-invariant periodic chain: a smooth periodic `E(k)` has `integral E'(k) dk=0`. Physical chirality requires extra structure, e.g. additional bands, higher-dimensional edges or external nonreciprocal couplers.

## 4. A strictly local *reciprocal* quantum transmission line

The more physically constrained construction has two endpoint storage levels, `n=300` intermediate oscillator sites, and only nearest-neighbour hopping, including at the two endpoint attachments:

    H_bus(t) = 2J [|L><L|+|R><R|+sum_{j=1}^n |j><j|]
       + J sum_{j=1}^{n-1} (|j><j+1|+h.c.)
       + g_L(t)(|L><1|+h.c.)+g_R(t)(|R><n|+h.c.).

Take `J=8, Gamma=.2, x=12.5`, time-of-flight `tau=(n-1)/(2J)=18.6875`, and transfer interval `[-x/Gamma,x/Gamma+tau]` of duration `T=143.6875`. Let

    g_L(t)=1.004 sqrt(J gamma_L(t)/2) s_L(t),
    g_R(t)=1.004 sqrt(J gamma_R(t)/2) s_R(t),

where `gamma_L/R` are the bounded logistic rates above (shifted by `tau` for the receiver). The factors `s_L,s_R` are raised-cosine-like polynomial `3u^2-2u^3` turn-on/off ramps, of width **4** time units at each attachment window endpoint. Couplings therefore vanish continuously with zero first derivative at their endpoints, without changing the underlying fixed nearest-neighbour graph. Maximum endpoint hopping is about `0.898`.

**All-time positivity theorem.** The static onsite energies are `2J=16`, each main-chain interior vertex has total adjacent hopping weight `2J`, and each boundary vertex has at most `J+max_t|g| <=2J` while memory vertices have only one hopping `<=J`. Since the Hermitian Hamiltonian is diagonally dominant with nonnegative diagonals, `H_bus(t)>=0` for all `t`. This remains true after taking second quantization in any particle sector; replacing endpoint oscillators by two-level hard-core states compresses positive quadratic forms and cannot create negative energy. No all-particle capacity-`m` threshold is inferred just from this positivity.

### A genuinely interacting gapless radiation arm

At the middle site `j0=151`, attach a separate semi-infinite Jacobi arm with onsite `2J`, hopping `J`, and coupling `eta=0.05` to its first site. Add an actual counterterm

    delta |j0><j0|,             delta=eta^2/J=0.0003125.

The arm has purely continuous spectrum `[0,4J]=[0,32]`, with arbitrarily soft excitations. Its endpoint zero-energy Green function is exactly

    <e1,h_arm^{-1} e1> = 1/J,

in the positive-form sense. At finite arm length `m`, it is `m/[J(m+1)]`. Completing the square in the arm gives, for every `t`,

    H_total(t) >= H_bus(t) + (delta-eta^2/J)|j0><j0| >= 0.

**This is a coupled gapless radiation channel, not an uncoupled spectator bath.** Crucially, however, *remote transport still uses the 300-site finite transmission line*. The gapless arm is a side radiation channel, not the sole bridge between sender and receiver. The earlier strictly-through-continuum four-port obstruction is not resolved by relabelling this model.

### Executed full-unitary transfer

At finite arm length `m=7000`, solving the complete Hermitian one-photon Schrödinger equation with all main-bus and side-arm amplitudes retained gives

    P_receiver       = 0.9999408928263
    P_main_bus       = 0.0000193434922
    P_side_radiation = 0.0000391858973
    P_sender         = 0.0000005777842
    ||state-ideal|| after known phase correction = 0.007688175802.

This is a **0.7688% full state-vector error**, corresponding to 99.9941% receiver excitation probability, with no postselection. A logical qubit `alpha|vac>+beta|L>` and any external reference inherit the same operator-norm error after correcting the known one-excitation phase, because the vacuum sector is invariant and the operation is linear. The stated figure is numerical, not a formal interval-enclosed propagator result. Norm loss in the executed calculation is below `2e-15`.

### Rigorous link between the finite calculation and the true gapless arm

Let `U_infty(T)` be the evolution with the infinite arm and `U_m(T)` that with a truncated `m`-site arm, embedded with a decoupled tail. After removing all diagonal energies by an interaction picture, the total offdiagonal operator has uniform norm at most `K=2J+eta=16.05`. To reach the truncated arm's last site from the sender, at least `m` hopping insertions are necessary. Dyson expansion therefore bounds its amplitude by `sum_{r>=m}(Kt)^r/r!`. Duhamel across the one missing arm-end edge gives, on the initial sender state,

    ||(U_infty(T)-U_m(T))|L>||
       <= J T * sum_{r=m}^infty (K T)^r/r!
       <= J T * (K T)^m/m! / (1-KT/(m+1))       (m+1>KT).

At `T=143.6875, m=7000` this **rigorous continuum-truncation norm bound is below `10^-334.45`**. It does *not* bound the numerical ODE integrator error; the numerical receiver amplitude is independently checked by varying `m`, integration step and tolerance. The limit contains an actual positive-frequency, gapless, continuous side-arm spectrum.

## 5. Independent diagnostics and failures preserved

- Local bus only, `n=300, J=8`: phase-corrected transfer error about `0.0040` in one executed pulse calibration.
- Side arm with `eta=.05`: ramp width 0, 1, 2, 4 gives numerical full-state errors near 0.742%, 0.745%, 0.749%, 0.769%, respectively. Smooth controls incur a measured modest penalty.
- Calibration changes matter: with ramp width 4, common endpoint multiplier `1.000` instead of `1.004` gives about 1.075% error; `1.002` gives about 0.851%. No general fabrication-tolerance certificate has been acquired.
- Adding the side arm without the positive local counterterm is **not** covered by the nonnegative all-sector proof. For a gapless critical Jacobi bus, even weak side coupling can change the bottom of the spectrum.
- A two-port reciprocal continuum with full-column-rank radiation coupling cannot have exact finite-time terminal radiation vacuum for nontrivial compact source histories. Neither the one-way chiral model nor the *finite discrete bus* model contradicts that theorem.
- The chiral continuum does not have a demonstrated strictly local static 1D lattice realization; the local bus does not establish perfect transfer exclusively through an infinite radiation continuum.

An elementary *dispersion-only* certificate helps explain why a weakly spectrally confined photon can cross a long ordinary lattice. For an infinite uniform Jacobi dispersion `E(k)=2J+2J cos k`, choose the forward branch

    k(E)=pi/2-arcsin((E-2J)/(2J)).

Subtracting the ideal linear propagation phase, any spectral wavepacket supported within `|E-2J|<=Delta<2J` has phase-only error at distance `D` bounded by

    D Delta^3 / [48 J^3 (1-(Delta/(2J))^2)^(3/2)].

This follows by integrating the derivative of `arcsin x-x`; it does **not** include errors from launching, receiving, finite endpoints or the attached side bath, which were evaluated with the full Hamiltonian separately.

## 6. Scientific conclusion and next hard attack

The constructive result is a *strictly local, positive, number-conserving* Hamiltonian with a real transmission path, smooth bounded endpoint controls, an actually coupled gapless radiation channel, and numerically demonstrated sub-1% complete coherent excitation-transfer error. Its strengths are that all amplitudes are accounted for, the transport graph contains no direct emitter-to-emitter bypass, and continuum completion/positivity have independent analytical proofs. It is not an experimental device or a historically novel state-transfer method.

The broader physical insight is a **three-level feasibility separation**: (i) terminal source-null algebra depends on the analytic rank of radiation ports, (ii) dynamical transfer speed depends on coupling action, and (iii) physically meaningful all-particle stability depends on the zero-energy Green-function compensation. Good source algebra alone does not imply a local device; high-fidelity transport through a finite local bus does not automatically solve exact transfer through a continuous bidirectional reservoir.

The strongest unresolved target remains a *through-continuum*, rather than finite-bus, near-perfect transfer using reciprocal local couplings with all unwanted directions and Maxwell/circuit implementation constraints retained. The strongest alternative remains multi-leg giant atoms and engineered dispersion (referenced above), which already demonstrate substantial capabilities and must not be replaced by an unsupported novelty claim.

## Executable sources

- `astra_radiative_rank_and_local_transfer_audit_20261027.py` — exact Markov receiver-amplitude check, rank witness, spectral inverse moment, continuum truncation bound.
- `astra_chiral_no_bypass_finite_band_20261027.py` — one positive-frequency, chiral-band Fano source-to-receiver evolution, full continuum amplitudes (quadrature).
- `astra_local_boundary_waveguide_transfer_20261027.py` — strictly nearest-neighbour finite Jacobi-bus transfer without a radiation arm.
- `astra_local_waveguide_gapless_arm_20261027.py` — gapless radiation arm, exact local counterterm and full transfer (with smooth finite coupling ramps).
- Corresponding executed JSON files, including the 7000-arm-site calculation, are in `/mnt/data`.
