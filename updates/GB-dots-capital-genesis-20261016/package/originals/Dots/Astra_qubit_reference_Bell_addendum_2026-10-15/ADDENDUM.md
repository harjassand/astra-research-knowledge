# Qubit reference estimation and Bell receiver addendum

15 October 2026. This is a separate scientific addendum; the two earlier delivered archives are unchanged. Results are internally proved and independently reconstructed, with portable exact checks. No experimental demonstration or historical novelty is claimed.

## Important provenance correction

The earlier research manuscript Complete quantum information orders, dated 10 October 2026, Appendix A, already states a finite complex-linear lift characterization of complete Petz-D2 comparison, including a finite semidefinite formulation. The later small classical signed-lift construction must be positioned as a direct constructive specialization, not the first finite comparison algorithm. This changes the novelty framing; it does not invalidate the previously delivered radius theorem. PROVENANCE.md details the distinction without reproducing the earlier manuscript.

## What is now established

A qubit reference suffices for the three-Pauli preparation family with output Bloch radius a=0.6 and erasure reveal q=0.2. Explicit faithful states and a fixed rational target receiver certify source-optimal MMSE minus achieved target risk equal to 0.005216075051827943 approximately. The target joint receiver has dimension four. The reference marginals differ, and the source computation explicitly retains the informative erased-reference branch.

A simpler two-input family has a fixed Bell measurement as its optimal target receiver after one fixed local output rotation. The preferred distinct design uses a=0.9, q=0.45, reference parameters delta=0.1 and t=0.3. Its exact gap is 335421/10671595, approximately 0.03143119655. Its two-input states are faithful and have identical reference marginals. This is a different channel and experiment from the a=0.6 fixture; the larger number is not a matched performance improvement.

For the preferred design, 25,283 independent IID evaluation trials per arm suffice for the stated two-sided 95% half-gap confidence radius under the ideal calibrated model. This excludes training, calibration, preparation errors, detector loss, and drift. A separate 5,229-per-arm bound concerns only the sign of empirical ordering. BELL_PROTOCOL.md states the exact receiver, risks, statistical assumptions, and distinction between these guarantees.

## Closest precedents and interpretation

Known-state comparison, equal/different-index ensembles, Bell measurements, and same-photon polarization/path Bell optics have established precedents. The protocol introduces no new physical operation. Its distinction is the specified universal reference-free SLD ordering and a reference-assisted quadratic-MMSE reversal, within the channel-order framework.

The Bell measurement is relevant to quadratic risk and its posterior scores. Local X measurements already achieve the optimal binary 0–1 decision in the rotated basis. It would be incorrect to claim that guessing the binary label requires an entangled measurement or to describe this witness as quantum data locking.

## Missing empirical step and next test

An actual advantage needs an upper confidence bound on held-out target risk below a rigorous lower confidence bound on the actual source's optimal risk. That requires task-specific preparation and source calibration, a frozen receiver/scoring rule, explicit treatment of no-click/loss events, and independent evaluation trials. Average Bell fidelity alone does not meet this gate.

The immediate next input is fixture-specific calibration and count data or a validated device model. IMPLEMENTATION_GATE.md describes a standard same-photon Bell-analyzer route and the required evidence. No apparatus availability, laboratory outcome, or practical advantage has been established.

## Reproduce

With Python 3 and SymPy, run verify_all.py by its full path from any working directory. The runner verifies SHA-256 integrity, all exact scripts, and the fixed-receiver fixture. No original research directories, network access, source PDFs, or optimization searches are needed.
