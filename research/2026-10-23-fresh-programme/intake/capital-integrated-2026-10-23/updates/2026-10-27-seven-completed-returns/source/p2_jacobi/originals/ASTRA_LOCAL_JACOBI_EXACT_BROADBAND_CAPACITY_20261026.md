# Astra foundational physics: local Jacobi broadband scattering and exact many-particle capacity

26 October 2026 — independent continuation. Mathematical scope: stationary single-photon scattering on semi-infinite **harmonic** oscillator chains, finite hard-core memory spins, real local hopping, and excitation-number conservation. The result is an exact model calculation and constructive spectral principle, not a new force, historical novelty claim, Maxwell hardware model, finite-time memory loader, or experimentally verified gate.

## 1. Decision between live directions

The previously established passive spectral-moment approach uses scalar Fano baths and positive-energy side oscillators to cancel successive derivatives of the reactance. Its hard-band Ohmic source permits fourth-order local flattening; its exponentially tailed Ohmic source is obstructed. The alternative here replaces high-order spectral fitting by **exact bulk translation symmetry**: choose a physical local Jacobi lead whose boundary Weyl function already has affine real part throughout a propagation band. This is a stronger mechanism for the *lossless idealization* because no derivative cancellation, side oscillator, or high-order pole tuning is necessary. A separately coupled gapless lead and the actual all-sector memory Hamiltonian are then reintroduced and assessed without conditioning on a surviving photon.

## 2. Exact local lead and entire-band scattering

Normalize energy by the bulk half-bandwidth and define the one-particle Hilbert space `C|e> ⊕ ℓ²(N)`. The local Hamiltonian has emitter energy `H`, bath on-site energy `b`, bath nearest-neighbour hopping `t>0`, and emitter–first-site hopping `v>0`:

    h = H |e><e| + b Σ_{n≥1}|n><n|
          + t Σ_{n≥1}(|n><n+1| + h.c.) + v(|e><1| + h.c.).

The bulk passband is `(b-2t,b+2t)`. With retarded surface Green function (root chosen analytic off the band)

    g_b(z) = [z-b - sqrt((z-b)^2-4t²)]/(2t²),

where the root is asymptotic to `z-b`, the on-shell real Fano self-energy in the convention `Σ(E)=-v² Re g_b(E+i0)` is

    Σ(E) = [v²/(2t²)] (b-E),
    Γ(E) = π J(E) = [v²/(2t²)] sqrt(4t²-(E-b)²).

Thus the exact reactance is

    D(E) = [1-v²/(2t²)] E + [v²/(2t²)] b - H.

**Local classification (proved):** `D(E)=0` at every energy in any nonempty open subinterval of the band iff

    v² = 2t²,   H=b.

The solution then gives **S(E)=[D(E)-iΓ(E)]/[D(E)+iΓ(E)]=-1** for every interior energy, not merely a high-order Taylor approximation. It uses one ordinary boundary oscillator and a translation-invariant bulk.

For the gapless choice `b=1, t=1/2, v=1/sqrt(2)`, the exact endpoint density is

    J(E) = sqrt(E(2-E))/π,                  0<E<2,
    Σ(E) = PV ∫ J(x)/(x-E) dx = 1-E.

The ordinary finite-interval Cauchy integral was evaluated at nine independent energies, agreeing with `1-E` to `4.7e-15`. A *separate real-space reflection calculation* using the discrete Schrödinger equation gives the scattering amplitude relative to a decoupled terminated lead, matching the Fano formula to `4.3e-15` over 199 energies and four emitter detunings. This fixes the scattering phase convention; the nontrivial quantity is the difference between memory sectors, not an arbitrary absolute reflection phase.

The Hamiltonian is literally the even-parity compression of an infinite uniform nearest-neighbour chain: its even basis is `|0>, (|n>+|-n>)/sqrt(2)`, generating the enhanced first hopping `sqrt(2)t`. Hence the affine Weyl function is an exact local-lattice effect. In the gapless case the quadratic form has the positive-square identity

    <ψ,hψ> = (1/2)|sqrt(2) a+β₁|²
            + (1/2) Σ_{n≥1}|β_n+β_{n+1}|²

on finitely supported vectors `ψ=a|e>+Σβ_n|n>`. Positivity extends by form closure. The infimum is zero, but no negative-energy bound orbital is present.

