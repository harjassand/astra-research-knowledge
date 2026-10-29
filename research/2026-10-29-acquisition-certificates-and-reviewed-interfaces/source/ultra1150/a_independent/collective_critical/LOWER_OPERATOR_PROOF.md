# An acquired collective lower operator with the harmonic critical coefficient

29 October 2026. Work in progress. This is a rigorous finite-K LOWER operator,
not yet a thermal approximation or a claim of Gaussian readouts. The missing
upper normalization/state comparison is not supplied by this argument.

## 1. Native class and ordinary candidate

Let T be real symmetric PSD on M>=2 sites, with unique uniform zero mode
u=(1,...,1)/sqrt(M), gap at least lambda>0 and norm at most Lambda. For K>=1
particles of EACH flavor use the unchanged physical Hamiltonian

`H=Hhop+U sum_i q_i^2`, `Hhop=b†Tb+c†Tc`, `q_i=nb_i-nc_i`, U>0.

All one-body diagonal/normal-order terms are retained. The connected frustrated
family in the frozen paired_endpoint proof supplies an actual all-M example
and acquired gap/norm bounds. Nothing here assumes fixed density or a
thermodynamic gap.

Ordinary number/phase or Bogoliubov expansion predicts

`C(T,U,M)=sqrt(2U/M) Tr_Q sqrt(T)`,

`E0 ~ C sqrt(K)`.

The following exact algebra obtains the matching LOWER coefficient without
substituting a free bosonic oscillator or assuming small depletion. Formal
oscillator theory, its sampling and continuum-variable approximations are
established incumbents; the input-dependent lower receiver is not claimed as
a new physical squeezing principle.

## 2. All four number-conserving quadratures are retained

Choose a real orthonormal eigenbasis e_j of Q=u^perp with eigenvalues t_j>0.
Write b0,c0 for the u modes and bj,cj for the e_j modes. Let

`Abj=b0† bj`, `Acj=c0† cj`,

`X+j=Abj+Abj†+Acj+Acj†`,
`X-j=Abj+Abj†-Acj-Acj†`,
`J+j=i(Abj-Abj†+Acj-Acj†)`,
`J-j=i(Abj-Abj†-Acj+Acj†)`.

Each preserves BOTH particle numbers. The exact operator identity is

`X+j^2+X-j^2+J+j^2+J-j^2`

`=4(Abj†Abj+AbjAbj†+Acj†Acj+AcjAcj†)`.

For either flavor, `A†A+AA†=2n0 nj+n0+nj <=(2K+1)nj+K`.
Multiplying by t_j and summing gives the all-K operator inequality

`sum_j t_j(X+j^2+X-j^2+J+j^2+J-j^2)`

`<=(8K+4)Hhop+8K Tr(T)`.                            (C1)

Keeping the COMMON position quadrature X+ is essential: bounding the
commutator error only by total depletion loses order K^(1/4).

## 3. Exact charge-current commutator and the acquired pressure vector

Define the commuting Hermitian charge modes

`Q_j=sum_i e_j(i)q_i`.

Since sum_i q_i=0, sum_j Q_j^2=sum_i q_i^2. Put Nexc for total depletion
from b0,c0, and n_j=nbj+ncj. Direct one-body commutation gives

`i[Q_j,J-j]=(2/sqrt(M))(2K-Nexc-n_j)`

`+sum_l <e_l,e_j^2> X+l`.                           (C2)

Here e_j^2 means the pointwise square. For example, with f_j=diag(e_j),
the one-particle commutator equals

`u(e_j^2)^T+e_j^2 u^T-(2/sqrt(M))e_j e_j^T`.

Its u-component is exactly the first term of (C2); no small-fluctuation
replacement has occurred.

Write S=Tr_Q sqrt(T), and define

`W_l=sum_j sqrt(t_j)<e_l,e_j^2>`.

This vector is acquired basis-independently from

`d_i=(sqrt(T))_ii`, `W=E^T d`,

