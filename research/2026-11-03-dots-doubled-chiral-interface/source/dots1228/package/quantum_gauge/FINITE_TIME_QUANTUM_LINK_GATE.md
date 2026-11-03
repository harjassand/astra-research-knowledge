# Actual compact quantum links: an acquired finite-time gate, and its scope

2026-11-03. This is a derived finite-volume real-time criterion, not a thermodynamic chiral gauge theorem. It uses the paid finite-volume matter regulator after the actual shared-rotor disentangler. No gauge electric cutoff or hard admissibility wall is imposed.

## 1. Actual matter input and charges

Use layers (a,v)=(1,2),(-4,1), with two same-chirality copies. Before optional removal of the vectorlike ±3 pair, charges per copy are (3,-1,-1,-1,-3,-5,4,4). The source construction supplies the actual finite-range matter Hamiltonian after D†; the finite auxiliary compression supplies a finite-volume unique neutral ground, energy shifted to zero, with proven gap Δ>0. Call it h(0)=Σ_X h_X. Terms are made individually globally U(1)-invariant by onsite twirling. The finite auxiliary worker confirms Q_x=L_theta+Σ_f q_f n_f+fixed integer countercharge, and neutral matter phi rotors. Thus ||Q_x||≤N+Σ_f|q_f|+|countercharge|=:q_x. Keep the UV normal lattice sites explicit.

This input is directly the two-massed-face gapped block. Identifying its projector with a mirror projector in a slab having a desired gapless face is NOT justified. The light-face issue is stated in §8.

## 2. Actual local gauging, including many-body charge transfer

On each oriented gauge link put L²(U(1)), angle A_l mod2π, E_l=-i∂_l. For each connected enlarged interaction support X choose a fixed local tree rooted at r. Let θ_x(A) be the oriented path sum from r to x. Set

 V_X(A)=exp[-iΣ_(x∈X) θ_x(A) Q_x],  h_X(A)=V_X(A) h_X V_X(A)†.

With A_xy→A_xy+λ_x−λ_y this obeys h(A^λ)=G_λ h(A)G_λ†, G_λ=exp(iΣλ_xQ_x). The root factor cancels because h_X commutes with total charge. Integer Q makes the definition periodic. The range increases only to the chosen local tree's diameter. This gauges the whole interacting term, not just a quadratic proxy. In a charge basis it attaches the appropriate integer Wilson powers to EVERY charge transfer.

Define b_Xl=Σ_(x∈X) |incidence(l,path_rx)| q_x. Then exact differentiation of the conjugation gives

 J_l=2Σ_X ||h_X|| b_Xl ≥ ||∂_l h||,
 K_l=4Σ_X ||h_X|| b_Xl² ≥ ||∂²_l h||.

Let J=Σ_l J_l and B=Σ_X||h_X||, including the ground-energy scalar shift. These are explicit finite sums. They are large but finite. No differentiability of the original discontinuous rotor circuit is used: the acquired finite charge representation is essential here.

## 3. Pure gauge fields are not perturbations

Take a finite simply connected cubic box, not a torus with uncontrolled holonomies. Choose a global spanning tree solely for PROOF and the initial-state formula. Every non-tree fundamental loop can be filled by at most S oriented plaquettes. If all principal plaquette curvatures obey |F_p|<ε and Sε<π, tree gauge sets all tree links to zero and every remaining link has a lift of magnitude≤Sε. Thus, modulo an exact matter gauge conjugation,

 ||h(A)-h(0)||≤η=Sε J.

Choose ε≤min(π/(4S),Δ/(8SJ)). Then η≤Δ/8. The isolated ground projector P(A) is well defined, rank one, gauge covariant, and the static gap is≥3Δ/4 throughout this curvature set. Arbitrarily large pure gauge link angles cause no error. Noncontractible Wilson loops on a torus require an extra argument or constraint; they are not covered by small plaquettes alone.

On this open set, a Riesz contour |z|=Δ/2 gives conservative bounds

 ||∂_l P||≤4J_l/Δ,
 ||∂²_l P||≤4K_l/Δ+20J_l²/Δ².

