# Mixed-degree geometric-dilation conductance consumer

Author construction; independent whole receiving is pending. Earlier reviewed
archives remain unchanged and are NOT code dependencies of this directory.

For an acquired raw polynomial F(y,z)=U(s(y)z), s=1+kappa(1-y^2)^2, with positive
quadratic and nonnegative quartic homogeneous components, predict equilibrium
full-fiber conductance without computing U's partition function, assuming its
homogeneity, sampling angular states, or identifying constant transverse mobility.
The exact declared block-SPD/FDT family and physical-model limitations are bound
in each certificate. This is not a general raw-potential solver or a MFPT claim.

The513D expanded raw example yields a certified outer ratio1.006730486859<1.01,
at conductance about2.42e-152; reading6,036,471 exponent entries,262,147 scalar
evaluations and actual receiving replay are paid. See RECEIVING_AND_COSTS.md.

## Read and run

- `PROOF_CANDIDATE.md`: complete spatial cancellation, radial comparison,
  fixed-fiber Cauchy/Jensen, global process, tail and raw acquisition proof.
- `GEOMETRY_ALONE_FAILURE.md`: same-marginal coercive radial-well family proving
  why spatial partition cancellation alone is insufficient.
- `receive_dilation.py`: standalone producer plus recomputing verifier.
- `check.py`, `check_results.json`: exact arithmetic, adversarial receiving and
  actual replay of all9 saved certificates, including the513D full-width request.
- `small_raw_fixture.json`, `small_certificate.json`: inspectable nonfirst-axis input.
- `results.json`: exact endpoints, tasks, raw metadata, costs and9 executed cases.
- `RECEIVING_AND_COSTS.md`, `SOURCES_AND_SCOPE.md`: honest costs/comparators/scope.

From this directory, `python -B check.py` runs the tests and rewrites only
`check_results.json`. Avoid running `python receive_dilation.py` on a frozen source
copy unless regeneration of results is desired; run in a separate copy to preserve
observed timing records. Programmatic usage:

```python
from fractions import Fraction
from receive_dilation import fixture, certify, verify
raw = fixture(3, axis=2)
certificate = certify(raw, beta=Fraction(1))
receipt = verify(raw, certificate, beta=Fraction(1))
```

A certificate's own requested tolerance is not trusted: pass the original external
request to verify. Insufficient grammar, arithmetic or total-width budget raises
`Unknown` (a ValueError subclass), never an unsupported success. Recorded display,
timing and work-counter fields are not proof-bearing. No earlier review receipt
accepts these new sources; wait for a specifically source-bound whole review.
