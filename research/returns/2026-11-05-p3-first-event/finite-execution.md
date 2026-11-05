# Executed first-event diagnostic and separately certified huge clock

The supplied [execution supplement](package/next4_root/execution_supplement.tex), [summary](package/next4_execution/execution_summary.json), [schedule certificate](package/next4_execution/acquired_schedule_certificate.json) and [event records](package/next4_execution/event_records.json) distinguish a genuine four-state execution from the [general theorem](README.md). The original C++/Python and native binary are retained as source evidence; Capital did not compile or run them.

The fixture has target `{2,3}`, `d=2^-100`, `a=1-3d` and invariant law `(2a/3,a/3,d,2d)`. A reset-to-pi generator plus directed cycle `0->2->1->3->0` preserves pi while violating detailed balance. Static rare access is elementary here; the general correlated Gibbs algorithm was not executed. With R=4, g=1/4, zeta=d, initial state 0, H=5 and mesh `2^-10`, the diagnostic uses b=320,L=65,536, 4,096 calibration proposals and 1,024 accepted conditional records.

| Quantity | Supplied value/scope |
|---|---|
| Stationary target mass | `2.3665827156630354e-30` |
| Exact mean first-event time from state 0 | `2.535301200456459e29` model time units |
| Exact / acquired block probability q_G | `6.4618554975e-26` / `6.4748373561e-26` |
| Observed relative probability error | About `.002009` |
| Empirical four-entry-category TV | `.0198568`; **not whole-path TV** |
| Empirical event-time KS distance | `.0304789` |
| Sample mean / exact mean | `1.0411672` |

Reference values were loaded only after calibration and geometric-clock generation. The independently constructed 180-digit four-state solver took about `.09 s` and is the faster appropriate baseline, not an inferior rejection simulator.

## What is certified and what remains floating

The acquired Palm statistic has an exact rational histogram value. Its mean interval plus a rational mixing bound gives, **assuming ideal independent Palm clocks**, structural error at most `.01282038` and parameter/geometric replacement error at most `.06741831`, total `.08023869` before finite-primitive errors. The confidence failure bound is below `.00676317`. Standard-library floating Poisson/gamma/order-statistic/binomial clocks do not have certified distribution errors here; this is not an end-to-end implementation certificate.

The huge waiting index actually attached to all 1,024 records uses the separate [finite-bit integer compiler](package/next4_execution/finite_geometric.py) and [exact rational checks](package/next4_theory/02_GEOMETRIC_CHECKS.json). At tolerance `2^-24`, it stores 89 powers with 205 fractional bits, uses 116 random bits per draw and caps the failed-block index at `370665681317113387681080266` (89 bits). It uses binary powers/CDF comparisons rather than iterating failed blocks. Its theorem assumes independent unbiased bits; the execution uses a seeded PRNG. Calendar indices remain integers/decimal strings, avoiding enormous-time floating conversion.

## Complete execution costs

The native run made **428,007,591** forward/reverse updates, including **268,446,811** for calibration; 998,834,361 PRNG words; 214,033,844 integer categorical calls; 35,680,481 integer rejection retries; 7,550 Poisson, 13,052 gamma and 1,024 binomial calls. Native execution took about 12.31 s on the producer executor. Integer geometric draws added about `.97 s`, 3,808,709 multiplications and 90,446 CDF queries. These are producer machine timings, not new Capital runs or physical exposure.

At epsilon=.1,delta=.01 the conservative **uniform** recipe instead prescribes b=444,L=18,472,960, 67,108,864,000 calibration proposals and roughly `1.24e18` leading updates. That sufficient schedule was **not executed** and is not a necessary cost; the instance certificate supports the smaller chosen schedule under its ideal-clock assumptions.

Exact-rational enumeration checks the Palm density on 1,364 short state paths. Wrong forward-as-reverse dynamics change the conditional path law; a wrong-direction boundary reconstruction differs by about TV `.4` from the correct first-entry law in the rare fixture. This tests time-direction sensitivity, not practical advantage on a large unknown physical system. [All original files and provenance](SOURCES.json).
