# Near-harmonic smallness is tied to the encoded physical clock

29 October2026. Root analytic consequence of the ordinary variational
equation. No novelty, computation-precision lower bound or device claim.
This checks the interpretation of the analytic-well result rather than
changing its accepted source geometry. No numerical run is needed.

Let V(q)=|q|^2/2+W(q), with ||D^2W||_global<=eta, and consider two
trajectories of dot q=p, dot p=-grad V. Their phase differences xi,nu
satisfy

    dot xi=nu,
    dot nu=-xi-[grad W(q)-grad W(q_tilde)].

The DIFFERENCE energy E=(|xi|^2+|nu|^2)/2 therefore obeys

    E'=-nu dot[grad W(q)-grad W(q_tilde)]<=eta E.

Consequently the full phase flow has Lipschitz bound exp(eta |t|/2),
and every variational Lyapunov exponent has absolute value<=eta/2.
The negative-time statement uses the same norm-one harmonic propagator.
Convexity eta<1 is not needed for this difference estimate.

If an invariant compact smooth embedding realizes a target flow Y at
physical speed epsilon, including an independent unit clock, every
positive target Lyapunov exponent lambda_Y becomes epsilon lambda_Y.
Compact smooth conjugacy has bounded tangent map/inverse for each fixed
epsilon, so these asymptotic exponents are unchanged by the embedding.
It follows NECESSARILY that

    eta >=2epsilon lambda_Y.                            (1)

This is an exact consistency check: a family retaining a chaotic target
cannot have eta=o(epsilon) while its encoded physical speed is epsilon.
Small perturbation alone is not an acceleration/robustness theorem.
The existing construction permits clock slowing and does not assert
the forbidden rate. A universal computational source need not have a
positive Lyapunov exponent, so(1) is not a general computing lower bound.

If W is bounded by delta on the global complex Euclidean tube
||Im q||<a, Cauchy's estimate on the complex line q+zv, |v|=1, gives

    |v^T D^2W(q)v|<=2delta/a^2.

For a real symmetric Hessian this bounds its operator norm. Thus the
stronger fixed-tube version of the constructor also must satisfy

    delta >=a^2 epsilon lambda_Y                         (2)

whenever that positive-exponent target is embedded. A fixed analytic
norm strengthens representation regularity but does not remove its
physical clock tradeoff.

The sufficient finite-time initial-error requirement from the upper
Lipschitz bound is not a necessary precision lower bound on all
trajectories. Actual hardware initialization, noise correction and
finite-time computation require a separate argument. Hamiltonian volume
preservation likewise prevents claiming an attracting error-correcting
basin from this exact invariant-torus theorem alone. Ordinary friction
in a unique-minimum natural well drains energy; it is not free
restoration of a nontrivial encoded trajectory.
