# Controlling correction-angle and detector-instrument qualifications

This addendum qualifies the unchanged nine-file finite-LO source freeze. It
does not claim an actual detector or calibrated control implementation.

## End-to-end angle tolerance

The numerical 4e-6 complete-error allowance is valid when EACH qubit's total
implemented phase differs by at most1e-6 radians from the EXACT ideal wrapped
correction angle. This total includes finite-table computation/rounding as well
as actuator/calibration error. The frozen exact table computation is bounded
below1e-8 radians. A sufficient split is therefore table error<=1e-8 and
actuator error<=0.99e-6 relative to the table command.

If instead an apparatus only promises actuator error<=1e-6 relative to the
rounded command, add the table error separately: a conservative extra complete
budget is4e-8 using the displayed table bound. The original exact numerical
grid is accepted under the END-TO-END1e-6 specification, not under an omitted
rounding term. Its accepted pass/fail values are otherwise unchanged.

## Number misassignment is an instrument statement

The example penalty2 epsilon_num applies to classical mislabeling AFTER the
declared number instrument, or to an explicitly received bad-event CP coupling
whose total probability is<=epsilon_num uniformly on every admitted data plus
reference input. The complete operation then differs only on that event.

A Fock-state confusion matrix or a preferred-input misassignment frequency
alone does not establish this complete instrument condition for a general
coherent optical measurement. Coherent POVM errors, hidden modes, detector
backaction and correlations with the data/control require their actual model
or a separately received complete-channel bound. They must not be converted
to2 epsilon_num merely by calling them misassignment.

The frozen grid's0.001 remaining allowance is already an explicitly SUPPLIED
complete-error bound covering such additional imperfections; it has not been
experimentally acquired or replaced by a confusion-matrix test. This addendum
does not change any exact optical/counting probability or certified grid term.
