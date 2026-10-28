# An automatic validated row fast path with a generic cap

28 October 2026. Short composition candidate. This imports the TWO SEPARATELY PENDING acquired-anchor and residual-validation constructions, not merely the received supplied-anchor theorem. It is not received until those load-bearing modules and this composition have been checked.

## Result and resource distinction

In an actual known k-dimensional receiver basis, the algorithm below needs neither a row-rank-one promise nor a supplied anchor, balance number, or useful recovery seed. It has the generic relative one-payload guarantee and deterministic source cap

    O_tilde(k^4/(gamma epsilon))+1.

It automatically completes a faster route on the exact rank-one diagonal subclass. Write d=2k and define its intrinsic balance

    kappa_* = max_{x in S^3} min_{i:lambda_i>0}|u_i^T x|^2.

On that subclass the ACTUAL number of calls is, with high probability,

    O_tilde((d+dr)/(kappa_* gamma epsilon))+1,

where r is the actual supplied loss-state rank bound (or simply d). This is a high-probability instance-sensitive call bound, not a smaller universal deterministic cap or an expected-stopping-time substitute. The equally informed conventional learner can use the same algorithm and receiver.

## 1. A universal but dimension-dependent anchor exists

For a uniform real x on S^3 and any real unit u, the coordinate t=u^T x has density (2/pi)sqrt(1-t^2) on [-1,1]. This follows by slicing the sphere; normalization uses the area of a semicircle. Thus

    Pr(|u^T x|<a)<=4a/pi.

There are at most d nonzero directions. At a=1/(4d), their union of bad bands has probability at most 1/pi<1. Consequently

    kappa_*>=1/(16d^2).                              (1)

Also kappa_*<=1/4, since sum_i lambda_i=4 and sum_i lambda_i |u_i^T x|^2=1. The maximum exists by compactness. This geometric fact does not by itself acquire the anchor or its coherences; the paid count/search and bank constructions are still necessary. Substituting the universal bound into the fast source bill gives k^4, not a generic k^2 breakthrough.

## 2. Fixed geometric schedule, no hidden balance input

Let

    J=ceil(log_2(4d^2)), kappa_j=2^(-j-2), j=0,...,J.

Then 1/(32d^2)<kappa_J<=1/(16d^2). For each stage use the candidate generator and validation procedure from `ORDINARY_ROW_RESIDUAL_VALIDATION_AND_FALLBACK.md` at the SAME target gamma,epsilon and kappa=kappa_j, except for the following explicit confidence allocation:

    beta_t,j=epsilon/[1024(J+1)],
    beta_0,j=epsilon/[8192(J+1)].

Here beta_t,j is the count-pilot event budget, and beta_0,j is the budget for EACH of its two validation tests. These changes enter only the displayed logarithms and their tail inequalities. The pilot count is still ceil[2^44 dL/(kappa_j gamma epsilon)], with L>=log(64d/beta_t,j). All stages use fresh pilot and validation calls. Unchanged thresholds are

    Lambda_max=gamma epsilon/2^20,
    S_max,j=kappa_j gamma epsilon/2^24.

If the rational anchor search fails, go directly to the next stage. If a candidate passes BOTH residual tests, stop the stage loop and acquire its single fresh actual anchor Bures bank, at m=kappa_j gamma epsilon/2^24 and beta_q=epsilon/512. Optimize and deploy its full-CPTP policy as in the validated module. Do NOT acquire a quantum anchor bank for every failed stage.

If all stages reject, run the received generic clipped learner on fresh data at local parameters (gamma/2,epsilon/512), using the known identity frame and, if needed, the trivial valid encoded-Choi rank bound 2k. The source and operation maximum for ALL stages, the possible one anchor bank, the possible generic fallback, and one payload is declared before any records. Unused branches do not have to consume their source allowance; their maximum is still paid in the finite control/error ledger.

## 3. Arbitrary-source soundness over adaptive histories

On every frozen stage history, the positive validation tests have the two actual conditional means proved by the pending module, independently of all earlier pilots and rejections. Their false-acceptance masses are at most beta_0,j per test. A union bound over the at most J+1 reached stages gives

    Pr(any accepted candidate has a false residual bound)
       <=2sum_j beta_0,j=epsilon/4096.               (2)

This is not conditioned on the selected acceptance record. The one subsequently acquired bank fails with unconditional mass at most beta_q because its conditional guarantee is uniform over all selected histories. On a valid accepted history and good bank, the module gives local loss at most (1+gamma/2)ell_star+epsilon/1024. On rejection, the fresh generic fallback has expected local loss at most (1+gamma/2)ell_star+epsilon/512, conditional on every prior history. Summing these alternatives yields

    E ell_selected <=(1+gamma/2)ell_star
                    +epsilon/512+epsilon/4096+epsilon/512
       =(1+gamma/2)ell_star+17epsilon/4096.           (3)

Private framing on one unknown payload and a SINGLE whole-process implementation discrepancy at most epsilon/2 therefore imply actual unhalved complete error at most min{2,(1+gamma)Delta_star+epsilon}. The theoretical processing/control cap and bounded sampler bits are fixed against the full worst-case horizon, not the realized early-exit length. No fixed-record or public-transcript correctness certificate follows from (2)-(3).

## 4. Instance-sensitive actual call count

For an exact rank-one source let j_* be the first stage with kappa_j<=kappa_*. Equation (1) ensures j_*<=J, and kappa_j*>=kappa_*/2. If any earlier stage accepts, it is already no more expensive than stage j_*. Otherwise the fresh count pilot at j_* satisfies its concentration event with probability at least 1-beta_t,j*, conditional on reaching that stage. Its true balance promise holds, so the acquired-anchor search succeeds and the pending module's repeated count proof gives

    Lambda<=Lambda_max/4, S<=S_max,j*/256.

The two validation tests then accept except probability 2beta_0,j*. Hence

    Pr(no acceptance by stage j_*)
       <=beta_t,j*+2beta_0,j*<epsilon/512.            (4)

This bound does not require earlier bad pilots to be identified. An earlier acceptance, even on a rare erroneous record, only shortens the source count; correctness is separately covered by (2).

All preceding pilot/validation bills scale geometrically in 1/kappa_j, with the same confidence logarithms. Since sum_{j<=j*}1/kappa_j<2/kappa_j*, their sum, integer ceilings included, is O_tilde(d/(kappa_* gamma epsilon)). The one anchor bank costs O_tilde(dr/(kappa_* gamma epsilon)). This proves the stated high-probability actual-call rate. The generic fallback still determines the allowed maximum on the rare remaining histories.

Finally kappa_J>1/(32d^2) and r<=d make the total maximum through stage J at most O_tilde(d^4/(gamma epsilon)). Adding the received generic fallback preserves that order. A constant intrinsic balance gives the useful k^2 rate; tiny balance may erase the gain. There is no source-eigenvalue floor, minimum row mass, protected input reference, coherent selector input or unknown-basis acquisition in this claim.

## Governing candidate versions

- `ACQUIRED_BALANCED_ROW_ANCHOR_EXTENSION.md`: SHA `c7556d29185e32dd308fb01d1cfca716b51452f19b67409ada3d4ca4774ff8b8`.
- `ORDINARY_ROW_RESIDUAL_VALIDATION_AND_FALLBACK.md`: SHA `67712222c80855995bd0ded173d4a2f9a1663bdf405f8ec7898f894c7917d442`.

The accepted base and generic fallback imports are those bound in the second source. This note does not change their guarantees or imply that pending proofs have already been independently received.
