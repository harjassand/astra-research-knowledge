# G is not a positive input-orbit synthesis of Dacorogna-Marcellini energies

Date: 15 October 2026. Internal analytic audit; external correctness review
and historical novelty UNKNOWN.

This result answers whether the new G certificate follows by a positive
combination of known Dacorogna-Marcellini input transforms and polyconvex
terms. It excludes that class even after coefficientwise closure. It does not
exclude signed decompositions, other quasiconvex generators, nonlinear spatial
transformations, or other applications of the underlying exact-form method.

## 1. Precise cone

For `|gamma|<=2/sqrt(3)`, write

    f_gamma(A)=|A|^4-2 gamma |A|^2 det A.

These energies are quasiconvex by
[Bruno and Pasqualotto, Theorem 1](https://arxiv.org/html/2608.06367v1).
Right multiplication by a constant invertible input matrix preserves
quasiconvexity after changing variables. Singular right multiplications have
convex rank-one pullbacks in this particular family.

Let C be the coefficientwise closed cone of homogeneous quartic polynomials
that are finite sums

    H(A)=sum_i c_i f_gamma_i(A S_i)+P(A),
    c_i>=0,    |gamma_i|<=2/sqrt(3),

where S_i are constant real 2x2 matrices and P is an arbitrary homogeneous
polyconvex quartic polynomial. Theorem: `G not in C`.

Thus G is not itself a legal single input transform of one of these energies,
nor obtainable from their positive input-orbit cone plus convex/polyconvex
terms. The result is separate from the pinned positive Fstar-orbit obstruction,
whose strict-acoustic-generator hypothesis does not directly apply to the
endpoint Dacorogna-Marcellini family.

## 2. The special shear acoustic probe

Define the linear coefficient functional

    ell(F)=D^2F(I)[e12,e12].

Rank-one convexity gives ell(F)>=0. For G,

    G(I+t e12)=-1/24+3t^4,    ell(G)=0.                  (2.1)

Write the rows of S as p,q, put
`s=|p|^2+|q|^2`, `r=p.q`, `delta=det S`. Since adding t times the second row to
the first leaves the determinant unchanged,

    ell(f_gamma(. S))=8r^2+4(s-gamma delta)|q|^2.          (2.2)

The determinant bound `|delta|<=s/2` gives

    ell(f_gamma(. S))
      >= 4(1-1/sqrt(3)) |S|^2 |q|^2.                    (2.3)

In particular, for `|S|=1`, this probe vanishes exactly when q=0. Every such
boundary matrix has the form `S=e1 tensor p`; then

    f_gamma(A S)=|A e1|^4 |p|^4,                         (2.4)

a convex function of A, independently of gamma.

This is the necessary special probe estimate. No globally strict acoustic
bound for the Dacorogna-Marcellini endpoint is assumed.

## 3. Uniform bound on orbit mass

Suppose for contradiction H_n in the displayed cone converges coefficientwise
to G. Homogeneity lets every nonzero S_ni be normalized to Frobenius norm one,
absorbing its fourth power into c_ni. Zero S terms may be omitted.

At rank-one matrices E11 and E12,

    f_gamma(E11 S)=|row_1 S|^4,
    f_gamma(E12 S)=|row_2 S|^4.

Their sum is at least 1/2 when |S|=1. Also P_n is nonnegative on every rank-one
matrix: rank-one convexity of `t -> P_n(tR)=t^4 P_n(R)` forces P_n(R)>=0.
Consequently

    sum_i c_ni <=2[H_n(E11)+H_n(E12)].                   (3.1)

The right side stays bounded under coefficient convergence. In fact,
`G(E11)+G(E12)=107/24+3=179/24`.

Since ell(P_n)>=0, equations (2.1)-(2.3) and coefficient convergence give

    sum_i c_ni |row_2 S_ni|^2 ->0.                      (3.2)

All orbit mass therefore concentrates near the compact null set
`Z={S: |S|=1,row_2 S=0}`.

## 4. The incompatible finite lifted-barycenter law

Let nu be the exact measure from Section 5 of `G_QUASICONVEXITY_PROOF.md`:
each of `+36I,-36I` has mass `1/[2(1+36^2)]`, and each of
`+diag(1,-1),-diag(1,-1)` has mass `36^2/[2(1+36^2)]`. Then

    E_nu A=0,    E_nu det A=0,
    E_nu G(A)=-1350/1297<0.                              (4.1)

For each polyconvex P_n, Jensen in the lifted variables yields
`E_nu P_n(A)>=P_n(0)=0`.

The function `J(gamma,S)=E_nu f_gamma(A S)` is continuous on the compact
parameter set `[-2/sqrt(3),2/sqrt(3)] x {|S|=1}`. On Z it is nonnegative by
the convexity in (2.4) and `E_nu A=0`. Thus for every eta>0 there is a uniform
neighborhood U of Z where J>=-eta. Its global negative part is bounded.

The weight outside U tends to zero by (3.2), and the total weight is bounded
by (3.1). Hence

    liminf_n sum_i c_ni J(gamma_ni,S_ni)>=0.

Adding the nonnegative polyconvex expectations and using coefficient
convergence gives `E_nu G(A)>=0`, contradicting (4.1). This proves the theorem.

The law nu is not a compatible gradient law; the new heat theorem proves that
it cannot be used as a negative G quasiconvexity witness. It is used here only
as a separating coefficient functional for this positive synthesis cone.

## 5. Verification scope

`verify_orbit_and_soft.py` independently checks (2.2), the determinant-bound
square identity, the normalized orbit-mass bound identity, the nonpolyconvex
law constants, the complete soft-potential expansion, and the compensated
inequality constant. Compactness and cone separation are analytic arguments
given above, not conclusions of a numerical cone test.

The broader both-left-and-right rotational quartic theorem in the primary
paper is not automatically reduced to the Dacorogna-Marcellini generator cone
defined here. This exclusion should not be presented as ruling out every
positive synthesis from that larger class without a separate classification.
