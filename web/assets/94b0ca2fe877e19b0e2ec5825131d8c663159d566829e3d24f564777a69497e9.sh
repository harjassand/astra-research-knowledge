#!/bin/zsh
set -u
task=/Users/harjas/Documents/Codex/2026-10-08/use-the-astra-research-knowledge-repository-2/work/agents/c4_lean_rpow_separation
"$task/lean.sh" -o "$task/RpowScaleSeparation.olean" "$task/RpowScaleSeparation.lean" > "$task/compile.log" 2>&1
lean_rc=$?
printf 'exit code: %s\n' "$lean_rc" > "$task/compile.exit"
if (( lean_rc != 0 )); then
  exit "$lean_rc"
fi
"$task/lean.sh" -o "$task/RaisedCoordinateContradiction.olean" "$task/RaisedCoordinateContradiction.lean" > "$task/raised_compile.log" 2>&1
lean_rc=$?
printf 'exit code: %s\n' "$lean_rc" > "$task/raised_compile.exit"
if (( lean_rc != 0 )); then
  exit "$lean_rc"
fi
"$task/lean.sh" "$task/KernelAudit.lean" > "$task/kernel_audit.log" 2>&1
lean_rc=$?
printf 'exit code: %s\n' "$lean_rc" > "$task/kernel_audit.exit"
exit "$lean_rc"
