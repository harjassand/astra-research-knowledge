# Local parity-breaking pair response

**Completed spectral result:** for the exact ladder and normalized even
hard-core pair in the supplied governing packet, the actual detuning
\(V=n_L-n_R\) has
\[
 0<\rho_{1/5}(E_p)<\infty.
\]
The proof actually covers \(0<g\le0.4\). It retains the complete
one-body bound atoms and continua and treats the odd hard-core constraint
by an exact rank-one resolvent compression. A positive on-shell continuum
integral gives the answer; analyticity and unequal second endpoint
moments prove that its dressed source cannot be constant, hence cannot
be removed by the hard-core scattering correction.

Continuum quadrature gives
\[
 E_p\simeq5.978579315166578,\qquad
 \rho_{1/5}(E_p)\simeq2.12750672152\times10^{-8}.
\]
The positive/finite classification is analytical; these decimal values
are not interval-certified. Three continuum tolerances agree. Independent
physical Fock calculations verify the source normalization and complex
resolvent identity to about \(2\times10^{-15}\); they are algebra checks,
not the infinite-system evidence.

**Files:** `PROOF.md` contains the full construction and direct scalar
boundary-limit proof. `continuum_response.py` and
`continuum_results.json` contain executable infinite-system quadratures.
`check_fock.py` and `fock_check_results.json` contain the independent
normalization/compression check. No shared input was modified.

**Remaining gap:** none for the requested spectral classification and
continuum expression. An actual resonance/lifetime theorem and certified
decimal enclosure are separate, unproved extensions. If a second-order
resonance theorem applies, the amplitude half width would be
\(\gamma=\pi\eta^2\rho+o(\eta^2)\), and the population rate/full width
would be \(\Gamma=2\gamma\), with \(\hbar=1\).

**Exact next attack:** prove the needed continuation or weighted resolvent
regularity for the \(\eta\)-perturbed even/odd block operator and control
the resonance-pole remainder before turning this density into a lifetime
or operational error statement.

Source boundary: the frozen
`../packet/ASTRA_SYMMETRY_FILTERED_EMBEDDED_PAIR_20261027.md` defines the
Hamiltonian and even-pair construction. The detuning source, odd
compression, scalar boundary proof, positivity argument, and computations
in this directory are the present construction. No historical novelty or
physical-device advantage has been established.
