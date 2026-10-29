# Canonical bin lifts and record-dependent coefficient bounds
2026-10-29. Mandatory additive clarification to COARSE_RECORD_INTERTWINING_DRAFT.md. Original preserved.

## Canonical numerical bin center
The phrase 'choosing representatives in [-3,3]' does not alone specify a suitable lift of a cyclic bin. Use this explicit convention. The physical spectrum lies in[-1,1], bin width w<=1, and the actual guard g_guard=nu^2 w/256<w/2. Among real-line lifts of a copied cyclic bin, choose the UNIQUE interval intersecting[-1-g_guard,1+g_guard], if one exists. Two lifts are separated by a gap4-w>=3, while the expanded physical window has length2+2g_guard<3, so there cannot be two. For a bin with no such lift, choose a center in[-2,2]. All selected centers lie in[-3,3]. On the good QPE event, the median estimate belongs to the expanded physical window, and its bin therefore gets the correct lift. Consequently |b-center|<=w/2+g_guard<=w. The bad-event bound |b-center|<=4 remains valid. This convention is computable from the recorded bin and public parameters alone.

## Blockwise coefficient argument
For record-dependent real unit vectors v(r),u(r), one cannot simply pull a pointwise l1 bound through an arbitrary global operator norm. Instead let E_ab=B_ab-g_ab act on the final target/record space, with ||E_ab V||<=zeta for each of the nine ORDERED entries (the symmetric entries are duplicated). On each classical record block r,
 ||sum_ab v_a(r)u_b(r) E_ab (V psi)_r||^2
 <= [sum_ab |v_a(r)u_b(r)|^2] sum_ab ||E_ab (V psi)_r||^2
 =sum_ab ||E_ab (V psi)_r||^2.
Summing records and then the nine entries gives norm squared<=9 zeta^2 ||psi||^2. Thus the stated3zeta bound is valid also with record-dependent eigenvectors. Taking u=v proves the squared-axis case. This argument uses the record block decomposition only; it does not assume the target components are independent of the record.

The later global commutator bound 3sqrt3 kappa/h^3 is a different, pointwise block-operator estimate: the coefficients are fixed scalars within each record block, and the target commutator norm is uniformly bounded. Taking the supremum over record blocks is legitimate there.
