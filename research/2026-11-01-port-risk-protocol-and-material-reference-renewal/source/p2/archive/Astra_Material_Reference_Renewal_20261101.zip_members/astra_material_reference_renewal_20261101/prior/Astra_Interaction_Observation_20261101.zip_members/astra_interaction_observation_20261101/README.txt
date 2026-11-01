ASTRA WARM CONTINUATION — 1 NOVEMBER 2026
Preserving a quantum interaction while observing its thermal noise

RESULT
======
The completed returning-error sensor is preserved in the prior archive.
The new main result is an exact physical-model theory for a more demanding
capability: an entangling quantum gate through a continuously hot, lossy mediator.

Measuring a separate cold output can reveal thermal motion. But the feedback
also changes the geometric interaction phase. Minimizing noise alone can select
an operation whose entangling phase approaches zero.

For an inaccessible continuing Markov hot bath, cold-output Gaussian observation
and local phase feedback leave an unavoidable cost at a retained nonzero phase P:

    J >= V_hot * kappa_hot * P^2 / E.

The delivered coherence is exp[-J(s-sprime)^2]; E is integrated squared force.
The proof includes the real input-output instrument. It is not a claim about all
quantum operations. Native bath access, non-Gaussian/encoded operations, quiet
noise windows and changes of coupling resources can escape its hypotheses.

CONSTRUCTION
============
An explicit finite smooth readout filter attains the hot part of the bound.
The remaining cold-input, detector and gain/bandwidth costs are written out.
An explicit two-channel finite-response detector extension includes its transfer
function, quantum added noise, electronic noise and derivative/gain penalty.
A positive quadratic optimization gives the complete minimum noise at the SAME
required gate phase within the admitted Gaussian/local-feedback model.
The executable supplies bounded smooth force and readout profiles, computes their
actual quantum channels, and compares the correct objective with a noise-only
estimator and an ordinary closed loop.

This investigation also supplies a linear phase-preserving observability test:
capturing the hot random phase and retaining the intended quantum interaction
are separate equations. A classical covariance certificate alone is insufficient.

STATUS
======
Conditional mathematical and physical-model construction with independent
analytical, Gaussian-collision and Fock-instrument checks. No device demonstration,
general fault-tolerance result, or historical-priority claim. The present examples
illustrate the boundary; the hot examples are not advertised as accurate gates.

The strongest conventional comparators are retained: geometric/hot gates,
dissipation-compensating and polychromatic loops, environmental quantum erasure,
physical thermal homodyne monitoring, and rotation-symmetric/binomial encoded
finite-angle gates. The last route is an explicit exception to an overbroad
continuous-HNLS argument, with recovery and hardware costs left visible.

FILES
=====
PROOF.txt                 Main root derivation, optimum, resources and limitations.
SOURCES.txt               Current primary research and exact selective Astra use.
warm_phase_frontier.py    Main finite smooth observer construction and figure.
results/                  Computed JSON, scientific figure, independent check log.
checks/                   Independent executable derivations and counterexamples.
supplements/              Competitor construction and complementary proofs.
prior/                    Exact earlier sensor archive, unchanged.

RUN
===
Python 3, NumPy, SciPy and Matplotlib are required. No network is needed.

    python warm_phase_frontier.py --output reproduced
    python checks/warm_transduction_cold_port_verify.py
    python checks/warm_bus_tradeoff.py
    python checks/warm_transduction_verify.py
    python checks/warm_competitor_cold_port_probe.py
    python checks/warm_coherent_clock.py
    python checks/warm_coherent_waveform.py
    python checks/warm_competitor_check.py

The finite collision program is a numerical independent model. Infinite thermal
occupation must not be exchanged with its finite time resolution. The continuous
analytic lower bound and finite smooth profile construction do not require that
exchange. Finite-profile convergence holds within its specified zero-endpoint
family, not automatically to the unrestricted Robin-boundary optimizer.

SCIENTIFIC NEXT QUESTION
=======================
The physical opening is an interface whose harmful environmental information can
actually be acquired while preserving its interaction, or a protected finite-angle
interaction with fully paid recovery. A nominally better cold observer is not
equivalent to acquiring the native hot bath. The accompanying criterion and bound
make that distinction quantitatively testable before investing in a device.
