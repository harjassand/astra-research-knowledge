# Fixed four-spin port: explicit nonzero-defect corollary
2026-10-29. Additive composition with the separately accepted fixed-port concatenated compiler. Does not change frozen robustv4. Author derivation, receiving review pending.

## Actual inherited compiler
Use `producer-workspace/GOVERNING_v1.md` with its receipt `producer-workspace/REVIEW_RECEIPT.json`. The actual port has FOUR physical spins for every block length. For h>=5, B=2^h, the verified [[16h,h,>=h]] inner stabilizer code and the finite-field outer code give
 N=16hB native service slots; payload=hB/2=N/32 qubits;
 u=floor((h−1)/2); t=(B/8)(u+1)>=N/256;
 b=floor(t/4), T=9N, p=1/3,s=2/9,a=4/9.
The actual finite inner generation/verification, total Clifford/syndrome decoder, endpoint controls and trusted buffers are inherited, not assumed free. A code-generation cap failure is charged as beta_code before physical source acquisition. At n=4 the transfer factor isalpha4=8 and there are3 star edges.

## Robust availability and unchanged soundness
Let Gamma_T denote the v4 fixed-comparator actual-history aggregate defect, conditional on deploying a verified code. Let
 A_T=(27/2)epsilon²T,
 G_T=(sqrt(Gamma_T)+sqrt(A_T))²+3R_T.
The v4 readiness theorem now gives for the SAME fixed port
 Pr[accept]>=1−(32/9)G_T/(b+1)−exp(−N/4)−beta_sampler−beta_code.
Since b+1>N/1024 and T=9N, a convenient looser bound is
 Pr[accept]>=1−32768 G_T/T−exp(−N/4)−beta_sampler−beta_code. (F1)
For all source processes, regardless of this defect budget, the accepted-map half-diamond soundness remains at mostexp(−3N/4096), plus separately declared control/calibration errors. The defect budget is not used for soundness.

If Gamma_T<=gT and use either v4 convergent net schedule, then G_T/T<=g+o(1). Thus for fixedg<1/32768 and vanishing sampler/generation budgets,
 liminf Pr[accept]>=1−32768g>0.
This gives a nonzero conditional source-exposure yield in one fixed four-spin port, under the explicit small approximate-symmetry defect condition. It does NOT give readiness tending to one for a fixed nonzero defect. For Gamma_T=o(T), readiness tends to one.

For the contamination or coherent perturbation examples of PERTURBATION_BUDGETS_v4.md, there are three edges, so g<=6 average(lambda_t) or g<=6 average(nu_t²). A sufficient limiting positive-readiness condition is therefore
 average(lambda_t)<1/196608,
or, for the coherent complete-joint model,
 average(nu_t²)<1/196608.
Here each average means T^(-1) E[sum over actual active rounds], conditional on deploying a verified code; a pathwise upper bound implying this expected budget also suffices. It is not an empirical post-selected certificate. These are extremely conservative interface-level sufficient constants. They are NOT laboratory thresholds, independent physical-gate error thresholds, necessary conditions or experimentally estimated tolerance. For a desired limiting readinessr<1, replace the right sides by(1−r)/196608 with strict slack.

The cap payload/native source-qubit exposure ratio remains exactly1/1152. Expected accepted payload multiplies that by the readiness lower bound; source-memory correlations are permitted. All code verification, classical learning, private sampling, endpoint storage, source isolation and physical synthesis remain paid. This is not unassisted channel capacity or a constant total-time rate. The equally informed full-path logical-testing comparator has the same fixed-port transfer order and code; no practical superiority over it is established.
