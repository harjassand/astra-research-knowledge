#!/bin/sh
set -eu
ROOT="/Users/harjas/Documents/Codex/2026-10-08/use-the-astra-research-knowledge-repository-2"
TASK="$ROOT/work/agents/c10_finite_minimum_AC"
FORMAL="$ROOT/work/agents/c4_rational_hostile/formalization"
PROJECT="$FORMAL/project"
MATHLIB="/Users/harjas/Documents/Codex/2026-07-14/i-want-you-to-look-at/work/tmp/erdos-1005-lean"
LEAN_BIN="/Users/harjas/.elan/toolchains/leanprover--lean4---v4.28.0/bin/lean"
LIB="$PROJECT/.lake/build/lib/lean"
DYNAMICS="$FORMAL/dynamics"
export LEAN_PATH="$TASK:$DYNAMICS:$PROJECT:$LIB:$MATHLIB/.lake/packages/mathlib/.lake/build/lib/lean:$MATHLIB/.lake/packages/plausible/.lake/build/lib/lean:$MATHLIB/.lake/packages/proofwidgets/.lake/build/lib/lean:$MATHLIB/.lake/packages/batteries/.lake/build/lib/lean:$MATHLIB/.lake/packages/aesop/.lake/build/lib/lean:$MATHLIB/.lake/packages/importGraph/.lake/build/lib/lean:$MATHLIB/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$MATHLIB/.lake/packages/Qq/.lake/build/lib/lean"
"$LEAN_BIN" -o "$TASK/FiniteMinimumCaratheodory.olean" "$TASK/FiniteMinimumCaratheodory.lean" > "$TASK/compile.log" 2>&1 || {
  cat "$TASK/compile.log"
  exit 1
}
"$LEAN_BIN" "$TASK/AxiomAudit.lean" > "$TASK/axiom-audit.log" 2>&1 || {
  cat "$TASK/axiom-audit.log"
  exit 1
}
if grep -q 'sorryAx' "$TASK/axiom-audit.log"; then
  echo 'FAIL: theorem audit contains sorryAx' >&2
  exit 1
fi
printf '%s\n' 'PASS: Caratheodory finite-minimum module compiles; audited declarations have no sorryAx.'
