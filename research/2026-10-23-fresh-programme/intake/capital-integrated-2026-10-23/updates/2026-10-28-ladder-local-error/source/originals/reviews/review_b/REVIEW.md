# Independent source-informed review B

All four endpoints are **ACCEPTED for the fixed target**
\(0<\rho_{1/5}(E_p)<\infty\). This is a mathematical spectral-density
acceptance, with no lifetime, experimental, novelty, or gate-error conclusion.
The agreement of their numerical answers is not my reason for acceptance:
the source, projection, scalar boundary limit, and strict sign can each be
reconstructed directly from the governing operator.

| Endpoint, reviewed in this order | Verdict | Decisive argument | Qualification |
|---|---|---|---|
| S62 | ACCEPT | Complete-measure normalization, exact rank-one compression, Hölder/Plemelj limit, and unequal-second-moment nonconstancy proof all close | Decimal remains ordinary quadrature |
| S29 | ACCEPT | Exact atom roots and all three weighted scalar boundary densities are controlled; explicit cancellation handles a coincident atom sum; moment proof excludes screening | No target-level proof/coding gap found |
| S83 | ACCEPT | Its distinct/coincident pole argument is valid: the atom residues cannot cancel because their weights are unequal | Smoothness needed for its Hölder statement follows from the explicit source formula; finite Fock evidence is only algebra evidence |
| S41 | ACCEPT | Its explicit endpoint boundary functions allow the dominated-convergence proof; the Poisson limit and moment proof close | Trailing decimal roundoff and an unused complex-real branch corner, detailed below |

## Reconstruction independent of endpoint agreement

Use the convention \(m_\sigma(z)=\int(t-z)^{-1}d\mu_\sigma(t)\), with
\(k_+=2/25,k_-=1/25\) and bath centers 5 and 1. The scalar Schur
function has one simple atom in each channel and the stated square-root
band density. Strict monotonicity off the bath band and the nonzero edge
denominators exclude extra atoms; the explicit square-root resolvent
excludes an omitted singular part. Cyclicity of the Jacobi endpoint means
these measures represent the full one-body channels.

For the even pair root \(L_+(E)+L_-(E)=0\), put
\[
D=L_+'(E)+L_-'(E),\qquad C=\sqrt{2/D}.
\]
The normalized state is
\[
\psi=D^{-1/2}\big[(A_{++}-E)^{-1}q_{++}
                         +(A_{--}-E)^{-1}q_{--}\big].
\]
The forbidden even vector is \((q_{++}+q_{--})/\sqrt2\); its overlap
vanishes by the root condition. This establishes both normalization and
the physical compression. The bare-pair weight is \(2L_+(E)^2/D\).

In the odd space the free harmonic operator is multiplication by \(x+y\)
on \(L^2(\mu_+\otimes\mu_-)\). Its forbidden vector is exactly the unit
constant \(q=1\), corresponding to \((|LL\rangle-|RR\rangle)/\sqrt2\).
The physical operator is the compression to \(q^\perp\). Direct contraction
of one memory coordinate, including the bosonic \(\sqrt2\), gives
\[
f=V\psi=C u,\qquad u(x,y)=m_+(E-x)+m_-(E-y),\qquad
\langle q,u\rangle=L_+(E)+L_-(E)=0.
\]
This is the dressed source; \(V|LR\rangle=0\) cannot replace it.

For complete-measure transforms
\(K=\int(x+y-z)^{-1}d\nu\),
\(J=\int u(x,y)(x+y-z)^{-1}d\nu\), and
\(F=\int u(x,y)^2(x+y-z)^{-1}d\nu\), elimination of the one forbidden
direction gives
\[
\langle f,(H_{\rm odd}-z)^{-1}f\rangle=C^2(F-J^2/K).
\]
The analytic square is essential. With \(\alpha=J/K\), direct algebra
gives the positive identity
\[
\operatorname{Im}(F-J^2/K)=
\int\frac{\epsilon|u-\alpha|^2}{(x+y-E)^2+\epsilon^2}\,d\nu.
\]
The odd atom-band continua are below \(E_++2<4.959\) or above
\(E_-+4>7.021\) at the fixed coupling. Only band-band states are
continuously on shell. The complete-measure correction still includes all
four atom/band products. The weighted band-band densities are locally
Hölder because the endpoint densities have square-root edges and the source
is analytic on the band rectangle. Their scalar Cauchy boundary values are
finite. The unweighted shell has positive mass, so \(\operatorname{Im}K>0\)
unless its atom term is divergent. If the free atom sum equals \(E\), the
common atom poles instead give \(\alpha\to u(E_+,E_-)\) with error
\(O(\epsilon)\); the atom contribution in the positive identity is then
\(O(\epsilon)\). Thus no unproved nonzero connected-shift assumption is
needed.

