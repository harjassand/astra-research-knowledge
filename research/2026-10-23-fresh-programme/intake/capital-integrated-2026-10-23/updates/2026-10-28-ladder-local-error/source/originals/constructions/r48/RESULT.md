# Local parity-breaking response

For the connected semi-infinite ladder in the supplied governing proof at
\(g=1/5\), the requested infinite-system response to \(V=n_L-n_R\) is
**finite and strictly positive**. `PROOF.md` proves this analytically and gives
the exact continuum expression, including the exact dressed pair, both
one-body atoms and continua, and the odd hard-core constraint. The numerical
value is approximately
\[
 \rho_{1/5}(E_p)=2.1275067206\times10^{-8},\qquad
 E_p=5.97857931516658.
\]
The classification is proved independently of the decimal evaluation. The
decimal is a non-interval quadrature diagnostic.

The proof reduces the odd constraint to a rank-one resolvent correction. On
the open shell the source amplitude is a sum of the exact one-body endpoint
resolvents. This amplitude is nonconstant by its large-energy moment
expansion, so the corrected shell integral is strictly positive. The source is
the true dressed pair rather than the bare memory pair. In particular the
bound–bound term is retained in the correction and materially contributes to
it. The stated scalar spectral and boundary-value imports and the special case
of a coincident bound–bound energy are treated explicitly in the proof.

The spectral-density target is closed at the analytical level. A mathematically
controlled resonance expansion and a certified numerical enclosure are not
established here. The next physical attack is to prove a weak-\(\eta\)
resonance or survival-law theorem for this exact lattice operator, including
remainder and time-uniform estimates. Under such a theorem only, the formal
population-rate / energy-FWHM coefficient would be
\(2\pi\rho\simeq1.3367518968\times10^{-7}\), multiplying \(\eta^2\); the
amplitude-rate / energy-HWHM coefficient is half this number.

Reproduce the continuum calculation, finite local Fock check, and independent
high-precision integral from this directory:

```sh
OPENBLAS_NUM_THREADS=1 /usr/local/bin/python3 spectral_response.py --eps 1e-11
OPENBLAS_NUM_THREADS=1 /usr/local/bin/python3 spectral_response.py --fock-check
OPENBLAS_NUM_THREADS=1 /usr/local/bin/python3 spectral_response.py --check
DPS=60 /usr/local/bin/python3 high_precision.py
```

`results.json`, `fock_check.json`, `compression_check.json`,
`single_integral_check.json`, and `high_precision_{30,60}.json` retain the
executed outputs. The full Fock comparison has maximum error
\(2.7\times10^{-15}\); the 30- and 60-digit implementations agree in the
displayed response digits. Neither finite-volume agreement nor matching
floating-point results is treated as a continuum proof or an interval bound.

Source: `packet/ASTRA_SYMMETRY_FILTERED_EMBEDDED_PAIR_20261027.md`, SHA-256
`b465b21250366e67b0e341951b5d2a0ae64df18be495e831b81e7b8b35f19730`.
