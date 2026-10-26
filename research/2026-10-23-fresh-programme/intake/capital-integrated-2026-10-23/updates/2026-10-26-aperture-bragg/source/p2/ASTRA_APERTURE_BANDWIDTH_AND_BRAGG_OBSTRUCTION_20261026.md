# Astra foundational physics — aperture/bandwidth, port rank and reciprocal-band obstruction

26 October 2026 (interim foundational-physics continuation). Original derivations and executable checks in this directory. Research status: **scoped mathematical lemmas and a failed microscopic gate attack; no Maxwell-complete device, experimentally demonstrated effect or historical-novelty claim.** This note continues `ASTRA_FOUNDATIONAL_PHYSICS_MAXWELL_PORT_PARITY_20261026.md`, especially its actual slab dispersion, collective-array radiation lemma and failed full finite-array scattering calculation.

## 1. Scientific choice and external comparison

The earlier two-emitter parity-flip construction required a guided/free-space coupling sign that was not acquired from a single Maxwell source. Its narrow separation also omitted a potentially enormous real near-field exchange. A conventional positive-index emitter array avoids that particular sign resource and has an exact geometrical selective-radiance bound, but its naive complete finite-band scattering gate failed badly. The strongest next question is not yet another conditional-resonance fit; it is **how many internal collective degrees of freedom must be accessed, and can a reciprocal positive-energy Hamiltonian follow the frequency-dependent guided phase?**

Established antecedents: Slepian, *Prolate Spheroidal Wave Functions, Fourier Analysis, and Uncertainty—V: The Discrete Case*, Bell System Technical Journal 57, 1371 (1978), DOI 10.1002/j.1538-7305.1978.tb02104.x; Asenjo-Garcia et al., *Phys. Rev. X* 7, 031024 (2017), DOI 10.1103/PhysRevX.7.031024, on selective radiance; Sheremet et al., *Rev. Mod. Phys.* 95, 015002 (2023), on waveguide collective self-energies; *Photonic qubit gates via 1D scattering from an array of two-level emitters*, *npj Quantum Information* (2026), DOI/link https://www.nature.com/articles/s41534-026-01324-w. The Fourier/Slepian machinery and reciprocity arguments are old mathematics/physics; the contribution here is applying their precise input/output constraints and testing a declared positive finite-band comparator. Historical priority of any combined statement has **not** been established.

## 2. Exact static-modal aperture/bandwidth inequality

Consider N equally spaced emitters and their normalized guided-matched excitation

    u(q)_j = exp(i (j-(N-1)/2) q)/sqrt(N), j=0,...,N-1.

The centering removes an irrelevant global phase. Suppose a **fixed** subspace P of rank r is to contain u(q) to norm accuracy ε for every q in an interval I of width W with 0<W<=2π:

    sup_{q in I} ||(I-P)u(q)|| <= ε.              (A)

This assumption is a fixed-low-mode description of the internal response, not a claim that every passive full-N Hamiltonian reduces to such a subspace.

The full-circle Fourier identity is exact:

    integral_{q_c-π}^{q_c+π} |u(q)><u(q)| dq = (2π/N) I_N.

For nonnegative projectors, restricting the integral to I gives

    integral_I |u(q)><u(q)| dq <= (2π/N) I_N.

Take the trace against P. Hypothesis (A) gives at least W(1-ε²) on the left, while the right is (2π/N)r. Thus

    **r >= (1-ε²) N W/(2π).**                    (B)

This is a literal finite-N Fourier sum rule. No narrow-band approximation, bath elimination or Markov limit enters it.

### Sharp average bound by a discrete prolate matrix

Set C_I=(1/W) integral_I |u(q)><u(q)|dq. Its entries in the centered emitter basis are

    (C_I)_{jl} = exp[i(j-l)q_c] sinc[(j-l)W/2] / N,

where sinc(x)=sin(x)/x. It is positive, trace one. By Ky Fan's variational principle the largest possible **average** capture by any rank-r subspace is Σ_{a=1}^r λ_a(C_I). Therefore a stricter necessary condition for (A) is

    **Σ_{a=1}^r λ_a(C_I) >= 1-ε².**             (C)

The top-r eigenspace optimizes average projection. This is the finite DPSS/Slepian construction; it does not minimize worst-case error as a theorem.

There is also a deterministic method for obtaining an *upper bound on continuous-band worst-case error* for any chosen fixed projection: since ||u'(q)||=sqrt((N²−1)/12), the residual e(q)=||(I−P)u(q)|| is Lipschitz with that constant. On a uniform grid of M points covering I, the maximum on the entire interval is at most

    max_grid e(q_i) + sqrt((N²−1)/12) W/[2(M-1)].  (D)

