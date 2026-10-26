#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
for f in causal_role_sealing_exact.py ebit_vs_encrypted_instrument.py ebit_complete_teleport_reference.py fine_record_and_last_gate_no_go.py online_causal_sealed_memory.py; do
  echo "==== RUN $f ===="
  python "$f"
  echo "==== PASS $f ===="
done
