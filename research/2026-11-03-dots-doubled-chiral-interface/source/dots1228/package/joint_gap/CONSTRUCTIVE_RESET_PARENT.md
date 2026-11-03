# A collective conditional-reset parent, and the unclosed free-slab bridge

2026-11-03. Status: **a completed thermodynamic construction for a shared-rotor conjugate-fiber completion; not the requested free–commuting-projector interface.** No claim that matching anomaly implies an embedding, locality, or gap. Primary text personally read: Thorngren–Preskill–Fidkowski, https://arxiv.org/html/2601.04304v2, §3.3, §4.1, Appendix E. Their specific unknown is still §4.1's interacting free/CP interface. This note addresses collective reset mechanisms, not only a reconnection anticrossing.

## 1. Microscopic input actually used

On the bounded-valence simplicial lattice, §3.3 places one complex fermion per face and controls a perfect matching p_phi of its Majoranas by nearby rotor vorticities. Pair choices, including the four-face resolution convention, are local functions of the rotor configuration. The axial generator is a local scalar self-linking density summed over the lattice plus K(phi), a quadratic matching operator. The rounding dependence is measurable and discontinuous; below we use bounded rotor resets rather than differentiating it.

In a finite volume write K(phi)=C+(i/4) gamma^T A(phi) gamma. A(phi) is real skew and has local disjoint matching blocks, up to normalization/sign convention. The original axial generator includes the scalar S(phi). This scalar cannot be removed by a finite-fiber charge-shifting unitary. It is cancelled explicitly in the model constructed below, not ignored.

## 2. Actual positive model

Use one shared set of rotors phi and two conjugate fermionic fibers. Their compensated symmetry is

Q(phi)=[S(phi)+K(phi)] tensor 1 - 1 tensor [S(phi)+K(phi)]^T.

The scalar and constant C cancel. Transposition is the local dual representation, not an assertion about the real free slab. With an appropriate local Majorana sign convention for the second copy, represent its Majoranas by b_j and those of the first by a_j, all anticommuting. Set c_j=(a_j+i b_j)/2. Then

Q(phi)=(i/4)[a^T A(phi)a+b^T A(phi)b]=i c^dagger A(phi)c,
N=sum_j c_j^dagger c_j.

Thus [Q(phi),N]=0 for every phi, and Q(phi)|vac_c>=0. The c vacuum is a product of cross-copy Majorana dimers at the same spatial positions. It is unique and independent of phi. This is the key positive algebraic operation: coherent cancellation is earned at the operator level, not inferred from anomaly coefficients or phase choices between changing ground-state fibers.

The construction requires a shared phi, not two independent rotor layers identified by a nonnormalizable delta function. It is therefore a conjugate-fiber comparator. Calling it an interface of the original two independent layers would overstate what was built.

## 3. Bounded local symmetric parent

Normalize Haar measure on each rotor circle. Let P_v=|+><+|_v, where the constant wavefunction |+> has unit norm, and B_v=1-P_v. Set U(t)=exp(itQ), with the axial period determined by the normalized matching generator (2pi in the integer-charge convention). Define

Bbar_v = integral_0^{2pi} U(t) B_v U(t)^dagger dt/(2pi),
H = Delta N + g sum_v Bbar_v,   Delta,g>0.

This is an explicit positive Hamiltonian. Each reset is noninvertible; no full-fiber unitary charge transporter has been introduced.

**Earned locality.** For every possible resolved-dual edge e, write its bilinear gate multiplied by the local indicator that e belongs to p_phi. These controlled generators commute pointwise: simultaneously selected edges are disjoint; overlapping alternatives have disjoint rotor support in configuration space. The scalar parts have cancelled. Bounded lattice valence permits a bounded coloring of their supports. Consequently U(t) is a finite-depth product of bounded-range controlled quadratic gates, uniformly in t and volume. In U(t) B_v U(t)^dagger all gates outside the bounded control neighborhood of v cancel. Therefore Bbar_v is bounded-range with norm at most 1. Its coefficients depend only on that neighborhood's rotors, not on an entire endpoint ground state.

No smoothness or unbounded-operator-domain claim is used: B_v and its conjugates are bounded operators on L²(S¹) rotor factors. Finite-volume H is self-adjoint and bounded below, with uniformly bounded local terms. Its norm is extensive, as usual.

