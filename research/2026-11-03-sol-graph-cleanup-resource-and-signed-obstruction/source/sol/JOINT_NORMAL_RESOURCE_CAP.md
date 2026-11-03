# A finite population-capped boundary trace through neutral debt loops

New author operation, not an inward drift theorem. This keeps the physical
clock and every actual failure output while allowing arbitrarily many
neutral borrow/repay cycles. It applies from EVERY fixed bounded-anchor
input, with no sign or scale assumption on the four hidden inventories.
It does not assert that its outputs are globally repaid.

## 1. Raw normal policy and its actual failures

For a port with coordinates (a,b,c), designate the following genuine
channels as CONTINUING:

    source0: a>=1 and (a==1 or b==0);
    source1: a==1;
    source2: a>=2 and (a==2 or b==1);
    source3: always, when its true falling-factorial source is enabled.

An unavailable designated channel still has rate zero; it is not inserted.
Both conservative directions continue ONLY when their DONOR anchor<=2.
Every other genuine channel is a FAILURE. Observe the full raw process
until its FIRST failure or until A=D=0 (SUCCESS). All failure landings
are the ACTUAL physical raw outputs.

No cold coordinate is frozen or required to hit zero. Low-anchor core
circulation can continue at arbitrary speed, and noncore neutral loops can
repeat an unbounded number of times before this stop.

If the initial anchors are <=H, all continuing anchors are <=max(H+2,4),
and a final failure raises this by at most1. A high port with b=0 can
take source0, then source2 at b=1, then can only terminate or fail once
b>=2. Incoming core packets cannot prolong that upward segment; outgoing
high-core transfers are failures. A low port reaches at most anchor4
before the same rule applies. Thus h=H+4 is a uniform actual anchor head.

## 2. Two acquired resource corrections

Define integer functions w(a,b),v(a,b) by finite recursion:

    a=0: w=v=0;
    a=1: w=b mod2,             v=0;
    a=2: w=-(b mod2),          v=-1;
    a>=3,b=0: w=v=0;
    a>=3,b=1: w=v=-1;
    a>=3,b>=2:
        w(a,b)=w(a-3,b-2)-2,
        v(a,b)=v(a-3,b-2)-2.                            (1)

These are finite raw arithmetic, not expectations. Their bounds include

    -2a/3-1<=w<=1, -2a/3-1<=v<=0.                       (2)

Both are nonincreasing on adding a packet b->b+2. At a<=2 they are
EXACTLY packet-periodic. For a>=3,b>=2 use induction in a in (1).
The remaining b=0,1 comparisons are direct: at b=0 the next value is
the low/base value minus2; at b=1 the exceptional a=3,4,5 values are
read explicitly, and a>=6 reduces to -3<=-1. This proves packet transport
for every integer, including the unbounded cold subsystem.

Put

    R_B=B+E+w(A,B)+w(D,E),
    R_C=C+F+v(A,B)+v(D,E).                              (3)

Each is NONINCREASING at EVERY continuing reaction.

For core transfers, the two hidden totals are conserved. The low donor's
correction is unchanged by removal of2, and the receiver's correction
cannot increase by addition of2. Thus every real core landing is covered.

For a terminal, each correction rises by2 under (1), exactly cancelling
the corresponding hidden-total decrement2. For continuing growth the
following finite table gives the changes; empty source1/source2 cases
remain unavailable:

| Continuing channel / source class | Delta R_B | Delta R_C |
|---|---:|---:|
| source0, a=1 | 0 | -1 |
| source0, a=2,b=0 | 0 | 0 |
| source0, a>=3,b=0 | 0 | -1 |
| source1, a=1,b even | 0 | 0 |
| source1, a=1,b odd | -2 | 0 |
| source2, a=2,b even | -1 | 0 |
| source2, a=2,b odd | 0 | 0 |
| source2, a>=3,b=1 | 0 | 0 or -1 |
| source3 | 0 | 0 |

For the source2 high case the R_C decrement is -1 at a=4, otherwise0.
The table follows by substituting (1), so there is no prescribed receiving
profile or omitted competing path in (3).

## 3. Population cap, independently of the number of neutral cycles

By (2),(3), until failure

    B+E <= (B+E)_in + 4(h+1),
    C+F <= (C+F)_in + 4(h+1).

Together with the anchor head and the last raw jump, one convenient bound
is

    M_t <= M_in+C_H, C_H=20(H+5),                        (4)

at EVERY time before and at the stop. This charges the cost of leaving
the normal region: the last real failure output is included. Core motion
can redistribute the entire cold population, but cannot violate (4).

