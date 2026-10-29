# What matching storage tests do not certify, and a matrix-free endpoint bridge

2026-10-29. Author construction; independent review pending. The exact physical
permutation/matching theorems remain intact. This addresses new deployment
obligations rather than silently assuming their exact control matrices.

## 1. Perfect round trips can hide a wrong encoder
Take n=4. Intended code P is the two-dimensional singlet sector. Let the
actual encoder E_bad instead map |0> to |0000> and |1> to |1111>, and let
D_bad be a TP inverse on that GHZ code (reset off-code output to I/2).
Then D_bad E_bad is EXACTLY the identity on every logical input/reference.
All calibration experiments using that round trip, including arbitrary logical
preparations and output measurements, are identical to a correct endpoint pair.
Every physical qubit permutation is the identity on this wrong code, so testing
inverse-permutation/forward-permutation round trips does not fix the problem.

Let the source be the genuine collective rotation

    U = exp(i*pi*(Z1+Z2+Z3+Z4)/8).

It acts as identity on P; every random-matching product singlet survives with
probability1. But on the GHZ code it acts as iZ. Consequently the actual
encode/permutation/source/inverse-permutation/decode service is logical Z,
with entanglement fidelity0 and half-diamond error1. The good-code and wrong-
code worlds have exactly the same matching and endpoint-round-trip data.
No memory, adaptive source, key leak, or measurement error is needed.

Therefore round-trip correctness plus matching storage tests cannot establish
correct placement in the protected subspace. One must either acquire that
placement or test the complete actual path. This is an identifiability failure,
not a statistical shortage that more of the same tests can repair.

## 2. Even perfect code containment does not certify permutation control
At n=6 the full singlet dimension is d=5. Select a K=4 singlet subcode Q
containing one matching state |M0>. Let source U=I-2|M0><M0| and let actual
encoder/decoder be exact. Suppose all requested physical permutations and their
inverses erroneously implement identity. Every permutation/inverse calibration
loop is perfect, and code membership and endpoint round trips are perfect.
Nevertheless the fixed-Q logical loss is3/4, whereas matching failure is17/40
and C_full*q=(8/5)*(17/40)=17/25<3/4. Genuine permutation orbit control has
raw bad mass16/25, consistent with its theorem. Thus the stronger orbit
coefficient cannot be inferred merely from inverse-gate consistency.
Exact fixture: ../permutation_orbit_instance_20261029/orbit_instance.json.

## 3. Matrix-free sufficient interface with stable, isolated endpoints
Here is a positive theorem, under explicit additional assumptions:
- E and D are fixed CPTP endpoint maps throughout acquisition and deployment;
  they have no carried memory or coupling to the source's retained memory.
  Their exact matrices are unknown and are not input data.
- The current source may have arbitrary retained quantum memory; its current
  conditional physical channel need not be stationary or collective.
- Actual private permutation/inverse control is as in the orbit theorem;
  any implementation error is separately acquired at its actual interface.
- Trusted logical probe preparation/readout, trusted three-axis physical
  measurement, and private bare-logical Pauli gates are available. These are
  reference operations, not inferred by testing them against themselves.

Let

    eta = Tr[(I-P) E(I_K/K)],
    delta = 1-F_e(D E),
    p(sigma) = 1-F_raw,P(N_sigma) <= C_n q_M(sigma).

The first two quantities are acquired by actual endpoint experiments, not
assumed control matrices. For every source memory state sigma initially
independent of the tested logical Bell input, the actual orbit service obeys

    sqrt(e_service(sigma)) <= sqrt(delta)+sqrt(p(sigma))+2sqrt(eta),
    e_service(sigma) <= 3delta+3p(sigma)+12eta.           (1)

### Proof of (1)
Let rho be the encoded logical Choi state, retaining its logical reference,
and let rho_P=P rho P/(1-eta) when eta<1. Projecting a purification shows their
purified distance is at most sqrt(eta). The reduced orbit source on P is the
convex mixture (1-p)id+pN_bad. Therefore its action on rho_P, including its
logical reference, changes that state by purified distance at most sqrt(p),
since fidelity to a mixture containing weight1-p of the same state is >=1-p.
CPTP maps, including actual D, contract purified distance. Connect the desired
logical Bell state to the actual noiseless round trip, then to its projected
input counterpart, then through the orbit source, then back to the unprojected
actual encoded input. Triangle inequality gives sqrt(delta)+sqrt(eta)+sqrt(p)
+sqrt(eta). Squaring and Cauchy-Schwarz yields (1). If eta=1 or a displayed
bound exceeds1, the trivial loss bound1 applies; no conditioning claim is made.

If eta=0 exactly, a stronger direct convex-mixture argument gives

    e_service <= delta+p-delta*p <=delta+p.             (2)

For fresh private bare-logical Pauli pre/post keys, applied BEFORE E and AFTER
D and retired, the complete logical-data/source-memory channel has the usual
exact Pauli CP decomposition. Its bad trace effect is I_logical tensor H_bad.
Because (1) holds for EVERY sigma, it lifts to the operator bound

    H_bad <= 3 C_n E_fail,M + (3delta+12eta) I_memory.    (3)

