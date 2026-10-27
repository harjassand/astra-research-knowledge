# Raw smooth stationary compilation beyond three ring coordinates

## Result and exact scope

`rank_five_stationary.py` extends the acquired-chain stationary compiler from three ring coordinates to any fixed module dimension `b`. Its production input is an explicit Boolean ANF `p` of degree at most three on the original `n` independent bits. It is not given a field, chain length, ring coordinates, an affine center, a smoothness certificate, or a decomposition.

The existing centroid acquisition first obtains, and verifies, a free module presentation over

\[
A=\mathbf F_{2^d}[t]/t^e,\qquad n=bed,
\qquad \lambda_e(a)=\operatorname{Tr}([t^{e-1}]a).
\]

It expresses the function exactly as

\[
p(x)=\lambda_e\!\left(\sum_{i<j<k}C_{ijk}X_iX_jX_k\right)+Q(X),
\]

where the coordinate map is binary linear and invertible, and `Q` is an explicitly reconstructed binary quadratic. The new compiler then repeatedly acquires a unique critical residue center and checks every proposed variable elimination. For `e` congruent to zero or two modulo three, accepted instances are counted exactly in polynomial time for each fixed `b`, without enumerating field points, ring points, or Walsh leaves.

This is a certified restricted compiler. Its initial third tensor must be radical-free and its full balanced centroid must be an acquired chain algebra acting freely. Smoothness of an arbitrary ordinary cubic alone does not imply those conditions: a sum of ordinary cubes can be projectively smooth while its binary third tensor is zero. Rejection by the acquisition or subsequent certificates is explicit.

A complete promised family accepted by the compiler is

\[
p(u)=\lambda_e(H(Lu+a))+Q_0((Lu+a)\bmod t^h)+c,
\qquad 3h\le e+1,
\]

where `L` is any hidden binary-linear isomorphism onto `A^b`, `H` is ordinary homogeneous cubic with projectively smooth residue, `Q_0` is any binary quadratic on the quotient, `d>=2`, and the third tensor has the stated chain-centroid property. The error rank can be the largest even integer at most `bdh`, hence linear in `n`. All representation and center data are manufactured from the raw ANF. The full arbitrary quotient-fitting theorem used for rank three is unnecessary here.

For chain length one a supplied exact terminal callback is required. The implementation does not replace that missing capability with implicit enumeration. The polynomial claim established and executed here concerns lengths congruent to zero or two modulo three. An arbitrary binary quadratic terminal must not silently be treated as an ordinary fixed-degree polynomial in `b` field variables.

## 1. Acquiring the highest-digit derivative

At a state of length at least two, add `t^(e-1) a` to ring coordinate `i`. Every squarefree cubic term containing that coordinate becomes affine in `a`; terms involving two highest-digit increments vanish. The quadratic remainder gives an affine binary-linear derivative.

The compiler first checks that the latter derivative depends only on the residue digits of every other coordinate. The nondegenerate field coefficient-trace pairing converts the `d` binary derivative components into an `F_q`-valued function. For each coordinate pair it then solves for coefficients of the map `x -> B_ij x+M_ij x^2`. The two maps `x` and `x^2` are linearly independent over `F_q` exactly when `d>=2`. This explains the field-degree restriction of this implementation.

The resulting exact derivative vector is

\[
g_i(X)=\sum_{\substack{j<k\\i\notin\{j,k\}}}C_{ijk,0}X_jX_k
       +\sum_jM_{ij}X_j^2+\sum_jB_{ij}X_j+c_i.
\]

Here subscripts on a cubic coefficient are sorted, and `0` denotes reduction modulo `t`. The fit is checked on an entire binary basis, so it certifies the complete additive map, not sampled agreement.

The homogeneous part is the gradient of the explicitly manufactured ordinary cubic

\[
H_0(X)=\sum_{i<j<k}C_{ijk,0}X_iX_jX_k
       +\sum_{i,j}M_{ij}X_iX_j^2.
\]

This identity includes `i=j`, since the derivative of `X_i^3` is `X_i^2` in characteristic two.

## 2. The affine center is solved, not searched

A translate of that homogeneous gradient has linear coefficient

\[
B_{ij}=\sum_k C_{ijk,0}a_k,
\]

