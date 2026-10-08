#!/bin/sh
set -eu
ROOT="/Users/harjas/Documents/Codex/2026-10-08/use-the-astra-research-knowledge-repository-2"
FORMAL="$ROOT/work/agents/c4_rational_hostile/formalization"
PROJECT="$FORMAL/project"
MATHLIB="/Users/harjas/Documents/Codex/2026-07-14/i-want-you-to-look-at/work/tmp/erdos-1005-lean"
LEAN="$HOME/.elan/toolchains/leanprover--lean4---v4.28.0/bin/lean"
LIB="$PROJECT/.lake/build/lib/lean"
DYNAMICS="$FORMAL/dynamics"
export LEAN_PATH="$DYNAMICS:$PROJECT:$LIB:$MATHLIB/.lake/packages/mathlib/.lake/build/lib/lean:$MATHLIB/.lake/packages/plausible/.lake/build/lib/lean:$MATHLIB/.lake/packages/proofwidgets/.lake/build/lib/lean:$MATHLIB/.lake/packages/batteries/.lake/build/lib/lean:$MATHLIB/.lake/packages/aesop/.lake/build/lib/lean:$MATHLIB/.lake/packages/importGraph/.lake/build/lib/lean:$MATHLIB/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$MATHLIB/.lake/packages/Qq/.lake/build/lib/lean"
"$LEAN" -o "$DYNAMICS/PlateauPrinciples.olean" "$DYNAMICS/PlateauPrinciples.lean" > "$DYNAMICS/PlateauPrinciples.compile.log" 2>&1
"$LEAN" "$PROJECT/PlateauPrinciplesAudit.lean" > "$PROJECT/PlateauPrinciplesAudit.log" 2>&1
if grep -E -q '\{[^}]*: Filter [^}]*\}' "$PROJECT/PlateauPrinciplesAudit.log"; then
  echo 'FAIL: plateau theorem exposes an unexpected implicit Filter parameter' >&2
  exit 1
fi
if grep -q 'sorryAx' "$PROJECT/PlateauPrinciplesAudit.log"; then
  echo 'FAIL: plateau theorem depends on sorryAx' >&2
  exit 1
fi
printf '%s\n' 'PASS: AC plateau invariance and finite-entry principles compile without sorryAx.'
