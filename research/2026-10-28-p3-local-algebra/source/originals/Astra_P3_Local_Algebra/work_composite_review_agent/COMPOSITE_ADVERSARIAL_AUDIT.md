# Adversarial audit of the acquired chain-ring counter

This note records an independent audit of the raw chain-ring compiler, the
product counter, chain-algebra acquisition, the field and nilpotent support
decoders, and the chain-ring character-sum backend. Its scope is the stated
restricted family. It does not establish historical priority or generic cubic
counting.

## Result and repaired issue

No counterexample to an accepted exact count or gap in the deterministic
acquisition theorem under its stated transversality condition was found.
The ordinary-ring coefficient fit and split-cubic factor certificate are
essential: an annihilator certificate alone is insufficient, especially for
the nilpotent operator.

One cost mismatch was found and repaired by the main author. The proof
rejected a centroid dimension `m > n` or `m` not dividing `n` before expanding
the multiplication table, while the code initially rejected only later.
The early `require_free` guard is now present. This affected the bound on
rejected inputs, not the correctness of accepted counts.

The deterministic seven-dimensional support condition is relative to the
generator or uniformizer actually acquired. A change to an arbitrary
full-degree field generator need not preserve the same scalar subspace.
The random-error guarantee nevertheless survives acquisition: coordinate
choices depend only on the third tensor, which a quadratic error does not
change. Thus the probability calculation uses an operator independent of
the random error.

## 1. Algebra acquisition and presentation invariance

Let `A = F_(2^d)[t]/(t^e)` and let `lambda(a)` be the field trace of the
coefficient of `t^(e-1)`. The pairing `lambda(ab)` is nondegenerate. A unit
multiple of the three-coordinate volume tensor is radical-free, and its
balanced input-slot centroid is exactly the multiplication algebra of `A`.
Repeated-coordinate arguments force the off-diagonal blocks of a centroid
operator to vanish. Nondegeneracy then gives `L1(x)y = xL2(y)`. Substituting
`1` forces all diagonal operators to be multiplication by the same element.
The algebra is therefore acquired from the raw tensor, not assumed.

The stable Frobenius image is the coefficient field, and the stable kernel
is the nilradical. The single-local-factor and one-dimensional `J/J^2`
checks force the nilradical to be principal by Nakayama. The subsequently
verified power basis and full multiplication table certify the chain ring.
The free-module criterion follows from nilpotent Jordan-block lengths; the
returned coordinate matrix is explicitly invertible. The coefficient-field
generator construction does not enumerate the field.

### Ring automorphisms preserve the ordinary cubic family

Let `sigma` be a ring automorphism. Since `lambda o sigma` is nondegenerate,
there is a unique **unit** `c` such that

\[
\lambda(\sigma(a))=\lambda(ca)\quad(a\in A).
\]

Consequently, with `sigma^{-1}` acting on polynomial coefficients,

\[
\lambda(P(\sigma(X)))=
\lambda\bigl(c\,\sigma^{-1}(P)(X)\bigr).
\]

This preserves ordinary degree, a unit leading coefficient, and splitting
into independent linear forms. Coefficient-field Frobenius and nonlinear
uniformizer changes therefore do not invalidate the acquired family.

The independent program `semilinear_ring_audit.py` tested 16 cases with
`(d,e)` equal to `(3,2)`, `(3,3)`, `(4,3)`, and `(7,2)`, using nontrivial
Frobenius, arbitrary higher terms in the uniformizer image, and triangular
invertible ring-linear coordinate changes. It verified **2,048 pointwise
identities**, all transformed exact counts, and **three complete raw-ANF
acquisitions**. Every exact assertion passed. Data are in
`semilinear_ring_audit_results.json`.

## 2. Ordinary cubic identification and Hensel lifting

The homogeneous ordinary cubic is unique modulo traced ordinary terms of
degree at most two for `d >= 3`. This is not uniqueness from the third binary
difference alone. Scale all ring variables by a coefficient-field element
`rho`. The cubic contributes trace exponent `3`, while lower-degree terms
have exponents `0`, `1`, and `2`. The binary cyclotomic orbit of `3` has
length `d` and is disjoint from the orbit of `1` when `d >= 3`. Thus the top
nilpotent coefficient of the cubic vanishes at every ring input. It is a
formal polynomial of degree three in coefficient variables, and `3 < 2^d`,
so it is zero. Each cubic exponent vector has an odd exponent; a coefficient
variable in an appropriate nilpotent layer isolates every ring coefficient.
This does not extend the current theorem to `d = 1` or `2`.

