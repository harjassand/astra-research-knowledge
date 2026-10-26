# ASTRA foundational physics — a reciprocal two-port capacity gate, passive rank law and independent-loss obstruction

26 October 2026. Independent continuation from `ASTRA_PASSIVE_POLE_ACHROMAT_20261026.md`. Mathematical construction and executed numerical checks, not an experimental device or a claim of historical novelty. The earlier homogeneous Jacobi-chain single-impurity capacity-two question remains open. All energies use the memory binding scale B=1 and ℏ=1.

## Scientific comparison and reason for changing the physical interface

The previous model achieved a mathematically certified 0.1 half-bandwidth with frequency-dependent orthogonal coupling vectors in two *chiral*, deliberately phase-matched photon continua, three side modes, a 10% port-intensity mismatch and a large charge-dependent emitter-frequency shift. Its limiting physical assumption was identical propagation delays and engineered relative coupling signs; a mismatch could destroy the tight frame. The alternative here uses one ordinary **reciprocal bidirectional** waveguide with two localized emitter attachments. It gives up the exact spectral tight-frame property but inherits **energy-independent emitter parity sectors**, which survive any reciprocal single-band dispersion law with conjugate forward/backward phases. Two passive side modes suffice to cancel the first two reactive scattering derivatives independently in these sectors. It avoids assumed chirality, nonreciprocal hopping, and a contrived sign pattern between two independent chiral guides. It has a narrower certified band and still requires large controls and extremely low independent radiation loss.

