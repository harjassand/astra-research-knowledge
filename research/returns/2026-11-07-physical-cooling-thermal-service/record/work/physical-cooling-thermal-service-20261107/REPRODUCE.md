# Reproduction

Run from the original workspace root:

```sh
uv run --with numpy --with scipy python work/physical-cooling-thermal-service-20261107/checks/check_collision_and_correlated_source.py
uv run --with numpy --with scipy python work/physical-cooling-thermal-service-20261107/auditor/check_cooling_algebra.py
uv run --with numpy --with scipy python work/physical-cooling-thermal-service-20261107/machinery/checks/collision_checks.py
uv run python work/physical-cooling-thermal-service-20261107/checks/validate_record.py
```

Inspect output paths before running from an extracted archive. The preservation check requires the original governing files; their cached copies and hashes are archived. Virtual environments and bytecode are excluded. Finite checks supplement the asymptotic proof and do not establish physical validation, novelty or advantage.
