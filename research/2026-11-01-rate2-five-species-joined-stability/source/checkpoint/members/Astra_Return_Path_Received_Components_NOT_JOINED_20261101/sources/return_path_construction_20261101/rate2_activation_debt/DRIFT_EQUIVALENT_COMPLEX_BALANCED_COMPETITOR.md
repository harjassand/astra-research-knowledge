# Rate-2 tree: exact drift-equivalent complex-balanced competitor

**Author structural component; pending independent review.** This does not say
that the original count chain is complex balanced or has a product-Poisson law.

Let s=(sqrt(7)-1)/2 and h=1-s. Thus 0<s<1, h>0, and
2s^2+2s-3=0. In the original rate-2 model, change only these binary channels:

* reduce 2A->AC and 2A->AD from rate 1 to rate s;
* add 2A->CD at rate h.

Every other rate, including CD->AE=2 and the unit port, is unchanged. The altered
network need not be reversible edge by edge, but its residual cycle is directed
and complex balanced. The original and altered DETERMINISTIC mass-action fields
agree identically, because

  (AC-2A)+(AD-2A)=CD-2A.

The same sourcewise first-moment equality holds for the falling-factorial count
generators. The full generators do NOT agree.

At c=(A1,B=s^2,C=s,D=s,E=2-s), the AC and AD pairs balance individually.
AB and CD have equal monomials s^2 and balance. The residual current h closes

  2A -> CD -> AE -> 2A:

2A->CD carries h; CD->AE has excess 2s^2-(2-s)=h; AE->2A has excess (2-s)-1=h.
The port also balances. Hence the altered model is complex balanced at c and
has its ordinary product-Poisson invariant distribution. This is an ordinary
competitor, not the stationary law of the original model.

For a separable potential V(x)=sum_i g_i(x_i), let a=x_A. At a>=2, direct
subtraction of the two count generators gives the exact identity

  (L_original-L_competitor)V
   =h a(a-1)[2g_A(a-1)-g_A(a-2)-g_A(a)].                  (1)

At a<2 both sides are zero. The C and D increments cancel individually; no
assumption on their sizes is used. Thus, if g_A is discretely convex, the right
side is nonpositive. Convexity of the other summands is not needed for this
particular identity. This is an actual stochastic generator inequality for the
specified potential class, not merely deterministic drift equivalence.

For the deterministic relative-entropy potential

  H(x)=sum_i [x_i log(x_i/c_i)-x_i+c_i],

complex balance of the competitor yields the usual entropy dissipation proof,
and identical vector fields transfer it to the original ODE. One can verify the
sign directly: write the complex-balanced fluxes c^y k_yz and monomial ratios
u_y=x^y/c^y; then use u(log v-log u)<=v-u and cancel inflow/outflow at each
complex. Equality in the connected internal graph forces all binary monomial
ratios equal; the port additionally forces x_A=c_A. Thus the only positive
zero-dissipation point is c. The standard interior deterministic tool is available
without pretending the original stochastic network is complex balanced.

Neither (1), entropy dissipation, nor the competitor's stationary law transfers
positive recurrence by itself: a geometric Foster potential for the competitor
has not been shown to lie in the separable convex class, and deterministic
interior dissipation does not price the actual delayed stochastic boundary phase.
In particular the already proved stretched-exponential geometry obstruction
prevents a bounded-multiplier shortcut. The companion mesoscopic return law is
an independent paid step toward that boundary continuation.
