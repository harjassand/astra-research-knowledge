# Stage 2 executed stress tests

All assertions passed with warnings treated as errors. A new frozen seed and nonbinary alphabets were used; stage1 was not modified.

32 noncommuting operator witnesses were compressed from dimensions exceeding the theorem bound.
Largest relative compression error: 4.38e-16.
Largest absolute gauge-identity error: 4.55e-13.
The spans were computed from the exact listed witness vectors, with a 1e-11 relative singular-value threshold recorded in the code and full singular values saved in the data.

Four random compressed witnesses and three known uniform-reset controls were converted into explicit faithful equal-reference-marginal state pairs. Both local BKM and finite relative-entropy ratios were evaluated; convergence trajectories are saved rather than assuming a favorable rate.

Two further nonbinary cases start from changing reference marginals. Their exact spectral BKM Hessians agree with 64-point quadrature over compressed free witnesses to relative error below 1e-10.

| Input labels | Exact ordinary scalar coefficient | Existing complete coefficient | Constructed free ratio |
|---:|---:|---:|---:|
| 3 | 0.3 | 0.333333333333 | 0.333332777776 |
| 4 | 0.333333333333 | 0.375 | 0.374999374997 |
| 5 | 0.357142857143 | 0.4 | 0.399999399996 |

The uniform values and simplex construction are existing controls from stage1/N967, not novelty claims.
No random search maximum is claimed to be a certified global optimum.

Run: `/usr/local/bin/python3 stress_finite_reference.py`
