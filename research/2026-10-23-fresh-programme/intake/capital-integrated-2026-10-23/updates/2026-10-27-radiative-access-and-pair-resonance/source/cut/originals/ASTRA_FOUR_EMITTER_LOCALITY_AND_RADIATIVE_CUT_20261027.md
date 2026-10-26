# Four-emitter temporal radiation echoes: local dynamical compatibility and a no-bypass speed bound

27 October 2026. Independent extension of `ASTRA_SPARSE_TEMPORAL_ECHO_AND_PASSIVE_NO_GO_20261027.md` and `astra_spatiotemporal_four_emitter_sources.py`. Energy and time units: B=1. This note proves **negative interface results** and a general resource inequality; it does **not** claim a completed remote-transfer apparatus, priority, or a new fundamental interaction.

## 1. Choice against the strongest alternative

The earlier three-emitter source cancellation and four-internal-mode Hamiltonian construction are valid **for their own stated control graph**, including internal connections that permit storage transfer across the purported remote cut. The four-emitter Fourier-null source family is a logical next attack because it permits different interior emitters to be the earliest and latest radiation sources. This alone is not a dynamical transfer construction.

A serious alternative is engineered giant-atom spatial coupling and dispersion: Diekmann et al., *PRX Quantum* 7, 043013 (20 October 2026), DOI `10.1103/6wcb-nj42` obtains a continuum passive-transfer construction and finite-leg simulations >99%, with significant chiral/coupling-engineering assumptions. Kuang et al., *PRL* 137, 103605 (4 September 2026), DOI `10.1103/m2md-rxkv`, constructs engineered-dispersion passive transfer. Those alternatives deserve a head-to-head **energy / coupling / channel / bandwidth** comparison; they do not automatically inherit the finite-time exact-vacuum property asserted for this four-point source.

The present attack tests whether terminal source cancellation actually survives a **strictly local physical graph**: storage `a` and emitters `1,2` belong to the left module; storage `b` and emitters `3,4` to the right; no direct internal Hamiltonian edge joins the modules. Both couple through the same positive-frequency continuum. This is the stronger physical interface than allowing a direct emitter-2-to-emitter-3 wire.

## 2. Exact model and the old source identity

Let the bath be `L²((0,12),dω;C²)` with free energy `ω`, two propagation signs σ=±1, emitter positions `(0,1/2,1,3/2)` and

    (W q)_σ(ω) = v(ω) Σ_{j=1}^4 exp(iσωx_j) q_j,
    v(ω)=η sqrt(ω) (1-ω/12)^2, η=0.01.

Then `W` is bounded and `W* ω^{-1} W` is finite. The earlier exact source null family at equal spacing τ is

    q1=A,
    q2= -A(t-τ)-A(t+τ)+B,
    q3= A-B(t-τ)-B(t+τ),
    q4=B.

Every source is zero-extended outside `[0,T]`. Laurent identities prove that the radiation Fourier amplitudes vanish in **both** signs at `T`. For the earlier specific history, `A` is a bump on `(τ,τ+1)` and `B` on `(T-τ-1,T-τ)` with `τ=.5`, `T=12`. There is no radiation at the end from either subpulse.

## 3. The omitted equation at the inactive fourth emitter

The complete Schrödinger equations contain not just the emission source `Wq`, but also the *off-shell backaction* `W* ξ`:

    i qdot_j = (H_internal(t)u)_j + (W*ξ)_j,
    ξ(t)= -i ∫_0^t exp[-iω(t-s)] W q(s) ds.

Initially (`0<t<τ`) the previously prescribed four-emitter source has `q1=q3=q4=0` and

    q2(t)= -[4t(1-t)]³= -64t³+O(t⁴).

If emitter 4 is connected internally only to emitter 3 (with arbitrary finite hopping) and has arbitrary onsite energy, the fourth equation demands `(W* ξ)_4=0` on this interval. But directly,

    (W*ξ)_4(t) = -i ∫_0^t K42(t-s) q2(s) ds,
    K42(s)=2∫_0^12 |v(ω)|² cos[ω(x4-x2)] exp(-iωs)dω.

Here `x4-x2=1` and the **exact** zeroth moment is

    K42(0)= (η²/432)[-653+12 sin(12)+5 cos(12)] < 0.

Strict negativity follows without numerical quadrature because `12 sin(12)+5 cos(12) ≤17<653`. Therefore

    (W*ξ)_4(t) = i 16 K42(0) t⁴ + O(t⁵) ≠0

