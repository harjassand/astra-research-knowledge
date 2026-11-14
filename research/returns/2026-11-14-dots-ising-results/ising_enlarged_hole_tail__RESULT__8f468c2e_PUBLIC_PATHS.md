# Enlarged-defect complementary tail: independent finite receipt

This is a direct Gibbs-mass pruning estimate, not a new clock or transport. It complements the separately proved marked-cover theorem with cutoff `A <= 4 R^2/3`.

## Scope
Use the unchanged Ising model theta=4, phi=4/R, L=8R, n=L^2, original non-target set B complement, original core normalizer ZA and voltage 0<=v<=1. Consider states with exactly two actual axial noncontractible walls and total essential physical perimeter at least `Pmin=4L-16`, and at least one contractible filled contour with area `A>4R^2/3`. Other contractible contours are arbitrary. The perimeter condition is earned in the residual branch after removing states with a short actual wall; it is not an assumption valid for all two-axis states.

For a contractible lifted contour, `A <= wh <= P^2/16`. Thus the marked large contour has

    P >= H = floor(8R/sqrt(3)) + 1.

The integer H is computed without floating point and certified by `3(H-1)^2 <= 64R^2 < 3H^2`. The strict area inequality matters at an integer threshold.

## Positive marked-wall overcount
Import the independently checked axial nonbacktracking estimate in `n1722_axis_nonbacktracking_tail_20261113/RESULT.md`: rho=13/4, vtilt=3/2, z=rho exp(-8), q=3 exp(-8), ordinary full-wall pressure `A0=100n q^4/(1-q)`.

Mark one long contractible contour. Root/walk count bounds the sum of its activities by `100n q^H/(1-q)`. Multiply by the unrestricted ordinary contour product `exp(A0)` for every other wall. Marking may count one configuration several times; all summands are nonnegative, so this is an upper bound. It does not require independent actual contours and does not remove the pressure of unmarked walls.

The exact existing essential-wall length sum, axes, roots, and global spin choice give

    Z_large/ZA <= 320000 n^2(Pmin+2)
        exp(32L+A0) (3/2)^(-2L) z^Pmin
        * 100n q^H/(1-q).

The global non-target field bound exp(phi n)=exp(32L) is used ONCE. In particular no additional local positive-area field factor is attached to the marked contour. ZA>=w_minus suffices. Since v<=1, the same expression bounds the actual original-clock occupation N_large/ZA.

## Exact finite arithmetic
`check.py` uses Fraction arithmetic, an exact positive Taylor lower bound exp(8)>2980, q<3/2980, and rational atanh logarithm bounds with explicit geometric remainders. All displayed polynomial prefactors and the unmarked wall pressure are charged.

- R=1000: H=4619, log upper < -457, so N_large/ZA <= exp(-457).
- R=10000: H=46189, log upper < -6265, so N_large/ZA <= exp(-6265).
- R=80 and200: this bound is vacuous. No claim at these instances.

The complementary small/enlarged-defect branch still requires its own corrected cyclic interval-peeling cover, pressure, failed-completion geometry, and finite source-union accounting. This note alone does not prove a full two-axis sector theorem, much less all winding or full residence closure.