For **unselected** memory sectors raise *only* the emitter energy by `λ=χ(m-k)>0`. Then

    D_k(E)=-λ,
    S_k(E)=(-λ-i sqrt(E(2-E)))/(-λ+i sqrt(E(2-E))),
    |S_k(E)-1|=2 sqrt(E(2-E))/sqrt(λ²+E(2-E)).

For a 1% coherent amplitude target over the entire open band, the sharp necessary and sufficient nearest-unselected detuning is

    χ ≥ sqrt(4/0.01²-1) = 199.997499984... .

With `χ=201`, the *entire-band* unselected error is `<0.00995013`, while the selected error is exactly zero. The band-edge scattering states have zero spectral weight; statements apply to the absolutely continuous channel and normalizable wavepackets, not to an invented isolated plane-wave state at an edge. The high pairwise cross-Kerr shift remains a very substantial control resource. The laboratory reflection amplitude also contains the **common free-boundary propagation phase**; all conditional gate statements use the correctly defined asymptotic scattering basis or an output encoding that compensates that common phase. The conditional *difference* is exactly frequency-flat, not an assertion that every laboratory pulse returns without dispersion.

## 3. Two distinct limits: gapless all-band flatness and strictly positive stability margin

For a scalar emitter and passive continuum with `K=∫J(E)/E dE<∞`, the one-body zero-energy Schur positivity condition is `H≥K` (with extra auxiliaries, subtract their positive `V²/Ω` as well). If `D(E)=0` down to a gapless continuum threshold at `E=0`, continuity of its real self-energy gives `D(0)=K-H=0`. **Exact whole-gapless-band -1 scattering forces the positive-square Schur margin to vanish.** This does not mean the Hamiltonian is unstable: the preceding gapless chain is a stable equality case.

There is a constructive escape if the *signal* passband begins above zero. Choose `b=6/5`, `t=1/2`, `v=1/sqrt(2)`, `H=b`. The signal band is `[1/5,11/5]`, it retains **exact** `S(E)=-1` at every interior energy, and its positive Schur margin is

    M = H - v² <1|h_b^{-1}|1>
      = sqrt(b²-1) = sqrt(11)/5 = 0.663324958... .

This is also an exact spectral equivalence to the even sector of an infinite lattice shifted by `1/5 I`; there is no negative or sub-band bound eigenvalue. But a gapped signal lead alone does not give the desired `E_N=-min(N,m)` dissociation thresholds for added bosons, so a separate *interacting* gapless channel is required for the stronger combined theorem.

## 4. Genuinely coupled soft bath: inclusive coherent gate and all-particle theorem

Attach a second semi-infinite harmonic Jacobi lead to the *same* emitter. Its on-site energy is `1`, bulk hopping `1/2`, and boundary coupling `ζ=3/2000=0.0015`. The main signal lead remains `b_a=6/5`, hopping `1/2`, boundary coupling `v=1/sqrt(2)`, emitter energy `H=b_a`.

At energies `E∈[2/5,9/5]`, both leads are open. Define

    Γ_a(E)=sqrt(1-(E-6/5)^2),
    Γ_s(E)=2ζ² sqrt(E(2-E)),
    Γ(E)=Γ_a+Γ_s,
    D_k(E)= -χ(m-k)+2ζ²(1-E),   χ=201.

Both outputs are included in the exact on-shell 2×2 matrix

    S_k(E)=I₂ - [2i/(D_k(E)+iΓ(E))] v(E)v(E)†,
    v(E)=(sqrt(Γ_a(E)),sqrt(Γ_s(E)))ᵀ.

For an incoming photon in the main lead, the selected target is `-|a>` and all unselected targets are `+|a>`. Exact *full-state*, not survival-conditioned, errors are

    ε_sel(E) = 2 sqrt{[D_m(E)^2+Γ_s(E)Γ(E)]/[D_m(E)^2+Γ(E)^2]},
    ε_off(E) = 2 sqrt{Γ_a(E)Γ(E)/[D_k(E)^2+Γ(E)^2]}.

Uniform analytic inequalities use `Γ_a≥3/5`, `Γ_a≤1`, `Γ_s≤2ζ²`, and `|D_m|≤(8/5)ζ²`:

    ε_sel(E) ≤ 2 sqrt{[(8ζ²/5)/(3/5)]² + (2ζ²)/(3/5)}
             = 0.005477238721...,
    ε_off(E) ≤ 2 sqrt(1+2ζ²)/[201-(8/5)ζ²]
             = 0.009950271323... .

