# Full nonaligned product-top anchored-gradient theorem

2026-10-25. Exact dimension-free theorem, retaining the actual channel and actual marginal. This supersedes the overlap threshold as a product-top result. It does not prove the unrestricted WH3 theorem.

## Theorem

Let 0<=X,Y<=I on any finite-dimensional reference space, and Xr=r for a unit vector r. Then

g(X,Y;r)=<r,log((X+2Y)/3)r>
         -2<r,log((X+Y)/2)r> >=0.                    (1)

In fact g>0 unless Yr=r, in which case g=0. All weighted logarithms are taken on their supported subspaces. No commutation or reference-marginal alignment is assumed.

Consequently a negative fixed-reference global minimizer of the actual WH3 entropy deficit cannot have ANY product vector in its maximal eigenspace, even if the minimizer lies on a rank boundary. The receiving argument and twirl are detailed in Section5 below.

## 1. Exact same-pencil identities

Put y=<r,Yr>, and, initially for faithful X,Y,

q(t)=<r,1_(0,infinity)(tY-X)r>,
w(t)=2/[t(t+1)(t+2)].

The accepted balanced binary testing-measure entropy identity gives

g=log(4/3)-integral_0^infinity w(t)q(t)dt,            (2)
integral_0^infinity q(t)/t^2 dt=y.                   (3)

For completeness, (2) is obtained by differentiating the balanced trace entropy with scalar second derivative w. Equation(3) comes from differentiating D(Y||X): its positive-part representation is

D(Y||X)=Tr(Y-X)+integral_0^1 Tr(tY-X)_+/t^2dt
 +integral_1^infinity [Tr(tY-X)_+-tTrY+TrX]/t^2dt.

The derivative in direction |r><r| is minus the integral in (3). Direct differentiation instead gives -<r,Dlog_X(Y)r>=-y because Xr=r. The same pencil is used in both identities; no independent source relaxation is substituted. See nonaligned_product_top_overlap_theorem.md for the complete calibration of (2).

## 2. TWO one-sided variance bounds

Let H_t=tY-X. Its spectral measure in r has

mean mu=ty-1,
variance sigma^2=t^2(<r,Y^2r>-y^2)<=t^2 y(1-y).

The variance identity is exact because H_t r=tYr-r. Scalar Cantelli applied to this spectral measure gives BOTH

q(t)<=U(t):=t^2 y(1-y)/[1-2ty+t^2y],  if t<1/y,
q(t)>=L(t):=(ty-1)^2/[1-2ty+t^2y],   if t>1/y.       (4)

Use q>=0 and q<=1 on the other respective ranges. The second, lower bound is essential: using only an upper cap and the moment in (3) does not prove the theorem. Increasing the variance to t^2 y(1-y) weakens both bounds in the correct directions. No monotonicity of the operator spectral projection in t is claimed.

## 3. Exact dual solution when 1/2<=y<1

Write delta=1-y and define a comparison function

q_*(t)=0,                              0<t<1;
       U(t),                           1<t<1/y;
       1,                              1/y<t<2;
       L(t),                           2<t<infinity.

Since y>=1/2, the endpoints are in the displayed order. The function q_* is not claimed to be a physical quantum pencil. It is an exact source-compatible scalar dual comparison.

The multiplier rho=1/3 has

w(t)-rho/t^2=-(t-1)(t-2)/[3t^2(t+1)(t+2)],

which is positive exactly on (1,2) and negative elsewhere. The bounds (4) therefore imply pointwise

[w(t)-rho/t^2]q(t) <= [w(t)-rho/t^2]q_*(t).          (5)

Crucially, q_* has EXACTLY the required weighted moment:

integral_0^infinity q_*(t)/t^2dt=y.                 (6)

To verify it, use

1-2ty+t^2y=y(t-1)^2+delta,
U(t)/t^2=y delta/[y(t-1)^2+delta],
L(t)/t^2=1/t^2-y delta/[y(t-1)^2+delta].

Thus the left side of (6) is y plus

integral_1^(1/y) y delta/[y(t-1)^2+delta]dt
 -integral_2^infinity y delta/[y(t-1)^2+delta]dt.

These integrals are equal: both equal

sqrt(y delta) arctan(sqrt(delta/y)),

using arctan(a)+arctan(1/a)=pi/2 for a>0. Equations(3),(5),(6) give

integral wq <= integral wq_*.

Finally 0<=q_*<=1_(t>1), and strictly less on a set of positive measure when y<1. Hence

integral wq <= integral wq_* < integral_1^infinity w(t)dt
 =log(4/3).

Equation(2) proves strict positivity in this whole range.

## 4. The remaining overlaps and singular limits

For 0<=y<=1/2, the elementary scalar bound

