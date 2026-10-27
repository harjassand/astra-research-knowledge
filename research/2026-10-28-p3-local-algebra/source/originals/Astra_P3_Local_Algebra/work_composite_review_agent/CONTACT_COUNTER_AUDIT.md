# Independent audit of acquired contact cubic counting

## Conclusion and scope

The implementation in `work_chain_root/acquired_contact_counter.py` passes
this independent mathematical audit. Its accepted class has an explicit,
checkable algorithm with running time

\[
2^\kappa\operatorname{poly}(n,L),\qquad
n=bde,\quad 0\leq\kappa\leq b-1,
\]

and polynomial space when the chain length is zero or two modulo three.
Here `b` is allowed to grow, `d` is the acquired residue-field degree,
`e` is the acquired chain length, and `L` is the original description size.
All algebraic operations and integers have polynomial bit cost; the final
signed count has at most `n+1` bits. The full centroid, a free module basis,
the quotient-supported perturbation, the contact hyperplane, and the
binary critical-point kernel are constructed from the raw scalar cubic.
The theorem is restricted to inputs passing these gates. It does not
count arbitrary radical-free cubic tensors in this time.

An additional executed field terminal in `contact_field_terminal.py`
extends the bound, at every chain length, to

\[
(2^\kappa+2^d)\operatorname{poly}(n,L)
\]

with polynomial space. This terminal conditions the acquired contact
coordinate and performs exact Gaussian elimination on the remaining
`(b-1)d` binary variables. It replaces full `2^(bd)` field enumeration.
It is a direct consequence of the acquired contact representation, not a
claim of a new general finite-field point-counting theorem.

## 1. Raw quotient reconstruction

The coefficient and center argument is proved in the companion
`GENERAL_MODULE_QUOTIENT_AUDIT.md`. The implementation agrees with it:

* The squarefree cubic coefficients are frozen from the acquired third
  tensor. All other homogeneous cubic monomials are repeated-variable
  terms and are binary quadratic in characteristic two.
* The fit includes these `b^2` coefficients, cross-pair quadratic
  coefficients, linears, and the constant. Pure squares are redundant
  under the primitive Frobenius trace functional.
* Only binary unary and pair rows outside the chosen quotient are fitted.
* For height `h`, the center is solved **modulo `J^(e-h)`** by the
  contraction map of the squarefree cubic. This precision is essential:
  a fitted cross-pair coefficient can have an arbitrary deep component
  outside the full contraction image.
* Residue radical-freeness gives an invertible `b` by `b` minor of that
  contraction matrix, hence injectivity over every truncated quotient.
* The final binary residual is constructed exactly, its cubic part is
  already certified to cancel, and all remaining terms are checked for
  quotient support. Translating this quadratic to the manufactured center
  preserves the support.

The edge `h=e` is handled correctly by the implementation: the center
system has zero columns and zero target, and the zero lift is admissible.
It does not instantiate a length-zero chain ring. The ordinary coefficient
invisibility lemma and fit completeness require `d>=3`; the counting
backend itself also works in smaller fields.

## 2. Acquiring the contact hyperplane

Write `F=F_(2^d)` and let `C` be the residue alternating third form. The
program computes the kernel of the `F`-linear map

\[
\ell\longmapsto \ell\wedge C\quad\text{in }\Lambda^4(F^b)^*.
\]

It performs this as binary linear algebra and requires kernel dimension
exactly `d`, so the kernel is one field line. A nonzero vector supplies
the covector `ell`; the code normalizes one coordinate and explicitly
builds a basis of `ker ell`, followed by a vector on which `ell=1`.
This is an invertible acquired field-linear chart.

For a nonzero covector, exactness of multiplication by that covector in
the exterior algebra says

\[
\ell\wedge C=0\quad\Longleftrightarrow\quad C=\ell\wedge\omega.
\]

Consequently the transformed residue cubic has no squarefree term wholly
within the transverse coordinates `y`. In the chart `z=ell=1`, the
ordinary gradient is therefore

