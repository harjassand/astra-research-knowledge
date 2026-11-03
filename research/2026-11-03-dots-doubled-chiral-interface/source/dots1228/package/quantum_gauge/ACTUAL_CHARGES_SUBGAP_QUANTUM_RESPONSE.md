# Actual same-chirality charges: subgap response and quantum elimination

2026-11-03. This does NOT reconstruct a Choi parent at nonzero gauge field. It derives the first actual quantum-gauge response from the acquired ungauged gapped finite device, retaining virtual mirror terms. The uniform thermodynamic assumptions are separately marked.

## 1. Exact failure of gauged conjugate doubling

At zero background, the canonical doubling uses a conjugate fast matrix with the graded identification and flavor relabeling. Its axial charge is retained; its vector charge reverses. For a paired orbital with axial/vector eigenvalues A_e,V_e, the physical subgroup charges are

 q1=a A_e+v V_e,     q2=a A_e−v V_e.

Literal complex conjugation of a Wilson factor exp(i q1 A_link) instead produces charge−q1. Their mismatch is

 q2−(−q1)=2a A_e.

For layer(a,v)=(1,2), A_e=V_e=1 gives actual q2=−1, versus conjugate−3. For layer(−4,1), the actual charge is−5, versus conjugate+3. Equivalently, with independent axial/vector backgrounds, the zero-background relation extends schematically as

 h2(B_A,B_V)=J h1(−B_A,+B_V)* J†,

not as J h1(B_A,B_V)* J†. Precise J includes the already fixed grading/flavor conventions; the charge mismatch is independent of those conventions.

Consequently W(sign h(A)) built by simply copying the old phase-free conjugate purification would generally change the gauged representation. No such replacement is used below. The previously proved free magnetic gap can persist while this algebraic purification identity fails.

## 2. Actual vertices, not a new model

Start with the actually onsite, finite-charge, finite-range device h_g(A) obtained by tree-gauging EVERY original interacting term. Its acquired ungauged gapped block has H0Ω=0 and H0≥ΔQ, Q=1−|Ω><Ω|. Define directly

 J_l=∂_(A_l) h_g(A)|_(A=0),
 K_lm=∂_(A_l)∂_(A_m) h_g(A)|_(A=0).

These are finite local many-body operators, computable from the actual integer charge transfer circuit. They include the two copies' ACTUAL different charges. For a tree-gauged term, they are nested commutators with its path-charge generators, so their norms and support follow from the charge/range ledger, without diagonalizing a gauged ground state or supplying an interface-response oracle.

The same construction gives all higher vertices and Taylor remainder bounds. If B_X(A)=Σ_l A_l B_Xl is the commuting path-charge generator for term X, Taylor's integral formula bounds the third-order remainder by

 ||remainder_X(A)||≤(8/6)||h_X||[Σ_l |A_l| ||B_Xl||]^3.

This is an operator bound on a coordinate chart, not a claim that the unbounded rescaled photon coordinate is norm-small. Applied to states it is controlled by their sixth moments.

## 3. Earned subgap polarization of this actual gapped block

For real |ω|<Δ the retarded mirror polarization is, with convention-dependent overall Fourier signs fixed consistently,

 Π_lm(ω)=<K_lm>
 −<Ω,J_l Q(H0−ω)^−1 QJ_m Ω>
 −<Ω,J_m Q(H0+ω)^−1 QJ_l Ω>.

The contact/diamagnetic term <K_lm> is compulsory. Both resolvents exist, and

 |Π_lm(ω)−<K_lm>|≤2||J_l||||J_m||/(Δ−|ω|).

There is no absorptive spectral weight from this block for |ω|<Δ. The function is analytic in that disk. This uses the full interacting many-body gap, not the single-particle propagator and not a Green-function zero ansatz. At finite size it is a directly computable response of the actual model.

Spatial locality can be proved whenever Δ and the interaction norm/range are uniform: choose a smooth frequency filter with transform fhat_ω(E)=1/(E−ω) on E≥Δ, zero near E=0, and smoothly continued on negative frequencies without singularities. Its time kernel has all finite moments, uniformly for |ω|≤Ω_*<Δ. Then

 B_m(ω)=∫f_ω(t)e^(itH0) J_m e^(−itH0)dt,
 B_m(ω)Ω=Q(H0−ω)^−1QJ_mΩ.

