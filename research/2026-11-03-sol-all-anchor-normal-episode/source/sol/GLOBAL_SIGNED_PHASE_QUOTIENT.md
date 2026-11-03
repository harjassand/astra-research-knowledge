# A global signed phase chart, without a bounded cold buffer

Live representation construction motivated by the failed native/phase
receivers and corrected factorial diagnostics. This earns exact normal
neutralization, a globally proper energy and its acquired bounded-log
transport. It does NOT by itself earn the global actual-return sign.

## 1. Tie phase credit to the actual anchor

For every a>=0 write a=3k+j, j in {0,1,2}, and define

    u(a)=2k+1_(j>=1), v(a)=2k+1_(j=2).

Use signed residual inventories

    z=(B-u(A), C-v(A), E-u(D), F-v(D)).              (1)

The credit is not an unlimited free packet store. Its magnitude is tied
to the PHYSICAL anchors A,D, which will be taxed by their own proper
energy. Negative z is an explicit borrowed inventory; no molecule or
physical reaction is inserted to make it nonnegative.

Both core directions still translate z by (-2,-2,+2,+2). For each port,
the EXACT residual increments of source0,source1,source2 are

    anchor mod3=0: (0,0),  (-1,+1), (0,+1);
    anchor mod3=1: (+1,-1),(0,0),   (+1,0);
    anchor mod3=2: (0,-1), (-1,0),  (0,0).          (2)

Every actual terminal has residual increment ZERO at every anchor>=3,
because u(a)-u(a-3)=v(a)-v(a-3)=2. Thus the correct phase0/1/2 growths
and all terminal events preserve the hidden chart exactly, at ALL anchor
heights. There is no pinning, bounded landing assumption or high-anchor
seam in this identity. The abnormal operations are now signed coordinate
birth, death or transfer with a fixed finite list (2).

The physical rates remain their ORIGINAL falling factorials in the
original counts. The chart is not a new mass-action process on z.

## 2. A coercive signed factorial quotient

Let h(m)=log(|m|!) for integer m (h(0)=h(1)=h(-1)=0). Its consecutive
differences are nondecreasing, so it is a convex function on Z. For fixed
positive raw reference theta=(theta_B,theta_C,theta_E,theta_F), define

    H_theta(z)=sum_i [h(z_i)-z_i log theta_i]
                        +sum_i(theta_i+theta_i^(-1)),
    Phi(z)=min_(k in Z) H_theta(z+k*(-2,-2,+2,+2)).     (3)

Every signed class is admissible, and the minimum is acquired from a
coercive one-dimensional convex integer problem. This representation is
NOT a dynamically reachable physical core fibre or its stationary law.
Core invariance follows from reindexing k, regardless of actual rates,
zeros, gap or permitted direction at the current physical state.

For m>=0, h(m)-m log theta >=-theta; for m<0 the same bound with theta^(-1)
applies. Thus H_theta>=0. Stirling's elementary lower bound and convexity
give a coercive lower bound in the conserved signed total n=sum z_i:

    Phi(z)>= |n| log(|n|/4)-C_theta|n|-C_theta.       (4)

The same argument using each conserved difference z_B-z_C,z_E-z_F gives
additional coercive directions; they are not needed for the following
physical properness proof.

Choose positive anchor references theta_A,theta_D and put

    E(x)=1+Phi(z(x))
       +log(A!)-A log theta_A+theta_A
       +log(D!)-D log theta_D+theta_D.               (5)

It is globally nonnegative and proper on physical states. Indeed bounded
E bounds A,D by their individual nonnegative Poisson energies. Then the
credit sum u(A)+v(A)+u(D)+v(D) is bounded. If hidden population diverges,
sum z_i diverges and (4) contradicts bounded E. This is why the earlier
unbounded-free-packet objection does not apply: the physical anchor pays
for the unbounded phase credit here.

## 3. Acquired finite jumps and actual normal cost

A minimizer in (3) has |k|<=C_theta*(1+||z||_1); one can acquire a bracket
by doubling until the consecutive convex differences have opposite signs,
then use integer binary search. For a fixed residual shift delta, evaluate
the output at the INPUT minimizer and conversely. Since h's one-coordinate
increment over a bounded shift is O_delta(log(2+|m|)), the acquired bracket
gives

    |Phi(z+delta)-Phi(z)|
        <=C_(theta,delta)*log(2+||z||_1).             (6)

No physical conservative transport or integer-fibre oracle is a premise.
The argument is the signed, unconstrained rank-one version of the banked
bounded-buffer quotient transport, not a general efficient lattice solver.

At a normal growth or terminal, hidden Phi is EXACTLY unchanged by (2).
Only the real anchor contribution changes:

    growth on A: log(A+1)-log theta_A;
    terminal A: -log((A)_3)+3 log theta_A.           (7)

All source jumps have O_raw(log(2+M)) energy increments globally. Core
energy increments are exactly zero. The physical clock and actual
reaction propensities have not been changed or suppressed.

## 4. What is still missing

Equations (1)--(7) remove the artificial finite-buffer/high-anchor
definition problem and expose the genuine birth/death/transfer debts.
They do NOT prove the signs or frequencies of those operations. In
particular normal residence can be slow, abnormal births can create a
loan, and actual peer interruptions and corner outputs must be received.

The source-current, extra-boundary and compensated reset operations apply
to the same physical process independently of choosing (5). Their raw
population factors can pay logarithmic costs from (6); a complete joint
return still has to be constructed. A globally proper quantity alone is
not recurrence, a numerical compiler or a practical advantage.

The new diagnostic probe_global_signed_phase_energy.py evaluates the same
actual completed episode at (5), with its OWN actual corner. Its ordinary
product-Poisson control and adversarial mixed boundaries are evidence to
guide this construction, separate from the algebraic proof above.
