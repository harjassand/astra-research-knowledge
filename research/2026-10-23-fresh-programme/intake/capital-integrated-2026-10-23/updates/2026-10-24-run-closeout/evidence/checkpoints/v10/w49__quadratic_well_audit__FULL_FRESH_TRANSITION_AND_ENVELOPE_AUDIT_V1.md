# Fresh audit of the quadratic-well transition and global quotient envelope

24 October 2026, Brisbane. W49. Exact target, read completely:

`work/workers/w26_fundamental_math/trace_compiler/QUADRATIC_WELL_TRANSITION.md`,
SHA256 `df3b51e754fcd0d7c761b54645b116aa9d91ae845fcb1d6740e6387687a6f5fe`.

I read its exact arithmetic source `78d74068...`, receipt `bc2e56e1...`
and binding file. I separately read the contextual
`PAIR_MEAN_PROJECTION_REPAIR.md`, SHA256
`644ad5a095fec2d71f11856bc6ac5ef1823ef5d868c33eba74717bb460219590`.
The NEW theorem is reconstructed directly below, without importing the
old exact-support argument, old tree grammar, a laminate density theorem
or any pending claim from other W26 files. Own raw-geometry arithmetic
imports no peer implementation or data.

**Verdict:** no blocking defect found in the general all-finite-tree
second-moment transition bound, the UI weak-limit exclusion, or the
globally finite continuous rank-one-convex envelope with its positive
analytic value at zero. The canonical five-by-two quotient and every
explicit coefficient/bound independently reconstruct exactly. The claim
is a QUOTIENT-law separator. It is not an actual affine-boundary
gradient-law Jensen counterexample, a two-output result, a quasiconvexity
claim, or a solution of Morrey. Historical priority and external
acceptance remain UNKNOWN.

## 1. Precise finite-tree contract and conservation

At each positive binary split, the parent matrix is the actual weighted
mean of its children, whose difference has rank at most one. All leaf
occurrences have positive probability. Fractions may be arbitrary REAL
numbers in (0,1); leaf matrices and depths are arbitrary but finite for
each tree. Occurrences may share the same matrix value while receiving
different W/O/E labels. Nothing below assumes rational masses, bounded
order or distinct atoms.

Let `F(X)=B(X-q,X-q)`, where B is symmetric bilinear,
`|B(Y,Z)|<=C|Y||Z|`, and `B(H,H)=0` for EVERY rank-one or zero H.
Along a line in such a direction the quadratic term vanishes exactly.
Thus F is globally rank-one affine. Induction from the finite leaves
gives at EVERY node v

    F(M_v)=E[F(T)|v],                              A1

where M_v is the conditional terminal mean. Conditional terminal second
moments are finite in each finite tree, regardless of how large they
are; no uniform bound is needed for this induction. Parent minus child
has rank at most one because it is a scalar multiple of the child
difference. Zero-rank and repeated-value splits pose no exception.

Assume W lies in the radius-rho ball about q; O obeys
`|T-q|<=R` and `F(T)>=delta`; E has no norm restriction. Set

    eta=delta/(16CR^2), 0<eta<=1/16,
    rho<=R eta^4,
    r_v=P(O|v), e_v=E[|T-q|^2 1_E|v]/R^2.

Call v clean if `e_v<=eta^8`. Conditional Cauchy--Schwarz and A1 imply

    |M_v-q| <=rho+Rr_v+R sqrt(e_v)
              <=R(r_v+2eta^4),                    A2
    F(M_v)>=delta r_v-Crho^2-CR^2 e_v
              >=CR^2(16eta r_v-2eta^8).            A3

In A2 the E contribution is bounded by
`sqrt(P(E|v) E[|T-q|^2 1_E|v])`; only its probability factor was
bounded by one. In A3 the W loss is at most `Crho^2 P(W|v)` and the E
loss is its ACTUAL conditional second moment times C. Small auxiliary
MASS has not replaced auxiliary SECOND MOMENT.

## 2. Clean interval, edge crossing and first-bad-node frontier

If a clean node had `eta^2<=r<=eta`, A2 and the global B bound would give

    F(M)/(CR^2 eta r)
       <=(r+2eta^4)^2/(eta r)
       <=1+4eta^3+4eta^5 <2.

