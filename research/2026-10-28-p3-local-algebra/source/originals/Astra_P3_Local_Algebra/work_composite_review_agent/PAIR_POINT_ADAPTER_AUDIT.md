# Production point-counter adapter audit

## Result

The production wrapper `work_chain_root/acquired_pair_counter.py` passes
the targeted audit. The manufactured coefficient polynomials, field
parameters, phase scales, callback arguments, and cardinality subtraction
are correct. No arithmetic or indexing bug was found. All new tests are
preserved in `pair_point_adapter_audit.py` and
`pair_point_adapter_audit_results.json`; no root source was modified.

## Polynomial construction

For a requested moment `(i,j)`, the wrapper allocates

    z, x1,y1, ..., x_(i+j),y_(i+j), w,

in that order. Its ordinary polynomial is exactly

    w^2+w+tau z^3
    + gamma sum_l [x_l^3+x_l y_l^2+y_l^3+z x_l y_l]
    + gamma z sum_(l>i) [x_l^2+y_l^2].

The first `i` pairs are positive and the final `j` are negative. Both
extra square terms are conditional on a negative pair. The coefficient
of `tau z^3` is `tau`, without an unintended extra factor of `gamma`.
The two Artin--Schreier coefficients are both one. The final coordinate
does not overlap a pair coordinate, including the zero-pair case.

There are `v=2(i+j)+2` variables. For every assignment to the first `v-1`
variables, the number of `w` satisfying the equation is

    1+(-1)^Tr(P),

where `P` denotes the phase without `w^2+w`. Therefore the exact moment
is the hypersurface cardinality minus `q^(v-1)`, precisely the value
computed by the callback adapter. It subtracts neither `q^v` nor a
quantity depending on the growing module rank.

The production eight-moment interface handles `(0,0)` by an exact binary
Gaussian. Its seven point-counter calls have indices

    (0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1).

The largest has `i+j=3` and `v=8`. The general helper's support for older
indices up to six does not introduce larger calls into this production
path. The supplied point-counter contract receives the acquired field
modulus, variable count, and a dictionary of ordinary exponent tuples to
field coefficients. Returned cardinalities are range-checked before
moment reconstruction.

## Independent exhaustive coefficient checks

The test enumerated all nonzero `gamma` and every `tau` over both `F_2`
and `F_4`, at every one of the eight moment indices. This gives 112
hypersurface cases. Each actual hypersurface was counted by evaluating
its manufactured ordinary polynomial at **every point, including w**.
The tests did not use the Artin--Schreier identity as a shortcut to obtain
those counts.

A separate direct pair-phase formula evaluated the expanded character
moment, without reading the manufactured polynomial. Every comparison

    actual_hypersurface_count - q^(v-1) = expanded_character_sum

passed. The totals were 1,728,136 actual hypersurface assignments and
432,404 independently expanded character assignments. These checks cover
nontrivial field coefficients, nonzero radial cubic phases, both pair
types, and the largest eight-variable reductions.

## Raw wrapper and transparent callback replay

The wrapper was executed on the existing raw 36-bit input, with an
explicit supplied callback and a zero reference-scan bit budget. The
callback matched the complete field modulus, variable count, and ordinary
coefficient dictionary against its prepared reductions before returning
each cardinality.

Preparation used the explicitly enumerated 16-value Gaussian-fiber
reference. Each replayed cardinality was formed as `q^(v-1)+moment`.
This is **not a Lauder--Wan implementation or execution**. The wrapper
made exactly seven calls in the expected order, used at most eight
variables, and returned

    signed_count = 3997696,
    zero_count   = 34361737216.

Both agree with the existing independent reference. The acquired
coordinate matrix, template parameters, and entire normalized ordinary
polynomial also agree with the reference certificate. Polynomial lists
are compared as coefficient dictionaries, since their insertion order
does not change the polynomial.

## Reporting scope

The original reporting ambiguity has been corrected in the root wrapper.
Its supplied-callback evidence now explicitly reports
`field_elements_enumerated_by_wrapper=0` and
`supplied_backend_internal_work_reported=False`, without an aggregate
`field_elements_enumerated` claim. The targeted replay asserts both
scoped fields and the absence of the former ambiguous key. Only the raw
36-bit replay was rerun after this metadata correction; the completed
exhaustive hypersurface counts were preserved without repeating them.

This test's callback used moments prepared by a 16-value scan. The saved
audit result records that preparation cost and labels the backend as
replay. It does not infer that the opaque callback executed a
polynomial-time point counter.

The generic fixed-variable point-count engine remains unimplemented.
