ASTRA P1 — SCALABLE OUTPUT-ONLY MANY-BODY ACQUISITION
Scientific return: 5 November 2026, Australia/Brisbane

READ FIRST

Astra_P1_Scalable_Many_Body_Acquisition.pdf is the integrated report. Its editable
LaTeX source is included. This is a constructive theorem in a specified calibrated
Markov/control model, not an experimentally validated device, practical economic
estimate, or established historical-priority claim.

COMPLETED CAPABILITY

An explicit output-only quantum operation recovers one arbitrary initial many-body
state, including all its external-reference correlations, while the source evolves
under a known continuous local Hamiltonian. The actual coherent pure-vacuum Weyl
ports, finite local collection, receiver controls, memory, precision and inverse
simulation are all specified. No source-side intervention or postselected retry is
granted. With beta=max_i sum_(X contains i)(|X|-1)osc(h_X) and kappa=r-beta>0,
the ideal full diamond error is at most 2 sqrt(n exp(-kappa T)).

The full coherent-dilation estimate
  eta_split <= 2 chi Delta sqrt(R T+(R T)^2),
  chi=max_i sum_(X contains i)osc(h_X), R=nr(1-q^-2),
earns the finite-bin interface from the actual interacting output. Two recycled
banks per site achieve O(n log(n/epsilon)) protected qudit storage at fixed local
scales and positive gap, with explicitly charged gate/readout/reset throughput.
A separate-bank implementation is a completed polynomial fallback. The sufficient
control-work upper bounds can be very large polynomials.

For Hamiltonians diagonal in one known fixed product basis, a separate exact ideal
decoder works for EVERY r>0. Keep first exports, process replacement labels, and
apply one diagonal phase gate per Hamiltonian term. General noncommuting weak-export
dynamics remain open; the general rate condition is sufficient, not universal.

PACKAGE MAP

  Astra_P1_Scalable_Many_Body_Acquisition.pdf / .tex
      Integrated proofs, actual interface, costs, certificate and comparisons.
  continuation_handoff.txt
      Scientific state, exact premises, boundaries and next decision.
  construction/continuous_hamiltonian_reverse_reset_decoder.txt
      Independent full construction and conservative all-bank implementation.
  construction/finite_local_depolarizing_port_collector_note_2026-11-04.md
      Explicit local controls, finite ramps, calibration and Kraus isometry.
  construction/global_history_and_recycling_audit.txt
      Improved full-history bound and two-bank throughput/memory audit.
  construction/continuous_hamiltonian_interface_audit.txt
      Independent projection, normalization, fidelity and splitting audit.
  construction/diagonal_hamiltonian_exact_acquired_decoder.txt
      Full diagonal theorem, proof, acquired interface and streaming costs.
  verification/verify_reverse_reset.py
  verification/reverse_reset_verification.json
      Small reproducible finite-matrix floating-point checks.
  environment_versions.txt
      Numerical and document-runtime versions.
  SHA256SUMS.txt
      Checksums of the package contents, excluding the manifest itself.
  preserved/
      Unchanged preceding research ZIP and handoff, and both original companion
      notes copied byte-for-byte. The previous interaction-order theorem, explicit
      meters, numerical evidence and source are inside that preserved ZIP.

The integrated PDF and recycling audit select the improved full-history comparison.
Earlier per-bin estimates in the collector note remain valid conservative bounds.
The exact local specialization has H_M=0; generic Hamiltonian upper bounds in the
diagonal note are looser sufficient bounds, not additional required controls.

REPRODUCE

Run: python3 verification/verify_reverse_reset.py
Requires NumPy and SciPy; rewrites the adjacent JSON. It checks the physical
decoder/projection identity, adjoint identity, support Lyapunov inequality, and
positive trace-preserving Choi maps at four times. It is not a large-n numerical
extrapolation or a formal proof certificate. Rebuild the PDF by running pdflatex
twice on the included .tex file; there are no external figure dependencies.

PRESERVATION AND BOUNDARIES

The previous interaction-order theorem retains its summed-term budget and
full-retained-instrument scope. Its proof boundary does not settle strong control.
Its source has inaccessible Z noise. The present source supplies specified
noncommuting coherent output records and has a different access contract.

The mixed-output companion uses a time-programmed source with a maximally mixed
incoming collision bath and unavailable purifiers. Its whole-output memory
obstruction is preserved. The present operation targets the initial payload and
reference under pure accessible ports. It neither reconstructs every bath
correlation nor promotes the mixed example to a stationary thermal Lindblad model.

Inherited N1732, Kraus/Stinespring freedom, Petz/inverse-dilation implementations,
operator-size methods, percolation and ordinary circuit inversion are credited.
The claimed scientific increment is the complete structured quantum acquisition
operation and its uniform quantitative guarantee. All resource assumptions and
unresolved regimes are made explicit in the report.
