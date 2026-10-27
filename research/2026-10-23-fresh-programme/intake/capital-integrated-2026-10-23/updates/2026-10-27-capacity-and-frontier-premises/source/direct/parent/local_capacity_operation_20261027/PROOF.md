# Direct local variational certificate for an actual rare excursion

Internal construction using ordinary potential theory, Galerkin/CG and a
spectral residual bound. No priority, new complexity class or practical
superiority claimed. This motivates a direct nonquadratic actual-model
calculation beyond the Gaussian-reference conductance envelope.

Let Q be a finite irreducible reversible BACKWARD generator, H=-Q, with
supplied positive unnormalised invariant w, w(a)=1,w(b)=rho<=1. Its gap is
at least supplied g>0 and exit rates are at most supplied Rmax. Inner product
is <f,h>_w=sum w*f*h. Define rational u=rho*1_a-1_b. Then <1,u>=0 and
<u,u>=rho*(1+rho). Established potential/capacity identities give

    I=<u,H^+u>_w/rho,
    f(t)=<u,exp(-tH)u>_w/rho
        =rho*P_t(a,a)+P_t(b,b)-2*rho*P_t(b,a),
    p_exc=rho/(R_a*I), stationary_capacity=rho/(Z*I).

P_t(x,y) means start x, end y; Z=sum w. The continuous-time exit-rate R_a
factor is essential. This is the TRUE exit-law success probability.
Ordinary primary antecedents:
https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch2.S2.html and
https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch3.S7.html .

For ANY finite-support real y, put r=u-Hy and

    L=(2<u,y>_w-<y,Hy>_w)/rho.

Taking x=H^+u and completing the square gives

    I-L=<x-y,H(x-y)>_w/rho=<r,H^+r>_w/rho.

The constant part of y causes no problem. Since r has zero weighted mean,

    L <= I <= L+<r,r>_w/(rho*g).

All terms are finite sums if the support of y and Hy is known. Rational
rates/weights/y give exact rational bounds. Invert a positive L outward for
probability/capacity; nonpositive or wide bounds remain unresolved.

Choose y in span{u,Hu,...,H^(k-1)u} by finite Galerkin equations or exact CG.
Linear dependence needs an independent basis or exact convergence, not an
inverse of a singular moment matrix. For M-site adjacent-pair flips, the
spin graph is an(M-1)-hypercube. Residual support is at most
2*sum_(j=0)^k binomial(M-1,j), counting overlaps once. M24,k3 gives2048
states per ball. This is a finite-cost opportunity, not a polynomial bound
when k grows. BACKWARD sparse H requires predecessor q(x,y) for terms
-q(x,y)*y(y) at x; blindly using forward multiplication is incorrect.

The explicit nonquadratic dynamics preserve w and have conductances at least
the reference ones, hence gap_actual>=gap_reference. Local contexts and
weights are generated without enumerating all states; Gaussianity is not
needed. Source uncertainty still needs valid weight/rate boxes. This does
not acquire global locality/reversibility/support from finite data.

## Equally informed ordinary Monte Carlo

Under these same promises rarity alone is not a1/p sampling barrier. Symmetric
spectrum gives mu=(1+rho)/(2Rmax)<=I and
tail(T)<=(1+rho)*exp(-g*T)/g. Choose tail<=eta*mu. For uniform t in[0,T]
and independent exact-law simulations from a,b, use

    Y=T*[rho*1{Xa_t=a}+1{Xb_t=b}-2rho*1{Xb_t=a}].

E Y=integral_0^T f. Range length <=(1+3rho)*T<=4T. Hoeffding gives additive
eta*mu error with failure delta for

    N>=((1+3rho)^2*T^2/(2*eta^2*mu^2))*log(2/delta).

Add the nonnegative tail, intersect with I>=mu and invert. eta=O(epsilon)
provides relative probability coverage on this event. Statistical confidence
is distinct from deterministic arithmetic enclosure. Efficient finite-time
simulation and honest independent randomness are premises; this is a
sample/event argument, not a claimed full exact finite-bit simulator proof.

Uniformisation at Rmax needs expected O(Rmax*T) events per trajectory. For
bounded local rates and polynomial inverse gap, sample/event cost is
polynomial in size and1/epsilon without1/p. Computational initialisation at
a/b is not free physical preparation for empirical validation. Tiny gap,
unknown invariant ratio, misspecified source or inaccessible calibration
remain real barriers. Ordinary methods receive this complete derivation.

Direct CG success should therefore establish an executed deterministic
certificate for the specified actual model, without claiming a new generic
rarity tractability class.
