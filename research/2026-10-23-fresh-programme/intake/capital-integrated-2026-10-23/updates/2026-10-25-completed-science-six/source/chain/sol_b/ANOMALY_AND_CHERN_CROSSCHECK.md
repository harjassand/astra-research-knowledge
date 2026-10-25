# Anomaly and Chern crosscheck

Private ASTRA principal crosscheck, Sol B, 25 October 2026.

The electron anomaly currently supplies a conditional test target. The loop-to-Chern identification admits an exact counterexample. These conclusions follow from independent primary-source reading before comparison with the L11, L19, and L20 worker outputs.

## Electron anomaly

The compendium's Theorem 141.1 prints the finite record grades

\[
T_0=1,\quad T_1=309,\quad
T_2=309^2+\text{closure},\quad T_3=0.
\]

Theorem 146.1 describes the grade as the coupling power, while its derivation constructs that grade from the degree of exchange-survival weights. Both are conditional results. The physical comparison is described as a correspondence by name. See the [compendium pages 327–328](https://alexwg.org/publications/ChainTheoryCompendium.pdf#page=327) and [pages 337–338](https://alexwg.org/publications/ChainTheoryCompendium.pdf#page=337).

A physical electron anomaly is the on-shell Pauli form factor \(a_e=F_2(0)\), with the current vertex decomposed as

\[
\Gamma^\mu(p',p)=
F_1(q^2)\gamma^\mu
+\frac{i\sigma^{\mu\nu}q_\nu}{2m}F_2(q^2),
\qquad F_1(0)=1.
\]

The printed finite grades do not themselves define that vertex or specify a numerical conversion to the total \(F_2(0)\). A grade that stops at two does not by itself force a measured third-order coefficient to vanish. For example, if a primitive finite kernel is \(K(z)=az+bz^2\), its repeated-insertion response

\[
\frac1{1-K(z)}
=1+az+(a^2+b)z^2+(a^3+2ab)z^3+\cdots
\]

has a nonzero cubic term. Conversely a model may define the observable to be the primitive polynomial. Which object is physical must be fixed before comparing coefficients. Reparameterizing an unspecified grade variable also changes its coefficients. These are exact identification obstructions; they are not arguments that the standard QED cubic term is uncertain.

L11 and L19 correctly identify a potentially large conditional disagreement with the standard nonzero three-loop coefficient. Their initial sensitivity ratios are not an experimental rejection of the compendium. A valid total-observable test needs the physical vertex map, the lower terms, higher terms, mass-dependent terms, hadronic and electroweak terms, and an alpha input independent of electron magnetic moment. A missing cubic term divided by measurement uncertainty cannot replace that calculation.

Current coefficient versions matter even for this conditional test. [Aoyama et al., arXiv:2412.06473](https://arxiv.org/abs/2412.06473), describes a revised no-fermion-loop tenth-order contribution. [Volkov, arXiv:2404.00649](https://arxiv.org/abs/2404.00649), gives a total tenth-order value. The no-loop subset and the total coefficient must remain distinct, and the older 2018 total cannot silently be treated as the current result. This point affects input provenance rather than the existence of the large conventional cubic term.

**Assessed status:** retain the anomaly as a gated discriminator. It does not presently furnish a source-faithful total numerical rejection. The strongest task is to derive \(F_2(0)\) in the proposed operational bridge and then compare the complete result using independent recoil alpha values.

## Exact reconstruction of the loop counterexample

Consider two smooth, periodic two-band Bloch Hamiltonians on \(T^2\):

\[
H_{\rm top}(x,y)=
\sin x\,\sigma_x+\sin y\,\sigma_y
+(-1+\cos x+\cos y)\sigma_z,
\]

\[
H_{\rm triv}(x,y)=\sin x\,\sigma_x+\cos x\,\sigma_z.
\tag{1}
\]

The first is the standard two-band Chern-insulator construction associated with [Qi, Wu and Zhang](https://arxiv.org/abs/cond-mat/0505308). The second is constant in the second momentum direction.

### Both gaps are exact

For \(H_{\rm top}=\mathbf d\cdot\boldsymbol\sigma\),

\[
|\mathbf d|^2
=1+2(1-\cos x)(1-\cos y)\ge1.
\]

Its eigenvalue gap is therefore at least two, attained on either coordinate-zero cycle. The trivial Hamiltonian has \(|\mathbf d|=1\) everywhere and gap exactly two. Neither model relies on a near-gap-closing numerical limit.

### The whole selected loop is identical

At \(y=0\),

\[
H_{\rm top}(x,0)=H_{\rm triv}(x,0)
\]

for every \(x\). The equality includes the full spectral projector and every measurement on that cycle, not merely one sampled Wilson-loop phase. The occupied-band holonomy around it is \(-1\), or a Berry phase of \(\pi\) modulo \(2\pi\), in both models.

### Their Chern numbers differ exactly

The unit vector \(\hat{\mathbf d}_{\rm top}:T^2\to S^2\) reaches the north pole only at \((x,y)=(0,0)\). At the other three simultaneous zeros of \(\sin x,\sin y\), its third component is negative. The north-pole preimage is regular and has positive orientation, since the two tangent derivatives there have Jacobian determinant \(+1\). Hence its degree is one.

The trivial unit-vector map is independent of \(y\). Its pulled-back two-form vanishes identically, so its degree and Chern number are zero. The occupied band's Chern sign depends on the Berry-connection orientation convention; its magnitude is one in the topological model and zero in the trivial model. The distinction is exact in either convention.

It follows that even the full one-period Hamiltonian and its Berry holonomy do not determine the two-dimensional band Chern number or the Hall conductance. This is stronger than saying that an explanatory bridge is absent: it gives two concrete gapped completions agreeing on the proposed loop data and disagreeing on the claimed physical output.

### General finite loop data remain insufficient without an extension rule

Let \(\Gamma\) be a finite embedded graph of sampled smooth loops in a two-dimensional parameter surface. A disk disjoint from \(\Gamma\) can carry a smooth skyrmion texture of any integer degree, while the Hamiltonian equals \(\sigma_z\) on a neighborhood of \(\Gamma\). Taking \(H=\hat{\mathbf n}\cdot\boldsymbol\sigma\) keeps the band gap exactly two. All loop-restricted projectors and holonomies on \(\Gamma\) remain fixed while the Chern number changes.

This extension argument assumes no independent finite-range, analyticity, curvature-bound, or interpolation rule that determines the unsampled interior. The explicit pair in (1) already uses short-range trigonometric Hamiltonians for the one-period case. The general statement identifies the extra kind of information required; it does not say that a complete two-dimensional connection can never determine its Chern number.

The strengthened construction in `outputs/l20/assessment.md` passes the following additional checks. Its preliminary radial map is constant near the disk center and the identity in the outer collar, so it is smooth and homotopic to the identity relative to that collar. For bubble winding \(\ell\ne0\), \(m=|\ell|\), and a smooth cutoff \(\chi\) which is one near the center and zero in the collar, put \(a(r)=\chi(r)r^{-m}\). The stereographic bubble has components

\[
s_x+i s_y=\frac{2a(r)e^{i\ell\phi}}{1+a(r)^2},\qquad
s_z=\frac{1-a(r)^2}{1+a(r)^2}.
\]

Near the center these become

\[
s_x+i s_y=\frac{2(x+i\operatorname{sgn}(\ell)y)^m}
{1+(x^2+y^2)^m},\qquad
s_z=\frac{(x^2+y^2)^m-1}{(x^2+y^2)^m+1},
\]

which proves Cartesian smoothness. The bubble is constant in a collar, permitting smooth gluing to the flattened background. Its degree is \(-\ell\): writing \(f=2\arctan a\), the integral is \((\ell/2)[-\cos f]_0^R=-\ell\). Thus \(\ell=-j\) shifts the degree by any prescribed \(j\). A constant target rotation in \(SO(3)\) preserves that sign. With the convention \(A=i\langle u_-|du_-\rangle\), the lower-band curvature is \(\tfrac12 n\cdot(\partial_xn\times\partial_yn)\,dx\wedge dy\), so its Chern number equals this degree.

The phrase "gap exactly two" concerns spectrally flattened representatives. If the prescribed graph data also include physical energies, begin with \(H_0=\epsilon_0I+|d_0|n_0\cdot\sigma\) and define \(H_j=\epsilon_0I+|d_0|n_j\cdot\sigma\). This preserves the original energies and gap pointwise on the whole torus, as well as the entire Hamiltonian near the graph. The integer shift remains unchanged. No existence claim is needed beyond an initial smooth gapped extension; if none exists, the graph data have no band-Chern realization in the first place.

## Relation to the compendium claim

The compendium's instrument I.51 already marks its Chern derivation as awaited. I.52 constructs a fan-sum statistic and explicitly leaves the identification of the Chern number with the sum over the periodic sink's faces open. See [pages 739–741](https://alexwg.org/publications/ChainTheoryCompendium.pdf#page=739).

The counterexample therefore refutes a premature promotion of one-period holonomy to a physical Chern or Hall invariant. It does not refute the finite winding or fan-sum arithmetic at its stated definitions. A sufficient completion must provide a gapped two-dimensional projector family, its connection or overlap links over the whole parameter surface, a controlled branch/admissibility rule, and the correspondence between the resulting Chern number and the model's fan sum. The [Fukui–Hatsugai–Suzuki construction](https://arxiv.org/abs/cond-mat/0503172) gives a precise lattice comparator once those data exist.

## Reproduction

The existing L20 numerical witness was read after the independent argument and then executed:

`outputs/l20/chern_loop_underdetermination.py`

It reports exact-slice equality to numerical precision, minimum direct gaps two and two, loop phases \(\pi\) and \(\pi\), and FHS Chern estimates \(-1\) and \(0\) in its convention. This independently checked analytic proof supplies the result; the grid calculation is a useful replay, not the justification of quantization.

## Scientific recommendation

Retain the exact scalar candidate as a mathematical model output and an explicitly conjectured physical identification. Retain the Lorentz isometry construction at its geometric scope. The strongest surviving photon bridge is the explicit Maxwell completion in the companion assessment: it supplies massless transverse propagation and conserved-current scattering, while exposing the remaining kinetic coefficient through \(\alpha=r/(4\pi\kappa)\).

The next consequential result should derive that coefficient and a normalized current from the finite operations. It can then produce a total independent observable such as the Pauli form factor. The loop countermodel should be retained as a permanent control against equating a finite winding statistic with a two-dimensional topological response. At present, neither an internally checked count nor those correspondences establish a new electromagnetic theory or a demonstrated physical capability.
