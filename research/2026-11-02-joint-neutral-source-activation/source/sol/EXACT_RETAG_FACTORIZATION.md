# Exact finite-complex retagging representation

An author-derived algebraic reformulation, not a claimed historical first or a recurrence proof. It preserves the actual embedded chain and its physical clock. No stationary physical fiber is introduced.

Let y range over raw complexes of a finite weakly reversible list. Set d_y=sum_(r:y_r=y) kappa_r and let K(y,y')=sum_(r:y->y') kappa_r/d_y be the finite embedded complex kernel. Every linkage is strongly connected, so acquire a positive stationary vector s for K by finite exact linear algebra or the finite tree formula. Across linkages any positive mixture is allowed.

Represent a physical state as x=z+y with z>=0 and finite mode y. Define two EXACT kernels:

* R retags at fixed physical x: choose a source a<=x with probability d_a(x)_a/q(x), and set (z,y)->(x−a,a).
* T follows the chosen complex edge: (z,a)->(z,b) with probability K(a,b).

The physical marginal of R followed by T is precisely the original embedded chain from EVERY tag representation. Every actual inventory change is retained. The holding time before that pair is Exp(q(x)); hence any integrated reward is restored using its actual 1/q(x), as in the common-envelope note.

On the augmented countable state space, the finite measures

    mu(z,y)=s_y/z!,       lambda(z,y)=d_y/z!

are summable. T preserves mu because it leaves z fixed and sK=s. R preserves lambda because its conditional law at fixed x is exactly

    [d_a/(x−a)!] / sum_(b<=x) [d_b/(x−b)!].

Moreover mu/lambda=s_y/d_y is bounded above and below by positive finite constants. This is a global factorization from the raw list, not a supplied equilibrium/mixing condition.

It does NOT follow that RT preserves either measure, or that the physical process is recurrent. Composition of kernels with different invariant laws needs its own proof. Treating bounded phase-density distortion as that proof would repeat the earlier incomplete-cell/rate-distortion mistake.

For calibration, replace 1/z! by c^z/z!, c_i>0. The two invariant laws coincide exactly when s_y is proportional to d_y c^y on each relevant linkage. This is the ordinary complex-balance compatibility condition. Its physical marginal after retagging is proportional to q(x)c^x/x!, and restoring the holding clock gives the established product-Poisson stationary law c^x/x!. Thus the ordinary complex-balanced route is recovered, not improved.

For generic non-complex-balanced lists the two conditional laws are incompatible. The remaining mathematical problem in this representation is a genuine global stability/occupation theorem for this factorial heat-bath and finite-complex motion, including actual physical time. No such theorem has been earned here. The representation removes a prescribed neighboring-profile law; it does not manufacture the missing stability operation.
