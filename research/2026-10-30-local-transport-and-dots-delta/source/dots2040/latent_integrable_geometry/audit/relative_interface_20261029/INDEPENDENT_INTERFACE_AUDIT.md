# Independent attack on rounded-kernel relative arithmetic

2026-10-29. Ordinary working proof/test notes. No full Toda arithmetic theorem, discovery priority, or implementation certification is asserted.

## Finding

I tried to break the hardest claim: an arbitrary normalized exact kernel of a rounded evaluation matrix suffices, even as the original divisor becomes conjugate to the reference divisor. The raw interpolation singular-value counterexample is valid, but **does not break this claim**. The residual-to-same-sheet-zero argument needs no continuity of the chosen kernel. Its use is legitimate provided the prescribed points are first separated, the matching is performed on the curve rather than just in x, and the globally unique effective representative argument is retained.

The draft's norm proof, Harnack zero proof, and nonspecial inverse-collar argument survive this review. In particular, choosing any one of several nearby zeros is not an untracked branch ambiguity: every resulting effective residual divisor has a directly controlled Abel class, and the collar plus global nonspeciality supplies the necessary physical proximity. This statement is conditional on the actual quantitative separation/matching implementation, not on a favorable singular value.

Here are explicit repairs for that interface. They are proofs of this interface, not acceptance of the whole end-to-end algorithm.

## 1. Three candidates suffice even at exact conjugacy

For one oval write its circle coordinate as u=exp(i theta). Given the three original inputs (D,D,iota D0), process them in order. Fix 0<h<=1/100. For each original angle a consider a,a+8h,a+16h. Each candidate is within 16h of a. Distinct candidates have chord distance at least 2 sin(4h)>7h. Declare a candidate usable if its chord distance to every previously accepted point exceeds 2h.

One prior point can rule out at most one candidate: otherwise two candidates would be within 4h. There are at most two prior points, hence one candidate survives. The accepted pairwise chord separation exceeds 2h. This includes branch endpoints, where separation in x alone would be quadratic and inadequate.

A certified implementation can calculate every chord to additive error <=h/8 and accept only if its computed value exceeds 2h. Then accepted true separation exceeds 15h/8. A candidate rejected on the uncertain side lies at distance <=17h/8 from that prior point; two such candidates would be within 17h/4<7h, so the same counting proof guarantees progress. This avoids equality-oracle assumptions.

Rotations can instead be rational circle rotations with t=tangent(4h), rounded with certified error; shrinking the above constants slightly leaves all inequalities strict. Alternatively evaluate sin/cos with intervals. Near-conjugate distance never appears in the required precision.

## 2. Explicit separation on the actual curve

Use M>=1, 0<Delta<=1. On oval j, set r=(beta-alpha)/2>=Delta/2, c=(alpha+beta)/2, Q(x)=-product of the 2g excluded branch factors, and W=sqrt(Q) with the physical sign. In the complex tube of x-distance <=Delta/8 from the gap interval, no excluded factor vanishes and |W|>=(Delta/2)^g, |W'/W|<=2g/Delta. The square root is single valued on this tube.

Set Y=2(2M+1)^(g+1). For |y|<=Y the inverse circle expression

    zeta(x,y)=(x-c)/r + i*y/(r*W(x))

has Lipschitz constant (using the ambient l1 metric) at most

    Lambda=10(g+1)(2M+1)^(g+1)(2/Delta)^(g+3).

Indeed |partial_y zeta|<=(2/Delta)^(g+1), while
|partial_x zeta|<=2/Delta+(2/Delta)*Y*(2/Delta)^g*(2g/Delta), which is below Lambda. Line segments in this convex tube establish the finite-difference bound. On the physical curve zeta=exp(i theta). Consequently the separated prescribed points on one oval have ambient separation >=h/Lambda. Points on different ovals already have x separation >=Delta.

Define

    d0=min(Delta/32,h/(100 Lambda)).

Ambient balls of radius 4d0 about all prescribed points are disjoint. Their y-coordinates remain in the stated Y range. There is no singular division by sin(theta) or by y.

## 3. The zero theorem can target those balls with polynomial precision

For the explicit ordinary and branch charts in HYPERELLIPTIC_ROBUST_ARITHMETIC_LEMMAS.md, a safe bound on |x'|+|y'| on their unit disks is

    C_chart=100(g+1)(2M+2)^(2g+2)(128/Delta)^(g+2).

Ordinary charts: each branch factor has modulus >=Delta/128, so |y|>=(Delta/128)^(g+1), and y'=s F'/(2y). Branch charts: differentiate s z sqrt(F_E(E+s²z²)); the excluded factors stay >=Delta/2. These elementary estimates give the displayed deliberately loose constant.

