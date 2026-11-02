# A source-debt progress function removes the comparable-population premise

New author construction. Preserve POSITIVE_UNPAIRED_JOINT_CLEANUP.md at
its earlier scope. The present operation replaces its service-priority
cleanup, rather than extending that service clock beyond its proved
assumptions. It removes ANY upper ratio bound on the two positive unpaired
inventories. It is still not full recurrence: negative/mixed unpaired
faces and the whole global receiving construction remain open.

## 1. Explicit raw progress, including its nonconstant parity correction

For a single port use only its anchor a and minority inventory c. Define
the nonnegative INTEGER function f(a,c) by

    f(0,c)=0,
    f(1,c)=3+4*(c mod2),
    f(2,c)=6 if c even, 2 if c odd,
    f(a,0)=3a,                    a>=3,
    f(a,1)=3a-4,                  a>=3,
    f(a,c)=1+f(a-3,c-2),          a>=3,c>=2.              (1)

The recursion is finite arithmetic, of length <=a/3, not an unknown
hitting expectation. For all integers a,c>=0,

    0<=f(a,c)<=3a+4,
    f(a,c)>0 iff a>0,
    f(a,c+2)<=f(a,c),
    f(a,c+2)=f(a,c) for a<=2.                            (2)

Every source1 or source2 changes (a,c) to (a+1,c+1).
WHEN the port is not terminal-ready (a<=2 or c<=1), its f increment is
<=-1. A genuine terminal changes (a,c) to (a-3,c-2), with increment
EXACTLY -1. Source0 is not assigned a favorable increment.

These claims are direct exhaustive algebra, not a kinetic approximation.
At a=1 both parities drop exactly1. At a=2,c=0 or1 the drop is1;
at a=2,c>=2 it is5 for even c and1 for odd c. At a>=3,c=0 or1 it
is1. The terminal identity is (1).

For the packet-addition claim, a<=2 is parity periodic. For a>=3 and
c>=2 reduce a by3 recursively. At c=0 the decrease on adding2 is8;
at c=1 it is4 at a=3,0 at a=4,and8 at a>=5. Hence (2) follows by
induction. In particular a LOW-anchor donor loses a packet with NO f
cost, while its receiver's f cannot increase. This parity correction is
what the naive autonomous completion count lacked.

For the two-port process put

    F=f(A,C)+f(D,F_hidden).                               (3)

Use F_hidden here to distinguish species F from the progress symbol.
Every core transfer FROM a port with anchor<=2 has nonpositive increment
in (3). This is true for every actual packet landing, regardless of the
other anchor or the unbounded inventories. No stationary core law is used.

## 2. The actual cleanup stop

Fix an initial anchor head A,D<=H and let n=min(B-C,E-F)>0. Set

    N=6H+8, h=H+N+1.

Stop cleanup successfully at A=D=0. Otherwise run the FULL raw process
until one of the following genuine events, which is a cleanup FAILURE:

* any source0;
* any source1/2 at a terminal-ready own port (anchor>=3, minority>=2);
* any core transfer whose DONOR anchor is>=3.

All other source1/2, all terminal events and all core transfers from low
donors CONTINUE. Each failure retains its ACTUAL physical landing. This
does not remove a competing channel, reset its inventory or demand a
chosen deletion word. It chooses an earlier actual observation time.

Before failure, every continuing noncore event decreases (3) by at least1,
and every continuing core event is nonincreasing. Hence there are at most
F(input)<=N continuing noncore events. A noncore failure adds at most1;
a core failure adds none. Every anchor stays <=h. For n>=4(N+1), both
positive unpaired counts remain >=n/2 throughout, because only source1
lowers them, by1 per event.

While either anchor is positive, the genuine source1 hazard of an active
port is >=c n. This is also a failure hazard when that port is ready;
it still stops the physical waiting time. Thus each interval to the next
noncore event or earlier failure has mean <=C/n, even with every low-core
path live. Summing at most N+1 intervals proves

    E cleanup_time<=C_H/n,
    J_nc(cleanup)<=N+1 pathwise.                          (4)

All intermediate physical states and genuine core motion are included.
P3 nonexplosion justifies the unstopped process; alternatively the finite
head and the finite-population bound before this stop give finite killed
localizations for the argument.

## 3. A uniform SUCCESS probability, earned by a bounded subsolution

Let T(x) be the sum of the two true terminal hazards, R(x) the sum of
high-donor core hazards, and G_ready(x) the sum of source1/2 hazards at
ready own ports. Within the proved anchor head h, exact cancellation of
the common falling-factorial source gives

    R<=K_H T,
    K_H=h*max(kf/alpha3,kb/beta3)/2.                     (5)

Indeed a donor's core/terminal ratio is
kappa*A_peer/[alpha3*(A_donor-1)*(A_donor-2)].
The total is bounded portwise by (5). No bound on r1/r2 or C/F enters.

For ready source1/2 the analogous exact ratios, using B_i>=n/2 and C_i>=2,
give a raw C such that

    G_ready <= (C/n) T.                                 (6)

Take n large enough that C/n<=1. Put p=1/(K_H+2), and assign

    g(x)=p^F(x)

