# Exact native committed-chain CP credit
2026-10-30. New construction candidate. It removes finite computation-clock startup, but not acquisition/cleanup service. Generic native continuous robustness remains open.

## 1. Setting and intended result
Use the reset-first, forest-gauged native transactional apparatus and the actual history flags B_h of `NATIVE_NONMONOMIAL_RESET_ENVELOPE.md`. Let D_h denote the actual projector onto

    clock in C_0,...,C_L; all R_h locks carry o_h; workspace W_h=0.

On this subspace the native C chain is scalar on DATA; its complete terminal reset applies the intended idempotent deterministic-syndrome CPTP map Phi_h and moves to Q0. Its only entrance from A is the complete one-way commitment reset. Ownership is invariant until terminal/abort reset. When D_h holds there is no abort edge.

**Payload qualification.** This credit requires Phi_h^2=Phi_h. If the existing native payload table chooses merely the first improving move, replace it by the finite local orbit-minimizer rule: identity on every locally minimal syndrome (including ties), and a fixed Pauli to a selected orbit minimum otherwise. The accepted SSF progress interface must be rechecked for that rule; its finite Stinespring circuit must be synthesized in actual hub/resource gates, and C-chain length and witness constants recomputed. The architecture admits a finite payload but this note does not claim the original gate list was already idempotent. The raw nonmonomial reset envelope itself did not require idempotence.

The construction below gives commuting bounded-support unital CP maps T_h, identity outside D_h in the appropriate Kraus sense, such that with T_C=product_h T_h,

    L_native^* T_C(V)
      <= -beta sum_h T_{C\h}(D_h d_h)
         - sum_b kappa_b T_{C\owner(b)}(Q_b)
         - other positive terms,
    d_h=(I-Phi_h^*)V>=0.

Here Q_b are the genuine bad-reset charges from the spectral-envelope lemma. In particular,

    L_native^* T_C(V) <= -beta T_C(sum_h D_h d_h)
                         - transformed bad-reset charges.

This is exact continuous generator drift, not an effective replacement of the C chain by a Poisson channel. All constants and circuit supports are independent of N. Choose worst-case beta across the finitely bounded local circuit types.

## 2. Finite-dimensional committed-clock survival witness
Restrict the actual controller dynamics to good committed C phases, including h's actual finite reset monitor. Delete the h-terminal gain, retaining its loss A_h=kappa_T |C_L><C_L| tensor I_monitor. Call the resulting local scalar killed adjoint K_C,h^*. Every other owner preserves these tags and cannot act any h payload while h is committed. Resource monitors act on fixed lock labels and can be omitted as spectators. The h monitor remains part of this finite matrix generator.

The finite forward-chain/reset path (or the accepted C-only actual-reset tail) gives exponential survival decay. Thus the finite-dimensional positive integral

    R_h=int_0^infinity exp(t K_C,h^*) I dt

exists, is strictly positive, and obeys K_C,h^*R_h=-I. There are fixed bounds 0<r_min I<=R_h<=r_max I. No global environment reconstruction is used: this is the actual isolated committed clock and its on-site monitor.

Choose Rmax>||R_h||, for example Rmax=2 max_h||R_h||, and 0<beta<1/Rmax. Put

    s0=1-beta Rmax>0,
    S_h=s0 I+beta R_h.

Then s_min I<=S_h<=s_max I<I and

    K_C,h^*S_h=-s0 A_h-beta I.

All coefficients are actual finite matrices and can be solved exactly/numerically after the native gate list is fixed.

## 3. CP channel, including coherences with uncommitted sectors
Extend S_h as I outside D_h. More explicitly define Kraus operators

    A_h=(I-D_h)+sqrt(S_h)D_h,
    B_h,s=sqrt(I-S_h)D_h K_h,s,

where K_h,s are DATA Kraus operators of Phi_h, commuting with all controller coordinates. In Heisenberg form

    T_h(O)=A_h^dagger O A_h+sum_s B_h,s^dagger O B_h,s.

The Kraus completeness identity is exact. This is NOT a projection/pinching onto C: cross-C/non-C coherences are retained by A_h. On DATA/flag-diagonal V,

    T_h(V)=V-D_h(I-S_h)d_h.

It preserves every actual flag block. Because d_h>=0 and S_h<=I, T_h(V)<=V; likewise T_h(W)<=W using the raw monotonicity of Phi_h for W.

## 4. Exterior commutation is exact ownership algebra
For g!=h, every nominal controller transition/reset of g preserves every projector onto lock label o_h and leaves h's clock/workspace/monitor untouched. Thus it commutes with D_h and the h-clock coefficients in A_h and B_h,s.

