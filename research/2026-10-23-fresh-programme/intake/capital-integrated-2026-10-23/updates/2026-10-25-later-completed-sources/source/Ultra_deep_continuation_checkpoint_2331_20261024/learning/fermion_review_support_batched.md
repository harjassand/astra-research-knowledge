# §6 marked-block proof audit

I checked §§1–6 of `fermion/BLOCK_CANONICAL_OBSERVABLES.md`, focusing on the merged support block, inserted filters, same-tilt mass transfer, and the marked outer arc. I found no substantive constant or variance-count counterexample under the stated finite-block, fixed-support, charge-conservation, and recalculated-KP assumptions.

For a union of (r_O) touched blocks, the merge gives (M'=M-r_O+1), size at most (r_Ob), and a coarse degree bounded by recomputation (coarsely (r_OD) at the merged node). Every F edge internal to the union must be put in its exact reference; remaining cross edges use newly checked (D',\Delta',\lambda',h',S'). The distant locations of the support blocks do not by themselves break the algebra: the even operator acts on the finite merged Fock space, and all fermionic permutation signs must remain in the explicit matrix.

The sectorwise filter perturbation checks out. For (A_\pm=I\pm tO), ∥O∥\le1 and (t=2^{-d_*-5}), each sector coefficient changes by at most ((2t+t^2)∥\Omega_q∥^2). Using the native sector bound (3),
\[
 (2t+t^2)2^{d_*}=\frac1{16}+2^{-d_*-10}
 \le \frac{65}{1024}<\frac18.
\]
So the marked reference denominator stays nonzero in the inner sector. More quantitatively,
\[
 |B_{*,\pm}(z)|\ge(7/8)2^{-d_*}B_{*,0}(|z|),\qquad
 B_{*,\pm}(|z|)\le(1+t)^2B_{*,0}(|z|).
\]
The resulting denominator/activity overhead is at most ((1+t)^2(8/7)2^{d_*}<2^{d_*+1}); the stated (2^{d_*+2}) allowance is conservative. The local activity must keep (A_\pm^\dagger A_\pm) after all cross-edge creators. Moving it through creators or treating the filtered vector as a new native BCS reference would not be justified. Since (O) is even and charge conserving, it preserves the marked block's parity/charge selection, so the two-incidence-per-active-block gain survives.

The same-tilt probability transfer is exact:
\[
 c_k^\pm\ge(1-t)^2c_k,\quad Z_\pm(r)\le(1+t)^2Z(r)
 \quad\Longrightarrow\quad
 \Pr_{r,\pm}(K=k)\ge\left(\frac{1-t}{1+t}\right)^2\Pr_r(K=k).
\]
No new marked tilt is needed. The merged node may have lost the native negative-root property, but the outer-arc step does not use its oscillatory decay: its normalized characteristic factor is at most one because its coefficients are nonnegative. The unmarked reference variance is computed at the same (r). From (7) and the factor-two tilt interval, (V_0(r)\ge\nu M/2); removing (r_O) original blocks loses at most (r_Od_{\max}/4). Thus the check (V_u(r)\ge\nu M'/4) follows for sufficiently large (M), and should be verified directly; a sufficient threshold is
\[
 M\ge r_Od_{\max}/\nu-r_O+1.
\]
For the marked outer estimate, the checked conditions give
\[
 -V_u+M'[S'+(D'+1)h'3^{d_*}]
 \le -\nu M'/4+\nu M'/16=-3\nu M'/16,
\]
so (10a) follows with no missing exponent factor. The rational tail (2^{-\lfloor3\nu M'/16\rfloor}) is a valid conservative upper bound. It must be divided by the filtered target-mass lower bound when converted to relative coefficient error.

Finally, (11) follows by bounding the two numerator errors by \(\sigma(c_k^++c_k^-)\), the denominator relative error by \(\sigma\), and using ∣\langle O\rangle_k∣\le1. With (t\le1/32) and \(\sigma=\epsilon t/16), the displayed additive-error bound is below (0.036\epsilon) for (0<\epsilon\le1), hence safely below ε. Since fixed (r_O,b) make (d_*) and (1/t) constants, the required relative precision and the exact-enumeration fallback remain polynomial in (1/\epsilon); if \(\nu) or support size shrinks/grows, that dependence must stay explicit.

One wording point: (I\pm tO) is invertible, but is not generally a contraction in operator norm (∥I\pm tO∥ may be (1+t)). The proof uses its bounded norm and the exact polarization identity, not contractivity. If the term is meant literally, the scaled operator ((I\pm tO)/(1+t)) is contractive, but using it as a physical Kraus filter would add success-probability and implementation costs; no such operation is established here. This is terminology, not a defect in the stated inequalities. The audit remains conditional on the reconstructed block-root theorem and the exact finite-matrix/KP computations in the construction.
