#!/bin/sh
set -eu
ROOT="/Users/harjas/Documents/Codex/2026-10-08/use-the-astra-research-knowledge-repository-2"
FORMAL="$ROOT/work/agents/c4_rational_hostile/formalization"
PROJECT="$FORMAL/project"
WORKER="$ROOT/work/agents/c4_lean_slice_family"
MATHLIB="/Users/harjas/Documents/Codex/2026-07-14/i-want-you-to-look-at/work/tmp/erdos-1005-lean"
LEAN="$HOME/.elan/toolchains/leanprover--lean4---v4.28.0/bin/lean"
LIB="$PROJECT/.lake/build/lib/lean"
"$FORMAL/repair/verify_filter_atTop_repair.sh"
export LEAN_PATH="$LIB:$PROJECT:$ROOT/work/agents/c4_lean_bad_neighborhood:$ROOT/work/agents/c4_lean_finite_glue:$MATHLIB/.lake/packages/mathlib/.lake/build/lib/lean:$MATHLIB/.lake/packages/plausible/.lake/build/lib/lean:$MATHLIB/.lake/packages/proofwidgets/.lake/build/lib/lean:$MATHLIB/.lake/packages/batteries/.lake/build/lib/lean:$MATHLIB/.lake/packages/aesop/.lake/build/lib/lean:$MATHLIB/.lake/packages/importGraph/.lake/build/lib/lean:$MATHLIB/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$MATHLIB/.lake/packages/Qq/.lake/build/lib/lean"
"$LEAN" -o "$WORKER/SliceFamily.olean" "$WORKER/SliceFamily.lean" > "$WORKER/LEAN_COMPILE.log" 2>&1
export LEAN_PATH="$WORKER:$LEAN_PATH"
"$LEAN" "$WORKER/ApiAudit.lean" > "$WORKER/API_AUDIT.log" 2>&1
"$LEAN" -o "$LIB/N33Affine/GlobalAffineComposition.olean" "$PROJECT/N33Affine/GlobalAffineComposition.lean" > "$PROJECT/GlobalAffineComposition.compile.log" 2>&1
"$LEAN" "$PROJECT/GlobalAffineAudit.lean" > "$PROJECT/GlobalAffineAudit.log" 2>&1
if grep -q '{atTop : Filter' "$WORKER/API_AUDIT.log" "$PROJECT/ApiAudit.log" "$PROJECT/GlobalAffineAudit.log"; then
  echo 'FAIL: public API exposes an implicit arbitrary Filter parameter' >&2
  exit 1
fi
if grep -q 'sorryAx' "$PROJECT/GlobalAffineAudit.log"; then
  echo 'FAIL: formal theorem depends on sorryAx' >&2
  exit 1
fi
printf '%s\n' 'PASS: repaired authoritative and task-local interfaces, all dependents, and full affine theorem compile and audit.'