But A3 gives a ratio at least `16-2eta^5>15`. These bounds hold for all
real `0<eta<=1/16` by monotonicity of the positive powers. Thus no clean
node has its conditional O probability in the closed forbidden interval.

Now let a clean parent A have r_A>eta and a clean child B have
r_B<eta^2. The matrix bounds A2 give

    |B-q|<2Reta^2,
    |A-B|<=R(1+eta^2+4eta^4)<2R.

The latter uses only `r_A<=1`; it does not bound terminal E atoms.
Rank-one affinity supplies the EXACT expansion

    F(A)=F(B)+2B(B-q,A-B),

with the direction-square term exactly zero. Consequently

    F(A)<CR^2(4eta^4+8eta^2)<9CR^2eta^2.

A3 at A instead gives `F(A)>CR^2(16eta^2-2eta^8)>15CR^2eta^2`.
Thus this clean edge cannot cross the forbidden interval either.

Suppose p_O>eta. A root-to-W-leaf path consisting entirely of clean
nodes would start with r>eta and end at r=0. It is finite. Since none of
its nodes lies in the forbidden interval, at some edge it must jump
directly from above eta to below eta^2, which was excluded. Hence EVERY
W path contains a bad node, `e_v>eta^8`.

Take its FIRST bad node on each W path. Their distinct set is an
antichain: if one were an ancestor of another, it would already be the
first bad node on the latter path. Their subtrees are disjoint and cover
all W occurrences. Writing pi_v for unconditional node probability,

    E[|T-q|^2 1_E]
       >=sum_frontier pi_v R^2 e_v
       >=R^2 eta^8 sum_frontier pi_v
       >=R^2 eta^8 p_W.                            A4

This includes a bad root and p_W=0. No tree depth, leaf count, maximum
terminal/intermediate norm or mass denominator occurs in A4. The bound
is applied to each FINITE tree; it does not quietly use an infinite
tree as a finite object. The argument is also the elementary stopping
frontier estimate for the nonnegative conditional-moment martingale.

## 3. Independent canonical mesh and quotient reconstruction

I rebuilt the five hat gradients from the listed vertices and eleven
triangles using signed barycentric-coordinate gradients, not a peer
gradient routine. The face areas are exactly

    10,10,6,10,2,2,1,2,1,3,3,

with total 50. All vertices lie in the outer triangle. After orienting
each face counterclockwise, internal edge chains cancel in pairs and
the only boundary is `0->1->2->0`. Positive oriented triangles with this
unit boundary cover the outer triangle once away from the finite edge
set, by the elementary winding identity. The nodal hat traces agree on
every shared edge and vanish on the outer boundary. Thus these really
are actual gradients of the specified continuous piecewise-affine
five-output map, with physical area weights.

The final two actual gradients have rank-one difference and equal
physical area 3. Their mean q is

    q = [ -1/2  -1/4 ]
        [   0      0 ]
        [   0      0 ]
        [  1/2   1/4 ]
        [   0   -1/6 ].                            A5

Replacing JUST these two occurrences by q gives ten distinct atoms
with exactly the displayed quotient weights and barycenter zero.
All ten two-row minor moments are zero both before and after this
replacement. In particular the null-minor constraints survive, so a
quadratic null Lagrangian by itself is not a Jensen separator.

For the supplied omega, direct exact evaluation gives

    F(H_i)=(10,10,10,21,10,10,10,10,10,0),
    F(0)=sum mu_i F(H_i)=11,
    max_i |H_i-q|^2=317/72.                         A6

For each two-row determinant the symmetric polarization has operator
norm one half in the corresponding four entries. Hence summing absolute
omega coefficients gives the deliberately safe `C=688` on ALL matrices;
every global rank-one direction annihilates its quadratic part.
These are global algebraic facts, not checks only on the ten wells.

The exact affine functional ell in the source satisfies all ten
interpolation equations, has `ell(0)=p=3/25`, and its linear coefficient
norm squared is `182118/15625`. Own Fraction arithmetic verifies these
equations directly from the independent hats. No estimated interpolation
or finite sample of matrices is substituted for the identity.

## 4. Neighborhood constants and UI weak limits

