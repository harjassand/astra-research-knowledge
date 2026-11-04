ASTRA P2 RESEARCH RETURN -- 5 NOVEMBER 2026

Result: a polynomial static-to-dynamic construction for the all-working mean
time to first disconnection of an independent exponential repairable network,
and a sharp component-count rate-calibration law.

READ FIRST
research_note.pdf contains the complete theorem, proofs, resources, limitations,
source comparisons and the status of the numerical evidence.

REPRODUCE
python3 check_reliability.py
python3 parallel_experiment.py
python3 make_figure.py
pdflatex -interaction=nonstopmode -halt-on-error research_note.tex
pdflatex -interaction=nonstopmode -halt-on-error research_note.tex

Dependencies: Python 3, NumPy, SciPy, Matplotlib; a standard LaTeX installation.
No internet connection is needed for these diagnostics.

EVIDENCE SCOPE
check_reliability.py uses floating-point full-generator checks for small
systems and a symmetry reduction for the faster-edge family. It is not formal
verification. parallel_experiment.py executes the short-path experiment on 40
parallel edges, using an exact conditional initial state and integer update
draws. It stores rational interval endpoints. Its statistical interpretation
assumes independent uniform draws; the execution uses a reproducible NumPy PRNG.

The general theorem invokes the published heterogeneous-probability Karger
static unreliability FPRAS and constructs a conditional sampler by self-reduction.
This bundle does not implement that general-purpose static oracle. The symmetric
parallel-edge example also has a better exact conventional birth-death solver,
which is included as a check. No practical superiority claim is made.

PHYSICAL SCOPE
The independent, time-homogeneous, two-state model is an explicit premise.
Physical calibration must count observation time, preparation, event detection
and timing errors. No physical measurements or hardware validation are claimed.
Historical priority of the combined theorem is not established.

CONTENTS
research_note.tex, research_note.pdf: full editable note and final PDF.
check_reliability.py, results.json: finite mathematical diagnostics.
parallel_experiment.py, parallel_experiment.json: executed rare-event estimate.
make_figure.py, figures/: research figure and its source.