These are coherent *vector* errors, uniformly for the entire energy interval, arbitrary spectral wavepacket amplitudes, all finite memory capacities, and untouched quantum references. The complete S matrix is unitary; a 3001-frequency independent audit found its worst unitarity residual `1.6e-15`. The frequency-grid maxima were approximately `0.004899` and `0.00995015`; **the proof is the analytic bound, not the grid**.

The selected one-body Hamiltonian has positive zero-energy Schur margin

    M = H - K_a - K_s
      = sqrt(11)/5 - 2ζ²
      = 0.663320458071... >0,

where `K_a=6/5-sqrt(11)/5` and `K_s=2ζ²`. Completing squares over both boson leads proves `h_m≥0`; for unselected charges the emitter-energy increase is positive, so `h_k≥h_m≥0`. The presence of the soft chain makes `inf spec h_k=0` for each charge, despite the strictly positive local Schur margin.

For `m` ordinary two-level memory sites let `K=Σ n_j∈{0,...,m}`, choose `H_mem=-K+T`, where `T≥0`, `[T,K]=0`, and each charge sector has a `T=0` state. On the full Fock space take the emitter term

    [6/5+201(m-K)] e†e,

with the two local harmonic chains and their ordinary number-conserving boundary hops. This interaction is **pairwise**: `201m n_e -201 Σ_j n_e n_j`. Total excitation `N=K+n_e+n_bath` is conserved. In each fixed charge sector, the unrestricted bosons evolve under `dΓ(h_k)`. Hence

    H_N≥-min(N,m).

Choosing the memory `T=0` sector at `k=min(N,m)` and, if necessary, extra bosons in arbitrarily soft scattering states of the **coupled** gapless lead gives the reverse inequality in the spectral infimum:

    **inf spec H_N=-min(N,m), for every finite N.**

This is a dissociation threshold, not a projection onto ≤m total particles or the assertion of a normalizable N>m ground state. It does not establish loading or multi-photon gate behavior.

## 5. Certified calibration box (second independent calculation)

Keep photon band `[2/5,9/5]` and memory shift `χ=201`. Admit simultaneous physical parameter errors:

    H=6/5+h,           |h|≤1/2000,
    v_a²=(1+η)/2,     |η|≤1/2000,
    ζ'=(3/2000)(1+ξ), |ξ|≤1/10.

