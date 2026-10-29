# A paid attempt to repair a characteristic-two tensor algorithm

The proposed operation was **use the exact obstruction to lifting a tensor
decomposition to select a rank-preserving structural repair**, rather than
perform an undirected search followed by a lift test. The native target was
the published AlphaTensor 4-by-4 scheme with 47 products. The experiment did
not acquire a characteristic-zero scheme. It completely excludes the first
two local repair classes specified below, including intermediate rank 48.
This is a failed acquisition attempt with a useful exact boundary, not a new
matrix-multiplication upper/lower bound or a general algorithm-discovery gain.

The substantive general construction is the tangent-update compiler in §3.
The ordinary plus/flip operations and Hensel lifting are established methods;
see COSTS_AND_PRIOR.md. No priority for the compiler lemma is asserted.

## 1. Native input and the actual lifting question

The input is `factorizations_f2.npz`, supplied by Fawzi et al. in the official
google-deepmind/alphatensor repository, entry `4,4,4`. Its shape is
`(3,16,47)`. All entries are 0 or 1. Coordinates are cyclic: the third factor
represents the transpose of the product. Thus the target is

\[
 T_{4i+j,\,4j+k,\,4k+i}=1\quad(0\leq i,j,k<4),
\]

with every other coefficient zero. The acquired factors obey all 4096 tensor
equations modulo 2. Native byte identity/provenance are in SOURCES.json.

Write a decomposition as \(f=((a_r,b_r,c_r))_{r=1}^R\), and
\(F(f)=\sum_r a_r\otimes b_r\otimes c_r\). For a binary solution, choose its
0/1 integer representative \(\widetilde f\), and put

\[
 e_f=(T-F(\widetilde f))/2\pmod2,
 \qquad J_f=dF_f,\qquad I_f=\operatorname{im}J_f.                 \tag{1}
\]

All coefficients of \(T-F(\widetilde f)\) are even. The Jacobian image is the
sum, over terms, of

\[
 \mathcal T(a,b,c)=V_1\otimes b\otimes c
                  +a\otimes V_2\otimes c
                  +a\otimes b\otimes V_3.                       \tag{2}
\]

Since
\(F(\widetilde f+2x)=F(\widetilde f)+2J_fx\pmod4\), there is an
**unrestricted coefficient lift to Z/4** precisely when \(e_f\in I_f\).
No support, sign, magnitude, equal-factor or symmetry constraints are imposed
on the corrections. Native \(J_f\) has rank 2117, with 2256 variables; (1)
is inconsistent. That fixed-point fact was already known in the literature.

Failure of this linear system excludes rational lifts integral at 2 with
the stated reduction, and unramified extensions of that lifting problem.
It does **not** exclude arbitrary characteristic-zero decompositions,
rational coefficients with even denominators, or ramified lifting. In
particular it is not a proof that rank 47 over C is impossible.

## 2. The exact structural moves being tested

For any two ordered terms, the standard plus identity is

\[
 abc+def=a(b+e)c+ae(f-c)+(d-a)ef,                                \tag{3}
\]

where juxtaposition means tensor product, not multiplication of vectors.
All six mode permutations and all ordered distinct term pairs are allowed.
The resulting integer factors are reduced to binary representatives. The
identity holds over Z before that reduction, and increases the term count
by one. Native factors are distinct in each mode, so every such expansion
has 48 nonzero terms.

For two terms with a common first factor, a flip is

\[
 abc+ade\longmapsto a(b+d)c+ad(e-c).                            \tag{4}
\]

There are analogous flips in the other modes. For a fixed common mode, the
two orders of the pair cover the two distinct outcomes; exchanging the two
other modes repeats one of these outcomes after reordering terms. We test
all shared-factor ordered pairs. A zero term may be dropped afterwards;
doing so can only shrink the subsequent Jacobian image.

The acquired finite classes are exactly:

* one plus move (3) from the supplied 47-term decomposition;
* one plus move followed immediately by one flip (4).

No bound on longer walks, two-plus moves, other rewrite systems, other
finite-field points, characteristic-zero direct searches, or global tensor
rank follows from this finite class.

## 3. A reusable exact tangent-update compiler

These lemmas hold for any three finite-dimensional vector spaces over F2,
and an integer target tensor with a binary decomposition. The executable
specializes to equal mode dimensions.

