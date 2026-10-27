# Local symmetry-breaking response and compensation

## Choice

I attacked the actual local-error channel of the supplied interacting embedded pair. Its ideal CZ is already established in the source; the missing coupling to the forbidden continuum was a concrete construction opportunity. N750's conditional resonance integration is a materially different high-consequence alternative, but its global phase/variance control remains unavailable.

## Construction

For the source ladder plus a local memory-frequency mismatch delta*(nL-nR), I constructed the exact odd-sector hard-core response and positive continuum integral. The small-error resonance-pole probability linewidth has the weak-g coefficient

\[
 \Gamma_{\rm pole}=\delta^2[0.0722287299931\ldots\,g^8+o(g^8)]
                  +O_g(\delta^4).
\]

The order of limits is error to zero at fixed g, then g to zero for the coefficient. A direct unconstrained estimate incorrectly gives g^12; retaining the odd hard-core scattering constraint changes the leading answer.

I then constructed a real local counterterm: an antisymmetric frequency shift epsilon*(nA0-nB0) on just the first rail rung. The two local errors have the positive leading linewidth matrix

\[
 g^8\begin{pmatrix}.0722287300&.0764655092\\.0764655092&.0818535682\end{pmatrix}.
\]

Choosing epsilon=-0.934174414911*delta reduces the leading coefficient to 0.000796607698822*delta^2*g^8, about 90.7 times smaller. Its residual is strictly positive by strict Cauchy-Schwarz: these two controls cannot cancel the full continuum shell. Finite coupling requires its computed finite-g optimum; at g=.2 the ratio is -0.87110445 and the remaining fraction is .0153891. The extended local Hamiltonian remains nonnegative in every excitation sector for g<=.4 and |delta|,|epsilon|<=.1.

## Evidence

The continuum calculation retains both bound atoms and all continuum weight. At g=.2, 80/160/320 quadrature nodes agree in the scaled memory-error coefficient to approximately 2e-15 absolute. Eighteen independent full physical Fock-resolvent comparisons, for both perturbations and three chain sizes, agree within 1.09e-15. These finite-chain checks validate identities; they do not measure continuum lifetimes.

## Residual gap

There is no explicit remainder uniform in g, error size, ramp duration and bath loss for the complete CZ code isometry. The local continued pole does not alone certify exponential behavior over a gate, loading error, or arbitrarily slow ramps. Ordinary bath loss has leading pair-plateau cost proportional to kappa/g^2 and opposes simply reducing g. Estimating delta, tuning the first rung, physical realization and practical comparator advantage remain unacquired. Direct memory retuning, if available, is a stronger ordinary correction.

The next attack is an explicit spectral-kernel bound from the constructed constrained resolvent, combined with the even-sector gap and finite ramps over times of order g^-4.

## Files

- `CONSTRUCTION.md`: derivation, local continuation, compensation, stability, failures and sources.
- `local_detuning_response.py`, `continuum_response_results.json`: infinite-chain response and convergence.
- `local_compensation.py`, `local_error_gram_results.json`: acquired counterterm and finite-g matrices.
- `finite_fock_audit.py`, `finite_fock_audit_results.json`: independent physical Fock checks.

Sources are the supplied frozen packet and primary literature identified in the construction. Historical novelty and experimental usefulness are unestablished. No shared inputs or retrieval checkout were changed.
