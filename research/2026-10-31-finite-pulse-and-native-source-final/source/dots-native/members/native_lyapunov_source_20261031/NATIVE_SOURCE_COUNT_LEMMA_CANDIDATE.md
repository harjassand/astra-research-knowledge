# Native dark-source activity bound from an acquired Lyapunov energy

31 October 2026. Root candidate, pending independent review. This is a count bound, not a completed coherent simulator. It keeps the native Lindblad generator rather than replacing it by a collision model.

Let psi be a known pure source state, P=|psi><psi|, Q=I-P. Suppose acquired source jumps L_a annihilate psi, and define

G=sum_a D[L_a],   H=(1/2)sum_a L_a^dagger L_a.

Assume certified constants h>=g>0 and kappa>0 such that

g Q <= H <= h Q,       G^dagger H <= -kappa H.

Consider arbitrary initial source/system/reference states and the physical generator

lambda G - i[H_sys + sqrt(lambda) K,.],

where H_sys acts only on the system/reference and K is Hermitian with ||K||<=b. All statements below extend by identity to external references. Centering of K is NOT needed for this count lemma; an uncentered mean can still have real sqrt(lambda) action and is not removed by this statement.

Let N count actual source jumps in this specified unraveling. For theta>0 put u=e^theta-1 and require

u <= min(1,kappa/(16h)).

Set a=4u/kappa and W=I+aH, so I<=W<=5I/4<=2I. The source tilted adjoint obeys

G_theta^dagger W = a G^dagger H + u sum_a L_a^dagger W L_a
 <= -a kappa H + u(2+2ah)H
 <= -(a kappa/4)H.

Here sum L_a^dagger H L_a<=2hH. The last inequality deliberately discards slack: -4u+2u+8u^2h/kappa<=-3u/2<=-u.

For a normalized joint state rho set q=Tr(Q rho). Since H vanishes on P, splitting the Hamiltonian commutator into PQ and QQ parts gives

|Tr(i[K,H] rho)| <= 2hb(q+sqrt(q)).

The QQ bound is 2hb q; the offdiagonal trace Cauchy-Schwarz bound is 2hb sqrt(q(1-q))<=2hb sqrt(q). No scalar-state Jensen step is applied to an unnormalized tilted state.

In the high-rate regime

sqrt(lambda) >= 16hb/(kappa g),

the QQ term 2ahb sqrt(lambda)q is at most a kappa lambda g q/8. Absorb it into the negative drift. For the remaining cross term use, for every q>=0,

-(a kappa lambda g/8)q +2ahb sqrt(lambda)sqrt(q)
 <= 8 a h^2 b^2/(kappa g).

Thus the FULL tilted adjoint satisfies the operator inequality

L_theta^dagger W <= [32u h^2 b^2/(kappa^2 g)] W.

It follows by positive tilted evolution, W>=I and initial W<=2I that

E exp(theta N(T)) <= 2 exp[32u h^2 b^2 T/(kappa^2 g)].

At p prescribed arbitrary common CPTP instrument slots, include the outcome register. Each normalized positive state has W-expectation at most2; equivalently instrument^dagger(W)<=2I<=2W. Segmentwise propagation therefore gives

E exp(theta N(T)) <= 2^(p+1) exp[32u h^2 b^2 T/(kappa^2 g)].

For any tail budget delta, a sufficient integer count cap is the ceiling of

[(p+1)ln2 +ln(1/delta)+32u h^2 b^2 T/(kappa^2 g)]/theta.

It is independent of microscopic lambda in the high-rate branch. Choosing a fixed permitted u shows the scaling O(max(1,h/kappa)[p+log(1/delta)] + h^2 b^2T/(kappa^2 g)), with numerical constants depending only on the displayed choices. The exact formula above is authoritative.

In the low-rate branch, the physical conditional jump intensity is at most2h lambda. Standard counting domination by a Poisson process therefore gives mean at most

2h lambda T <= 512 h^3 b^2 T/(kappa^2 g^2).

This is an ordinary low-rate fallback bound, not a claim that expected counts alone construct a coherent simulator. At lambda=0 there are no source jumps. At b=0, every positive lambda is in the high branch and the finite initial energy still gives a time-uniform count bound.

## What remains unearned

The bound is tied to the actual acquired dark-jump representation; changing the unraveling changes N. It is not a microscopic laboratory detection guarantee. A coherent retained simulator still needs its complete first-event isometry, normalized positive clock proposals, fast no-jump kernel construction, actual jump labels, arithmetic precision, output controls and all circuit costs. The source-only no-jump kernel is e^(-lambda H t), whose gap permits a plausible acquired fast implementation, but no complete algorithm follows merely from the count estimate.

The direction-merged high-temperature Gibbs construction supplies one candidate H/g/kappa triple. Its existing native-source return proof remains separate. Known dissipative-state-preparation and simulation methods are strong comparators; neither this lemma nor its conjunction with that source establishes novelty or practical advantage.
