# Executable threshold-source acquisition: scope and tests

31 October 2026. This is classical circuit-spec acquisition, not a quantum simulator implementation.

## Interface

`ThresholdSource(onsite, edges)` accepts a nonempty open binary chain. `onsite[i][b]` and `edges[i][a][b]` are strictly positive exact integers, rational strings or `Fraction` values; float and boolean inputs are rejected. The stationary law is proportional to the product of these supplied factors. There is no claim to infer them from observations.

The object acquires exact rational heat-bath rate tables and sorted threshold colors, local deterministic maps, `R`, `Ri`, and the fixed two-slot probability table for any supplied source label through `column(x)`. `map(f,y)` computes the needed forward threshold map, so the acquired output relation x=f(y) is directly checkable. The code never enumerates all2^n source states in acquisition or in an individual column request.

Right-hand conditional messages acquire the exact initial and conditional probabilities for a sequential preparation of sqrt(pi). They also compute the exact partition function and pi_min by sum-product/min-product dynamic programming. `parity_mean(mask)` evaluates an arbitrary source-diagonal Z-string expectation exactly by signed transfer messages; `sparse_parity_means` caches repeated masks within the request. It does not evaluate arbitrary Boolean coupling means for free, synthesize quantum rotations, or implement the fast-source consumer.

The exact maximum COLUMN influence sum gives kappa. If kappa<=0, the source data/columns remain valid but the Dobrushin return certificate is not admitted. If kappa>0, let ell be the smallest integer with2^ell>=16n/pi_min; the output m=ceil(R ell/kappa) gives the conservative certificate

    n(1-kappa/R)^m/pi_min <= 1/16.

This avoids floating log comparisons. A positive but extremely small kappa can give an enormous m. Returning its binary representation is not a claim that downstream execution has polynomial cost in input bit length independent of m. Actual m, coupling access, reference preparation, controls and precision stay paid.

## Verification and finite evidence

`specification(masks)` serializes the raw factors and acquired rational data. `verify_spec` reconstructs all data from those inputs and compares canonical JSON, rejecting altered probabilities, dimensions, budget fields, malformed factors, noncanonical numeric types and parity means. It verifies an algebraic record, not the truth of a physical source model, the correctness of a future gate backend, or an unknown clock.

The10 supplied test groups passed:
- invalid matrix/factor shapes, nonpositive/nonexact inputs and invalid labels;
- all exact columns and local erasure relations for test chains of sizes1 through4;
-32 seeded rational small-chain instances, checking equality of forward threshold and quantum-diagonal kernels and detailed balance exactly;
- exact conditional-message probabilities, pi_min and every parity mean on small chains;
- dense numerical W†W=I and W psi=c tensor psi on sizes1 through4;
- weak versus nonadmitted strong-interaction cases, exact dyadic return arithmetic, and deliberate record tampering;
- an n=64 symbolic chain, three individual columns and sparse means, with no full source-state table.

The n64 example uses onsite factors(1,1) and edge factors[[11,10],[10,11]]. It has380 interval colors, R=324808/4641, kappa=8399/9282 and conservative m=6111. Its saved circuit-spec JSON is67,077bytes. This is evidence of classical symbolic acquisition scaling, not evidence of practical complete quantum simulation.

## Binding source files

- `acquire_threshold_source.py`:9,263bytes, SHA256 1b79b249475c1cae8e240a1898c3413a4d8f29608f8365e07ae132d28bbd94be.
- `test_threshold_acquisition.py`:5,972bytes, SHA256 1675bed798d8cad401695f76e8fd2bb196bc268a1d5af4e62a37a827760b294a.
- `threshold_acquisition_tests.txt`:931bytes, SHA256 95fe211b78df9ff6a0e64c3cce31cd9bd90f67968c64500cfddcbb78c09c06ad.
- `threshold_source_n64_example.json`:67,077bytes, SHA256 21e1a986926e5bb452ccdade338732a0de886566c508d1be89514cd2b76799e8.

The paper circuit consumer is the separately checked `FINITE_BIT_THRESHOLD_STINESPRING_CONSTRUCTION.md` (d560f37e...). The prior weighted-grand-coupling mechanism is credited to Temme–Wocjan; this executable does not establish a new general quantization or a practical advantage over retained ordinary methods.