With `R0=9/4`, `R=3`, `delta=5`, `r0=1/1000`,

    eta=5/99072, rho=3eta^4,

the O balls obey `|A-q|<=R0+r0<R`. Expanding F around their centers
gives on ALL of those balls

    F(A)>=10-C(2R0 r0+r0^2)>5.

The W ball obeys `F(A)<=C rho^2<5`, so W and O are disjoint.
Every limiting quotient atom lies in the INTERIOR of its appropriate
ball, while the closure of E misses all of them.

If terminal laws of finite trees converged weakly to this quotient,
then p_W would tend to 3/25 and p_O to 22/25. On any fixed compact set
the E contribution to the second moment tends to zero: its mass tends
to zero because its closure is disjoint from the limiting finite
support. If squared terminal norms are uniformly integrable, the
unbounded contribution also tends to zero, since
`|T-q|^2<=2|T|^2+2|q|^2`. This contradicts A4, whose right side tends
to a strictly positive constant.

Uniform boundedness of second moments alone does NOT prove the tail
contribution tends to zero. The source correctly requires UNIFORM
INTEGRABILITY and explicitly permits the remaining concentration
loophole. No bounded-gradient or tree-order assumption was imported.
Nor is any general approximation theorem for laminates needed.

For an exact completion `(1-epsilon)mu+epsilon sigma`, label the
designated original occurrences W/O and ALL added occurrences E, even
when values coincide. Using rho=0, delta=10 and any R>=3 yields the
source's A4 analogue. If auxiliary values satisfy `|A-q|<=R`,

    epsilon >=p eta_R^8/(1+p eta_R^8),
    eta_R=10/(16*688*R^2).                          A7

For epsilon<=1/2, p_O>=11/25>eta_R; the other epsilon case is automatic.
At R=3 the source's dyadic lower bound `2^-110` checks exactly.
Without the auxiliary norm bound, the conclusion is instead its
weighted auxiliary second-moment inequality (13). The same R then
bounds only the designated physical O atoms. These two distinct
statements have not been conflated.

## 5. The envelope is globally rank-one convex and continuous

Let `K={H_0,...,H_9}`, `h(A)=dist(A,K)^2`, and define f(A) to be the
infimum of terminal h-cost over all finite positive binary rank-one
trees with barycenter A. A one-leaf tree is allowed, so

    0<=f(A)<=h(A)<infinity                           A8

at EVERY real five-by-two matrix, not only the finite support or a
projected chart. Near-minimizing finite trees exist by the definition
of an infimum, without assuming an optimizer. If rank(A-B)<=1 and
0<t<1, put two such trees below the root split of tA+(1-t)B. The
concatenation is still finite, has precisely that barycenter and rank-one
first jump. Send the two cost tolerances to zero to obtain the global
rank-one-convex inequality. Endpoint t values are immediate.

Continuity is not inferred from an arbitrary infimum of continuous
functions. The coordinate matrix directions are rank one, so f is
separately convex. On a fixed outer coordinate box, A8 gives a uniform
bound `0<=f<=M`, with `M=max_box h<infinity`. On an inner box separated
from the coordinate boundaries by distance d, ordinary convex secant
bounds give slopes between `-M/d` and `M/d` in EACH coordinate, uniformly
in the other coordinates. Telescoping coordinate changes gives local
Lipschitz continuity (Euclidean constant at most `sqrt(10)M/d`). Every
point lies in such an inner box. This proves global continuity and
finiteness directly, without a hull-closure identification theorem.

Since h vanishes at every well, `f(H_i)=0`. It remains essential to prove
f(0)>0 rather than merely naming an envelope; the next section does so.

## 6. Positive lower bound at zero with all tails included

Take ANY finite tree at zero, and write `z=E h(T)`. Choose one nearest
atom pi(T), resolving ties in a fixed measurable way. The affine
coordinate and barycenter zero give

    |P(pi(T)=q)-p|
      =|E ell(pi(T))-E ell(T)|<=L sqrt(z).           A9

On the nearest-q class, leaving its radius-rho ball costs at least
rho squared in h. The corresponding statement for any other nearest
well uses r0. Hence exactly

    p_W>=p-Lsqrt(z)-z/rho^2,
    p_O>=1-p-Lsqrt(z)-z/r0^2.                       A10

