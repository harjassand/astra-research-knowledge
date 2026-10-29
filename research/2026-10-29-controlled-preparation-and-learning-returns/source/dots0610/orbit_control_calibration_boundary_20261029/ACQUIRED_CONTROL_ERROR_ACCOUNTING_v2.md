# Explicit control-calibration debit, supplement to endpoint bridge

2026-10-29. Author derivation, awaiting independent review. Read with
OPERATIONAL_CALIBRATION_BOUNDARY_v1.md. This does not replace unknown control
errors by a supplied unexplained SPAM constant.

The native two-qubit test in Section5 also applies to a CNOT: on both the
computational-product and Hadamard-product bases, its ideal output is a known
product-basis string. These two bases are mutually unbiased. Thus target
process infidelity <=2q_gate and half-diamond distance <=4sqrt(2q_gate), exactly
as for SWAP. This can calibrate the Bell-pair preparation/readout CNOTs as well
as the CNOT decomposition of a requested SWAP. Known one-qubit Clifford targets
use factor2 in place of4. Arbitrary non-Clifford frame rotations require
preparing or measuring their known rotated target states, or another explicitly
implemented target-verification circuit; they are not covered for free by an
unrotated two-basis readout.

Let gamma_g be upper bounds obtained from actual finite gate-calibration data,
with a declared confidence allocation and the stationary/context-independent/
source-isolated primitive-channel hypotheses. Let
Delta_M be the sum of gamma_g over the matching-test preparation and readout
circuit, and Delta_S the sum over service permutations/inverses and any other
controls being compared with their ideal reference (do not count unknown E,D
here; their errors are acquired by the separate endpoint experiments).
A telescoping channel comparison, with every primitive bound valid on
entangled inputs, gives

    q_M,ideal <= q_M,actual + Delta_M,
    e_service,actual <= e_service,ideal + Delta_S.

Combining with the endpoint theorem gives the explicit acquired inequality

 e_service,actual <=3 C_n q_M,actual +3delta+12eta
                    +3 C_n Delta_M+Delta_S.

The right side contains observed endpoint error bounds and gate bounds whose
acquisition and number of uses are specified, not a promise inferred from
inverse consistency. If trusted bare logical Pauli pre/post operations are
still exact, this all-memory-state inequality transfers to their bad-event
effect. If those Pauli gates are also only approximately implemented, compare
the whole protocol to an ideal-pad surrogate and charge the sum of their
acquired diamond errors to the final complete-process certificate; do NOT
assert an exact stochastic error decomposition for imperfect pads.

The same principle applies to axis-measurement calibration, but it needs an
independent reference interface. Testing a detector against its own unknown
preparation does not certify its absolute measurement axes. Our construction
keeps trusted bare preparations/readouts as explicit reference operations,
as the full-path conventional comparator does.

There is a genuine cost. Uniformly assigning a total control debit Delta to L
primitive instances with dimension d_g requires target gate failure rates of
order Delta^2/(2 d_g^2 L^2) under the conservative Choi/diamond conversion.
Zero-failure calibration therefore costs order d_g^2 L^2 log(1/alpha)/Delta^2
shots for each separately calibrated gate family. This may overwhelm any saved
validation gates. The construction removes the need to know actual matrices;
it does not establish efficient complete-system calibration or superiority to
actual full-path logical tests.
