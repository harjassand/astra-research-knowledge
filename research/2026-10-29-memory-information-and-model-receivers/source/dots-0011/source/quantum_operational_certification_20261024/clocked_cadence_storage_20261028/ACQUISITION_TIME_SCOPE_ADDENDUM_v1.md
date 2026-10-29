# Acquisition-time accounting clarification

28 October2026. No numerical result changes.

The reported127,838,208 reference-time units sum the elapsed durations of the61,440 individual selection/validation trajectories. The five data carriers operate in parallel **inside each trajectory**. This is not summed carrier-time or total hardware-qubit-time, and it is not an assumed laboratory wall-clock duration when trajectories can run in parallel.

The corresponding five-data-carrier duration sum is639,191,040 carrier-time units, before endpoint preparation/readout. Ancilla live-time is additional and branch dependent; the current pilot does not report an exact averaged ancilla-time bill. Its fixed201-unit EC windows do reserve the physical two-ancilla apparatus, but a skipped check does not keep an ancilla logically live in the channel model.

Native carrier exposures, trajectory counts, summed trajectory time, available parallelism and hardware/energy costs are distinct resources. No conversion from arbitrary reference units to seconds, watts or hardware performance is supplied. The prior learned-frame acquisition is separate inherited capital, not included in this new trajectory sum.
