Hidden phase complexity inside an exact collective law

Read RESEARCH_REPORT.txt for the full theorem, proof, observation/intervention
contract, rational algorithms, costs, primary credit and limits.

Files:
  RESEARCH_REPORT.txt
  exact_core.py
  verify.py
  EXECUTED_CERTIFICATES.json
  SOURCES_AND_SCOPE.txt
  README.txt

Reproduce the finite checks:
  python3 verify.py

Python 3.10+ and NumPy are needed for verify.py.
exact_core.py uses only the Python standard library.
No network call, source experiment, solver oracle or training step is required.

The proof covers every member of the stated families. The execution checks
one 13-state weak graph, selected partition cases, four addressed phases using
the rational algorithm, and one exact MaxCut-to-bisection reduction.

A compact binary partition input produces compact group amplitudes by
default. Requesting expand_physical=True explicitly incurs its physical
output-size cost. The weak-graph interface already lists every coordinate.

This is a new standalone package. It contains no predecessor archive and does
not recover or confirm any held earlier transfer.

