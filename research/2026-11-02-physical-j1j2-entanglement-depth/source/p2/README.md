# ASTRA | Connected physical spin prediction: six-spin entanglement-depth certificate

**Report date:** 2026-11-02. **Actual system:** spin-1/2 square-lattice antiferromagnetic Heisenberg J1-J2 at J2/J1=1/2. **Strongest earned conclusion:** all ground states have entanglement depth >=6, and the Gibbs state does as well at `k_B*T/J1 <= 0.02`. **Not achieved:** VBS/QSL phase identification, long-range dimer response, improved large-system energy solver, historical novelty or practical superiority.

## Files

- `00_CONNECTION_TEST.md`: target-first decision, direct Hamiltonian bridge, and failures before the proof objects.
- `RESEARCH_REPORT.md`: complete source-specific proof, actual input/output/cost, comparison, quantitative temperature and local-observable consequences.
- `verify_replica_exact.py`: stdlib-only exact Bareiss positivity for 22 interaction graphs of 1-4 sites; main threshold `-91/200` per site.
- `verify_gram_k5.py`: independent integer-only Gram/residual test for 45 five-site weighted motifs; requires NumPy for fast signed-int64 matrix multiplication, with explicit no-overflow checks. No floating linear algebra in this verifier.
- `make_gram_k5.py`: **constructor**, numerical Cholesky can propose candidate integer Gram factors, never serves as a proof by itself.
- `K5_GRAM_MANIFEST.json`, `K5_GRAM_WITNESSES.npz`: explicit five-site certificate arrays, ~3.1 MB compressed.
- `verify_physical_exact.py`: exact Fraction checks for the physical four-spin trial, alpha interval, and local square completion.
- `run_all.py`: reproducibility entry, also replays the original 16-spin variational witness from its unchanged source zip.
- `REPLICA_RESULTS.json`, `K5_VERIFICATION_RESULTS.json`, `PHYSICAL_CHECKS.json`: executed machine-readable receipts.
- `preserved_original_cluster_baseline.zip`: immutable earlier 20-file programme, SHA256 `a339c1e31c60c27b0dfb77c13c725e19f04f8486a847e24e5f84ee2fe67e5a21`.
- `preserved_previous_phase_research.zip`: unchanged immediately preceding phase-research package and its informative failures.

## Replay

```bash
python run_all.py
```

The k<=4 verifier and physical checks need only the Python standard library. The five-site proof verifier requires NumPy for integer matrix multiplication; it has separate strict overflow bounds, so it **does not** rely on floating eigenvalues. Independently, the original 16-spin upper trial is a checked **rational** Rayleigh quotient, not a trusted external numerical extrapolation.

Time observed in this environment: ~2.1 s for 22 exact Bareiss cases; ~15.8 s for 45 integer Gram cases, excluding candidate-generation time. Numerical construction and verification are distinct operations. If a constructor fails it does not falsify the inequalities; if the integer verifier fails, certification is withheld.

All results are ordinary reproducible scientific arguments and code checks. They do not confer external correctness certification or historical priority.
