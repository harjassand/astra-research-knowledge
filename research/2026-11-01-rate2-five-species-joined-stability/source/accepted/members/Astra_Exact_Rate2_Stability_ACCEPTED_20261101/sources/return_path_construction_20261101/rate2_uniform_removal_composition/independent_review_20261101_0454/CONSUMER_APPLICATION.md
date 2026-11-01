# Applying the accepted sampled consumer to this exact rate-2 chain

**PASS as an application of the received uniform block and the final accepted
consumer.** The exact consumer source is
`sampled_return_consumer_root_20261101/PAID_ACTIVATION_TO_STATIONARY_MOMENT.md`,
SHA-256 `a4d41076e1c5cfaa9448d276a71fe0e3055de89560405334760598c83ce0dff4`.
Its final source binding and ordinary proof receipt in
`sampled_return_consumer_audit_20261101_ta90776j/` were read. Earlier drafts are
not used. This application depends on the exact accepted block reviewed in
`INDEPENDENT_COMPOSITION_REVIEW.md` and its qualified dependency receipts.

## Actual-chain hypotheses, including communication

The state space is Z_+^5, and every total-population sublevel is finite. There
are twelve possible outgoing channels, each of finite rate at each state.
Internal reactions conserve total, the sole increasing port is unit immigration,
and actual A deaths decrease total. Thus under every initial state

    S(t)<=S(0)+I(t)

for the same-rate unit Poisson immigration counter. This bounds the state in a
finite set on each finite time interval, giving nonexplosion by finite-rate
localization. No Poisson stationary distribution is assumed.

Irreducibility follows from the following explicit positive-rate paths.
From any nonzero state, add one A by immigration if needed. Each C,D,E can then
be converted to one additional A by `AC->2A`, `AD->2A`, `AE->2A`. Each B can
be converted to one additional A through

    AB -> CD -> AE -> 2A.

This consumes one B and returns the existing A together with the converted A.
Intermediate complexes are enabled even when the single assisting A was
consumed in the first step. After converting all satellites, remove all A by
the actual death channel to reach zero.

Conversely, for a desired state x of total n, immigrate n+1 copies of A from
zero. Produce each desired C,D,E through `2A->AC`, `2A->AD`, `2A->AE`.
Produce each desired B through

    2A -> AE -> CD -> AB.

Before each conversion at least two A remain, because the construction retains
one extra A beyond the target. End with the desired satellites and x_A+1 A;
remove the extra A by death. All steps have positive actual rate, including
coefficient two on CD->AE where used. Finite paths with exponential holding
times have positive probability. Hence every pair of states communicates.
This argument uses only positivity of the actual rate-2 channels, not rate-1
detailed balance or product-Poisson stability.

## Exact parameters and positive tilt

For every state choose the deterministic duration

    d(x)=1+10^8 sqrt(S(x)).

For all states it has lower bound d0=1 and upper bound
`D(1+S(x)^(1/2))` with D=100000001. For sufficiently large N, the independently
received uniform block gives (H) with

    a=1/2, delta_remove=1/16, p=32, c=10^-6, lambda=1.

Take the sampled tilt `theta=10^-16`. Since `0<=2theta<=1`, convexity on [0,1]
and e<3 imply `exp(2theta)-1<=4theta`. Therefore

    D(exp(2theta)-1) <= 4D theta
                     = 4.00000004 * 10^-8 < 10^-6=c.

Thus the consumer's tilt condition is strictly satisfied. In particular,
with `kappa=[c-D(exp(2theta)-1)]/2>0`, the exact conditional split gives

    QV(x)/V(x)
      <= exp(-theta N/16)
         +sqrt(32) exp[D(exp(2theta)-1)/2-kappa sqrt(N)],
    V(x)=exp(theta S(x)).

The right side tends to zero uniformly as N grows. The remaining finite head
has finite QV by the same actual immigration MGF. Hence the sampled kernel
`Q(x,.)=P_(d(x))(x,.)` has the received geometric Foster inequality. This is a
state-dependent observation schedule, not an intervention or reset.

## What follows at actual continuous time

The accepted consumer constructs an invariant sampled law nu with nu(V)<infinity
using tight Cesaro averages and Fatou, without subtracting unknown infinite
stationary expectations. Its positive finite mean holding time is `h=nu(d)`.
The actual occupation measure

    pi(f)=h^-1 sum_x nu(x) E_x integral_0^(d(x)) f(X_t) dt

is invariant for the original CTMC. For every `0<xi<theta`, immigration
controls the entire holding-interval reward by

    E_x integral_0^d exp(xi S(X_t))dt
      <= d exp[xi S(x)+(exp(xi)-1)d]
      <= K_xi exp(theta S(x)),

since d grows only as sqrt(S). Thus this exact rate-2 chain has a unique
invariant probability, is positive recurrent, and satisfies, for example,

    E_pi exp(5*10^-17 S) < infinity.

The consumer guarantees the continuous-time exponent xi strictly below theta;
it is not necessary to claim the same exponent at sampling and physical time.
No useful numerical bound on the moment or on the enormous threshold is supplied.

This conclusion does not construct a continuous-time geometric Foster function
uniformly comparable to exp(theta S). The separately proved fixed-horizon
obstruction forbids that bounded-comparability representation for this chain.
There is no conflict: state-dependent real-time sampling plus its occupation
measure is a different construction. No product-Poisson law, general-network
extension, novelty claim, efficient algorithm, hardware action, or publication
is inferred.
