DISSIPATION FROM THREE OBSERVATIONS
Research record, 5 November 2026

STATUS AND SCOPE

The main deliverable is reflection_report.pdf. It contains the final statements,
proofs, explicit four-state construction, statistical protocols, synthetic
results, resource accounting, prior-work comparison, and material limitations.
The mathematical results were internally derived and checked during this task.
The literature audit is bounded and does not establish priority. No peer review,
laboratory result, or civilization-changing consequence is claimed.

The inference class is stationary, finite, irreducible continuous-time Markov
chains with deterministic, noninvasive observations and microscopic states
that are even under physical reversal. The hidden state count is unrestricted.
Physical interpretation as entropy production requires local detailed balance.
Changing the hidden physical reversal can invalidate a positive physical
entropy claim, as the report demonstrates explicitly.

All experimental results in this archive are synthetic. Population inequalities
must not be applied directly to empirical means without a valid statistical
protocol. The uninterrupted null test requires stationary initialization and
a fixed score and sample count. The arbitrary-start protocol instead assumes
a supplied uniform mixing envelope and pays the explicit waiting cost.

CONTENTS

reflection_report.pdf          Final 11-page research report.
reflection_report.tex          Complete LaTeX source of the final report.
reflection_results.png         Exact-model figure used in the report.
dynamics_reflection_check.py   Construction and analytic-formula checks;
                              also reproduces the figure.
simulate_certificate.py        Two reproducible synthetic inference protocols
                              and calibrated readout-noise check.
simulation_results.json        Results produced by the supplied simulation.
audit_notes/                   Independent internal derivations and audits.
auxiliary/physics_aliasing_note.md
                              Separate temporal-aliasing result, not needed
                              for the main reflection theorem.
SHA256SUMS.txt                 Hashes of the packaged files, excluding itself.

The audit notes preserve detailed reasoning and some alternative formulations.
The final report is authoritative for the scope and claims of this deliverable.
The auxiliary note is not evidence of a physical experiment and is not used
to enlarge the main result's claimed significance.

REPRODUCTION

Extract the archive and run from its reflection_research_record directory:

    python3 dynamics_reflection_check.py
    python3 simulate_certificate.py

The first command prints numerical checks and regenerates the figure. The
second regenerates simulation_results.json using the declared fixed random
seeds. It simulates exact CTMC transition kernels at the measurement times;
it does not approximate the CTMC by an Euler time step. The inference uses only
the recorded binary observations plus the declared protocol assumptions.

The arbitrary-start run uses 20,000 training blocks and 750,000 validation
blocks, starts in hidden state 0, and never resets the apparatus between blocks.
Its modeled elapsed duration includes every waiting gap. The second run uses
750,000 consecutive blocks and exact uniform stationary initialization for the
known synthetic model. CPU runtime is not the modeled physical duration.

Observed numerical environment:
    Python 3.12.14
    NumPy 2.3.5
    SciPy 1.17.0
    Matplotlib 3.10.8

The scripts require NumPy and SciPy; figure generation also needs Matplotlib.
Tiny floating-point differences can occur across library versions/platforms.

To rebuild the report, with a standard LaTeX installation containing the
packages declared in its source:

    pdflatex -interaction=nonstopmode -halt-on-error reflection_report.tex
    pdflatex -interaction=nonstopmode -halt-on-error reflection_report.tex

The existing report and figure can be inspected without running any code.

PRINCIPAL NUMERICAL RESULTS

For a=1, epsilon=0.4, and analytic half-window t=0.5:
    Conditional covariance:       -0.0147151776469
    Linear population rate floor:  0.0294303552937
    Nonlinear population floor:    0.0295760010299
    True generating rate:          0.439444915467

For the arbitrary-start protocol, at t=1:
    Binary observations:           2,290,000
    Modeled duration:              73,242,880.49489523
    95% linear rate lower bound:   0.009402592238638523
    95% nonlinear lower bound:     0.00943212402959255

For the stationary uninterrupted protocol, at t=1:
    Binary observations:           1,500,001
    Modeled duration:              1,500,000
    Equilibrium tail-probability bound: 9.743585256583219e-6
    95% conservative rate floor:        1.0091708898648661e-6

All entropy rates use natural logarithms and k_B=1. Converting a rate to
physical power requires a justified steady isothermal model and temperature.
