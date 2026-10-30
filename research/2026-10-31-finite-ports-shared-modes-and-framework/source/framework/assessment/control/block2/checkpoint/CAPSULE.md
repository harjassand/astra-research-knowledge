# Earned scientific checkpoint and next scope

The original task is `packet/CONTROL_TASK.md`. This attempt constructs the requested exactly-known-gain gate at the averaged private-coin channel scope. Its proof and reported calculations are frozen beside this capsule. Root has read the complete derivation; this does not add a fresh whole independent review or historical-priority claim.

Each cycle uses ten chronological unit-strength native segments of duration d:

B(-sB), C(-sC), B(sB), C(sC), A(-sA), C(-sC), B(-sB), C(sC), B(sB), A(sA),

with fresh fair private sA,sB and sC=sA*sB. The frozen Pauli identity is U=I-4i*d^3*F+O(d^4), F=Z1X2, with every signed handle area zero. In the bath-only interaction frame each memory Pauli is norm-one Lipschitz using ONLY the first local commutator promise, with no bound on total bath norm or spectator size.

Let L=10d. The first controlled Dyson term has norm <=L^2/4 and zero sign mean. The same-handle second-order survivor is a bath-only anti-Hermitian G, ||G||<=L^3/6, plus a symmetric square term O(L^4). The latter and the first-term variance are retained in the channel. Midpoint freezing changes the cubic term by O(L^4), and the fourth-order CHANNEL Dyson remainder is bounded using unitary-channel norm one. The proof obtains

|| Phi_cycle - Ad_(exp(-4i*d^3*F) tensor exp(G)) ||_diamond <=(5/4)L^4, L<=1.

Fresh independent signs and a coin-independent drift give joint-channel telescoping without resetting M. With d=(pi/(16N))^(1/3), the full gate error after final M discard is <=(3125*pi/4)*d. The guarantee includes arbitrary initial DMR correlations but averages over current private coins; it is not a guarantee for each realized sign record.

The sufficient duration is O(epsilon^-2), with O(epsilon^-3) native segments and O(log(1/epsilon)) scalar-description bits. A common rational duration with relative error <=epsilon/100 plus absolute SWITCHING-EVENT tolerance <=epsilon/(160N) is explicitly covered. Event-time error is a different model from independently accumulating segment-duration errors. The numerical constants are prohibitive: at epsilon=0.01 the displayed bound uses about 2.45e17 segments and duration 4.91e11 in rate-one units. No practical advantage or resource optimality is established.

An exact local check adds a real obstruction for THIS word. For admitted static H_M=Z_M/2, after removing the cubic data/bath comparison unitary, the channel's leading residual is

d^4 [25(Ad_(X1 Y_M)-Id)+16(Ad_(X2 X_M)-Id)]+O(d^5).

Its normalized Choi trace norm is 82*d^4+O(d^5). Thus the fourth-order fluctuation cannot simply be erased by averaging the unitary. This is not an all-policy lower bound. Finite diagnostics of the same fixed zero-mean moving bath also show that reusing one sign pair can fail badly while fresh signs converge; this is a construction-specific comparison, not universal necessity of independent signs.

An important source correction applies equally to ALL physical continuations: `predecessor_supplement/` contains exact older Astra native sign-group/order-raising and coarse-uniform-gate originals retrieved after the initial packet was frozen. The initial packet omitted those exact originals. Sign projection, same-handle memory cancellation and polynomial unknown-gain compensation are not new general inventions here. The older physical words need stronger finite-order/static local regularity; the claimed new scope is arbitrary-time-dependent first-motion averaged-channel control. Read those sources for the actual distinction.

The common next scientific scope is `CONTROL_NEXT_SCOPE.md` beside this capsule. It removes exact gain knowledge while retaining first local motion, no calibration and the original native operations. Every continuation receives the same question and predecessor supplement. No new representation or solution method is prescribed.
