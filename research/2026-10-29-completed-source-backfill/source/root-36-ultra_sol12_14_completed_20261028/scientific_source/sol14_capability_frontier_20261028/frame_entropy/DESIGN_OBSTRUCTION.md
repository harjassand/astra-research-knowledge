# A finite 2-design that fails the score-convex-order mechanism

This is an exact obstruction to hypothesis(H) in `PROOF.md`, and hence
to its full convex-order conclusion. It is **not** an entropy
counterexample. The unrestricted preparation entropy inequality for
projective 2-designs is not decided by this construction.

## Actual48-state weighted construction

In C^3 fix v=e0 and its orthogonal qubit space. Let phi run through the
six Pauli qubit rays

    e1, e2, (e1+e2)/sqrt2, (e1-e2)/sqrt2,
            (e1+i e2)/sqrt2, (e1-i e2)/sqrt2,

with equal weights1/6. Let theta run uniformly through0,pi/2,pi,3pi/2.
Independently choose

    Y=2/9 with probability9/11,
    Y=5/6 with probability2/11.

The48 distinct unit states are

    psi_(Y,phi,theta)=sqrt(Y)e0+sqrt(1-Y)e^(i theta)phi.

Each low-radius state has weight3/88, and each high-radius state1/132.
The phase twirl kills harmonics1 and2, the Pauli rays form a qubit
projective 2-design, and

    EY=1/3, EY^2=1/6, E[Y(1-Y)]=1/6,
    E(1-Y)^2=1/2.

Decompose the symmetric square of C^3 into `e0 tensor e0`, the
two-dimensional symmetrized `e0 tensor C^2` sector, and `Sym^2 C^2`.
The corresponding eigenvalues of the averaged tensor-square projector
are respectively `EY^2`, `E[Y(1-Y)]`, and `E(1-Y)^2/3`; all equal1/6.
Thus

    sum_i w_i S_i tensor S_i=(I+Swap)/12,
    sum_i w_i S_i=I3/3.

This is an actual weighted projective 2-design, not merely a scalar
moment distribution. `certify_design_obstruction.py` constructs every
projector over Q[sqrt2,sqrt5,sqrt7,i], checks all48 Hermitian rank-one
idempotents, distinctness, the first moment, and all81 second-moment
components. No floating-point matrix is a proof premise.

## Exact separating functional

For K=|e0><e0|, the score law `2Tr S_i K` is4/9 with probability9/11
and5/3 with probability2/11. The uniform pair-eigenvalue law has values
2,1,0 with multiplicities1,4,4. For the convex hinge phi(x)=(x-1)_+,

    E_w phi(score)=4/33,
    E_pair phi(score)=1/9,
    difference=1/99>0.

Equivalently the selected high-radius weighted sum, in the scaling used
by the transport lemma, is

    C=9 sum_high w_i S_i=diag(15/11,3/22,3/22),
    m=18/11, 2lambda_max(C)-(m+1)=1/11>0.

Thus the sole exceptional edge cut is exactly where this real design
fails. The nonedge moment/discriminant argument cannot pay it.

Every unitary qutrit SIC measure satisfies H(v)<=1/9 for every v.
Convex mixtures and weak limits preserve that inequality, because
`S -> (2<v,Sv>-1)_+` is a bounded continuous function on projective
space. This48-state measure is therefore strictly outside even the
weakly closed convex hull of all unitary qutrit SIC measures. The
gap1/99 is an explicit continuous separating witness.

## Uniform264-state distinct version

If uniform rather than nonuniform design weights are desired, use the
same six qubit rays. At Y=5/6 use the8 equally spaced relative phases;
at Y=2/9 use the36 equally spaced phases. There are48 high-radius and
216 low-radius states, all with weight1/264. Their radial probabilities
are again2/11 and9/11. Both phase grids annihilate harmonics1 and2, so
the preceding exact moment proof applies unchanged. Distinctness follows
from distinct qubit rays, distinct relative phases, and distinct Y.
The same hinge violation1/99 remains. This is not a repeated-label
cardinality trick.

## Matched entropy control and scope

Choosing preparation p uniformly on the24 high-radius states of the
weighted version gives `M=diag(5/6,1/12,1/12)` and
`D(p||w)=log(11/2)`. Direct rational log enclosures give

    D(p||w)-2D(M||I3/3)=0.6396949928214637...>0.

Thus even this explicit mechanism-failing design has a positive entropy
control. This one control is not an all-p proof and is not needed for
the obstruction. The weighted48-state acquisition and full exact moment
checks took about0.0165s after imports. The uniform264-state variant is
proved by the exact character-sum construction, without a separate264
matrix execution. Historical priority of the specialized obstruction is
UNKNOWN; no general entropy failure is claimed.
