# Why the scalar integrated-path join fails for noncommuting noise

31 October 2026. An explicit standard commutator-loop obstruction, retained as a useful failed transfer. It is not an averaged-channel lower bound or a novelty claim.

Let A1,A2 be bounded Hermitian matrices with nonzero commutator. Put B=A1+A2 and C=A1-A2. On [0,1], take N identical four-piece cycles, with velocities of the two integrated coordinates proportional to

(+1,+1), (+1,-1), (-1,-1), (-1,+1).

Each piece has duration 1/(4N). At fixed diffusion parameter gamma>0 choose lambda=2N and speed c=sqrt(gamma*lambda), so the signed displacement per piece is h=c/(4N)=sqrt(2gamma)/(4sqrt(N)). Each coordinate path stays within 2h of zero and returns to zero at the end of each cycle.

The chronological system generators on a cycle are cB,cC,-cB,-cC. Its propagator is

U_cycle=exp(ihC) exp(ihB) exp(-ihC) exp(-ihB)
       =exp(-2h^2[A1,A2]+O(h^3)).

The bounded-matrix commutator expansion is uniform as h->0. Since N h^2=gamma/8 and N h^3->0,

U_cycle^N -> exp[-(gamma/4)[A1,A2]],

which need not be the identity. For A1=X,A2=Z it is exp(i gamma Y/2), a nontrivial rotation for generic gamma.

Thus both scalar integrated coordinates converge uniformly to zero, but the corresponding time-ordered propagator does not converge to the zero-noise propagator. A pathwise receiver bound depending only on the sup errors in the separate scalar integrals cannot handle arbitrary noncommuting noise. Signed area and higher ordering information matter.

The sign patterns use finite telegraph-type flips. Exact prescribed flip times have probability zero under a continuous Poisson law, and nearby patterns need not have appreciable probability as N grows. Consequently this example does NOT prove that averaged telegraph simulation is hard, that stochastic approximations necessarily fail, or that the newly constructed damped-ancilla/first-event method is obstructed. It rules out transferring the scalar uniform-path continuity argument without additional stochastic/ordering machinery. The positive quantum-reservoir construction avoids assuming that false transfer.
