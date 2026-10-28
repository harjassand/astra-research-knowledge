# Completed common-cone obstruction

In the invariant basis \((u^2,v^2,uv,w^2,uw,vw,qu,qv,qw)\), the rational target

\[
10^{10}p=(55220381,55220381,1830880464,-1603523974,
                         0,0,297124543,-297124542,0)
\]

is strictly rank-one convex, yet lies outside the sum of the following
sufficient QC classes:

- Global polynomial minor support certified after multiplying by \(|X|^2\),
  with all polynomial selector degrees included through the complete
  60-feature, ten-selector reduction.
- Identity spatial Laplacian heat monotonicity with all closed quadratic
  two-forms and a bilinear 24-feature SOS remainder.

Nonnegative determinant-square removal is included. The same conclusion
holds throughout a full nine-coefficient box of radius \(1/52800000\).

`PRIMARY_PROOF.md` gives the complete universal argument. The exact
`EXACT_COMMON_SEPARATOR.json` has a shared negative pairing
\(-28689295580537827/3025000000000000000000\), 60 and 24 positive moment
pivots, all ten selector annihilators, and a literal exterior-derivative
identity annihilating every closed quadratic form. The target's separate
8 by 8 acoustic certificate has shift \(1/200000\).

Read-only, standard-library replay:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_common.py
```

It reconstructs the literal polynomial, acoustic certificate, both moment
matrices, all closed-form columns and all shared energy pairings. The
saved replay took 1.515 seconds. A separate parent implementation using
SymPy QQ passed in 2.51 seconds without producer imports or saved interface
arrays. Its receipt is preserved under `external_inputs/`.

This answers the proposed containment for the precise fixed-level/flow
classes above. It does not disprove quasiconvexity or general
polyconvexity, exclude higher norm powers, or cover arbitrary spatial SPD
or output-coupled flows. A single level-two numerical failure remains
inconclusive. True-PC geometry is investigated independently by the peer.
Further pure-target flow work belongs to `output_flow_extension/` and is
not part of this core freeze.

Controls, independent exact strict-ROC acquisitions, redirected normal
targets, acquisition costs, implementation failures and scope limits are
preserved. The preceding gap and sharp-boundary theorem packages are
unchanged. Historical priority and the full ROC/QC question remain open.