Matter Lieb–Robinson bounds give B_m rapidly decaying spatial tails with range set by v_m/(Δ−Ω_*). Combining this with gapped ground-state clustering bounds the connected susceptibility at separated supports by rapidly decaying functions. Thus the low-frequency response is local, rather than a massless mirror pole hidden by a fermion propagator zero. This statement does NOT prove that the complete gauged model retains the gap at finite g, nor that every coefficient has the correct target continuum normalization.

For the presently acquired finite-volume auxiliary regulator, N and possibly R depend on volume. Insert those actual norms and lengths in this estimate. There is not yet one fixed-capacity thermodynamic family with these uniform constants.

## 4. Quantum photons: denominators depend on photon frequency, not vacuum energy

Use the weak-field Maxwell reference of the SAME compact Wilson Hamiltonian, in a physical transverse gauge, with Gauss's law retaining its Coulomb contribution. Write A_l=g a_l and

 H_Max−E_vac=Σ_k ω_k b_k†b_k,
 a_l=Σ_k(f_lk b_k+f_lk* b_k†).

The vacuum energy is subtracted as an explicit scalar here, not discarded from a positivity estimate on the separate electric or magnetic terms. The longitudinal electric/Coulomb interaction appears at order g² and must be included in V2. On a coarse cubic gauge lattice ω_max≤2sqrt(d)/a_g. Choose a_g so Ω_g:=ω_max<Δ, preferably Ω_g≤Δ/2. This is a paid separation of gauge UV and mirror scales; it is not the original all-scales continuum limit.

To first order the actual interaction is V1=Σ_l a_l J_l. Put J_k=Σ_l f_lk J_l. The rest-off-diagonal operator is built with QJ_kP and its adjoints, where P=|Ω><Ω|. Define an antihermitian Schrieffer–Wolff generator S by its QP block

 S_QP=Σ_k[ (H0−ω_k)^−1 QJ_kP b_k
             +(H0+ω_k)^−1 QJ_k†P b_k† ],
 S_PQ=−S_QP†.

Then [H0+H_Max,S]=V1_off exactly on the finite-particle core. Under e^(gS), the order-g off-diagonal interaction cancels. The denominators are bounded by(Δ−Ω_g)^−1 even though total gauge bandwidth and total zero-point energy are unbounded/extensive.

On a photon sector with at most n quanta,

 ||S P_≤n||≤[2sqrt(n+1)/(Δ−Ω_g)] Σ_k||J_k||=:s_n.

For a fixed device this is a fully paid finite sum. It is deliberately not advertised as a volume-uniform norm. Local versions follow from the filtered response kernel, with locality limited by the photon and matter support as well as any transverse-gauge Coulomb tails.

The induced low-rest Hamiltonian through second order is

 H_eff=H_Max+gPV1P+g²P[V2+(1/2)[S,V1_off]]P+O(g³),

where V2 contains the actual K_lm a_l a_m/2, longitudinal Coulomb energy, and the compact magnetic quartic correction. Omitting the paramagnetic commutator or the diamagnetic/contact term would give the wrong gauge response. The resulting photon bilinears reproduce the resolvent polarization of §3. This is an actual-current construction, so the charge mismatch in §1 cannot be bypassed by a hidden vectorlike replacement.

The formula is an exact algebraic first-order block elimination on a dense finite-particle core. A claimed nonperturbative error bound needs photon moment/capacity bounds and a chosen remainder order; it is NOT obtained merely by exponentiating this unbounded S on the entire Fock space. For bounded finite-device capacities, all factors are finite matrices and Taylor/Duhamel remainders are explicitly bounded by nested-commutator norms. Boundary overflow and compact-coordinate errors must be charged separately, rather than declared absent.

## 5. Relation to Berry and Born–Huang terms

A slowly moving link configuration has the exact projected electric form

 (κ_E/2)Σ_l||(-i∂_l+mathcal A_l)f||²
 +<f,[H_B+E0(A)+Phi_BH]f>,
 mathcal A_l=−i<Ω(A),∂_lΩ(A)>,
 Phi_BH=(κ_E/2)Σ_l||Q(A)∂_lΩ(A)||².

