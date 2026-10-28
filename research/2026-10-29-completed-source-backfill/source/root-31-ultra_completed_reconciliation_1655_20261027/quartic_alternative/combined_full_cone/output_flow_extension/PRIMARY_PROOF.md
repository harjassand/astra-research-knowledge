# All constant output-coupled pure-target flows are excluded in the stated class

This completes the wider pure-target flow test. The parent's independent
literal replay and the complete symmetry/parameter argument are accepted
internally at the scope stated here. It is not a non-QC theorem.

## Target and theorem

Use \(u=a^2+c^2,v=b^2+d^2,w=ab+cd,q=ad-bc\), and the invariant basis
\((u^2,v^2,uv,w^2,uw,vw,qu,qv,qw)\). The exactly symmetric target is

\[
p=\left(\frac{55220381}{10^{10}},\frac{55220381}{10^{10}},
\frac{114430029}{625000000},-\frac{801761987}{5000000000},0,0,
\frac{118849817}{4000000000},-\frac{118849817}{4000000000},0\right),
\qquad F=p\cdot\mathcal B.                              \tag{1}
\]

It differs from the preceding strict-ROC target only by
\(1/20000000000\) in each of two coefficients, inside its proved
\(1/52800000\) coefficient box. Thus that common-cone obstruction still
applies. `SYMMETRIC_TARGET.json` separately supplies an exact literal
8 by 8 ROC Gram with positive shift \(1/400000\).

**Theorem.** There are no constant real output matrices \(C^{jk}\),
symmetric in the spatial indices, no \(\gamma\geq0\), no closed
homogeneous-quadratic matrix-space two-form \(\omega\), and no PSD matrix
\(R\) on the 24 features \(Z=(A_i z_j)\), satisfying

\[
\sum_{j,k=1}^2D^2(F-\gamma q^2)(A)[B_j,C^{jk}B_k]
                   +\omega_A(B_1,B_2)=Z^TRZ              \tag{2}
\]

for all compatible jets, when the principal symbol is uniformly coercive:

\[
\operatorname{sym}\!\left(\sum_{j,k}C^{jk}\xi_j\xi_k\right)
                     \succeq c|\xi|^2I\quad(c>0).        \tag{3}
\]

No output self-adjointness is assumed. The compatible coordinates are
\(z=(v^1_{xx},v^1_{xy},v^1_{yy},v^2_{xx},v^2_{xy},v^2_{yy})\), with
\(B_1=(z_0,z_1,z_3,z_4)\), \(B_2=(z_1,z_2,z_4,z_5)\).
The theorem concerns this global polynomial SOS representation, including
all closed quadratic corrections. It does not cover non-SOS nonnegative
densities, norm-multiplied heat certificates, other correction classes, or
the weaker assumption of positive-real-part eigenvalues alone.

## 1. Exact target symmetries reduce the whole operator class

Both \(F\) and \(q^2\) are invariant under left output rotations, column
exchange \(S\), and the paired reflection \(A\mapsto DAD\),
\(D=\operatorname{diag}(1,-1)\). These are checked literally in the replay.
For a hypothetical (2), conjugate by these actual symmetries and average.
The energy \(F-\gamma q^2\) stays fixed. Compatible jets transform linearly,
the two-form correction transforms by its oriented pullback and remains
closed quadratic, and Grams transform by congruence and stay PSD.
Coercivity (3) survives orthogonal conjugation and averaging.

Average first over output quarter turns. A real output block then lies in
\(\operatorname{span}(I,J)\), where
\(J=\left(\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right)\). Write
\(C^{jk}=A_{jk}I+B_{jk}J\), with real symmetric spatial matrices \(A,B\).
Column exchange imposes \(A=SAS,B=SBS\); paired reflection imposes
\(A=DAD,B=-DBD\). The simultaneous fixed space is exactly

