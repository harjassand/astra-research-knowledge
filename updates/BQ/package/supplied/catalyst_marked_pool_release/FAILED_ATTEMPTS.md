# Superseded execution notes

These are retained to keep the benchmark record transparent. They do not
change the mathematical or timing claims in `README.md`.

* The first timing script used three repeats at every N and exceeded the
  command's 30-second wait with no JSON result. The benchmark was rerun once
  per case, with both FSP forward and adjoint endpoint-query modes; the final
  JSON is `benchmark_results.json`.
* The first write of the tolerance-sensitivity JSON failed because the
  observation tuple contained NumPy `int64` values, which the standard JSON
  encoder does not serialize. The output was regenerated after converting
  those entries to Python integers; the saved file is
  `numerical_tolerance_check.json`.

