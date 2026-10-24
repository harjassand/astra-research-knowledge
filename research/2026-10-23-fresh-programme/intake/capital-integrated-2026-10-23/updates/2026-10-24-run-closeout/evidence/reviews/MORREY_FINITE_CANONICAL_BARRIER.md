# Independent audit of the continuous exact-support finite-tree obstruction

The frozen `CANONICAL_FINITE_BARRIER_audited_snapshot.md`, SHA256
86c61a9789d5c3f177a990f858ee79261a366f51dca45a231e0fb274d2e7d5ef,
survives independent mathematical reconstruction. Its rational polynomial
certificates have been independently verified without Z3, SymPy, the sibling
atom builder, or the sibling replay implementation. The algebra covers all
positive real weights and all finite merge trees, not a finite weight grid.

## Exact statement checked

Use the retained positive straight N9 triangular mesh from
`../escape/certificate.json`. Map interior vertices3,4,5,6,7,8 to the six
standard basis vectors, map the three outer vertices to zero, and extend
continuously and affinely over every physical face. Its face gradients H_i
are six-by-two matrices. They are thirteen distinct actual physical atoms.
Writing d_i=twice physical area gives

```
d=(20,20,12,20,4,4,4,4,2,2,4,2,2),  sum d_i=100.
```

The physical law mu=sum_i(d_i/100) delta_(H_i) has mean zero. It admits
**no finite positive binary rank-one tree with this exact terminal law**,
even with arbitrarily many repeated occurrences, arbitrary positive real
occurrence weights, and arbitrary internal barycenter matrices. This is
an obstruction to finite order/prelaminate representation of this six-output
law. It is not an assertion that mu fails the rank-one-convex Jensen
condition or cannot be a limiting laminate.

## State definition and the closure proof

For coefficients c_i>=0 with at least one positive, let

```
M(c)=sum_i d_i c_i,
P(c)=sum_i d_i c_i H_i,
B(c)=P(c)/M(c).
```

The support of a coefficient state is the set of positive c_i. Its
coefficients record all descendant terminal masses; they are not a
physical patch or a replacement law with only the same mean. At a merge
states add. The two means must differ by rank at most one.

The invariant family consists of thirteen singleton supports, eighteen
physical adjacent-face pair supports, and the following two full stars:

```
Q5=(4,5,10,11),  F5(c)=c4*c11-c5*c10=0;
Q7=(6,7,9,12),   F7(c)=c6*c12-c7*c9=0.
```

On each listed support every active coefficient is strictly positive.
The eighteen pairs are generated independently by sharing an entire
physical edge. The two four-face stars are independently identified as
the full stars of the only degree-four interior poles5 and7. The proof
needs this family to contain every reachable state; it does not need
every listed state to be reachable.

There are33*34/2=561 unordered type pairs including equal types. The
independent verifier generates all of them and checks exact certificate
coverage. For85 pairs the support union is a singleton or allowed adjacent
pair, so the positive sum is automatically in the family. For the other
476 pairs normalize each child separately to mass one, with active
variables a_i and b_i strictly positive. Overlapping supports have separate
a_i and b_i variables. The child means then equal P(a) and P(b).

The fifteen two-by-two minors of P(a)-P(b) vanish under the rank-one
hypothesis. Applicable child product forms vanish, and the two mass
equations sum d_i a_i-1=sum d_i b_i-1=0 vanish. These are precisely the
equations reconstructed by the independent verifier; only a mass equation
may be additionally multiplied by1 or one active variable. Thus every
supplied identity is a rational polynomial consequence of valid equations.

For454 pairs the union is outside the allowed support list. The supplied
combination equals a nonzero polynomial with positive coefficients on all
its present monomials. Because every variable is strictly positive, this
polynomial is strictly positive for every real admissible coefficient
assignment. The vanishing equations would make it zero, a contradiction.
For example, the singleton pair0,1 yields the exact identity

```
(-1/100) * minor_(rows3,4)(P(a)-P(b)) = a0*b1 > 0.
```

