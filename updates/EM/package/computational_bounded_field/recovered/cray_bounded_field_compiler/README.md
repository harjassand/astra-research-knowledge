# CRAY bounded-field mixture compiler: research handoff

Start with `RESEARCH_NOTE.md` for the theorem, proof, full-cost construction, counterexamples and priority/implementation limits.

## Files

- `verify_compiler.py`: constant-resolution envelope and rank-one mass diagnostics.
- `results.json`: captured output of that script.
- `verify_discrete_mixture.py`: full small-system output probabilities for the rejection-free mixture.
- `mixture_results.json`: captured output of that script.
- `verify_integral_layers.py` and `integral_results.json`: rank-one positive-volume-sum checks, including thin and far-shifted cells.
- `rank_one_product_compiler.py` and `product_prototype_results.json`: non-exhaustive rank-one product-base executable with uncertified hybrid numerical weights.
- `IMPLEMENTATION_LOG.md`: implementation changes and timed-out attempts.
- `CLAIMS.json`: explicit status and unresolved gates.
- `MANIFEST.json`: SHA-256 of the other handoff files.

## Reproduce

Python 3.10 or later; dependencies `numpy`, `scipy`, `mpmath`.

```sh
python verify_compiler.py --output results.json
python verify_discrete_mixture.py --output mixture_results.json
python verify_integral_layers.py --output integral_results.json
python rank_one_product_compiler.py --output product_prototype_results.json
```

The verification scripts enumerate their small base spin systems or compute one-dimensional volumes. The separate product-base prototype does not enumerate configurations while compiling or sampling, but uses uncertified hybrid SciPy/mpmath weights. None is the general, certified polynomial-time compiler. The high-precision diagnostics use 90-digit mpmath, not certified interval arithmetic. Timings are diagnostics only and are not comparative benchmarks.

**Scientific status:** a complete new proof candidate with credited algorithmic imports; finite tests passed; independent proof review, historical priority, general implementation and practical advantage remain unresolved. No GitHub repository was modified.
