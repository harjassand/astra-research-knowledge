# Independent strict-subcritical sufficiency and genuine moment transfer

Date: 2026-10-15. Internal analytic derivation, written before reading the new author's sufficiency proof. No finite-grid positivity test is used.

## 1. Statement and sole imported finite-block dependency

Use the contract in `INDEPENDENT_RECONSTRUCTION.md`. For every 0<R<r_*, there is one scalar probability noise with MGF finite throughout the open Euclidean ball B_R such that all blocks, and therefore the Hilbert direct sum, have a positive normalized regularization.

The tail construction below is explicit and does not use the abstract compact Laplace-coercivity theorem. The finite exceptional block family uses the bounded Wigner regularizer theorem: every finite bounded self-adjoint tuple has an all-exponential scalar regularizer. The relevant direct all-tail proof was read in the pinned source checkout at `updates/FU-regularization-clock-pressure-20261015/package/workers/operator_adversary/PROOF_AND_COUNTERMODELS.md`, Section 3, particularly the relative-error estimate and normalization argument. That dependency remains an internal proof, not an external certification.

## 2. One product noise regularizes every sufficiently large block

Choose R<L<r_* and S>R. Let

    p(x)=L/pi sech(Lx),  q(y)=S/pi sech(Sy).

Then |(log p)'|<=L. There is a finite C depending only on S such that, for every integer j>=1 and real y,

    |q^(j)(y)| <= j! C^j q(y).                         (1)

For completeness, choose h=pi/(4S). For complex z with |z|<=h, the inequalities

    |cosh(S(y+z))| >= cos(S Im z) cosh(S(y+Re z))
                     >= cos(pi/4) exp(-pi/4) cosh(Sy)

give |q(y+z)|<=C0 q(y), C0=sqrt(2)exp(pi/4). Cauchy's formula gives (1), for example with C=C0/h.

Fix a>0 and real b with C|b|<1, and ignore the harmless cI shift for now. Dyson's expansion of

    exp(i(k_1 a sigma_z+k_2 b sigma_x))

about i k_1 a sigma_z is indexed by the number j of flips sigma_x. Its j-th term is an integral over the time simplex of volume 1/j!. The accumulated sigma_z displacement lies in [-a,a]. When j is even the term is diagonal; when j is odd it is off-diagonal. Convolution with pq replaces each (i k_2)^j by (-1)^j q^(j)(y), times a translate p(x-u), u in [-a,a]. This follows from the Fourier convention integral exp(i k.x)f(x)dx, under which the transform of the j-th derivative is (-i k_2)^j times the transform.

All statements about the series can be justified in L1: the j-th absolute integral is bounded by (C|b|)^j times a constant independent of j, since p's translates integrate to one and (1) bounds the L1 norm of q^(j) by j!C^j. Hence the inverse transform and summation commute. The resulting continuous matrix density has exactly the desired characteristic function. It is self-adjoint because that characteristic function has Hermitian symmetry.

The zeroth term is the positive diagonal matrix

    D(x,y)=diag(p(x-a),p(x+a)) q(y).

Let E be the sum of all positive-order terms. For u in [-a,a], log-Lipschitz continuity gives

    p(x-u) <= exp(2La) p(x-a),
    p(x-u) <= exp(2La) p(x+a),
    p(x-u) <= exp(La) sqrt(p(x-a)p(x+a)).               (2)

The last inequality follows by multiplying

    p(x-u)<=exp(L(a-u))p(x-a),
    p(x-u)<=exp(L(a+u))p(x+a)

and taking square roots. Thus, writing alpha=C|b|, the diagonal entries of D^{-1/2}ED^{-1/2} are bounded in absolute value by

    exp(2La) alpha^2/(1-alpha^2),

and the off-diagonal entries are bounded by

    exp(La) alpha/(1-alpha^2).

For this self-adjoint 2-by-2 matrix, the row-sum bound gives

    ||D^{-1/2} E D^{-1/2}||
      <= [eta+eta^2]/[1-alpha^2],
       eta=C|b| exp(La).                              (3)

This is uniform over every real (x,y), including all remote tails. There is no discretization of space.

