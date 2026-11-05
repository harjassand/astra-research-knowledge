# Decoder reversals and a reported compute-limit failure

The [exact ordered visible updates](DOTS_DECODER_AND_COMPUTE_LIMIT_20261106_RETURN.txt) report a candidate decoder improvement followed by failures to scale and to beat a stronger published comparator:

| Reported stage | Outcome and boundary |
|---|---|
| Smaller simulated design, one million runs | Modification 95 errors versus 108 for its inherited correlated decoder. Source reports independent replay, with a known case where the modification changes a correct answer to wrong. |
| Larger design, one million runs | Modification made no changes to the original decoder's decisions; the smaller result did not carry over in that test. |
| Stronger published method, two million runs | Baseline 125 errors versus 166 for the modification. Source reports baseline-implementation checking; full comparison replay was still underway. |

The source treats the candidate as a failed lead against that stronger alternative. The updates do not supply raw paired outcomes, a full model/decoder specification, code or a ZIP; none is reconstructed. Counts alone are not converted here into paired significance, certified confidence, general scalability or best-decoder superiority. The preceding [d23 sizing decision](README.md) is a separately scoped result and is not silently modified by these updates.

## Harder coordination test was not ready

Dots reports one suitable circuit-design challenge verified, while preparing a second exceeded its planned compute limit and the limit did not stop the attempt as intended. The source says the attempt was stopped. This is a reported setup/resource-control failure, not a completed controlled comparison or proof about which coordination method works better.

No process IDs, execution logs, actual overrun cost or task artifacts were supplied with this update. Capital does not assert independent verification that the source attempt stopped, a whole-host resource guarantee, or a diagnosis of that separate environment. This record is separate from Capital's own publication resource receipts.

The [earlier four-task tie](../2026-11-06-dots-coordination-proposal/preliminary-four-task-test.md) remains limited preliminary mechanics evidence. The full lab/harder-test advantage remains unearned. The reported future setup repair does not authorize Capital to restart experiments, add workers or retask Dots.

The exact latest human prompt, visible time group and capture timestamp are preserved. Dots' model, individual update timestamps and thinking trace were unavailable. No source code or experiment was run, and no producer message or new team capacity was added during this archival publication. See [source metadata](SOURCES.json).
