# Quantitative lemmas for robust relative divisor doubling

**Status, 2026-10-29.** Independent mathematical review/extension of `RELATIVE_DOUBLING_ROBUST_DRAFT.md`. The norm, same-sheet zero, exact sheet/infinity bookkeeping, and complex inverse-collar arguments below have explicit proofs. They are not an implementation receipt, a published priority claim, or an accepted full raw-equation fast-forwarding theorem. The finite-precision pipeline must still be assembled and audited end to end.

The operation is a specialization of classical approximate divisor arithmetic, not a new group law. [Couveignes–Edixhoven, Chapter 12, §§12.8–12.9](https://www.math.u-bordeaux.fr/~jcouveig/publi/book.pdf) round an evaluation matrix, choose a normalized exact kernel vector, recover nearby true zeros, and charge error on the analytic torus. Their zero theorem is §5.4.22: it assumes effective coefficient-growth and a lower bound on a local maximum, not favorable interpolation pivots. The explicit hyperelliptic calculations below supply analogous bounds. No modular-curve complexity theorem is silently being applied to this different family.

## 1. Setup and exact divisor bookkeeping

Let `X: y²=F(x)`, with monic rational squarefree `F` of degree `d=2g+2`, all roots real, in `[−M,M]`, separated by `Δ`, where `M≥1`, `0<Δ≤1`. Let `I=∞_++∞_−`. For physical degree-g divisors `D,D0`, relative doubling asks for `E~2D−D0`.

Use the `3g+1` dimensional space

`L(2g I)={A+yB: deg A≤2g, deg B≤g−1}`.

Its sections have zero divisors of degree `4g`, counting zeros at infinity. With `S=2D+ιD0`, a section vanishing at S leaves residual degree-g divisor Rdiv satisfying

`S+Rdiv~2g I`, hence `Rdiv~ιE`.

**The returned physical divisor is `E=ιRdiv`.** Forgetting this final involution reverses the intended operation. These identities use `D+ιD~g I`.

## 2. Explicit algebraic norm bound

Normalize the coefficient max norm of `(A,B)` to 1, and write

`P=A²−FB²`, `D*=4g`, `r=||P||_1`, `L=2M+1`.

Squarefreeness makes P nonzero. Interpolation at `2g+1` branchpoints gives

`||A||_∞≤K_A sqrt(r)`,

`K_A=(2g+1)((1+M)/Δ)^(2g) M^(2g)`.

Indeed `|A(E_j)|²=|P(E_j)|≤r M^(4g)`, and cardinal-polynomial coefficient sums are bounded by `((1+M)/Δ)^(2g)`. Thus

`||A²−P||_1≤K_C r`, `K_C=(2g+1)² K_A²+1`.

On `|z|=L`, every `|z−E_j|≥M+1≥1`, so

`|B(z)|²≤K_C r L^(4g)`.

Cauchy bounds every B coefficient by `sqrt(K_C) L^(2g) sqrt(r)`. Therefore

`||P||_1 ≥ η := min(K_A^−2, K_C^−1 L^−(4g)) >0`.

All logarithms of these constants are polynomial in `g, log M, log(1/Δ)`. The argument permits complex A,B, arbitrary leading-coefficient cancellation, and a singular evaluation matrix. It does not lower-bound any interpolation pivot.

## 3. An elementary same-sheet zero theorem

**Analytic lemma.** Suppose h is holomorphic on the unit disk, `|h|≤U`, and some Taylor coefficient `c_k`, `k≤K`, has `|c_k|≥u>0`. For `0<ρ≤1`,

`|h(0)| < u³ U^−2 (ρ/2)^(3K)`

forces a zero of h within radius ρ.

**Proof.** Otherwise `log(U/|h|)` is nonnegative harmonic on the ρ-disk. Harnack on its half-radius disk gives `|h(z)|≤U^(2/3)|h(0)|^(1/3)`. Cauchy's coefficient estimate then gives

`u≤(2/ρ)^K U^(2/3)|h(0)|^(1/3)`,

a contradiction. Enlarge U slightly if desired to make the harmonic function strictly positive. This proves a zero on the actual local curve chart, not merely on the opposite hyperelliptic sheet.

### Explicit chart constants for all physical inputs

Set `U=2(3g+1)L^(2g)` and retain `D*=4g`. At a physical point P, select one of the following charts; no large atlas needs enumeration.

**Ordinary case.** If x(P) is at least `Δ/64` from every branchpoint, put `s=Δ/512`, `x=x(P)+s z`. For `|z|≤2`, all branch factors remain nonzero, so both `h=A+yB` and `h*=A−yB` are analytic and bounded by U. The polynomial `T(z)=P(x(P)+s z)` satisfies

`||T||_1≥η (s/(1+M))^(D*)`.

This follows by applying the inverse affine substitution to T. Since `T=h h*`, some Taylor coefficient of h through order D* has magnitude at least

`u_ord = η (s/(1+M))^(D*) / [(D*+1)² U]`.

To see this, each h* coefficient is at most U by Cauchy, and each product coefficient is at most `(D*+1)U max_(k≤D*)|h_k|`.

**Branch case.** If x(P) is within `Δ/64` of E, put `s²=Δ/16`,

`x=E+s² z²`, `y=s z sqrt(F_E(E+s²z²))`, `F_E=F/(x−E)`.

Choose the square-root branch and `z0` to represent P; `|z0|≤1/2`. Center with `z=z0+w/2`. On `|w|≤2`, both h and h* are analytic and bounded by U; the other branchpoints stay at distance at least `3Δ/4` in the larger z-disk. The product is a polynomial of degree at most `2D*` in w. Inverting the quadratic substitution followed by centering gives

`||P(E+s²(z0+w/2)²)||_1 ≥ η (s²/(1+M))^(D*) 3^(−2D*)`.

Consequently a coefficient of h through order `2D*` is at least

`u_br = η (s²/(1+M))^(D*) / [3^(2D*) (2D*+1)² U]`.

Use `K=2D*=8g`, `u=min(u_ord,u_br)` in the analytic lemma. This is an explicit residual-to-zero estimate with exponent `3K=24g` and polynomial-log constants, uniformly including band edges. A zero distance `2^−b` therefore requires only

`O(g b + log(U/u)) = poly(g, log M, log(1/Δ), b)`

residual bits. The displayed formulas, rather than compactness, provide the bound.

Local Abel displacement is also bounded explicitly. In the ordinary chart `dx/y=s dz/y`; in the branch chart `dx/y=s dw/sqrt(F_E)`. The factors remain bounded below by powers of Δ. For example the deliberately loose bound

`C_Abel=3 sqrt(g) (M+1)^g (128/Δ)^(g+1)`

bounds the Euclidean norm of the vector of coefficients of the unnormalized forms `x^(k−1)dx/y`, `1≤k≤g`, on the needed local disks. Thus local zero/point displacements imply small direct Abel errors without constructing periods.

## 4. Root, sheet, multiplicity, and infinity bookkeeping

After rounding the evaluation matrix, choose an **exact rational** nullvector, normalize it, and regard its A,B as exact rational polynomials. This is essential: exact rational arithmetic may be used for their algebraic bookkeeping even though their residual at the input points is approximate.

1. Compute `C=gcd(A,B)` exactly, and `A=C A0`, `B=C B0` with coprime A0,B0. If B=0, this convention handles the purely polynomial section separately.
2. Roots of C contribute both hyperelliptic sheets. At a branchpoint a root of multiplicity m contributes local multiplicity 2m at the one ramification point.
3. For `P0=A0²−F B0²`, every finite root ξ obeys `B0(ξ)≠0`: otherwise A0(ξ)=0, contradicting coprimality. Its unique remaining sheet is exactly `y=−A0(ξ)/B0(ξ)`. Generic-root multiplicity in P0 equals local section multiplicity. At a branchpoint, P0 has a simple root because `P0'(E)=−F'(E)B0(E)²≠0`; the local section zero is also simple.
4. A nonzero integer resultant after clearing denominators gives a **derived** lower bound on `|B0(ξ)|`. If degrees are O(g) and coefficient heights have h bits, Cauchy root bounds and the resultant product give `|B0(ξ)|≥2^−poly(g,h)`. Thus evaluating the sheet quotient requires polynomial precision, not an assumed denominator margin. Exact squarefree factorization and algebraic root separation similarly handle arbitrarily close distinct roots; repeated roots are retained with multiplicity.
5. At infinity put `z=1/x`, `H(z)²=z^(2g+2)F(1/z)`, `H(0)=1`. The local section representatives are

   `s_±(z)=z^(2g) A(1/z) ± H(z) z^(g−1) B(1/z)`.

   Their orders at zero are the two infinity multiplicities. Compute their Taylor coefficients exactly over Q through order 4g; neither representative vanishes identically. Their product is `z^(4g)P(1/z)`, so the two orders sum to `4g−deg P`.

The case `gcd(C,F)≠1` is covered by the ramification multiplicity rule. These rules count exactly 4g section zeros. They avoid a numerical decision about whether a tiny B value is zero.

For matching, perturb the 3g prescribed points to separated nearby points. Require residual-zero neighborhoods smaller than one quarter of their separation, then remove one true zero per disjoint neighborhood. If there are multiple candidate zeros in one neighborhood, any one works. Use an inner existence radius and a larger selection radius to avoid exact boundary-equality tests. The inverse signed coordinates

`cosθ=(x−c)/r_gap`, `sinθ=y/[r_gap W(x)]`

have polynomial-log Lipschitz constants on each real oval; therefore angle separation translates quantitatively into curve-point separation even at edges.

## 5. Uniform complex inverse collar and global uniqueness

Let `A(θ)` denote the Abel map in the unnormalized holomorphic basis and signed gap angles. The real derivative is the weighted Vandermonde matrix. Retain the independently checked uniform bound

`||J(θ)^−1||₂≤K := g(2M)^g ((1+M)/Δ)^(g−1)`.

Every signed-angle chart extends holomorphically to complex increments of norm at most

`ρ=Δ/(16M)`.

Indeed `|μ(θ+h)−μ(θ)|≤2M|h|≤Δ/8`; every excluded factor remains at least `Δ/2` away from zero and a consistent square root exists. In this collar one may safely use

`L_H=100 g² (4M/Δ)^(g+2)`

as a bound on the operator norm of the second derivative of the Abel map. This follows directly from `|μ|≤2M`, `|μ'|≤2M`, `|w|≤(2/Δ)^g`, and `|w'|≤4gM|w|/Δ`. The columns depend only on their corresponding θ coordinate.

Set

`r=min(ρ/2, 1/(4K L_H))`, `η_col=r/(2K)`.

For every complex vector v with `||v||≤η_col`, solve

`A(θ+h)−A(θ)=v`

by the contraction `h=J(θ)^−1[v−R(h)]`, where `||R(h)||≤L_H||h||²/2`. On the r-ball the contraction factor is at most 1/4. It produces a unique nearby inverse with

`||h||≤2K||v||`,

and its Abel differential remains nonsingular.

**No period-lattice separation is needed.** If a divisor class is within η_col in direct torus error, by definition there is a representative lift v of that error with `||v||≤η_col`; use that lift in the existence argument. The arithmetic proof can furnish its small lift as a sum of short local integrals, without evaluating a period lattice.

**No distant effective representative can defeat the local inverse.** Nonsingularity of the Abel differential at this degree-g divisor is equivalent to nonspeciality, hence by Riemann–Roch `h⁰(O(D))=1`. Its complete linear system contains only that effective divisor. Therefore any effective degree-g residual divisor with the same Abel class must be precisely this local inverse, globally. This is algebraic uniqueness, not an unquantified compactness argument.

To project a complex nearby divisor to its physical oval, compute

`z=(x−c)/r_gap + i y/[r_gap W(x)] = exp(iθ)`

with the chart's fixed square-root sign, and replace z by `z/|z|`. Its modulus is bounded above and below in the collar. This avoids arccos/square-root singularities at band edges. The Abel error introduced by projection is bounded by the local derivative bound times `||Im θ||`. Gap separation identifies the correct oval uniquely.

## 6. Precision is charged per operation, not composed as Hölder exponents

The exponent O(g) in residual-to-zero conversion does **not** require `g^m` bits after m doublings if the invariant is direct torus error. At each call, the computed coordinates denote an actual nearby curve divisor. Exact group doubling amplifies previous direct error by 2; the new local error adds. Thus

`e_(j+1)≤2e_j+δ`.

Choose every operation's direct error `δ≤ε 2^−m / κ_dec, where log κ_dec is polynomial in the spectral input size`. Its matrix/kernel/root work then needs `poly(g, input_bits, m, log(1/ε))` bits. Output coordinates can be rounded afresh at the fixed working precision and reinterpreted as nearby true curve points. The Hölder cost is paid afresh; it is not multiplied across stages.

This closes the principal mathematical conditioning objections to the **relative arithmetic step**, subject to a complete explicit implementation/bit audit of perturbation, root matching, rounding, and projection. It does not by itself establish acquisition of Toda geometry from raw equations, local continuous-flow initialization, or a comparative advantage over the equally informed classical spectral algorithm.

## Exact bookkeeping receipt

`audit/robust_divisor_bookkeeping.py` and its JSON receipt check four genus-two hostile section cases exactly: B=0 with common branch roots; A=0 with a branch common factor; cancellation producing infinity orders (0,5) and only three finite norm roots; and an ordinary common factor. All count degree eight, preserve ramification multiplicities, and verify the reduced sheet denominator is coprime to the reduced norm polynomial. These are bookkeeping tests only, not an implemented relative-doubling or bit-complexity receipt.
