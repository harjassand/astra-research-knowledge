# Finite implementation also debits the fast-path resource event

28 October 2026. Author acceptance of an independent-review clarification. The frozen source texts remain unchanged; this note narrows their implementation-sensitive probability interpretation without changing the source order or the all-source risk guarantee.

Affected candidates:

- `ORDINARY_ROW_RESIDUAL_VALIDATION_AND_FALLBACK.md`, SHA `67712222c80855995bd0ded173d4a2f9a1663bdf405f8ec7898f894c7917d442`.
- `AUTOMATIC_VALIDATED_ROW_FAST_PATH.md`, SHA `69b012d669b6e8a32a587b804768acf2bc3155906ea2598727275c357a89fd05`.

Their displayed probability of completing the fast branch is first derived for the IDEAL reference sampler and controls. Finite implementation differences affect the distribution of the acceptance/fallback record, as well as the final payload channel. A complete-process distance allowance cannot be used for the latter while silently omitting it from the former.

Declare a predecision implementation allowance

    nu_pre<=epsilon/1024

INSIDE the existing total whole-process allowance epsilon/2. This bounds the event-probability difference between actual and ideal records by at most nu_pre. If the employed complete-process convention gives the stronger factor-one-half bound, no improvement is needed here. All pilot and validation sampler bits, source controls, measurements and adaptive record processing before the branch decision must fit this predecision allowance. Use the predetermined worst-case horizon to allocate finite per-operation errors; no observed early exit is used to choose a retroactive precision.

For the one-stage residual route, its ideal exact-subclass fast-completion failure is at most

    beta_t+2beta_0=epsilon/512+epsilon/1024.

The ACTUAL failure is therefore at most epsilon/256 after the predecision debit. The actual high-probability source-count statement should be read with this bound, not with the unadjusted ideal probability.

For the automatic geometric schedule, the ideal failure to stop by the first sufficiently balanced stage is less than epsilon/512. Charging the same nu_pre over the ENTIRE multi-stage predecision process gives actual failure less than 3epsilon/1024, hence less than epsilon/256. This is one total record-distance debit, not a free new allowance at each stage. Its count bound and deterministic generic fallback cap are unchanged.

The acquired-anchor extension's fixed source cap does not depend on a resource-success event, so this clarification does not change that cap. Its final payload guarantee already charges the complete-process discrepancy. Likewise, the residual and automatic all-source payload-risk bounds already charge the full epsilon/2 and must NOT add nu_pre again outside it. The change is a stricter allocation and an explicit probability interpretation, costing additional precision bits but no new source calls or favorable-conditioning premise.

No fixed-record or publicly revealed acceptance certificate is obtained. Statistical false-acceptance mass and the implementation error remain unconditional. The ordinary source-input restriction, actual known receiver basis, fresh-bank chronology, full-CPTP comparator, and stronger conventional baseline remain unchanged.
