# Exact local-noise lemma for bounded-depth CP animal dressing
Root proposal independently checked 2026-10-29. This lemma does NOT establish clean finite-clock drift.

Let f_A be the original positive syndrome-diagonal animal observable, and suppose its established local-orbit estimate applies to every bounded-support Hermiticity-preserving, identity-annihilating Heisenberg map M_X (including arbitrary spectator bath):
-C_X ||M_X||_cb (f_A tensor I)<=M_X(f_A tensor I)<=C_X ||M_X||_cb (f_A tensor I),
with zero action when X misses the checks/data influencing A. Constants depend on support radius/size but not A or volume.

Let T be a finite-depth circuit of bounded-support unital completely positive Heisenberg maps. Layer supports are disjoint; depth, support size, and local Stinespring dimensions are fixed independently of volume. Introduce fresh product-state environments for every circuit channel and implement each local channel by a local UNITARY dilation. Their composition is a local unitary circuit U of the same bounded depth (up to a fixed factor). With E the product-environment compression,
T(O)=E[U^dagger(O tensor I_E)U].

For a physical local HP identity-annihilating map N_Z^*, define on physical+environment systems
M_Z=Ad_U composed with (N_Z^* tensor id_E) composed with Ad_{U^dagger},
where Ad_U(O)=U O U^dagger.
Direct algebra gives the EXACT identity
N_Z^* T(O)=E[U^dagger M_Z(O tensor I_E)U].
N acts through E because E touches only the fresh environments. This checks the conjugation orientation.

M_Z is HP, annihilates identity, and has unchanged completely bounded norm. Its support is contained in the bounded-depth causal cone of Z under U. This remains true with a shared external bath: retain the bath inside the local map's spectator system while counting only its bounded physical support. Locality here refers to physical sites, not the bath's Hilbert-space dimension.

Apply the original orbit inequality to M_Z and f_A tensor I_E. Unitary conjugation and E are positive, hence preserve order:
-C ||N_Z^*||_cb T(f_A)<=N_Z^* T(f_A)<=C ||N_Z^*||_cb T(f_A).
If the expanded causal cone misses A's relevant data support, M_Z(f_A tensor I_E)=0 exactly, so the term vanishes.

For a bounded-incidence local perturbation N^*=sum_Z N_Z^*, only C'|A| expanded cones meet A. Therefore
N^* T(V)<=epsilon C'' T(W),
V=sum_A f_A, W=sum_A |A| f_A,
when each local strength is at most epsilon in the chosen local norm. The analogous lower bound also holds.

No inverse of T, global condition number, CP lower bound T>=c Id, or pairwise expansion of the dressed observable is used. In particular, T need not be invertible. Thus any clean drift L_0^*T(V)<=-c T(W)+CN is robust to sufficiently weak perturbations of the stated local class.

Caveats: the original local-orbit bound must apply to HP identity-annihilating maps after unitary dilation (not only to diagonal Pauli noise); use a completely bounded norm or a generator-form estimate stable under adjoining environments. A merely positive, non-CP dressing or an unbounded-depth/quasi-local circuit does not satisfy the lemma as stated. If the physical clean generator and T are defined only on an invariant code subspace, this lemma alone does not extend their drift inequality to dirty sectors.
