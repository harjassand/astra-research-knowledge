# Arbitrary FPT dependence can be diagonalized uniformly

30 October 2026. A strengthening of PACKED_GUARD_THEOREM Sections 7--8:
the computational negative needs only absence of SUBEXPONENTIAL-time
constant-advantage NC1-PRF distinguishers, not a single fixed exponential
security exponent. The source/guard/control program is unchanged. No new
numerical case, query experiment, or cryptographic instance is involved.

## 1. Explicit weaker premise

Keep the polynomial-time key generation, public template, polynomial key
length and fixed-key NC1 evaluation assumptions in the main proof. Replace
its security premise E by Esub:

    Every uniform classical randomized membership-oracle algorithm with
    time2^{o(n)} has distinguishing advantage<1/20 at every sufficiently
    large n (with its own cutoff).

This is still a quantitative cryptographic premise, stronger than ordinary
polynomial security. E implies Esub. The main proof's specified D4 premise
therefore supplies Esub too; ordinary qualitative LPN/DDH does not.
No arbitrary-FPT impossibility follows from polynomial security alone.

## 2. Pay the evaluation of the arbitrary parameter function

Suppose a uniform FPT learner exists with a COMPUTABLE integer bound

    f(d)*(T+alpha+L_in+1)^c                                       (1)

for fixed epsilon=1/64 and delta=1/3, including its standalone student's
one-output generation cost. The degree c is an absolute integer. Replace
f by a larger positive integer function if needed. The adversary may hardcode
the learner, c, and a program computing this witness bound f; existence of
such a program is part of the standard FPT definition. It is not supplied
to the learner as a scientific oracle.

For payload length n put B_n=2^{floor(sqrt(n))}. For EVERY integer
1<=p<=floor(sqrt(n)), run the program for f(2p+9) for at most B_n steps.
Call p qualified if it halts within that budget and its output is at most
B_n. Choose the largest qualified p; use p=1 if none qualify. Denote the
choice by p_n. This whole search costs at most sqrt(n)*B_n=2^{o(n)} steps,
even if some f computations are exceptionally inefficient. In particular
it does not assume that computing f(d) is polynomial in its value.

For EACH fixed p, both the value f(2p+9) and its computation time are finite.
Thus that p qualifies at every sufficiently large n. Consequently

    p_n -> infinity,     p_n<=sqrt(n),     f(2p_n+9)<=B_n          (2)

for all sufficiently large n. The qualification search is uniform; no
advice sequence or uncomputable inverse-growth function is used.

## 3. Instantiate the same source at this slowly growing parameter

Use the exact construction with p=p_n, s=ceil(n/p_n), d_n=2p_n+9. Public
read length L and active length remain polynomial(n), uniformly in p_n.
All integer state, guard, majority-copy and known-noise simulation work
is polynomial(n); the rank remains d_n. The declared bounds are

    log2(T+alpha+L_in+1) <=2n/p_n+O(log n),                       (3)

with an absolute O constant; d_n<=2sqrt(n)+9 is absorbed into that logarithm.
The finite parameter/description input has polynomial(n) bit length and
the source's original secret key is never supplied. T and alpha themselves
are computed as binary integers, not by first enumerating a length-T word.
Writing generated outputs and submitted prefixes is already charged.

Cap the learner plus generator by a sufficiently large fixed multiple of
B_n*(T+alpha+L_in+1)^c and reject malformed/time-exceeded output. By(1)--(3),
the real promised sources fit that cap; for an expected-time bound Markov
loses at most a chosen small constant, as in the main proof. The cap is
also enforced against the random-function simulator, where no structural
promise is being asserted. Total time, including qualification search,
oracle simulation, interpretation and fresh-payload verification, obeys

    log2(time) <=sqrt(n)+2c*n/p_n+O(log n)=o(n).                   (4)

Any fixed polynomial(n) overhead only changes the O(log n) term.

## 4. The full-law event survives this parameter choice

The teacher transcript discrepancy is at most16*q*2^{-2(n^2+1)} and its
copy failure at most m*2^{-2(n^2+1)}. Both vanish even for the subexponential
q in(4). Also q/2^n=o(1), so the first n emitted input bits are fresh with
probability1-o(1) under a TV-accurate standalone sampler. The EXACT same
test as in the main proof has real acceptance>=59/96-o(1), random-function
acceptance<=1/2, and constant advantage11/96-o(1). A fixed expected-time
cap reserve can reduce this by, for example,1/100 and still exceed1/20.
It is a uniform2^{o(n)} PRF distinguisher, contradicting Esub.

Thus Esub excludes arbitrary computable FPT f(d), not merely polynomial f.
This uses the NEW packed source's rank/dynamic-range tradeoff and the paid
diagonal selection(2). It does not reinterpret the old n+O(1)-rank PRF
construction as an FPT obstruction.

## 5. The sublinear-rank exponent consequence survives too

Suppose instead the claimed bound is

    f(d)*(T+alpha)^h(d)*poly(L_in),       h(d)=o(d),               (5)

where f,h are computable nonnegative integer-valued bound functions
(rounding up an exponent preserves o(d)). Qualify a p only if BOTH f(2p+9)
and h(2p+9) halt within B_n steps and both values are<=B_n. This doubles
the search budget and still gives p_n->infinity. For sufficiently large n,
h(2p_n+9)<=O(p_n). Therefore its logarithmic total time is at most

    sqrt(n)+2n*h(2p_n+9)/p_n+O(h(2p_n+9)*log n)+O(log n)=o(n).

The second term is o(n) by h(d)=o(d), and the third is at most
O(sqrt(n)*log n)=o(n). Computing the cap from the qualified integer values
requires only polynomial work in its bit length. The identical fresh-label
test again contradicts Esub. Thus the conditional linear-exponent boundary
does not require assuming a particular fixed exponential security exponent.

## 6. Scope

The original no-FPT proof under E remains correct, with its simpler fixed-p
limit order. This appendix weakens the premise by choosing p_n uniformly
slowly enough to pay ANY computable parameter dependence. It supplies no
unconditional computational lower bound, no quantum-security conclusion,
and no evaluated cryptographic instance. The fixed-d XP/native compiler
still takes T^{O(d)} and can have2^{O(n)} cost on these packed sources;
neither (4) nor (5) applies to it. Its established positive theorem is
preserved without contradiction.
