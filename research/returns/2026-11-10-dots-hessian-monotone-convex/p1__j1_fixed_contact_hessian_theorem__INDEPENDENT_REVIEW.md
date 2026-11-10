# Independent review of the arbitrary-Hessian contact theorem

Reviewed mathematical source SHA256: f58e034d881f8308f026f7df2156be5f96e4cb0c8725fd3952f7ac20e838b8b4. THEOREM_AND_PROOF.md retains Sections 1–5 of that source verbatim; its introduction and final provenance section are edited for standalone delivery.

This is a narrow mathematical review, not a review of the unresolved full J_r problem. It does not enlarge the theorem's quantifiers.

## Disposition

The theorem in the reviewed proof is supported at its stated scope. I found no missing compatibility, mean, amplitude, heat-integrability, or Sobolev-extension obligation. In addition to reading its complete proof, I independently reconstructed the contact expansion and obtained a different explicit pointwise payment for the same all-frequency heat operator. The latter is given below and does not rely on the author's 3x3 Gram matrix.

Precisely, at r=k=1 and A=[[0,1],[1,0]], every real periodic scalar psi in W^{2,4} satisfies the original Jensen inequality under X=diag(2,-4)D^2 psi, at every real amplitude. The gap is strictly positive for a nonzero amplitude and nonzero Hessian. The periodic-to-compact-support consequence and the W^{2,4} closure stated in the source are valid.

This does NOT prove unrestricted vector-gradient quasiconvexity, arbitrary affine means, or every r>0. A compact-support scalar Hessian potential is not an arbitrary zero-boundary vector perturbation.

## Independent reconstruction of the mechanism

For U=psi_xx, V=psi_xy, W=psi_yy, I obtain directly

    gap=16t^2<W^2>-8t^3<V^3+4VW^2>+t^4<J_1(X)>.

The contact quadratic has the integrated form (2b+c)^2+d^2. The determinant translation used to obtain it is legitimate because det D phi has zero integral for the actual periodic compatible field. Here 2b+c=0 and d=-4W.

For R=-6 integral partial_y P_s[V_s partial_y U_s] ds, periodic Hessian compatibility U_y=V_x and W_x=V_y gives

    <V^3>=<W R>.

The terminal cubic is zero because the y-average of psi_xy is zero at each x. No vanishing y-average of U is needed. The vertical heat estimate is bounded on L4 times L4 into L2; smooth approximation therefore passes this exact compatibility identity to W^{2,4}. A rectangular torus causes no change to the constants.

The resulting full gap is

    t^2||4W-t(R+4VW)||_2^2
      +t^4[<J_1(X)>-||R+4VW||_2^2].

Thus the only substantive global budget is the one paid in the source, not a collection of independent triad checks.

## Alternative all-frequency budget

Use the author's elementary heat estimate with lambda=1/3, rather than 2/5:

    ||R||_2^2 <= <U^4/2+9U^2V^2+81V^4/2>.

The elementary inequality (r+s)^2<=2r^2+2s^2 gives

    ||R+4VW||_2^2
      <=<U^4+18U^2V^2+81V^4+32V^2W^2>.

Subtract this from the independently expanded original density. The remainder is

    A(U,W)+B(U,W)V^2+113V^4,
    A=U^2(U-8W)^2+16W^2(3U^2+4UW+2W^2),
    B=18U^2-240UW-16W^2.

A is strictly positive unless U=W=0. When B>=0, positivity is immediate. When B<0, complete the square in V^2. The discriminant reserve is

    452A-B^2=128[U^4+11U^3W-50U^2W^2+166UW^3+111W^4].

If UW>=0 and U!=0, put s=W/U>=0. The bracket divided by U^4 is

    1+s(166s^2-50s+11)+111s^4>0,

because 166s^2-50s+11 has negative discriminant. If UW<0, put s=|W/U|. The condition B<0 implies s>15. On all s>=2 the relevant polynomial has the explicit positive expansion

    111s^4-166s^3-50s^2-11s+1
      =111(s-2)^4+722(s-2)^3+1618(s-2)^2+1349(s-2)+227.

The U=0 case is immediate. This proves a strict quartic reserve by a second set of exact constants and establishes the same all-frequency budget independently of the source Gram factorization.

I also read the source's original Gram argument. Its Schur bounds have the correct directions: a0 in (52,53) gives S11>5600, S22>16600 and 0<S12<8700, hence a positive determinant. Its stricter pointwise remainder, exact contact factors, and final square completion are consistent with the independent reconstruction.

## Prior comparison and novelty limits

I read the primary statement of Guerra, arXiv:2608.23388v1, especially Theorem 1.1, Corollary 1.3 and Theorem 3.3: https://arxiv.org/html/2608.23388v1 . Those results concern the specified Burkholder/separating integrands under scalar Hessian perturbations, allowing general affine matrices. They are highly relevant prior, but their hypotheses are not automatically a theorem for the different integrand H -> J_1(A+diag(2,-4)H). Neither the source nor this review provides a positive domination/representation deriving the present statement from them.

Corollary 1.4's p>2 condition concerns a real output under the stated Beurling convention, not an unqualified improved upper bound for real inputs. The present proof does not need that estimate. Its heat-energy bound is elementary and standard in nature; the density-specific contribution is its simultaneous payment by the original quartic reserve and the resulting infinite-dimensional contact theorem.

No exhaustive literature novelty determination has been made. The result should be called an independently checked, author-derived restricted theorem, not a newly established historical result without qualification.