Equation (D) is analytic; its numerical inputs in the supplied script are double-precision eigensystems and grid evaluations, **not verified rational interval arithmetic**. The margin to the target exceeds the observed floating-point residuals by orders of magnitude, but the report should describe it as a deterministic a-posteriori numerical certificate, not machine-checked formal proof.

For the TE slab previously solved, guided phases at E=1.45 and 1.55 are 2.98476557449 and 3.30066156287, giving W=0.31589598838. With ε=0.01 and N=33:

    1 - Σ_{j=1}^4 λ_j = 0.0001211085027948335... > ε²=0.0001;

so **every rank-four fixed subspace fails** the required uniform accuracy. This value was reconstructed with 55-digit mpmath real-symmetric eigenvalues, not merely a low-accuracy numerical diagonalization. Conversely, the rank-five DPSS projector has sampled maximal residual 0.0047647208 and Lipschitz grid allowance 0.0001835896, giving worst-band upper 0.004949 <0.01. Thus five modes are necessary and numerically certified sufficient for the *fixed-subspace approximation task* at N=33. In contrast, this does NOT imply five uncoupled physical emitters, five poles of a passive scattering function, or a completed conditional gate. A full N-mode response may track without a fixed low-rank approximation.

Additional N (W=0.315896): necessary/sufficient tested ranks: N18 4/4; N40 5/6; N64 6/7; N100 8/9. Exact data and the complete interpolation grid are in `astra_collective_aperture_modal_theorem_20261026.py` and JSON.

## 3. A second exact Bragg obstruction: photon-port rank

With *identical local reciprocal couplings* and two 1D propagation directions, the guided on-shell source matrix has columns

    W_R(ω)_j = g(ω) exp(i β(ω) a j),
    W_L(ω)_j = g(ω) exp(-i β(ω) a j).

At the Bragg point β(ω0)a=π the columns are equal, because exp(±iπj)=(-1)^j. The odd input φ=(1,-1)/sqrt(2) obeys W_g φ=0. In the exact Fano scattering formula

    S_total(E) = I - 2π i W(E)^* [E-H_int+PVΣ(E)+iπ W(E)W(E)^*]^{-1} W(E),

this photon input gives **S_total(ω0)φ=φ**, with zero unwanted-radiation amplitude, for any static internal Hermitian H_int and any other bath couplings, provided the wave operator/scattering limit exists. Consequently

    **||(S_total(ω0)+I)φ|| = 2.**               (E)

No device from this class can implement a sign -I on *arbitrary two-sided guided photon states* at the Bragg frequency. It can still implement a conditional operation on the **encoded even photon channel**; equation (E) does not challenge earlier even-channel-only results. The explicit 18-emitter 62-channel finite-band check finds ||Wφ||=3.16e-15, ||Sφ-φ||=4.64e-15, and wrong-sign error 2.0. At q=2π/3 instead, the two guided coupling columns are independent (indeed orthogonal for N multiple of three).

This is a port-rank, not aperture, obstruction. Adding more internal resonators without changing the two local guided source columns cannot eliminate it.

## 4. Reciprocal single-band obstruction and a concrete bypass

Let E_int(q) be any differentiable, *nondegenerate* band of a scalar one-orbital time-reversal-symmetric reciprocal lattice of period a. Reciprocity and periodicity give E_int(q)=E_int(-q)=E_int(q+2π), so

    E_int'(π)=0.

If the guided photon phase q_g(E) obeys q_g(E0)=π, q'_g(E0) finite, and one seeks a first-order internal-band tracking identity E_int(q_g(E))=E+O((E-E0)^2), then differentiation at E0 would require

    E_int'(π) q'_g(E0)=1,

which is impossible. The result covers all finite-range real reciprocal hopping amplitudes and smooth isolated bands, not degenerate crossings or frequency-dependent self-energies engineered with auxiliary modes. This group-velocity obstruction is distinct from (E).

**Bypass A: off-Bragg momentum.** Take a conventional slab with core index 3.5, cladding 1, slab thickness d/λ0≈0.060136 and central n_eff=2. Change the emitter spacing from λ0/4 to λ0/6. Now the guided phase at E0=1.5 is q0=2π/3, the radiative phase is θ0=π/3, and q'_g(E0)=2.106... (actual TE dispersion, not a postulated linear group index). For a reciprocal nearest-neighbor internal band

    E_int(q)=ε+2J cos q,