\[
\nabla f(y)=M y^{[2]}+B y+c.
\]

The code checks this degree pattern directly. It also checks that `B` is
alternating and nonsingular and that `M` is nonsingular. Higher nilpotent
coefficients of the cubic need not be contact forms; they are retained
and used in the exact lifts. Only the residue form is required to pass
the contact tests.

## 3. Why no critical ray is missed

The hyperplane omitted by `z=1` is `z=0`. On it, homogeneity and the absence
of squarefree transverse cubics give

\[
\partial_y H_0(y,0)=M y^{[2]}.
\]

Since `M` is nonsingular, this is zero only when `y=0`, over the algebraic
closure as well as over `F`. Thus the omitted hyperplane contains no
projective critical point. This is the substantive role of the square
coefficient gate; contact structure alone would not suffice.

Within `z=1`, the gradient is an affine binary-linear map. Solving its
`(b-1)d` bit system produces one solution and a binary kernel of dimension
`kappa`. Every gradient zero is enumerated exactly once in `2^kappa`
steps. Euler's identity for degree three in characteristic two gives

\[
H_0=\sum_i X_i\partial_i H_0.
\]

At a transverse critical point with `z=1`, the remaining homogeneous
gradient coordinate equals `f(y)`. Therefore the additional test
`f(y)=0` selects exactly the projective singular rays.

### Elementary proof that `kappa <= b-1`

Put `m=b-1` and `T=M^{-1}B`, which is invertible. Kernel vectors satisfy
`u^[2]=T u`. Suppose binary-independent kernel vectors were field-dependent.
Choose a dependence of minimum support, normalize its first coefficient
to one, square the relation, and multiply by `T^{-1}`. Subtract the
original relation. The resulting dependence has its first coefficient
zero. Minimality forces every other coefficient `a` to satisfy `a^2=a`.
All coefficients were therefore binary, contradicting binary independence.
Thus binary-independent kernel vectors are also field-independent and
there can be at most `m` of them. This avoids any unstated effective
Bézout computation in the complexity argument.

## 4. Exact lifting and Gaussian factors

The ordinary transverse Hessian reduces to the same nonsingular `B` at
every residue point. Layer-by-layer Hensel lifting therefore constructs
the unique full-ring transverse critical point above each accepted
residue point. `lift_contact_ray` uses the inverse columns of `B` and
checks the entire final gradient identity.

The formal degree-two Taylor coefficient routine is correct. Its test
`beta & ~alpha == 0` is Lucas's criterion for an odd binomial coefficient;
the coefficient is then multiplied by the remaining power of the center.
In particular, the routine distinguishes ordinary squares from binary
linear terms and does not mistakenly discard the translated quadratic
part of a cube.

With `m=b-1` even, the exact local contribution above a fixed unit radial
coordinate `r` is

\[
q^{me/2}\epsilon^{e\bmod2}
(-1)^{\lambda(c r^3)+Q(r v)},
\]

where `v` is the lifted ray, `c` is its critical value, and `epsilon` is
the sign of the nonsingular residue quadratic Gaussian. The proof uses
successive highest-digit orthogonality, not a characteristic-two Morse
lemma. Cubic transverse terms vanish at the needed stage. Quotient
weights of height at most `floor(e/2)` are constant on the surviving
transverse cosets and can be evaluated at `r v`.

The factor is an integer because `m` is even. The implementation computes
it as `2^(d*m*e/2)`. Multiplying the residue quadratic by a unit radial
cube does not alter its Arf sign: after symplectic normalization, each
two-coordinate contribution depends on a ratio unchanged by that common
scaling.

The radial phase is binary quadratic in the `de` coordinates of `r`,
because cubing is a product of a linear Frobenius map and the identity.
The unit sum is therefore one Gaussian over all `r` minus one over `tA`.
The imported radial routine accepts any ray-vector length; it does not
retain a ternary restriction.

