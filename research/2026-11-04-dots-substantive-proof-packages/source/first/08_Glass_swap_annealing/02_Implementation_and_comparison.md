# Last decisive test: reversible proximity handover

2026-11-04. Conclusion: passive handover can evade full-release kinetics in principle and in existing bond-exchange materials. We have NOT acquired its exclusive, packing-shape-changing implementation or a matched annealing advantage. Preserve as a scoped hypothesis, not a breakthrough or a general no-go.

## Exact reversible finite-time construction

Let A and C be valid endpoint assignments, and B a shared-token bridge. For arbitrary endpoint energies, microscopic detailed balance requires k_AB/k_BA=exp[-beta(E_B-E_A)] and k_CB/k_BC=exp[-beta(E_B-E_C)]. Eliminating B in trace time gives

k_AC = k_AB k_BC/(k_BA+k_BC),
k_CA = k_CB k_BA/(k_BA+k_BC).

Their ratio is exp[-beta(E_C-E_A)]. No fuel or thermal-path reversal is necessary. These are trace-time rates, not claims that bridge duration is zero in wall-clock time.

For equal-energy endpoints take A->B=C->B=a and B->A=B->C=b. Then stationary bridge fraction f=a/(a+2b), mean bridge residence 1/(2b), and mean A-to-C first-passage time T=2/a+1/b. Consequently 1/T=fb. This last identity is model-specific, not a universal bound on every handover topology. It expresses the occupancy/throughput relation in a completely solvable model.

At tolerated bridge fraction .001:
- One endpoint transfer per 1000s needs b=1/s and mean bridge residence .5s.
- One per 100s needs b=10/s and mean residence .05s.
- One per second needs b=1000/s and mean residence .0005s.

The bridge free energy is ~6.214 kBT above either endpoint for all three examples. Detailed balance does not forbid these rates; it fixes ratios, not a universal kinetic ceiling. A transition-state catalyst can increase rates without altering endpoint weights. `handover_test.py` verifies stationarity, detailed balance and exact mean hitting times. All rate choices are hypothetical, not measured molecular parameters.

Thus the earlier 2003s release calculation is not a bound on handover. A 50ms bridge with low occupancy would improve that example's first-passage rate approximately twentyfold. We have no acquired loaded single-token implementation with those parameters.

## Exclusivity and arrest

An ideal hard exclusion allowing each particle to interact with at most one token makes the instantaneous interparticle-bridge graph a matching: every vertex has degree at most one. Such bridges alone cannot form an extensive connected gel. They can still pin dimers, and the occupancy/lifetime must be included in structural relaxation. This is a useful sufficient construction condition, NOT an acquired chemical property.

Two-arm DNA locks do not automatically enforce it. A token can bridge two particles while another occupies a remaining handle, allowing chains or networks and nontrivial loops. Small mean bridge fraction does not alone control locally correlated clusters, mechanical constraint propagation, or sensitivity near jamming. A random-bond percolation estimate would not certify the material. The published linker actuator actually exhibits competing two-token occupancy, and clears it by linker destruction. Adding an abstract exclusion constraint to a simulation does not solve that problem.

## Strongest acquired passive comparator

Le Bourdonnec et al., Advanced Materials (2026), https://doi.org/10.1002/adma.202516741 ; full primary preprint https://arxiv.org/pdf/2508.19937 . Fully reversible toehold-mediated associative exchange changes DNA hydrogel relaxation from over 10^5s to under 200s while retaining crosslink stability. Blocking toeholds slows the pathway. The mechanism uses a pivot sequence with two alternative invading sequences and short exchangeable toeholds. It is a bulk demonstration that passive exchange can separate reorganization kinetics from bond strength. It is NOT packing-size/shape-label exchange, nor evidence of dense-glass equilibration.

Li et al.'s 2018 cartwheeling walker, https://doi.org/10.1038/s41565-018-0130-2 , supplies repeated reversible proximity handover, with about 0.72 steps/s on fixed tracks. Its occupied state is predominantly a two-foothold bridge. Its speed cannot be combined with a hypothetical .001 bridge fraction or a loaded hinge as if demonstrated in one device.

Bakhtawar et al., Nano Letters (2025), https://doi.org/10.1021/acs.nanolett.5c03063 , demonstrate acceleration of four-way strand exchange using bulged toeholds. This is a relevant existing approach to intermediate/transition-state engineering, not proof of exclusive token handover in a glass. The general kinetic-control idea is established.

## Strongest acquired active and annealing comparators

Wang et al., Nature Communications (2026), https://doi.org/10.1038/s41467-026-69521-x , supplies large single-linker hinge actuation and about ten-second fueled cycles. RNase H clears trapped linkers by destruction; therefore neither conserved-token equilibrium nor passive operation follows. This is the closest mechanical actuator, not a physical packing-swap experiment.

Laser-produced defects can experimentally manipulate glass relaxation: https://doi.org/10.1103/PhysRevE.110.064603 . Such particle removal changes local density and must be compared with restoration/preparation costs, not treated as same-Hamiltonian equilibration.

Established cyclic-stress control (https://doi.org/10.1103/PhysRevX.15.011043), thermal/volume-fraction cycling and softness control are real alternatives. Their advantages or disadvantages cannot be numerically ranked against our nonexistent device. A valid benchmark requires identical final interaction law, volume fraction, structure target, elapsed time, mechanical work, fuel/heat, and preparation costs. No experimental conserved shape-swap implementation satisfying this comparison was acquired in this search; absence from a targeted search is not proof none exists.

## Stop condition and surviving claim

The associative pathway is not ruled out by thermodynamics and is not a new general principle. The narrow unresolved operation is: physically realize reversible exclusive transfer of a shape-setting token between caged particles, fast enough to beat their structural relaxation, with measured short-lived bridges and a demonstrably unchanged endpoint ensemble. Existing work supplies its components separately but not their conjunction. Further arbitrary-rate toy models would not advance this claim. Preserve the conditional specification and move to another opening unless a documented material supplies this missing operation.