with coefficients zero for repeated indices. The compiler solves all `b^2` equations for the `b` unknown field coordinates of `a`. It explicitly checks that the contraction matrix has rank `b`. This follows for the promised family from radical-freeness of the residue alternating third tensor; the check makes the algorithm sound independently of that promise.

The recovered center is verified by the exact equations `g_i(a)=0`. These conditions imply

\[
g(a+Y)=\nabla H_0(Y).
\]

There is no search through `q^b` residue vectors. Both the center and its uniqueness certificate are acquired by linear algebra.

## 3. A complete fixed-dimensional smoothness certificate

Let `g_1,...,g_b` be the homogeneous gradient quadrics. Form the Macaulay matrix whose rows are the coefficient vectors of `g_i m`, for every monomial `m` of degree `b-1`, and whose columns are all monomials of degree `b+1`. Its dimensions are

\[
R_b=b\binom{2b-2}{b-1},\qquad
C_b=\binom{2b}{b-1}.
\]

This matrix has full column rank if and only if the quadrics have no nonzero common zero over the algebraic closure.

For one direction, full rank puts every degree-`b+1` monomial in their ideal. At a nonzero common zero, a nonzero coordinate raised to that power would then vanish, a contradiction.

Conversely, no nonzero geometric common zero means the homogeneous ideal has height `b`. In the polynomial ring in `b` variables, these `b` homogeneous generators form a regular sequence. The complete-intersection Hilbert series of their quotient is

\[
\frac{(1-z^2)^b}{(1-z)^b}=(1+z)^b.
\]

Its degree-`b+1` piece is zero, exactly the required surjectivity of the Macaulay map. Extension of the coefficient field does not change matrix rank. Thus the certificate proves uniqueness over the algebraic closure, and in particular over the actual residue field.

For `b=5` this is a `350 by 210` matrix of rank `210`. For `b=3` it reduces to the earlier `18 by 15` matrix. The dependence on `b` is exponential through these binomial dimensions; this is a polynomial theorem for fixed `b`, not a uniform polynomial bound when the module rank is unbounded.

## 4. Exact restriction and arithmetic reconstruction

Summing each highest-digit direction annihilates every residue class with `g_i(X_0)!=0`. The certified unique surviving residue class is `X_0=a`. Hence the original sum equals its restriction to

\[
X=a+tY.
\]

No multiplicity is introduced by this restriction: the sum over the surviving full residue fiber already includes its highest digits.

When `e` is two or three, the restricted cubic third tensor vanishes because its cubic term is divisible by `t^3`. The entire restricted phase is consequently binary quadratic in `bd(e-1)` bits. Its constant, unary, and pair coefficients are recovered exactly from evaluations at zero, basis vectors, and pairs. Binary Gaussian elimination gives its signed sum.

When `e>=4`, subtract the canonical squarefree cubic with coefficients `C_ijk mod t^(e-3)` in the first `d(e-3)` bits of each `Y` coordinate. The difference is exactly binary quadratic: the canonical third tensors cancel algebraically, including under the affine translation. Recover all its quadratic coefficients. The implementation then checks that every monomial using either of the two proposed discarded high layers is zero.

Only after this check does it drop the layers, multiply by

\[
q^{2b}=2^{2bd},
\]

and recur with length `e-3`. The check is not inferred from numerical agreement or a promise of easy decomposition. For the promised homogeneous-plus-low-quotient family it always succeeds: substitution `X=a+tY` reduces the quotient height by one, and `3h<=e+1` is preserved by `e -> e-3`.

All integer counts have at most `n+1` bits. The Boolean zero count is reconstructed as `(2^n+S)/2`. The new compiler never introduces independent internal witness variables.

## 5. A smooth rank-five family with acquired centroid exactly A

Write the five coordinates as `X1,Y1,X2,Y2,Z`. For nonzero coefficients `a_i,b_i`, put

\[
H=Z^3+Z(X_1Y_1+X_2Y_2)
 +a_1X_1^2Y_1+b_1X_1Y_1^2
 +a_2X_2^2Y_2+b_2X_2Y_2^2.
\]

