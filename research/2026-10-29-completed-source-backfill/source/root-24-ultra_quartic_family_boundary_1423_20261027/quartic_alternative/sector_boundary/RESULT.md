# Completed sharp classification

For \(u=a^2+c^2\), \(v=b^2+d^2\), \(w=ab+cd\), \(q=ad-bc\), define

\[
F_\tau=u^2+v^2+3w^2+\tau q^2+4q(u-v).
\]

For every real \(\tau\), this entire oriented quartic line satisfies

\[
F_\tau\text{ rank-one convex}
\iff F_\tau\text{ polyconvex}
\iff F_\tau\text{ quasiconvex}
\iff\tau\geq89-12\sqrt{42}.
\]

The edge is included. `PRIMARY_PROOF.md` gives the complete argument. An
exact boundary minor-affine support is certified by a norm-multiplied SOS
over \(\mathbb Q(\sqrt{42})\), with positive Gram blocks of dimensions 16
and 6 after removing the acoustic kernels. Adding a nonnegative multiple
of \(q^2\) supplies every larger parameter without another optimization.
A single fixed algebraic background and rank-one direction give negative
curvature for every smaller parameter.

`EXACT_BOUNDARY_SUPPORT.json` contains the positive support;
`CRITICAL_PAIR.json` contains the common lower-parameter witness. All
polynomial identities, field signs, and 22 shifted LDL pivots are exact.
The final standard-library replay took 0.4533 seconds. A separate parent
implementation using a different exact field engine passed in 3.066 seconds;
the complete analytic proof was independently read and accepted internally
at its stated whole-line scope. The parent receipt is retained in
`external_inputs/PARENT_BOUNDARY_REPLAY.json`.

Read-only full replay from this folder:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_boundary.py
```

Exact rational-input classification, returning a support or counter-witness:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 classify_tau.py 1404/125
PYTHONDONTWRITEBYTECODE=1 python3 classify_tau.py 11231111/1000000
```

These return true and false, respectively, for all three properties.
`CLASSIFICATION_EXAMPLES.json` saves both outputs. Input bit costs are
charged; the stored matrices and theorem are fixed for this line.

The substantive construction is the exact singular-boundary support and
the resulting classification, using ordinary SOS/facial-reduction tools.
Failed searches, solver/export errors, timings, and field bit costs are
retained. The earlier `../sector_gap/` result is frozen unchanged.

This fixed \(r=3/2,L=4\) line does not exhaust the nine-coefficient cone.
Known non-polyconvex quasiconvex quartics in the wider invariant class are
preserved. Historical priority beyond the checked primary sources remains
UNKNOWN; no general Morrey theorem or physical capability is claimed.
