# Independent cut-balance receiving verification costs

One exact checker execution was performed, at
`2026-10-21T22:25:16Z` (22 October in Brisbane). It covered both the cut-balance
fixture and the later requested 99-vertex receiving fixture. Both were added
before the first execution. There were no failed or discarded executions,
floating eigensolver calls, numerical optimization attempts, precision sweeps,
package installations, or earlier benchmark/transition replays in this task.

## Measured execution

| Boundary | Observed value |
|---|---:|
| Whole child process wall time | 0.39036670100176707 s |
| Whole child process user CPU | 0.39003099999999996 s |
| Whole child process system CPU | 0.0 s as reported |
| Peak child RSS from parent `RUSAGE_CHILDREN` | 17432576 bytes |
| Verification body wall time | 0.35044799800380133 s |
| Verification body CPU time | 0.350444293 s |
| Peak self RSS sampled before result serialization | 17039360 bytes |

Whole-process timing includes Python startup/imports, all exact verification,
and result/log serialization. The smaller body measurement excludes startup,
imports and serialization. The two RSS samples have different sampling
boundaries; neither is incremental allocation. The whole-process figures are
the safer complete measured replay boundary.

The whole-process record is
`cut_balance_whole_process_runs.jsonl`. The checker's own record is
`cut_balance_independent_runs.jsonl`. Captured successful output and empty
standard error are retained in `cut_balance_last_stdout.txt` and
`cut_balance_last_stderr.txt`.

## Work outside the measurement

The first source/fixture inspection recorded `2026-10-21T22:18:12Z`.
Independent derivation, code authoring, source inspection, tool overhead,
report writing and review all occurred outside the measured replay. Their
complete compute, wall, inference, energy and monetary costs are not metered
here and remain **unknown**, not zero. Prior literature work has its separate
record in `research/literature/COSTS.md` and is not erased or absorbed into
this small runtime.

Eight read-only shell invocations inspected fixture structure, the current
proof, pinned structural data, or post-run result metadata. These were not
executions of the numerical/scientific producer or checker. Their complete
cost was not instrumented. Authoring used two source patches before the one
run, then report creation. No private-source retrieval or delivery operation
was performed by this helper; root owns archive integration and delivery.

No inference about runtime superiority follows from this finite receiving
verification. In particular, its 0.39-second replay is not a discovery cost,
not a matched application comparison, and not a replacement for charged
action acquisition, design preparation, arithmetic error control, and
downstream work in any practical operation.
