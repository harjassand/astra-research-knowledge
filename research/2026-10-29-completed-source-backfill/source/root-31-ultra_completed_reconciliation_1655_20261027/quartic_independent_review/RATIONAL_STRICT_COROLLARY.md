# Strict support gives an eventual positive-definite rational Gram

This strengthens the implementation interface of the scoped
HIERARCHY_PROOF.md. It uses the same established Scherer–Hol matrix
positivity machinery. No degree bound, coefficient-height bound, practical
solver complexity, or negative-instance stopping rule is asserted.

## Proposition

Let H be a homogeneous quartic with rational coefficients. Suppose some
real homogeneous quadratic kappa and a,b>0 satisfy globally

    P(A,X)=B_H(A,X)-kappa(A)detX
            >=a|A|²|X|²+b|X|⁴.

Then for some finite r there are a rational homogeneous quadratic
kappa_hat and a rational symmetric matrix R that is **positive definite**,
on all features

    Z_r=(A_i X^alpha, |alpha|=r+1;
         X^beta, |beta|=r+2),

such that

    |X|^(2r)[B_H(A,X)-kappa_hat(A)detX]=Z_r^T R Z_r.

The original strict selector need not be rational.

## Proof

Choose a rational0<eta<min(a,b), and let

    S(A,X)=|A|²|X|²+|X|⁴,
    P_tilde=P-eta*S.

P_tilde retains the same weighted degrees and parity as P: quadratic in
A with X degrees2,3,4. It still has global strict support constants
a-eta,b-eta. The matrix-on-sphere/parity-homogenization proof applies
without requiring that its polynomial be literally a Bregman difference:
only those degrees, parity, and strict inequality enter that argument.
Thus for some r,

    |X|^(2r)P_tilde=Z_r^T R_tilde Z_r,   R_tilde>=0.

On exactly the full Z_r feature list, the reserve has a positive diagonal
Gram. Indeed the multinomial theorem gives

    |X|^(2r)S
      =sum_i sum_|alpha|=r+1 multinomial(r+1;alpha)
                                  (A_i X^alpha)^2
       +sum_|beta|=r+2 multinomial(r+2;beta)(X^beta)^2.

Every diagonal coefficient is a positive integer. Write this diagonal
matrix as D_r; then D_r>=I. Consequently

    R_real=R_tilde+eta*D_r >=eta I >0

represents |X|^(2r)P with the original possibly real kappa.

At this fixed r, all coefficient equations linking the ten selector
coefficients and the symmetric Gram entries are affine equations with
rational coefficients and rational right-hand side, because H is rational.
Their real solution affine space is nonempty by(R_real,kappa).
Gaussian elimination over Q supplies a rational particular solution and a
rational basis for its homogeneous nullspace. Rational points are therefore
dense in the real solution affine space. Positive definiteness of the
Gram is an open condition. Choose a rational solution sufficiently close
to(R_real,kappa); its Gram remains positive definite.
This is the required(R,kappa_hat).

## Consequence and scope

For rational input H, one can dovetail over levels r and rational
coordinates in each exact affine solution space, verifying positive
definiteness by rational LDL. If the displayed strict-support premise
holds, this search eventually outputs an exact rational certificate.
This is a semidecision procedure with potentially enormous cost, not an
efficient algorithm or an all-PC decision method.

The reserve avoids reliance on rational reconstruction of a singular
feasible face: some sufficiently high level admits a full positive-definite
Gram. It does not say that the first feasible level, or every feasible
level, has such a Gram, nor does it bound the required rational precision.

If H has arbitrary real coefficients, rational affine density is not
available in this form. If a=0 or b=0, subtracting the reserve may destroy
positivity and the conclusion is not established here.
