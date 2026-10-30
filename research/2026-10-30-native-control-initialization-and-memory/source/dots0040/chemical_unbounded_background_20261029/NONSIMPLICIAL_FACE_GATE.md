# Why the upper-frontier construction is not a general recurrence proof

The new moving-fugacity construction acquires strict coefficient inequalities on every adjacent two-vertex exposed face. The restriction to such faces is substantive.

Consider the strongly connected network

    2B --100--> A+B --1--> 2A --100--> 2B,
    2B <--1 / 1--> B.

The maximal total-degree face contains three collinear complexes 2B, A+B, 2A. For a product-Poisson fugacity c=(c_A,c_B), put rho=c_A/c_B. The adjoint defect coefficients at A+B and 2B are

    d_(A+B)=100/rho-1,
    d_(2B)=100 rho^2+1/c_B-101.

Strict negativity of the first requires rho>100, while negativity of the second requires rho<sqrt(101/100)<1.005. Thus no fugacity can make all exposed-face coefficients negative. Taking a larger normal fugacity does not remove the contradiction.

This does not refute recurrence, a more general dual envelope, or even negativity of the weighted sum at one specific physical composition ratio. It disproves the coefficientwise face-selection primitive used in the upper-frontier theorem when a face has three collinear complexes. The actual ratio A/B must matter, or one must solve a non-Poisson face operator.

A possible next representation is an exact killed conservative-shell operator rather than a stationary frozen background. In two dimensions its internal state space grows with total population; finite-phase rational-shift control is not automatically available. Weak reversibility supplies finite enabled paths to a leaking face edge, potentially giving polynomial absorption bounds, but adjacent-shell variation and global dual summability still require proof. No such bounds are assumed here.

In higher dimensions, additional issues arise: faces need not be simplices, the face dynamics is multidimensional, and a proposed moving fugacity field must be the gradient of a single log-density up to controlled errors. Astra N33's deterministic absorbing geometry does not itself settle any of these stochastic adjoint requirements.
