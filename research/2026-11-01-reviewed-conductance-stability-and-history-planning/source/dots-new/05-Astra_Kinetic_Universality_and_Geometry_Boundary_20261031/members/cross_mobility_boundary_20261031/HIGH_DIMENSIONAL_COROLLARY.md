# The same obstruction persists at arbitrary Gaussian fiber dimension

Status: separately marked corollary; independent review and exact checks PASS.
This adds no new mechanism and does not alter the exact two-dimensional
classification. It prevents reading the 2D example as only a low-dimensional
failure of an otherwise dimension-uniform, cross-mobility claim.

For each m>=1 fix

    F_m(y,z)=v(y)||z||^2/2,  z in R^m,
    v(y)=1+(1-y^2)^2,       beta=1,
    A={y<=-1/2}, B={y>=1/2}.

Use the same rational 2-by-2 cross block D_(epsilon,k) on (y,z_1), and the
identity on z_2,...,z_m. The matrix is constant SPD for every finite m,k and
0<epsilon<1. The invariant y density is proportional to v(y)^(-m/2), so its
tail is integrable for every integer m>=1. Its conditional z law is Gaussian
N(0,v(y)^(-1)I_m).

The same all-SPD Lyapunov works in dimension m+1:

    V_D=1+x^T D^-1 x,
    L V_D=2(m+1)-[6(y^2-2/3)^2+4/3]||z||^2<=2(m+1).

Thus nonexplosion, conservative reversibility and invariant probability are
received for every actual member by the same stopped/exhaustion argument.

The same exactly admissible smooth trial from PROOF.md depends only on (y,z_1).
Its core energy is <=36epsilon. Nonzero patch energy is <=900 and requires
|z_1|>=k/8. Uniformly in y, the conditional variance of z_1 is <=1. The elementary
Gaussian Chernoff bound gives

    P(|z_1|>=k/8 | y)<=2exp(-k^2/128).

Therefore, WITHOUT ANY m-dependent normalization input,

    cap_m,D(A,B)<=36epsilon+1800exp(-k^2/128).             (H1)

The shoulder comparison remains valid: the central interval has length 1 and
v>=25/16 there, whereas the shoulder [-1,-1/2] has length 1/2 and v<=25/16.
Raising v to the negative power m/2 preserves the comparisons, giving
mu_m(A)>=1/4. Consequently

    cap_m,D(A,B)/mu_m(A)<=144epsilon+7200exp(-k^2/128).    (H2)

## Explicit collapse relative to the freely equilibrated benchmark

Let Q_m=integral_R v^(-m/2)dy and
R_m=integral_{-1/2}^{1/2}v^(m/2)dy. The optimal y-only trial has capacity

    C_free,m=1/(Q_m R_m).

This notation identifies a variational benchmark, not a fast-equilibration
assumption about the actual cross-mobility process. Since v>=1,
Q_m<=Q_1<8, by the 2D normalization bound in PROOF.md. On the unit-width slab,
v<=2, so R_m<=2^(m/2)<=2^m. Thus

    C_free,m>1/(8*2^m).

Choose the explicit rational family

    epsilon_m=2^(-3m-10),    k_m=16m.

Because exp(-2m^2)<=2^(-2m^2), (H1) gives

    cap_m,D / C_free,m
      <=288*2^(-2m-10)+14400*2^(m-2m^2) -> 0.           (H3)

The same ratio holds for capacity/mass versus C_free,m/mu_m(A).
Thus growing Gaussian fiber dimension cannot rescue a uniform relative
free-capacity guarantee once these cross mobilities are admitted.

Costs are part of the statement: the cross coefficient is 16m, the transverse
mobility on z_1 is (16m)^2/(1-epsilon_m), the Schur complement is 2^(-3m-10), and
the matrix condition number grows on the order of m^2*2^(3m). The denominator of
epsilon_m has O(m) bits, and the full explicit matrix has m+1 coordinates. No
uniform conditioning, bounded mobility, fixed precision, physical implementation,
or hidden fast mixing is claimed. This is a direct application of the exact
boundary patch, not a second discovery or a new PDE theorem.