to the continuing states, value1 to successful absorption, and value0 to
failure absorption. This assignment is a success-probability subsolution,
not the physical receiving function. In particular a core failure's REAL
output is still charged later at Z^2, not given receiving value zero.

At a terminal the progress falls exactly1, so g's gain is
(p^-1-1)g=(K_H+1)g. High-donor core failure loses at most K_H*T*g;
ready-growth failure loses at most T*g by (6). All continuing growth and
low-donor core gains are nonnegative. Only the constant source0 failures
remain, with loss >=-(alpha0+beta0). Hence for the ACTUAL killed generator

    L_killed g >= -(alpha0+beta0).                       (7)

Bounded optional stopping, using (4), proves

    P(success)>=p^F(input)-(alpha0+beta0)E cleanup_time
               >=p^N-C_H/n >=delta_H:=p^N/2>0.          (8)

This is a raw population-UNIFORM probability, not a favorable input law
or a small fixture. All source1/source2 competition and all low-core
paths remain live; high-core paths are paid complete failure outputs.

## 4. Actual output cost

Keep the SAME global physical receiver

    Z=15+M-m(A)-m(D), m=(0,2,4,7,7,...).

Every core event preserves Z exactly. Every raw noncore event has
|Delta Z|<=14. Thus at every success or failure landing,

    |Z_out-Z_in|<=b_H:=14(N+1).                          (9)

At success both anchors are zero; q=C+F has changed by at most3(N+1),
and the positive unpaired counts by at most N+1. Equations (4),(8),(9)
are a complete actual cleanup interface: finite count/time, bounded mass
cost, and a uniform success probability from EVERY bounded-anchor input
with both unpaired counts sufficiently positive, however different their
scales. A failure is NOT declared globally repaid on its own.

## 5. Delayed repayment at the same Z^2, with arbitrary hot-scale ratios

Reuse the actual isolated activation trials of sections4--5 in
POSITIVE_UNPAIRED_JOINT_CLEANUP.md. They stop immediately on peer input,
own active input or ready growth and retain every actual output. Starting
at both anchors zero, each successful trial is neutral or deletes one
unpaired majority molecule. Its acquired bounds are

    P(good)>=c/(q+1), P(interruption)<=C/n,
    E time<=C, genuine noncore count<=4.                 (10)

NONE of their raw divisions uses an upper bound on either B-C or E-F.
In fact a larger majority only improves the early clock and interruption
bounds. This is why the new cleanup can genuinely remove the former
comparable-population assumption, rather than just relocate it.

After cleanup success run L=ceil[K(q+1)] trials, stopping at the first
interruption or good-deletion guard D>=floor(n/4). Choose eps small so
the interruption and guard probabilities are together <=1/2 whenever
q<=eps n+O_H(1). Exactly as before, conditional on cleanup success,

    E D>=cK/2,
    E time+E J_nc<=CK(q+1).                              (11)

On cleanup failure take D=0. Equation (8) now gives the unconditional
lower bound E D>=delta_H*cK/2, rather than requiring failure to be rare.
Every output still satisfies

    Z_out=Z_in+B-D, |B|<=b_H+3,
    0<=D<=n/4+1<=Z_in/4.

Choosing K>=8(b_H+4)/(delta_H*c), then eps sufficiently small and n0
sufficiently large, yields the identical squared-power estimate and pays
all physical time and noncore count:

    E[ sigma+J_nc(sigma)+Z(X_sigma)^2 ]<=Z(x)^2.           (12)

Consequently, for each H there are raw eps,n0 such that (12) holds for
EVERY

    A,D<=H,
    n=min(B-C,E-F)>=n0,
    C+F<=eps n,                                         (13)

with NO upper bound on max(B-C,E-F)/n. Both unbounded cold subsystems
and arbitrarily separated hot scales are included in the same physical
construction. The constants can be extremely poor; no practicality claim
is made.

## 6. Reusable acquired rule and actual frontier

The useful rule is more general than the original pure-service clock:
an integer raw progress can tolerate conservative moves with the wrong
sign if their FAILURES are observable and their hazards are bounded by
progress-producing channels. The bounded subsolution p^F earns a uniform
success chance; later actual deletion trials repay every bounded failure
cost. It requires neither a received stationary profile nor a mixing gap.
Here the progress (1), the packet transport (2), the hazard comparison
(5),(6) and the physical lower clock were constructed from the raw list.
They are not assumed interfaces of arbitrary weak reversibility.

The preceding pure-service comparison remains correct at its stated
scope, but its total-growth interruption estimate must NOT be transferred
to arbitrary hot-scale ratios. For example at (A,C,D,F)=(3,2,1,0), with
the peer majority far larger than the square of the first majority, the
peer's LOW source1 fires before terminal/core service with probability
approaching1. That event is neutral in Z and is now CONTINUED by (1)--(8).
This is a precise obstruction to the old decomposition, not to recurrence.

Remaining obligations are still substantive: negative/mixed unpaired
signs, regions in which a minority is comparable to or larger than a
majority difference outside the existing cone, arbitrary initial high
anchors, and one global receiving geometry across all established stops.
The full six-species theorem and arbitrary weak reversibility remain
unproved. This progress rule is a reusable operation toward that target,
not a replacement endpoint.
