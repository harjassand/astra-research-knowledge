# Exact heat-cone separation on an exposed quartic ray

The result is an explicit exposed extreme ray of the full nine-coefficient
left-SO(2) ROC cone for which no fixed strongly parabolic constant linear
diffusion admits a pointwise closed quadratic-form correction. This includes
arbitrary real output matrix diffusion coefficients and a nonnegative
determinant-square supplement. It is not a nonquasiconvexity theorem.

Read `PROOF.md`. Run:

```sh
python3 verify_heat_separation.py
python3 verify_null_corrections.py
```

The first requires SymPy only; the second uses the Python standard library.
Both reconstruct all mathematics without reading optimizer results or
certificate inputs. Their outputs are `HEAT_SEPARATION_CERTIFICATE.json` and
`NULL_CORRECTION_CERTIFICATE.json`.

`FROZEN_RESEARCH_STATE.md` retains the research checkpoint before the complete
proof was written. `SOURCE_LEDGER.json` records the supplied inputs and primary
literature. `FROZEN_MANIFEST_v2.json` pins the current principal files for
independent reconstruction. The unchanged first freeze is archived under
`frozen_v1/`.

The exact exposed-ray theorem means that positive polyconvex addends cannot
share a decomposition with a left-invariant heat-certified piece on this
ray: every heat piece must vanish. Collect the arbitrary PC pieces before
applying exposure; they need not individually be left-invariant. The
remaining operation is unrestricted direct
polyconvexity of the ray, or a different compatible global Jensen argument.
The ray's polyconvexity and quasiconvexity remain UNKNOWN.

All files named `*search*`, `*explore*`, `candidate*`, or `acquire*`, together
with their numerical receipts, are discovery records. Their feasibility
statuses and failed witness searches are not mathematical conclusions.
The local `.venv` contains optional acquisition dependencies and is unnecessary
for either principal proof after SymPy is available.

The copied G certificate in `inputs/` is a comparator and continuity check.
Its seven exact verification groups passed. It is not a premise of the new
ray theorem.

External correctness review, historical priority, full-cone QC, and the
unrestricted heat-plus-polyconvex cone equality remain UNKNOWN.
