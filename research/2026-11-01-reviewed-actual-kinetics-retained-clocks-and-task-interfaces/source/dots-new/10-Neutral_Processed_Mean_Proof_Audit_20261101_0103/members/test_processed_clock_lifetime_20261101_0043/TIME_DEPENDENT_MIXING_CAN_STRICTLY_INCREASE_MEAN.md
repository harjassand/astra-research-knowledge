# The autonomous constant-one comparison does not extend unchanged

Status: exact finite-state construction, 2026-11-01 UTC; independent review
pending. This does not challenge the common-form constant-four upper bound.
It shows that even an additional predetermined REVERSIBLE mixing pulse can
strictly increase mean lifetime above the autonomous reference inverse form.
No arbitrary signed dynamics, feedback, or physical implementation is used.

Let D={0,1,2}, m(i)=1/3, h=1_D, and take the symmetric killed generator

    A = [[1, 0, 0],
         [0, 2, -2],
         [0, -2, 102]].

Thus state 0 is killed at rate 1; states 1 and 2 exchange at rate 2; state 2
is killed at rate 100. This is a genuine finite killed Markov chain. The
conservative part preserves the same uniform measure; killing makes both
propagator directions sub-Markov. All domains and common-form energy estimates
are finite-dimensional and exact.

For v=A^(-1)1_D,

    v=(1,13/25,1/50),
    Q=<1_D,v>_m=77/150.

Let u(t)=exp(-tA)1_D be the forward density from m. Then

    u(0)=1_D,
    u'(0)=-(1,0,100),
    [u_1(t)-u_0(t)]'=1 at t=0.

Hence u_1(t)>u_0(t) for every sufficiently small fixed positive t. Also
v_0-v_1=12/25>0.

Now define the conservative symmetric mixing generator (in positive A sign)

    C = [[1,-1,0],[-1,1,0],[0,0,0]].

It annihilates h=1_D on both sides, is nonnegative, preserves m, and is a
valid additional reversible Markov mixing term. Fix any b>0 and let

    M_b=exp(-bC).

This mixes states 0 and 1, with interchange fraction

    alpha=(1-exp(-2b))/2>0.

If one applies the Markov contraction M_b at the scheduled time t, and
otherwise runs the reference chain, total mean lifetime becomes

    Q + <v,(M_b-I)u(t)>_m
      =Q + alpha (v_0-v_1)(u_1(t)-u_0(t))/3
      >Q.                                                     (1)

The identity follows simply by splitting the occupation integral at t and
using the future reference resolvent v. The intervention is positive,
common-measure preserving, fixes h on both sides, and contracts L2.

An instantaneous map is NOT essential. For any epsilon>0 apply the ordinary
finite-rate time-dependent killed Markov generator

    A+(b/epsilon)C    on [t,t+epsilon],
    A                at all other times.

For every epsilon this has finite rates, is a globally nonexplosive actual
chain, retains the reference form with additional nonnegative dissipation,
and has predetermined processing that fixes h on both sides. Its pulse
operator is exp(-epsilon A-bC), which converges to M_b as epsilon tends to
zero. The occupation accrued during the pulse is at most epsilon. The mean
after the pulse is the continuous function <v,u(t+epsilon)>_m. Therefore its
mean converges to the strictly larger quantity in (1), and is strictly larger
than Q for all sufficiently small positive epsilon. No infinite processing
rate is present in any member of this finite-rate family.

This is a proof of strict increase, not an unbounded ratio construction. The
reference data and full source inverse form are fixed. It demonstrates why a
constant-one stationary variational comparison should not be substituted for
the newly earned nonautonomous constant-four principle.

The protocol is fixed from model parameters and calendar time; it never
observes or branches on the actual state. Density concentration is not
injected: the pulse is doubly stochastic and strictly reduces the difference
between the two coordinates. Its benefit occurs because the coordinate with
larger FUTURE reference lifetime has slightly smaller survivor density at
that early scheduled time.

No external retrieval, mutation, denial, or blocked action was required.