for sufficiently small positive `t`. This proves that the **old, specified four-emitter source trajectory** cannot solve a Hamiltonian with only the local fourth-emitter neighbour, regardless of whether that internal hopping is real or complex. It is not an impossibility theorem for all choices of source histories.

Independent Gauss-Legendre frequency quadrature plus time integration gives `K42(0)≈-0.000151671204913`. At `t=.01`, the calculated imaginary backaction is `-2.3690×10^-11`, converging to the `-2.4267×10^-11` leading term as t decreases. These nonzero values are tiny because η is small, but exact zero is the relevant terminal-source construction claim.

**Why simple geometric retuning fails.** A numerical separation of `x4-x2≈.48375045294` zeros `K42(0)`. It does not zero the complete memory kernel: its next moment is `M1=2∫ω|v|² cos(ωd)dω≈-0.00110824611664`. Consequently the leading unwanted drive becomes `3.2 M1 t⁵+O(t⁶)`, still nonzero. Vanishing one spectral moment is not equivalent to an identically vanishing causal convolution. Exact suppression over a finite interval needs stronger spectral orthogonality, a different active-source history, a changed internal graph, or time-dependent emitter–bath coupling.

**A partial constructive interface repair.** Multiplying the fourth emitter's entire bath coupling by a switch `λ4(t)` with `λ4=0` when `q4=0` removes the unwanted forcing while leaving `W(t)q(t)` unchanged in those intervals. A similar switch can be applied to the inactive first emitter. This preserves the *algebraic* terminal radiation-null identity for the prescribed source and repairs this particular leaf equation. It does not supply a complete positive local Hamiltonian or cure the speed-limit obstruction below. Time-dependent bath coupling is a new physical control, not a free consequence of fixed waveguide hardware.

## 4. A universal radiative-cut transfer theorem

**Theorem.** Let a one-excitation Hamiltonian on `H_L ⊕ H_R ⊕ H_B` have block form

    H(t) = [ H_L(t)     0          W_L* ]
           [ 0        H_R(t)      W_R* ]
           [ W_L      W_R         Ω    ]

where `H_L(t),H_R(t)` may contain arbitrary local self-adjoint controls, `Ω` is self-adjoint and its propagator unitary, and `W_L,W_R` are bounded *fixed* bath couplings. There is no direct L–R coupling. Let `w_L=||W_L||`, `w_R=||W_R||`. Starting with a normalized state entirely in L and empty R and bath,

    ||P_R ψ(T)|| ≤ (w_L/w_R) [cosh(w_R T)-1]   (w_R>0).  (1)

In particular exact unit-amplitude transfer requires

    T ≥ (1/w_R) arcosh(1+w_R/w_L).                   (2)

This result requires neither spectral positivity nor a finite excitation-number cutoff; it is a finite-time, one-excitation operator inequality.

**Proof.** Duhamel's formula and unitarity of the three diagonal propagators give, writing `r(t)=||ψ_R(t)||`, `b(t)=||ψ_B(t)||`,

    r(t) ≤ w_R ∫_0^t b(s) ds,
    b(t) ≤ ∫_0^t [w_L ||ψ_L(s)||+w_R r(s)]ds
         ≤ w_L t + w_R∫_0^t r(s)ds.

Hence

    r(t) ≤ (w_L w_R/2)t² + w_R² ∫_0^t (t-s)r(s)ds.

Comparison with the nonnegative solution of `R''=w_L w_R+w_R²R`, `R(0)=R'(0)=0`, gives (1) by Volterra iteration. This proof is unaffected by arbitrarily rapid local Hamiltonian control or by a gapless bath.

**Exposure corollary.** In any perfect no-bypass transfer, let `A_B=∫_0^T ||ψ_B(t)||²dt`. From `1≤w_R∫||ψ_B||dt≤w_R√(T A_B)`,

    A_B ≥ 1/(w_R² T).                               (3)

Depleting the left region similarly gives `A_B ≥1/(w_L² T)`. Thus the bus must have substantial transient occupation for fast transport through bounded couplings; exact return to bath vacuum at the final time does not remove this cost. If the bus also experiences weak independent loss κ, its leading integrated leakage is κA_B; this is an added loss-model assumption, not a universal microscopic radiation law.

## 5. Exact bath norms and resource consequences