This addresses correlated service inputs and arbitrary current source memory,
without pretending endpoint calibration also establishes endpoint isolation.
The endpoint Pauli gates are O(log K) single-qubit operations; physical orbit
control remains additional work.

## 4. Actual acquisition, not unspecified SPAM constants
For eta, invoke E on uniform computational-basis inputs and use the three-axis
zero-magnetization test in THREE_AXIS_MEMBERSHIP_v1.md. It proves
eta<=c_n q_L, with c_n=12/5 universally (2 for n4/6).
For delta, use the TWO logical mutually unbiased bases (computational and
Hadamard product), traverse the ACTUAL round-trip D E, and measure in the input
basis, failing on any wrong logical string. This established channel-survival
witness gives delta<=2 q_R. No entangled logical reference or full E/D process
tomography is required. The actual probes/readout remain the trusted references.

For iid endpoint acquisition, observing zero failures in N_L and N_R trials
bounds q_i<=1-alpha_i^(1/N_i) with failure probability at most alpha_i. For
nonzero counts use an exact one-sided binomial bound, not a zero-count formula.
Allocate alpha_L+alpha_R+alpha_controls<=alpha_total. These statistical bounds
are about the same fixed E,D maps; they do NOT certify arbitrarily drifting
future endpoint channels.

Alternatively, interleave the two calibration experiments with matching tests
and services while retaining the fixed-isolated-endpoint model. With role
probabilities s,a_M,a_R,a_L, the bound

    e_service <= 3 C_n q_M + 6 q_R + 12 c_n q_L

gives per-history bad-service hazard ratio

    R = s * max(3 C_n/a_M, 6/a_R, 12 c_n/a_L)

against the sum of observed test-failure hazards. The source-memory part may
adapt arbitrarily across roles; q_R and q_L remain actual fixed endpoint rates.
The existing negative-binomial stopping argument then applies with this R,
provided the exact same role/privacy/stopping conditions hold. This is an
explicit but conservative calibration allocation, not an efficiency claim.
Weighted Cauchy-Schwarz improves tradeoffs when one component is small.

## 5. Native permutation/control calibration and its real price
Inverse consistency is insufficient, as Section2 proves. A concrete sufficient
local interface is stationary memoryless native gate channels, independent of
source memory and circuit context. Their actual matrices can remain unknown.
For a two-qubit SWAP gate, prepare random computational or Hadamard-product
basis states, execute the ACTUAL gate, and compare output with the known swapped
bit string in that basis. The two-basis test gives target entanglement
infidelity<=2q_gate. General Choi/diamond inequalities then give

    (1/2)||Gamma-Ad_SWAP||diamond <=4 sqrt(2q_gate).

This bound applies to arbitrary entangled gate inputs. For L deployed SWAP
instances with individually valid bounds gamma_i, a hybrid argument charges
sum_i gamma_i to the full operation; it does not infer this from a reduced
state or average signal. With zero failures and desired gamma_i<=Delta/L,
a sufficient calibration is q_gate<=Delta^2/(32L^2). The necessary zero-count
sample size is explicitly log(alpha_i)/log(1-Delta^2/(32L^2)). Shared gate
families can reuse evidence ONLY if the stationary context-independent channel
assumption genuinely holds. One-qubit target rotations have the corresponding
factor2 instead of4. Their reference preparations/readouts must be trusted or
separately warranted, otherwise this is circular self-calibration.

These conservative tests can be much more costly than testing the complete
logical path. They are a sufficient matrix-free calibration route, not a
realistic-performance demonstration or a removal of all reference assumptions.
Gate calibration performed before deployment cannot certify a gate with an
arbitrary counter, drift or source-coupled bath. A deterministic switch after
all calibration calls is already an indistinguishable failure of stale transfer.

## 6. Strong conventional comparison and unavoidable boundary
A full-path logical two-basis test traverses the ACTUAL E, requested physical
controls, source and D. As a witness on the complete current logical channel,
it directly sees endpoint and control failures, with coefficient2. An actual
private logical Pauli pre/post pad supplies the existing memory-safe hazard
bridge. Its trusted references are bare logical preparations, measurements,
private pads and a common current source boundary; it does not need separately
known encoder matrices, code-containment evidence or SWAP calibration.

In the worst case matching tests are blind to all endpoint errors, so adding
cheap matching tests cannot replace a full-path correctness witness without
additional acquired structure. Under a hybrid scheme with otherwise unrestricted
endpoints, an adversary can put all error in an endpoint invisible to matching;
only full-path test frequency controls that error. Moreover the variable-role
budget result shows that a large outer block can require only O(log(1/epsilon))
full-path tests at fixed tolerated bad fraction and target epsilon. Avoiding
full encoder/decoder calls on tests alone is therefore not an asymptotic total-
cost advantage.

The new positive content is an explicit matrix-free sufficient interface:
three-axis code-membership evidence plus actual round-trip evidence, with
quantitative transfer through arbitrary source memory WHEN endpoints and
control references have the stated isolation/stability. It does not establish
those physical assumptions from the same data. Full-path tests remain the
stronger default if such independent control evidence is unavailable.