Let `c_i=(a_i b_i)^(-1)`. At a critical point with `Z=0`, the `X_i,Y_i` derivative equations force every coordinate to be zero. Otherwise normalize `Z=1`. All critical possibilities, even over the algebraic closure, satisfy `X_i in {0,a_i^(-1)}`, `Y_i in {0,b_i^(-1)}`. The final derivative is

\[
1+\epsilon_1c_1+\epsilon_2c_2.
\]

It never vanishes when `{1,c_1,c_2}` are binary independent. The F8 fixtures use `a_1=a_2=1`, `c_1=alpha`, `c_2=alpha^2`. The F4 fixture uses `c_1=c_2=alpha notin F2`; the possible subset sums are only zero and `alpha`, so it is also smooth.

In fact the latter construction works for every fixed odd `b=2k+1>=5` and every `d>=2`: take

\[
H=Z^3+Z\sum_{i=1}^kX_iY_i
 +\sum_{i=1}^k(X_i^2Y_i+\alpha^{-1}X_iY_i^2),
\qquad \alpha\notin\mathbf F_2.
\]

The last derivative is `1+alpha sum_i epsilon_i`, which cannot vanish. This supplies a nonempty family across fixed module dimensions; it is an algebraic proof, not an assertion that all those dimensions have been executed.

The alternating third form of the rank-five residue is `T=Z wedge omega`, with `omega` a nonsingular symplectic form on the other four coordinates. It has zero radical. Its field centroid is precisely the scalars: write an operator in blocks as `EZ=aZ+u` and `Ew=ell(w)Z+Bw`. Balancing repeated `Z` slots gives `u=0`. Balancing three vectors in the four-dimensional symplectic space gives `ell=0`. Finally, balancing `(Z,w,v)` gives `omega(Bw,v)=a omega(w,v)`, hence `B=aI`.

This conclusion also survives arbitrary higher nilpotent coefficients in all mixed cubic monomials; the tests include those deformations. Here is the full binary-centroid argument, so no linearity is assumed for free. Scalar multiplication by `A` is contained in the balanced centroid of the transferred form `lambda_e T`. A radical-free balanced trilinear form has commutative centroid: moving two centroid operators successively between its three slots shows their commutator lies in the radical. Thus every binary centroid operator commutes with `A` and is automatically `A`-linear. The nondegenerate coefficient-trace pairing turns binary balancing into `A`-valued balancing.

Reduce such an operator modulo `t`. The residue centroid just proved scalar, so subtract a scalar lift. The difference is divisible by `t`. Divide it by `t` and reduce again: its leading coefficient must again be scalar. Inducting through the `t`-adic layers shows the original operator is scalar multiplication by an element of `A`. Therefore the full binary centroid is exactly `A`, including after the nilpotent mixed-coefficient deformations. The acquired centroid dimension `ed` in the raw executions verifies this conclusion on the concrete inputs.

For completeness, radical-freeness itself survives these ring deformations. If a vector has first nonzero layer `t^j v_0`, choose two residue vectors with `T_0(v_0,u_0,w_0)!=0`. Multiplying one of them by a suitable scalar times `t^(e-1-j)` makes its binary coefficient trace nonzero. Thus no nonzero ring vector can lie in the binary radical.

Finally, the acceptance claim does not depend on recovering the planted coordinates. Two free presentations of the same acquired centroid differ by an algebra isomorphism and an invertible semilinear module map. These preserve every ideal `t^h A`. Transporting a nondegenerate coefficient functional changes the standard functional by multiplication by a unit, using the Frobenius pairing. Ordinary homogeneous degree, residue smoothness, and the stated quotient-height condition all survive these operations. Consequently the acquired presentation belongs to the same admissible family, even when its coordinates and coefficients differ from the planted ones.

## 6. Description size and charged computation

Let `L` be the bit length of the explicit input ANF and `n` its independent-input count. A dense Boolean cubic has `1+n+binom(n,2)+binom(n,3)` coefficient bits. A sparse list uses at most three variable indices per monomial, plus its encoding overhead. No coordinate matrix is part of the input.

The centroid has `n^2` unknown bits and `O(n^3)` linear equations. The existing acquisition proof and executable charge `O(n^7+L n^4)` conservative bit time, including an optional full third-coefficient audit, and `O(n^4)` bits of elimination storage. Ring-action and multiplication certificates are checked, rather than inferred from algebra dimension. See the accompanying `CHAIN_ALGEBRA_ACQUISITION.md` in `work_local_algebra_agent/` for those separately established steps.

