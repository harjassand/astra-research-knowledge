# Bounded audit: exact prefix-fibre sampler and the (\mathbb F_8) cube

Scope: this checks only the algebraic fibre-sampling operation and the stated
three-bit cube facts in `../FIRST_CONSTRUCTION.md`. It does not validate the
median-label acquisition/error bound or the overall comparison-query theorem.

## Exact fibre calculation

Let (Q:\mathbb F_2^n\to\mathbb F_2^n) be a bijection with coordinate degree
at most two. Let (F=(Q_1,\ldots,Q_t)) be an acquired prefix, let

\[
 B_i(x,v)=Q_i(x+v)+Q_i(x)+Q_i(v)+Q_i(0),\qquad
 L=\bigcap_{i\le t}\operatorname{rad}(B_i),
\]

and write (r=n-\dim L). Choose any linear complement (R\) to (L), so
each (x\) has a unique decomposition (x=Rz+v), with
\(z\in\mathbb F_2^r\), \(v\in L\). For (v\in L\), degree at most two and
\(B_i(Rz,v)=0\) give

\[
 F(Rz+v)=F(Rz)+F(v)+F(0)=F(Rz)+A(v),\quad A(v):=F(v)+F(0).
\]

On (L), every (B_i(v,w)=0); hence (A(v+w)=A(v)+A(w)). Thus (A:L\to
\mathbb F_2^t\) is linear. Set (s=\operatorname{rank}A\). For a desired
prefix (y), a core (z) is feasible iff

\[
 A(v)=y+F(Rz)
\]

is consistent. Each feasible core has exactly (2^{n-r-s}) solutions,
because the solution set is one coset of \(\ker A\). Different cores yield
disjoint inputs by uniqueness of the direct-sum decomposition.

The bijection promise implies every (t\)-bit prefix has exactly
\(2^{n-t}\) preimages: it is the projection of the (2^n) distinct outputs
onto (t) bits. Consequently the number of feasible cores is exactly

\[
 |Z_y|=\frac{2^{n-t}}{2^{n-r-s}}=2^{r+s-t}.
\]

In particular, (r+s\ge t), and **the feasible-core count is a power of two
under the stated bijection promise**. This corrects the construction draft’s
generic note that core choice needs rejection for a non-power-of-two count.
With exact unbiased bits, choose one of the feasible cores using (r+s-t)
bits and choose a uniform kernel element using (n-r-s) further bits. The
result is uniform on the fibre, uses exactly (n-t) random bits (the fibre
size is (2^{n-t})), and needs no rare-prefix rejection. If (t=n), the
fibre has size one and this operation returns the exact inverse.

For implementation, form the stacked polar matrix, find its nullspace and a
complement by binary Gaussian elimination, and row-reduce the matrix of (A).
These are polynomially many bit operations in (n,t) (naively, at most a
polynomial such as (O(tn^3))). For a query prefix, scan the (2^r) core
values and test consistency against the row-reduced (A); worst-case time is
\(O(2^r\operatorname{poly}(n,t))\), with \(r\le b(Q)\). A feasible-core
list can be stored in \(O(r2^r)\) bits. To use polynomial working memory,
draw the \((r+s-t)\)-bit index first and scan in a fixed order until that
indexed feasible core is reached; the promised count is known from (r,s,t).
Then use \(n-r-s\) bits to sample a kernel vector. Polynomial preprocessing
and ANF evaluation costs are additional. These costs presume exact acquired
coordinate polynomials and an unbiased-bit source; they do not include the
cost of acquiring those polynomials.

## Why the promise matters

Without bijectivity, some target prefixes can be infeasible, and the
feasible-core count need not be a power of two. For example, on
\(\mathbb F_2^2\), the non-bijective quadratic map \(F(a,b)=ab\) has a
three-point zero fibre and a one-point one fibre. The equal-size-per-feasible-
core fact remains true for quadratic (F) and a correct common radical, but
the total fibre size and core count are no longer forced to be powers of two;
an exact generic sampler would need different index sampling (or charged
rejection). The direct-sum condition is also essential: using a non-complement
or an incorrectly computed common radical can duplicate or omit inputs.
Degree at most two is load-bearing because it makes the polar expansion exact;
for higher degree, vanishing bilinear polar forms does not imply affine
variation along (L). Finally, (L) must be the common radical of every
acquired prefix coordinate, not just one selected coordinate.

The check therefore supports the bootstrap operation once exact prefix
polynomials are known and the promised permutation class applies. It does
not establish the correctness of the separate noisy/median procedure that
purports to acquire the next coordinate.

## Exact (\mathbb F_8) cube check and scope of the affine claim

Use \(\mathbb F_8=\mathbb F_2[\alpha]/(\alpha^3+\alpha+1)\) and write
\(z=a+b\alpha+c\alpha^2\). Direct multiplication gives

\[
 z^3=(a+b+c+bc)+(b+ab+ac)\alpha +(c+ab)\alpha^2.
\]

The three Boolean coordinate polynomials therefore have quadratic polar
coefficients, in the pair order \((01,02,12)\),

\[
 B_0=(0,0,1),\qquad B_1=(1,1,0),\qquad B_2=(1,0,0).
\]

These rows are linearly independent. Their common radical is zero: (B_0)
forces the second and third coordinates of a radical vector to vanish, and
then (B_2) forces the first coordinate to vanish. So the cube map has joint
polar rank exactly three. Every nonzero output linear combination has
nonzero polar form, and hence cannot be affine (adding a constant does not
change its polar). Input affine changes preserve nonzero-ness of these polar
forms by invertible congruence, while invertible output changes only take
invertible linear combinations. Thus the three-bit cube itself has no
affine output coordinate under any invertible affine input/output
reparametrization, ruling out a complete scalar triangular flag that would
require an affine first coordinate. The map is a permutation because
\(z\mapsto z^3\) permutes the seven nonzero elements of \(\mathbb F_8\)
\((\gcd(3,7)=1)\), and fixes zero.

Scope caveat: the direct product of this cube with identity coordinates has
affine output combinations from those identity coordinates. The correct
claim is that the *three-dimensional residual cube block*, after the
zero-polar/identity directions are exposed, has no affine output combination
and joint polar rank three. Do not state that the entire product map has no
affine output combination. Any triangular-flag exclusion for the whole
product must explicitly allow removal of its affine identity block before
applying the residual obstruction.

## Replay

`fibre_cube_check.py` uses exhaustive enumeration and exact \(\mathbb F_2\)
arithmetic to check a small bijective prefix example, the fibre/core
cardinality identities, the displayed cube coordinate formula and polar
matrices, the cube permutation, and the non-bijective fibre-size warning.
It passes under Python 3’s standard library:

```text
PASS: fibre identities, F8 cube polars, and non-bijection counterexample
```
