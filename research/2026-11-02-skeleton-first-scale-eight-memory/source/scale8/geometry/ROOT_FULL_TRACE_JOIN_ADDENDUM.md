# Root join: removable full traces for the packet decoder

2026-11-02. Addendum to the small-scale whole-construction candidate. It binds the newly reviewed abstract full-trace extension to the specified decoder design; the actual-family binding is included in the whole-family audit.

## Trace definition
At level i record every nonempty active component's complete input packet blocks, its chosen A/B flag, actual correction coordinates c_i, coarse syndrome outputs, and the bounded potential stencils of BOTH branch maps. Include all operands of the linear rows

 sigma_i + J_i sigma_(i+1) + d_i c_i = 0

whenever that row has a nonzero operand. These rows are already within a fixed enlargement of the input-seeded map stencils. Include the local residual rows used to make component restriction safe. Zero halo vertices do NOT trigger further row/gate activation. A zero coarse output does not fire the next level. Potential output/correction collisions are included in the input component graph before choosing sheets.

At the fixed finite base, one bag contains all terminal syndrome and correction coordinates whenever the base input is nonzero. The base decoder corrects every valid base syndrome and outputs zero on zero. This is a fixed-size contribution, not a volume-sized central gate.

All fixed row, map and packet-block degrees are bounded. Complete active component shapes/corrections are paid by their packet charge. Counting does not store an unbounded-fanout central decision gate: a component's chosen flag can be copied along its bounded-degree shape with O(component size) finite labels. Verifying the minimum choice is a finite computation on that whole component; it is not claimed to be a constant-time local hardware operation.

## Restriction before validity
Select an entire connected component of the resulting original trace. Each residual row retains all its nonzero operands or none; every decoder component and packet block it meets is retained whole. Hence every stage correction identity remains true for the restricted recorded values, BEFORE claiming that the restricted top syndrome is valid. The terminal restricted input is either the complete original valid terminal syndrome or zero. Telescoping the lifted correction identities therefore proves

 tau = d_top f_trace.

Thus tau is a valid coboundary supported on the original occupied syndrome. No new physical check generators are introduced. Only after this algebraic proof is it meaningful to rerun the decoder on tau. Union-of-input-seeded stencils, whole component decisions, complete owner blocks and zero preservation show that removing other trace components does not alter the retained record.

For Gibbs-ratio probability bounds, validity plus injective translation by a FIXED tau is sufficient; rerun deletion stability is stronger and need not be silently used to claim the removal image has the same instability witness.

## Two-run root witness
Compare full traces for sigma and sigma+d e, joining matching active sites INCLUDING physical occupied base leaves and prepass gate ports, and the bounded local fault connector. Take the complete connected union component containing the fault. Every selected original trace component is retained whole; its top union tau is therefore valid and tau subset sigma. Shared occupied base sites force the selected perturbed top set tau' to differ from tau only on fault checks. Both trace masses are O(|tau|+k_fault), with bounded-degree connected shape entropy exponential in |tau|.

If this union reaches an OCCUPIED level h, ancestry contraction requires at least 2^h units up to fixed constants. A mere ghost output at level h only proves occupied height h-1; that one-layer shift is explicitly harmless. If the union has lower occupied height, higher corrections cancel between runs and the remaining physical correction difference has support at most C(|tau|+k_fault) sum_(i<h)(K_lift/2)^i. Logical distance gives the complementary lower bound. This is the independently reviewed FULL_TRACE_REMOVABLE_EXTENSION.md mechanism, not an assumption that a globally chosen component branch has bounded radius.

Consequently the fixed-witness probability can use

 W(sigma)/W(sigma+tau)<=exp[-B|tau|+o(1)]

for ANY admitted positive syndrome weights with the valid-removal ratio. Pure product-Gibbs Walsh positivity is no longer the only probability route. The resulting entropy bound is the same charged-contour bound with adjusted constants.

## Physical opposite-sector trace
Prepend the bounded local duality computation u=F^2 sigma and the H^2 sigma correction stencil. Retain cancelling F gates whenever a nonzero physical input enters; do not recursively activate zero nodes. Restricting whole augmented trace components gives u_C=F^2 tau. The complete dual residual/terminal certificate gives d_B r_C=u_C. Top-degree homotopy I+GF=d_AH then gives

 d_A(G^1 r_C+H^2 tau)=tau.

Thus the physical opposite-sector witness is valid as well. G is applied algebraically to selected already-lifted corrections; its expanded finest-level support is NOT inserted into the entropy trace. Its fixed column norm only enters the physical support bound. The fixed F/H prepass costs a constant factor in physical leaf mass and footprint. See local_duality_transfer_20261102/REMOVABLE_TRACE_EXTENSION.md and its independent review.

## What this would unlock
Once the actual family atlas/maps and whole join are admitted, both error sectors have removable witnesses with bounded entropy. Along with the polynomial distance/filling theorem, this supplies the specific static interface used by the earlier full-temperature native-clock and generic-perturbation constructions. A mere unperturbed rare-event bound would not have supplied this interface; the distinction is material.

The target code's actual maximum check weight must still set the fixed clock dimension. All ideal-equilibrium and physical-access limitations of the earlier native theorem remain. This addendum does not manufacture noisy WRITE or certify a practical numerical operating point.
