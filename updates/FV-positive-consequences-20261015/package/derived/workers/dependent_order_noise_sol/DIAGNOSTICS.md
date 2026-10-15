# Diagnostics and their exact scope

`verify_exact_construction.py` uses `fractions.Fraction`. It checks the nine core determinant inequalities, the three analytic strip types, the all-tail inequality, the exact normalization, and the exact variance formula. The infinite-support reduction is proved in `PROOF.md`; the script does not infer it by scanning a finite grid. Output: `exact_construction_certificate.json`.

`verify_lower_bound.py` verifies the derivative of the one-variable slope formula and encloses the cubic root and the resulting bound using exact rational intervals. Output: `lower_bound_certificate.json`. The global inequality and angular maximization are proved in `PROOF.md`; this numerical/symbolic evaluation is not a substitute for those arguments.

Run these two scripts with the supplied runtime:

```text
R/.venv/bin/python R/workers/dependent_order_noise_sol/verify_exact_construction.py
R/.venv/bin/python R/workers/dependent_order_noise_sol/verify_lower_bound.py
```

Here `R` is `/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-positive-consequences-real-capabilities-v1`.

The following files are search diagnostics only:

- `diagnostic_lp.py`: finite angle approximation of the cone, a truncated lattice, and imposed separate reflection symmetry. A unit integer-coset run at N=12, 128 directions reported approximately 3.17609. Its true-cone residual was about -5.8e-6. These values are not certified bounds on the full global problem.
- The analogous half-integer symmetric-coset run reported approximately 4.92951, with true-cone residual about -2.9e-7. This does not classify nonsymmetric phases or laws.
- `core_tail_opt.py`: continuous optimization of a finite core with an analytic infinite-tail ansatz. N=3 reported about 3.19495, but the solver stopped with a line-search failure and a cone residual about -5.2e-8. Its floating output is not claimed feasible. The final integer core was chosen separately and is certified exactly.
- `family_maxmin.py`: a two-parameter homogeneous max/min ansatz did not improve the independent value 4. Failure of that ansatz does not prove global optimality.

The `.npz` files preserve raw exploratory arrays. Neither the theorem nor its explicit construction relies on their feasibility or optimality.

No claim of formal verification, independent external review, or exhaustive priority clearance is made.