By the definition of r_* and L<r_*, choose epsilon>0 such that L+epsilon<r_*. Eventually

    |b_n|<=exp(-(L+epsilon)a_n),

so eta_n tends to zero. Therefore one finite index N makes (3) strictly less than one for all n>=N. The same scalar product density pq regularizes all those infinitely many blocks pointwise and simultaneously. Each block density is integrable and has characteristic value I at zero, hence integrates to I. Restoring c_nI translates the first coordinate by c_n.

The scalar noise pq has finite MGF whenever |g_1|<L and |g_2|<S, so it has every moment required by B_R.

## 3. Finitely many exceptional blocks and one common noise

Let T_fin be the finite direct sum of blocks n<N. It is a bounded self-adjoint pair. By the bounded Wigner regularizer theorem, choose one all-exponential scalar probability noise rho making its regularization a normalized positive operator measure. Define

    nu=(p(x)q(y) dxdy)*rho.

For n<N, positivity follows by convolving the rho-regularized measure with pq. For n>=N, positivity follows by convolving the pq-regularized measure with rho. The very same nu is used in every block. Its MGF is the product of the two scalar MGFs, and is finite on B_R.

Assemble the normalized block measures by the strong direct sum. For disjoint sets E_j and v=(v_n), the square of the norm of any countable-additivity remainder is bounded by a fixed constant times sum_n||v_n||^2; it tends to zero in each finite block. Dominated convergence proves strong countable additivity. Each effect is between zero and I and normalization is exact. This supplies the required infinite-dimensional POVM.

This proves strict-subcritical sufficiency only. It does not prove the endpoint R=r_* when r_* is finite. It also does not yield one all-exponential regularizer when r_*=infinity: the regularizer above depends on the chosen finite R. Those are exactly the two remaining candidate claims.

## 4. A self-contained genuine-moment argument for the necessity calculation

The finite-block moment identity does not need the difficult sufficiency theorem. Here is a scalarized analytic proof directly from the characteristic identity.

For a unit block vector v and a real direction h, let mu be the scalar positive probability measure obtained by projecting the compressed POVM along h. Its characteristic function is

    chi(z)=nu_hat(zh) <v,exp(i z(h_1 A_n+h_2 B_n))v>

on real z. The right side is holomorphic in the strip |Im z|<R/||h||, because the noise MGF is finite on B_R and the block exponential is entire. On every compact complex disk within that strip, Cauchy's estimate gives

    |chi^(2k)(0)| <= C (2k)! rho^(-2k).

The nonnegative finite difference integral

    integral [2-2cos(tx)]^k mu(dx)

is a finite linear combination of chi(jt). Division by t^(2k), Taylor expansion, and Fatou give a finite 2k-th moment bounded by the displayed derivative estimate. Having obtained that moment, dominated convergence for the same difference quotient gives its exact derivative identity. Tonelli applied to the nonnegative cosh series yields

    integral cosh(r x)mu(dx) <= C sum_k(r/rho)^(2k)<infinity

for every r<rho. Hence mu has genuine exponential moments throughout the projected strip. Both sides of the characteristic identity now admit Laplace continuation in that strip; identity on the real axis gives

    integral exp(g.x) <v,M_n(dx)v>
       =m_nu(g)<v,exp(g_1 A_n+g_2 B_n)v>

for every g in B_R. Polarization recovers the operator matrix identity.

At any (s,0) in the interior, choose delta>0 with (s,delta) and (s,-delta) still inside B_R. The elementary bound y^2<=C_delta exp(delta|y|), together with the two genuine moments at those tilts, justifies the first two transverse derivatives. Thus the tilted positive operator moment matrix and its Schur complement used in the necessary threshold argument are genuine integrals.

Alternatively, for each finite block, the compact-support Wigner distribution admits an elementary smooth exponential-cutoff proof: all translated cutoff derivatives are bounded by C_g exp(g.z), integrable against nu when m_nu(g)<infinity. Dominated convergence on the distributional side and monotone convergence on the positive measure side prove the same identity. This second route was read in the pinned internal source, Section 1 of the cited operator-adversary file.