Let `m=min(p,1-p)`, `D=2+2R0^2/rho^2`, and take the minimum of the
three positive quantities in the source's (17):

    gamma=min(m^2/(16L^2), m rho^2/4,
                       R^2 eta^8 p/(4D)).          A11

If z<=gamma, then `Lsqrt(z)<=m/4` and `z/rho^2<=m/4`.
Since rho<r0, A10 implies p_W>=p/2 and p_O>=(1-p)/2>eta.
The transition theorem A4 thus forces

    E[|T-q|^2 1_E]>=R^2 eta^8 p/2.                 A12

On the other hand E is outside radius rho of EVERY well, so
`P(E)<=z/rho^2`. Comparing T to its chosen nearest well gives on ALL
matrices `|T-q|^2<=2h(T)+2R0^2`, even for arbitrarily remote atoms.
Therefore

    E[|T-q|^2 1_E]<=Dz<=R^2 eta^8 p/4,              A13

contradicting A12. Thus every finite tree at zero costs MORE than gamma,
and its infimum satisfies `f(0)>=gamma>0`.

The independent exact replay reproduces all three quantities in A11
and verifies `gamma>=2^-231`. The strict per-tree bound and the
nonstrict infimum bound are correctly distinguished. No finite-tree
search, envelope evaluation oracle or attainment assumption enters this
proof. It follows that the actual globally continuous rank-one-convex
function f has the quotient Jensen gap

    integral f dmu-f(0)=-f(0)<=-gamma<0.             A14

The specified witness is variational. A polynomial algorithm to evaluate
it, an elementary closed expression or a sharp separation size is not
claimed and does not follow.

## 7. Actual-gradient and two-output boundaries

The original eleven-face law is an actual five-output hat-gradient
law. The NEW law is obtained by replacing two selected occurrences by
their physical mean. Such a replacement need not be a legal sibling
merge of an actual rank-one tree, nor the gradient law of a modified
continuous map with the old boundary trace. On the selected patch, for
example, the collinear source vertices 3,8,6 have nodal images
`e_3,e_8,e_6` (in the stated hat-row labels); the middle value is not
the affine average of the endpoint values. Flattening the pair to one
gradient therefore does not preserve that trace. This audit proves
NO actual-gradient-law Jensen violation. The contextual prior theorem
that the original eleven-atom law is finite is not independently
recertified here and is not used by the new proof.

The skew coefficient matrix omega has rank FOUR by exact rational
elimination. A scalar determinant obtained from a two-output left
projection has a decomposable coefficient two-form of rank at most two.
Thus the load-bearing quadratic F cannot be factored into that
two-output determinant. The nonlinear envelope f has no proved descent
preserving its well values and separation either.

For clarity, composition `f(RA)` with a fixed linear output injection R
DOES preserve rank-one convexity, since left multiplication preserves
rank-one directions. What is missing is the required identity
`f(R C H_i)=f(H_i)` for a two-output projection C and all wells/root.
An arbitrary inverse prescription on a finite projected set supplies
neither a rank-preserving global map nor those identities. No transfer
of A14 to two-by-two matrices is justified. Quasiconvexity of f and any
Morrey implication remain unproved.

## 8. Independent arithmetic receipt and scientific status

Own `check_geometry_and_constants.py` uses only Python stdlib Fraction
arithmetic; no peer code/receipt, solver, floating point or package is
imported. It reconstructs the original hats, oriented boundary chain,
pair rank, all original/quotient minor moments, well values, affine
coordinate, skew rank and every stated constant. All pass. Its raw
receipt is `GEOMETRY_AND_CONSTANTS_CHECKS.json`; runtime was about
0.0032 seconds. Peak memory and total inference/review cost were not
measured. This is exact finite input/certificate verification, not
enumeration of every finite tree. The universal quantifiers come from
the analytic arguments in Sections 1--6.

No physical displacement field, apparatus, publication, outreach or
equipment operation was acquired/performed. No claim of new general
incompatibility, hull or transition-layer theory is made. Internal proof
reconstruction: no blocking defect found. Historical novelty and external
mathematical acceptance UNKNOWN; computational/practical advantage
NOT_ESTABLISHED; actual-gradient-law/m2/Morrey resolution NOT_ACHIEVED.