The fitter includes repeated-variable cubics and cross quadratic monomials.
Traced squares are binary-linear and are absorbed into the linear fit. A
recovered quadratic error need match a planted error only in its polar
form; the affine difference is absorbed exactly.

The factor lift is correctly gauge-fixed. After residue splitting, the
cubic is a unit times `XYZ`. At each nilpotent layer, the leading-coefficient
correction supplies `XYZ`; six off-diagonal plane corrections supply the
other six nonpure cubic monomials. Pure cubes are obstruction checks.
Normalizing the three diagonal plane coefficients to one makes the lift
unique. The final complete coefficient identity certifies the factorization.

For `lambda(c X^2) = lambda(a X)`, the square adjoint is

\[
a_{e-1-j}=\sqrt{c_{e-1-2j}},\qquad
0\le j\le\lfloor(e-1)/2\rfloor,
\]

with other coefficients zero. The implementation correctly uses this
layerwise expression rather than a field-only square-root rule.

## 3. Field-generator support acquisition

Let `G` be the trace Gram matrix, `L = G^{-1}B`, and let the selfadjoint error
operator be `E = U K U*`, with nonsingular alternating `K`. For a degree-`d`
generator `z`, `d >= 7`, set

\[
p=z+z^2,\quad q=z+z^3,\quad
C=\langle1,z^4,p,q\rangle_{\mathbb F_2},\quad S=C+pC.
\]

Then `S = <1,z,...,z^6>` and `C intersect pC = <p>`. Define

\[
\mathcal H(L)=L M_{z^4}+M_{z^4}L+M_p L M_q+M_q L M_p.
\]

The scalar identity is

\[
\begin{split}
P(X,Y)&=(X+Y)(X^2+Y)(X+Y^2)\\
&=X^4+Y^4+(X+X^2)(Y+Y^3)+(X+X^3)(Y+Y^2).
\end{split}
\]

It kills exactly the Frobenius offsets `0,+1,-1` for a full-degree generator.
For the error,

\[
\mathcal H(E)=V(J_4\otimes K)V^*,\qquad
V=[U,z^4U,pU,qU],
\]

where `J4` swaps the first pair and last pair of coefficient blocks. Under
`dim(SU)=7r`, `V` has full column rank, so `W = im H = CU`. Hence

\[
U=p^{-1}(W\cap pW).
\]

Expanding `H` in columns `[U,z^4U,pU,qU]`, the **second** row block is `KU*`.
Multiplying it by `U` recovers `E`; the code's zero-based block index `1` is
correct. Alternation, rank, annihilation, and ordinary membership checks
then certify the output.

For iid uniform support columns, each nonzero tuple in `S^r` defines a
uniform ambient vector because some scalar is invertible. The union bound
is less than `2^(7r-n)`. Full-rank conditioning costs at most a factor two
for `r <= n-1`. Uniform full-rank `U` with fixed nonsingular alternating `K`
induces a uniform rank-`r` alternating error by congruence transitivity.
No independent-subspaces hypothesis is used.

## 4. Nilpotent extension: independent derivation

Use the ring Frobenius pairing on `A^b` and `N=M_t`, with `e >= 7`. Replace
`z` by `N` in the preceding operator. Its scalar operators are selfadjoint,
and

\[
C=\langle I,N^4,N+N^2,N+N^3\rangle,\quad
S=C+(N+N^2)C=\langle I,N,\ldots,N^6\rangle.
\]

The square map `F(x)=x^2` satisfies `FN=N^2F`; adjunction gives
`NF*=F*N^2`. Multipliers commute with `N`. Thus `P(N_left,N_right)` kills
multipliers, `M_a F`, and `F* M_a`, which include all blocks arising from
ordinary quadratics and repeated-variable cubics. This is an inclusion in
the kernel, not an identification of the whole kernel with the base family.

Under `dim(SU)=7r`, write `c=N+N^2`. The operator `c` is not invertible on
the whole module, but it is injective on `CU`: `cC` has dimension four and
lies in `S`. Therefore

\[
U=\{w\in W:cw\in W\},\qquad W=CU.
\]

Indeed `W intersect cW = cU`, and injectivity of `c` on `W` identifies the
restricted preimage. The code solves within the independent columns `cW`
and does not invert `c` globally. Its reversal of the nilpotent index in the
Gram conversion and its second-block readout are correct.

### Probability with noninvertible scalars

