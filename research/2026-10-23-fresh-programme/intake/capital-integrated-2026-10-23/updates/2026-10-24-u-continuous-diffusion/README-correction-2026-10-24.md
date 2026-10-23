# Correction: fixed-H replay source layout — 24 October 2026

The preserved [fixed-H replay](source/fixed_H12_full_cycle/fixed_h12_replay.py) loads the model using its original packet-relative path, `BASE / "opportunity_diffusion/lead/continuous_model.py"`, and imports `cyclic_solver` from the replay's own directory. The selected archive groups files by role, so the script's original model path is absent when the archived replay is run in place. The replay and model bytes remain unchanged.

From this correction file's parent directory, reconstruct the expected paths in a temporary directory with byte-preserving copies:

```sh
stage_dir=$(mktemp -d)
mkdir -p "$stage_dir/opportunity_diffusion/lead" "$stage_dir/opportunity_diffusion/colored_counterexample"
cp source/continuum/continuous_model.py "$stage_dir/opportunity_diffusion/lead/"
cp source/continuum/CONTINUOUS_CONSTRUCTION.txt "$stage_dir/opportunity_diffusion/lead/"
cp source/fixed_H12_full_cycle/cyclic_solver.py "$stage_dir/opportunity_diffusion/colored_counterexample/"
cp source/fixed_H12_full_cycle/fixed_h12_replay.py "$stage_dir/opportunity_diffusion/colored_counterexample/"
cp source/fixed_H12_full_cycle/FULL_CYCLE_RESULTS.md "$stage_dir/opportunity_diffusion/colored_counterexample/"
```

The staged replay path is `$stage_dir/opportunity_diffusion/colored_counterexample/fixed_h12_replay.py`. Its `parents[2]` base is `$stage_dir`, so the model import resolves under `$stage_dir/opportunity_diffusion/lead/`; the local solver import resolves when run from the staged `colored_counterexample` directory. Copying the report there also restores its relative links to the model and specification.

This is a documentation correction only. It adds no numerical result and does not alter any hash-pinned source payload. No scientific script or replay was run for this correction.
