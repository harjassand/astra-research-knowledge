# Independent audit: canonical cross-Choi ranks of a strict QCA

24 October 2026. Sol audit requested by root. No changes to group A's files,
new workers, numerical fixture, or constants optimization. Primary input:
[Ranard–Walter–Witteveen, Sections 4.1–4.2](https://arxiv.org/html/2012.00741v2),
especially Lemma 4.5 and Proposition 4.7. The proof below does not infer the
rank statement from the von Neumann or Renyi-2 equalities.

**Verdict: the proposed rank identity holds.** Write kappa for the
multiplicative GNVW index; RWW use its logarithm. With their Choi orientation,

```
rank(J_B)/rank(J_A)=kappa^2,
A=L1' R1, B=L1 R1',
L1={−r+1,...,0}, R1={1,...,r}.
```

The needed repair to a too-quick circuit argument is to allow a larger
intermediate window. One cannot simply delete half-chain gates while keeping
the raw rank of a fixed collar unchanged. Normalized support fractions give
the rigorous finite quantity that survives the removal and relocalization.

## 1. Inverse locality and exact collar factorization

Let alpha have strict radius r on the uniform D-dimensional chain, and
tau be its product tracial state. This trace is invariant under alpha.
Its Choi expectations are
`phi(b tensor a')=tau(alpha(b) a^T)`.

The inverse has the same radius. Indeed, if b is supported on X, then for
every one-site a outside the r-neighborhood of X, alpha(a) is disjoint from
b. Thus alpha^−1(b) commutes with all those one-site algebras, placing it
inside the r-neighborhood of X by the tensor-product commutant property.

Put L2={...,-r}, R2={r+1,...}. For local test operators
a1 in L1, a2 in L2, b1 in R1, b2 in R2, strict locality first gives

```
phi(b1 b2 tensor a1' a2')
 =tau(a2) tau(alpha(b1 b2) a1^T),
```

because alpha(b1 b2) has no support in L2. Trace invariance then rewrites
the second factor as `tau(b1 b2 alpha^−1(a1^T))`. Inverse locality places
alpha^−1(a1^T) at sites <=r, so b2 factors out as well. Consequently

```
phi_{L' R}=J_A tensor tau_{L2' R2}.
```

This is full state factorization, not merely vanishing pair correlations.
The same calculation with the two sides exchanged gives

```
phi_{L R'}=J_B tensor tau_{L2 R2'}.
```

Product test operators are dense, so the equalities determine the states on
the full cross algebras. They prove localization in the actual r-collars.

## 2. A finite support fraction, with no infinite-rank subtraction

The first factorization means the cross-half state has finite local density
`h_A=M J_A` relative to the product trace on L'R, where M=D^(2r). Define

```
p_A=tau_cross(supp h_A)=rank(J_A)/M,
p_B=tau_cross(supp h_B)=rank(J_B)/M.
```

When collars are enlarged, each density embeds as h tensor I. Its support
embeds as supp(h) tensor I; the normalized trace of that support is
unchanged. This defines the same p_A,p_B for any collars at least as large
as the QCA radius, and works also with nonuniform finite local dimensions.
There are no infinite Hilbert-space ranks here. The support projection is
itself local: h is a finite-dimensional positive matrix.

Tensoring two QCAs tensors these densities (after choosing common collars),
so p_A and p_B multiply. Therefore

```
I0(alpha)=(1/2) log(p_B/p_A)
```

is tensor additive. The remaining steps establish its circuit and shift
normalizations directly.

## 3. Circuit normalization, including half-circuit removal

Use the Schrodinger circuit implementation U of alpha. In each finite-depth
layer, separate the finitely many gates crossing the cut from gates wholly
in L or R. Move all crossing gates to one end of the product by conjugating
them through the preceding half-chain layers. Conjugation enlarges a finite
support by only a bounded amount. Thus, as automorphisms,

```
U=(H_L tensor H_R) V,
```

where H_L,H_R are circuits restricted to their respective half-chains and
V is a single unitary supported on some finite interval X union Y about the
cut, with X in L and Y in R. This finite interval need not have width r.

For the cross state L'R, applying H_L to the traced-out outputs does nothing;
H_R induces an automorphism on the retained output half. A half-chain
circuit preserves its product trace. Consequently its action sends the
finite density h_A to an automorphic image and sends its support projection
to the corresponding image, preserving p_A. For LR' the same reasoning
preserves p_B using H_L. These statements are algebraic and do not require
an infinite tensor-product Hilbert-space unitary or an infinite rank.

For V alone the finite Choi vector on X Y X' Y' is pure. Its reductions on
X'Y and XY' have equal ranks by Schmidt decomposition, and these two cross
spaces have the same dimension dim(X)dim(Y). Outside that finite interval
the cross marginals are tracial. Hence p_A(V)=p_B(V), and therefore
I0(alpha)=0 for every circuit.

Equivalently, work throughout in a finite window large enough to include
V and the images of its support projections under H_L,H_R; unitary
conjugation preserves ranks there and all added tensor identities cancel
in the normalized fractions. Only after this removal does one return to
the canonical r-collars by the factorization in step 1. No claim that the
removal fits inside the r-collars is used.

## 4. Shift normalization and the index

For a k-site shift on d-dimensional cells, k>0, choose r>=k. In the RWW
orientation J_A contains k crossing Bell pairs and otherwise tracial
factors, while J_B is tracial. Their ranks are respectively
d^(2r−2k) and d^(2r). For k<0 the roles interchange. Thus
`I0(sigma_d^k)=k log d` for every integer k.

We have now proved tensor additivity and the correct values on circuits
and all elementary shifts. RWW Lemma 4.5 therefore identifies I0 with their
logarithmic index. Explicitly, tensor alpha with an opposite-index shift
beta; the tensor product has index zero and hence is a circuit. Its I0 is
zero, so I0(alpha)=log kappa. Returning to equal canonical collar dimensions
gives

```
(1/2) log[rank(J_B)/rank(J_A)]=log kappa.
```

This proves the identity for the actual finite marginals. Purity was used
only for the finite crossing-unitary circuit representative, not assumed
for the generally mixed canonical joint Choi marginal.

## 5. Separate check of the matching-record implication

The elementary implication in A's opening also passes. For the finite joint
Choi state J on S_out S_ref, automorphism/traciality gives J_out=I/M.
After ordering A=L1'R1 and B=L1R1', the all-record matching space is exactly
the span of |x>_A |x>_B. Therefore, for G=Pi J Pi,

```
G_A=G_B=diag(g_x),
0<=g_x<=1/M,  sum g_x=1−E.
```

The upper bound follows by summing all reference diagonal entries at a
fixed full output record x; one selected diagonal entry cannot exceed their
sum 1/M. Off-diagonal entries of G do not survive either partial trace.
Hence ||G_A−I/M||_1=E. Gentle projection and contractivity give

```
(1/2)||J_A−I/M||_1 <= sqrt(E)+E/2,
```

and likewise for B. If its rank is at most M/a, the kernel projection gives
trace distance at least 1−1/a. The stated
`E >= [sqrt(3−2/a)−1]^2` follows. This does not require J to be pure.
For fixed kappa!=1 take a=max(kappa^2,kappa^−2); the rank identity ensures
one cross marginal has the required deficit. The union bound over 2r
commuting computational record tests then yields the opening's constant/r
lower bound. The constant depends on the fixed index; there is no asserted
uniform constant over indices tending to one.

**Scope:** exact strict QCA, full output traciality, and full joint matched
records. This argument is discontinuous in rank and does not extend by
itself to approximate locality, approximate automorphisms, or access to
only separate one-site output marginals.