This is consistent with the virtual response expansion, not a license to delete its terms. The local Berry curvature is

 mathcal F_lm=2 Im<Ω,J_l Q H0^(−2) QJ_mΩ>

up to the sign convention chosen for mathcal A; the unambiguous derivation is differentiating mathcal A=−i<Ω,dΩ>. In that stated convention the displayed plus sign follows. The metric/Born–Huang matrix uses the real part of the same H0^(−2) kernel. These are computable from the ACTUAL current vertices; conjugation of the second copy is not assumed to cancel them.

## 6. A desired distant light face: finite-time response, not a global gap claim

For an actual physical near-interface observable/current, compare the one-light-face device with the two-massed-face reference. If their local Hamiltonians agree within a distance L of that current and differ only at the remote face, the ordinary ungauged matter Lieb–Robinson estimate bounds their Heisenberg-current difference through time T by C exp[−μ(L−v_m T)], with the appropriate area/support factors paid. Thus finite-time near-interface current experiments can use the gapped reference response without taking sign(h) of the gapless full slab.

This comparison requires actual agreement of the prepared reduced initial states in the relevant light cone (or an added trace-distance term). Agreement of Hamiltonians alone does not identify their ground states. Infinite-time Fourier response cannot be deduced by letting T→∞ at fixed L. The independently acquired finite-device rest gap can alternatively justify selected low-energy experiments, but a sharp projected far momentum band is nonlocal and cannot be silently assigned a uniform spatial Lieb–Robinson bound.

## 7. Predictive boundary and strongest ordinary alternative

What is now concrete is the actual finite-device current/polarization calculation and a quantum, subgap, single-photon/low-occupation elimination mechanism whose denominator does not contain extensive gauge vacuum energy. It can test a real finite-device response at a chosen nonzero coupling after paying photon capacity and perturbative remainder. It does not produce an all-time or finite-energy-density gap from the ungauged gap alone. Multiphoton processes can reach the mirror threshold, and a desired light face, fixed local capacity, and uniform interacting weak-curvature response remain separate gates.

This is the standard physical decoupling principle applied to a newly explicit microscopic mirror parent, not a claimed improvement over established anomaly-free Abelian overlap gauge reconstruction. Exact gaugeability, an ungauged rest gap, and a local analytic reduced response are each useful, but none alone resolves the nonperturbative fixed-coupling chiral-gauge problem. The ordinary Lüscher construction and the propagator-zero/SMG constraints remain the comparator; no claim of a Standard Model, continuum limit, or novelty is made.

## 8. A completed bounded-capacity second-order elimination theorem

Here is an explicit error certificate rather than an unqualified formal SW expansion. It applies to the finite photon-capacity weak-field Hamiltonian, with any error in its approximation to compact quantum links charged separately.

Use a finite tensor of truncated oscillator modes. The exact identities [H_Max,b_k]=−ω_k b_k and [H_Max,b_k†]=ω_k b_k† remain true even at the truncation boundary; canonical [b,b†]=1 is NOT needed. Write the computed finite matrix as

 H=H00+gV1+g²V2+R,   ||R||≤r|g|³,
 H00=H0+H_Max,   ||V1||≤L1, ||V2||≤L2.

Require 2Ω_g<Δ. The first generator S above remains exact. Let s=||S||, bounded by its finite mode sum. Put

 D1=(V1)_diag,
 W2=V2+[S,(V1)_diag]+(1/2)[S,(V1)_off].

All off-diagonal rest blocks of W2 have photon frequency shifts of magnitude at most2Ω_g: its matter-dependent terms are quadratic or lower in b,b†. The magnetic quartic is proportional to identity on rest and has no off-diagonal rest block. The Coulomb term has photon frequency shift zero. Decompose the computed (W2)_QP into photon monomials A_nu B_nu, with [H_Max,B_nu]=omega_nu B_nu. Define

 (S2)_QP=Σ_nu(H0+omega_nu)^−1 Q A_nu P B_nu,
 (S2)_PQ=−(S2)_QP†.

Then [H00,S2]=(W2)_off and all denominators≥Δ−2Ω_g. Define s2 by the explicit triangle bound2Σ_nu||A_nu||||B_nu||/(Δ−2Ω_g), so ||S2||≤s2. Mode enumeration is finite. It can be enormous; no polynomial classical solution of the interacting rest is claimed.

