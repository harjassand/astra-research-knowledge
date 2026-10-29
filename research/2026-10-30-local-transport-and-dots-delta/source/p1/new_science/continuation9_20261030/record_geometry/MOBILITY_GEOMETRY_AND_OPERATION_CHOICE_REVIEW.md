# Receiving review: mobility geometry and the supplied operation

Existing record-geometry role. Actual root input:
`../MOBILITY_GEOMETRY_AND_OPERATION_CHOICE.md`, SHA-256
`50410d4b89838cb520b1d27f07f1f7b658da038ed17fa74f3f1612c383147b60`.

Exact snapshot: `MOBILITY_GEOMETRY_AND_OPERATION_CHOICE_REVIEWED_50410d4b8983.md`.

**Accepted as stated:** the finite-dimensional response/noise criterion, its stronger Loewner-order necessity theorem, force normalization, the exact rank-at-most-k added current port, and the conditional nonlinear variational calculation. These are claims about specified operations and comparison laws. They do not identify the limit of the particle-field apparatus or supply an acquired/local nonlinear implementation.

No mathematical correction and no numerical fixture were needed.

## 1. The native metric projection

With M positive definite and H full column rank, `G=H*MH` is positive definite. The matrix

\[
\Pi=M^{1/2}HG^{-1}H^*M^{1/2}
\]

is an orthogonal projector. Therefore

\[
M_c=M^{1/2}(I-\Pi)M^{1/2}
\]

is symmetric positive semidefinite, obeys `0<=M_c<=M`, and annihilates H. The oblique map `T_M=I-MHG^{-1}H*` obeys `H*T_M=0` and `T_M M T_M*=M_c`. All matrix orders in the input are correct; no commutation assumption is used.

For `b=Mf`, both the physical response and the covariance are indeed changed through M_c. The removed density covariance is

\[
2(BMH)G^{-1}(BMH)^*.
\]

Its vanishing is equivalent to BMH=0 because G is positive definite. Equality of density response for every force has difference `BMHG^{-1}H*M`; multiplying by H on the right recovers BMH. Thus all three equivalences in Section 2 hold. Merely requiring BH=0 does not suffice.

The statement is about all forces in the stated port. A special self-consistent thermodynamic drift may remain feasible even when some externally probed density responses and the density noise change. The nonlinear heat example uses precisely this distinction; it does not contradict the criterion.

## 2. The stronger necessity theorem

Suppose `0<=M'<=M`, `M'H=0`, and `BM'B*=BMB*`. Put `L=M-M'>=0`. Then

\[
0=BLB^*=(BL^{1/2})(BL^{1/2})^*
\]

implies `BL^{1/2}=0` and hence BL=0. Consequently

\[
BMH=BM'H+BLH=0.
\]

No invertibility of B or M' is used. Conversely, if BMH=0, M'=M_c satisfies every requested condition. The stated necessary-and-sufficient condition is therefore proved for the full declared Loewner-order class, not just the particular projected choice.

The physical interpretation must remain the one printed in the source. An added reciprocal passive **series impedance at the unchanged native current port**, with a well-defined DC limit, has resistance `M^{-1}+S` with S positive semidefinite, so its DC mobility is no larger than M; ideal constraints are limiting cases. This does not bound every passive transformer, every added transport channel, or a complex finite-frequency response in Loewner order. The root text correctly confines its conclusion to the specified port/DC class.

## 3. Force normalization

Let `b_c=T_M b`, `r=b-b_c=MHG^{-1}H*b`, and take a feasible current `H*j=0`. Then `H*(j-b_c)=0`, so

\[
(j-b_c)^*M^{-1}r=0,
\qquad
r^*M^{-1}r=(H^*b)^*G^{-1}(H^*b).
\]

Expansion gives exactly equation (7), including its factor 1/4 for noise covariance 2M. On the allowed subspace the inverse quadratic form of M_c equals that of M: for feasible a, `M_c M^{-1}a=a`, and adding a kernel vector to an inverse solution does not change `a* M^{-1}a`. Thus the first term really is the physical degenerate-Gaussian action, with minimum zero at b_c.