choose

    J= -1/[2 sin(q0) q'_g(E0)] = -0.2741103825471,
    ε= E0-2J cos(q0) = 1.225889617453.

Then E_int(q_g(E0))=E0 and d/dE E_int(q_g(E)) at E0 equals one **exactly by construction**. The bare internal band is strictly positive, with minimum 0.67766885236 energy units. Solving the actual TE slab dispersion at the 301 sampled E points between 1.45 and 1.55 gives a maximum internal energy mismatch of ≈0.0012864, as opposed to a first-order mismatch at q0=π. With an exactly linear guided phase slope v, the analytic Taylor remainder satisfies |E−E_int(q_g(E))|≤|J|v²|E−E0|²≤0.003041 for |E−E0|≤0.05.

The new phase remains outside the ideal free-space radiation light cone over the requested band (sampled minimum q_g−θ≈0.97755). The finite-array Dirichlet upper prefactor is ≈0.04687/N² for the idealized electric-dipole angular profile and 1% per-emitter radiative-to-guided intensity. Therefore N=44 suffices for **the ideal isolated phase-matched radiative-branching certificate**, not a full gate. The modal covariance for the off-Bragg slab interval W≈0.210597, N=44 requires at least four fixed modes; a five-mode DPSS subspace has a sampled-and-Lipschitz worst-band residual <0.00284.

**Bypass B: band crossing.** A reciprocal two-orbital Bloch Hamiltonian

    H(q)= ε I_2 + J [[0,1+exp(-iq)],[1+exp(iq),0]]

has a degeneracy at q=π and linearly crossing eigenvalues ε±2J|cos(q/2)|. Continuously followed branches can have nonzero one-sided slopes. This removes the *nondegenerate single-band* no-go, but requires an explicitly two-band emitter interface and correct coupling to the guided photon; it is not a complete solution.

## 5. Actual full finite-band array attacks: failures retained

The off-Bragg single-band matching is not a gate theorem. I computed the genuine finite-band self-energy of a declared Fano-Anderson array, including its real principal-value matrix and **all 60 unwanted angular output channels**, with two guided propagation columns and a frequency-dependent positive bath spectrum. One-channel coherent input error is calculated from the full normalized final state, not postselected transmitted photons. The model uses phase functions q_g(E)=q0+q'_g(E0)(E−E0), θ_rad(E)=θ0 E/E0; it has NOT acquired the full Maxwell dyadic for a finite-cross-section guide.

A deterministic diagnostic search varied the common bare emitter energy ε, real nearest-neighbor hopping J and common light-matter density scale γ, under a positive one-body Schur-margin constraint, with N=42, q0=2π/3 and 1% independent per-emitter radiation. The best run of the reported differential-evolution search (seed 13, 1418 objective evaluations) gave

    ε=5.064048483893, J=-0.13645303187, γ=0.03756806894,
    full-state errors at energies [1.495, 1.4975, 1.5, 1.5025, 1.505]:
    [0.05012420, 0.02932139, 0.01265577, 0.02463001, 0.04688240].

Direct scattering output-vector evaluation independently reproduced these five errors to better than 1e-11. Thus **this actual three-parameter, positive Fano array is not a sub-1% 0.01-wide photon gate**. The optimization is *not* a global lower-bound proof: more internal controls, a larger multimode network or a different source geometry may perform better. It also shows why a small scalar band-dispersion mismatch is insufficient to bound coherent scattering; the full off-shell matrix and its unwanted output channels matter.

### Proved positivity and all-sector storage in this *failed gate* comparator

The numerical Schur minimum was ≈4.733, but an elementary independent **analytic positivity bound** is available. With bath frequency x∈(0,2), guided coupling columns of squared norm γ x² per site in total, and radiation columns totaling (ργ/E0)x³ per site, the integrated Fano one-body Schur block obeys

    H_int - ∫_0² W(x)W(x)^*/x dx
       >= [ε-2|J| - Nγ(2 + 8ρ/(3E0))] I.

The inequality uses ||∫ PSD|| <= tr∫ PSD and ||J(S+S*)||<=2|J|, and is independent of propagation phases. Substituting the optimizer parameters gives a strictly positive **1.6073738044** margin. Completion of squares with the positive bath multiplication operator establishes the full one-body h_sig>=0.

Therefore, if an independent m-site hard-core memory has H_M=-B K+T with K≤m, [T,K]=0, T>=0 and T annihilating at least one state in **every** K=0,...,m memory sector (for example the Dicke states of a nonnegative exchange graph Laplacian), and the signal Hamiltonian acquires only a positive memory-conditioned frequency shift χ(m−K) N_emitters with χ>=0, then every N-excitation sector satisfies

    H_total,N >= -B min(N,m),

because K≤min(N,m) and the signal quadratic Hamiltonian is positive. With continuum soft modes of arbitrarily small energy, the full spectral infimum is exactly -B min(N,m) from K=min(N,m) with soft spectators escaping. Thus the failed gate comparator **does preserve an exact all-N spectral capacity**. The memory preparation, nonzero temperature and loss-related operational fidelity remain separate.

## 6. Physical assessment and next substantive attack

The incumbent capacity theorem remains useful, but coherent gate performance requires control of a moving continuum-coupling subspace, not just a spectral-energy threshold. Three independently proved constraints converge at the Bragg interface: (i) modal aperture/bandwidth, (ii) a one-dimensional antisymmetric *photon input* that is rigorously decoupled, and (iii) zero Bloch group velocity for a smooth reciprocal nondegenerate internal band. The first is an instance of Slepian concentration, the third a standard reciprocal-band property; neither is claimed as a new universal physical law. Their joint implication for this **declared** source architecture is concrete.

The off-Bragg reciprocal hopping band repairs (iii), evades the rank collapse (ii), and preserves ideal guided-vs-radiation momentum separation, but the actual three-parameter Fano scattering operation still fails (i)/off-shell mixing on the requested bandwidth. The main promising continuation is an **acquired multimode collective response**, e.g. a reciprocal two-band lattice or a finite set of DPSS-like collective degrees of freedom with independently calibrated reactive couplings, and a sourced radiative Green tensor from *one* Maxwell waveguide. A cavity-assisted scheme with complete intrinsic loss and cooperativity resources is an equally serious competing physical architecture. Without such a response, further ideal on-shell optimizations are not genuine device progress.

## 7. Reproduction files

- `astra_collective_aperture_modal_theorem_20261026.py` / `.json`: exact Toeplitz concentration formula, rank bounds and grid+Lipschitz residuals.
- `astra_bragg_port_rank_audit_20261026.py` / `.json`: explicit two-port dark input identity in a 62-channel Fano system.
- `astra_offbragg_maxwell_band_match_20261026.py` / `.json`: TE dispersion, positive reciprocal NN band and radiative light-cone gap.
- `astra_offbragg_array_attack_20261026.py` / `.json`: finite-band principal-value and complete photon-output comparison of scalar, locally compensated and full reactive calibration.
- `astra_offbragg_optimized_diagnostic_20261026.py` / `.json`: seed-fixed three-parameter positive-network search and full complex-vector independently reproduced result.
- Original predecessor `ASTRA_FOUNDATIONAL_PHYSICS_MAXWELL_PORT_PARITY_20261026.md` and prior `astra_dielectric_slab_dispersion_20261026.py` remain unchanged.

## 8. An equally equipped cavity-assisted comparator: exact inclusive loss resources

A single-sided resonator with one conditional two-level emitter entirely avoids the array Fourier-aperture obstruction. This makes it a serious competitor, rather than merely an incidental mention. Let κ denote its useful photon-port linewidth, λ its independent intrinsic loss linewidth, γ the emitter's unwanted-radiation linewidth and g the coherent emitter/cavity coupling. In the declared one-photon Markov input-output model, with emitter and cavity on resonance and photon detuning δ,

    r(δ)=1 - κ/[iδ+(κ+λ)/2+g²/(iδ+γ/2)].

When the emitter is disabled, omit the g² term. For the desired scalar phase σ=±1, unitarity of the full inclusive waveguide+unmonitored-bath scattering system gives the *exact full outgoing state-vector error*

    ||Ψ_out−σ Ψ_in||² = 2[1−σ Re r(δ)].

This is **not** postselection on reflection. At δ=0 and g=0, r_0=(λ−κ)/(λ+κ) and the desired phase is −1. A 1% error therefore requires

    λ/(κ+λ) < 0.000025.

At δ=0, λ=0 and a resonant coupled emitter, the desired phase is +1, and a 1% error requires

    4 g²/(κ γ) >= 39999.

These constraints are individually necessary in this two-branch cavity architecture. For the empty-cavity, intrinsic-loss-free branch at small photon detuning, the full-state phase error is approximately 4|δ|/κ; at |δ|/κ=.0025 the exact value is 0.0099998750. Therefore a 0.05B half-bandwidth at 1% error requires κ roughly 20B or greater before charging the emitter/cavity dispersion and positive-frequency completion.

The cavity avoids collective mode tracking but pays an exceptional cooperativity and intrinsic-loss resource cost. The reciprocal array retains a competing route through collective selective radiance, but its full all-output gate with an actually constrained source has not been acquired. Neither comparator is judged experimentally superior. The exact cavity calculation is in `astra_cavity_equal_resource_comparator_20261026.py` and `.json`.

## 9. Constructive Slepian subspace preserves selective-radiance geometry uniformly

The aperture bound did not settle whether representing the moving guided vector would destroy the light-cone radiation suppression. I therefore constructed the **normalized projected excitation**

    v_r(E) = P_r u(q_g(E)) / ||P_r u(q_g(E))||,

where P_r is the top-r eigenprojector of the exact guided-phase covariance. This is a static set of internal modes; only the occupied *superposition* changes with photon frequency. The definition does not assert a physical Hamiltonian that realizes v_r(E).

Let the idealized perpendicular electric-dipole angular distribution be p(μ)=3(1+μ²)/8. The exact free-space radiation Gram is G_θ,jl = ∫_{−1}^{1} p(μ) exp[i θ(j−l)μ] dμ, with θ(E)=k0(E)a. The exact angular integral is

    g(x)= (3/2)[sin(x)/x+cos(x)/x²−sin(x)/x³],   g(0)=1.

Define the normalized unwanted/wanted intensity ratio

    λ_r(E) = ρ(E) [v_r(E)^* G_θ(E) v_r(E)] /
                  [N |u(q_g(E))^* v_r(E)|²],

where ρ(E)=0.01 E/E0 is the per-emitter unwanted/guided spectral-density ratio in the declared model. For a hypothetical *isolated scalar resonant mode* with these couplings, the minimum inclusive norm error from this radiation ratio alone is 2 sqrt[λ/(1+λ)]. This is not the full scattering response of a finite array.

### Continuous-band bound without sampling-only inference

Write L(E)=sqrt(v_r(E)^*G_θ(E)v_r(E)) and c(E)=||P_r u(q_g(E))||. Let L_N=sqrt((N²−1)/12). If the projection error is at most δ<1 throughout the band, then c_min=sqrt(1−δ²), and for any two phase pairs (q,θ), (q',θ'),

    |L(q,θ)−L(q',θ')|
       <= sqrt(N) L_N [2 |q−q'|/c_min + sqrt(2/5)|θ−θ'|].     (F)

Proof: ||u'(q)||=L_N, normalized projected vectors satisfy ||v_r(q)−v_r(q')||<=2L_N|q−q'|/c_min, the free-space angular map has operator norm at most sqrt(N), and its θ derivative has norm at most sqrt(N) L_N sqrt(∫p μ²)=sqrt(N)L_N sqrt(2/5). Triangle inequality proves (F). No frequency-dependent retuning of the subspace is assumed.

