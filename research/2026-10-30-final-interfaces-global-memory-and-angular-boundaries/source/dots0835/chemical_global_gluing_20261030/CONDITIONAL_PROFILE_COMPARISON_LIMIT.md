# Do not generalize the earned shell comparison across frozen catalyst phases

A simple exact obstruction limits the next generalization. Consider the reversible conservative fast network

    A <--> C (rates1,1),
    E+A <--> E+C (rates10,1).

Freeze E=k and A+C=N. The exact stationary A profile is Binomial(N,p_k), where

    p_k=(1+k)/(2+11k).

For adjacent catalyst values k=1,2, p_1=2/13 and p_2=1/8. At A=N,

    sigma_(N,2)(N)/sigma_(N,1)(N)=(13/16)^N.

The Hellinger affinity is

    [sqrt(p_1 p_2)+sqrt((1−p_1)(1−p_2))]^N→0.

Thus a one-particle change in a bounded catalyst phase can change the conditional conservative-shell profile exponentially in N. No polynomial neighboring-profile comparison holds merely because each frozen phase is a perfectly reversible mass-action chain. This is not a recurrence counterexample and does not invalidate the explicitly derived neighboring-N comparison for the earlier fast chain.

A general replacement must keep finite catalyst switching and conservative composition JOINTLY in the growing-shell operator when they interact this way. Assuming instantaneous conditional equilibration or uniform comparison of the separately frozen profiles would supply the missing capability. This example prevents treating the successful one-component Green calculation as a universal infinite-fiber estimate.
