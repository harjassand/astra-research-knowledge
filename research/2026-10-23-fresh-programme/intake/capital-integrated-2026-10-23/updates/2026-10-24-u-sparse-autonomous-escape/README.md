# U sparse autonomous CTMC certificate — 24 October 2026

This is a separate sparse certificate for the finite classical population-channel construction. It retains a reported exact rational 48-state generator with 24 memory states per bit, `a=99999/100000`, and external readout time `T=pi`. The exact certificate, supplied result records, Root independent-check report and source scripts are pinned in the [source manifest](source_manifest.json). No source script or checker was run by this intake.

## Exact finite construction and sparse boundary

The source reports exact row and column balance, the intertwining relation, nonnormality, the return identity

```text
exp(pi Q) z = -exp(-pi a) z,
```

and a population-channel flip probability `(1+exp(-pi a))/2`. It reports a success gain of about `6.7881e-7` over the stated four-cycle comparison. The result is finite and exact at the certificate level; it does not describe a coherent quantum NOT.

The sparse support has 235 positive directed rates among 48 states, while the exact minimum off-diagonal rate is zero. Strong connectivity and the two balance identities hold, but **strict positivity of every off-diagonal entry fails**. The construction includes one-way edges. Under the result file's uniform-stationary, dimensionless natural-log CTMC edge-entropy convention, such an edge has positive forward stationary flow and zero reverse flow, so the formal stationary entropy production diverges. The source output records that quantity as `null` and marks `has_one_way_edges=true`.

## Kept distinct from the dense certificate

The earlier [dense V2 certificate](../2026-10-23-u-exact-autonomous-escape/README.md) remains intact. It has strictly positive off-diagonal rates and a finite source-reported stationary edge-entropy diagnostic. This update is a separate sparse-support certificate over the related V2 finite-state construction; it does not supersede or rewrite the dense result. The sparse certificate preserves zero rates and one-way edges, which change the formal entropy-cost boundary.

The generator is time homogeneous, but `T=pi` is externally selected. Physical implementation, useful utility, robustness, practical advantage and historical novelty are not established. The supplied independent exact-check report is preserved as source data; this intake did not replay it. The copied generation scripts are not standalone replay material because the sparse floating-support input is absent from the selected source snapshot.
