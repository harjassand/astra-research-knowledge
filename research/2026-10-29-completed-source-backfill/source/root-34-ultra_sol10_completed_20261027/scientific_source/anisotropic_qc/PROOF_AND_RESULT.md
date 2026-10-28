# Anisotropic QC construction: exact growth budgets and compatible-field tests

**Target QC contact: NOT_ACQUIRED. Global target QC: UNKNOWN.**

This run implemented a concrete off-diagonal penalty/envelope construction
from the actual witness plane and a separate compatible periodic-field
search. It obtained an exact obstruction to the value-preserving penalty
construction, including an explicit compatible laminate that loses value.
It did not obtain a target QC certificate or a negative compatible field.

The accepted strict-ROC/non-PC quartics and physical completion retain
their previously accepted statuses. The actual three-atom minors witness
is not treated as a gradient microstructure.

## 1. Global polynomial contacts have a degree-four ceiling

**Lemma.** If a polynomial P on R^(m by n) is globally rank-one convex and

    P(A)<=C(1+|A|^q)

for every A and a finite q>=0, then deg P<=floor(q).

If its degree D is larger than q, scaling P(tA)/t^D as t tends to infinity
gives its leading homogeneous polynomial P_D. Pointwise limits preserve
rank-one convexity, and the growth assumption gives P_D<=0 everywhere.
A finite rank-one convex function is separately convex in all matrix entries.
Holding all other entries fixed, a convex real function bounded above on
the whole real line is constant. Repeating over every entry makes P_D
constant, and positive homogeneity D>0 then makes it zero. This contradicts
the definition of D.

In particular every QC polynomial that is globally below the quartic target
has degree at most4. The same conclusion holds for a shifted point-contact
model satisfying a global Bregman/minor-affine comparison, since the other
terms have degree at most4. This is an elementary growth observation, not
a new general QC approximation theorem.

Thus Heinz's established local polynomial density theorem supplies no
automatic global contact below this target. Its proof deliberately adds
high-degree convex terms to control the function outside the approximation
ball. Such terms cannot be hidden below a fixed quartic simply by passing
to a later polynomial degree.

## 2. The explicit anisotropic penalty construction

Use the main exact target

    F(A)=|A|^4+(252/25)(detA)^2+(99/25)detA*x(A).

Write alpha=sqrt(110)/240, r0²=3591/10000, and normalize the actual
witness base to Abar=diag(36,35)/sqrt2521. Set

    Ubar=(1/r0)[[alpha*12/5,−alpha*12/5],[-1/25,−1/25]],
    V=[[1,sqrt110/2],[1,−sqrt110/2]].

Then Ubar E11 V and Ubar E22 V are the two unit Frobenius rank-one
directions of the actual witness plane. The off-diagonal directions
Ubar E12 V and Ubar E21 V also have rank one and unit norm. These facts
were checked symbolically, not inferred from numerical singular values.

For C a real2 by2 matrix, define

    f(D)=F(Abar+Ubar D V) for diagonal D,
    p(C)=|off C|²,
    h_M(C)=f(diag C)+M p(C)(1+|C|²), M>=0,
    G_M=Q h_M,

where Q h_M denotes the largest global QC minorant. Each h_M is explicit,
nonnegative and has quartic growth. For M>0 it is coercive. Its QC envelope
is finite because zero is an admissible QC minorant and h_M is finite.
The operation is a genuine anisotropic QC-generator definition; evaluating
the envelope or its contact loss is an additional variational acquisition
cost, not assumed free or supplied by a finite sample.

The diagonal restriction f is separately convex by the accepted ROC of F
and the rank-one axes. A plausible Müller-based attack is to increase M
until G_M preserves f at zero while keeping the generator globally below
the transformed target. The following exact calculation rules out that
particular value-preserving attack, at every M.

## 3. Exact local price of preserving the target value

The half-Hessian of f at zero is

    [[a,b],[b,a]],
    a=276442/45264555,
    b=6601754/5029395.

Set

    L=b−a=59139344/45264555>1.

Consider the rank-one matrix R=[[1,1],[-1,−1]]. Direct exact expansion gives

    [h_M(tR)+h_M(−tR)]/2
      =f(0)+2(M−L)t²+(d4+8M)t^4,
    d4=17245888/12895281>0.                         (1)

Every finite QC function is rank-one convex. If G_M(0)=f(0), its rank-one
Jensen inequality and G_M<=h_M would require the right side of(1) to be
at least f(0) for every t. Therefore value preservation requires M>=L.

There is a quantitative loss when0<=M<=1. Minimizing(1) in t² gives

    G_M(0)<=f(0)−(L−M)^2/(d4+8M)
            <=f(0)−epsilon0,

    epsilon0=192509769794521/19131170106699400>0.

The first bound uses the actual two-point rank-one laminate at +/-tR.
It is compatible and can be realized by ordinary one-dimensional laminates;
it concerns the newly constructed obstacle h_M, NOT the target F. At M=1
the optimizing squared amplitude is exactly

    t²=49824367299/1517744554280.

This gives an explicit finite value-loss certificate rather than a failure
of a numerical envelope solver.

## 4. Exact global off-plane growth budget

The obstacle has the pointwise convex lower bound

    h_M(C)>=M[p(C)+p(C)^2],

because F>=0 and |C|²>=p(C). The right side is a convex function of the
off-diagonal entries, so it is itself an admissible QC minorant. Hence

    G_M(C)>=M[p(C)+p(C)^2].                         (2)