Let `n=bde`. A nonzero tuple `(s1,...,sr)` in `S^r` has minimum valuation
`v` between zero and six. There are

\[
2^{(7-v)r}-2^{(6-v)r}
\]

such tuples of valuation `v`. For iid uniform `u_j`, the sum `sum s_j u_j`
is uniform on `t^v A^b`, of binary dimension `n-bdv`. Thus the iid failure
probability is at most

\[
\boxed{\sum_{v=0}^{6}
 (2^{(7-v)r}-2^{(6-v)r})\,2^{-n+bdv}.}
\]

Full-rank conditioning again costs at most two in the small-rank regime.
For `r>bd`, a simpler bound before conditioning is

\[
\frac{2^{7r-n}}{1-2^{bd-r}}.
\]

For fixed `d`, `b=3`, and increasing `e`, generic ranks `r=o(n)` have failure
tending to zero, even when `r` exceeds the residue-field degree. For bounded
`r`, the exact finite sum directly tends to zero. The code records that
exact rational bound.

This audit read the nilpotent implementation and its author's executed
evidence without duplicating the suite. The preserved rank-two error in
the annihilator kernel is a decisive example requiring the subsequent
ordinary-ring fitter. That gate must remain mandatory.

## 5. Exact summation, costs, and space

The local character-sum reduction and stationary-phase equations check out.
After balancing and translating, summing the third coordinate imposes
`xy=c` by character orthogonality. Partitioning `x` by valuation gives the
implemented powers of `q` and conductor reductions. For unit sums the deep
ideal linearization has `U=1+u/a^2`, `V=u/a^3`, with constraints

\[
U_i+\sqrt{V_{2i-e+1}}=0.
\]

The recursive even equations determine the required center coefficients;
the remaining equations are tested. In the one-layer residual case, the
trace of a field cubic is a binary quadratic form, so the exact Gaussian
sum is valid. The backend does not use approximate stationary phase.

The Walsh loop streams `2^r` selectors without retaining a leaf array.
The numerator uses `O(n+r)` bits and its denominator is `2^(r/2)`. Ring
coefficients have `ed` bits. Acquisition, fitting, factor lifting, ring
arithmetic, and the finite Dwork residue backend are polynomial in their
explicit bit lengths. The masked machine-integer path is valid modulo its
power-of-two precision, which divides the wraparound modulus; the other
path uses arbitrary-precision integers. Neither enumerates the field.
These facts support `2^r poly(n,L)` bit complexity and polynomial space
for the certified family.

The product counter retains cross-component error terms in one global
defect and performs one global Walsh reconstruction. Its allocation of the
constant to one component agrees with the product identity.

## 6. Focused primary-source comparison

The check found related established machinery, not an equivalent compiler.
This does not establish novelty by absence of a search hit.

- Alain Couvreur, *Improved decoding of Gabidulin codes with symmetric
  errors*, [arXiv:2212.08713](https://arxiv.org/pdf/2212.08713), Theorem 5:
  its transpose-cancellation decoder requires trivial intersection of the
  code and the symmetric space. Here both base and error are selfadjoint,
  making that particular cancellation zero. This distinguishes the stated
  theorem, not all possible structured rank decoders.
- Maxime Bombar and Alain Couvreur,
  [arXiv:2112.07322](https://arxiv.org/pdf/2112.07322), gives relevant
  adjoint and right-side decoding ancestry. Classical and interleaved
  rank decoding should remain credited.
- Terry Shue Chien Lau et al., *On the Security and Design of Cryptosystems
  Using Gabidulin-Kronecker Product Codes*,
  [arXiv:2410.06849](https://arxiv.org/pdf/2410.06849), Section 2, uses
  component decoding with selected errors inside the component half-distance
  radius; it notes that the first factor's Moore structure is unused.
- Zhe Sun et al., *Extended Gabidulin-Kronecker Product Codes and Their
  Application to Cryptosystems*,
  [arXiv:2601.12780](https://arxiv.org/pdf/2601.12780), Algorithm 4, Remark 5,
  and Theorem 5, likewise reduce the stated decoder to component extended
  Gabidulin decoding and linear algebra. These algorithms do not supply the
  present recovery for generic dense errors of global rank exceeding the
  field degree. Its broader Theorem 7 radius statement should not be used
  as a stronger constructive decoder without separately checking the proof.

The defensible output is a certified restricted-family compiler, with
manufactured representations, explicit error conditions, arithmetic costs,
and executed evidence. This audit supports neither a generic circuit-counting
claim nor a practical speed advantage over equally informed competitors.
