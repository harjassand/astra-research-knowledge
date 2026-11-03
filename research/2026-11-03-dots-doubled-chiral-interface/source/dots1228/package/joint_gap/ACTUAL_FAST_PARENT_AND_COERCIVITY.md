# Actual-free-bulk canonical parent and product-frame coercivity

2026-11-03. Candidate construction for audit. Uses the now-audited uniformly gapped **two-massed-face** Wilson family (or its gapped half-space limit), and the checked combined-fast Gaussian purification. It retains the original free Hamiltonian; it does not flatten the physical bulk. Strict bounded-range truncation is a separate stability step.

## 1. Physical fast system, representation and normal ordering

At fixed rotors phi, let H_fast(phi) be the ORIGINAL nearest-neighbor Wilson Hamiltonian plus the actual decoration pairing Hamiltonian, in each of two same-chirality copies. Copy2 uses the onsite-identified conjugate fast representation, with the graded phase F=exp(i pi N_2/2) retained. The free vector ±1 flavors are exchanged under the onsite real-structure identification; the free chiral root is not reversed. The scalar self-linking charge S has the SAME sign in the conjugate decoration generator, not the inverse sign. Original physical axial charge includes the fixed particle-hole normal-ordering constant. For the compensated face orientations the static index gives total Q_A=0 on the fast ground, and hence even total fast parity.

See GRADED_PURIFICATION_AND_STABILITY_ENTRY.md and the independently matched 2–4-mode checks. The construction must purify the COMBINED free+decoration fast state, not drop separate parity-dependent phases.

Uniform static input: every fixed-phi fast Hamiltonian has a unique Gaussian ground, excitation gap g>0 and one-quasiparticle energy bound R<infinity, with constants independent of lateral volume. For the two-faced slab the one-body free gap is >=M/3; include the chosen decoration pairing gap in g. All resources in the Wilson/localizer ledger remain paid.

Let E0(phi) be its fast ground energy (both copies). Let W_phi be the explicit canonical Gaussian Bell-to-ground rotation, and W its rotor-controlled direct integral. The phase of W_phi|Bell> is canonical, including grading.

## 2. The parent retains the actual free bulk

With normalized rotor reset projectors P_v=|+><+|_v, define

 H_rot=sum_v(1−P_v),
 H_parent=H_fast(phi)−E0(phi)+W H_rot W^dagger.

Conjugate by W. Since a quadratic Hamiltonian whose Gaussian vacuum is |Bell> has no pairing/linear/scalar terms after subtracting its vacuum energy,

 K_ref(phi)=W_phi^dagger[H_fast(phi)−E0(phi)]W_phi
           =sum_{ij} f_i^dagger A_ij(phi) f_j,
 g N_Bell <= K_ref(phi) <= R N_Bell.

Here f_i are fixed ONSITE Bell quasiparticle annihilators, and N_Bell=sum_i f_i^dagger f_i is phi-independent. The inequality is an operator inequality on the entire Fock space, not only a ground-state statement. H_rot commutes with N_Bell although it need not commute with A(phi).

Thus K_ref+H_rot has a unique ground |+>_rot tensor |Bell>, gap >=min(g,1), in every volume. N=0 is exactly the independent rotor-reset model; N>=1 costs at least g. No adiabatic elimination or extensive-operator-norm perturbation estimate is used. The prepared physical ground is W times that product.

## 3. Axial averaging preserves the SAME excitation grading

The fast Hamiltonian and E0 are already A/V invariant. Twirl only the dressed rotor-reset part:

 H_sym=H_fast−E0+integral_0^{2pi} e^{itQ_A} W H_rot W^dagger e^{-itQ_A} dt/(2pi).

At each phi, Q_ref(phi)=W_phi^dagger Q_A(phi) W_phi is quadratic. The Bell vacuum is its exact eigenstate with eigenvalue0 by the static charge match. Therefore, just as for K_ref,

 Q_ref(phi)=sum_{ij} f_i^dagger q_ij(phi) f_j,

with NO pairing terms and NO scalar. Consequently [Q_ref,N_Bell]=0 for all phi. It acts as identity after exponentiation on the whole N_Bell=0 subspace, for every rotor wavefunction.

In the product frame,

 K_sym=K_ref+K_rot,
 K_rot=integral V_t H_rot V_t^dagger dt/(2pi),
 V_t=W^dagger e^{itQ_A}W.

K_rot>=0, preserves N_Bell and reduces to H_rot at N=0. Hence H_sym has the SAME unique ground and gap >=min(g,1), now with exact axial symmetry. Vector symmetry follows from canonical doubled covariance and the V-covariant W/reference Bell state. The microscopic axial action has bounded-depth controlled local gates, so twirling preserves quasilocality.

This sector proof is stronger than merely observing that all conjugate parents share a ground state. It identifies a fixed product excitation grading useful for stability.

