# Independent substantive review: all-r adapted-Hessian theorem

## Verdict

The stated theorem in ALL_R_ADAPTED_HESSIAN_THEOREM.md passes this
source-bound mathematical and exact-certificate review. I found no
defect in its original-density identity, positivity proof, strictness,
left-QR transfer, compactness reserve or stated Sobolev extension.

The accepted conclusion is the determinant-translated pointwise support
for every k>1/3, every upper-triangular affine mean and every symmetric
H, and its left-SO(2)-adapted scalar-Hessian consequence at every affine
mean. This does NOT establish quasiconvexity for arbitrary compatible
vector gradients, a k-independent positive reserve, variable-reference
support, a practical runtime advantage or historical priority.

Governing theorem SHA256:
d4950595aefd6ecf5e9b299058568c19f1fcfa0a6ffd39353b493ee24478a33a.

The author-supplied replay was read in full and executed without changes.
It passed 1,272 exact gates. A separately written supplement, importing
no constructor or replay code, reconstructed the uncompleted original
density and passed 74 additional binding/closure checks. These are
distinct review operations; I do not call the supplied replay an
independently authored implementation.

## 1. Original density and affine identity

The independent supplement starts with

  8n J=ell(k^2 u^2+v^2+2uv+4kuj-4vj)+4(5k+1)j^2,

not the author's completed-square expression. At
A=[[alpha,beta],[0,delta]] and
X=[[x,2kV],[-mV,y]], it expands J(A+tX), extracts the second,
third and fourth amplitude coefficients, and subtracts the stated
Lambda_k(A)det X. Exact rational cancellation matches the complete
stored affine polynomial, including every mixed alpha/delta/beta term.
This independently binds the certificate to the ORIGINAL J_r.

The scale 8nm is strictly positive on k>1/3. The affine mean order
(alpha,delta,beta) and the off-diagonal signs in X are consistent with
L_k=diag(2k,-m). The variables x,y,V parametrize every real symmetric
H because k and m are nonzero.

## 2. Exact certificate coverage and Sturm logic

I inspected the supplied replay's reconstruction of every leading
minor directly from the stored full affine matrix, using exact rational
polynomial determinant arithmetic. Its coefficient coverage is literal,
not a comparison on sampled parameter or field values.

The declared 128 records contain exactly one unsuccessful historical
record, tail_T1_determinant. It is explicitly excluded. The independent
supplement checked that exclusion, the full frozen manifest, the literal
printed T1/T2 polynomials against their coefficient records, and the
absence of coordinate factors in the forms whose STRICT positivity is
used in the grouped arguments.

For each successful homogeneous binary form, the replay checks only
even removed coordinate powers, the exact reduced polynomial, its
square-free monic Sturm start, derivative, every negative-remainder
recurrence, a nonzero constant endpoint and both infinity variation
counts. Equal variations exclude all real roots; positive leading
coefficient and even degree then give positivity. Homogeneity and the
recorded coordinate factors cover y=0 as well. The separate degree-28
negative cubic discriminant has the required full degree and positive
coefficient at infinity.

The T^2 tail is a genuine positive quadratic in z=ell*x for either sign
of x. The T^1 replacement uses the FOUR coefficients ell^8 through
ell^11, with ell^8 used once, not added again as an individual reserve.
Its cubic has positive leading and constant coefficients for x nonzero
and strictly negative discriminant. Therefore it has exactly one real
root, and that root is negative. This proves positivity on z>=0.
The separately checked original x=0 chart avoids division by x^2.
The failed three-term allocation is not a dependency of this proof.

## 3. Complete diagonal block and strictness

At V=0 the beta mean decouples with strictly positive coefficient for
(x,y) nonzero, since m>|1-k|. The diagonal-mean change

  s=k alpha x-delta y, t=alpha y+delta x

has determinant kx^2+y^2>0. Also
E2=(kx^2+y^2)^2>0. The displayed diagonal metric determinant is positive
by its explicit discriminant reserve; its first diagonal entry has
positive sign at j=0 and cannot cross zero while the determinant stays
positive on the connected punctured (d,j) plane.

