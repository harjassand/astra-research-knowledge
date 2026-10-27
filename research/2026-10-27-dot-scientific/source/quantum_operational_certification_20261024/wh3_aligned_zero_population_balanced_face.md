# An analytic lower-population boundary: balanced Schmidt weights

Consider the aligned rank-three program with all six populations aij=0. The input is supported on the maximally correlated subspace and represented by 0<=X<=I, Xu=u, u_i=sqrt(lambda_i). Assume every lambda_i<=1/2. Then the actual anchored gradient g is nonnegative.

Set x_i=Xii. Since X>=uu^T (the top eigenvalue is one and the remaining spectrum is nonnegative), lambda_i<=x_i<=1. The exact pair Rayleigh identity and scalar log Jensen give

 g>=G=sum_i f_{lambda_i}(x_i),
 f_l(x)=l log(x/3)-(1-l) log[(1-2l+l x)/(2(1-l))].

For l>0 the derivative is

 f_l'(x)=l(1-2l)(1-x)/[x(1-2l+l x)].

The denominator is positive on [l,1], since at x=l its second factor is (1-l)^2. Thus for l<=1/2 the function increases and

 G>=sum_i f_{lambda_i}(lambda_i)=g(P;P)=Delta(P)>=0,

where the last pure-input sign is already covered by the proved all-projector theorem. This establishes an entire genuine source boundary face without needing a within-pair log-gap payment.

## One heavy Schmidt weight: the PSD coupling cannot be discarded

If one weight l>1/2, its f_l decreases, whereas the other two increase. Independently optimizing the diagonal intervals is NOT sufficient. At lambda=(2/3,1/6,1/6), it selects the formal diagonal x=(1,1/6,1/6), yielding

 sum_i f_{lambda_i}(x_i)=(1/3)log(3072/3125)<0.

That diagonal is infeasible. X00=1 with X<=I forces the entire offdiagonal first row to vanish. Xu=u then forces the remaining block to have eigenvalue one along (u1,u2); positivity gives X11,X22>=1/2, not 1/6.

A useful necessary diagonal constraint comes from S=X-uu^T>=0 and Su=0:

 sqrt(lambda_0(x_0-lambda_0))
 <=sqrt(lambda_1(x_1-lambda_1))+sqrt(lambda_2(x_2-lambda_2)),

and its cyclic versions. These are the triangle inequalities for the three weighted Gram vectors of S. The exact affine LMI from the main finite-interface note retains the full feasibility. The heavy-weight all-zero-population face remains open in this note.

## Exact failure of concavity on this support

The function g is not concave even when restricted to the all-zero-population face with fixed top vector. Let

 u=(2,1,1)/sqrt(6), q=(0,1,-1)/sqrt(2), w=(-1,1,1)/sqrt(3),
 X(b)=uu^T+(3/10)qq^T+b ww^T.

All three vectors are orthonormal, so X(b) is a valid source for b in [0,1]. Exact rational matrix-log atanh series certify

 g(X(3/5))+g(X(4/5))-2g(X(7/10))>1/2000.

The actual second difference is about 0.00083400574; the rigorous error bound is below 5e-29. See `wh3_maxcorr_concavity_obstruction.py/.json`. Thus an unproved concavity lift from the projection endpoints cannot be used even on this small source face. This is solely a counterexample to that proof mechanism, not to the target entropy inequality.

## Source-paid one-variable envelope for the remaining heavy case

Let a=lambda0>1/2, b=lambda1, c=lambda2, t=b+c=1-a, x=X00. Write S=X-P>=0, Su=0. Since S is supported on u-perp and the squared norm of Qe0 is t,

 S00<=t Tr S,

so the light diagonal increments obey

 (X11-b)+(X22-c)>=(a/t)(x-a).                 (2)

For 0<l<1/2, f_l is increasing and concave on [l,1]. Its chord slope is

 C(l)=[f_l(1)-f_l(l)]/(1-l)
     =log(1-l)-[l/(1-l)]log l >0.

Consequently the exact source and scalar pair Jensen yield

 g>=L(a,b,c,x)
  :=sum_{l=a,b,c} f_l(l)+f_a(x)-f_a(a)
       +(a/t)(x-a) min(C(b),C(c)),

for a>=1/2, b+c=1-a, b,c>0, a<=x<=1. This is a rigorous lower envelope; its universal sign is NOT established here. In terms of s=(x-a)/t, the heavy correction is explicitly

 f_a(x)-f_a(a)=a log(1+t s/a)-t log(1+a s/t),

and the paid chord term is a s min(C(b),C(c)). Proving L>=0 would close the entire remaining all-zero-population face. It cannot be obtained by dropping the paid term: the exact negative formal endpoint above proves that shortcut fails.