The same bounds hold in arbitrary gauge because the ungauge-fixed h(A) itself has the derivative bounds in §2. No derivative of a discontinuous gauge-fixing map is needed in these estimates.

## 4. Smooth curvature-supported mirror detector

Choose a smooth even scalar cutoff c(u), equal1 for |u|≤1/4, zero for |u|≥1, and at most1/2 for |u|≥1/2. Put χ(A)=Π_p c(F_p/ε). It is a globally smooth gauge-invariant function because its support stays away from the principal-angle seam. Define

 F(A)=χ(A) P(A),

extended by zero outside the admissible open set. This is a smooth positive contraction, gauge covariant, and commutes EXACTLY with h(A). The support cutoff is flat to all orders at its boundary. It is a proof observable, not an added interaction or global Hamiltonian operation.

Let d_l be the number of plaquettes touching link l and c1,c2 bounds on the cutoff derivatives. Define

 u_l=c1 d_l/ε,
 v_l=(c2 d_l+c1²d_l²)/ε²,
 a_l=u_l+4J_l/Δ,
 b_l=v_l+8u_l J_l/Δ+4K_l/Δ+20J_l²/Δ²,
 C1=(Σ_l a_l²)^(1/2),  C2=Σ_l b_l.

Then ||∂_l F||≤a_l and ||∂²_l F||≤b_l. Bounds are deliberately conservative.

## 5. Ordinary Wilson electric AND magnetic quantum dynamics

Use the actual unbounded-link Hamiltonian

 H=(κ_E/2)Σ_l E_l² + κ_B Σ_p(1−cos F_p) + h(A).

For physical lattice units κ_E=g²/a_g and κ_B=1/(g²a_g). All nonkinetic terms are bounded at finite volume. H is self-adjoint on the electric Laplacian domain and preserves Gauss's law. There is no truncation of E, no fixed background, no hard magnetic wall, and no assumption that weak gauge coupling is small in operator norm.

Let ψ0 be normalized, in the electric Sobolev domain, obey Gauss law, and satisfy Fψ0=ψ0. Let E=<ψ0,Hψ0>. Energy conservation and h(A)≥−B imply

 Σ_l ||E_l ψ(t)||²≤2(E+B)/κ_E.

Since the magnetic multiplication and h commute with F, the only commutator is

 [H,F]=−(κ_E/2)Σ_l[(∂²_l F)+2(∂_l F)∂_l].

Duhamel plus Cauchy–Schwarz therefore proves the EXACT bound

 ||(1−F)ψ(t)|| ≤ |t| [ C1 sqrt(2κ_E(E+B)) +(κ_E/2)C2 ] =: e(t).

Domain issues are handled first on the smooth core and then by the conserved quadratic-form bound. In the curvature region, the component orthogonal to the instantaneous ground ray has norm≤e(t). Probability of either mirror excitation (where P is defined) or leaving the entire ε-curvature region is≤e(t)². Probability of reaching |F_p|≥ε/2 for any plaquette is≤4e(t)². These are genuine quantum-link statements, including arbitrarily high electric eigenvalues.

## 6. An explicit gauge-invariant initial state and resource scaling

In tree gauge let a_r be the b1=|links|−|vertices|+1 non-tree angles. Choose a product normalized C∞ bump f_σ(a), each factor supported |a_r|<σ, with ||f'_σ||²=c_b/σ². Take σ≤ε/16 so every plaquette is in χ=1. In this chart,

 Ω(a)=P(a)Ω0/||P(a)Ω0||

is smooth and well defined by the projector perturbation bound. Lift to arbitrary link coordinates by ψ(A)=f_σ(a(A))G_tree(A)Ω(a(A)). Global charge neutrality of Ω0 makes this unambiguous under the residual root gauge transformation. It is precisely Gauss invariant. Haar measure factors into tree gauge-orbit variables and the non-tree variables, so normalization is explicit.