The origin contributes `q^(2b)` times the depth-`e-3` count. At depths two
and three it contributes respectively `q^b` and `q^(2b)`, multiplied by
the constant quotient phase. The imported quotient-restriction routine
also handles arbitrary module rank. The initial height condition
`3h<=e+1` guarantees the half-height condition at every stage.

## 5. Complexity and coordinate invariance

All origin states are retained in a polynomial-size list, and each of
the at most `2^kappa` candidates is processed across that list. Only eight
sample rays are saved. There is no exponentially large table of rays.
All Gaussian, Hensel, polynomial substitution, and reconstruction
operations have polynomial bit cost in `n` and the explicit description.
Integers throughout the counter need only polynomially many bits.

The class is stable under the acquired coordinate ambiguity. A ring
automorphism preserves every power of the maximal ideal and induces a
field automorphism on the residue. A change of primitive Frobenius
functional multiplies the ordinary polynomial by a unit. A free-module
coordinate change induces an invertible residue linear transformation.
These operations preserve the contact covector line and the
nondegeneracy of its transverse alternating form. The restriction to the
contact hyperplane changes the square matrix by invertible left and
Frobenius-twisted right factors, preserving its nonsingularity. Changes
of affine chart induce invertible binary-linear maps on the homogeneous
gradient kernel, preserving `kappa`.

Within the certified height range, `e-h>=1`, so any ambiguity in the
fitted cubic coefficients and center lies in the maximal ideal and
does not change this residue geometry. Hence the raw promise survives
the noncanonical acquired field generator, uniformizer, and module
basis. The exact final identity check remains the soundness certificate.

The earlier obstruction `X1*(X2*X3+X4*X5)` has a positive-dimensional
degenerate critical locus despite a radical-free third form and full
scalar centroid. It is correctly rejected here by the nonsingularity
test on `M`. Its 82 singular points over `F_8` do not contradict this
contact theorem with all its gates.

## 6. Executed field-terminal improvement

The acquired chart writes the field polynomial as `H(y,z)` with no
squarefree transverse cubic. For each fixed `z`, every remaining
ordinary cubic in `y` has a repeated variable. Squaring is binary linear,
so `Tr H(y,z)` is a binary quadratic on `(b-1)d` bits. Therefore

\[
\sum_{x\in F^b}(-1)^{\operatorname{Tr}H(x)}
=\sum_{z\in F}\operatorname{GaussianSum}_{y\in F^{b-1}}
 (-1)^{\operatorname{Tr}H(y,z)}.
\]

The supplied implementation enumerates exactly `2^d` contact values,
constructs each quadratic from its constant, unary, and pair values,
and computes its exact Gaussian. It streams the slices and records
only eight samples. The dehomogenized chart polynomial determines the
homogeneous polynomial uniquely, since a transverse exponent `alpha`
has last exponent `3-sum(alpha)`.

Use it with the unchanged parent API:

```python
from contact_field_terminal import contact_field_sum
signed, certificate = weighted_contact_sum(
    h, e, H, Q, b, terminal_bit_budget=0,
    field_terminal=contact_field_sum,
)
```

`contact_field_terminal_results.json` records six fully exhausted field
checks at `(b,d)=(5,1),(5,2),(5,3),(5,4),(7,2),(7,3)`, totaling 3,195,936
field assignments. The polynomials were subjected to arbitrary acquired
field-linear disguises. Four chain integrations exercised depths four
and seven, with zero enumeration budget in the parent counter. Two
20-bit chain instances were also checked against their entire binary
truth tables; one has actual critical rays. All exact assertions passed.
The two larger chain integrations compare against an independently
exhausted field leaf, not against an exhaustive truth table of their
whole 60-bit or 147-bit chain domain.

These tests establish implementation agreement on the stated examples.
They do not establish a practical speed advantage over equally informed
competitors. General point-counting polynomial bounds for a fixed number
of variables must not be described as polynomial uniformly in this
growing module rank.
