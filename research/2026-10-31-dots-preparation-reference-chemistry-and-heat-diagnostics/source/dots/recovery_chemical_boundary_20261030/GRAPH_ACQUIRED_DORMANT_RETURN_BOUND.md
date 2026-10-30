# A graph-acquired dormant-return exponent

30 October 2026. First broader construction, NOT independently reviewed and NOT a recurrence theorem. It acquires an asymptotic kernel estimate from a raw finite reaction graph rather than solving every population shell.

## Raw structural input

There are types X_1,...,X_k with distinguished A=X_1 and catalyst D. The conversion reactions `X_i+D -> X_j+D` have fixed positive rates on a strongly connected directed graph. The only linear D-consuming birth is `A+D -> 2A`, with positive rate. Nonlinear seed reactions include `2A -> A+D` and may include `2A -> 2D`; their rates are proportional to (A)_2. Killing/clearing has rate k0(A)_2, k0>0. An optional `2D -> A+D` channel is allowed. No birth from a non-A type is assumed: such a birth can exhaust D before A is produced and destroys the argument below.

Total residual count n=sum X_i+D is conserved before killing. Let L>=1 be the maximum shortest directed conversion distance to A, with L replaced by 1 if all non-A types have distance at most one. Distances and prescribed-path constants are computed from the raw finite graph.

Claim: uniformly over all active positive-D inputs,

`P(hit D=0 before clearing) <= C n^-delta`,
`delta=1/(8L+8)`.

Constants depend on the finite graph and fixed rates. No finite cap, mixing law, stationary fast distribution, or full-network recurrence is supplied.

## 1. Earn the local conversion clock from graph paths

In the D-clock u=integral D_t dt, conversion is an ordinary independent-particle finite-state Markov chain. Before the first nonlinear seed/clearing event, A-births can be coupled as extra particles; the original particles continue their conversions unchanged. The optional 2D channel adds A and is also favorable. Stop before D=0.

For every initial type i, a prescribed shortest path followed by no further jump gives

`P_i(X_u=A)>=c_i u^(ell_i)>=c u^L`, 0<u<=u0,

where ell_i<=L and c,u0 are explicitly computable from the edge rates and maximal exit rate. For ell_i=0 (an initial A particle), the no-jump probability gives the same lower bound after decreasing c.

With at least n-J original type particles, their A-occupancy at a fixed u is a sum of independent Bernoulli variables. For

`t_*=C(K/n)^(1/L)`,

its mean is at least 4K, and the chance it is below 2K is at most exp(-cK). This is an ordinary finite-graph/Poisson-binomial estimate, used on the actual common clock. It is not an assumed O(1/n) direct-source drift.

## 2. Low-A stage, with actual stopping and restart

Choose

`K=floor(n^(1/(4L+4)))`, `J=floor(n^(1/(8L+8)))`.

Start with A<K and 1<=D<J. Stop a chunk at A>=K, D=0, D>=J, clearing, the next nonlinear seed, or D-clock duration t_*. If no earlier stop occurs, failure to reach K by t_* has probability at most exp(-cK), by the coupling in Section 1. Conditioning on absence of a seed is not used to assert independence: the pathwise inclusion of the failure event in the reference occupancy event suffices.

A nonlinear seed interrupts the chunk and restarts it in the new actual state if still in the low strip. Clearing and nonlinear seed marks have the SAME (A)_2 clock, so the total seed count before clearing has a geometric tail with fixed parameter k0/(k0+k_seed). Thus its mean is bounded. Horizon-only failures restart with probability exp(-cK). Positive iteration gives total expected D-clock duration of the low stage at most C t_*.

Only A+D->2A at D=1 can enter D=0; the 2D channel is disabled there. In the D-clock its rate is k_birth A<=CK. Therefore the actual low-stage dormant-entry probability is at most

`C K t_* = C K(K/n)^(1/L)`.

Clearing or a seed has D-clock rate at most C K^2/D<=C K^2, so these interruptions have the corresponding C K^2 t_* upper bound when needed. Physical operational duration is at most D-clock duration while D>=1. No event is assigned a favorable unrecorded output.

## 3. High-A stage

From A>=K and D<J, stop at clearing, A<K/2, D=0 or D>=J. Clearing hazard is at least cK^2, giving operational mean <=C K^-2. Its compensator gives E integral(A)_2<=1/k0. Since D<J and A>=K/2,

`E integral A D <= C J/K`.

This bounds the chance of an A-consuming conversion event and the D=0 birth exit. Losing K/2 A through nonlinear seed jumps requires order K seed marks, whose probability is exponentially small. Thus high-to-low restart probability is at most `C J/K+C exp(-cK)`.

The optional 2D channel only increases A and cannot reach D=0 from D=1. All other non-A conversions leave A unchanged. The bound is therefore independent of how many conversion intermediates exist.

## 4. Sum the actual stages

Conditional low/high restart summation is finite because J/K tends to zero. An upper D exit from input D=1 requires at least (J-1)/2 nonlinear seed events, hence has probability exp(-cJ). It can be assigned its entire mass as a possible later dormant return; no continuation law is needed.

The dormant-return probability from D=1 is consequently at most

`C[K(K/n)^(1/L)+J/K+exp(-cJ)] <= C n^(-1/(8L+8))`.

Every path from any D>=1 to zero must first visit D=1, because all negative D jumps have size one. Strong Markov extends the bound uniformly to every active positive-D input.

Finite small n are covered by enlarging the probability constant. Eventual clearing need not be assumed for this probability bound. If finite-shell absorption is desired separately, the raw complex graph supplies a prescribed path to 2A of length at most L+1, then clearing; the usual geometric event-path bound gives an explicit polynomial finite-shell mean.

## Acquired capability and limitation

The input graph is finite; shortest paths and path-rate constants are computable in polynomial graph work. The proof gives a uniform population-scale return exponent without enumerating the O(n^k) count states or presuming a direct A-producing source at every face. The graph-uniform constants are conservative: L=1 gives probability exponent 1/16, whereas the specialized direct-source proof earned probability exponent 1/8 and then profile exponent 1/16.

This probability estimate is NOT enough for the full feedback theorem: weighted outgoing inverse-A moments and their ratio to the SAME occupation margin are still missing for general conversion graphs. The exact two-edge first-arrival counterexample shows that the old x^3+nD resolvent cannot simply be reused. That joint acquired profile, not a catalogue of larger networks, is the substantive next question.
