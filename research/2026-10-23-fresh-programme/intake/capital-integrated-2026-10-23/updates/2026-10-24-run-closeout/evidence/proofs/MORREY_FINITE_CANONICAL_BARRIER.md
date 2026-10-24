# An exact finite-order barrier for the canonical six-output lift

23 October2026. Computer-assisted elementary algebraic proof, with independent
stdlib rational identity replay. Fresh external independent audit pending.
This does not exclude limiting laminates and is not a two-output Morrey claim.

## Statement

Take the admitted positive straight triangle mesh with boundary0,1,2,

    x0=(0,0),x1=(10,0),x2=(0,10),x3=(2,4),x4=(4,2),
    x5=(6,2),x6=(4,4),x7=(2,6),x8=(3,4),

and physical faces numbered0..12 by

    014,023,034,126,145,156,237,267,348,378,458,568,678.

Let phi(x_i)=e_(i-3) for interior vertices i=3..8 and phi=0 at the boundary,
extended continuously and affinely on each physical face. Let H_i be its
actual6-by2 face gradients and d_i=2|T_i|, so

    d=(20,20,12,20,4,4,4,4,2,2,4,2,2).

The normalized actual gradient law is sum_i(d_i/100)delta_H_i. These13
gradients are distinct. **It has no finite binary laminate representation
whose terminal matrices are its actual support atoms**, even with arbitrarily
many repeated leaves and arbitrary positive real splits of their masses.
In particular it is not a finite-order laminate/prelaminate.

This is an obstruction to the all-output exact finite-tree compiler proposed
through the canonical lift. It says nothing by itself about a limiting
laminate, rank-one-convex Jensen separation, or any2-by2 pushforward.

## Positive coefficient states and the invariant family

For a nonzero coefficient vector c>=0, define its mass, moment and barycenter

    m(c)=sum_i d_i c_i,
    P(c)=sum_i d_i c_i H_i,
    B(c)=P(c)/m(c).

A terminal occurrence of physical atom H_i, at any positive mass, is a
singleton coefficient state. At an internal node coefficient states ADD.
That merge is legal exactly when rank(B(c)-B(e))<=1. The coefficient vector
retains full terminal face masses; no assumption about a physical region
or connected support is made.

Define a family C of states by33 allowed exact support types:

1. The13 singleton supports, with every positive coefficient allowed.
2. The18 adjacent-face pairs, with both coefficients arbitrary positive:

       (0,2),(0,4),(1,2),(1,6),(2,8),(3,5),(3,7),(4,5),(4,10),
       (5,11),(6,7),(6,9),(7,12),(8,9),(8,10),(9,12),(10,11),(11,12).

3. Two four-face supports, with every coefficient positive and one relation:

       Q5=(4,5,10,11),    F5(c)=c4*c11-c5*c10=0;
       Q7=(6,7,9,12),     F7(c)=c6*c12-c7*c9=0.

These are respectively the two four-face stars about interior vertices5,7.
The claim needed below is only that C is closed under legal rank-one merges.
No claim that every state of C is reachable is needed for the obstruction.

## Exhaustive exact closure identities

Consider all unordered pairs of types, including equal types:33*34/2=561.
In85 cases their union is a singleton or an allowed adjacent pair, so their
sum automatically lies in C. There are476 remaining cases. Every case is
covered by an explicit rational polynomial identity in the retained file
`cone_algebra_certificates.json`, SHA256

    c1f6d5501fe48c82c74c23acb9d42bc3d9752a3ddb1ad07cb88fba14a6b23032.

Here is precisely what those identities prove and how to verify them.

Normalize each child separately to mass1; this scales c,e by positive
numbers and preserves both their support/cone relations and their rank-one
compatibility. Give each positive coefficient in the first state its own
variable a_i and each in the second its own variable b_i. The variables
are strictly positive even when their face supports overlap. The following
polynomials vanish:

* sum d_i a_i-1 and sum d_i b_i-1;
* each child's own F5 or F7 when applicable;
* the15 two-by-two minors of P(a)-P(b).

