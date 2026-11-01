# Additive v2 receiving repairs — whole executable review pending

The original directory, manifest16c0b44e613b2b779422ac81c7356d6b31ed61f47180d8ad177154527bfe9a44
and codea5b1049d3af540c8cf6df2f1cf3f540ccc48827d27bf68830154637daeb1845e remain
immutable. `history/` preserves exact original code, manifest, README and the
independent reviewer's real diagnostic. Those v1 executable failures are not
rewritten as passes. This v2 directory is a new source freeze.

## Repaired operations

1. `tail_recipe` makes a detached copy of the acquired CF expression. Its two
   returned bound branches also have separate mutable containers. Mutating a
   returned recipe cannot mutate the acquired certificate or another recipe.
   The input certificate remains a trusted acquired object; this is not a claim
   against deliberately replacing its fields or arbitrary Python introspection.
2. `RiskLedger.total`, `.spent`, and `.allocations` are read-only public properties.
   Allocation views are immutable tuple snapshots; later reservations cannot
   alter an earlier snapshot. Returned receipt dictionaries carry no writable
   reference to ledger state. This is a single-owner sequential in-process API,
   not a transactional concurrency or private-state tamper-proof guarantee.
3. Wire admission has separate exact-type byte, lexical token, depth, expanded
   finite-tree node, atom-bit and string bounds. The lexical depth/token scan
   precedes JSON parsing. The iterative structural pass charges queued children
   BEFORE materializing/pushing them, rejects cycles, and charges repeated DAG
   visits as expanded-tree work. Numeric tags require canonical exact hexadecimal
   integers, positive denominators and reduced Fractions. Duplicate keys,
   floats/nonfinite JSON, bool/null atoms, malformed tags and noncanonical data
   are refused. Malformed/deep receiving produces `Unsupported` or `BudgetRefusal`,
   rather than unhandled recursion/division/parser exceptions. Logical budgets
   do not purport to measure every Python object header or all raw arithmetic.
4. `receive_resource_budget` now REQUIRES separately supplied keyword arguments
   `initial_total_upper_bound`, `horizon`, and `failure`. It reacquires the receipt
   from that original client request and the raw box, so an internally valid
   record for a changed request is rejected. This binds arithmetic to a task;
   it still does not prove that a claimed count upper bound is a true observation.
5. The low-level rational-power helper now requires an exact positive rational
   base and exact integer exponent. Its exponent/bit budgets do not silently
   permit a float-power computation.

## Deliberately unchanged mathematics and honest boundaries

All scalar construction formulas, the governing theorem d53758d6f0a7f311e4a3d06e38882b113680ea5604f74f4e4132d17b8542c7de,
and the10,948-byte fixture certificate remain byte-identical. The model intensity,
actual-count observation, predictable-policy, finite-horizon and repeated-risk
contracts do not change. The theorem-only acceptance is separate from executable
acceptance; no new mathematical theorem or source-process clearance is claimed.

`multiplier(p,x,fs=...)` treats a supplied face cache as a TRUSTED internal diagnostic
input: it bypasses default `faces()` enumeration and does not independently
receive the cache. `worst_scaled_drift(p,x,fn)` likewise takes a trusted diagnostic
function, not a received arbitrary Lyapunov function. Their default construction
is checked; these overrides must not be marketed as oracle-free validation of
untrusted supplied objects. Scalar `construct` has the stated polynomial input-bit
formula cost, not a user-configured universal wall-time/heap limit. Mask, rational
power and wire limits cover their stated operations only.

All executable receivers remain same-author implementations until the independent
whole reviewer binds this exact v2 source. No upload or external retrieval occurs.

## Paid ledger history cost

The chosen implementation stores an immutable allocation tuple. Reading its
public snapshot is O(1), but reservation j constructs a new tuple and copies O(j)
references, in addition to exact rational arithmetic. J reservations can therefore
cost O(J^2) cumulative tuple copying. Current ledger storage is O(J); retaining
all old prefix snapshots can retain O(J^2) references. This is not hidden inside
the reaction-firing resource budget, which explicitly excludes controller work.
