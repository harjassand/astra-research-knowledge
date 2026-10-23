# Independent Cycle9 receiving-check costs

One first execution of `verify_receiving.py` passed, with no producer
imports and no failed checker attempt:

| Resource | Observed value |
|---|---:|
| Total check body wall time | 0.10583182400023361 seconds |
| Total check body CPU time | 0.10218705499999998 seconds |
| Peak process RSS | 21,499,904 bytes |
| Included marked-projection wall time | 0.07103120300007504 seconds |
| Included marked-projection CPU time | 0.06918160500000001 seconds |

The total includes pinned source reads; independent native block/recipe
validation for two original supports; verification of all actual parity
colors and component arms; four complete exact receiving operations using
rational incidence normal equations; same-D/noise-padding comparisons;
the 66 new marked-midpoint witness checks against the pinned inherited
certificate; and binding of the failed first producer source and receipt.
Process startup and final receipt serialization are excluded. Per-operation
and per-receiver timings are retained in `RESULT.json` and are included in
the total, not additive extras.

The earlier accepted star-obstruction enumeration and old 11,142-transition
closure gate were not executed. The obstruction's exact input bytes and
the inherited target table were read as dependencies for new receiving
uses. No larger graph sample, precision sweep or closure search occurred.

The checker is separate from the producer. Exact normal equations are
formed from original edge endpoints and solved by `Fraction` elimination;
the producer's signed-divergence/subtree decoder is not imported. The
checker uses dense matrices only within the small actual color components,
not a claimed general production implementation. No floating decision
enters a source, graph, coefficient, projection, norm or inequality check.

Reading, reasoning, source authoring, proof review and integration costs
were not instrumented and remain unknown. The producer's four new
operations and serialization are separately charged in
`results/RECEIVING_COSTS.json`. Its first component-certificate invocation
failed through variable shadowing and lacked an exception cost handler;
its costs remain unknown, not zero, in `failed/RECEIVER_ATTEMPT_01.json`.
That preserved failed source was not executed again by this checker.

The observed check duration is not the cost of discovery, a physical action
cost or an application speedup. Actual action acquisition, preparation
sorting and set construction, rational bit growth, numerical error for a
floating implementation, and downstream work retain their separate costs.
