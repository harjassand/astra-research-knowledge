# Bounded-bit reporting of certified optimization gaps

2026-10-29 — receiving review requested. This is an additive implementation of the accepted variable-gap/observable-gap interfaces, not a change to the raw lower-bound certificates.

Let e>=0 be the exact candidate-minus-sound-lower gap. Let Bcap be a public dyadic cap with e<=Bcap on every query; if the analytical cap is not dyadic, first round that PUBLIC cap upward. Fix public b with Bcap*2^b integral and report

 e_report=min(Bcap,2^{-b} ceil(2^b e)).

Then e<=e_report<=e+2^{-b}, and0<=e_report<=Bcap. The approximate-action finite-difference proof only requires a pointwise UPPER bound on optimization error, so it remains valid with e_report. The nonnegative-gap supermartingale applies directly to the reported variable and its conditional mean using cap Bcap. No expectation is estimated by a realized sum. Raw candidate/lower certificates remain intact; reported counters are explicitly conservative upper gaps, not exact equality claims.

AfterN reports the added aggregate is at mostN2^{-b}. Maintain integer units rather than arbitrary-denominator rational sums. Counter storage is at most b+ceil(log2(N Bcap+1))+O(1) bits. The public cap and precision are themselves charged. Per-edge counts can be combined with the same known denominator. This avoids the large LCM denominator growth observed when summing exact rational Gram-repair gaps.

Executable: dyadic_gap_counter.py. Both prior360-query OFFLINE replay files were processed with b39 and Bcap340050. There are120 reports per edge, so maximum upward excess is120/2^39 per edge. The improved bounded-SOS cumulative counters use34 bits per edge; the loose DD baseline counters use56 bits. Every rounded report and the final sum were checked exactly against retained raw certificates. Zero/cap boundaries and multiple b choices are tested.

This is only an arithmetic/resource improvement. The records are still from an old fixed query history, not a new controller/source trajectory; no readiness or expected-gap conclusion follows merely from their values. The live protocol still needs the source/control/key privacy and finite-clock interfaces from its governing theorem.
