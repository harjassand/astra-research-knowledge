# Exact tagged-path diagnostic

Run `python replay.py` from this directory or any current directory. The script
uses only Python's standard library and exact `fractions.Fraction` arithmetic.
It checks the frozen `INPUTS.json` hash against `FREEZE.json` before evaluation.
There is no fitting or parameter search.

This is a newly defined four-state reciprocal, nonreversible proposal. Its
clockwise proposal likelihood product is 8 and the reverse product is 1/8.
The proposal-start target model, screen, second correction, global IMH rule and
actual lazy rejection diagonal are built explicitly. The screen is rational
because eta=1/2, kappa=0 and the unnormalized q entries are rational squares.
All target detailed-balance equations and row sums are checked exactly.

The fixed inputs have D(pi||q)<24 by the displayed exact admission bound;
they are not asserted to satisfy K=1 or to lie on the asymptotic critical
sequence. The finite path lemma does not require a KL bound. This diagnostic
checks its algebra and event containment, not a critical amplitude.

The single execution passed 16,401 exact tagged-path identity checks and
enumerated 4,686 first-hit paths at deterministic N=5. Among them were 640
high-signed-progress paths whose final hit was global; their positive-progress
threshold was reached strictly earlier, as required by the proof. Positive and
negative signed cycles, actual diagonal factors, low-progress reverse bounds,
native row budgets and an independent first-hit recurrence were checked.

Observed diagnostic CPU was 0.129040814 seconds and wall time 0.12904939099826152
seconds, with reported peak RSS 10,624 KiB. These are the diagnostic body's
reported resources, not discovery or inference cost. The source-bound complete
receipt is `RESOURCE_RECEIPT.json`. All unavailable totals remain unknown.

No historical fixture, old scientific suite, long Markov run, huge support,
external service, hardware or paid resource was used. Existing frozen admitted
and failed examples are untouched.
