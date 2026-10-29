# Additive execution-cost clarification — 2026-10-29 07:52 UTC

The frozen one-instance proof/certificate is unchanged. After completion, the redundant default-refinement cached run was explicitly interrupted (session80735, exit130), preserving partial logs. It is no longer running.

A separate exact diagnostic `check_fast_initial_isolation.py` found all28 real roots in0.0519s using SymPy `intervals(..., fast=True)`, versus545.2s in the original default call. `fast=True` is an exact continued-fraction acceleration, not floating root finding. Earlier default nearzero refinement similarly cost>216s whereas its fast equivalent cost0.0206s. These are implementation-option costs, not inherent lower bounds for algebraic optimization.

The completed frozen certificate used the slow cached initial isolation and fast subsequent refinement. It remains valid. A new optimized clean rerun would use fast=True at BOTH stages; no unexecuted combined total runtime is claimed. The exact shape/FGLM stage still cost250.3s and is not accelerated by this flag. No hardware-latency independence or uniform worst-case fast runtime follows.
