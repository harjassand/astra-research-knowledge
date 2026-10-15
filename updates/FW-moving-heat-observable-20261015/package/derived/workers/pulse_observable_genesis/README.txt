Retained result: an actual-input positive RC hard pair plus a sharp acquisition
law for its informed convex segment. Historical novelty unestablished; physical
validation and an advantage over experimentally validated incumbents absent.

Read PROOF.txt first. It gives the explicit construction, all-waveform and
adaptive indistinguishability proofs, optimal finite-ramp probe, sharp segment
minimax risk, numerical scope, prior confrontation, and reproducibility.

verified_hard_pair.json contains exact rational coefficients/errors and
authoritative directed decimal-string interval enclosures.
verify_hard_pair.py independently verifies its arithmetic using mpmath only.
joint_pair_candidates.json and explore_joint_pair.py retain the exploratory
shared-baseline optimization that generated the chosen witness.
PRIMARY_SOURCES.json records primary literature and inspection limits.
FROZEN_MANIFEST.json pins the artifact files and immutable input/source hashes.

Important distinction: 0.1 mOhm is the source EIS-box premise, not calibrated
model error. eta is a separate symbolic bounded voltage-error / peak-current
premise, in mOhm (mV/A). Do not identify these without measured evidence.

The 58-point source interface admits Q1000=187.72905... and 266.16089... mOhm.
After ANY admissible 10-second peak-limited scalar-current experiment, a bounded
voltage error eta>=0.015181226 mOhm can still conceal which model generated the
entire record. An ideal pulse is exactly optimal for this pair after its common
inductance is removed; a maximum ramp/plateau is exactly optimal with a slew
limit. At hypothetical eta=0.1 mOhm and a one-second rise time, the known binary
pair needs more than about 26.486584 seconds for certain discrimination.

This is not an acquisition-time lower bound under every possible noise law,
not a global minimax optimizer over all EIS-feasible models, not a validated
battery experiment, and not an obstruction for the complete original dataset's
additional pulse and pseudo-open-circuit observations. The rejected full-band
positive RC model remains rejected.

Audit correction: mpmath float(endpoint) plus one nextafter was found unreliable
for outward decimal displays. The frozen checker extracts exact binary
endpoints into Fractions and directs decimal rounding instead. Exact rational
EIS feasibility and the analytic theorem were unaffected.
