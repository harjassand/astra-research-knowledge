# Audit of the nonsmooth homogeneous chain-ring counter

The formulas in `work_stationary_prior_agent/homogeneous_chain_counter.py`
are correct under the stated ordinary-homogeneous-cubic and unit-`XYZ`
hypotheses. In particular, the characteristic-two square terms do not
invalidate the transverse sign. The following proof avoids a formal Morse
lemma entirely and derives the sum by exact digit elimination.

## 1. Projective coverage and acquisition of the rays

Let `A_e=F_q[t]/(t^e)`, `q=2^d`, and let `lambda_e` be the field trace of
the coefficient of `t^(e-1)`. Let `H` be an ordinary homogeneous ternary
cubic whose mixed coefficient `mu` is a unit.

Partition nonzero residue vectors according to their largest nonzero
coordinate. On the corresponding chart, write the vector as

\[
(X_1,X_2,X_3)=r\,(x,y,1)
\]

after permuting coordinates, with `r` a unit. The transverse residues obey
the chart's fixed zero conditions; every projective residue point and every
ring vector with nonzero residue occurs exactly once. The implementation's
test that all coordinate indices above `chart` vanish gives precisely this
partition.

The dehomogenized polynomial `h(x,y)` has constant Hessian

\[
\begin{pmatrix}0&\mu\\\mu&0\end{pmatrix}.
\]

Its gradient is affine over `F_2`: each component is a combination of
`1,x,y,x^2,y^2`. Thus its residue critical points are found by one binary
linear solve and a kernel computation, not by enumerating the field.

There are at most four critical points in an affine chart over the algebraic
closure. One can see this directly for equations

\[
a x^2+b y^2+\mu y+c=0,\qquad
d x^2+f y^2+\mu x+g=0.
\]

If `f=0`, the second equation has at most two choices of `x`, and the first
at most two choices of `y`. If `f!=0`, substitute its expression for `y^2`
into the first equation, solve for `y`, and substitute back. The result is
a degree-at-most-four polynomial in `x` with nonzero linear coefficient
`mu`. Hence the rational solution space has at most four elements, and an
affine binary solve has kernel dimension at most two. This justifies the
constant-size enumeration in the code.

Retain only critical points where `h_0=0`. These are the projective singular
points of `H_0`, by Euler's identity with `3=1` in characteristic two.
There are at most three such points. Indeed `mu_0!=0` excludes a repeated
component: a nonreduced homogeneous cubic over the algebraic closure would
be `L^2 M`, which has zero `XYZ` coefficient. A line joining two singular
points must divide the cubic, because its restriction has two double zeros.
Three collinear singular points would force that line to be repeated. Thus
three singular points determine the three distinct line factors of a
triangle, and there cannot be a fourth. This gives an elementary bound of
three without requiring a supplied factorization.

For `e>=2`, transverse noncritical residue classes cancel by summing highest
digits. Transverse critical classes with `h_0!=0` cancel in the subsequent
unit radial sum. Therefore the retained singular rays cover every possibly
nonzero nonorigin contribution.

## 2. Unique critical lifting

For each retained residue point, solve `grad h(a)=0` through depth `e`.
Suppose a solution is correct modulo `t^k`, `k>=1`. Changing it by
`t^k(delta_x,delta_y)` changes its next gradient digit by

\[
\mu_0(\delta_y,\delta_x).
\]

The square terms enter at valuation at least `2k>=k+1`, so they do not
affect this correction. The invertible Hessian gives exactly one correction
per layer. The code uses `mu_0^{-1}` and the swapped gradient residual,
which is the correct update.

The full lift reduces to the unique lift at every smaller depth. It is
therefore valid to compute each critical value once at the original depth
and truncate it during the depth-three recurrence.

After translating by the exact critical lift, the chart polynomial is

\[
h(a+(u,v))=c+A u^2+\mu uv+B v^2+C_3(u,v),
\]

where `C_3` is homogeneous cubic. The implemented quadratic coefficients
are the exact characteristic-two Taylor coefficients. In particular the
`u^3` term contributes its coefficient times `a_x` to `A`, and the
`u^2v` term contributes its coefficient times `a_y`; the analogous formula
holds for `B`. The polar coefficient remains exactly `mu`.

## 3. Transverse sum by digit elimination, without Morse theory

Fix a unit radial value `r`, put `rho=r^3`, and sum over `u,v in tA_e`.
The constant contributes `(-1)^lambda_e(rho c)`. Write `u=tU,v=tV`. For
`e>=3`, the remaining sum is `q^2` times the sum at depth `ell=e-2` of

\[
\rho\bigl(q_2(U,V)+tC_3(U,V)\bigr),\qquad
q_2=A U^2+\mu UV+B V^2.
\]

The extra `q^2` comes from the unused last digit of `U` and `V`.

