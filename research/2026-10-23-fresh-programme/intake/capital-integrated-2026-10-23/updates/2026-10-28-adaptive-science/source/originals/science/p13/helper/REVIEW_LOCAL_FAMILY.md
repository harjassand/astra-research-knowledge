# Review of the general five-root theorem and local joint-cap family

The proposed generalization is valid, with local resource coverage as its exact scope. I found no sign or normalization error.

For nu>0 and eta>0, the continuous coefficient extension for x>=3 satisfies

`B'''(x)=nu*(96*x-72)+192*eta*((2*x+1)^(-4)-(2*x+2)^(-4))>0`.

Thus B has at most three distinct zeros on that interval by Rolle's theorem; the nonzero integer tail B_n can have at most three sign variations. Its eventual sign is positive because the positive quartic term dominates. If the first nonzero tail sign is negative, its variation count is odd and at most three. The prefix `[-eta,B1,+1 at degree3,B2,first-tail-sign]` then has at most two variations. If the first tail sign is positive, the tail has an even number of variations, at most two, and the prefix has at most three. Zero coefficients are discarded throughout. Hence the full entire-series coefficient list has at most five variations for arbitrary lambda and mu.

The existing finite-sign-variation lemma therefore bounds every such dual to at most five positive roots counted with multiplicity. Five known distinct positive edges are necessarily simple and exhaust the positive roots; eta>0 and nu>0 supply the negative sign near zero and positive sign at infinity. This establishes the all-frequency three-band sign pattern throughout any region where these five roots exist.

For `epsilon=(+1,-1,+1,-1,+1)` and

`z=(ell,T,E,D)=(sum eps log x, sum eps x^2, sum eps x^4, (sum eps x^-2-1/2)/2)`,

the differential vector is exactly `u(x)=(1/x,2*x,4*x^3,-x^-3)`. Since `R(x)=0`, its root differential is `dx=-u(x)^T da/R'(x)` for `a=(lambda,mu,nu,eta)`. Consequently

`Dz/Da=-sum_i [epsilon_i/R'(x_i)]*u(x_i)*u(x_i)^T`.

Every weight is strictly positive by the alternating simple-root signs. Multiplying a linear combination of the four entries of u by x^3 gives a polynomial of degree at most three in x^2. Four distinct positive roots force that polynomial, and hence the coefficient vector, to vanish. Therefore the Jacobian is strictly negative definite and nonsingular.

The analytic inverse function theorem gives an open resource neighborhood around the certified finite joint-cap point. Holding ell and T fixed preserves M=2 and m=1. Strict interlacing, eta>0, nu>0, and positive finite inverse-star masses/springs persist in a sufficiently small neighborhood. Thus varying `(C,kappa)` there gives an actual analytic positive two-pendant design family, globally optimal over every finite internal topology at its respective joint caps. This does not assert global coverage or classify all resource regimes.

At fixed ell and T, endpoint differentiation gives `dJ=-nu*dE-eta*dD`. Since `E=16+8*kappa` for the attaining star and `D=C/4`, the sensitivities are exactly

`dJ/dkappa=-8*nu`, and `dJ/dC=-eta/4`.

For dimensional clarity, ell should use a fixed positive frequency reference, or the text should explicitly state that the frequencies in these coordinates are already dimensionless. This only adds a constant to ell and leaves the Jacobian unchanged.
