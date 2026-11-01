# Uniform fully retained initial-growth clock

**Author theorem candidate, pending independent review.** This is a uniformly
paid hitting law, not a population-removal, recurrence, or stationary-moment
statement. It applies to the rate-2 five-species count tree and retains every
actual channel, including deaths and all unsuccessful returns.

## 1. Exact domain, coordinate and function

The rates are unit for 0<->A, 2A<->AC, 2A<->AD, 2A<->AE, AE<->CD, CD<->AB,
except CD->AE has rate 2. Propensities use falling factorials. Fix integers N,m>=1
such that

  N>=10^8(m+1)^2.                                           (1)

N is a reference parameter, not a variable total count. Define on all states

  M=A+min(C,D), R=C+D+E,
  phi(M,R)=min(1,max(0,[96-R/(M+1)]/48)),
  h=1+(16/N)phi(M,R) A^2,
  V=2^(-M) h.                                               (2)

The pointwise domain is B>=N/2 and M<m. Targets of transitions leaving that domain
are evaluated by the SAME formula (2). No killed transition or boundary reset is
used in the generator calculation. Throughout this domain and its one-jump targets,
A<=m and

  1<=h<=101/100.                                            (3)

The claimed actual-generator inequality is

  L V<=-V/4,  whenever B>=N/2 and M<m.                       (4)

## 2. All M jumps and source groups

Every M jump is 0,+1 or -1. Its total negative-jump intensity q_minus is

  A+3A(A-1), if C=D,
  A+2A(A-1), if C!=D.

Hence A^2<=q_minus<=3A^2, including A=0. Immigration is always a positive M jump.
AE->2A is a positive M jump; AC->2A is positive when C>D, and AD->2A is positive
when D>C. AB<->CD and CD->AE, AE->CD preserve M exactly.

On every negative M jump, A decreases by one while R does not decrease. The
cutoff phi therefore does not increase, and h_after<=h_before. Using (3), a
positive M jump contributes at most -(99/200) times its rate to LV/2^(-M), while
a negative M jump contributes at most (101/100) times its rate.

All zero-M jumps except CD->AB, CD->AE, and possibly AC/AD->2A have nonpositive
h change. In particular the true AB->CD capture decreases both A and the cutoff
and is a useful phase reserve.

## 3. Full cost of positive zero-M phase jumps

For one of the positive zero-M phase jumps, A increases by one and R decreases
by j=1 or 2, while M is unchanged. The cutoff's Lipschitz constant as a function
of R is 1/[48(M+1)]. Therefore

  Delta[A^2 phi] <=2A+1+A^2/[24(M+1)]<=3A+1.                (5)

If the change is positive then phi_after>0, so R<=98(M+1). Consequently CD is
at most 2401(M+1)^2 and the total intensity of the relevant source groups is
at most

  7203(M+1)^2+98A(M+1).

Using 3A+1<=2(A^2+1) for integer A and A(3A+1)<=4A^2, (5) bounds their entire
positive contribution to LV/2^(-M) by

  240000(m+1)^2(A^2+1)/N <=(A^2+1)/100.                    (6)

This is the actual cost of cutoff crossings and reverse-arm phase changes. It
is not a claim that the individual channels are favorable.

## 4. Core and outer-region payments

In the core R<=48(M+1), phi_before=1. For AB->CD, M is unchanged and the new
cutoff is no larger. Its phase change is at most -16(2A-1)/N. Multiplication by
its actual rate AB and use of B>=N/2 give the reserve -8A^2 (with the same bound
at A=0). Discarding other favorable positive-M jumps but keeping immigration,
(6) yields

  LV/2^(-M) <=-99/200-8A^2+(101/100)3A^2+(A^2+1)/100
             <=-12/25.                                   (7)

Outside the core, R>48(M+1), so max(C,D,E)>16(M+1). If the maximum is E,
AE->2A is an actual positive M jump of rate AE. If it is C or D, that satellite
is strictly larger than the other one (the smaller is at most M), and its arm
return to 2A is an actual positive M jump. Thus a positive-jump source group has
rate at least A max(C,D,E), which is at least 4q_minus. This remains true at
A=0, where q_minus=0. Combining its reserve with immigration and (6),

  LV/2^(-M) <=-99/200-[4(99/200)-101/100]q_minus
                         +(A^2+1)/100
             <=-12/25.                                   (8)

There is no assumption that A is in a stationary fiber. Equations (7)-(8),
together with h<=101/100, imply the deliberately weaker bound (4).

## 5. Paid uniform actual hitting law

Let sigma be the first actual time at which M>=m OR B<N/2. Give either event
success priority over auxiliary localization exits. No actual channel is removed.
A positive M jump is at most one, so M(sigma)<=m; a B-exit jump cannot increase
M above m either. Therefore V at the terminal state is at least 2^(-m).

Constant-rate immigration bounds the total count on each finite horizon, proving
nonexplosion and legitimizing stopped Dynkin. Applying the integrating factor
from (4), localizing and taking Fatou gives

  E_x exp(sigma/4) <=2^m V(x)<= (101/100)2^m.                (9)

In particular sigma is finite almost surely and, uniformly over EVERY initial
state with B>=N/2 and M<m,

  P_x(sigma>t) <=(101/100)exp[m log2-t/4],
  P_x(sigma>8m) <=(101/100)exp(-m).                         (10)

The exit can instead be B<N/2. That is an explicitly named output, not silently
identified with macroscopic A occupation or a loss of total population.

## 6. Possible scales and remaining consumers

For any fixed K, m=ceil(K N^(1/5)) satisfies (1) beyond an explicitly checkable
finite N threshold. Thus (10) gives a fully retained, uniform, exponentially
priced first M scale without the earlier fixed-level fluid approximation.
A slower choice m=floor(sqrt(N)/(2*10^4)) also satisfies (1) for N>=4*10^8 and
yields an O(sqrt(N)) paid clock with exponential-in-sqrt(N) failure.

Neither output of (10) yet receives the old balanced dyadic entrance: at M=m,
E and C-D may be arbitrary and A may be a large share of M. At B<N/2 the non-B
mass may be unbalanced. These interfaces, their actual occupation/removal blocks,
and any sampled-kernel stationary-moment argument remain separate operations.
No recurrence or tail conclusion is claimed by this initial-growth theorem.

## 7. Construction and costs

The function uses one min, a rational piecewise-linear cutoff, a finite integer
power 2^(-M), and rational arithmetic. Evaluation at a supplied state is exact;
expanding its power costs O(M) bits, so an exponent/bit budget may refuse it.
The mathematical bound uses no face enumeration, oracle, numerical fluid limit,
or assumed attempt independence. The square-root and fifth-root scale choices
are optional exact algebraic expressions, not hidden unit-cost numerical inputs.
