# Uniform occupation bound for common damped interacting reservoirs
31 October 2026. Root candidate, not independently accepted yet.

Let R=R_plus, R R^dagger <= g^2 N, [N,R]=R, [H_f,N]=0, J_i=2sqrt(lambda)a_i and initial vacuum. Work first on the global finite cutoff N<=L. Every statement concerns normalized, nonselective joint states (including arbitrary external references and system instrument records). It is not a bound after normalization on a rare selected outcome.

For z>1, F=z^N, M_z=Tr(F rho), and Q_z=Tr(N F rho), conjugating the adjoint generator by F^{-1/2} gives the number-decay term -4lambda(1-1/z)N and an Hermitian interaction term with coefficient c=(z-1)/sqrt(z) multiplying i(R-R^dagger), up to an irrelevant overall sign. The relation R R^dagger<=g^2 N implies for every eta>0

    +/- c i(R-R^dagger) <= eta N + c^2 g^2/eta.

This follows by Cauchy-Schwarz on R^dagger followed by 2ab<=eta a^2+b^2/eta. Choose eta=2lambda(z-1)/z and define Gamma=g^2/lambda. Therefore

    d M_z/dt <= Gamma(z-1) M_z/2 - 2lambda(z-1) Q_z/z.       (1)

There is no dependence on H_f's norm in this moment inequality; its compilation cost remains an entirely separate obligation.

For a normalized state, f(s)=ln Tr(e^{sN}rho) is convex, f(0)=0. At s=ln z>0, convexity gives f'(s)>=f(s)/s. Thus

    Q_z/M_z >= ln M_z / ln z.

Combining with (1), u=ln M_z satisfies

    u' <= a-bu,
    a=Gamma(z-1)/2,
    b=2lambda(z-1)/(z ln z).

Vacuum has u(0)=0, so

    ln M_z(t) <= [g^2 z ln z/(4lambda^2)](1-exp(-bt)).      (2)

This is uniform in the finite cutoff and in time. Trace-preserving system-only instruments, including stored classical outcomes, preserve M_z exactly; consequently the differential comparison composes across all prescribed controls. Conditional postselection does not.

At z=2, write mu=g^2/(4lambda^2). Then

    M_2(t)<=exp[2mu ln2 (1-exp(-lambda t/ln2))]<=2^{2mu}.

The vacuum source tail is P(N>=L)<=2^{2mu-L}. Applying the same finite-to-finite cutoff Duhamel comparison as the accepted domain construction, the only outgoing Hamiltonian block has norm at most g sqrt(L+1). Common loss jumps agree on the embedded lower space and H_f has compatible number-preserving restrictions. Thus the controlled trace-distance estimate is

    2 T g sqrt(L+1) 2^{mu-L/2}.                            (3)

One can take the minimum with the earlier exp(Gamma T/8) bound in the cutoff prefactor. Formula (3) separates the occupation scale g^2/lambda^2 from the total activity scale Gamma T. A finite cutoff L polynomial in 1+mu+log(2+Tg)+log(1/epsilon) suffices after absorbing log(L+1). It does not reduce the accumulated emission-count budget, source preparation cost, or H_f simulation cost automatically.

Important distinction: the jump-count tilted state does not have trace one. The log-moment convexity step above therefore cannot be reused on it without subtracting its log trace and carrying that extra coupled variable. No time-uniform jump-count bound is claimed.

## Domain scope
For an infinite-reservoir conclusion require a self-adjoint direct-sum H_f with compatible sector restrictions, not arbitrary unrelated matrices for different cutoffs. Moment bounds (1)-(2) first hold in every finite model; (3) yields the canonical controlled Cauchy limit. No arbitrary unbounded-generator uniqueness follows.