Let rho<=min(1/4,d0/(4 C_chart)). A zero within chart radius rho is within ambient distance d0/4. If (A,B) has max coefficient 1, rounding every evaluation entry to absolute error <=2^-q gives

    |f(P_i)| <= (3g+1) 2^-q.

With U,u,K=8g as explicitly defined in the companion lemma, it suffices to choose an integer q strictly larger than

    log2(3g+1)+3log2(1/u)+2log2(U)+3K log2(2/rho).

This proves existence of a zero on the correct curve sheet in every disjoint prescribed ball, for *any* rational kernel vector. All logarithms are polynomial in g, log M, log(1/Delta), log(1/h). No inverse interpolation singular value or inverse near-conjugate distance enters.

For a prescribed direct Abel error budget tau, require h<=tau/(100g J_col), where

    J_col=sqrt(g) max(1,M^(g-1)) Delta^-g.

The perturbations contribute at most 48g J_col h. IMPORTANT: the existence radius rho is not automatically the displacement of an arbitrarily selected zero in a larger matching ball. To bound the latter, further shrink d0 before setting rho so that

    d0<=min(tau/(100g Lambda J_complex),rho_col/(100 Lambda)),
    J_complex=sqrt(g) max(1,(2M)^(g-1)) (2/Delta)^g,
    rho_col=Delta/(16M).

For any selected zero within ambient d0, the inverse circle expression gives a unique angle increment of modulus <=2 Lambda d0, by the local logarithm at the original unit-circle coordinate. This is inside the complex collar. Its Abel displacement is <=2 J_complex Lambda d0. Summing 3g selected zeros contributes <=6g J_complex Lambda d0<=0.06 tau. Thus the pre-projection direct torus error is below tau. To budget the final projection, reduce tau by the explicit collar inverse/forward Lipschitz amplification and require tau<eta_col; this is still polynomial in logarithmic precision.

This extra inequality closes a real logical trap: the inner existence radius alone cannot be used to charge the error of a zero chosen from an outer selection radius.

## 4. Root matching without a boundary decision or compositum explosion

Compute the exact rational norm polynomial and all its finite roots with multiplicities, plus the two infinity multiplicities, as in the draft. Split common factors first; attach the exact sheet y=-A0/B0 for reduced roots and both sheets for ordinary common-factor roots. At branch roots use the stated ramification multiplicities. A candidate zero is an occurrence in this divisor, not merely a distinct x-root.

Approximate every finite curve point and prescribed center to ambient error <=d0/16. Accept an occurrence when its computed distance to the center is <d0/2. An occurrence guaranteed within d0/4 is certainly accepted; anything accepted is truly within 5d0/8. No occurrence can be accepted for two centers, since the larger balls are disjoint. Thus remove one occurrence per center, preserving all others. The algorithm never needs to decide whether a root lies exactly on an arbitrarily chosen boundary. Infinity occurrences cannot be selected for finite centers and remain in the residual until the collar theorem excludes them.

Resultant-based denominator bounds and exact rational root separation are required to compute these ambient approximations; they cannot be replaced by an assumed sheet denominator margin. Their heights are polynomial in the rounded kernel height.

A precision implementation must not build the compositum of all branch roots. Each prescribed oval point can be represented using its own pair alpha,beta and rational circle coordinates; mu=c+r cos(theta) lies in a field of degree <=d(d-1), d=2g+2. Then y is obtained by one square root of F(mu), or W from -F(mu)/((mu-alpha)(mu-beta)) with endpoint-safe polynomial division. This has polynomial algebraic degree. Evaluate entries independently with intervals, round to rationals, and only then do matrix elimination. Do not perform exact matrix elimination in the joint algebraic field. The rational kernel has polynomial bit height by integer minor/Hadamard bounds, including rank-deficient matrices.

## 5. Hostile executable receipt

`rounded_kernel_test.py` builds exact rational rounded kernels at q=256 and uses exact rational complex polynomial isolation to count all quartic roots. It tests near conjugacy at 2^-60, exact conjugacy, branch-edge coincidence, and opposite edges on y²=(x²-4)(x²-1). All cases have matrix rank 3 and four simple finite norm roots. Coefficient bit lengths are 250--748; same-sheet numerical matching errors are <=1.7e-71. Full numbers are in `rounded_kernel_test.json`.

This is **genus one**, not an N>=3 Toda instance. Root-count isolation is certified; same-sheet distances in this receipt are high-precision diagnostics, not interval-certified distances. The uniform proofs above apply to higher genus, but there is not yet an implemented higher-genus, closed-gap, repeated-doubling regression or end-to-end complexity receipt here. Those remain required before accepting a full certified Toda arithmetic theorem.
