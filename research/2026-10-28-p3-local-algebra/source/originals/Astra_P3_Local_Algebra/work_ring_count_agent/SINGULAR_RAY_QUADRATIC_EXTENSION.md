# Exact homogeneous chain-ring cubic sums with arbitrary quotient quadratic weights

This note supplies an independent proof and implementation audit for the singular-ray mechanism developed with the parent construction. It is a coefficient-input evaluator. The parent compiler separately acquires the chain algebra, coordinates, and affine translation from a raw Boolean cubic. No smoothness assumption or bound on the rank of the permitted quadratic weight is used here.

## 1. Statement, encoding, and scope

Let `F = F_(2^d)` be supplied by an irreducible binary modulus of degree `d`, and let

\[
R_e=F[t]/(t^e),\qquad q=2^d,\qquad
\psi_e(a)=(-1)^{\operatorname{Tr}_{F/\mathbf F_2}([t^{e-1}]a)}.
\]

Let `H(X,Y,Z)` be an ordinary homogeneous cubic with coefficients in `R_e`. Its coefficient `mu` of `XYZ` must be a unit. There are ten cubic coefficients, using at most `10ed` bits. Let `Q` be an arbitrary Boolean quadratic in the `3dh` bits describing `(X,Y,Z) mod t^h`, where

\[
3h\le e+1.
\]

The target is the exact signed sum

\[
S_e(H,Q)=\sum_{X,Y,Z\in R_e}
\psi_e(H(X,Y,Z))(-1)^{Q(X,Y,Z)}.
\]

The independent-input count is `n=3ed`, and the Boolean zero count is `(2^n+S_e)/2`. An explicit coefficient array for `Q` uses `1+3dh+binom(3dh,2)` bits. Sparse index encoding adds logarithmic factors. Its polar rank may be as large as `2 floor(3dh/2)`, which grows linearly in `n`.

For `e = 0 or 2 mod 3`, the algorithm below is deterministic and polynomial in `e,d` and the supplied description size, with no field-point or ring-element enumeration. For `e = 1 mod 3`, it reduces to one ordinary ternary homogeneous cubic sum over `F`; an exact terminal oracle is an explicit additional dependency. Generic fixed-dimensional finite-field point counting supplies a polynomial-time theorem, but this implementation deliberately requires a supplied terminal callback. An implemented Laurent-Dwork backend handles the explicit Hesse family and its linear perturbations; it is not an acquisition of Hesse normal form for arbitrary cubics.

The polynomial claim concerns the acquired coefficient representation. A generic Boolean cubic is not thereby known to have that representation. The raw acquisition, acceptance certificate, and its costs are separate parts of the parent construction.

## 2. Top-digit orthogonality leaves only the origin and singular rays

Assume `e>=2`. Since `h<=floor(e/2)`, the weight does not depend on the highest ring digit. Replacing one coordinate by itself plus `t^(e-1) a`, for `a in F`, changes the phase by the trace of `a` times the corresponding ordinary derivative of `H mod t`. Higher Taylor terms vanish modulo `t^e`. Summing that highest digit therefore annihilates each residue vector at which the residue gradient is nonzero.

Euler's identity has the form `H = X H_X+Y H_Y+Z H_Z`, because `3=1` in characteristic two. Every nonzero residue critical vector consequently lies on a projective singular point of the plane cubic `H mod t=0`.

The unit `XYZ` coefficient guarantees that the residue cubic is reduced over the algebraic closure. Indeed, a repeated factor in a cubic must be a repeated linear factor; a cubic of the form `L^2 M` has no `XYZ` term in characteristic two. A reduced plane cubic has at most three geometric singular points: an irreducible cubic has at most one, an irreducible conic plus a line has at most two intersections, and three distinct lines have at most three pairwise intersections. Only rational singular points contribute residue vectors over `F`.

Thus there are at most three nonzero projective branches, in addition to the origin. These branches are acquired below, not supplied as a decomposition.

## 3. All chart critical centers are acquired by binary linear algebra

Choose the largest index of a nonzero residue coordinate as pivot and normalize that coordinate to one. This gives three disjoint affine charts. In a chart with pivot `Z`, write `f(x,y)=H(x,y,1)`. It has the form

\[
\begin{aligned}
f={}&c_{300}x^3+c_{210}x^2y+c_{120}xy^2+\mu xy
       +c_{201}x^2+c_{102}x\\
   &+c_{030}y^3+c_{021}y^2+c_{012}y+c_{003}.
\end{aligned}
\]

