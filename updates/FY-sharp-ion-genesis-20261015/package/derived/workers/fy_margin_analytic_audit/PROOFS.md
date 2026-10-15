# Reconstructed proofs and rate audit

Fix `r<-2`, `alpha=3r/[8(r+2)]>0`, `beta=r(r-1)/6>0`, and

```
J(A)=alpha*((a-d)^2+(b+c)^2)^2
      +beta*(a^2+c^2)^2+(ad-bc)^2+r*(a^2+c^2)*(ad-bc),
A=[[a,b],[c,d]].
```

Use ordinary Lebesgue measure on a fixed rectangular torus Omega, or on
R2 when explicitly stated. All matrix norms are Frobenius norms. Integrals
of derivatives and determinants of periodic or compact zero-extended
compatible gradients vanish. Approximation makes these identities valid
for W1,4 maps. Every constant below is finite for fixed r; the cubic
estimate does not supply a numerical constant for the unrestricted margin.

## 1. Inherited rank-one Bregman estimate

Rank-one convexity of J and homogeneity imply, for every constant matrix B
and every rank-one R,

```
J(B+R)-J(B)-DJ(B):R >= J(R)/3 >= (alpha/3)|R|^4.       (1)
```

For completeness, write the convex scalar quartic `J(B+tR)` as
`at^4+bt^3+ct^2+dt+e`, with `a=J(R)>0` if R is nonzero. Nonnegativity of
its second derivative on the whole real line gives `c>=3b^2/(8a)`. Thus

```
a+b+c >= a/3+3(b+4a/3)^2/(8a) >= a/3.
```

For rank-one R the determinant terms vanish and `H(R)=|R|^4`, giving the
second inequality in (1). The zero matrix case is immediate.

## 2. Conditional two-step proof on the triangular class

Let `phi=(f(x,y),g(y))` be periodic W1,4, so `phi_2,x=0`. Denote x
conditional averaging by E_x and set

```
m=E_x Dphi=[[0,(E_x f)_y],[0,g_y]],
w=Dphi-m=[[f_x,f_y-(E_x f)_y],[0,0]].
```

Both m and w have rank at most one. For a.e. y, `E_x w=0`. Apply (1)
pointwise at background `B+m(y)` and integrate in x. The linear term
cancels because the background and its derivative are independent of x:

```
integral_Omega [J(B+Dphi)-J(B+m)] >= (alpha/3) integral_Omega |w|^4.
```

Apply (1) to m at B and integrate over Omega. The mean of m is zero,
so its linear term also cancels. Addition gives

```
Gap_B(phi) >= (alpha/3) integral_Omega (|w|^4+|m|^4)
           >= (alpha/24) integral_Omega |Dphi|^4.      (2)
```

No side-length factor is lost: the first step uses conditional averages,
and the second step is integrated over the entire rectangle. This proves
the constant independent of B and the rectangle side lengths. Strong
W1,4 approximation, or the a.e. conditional argument itself, covers rough
periodic maps. The conditional nonlinear background causes no issue.

## 3. Mixed-Hessian interpolation with explicit axis handling

For a periodic scalar f with Hessian in L4, and with f_xx additionally in
L2, there is an absolute constant C such that

```
||f_xy||_(8/3)^2 <= C ||f_xx||_2 ||f_yy||_4.          (3)
```

The same holds on R2 in the homogeneous Hessian class `D2f in L4` with
`f_xx in L2`. The full-Hessian condition excludes a polynomial mixed
term. It is essential to some such homogeneous formulation: f=xy shows
that pure-derivative assumptions alone are insufficient on R2.

Here is a direct proof on the torus. First take a trigonometric polynomial
and replace it by `f'=(I-E_x)(I-E_y)f`. Then `f'_xy=f_xy`,
`f'_xx=(I-E_y)f_xx`, and `f'_yy=(I-E_x)f_yy`. The first projection is an
L2 contraction; the latter has L4 norm at most 2. Only modes with both
frequencies nonzero remain.

For nonzero one-dimensional frequencies n, the symbol `|n|^(2it)` has
modulus 1 and dyadic variation bounded by `2|t| log 2`. The periodic
one-dimensional Marcinkiewicz multiplier theorem therefore gives an Lp
bound `C_p(1+|t|)` for every `1<p<infinity`. Tensoring in x and y gives
the corresponding polynomial bound for
`U_t=|Dx|^(2it)|Dy|^(-2it)`. These constants are independent of the circle
lengths: rescaling contributes only unimodular scalar factors. On the
remaining modes U_t is an L2 isometry.

