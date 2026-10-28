# Completion map and evidence

## Canonical qubit result

`DIRECT_CPTP_BURES_RISK_RECOVERY.md` is the complete standalone proof. Its exact received bytes are identified by `independent_bures_bridge_receipt.json`; `independent_bures_bridge_audit.md` states the audited assumptions and limits. The root candidate and earlier frozen receipts have not been overwritten.

The theorem achieves the unrestricted CPTP comparator

    ell_alg ≤ (1+gamma)ell_opt+epsilon

with six ordinary pre-datum banks, deterministic calibration cap `O(R² log(2R)/(gamma epsilon))`, and theoretical polynomial processing. It uses actual local purification plus finite Clifford tomography and directly optimizes a measured-data CPTP decoder. No coherent reversal of tomography or SDP is required. The shared bank/datum frame is consumed and not reusable.

## Executed evidence

- `independent_bures_bridge_checks.py/.json`: independent exact symbolic design/Clifford identities, 60 random physical-channel cases, 120 top-vector perturbations, and scalar-budget checks.
- `finite_decoder_sdp_checks.py/.json`: custom logdet-dual solver for three direct decoder problems with output-support dimensions 2, 3, and 4; Choi/Kraus/objective consistency.
- `finite_decoder_sdp_certificates.json`: exact dyadic H,C,Y matrices for those stated rounded coefficient problems.
- `verify_decoder_sdp_certificates.py/.json`: separate exact rational partial-trace, Sylvester-minor and objective-gap replay.
- `independent_decoder_certificate_replay.py/.json`: independent exact-LDL replay. The three gaps are approximately 3.52e-7, 4.93e-7, and 8.47e-7, all below 1e-6.

The full Schur/purification learner and final gate synthesis were **not** executed. These are mathematical/numerical certificates, not hardware experiments or practical cost estimates.

## Separately scoped extension

`GENERAL_Q_DESIGN_ADDENDUM.md` gives an explicit polynomial-size weighted state 2-design for every logical dimension q using a computational ensemble and four-wise independent fourth-root phases. It yields a safe `O(q^5 R² log(2qR)/(gamma epsilon))` direct-decoder cap and records the known-dimension `O(k² log(2k)/(gamma epsilon))` qubit corollary. `general_q_design_checks.py/.json` exactly enumerates finite-field moments for q=2,3,4,5. Its independent review is separate from the qubit receipt; do not treat either as an automatic revision of older encoder/support certificates.

## Important finite-precision points

1. A near-feasible dual shift `Y→Y-delta I_k` loses `k delta`, so its tolerance scales as eta/k.
2. A seed-distribution TV discrepancy delta contributes at most `2delta` to an **unhalved** diamond budget.
3. High-confidence virtual-frame learning needs beta-scale approximation of the learner **record distribution**; O(epsilon) is not sufficient when beta is smaller. Decoder synthesis has its separate loss-scale budget.
4. Approximate outer compression is paid as a full-channel deployment error. Its actual output is not asserted to have an exact latent-U iid decomposition.

No novelty, generic-noise scalability, reusable programme, physical source inverse/environment access, or fixed-exposed-record guarantee is claimed. R and q may themselves be exponential in qubit counts. No uploads or merges were performed.
