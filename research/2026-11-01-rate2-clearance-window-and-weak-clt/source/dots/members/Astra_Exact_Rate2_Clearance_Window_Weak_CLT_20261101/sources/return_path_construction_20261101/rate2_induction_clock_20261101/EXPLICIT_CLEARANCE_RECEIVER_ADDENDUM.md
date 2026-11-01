# Explicit replacement of the interior acquisition gate

**Author addendum, pending independent review of the new harmonic receiver and
this join.** Existing frozen clock and stability sources are unchanged.

The earlier clearance continuation
`ACTUAL_CLEARANCE_WINDOW_AND_OCCUPATION.md`, SHA256
 0eeb311064eaaad654d69ada711e22d26b4e8622b38d15e3a3998bcfbae1bd4d,
left a numerical acquisition gate at the interior constants c(epsilon),n0(epsilon).
The new actual-generator receiver
`../rate2_explicit_macro_removal/EXPLICIT_HARMONIC_PERSISTENCE_AND_REMOVAL.md`,
SHA256 4d1ad7a929f7e3c6d81d06222bd8217eb96e06eb183e6f0cfe3f5dbca6ca16ca,
replaces exactly that interface, without a deterministic attraction supplier.

## 1. Explicit parameters and hypotheses

Retain the finite-level hypotheses and notation from
`FINITE_LEVEL_CORRECTED_CLOCK.md`, SHA256
 e0700bad37717a38976f295049a8d2cb1120aeb155c343783780d6b201f20c9d:
K>=10^40, 0<a<=1/4, T=N^(1/5), p=K+1,
q=2sqrt(K+1)+1, H=p+q+1, the three finite algebraic size tests,
and B_clock,B_A. Keep delta=10^-100, Cstar=3*10^12 and KT<=delta N.
Set the new literal receiver parameters

    m0=delta/2,
    h=400/m0^2=1600delta^-2,
    N>=32h=51200delta^-2.                               (1)

These replace ALL requirements involving n0(epsilon),c(epsilon).
There is no remaining unspecified interior constant in this version.

## 2. The actual macro entrance receives the harmonic theorem

On the same good finite-level/dyadic path and before either mass-band exit,
the first macro L>=delta N has

    (1-delta)N<=S<=(1+delta)N,
    M=A+min(C,D)=L-|C-D|/2>=delta N/2=m0N.              (2)

Indeed the accepted last-stage bound gives
`|C-D|<=m_j/16+1<=delta N/16+1`; since delta N>=4, (2) follows.
If the finite-level entrance itself is already macro, its C-D is exactly zero.
Thus initial macro states cause no unsupported upper-overshoot assertion.
Since delta<1/4, (2) lies in .75N<S<=1.25N, exactly the harmonic receiver's
upper as well as lower entrance region. No positive fraction of B or E is needed.

Strong Markov at this actual entrance receives the uniform actual conclusion
S after h additional physical units <=13N/16, except on the explicit sum

    B_harm=32N^2 h exp[-delta N/2000]
       +exp[-200N^2/(32h+20/3)]+exp(-N/2)+exp(-N/96).    (3)

The theorem's original-immigration and unused-time costs are already in (3).
Its actual clock is not replaced by an independent service attempt. Its uniform
conditional bound is applied at the genuine past-measurable entrance.
Since 13N/16<15(N+2)/16, this is actual clearance of the original target.

## 3. Fully explicit analytical first-passage/occupation packet

Let tau_clear be the first S<=15(N+2)/16 hit. Replace the earlier error terms by

    B_imm_exp=P(Pois(4T+h)>delta N/2-2),
    B_stage=32exp[-KT/Cstar],
    B_band=P(Pois(4*10^4sqrt(delta))>=ceil(delta N)),
    B_exp=B_clock+B_A+B_imm_exp+B_stage+B_band+B_harm.

Use ONE original immigration counter over [0,4T+h] for the headroom event.
This deliberately conservative charge includes the service interval as well;
it does not make a fresh independence assertion at phase boundaries. Its cost
is retained even though the harmonic theorem already prices its own conditional
immigration event. Double counting an error only weakens the bound.
Then the exact continued proof gives

    P{(s_K-a)T<=tau_clear
       <=(s_K+a)T+32T/K^(3/2)+h} >=1-B_exp.             (4)

The original finite-level no-death lower bound, the dyadic common-clock good
event, and the lower-band death tail are unchanged. The entire upper time is
<=4T+h. Every quantity in (1)-(4) is now a literal algebraic, exponential or
Poisson-tail expression, plus the ordinary scalar s_K. No hidden finite-cover
or attraction constant remains.

The earlier occupation outputs also remain valid: with additional error
`24p^2/T`, actual A occupation before macro entrance is <=1/T+4*10^4sqrt(delta).
At actual clearance, occupation is >(N+2)/32 except on
`P(Pois((N+2)/32)>=ceil((N+2)/16))`. These are continuing actual-clock statements,
not unconditional expected-occupation limits or stationary assertions.

For each fixed K,a, every term in B_exp tends to zero as N tends to infinity,
and h/T tends to zero. With the same N-then-K order and the scalar tail bound
`0<s_*-s_K<=sqrt(3)/[9(K-2)^(3/2)]`, this version proves the same actual
clearance LLN without importing the interior global-attractor component.

## 4. Cost and numerical admission

This is a FULLY EXPLICIT ANALYTICAL certificate, not a claim that a numerical
admission implementation has been run. Such an implementation must check all
size tests, certify the scalar interval and Poisson/exponential error enclosures,
and return UNKNOWN if its total error or work/bit budget fails. Enormous values
must not be expanded merely to compare an exponent; exact logarithmic or interval
comparisons are appropriate when separately received.
The costs remain severe: h=1600*10^200, and the inherited K>=10^40 plus the
coarse H^6/T bound can require N around 10^1200 or more for modest errors.
Removing an unspecified supplier is a genuine acquisition improvement, not a
practical predictor claim. No CDF approximation by a point mass, distribution
kernel, central-limit law, changing-rate operation or arbitrary-network theorem
is inferred.
