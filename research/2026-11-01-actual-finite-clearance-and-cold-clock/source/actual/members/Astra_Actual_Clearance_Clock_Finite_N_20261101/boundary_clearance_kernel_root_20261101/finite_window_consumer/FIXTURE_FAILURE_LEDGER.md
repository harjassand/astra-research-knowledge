# Explicit failure sum for the two finite-window fixtures

Root conditional numerical join; depends on independent acceptance of all component sources. Fixtures only: T=10000 or100000, N=T^5. Every event refers to the original raw path until cap or original4T; the five-unit entropy receiver starts conditionally at the actual cap.

The literal failure terms are:

1. Original count-band failure: exp(-N/6200)+exp(-T)+exp(-5T).
2. Actual startup/A/Z/floor/time/source-budget gates: the source-bound finite-sum table, below10^-8 for BOTH fixtures. These include their own startup and original E-counter charges; do not add them again.
3. Global upper ratio: exp(-276).
4. Additional regularized-source gate U>=-T³: exp[-(T³-1)/20].
5. Regularized weighted source Q budget: exp(-T³/2500).
6. Bounded-primitive bracket budget: exp(-T/80).
7. Full corrected-clock martingale: 2exp(-6)<1/200, by the exact rational exponential partial sum exceeding400.
8. Five-unit entropy endpoint receiver: delta_5 in ACTUAL_SOURCE_GATE_AND_FAST_HANDOFF.md.

Each individual exponential in entries1,3,4,5,6 is <=2^-100, since its exponent is at least100 and e>2. There are seven such terms.

For entry8, use ell=log(6N)<64. An exact proof is e^4>50 from its Taylor partial sum, hence e^64>50^16>6*10^25. Put y=x/N=N/(1920*10^12)-169. Throughout these two fixtures y>=50000 and y/N<1/(1920*10^12). Therefore the exponential entropy bound has exponent

 y²/[520 ell²+(4/3)ell y/N] > 50000²/(520*64²+1)>1000.

Its failure is <=2^-1000. The entropy persistence prefactor is
160N² exp(-N/10^9). Since160N²<2^200 and N/10^9>=10^11, this too is <2^-1000. The death and immigration exponentials exp(-N/64),exp(-N/96) are each <=2^-1000. Thus delta_5<=4*2^-1000. This weaker rational ceiling is sufficient and requires no high-precision exponential evaluation or finite-state simulation.

The whole failure is consequently less than

 1/200 +1/10^8 +16/2^100 <1/100.

The surplus power-of-two allowance conservatively covers all seven pre-cap exponentials and four entropy terms. This does not count an unknown event as negligible: every named event has a received formula, and no further drift/bracket/gate event may be silently added without updating the ledger.

The numerical consumer may report at least99% confidence only after its source binding verifies the raw drift, full bracket/jump, padded startup domain, and whole same-path composition. Until then its output is explicitly pending.
