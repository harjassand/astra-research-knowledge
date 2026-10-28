# Certified local entropy variables

Assume the separately proved stationary maximizer a* in the Euclidean ball
|A|<=r=1/4000 for the certified five-dimensional box. The root receiver
independently reconstructs the bound -ell_AA>=eI in this ball. For a rational
proposal a in it, the exact linear residual in D(a+Y)[ell_a-ell_(a+Y)] is2l:Y.
Strong monotonicity and D>=sigma² imply

    |a-a*|<=|grad_A ell_a|/e<=2|l|_1/(sigma²e).

For j(A)=grad_z ell_A=(DH+2eA-kcofA,k), C=||H||coeff,1 and P=||pH||coeff,1,
direct differentiation gives |k|<=k0=Pr6/sigma² and
|grad k|<=k1=6Pr5/sigma²+4Pr7/sigma³. Thus

    ||Dj||<=Lj=12Cr²+2e+r k1+k0+k1,

using |cofA|=|A| and ||Dcof||=1. The sum of the two block norms bounds the
stacked output Jacobian. The envelope identity grad G=j(a*)+2kappa z shows
that j(a)+2kappa z has Euclidean, and therefore componentwise, error at most
Lj*2|l|_1/(sigma²e). Newton convergence is not a premise.

gradient_receiver.py executes the bound on both actual off-axis proposals,
without producer imports; GRADIENT_RECEIVER.json stores exact vectors and
errors. This supplies entropy variables as well as values. The receiver uses
the open-box root theorem, not an assertion of roots for arbitrary inputs.
No physical material, PDE solver or practical advantage is acquired.

## Global inverse and conjugate receiver

Global2kappa strong convexity and G>=kappa|z|² imply a unique conjugate
maximizer z*(w). For any z in the smooth box,
|z-z*(w)|<=|grad G(z)-w|/(2kappa). If the rational approximate gradient
is g0 with Euclidean error d, use R=|w-g0|_1+d for any rational w.
The inverse error is at most R/(2kappa). For L<=G(z)<=U, completing
the strong-convexity quadratic also gives

    w:z-U <= G*(w) <= w:z-L+R²/(4kappa).

The executable sets w=g0 for both actual inputs and stores global inverse
and conjugate bounds. This uses established strong convexity. It is a
receiver, not an arbitrary-w proposal solver; poor proposals give wide bounds.