Take U=exp(g²S2)exp(gS). Direct BCH/Duhamel estimates give

 UHU†=H00+gD1+g²(W2)_diag+R3,

with, for |g|≤1, the explicit conservative bound

 ||R3||≤|g|³ C3,
 C3=exp(2s)[(8/3)s²L1+2sL2]+r
       +2s2 L1+2s2||W2||+2s2||(W2)_off|| exp(2s2).

Explanation of the constants: the first two BCH tails cost(8/3)s²L1, conjugating g²V2 costs2sL2, and R is unitary invariant. The second transformation changes gD1 by at most2|g|³s2L1, changes g²W2 by at most2g⁴s2||W2||, and its second-and-higher commutators with H00 cost at most2g⁴s2||(W2)_off||exp(2g²s2). Replacing g⁴ by|g|³ gives the displayed safe expression.

The comparison Hamiltonian H_bd=H00+gD1+g²(W2)_diag preserves P EXACTLY. Therefore

 ||e^(−itH)−U†e^(−itH_bd)U||≤|t| |g|³ C3.

For a dressed initial state U†Pψ, leakage out of the dressed rest-ground subspace is≤|t||g|³C3. For a bare P initial state, the bare-rest leakage bound acquires at most2(|g|s+g²s2), the physical virtual-mirror dressing. All target photon predictions in operator norm have the same dynamical error, plus the appropriate initial/observable dressing.

This is a nonzero-coupling, finite-energy/capacity, finite-time prediction with explicit matrices and errors. It can resolve the actual O(g²) virtual mirror polarization for times with |t||g|³C3 small. It does not require the total photon zero-point energy or total matter norm to be smaller than Δ. It DOES require a slow gauge UV and paid photon capacity. Rest or photon truncation errors add by Duhamel, not by wishful identification.

## 9. Exact remaining compact-link and target-transfer costs

To identify §8 with a prescribed compact-link experiment one must pay:

- The weak-field chart/periodic seam probability and kinetic cutoff-shell errors.
- Photon capacity overflow under the chosen initial state and time evolution.
- The sixth-moment remainder of actual matter link exponentials and higher compact magnetic terms.
- Any initial state preparation and response-filter approximation errors.

The local electric/curvature moment theorem pays a useful second-moment part of this list, but not all higher moments or capacity tails automatically. A finite electric-register compiler supplies an alternative exact compact Hamiltonian simulation, but a mere link register cutoff is not the same as the low-photon spectral truncation used in this theorem. These maps must not be conflated.

Similarly, an ungauged global norm estimate ||H_phys(0)−(H_F+K_Q)||≤epsilon does NOT by itself bound derivatives of the separately gauged models. Small ungauged differences can rely on cancellations destroyed by path dressing. To transfer §8 to the desired light+rest device, either acquire a termwise gauged approximation bound (including current/contact vertices), or compute the actual device vertices and prove their rest-transition frequency bounds. This is a concrete remaining operation. The finite gapped block's prediction is earned; the full chiral-device prediction is not silently inherited.

### Gauge-invariant mismatch diagnostic

The mismatch is not merely an inconvenient choice of link gauge. Around a plaquette of flux F, a charge-q Wilson product is exp(iqF). For the first example, actual copy2 gives exp(−iF) while conjugating copy1 gives exp(−3iF); their ratio is exp(2iF). No site-dependent gauge transformation changes this loop ratio. At nonzero generic curvature it cannot be repaired by a link-independent grading/flavor unitary. A curvature-dependent repair would be a NEW physical operation and must preserve the charge representation; it is not supplied by the zero-background identity.

### Exact tree-gauge electric correction to the photon vertices

COMPACT_LINK_DYSON_RESIDUAL_CERTIFICATE.md solves Gauss law without a nonperiodic Coulomb transformation. In that chart the order-g interaction also contains p^T RQ/a, and order-g² contains Q^T C_QQ/(2a). Include the p term in the mode coefficients J_k of §4 and §8; it is still linear in b,b†, so all frequency-denominator and photon-degree arguments remain unchanged. Omitting it would correspond to using a different gauge/dressing and would require proving that transformation, including its boundary conditions. The compact residual certificate pays chart-shell errors and actual higher moments explicitly, rather than assuming a photon-register truncation.
