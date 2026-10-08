#!/bin/sh
set -eu
ROOT="/Users/harjas/Documents/Codex/2026-10-08/use-the-astra-research-knowledge-repository-2"
PROJECT="$ROOT/work/agents/c4_rational_hostile/formalization/project"
MATHLIB="/Users/harjas/Documents/Codex/2026-07-14/i-want-you-to-look-at/work/tmp/erdos-1005-lean"
LEAN="$HOME/.elan/toolchains/leanprover--lean4---v4.28.0/bin/lean"
LIB="$PROJECT/.lake/build/lib/lean"
export LEAN_PATH="$LIB:$PROJECT:$ROOT/work/agents/c4_lean_bad_neighborhood:$ROOT/work/agents/c4_lean_finite_glue:$MATHLIB/.lake/packages/mathlib/.lake/build/lib/lean:$MATHLIB/.lake/packages/plausible/.lake/build/lib/lean:$MATHLIB/.lake/packages/proofwidgets/.lake/build/lib/lean:$MATHLIB/.lake/packages/batteries/.lake/build/lib/lean:$MATHLIB/.lake/packages/aesop/.lake/build/lib/lean:$MATHLIB/.lake/packages/importGraph/.lake/build/lib/lean:$MATHLIB/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$MATHLIB/.lake/packages/Qq/.lake/build/lib/lean"
compile() {
  module="$1"
  "$LEAN" -o "$LIB/N33Affine/$module.olean" "$PROJECT/N33Affine/$module.lean" > "$PROJECT/$module.repair-compile.log" 2>&1
}
compile SliceFamily
compile B2Mechanism
compile StageEnvelopes
compile StageLocalEstimate
compile StageArchive
compile StageCertificate
compile StageLocalCompose
compile B2GluePlacement
compile AffineInduction
"$LEAN" "$PROJECT/ApiAudit.lean" > "$PROJECT/ApiAudit.log" 2>&1
"$LEAN" -o "$LIB/N33Affine/PreRepair/SliceFamily.olean" "$PROJECT/N33Affine/PreRepair/SliceFamily.lean" > "$PROJECT/PreRepair.compile.log" 2>&1
"$LEAN" "$PROJECT/PreRepairApiAudit.lean" > "$PROJECT/PreRepairApiAudit.log" 2>&1
if grep -q '{atTop : Filter' "$PROJECT/ApiAudit.log"; then
  echo 'FAIL: repaired public API still exposes arbitrary atTop filter binder' >&2
  exit 1
fi
if ! grep -q '{atTop : Filter' "$PROJECT/PreRepairApiAudit.log"; then
  echo 'FAIL: preserved pre-repair source no longer reproduces hidden filter binder' >&2
  exit 1
fi
printf '%s\n' 'PASS: rebuilt SliceFamily dependents; repaired public API fixes Filter.atTop; preserved source reproduces the old hidden binder.'
