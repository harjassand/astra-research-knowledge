# Independent exact receiving check of separator/path witnesses

Contributor: `/root/separator_witness_check`.
Date: 22 October 2026 Australia/Brisbane / 21 October UTC.

## Accepted numerical claims

All seven frozen JSON witnesses passed a separate implementation using Python
`fractions.Fraction`. The verifier does not import the producer or its linear
algebra helpers. It reads the exact rational query matrix from each JSON,
reconstructs the sparse symmetric witness from its upper-triangle entries, and
computes every entry of its action directly.

For the largest supplied fixture, `s=2`, `m=4010`, `n=4012`, `q=4`, it verified

```
maximum row energy             = 1
||D X||_F^2                    = 24651/4
max path-edge coefficient^2    = 1447209
certified operator/action^2    = 643204/2739
certified operator/action      >= sqrt(643204/2739)
                               = 15.324219079547102... (display only)
integer-tent uniform bound C^4 = 160801/12027
constraint rank                = 3 (at most 2s=4)
```

The operator lower bound uses the magnitude of an actual matrix entry, which
is bounded above by the operator norm. No computed eigenvalue or singular
value is accepted as a certificate. The displayed decimal is explanatory;
the exact rational squared quotient is the acceptance datum.

The other four flow fixtures use `(s,m)=(0,8),(1,12),(2,20),(3,28)`. Their
maximum certified squared quotients, taking the larger of the path-flow and
local rank-one witnesses, are respectively `25/8`, `13/5`, `3`, and `3`.
These are individual exact witnesses, not the universal theorem or an
optimization over query designs. Two additional degenerate fixtures give
nonzero rank-one matrices with exactly zero action.

## What was independently checked

For each flow fixture the verifier establishes all of the following from
the frozen rational input and witness:

1. Shape, row-energy cap, joined-path support, unique upper-triangle entries,
   and the symmetric matrix represented by those entries.
2. The exact orthogonal projection off the apex query row span, reconstructed
   by a separate rational Gram inversion; quotient-row norms and orthogonality.
3. The oriented two-dimensional form, its positive scale `kappa`, and the
   nonzero determinants of consecutive quotient rows.
4. Reconstruction of the saved flow from its stated integer tents and
   coefficients; both endpoint conditions, nonzero flow, exact energy and
   mass, and `h^2 * energy <= 3 * mass`.
5. Every path diagonal and edge formula; every border entry and apex block
   entry in the support-preserving lift.
6. Every action entry, exact zero apex action, the transverse path-action
   identity, action squared norm, entry-based operator lower bound, and exact
   certified quotient.
7. Exact rank of the `2s`-by-`(2s+1)` constraint matrix and its annihilation by
   the saved coefficients. Full rank is unnecessary and is not assumed.
8. The small-row witness's minimizing quotient row, full rank-one identity,
   exact action norm and operator norm, and the combined rational fourth-power
   lower bound.

For the degenerate fixtures it verifies the actual nonzero vector, its
clique-supported rank-one matrix, the vector's zero action, and the matrix's
zero action. The apex-rank diagnostic is also independently checked. The
clique kernel's actual dependence is certified directly; locating the producer's
first eligible dependent clique is unnecessary for that claim.

## Source binding and its limit

Every frozen file's byte count and SHA-256 matches the original
`witnesses/PRODUCER_RECEIPT.json`. The receiver receipt records that manifest's
SHA-256:

`a982687e53cacb7b44286595143ac61b23354ecbfbbb7b4174bd7567d6c24374`.

The large fixture is 1,117,623 bytes with SHA-256

`f1e2e676e1d51d6072744f21b05a041b85ce3a78fcad8e9729eb1bb9c6b730d9`.

This binds the certificate to its saved exact `X`. It does not authenticate a
mutable manifest by itself. The receiving archive's externally supplied digest
remains the transport trust boundary. The fixture is a new structural example;
it is not the original NIST input or a claim about a measured physical operator.

## Targeted rejection checks

Four in-memory copies of the small `(s,m)=(2,20)` witness were corrupted. The
original files were left unchanged. All were rejected for the intended reason:

| Corruption | Rejection |
|---|---|
| Change one path coefficient | Path edge formula mismatch |
| Add a forbidden leaf-to-leaf edge | Outside joined-path support |
| Set one query entry to violate the cap | Row energy cap |
| Inflate the claimed uniform lower bound | Rational bound mismatch |

These checks exercise the scientific acceptance layer after parsing. The byte
hash checks would independently reject changed transported files.

## Replay and observed costs

From any working directory:

```
python3 /path/to/package/checks/verify_separator_witnesses.py \
  --witnesses /path/to/package/witnesses \
  --output /writable/path/independent.json
```

Source: `checks/verify_separator_witnesses.py`.
Receipt: `results/separator_witness_independent.json`.

One execution completed with no failed numerical run:

| Scope | Wall seconds | CPU seconds |
|---|---:|---:|
| Entire checker body, including source reads, hashes and four rejection checks | 1.530646674 | 1.530533601 |
| Largest fixture, already included above | 1.481536362 | 1.481430503 |

Peak process RSS was **31,256,576 bytes**. Imports precede the body timer.
Per-fixture timers are nested within the body and must not be added to it.
The initial source inspection was a separate brief tool call whose displayed
latency was about 0.4 seconds. Reading, authoring, reasoning, service latency,
model cost, money and energy are additional and not fully metered.

No original benchmark, old obstruction diagnostic, floating solver, witness
optimization, precision sweep, installation, external source search, or other
owner's work was performed. This is a receiving check of the supplied finite
witnesses. The universal theorem remains the parent's full analytic argument.