In terms of a physical corrected mass, (3) says

    T=M+u(A,B)+u(D,E), u(a,b)=w(a,b)+v(a,b)-a,             (5)

is pathwise nonincreasing along all continuing channels. For fixed H,
u is uniformly bounded. T is not being promoted to a global proper
receiver for unbounded anchors. Its role here is the acquired cap (4).

## 4. Actual absorption and physical residence

At any nonterminal state there is a raw path of at most TWO genuine
reactions to failure, with both propensities bounded below by positive
raw constants:

* if an anchor is0, its source0 is already a failure;
* at an active a>=2,b>=1, source1 is a failure;
* at a>=2,b=0, source0 continues to b=1, then source1 fails;
* at a=1,b>=1, source1 continues to anchor2, then source1 fails;
* at a=1,b=0, source0 continues to anchor2,b=1, then source1 fails.

All other channels compete normally. The maximum total genuine rate
inside (4) is <=K_raw(1+M_in+C_H)^7. Consequently each block of two
genuine reactions has conditional absorption probability at least

    p>=c_raw(1+M_in+C_H)^(-14).                          (6)

This is a lower bound from an actual path, not deletion-word sufficiency
for recurrence. It works here because the GLOBAL stopped population cap
has already been proved. The number J_all of all genuine reactions to
absorption is dominated by twice a geometric variable with parameter p.
The two constant source0 channels remain live with total hazard B0>0,
so the physical clock is also paid. For every fixed integer r>=1,

    E J_all^r + E sigma^r <= C_H,r(1+M_in)^(14r).         (7)

For example the physical tail follows by splitting at J_all>B0*t/2:
if sigma>t with at most B0*t/2 genuine events, the independent constant
input Poisson clock has made at most half its mean count. Its exponential
lower tail and the geometric reaction-count tail prove (7).

This result does not DEMAND finite activity for the larger recurrence
theorem; it happens to acquire it for this particular finite stopped trace.

## 5. A real finite boundary operator, not a supplied oracle

For each finite input, (4) and the anchor head give an actual finite set
of possible continuing states, bounded by

    (h+1)^2 * binomial(M_in+C_H+4,4).

Its full generator, failure halo, clock and genuine-count rewards are
enumerable from the raw list. Absorption has been proved by (6), so its
finite killed inverse exists. For rational rates this yields exact
rational output and reward values by ordinary finite linear algebra.
One must still acquire that finite data when advertising a numerical
solver. Complexity polynomial in M is generally exponential in the bit
length of a population input; no practical or asymptotic advantage is
claimed.

The new operation is the raw policy, all-path cap and paid absorption,
not the established killed inverse itself. Accepted Astra Green/halo
constructions remain credited at their actual scopes.

## 6. Why strict negative-sign progress was the wrong premise

The positive-majority proof used a strictly decreasing noncore progress
and packet-periodic low anchors. Its naive negative-sign mirror cannot
have those properties. Consider a putative one-port f(a,b) packet-periodic
at anchors1 and2, nonincreasing under incoming packets, and strictly
decreasing on each designated noncore transition. Its requirements would
include

    f(1,0)=f(1,2)>f(2,2)=f(2,0)
           >f(3,1)>f(4,2)>f(1,0),                      (8)

an impossibility. The middle transitions are source0,source2,terminal;
the first is source1. This refutes that strict local representation,
not recurrence or a stopped physical argument.

The corresponding REAL neutral loop can be embedded with both ports
live. Starting at (A,B,C,D,E,F)=(1,0,n,1,2,m), m>=2, use

    COREb, I1, COREf, I0, I2, I3.

It returns to the EXACT initial physical state. Both core donors are
low (anchors1 or2). An unbounded number of such loops cannot be paid by
a fictitious decrease at every noncore step. The resources (3) remain
constant on the loop and (6),(7) instead pay its ACTUAL finite clock until
the complete trace absorbs.

## 7. What is still not earned

Neither (4) nor a finite killed inverse proves inward drift. Cleanup can
fail at a high-core transfer or an unselected source, and those actual
outputs may carry a new debt. A fixed positive population overrun and a
polynomial residence bound do not by themselves make their repetitions
positive recurrent. The negative/mixed-sign joint repayment and the
globally common receiving geometry remain unresolved.

This operation does remove a concrete obstacle across ALL bounded-anchor
hidden faces: neutral joint cycles cannot force an unbounded population
loan BEFORE the stop, and the full clock/output operator is acquired
rather than assumed. It is useful input to the global synthesis, not a
catalogue endpoint or an unrestricted weak-reversibility result.