The complete diagonal augmented determinant is paid by the explicit
three-square identity in theorem section 3. All its remaining Schur
coefficients have strictly positive ell-polynomial certificates. For
j nonzero the final j^4 square is positive; for j=0,d nonzero the first
square is positive. This proves the full diagonal augmented matrix
positive definite, not just its quadratic top block.

For nonzero (x,y), these positive T=0 minors plus all the nonnegative
positive-T contributions prove strict Sylvester positivity. For x=y=0
and V nonzero, the supplement directly checked that the T^2,T^3,T^5
coefficients of D2,D3,D4 are nonzero polynomials with nonnegative
ell coefficients. They are strictly positive for ell>0; initial zero
coefficients at the excluded endpoint are harmless. All other pure-V
powers vanish, and the displayed D1 coefficient is strictly positive.

Thus every nonzero H gives a positive-definite four-by-four augmented
affine matrix. Its evaluation on (alpha,delta,beta,1) is strictly
positive for every affine mean.

## 4. Quantitative reserve and function-space closure

For fixed k, restrict X to the unit sphere of its adapted three-dimensional
linear space. The positive-definite matrix is continuous there, so its
least eigenvalue has a strictly positive minimum. If X=r X_unit, the
polynomial equals

  r^2 (a,r)^T M(X_unit)(a,r), a=(alpha,delta,beta).

This proves the claimed bound by a positive multiple of
|A|^2|X|^2+|X|^4 after restoring the positive scale. The same reasoning
is uniform on a compact k interval strictly inside the open half-line.
It gives no uniform bound as k approaches 1/3 or infinity.

The density and the translator are invariant under constant left SO(2)
rotation, because their ingredients are column norms and determinant.
Left QR makes every A upper triangular. The A1=0 case is legitimate:
its first column remains zero under any such rotation. No right/source
rotation or fixed mean-independent adapted matrix is assumed.

On a periodic torus, the Hessian has zero average and its determinant
has zero average. Therefore the affine tangent and the CONSTANT affine
translator integrate to zero. Smooth approximation in W^{2,4} passes
all degree-four and lower terms. The quantitative remainder gives
strictness unless the Hessian vanishes almost everywhere. Compactly
supported W^{2,4} scalar potentials can be periodized in a sufficiently
large cell. These conclusions do not control an additional transverse
vector-gradient component or a variable QR/reference field.

## 5. Executions, preserved checker failures and exact scope

The first timing wrapper used /usr/bin/time, which is absent. Both
checker launches stopped before execution with return code 127. The
wrapper failure is preserved. A Python subprocess/resource wrapper then
ran the unchanged supplied replay once:

  1,272 exact gates, return code 0, 6.78588318 s process wall,
  61,836 KiB cumulative child maximum RSS.

My supplement v1 stopped at a syntactic expanded-expression equality:
the rational denominator 3k+1 had not been cancelled. A direct exact
diagnostic showed the difference cancels identically. The preserved v1
also had an unnecessarily strong pure-V positivity criterion at ell=0;
source inspection showed initial zero coefficients at that excluded
endpoint. V2 changes only rational normalization and the correct
positive-half-line criterion. It does not change any theorem, polynomial,
coefficient or certificate input. V2 passed:

  74 checks, return code 0, 2.12168502 s process wall,
  54,880 KiB child maximum RSS.

V1 SHA256:
d4a5477d5666d4ac3c4a2d4acdd53ca55d53359f2a2bd8aa133764301af069c7.
V2 SHA256:
bd9f4d59cd2a52f675283248b971f97178437307be2b9d023306283775180ecb.
Supplied replay SHA256:
f57c3f068493595267d6f8d0ba71cc53e30e06440f55f3d654ec796d45a5e6b9.

Both use the available Python 3.12.14 and SymPy 1.14.0. No floating
optimization, state/parameter sampling, source fitting or scientific
retuning was performed. All failed launch/checker receipts are retained
alongside successful receipts. The governing candidate bytes remained
unchanged and their supplied full manifest passed.

The mathematical review is complete at the stated adapted-Hessian
scope. The original arbitrary-gradient J_r problem remains open in this
work. The next construction must pay its actual mixed/transverse cost,
not infer it from this theorem.