\[
A=aI,\qquad B=b\begin{pmatrix}0&1\\1&0\end{pmatrix}.     \tag{4}
\]

The replay checks this projection on every one of the 12 real operator
coefficient basis vectors. Its scalar coefficient is
\(a=[\operatorname{tr}C^{11}+\operatorname{tr}C^{22}]/4>0\), by (3).
Divide (2) by \(a\). It suffices to exclude every real \(b\) for

\[
v_t=\Delta v+2bJ\partial_{12}v.                          \tag{5}
\]

This is an admissible strongly parabolic flow for every real \(b\); its
symmetric principal symbol is \(|\xi|^2I\). The reduction is the
established symmetry argument previously proved for F16, now applied to
the actual symmetries of the new rational target. It is not a new generic
operator-averaging theorem.

Integration by parts in the flow (5) gives the normalized dissipation

\[
E_IH+bE_JH,\qquad
E_IH=D^2H[B_1,B_1]+D^2H[B_2,B_2],\quad
E_JH=D^2H[B_1,JB_2]+D^2H[B_2,JB_1].                    \tag{6}
\]

The two mixed terms arise by averaging integration by parts in the two
spatial directions. Their difference integrates to zero. The local maps
in (6) are rebuilt from the literal Hessians in both independent replays.

## 2. A rigorous compact gamma range

Any identity (2), after reduction, would make \(H=F-\gamma q^2\) QC by
the standard heat-flow/null-Lagrangian argument. For completeness, (5)
has the complex scalar form \(w_t=\Delta w+2\mathrm i b\partial_{12}w\).
Its kernel has modulus

\[
\frac1{4\pi t\sqrt{1+b^2}}
 \exp\left(-\frac{|x|^2}{4t(1+b^2)}\right).
\]

Consequently, for each fixed \(b\), the usual \(L^1\)-to-\(L^p\) gradient
decay holds, with constants depending on \(b\). Relative quartic energy
therefore tends to zero. A closed quadratic two-form is exact by
\(\omega=\tfrac14d(\iota_A\omega)\); its pullback has zero integral.
Integrating (2) and using decay proves QC on compactly supported smooth
perturbations, then on \(W^{1,4}_0\) by density. No uniform decay constant
in \(b\) is asserted or needed.

QC implies ROC. The following one exact rational rank-one pair therefore
bounds any permissible determinant-square removal:

\[
A_0=\begin{pmatrix}-9338/15625&640641/10^6\\34499/10^5&67349/200000\end{pmatrix},
\qquad H_0=e_1\otimes(1,515437/10^6).
\]

The replay verifies

\[
D^2F(A_0)[H_0,H_0]
=\frac{63436807791995668485673403369}{5000000000000000000000000000000000},
\qquad\operatorname{cof}A_0:H_0=\frac{15892438937}{10^{11}}\ne0.
\]

Since \(D^2(q^2)(A_0)[H_0,H_0]=2(\operatorname{cof}A_0:H_0)^2\), ROC forces

\[
0\leq\gamma\leq
\frac{63436807791995668485673403369}{252569615366273689969000000000000}
\leq G:=\frac{25117}{10^8}.                             \tag{7}
\]

This is one acquired rational witness, not a claimed sharp gamma optimum.
The old coordinate plane-wave bound was about 0.127; the improved (7)
reduces the interval by more than two orders of magnitude, with all
rounding resolved by exact evaluation.

## 3. One exact affine dual family covers every b and gamma

`EXACT_FLOW_FAMILY.json` supplies rational 210-vectors \(L_0,L_1\). Their
SHA256 is `1791139d3cde668f22854406f99e62189d2dc39c7f327cd7df4a59073a9fa15e`.
Coefficients are ordered by lexicographic pairs \(A_iA_j\), \(i\leq j\),
then compatible-jet pairs \(z_kz_l\), \(k\leq l\).

For \(t=\gamma/G\in[0,1]\), put \(L_\gamma=L_0+tL_1\). The exact facts are:

