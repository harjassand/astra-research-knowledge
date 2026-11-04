# Sparse acquisition of the weight-four checks

This construction replaces exhaustive enumeration of all four-wire supports. It uses the same promised code family: a fixed product of square toric blocks of distance greater than four, hidden by a wire permutation and local Clifford frame. There are exactly `N` elementary weight-four checks and no weight-two stabilizers. Any physical Pauli of weight at most four that is not a check has expectation zero, for every logical state in the codespace.

Suppose every fresh calibration measurement has a state-independent stochastic fault support, with per-wire probability at most `q_c < 1/36`. Faults on the support may be arbitrary completely positive maps. The support bound holds conditional on the chosen product basis and previous experiments. Let

\[
a=1-4q_c,\qquad b=\tfrac12+4q_c,\qquad
g=\tfrac12-8q_c.
\]

## Discovery

Choose a uniform random product Pauli basis and measure `t` fresh copies in that basis. Write `c_i` for the `t`-bit outcome column on wire `i`. Sort all unordered wire-pair records by the key

\[
\min(c_i\mathbin\oplus c_j,
\overline{c_i\mathbin\oplus c_j}).
\]

Equal keys for disjoint pairs propose a signed weight-four parity check. The complement identifies the two possible signs. No four-tuple is visited unless a pair collision proposes it.

A specified genuine check matches the random basis with probability `1/81`. On every fresh copy, its ideal parity is fixed. No fault on its four wires occurs with probability at least `a`, so all `t` discovery rows have the correct parity with probability at least `a^t`. The check is then proposed through all three pair partitions of its support. With

\[
m\ge81a^{-t}\ln(N/\delta_{\rm miss}),
\]

random-basis rounds, the probability that any genuine check is never proposed is at most `delta_miss`.

## Collision count and an explicit runtime cap

For a noncheck of weight four, arbitrary local faults can change the mean by at most `8 q_c`. Therefore each parity outcome has either sign with probability at most `b`. Its discovery rows are all equal with probability at most `2 b^t`. Comparisons of overlapping pairs reduce to a weight-two noncheck and obey the same bound.

Choose

\[
t=\left\lceil\frac{2\ln N}{\ln(1/b)}\right\rceil.
\]

There are fewer than `N^4/8` comparisons of two pair records. Their expected noncheck collisions are at most `N^2/4`. Genuine checks contribute at most three collisions per check, hence at most `3N`. For `m` rounds,

\[
\mathbb E C\le m(3N+N^2/4).
\]

Set

\[
H=\left\lceil
\frac{m(3N+N^2/4)}{\delta_{\rm time}}
\right\rceil.
\]

The algorithm aborts if its total collision comparisons exceed `H`. Markov's inequality gives abort probability at most `delta_time`. The cap includes overlapping comparisons and duplicate proposals, so it also bounds the number of distinct checks sent to verification. It is an explicit cost/error tradeoff, rather than an assumed average-case oracle.

## Independent verification

For each random-basis round, reserve `u` additional fresh copies measured in that same basis. They are not used to form collision keys. Verify every proposed quartet using its parity mean on these held-out rows, accepting when its absolute value exceeds `1/2`.

A genuine check has mean magnitude at least `1-8q_c = 1/2+g`. A noncheck has mean magnitude at most `8q_c = 1/2-g`. Conditional on any proposal from the discovery rows, Hoeffding's inequality bounds its verification error by

\[
2\exp(-u g^2/2).
\]

Thus

\[
u\ge\frac{2}{g^2}\ln(2H/\delta_{\rm verify})
\]

suffices simultaneously for all proposed checks. Proposals may be adaptive and their verification outcomes may be mutually dependent; independence between discovery and the fresh verification rows, followed by a union bound over at most `H` proposals, is sufficient. The resulting acquisition failure probability is at most

\[
\delta_{\rm miss}+\delta_{\rm time}+\delta_{\rm verify}.
\]

## Complete costs

Calibration uses `m(t+u)` source copies. Sorting pair records costs `O(m N^2 t log N)` bit operations. Collision processing and verification cost at most `O(H(u+log N))`, with the cap enforced in the implementation. Raw measurement data cost `O(mN(t+u))` bits to record; rounds may be streamed if a full archive is unnecessary.

For fixed fault rate and fixed error budgets, write

\[
\alpha(q_c)=\frac{2\ln(1/a)}{\ln(1/b)}.
\]

The copy cost is `O(N^alpha polylog N)` and the classical acquisition cost is `O(N^(2+alpha) polylog N)`. The runtime-failure budget contributes the displayed `1/delta_time` factor when it varies. For `q_c < 1/36`,

\[
a>8/9,\quad b<11/18<(8/9)^4,
\]

so `alpha < 1/2`; its limiting value is approximately `0.4783295821`. For the code family `N = k polylog(k)`, calibration copies remain sublinear in `k` up to logarithms. The `O(k)` logical Bell rows therefore retain the leading sample complexity of the learning task.

The earlier `O(log N)` calibration bound remains valid with exhaustive enumeration. The sparse algorithm makes a different, explicit tradeoff: more calibration copies, far less classical search. Neither bound grants a generic decoder for unknown quantum codes outside the promised family.

## Executed finite point

The preserved records have `N=50`, 1,000 random bases and 256 fresh rows per basis. The sparse run uses 12 discovery rows and 244 held-out verification rows. The simulation's independent outcome-flip probability is `q_c=0.005`. It forms 1,225,000 pair records, examines 367,551 collisions and verifies 113,269 distinct pattern/quartet proposals, recovering exactly the same 50 checks as the 230,300,000-test exhaustive audit.

With collision-risk parameter `0.003`, the cap is 258,333,334. Exact rational tail certificates give an acquisition failure bound below `0.009278` under the stated model. This cap is conservative; observed collision counts are reported separately and do not replace the proof. No physical threshold or hardware fidelity is inferred from this finite execution.
