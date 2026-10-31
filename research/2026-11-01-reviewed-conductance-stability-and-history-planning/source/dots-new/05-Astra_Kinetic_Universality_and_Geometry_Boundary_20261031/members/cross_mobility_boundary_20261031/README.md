# Fixed marginal diffusion is insufficient; the cross-mobility boundary is exact

Fixed ordinary reversible model: F(y,z)=[1+(1-y^2)^2]z^2/2, beta=1,
A={y<=-1/2}, B={y>=1/2}, and the same invariant Gibbs law for every matrix.

For arbitrary constant SPD D=[[1,b],[b,c]], put delta=1-b^2/c. The proof earns:

    cap_D -> 0  iff  delta -> 0 and |b| -> infinity.

Thus the no-cross premise of the accepted transverse-mobility family is
consequential, not removable from knowledge of the potential and D_yy=1 alone.
The construction is a true global diffusion family with exact full-fiber trial
boundaries, not a locally small gradient energy or a singular-process argument.

## Concrete rational family

For integer k>=1 and rational 0<epsilon<1,

    D=[[1,k],[k,k^2/(1-epsilon)]],
    epsilon/16 <= cap_D <= 36epsilon+(1200/k)e^(-k^2/128),
    cap_D/mu(A) <=144epsilon+(4800/k)e^(-k^2/128).

Taking k=n,epsilon=1/n proves collapse with rational, finite, SPD inputs at
every n>=2. All matrices retain D_yy=1. Their transverse mobility and cross
covariance diverge, conditional longitudinal mobility vanishes, and spectral
conditioning deteriorates. Those costs are explicit, not a uniform resource
claim.

## Files and replay

- `PROOF.md`: global normalization/process proof, smooth exact boundary patch,
  explicit constants, lower bounds, exact geometry classification, costs.
- `receive.py`: strict fixed-grammar exact rational receiver.
- `check.py`, `check_results.json`: algebra checks, 21 malformed-input rejections,
  four exact finite certificates, and explicitly non-authoritative float summaries.
- `certificates.json`: all exact rational enclosures from the replay.
- `example_input.json`, `example_certificate.json`: standalone received model.
- Independent review/check files were authored separately; final audit PASS.

Replay from this directory:

    python check.py
    python receive.py example_input.json --output example_certificate.json

No nonstandard Python package, quadrature, equilibrium sampler, hidden partition,
PDE solver, fast-equilibration premise, or physical implementation is consumed.
No original Dirichlet-principle, generic rate-hardness, arbitrary-start MFPT,
biology, or chemical implementation claim is made. Other source freezes remain
unchanged.

The finite receiver is deliberately narrow: it receives only this analytic
potential and exact rational constant mobility; its output is not a certificate
for arbitrary measured dynamics. The all-real-matrix classification is analytic
and wider than the receiver's admitted parameter grammar.

Additional verified files:
- `HIGH_DIMENSIONAL_COROLLARY.md`: dimension-free patch bound and explicit
  rational sequence defeating the relative free-capacity benchmark, with
  exponentially deteriorating conditioning fully paid.
- `INDEPENDENT_REVIEW.md`: final whole mathematical/receiver/corollary audit PASS.
- `independent_highdim_check.py` and results: exact extension checks.
- `cli_replay_results.json`: valid CLI receiving, raw duplicate-key rejection,
  and pre-allocation resource-budget rejection.
- `DEPENDENCIES.json`: replay environment; main receiver needs only stdlib.
- `FROZEN_SHA256.txt`: exact final file digest manifest.

Default resource policy rejects expanded integer exponents over 1,000,000 before
allocation; `--max-expanded-power` is an explicit configurable computational
budget, not a restriction on the analytic theorem.