Then the exact real reactance is

    D_k(E)= -201(m-k)+η(6/5-E)-h+2(ζ')²(1-E).

On the full band, bound `Γ_a≥(1-1/2000)*3/5`, `Γ_a≤1+1/2000`, `Γ_s≤2(33/20000)²`, and

    |D_m|≤ (4/5)(1/2000)+(1/2000)+(8/5)(33/20000)²
         = 0.000904356.

Substitution into the preceding exact two-port formulas and rational squaring establishes for **every** allowed parameter tuple and every photon energy:

    ε_sel < 0.006739035 <0.00675,
    ε_off < 0.009955296 <0.00996,
    M ≥6/5-1/2000-(1+1/2000)(6-sqrt(11))/5-2(33/20000)²
      >0.66255117>0.6625.

No sampled parameter grid is needed for this certificate. A separate seeded 200-parameter ×1001-energy test gave maximum errors `0.0059530` and `0.00995509`, both below the analytic bounds.

## 6. A sharp opposite threshold: spectral capacity fails at strong soft coupling

For the *uncalibrated* two-lead model of §4 with `H=6/5` and variable soft coupling `ζ`, the necessary and sufficient zero-energy positivity condition is

    ζ² ≤ sqrt(11)/10 = 0.3316624790355... .

Proof: `K_a=(6-sqrt(11))/5`, `K_s=2ζ²`, so the positive-square Schur margin is `sqrt(11)/5-2ζ²`. If negative, minimize the full one-body quadratic form over both baths (using a finite-energy form-core approximation): it is strictly negative for some normalized vector. Since all bath energies are nonnegative and the emitter is finite rank, one simple negative bound orbital appears below the soft continuum; monotonicity of its scalar Birman–Schwinger equation gives uniqueness. A harmonic signal field allows arbitrarily many bosons to occupy it, so fixed-memory N-sector energies become unbounded below *as N increases*: no finite all-N capacity limit survives.

At `ζ=0.6`, an independent solution of the exact two-chain surface Green functions gives the negative orbital energy `-0.00277406926`. At `ζ=0.7`, it gives `-0.04142278744`.

The 1% full-photon-state fidelity requirement is much more restrictive than mere positivity. With a single externally driven emitter and a signal and independent soft output, at any fixed E the lowest possible selected-state error over *any real detuning* is

    ε_min(E)=2 sqrt[Γ_s(E)/(Γ_a(E)+Γ_s(E))].

At `E=6/5`, `Γ_a=1` and `Γ_s=2ζ² sqrt(24/25)`. Thus a 1% state-vector target forces

    Γ_s/Γ_a < 1/39999,
    ζ < 0.00357184519...

for this fixed coupling geometry. The actual chosen `ζ=0.0015` satisfies this. Additional passive, closed auxiliary modes that only alter the emitter's *real* self-energy cannot remove this independent-output leakage floor; changing the radiation-coupling topology could.

## 7. Finite-Hilbert-transform classification (support-local)

There is a useful uniqueness statement beyond the uniform-chain realization. Restrict to positive scalar spectral densities supported exactly on `[0,2]`, without point masses, with the standard weighted-Hölder endpoint regularity that makes the finite Hilbert transform well defined. Assume finite `K=∫J(x)/x dx`. If a single emitter has `S(E)=-1` for all `E∈(0,2)` (and J(E)>0 there), then

    PV ∫ J(x)/(x-E) dx=H-E.

Put `w(E)=sqrt(E(2-E))`. Three explicit Cauchy transforms give

    PV ∫ [w(x)/π]/(x-E) dx = 1-E,
    PV ∫ [x/(πw(x))]/(x-E) dx = 1,
    PV ∫ [1/(πw(x))]/(x-E) dx = 0.

The nullspace of the finite Hilbert transform in the stated weighted class is exactly the last, arcsine-weighted profile (proved by multiplying its Cauchy transform by the square root `sqrt(z(z-2))` and removing the endpoint singularities). Therefore every such exact-flat source is

    J(E)= [w(E)+(H-1)E/w(E)+c/w(E)]/π.

Finiteness of `K` forces `c=0`. Positivity at the upper band edge forces `H-1≥0`. If `H>1`, `Γ(E)=πJ(E)` diverges as `E→2-`, so a *finite* emitter-only detuning can never make the unselected scattering phase uniformly approach +1 over the **entire** open band: its coherent error approaches 2 at the upper edge.

Thus, in this well-specified scalar support class, the **semicircular source is unique** among sources permitting both exact selected -1 and uniformly accurate unselected +1 over the whole propagation band with finite emitter-only detuning. This is a mathematical classification based on the classical finite Hilbert transform and causal Cauchy transforms—not an assertion that all passive devices must use semicircular spectra.

The same result suggests a design principle: useful broadband impedance matching and many-body stability should be tested jointly through the *real and imaginary* boundary Weyl function, rather than separately optimizing local Taylor coefficients.

## 8. Limitations and next consequential interface

- The bath is a *mathematically exact* infinite oscillator lattice. Finite chains have return echoes; no finite-time pulse-source/retrieval/absorption protocol has been certified here.
- The model contains a dedicated signal lead and a weak but genuinely coupled soft lead. Independent three-dimensional radiation, propagation disorder, nonlinear dispersion, temperature and spin dephasing have not been included. The complete two-port state error is not an experimental error estimate.
- The emitter–memory controlled onsite shift `χ=201B` is large compared with lattice hopping `B/2`. Its near-optimality is **only** within the emitter-detuning, single-site, entire-band selectivity contract.
- Memory qubits are prepared and have exactly conserved charge. Cross-sector memory transitions and preparation availability remain external resources. This does not prove a practical quantum memory, high-efficiency transducer, or physical gate advantage.
- The positive Schur margin is **not a spectral gap** for the total interacting soft continuum, whose essential spectrum begins at zero.
- The exact-flat mechanism is a familiar property of local tight-binding surface Green functions / the folded infinite chain. Its combination with exact all-sector bosonic capacity is the new *scoped construction* within Astra, not a historical priority claim.

Background references: standard semi-infinite-chain surface Green functions (Lopez Sancho-type decimation), e.g. https://cpoli.github.io/tbkit/api/gallery/tight_binding/plot_surface_greens_function.html and the tutorial https://www.scielo.br/j/rbef/a/yvDhk5GVrC5fTtmT9JQMFWb/?lang=en ; passive electromagnetic oscillator sum rules (https://www.nature.com/articles/s41467-023-43221-2). These establish precedent, not a Maxwell validation of this device.

## Executed ordinary files

- `astra_boundary_work/local_jacobi_broadband_audit.py` and `.json`: independent Cauchy quadrature, direct reflection, finite-matrix spectra, full two-port unitarity/error checks, plus analytic-error parameter output.
- `astra_boundary_work/local_jacobi_parameter_box.py` and `.json`: exact-rational proof for all uncertainties in the full parameter box; additional random-grid diagnostics separately labelled.
- `astra_boundary_work/local_jacobi_stability_frontier.py` and `.json`: exact stability frontier and negative-bound-orbital root checks.

All paths refer to files actually created and executed in the present active workspace. No repo publication or formal verification is claimed.

## 9. Further attack: finite-chain approximation for finite-time dynamics (proved)

The infinite leads above define asymptotic scattering exactly. A finite chain is not an asymptotic scatterer and will eventually exhibit revivals. However, finite-time evolution admits a quantitative *locality* guarantee without assuming that momentum-band-limited photons are compactly supported in space.

Truncate both half-chains after site `L` and compare the resulting unitary evolution `U_L(T)` with `U_inf(T)` on the common Hilbert space, leaving the sites beyond `L` dynamically disconnected in `U_L`. Let `P_R` project onto the emitter and sites `1,...,R` on either arm. Define `d=L-R>0`, and let `a` dominate the norm of the off-diagonal hopping operator (with the current and calibrated couplings one can use `a=1.21`, uniformly for all memory charges and the preceding calibration box). Then

    ||[U_inf(T)-U_L(T)] P_R||
      <= T * sum_{n=d}^infinity (a T)^n/n!
      <= T * (a T)^d/d! / [1-a T/(d+1)],  d+1>a T.

**Proof:** Work in the interaction picture of *all onsite terms*, including the potentially very large memory-conditioned detuning `201(m-K)`. The time-dependent hopping operator has constant norm at most `a`, and each Dyson term with fewer than `d` hops has zero matrix element from `P_R` to the terminal sites at `L`. The Dyson tail bounds the terminal amplitude by `sum_{n>=d}(aT)^n/n!`. Duhamel's formula for the two deleted terminal links (each hopping `1/2`, total norm contribution bounded by 1) then gives the displayed bound. The result is uniform in memory capacity `m` and unaffected by an untouched reference system.

At `T=10/B` and `L-R=50`, the exact analytic upper bound is `5.940380e-10`. For a state with spatial tail `|| (I-P_R) ψ||<=η`, the error bound becomes `2η` plus the expression above; a photon cannot be exactly compact in both spectral and spatial support. The bound controls *finite-time evolution*, not the existence of an infinite-time S matrix for finite chains, and it does not prepare a photon or eliminate independent radiation.

An actual sparse-matrix time-evolution comparison at `T=10/B`, `R=2`, `L=42`, and larger comparison chains of length 90 per arm yielded norm differences `5.7e-15` (selected) and `1.1e-13` (one off-selected detuning). Both lie below the much more conservative finite-propagation certificate `3.562e-4`. These checks are diagnostics; the theorem follows from locality.

Executed script and data: `astra_boundary_work/local_jacobi_finite_time.py` and `astra_boundary_work/local_jacobi_finite_time.json`.

## 10. Resource balance and interpretation

The architecture exchanges the earlier continuum-tail fitting and multiple passive side resonators for ordinary translation-invariant nearest-neighbour hopping. For a chosen 1% two-port coherent gate, the interaction cost is now a pairwise memory–emitter shift of `201B` per absent stored excitation. The **total emitter tuning range grows as `201m B`** across `K=0,...,m`, despite the capacity- and finite-time-error estimates being uniform in `m`. This is the principal scaling cost and should not be hidden by the uniform spectral theorem.

The spectral response, positive-square capacity, and finite propagation bounds are all established model mathematics. The remaining acquisition is a microscopic implementation that realizes the strong charge-dependent detuning, genuinely separate signal and weak soft channels, readout and memory loading without significant independent noise. In particular a circuit-resonator array may model the Jacobi Hamiltonian, but a Maxwell-compatible electromagnetic derivation and demonstration of its control resources have not been acquired.
