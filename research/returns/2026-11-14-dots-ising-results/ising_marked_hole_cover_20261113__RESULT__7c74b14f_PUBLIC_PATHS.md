# Marked-hole interval-cover bound with exponent12

This is a conditional contour bound for GKP's failed-completion pruning, not an unrestricted phase theorem. It preserves actual physical wall costs and pays all unmarked loops separately.

## Assumptions and required activity
Theta=4, phi=4/R, L=8R, 80<=R<=10000. Every relevant contractible FILLED contour domain has area A<=R². A contour of physical perimeter P is assigned the conservative activity

 a_gamma = exp[-8P+8A/R].

This is the field-reduced activity already earned in the global erased-phase comparison. The present argument does NOT independently justify that field comparison or the area cutoff. It applies to outer minus holes inside a retained plus phase. Their filled projections must cover a specified interval of c columns if the erased phase had full plus columns there but the actual state has none.

## Geometry and a column-rooted count
For an embedded contractible filled hole, let w,h be inclusive bounding-box side lengths in a finite lift. Then

 A<=min(R²,wh), P>=2(w+h), and w<=P/2-1.

Its projection to the cyclic column axis is a connected interval or the whole circle. If it covers a current column, that column contains a filled site but cannot be entirely filled: a contractible disk cannot contain a complete essential vertical column. Therefore some PHYSICAL VERTICAL edge in that column crosses the OUTER boundary. Root at a canonical first such edge and orient the contour. There are at most2L roots/orientations and3^(P-1) physical nonbacktracking walks. We safely use12L3^P. No unknown horizontal origin, factorP, or ambient factorn is needed.

## Joint area/width cost, not incompatible worst cases
For any w,h,A satisfying the hypotheses,

 8P - 8A/R - 12w >= (11/8)P.                     (1)

Proof: put W=w/R,H=h/R. It suffices to show
 8min(1,WH)+12W <=(53/4)(W+H).
The residual RHS is(5/4)W+(53/4)H, at least(sqrt265/2)sqrt(WH), which is at least8min(1,WH), since265>256.

This JOINT inequality is why the long-perimeter activity does not diverge. Independently replacing A by its worst bound and w by P/2 would lose this fact.

For P<=80, R>=80 gives the sharper bound A<=P²/16 and hence

 a_gamma exp(12w) <= exp[-2P-12+P²/160].          (2)

## Uniform tilted kernel is strictly subcritical
For contours covering a prescribed current column, define the tilted root activity S=sum_gamma a_gamma exp(12w_gamma). By(1)-(2) and the rooted contour count,

 S <=12L [sum_(P=4..80) 3^P exp(-2P-12+P²/160)
          +sum_(P>=81) (4/5)^P].

Here3exp(-11/8)<4/5 is paid, not fitted. WithL<=80000 the exact rational certificate proves

 S < 2/5.

Actual conservative displayed value is about.380666. certificate.py uses positive Taylor lower bounds and reciprocals to bound every exponential in the correct direction; all decisions are exact fractions. The tail and the finite sum are both included.

## Greedy interval cover and first-passage sum
Maintain the remaining target as ONE cyclic interval, initially the specified c columns. Choose a hole whose projected cyclic interval contains the left endpoint, with a deterministic fixed tie break. REMOVE ALL of that hole's intersection with the remaining interval: this includes a possible suffix as well as the prefix when the hole projection wraps the chosen cut. The remainder is again one interval or empty. Each selected contour is new, since none of its columns remains after it is selected. Progress is the TOTAL number of removed target columns, at least1 and at most its inclusive lifted width w. A full-circle projection removes the entire remainder. Accumulated progress is exactly c.

This cyclic removal is essential. An ordinary left-to-right scan may select the SAME contour twice (L10, target0..7, holeA projection6,7,8,9,0,1 and holeB2..5 gives A,B,A), incorrectly replacing one activity by its square. The full-intersection removal avoids that error.
Dropping disjointness and all previously selected contours only increases the sum over possible marked chains. Under the tilted weight a_gamma exp(12 progress), every node's outgoing total is at most S<1. The total weight of ALL finite chains that first reach the target is therefore at most1: it is a substochastic first-passage tree, not a geometric series over arbitrary continuations after completion. Untilting pays exactly12c because accumulated progress=c. Thus

 sum_(covering marked chains) product a_gamma <= exp(-12c). (3)

The proof also follows by induction on the number of remaining columns, with each node retaining its actual cyclic interval location. No overshoot or repeated-contour factor is needed.

## Unmarked contours remain paid
A physical configuration is mapped to its deterministic marked chain plus its unmarked wall set. Overcounting possible unmarked sets gives its ordinary wall-product factor, for example

 exp[sum_all_contractible_gamma a_gamma]
 <=exp[100n q0^4/(1-q0)], q0=3exp(-6),

using A<=RP/4 from the same area cutoff. Equation(3) does NOT replace this factor or erase it. Essential-wall labels/activities, phase field budget, and the target majority constraint must likewise remain in GKP's global bound.

## Scope limitation
The result does not cover a hole with filled area>R², disconnected projection data that are not actual filled holes, or an arbitrary externally chosen conditional law. It is a rigorous weighted marked-cover factor within the stated erased-phase contour comparison. In particular it does not treat the actual source current as a Gibbs entrance law.
