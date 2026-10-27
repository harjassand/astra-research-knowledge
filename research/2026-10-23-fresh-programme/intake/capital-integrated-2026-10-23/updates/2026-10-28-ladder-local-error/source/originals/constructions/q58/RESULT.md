# Local parity-breaking pair response

## Construction and result

For the supplied semi-infinite hard-core ladder at **g=1/5**, I constructed the normalized dressed even pair, applied **V=n_L-n_R** exactly, and compressed the complete mixed-parity one-body product by its single forbidden odd double-memory vector. Every one-body atom and continuum is retained.

The exact response is the explicit one-dimensional continuum integral

\[
\rho(E_p)=\mathcal N^2\int_{4}^{E_p}a_+(x)a_-(E_p-x)
\left|r_+(E_p-x)+r_-(x)-\frac{A(E_p+i0)}{D(E_p+i0)}\right|^2dx.
\]

All factors and the correction constant are explicitly constructed in `PROOF.md`, equations (1)–(15). The proof establishes **0 < rho(Ep) < infinity**. Strict positivity follows because the real on-shell source cannot be constant; the odd hard-core compression subtracts only a constant. An independent interval certificate proves **rho(Ep)>4e-16** and **5.9785<Ep<5.9787**, without assuming quadrature accuracy.

Complete continuum quadrature gives **rho(Ep) ≈ 2.12750672e-8** and **Ep ≈ 5.978579315166579**. The nearby bound-bound atom at **E+ + E- ≈ 5.979315299977250** is retained and materially affects the scattering correction. The result is for the local parity-breaking operator; the source's parity-preserving wrong-band perturbation is different.

## Consequence and boundary

This supplies a fixed-coupling local symmetry-breaking coefficient for the actual protected pair. Exact parity conservation remains the strongest available protection in the source. The requested spectral classification is complete. A tight certified enclosure of the decimal coefficient and a resonance/finite-time theorem remain open. A probability linewidth **2*pi*eta^2*rho + o(eta^2)** for a static bias is conditional on that further theorem; no measured lifetime, hardware tolerance or gate advantage follows here.

## Files and reproduction

- `PROOF.md`: full construction, continuum formula, regularity and strict-positivity proofs, certificate explanation, limits and preserved failed shortcuts.
- `continuum_response.py`: exact half-line spectral measures, normalized pair and complete odd continuum evaluation.
- `continuum_results.json`, `continuum_convergence.json`: executed numerical results and convergence checks.
- `certify_positive.py`, `positive_certificate.json`: outward-rounded support/interval certificate.
- `check_operator_identities.py`, `operator_identity_checks.json`: separate finite physical-Fock checks of source/compression factors at a nonreal spectral parameter.

Run with Python 3 plus numpy and mpmath. No SciPy or finite-chain approximation enters the continuum value or its classification. Next attack: prove analytic continuation or a weighted limiting-absorption perturbation theorem for **H+eta V**, then certify the finite-time regime of the conditional decay law.