Along C=tE12 the transformed target has leading coefficient

    F(Ubar E12 V)=1,

because the physical direction is unit rank one. Equation(2) therefore
shows that any global comparison

    G_M(C)+ell(C,detC)<=F(Abar+Ubar C V)

with an affine function ell in the minor coordinates requires M<=1.
No such minor-affine term can cancel the excess t^4 growth. The same holds
along E21. Consequently the value-preserving extension would require
simultaneously

    M>=59139344/45264555 and M<=1,

which is impossible.

For M>1, the generator is also provably materially anisotropic: along E12
its quartic leading lower bound is M, whereas along E11 its upper bound
h_M=f has quartic leading coefficient1. A right quarter-turn exchanges
these directions up to sign. Thus G_M cannot be right-rotation invariant.
That observation does not make it an affordable target contact.

**Restriction of this obstruction.** It excludes preserving G_M(0)=f(0)
while obtaining global subordination. A positive constant shift can recenter
a model whose envelope already lost value; that changes the contact task.
This argument does not exclude every such affine-recentered contact, nor
unequal quadratic/quartic penalties, matrix-valued penalties, other
anisotropic QC generators, or target quasiconvexity. Earlier interim wording
was explicitly corrected to retain this loophole.

## 5. Actual compatible periodic-field acquisition

A separate attack used genuine periodic gradients rather than the known
incompatible three-atom measure. Let k1,k2 be linearly independent vectors,
k3=k1+k2, and ui real two-component polarizations. On the corresponding
parallelogram torus, take

    Dphi(x)=sum_(i=1)^3 ui tensor ki cos(ki dot x).

An omitted common2pi factor can be absorbed into ui. Every component is
the derivative of the explicit sine potential, so the gradient is compatible.
All spatial modes, amplitudes and shape parameters here are finite and
fully specified in the saved input/output.

For a quartic F and fixed base A, exact polarization gives

    mean F(A+tDphi)−F(A)=P2 t²+P3 t³+P4 t^4.

The linear term vanishes by the exact mean gradient. The accepted ROC gives
P2>=0 for compatible fields and positivity gives P4>0 for a nonzero field.
A negative Jensen value on this ray exists precisely when

    P3²/(4P2P4)>1.

The numerical search optimized six real polarizations and three wave-shape
parameters, with64 restarts per energy and up to500 optimizer iterations.
A16 by16 trigonometric quadrature has no frequency aliasing through degree4
for these phase modes; its arithmetic was numerical during acquisition.
The known-QC norm-four control was retained. The best acquired ratios were

| Energy / base | Best numerical ratio |
|---|---:|
|norm-four, I|0.1333087705|
|main beta=.99 target, normalized diag36,35|0.2887863393|
|m=197 family target, I|0.2964355779|

No negative field was acquired. The entire192-restart search, including
the matched control, took8.895 seconds on this host. This finite diagnostic
does not bound the family-wide maximum or establish QC.

For an independent literal check, the acquired wave vectors and polarizations
were rounded rationally. verify_triad_fields.py constructs exact Laurent
polynomials for all gradient entries, verifies zero mean gradient and zero
mean determinant, and exactly extracts the constant coefficients P2,P3,P4.
It proves P3²<4P2P4 for each of those THREE actual rounded gradient rays,
hence no overall amplitude on those rays violates Jensen. It is not a
certificate for other shapes, more modes, or arbitrary compatible fields.

## 6. Primary-source scope and the remaining operation

Müller's1999 primary preprint was visually checked at printed pp.1,3,4:
[primary PDF](https://files-www.mis.mpg.de/mpi-typo3/preprints/1999/preprint1999_29.pdf).
Corollary3 supplies QC approximation on each compact diagonal set. Theorem1
as printed assumes nonnegative f with at most QUADRATIC growth; it does not
directly apply to this quartic f. I did not promote an unproved L4 extension
or an unbounded concentration limit into a premise. The known bounded
gradient-Young-measure theorem retains its accepted scope.

Heinz2008 Theorems1.1/6.1 and the proof of global convex correction were
read in the [primary paper](https://www.numdam.org/item/10.1051/cocv:2008010.pdf).
They are established density results. They do not give a uniform degree,
finite target contact, off-plane subordination, or the coefficient budget
needed here. The growth lemma in Section1 explains why their high-degree
correction cannot simply be imported under the present quartic bound.

A separate attempt to retrieve Iwaniec–Kristensen2005 reached the official
journal record and cached introductory text, but direct public PDF retrieval
returned the journal's maintenance page. No theorem from that incompletely
read text is used as a premise. No paid retrieval or external action occurred.

The concrete target operation remains: acquire an anisotropic QC model
with controlled off-plane growth, its actual value and derivative, and a
global comparison at the required base. The present exact results identify
two growth constraints and one failed natural generator, while the actual
compatible-field test remains negative. Target global QC, a successful
point contact, a QC counterexample, generic novelty and practical advantage
remain UNKNOWN/NOT_ACQUIRED.

## Replays and charged costs

verify_penalty_budget.py uses Sympy and exact algebra; its latest replay
took.115 seconds. verify_triad_fields.py uses only the standard library
and exact Laurent/Fraction arithmetic; its replay took.010 seconds. Their
saved JSONs contain all literal constants and rational fields. Model
reasoning, proof writing, source retrieval, and the uncomputed QC-envelope
evaluation are additional costs, not claimed zero. No efficient algorithm,
negative-decision bound, or full target success is asserted.
