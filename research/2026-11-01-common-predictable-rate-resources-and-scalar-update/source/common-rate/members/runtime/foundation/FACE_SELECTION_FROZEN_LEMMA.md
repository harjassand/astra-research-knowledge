# Exact multiscale face selection without an activation oracle

**Separate author proof/component, not a global Foster join.** Let a>=0 and
x_1,...,x_n>=0 be counts, n>=2, on a nonempty simple satellite graph. Put
N=a+sum x. Fix rational0<delta<=1/4 and acquire

 eta=delta/(4n), h=eta^(n-1)/(2n),
 epsilon=min(1/4,h²/2,h/8), gamma=delta*h/8.

There is an explicit finite algorithm returning one of:
1. a>gamma N;
2. an edge whose BOTH endpoints have count>gamma N;
3. a nonempty independent I, with U=a+sum_{j outside I}x_j,
   fmin=min_{i in I}x_i>0, U<=delta fmin, and either U=0 or
   T=a*F_I+Qcross+Qfar>=epsilon U².
Here F_I=sum_I x, Near=N(I)\I, Far=remaining vertices,
Qcross=sum_{I--Near edges} x_i x_j, Qfar=sum_{Far--Far edges}x_i x_j.
N=0 is separately returned as the zero state. At most n face stages are used.

Outputs1/2 are genuine interior witnesses: R=a+minimum weighted vertex cover
is then>gamma N, without computing that minimum cover. Output3 is the actual
unbalanced-count activation used by the local-face lemma. No graph maximality,
stationary law, or favorable face is a supplied premise.

## Prefix-gap operation

Sort a nonzero set of m<=n counts in decreasing order and retain a prefix ending
at the FIRST gap x_next<=eta*x_last; retain all if no such gap occurs. Its
smallest retained value is at least eta^(n-1) times the largest. Every remaining
value is<=eta times this smallest retained value. At most n remain, so their
sum is<=n eta times it. The prefix cannot contain a zero if total mass is positive.

## Initial face

If a>gamma N return1. Otherwise a<=gamma N<=N/2, so the largest satellite is
at least N/(2n). Apply prefix-gap; its minimum is>=hN. If the prefix contains
an edge return2, since h>gamma. If not, call it I. Its outside mass obeys

 U<=a+n eta fmin<=gamma N+delta fmin/4
   <=delta fmin/8+delta fmin/4=3delta fmin/8.

Thus the cone is earned, with room to spare. No minimum-cover enumeration was
needed; the edge check itself certifies the alternative.

## Extension after an actual activation failure

If U=0 return the pure face. If T>=epsilon U² return activated face. Otherwise
Qcross>=fmin*NearMass and aF_I>=a*fmin imply

 a+NearMass<T/fmin<epsilon U²/fmin<=epsilon delta U.

Hence FarMass>U/2. Prefix-gap applied to Far yields nonempty J with minimum
b>=hU and remaining Far mass<=delta b/4. It is independent: any internal
J edge would contribute at least b²>=h²U²>epsilon U² to Qfar, contradicting
the failed activation. J is Far, so it has no edge to I either.

Extend I to I'=I union J. Since b<=U<=delta fmin<fmin, the new minimum is b.
The new outside mass is bounded by

 U'<=epsilon delta U+delta b/4
    <=delta b/8+delta b/4=3delta b/8,

using epsilon<=h/8 and b>=hU. Thus the SAME cone is preserved. Each failed
activation adds at least one vertex. If Far is empty but U>0, then
T>=fmin U>=U²/delta>epsilon U², so failure is impossible. Consequently the
algorithm terminates in at most n stages with an actual witness.

## What is still missing

The local-face profile weights make J comparable to U with acquired constants.
For large enough J the displayed T bound therefore gives a uniform negative
local tail; bounded J has its acquired birth head. Combined with the interior
case, this provides a constructive FINITE COVER by negative candidates. It does
not produce a single Lyapunov function or sampled return kernel.

In particular max_I g(J_I)=g(min_I J_I) does not inherit an upper generator
bound. A min-I cutoff can enter at positive O(N) rate during fast redistribution
between bulk coordinates while its multiplier at the source is zero. A source
reserve already multiplied by that zero cutoff cannot pay the entry cost.
Cutoff widths selected after enormous profile heads can also change the face
activation constants and create a circular acquisition if handled naively.
These are compatibility/receiving questions, not absent activation or face-search
oracles. No polynomial global constructor is claimed: building all independent-
face profiles may cost exponentially many raw subsets, even though this state
selection routine uses at most n sorts and graph scans.