Recent giant-atom literature establishes substantial prior physical context for spatial phase engineering and delayed coupling (e.g. https://doi.org/10.1103/crzs-k718 and https://doi.org/10.1002/qute.70469). The present analysis is an exact restricted-Hamiltonian resource construction, not a novelty or superiority claim.

## 1. Complete physical Hamiltonian and exact reciprocal parity decomposition

Let memory contain m hard-core sites with conserved charge K in {0,...,m}, bare H_mem=-K and optionally a positive graph-Laplacian exchange interaction T satisfying [T,K]=0 and annihilating one state in each K sector (the Dicke states). Couple a two-emitter *signal* subsystem with hard-core emitter occupations to memory via the pairwise longitudinal interaction

    H_charge = chi (m-K) (n_e1+n_e2).

For each memory charge k, one-body signal Hilbert space is C²_emit ⊕ C²_side ⊕ L²((0,2),dω;C²_right,left). The two positive-energy harmonic side oscillators couple to symmetric/antisymmetric emitters, with energies Ω_+, Ω_- and residues r_+,r_->0. The parity emitter bare energies are ε_+,ε_-. Write |+>=(|e1>+|e2>)/sqrt(2), |->=(|e1>-|e2>)/sqrt(2). In emitter coordinates the photon form factors are

    v_R(ω) = sqrt(γ) ω/sqrt(2) (1,e^{+i τω})ᵀ,
    v_L(ω) = sqrt(γ) ω/sqrt(2) (1,e^{-i τω})ᵀ,  0<ω<2.

These obey ordinary reciprocity. They correspond to two equal local attachments at separated points in an ideal linear-dispersion bidirectional 1D waveguide, without an artificial direction-dependent coupling sign. A physical realization of the ω envelope, band edges, and parity-selective auxiliary contacts is a separate engineering question. Both outgoing directions are retained; no reflection or radiation is silently discarded. Hard-core signal-emitter compression does not alter the one-photon Hamiltonian and cannot lower a positive quadratic form in higher sectors.

The complete emitter spectral density matrix is

    V(ω)V(ω)†= γω²[I + cos(τω) σ_x].                         (1)

Thus *all frequencies* have the same two emitter parity eigenvectors. The parity spectral weights are

    f_p(ω)=ω²[1+p cos(τω)],  p=+1,-1.                      (2)

This exact decomposition persists if τω is replaced by a real frequency-dependent phase θ(ω)=k(ω)L and the two directions retain conjugate phases, even when θ is nonlinear. It fails if directional couplings are not reciprocal or equal in strength. By contrast, a tight frame VV† proportional to I cannot hold throughout an open band for θ(ω) nonconstant, except accidental degeneracies at isolated energies.

Define the real principal-value function

    B_p(E)=PV ∫₀² f_p(ω)/(ω-E) dω, 0<E<2.                (3)

The complete one-photon on-shell denominator in parity p, including the side resonator, is

    D_{p,k}(E)=q_p(E) - χ(m-k) + i a_p(E),
    q_p(E)=E-ε_p+γ B_p(E)+r_p/(Ω_p-E),
    a_p(E)=π γ E²[1+p cos(τE)]>0.                       (4)

The side mode contributes exactly r_p/(Ω_p-E) from Schur elimination. The exact two-port physical S matrix has eigenvalues

    s_{p,k}(E)=[q_p(E)-χ(m-k)-i a_p(E)]/
               [q_p(E)-χ(m-k)+i a_p(E)].               (5)

Its eigenvectors in photon-port coordinates vary with energy; nevertheless its operator norms are governed by these two scalar eigenvalues. This is an exact full two-port result, not a selected-parity input model. The emitter is hard-core, side resonators and photon modes are bosonic, and all further signal excitations remain in the full finite-particle Hamiltonian.

## 2. Explicit passive cubic-flat calibration

Use E₀=3/2, γ=1, τ=11/10 and operate on E∈[1.452,1.548]. Set

    t_p=-1-γ B'_p(E₀),
    d_p=-2 t_p/(γ B''_p(E₀)),
    Ω_p=E₀+d_p,  r_p=t_p d_p²,
    ε_p=E₀+γ B_p(E₀)+r_p/d_p.                             (6)

For both p, exact-rational series enclosures prove t_p,d_p,r_p>0 and Ω_p>1.548. Then

    q_p(E₀)=q'_p(E₀)=q''_p(E₀)=0.                           (7)

Displayed approximations (the exact controls are *defined* by the integrals and (6)):

| p | Ω_p | r_p | ε_p |
|---|---:|---:|---:|
| + | 3.9916289178 | 51.9212685917 | 21.8288868891 |
| − | 1.6851241076 | 0.1449097322 | 7.8484115672 |

Both physical auxiliary oscillators have positive frequencies and positive coupling residues. All hopping can be chosen real in the localized emitter basis; no artificial magnetic flux is needed. The stronger symmetric auxiliary has coupling amplitude sqrt(r_+)≈7.206, so this is a high-resource construction rather than a low-control proposal. The total memory-charge-dependent emitter frequency span remains χm, with χ=1800.

### Continuous-band certificate, not frequency sampling

Let I_n(E)=PV ∫₀² ωⁿ/(ω-E)dω. Exact division gives

    I_n(E)= Σ_{j=0}^{n−1} [2^(n−j) E^j/(n−j)]
            + Eⁿ log((2-E)/E).                           (8)

Expanding cos(τω), B_p=I_2+p Σ_{n≥0}(-1)^n τ^{2n}I_{2n+2}/(2n)!.
At E₀=3/2, log(1/3) has a rational artanh expansion. The executed `astra_reciprocal_parity_interval_certificate_20261026.py` encloses the first 20 cosine terms and 65 logarithm terms with exact Fraction arithmetic. The full cosine-derivative tail through derivative two is bounded by 1.814×10^−27, using |I_n^{(j)}(E₀)|≤100 n³2ⁿ for j≤2. This gives narrow rational intervals for B_p(E₀), B'_p(E₀), B''_p(E₀), and (6).

For E∈[1.452,1.548], write f(E)=E²[1+p cos(τE)] and L(E)=log((2-E)/E). The identity

    B_p(E)=f(E)L(E)+∫₀²∫₀¹ f'[E+u(ω-E)]du dω

is an ordinary nonsingular double integral. Differentiating three times proves

 |B_p'''(E)| ≤ |f'''||L|+3|f''||L'|+3|f'||L''|
                 +|f||L'''|+(1/2)sup_{0≤x≤2}|f''''(x)|
              < 415.359.                                (9)

All inequalities (including bounds on log and π) are checked by rational arithmetic, using sin and cos bounded by one. Since the three lower Taylor coefficients of q vanish exactly, its absolute remainder is bounded by

    |q_p(E)| ≤ γ(415.359)|E-E₀|³/6
                   + r_p |E-E₀|³/[d_p³(d_p−|E-E₀|)].     (10)

The certified radiation-halfwidth lower bound over the entire band is min_{p,E} a_p(E)>5.7491. The exact all-output eigenvalue identities give

    |s_{p,m}(E)+1|≤ 2|q_p(E)|/a_p(E),
    |s_{p,k<m}(E)-1|≤ 2 a_p(E)/[χ−|q_p(E)|].               (11)

The conservative interval result (both propagation directions, all photon superpositions) is

    sup_{E∈[1.452,1.548]} ||S_full(E)+I₂|| < 0.009071721,
    sup_{E∈[1.452,1.548]} ||S_not_full(E)-I₂|| < 0.009469018.   (12)

These bounds hold on **all normalized one-photon spectral wavepackets supported on this band**, with arbitrary memory/reference entanglement. They are for asymptotic, stationary scattering of the complete lossless model; not finite-duration source, trapping, leakage into missing physical channels, or an acquired working gate.

The independent `astra_reciprocal_full_hamiltonian_audit_20261026.py` diagonalizes/inverts the actual four-internal-mode Hamiltonian (two emitters plus two side modes), retaining both waveguide ports. Direct S matrices agree with scalar parity eigenvalues within 3.5×10^−15, unitarity error is below 2.8×10^−15. The sampled max selected operator error is 0.003503 and unselected 0.009466; these sample values are diagnostics, **not** what supports (12).

## 3. An actual all-particle capacity theorem

For k fixed, complete the square in the zero-energy one-body quadratic signal form, eliminating positive waveguide and side-mode coordinates. In each emitter parity channel the remaining coefficient is

    C_p=ε_p+χ(m-k)-γ∫₀² ω[1+p cos(τω)]dω-r_p/Ω_p.        (13)

The elementary bound 0≤∫ ω[1±cos]≤4 and exact-rational (6) imply, for all k≤m,

    C_+>4.8213,  C_->3.7624.                             (14)

Therefore the complete signal one-particle operator h_k≥0, even though the photon continuum is gapless and the side-mode energies differ. Every fixed-particle restriction of dΓ(h_k) is nonnegative. The physical hard-core emitter operator is a form compression and remains nonnegative. Since a memory sector with k excitations has memory energy at least −k, the complete total-N Hamiltonian satisfies H_N≥−min(N,m). Fill N memory sites for N≤m, or fill m sites and let N−m photons approach zero energy, giving the matching upper threshold:

    inf spec H_N = −min(N,m), for every finite N.          (15)

For N>m equality is a soft-photon dissociation threshold, **not** a new normalizable bound cluster. The theorem is true for the specified reciprocal architecture, not the original homogeneous Jacobi single-impurity operator. It survives replacing independent memory sites by the graph-Laplacian interaction T described above, because T≥0, [T,K]=0, and Dicke states saturate the memory-sector minima. The selected photon S matrix is compatible with these entangled stored states because the signal Hamiltonian depends only on K.

## 4. Two exact passive-resource obstructions

**Minimum number of side modes.** At E₀, prior to side-mode addition, the reactive slope matrix is

    R'_0(E₀) = (1+γ B'_+)P_+ + (1+γ B'_-)P_-.

Both eigenvalues are strictly negative by the exact-rational intervals; t_+≈8.3633, t_-≈4.2284. An ordinary positive-energy passive side oscillator with coupling column g_j adds the positive rank-one matrix g_jg_j†/(Ω_j-E₀)² to this slope. Cancelling both negative eigenvalues requires a positive correction of rank two. **At least two independent passive side-mode columns are necessary** in this fixed bare-spectral family, even if their couplings are allowed to mix the parity directions. The design in (6) attains this lower bound.

**An in-band pole is unavoidable in the odd parity channel.** If every positive-residue pole lies at Ω_j≤E₀ or Ω_j≥2, write d_j=Ω_j−E₀. Terms at d_j<0 contribute r_j/d_j³<0. Terms at d_j≥1/2 obey r_j/d_j³≤2r_j/d_j². Thus necessarily

    Σ_j r_j/d_j³ ≤ 2 Σ_j r_j/d_j².

But canceling the odd-channel first and second derivatives requires

    Σ_j r_j/d_j²=t_-=4.22836...,
    Σ_j r_j/d_j³=−γ B''_-/2=22.84066...,

and 22.84066−2(4.22836)>14.38. Contradiction. Therefore **at least one side-mode pole must lie in (E₀,2)**. This is a real resource/dispersion cost; it is not a no-go for arbitrary frequency-dependent controls or different waveguide spectral envelopes.

More generally, a base reactive-slope matrix with r negative eigenvalues requires at least r positive rank-one side-mode residues to make the full slope zero, provided the other controls do not contribute frequency dependence. This is an inertia/rank rule, not evidence of a new fundamental force.

## 5. Physical attack: two independent radiation continua

The bidirectional waveguide still ignores unguided radiative emission. Add **two independent physical loss continua**, one per emitter, with on-shell spectral-density matrix κE²I₂ and causal principal-value response κA(E)I₂, where A(E)=2+2E+E² log((2−E)/E). All four outgoing photon ports are retained. Retune the bare emitter energies by +κA(E₀), maintaining the selected real resonance center. The one-body positivity margins survive because the zero-energy subtraction changes by κ(A(E₀)−2)>0.

At E₀, in parity p let a_p=πγ E₀²(1+p cosτE₀) be the wanted-waveguide radiative halfwidth and ell=πκE₀² the independent-radiation halfwidth. With an arbitrary real resonant detuning q, the wanted output and total loss output satisfy

    S_w=1−2i a_p/[q+i(a_p+ell)],
    ||S_loss||=2 sqrt(a_p ell)/sqrt(q²+(a_p+ell)²).

The **complete physical output-state** error against an ideal negative phase is

    ε_p(q)²=|S_w+1|²+||S_loss||²
           =4[q²+ell(a_p+ell)]/[q²+(a_p+ell)²].          (16)

It is minimized at q=0, so no Hermitian on-site frequency retuning can beat

    ε_{p,min} = 2 sqrt[ell/(a_p+ell)].                    (17)

For a 1% full-state error on *both* physical photon input modes, a necessary condition is

    κ/γ < (0.01²/[4−0.01²]) [1−|cos(1.65)|]
         = 2.3022553344×10^−5.                           (18)

This **necessary**, not sufficient, condition is notably more severe than the already excellent ideal lossless wavepacket bound. In the actual four-port executed diagnostic with center-retuned causal Lamb shift, κ/γ=2×10^−5 gives a max selected **right-incident** photon error 0.009356 on an energy grid; 3×10^−5 gives 0.011324. Those grid maxima are *not* interval certificates or a physical calibration guarantee. The precise matrix scattering is unitary when all four ports are included, with residual below 4×10^−15. The obstruction applies to genuinely independent radiation with full emitter-space rank, not specially correlated decoherence-free radiation channels.

The sharper scientific distinction: **all-N spectral capacity survives these independent channels while coherent gate fidelity need not**. Hamiltonian boundedness is not a certificate of useful quantum operations.

## 6. Robustness, limits and the next physical attack

Because the reciprocal spectral matrix is a linear combination of I and σ_x at every frequency, the exact parity reduction remains valid for an arbitrary real dispersive phase θ(ω)=k(ω)L and any common nonnegative spectral envelope, provided both directions share conjugate phases and equal attachment strengths. Its B_±, poles and margins need to be recalibrated; the numerical 0.048 bandwidth is **not** inherited without a new certificate. The inequalities defining positive residues, separated poles and positive Schur margins are strict here, so an open set of sufficiently small smooth reciprocal spectral perturbations retains a calibrated version of the construction by continuity. No fabrication tolerance is inferred.

Important costs and missing physical interfaces: the symmetric side-mode coupling sqrt(r_+)≈7.206, emitter bare energies ε_+≈21.83 and ε_-≈7.85, a side pole inside the guided photon band, collective memory-charge shift χ(m−K) with χ=1800 per missing excitation, independent side-mode parity access, possible radiative/bath dephasing, photon injection/retrieval, finite-time pulse duration, and the physical origin of the assumed ω envelope and sharp spectral cutoff. No hardware controls or measured losses have been acquired. Optical/solid-state realizations may not reproduce the exact spectral functions.

**Strongest next test:** Derive both parity-selective side-mode contacts and the memory-charge shift from one realistic two-emitter/two-cavity microscopic circuit, with all independent radiative baths included and controls limited to accessible local parameters. If κ/γ cannot satisfy (18) at plausible device parameters, pursue a correlated-loss architecture or move resources back to foundational continuum spectra; further idealized phase-flattening alone will not address the decisive blocker.

## Reproducibility and primary source notes

- `astra_reciprocal_parity_design_probe_20261026.py`: arbitrary-precision PV derivative formulation, pole and Schur-margin feasibility over τ,γ.
- `astra_reciprocal_full_scattering_search_20261026.py` / `.json`: parity scattering formula with candidate probes. Its grid is exploratory only.
- `astra_reciprocal_parity_interval_certificate_20261026.py` / `.json`: **governing exact-rational continuous-band certificate**, positivity bounds, rank-two necessary condition, mandatory odd-sector in-band side pole.
- `astra_reciprocal_full_hamiltonian_audit_20261026.py` / `.json`: independent full 4×4 internal inversion, both photon ports, exact parity equivalence and energy-form positivity.
- `astra_reciprocal_independent_loss_audit_20261026.py` / `.json`: fully retained additional radiative channels, exact center obstruction and causal finite-grid physical-output checks.
- Historical precursor `ASTRA_PASSIVE_POLE_ACHROMAT_20261026.md`, and original uploaded `CONCAVE_SCHUR_IMPURITY_CAPACITY(1).txt`, `TRIPLE_CORNER_AND_CAPACITY_HIERARCHY(1).txt`.

Research antecedents: Shi et al., *Phys. Rev. X* 6 021027 (2016), https://arxiv.org/abs/1512.07238 ; Heeres et al., *Phys. Rev. Lett.* 115 137002 (2015), https://doi.org/10.1103/PhysRevLett.115.137002 ; Du et al., *Phys. Rev. Lett.* 135 223601 (2025), https://doi.org/10.1103/crzs-k718 ; Wang et al., *Advanced Quantum Technologies* (2026), https://doi.org/10.1002/qute.70469 . Prior quantum routing/interference and giant-atom designs overlap broadly; uniqueness, priority and physical advantage remain unknown.

## 7. Second attack: realize the parity poles using an ordinary reciprocal auxiliary graph

A parity-eigenmode coupler need not be assumed as an indivisible hardware component. Two actual positive-frequency auxiliary oscillators b₁,b₂ suffice. In their **localized** basis choose

    H_side = Ω₀ I + J σ_x,
    G_emit,side = g_d I + g_c σ_x,                       (19)

with all entries real; the two emitter modes couple directly and across to the auxiliary nodes. Under the common parity basis transform, H_side has energies Ω₀±J and G has couplings g_d±g_c. Its exact eliminated emitter self-energy is

    G(H_side−E)⁻¹Gᵀ = r_+ P_+/(Ω_+−E)
                       + r_- P_-/(Ω_-−E).                (20)

The previously certified poles are reproduced by the **positive, real** choices

    Ω₀=(Ω_++Ω_-)/2 ≈ 2.8383765127,
    J=(Ω_+−Ω_-)/2 ≈ 1.1532524051,
    g_d=(sqrt(r_+)+sqrt(r_-))/2 ≈ 3.7931557757,
    g_c=(sqrt(r_+)−sqrt(r_-))/2 ≈ 3.4124856663.           (21)

Direct inversion of the two-local-side-node matrix matches the two-parity-pole resolvent on 101 probe energies with residual <2×10^−13. More importantly, (20) is an exact identity, so the entire continuous-band certificate and all-N positivity theorem transfer *unchanged* to this local-node Hamiltonian. No chiral auxiliary field, imaginary hopping, active gain or effective negative residue is required.

**Structural cost:** The cross-coupling is 89.9643% of the direct coupling. If the auxiliary graph is required to have *only* local matching contacts G=diag(g₁,g₂), and its site frequencies/hopping preserve reflection symmetry, the induced self-energy commutes with emitter parity for all E only when |g₁|=|g₂| (up to degenerate cases). Its two parity residues are then equal. Because r_+/r_-≈358.3, the exact present cubic-flat design **cannot** arise from that stricter two-site-local matching graph. A strongly crossed real coupling or a larger alternative passive network is needed. This no-go is specific to exact reflection-symmetric two-mode side networks, not a statement about all local quantum devices.

Script: `astra_reciprocal_passive_bus_realization_20261026.py`, numerical identity audit `astra_reciprocal_passive_bus_results_20261026.json`.
