CERTIFIED COLLECTIVE STATE PREPARATION AND RETENTION

Start with RESEARCH_REPORT.txt for outcomes, THEOREM.txt for the full contract,
proofs, uniform addressable-family consequence and explicit limitations.

Reproduce the executed software operation from this directory:

    python run.py
    python verify.py
    python certify_resources.py
    python plot_results.py

The operation uses existing Python and NumPy; the optional figure uses
Matplotlib. No installation is required in the environment used for the
recorded run. Ordinary IEEE binary64 semantics and the rationally checked
native numerical bounds are stated in THEOREM.txt and EXECUTION.json.

plan.py reads only the two retained acquired-data/design inputs. It computes
exact rational source-family certificates and the finite schedule.
controller.py implements the finite fixed-point program without importing the
native source. native_source.py is the separately paid private 512-state
software source and first-order actuator. run.py emits every port reading and
command to results/PORT_RECORDS.bin. verify.py checks the complete record
against the integer error contract and produces a continuous-time bound for
that particular execution. family_certificate.py checks the parameter-free
rational inequalities of the all-n theorem; it is not a second acquisition
experiment. The general feedback write extension and all-n operation are
proved/costed; the executed acquired network has six ports and uses constant
writing.

The binary record has 344064 rows of 12 little-endian signed 64-bit integers:
six port readings followed by six command values. Divide by 2^40. Row k is at
source time 9+k/131072. The preceding nine-unit constant write command is in
PLAN.json. Commands hold for 1/131072; the actual actuator has the same time
constant and is propagated continuously. This is virtual source time, not a
physical real-time experiment. The deterministic bounded disturbance streams
are specified in native_source.py. They are not averaged away.

Results include the exact source-family plan, all-n certificate, native cost
and roundoff certificate, complete-record audit, a reduced display trace, and
scientific PNG/SVG figures. The archive includes the entire previous
Certified_collective_order_2026-11-07.zip unchanged. Its nested archives
preserve every earlier theorem, failure family, execution and source credit.
No predecessor is replaced or declared broader than its actual proof.

This is a complete construction under its model and channel assumptions.
It is not a physical validation, a generic control algorithm for arbitrary
hardwired nonlinear systems, a solution of frustrated global optimization,
or a resolution of P versus NP. N1683 and the team/access/transfer holds
remain intact. See SOURCES.txt for precise credits and access scope.
