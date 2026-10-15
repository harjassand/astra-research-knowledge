# Proposal-budget audit handoff

16 October 2026. Worker `fz_proposal_budget_audit`; no subagents spawned.
All writes stayed inside this worker folder. Root v0001, v0002, the producer,
the pinned checkout, and Git were not edited.

**Result:** internal analytic PASS for the orthogonal-Pauli exact-rate theorem,
both robust one-block minimax formulas, and their conditional CPTP-Poisson
memory interface. No physical memory, practical threshold, novel primitive,
or independently verified inherited probability theorem is claimed.

Read `AUDIT.md` for the independent full proof, `CORRECTIONS.md` for the
v0001 precision changes, and `SPATIAL_ADDENDUM.md` for the v0002 follow-up.

The exact minimum over **every finite-total-rate state-independent CPTP
proposal family** for the fixed generator is

`r_min=sum gamma_i+h^T diag(gamma)^+h`,

subject to `h in Ran(diag(gamma))`; otherwise it is infinite. Zero generators
admit an empty rate-zero decomposition. Joint vanishing coefficient/floor
limits can have rate limits zero, nonzero, or infinity. The box optimum is
`2sum epsilon_i`, and the diagonal-ellipsoid total optimum is
`2sqrt(sum b_i^2)`.

The receiver uses type-summed **per-center** rates and separately counts
centers intersecting a guard. The audit spells out the exact touching-cell
incidence sums and the conversion bound `(2q+1)^4` for the specified 4D
patch geometry. It does not multiply this factor into a guard proof that
already counts centers. Pauli weight and geometric range are distinct.

For v0002's one global ellipsoid and common spatial cap, the convex
feasibility test is valid, and its disjoint closed form extends to arbitrary
overlaps within the **modewise diagonal-floor proposal family**:

```
B_max = max_c sqrt(sum_{i in S_c} b_i^2),
q_* = 2 B_max,
gamma_i = b_i^2/B_max.
```

Proof: each cell gives the lower bound `2B_c`; the shared floor vector gives
`F_c=B_c^2/B_max+B_max<=2B_max`. This does not solve the different contract
of independently variable ellipsoid blocks per center or unrestricted
correlated CPTP proposal decompositions.

Exact checks passed:

- 729 one-qubit coefficient/floor cases, with directly constructed normalized
  Choi matrices, positive Gram certificates at the claimed minimum, and
  negative quadratic certificates below it.
- 16 direct unitary proposal identities, five two-qubit frames including the
  full 15-string nonidentity basis, and spectator-dimension invariance.
- Pure-Hamiltonian, wrong-floor, amplitude-damping, shared-bath, duplicate-frame,
  operator-norm, joint-zero-limit, and spatial-objective countermodels.
- All 109 covering incidence families on three modes, 2,943 feasibility
  compression cases, 2,943 box cases, and a rational overlapping-support
  example with unequal cell norms.

The main exact run took about 59.6 seconds. These bounded algebra checks
do not certify the asymptotic memory theorem. `EXACT_CASES.json` and
`EXACT_SPATIAL_CASES.json` preserve their separate scopes.

`INPUT_RECEIPT.json` pins the exact read inputs and verified checkout commit
`3dde9ce74d829a93388e64032d27351b36dd2221`. `SHA256_RECEIPT.json` hashes the
saved artifacts and checks whether originals still match their snapshots at
closure. The manifest deliberately does not hash itself.

The elementary displaced-jump identity was independently checked against
Shang-França arXiv 2604.18533v1 equation (4); it is prior art. External
correctness, historic priority of the exact optimization, inherited LSS/HT
premises, acquired controls, and technological advantage remain separate.