Restricting a forced native action without removing the second term would give a nonzero minimum. The source correctly separates that normalization error from the unforced nonlinear density-contraction penalty.

## 4. The extra matched current port is algebraically sufficient

The Euclidean projector Q satisfies `QH=0` and `BQ=B`. Because M_c is symmetric and annihilates H, `QM_cQ=M_c`. Projecting its defining identity gives

\[
QMQ=M_c+QMHG^{-1}H^*MQ.
\]

Thus E and U in equation (9) obey `E=UU*>=0`, `rank E<=rank H`, and `H*U=0`. M_g is positive semidefinite, strictly positive on the allowed subspace; it is not positive definite on the full current space when H is nontrivial.

An actual additional independent port with response E f and covariance 2E therefore changes the total response/noise from M_c to M_g and keeps the protected current zero. Both terms are essential. Supplying noise only, changing a measured output, or applying a formal projection to a recorded current does not provide that port.

For density-conjugate forces `f=-B*grad V`, constant M and B give

\[
BM_gB^*=BMB^*,
\]

so the complete density SDE has exactly the native drift and covariance. Under the ordinary well-posedness/uniqueness assumptions implicit in the stated regular confining potential and the same actual initializer, it has the same complete density path law. This is stronger than matching a static covariance. It applies to constant mobility with the explicitly supplied added current channels and noise, not to the unproved state-dependent particle-field elimination.

The input correctly limits unchanged force response here to density-conjugate forces. In general `BM_g f=BM Qf` need not equal BMf for an arbitrary force having a protected component. The operation changes that part of the physical port.

## 5. The nonlinear variational statement

The Section 3 clock convention is consistent: D=1 and noise strength `2chi` give action `1/4 integral (j+rho_x)^2/chi`. Writing compatible current as k+I and completing its scalar square yields `I_*=-L/R` and penalty `L^2/(4R)` under I=0. Completing two squares under a common I yields the coefficient in equation (5), including the factor 1/4.

For the traveling wave, `k=v(rho-m)` satisfies continuity, and the weighted gradient term integrates to zero because `rho_x/chi(rho)` is a periodic derivative. The displayed radicals in equation (6) and the m=1/4, a=1/8 example are correct. A static flat second ring has zero optimal circulation, so the two-ring density-action gap is strictly positive.

The separate `MOBILITY_WEIGHTED_DENSITY_ACTION.md` preserves my independent derivation with general constant D, the explicit example, and the different Euclidean port. Neither calculation proves that the root microscopic nonlinear dynamics realizes the metric-constrained comparison action. The root source preserves that missing theorem and does not call the calculation a no-go for every passive architecture.

## 6. Direct primary predecessor for the positive-operator geometry

There is a particularly close established formulation: the **shorted operator**. The primary publisher abstract of Anderson and Trapp, *Shorted Operators. II*, SIAM J. Appl. Math. 28 (1975), 60-71, [DOI 10.1137/0128007](https://epubs.siam.org/doi/10.1137/0128007), defines the maximal positive operator below a given one whose range lies in a specified subspace, and connects the problem to electrical networks. I read that original publisher abstract; its paywalled full proof was not imported.

Here M_c is exactly the short of M to `ker H*`. This can be checked directly in finite dimensions: in an orthonormal basis adapted to that subspace, write M as `[[A,C],[C*,D]]`. The largest positive X supported in the first block with X<=M is `diag(A-CD^{-1}C*,0)`, by the Schur-complement criterion. That matrix is M_c. This is close prior machinery for the projection/order part; the task-specific response/noise consequence remains the explicit calculation with B.

## Final receiving status

Accepted at the stated finite-dimensional and actual-port interfaces. The stronger necessity theorem is valid, and the added rank-k matched port is a genuine mathematical alternative because it leaves the restricted class of merely reducing native mobility. The source neither supplies that operation by acquisition nor asserts locality for generally extended U. No changes to the reviewed input are required for mathematical correctness.
