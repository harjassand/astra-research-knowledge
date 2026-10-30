# Chemical recurrence: exact layer lift, gluing falsifier, and corrected gate

Private exploratory derivation, 29 October 2026. No external review, no novelty clearance, no solution of the arbitrary-dimensional chemical recurrence conjecture.

## Target and source boundary

Target: prove positive recurrence on every closed irreducible class of every finite weakly reversible stochastic mass-action network, with arbitrary fixed positive rates. Neither a stationary distribution nor a Foster certificate is supplied. Physical holding times, nonexplosion, and actual molecular boundaries must be handled.

Astra revision: `81919dc2428968e929c865e9f10b88c0605f529a`, starting with `00_START_HERE.txt`. N33 contains a deterministic permanence candidate; N76 contains an exact factorial increment bound but explicitly not negative drift; N77 refutes classwise uniform stationary tightness as a consequence of a common deterministic attractor. These are navigation/conditional capital, not assumed solutions. The derivations below require none of their unreviewed theorem assertions.

Primary scope references:
- Anderson and Kim, https://web.math.wisc.edu/~dfanderson/papers/AndersonKimSIAP2018.pdf : positive recurrence conjecture and restricted sufficient conditions.
- Anderson, Cappelletti, Kim, https://arxiv.org/abs/1904.08967 : embedded-chain technique for restricted single-linkage systems.
- Wiuf and Xu, https://arxiv.org/abs/2312.07590 : stationary measures need not be normalizable distributions.
- https://constrained.polito.it/publications/ : project reports two-dimensional solution, general dimension still open. This is author/project status, not my audit of that proof.

## 1. Exact finite complex-layer lift

Write a reaction as y -> y', with integer nonnegative vectors and rate k(y,y')(x)_y. For any fixed nonnegative residual vector z, restrict attention to the finite state set {z+y: y is a complex} and only the reactions connecting these states with that same residual z. Its rate is

    Q_z(z+y,z+y') = k(y,y') (z+y)! / z!.

On one strongly connected complex linkage class let q_y>0 be the stationary weights of the finite complex graph whose edge rates are k(y,y'). Then

    pi_z(z+y) proportional to q_y/(z+y)!

is stationary for the layer. Indeed each stationary edge flux is proportional to q_y k(y,y')/z!, so finite complex-graph balance proves the assertion. Each enabled original reaction belongs to exactly one such residual layer; the full generator is a sum of these finite-layer generators. Every original reaction has a return path with the same residual, so there is no boundary-feasibility assumption.

This is a useful exact decomposition, NOT a proof that the sum has a finite invariant measure.

## 2. Smallest explicit gluing failure

Try to find a positive global stationary measure that balances every layer separately. Put h(x)=pi(x)x!. For the one-species directed cycle

    0 --1--> A --2--> 2A --3--> 0

the complex stationary weights are q=(1,1/2,1/3). Layerwise balance would require for every integer z>=0:

    h(z+1)/h(z)=1/2,
    h(z+2)/h(z)=1/3.

The first equation applied twice gives 1/4 instead of 1/3. Thus no strictly positive layerwise-balanced global measure exists. The underlying network is nevertheless positive recurrent: for V(x)=x its actual continuous-time drift is

    LV(x)=1+2x-6x(x-1),

negative outside a finite set. The failed gluing assumption is strictly stronger than recurrence and cannot be smuggled into the universal construction.

## 3. A genuinely implemented finite-gate correction

Consider four abstract complexes and positive epsilon:

    C --epsilon--> A+C --1--> A+B --epsilon--> B --1--> C.

This is a weakly reversible single cycle, and B+C=M is an integer conserved quantity. For any M>=1 define the proper nonnegative function

    V(A,B,C)=A+epsilon C.

The four reaction contributions, without diffusion or large-copy approximation, give

    LV = epsilon C - epsilon A C - epsilon A B + epsilon B
       = epsilon M(1-A).

Consequently on each irreducible class with M>=1, LV is negative by a constant outside a finite set. The upper bound LV<=epsilon M and proper V give nonexplosion by the usual stopped Foster argument. The negative drift gives positive recurrence. M=0 consists of absorbing singleton states. The construction handles physical time and the zero-copy faces exactly. It is an elementary valid family, not a claimed new universal theorem.

For M=1 and epsilon -> 0, fast internal averaging gives p_C=1/(1+A), p_B=A/(1+A). Effective birth and death rates are epsilon/(1+A) and epsilon A^2/(1+A). Their stationary weights are proportional to (A+1)/(A!)^2. This averaged formula is only a singular-limit diagnostic; the exact drift above, not an unproved interchange of stationarity and averaging, establishes recurrence for every epsilon>0.

## What is still missing

The finite gate succeeds because one bounded internal-coordinate correction cancels the fast reaction drift and exposes negative slow drift. A universal result needs a construction of compatible proper corrected potentials across every boundary scale and every communicating component, without assuming a finite fast class or a uniformly invertible fast generator. Arbitrary-dimensional weak reversibility alone has not supplied those properties here. Layerwise equilibrium gluing is already disproved; repeating it in different notation would not close this gap.

No molecular implementation, biology experiment, external publication, or data-source mutation was performed.
