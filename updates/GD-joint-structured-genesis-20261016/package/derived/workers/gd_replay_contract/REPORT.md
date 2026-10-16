# GD replay contract utility

Status: utility and bounded tests frozen. This is replay orchestration support, not a scientific proof or qualification result.

## Purpose

This standalone standard-library utility supplies the fail-closed semantics recommended by the PR105 receiving audit. The pinned checkout was `2688d7a383502df4fc1e64001d04bb76e6ec05e5`. The frozen GC runner was inspected statically and not executed or modified. Its source bytes match the preserved copy in this report package (SHA-256 `7953eca8d8c01be2f12db476a0a85f90af3f86408196b3e7b3b2fbedb3f9d1ef`). The launcher dependency probe, aggregate status predicate, and optional producer row are the three wrapper behaviors this utility addresses.

No scientific checker list or runnable plan is included. The root author must review a JSON plan and define each check's accepted output before using the utility.

## Plan contract

Run `gd_replay_contract.py --plan <reviewed-plan.json> --python <selected-python> [--receipt <path>]`. The selected Python argument is required. Every mandatory `argv` is an argument list beginning with `"{python}"`, followed by the checker and its arguments; shell strings are not accepted. `cwd` and output paths are relative to the plan file unless absolute. `required_modules` are imported and version-probed by the selected interpreter before the checker runs. The probe records that interpreter's own `sys.executable`, version, prefix, and module versions. Launcher and checker interpreter provenance are separate receipt fields.

The plan has schema `gd-replay-plan/v1` and contains `mandatory` and optional `optional` arrays. A mandatory row has `id`, `argv`, optional `cwd`, `timeout_seconds` (at most 600), optional `required_modules`, and an explicit `accept` object. Output predicates support exact or required stdout/stderr text, whole-value JSON equality, or recursive expected JSON fields. Accepted JSON files are always checked for a fresh change during that run; `fresh_outputs` can add other required output files. A JSON predicate without a fresh write fails, even if an old file has acceptable contents.

Optional rows describe omitted work with `id`, `reason`, and optional `required_modules`; they cannot declare a command. They always report `NOT_RUN`. Dependency availability is diagnostic only and does not alter that status.

## Status semantics

An executed mandatory check is `PASS` only when it exits zero, every declared output predicate succeeds, and every tracked output is fresh. A nonzero exit, timeout, rejected output, or stale output is `FAIL`. Missing or unimportable declared dependencies, an unavailable selected interpreter, a missing working directory, or a command that cannot start is `BLOCKED` and the command is not run. Aggregate status is `FAIL` if any mandatory row fails, `INCOMPLETE` if there are no mandatory rows or any mandatory row is not `PASS`, and `PASS` only when every mandatory row passed. Exit codes are 1 for `FAIL`, 2 for `INCOMPLETE`, 0 for `PASS`, and 64 for an invalid plan.

Receipts include the exact plan path and SHA-256, selected interpreter request and invocation path, interpreter-reported version/dependencies, per-command argv and result, and launcher provenance. Captured output is retained up to 16,000 characters per stream, with truncation recorded; full streams are used for acceptance predicates.

## Verification and limits

`python3 -m unittest -v test_gd_replay_contract.py` passed all five bounded tests: launcher/selected-interpreter separation, missing mandatory dependency, an omitted optional producer with both available and missing modules, a failed assertion despite matching output text, and a stale JSON receipt. Tests use small local Python snippets and temporary files; they require no package installation or network access.

The tests establish the utility's status and provenance behavior for these cases. They do not replay the frozen GC scientific checkers, validate future plan predicates, certify the underlying mathematics, or establish external review.
