# Local-port tolerant prediction package

Read `research_note.md` for the exact experimental model, theorems, complete analytic proofs, construction, resource boundaries, and primary-work comparisons.

The main result is a superpolynomial lower bound for **tolerant**, one-qubit trajectory certification from **short real-time local-port experiments**. An elementary polynomial exact-null test is proved under the same access. The hard instances are connected, interacting, gapped, reflection-isospectral, and specified up to one bit.

No imaginary-time filter, candidate-dependent many-body preparation, or Hamiltonian reconstruction is a premise. The lower bound does assume fresh vacuum outside the controlled ports and a bounded total native duration per experiment. It does not apply to arbitrary bath preparation or systemwide control.

## Files

- `research_note.md`: theorem statements, self-contained proofs and limits.
- `check_core.py` / `diagnostics.json`: 690 multiprecision and 751 floating-point checks.
- `check_interfaces.py` / `interface_diagnostics.json`: 1,061 further floating-point checks.
- `example_d4.json`: an explicit dyadic ten-qubit instance with a reflection-defined alternative.
- `sources.json`: inspected primary-source metadata and scope of use.
- `MANIFEST.json`: SHA-256 hashes of package payloads, excluding the manifest itself.

## Replay

Requires Python with NumPy, SciPy and mpmath. From this directory run:

```bash
python check_core.py
python check_interfaces.py
```

The first script uses 110 decimal digits and fixed random seed 184729. The second uses seed 583019. The scripts overwrite their diagnostic reports; the second also regenerates the example. Floating-point details can differ across numerical-library versions.

The 2,502 assertions are finite diagnostics, not independent proof validation. No formal proof, interval-certified general compiler, quantum-circuit compilation, or laboratory experiment was performed. Historical novelty is unresolved. No research repository was modified.
