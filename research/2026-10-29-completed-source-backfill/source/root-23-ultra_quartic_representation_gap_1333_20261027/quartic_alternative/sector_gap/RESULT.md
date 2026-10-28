# Completed exact mathematical separation

For \(A=\left(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right)\), set
\(u=a^2+c^2\), \(v=b^2+d^2\), \(w=ab+cd\), and \(q=ad-bc\). The quartic

\[
F=u^2+v^2+3w^2+\frac{113}{10}q^2+4q(u-v)
\]

is globally polyconvex and quantitatively quasiconvex, but is **not SOS
polyconvex for any polynomial selector degree** under Definition 2.5 of
[Fantuzzi et al., arXiv:2604.11124v1](https://arxiv.org/html/2604.11124v1#S2.Thmdefinition5).
The same separation holds throughout a 35-dimensional monomial coefficient
box of radius \(1/616000\). It supplies the planar quartic case left open
in that source's Remark 2.1. Historical priority beyond the checked sources
is UNKNOWN; the full Morrey implication remains unresolved.

The positive construction is a rational 60-feature identity
\(|X|^2P(A,X)=Z^TRZ\), with \(R-I/200\succ0\), where

\[
P=F(A+X)-F(A)-DF(A):X-
 \left[\frac{14611}{2500}(u-v)+\frac{110757}{5000}q\right]\det X.
\]

It gives the global compatible-gradient bound

\[
\int[F(A+D\varphi)-F(A)]\geq
\frac{|A|^2}{400}\int|D\varphi|^2+
\frac1{1200}\int|D\varphi|^4.
\]

The parent's independent rational dual is negative on the unmultiplied
Bregman residual by \(-39/125000\), vanishes on all ten quadratic determinant
selector directions, and has a positive-definite 26-feature moment matrix.
The all-degree reduction is proved analytically, without symmetry.

`PRIMARY_PROOF.md` gives the complete theorem, finite convex lift, all-degree
obstruction, perturbation bound, ordinary comparator, costs, retained failed
assumptions, and exact limitations. `EXACT_MULTIPLIER_SUPPORT.json` contains
the positive certificate. `external_inputs/PARENT_EXACT_SUPPORT_SEPARATOR.json`
is a byte-identical snapshot of the independently acquired negative input.

Run from this folder with ordinary Python 3:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 verify_sector.py
```

The checker uses only the standard library, rebuilds literal polynomials,
verifies all coefficients and both full exact LDL reconstructions, and
checks the full-dimensional stability bound. It does not import a symbolic
generator, numerical solver, or prior checker. `VERIFY_SECTOR.json` is the
saved receipt; default replay prints its result without modifying the bundle.
Parent independent replay and complete proof review passed
at the stated mathematical scope; the parent receipt is in
`../../principal_combined_quartic/INDEPENDENT_GAP_REPLAY.json`.

The new capability is a strictly stronger executable support certificate
for this open neighborhood: an ordinary norm multiplier succeeds where
every unmultiplied polynomial SOS support fails. General completeness,
computational superiority over all ordinary PC methods, external priority,
and a physical or civilisation-level capability are not established.

Current Astra source pin: `54b1e0d80cf653a82db573a984020865f2ba7794`.
The nine selected governing proof files and four current packets are
byte-identical to the previously read source versions. See
`SOURCE_MANIFEST.json` and `sources/ASTRA_FRESHNESS.json`.
