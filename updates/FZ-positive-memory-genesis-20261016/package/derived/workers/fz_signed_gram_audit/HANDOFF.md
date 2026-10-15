# Signed Gram audit handoff

**Result:** `PASS_INDEPENDENT_EXACT_ALGEBRA_WITH_SCOPE_BOUNDARIES`.

The complete proof and claim ledger are in `SIGNED_GRAM_AUDIT.md`. The
independent script `independent_exact_diagnostics.py` passes eight exact
symbolic/rational diagnostic groups; see `EXACT_DIAGNOSTIC_RECEIPT.json`.
The producer script was inspected but never executed or imported.

The reconstructed normalized Choi block is

```
M(r) = [[r-tr(D), a^dagger], [a,D]],
D=diag(gamma)+C,       a=-k/2-i h.
```

Trace annihilation gives `2 Re(a)=-k`. Positivity is equivalent to
`D>=0`, `a in range(D)`, and
`r>=tr(D)+a^dagger D^+a`. This is the exact fixed-generator minimum;
unlisted Kraus directions do not evade it. The factorization and scalar
rate construction are valid for complex coefficients and singular `D`.
No ambient Hilbert-dimension factor is missing.

The sufficient fixed-floor constants are correct for `N>=1`, `nu>0`:

- `gamma_i=nu/(2N)`, `b<=nu/(8N)`, `||h||_2<=nu/(4 sqrt(N))`
  give `r_min<nu`, with upper fraction `2/3+13/(96N)<=77/96`.
- HP/TA errors with the specified normalized-Choi support and
  `||E||_diamond<=nu/(8N)` give upper fraction
  `1/2+1/(6N)<=2/3`.
- For `C=0`, the sharp uniform coefficient radius is
  `nu/(2 sqrt(N))`. Root box/ellipsoid floor optimizations are
  consistent corollaries within the diagonal-floor family.
- The jump replacement bound and its relative-amplitude constant
  are valid when every affected jump, induced Hamiltonian gauge,
  and actual product support are charged.

Retain the exact catalog obligation. A sparse catalog's robustness
neighborhood is within the verified structured model. Arbitrary
Hermitian `C` on a non-product-closed catalog is not automatically
covered. New exact signed-imaginary and positive-real examples have
unfloored product compressions with determinant `-eps^2` for every
rate, for arbitrarily small `eps`. A new rank-one signed-complex
case attains `r_min=1`; a kernel Hamiltonian perturbation gives
determinant `-4 eps^2` for every rate. These confirm the decisive
range/product boundaries.

No mathematical source repair is required under the already stated
hypotheses. A downstream summary should say “neighborhood within the
verified structured model,” keep the general signed theorem distinct
from the diagonal root theorem, and keep the memory conclusion
conditional on its universal support/recovery premise. This audit
does not establish that premise, physical feasibility, useful device
advantage, external peer verification, or historical originality.

Shang–França arXiv:2604.18533v1 Eq. (4) was independently acquired and
frozen as primary prior art for the shifted-jump identity. It is not
evidence of blanket novelty for the theorem or its application.

All four inputs are frozen and hashed in `INPUT_RECEIPT.json`; the
producer theorem pin is
`341fe38c2f66602c22868a36bdfe76c79add1097403834a5955bbe8e81e28555`.
All source files matched the freeze on verification. All writes were
confined to this audit directory; no source/root/other-worker/Git data
was edited. `ARTIFACT_HASHES.json` records the final artifact hashes.
