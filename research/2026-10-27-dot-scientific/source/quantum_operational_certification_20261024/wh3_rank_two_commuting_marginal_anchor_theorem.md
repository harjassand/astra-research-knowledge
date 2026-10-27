# Actual WH3 maximal gradient: Schmidt rank at most two and commuting marginals

## Statement
Let N=W3 tensor id, E=I3/3 tensor Tr_A, 0<A<=I, A psi=psi, and P=|psi><psi|. Assume [Tr_A A,Tr_A P]=0 and psi has Schmidt rank at most two. Then

 g(A;P)=Tr EP log EA - 2 Tr NP log NA >=0.

This is an actual-channel anchored gradient theorem; no Jensen replacement of N squared is made. It does not settle Schmidt rank three or noncommuting marginals, and does not alone prove the full entropy inequality for every state having a rank-two top vector: spectral flattening must preserve the hypotheses at every subsequent top eigenspace.

## Source-preserving reduction
Use the phase-twirl proof in `wh3_anchored_phase_covariant_finite_interface.md`. At fixed EA, g is convex in A. The joint physical/reference phase twirl fixes P and EA, and covariance fixes NP in the transformed output representation. Thus the twirled A has g no larger than the original. It suffices to treat the finite twirled face, with unused reference dimensions contributing nothing to either anchored trace.

## Schmidt rank two
Write psi=sqrt(lambda0)|00>+sqrt(lambda1)|11>, with positive lambdas summing to one. On span{|00>,|11>}, the twirled input is

 X=uu*+t(I-uu*),  0<=t<=1,
 u=(sqrt(lambda0),sqrt(lambda1)).

Set p=a20, q=a21 (the populations on |20>,|21>), and rj=(Tr_A A)jj. Then 0<=p,q<=1 and 0<rj<=3. Put v=(sqrt(lambda1),-sqrt(lambda0)), a unit vector. The exact anchored expression is

 g=lambda0 log(r0/3)+lambda1 log(r1/3)-v*log K v
   -lambda0 log((r0-p)/2)-lambda1 log((r1-q)/2),
 K=1/2 [[X11+q,-X01],[-X10,X00+p]].

The top-eigenvector relation yields the exact cancellation

 v*Kv=(1+lambda0 p+lambda1 q)/2.

Indeed lambda1 X11+lambda0 X00+2 sqrt(lambda0 lambda1) X01=1, independent of t. Scalar spectral Jensen gives v*log K v<=log(v*Kv). Let z=lambda0 p+lambda1 q in [0,1]. Since rj<=3,

 g >= log(4/3)-lambda0 log(1-p/r0)-lambda1 log(1-q/r1)-log(1+z)
   >= log(4/3)-lambda0 log(1-p/3)-lambda1 log(1-q/3)-log(1+z)
   >= log(4/3)-log(1-z/3)-log(1+z)
   = log[4/(3+2z-z^2)] >=0.

The last inequality is 3+2z-z^2=4-(1-z)^2<=4. Faithfulness ensures the displayed logs are finite; singular supported limits follow by regularization whenever the anchored quantity is defined.

## Schmidt rank one
The twirled relevant reference block is diag(1,a,b), 0<=a,b<=1. Its marginal is r=1+a+b. Direct calculation gives

 g=log[4(1+a+b)/(3(1+a)(1+b))] >=0,

because 4(1+a+b)-3(1+a)(1+b)=1+a+b-3ab is bilinear and nonnegative at all four corners of the unit square.

## Scope and next boundary
This closes the full actual-N finite convex program for Schmidt ranks one and two under the commuting-marginal hypothesis. The bound can be zero only at z=1 in the rank-two scalar estimate; no claim of exhaustive equality classification is needed. Schmidt rank three still has three coupled 2x2 output blocks, and the t-independent single-block cancellation no longer directly eliminates the source variables.