Its derivatives are

\[
f_x=c_{300}x^2+c_{120}y^2+\mu y+c_{102},\qquad
f_y=c_{210}x^2+c_{030}y^2+\mu x+c_{012}.
\]

Squaring in `R_e` is binary linear. Hence `(f_x,f_y)=0` is an affine linear system in exactly `2ed` binary unknowns. The code evaluates its zero offset and basis columns, then solves that system.

The ordinary Jacobian is the constant invertible matrix

\[
\begin{pmatrix}0&\mu\\\mu&0\end{pmatrix}.
\]

Each residue solution therefore has a unique lift to `R_e`, by successive-digit Hensel lifting. Over the algebraic closure, the two degree-at-most-two equations have finitely many, at most four, solutions: the invertible Jacobian excludes a positive-dimensional common component, and Bézout gives the bound four. Consequently, the binary kernel of the full-ring system has dimension at most two. Enumerating its at most four combinations is a constant-size operation, not enumeration of `F`.

For each acquired full-ring center `v=(a,b,1)`, retain it only when `f(a,b) mod t=0` and the residue pivot belongs to this disjoint chart. Across all charts, at most three centers remain. Write

\[
c=f(a,b),\qquad
A=[s^2]f(a+s,b)\bmod t,\qquad
B=[u^2]f(a,b+u)\bmod t,
\]

where the brackets denote Hasse coefficients. Define

\[
\kappa=(-1)^{\operatorname{Tr}(AB/\mu_0^2)}.
\]

These coefficients, the centers, and the critical values are all manufactured from `H`.

## 4. Exact transverse sum with the quadratic weight present

Fix a radial unit `r`. The points on this residue branch are `r(x,y,1)` with `x=a mod t` and `y=b mod t`. The corresponding chart phase is `r^3 f(x,y)`.

Let `m=floor(e/2)`. If `e=2m`, split each transverse coordinate into its residue modulo `t^m` and its last `m` digits. The phase is affine in those last digits. Orthogonality forces the gradient to vanish modulo `t^m`, and the unique lifted center forces `x=a,y=b mod t^m`. At those surviving points the quadratic and cubic Taylor terms have valuation at least `e`, so their phase vanishes. There are `q^(2m)=q^e` free high digits. The weight is constant on these surviving transverse fibers because `h<=m`.

If `e=2m+1`, summing the last `m` digits similarly forces `x=a,y=b mod t^m`. One pair of field digits remains. Its phase is a nonsingular binary quadratic with field expression

\[
\operatorname{Tr}\bigl(r_0^3(Au^2+\mu_0uv+Bv^2)\bigr).
\]

Its exact sum is `q kappa`. To see the sign directly, use the identity `Tr(Au^2)=Tr(sqrt(A)u)`, sum one variable, and substitute its uniquely selected value in the other. The factor `r_0^3` cancels from the invariant `AB/mu_0^2`. The other high digits contribute `q^(2m)`. Again the weight is constant because `h<=m`.

Thus, for either parity of `e`, the complete transverse sum is exactly

\[
q^e\kappa^{e\bmod2}\psi_e(cr^3)(-1)^{Q(rv)}.
\]

This is the point where arbitrary quotient quadratic rank is handled: the weight survives as a function of the radial variable, instead of being expanded into exponentially many Walsh shifts.

## 5. The radial sum is a binary Gaussian sum

Define the binary function on the `ed` bits of `r`

\[
F_v(r)=\operatorname{Tr}([t^{e-1}]cr^3)+Q(rv).
\]

The map `r -> r^2` is binary linear and multiplication is binary bilinear. Therefore `r -> Tr([t^(e-1)]cr^3)` has Boolean degree at most two. Multiplication by each fixed coordinate of `v` is binary linear, so `Q(rv)` is also quadratic. There is no rank assumption on either part.

The required unit sum is

\[
U_v=\sum_{r\in R_e^\times}(-1)^{F_v(r)}
    =\sum_{r\in R_e}(-1)^{F_v(r)}
     -\sum_{s\in R_{e-1}}(-1)^{F_v(ts)}.
\]

Both terms are exact binary quadratic sums. Their coefficients can be recovered from values at zero, single basis vectors, and pairs of basis vectors, then evaluated by Gaussian elimination. The second term uses only `d(e-1)` variables. The branch contribution is