**Symmetries.** Haar averaging gives [H,Q]=0. The global vector shift leaves local vortex matching invariant. P_v commutes with global rotor translation, and N is rotor-independent, so H also preserves U(1)V. Fermion terms are even. The doubled dual representation has the expected compensated parity action, subject to the fixed graded-tensor convention.

## 4. Complete thermodynamic gap and uniqueness proof

All terms commute with N, so decompose into its eigenspaces.

- In N=0, the fermionic fiber is one-dimensional and U(t)=1. H reduces exactly to g sum_v(1-P_v). Its unique ground is the product of constant rotor wavefunctions; its first excitation costs g.
- In N>=1, positivity of every Bbar_v gives H>=Delta N>=Delta.

Thus every finite volume, with any spatial topology and any number of local rotors, has a unique ground

|Psi_0> = tensor_v |+>_v tensor |vac_c>,

and spectral gap at least min(Delta,g). The argument is volume-independent and proves the thermodynamic gap in this model; it is not extrapolated from a finite patch. The ground is topologically trivial: cross-copy dimers are bounded-support Bell-like pairs, removable by local gates if symmetries are ignored. No local reconnection phase or loop-flatness premise occurs. The protected common vacuum supplies compatibility for arbitrary overlapping matching changes.

A finite 64-dimensional test in `check_reset_parent.py` uses two discrete reset variables controlling four incompatible signed matchings of four c modes. Exact spectral twirling gives gap 1 for Delta=2,g=1, unique ground, symmetry commutator 6.55e-15 and vacuum residual 0. This checks conventions; the analytic proof supplies thermodynamic scope. The discrete control test is NOT a rotor truncation theorem.

## 5. Attempted actual free-slab transfer

The actual free slab's axial action is onsite and its occupied projector P_phi varies with the rotor-generated boundary masses. It is NOT the dual K(phi)^T action above. Identifying them would exactly assume the missing interface, and full-fiber charge transport can already fail by finite-dimensional trace arguments when self-linking changes.

A concrete attempt was a fixed-color coherent sweep. Start at reference rotors, set one bounded-color class at a time to their target values, and use endpoint resolvents/local polar or partial maps to transport fermion states. Define all phases by this fixed circuit, avoiding an assertion that arbitrary loops are flat. Root's resolvent route can in principle make endpoint differences exponentially localized if the actual interface endpoints have a uniform spectral gap; it does not itself establish that gap.

Two missing operations prevent promotion:

1. A color step changes an extensive set of sites. Independent patch maps reproduce it only after uniform common-exterior coefficient/error estimates, not merely pointwise exterior fidelity. A local fermion-support optimum can still depend on far rotor variables. Summing an extensive error in norm is not acceptable; a local-interaction stability estimate would be needed from actual coefficients.
2. Fixing reference rotors generally breaks vector-shift covariance of the constructed section. Averaging the resulting parent over U(1)V is not automatically a small perturbation, even if each fiber approximates the free-slab ground. The off-diagonal rotor kernels remember the phase connection. An O(1) symmetry averaging change can close a gap or change ground structure. A global reference rotor is nonlocal; adding independent reference rotors merely transfers the same interface problem to them.

The common-N-vacuum proof cannot be copied by replacing N with a rotor-dependent spectral excitation number N_phi: the ordinary rotor reset does not preserve its vacuum sector, and the averaged reset need not reduce to a tensorized scalar heat bath. Compressing by a global P_phi ground projector violates the requested locality/oracle gate. A Lindblad reset to the mixed state is not a coherent Hamiltonian parent for the desired unique pure ground.

## 6. Comparison and stopping conclusion

This is an exact positive reset/gap construction, not only a list of hoped-for premises. Its special resource is a supplied local conjugate representation sharing the original rotor configuration. Ordinary CP/inverse-CP stacking and symmetry-disentangler methods already exploit cancellation, so no broad novelty or advantage over mirror SMG is claimed. It does not acquire the free-fermion-to-conjugate-decoration conversion. The free-slab task remains at the genuinely interacting mirror/interface problem; the present construction gives a sharp algebraic target (a locally earned common excitation vacuum) but does not furnish it.

The completed useful result is the bounded local parent and its all-volume gap proof, plus the explicit failed coherent color-sweep transfer. The requested free–CP joint gap/unique-ground-state proof remains **unestablished**. No denied tool action or external permission blocker occurred; this is a mathematical construction gap, not an access failure.
