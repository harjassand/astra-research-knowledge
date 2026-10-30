# Preserved P2 source layout

The eight final attachments were received flat. They are preserved byte for byte. They are not a standalone replay package. SOURCE_LAYOUT.json maps those actual files, plus the already preserved orbital_echo.py, to the hierarchy used by their literal imports:

```
p2_continuous/
  DERIVATION.md
  spinless_open_source.py
  spinless_open_source_results.json
  real_compiler.py
  positive_phase_clock.py
  retune_sorter.py
  alternatives/spinless.py
  continuous_port/gaussian_sorter_positive.py
p2_physical_bridge/orbital_echo.py
```

The adjacent materialize_source_layout.py takes --repository and --output, verifies every declared byte hash, and copies only these files. It does not import or execute the scientific code or install an environment. The transport preview was materialized without running the science. NumPy/SciPy and all numerical/runtime qualifications remain external. Other worker scratch paths in WORKER_FILE_REFERENCES.json are pointers, not acquired originals; missing files are not synthesized or fetched.
