# Arbitrary-weight three-block pure-success reset: whole value by joint stationarity

Status: independently received PASS in `arbitrary_weight_three_block_pure_success_independent_audit.md` (26 October 2026). All prior boundary receivers are explicitly identified below. The new ingredient is an exact scalar single-crossing lemma, not convexity or permutation balancing.

## Statement

Let s,v_1,v_2,v_3 be arbitrary unit logical vectors in any finite dimension. For nonnegative w_i summing to one and p+q=1, the actual TP channel

E(rho)=p rho tensor P_s+q Tr(rho) sum_i w_i |i><i| tensor P_vi

has nonnegative WH3 Choi deficit. For 0<p<1, equality holds exactly when every occupied reset vector is orthogonal to s, equivalently sum_i w_i |<s,v_i>|^2=0.

The physical reset is block diagonal with at most three pure logical blocks, and success is pure logical. This is not arbitrary mixed logical blocks, arbitrary physical coherence, or arbitrary mixed logical success.

## 1. Actual source coordinates and exact scalar integral

Use the actual dual Gram source from `three_block_pure_success_dual_star_interface.md`. Set

d=p/3, x_i=q w_i, b_i=x_i/3, c_i=sqrt(d x_i r_i), r_i=|<s,v_i>|^2.

Then 3d+3 sum_i b_i=1 and 0<=c_i^2<=3d b_i. The exact input blocks are T_i=[[d,c_i],[c_i,3b_i]]. The changing reference arrowhead R has center3d, leaves b_i and couplings c_i/sqrt3. The normalized output pair O_ij has center d, leaves b_i,b_j and couplings c_i/sqrt6,c_j/sqrt6. Spectators cancel as recorded in the interface. All spectral formulas are from an actual TP source.

For interior parameters put

u_i(t)=d-c_i^2/[3(b_i+t)], U=sum_i u_i,

G_t(u;d)=-3 sum_i log[(u_i+3t)/(d+3t)]
          -log[(U+t)/(3d+t)]
          +2 sum_{i<j} log[(u_i+u_j+2t)/(2d+2t)].

The homogeneous deficit satisfies exactly

Delta=integral_0^infinity G_t(u(t);d) dt.                     (1)

This is obtained by subtracting the zero-coherence source in the determinant representation and replacing the input resolvent parameter by 3t. The exact derivation and independent value/gradient replay are in `three_star_scalar_resolvent_stationarity_interface.md` and `three_star_resolvent_stationarity_check.py`.

Write

G_i(t)=partial_{u_i}G_t
      =-3/(u_i+3t)-1/(U+t)
        +2/(u_i+u_j+2t)+2/(u_i+u_k+2t).                     (2)

We prove each G_i(t) has exactly one negative-to-positive crossing on (0,infinity).

## 2. Scalar zero geometry

First freeze positive a,b,c and consider

g_t(a,b,c)=-3/(a+3t)-1/(a+b+c+t)+2/(a+b+2t)+2/(a+c+2t).

Its positive denominator has numerator

N(t)=(4a+6b+6c)t^2+(2a^2+2ab+2ac-6bc)t
     -a^2b-a^2c-ab^2-6abc-ac^2-3b^2c-3bc^2.

Its leading coefficient is positive and its constant coefficient negative. Hence it has exactly one positive root. Assuming b<=c, substitution gives

g_b=-1/(a+3b)+1/(a+c+2b)<=0,
g_c=-1/(a+3c)+1/(a+b+2c)>=0.

The positive root therefore lies in [b,c]. Put m=(b+c)/2, v=(b-c)/2. An exact factorization is

N(t)=2[(a+3m)(t-m)(a+m+2t)+v^2(2a+3m+3t)].

Consequently the root is at most m, strictly below m if b!=c.

Now examine a zero at t=1. Set A=a+3, D=a+b+c+1 and let B,C denote a+b+2,a+c+2 in increasing order. The preceding facts imply

B<=A<=D<=C.

For reciprocals v=1/B, x=1/A, y=1/D, u=1/C, this becomes

v>=x>=y>=u>0.

The zero equation and the denominator identity A+D=B+C give

2(u+v)=3x+y,  1/x+1/y=1/u+1/v.                         (3)

The derivative in a is

partial_a g_1=3x^2+y^2-2u^2-2v^2
             =(3/4)(x-y)^2-(v-u)^2<=0.                 (4)

The derivatives in b and c are y^2-2u^2 and y^2-2v^2, in some order. Both are strictly negative. To verify the only nontrivial one, put T=x/y>=1. The numbers u/y,v/y have sum (3T+1)/2 and product T(3T+1)/[2(T+1)]. Their quadratic evaluated at 3/4 equals

(6T^2-7T+3)/[16(T+1)]>0.