and its completed-square cost is `W^T T_Q^(-1)W=d^T T^+ d`.
No logical/collective pressure is assumed zero just because the condensate
mode is uniform. It is generally nonzero on the native trimer.

## 4. A global finite-K sum-of-squares bound

Set R=8K+4 and choose an acquired upper constant

`cbar >=2sqrt(U)(S+sqrt(Lambda))/(sqrt(M)lambda)`.

For K with R>=4cbar^2, take epsilon=cbar/sqrt(R)<=1/2,
a=(1-epsilon)/R and s=sqrt(Ua). Reserve epsilon Hhop and apply (C1)
to the remaining fraction. Define exact finite-K fast defect operators

`Y_j=sqrt(U)Q_j-i sqrt(a t_j)J-j`.

Their squares produce the positive commutator in (C2):

`UQ_j^2+a t_j J-j^2=Y_j†Y_j+sqrt(Ua t_j)i[Q_j,J-j]`.

The total negative number term is bounded by

`(2s/sqrt(M))(S+sqrt(Lambda))Nexc <=epsilon lambda Nexc`

`<=epsilon Hhop`.

It is therefore paid by the RESERVED hopping, not by an assumed depletion
bound. Complete the X+ squares using

`a sum_l t_l X+l^2+s sum_l W_l X+l`

`=a sum_l t_l[X+l+sW_l/(2a t_l)]^2-(U/4)d^T T^+d`.

All remaining X- and J+ squares are nonnegative. Consequently

`H >=4K sqrt[U(1-epsilon)/(M(8K+4))] S`

`-(1-epsilon)(8K/(8K+4))Tr(T)-(U/4)d^T T^+d`.         (C3)

More strongly, the right side can retain the explicit sum Y_j†Y_j and
the completed common/relative squares above. The scalar bound is an
operator inequality on the ENTIRE K,K sector, not a low-energy fixture.

Since sqrt(1-x)>=1-x on[0,1], for the same range of K,

`H >=C sqrt(K)-B`,

`B=Tr(T)+C cbar/sqrt(8)+C/2+(U/4)d^T T^+d`.           (C4)

Small K can always use H>=0. The required cbar, lambda, Lambda, square root,
pseudoinverse and thresholds are native matrix acquisitions with their
precision paid, not a missing many-body coefficient oracle.

## 5. Exact native trimer constants

For the unchanged trimer

```
T = [ 3  1 -4
      1  3 -4
     -4 -4  8 ],  U=1,
```

the nonzero eigenvalues are2,12, and

`S=sqrt(2)+2sqrt(3)`, `C=2sqrt(2)+2/sqrt(3) <4`,

`2(S+sqrt(12))/(sqrt(3)*2)=4+sqrt(2/3)<5`,

`d^T T^+d=(7-2sqrt(6))/36`.

Thus cbar=5 is acquired, (C3) holds for K>=13, and the conservative
all-K consequence is

`H_K >=[ (2sqrt(2)+2/sqrt(3))sqrt(K)-24 ] I`           (C5)

for EVERY K>=1. For K<13 its right side is negative, so positivity pays
that range. This is the CORRECT candidate harmonic coefficient in a
rigorous lower operator, improving the previous one-direction coercivity.
It does not yet prove that the coefficient is attained.

## 6. Honest M, gap and thermal boundaries

For the connected bounded-range family T_M, lambda>=4epsilon_bus/M^2 and
Lambda<=12+4epsilon_bus are explicitly available. The resulting cbar and B
can grow rapidly with M (coarsely cbar=O(sqrt(U)M^(5/2)/epsilon_bus),
B=O(UM^3/epsilon_bus+M)). This is not a useful fixed-density bound just
because it is all-K at each fixed M.

The normalizer only receives the valid one-sided consequence

`Z_K <=D_(M,K)^2 exp[-beta(Csqrt(K)-B)]`.

A matching variational coefficient, an absolute log-normalizer error,
actual thermal charge convergence and a positive approximate observation
law remain to be acquired. A formal harmonic spectrum or a passing
high-K plot will not supply them.