More generally, for `k>=1`, consider a phase at depth `ell` of the form
`rho(q_2+t^k C_3)`. If `ell>=2`, its highest-digit derivatives depend only
on the nonsingular polar form of `q_2`. The cubic is killed by its factor
`t^k`, and pure-square highest-digit changes vanish. Orthogonality therefore
forces `U_0=V_0=0`. Restriction by another factor `t` produces `q^2` times
the same problem at depth `ell-2`, with cubic coefficient `t^(k+1)`.

The terminal at depth zero is one. At depth one, the cubic is absent and

\[
\sum_{U,V\in F_q}(-1)^{\operatorname{Tr}
 (\rho_0(A_0U^2+\mu_0UV+B_0V^2))}
 =q\,(-1)^{\operatorname{Tr}(A_0B_0/\mu_0^2)}.
\]

This follows by replacing the two square terms under the trace with their
linear adjoints and summing one variable. Multiplying all three quadratic
coefficients by `rho_0` cancels from the Arf ratio, so the sign is independent
of the radial unit. Let

\[
\kappa=(-1)^{\operatorname{Tr}(A_0B_0/\mu_0^2)}.
\]

Combining the recurrence gives, for every `e>=2`,

\[
\boxed{
\sum_{u,v\in tA_e}(-1)^{\lambda_e(r^3h(a+(u,v)))}
 =q^e\kappa^{e\bmod2}(-1)^{\lambda_e(r^3c)}.
}
\]

At `e=2`, the restricted quadratic and cubic vanish directly and the
`q^2` points give this same formula. At `e=3`, the preceding field Gaussian
sum gives `q^3 kappa`. No small-depth exception has been omitted.

## 4. Unit radial sum

Define

\[
U_e(c)=\sum_{r\in A_e^\times}(-1)^{\lambda_e(cr^3)}.
\]

For each fixed nonzero residue `r_0`, the cube map bijects the principal
unit coset onto the coset with residue `r_0^3`: its derivative is the unit
`r^2`, or equivalently cubing is an automorphism of the principal-unit
2-group. Therefore the higher digits sum to zero unless
`c in t^(e-1) A_e`. This reasoning does not assume cubing permutes all
nonzero residues, which would fail when `d` is even.

Writing `c=t^(e-1)b`, the exact formula is

\[
\boxed{
U_e(c)=q^{e-1}
 \left(\sum_{s\in F_q}(-1)^{\operatorname{Tr}(bs^3)}-1\right).
}
\]

It includes `c=0`, giving `(q-1)q^(e-1)`. The field phase `Tr(bs^3)` is
binary quadratic, since squaring is binary-linear, so its sum is computed
by exact Gaussian elimination in polynomial time. If `v(c)<=e-2`, the
answer is exactly zero. The implemented mask test and top-coefficient
extraction match these cases.

## 5. Complete recurrence and complexity

For `e>=2`, the nonorigin contribution is

\[
q^e\sum_{P\in\operatorname{Sing}(H_0)(F_q)}
          \kappa_P^{e\bmod2}U_e(c_P).
\]

The origin contribution is `q^3` at depth two, `q^6` at depth three, and

\[
q^6 Z_{e-3}(H\bmod t^{e-3})
\]

at larger depth. There are at most three nonorigin rays, and they are
acquired once rather than recursively branching. The code accumulates
each ray contribution with the current origin multiplier; this is the
correct normalization. The same residue rays and Arf signs apply at each
smaller depth, and critical values are simply truncated.

The chart systems have `2d` binary unknowns, their kernels have dimension
at most two, and each critical lift takes `e-1` ring-digit corrections.
There are at most `ceil(e/3)` depth levels and at most three radial Gaussian
sums per level. All ring coefficients have `ed` bits and output counts have
`O(ed)` bits. Hence these parts have polynomial bit time and space without
enumerating the field or the ring. The depth-one terminal retains exactly
the explicitly stated finite-field-backend boundary; a known fixed-degree
point counter supplies a uniform polynomial theorem, while the current
default implementation budgets explicit enumeration.

This proves the nonsmooth extension for an acquired ordinary homogeneous
ternary cubic with unit mixed coefficient. It does not automatically cover
an arbitrary binary quotient perturbation: such a perturbation may vary
along a nonzero ray and must not be omitted from these sums.

## 6. Executed independent checks

`singular_ray_audit.py` and `singular_ray_audit_results.json` preserve:

- **32 transverse truth tables**, through depth eight, with random square,
  cubic, constant, and unit coefficients. They test the individual fixed-
  radial-unit identity, so cancellation in a full sum cannot hide an
  incorrect Arf sign.
- **31 direct unit radial sums**, including valuations zero, `e-2`, `e-1`,
  and the zero coefficient, for both odd and even residue-field degrees.
- **24 exhaustive projective coverage checks** over fields of sizes four,
  eight, and sixteen. They include split triangles, nonsplit nodal points,
  irreducible nodal examples, smooth cubics, and random coefficients.

Every exact assertion passed. No repeated full-counter suite was needed.