The quadratic vertex is (3T+1)/4>=1, so 3/4 lies strictly below its smaller root u/y. Thus u/y>3/4>1/sqrt2, proving y^2-2u^2<0. The numerator positivity follows, for example, from its negative discriminant 49-72 and positive leading coefficient.

The exact polynomial identities are replayed by `three_star_single_crossing_symbolic_check.py`.

## 3. Actual resolvent paths have one crossing

For the actual source,

u_i(t)/t=d(1-r_i)/t+d r_i/(b_i+t).

Every one of these positive ratios strictly decreases on (0,infinity) at interior parameters. By homogeneity,

G_i(t)=(1/t) g_1(u_i(t)/t,u_j(t)/t,u_k(t)/t).

At every zero, (4) and the strictly negative companion derivatives show that the derivative of g_1 along this path is strictly positive. Therefore every zero is a strict upward crossing. At t=0 the limiting values u_i(0)=d(1-r_i) are positive, and the constant term of N shows G_i(0)<0. At infinity, u_i(t)=d+O(1/t), and

G_i(t)=4d/(3t^2)+O(1/t^3)>0.

Continuity plus strict upward crossing at every zero proves there is exactly one zero theta_i>0, with G_i<0 below theta_i and G_i>0 above it.

## 4. Joint stationary equations contradict this crossing

Differentiating the exact integral (1) gives

partial_{c_i}Delta=-(2c_i/3) integral G_i(t)/(b_i+t) dt,
partial_{b_i}Delta=(c_i^2/3) integral G_i(t)/(b_i+t)^2 dt.       (5)

At a stationary point all c_i>0, so the first expression implies

integral G_i(t)/(b_i+t) dt=0.

The strict one-crossing property then implies

integral G_i(t) dt
 =integral (t-theta_i)G_i(t)/(b_i+t) dt>0,

integral G_i(t)/(b_i+t)^2 dt
 =integral [1/(b_i+t)-1/(b_i+theta_i)]G_i(t)/(b_i+t) dt<0.    (6)

All these integrals converge; near infinity G_i=O(t^-2), and at zero the interior denominators are positive.

For the d derivative, all u_i have partial_d u_i=1. The explicit baseline derivative in G integrates to zero:

integral_0^infinity [9/(d+3t)+3/(3d+t)-6/(d+t)]dt=0.

For example each equal-coordinate baseline kernel integrates to zero because an antiderivative is -log(d+3t)-log(3d+t)+2log(d+t), with the same limit -log3 at both endpoints. Therefore

partial_d Delta=sum_i integral G_i(t)dt>0,
while partial_{b_i}Delta<0 for every i.                    (7)

But the actual normalization constraint is 3d+3 sum_i b_i=1. The original coordinates (p,w_i,r_i) and (d,b_i,c_i) are locally equivalent on the strict interior: r_i=c_i^2/(3d b_i), so all small affine variations satisfying normalization and strict positivity are actual TP sources. At an interior constrained stationary point, the derivatives in d and every b_i must be equal. Equation (7) makes that impossible. Thus the entire normalized family has no interior stationary point. This conclusion is not a generic entropy-convexity statement.

## 5. Compact boundary receiving proves the value

The normalized parameter domain is compact and Delta is continuous. A negative value would yield a negative global minimum.

* If p=0 or q=0, the deficit is zero.
* If a physical weight is zero, the source is in the received two-physical-block theorem (`two_physical_block_mixed_reset_value_theorem.md` and its audit).
* If an overlap r_i is zero, that reference reset sector is orthogonal to success and all other physical reset sectors. It has zero homogeneous deficit. Removing it leaves an actual two-physical-block source after normalization, again received.
* If all overlaps are one, the source is the received arbitrary-qutrit mixed-reset theorem (`arbitrary_qutrit_mixed_reset_value_theorem.md` and its audit).
* If exactly one or two overlaps equal one, the point is not a local minimum. The exact inward expansion and strict positive t log t coefficient are proved in `three_block_pure_success_boundary_stationarity_reduction.md`.

Consequently a negative global minimum would have to be interior. Section 4 excludes it, proving nonnegativity throughout.

The same argument gives the stated equality classification. An interior zero would be a global minimum and is impossible. Proper saturated faces cannot minimize. The fully saturated source is strictly positive at p,q>0 by the qutrit theorem. On zero-weight or zero-overlap boundaries the received two-block equality classification is orthogonality of all occupied reset logical support to success. Thus for p,q>0 the only zeros are sum_i w_i r_i=0.

## Scope and mechanism failures retained

The proof does not use generic affine convexity, pair affine averaging, or full three-label permutation averaging; all three fail on actual positive-deficit sources. The last failure and its rational witness are preserved in `three_star_full_balancing_failure.md`. The present replacement is joint stationarity with an exact scalar crossing inherited from the constrained source resolvents. No arbitrary mixed three-block or unrestricted WH3 value theorem is inferred.