Set `A=||f_yy||4`, `B=||f_xx||2`; if either is zero, Fourier coefficients
give `f_xy=0`. Otherwise use the finite-mode analytic family

```
F(z)=A^(z-1) B^(-z) |Dx|^(2z)|Dy|^(2(1-z)) f'.
```

At `Re z=0`, the L4 norm is bounded by `C(1+|Im z|)^2`; at `Re z=1`,
the L2 norm is at most 1. The exponents arise because the first boundary
contains `|Dy|^2 f'` and the second `|Dx|^2 f'`.

To make the interpolation step explicit, let g be a simple dual test
function with `||g||_(8/5)=1`. Define an analytic scalar dual family by

```
G(z)=conjugate(sgn g)*|g|^[(8/5)(3/4-z/4)],
G(z)=0 where g=0.
```

At Re z=0 its L(4/3) norm is 1; at Re z=1 its L2 norm is 1; and
`G(1/2)=conjugate(g)`. The function

```
exp(epsilon*(z-1/2)^2) * integral F(z)G(z)
```

is bounded on the closed strip for any fixed epsilon>0. The Gaussian
absorbs the boundary polynomial growth. The scalar three-lines theorem
therefore bounds its midpoint by an absolute constant. Duality gives

```
|| |Dx||Dy| f' ||_(8/3) <= C A^(1/2)B^(1/2).
```

The x and y sign multipliers, equivalently the two coordinate Hilbert
transforms, are bounded on L(8/3) by the same one-dimensional multiplier
theorem. They convert this expression to f_xy, proving (3).

For periodic rough Hessians use periodic smoothing and finite Fourier
approximation, or smooth rectangular Fourier cutoffs with uniform Lp
bounds, then lower semicontinuity. On R2 use smooth separable frequency
cutoffs supported away from the coordinate axes and infinity, followed by
the identical argument with the real-line multiplier theorem. Uniform
Lp boundedness and convergence on the given L4 Hessian components remove
the cutoffs. Their mixed component converges in L4, so it identifies the
L(8/3) weak limit and excludes polynomial ambiguities.

## 4. Exact cubic coefficient and an elliptic right inverse

Write the compatible gradient as `q=[[p,b],[c,z]]`, and put

```
S=(r+1)p+z,
lambda=r(r+2)/3>0,
m(q)=integral(S^2+lambda*c^2),
n(q)=||p||4+||c||4+||z||4,
K(q)=integral J(q),
ell(q)=integral DJ(q):I.
```

Quartic expansion, the zero means, and `integral det q=0` give

```
Gap_(tI)(phi)=t^2 m(q)+t ell(q)+K(q),                  (4)
ell(q)=integral [2pS^2+S*(-2bc+r*c^2-(r+2)*p^2)
                -lambda*p*(c^2+p^2)].               (5)
```

Pointwise, the coefficient of t^2 is `S^2+lambda*c^2+(r+2)det q`.
The exact checker verifies both identities.

Solve `Delta w=S` and set `eta=(w_x/(r+1),w_y)`, `e=Deta`.
On the torus S has zero mean, so use the mean-zero inverse. On R2 use
the homogeneous Fourier inverse. Only e is needed. Its entries are
constant multiples of the second-order Riesz transforms of S, and hence

```
||e||_p <= C_(r,p,Omega) ||S||_p,  1<p<infinity.       (6)
```

On R2 the constant has no Omega dependence. On a fixed torus this is the
standard periodic elliptic multiplier bound. Constants need not be made
uniform over varying tori for the compactness theorem below. There is
no zero-mode defect because S has zero mean and the inverse is set to
zero on the constant mode.

The compatible remainder `q0=q-e` satisfies `(r+1)p0+z0=0`. Put
`k=-(r+1)>1`. Subtract component means from its potential. The closed
one-form `(phi0_2/k)dx+phi0_1 dy` then has zero periods and gives

```
q0=[[f_xy,f_yy],[k*f_xx,k*f_xy]].                     (7)
```

This representation also follows frequency by frequency, including the
axes: on the y axis phi0_2=0; on the x axis phi0_1=0. The zero mode of
the gradient is absent. On R2 the representation is distributional; the
L4 entries of q0 supply the homogeneous Hessian class required in (3).