w(t)t^2<=6-4sqrt(2)

together with (3) gives

g>=log(4/3)-(6-4sqrt(2))y
 >=log(4/3)-(3-2sqrt(2))>0.

For example log(4/3)>1/4>3-2sqrt(2), so the final sign is exact without numerical evaluation. If y=1, positivity of I-Y forces Yr=r, and both mixed matrices in (1) act as identity on r; therefore g=0.

For singular X,Y replace them by X_e=(1-e)X+eI and Y_e=(1-e)Y+eI. Then X_e r=r, the hypotheses persist, and the supported weighted logarithms converge. Since each mixed matrix dominates a positive multiple of |r><r|, no unsupported logarithm occurs. The nonnegative result follows immediately. Strictness for y<1 also follows from the displayed lower bound log(4/3)-integral wq_*, continuous and strictly positive at that y, or from the small-y bound. Thus equality holds exactly when Yr=r.

## 5. Actual WH3 stationary receiver

Let 0<=A<=I and let a tensor r be ANY product vector with A(a tensor r)=a tensor r. Twirl A by physical unitaries in U(1) times U(2) preserving the line a, tensored with identity on reference. This preserves P=|a tensor r><a tensor r| and B=EA exactly. WH covariance and convexity of -Tr NP log NA at fixed B imply that the twirl cannot increase

g_N(A;P)=Tr EP log EA-2Tr NP log NA.

The twirled input is

Abar=|a><a| tensor X+(I-|a><a|) tensor Y,
0<=X,Y<=I, Xr=r.

Its WH output consists of Y on the conjugate-a line and (X+Y)/2 on the physical complement; NP lives on that complement with weight1/2. Hence g_N(A;P)>=g(X,Y;r)>=0.

For the negative-global-minimizer receiving statement, no channel regularization is needed. Let A minimize the entropy deficit on the trace-one positive cone in a fixed finite reference dimension, suppose its deficit is negative, and rescale to ||A||=1. Write tau=TrA. The curve

(A+sP)/(tau+s)

is feasible for sufficiently small positive AND negative s. Its input, output and marginal supports are constant: A>=P, NA>=NP and EA>=EP imply, for 0<e<1, A-eP>=(1-e)A and the analogous output/marginal bounds. Therefore the supported entropy derivatives exist. Homogeneity and top-eigenvalue normalization give

0=d/ds [Delta(A+sP)/(tau+s)] at s=0
 =(tau*g_N(A;P)-Delta(A))/tau^2.

Thus g_N(A;P)=Delta(A)/tau<0, contradicting the product-top theorem. This argument works even when A or NA is singular and does not infer any unproved monotonicity from g_N to g_(N_t). It is a global-minimizer exclusion, not a pointwise assertion Delta(A)>=0 for every input with a product top vector.

The essential new result here is g_N(A;P)>=0 for every physical input possessing a product top vector, with the true marginal kept fixed. The unrestricted problem can still have an entangled top vector and a nonaligned marginal.

## 6. Full entropy corollary: physical-CQ and product-eigenbasis inputs

The anchored theorem yields a genuine POINTWISE full entropy theorem on a preserved spectral class.

Suppose A has an orthonormal eigenbasis consisting of product vectors across physical qutrit and reference. Then

Delta(A)=D(A||EA)-2D(NA||EA)>=0.                     (7)

In particular (7) holds for every physical-classical/quantum-reference input

A=sum_(i=1)^3 |i><i| tensor X_i,

where the X_i are arbitrary positive operators on the same finite-dimensional reference, with no pairwise commutation assumption. This is not limited to a classical reference.

Proof: lower the largest spectral level continuously to the next level while fixing all lower levels. At every interior point, the entire maximal projection is a sum of mutually orthogonal product eigenprojections P_j. The derivative of Delta in the direction of increasing that common top level is the sum of its derivatives in P_j. Each derivative is nonnegative by the anchored theorem after scaling the current maximum to1; the gradient is invariant under positive global scaling. Thus lowering the top level cannot increase Delta. The operation preserves the product eigenbasis. Repeat through the finitely many original levels, finishing at a scalar multiple of identity (or zero if the smallest eigenvalue is zero), where Delta=0. Along each open segment, support-restricted logarithmic derivatives are justified by A>=lambda P_j and channel positivity. At the endpoint where a level reaches zero use entropy continuity. Therefore the original Delta is nonnegative.

The same argument works whenever every cumulative spectral superlevel projection admits a positive decomposition into product rank-one projectors: every product vector in such a decomposition lies in the top eigenspace, and the derivative is the corresponding positive weighted sum of anchored derivatives. No claim is made for arbitrary separable A, whose spectral projections need not have this property.
