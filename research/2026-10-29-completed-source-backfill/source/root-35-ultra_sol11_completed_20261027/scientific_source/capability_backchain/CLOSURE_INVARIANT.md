# A robust blocker for the declared closure

This concerns the reset/white/bath/isometric/flagged closure actually proved,
not arbitrary reference channels, nonunitary filters or unflagged sums.
Write T(X)=X-EX. In an HS-orthonormal HERMITIAN traceless qutrit basis Ga,

    T(X)=sum_(a=1)^8 Ga tensor Ba,
    Gamma(X)_(a,b)=Tr(Ba* Bb).

Its eigenvalue square roots are the eight physical traceless operator-
Schmidt singular values. Basis changes conjugate Gamma unitarily. In the
displayed A0 expansion the companion is Ga^T because Ga is Hermitian;
for a general complex basis one uses conjugate(Ga). The invariant is
basis-independent.

For A0=P_Omega tensor C,

    T(A0)=sum_a Ga tensor(Ga^T tensor C),
    Gamma(A0)=||C||F² I8.

Every reset I_A tensor Y leaves T unchanged. For a density direction H,
E is an orthogonal HS projection, hence ||H-EH||F<=||H||F<=1. The norm
of its coefficient flattening is at most one. For a certified quadratic
ray eps<=m ell²/(2^14r²), ||C||F>=m sqrt(r), so

    delta=eps/||C||F<=2^-14,
    (||C||F-eps)² I8<=Gamma(A0+epsH)
                         <=(||C||F+eps)² I8.

Consequently every nonzero ray seed satisfies

    lambda_max Gamma<=c² lambda_min Gamma,
    c=(1+2^-14)/(1-2^-14)=16385/16383.                 (1)

The reset seeds satisfy the stronger equality c1.

White additions leave T unchanged. A bath lift tensors T with U, so Gamma
is multiplied by ||U||F², or becomes zero when U0. Reference isometries
and unitaries preserve reference HS inner products. Physical covariance
rotates the physical basis. A flagged direct sum adds the branch Gram
matrices; sums preserve scalar lower/upper Loewner bounds with the same
ratio c². Positive scalar rescaling also preserves (1).

Thus the whole stated closure satisfies (1), including fixed finite-
dimensional norm limits. This is stronger than an open rank condition:
the inequality lambda_max<=c²lambda_min is closed. A limiting nonzero
Gram cannot lose only some of its eight eigenvalues.

The explicit TP Choi target H_star of POSITIVE_RAY_OPERATION.md has

    T(H_star)=(E01+E10)tensor diag(1,-1,0)/36.

It has one nonzero operator-Schmidt singular value1/18 and seven zeros,
so violates (1). It remains excluded even after adding the new ray seeds
and all those closures/limits. This is not a negative entropy value:
H_star itself is a simple classical-correlated source. It proves the
current architecture cannot reach every positive TP Choi target.

The admitted point P_Omega+eps H_star escapes the OLD square-zero block
invariant, yet retains eight nearly isotropic signal singular values.
This is a package diagnosis, not an unknown anisotropy capability. Root's
exact ordinary comparator rho_cc=(1/3)sum_i|ii><ii| is TP, has physical
signal rank2 and Delta=2log2-log3=log(4/3)>0. Adding this established
classical positive seed immediately breaks the invariant. The argument
therefore does not bound an equally informed all-known-positive-seed method.
Arbitrary reference CPTP processing is not a proved Delta-preserving
closure here and likewise cannot be silently granted.

The argument is an analytic representation boundary at the stated
operations, not a global impossibility theorem for WH3 contraction or
for physical noise engineering. Root whole-read and accepted it at this
declared package scope, with the ordinary comparator correction retained.