The acquired scalar representation uses `O(n^2+ed binom(b,3))` bits, the modulus and length, and an `n^2`-bit coordinate map. At a stationary stage the coefficient-trace inversions, `x,x^2` map fitting, center solve, and binary quadratic reconstruction all have polynomial cost in `n`. The Macaulay calculation uses the explicit `R_b by C_b` matrix above, with polynomial-bit arithmetic over the degree-`d` field. There are at most `ceil(e/3)` stages. A conservative combined bound remains `O_b(n^7+L n^4)` bit time for each fixed `b`; its constant is not uniform polynomial in `b` because of the Macaulay dimensions. Storing the stage certificate uses only polynomial space. Powers of `q` are shifts of integers of at most `n+1` bits.

This specifies the input size, independent bits, representation-acquisition cost, and reconstruction arithmetic separately. It is not a circuit-to-CNF corollary. It also does not show that arbitrary programs, circuits, or binary cubics have an admissible chain centroid or smooth acquired gradient.

## 7. Executed evidence

The production API is:

```python
compile_fixed_rank_stationary(poly, n, *, field_terminal=None)
```

The lower-level API, useful after acquisition, is:

```python
stationary_fixed_rank_state(h, e, cubic, Q, b, *, field_terminal=None)
```

`cubic` maps ordered triples of distinct ring-coordinate indices to packed ring coefficients; `Q` is its explicit binary quadratic remainder. The field-terminal callback, if provided, receives `(h,b,cubic,Q)` and is charged separately.

Executed raw cases, all with full binary affine disguises, random higher nilpotent coefficients in every ordinary cubic monomial, and dense maximum-rank quotient noise:

| Original bits | Field degree | Ring length | Acquired module rank | Acquired centroid dimension | Quotient noise rank | Signed sum | Zero count |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 20 | 2 | 2 | 5 | 4 | 10 | -1024 | 523776 |
| 30 | 3 | 2 | 5 | 6 | 14 | 32768 | 536887296 |
| 45 | 3 | 3 | 5 | 9 | 14 | -1073741824 | 17591649173504 |
| 75 | 3 | 5 | 5 | 15 | 30 | -35184372088832 | 18889465913886394810368 |

The 20-bit result was checked against all `1,048,576` raw assignments using a separate NumPy Boolean Möbius transform. This directly checks the `d=2` feature fit and the final count. The larger raw cases agree with the independently specified homogeneous smooth-recursion identity and each passed 1024 additional pointwise checks of the manufactured representation. Every stage has Macaulay rank `210`; the 75-bit case acquires both stages `5 -> 2`, verifies all discarded-layer coefficients, and applies factor `2^30`.

A separate coefficient-state check at 120 bits, length eight and noise rank 44, passed the three stages `8 -> 5 -> 2`, including arbitrary nonconstant affine translation. This validates deeper recurrence but is explicitly not a raw-acquisition example.

Three decisive rejection checks also passed:

1. A highest-digit linear perturbation whose manufactured center is not critical is rejected.
2. A lower linear perturbation that survives in a proposed discarded high layer is rejected by its exact coefficient test.
3. Removing the `Z^3` term creates a projectively singular residue and is rejected by the deficient Macaulay rank.

Files retaining actual inputs, code, and exact certificate data:

- `rank_five_stationary.py`
- `rank_five_recursive_checks.py`
- `rank_five_f4_check.py`
- `rank_five_stationary_results.json`
- `rank_five_f4_results.json`
- `rank_five_20_input.json`, `rank_five_30_input.json`, `rank_five_45_input.json`, `rank_five_75_input.json`

The computations establish exactness and acquired admissibility for these examples. No practical speed advantage or historical priority is inferred from their elapsed times. The constituent algebraic ingredients—centroids, finite local-algebra structure, coefficient-trace pairing, stationary phase, complete-intersection Hilbert series, and binary Gaussian elimination—are standard. The extension established here is the complete raw fixed-rank compiler, the acquired center and smoothness tests, and exact checking of the recursive eliminations in this wider family.