It follows that the requested scalar boundary density is
\[
\rho(E)=C^2\int_{\max(4,E-2)}^{\min(6,E)}
r_+(x)r_-(E-x)
\left|m_+(E-x)+m_-(x)-\alpha_*\right|^2dx.
\]
This is an infinite-system expression, not a finite-chain extrapolation.
Its integrand is bounded. For the strict sign, on the connected half-line
\(x>\max(E-E_+,E_-)\), write \(U(x)=m_+(E-x)+m_-(x)\). Exact endpoint
moments give
\[
U(x)=\frac{E-6}{x^2}
 +\frac{E^2-6E+k_+-k_-}{x^3}+O(x^{-4}).
\]
If \(U\) were constant on the open shell, analyticity and its zero limit at
infinity would make it identically zero there. The first coefficient would
require \(E=6\), and the next would require \(k_+=k_-\), contradicting
\(k_+-k_-=1/25\). The positive shell weight therefore gives strict
positivity for every scalar correction \(\alpha_*\). This reasoning also
independently checks the sign conclusion of S83's different pole proof.

## Case-specific assessment

**S62.** Equations (5)–(10) have the correct state normalization, source
arguments, bosonic factor, analytic square, and density convention. Its
moment expansion has the correct signs. The coincident atom treatment
closes a potential scalar limiting-absorption loophole rather than relying
on the numerical connected shift. I replayed the double integral, independent
single-integral reduction, finite compression, local Fock check, and 60-digit
script from copies. The Fock differences are at most \(2.67\,10^{-15}\).
The double-integral density is \(2.1275067206108463\,10^{-8}\); the
60-digit diagnostic is \(2.12750672061584377236\,10^{-8}\). No target
repair is needed.

**S29.** The exact atom roots satisfy the unsquared Schur equations, with
the excluded quadratic roots not silently included. The proof controls
\(N_0,N_1,N_2\), explicitly displays the cancellation at atom coincidence,
and correctly distinguishes the source-scaled correction from the unscaled
one in S62. The variance inequality is mathematically valid; its decimal
evaluation is not an interval certificate. All continuum, physical-rail Fock,
and arbitrary-precision checks replayed successfully. Maximum physical
resolvent discrepancy was \(1.86\,10^{-15}\). No target-level gap found.

**S83.** For \(F(z)=s_+(E-z)+s_-(z)\), the transformed plus atom residue
is \(+w_+\) and the minus atom residue is \(-w_-\). Both poles lie away
from both band cuts. Distinct poles cannot cancel. At coincidence,
\(d_+>d_-\) and strict increase of
\(d/\sqrt{d^2+4d+3}\) imply \(w_+<w_-\), so the merged pole is also
nonremovable. Analytic continuation through the connected complement of
the cuts/poles justifies the nonconstancy conclusion. Its boundary discussion
can be read directly using the analytic source already established in (5),
including the squared source in (7); no extra LAP import is necessary.
The replayed Fock relative errors were at most \(2.98\,10^{-14}\).
The extension to the governing \(0<g\le0.4\) gap regime is supported.

**S41.** The bounded explicit endpoint boundary functions in (9) give a
valid dominated-convergence route to the needed ratio, and continuity of
the weighted sum density then suffices for the positive Poisson limit.
Its first two moment coefficients agree with direct reconstruction. Its
general gap-regime extension is supported. The continuum replay yields
\(2.12750672152351\,10^{-8}\), about \(9.1\,10^{-18}\) above the
arbitrary-precision diagnostic. My independent unsplit Gaussian calculation
reproduces that offset; separating the common near bound-bound pole reduces
it to the \(10^{-19}\) scale. The two large atomic contributions to the
unscaled \(J\) cancel and amplify atom/root roundoff; tightening the band
quadrature tolerance does not diagnose it. Accordingly its trailing quoted
digits should not be treated as validated precision.

