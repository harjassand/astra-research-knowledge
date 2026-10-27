# Local resonance result

The supplied handoff **already closes the full qualitative pole target**.
After inspecting its complete proof and code, and the named normalized-pair
and dressed-source input, no load-bearing repair is required. At fixed
`g=1/5`, the actual infinite hard-core Hamiltonian
`H_eta=H_g+eta(n_L-n_R)` has an outgoing local resonance pole

\[
 \lambda(\eta)=E-s(E+i0)\eta^2+O(\eta^4),\qquad
 \operatorname{Im}\lambda(\eta)=-\pi\rho_g(E)\eta^2+O(\eta^4),
 \quad \rho_g(E)>0.
\]

The pole is simple and visible in both the bare-memory-pair and the
unperturbed dressed-pair response for every sufficiently small real eta;
it lies strictly below the real axis for sufficiently small nonzero eta.
The sheet lowers both bath momentum contours by
`k -> k-(i/4)sin(k)` with fixed endpoints. The disk and positive detuning
radius are specified by resolvent inequalities; their numerical sizes are
not certified.

# What the supplied construction established

The supplied proof already contains the exact bounded analytic deformation
of the full detuned hard-core operator, an analytic proof `E<6`, exclusion
of deformed spectral sums, odd hard-core invertibility even if E coincides
with the harmonic bound-bound sum, physical-response matching, and a
rank-one Riesz perturbation argument. Its source identity identifies the
actual coefficient and its sign. These are sufficient for the stated
theorem; this integration does not claim another theorem from them.

# Added derivation and executed checks

`PROOF.md` gives a coherent source-bound construction and adds an exact
local Feshbach denominator that retains every power of eta:

\[
 \mathcal F(\eta,z)=E-z-\eta^2B(f,D_\eta(z)^{-1}f),\qquad
 D_\eta(z)=Q_0(H_\theta+\eta V-z)Q_0|_{\operatorname{ran}Q_0},
 \quad f=V\psi_\theta.
\]

It derives `G_psi^out=1/F` and an explicit analytic numerator for the bare
response. It also expands the coincident harmonic-atom cancellation into
a manifestly regular operator formula. These are independent algebraic
derivations/checks of the supplied endpoint, not missing hypotheses or
new scientific claims.

An owned unchanged copy of the supplied contour script reproduced its
results. The independent `integration_check.py` constructs physical L,R
Fock states and checks both exact reductions. At 20 nodes per bath, with
901 allowed states, the two-constraint inverse error is `2.1e-13`;
Feshbach equation residuals are below `8.5e-14` across the executed cases;
the two explicit response identities agree within `2.2e-10` absolute
error, and eta-evenness within `4.1e-20`. The perturbation norm is one.
The direct estimate `Im(s)=6.68387e-8` agrees with the better supplied
96–160-node estimate `6.6837594e-8` at its modest numerical scope.

Coarse failures are retained: eight nodes produce a spurious unperturbed
imaginary energy and a wrong-sign imaginary coefficient; twelve nodes
still underresolve the width. They do not establish or refute the
infinite-system theorem. All numerical outputs are floating-point
diagnostics, not interval certificates. Original inputs are unchanged.

# Remaining scope and next attack

There is no remaining mathematical obstruction to the requested local
small-eta existence and leading-width statement. The coefficient decimal
and a usable numerical detuning range remain uncertified. The next
quantitative attack is validated deformed-arc/Schur-resolvent bounds for
`r, M_r, N_*`, followed separately by threshold-aware inverse-transform
control if a survival law is wanted. No exponential lifetime,
finite-device fidelity or hardware advantage is claimed.

Reproduce the executed work with:

```sh
/usr/local/bin/python3 /Users/harjas/Documents/ChatGPT/coordination/work/astra-policy-terra-20261027/c86/supplied_contour_check.py
/usr/local/bin/python3 /Users/harjas/Documents/ChatGPT/coordination/work/astra-policy-terra-20261027/c86/integration_check.py
```
