# Exact asymptotic failure that motivates quadratic clipping

Keep the linear clip p*=A²/(B+1) min(tau/2,1), and add any fixed reciprocal
coefficient lambda, negative hub coefficient kappa, and angular coefficient beta>=0:

  W_lin = r^N [ exp(tau)(1+20p*) + lambda P - beta A/(N+1) + kappa R ].

Here P=1/(c+1)+1/(d+1), R=-A/[(c+1)(d+1)]. At
x_n=(A=n,B=n,C=D=E=0), H=tau=0. Only the two forward arms 2A->AC and
2A->AD create positive debt; each successor has

  tau' = a/[2n(n-1)] + O(n^-4).

Its phase is 10(n-1)^2 tau'/(n+1)=a/(2n)*10+O(n^-2).
Each arm therefore contributes .05n+O(1), for a combined .1n+O(1).
The angular baseline increases by beta/(2n+1) under each of the three
2A-source reactions and under AB->CD. Their combined contribution is
2 beta n+O(1). P and R have only O(1) drift on this ray. The true-death
exponential tilt contributes

  -(1-1/r)(1-beta/2)n+O(1).

Hence

  LW_lin(x_n)/r^(2n)
   = [ .1+2 beta-(1-1/r)(1-beta/2) ] n+O(1).

For beta>=0 and 1<r<=1.01 the coefficient is positive. Thus the linear clip
plus a fixed angular baseline cannot be the claimed global Foster function.
Even beta=0 fails. This is not a failure of the accepted tau>=2 charging theorem.

The quadratic clip min(tau²/4,1) changes the two kink phase contributions
from order n to order 1/n. It leaves the full tau>=2 theorem untouched by
successor domination. The negative angular baseline is omitted in the new
candidate, not silently retained with a different numerical coefficient.
