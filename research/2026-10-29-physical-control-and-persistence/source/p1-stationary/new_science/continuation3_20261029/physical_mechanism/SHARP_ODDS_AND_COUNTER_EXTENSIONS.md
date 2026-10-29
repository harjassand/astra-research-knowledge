# Sharp odds budget and an independent controller representation

29 October2026. Complementary derivations; root owns the central compiler.

## 1. Mandatory native calls bound unknown-source odds

One actual native primitive flips the current bit with iid probability p,
unknown on an open interval. A causal controller observes its outcomes and
independent supplied randomness, uses1 throughN native calls on every branch,
and returns its actual physical bit. No other actuator or kinetic oracle is
present. Its opposite-endpoint probability F(p) is a polynomial of degree<=N.

For each fixed random seed, let d be the stopping depth on the all-no-flip
branch. At first order in p only one-flip paths contribute. The first flip
can occur at each of the d all-hold-prefix positions. If no later flip occurs,
the endpoint remains opposite, regardless of subsequent stopping decisions.
Each path contributes p+O(p^2). Hence F(0)=0 and F'(0)=d. Integrating seeds,

    F'(0)=E[d] in[1,N].

The physical interval need not contain0. If two such controllers obey the
exact identity F_A=r F_B throughout an open interval, polynomial identity
gives r=F_A'(0)/F_B'(0), so1/N<=r<=N. The root's ratioN is sharp. If every
branch uses exactly N calls, both derivatives equalN and only ratio1 is
possible. A genuine zero-native-call identity branch removes the lower
derivative bound. Multiple different unknown primitives are a different
interface; if p_j=c_j p then F'(0)=E[sum along the all-hold branch c_j],
giving only the corresponding c_min to N*c_max bounds.

Also F(p)<=1-(1-p)^N: on an all-no-flip realization of N possible native
calls, no stopping controller can return the opposite bit. The root first-hit
rule attains this upper bound. This is a physical terminal-state restriction,
not a Bernoulli factory that may output an arbitrary digital symbol.

The adjacent checker enumerates all676 deterministic mandatory-first-call
trees through depth4, verifies the exact derivative identity, and groups
proportional endpoint polynomials. Its largest exact ratio is4. The finite
check supports the reasoning and catches indexing/sign errors; it is not a
substitute for the general proof.

## 2. Renewal countdown explains the binary invariant-law theorem

Let H<=N be a positive horizon, r=E H, and rho_j=Pr(H>j)/r for j=0,...,N-1.
A countdown chain decrements j>0 and at0 draws H and resets to H-1. Its
stationary distribution is rho, because

    rho_{j+1}+rho_0 Pr(H=j+1)=rho_j.

Augment the native P chain by this countdown. On departure from visible A,
use its countdown update; on departure from B, redraw the phase from rho.
Both controller updates preserve rho, so any native stationary mu gives
an augmented invariant product mu*rho. Watch on B at every phase and on A
only at phase0. Its conditional native law is proportional to mu_A/r+mu_B.

At an A watch epoch, phase0 triggers a fresh horizonH. At a B watch epoch,
the next native call also redraws phase independently, giving exactly the
root residual L~rho after entry to A. Thus the projected watched process
is the root kernel, not an unspecified hidden-controller process. Native
stationarity alone proves invariance; native reversibility separately proves
the stronger path-reversal statement. A geometric H produces ordinary
independent endpoint acceptance. A deterministic H=N produces the bounded
uniform-residual construction. This is an independent conventional trace-
chain interpretation of the root algebra.

## 3. Useful extension of the root's later general integer counter

Root subsequently supplied a simpler all-label counter: for integer target
weights w(x) between1 andN, initialize the phase uniformly on1,...,w(x),
execute P and increment phase moduloN after each call, and stop when
phase<=w(current state). This is a watched product chain with phase refresh
conditional on the current native state; its invariant law is mu*w/mu(w).
Average the two clock directions to inherit native reversibility.

If the minimum weight is m>1 and maximum is N, incrementing by m rather
than1 sharpens the deterministic call cap to ceil(N/m). The cyclic map
c -> 1+((c-1+m) mod N) still preserves the uniform phase law. Every trajectory
hits the common accepted phase set {1,...,m} within ceil(N/m) advances:
before the first wrap the phase grows by m, and the first wrap lands in this
set. If it starts there, the next positive return satisfies the same bound.
The reverse shift -m has the same bound, by the corresponding backward-gap
argument. The invariant law and stationary mean N/mu(w) are unchanged.

Consequently the deterministic native-call ceiling can match the integer
rounding of the root's universal lower bound w_max/w_min even when the
weights have a large common scale. An exact initial uniform selector on
1,...,w(x) is still required. Rational weights can be scaled to integers;
their selectors need not have bounded fair-bit implementation. Arbitrary
positive real weights also admit a formal circle rotation by w_min with
uniform phase on[0,w(x)], but continuous exact selectors/comparisons are
additional resources and not a literal finite-bit physical deadline.

## 4. Scope

The controller coordinate is a stored phase, not elapsed laboratory time.
Native-call bounds require compatible native call durations and controller
latencies before they imply a physical deadline. None of these trace
representations changes the raw path of one native operation run repeatedly,
erases retained records, fixes conserved-class proportions, or prepares an
invariant sample from arbitrary starts. Correlated auxiliary acceptance
variables and the under-graph augmentation have close primary predecessors
identified in PRIMARY_PREDECESSORS_AND_SCOPE.md; priority is not established.
