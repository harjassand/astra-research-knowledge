PHASE-4 EXCHANGE VERIFICATION WORK

Read GAP_FREE_STAR_PROJECTOR.txt first. It is the definitive operation, derived
by root and independently verified here: one coherent singlet helper pair and
positive exchange pulses implement an exact projector onto the four-spin singlet
code, with arbitrary concurrent local exchange gates.

Run check_exact_star_projector.py for full six-spin validation. Results are in
exact_star_projector_results.json. The program includes fine helper Kraus
operators, all input total-spin sectors, calibration errors and the explicit
late-magnetic-fault boundary. It does not simulate a fitted microscopic device.

EXCHANGE_ONLY_ERASURE_FILTER.txt is the earlier finite-gap construction and
the proof that no accepted exact recovery branch exists for unknown local-spin
errors in the four-spin code. The finite-gap filter is mathematically valid but
has been superseded by the gap-free construction. Its proof/program remain
capital, not a second compulsory hardware route.

Run check_exchange_erasure.py for those earlier finite-gap and recovery checks;
results are in exchange_erasure_results.json.

All results are interaction-model or algebraic claims. Root owns the full
architecture, literature synthesis, actual duration comparison, microscopic
closure and final conclusion. No paper, repository integration or publication
has been made by this agent.