Equations (6)-(7) give

```
||c0||2 <= C_r sqrt(m),
||p0||4 <= C_r n(q),
||b0||4 <= C_r ||q||4.
```

The only cubic term in (5) not directly charged to S or c in L2 is p^3.
By Holder and (3),

```
integral |p0|^3 <= ||p0||4 ||p0||_(8/3)^2
 <= C_r ||p0||4 ||c0||2 ||b0||4
 <= C_r sqrt(m) n(q) ||q||4.                          (8)
```

The polynomial perturbation is bounded at the required rate:

```
|integral(p^3-p0^3)|
 <= C ||e11||2 (||p0||4^2+||e11||4^2)
 <= C_r sqrt(m) n(q)^2
 <= C_r sqrt(m) n(q) ||q||4.                          (9)
```

For all other terms of (5), put one S or c in L2, and the remaining two
factors in L4. For example `|integral Sbc|<=||S||2||b||4||c||4` and
`|integral pc^2|<=||c||2||p||4||c||4`. Together with (8)-(9), this proves

```
|ell(q)| <= C_r sqrt(m(q)) ||q||4 n(q).               (10)
```

The constants in this proof may depend on the fixed torus. Smooth
approximation proves (10) for the stated W1,4 classes. Neither the
projection nor the elliptic correction is asserted to preserve compact
support; their global Lp bounds are the properties actually used.

## 5. Growing exact contact backgrounds under uniform integrability

Let `||q_n||4=1`, let `|q_n|^4` be uniformly integrable, and suppose
`|t_n| -> infinity`. The domain is one fixed torus, or q_n are supported
in one fixed bounded set of R2. Then

```
liminf Gap_(t_n I)(phi_n) >= alpha(r).                (11)
```

To prove this, select a subsequence whose gaps are bounded above. The
quartic coefficient K and n(q_n) are bounded. By (4) and (10),

```
Gap_(t_n I) >= t_n^2 m_n-C_r |t_n| sqrt(m_n)-C_r.
```

The right side is a quadratic polynomial in `|t_n|sqrt(m_n)` with
positive leading coefficient. Bounded gaps therefore imply
`|t_n|sqrt(m_n)=O(1)`, and in particular `m_n=O(|t_n|^-2) ->0`.
Consequently S_n and c_n tend to zero in L2.

The determinant identity is

```
0=integral(pz-bc)=integral[pS+k*p^2-bc],
k*||p||2^2 <= ||p||2||S||2+||b||2||c||2.              (12)
```

All original L2 norms are bounded by the fixed finite-measure domain or
support and the L4 normalization. Equation (12) gives p_n ->0 in L2,
and `z_n=S_n+k*p_n ->0` in L2. Uniform integrability of the fourth
powers upgrades all three convergences to L4. Thus `n(q_n)->0`.
The same conclusion follows by splitting into small, bounded, and tail
values; it does not assume convergence of the full q_n in L4.

Since the only surviving component is b_n, normalization gives
`integral|b_n|^4 ->1`. Polynomial continuity on bounded L4 sets gives

```
K(q_n)-alpha*integral|b_n|^4 ->0,
K(q_n) -> alpha.
```

If m_n>0, (10) now yields `ell_n^2/m_n <= C_r n(q_n)^2 ->0`.
Completing the scalar affine square in (4) proves

```
Gap_(t_n I) >= K(q_n)-ell_n^2/(4m_n) -> alpha.
```

If m_n=0, (12) directly gives p_n=c_n=z_n=0, ell_n=0, and the gap is
alpha. Subsequences with unbounded gaps cause no smaller liminf. This
proves (11). It also proves `inf_t Gap_(tI)(q_n) -> alpha` whenever
`m(q_n)->0` under the same normalization and uniform-integrability
hypotheses.

The asymptotic constant is exact: for any normalized periodic pure shear
`q=[[0,b(y)],[0,0]]`, the gap at tI equals `alpha*integral b^4=alpha`
for every t. This example satisfies uniform integrability when fixed.

## 6. Scope of what has and has not been closed

The second theorem rules out uniformly integrable normalized zero-margin
sequences on the exact scalar contact ray. It says nothing by itself
about concentration, changing unbounded transverse affine offsets, or
the four-dimensional affine minimization. The first theorem closes the
triangular gradient class even when its matrices have rank two. No
positive constant for all compatible gradients and all B follows from
these two results. No sharp-J storage transfer is supplied.