The row numbers here refer to the interior nodal hats; in the stored
zero-based six-output row convention they are rows0,1. This explicitly
illustrates the sign mechanism. The complete identities, not this sample
alone, cover all454 forbidden unions.

For22 pairs the union is Q5 or Q7. The exact combination equals the
appropriate F(a+b), hence this product form is zero for normalized children.
Normalization does not force equal actual child masses. To restore them,
write c=alpha*a and e=beta*b with alpha,beta>0. Every allowed child whose
support lies in this quad already has F(child)=0: for singletons/eligible
adjacent pairs this is an identically zero polynomial; for the quad itself
it is the defining relation. Homogeneous polarization therefore gives

```
F(alpha*a+beta*b)
 = alpha^2 F(a)+alpha*beta*(F(a+b)-F(a)-F(b))+beta^2 F(b)
 = 0.
```

The independent verifier checks the sparse-child zero-form assertion for
every applicable case. This discharges the arbitrary positive split-ratio
issue. The family is closed under every legal positive binary merge.

## Why this rules out arbitrary finite exact-support trees

All leaf states are singletons. Every internal coefficient vector is its
children's sum, and every child-mean difference is rank at most one.
Induction up any finite binary tree therefore leaves every node inside the
invariant family, with support size at most four. The physical terminal law
has thirteen distinct positive atoms, so its root coefficient state has
support thirteen. This contradicts the invariant.

The proof permits arbitrary real weights because the verified identities
are polynomial identities evaluated on all strictly positive real variables.
It permits any finite number of repetitions and any tree topology because
the invariant is compositional. Its state cone omits the extra per-face root
capacity bounds, making the obstruction stronger rather
than excluding a valid subtree. Arbitrary auxiliary INTERNAL matrices
cannot help a finite exact-support tree: they are already the barycenters
of their positive descendant exact-support measures.

The exact-support restriction is essential for TERMINAL atoms. A finite
approximation may contain auxiliary terminal atoms off this support; those
states are outside the invariant. Such residual atoms might tend to zero
mass along an infinite sequence. The proof neither excludes that possibility
nor provides a quantitative mass/transport lower bound or a continuous
rank-one-convex separator.

## Evidence, consequences and remaining uncertainty

`independent_polynomial_replay.py` uses only standard Python plus the earlier
auditor's elementary Fraction gradient routine. It recomputes all physical
areas and six-output hat gradients from the raw geometry, checks distinct
atoms, constructs all33types/all561pairs, checks476 exact identity payloads
with sparse exponent dictionaries, checks every final coefficient sign,
every target product form and every normalization hypothesis, and verifies
the zero mean/full root support. There are454 strict-positive identities
and22 product identities. Maximum identity size is14 equation summands;
maximum result size is8 monomials. The exact replay took approximately0.054s
locally; its saved receipt controls current run timing. This is a
computer-assisted elementary algebraic proof, not a nonlinear solver
UNSAT assertion or a claim of formal proof-assistant verification.

The supplied certificate file has SHA256
c1f6d5501fe48c82c74c23acb9d42bc3d9752a3ddb1ad07cb88fba14a6b23032.
The independent physical input has SHA256
fc0d299d8ff65b74adfcf6c7b312c354777604a92b4e6071715592aec689b05a.
The packet retains a local copy of the certificates, the source proof
snapshot, the independent verifier, and its case-by-case receipt.

Combined with the preserved <=5-interior-vertex positive proof, this makes
five the sharp interior-vertex threshold for the universal **all finite
output dimensions / exact finite binary-tree** assertion in this triangular
boundary setting. An admitted six-interior-vertex counterexample exists in
output dimension six. This does not establish sharpness for output dimension
two, and it says nothing about the historical novelty of such a threshold.

For the same geometry, the retained two-output projected field DOES admit
the independently verified fifteen-leaf tree. Left projection can create
rank-one connections; nonexistence in six outputs cannot be pushed down
to two outputs. General two-output closure, limiting lamination of this
canonical law, rank-one-convex Jensen separation, and Morrey remain
unresolved here. Historical novelty and external expert acceptance remain
UNKNOWN. Full Morrey and the wider mission remain NOT_ACHIEVED.
