# Local resonance theorem

The construction in `PROOF.md` gives a local resonance pole for the actual
semi-infinite hard-core Hamiltonian

\[
 H_\eta=H_g+\eta(n_L-n_R),\qquad g=1/5.
\]

It deforms both bath momenta by (k\mapsto k-i\theta\sin k), with

\[
 \theta=1/4,
\]

leaving the memories and the two forbidden double-memory states fixed.
The resulting bounded analytic operator is an exact deformation of the
physical two-particle Hamiltonian. The unperturbed pair is an isolated,
algebraically simple eigenvalue of this operator, including its odd
sector. A Neumann/Riesz argument then gives, for sufficiently small

\[
 |\eta|,
\]

a unique analytic even pole branch, visible in both the bare-memory-pair
and the unperturbed dressed-pair responses:

\[
 \lambda(\eta)=E-\eta^2
 \langle V\psi,(H_{g,\mathrm{odd}}-E-i0)^{-1}V\psi\rangle
 +O(\eta^4).
\]

Consequently the supplied exact positive source density is the actual
leading width coefficient:

\[
 \operatorname{Im}\lambda(\eta)
 =-\pi\rho_g(E)\eta^2+O(\eta^4)<0
\]

for every sufficiently small nonzero real detuning.

Two gaps in a naive deformation argument are resolved explicitly:

- The mixed-band threshold at 6 is excluded by an analytic proof that
  (E<6), using positive-block monotonicity in the upper-channel coupling.
- A possible equality (E=E_++E_-) is not assumed away: its simple
  harmonic atom pole cancels in the odd hard-core compression.

The exact full-(eta) pole criterion is the two-by-two forbidden-state
Schur matrix when the harmonic resolvent exists, and the augmented
operator in equation (27) otherwise. It retains every power of (eta).
The local disk and positive detuning radius are specified by explicit
resolvent inequalities; their numerical sizes are not certified.

# Executed checks

Run:

```sh
/usr/local/bin/python3 /Users/harjas/Documents/ChatGPT/coordination/work/astra-policy-terra-20261027/c74/contour_check.py
```

The script evaluates the continuum momentum deformation by Gauss-Legendre
quadrature and separately solves the actual-detuning hard-core Schur
equation of that quadrature. Its output is
`contour_check_results.json`.

It finds

\[
 s(E+i0)\simeq0.00707837231216+6.6837594\times10^{-8}i,
\]

consistent with the supplied

\[
 \rho_g(E)\simeq2.1275067206\times10^{-8}.
\]

Roots at (eta=.04,.02,.01) have

\[
 \operatorname{Im}(\lambda-E)/\eta^2
 \simeq-6.6985\times10^{-8},\ -6.6861\times10^{-8},\ -6.6844\times10^{-8}.
\]

These are floating-point diagnostics, not interval enclosures or the
existence proof. No finite-chain root is used to infer an infinite-system
pole.

A separate direct two-boson Fock check of the full two-constraint inverse
agrees with the Schur formula to (5.7\times10^{-12}) entrywise at a
declared off-real point and confirms the physical perturbation norm is
one.

# Remaining scope

The written construction closes the local mathematical target, subject
to review of the operator proof and retention of the supplied exact
dressed-source density calculation. No independent audit of this new
proof is claimed. A numerical lower bound for the detuning radius,
interval bounds for the coefficients, survival-law control, and physical
device performance remain unestablished. They are not premises of the
qualitative local theorem.