For implementation/energy bounds, enumerate the integer cycle matrix C_rl taking original link angles to a_r and the tree-path generators T_l. All entries of C are0,±1. Let Jbar_l=Σ_r |C_rl|J_r. A conservative explicit kinetic estimate is

 Σ_l||E_l ψ0||²≤3[c_b||C||_F²/σ² +Σ_l(16 Jbar_l/Δ)² +Σ_l||T_l||²],

where ||T_l||≤Σ_(vertices downstream of l)q_x. The numerical16 safely includes normalization derivatives. This large bound is finite and computable, not optimized. Magnetic energy≤8κ_B (#plaquettes)σ²; matter energy is bounded by Jσ in the tree chart. These give an explicit E+B for §5.

Set σ=g s with fixed s and require g s≤ε/16. Then κ_E times the σ^-2 kinetic term and κ_Bσ² are independent of g. The gauge vacuum/wavepacket energy is O(number of modes/a_g), NOT zero as g→0. Keeping this energy in E+B gives e(t)=O(g|t| C1 sqrt((E+B)/a_g))+O(g²|t|C2/a_g). Thus any fixed finite box and finite time admit an explicit nonzero g achieving a chosen leakage error. Photon oscillation frequencies remain O(1/a_g), since κ_Eκ_B=1/a_g²: this is not obtained by freezing gauge dynamics.

The bandwidth remains infinite throughout. The criterion does NOT remain useful at fixed g as volume→∞ with these constants: J,S,C1,C2 and E+B grow. This is a finite-volume test, not the desired uniform chiral-gauge foundation.

## 7. Why the simpler total-energy argument is insufficient

One can dominate bad-curvature configurations by a large magnetic penalty and derive a global excitation bound ~(E+η)/Δ. It fails on the ordinary quantum gauge vacuum: E includes O(V/a_g) zero-point energy, while mirror gap is below matter UV cutoff. Subtracting gauge vacuum energy does not permit retaining the unshifted positivity bound on magnetic energy. The commutator result above avoids that logical error, but still pays volume in a weaker form. It is therefore useful for a finite-time experiment/compiler test, not a substitute for a local thermodynamic decoupling estimate.

## 8. Exact remaining operation

The acquired parent is a uniformly gapped two-massed-face slab. Reopening a desired light face removes the total matter spectral gap and invalidates its rank-one P. One needs a LOCAL mirror excitation penalty/projector family, with a gauge-covariant quasi-local light–mirror splitting and estimates uniform in the tangential volume and slab thickness. The actual remaining quantum-gauge operation is to control the electric commutator of that LOCAL dressed mirror penalty, in terms of LOCAL electric-energy density, while accounting for matter/gauge propagation. The present proof does not supply that family.

If an added light system is tensor-separated and a coupling V_LM has normλ, a direct Duhamel comparison adds |t|λ to the error. This is an explicit finite-system statement but does not earn such a small λ for the actual one-light-face Wilson slab. Bulk mass and large spatial separation alone must be converted into a local, gauged, many-body estimate; merely invoking them would restart the mirror-relocation loophole.

## 9. Strongest relevant ordinary baseline

Lüscher's anomaly-free Abelian overlap construction already gives exact gauge invariance nonperturbatively, including finite-volume topological sectors, under its locality/admissibility framework: https://arxiv.org/abs/hep-lat/9811032 . A finite weak-field gaugeability observation does not surpass that result. The newer Hamiltonian overlap analysis explicitly observes that gauge-field operator dynamics matters and the fermionic axial charge need not commute with the electric Hamiltonian: https://arxiv.org/abs/2305.18934 (PRD108,034511). The derivative issue here is the same type of missing operation, addressed only in the limited criterion above.

The propagator-zero and SMG constraints remain pertinent: https://doi.org/10.1103/PhysRevLett.132.081903 and https://arxiv.org/abs/2505.20436 (latest visible v3,12January2026). A gapped reduced mirror spectrum alone does not establish the correct gauged generating functional. The doubled parent contributes a concrete ungauged interaction/gap and, after finite charge compilation, the real-time quantum-link bound above. It has NOT yet earned fixed-coupling, volume-uniform mirror decoupling, correct target gauge response, continuum limit, or a Standard Model construction. No novelty claim is made.