On a finite energy grid, both the fundamental TE slab guided phase and θ(E) are monotone. Every in-between point is no farther from the preceding grid point than the largest adjacent guided-phase step Δq and radiation-phase step Δθ. Therefore

    L(E) <= max_grid L + sqrt(N)L_N[2Δq/c_min + sqrt(2/5)Δθ].

The radiative ratio is bounded uniformly by ρ_max(max L)^2/[N c_min²]. A similar phase-step Lipschitz bound certifies c_min from grid projection residuals. All functions at grid points are evaluated with the closed-form angular Gram, not a sampled angular quadrature. Numerical floating point eigenvectors and trigonometric evaluations are still not outward-rounded interval arithmetic; the inequalities enclosing unobserved photon frequencies are analytic.

The 1201-point executed checks yield:

| geometry | projector rank | continuous projection-error upper | continuous ideal isolated-mode loss-error upper |
|---|---:|---:|---:|
| N=33, Bragg a=λ0/4 | 5 | 0.007306 | 0.005688 |
| N=40, Bragg a=λ0/4 | 6 | 0.004873 | 0.005105 |
| N=44, off-Bragg a=λ0/6 | 5 | 0.004930 | 0.005025 |

All upper bounds are strict and substantially beneath the target 0.01 for the *projection/radiative-branching problem*. The result strengthens the earlier bare N^-2 on-shell spin-wave calculation: there is an **explicit fixed low-dimensional collective subspace** that tracks the entire chosen photon band and retains strong selective-radiance geometry. This does not prove it can be dynamically populated, excited or retrieved by a passive local control network. The previous full scattering failure therefore cannot be attributed to an inherent geometric incompatibility between broadband phase matching and selective radiance; it specifically indicts the inadequate reactive/mode synthesis in the tested simple network.

Executed checks: `astra_slepian_multimode_radiance_20261026.py` / `.json` (full angular Gram numerical diagnostic) and `astra_slepian_radiation_continuous_bound_20261026.py` / `.json` (closed-form angular Green function and continuous-phase variation bound). The latter makes no photon-gate fidelity claim.
