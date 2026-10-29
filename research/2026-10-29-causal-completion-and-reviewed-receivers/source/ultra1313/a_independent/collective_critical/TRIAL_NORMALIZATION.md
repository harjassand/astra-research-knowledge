# Paid collective Gaussian filter: norm and matching variational energy

29 October 2026. Constructive derivation; independent review pending. This
qualifies a normalized trial, not a supplied Gibbs state. Together with the
separate lower operator it can control actual thermal energy/defects.

## 1. A uniform local-CLT receiver derived from the finite source

Put d=M-1, M>=2. Let X be uniform on {0,e1,...,ed} in Z^d, m=E X,
Sigma=Cov(X)=I/M-11^T/M^2. Its eigenvalues are1/M and1/M^2 and
det Sigma=M^(-M). Let phi(t)=E exp(it.X), chi=|phi|^2 and
u=t^T Sigma t. The paired K,K difference has characteristic chi^K.
The K-1,K difference, after subtracting its mean -m, has characteristic
chi^(K-1)psi*, where psi=exp(-it.m)phi.

For t in[-pi,pi]^d the exact finite characteristic gives

`chi(t)<=exp[-a|t|^2]`, `a=4/(pi^2 M^2)`.

Indeed1-chi contains `(2/M^2)sum_j(1-cos t_j)`, and the other pair terms
are nonnegative. On |t|^2<=1/(8d), use centered categorical moments:

`E(t.(X-m))^4<=M u^2`,

`|chi-(1-u)|<=(M+3)u^2/12`.

Consequently chi>=1-u, `chi<=exp[-b u]`, b=1-1/(24d), and

`|log chi+u|<=C4 u^2`, `C4=(M+15)/12`.

Here u<=1/(8dM)<=1/16. These are elementary finite-source bounds, not a
supplied local-limit constant. They imply

`|chi^K-exp(-Ku)|<=K C4 u^2 exp(-bKu)`

on that ball. Also `|psi*-chi|=|psi*||1-psi|<=u/2`.

Gaussian integration after whitening Sigma, with b^(-d/2-2)<2, bounds the
paired local Fourier error relative to its Gaussian density at zero by
`C4 d(d+2)/(2K)`. The extra residual factor is bounded by3d/K when
K>=4d+4. Outside the ball, the global a bound gives both Fourier tails
with the following COMMON conservative error:

`E_K=A_M/K+B_M exp(-tau_M K)`,

`A_M=C4 d(d+2)/2+3d`,
`B_M=2(4/a)^(d/2) M^(-M/2)`,
`tau_M=1/(8pi^2 d M^2)`.                             (N1)

For the residual use K-1>=K/2, split the remaining Gaussian exponent in
half, and integrate over all R^d. This gives the displayed B_M and tau_M.
The Gaussian comparison itself is integrated over all R^d, so its portion
outside the Fourier torus is included. The conclusion is UNIFORM in every
integer difference q, including values outside the physical support.

Equivalently, on the physical zero-sum lattice A_d={q in Z^M:sum q=0},

`|P_K(q)-g_K(q)|<=g_K(0) E_K`,

`g_K(q)=g_K(0) exp[-alpha|q|^2]`,
`g_K(0)=M^(M/2)/(4pi K)^(d/2)`, `alpha=M/(4K)`.

For K-1,K use the same bound at the centered affine lattice qbar=q+1/M,
which has sum zero. No occupation point was enumerated to acquire (N1).
Its local constant is polynomial in M. B_M may be large, but log B_M and
tau_M^(-1) have polynomial size; its actual tail is explicitly charged.

## 2. Lattice-Gaussian sums, including all shifts

Let G be SPD on Q=1^perp and zero on1, with acquired bounds
`0<gmin<=G|Q<=gmax`. Define

`A=G/sqrt(K)`, `C=A+alpha I_Q`.

For any shifted copy of A_d, Gaussian Poisson summation gives its sum
`I_C(1+xi)`, where

`I_C=pi^(d/2)/[sqrt(M) sqrt(det_Q C)]`.

In integer coordinates q=(n,-sum n), the embedding has squared norm M.
Therefore a valid UNIFORM shifted relative error is

`theta_C=[(1+r_C)/(1-r_C)]^d-1`,

`r_C=exp{-pi^2/[M(gmax/sqrt(K)+alpha)]}`.              (N2)

For A use the same formula with alpha=0, giving theta_A. This follows by
bounding every nonzero dual Gaussian term with the product theta series;
`sum_(n>=1) r^(n^2)<=r/(1-r)`. It does not assume the shifted sum is maximal
at its center. For the unshifted lattice all dual phases are1, and
differentiation in an isotropic positive direction additionally gives

