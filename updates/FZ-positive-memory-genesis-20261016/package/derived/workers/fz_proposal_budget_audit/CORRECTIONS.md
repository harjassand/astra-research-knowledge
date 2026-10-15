# Corrections and scope clarifications for the root

Against `SOURCE_ROOT_THEOREM.md`, SHA-256
`f68d5563912410e6497b7f5d5b1460a48864b5f9a576db448c87d9003390965d`.

1. **Lines 50-52: extend the exact statement and remove ambiguous limits.**
   Replace the finite-collection restriction by any state-independent CPTP
   proposal family of finite nonnegative total rate. For `gamma_i>=0`, state
   `h in Ran(diag(gamma))`, with `r_min=sum gamma+h^T diag(gamma)^+h`;
   otherwise `r_min=+infinity`. Treat the zero generator as an empty rate-zero
   decomposition. Joint zero-floor limits are path dependent.

2. **Lines 68-70 and 90-102: match the receiver's rate convention explicitly.**
   The receiver's equation (8) caps the sum of proposal types **per center**
   and already counts all centers whose bounded support reaches the guard.
   Write the local hypotheses with an anchor index: `2sum_t epsilon_(x,t)`
   or `2sqrt(sum_t b_(x,t)^2)` bounded by the receiver's `nu_q` for every `x`.
   If using a touching-cell budget, instead state the full support-incidence
   sum and any conversion factor; do not identify it silently with center
   rate or multiply incidence twice.

3. **Lines 66-67 and 78: keep “optimal” tied to the total-rate objective.**
   The proofs optimize total rate for one given catalog block. With different
   supports this need not optimize the largest touching-cell rate. A two-term
   disjoint-support ellipsoid with axes `(3,4)` is an exact counterexample:
   total-optimal floors have maximum touch `41/5`, while floors `(3,4)` have
   maximum touch 8 and a larger total rate. Add a short objective qualifier.

4. **Line 107: fixed body count must also have fixed geometric range.**
   Two qubits can be arbitrarily far apart. The receiving theorem needs
   uniform support radius and bounded incidence, beyond fixed Pauli weight.

5. **Line 23, minor wording:** any real scalar identity part of `H` is
   irrelevant, not only a positive scalar part.

The root already correctly excludes operator-norm substitution without a
conversion, arbitrary bath-valued coefficients, unrestricted dissipators,
the unmodified correction generator, physical fabrication, and historic
novelty. No reversal of the core rate or minimax formulas is required.
