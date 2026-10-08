#!/bin/zsh
set -eu
project=/Users/harjas/Documents/Codex/2026-07-14/i-want-you-to-look-at/work/tmp/erdos-1005-lean
task=/Users/harjas/Documents/Codex/2026-10-08/use-the-astra-research-knowledge-repository-2/work/agents/c4_lean_rpow_separation
export LEAN_PATH="$task:$project/.lake/packages/mathlib/.lake/build/lib/lean:$project/.lake/packages/plausible/.lake/build/lib/lean:$project/.lake/packages/proofwidgets/.lake/build/lib/lean:$project/.lake/packages/batteries/.lake/build/lib/lean:$project/.lake/packages/aesop/.lake/build/lib/lean:$project/.lake/packages/importGraph/.lake/build/lib/lean:$project/.lake/packages/LeanSearchClient/.lake/build/lib/lean:$project/.lake/packages/Qq/.lake/build/lib/lean"
exec /Users/harjas/.elan/toolchains/leanprover--lean4---v4.28.0/bin/lean "$@"