`sum_q |q|^2 exp(-q^T Cq) <=(Tr_Q C^(-1)/2)sum_q exp(-q^T Cq)`. (N3)

The discarded dual derivative has the correct NONPOSITIVE sign. Termwise
Gaussian differentiation is justified on compact SPD neighborhoods. This
moment statement is used only for the centered lattice, not arbitrary shifts.

## 3. Actual trial normalization, with no norm oracle

Let Omega_K=|u^K>_b|u^K>_c and

`F(q)=exp[-q^T Gq/(2sqrt(K))]`,

`p=<Omega_K,F^2 Omega_K>`, `Psi=F Omega_K/sqrt(p)`.

The exact p is the positive tilt of two known independent multinomials.
Applying (N1) and (N2) to the WHOLE lattice, not a finite velocity/count
cutoff, yields

`p0=det_Q[I+(4sqrt(K)/M)G]^(-1/2)`,

`Rdet=sqrt(det_Q C/det_Q A)`,

`delta_K=theta_C+E_K(1+theta_A)Rdet`,

`p0(1-delta_K)<=p<=p0(1+delta_K)`.                    (N4)

The usable gate is delta_K<1. Every determinant, norm, tail and error in
this test is acquired from M,K and G. No interacting normalizer, permanent,
occupation cutoff or Gibbs element is supplied. The CLT's ABSOLUTE error
integrates against a Gaussian; no unsupported uniform relative local limit
on the full occupation lattice is assumed.

Using (N3), the actual trial charge moment is bounded by

`<sum_i q_i^2>_Psi <=sqrt(K)Tr_Q G^(-1)/2`

`* (1+delta_K)/(1-delta_K)`.                          (N5)

This is an unbounded moment of the explicitly normalized TRIAL, paid by
the lattice Gaussian calculation; it is not inferred from a TV bound.

## 4. The one-body hopping ratios are acquired by the same norm receiver

Annihilation in the product condensate gives EXACTLY

`<Hhop>_Psi=(2K/M)sum_ij T_ij r_ij/p`,

`r_ij=E_(K-1,K)[F(q+e_i)F(q+e_j)]`.

The residual difference has sum -1. Set
`delta_ij=(e_i+e_j)/2-u/sqrt(M)` and
`a_ij=(e_i-e_j)^T G(e_i-e_j)`.
The product of the two filters is a shifted Gaussian times
`exp[-a_ij/(4sqrt(K))]`. The continuous Gaussian integral has the extra
factor exp(-sigma_ij), where

`0<=sigma_ij=alpha delta_ij^T A C^(-1)delta_ij<=alpha`.

Applying the SAME shifted-lattice and residual CLT bounds gives

`|r_ij/p-exp[-a_ij/(4sqrt(K))]|<=gamma_K`,

`gamma_K=[M/(4K)+2delta_K]/(1-delta_K)`.               (N6)

Here ||delta_ij||<=1, and all numerator/denominator errors are accounted for.
In particular diagonal hopping/potential contributions have NOT been dropped.

Because T1=0, `sum_ij T_ij a_ij=-2Tr(TG)`. Using
`|exp(-x)-1+x|<=x^2/2` for x>=0 and a_ij<=2gmax gives

`<Hhop>_Psi<=sqrt(K)Tr(TG)/M`

`+ (sum_ij|T_ij|/M)[gmax^2/4+2K gamma_K]`.            (N7)

The absolute entry sum is essential for frustrated hopping; no positive
bond Dirichlet form or false sign cancellation is assumed.

## 5. A matching coefficient with an explicit finite-K remainder

Acquire

`G=sqrt(MU/2) (T_Q)^(-1/2)`.

Then the leading sum of (N5) and (N7) is exactly

`C sqrt(K)`, `C=sqrt(2U/M)Tr_Q sqrt(T)`.

For every qualified K>=4d+4 with delta_K<1,

`<H>_Psi <=C sqrt(K)+R_up(K)`,

`R_up=(sum_ij|T_ij|/M)[gmax^2/4+2K gamma_K]`

`+U sqrt(K)Tr_Q G^(-1) delta_K/(1-delta_K)`.           (N8)

At fixed M,U and positive gap this remainder is O(1) as K tends to infinity:
E_K=O(1/K), theta errors decay exponentially in sqrt(K), Rdet->1.
All M/gap dependencies are explicit; no uniform K=rho M conclusion follows.

This is ordinary Gaussian/local-limit/Poisson machinery composed for a
number-conserving filter. It acquires the missing normalization and energy
of that filter, not a full canonical Gibbs sampler. The exact lower operator
and the entropy bound control actual THERMAL defect expectations in the
separate THERMAL_READOUT.md proof. This trial argument alone is not that
thermal-state comparison.
