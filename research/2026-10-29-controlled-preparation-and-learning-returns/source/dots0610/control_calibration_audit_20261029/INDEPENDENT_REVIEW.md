# Independent review: acquired singlet membership and endpoint transfer

2026-10-29 04:43 UTC. Reviewer did not author the three governing manuscripts. Verdict: **accepted at the explicit stable, isolated control-interface scope**, including the control-debit supplement. This is internal mathematical acceptance, not acquisition of actual hardware assumptions, historical novelty clearance, or an efficiency advantage.

Reviewed manuscripts are hash-bound in REVIEW_RECEIPT.json. The low-rank defect draft from this reviewer is unrelated and remains independently unreviewed.

## 1. Three-axis membership

Accepted. In integer spin j, each zero-magnetization projector has rank one on the spin factor and identity on its multiplicity. In the real zonal-harmonic realization the normalized vectors for x,y,z have Gram diagonal 1 and common off-diagonal P_j(0); this is phase-consistent, not three independently chosen phase equalities. Odd j gives an orthogonal triple. For j=2r the magnitude binom(2r,r)/4^r decreases monotonically, alternating sign. The largest positive case is j=4, giving (1+2*3/8)/3=7/12, while the most negative j=2 gives (1+1/2)/3=1/2. This establishes the stated n=2, n=4/6 and n>=8 constants and their attainability, not just an upper estimate. Reference entanglement does not alter the reduced-state operator inequality.

An independent matrix implementation constructed Jx,Jy,Jz and their zero-eigenvector rotations for j=1..30. Every top eigenvalue matched the formula; maximum was 7/12. The author's separate program was rerun in a copied folder and passed j=1..50 plus physical n=2,4,6,8. Numerical checks supplement the all-j proof.

The test certifies average encoded leakage for the explicitly prepared mean input I/K. It does not certify worst-input leakage before actual randomization. Unknown detector axes cannot be calibrated by their own unknown preparations. These limitations are retained.

## 2. Endpoint bridge

Accepted. For the encoded logical Choi state rho, normalize its P-projection to rho_P. A purification projection gives purified distance at most sqrt(eta). The physical orbit channel restricted to P and a fixed independent memory state is (1-p)id+pR; its change to any rho_P, including a reference, is at most sqrt(p) in purified distance. Connect the ideal logical Bell state to D(rho), to D(rho_P), to D(T(rho_P)), then to D(T(rho)). Contractivity yields the exact stated sqrt(delta)+sqrt(p)+2sqrt(eta) bound. Cauchy-Schwarz gives 3delta+3p+12eta. No unknown matrix entry is needed, but fixed endpoint maps and source isolation are necessary assumptions. For eta=0 the direct convex-mixture estimate delta+p-delta*p is valid.

Independent fixtures used mixed encoders, exact inverses of deliberately leaky isometries, and small nonunital CPTP source perturbations, explicitly averaged over all 24 permutations at n=4. Sixteen cases satisfied both appropriate bounds. The author's 36 distinct mixed-encoder/imperfect-decoder/nonunital-source fixtures also reran successfully.

The all-memory-state operator lift is valid: with fresh exact bare-logical Pauli keys surrounding the COMPLETE E/control/source/D operation and retired afterward, its Pauli-diagonal CP decomposition has a nonidentity trace effect I_logical tensor H_bad. Testing the reduced Bell-input channel against every memory density matrix sigma establishes the positive-operator inequality. Thus correlated service input is not assumed away at this step. A scalar estimate for only one measured sigma would not suffice; the derivation genuinely holds for every sigma under the fixed isolated endpoints.

## 3. Counterexamples

Both checked independently. The n=4 GHZ encoder has an exact round trip while the supplied collective phase acts as logical iZ and is identity on spin zero. Hence matching tests plus endpoint round trips do not identify correct code placement. At n=6, identity in place of requested permutations leaves the specified K=4 code at loss 3/4, while the nominal orbit witness gives 17/25. The computed matching failure is 17/40. These disprove inverse-consistency-only control certification without involving statistical error or an adversarial memory.

## 4. Acquisition and multiple private test roles

The zero-failure binomial bound and confidence allocation are correct for independent repetitions of the same stationary encoder/round-trip/primitive channel with trusted references. They do not transfer to arbitrary drift or a calibration-aware counter. Exact one-sided binomial treatment is required with nonzero failures, as the manuscript states.

With fixed isolated E,D, q_R and q_L are constant actual endpoint experiment rates. For any conditional source-memory state, the matching contribution has the same current-channel witness. Summing positive hazards gives s e <= R(a_M q_M+a_R q_R+a_L q_L), with R=s max(3C/a_M,6/a_R,12c/a_L). This can feed an existing all-history negative-binomial proof, provided role choice and the matching/service current source boundary satisfy its privacy assumptions. Round-trip or membership branches may have different subsequent memory evolution; the inequality is uniform over the next conditional state, so that does not by itself break it. Current-role side channels distinguishing matching from service, source-coupled endpoints, or newly retained key records are not covered. This review does not replace the governing guard/outer-code proofs.

## 5. Native gate calibration and finite control errors

The two-MUB test coefficient 2 for a full target SWAP or CNOT is valid. Both gates permute computational product states and Hadamard-product states, so the predicted output can be checked with the stated trusted product-basis interface. For local dimension d_g, halfdiamond <= d_g sqrt(1-F_e) gives d_g sqrt(2q_gate). Thus d_g=4 produces the stated Delta²/(32 L²) sufficient per-instance failure threshold. The one-qubit factor is 2. This is conservative but valid on entangled inputs.

The supplement correctly telescopes primitive diamond errors over the complete circuits and charges Delta_M to observed matching failure and Delta_S to actual service infidelity. It does not treat wrong pads as an exact Pauli channel: imperfect pads instead incur complete-process comparison error. Arbitrary non-Clifford frame-rotation readout is expressly not free. Stationarity, context independence, isolation, trusted state preparation/readout and confidence coverage remain necessary, not inferred from inverse consistency.

## 6. Consequence and strongest comparator

The result supplies a concrete matrix-free sufficient endpoint interface and a constant-gap membership test. It does not remove the physical reference boundary. Full-path logical two-basis testing still detects endpoint/control failures directly with coefficient 2 and can be cheaper; this is properly retained. No complete-system cost advantage or universal fault-tolerance claim is supported by the reviewed data.

Reproduce independent diagnostics: OPENBLAS_NUM_THREADS=1 python independent_checks.py. Author replay: same command on author_replay/check_calibration_boundary_v1.py. Neither diagnostic program is an experiment or interval-certified numerical proof.