For each local emitter, `||W_j||²=2∫|v|²dω=9.6η²`. For two neighbouring emitters the Gram matrix is

    G = [[9.6η², c],[c,9.6η²]],
    c=2η²[-10/27+(4/9)sin6+(10/27)cos6].

Thus `w_L²=w_R²=9.6η²+|c|`, giving

    w_L=w_R≈0.0314290833832 at η=.01.

At T=12, bound (1) gives

    ||P_Rψ(T)|| ≤0.07196771689,
    Prob(right) ≤0.00517935 (about 0.518%).

A completely oscillation-free analytic estimate is also enough: `w_L,w_R≤sqrt(19.2)η`, and monotonicity of the rhs of (1) implies `||P_Rψ(12)||≤cosh(sqrt(19.2)η*12)-1≈0.141455<1`. Thus the physical impossibility does **not** depend on the numerical evaluation of c.

Necessary resources for perfect transfer (not sufficient):

    T≥41.90252324 at η=.01, or
    η≥0.03491876937 at T=12 with otherwise identical bath shape.

At exactly that necessary coupling threshold, corollary (3) would require `A_B≥6.9189`, meaning at least 57.7% average occupation of the common bath over the 12-unit interval. In the original weak-coupling model the exposure lower bound is `84.36>T`, another immediate impossibility witness.

**Multiple radiative ports alternative.** If there are `n` equally bounded point-emitter ports on each side, with the same individual `||W_j||²=9.6η²`, trace positivity gives `w_L,w_R≤sqrt(9.6n)η`. Equation (1) then requires

    n ≥ ceil{[arcosh(2)/(T sqrt(9.6)η)]²}

for exact transfer under this symmetric resource ceiling. For η=.01 and T=12 the necessary count is **13 ports per side**. It is not a sufficient prescription; port phases, frequency dependence, time reversal and unwanted channels remain unresolved. This makes engineered multi-leg giant atoms a serious alternative, not a minor implementation detail.

## 6. Independently executed microscopic checks

`astra_four_emitter_radiative_cut_frontier_20261027.py` reconstructs the two-direction continuum with 40 Gauss-Legendre positive-frequency nodes per direction; it computes the exact analytic emitter Gram moments and independently exponentiates the complete Hermitian one-photon matrix.

* With local A/B Hamiltonian blocks and the shared bath but **no cross-block edge**, the computed right-region amplitude is `0.0020451481` at T=12, below the rigorous bound `0.0719677169`.
* Adding a direct internal edge e2–e3 and a four-site perfect-transfer chain gives right-region amplitude `0.9975169098`. This does **not** violate the theorem because the no-bypass assumption is deliberately removed.
* The early-time backaction residual converges toward the exact fourth-order Taylor coefficient. Tuning the separation to zero the zeroth Gram moment leaves a nonzero first moment.

These are diagnostics of the inequality and changed graph, not an optimization over all local controls and not a physical device demonstration.

## 7. Scientific decision

**Preserve:** the exact Fourier-null generator equations as source algebra; the previous positive time-dependent Hamiltonian at its larger internal-control interface; the new no-bypass speed/exposure theorem, spectral-memory compatibility failure and port-count necessity.

**Reject:** treating the previous four-emitter Fourier-null source as an already realized nearest-neighbour transfer; describing the short weak-bath echo as remote transfer; claiming a pointwise vanishing spectral Gram eliminates the full delayed backaction; importing source-free Maxwell microcausality into this positive-frequency rotating-wave Fano model. RWA's causality qualifications have been studied (Funai and Martín-Martínez, *PRD* 100, 065021, 2019; Dinc, *PRA* 102, 013727, 2020).

**Next physical attack:** increase port action, introduce genuinely switchable radiation couplings, or move to a chiral/multi-leg, dispersion-engineered waveguide with explicit finite-time source preparation. Any candidate must pass three independent tests: (i) terminal Fourier radiation-null equations, (ii) local time-resolved Schrödinger consistency, and (iii) the radiative-cut transfer and exposure resource inequalities. Prove a full device only if all three pass and the complete Hamiltonian remains positive with realistic losses.

## Files

- Executable: `/mnt/data/astra_four_emitter_radiative_cut_frontier_20261027.py`
- Executed output: `/mnt/data/astra_four_emitter_radiative_cut_frontier_20261027.json`
- Source comparator: `/mnt/data/ASTRA_SPARSE_TEMPORAL_ECHO_AND_PASSIVE_NO_GO_20261027.md`
- Prior null generator: `/mnt/data/astra_spatiotemporal_four_emitter_sources.py`
