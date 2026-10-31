# Corrections retained in the audit trail

These were implementation/test issues, not suppressed theorem counterexamples.

1. The first cubic negative control reused direction (4,3,3), which works for the earlier acquired quadratic polynomial H=2A(B+C)+BC. The generalized cubic cone chose a different first vertex, H=2AC+(2/3)BC; its unattenuated quotient on that old direction was negative, so the assertion correctly failed. Inspecting its exact leading polynomial gave the relevant negative-leading direction (1,0,1). The corrected control uses the **same acquired cubic polynomial** with and without the required radial attenuation. Both the original independent base-polynomial fixture and the new acquired-polynomial fixture are retained under their actual scopes.

2. An expanded rational Foster constant for a small exponential base fit the requested 100,000-bit arithmetic expansion cap but exceeded Python's default 4,300-decimal-digit string-conversion limit. All mathematics and state assertions had run, but JSON serialization failed. The constructor now has a separately disclosed 12,000-bit serialization cap and stores larger constants as exact rational-power expressions. The failed output file was empty, not treated as a completed result. Corrected replays finish and print complete JSON.

3. Independent review found that the first finite structural receiver validated support paths but accepted a falsified zero work count. This did not admit a false recurrence theorem, but violated exact accounting. The receiver was revised to independently replay the deterministic first-enabled support scan, compare its full trace, and bind both witness and reported work counts. The independent review preserves the previous source hash and tests the repaired receiver. No earlier accepted package was altered.

The explicit basis limit is only a basis-attempt cap. Polynomial preprocessing, scalar-bound arithmetic and memory are not capped by it; the README and final review retain that distinction.
