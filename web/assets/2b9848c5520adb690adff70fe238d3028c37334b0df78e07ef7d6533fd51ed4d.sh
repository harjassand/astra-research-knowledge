#!/bin/sh
set -eu
ROOT="/Users/harjas/Documents/Codex/2026-10-08/use-the-astra-research-knowledge-repository-2"
FORMAL="$ROOT/work/agents/c4_rational_hostile/formalization"
PROJECT="$FORMAL/project"
MATHLIB="/Users/harjas/Documents/Codex/2026-07-14/i-want-you-to-look-at/work/tmp/erdos-1005-lean"
LEAN="$HOME/.elan/toolchains/leanprover--lean4---v4.28.0/bin/lean"
LIB="$PROJECT/.lake/build/lib/lean"
export LEAN_PATH="$LIB:$PROJECT:$ROOT/work/agents/c4_lean_bad_neighborhood:$ROOT/work/agents/c4_lean_finite_glue:$ROOT/work/agents/c4_lean_slice_family:$MATHLIB/.lake/packages/mathlib/.lake/build/lib/lean:$MATHLIB/.lake/packages/plausible/.lake/build/lib/lean:$MATHLIB/.lake/packages/proofwidgets/.lake/build/lib/lean:$MATHLIB/.lake/packages/batteries/.lake/build/lib/lean:$MATHLIB/.lake/packages/aesop/.lake/build/lib/lean:$MATHLIB/.lake/packages/importGraph/.lake/build/lib/lean:$MATHLIB/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$MATHLIB/.lake/packages/Qq/.lake/build/lib/lean"
"$LEAN" -o "$LIB/N33Affine/UniformActivity.olean" "$PROJECT/N33Affine/UniformActivity.lean" > "$PROJECT/UniformActivity.compile.log" 2>&1
"$LEAN" "$PROJECT/UniformActivityAudit.lean" > "$PROJECT/UniformActivityAudit.log" 2>&1
if grep -E -q '\{[^}]*: Filter [^}]*\}' "$PROJECT/UniformActivityAudit.log"; then
  echo 'FAIL: uniform activity theorem exposes an implicit Filter parameter' >&2
  exit 1
fi
if grep -q 'sorryAx' "$PROJECT/UniformActivityAudit.log"; then
  echo 'FAIL: uniform activity theorem depends on sorryAx' >&2
  exit 1
fi
printf '%s\n' 'PASS: uniform activity cutoff theorem compiles with fixed sequence filters and has no sorryAx dependency.'