The stored rational identity is a constant linear combination of those
minor/cone equations and of the two mass equations multiplied by1 or a
single coefficient variable. Thus every generator has degree at most2.

For454 cases the support union is NOT any allowed type. The combination
equals a nonzero polynomial whose monomial coefficients are all strictly
positive. It cannot vanish when ALL variables are strictly positive. This
contradicts the rank-one hypothesis. The resulting positive polynomials
have at most8 monomials. Hence these454 support unions cannot occur.

For the remaining22 cases the union is Q5 or Q7. The combination equals
EXACTLY the relevant parent polynomial F(a+b). Thus F(a+b)=0 for normalized
children. To restore arbitrary actual child masses alpha,beta>0, observe
that each child supported inside Q already has F(child)=0: a singleton or
an eligible adjacent pair occupies one row/column of the2-by2 density array;
a quad child has its cone relation by hypothesis. Therefore

    F(alpha*a+beta*b)=alpha*beta*F(a+b)=0.

This explicitly discharges the otherwise missing normalization-to-arbitrary
split-ratio step. The parent stays in C at EVERY positive actual mass ratio.

`replay_cone_algebra.py` uses only Python's standard library and exact
fractions. It does NOT import SymPy, Z3, the synthesis code or a sibling
implementation. It independently recomputes the actual hat gradients and
physical d_i from geometry; builds all33 types from adjacency and the two
listed stars; checks exact coverage of all476 nontrivial pairs; reconstructs
every polynomial generator by sparse exponent dictionaries; and verifies
each rational identity coefficient by coefficient. It also checks each
positive result is nonzero with positive coefficients, every parent target
is precisely F(a+b), and the sparse-child F=0 assertion used in restoring
arbitrary masses. The maximum identity has14 nonzero equation summands.

The synthesis used Z3 only to find rational linear-combination coefficients.
The proof is the finite list of elementary identities and their independent
exact replay; it does not rely on a nonlinear solver's UNSAT answer. Current
replay passes all476 identities in about0.05s. Runtime is an implementation
diagnostic, not a formal proof-assistant assertion or a priority certificate.

## Induction and the exact scope of the obstruction

At every leaf the coefficient state lies in C. At every internal node its
two child barycenters differ by rank at most one. Closure just proved puts
its positive coefficient sum back in C. Induct over any FINITE binary tree.
Every node, including its root, has an allowed support of size at most4.

The actual law has all13 distinct atoms at positive mass. Any representation
of that law must have positive aggregate coefficient on every face. Its
root coefficient state therefore has support13 and cannot belong to C.
Contradiction. This applies to ANY number of repeats, ANY positive real
terminal weights, and ANY binary merge topology; no denominator bound,
preferred physical matching, prescribed root split or disk tree was used.

The barrier is deeper than the earlier no13-leaf tree: splitting more exact
support masses cannot make this canonical6-output law a finite-order
laminate. On the other hand, the actual2-output field from the same mesh
DOES have a15-leaf certificate. Left projection can create new rank-one
connections, so the6-output failure does not transfer back to2outputs.

Nor does this exclude limiting laminates with approximate/auxiliary terminal
atoms. A sequence of finite-order laminates with atoms off the exact support
is not captured by the coefficient-state invariant. No globally rank-one-
convex separating function, no failure of rank-one-convex Jensen, and no
Morrey counterexample has been proved. A useful next operation must exploit
two-output-specific connections or a controlled auxiliary/limiting web.

All inputs are exact constructed mathematical fields, not experimental
data. The standalone input is `canonical_hat_input.json`; its source mesh
was w43's admitted fixture SHA256104db6cc9f4e23c20ad73a891f2b7aa5765b5ec131ae2af55f77527f9fa19866.
New source novelty and external validation remain UNKNOWN. No acquisition,
purchase, outreach or publication occurred. Total model-reasoning costs
remain UNKNOWN; every retained arithmetic/retrieval cost is separate from
the mathematical consequence.