\[
q^e\kappa^{e\bmod2}U_v.
\]

This computes every radial unit at once; no valuation expansion, stationary-center promise, or field sum is hidden in the radial step.

## 6. Origin recursion and preservation of the weight condition

At the origin residue class put `(X,Y,Z)=t(X',Y',Z')`. Homogeneity gives `H(tX',tY',tZ')=t^3 H(X',Y',Z')`.

For `e>=4`, the last two digits of each primed coordinate are unused, hence contribute `q^6`. Truncate `H` to `R_(e-3)` and define `Q_t(X',Y',Z')=Q(tX',tY',tZ')`. The latter depends on at most the first `max(h-1,0)` digits. Thus

\[
S_e(H,Q)=q^6S_{e-3}(H\bmod t^{e-3},Q_t)
 +\sum_{\text{acquired singular rays }v}
 q^e\kappa_v^{e\bmod2}U_v.
\]

For `e=2` or `e=3`, the origin contribution is simply `(-1)^(Q(0)) q^(3(e-1))`, and there is no recursive call. For `e=1`, the allowed weight is constant and only the finite-field terminal remains.

The condition is stable under recursion: `3h<=e+1` implies `3(h-1)<=e-2`. Equivalently, at recursion level `j<h`, the transverse pullout requires `h-j<=floor((e-3j)/2)`, or `2h+j<=e`; its strongest instance is `j=h-1`, precisely `3h<=e+1`. The condition is therefore a proved preservation condition, not an assumption that successive decompositions stay easy.

## 7. Arithmetic and reconstruction costs

Let `w=ed` and let `s_Q` be the number of stored quadratic terms. The output integers have `O(w)` bits. Precompute the binary linear functional for field trace once; even direct basis evaluation costs at most `O(d^4)` bit operations. With naive polynomial-basis field multiplication, one ring multiplication costs `O(e^2 d^2)=O(w^2)` bit operations. Each chart uses `2w` affine-map evaluations and binary elimination on a `2w` square matrix. Each of at most three radial branches reconstructs two quadratic forms using `O(w^2)` phase evaluations, each costing `O(w^2+s_Q)` elementary bit operations when a quadratic is stored as pairs of bit indices.

A direct implementation therefore admits the conservative bound

\[
O\bigl(e(w^4+w^2s_Q)\bigr)
\]

bit operations, up to ordinary indexing logarithms, and polynomial space. Since `s_Q=O(w^2)`, this is `O(e^5 d^4)` up to those logarithms. No arithmetic on numbers of exponential bit length occurs. The integer powers of `q` are shifts of `O(w)`-bit integers.

The prototype uses Python integer masks for ANF monomials and optional recursive evidence records; a conservative bit-accounting bound for that particular representation is one additional factor `O(w)`. The theorem does not rely on native-word operations being constant time. These are upper bounds, not measurements of practical advantage against optimized point-counting or tensor methods.

