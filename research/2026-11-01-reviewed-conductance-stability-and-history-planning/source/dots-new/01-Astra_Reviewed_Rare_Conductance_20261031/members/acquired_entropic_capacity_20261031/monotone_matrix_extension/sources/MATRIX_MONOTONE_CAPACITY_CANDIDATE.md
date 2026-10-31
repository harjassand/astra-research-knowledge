# Dimension-free conductance from monotone Gaussian precision, without commuting fibers

Status: ROOT candidate, UNREVIEWED. Uses the accepted conditional-transport/Dirichlet capacity sandwich in acquired_entropic_capacity_20261031/PROOF.md. This is a mathematical diffusion statement, not a physical experiment or a historical-priority claim. It does not change the frozen accepted scalar-pencil package.

## Scope

Consider isotropic overdamped reversible diffusion at inverse temperature beta>0 with a normalizable smooth density whose conditional z|y is centered Gaussian of precision beta A(y). Assume y in [-b,b] is the transition slab between full-fiber basins y<=-b and y>=b. In this note the marginal is p(y)=q(y)/Z, q(y)=det(A(y))^(-1/2), with no additional y-dependent energy. The full density/coefficients outside the slab must actually define a conservative reversible diffusion and finite basin mass; these are not inferred from the slab bounds alone.

Suppose A(y) is even, twice differentiable, symmetric positive definite, and on [0,b],

  A'(y) <=0 in Loewner order,
  A'(0)=0,
  lambda_min(A(y)) >= a>0,
  ||A''(y)|| <= L.

These are operator bounds, not entrywise inequalities. Their values must be acquired. They may depend on coefficient conditioning and b, but the conclusion has no explicit fiber-dimension factor. Matrices at different y need NOT commute or have a common eigenbasis.

## Actual Gaussian transport current

Let C(y)=beta^(-1)A(y)^(-1). The symmetric matrix S solving

  SC+CS=C'

defines the conditional continuity current w_y(z)=S(y)z. Its kinetic cost is K(y)=Tr(S C S). In an orthonormal eigenbasis of A at the SINGLE evaluation point, with eigenvalues lambda_i,

  C'_(ij)=-A'_(ij)/(beta lambda_i lambda_j),
  S_(ij)=-A'_(ij)/(lambda_i+lambda_j),
  K=(1/(2 beta)) sum_(i,j) |A'_(ij)|^2/
                              [lambda_i lambda_j(lambda_i+lambda_j)].   (1)

The basis is used in the proof only; it is not an acquired simultaneous diagonalization or a computational oracle.

Put B=-A^(-1/2)A'A^(-1/2). By matrix monotonicity B>=0. Equation (1) implies

  K <=Tr(B^2)/(4 beta a)
    <=||B|| Tr(B)/(4 beta a).

Since A'(0)=0 and ||A''||<=L,

  ||B||<=||A'||/a<=Ly/a.

For W(y)=1/q(y)=sqrt(det A(y)), Jacobi's determinant identity gives

  -W'/W=Tr(B)/2.

Consequently

  K(y) W(y) <= [L y/(2 beta a^2)] (-W'(y)).             (2)

This is the key replacement for commutation of conditional covariance matrices. Without Loewner monotonicity B need not be positive: Tr(B^2) cannot be bounded by ||B||Tr(B), and changing eigenvectors at constant determinant may incur transport cost invisible to the scalar free energy.

## Integrated finite-rate bound

Integrating (2) on [0,b] and retaining the sign of the boundary term,

  integral_0^b K W
    <= [L/(2 beta a^2)] [-b W(b)+integral_0^b W]
    <= [L/(2 beta a^2)] integral_0^b W.

Evenness doubles both sides. Set

  R0=integral_-b^b 1/q,
  R1=integral_-b^b (1+K)/q,
  MA=integral_b^infinity q,
  k_free=1/(beta MA R0).

The conditional-transport capacity sandwich, for the ACTUAL full diffusion, gives

  k_free/[1+L/(2 beta a^2)] <= cap_mu(A,B)/mu(A) <= k_free. (3)

This is not a Markov claim for y_t, a fast-fiber limit, an arbitrary-start hitting-time bound, or a proof that 1/k is every mean passage time. Ordinary Thomson/Dirichlet principles and Gaussian transport are the components. The proposed new scoped consequence is the acquired dimension-independent integrated loss for this monotone matrix class; historical matching remains open.

## Concrete noncommuting polynomial family

Take orthogonal coordinates y=ell.x, z perpendicular ell, and

  v(y)=(1-y^2)^2,
  A(y)=I+v(y) H1+v(y)^2 H2,
  F(y,z)=z^T A(y)z/2,

where H1 is positive definite on the fiber and H2 is positive semidefinite there. No commutation is assumed. At b=1/2, v'<0 on (0,b], hence A'=v'(H1+2vH2)<=0 and A'(0)=0. Also A>=I, so a=1 is always valid; a>=1+(9/16)lambda_min(H1) is a sharper acquired bound.

On [0,1/2], |v''|<=4 and |(v^2)''|<=8. The latter follows from

  (v^2)''=8(1-y^2)^2(7y^2-1),

whose absolute value is at most8 on that interval. Thus

  L=4||H1||+8||H2||

is a sufficient acquired constant. If the matrix norms remain bounded as fiber dimension grows, the loss in (3) remains bounded, while det(A(0)) and the entropic bottleneck can grow exponentially with dimension.

For example, repeating two-dimensional blocks H1=diag(kappa_1,kappa_2), H2=(eta/2)[[1,1],[1,1]], with positive unequal kappas and eta>0, gives [H1,H2]!=0. Its matrices A(v1),A(v2) generically fail to commute, yet determinant evaluation can use actual acquired2x2 blocks and no varying eigenbasis. This is an ordinary block determinant method; no exclusive computational advantage is asserted.

## Acquisition and unfinished obligations

The quadratic homogeneous term again has Hessian P+H1+H2 with unique kernel ell, so the exact rational-projector acquisition from the accepted family is available. Higher homogeneous coefficients can recover H2 and H1, followed by verification of the ENTIRE raw polynomial, PSD/positive fiber conditions and actual physical metric. This paragraph proposes a route, not an executed parser. Arbitrary approximate/noisy coefficients or a supplied coordinate cannot be silently substituted.

Det(A(v)) is a scalar polynomial. An exact determinant backend, certified integration, a global normalizability/nonexplosion proof for the stated polynomial family, all input/task/budget receiving, and strongest prior comparisons remain to be completed before an executable or accepted consequence is claimed. The accepted scalar-pencil program does not already validate this different generator/potential by renaming its input.