**Plus lemma.** Let \(f'\) be the binary result of (3), and let
\(t=(a,e,f-c)\), with the subtraction interpreted modulo 2. Then

\[
 I_{f'}=I_f+\mathcal T(t),\qquad e_{f'}-e_f\in I_{f'}.           \tag{5}
\]

Consequently,

\[
 f'\text{ lifts to Z/4}\iff
 [e_f]\in\operatorname{span}\{[v]:v\in\mathcal T(t)\}
 \text{ in }(V_1\otimes V_2\otimes V_3)/I_f.                   \tag{6}
\]

Proof. Identity (3) defines a polynomial map from the old six factor
vectors to the new nine, satisfying \(F\circ\phi=F\). Differentiating gives
\(I_f\subseteq I_{f'}\). The tangent space of the middle new term belongs
to \(I_{f'}\), proving one containment in (5).

For the reverse containment, denote the tangent columns of the new first,
middle and last terms by their corresponding factor derivatives. Variations
in the old \(d,b,c,f\) respectively give: the last first-factor derivative;
the first second-factor derivative; first minus middle third-factor
derivatives; and middle plus last third-factor derivatives. The old
\(a,e\) derivatives give the remaining combinations. Together with the
three groups of middle-term derivatives these express every new derivative.
This proves the reverse containment. This argument uses vector derivatives,
so it also covers vanishing or dependent factor vectors.

Explicitly, let \(P_{ij}\) be the derivative of new term \(i\) with respect
to its factor \(j\), each acting on an arbitrary vector in that mode.
For the six old factor derivatives,

\[
\begin{array}{lll}
 J_a=P_{11}+P_{21}-P_{31},&J_b=P_{12},&J_c=P_{13}-P_{23},\\
 J_d=P_{31},&J_e=P_{12}+P_{22}+P_{32},&J_f=P_{23}+P_{33}.
\end{array}
\]

Solving these relations expresses all \(P_{ij}\) using the old derivatives
and \(P_{21},P_{22},P_{23}\), precisely the middle-term tangent space.

For the residual statement, \(\phi(\widetilde f)\) and
\(\widetilde f'\) differ by \(2h\) for integer factor corrections \(h\).
Apply the exact identity before reducing, and linearize modulo 4:
\(F(\widetilde f)=F(\widetilde f')+2J_{f'}h\pmod4\).
This proves the second assertion of (5) and then (6). ∎

Thus the old 4096-by-2256 system is compiled once. A plus proposal needs
only 48 columns reduced in its quotient, not a fresh full Jacobian.
The compiler uses the entire correction space, rather than a single chosen
dual obstruction or an arbitrary Hamming score for the residual.

**Flip union lemma.** Let \(g\) contain \(abc+ade\), and \(g'\) be the
result of (4). Put

\[
 U=I_g+(V_1\otimes d\otimes c).
\]

Then

\[
 I_{g'}\subseteq U,\qquad e_{g'}-e_g\in I_{g'},\qquad
 e_g\notin U\Longrightarrow g'\text{ has no Z/4 lift}.          \tag{7}
\]

Proof. The two new first-factor derivative groups are
\(\delta a\,(b+d)c\) and \(\delta a\,d(e-c)\). Their extra part beyond
the old first-factor groups is \(\delta a\,dc\). Every second- and
third-factor derivative is a linear combination of old derivative columns.
This proves the image inclusion, with the analogous formula in each mode.
The integral identity at the binary common factor again gives the residual
transport by a multiple-of-two factor correction. If a term becomes zero
and is deleted, the smaller Jacobian remains a subspace of the one just
bounded. The implication follows. ∎

Unlike a plus move, a flip need not preserve the old full tangent image.
Therefore (7) is only a **necessary** pruning test. The implementation
constructs and solves the full actual new system if this test survives.
No candidate in the acquired class survived it.

## 4. Executed complete local repair and ordinary controls

`tangent_repair.py` does exact GF2 linear algebra using Python integer
bit vectors; no floating tolerances or external optimization solver occur.
The row-major tensor coordinate \((i,j,k)\) is bit \(256i+16j+k\).
Column elimination stores a basis by its largest pivot. Normal reduction
eliminates **all** pivot coordinates, including below a nonpivot bit, so
its remainder is a linear quotient map. This last detail is essential to
using (6) rather than only a yes/no membership oracle.

`PLUS_SCAN.json` records all \(6\cdot47\cdot46=12972\) ordered proposals.
None passes (6). The extra quotient ranks range from 32 to 42. The kernel
timer, including native load and base assembly, was 15.1562994 seconds.

For the next class, sorted triples of the three 16-bit factor masks
canonicalize only term permutations. There are 6486 distinct expanded
states. `flips` then visits every equal-factor group in every mode and
every ordered distinct pair in the group. There are 27924 such flips.
For **each**, even the enlarged image in (7) misses the transported defect.
`PLUS_FLIP_SCAN.json` records zero survivors and zero lifts, in 28.6214216
seconds. These counts are finite native-input acquisition, not a probability
estimate or a sampler claim.

`compare_full_system.py` additionally executes:

* independent equation-row GF2 elimination on the native full system;
* the same row elimination on the native 2-by-2 Strassen scheme, which
  admits a mod-4 lift (a reject-everything implementation would fail);
* ordinary full-Jacobian solves for the same first 64 ordered plus proposals,
  agreeing with both the compiler's answer and its predicted Jacobian rank;
* raw whole-image equality and residual-transport checks on the first eight
  proposals, and full post-flip systems on all 32 flips of those states.

All checks passed. These implementation controls support, but do not
replace, the general identities in §3 or the complete enumeration in §4.
There has been no separate agent whole-proof acceptance of this package at
freeze. In particular, the independently written row routine is a second
code path by the same worker, not a separate scientific review.

## 5. Research decision

The proposed short local repair has failed at an entire acquired boundary;
it did not merely rediscover that the original 47-term point fails to lift.
The compiler acquires this stronger failure cheaply enough for a laptop,
but its Python timing is not evidence of superiority over optimized
published search implementations. General flips/plus/Hensel methods and
the rational 48-term construction are controlling prior methods.

There is no basis here to allocate a larger undirected search or promote
this route as the civilisation-level discovery operation. A real next
evidence gate would be an actually acquired characteristic-zero-aware
rewrite that escapes this boundary, or a repeatable successful acquisition
comparison against equally informed direct characteristic-zero and modular
searches. No such success was acquired. The global rank-47 problem remains
open in this work.
