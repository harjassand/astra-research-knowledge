# Acquisition, arithmetic, ordinary comparison and replay

## Mathematical inputs are explicit

The weighted reset receiver needs PSD C,Y, C nonzero and an operator-order
certificate Y<=I_B tensor C/192. The examples provide exact rational/Gaussian-
rational factors: C=Dc² and

    Y=eps D R diag(w) R* D,
    eps I_B tensor C-Y=eps D R diag(1-w) R* D,
    D=I_B tensor Dc, eps=1/192, 0<w<=1, R*R=I.

These certify the order even when Y and C do not commute. They do not
physically whiten/filter the source. Reading C,Y alone costs10r² entries;
checking supplied factors uses ordinary exact matrix arithmetic. An unknown
physical channel would additionally require tomography/structural and error
certificates, which are not acquired here.

The general-ray receiver needs H>=0,TrH1, C>=mI,m>0 and actual leakage
ell=Tr[(I-p)H]. A certified positive lower bound on ell may be used
conservatively in both radius and margin. Reading general H costs81r²
entries. The rational endpoint has O(bits(m)+2bits(ell)+log r) bits; the
normalized CMI margin must also pay the full trace3TrC+eps.

The r2 arbitrary-direction example's largest recorded input/output rational
numerator/denominator sizes are129/150 bits. The strongly nonflat complex
reset's corresponding sizes are59/54. Full exact matrices and factors are
retained, not replaced by source hashes or an assumed spectral oracle.

## The precision improvement is real but is not a generic speed separation

The old finite-ray exponent grew as log(r/ell)+(log kappa)/ell. For
r1,kappa1,ell2^-40, its denominator would require8796093022300 bits.
That denominator was NOT materialized. The new radius is2^-94 (95 denominator
bits), and its raw margin is2^-135 (136 denominator bits).

An explicit small-leakage direction H=(1-ell)p+ell(I-p)/8 has an O(40)-bit
description, but is already a commuting/white known family. Thus this
example illustrates the coarse receiver's precision loss; it does NOT
establish a separation from competent ordinary entropy methods. Such methods
can exploit its two-level spectrum. The new theorem's value is its rigorous
larger admissible radius for every positive direction, without logarithm
evaluation or the old condition-number/output-bit penalty.

## Completed ordinary controls

All dense controls receive the SAME exact matrices, complete active supports
and normalization. They are not denied coherence, basis factors or flags.
Both numpy and mp65/70 entropy values are untrusted numerical diagnostics;
agreement does not certify matrix logarithms. The analytic theorem and exact
order/PSD factors supply the certificate.

| Control | Exact input/qualification seconds | Ordinary numpy entropy seconds | Ordinary high-precision entropy seconds |
|---|---:|---:|---:|
| r2 complex coherent reset, kappa1e4 | 1.851 | .00985 | .06386 |
| r3 coherent reset, kappa1e8 | .0381 | .00817 | .13040 |
| r3 flat main, arbitrary reset | .0422 | .00850 | .14777 |
| r3 singular aligned main | .0282 | .00397 | .05080 |

These are single script-reported computational wall times. Qualification
also includes classification and structural comparisons, not just checking
a scalar radius. The ordinary unvalidated eigensolver is cheaper than that
symbolic work on several fixtures. No runtime superiority is claimed; a
competent ordinary validated-entropy comparator remains entitled to all
the same exact inputs and this lemma.

The new general-ray H_star exact qualification took.00341 seconds, mp70
entropy.00433 and direct27-state CMI.00138. The arbitrary non-TP r2 input
took.01968 seconds for exact qualification, .05103 for mp70 entropy and
.17365 for its explicit flag construction and full486-state CMI. Its
reference grows6→54 and Choi dimension18→162. An equally informed solver
can exploit that classical block structure; the dense extension is an
operational identity control, not a deliberately inflated incumbent.

The exact9-matrix-unit leakage/isometry/radius replay took.00314 seconds.
Python startup, reading, proof, review, source retrieval and a failed initial
JSON-serialization run are additional. That failure is retained as a log;
only the corrected completed aggregate supplies fixture results. Peak RSS
was not instrumented. All work used free local computation and the existing
runtime; no physical or paid input was acquired.

## Replay

Run from the workspace root. The independent scripts import only their own
code and ordinary libraries, never producer proof/consumer code.

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol11_operation_discovery_20261028/quantum_boundary_review/code/exact_controls.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol11_operation_discovery_20261028/quantum_boundary_review/code/coherent_fixtures.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 work/sol8_opportunity_selection_20261027/solver_runtime/.venv/bin/python work/sol11_operation_discovery_20261028/quantum_boundary_review/code/general_ray_controls.py
```

Each JSON records exact inputs, factors, radius, margin, comparison scope and
timing. Arithmetic bit counts are in results/arithmetic_costs.json. The
peer challenge and independent peer endpoint acquisitions are archived under
sources/, with original paths and hashes in INPUT_AND_REVIEW_RECEIPTS.json.
The actual substantive review, not hashes alone, receives the proof.

Only this quantum_boundary_review directory was written. No protected source,
Capital repository, previous thermal/optical artifact, formal goal, automation,
new worker, physical instrument, public action or paid service was changed
or used. No claim of a whole white-noise curve or arbitrary bath lift follows
from these pointwise/local receivers without its separate premise.
