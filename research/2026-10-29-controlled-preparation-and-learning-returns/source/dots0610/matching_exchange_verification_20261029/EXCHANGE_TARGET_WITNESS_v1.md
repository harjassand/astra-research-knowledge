# Constant-sensitivity verification of one exchange operation on spin zero

2026-10-29. Author derivation and executed finite checks; independent review pending. Dependency: matching-survival theorem PROOF_MATCHING_SURVIVAL_v1.md and its independent reviews, not re-proved here. No historical novelty or hardware advantage asserted.

## Statement and proof

Let P be the n-even-qubit spin-zero projector, d=rank(P), n>=4. Let S_ij be a physical SWAP and U=exp(i theta S_ij). Since a permutation commutes with collective spin, [U,P]=0. A uniformly random matching M produces rho_M, a product of singlet projectors. For any CPTP map N on the complete n-qubit physical register, define

q_U = 1 - E_M Tr[U rho_M U† N(rho_M)].

Set N'=Ad(U†) composed with N. This is CPTP even if N leaks outside spin zero or is nonunital. Its matching survival failure is exactly q_U. The governing matching theorem therefore gives

1 - F_e(D_V Ad(U†) N V) <= (d/K) (n+2)/(n-1) q_U

for every fixed isometry V:C^K -> range(P), with reset-completed decoder D_V. For K=d this is target-relative full-singlet entanglement infidelity with coefficient (n+2)/(n-1). The Kraus formula for the raw target fidelity is sum_a |Tr(P U† K_a P)/d|²; reset completion only adds nonnegative fidelity terms. The proof uses no collective-noise promise, stationarity or reconstructed environment. It certifies the tested channel, not arbitrary future calls.

**Subcode caveat:** an arbitrary largest-power-of-two subcode Q=VV† need not be preserved by a single physical exchange. The displayed statement compares against the isometric target UV and the moving output code UQ. It becomes a fixed-code logical gate statement only if [U,Q]=0, in which case W=V†UV is unitary. Universality of exchange on the full singlet space does not supply invariance of an arbitrary computational subcode.

## Explicit physical target projector

If i and j form one edge of M, then S_ij|M>=-|M>, so U|M>=exp(-i theta)|M>. Ordinary matched-pair Bell readout is already the correct target test; no inverse exchange is needed.

Otherwise let a and b be their distinct matching partners. Only the four sites {i,j,a,b} change. Their target seed is

|chi_theta> = cos(theta)|s_ia s_jb> + i sin(theta) S_ij |s_ia s_jb>.

The rest stays a product of singlets. The two displayed vectors are generally not orthogonal (their overlap is 1/2), but this superposition is normalized because the cross term is purely imaginary. A target-projector measurement applies U† only to i,j, then performs the same Bell readout on all original matched pairs and accepts iff all are singlets. Equivalently, a four-qubit rank-one seed projector is measured and all other singlets are checked independently. This is a constant-size extension of the memory witness, not a full Schur transform.

## Elementary trusted circuit, with no trusted exchange assumption

Prepare |s_ab> from |00> by chronological gates X_b, H_a, CNOT_(a->b), Z_a. Its inverse is Z_a, CNOT_(a->b), H_a, X_b followed by computational measurement accepting 00. This uses one CNOT and three single-qubit gates for preparation, and the same counts for readout.

SWAP=(I+XX+YY+ZZ)/2. The three Pauli products commute. Up to an irrelevant global phase,

U† = exp(-i theta XX/2) exp(-i theta YY/2) exp(-i theta ZZ/2).

Write Rz(theta)=exp(-i theta Z/2), T=CNOT [I tensor Rz(theta)] CNOT. Then T=exp(-i theta ZZ/2). Set B_X=H tensor H, B_Y=(H S†) tensor (H S†), and B_Z=I. Each factor is B_P† T B_P. This gives a conservative exact six-CNOT, fifteen-single-qubit-gate inverse-exchange synthesis. It is not an optimal synthesis claim. Matrix checks verify the sign/order convention including the ignored global phase.

For different matching partners, preparing the four-qubit target seed would cost eight CNOTs and twenty-one single-qubit gates: two singlet preparations and the six-CNOT exchange synthesis with theta sign reversed. Actual channel verification does not prepare the target seed before the source: it prepares ordinary singlets and uses the inverse target only in trusted readout. Total test preparation plus readout, excluding the source, uses n+6 CNOTs and 3n+15 single-qubit gates in this case, versus n CNOTs and 3n single-qubit gates when i,j were paired. Arbitrary pair access is assumed for these counts; line routing is additional and the existing quadratic preparation lower bound still applies.

If a calibrated exchange primitive is independently trusted, one inverse exchange pulse can replace the six-CNOT construction. Reusing the very uncalibrated primitive under test as an allegedly perfect inverse is circular: cancellation errors can conceal the target error. The complete trusted inverse circuit needs its own calibration budget or a separately justified verification model.

## Calibration and boundary conditions

For test-state preparation trace-distance error alpha and target-effect operator-norm error beta, each pass probability differs by at most alpha+beta. Thus the displayed certificate becomes C(q_observed+alpha+beta), with C=(d/K)(n+2)/(n-1). A gatewise hybrid sum provides a sufficient alpha+beta bound for the entire trusted circuit. The primitive errors, routing, timing, storage and readout costs are not acquired by this mathematical identity.

The same actual source boundary N must apply to every private matching. The source must not learn M through classical control/role leaks before acting. Known local frame conjugations can be included consistently in preparation, target exchange and readout; arbitrary nominal physical exchange is not generally the twisted-frame target. All these controls require implementation.

## Why this is not yet a computation guard

Entanglement infidelity is not linearly equal to unrestricted diamond error without an actual twirl. To Pauli-twirl the error relative to a logical target W, a pre-key P requires output correction W P† W†, not the same P† in general. For non-Clifford exchange angles that correction need not be a Pauli or a cheap known physical operation. Keys must be private/retired under the governing memory results. A gate sequence also has unknown evolving data, target-dependent backaction, possible subcode movement and control errors. The previously accepted identity-memory guard is not automatically a universal verified-computation theorem. This note supplies a one-operation witness and an explicit target test only.

## Established exchange-only computation context

Kempe, Bacon, Lidar and Whaley, *Theory of Decoherence-Free Fault-Tolerant Universal Quantum Computation*, arXiv:quant-ph/0004064v2, Theorem 5 and Eq. (119), proves exchange-generated su(d_J) actions on collective-decoherence sectors; Section IX discusses asymptotically unit-rate singlet encoding. Section VII gives small-sector constructions. This is old universality machinery, not new here. Theorem 5 permits algebraic generation via sums, commutators and conjugations; it must not be read as a free finite compiled sequence for an arbitrary exponentially dimensional unitary.

Primary governing passages read: https://arxiv.org/html/quant-ph/0004064 , Theorem 5, Eq. (119), Section IX Eq. (138). Complementary specific architecture: DiVincenzo et al., *Universal quantum computation with the exchange interaction*, Nature 408, 339–342 (2000), https://arxiv.org/abs/quant-ph/0005116 and https://www.nature.com/articles/35042541 . Its three-spin encoding and overhead are distinct from an arbitrary high-rate full-singlet computational subcode.

## Reproduction

OPENBLAS_NUM_THREADS=1 python check_exchange.py

The deterministic program checks inverse-exchange decomposition and every target matching projector for n=4,6 at five angles, plus 80 arbitrary rectangular Kraus-channel instances with possible leakage. These are floating-point diagnostics, not physical observations or interval certificates. The all-n bound is the conjugation proof above; no numerical extrapolation is used.