## 4. The ground-energy counterterm is acquired, not an oracle

For a number-conserving free block,

 E0_free(phi)=1/2 Tr[h_phi−|h_phi|].

For general quadratic decoration add its explicit pairing constants. A uniformly gapped bounded finite-range matrix admits exponentially convergent finite-degree polynomial approximants to sign(h), and hence |h|=h sign(h), on the two spectral intervals. The diagonal per-site internal trace of each polynomial is a finite-stencil scalar rotor function. Telescope successive polynomial approximants: coefficient norms decay exponentially, multiplied only by fixed onsite orbital dimension and polynomial stencil-count factors, never the full slab dimension.

Subtract a phi-independent bulk reference energy density. The phi-dependent difference at a site farther than n hops from a rotor-controlled boundary is EXACTLY zero for every degree-n polynomial, by the finite-path expansion. Its remaining tail therefore decays with distance to the interface. This gives an explicit quasilocal scalar rotor interaction for E0(phi)−E0(reference), with summable norm per boundary cell. Uniform absolute error times total volume is NOT the acquisition argument.

The scalar counterterm is A-invariant because it is diagonal in phi, and V-invariant because the mass family transforms by unitary conjugation. Rounding-wall discontinuities are bounded measurable coefficients, not derivative-domain assumptions. Coupling strengths, polynomial accuracy, range and the enormous UV stencil are charged by the prior endpoint ledger.

## 5. Joint rotor–fermion locality of W and Q_ref

Fiberwise spatial decay alone would be insufficient. A constructive JOINT interaction expansion is available: write sign(h_phi) as a uniformly convergent polynomial telescoping series. A degree-n matrix entry depends only on the actual hopping paths and the rotor stencils they meet. It vanishes between sites farther than n hops. A telescoping block has norm O(exp(−mu n)); summing its entries/stencils introduces only polynomial volume factors. Consequently the quadratic controlled generator of W has a finite exponentially weighted interaction norm on the combined lattice of rotors and fermions, uniformly in volume.

The decoration covariance is a finite-range controlled matching matrix. Its contribution is already local. Finite-time evolution of the combined bounded quasilocal generator gives a genuine joint quasilocal automorphism; bounded rotor resets are covered. No derivatives in phi are required. Conjugating the actual bounded-local axial charge density gives a quasilocal number-conserving Q_ref generator. The global axial unitary itself is a bounded-depth controlled matching circuit before conjugation.

## 6. Product-frame coercivity needed for stability

Let B_v=1−P_v and D_v(t)=V_t B_v V_t^dagger−B_v. Because V_t is identity on N_Bell=0 for ALL rotor wavefunctions,

 D_v(t)[|Bell>_fermion tensor arbitrary rotor state]=0.

D_v(t) is self-adjoint and uniformly quasilocal for t in [0,2pi]. Localize it by conditional expectation onto balls using the fermion Bell vacuum and any fixed product rotor reference outside. Each shell still annihilates the fast vacuum on its entire local support, for arbitrary local rotor states. Hence for a shell O_X,

 |<psi|O_X|psi>| <=||O_X|| <psi|(1−P_Bell,X)|psi>
                 <=||O_X|| sum_{i in X}<psi|n_i^Bell|psi>.

Summing weighted tails and centers yields a finite volume-independent C such that

 −C N_Bell <= K_rot−H_rot <= C N_Bell.

Define the FULL product excitation number N_total=N_Bell+H_rot. Positivity of K_rot and g N_Bell<=K_ref now imply

 N_total <=K_rot+(C+1)N_Bell
         <=max(1,(C+1)/g) K_sym,

while the upper inequality gives

 K_sym <=H_rot+(R+C)N_Bell <=max(1,R+C)N_total.

Therefore

 c N_total <=K_sym<=C' N_total,
 c=min(1,g/(C+1))>0, C'=max(1,R+C).

This is a true local-excitation coercivity estimate, not an assumption that a global gap implies such a bound. It is the input for the separate product-frame filtered-spectral-flow stability proof. The original free bulk remains exactly H_fast throughout; only rotor scalar and reset interactions are quasilocal additions near the interface.

## 7. Scope still to audit/finish

The exact parent and its gap are quasilocal. To obtain strictly bounded-range symmetric interactions, apply the separate direct product-frame stability/truncation proof, not a generic theorem that every gapped Hamiltonian is stable. A naive finite-range Yarotsky cutoff argument has a threshold/range circularity already recorded in GRADED_PURIFICATION_AND_STABILITY_ENTRY.md.

For one desired remote chiral surface, first use the uniformly gapped two-interface/half-space construction. Do not use sign(h) for a slab with an untreated gapless far face as if its range were uniform. Half-space attachment and bounded-range truncation must retain the physical far-surface modes and their finite-size/thickness accounting. These are separate from the exact N_Bell sector proof above.