For a generic depth-one terminal, the Artin-Schreier hypersurface `W^2+W=H(X,Y,Z)` has four variables, degree at most three, and fixed characteristic two. Its number of rational points is `q^3+S_1`. Specializing Proposition 36 of Lauder-Wan, *Counting points on varieties over finite fields of small characteristic* (https://arxiv.org/abs/math/0612147), gives a first-point-count bound of soft-`O(d^19)` bit time and soft-`O(d^12)` bit space. This provides a generic polynomial theorem, but that multivariate engine is not implemented in these files. The Laurent backend has a much smaller fixed-dimensional matrix for its verified explicit family.

## 8. Raw-fit ambiguity audit for the parent compiler

The evaluator itself works for every `d>=1`. The following ambiguity argument for the parent's raw fitting step uses `d>=3`.

Suppose two ordinary degree-at-most-three coefficient descriptions have the same traced Boolean function modulo a function of the first `h` ring digits. For a high translation `v in (t^h R)^3`, subtracting the translated function gives zero for all `X`. Scale `X,v` together by an arbitrary `lambda in F`. The cubic difference contributes the trace orbit of `lambda^3`; degree-one and degree-two terms contribute the trace orbit of `lambda`. For `d>=3`, these cyclotomic orbits are disjoint, and the coefficient map of the cubic orbit has full dimension `d`. Hence the top-ring-coefficient of the cubic difference under that translation is identically zero as an `F`-valued function.

Take a high translation in one coordinate and inspect its term linear in that translation, quadratic in the constant field coordinates of `X`. Since `q>=8`, a degree-at-most-three polynomial is determined by its values. Ordinary differentiation is injective on homogeneous cubics in characteristic two, by Euler's identity. Coefficient isolation consequently forces every cubic-coefficient ambiguity into `t^(e-h) R`. After removing that part, polarizing with one high translation in each of two different coordinates forces every cross-quadratic coefficient ambiguity into the same ideal, by the perfect coefficient-trace pairing.

The parent fixes the full unit `mu XYZ` tensor before this fit. Its fitted other ordinary cubic monomials have Boolean degree at most two. Thus no unexamined cubic term can remain inside the ignored low quotient. Cross-quadratic coefficients read the affine center exactly: `a_X=P_YZ/mu`, `a_Y=P_XZ/mu`, `a_Z=P_XY/mu`. The ambiguity between centers lies in `t^(e-h)R`. Since `e>=2h`, products of two such ambiguities vanish. Translating a homogeneous cubic by that ambiguity changes only a low-quotient function. Therefore every fitting solution yields the same admissible class after translation and exact remainder verification; an arbitrary linear-system solution need not select a special planted representative.

The field-size restriction here is substantive. For `d=2`, the cubic trace orbit can have a coefficient kernel. It must not be removed from the raw-fit completeness theorem merely because the coefficient-input evaluator works over `F_2` and `F_4`.

## 9. Executed independent checks and API

Implementation: `singular_ray_quadratic.py`.

```python
homogeneous_quotient_sum(R, H, Q, depth=None,
                        terminal=None, details=False)
```

`R` is `ChainRing(binary_modulus,e)`. `H` maps exponent triples of total degree three to ring coefficient tuples. `Q` is the ANF set of bit masks, with mask zero representing the constant. The default depth is `floor((e+1)/3)`. Rejected inputs include a nonunit `XYZ` coefficient, nonhomogeneous cubic coefficients, a nonquadratic remainder, or a remainder using a forbidden high digit. A missing generic depth-one callback raises an error; it is never replaced by enumeration or a conjectural value.

Executed evidence:

- `singular_ray_quadratic_results.json`: 44 comparisons against complete Boolean enumeration, including residue fields of sizes 2, 4, and 8, lengths 2, 3, and 5, random ring cubic coefficients, singular and smooth reductions, and dense quotient quadratics.
- The same file contains four independent pure-`XYZ` comparisons at 99, 108, 132, and 144 input bits. Their oracle is the direct identity `S_e(XYZ,0)=q^(2e)+e(q-1)q^(2e-1)`, obtained by counting pairs with product zero.
- `singular_ray_fiber_results.json`: three 30-input-bit examples over `F_4[t]/t^5`, each with a quotient quadratic of polar rank 12. A separate oracle enumerates all 4096 low prefixes and exactly eliminates the remaining 18-variable quadratic in each fiber. The singular-ray algorithm obtains the same signed sums `-786432`, `262144`, and `131072`, giving zero counts `536477696`, `537001984`, and `536936448`. The coefficient arrays, raw ANFs, ray contributions, and oracle histograms are retained.

The independent fiber oracle is an intentionally exponential verification method. Its execution validates the exact counts; it is not presented as a practical performance competitor. The production evaluator performs at most three acquired ray calculations at each ring depth, including on these rank-12 cases.

## 10. Relation to existing machinery and limits

Top-digit orthogonality, local stationary phase, binary quadratic elimination, Hensel lifting, and Dwork point counting are established machinery. This note claims the displayed exact combination and its proved admissibility conditions, not historical priority for those ingredients. Sawin's *The size of wild Kloosterman sums in number fields and function fields* (https://arxiv.org/abs/2209.02170) is relevant primary literature on characteristic-two local exponential sums; no unverified source bound is needed by this proof.

The useful closure proved here is an arbitrary-rank binary quadratic on a sufficiently low nilpotent quotient. Arbitrary quadratic perturbations in all original directions are not covered. Arbitrary parity constraints on the field-product model are also not covered; the separate `PARITY_CONSTRAINT_BOUNDARY.md` gives an exact encoding of general Boolean cubic phases into such constrained instances. Neither a universal raw compression theorem nor a general polynomial-time circuit counter is asserted.