There is also an unused helper corner: for its plus channel,
`surface(3.) = 0.535898384862...`, whereas `surface(3.+0j) = 7.464101615137...`.
The complex branch rule tests a strictly negative imaginary part and misses
the real-left-of-band branch when that part is signed zero. Its actual
continuum path passes real floats there and is unaffected; the upper-half-plane
limit selects the correct branch. This is a concrete, nonblocking coding
limitation, recorded in `S41_nonblocking_api_probe.json`. Frozen code was not
repaired.

## Independent checks and replay evidence

`independent_checks.py` imports none of the endpoint implementations. It:

- verifies the odd compression identity exactly with SymPy at
  \(z=31/5+i/17\) for the one-rung parity tensor operator, and verifies the
  exact bosonic \(\sqrt2\) conversion and \(V|LR\rangle=0\);
- constructs the original connected rails and the full harmonic/physical
  Fock operators by occupation-number hopping at lengths 3, 5, 7, reconstructs
  the normalized pair with the full harmonic resolvent, and compares the
  source pointwise in every plus/minus eigenmode;
- checks three complex resolvents, including nonzero real shifts, instead
  of only the endpoint-supplied regulators;
- integrates the complete continuum measures using fixed Gaussian rules of
  24, 48, 96, 192, 384 nodes per smoothed segment, with an independently
  evaluated atom-subtracted correction.

Maximum pointwise source discrepancy was \(3.14\,10^{-14}\); maximum pair
eigen-equation residual was \(1.24\,10^{-14}\); maximum complex resolvent
discrepancy was \(1.58\,10^{-15}\). The exact finite-\(\epsilon\) positive
identity differed by at most \(1.31\,10^{-18}\). Complete moments reproduce
\((1,3,9.08)\) and \((1,3,9.04)\). The weighted-variance diagnostic is
\(1.50513922228\,10^{-12}>0\); its numerical sign is auxiliary to the
analytic proof. Dropping the odd compression gives about
\(1.42621721824\,10^{-11}\), and dropping the atom terms in the correction
also changes the result materially.

All endpoint code replays exited successfully. Commands and main results are
in `evidence_summary.json`; complete new outputs are in `replay/`; the
independent raw output is `independent_results.json`. The first independent
Fock run emitted macOS BLAS floating-flag warnings despite finite residuals.
The final script explicitly checks finiteness of every recorded numerical
field and suppresses those retained flags during Fock operations. No
numerical result is being promoted to an interval enclosure.

## Scope and actual source exposure

Each endpoint correctly leaves resonance and lifetime claims conditional.
A scalar unperturbed density alone does not establish a resonance pole for
the full bounded \(V\), continuation of the reduced resolvent in the
perturbed even/odd block problem, or a survival-law remainder on a specified
time scale. The factors \(\pi\rho\) for amplitude HWHM and \(2\pi\rho\)
for population rate/FWHM are consistent under an applicable second-order
resonance theorem. No such theorem has been supplied or acquired here.

I read the governing Markdown note and **all five** packet Python sources in
full: `astra_symmetry_filtered_embedded_pair.py`,
`astra_local_ladder_embedded_pair_audit.py`,
`astra_local_pair_interaction_tunability.py`,
`astra_band_filter_leakage_coefficient.py`, and
`astra_symmetry_filtered_CZ_protocol.py`. I then read each endpoint's entire
governing prose and every Python source, in the requested order S62, S29,
S83, S41. I also read their frozen manifests; selected original S62 numerical
outputs; and the new replay/independent outputs used above. All original
manifested files still match their frozen hashes after review.

I did not read memory, coordinator notes, model maps, protocols/admission
files, programme chats, other reviewers, or external cited papers. No mapping
from the four opaque S labels to models or policies was accessed. The supplied
required path itself contains the literal name `astra-policy-terra-20261027`;
I made no endpoint-provenance inference from that name. All authored review,
copied-source, and replay files are under `review_b/`.
