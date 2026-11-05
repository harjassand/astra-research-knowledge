# P3 continued exchange: a reusable thermal quantum register

P3's completed result turns the accepted source-conditional random-embedding BDL memory/loader into a reusable register for a complete classically adaptive campaign. Initialization is paid once; unknown reference-entangled inputs, paid logical operations, readout and replacement share one bound under the specified bath and active-control contract.

\[
\epsilon_{campaign}\le\epsilon_{init}
+\sum_j\epsilon_{ctrl,j}
+C\Gamma NT e^{-cN^\eta}.
\]

`T` is **total accumulated passive holding time**, capped on every branch. Access count enters actual implementation costs and errors; it does not separately multiply initialization error or the total-exposure term.

## Governing files

| Read | Contents |
|---|---|
| [Complete continued return](P3_CONSTRUCTIVE_EXCHANGE_CONTINUED_20261105_RETURN.txt) | Exact earlier assignment, separate human prompt `PLease continue`, complete rendered answer/activity and available native prefix |
| [21-page report](package/Astra_Thermal_Register_Exchange.pdf), [report text](package/report_text.txt) | Complete operating theorem, structural comparisons, constructive alternatives and resources |
| [Register theorem](package/reusable_register_opening.md), [completed independent audit](package/sampler_route/reusable_register_audit.md) | Adaptive intrinsic-time proof and exact interface/initial-state scope |
| [Sampler obstructions and TFD alternatives](samplers-and-tfd.md) | Actual physical checks, relation-code obstruction, coherent preparation and central-sector transduction |
| [Calibration and finite reset/mark](acquisition-and-intervention.md) | Priced Ramsey acquisition, an explicit finite instrument and campaign resources |
| [Verification receipt](package/verification_receipt.json), [package guide](package/README.txt), [checksum manifest](package/SHA256_MANIFEST.json) | Supplied executions, environments, script hashes and proof scope |
| [Original ZIP](original/Astra_Thermal_Register_Research_Package.zip), [publication metadata](SOURCES.json) | Exact current package and predecessor preservation |

The producer was GPT-6 Pro in normal web Chat, observed completed 5 November 2026 at 09:09 UTC (7:09 PM Brisbane). The capture's historical pending-download header is unchanged; the ZIP is now available. Its native prefix is capped at 20,000 characters, while the rendered response is complete. No missing source text has been reconstructed.

## Register-process theorem

Let `V_s` identify each syndrome sector with a common logical subsystem. In the stipulated energy-resolved Pauli bath, labeled jump `a` has rate `q_a(s)`, changes syndrome to `s+d_a` and applies logical Pauli `ell_a(s)=V_(s+d_a)^dagger P_a V_s`. The syndrome trajectory is autonomous and the no-jump evolution is syndrome-scalar. Count nonidentity logical Paulis modulo global phase:

\[
b(s)=\sum_a q_a(s)1_{\ell_a(s)\not\propto I},\quad
\lambda_L=\sum_s\pi(s)b(s).
\]

Initialize a **classical syndrome-block-diagonal** state with `TV(p,pi)<=epsilon_init`; its logical/reference state conditional on syndrome can be arbitrary. Allow syndrome-preserving logical instruments and classically adaptive holding intervals with total passive time at most `T` on every branch. The entire retained-record/output experiment differs from its ideal logical experiment by at most

\[
\epsilon_{init}+T\lambda_L+\sum_j\epsilon_{ctrl,j}.
\]

The proof fixes one stationary labeled syndrome path on deterministic intrinsic passive time `[0,T]`. Ideal active operations preserve syndrome and pause that path. Any adaptive execution traverses a stopped prefix; a bad jump in it is contained in a bad jump somewhere on the full path. Stationarity at deterministic intrinsic times gives `E N_bad(T)=T lambda_L`. It does not assert stationarity at a stopping time or a uniform posterior hazard on rare reports. Initial coupling costs once; a channel hybrid charges faulty active implementations.

For the accepted BDL random-embedding model, stable syndromes have zero logical flux and the inherited unstable-syndrome estimate gives `lambda_L<=C Gamma N exp(-cN^eta)`. The theorem does not transfer that passive bound to a separate explicit embedding, a general correlated non-Pauli Davies generator or another noise law.

## Actual access and reuse

At an access, isolate the bath or include its effects in control error; measure syndrome `s`; apply decoder frame and inverse encoder; perform the logical instrument or swap out/in an unknown input; re-encode and restore the same syndrome frame. Every ideal branch returns the same `s`. A new Gibbs sample and whole-device thermal reset are unnecessary merely because logical contents changed.

Syndrome metrology, routing, protected ports, encoding, controller/ancilla reset, isolation, accuracy and refrigeration are charged. With `Q` imperfect locations, a sufficient per-location allocation is `O(epsilon_ctrl/Q)`; obtaining it is a platform cost, not a proved constant-rate faulty-control threshold. Total spacetime includes `NT`, and holding energy includes the maintenance-power integral. General noncommuting fabrication robustness is not inferred from uncertainty in commuting thermal weights.

The guarantee is unconditional and includes retained records. Rare postselection can amplify conditional error. Timing is classical. A TFD coherent across syndrome sectors is a separate capability, not an initial state automatically covered by the trajectory theorem.

## Supplied audits and historical boundaries

The package includes completed audits of the register theorem, physical matroid bridge, QD-HDQI comparison and Ramsey calibration, alongside finite exact/numerical receipts. The five-qubit example is an interface check, not a BDL hardware or lifetime experiment. Capital preserves the supplied audits and performs no new scientific replay.

The entire preceding [burst package](package/preserved/Astra_Burst_Recoverability_Research_Package.zip) is retained unchanged, including nested productive-control/direct-prevention/first-event archives. P3's own package still labels the positive burst recurrence unproved at its source version. Independently supplied [P1 regularizing compiler](../2026-11-05-p1-burst-constructive-exchange/README.md) and [P2 forced-output construction](../2026-11-05-p2-burst-constructive-exchange/README.md) now provide positive results under their own scheduled-circuit proofs. This note adds navigation without rewriting P3's original status or fabricating a cross-source audit.

No source checker, solver, numerical array load, PDF build or heavy corpus build ran during publication. Generated current retrieval remains unchanged.