When D_h=1, h owns the ENTIRE declared DATA/read footprint of K_h,s. Every payload Hamiltonian or forest-reset unitary of g acts only on resources actually owned by g, hence is disjoint from this footprint. On D_h=0 the B_h,s branch vanishes. Therefore every Kraus B_h,s and A_h commutes with every exterior nominal Hamiltonian or reset Kraus operator (or its adjoint). This includes malformed g masks: the forest gauge guarantees that even their partial payload circuits use only g-owned resources. Lock cleanup z_g->free, acquisition free<->o_g, and resource label monitors also preserve the o_h projector.

Consequently T_h commutes with every exterior adjoint generator term. This is stronger than a clean-sector approximation.

For overlapping h,g, D_h D_g=0 because both would require the same lock to have distinct owner labels. For nonoverlapping h,g their nonidentity DATA actions are disjoint. The coefficients are controller-diagonal in locks and do not change ownership. It follows directly that every pair of T_h Kraus families commutes, hence the T_h commute as maps. Their product is a bounded-depth local unital CP circuit, obtained by coloring the bounded overlap graph.

The distinction between OWNED resources and the full possible partial-circuit footprint is essential. This argument would fail for unguarded gates or for a model permitting release/reacquisition during an unfinished C episode.

## 5. Own-generator calculation
On the good C subspace,

    T_h(V)=Phi_h^*V+S_h d_h.

Idempotence gives Phi_h^*d_h=0. The actual terminal gain exits C into a sector where T_h is identity; it applies Phi_h, cancelling the killed loss acting on Phi_h^*V. All remaining C-clock evolution is scalar on DATA. Therefore exactly

    L_h^* T_h(V)|_{D_h}
      =(K_C,h^*S_h)d_h
      =-beta D_h d_h-s0 A_h D_h d_h.

At commitment A_k->C0, the source has T_h(V)=V and the target has the above credit. On a GOOD complete-lock source the added decrement is

    kappa_commit (I-S_h[C0,C0]) d_h >=
    kappa_commit (1-s_max) d_h,

as an operator on the retained monitor. On an incomplete-lock source T_h stays identity. For a dirty-workspace complete-lock source, the credit decrement is the reset-pullback of d_h with h's flag CLEARED, not the source d_h with its tokens occupied. It is still nonnegative. Such a source additionally loses its actual flag; complete workspace overwrite makes the source effect workspace diagonal, so the flag-removal decrement is retained, not hidden.

All other own A/Q and inconsistent/abort Hamiltonian transitions have D_h=0 at both ends, hence the credit is identity there. Clean H preserves all raw syndrome/flag observables. Nonpayload resets are raw monotone. On bad terminal/abort sources the credit is identity and the exact spectral-envelope loss Q_b applies. For complete-lock terminal sources, the raw reset adjoint has zero good/dirty workspace cross block by the deterministic-syndrome Stinespring argument. The loss and Hamiltonian pieces preserve those blocks, so no unbounded cross term has been discarded.

Thus the stated own-generator bound holds on the ENTIRE physical Hilbert space, including coherent superpositions of good and dirty sectors.

## 6. Global composition and positivity
Let T_{C\h}=product_{g!=h}T_g. Exterior commutation gives

    L_native^* T_C(V)=sum_h T_{C\h} L_h^* T_h(V)

with any shared resource-only terms assigned separately; those commute with all credits and have raw nonpositive drift. Applying the positive maps T_{C\h} to the own bounds proves the result in section 1. There is no extensive pairwise remainder.

Since Phi_h^*d_h=0,

    T_h(D_h d_h)=D_h S_h d_h<=D_h d_h.

Positivity of the other commuting T_g therefore gives the weaker but convenient bound by -beta T_C(sum_h D_h d_h). The same construction can be applied to W, with d_h^W=(I-Phi_h^*)W>=0.

## 7. Barrier/noise interface and remaining gap
T_C is a finite-depth local CP dressing. Existing local Stinespring transfer bounds therefore apply to arbitrary local Hamiltonian/Lindblad/common-bath perturbations after the finite forest-frame enlargement. The no-jump branch A_h commutes with each raw f_A and is bounded below by sqrt(s_min) I. Only O(|A|) local credits affect f_A, so

    T_C(f_A)>=exp[-C|log s_min| |A|] f_A.

Choosing beta small permits the usual fixed exponent margin for raw basin comparison. These statements do not give a native threshold by themselves.

The earned negative term serves every committed C phase uniformly and provides a strictly beneficial commitment jump. It does NOT yet serve active DATA hubs stalled in A/Q or blocked by other owners, nor arbitrary non-endpoint dirty flags. Acquisition/cleanup requires a further phase-aware multiplicative service construction. One cannot replace that missing inequality by the actual-reset tail, nor by fixed-horizon global averaging.

**Audit status:** new proof candidate, requiring independent review of exterior Kraus commutation, the exact killed C restriction, and full source-block decomposition. No native continuous-noise theorem is claimed.