1. Both \(L_0\) and \(L_1\) annihilate every closed quadratic form pullback.
   Stored 16-entry vectors \(\eta_0,\eta_1\) give the literal identities
   \(L_i(\omega_A(B_1,B_2))=\eta_i\cdot\operatorname{coeff}(d\omega)\)
   on every one of the 60 coefficient basis forms.
2. The 24 by 24 moment matrices at \(L_0\) and \(L_0+L_1\) are positive
   definite, with 48 exact positive LDL pivots and full reconstructions.
   Convex interpolation makes \(L_\gamma\) nonnegative on every admitted
   SOS Gram for every \(t\in[0,1]\).
3. The three identities

\[
L_0(E_JF)=0,\qquad L_1(E_JF)=G L_0(E_Jq^2),\qquad L_1(E_Jq^2)=0
\]

   hold exactly. Thus \(L_\gamma(E_J(F-\gamma q^2))=0\) identically in
   \(\gamma\). The unbounded real coefficient \(b\) disappears entirely.
4. The polynomial \(L_\gamma(E_I(F-\gamma q^2))\) has degree at most two
   in \(t\). All three exact Bernstein coefficients on \([0,1]\) are
   strictly negative. They are stored explicitly in the certificate.

Applying \(L_\gamma\) to any reduced (2) therefore gives a negative left
side and a nonnegative right side, a contradiction. Equation (7) covers
every possible \(\gamma\geq0\), and Section 1 covers every operator (3).
This proves the theorem with no parameter-grid inference.

## 4. Replay, prior construction, costs, and limits

`verify_flow.py` is read only by default. It uses standard-library exact
fractions and the local `literal_polynomials.py` prefix snapshot of the
frozen preceding helper. Thus the local replay has no outside-file
dependency. It imports
no producer, numerical interface, solver or symbolic package. It rebuilds
the target, both dissipations, all 120 exterior-basis checks, both moment
endpoints, the gamma witness, the parameter identities, negative Bernstein
coefficients, the 12-dimensional operator projection, target symmetries,
and the exact shifted ROC certificate. Its saved final computation took
0.1274 seconds after imports. Pivot integers have at most 402 bits.

The parent's separate `independent_flow.py` uses SymPy QQ with no author
code, maps, or verifiers. It passed in 0.328 seconds, and the parent
accepted the complete pure-target theorem with the explicit coercivity
assumption (3). Its receipt is preserved under `external_inputs/`.

The affine parameter-dual method is established by the preceding
`principal_coupled_flow/PROOF.md`; it was not invented again here. New
content is its exact application to this previously uncovered strict ROC
target, including the acquired tight gamma gate. The numerical family
search took 0.071 seconds and rational reconstruction 0.212 seconds at one
thread. The 93 linear equations had rank 93; denominator \(10^{10}\) and a
\(1/100000\) Gaussian interior perturbation passed on the first attempt.
These are saved run timings, not complete research effort or a universal
runtime guarantee.

A constant common dual annihilating the entire mixed energy map did not
yield a negative result. A pure-target constant dual valid for all gamma
also did not. Those numerical failures are retained without a no-go
interpretation; the exact affine family above supplies the conclusion.

Crucially, the symmetry reduction keeps \(F-\gamma q^2\) fixed. In a
different proposed decomposition \(F=G+H\) with an unknown energy \(H\)
and unknown general operator, averaging changes both factors of the
bilinear map \(E_C(H)\). One cannot replace that average by
\(E_{\mathrm{avg}C}(\mathrm{avg}H)\). No such arbitrary combined-class
obstruction is claimed. Nor does the theorem exclude norm-multiplied
heat densities, more general nonnegative corrected densities, nonlinear
flows, rational/nonpolynomial minor supports, or QC itself. Historical
priority and the general nine-coefficient ROC/QC implication remain open.
