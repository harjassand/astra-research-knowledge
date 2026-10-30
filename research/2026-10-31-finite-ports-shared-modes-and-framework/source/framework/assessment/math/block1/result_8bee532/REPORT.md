# Exact safety of resonant characteristic triads; cusp geometry at the ROC boundary

The central question remains open: this continuation does not prove QC of P0 on all gradients, and does not resolve the entire exceptional ROC face. It proves an infinite compatible theorem beyond the supplied vanishing-third-moment class, together with a complete description of the sharp quadratic degeneracy that the next proof must handle.

For the checkpoint's globally ROC polynomial

\[
P_0=|w|^4+2|z|^2|w|^2+\operatorname{Re}(\bar z w^2)+\frac3{16}(|z|^2+|w|^2),
\]

**every characteristic-polarized resonant three-wave field satisfies the QC inequality at every background mean, for arbitrary wave amplitudes and phases.** Here an actual map is constructed as

\[
\phi(X)=\sum_{j=1}^3 t_j U(k_j)\sin(k_j\cdot X+\theta_j),\qquad
U(k)\ \text{has complex coordinate }i\bar k^3,
\]

where k3=k1+k2 and k1,k2 are noncollinear. Its gradient, rather than a free distribution of matrices, is the test field. “Characteristic-polarized” means each individual rank-one mode saturates the explicit residual part of the checkpoint's sharp ROC inequality. Arbitrary output polarizations and fields with more modes are outside this result.

This is not a class with vanishing third moments. For example, k1=(1,0), k2=(2,e), k3=(3,e), amplitudes (1,1/16,1/81), and zero phases give

\[
\langle C(D\phi)\rangle=-5e^3(e^2+3)(e^2+8)/648\ne0.
\]

The cubic Schur correlation is also nonzero near e=0. Thus the proof really controls the remaining correlation, rather than eliminating it by symmetry.

The exact construction uses the supplied compatible moment-Schur theorem but adds an actual all-parameter certificate for this resonant family. Direct reconstruction from P0 gives a polynomial 6-by-6 determinant. For normalized frequencies (1,0),(p,e),(p+1,e), choosing the shortest and longest sides gives p≥-1/2 and e²≥1-p². The determinant is certified throughout this domain:

* For p≥0 it has 5,047 positive rational coefficients in even powers of e and nonnegative squared wave amplitudes.
* For -1/2≤p≤0, substitute e²=1-p²+S and p=-t/2. After an e⁶ factor, all 4,616 Bernstein coefficients on 0≤t≤1 are nonnegative, with S and squared amplitudes nonnegative.

The symmetric moment matrix has PSD diagonal Schur blocks from inherited homogeneous QC and global ROC. The certified determinant therefore proves its remaining scalar correlation inequality. Arbitrary phases only multiply both third-moment columns by cos(θ1+θ2-θ3), so the zero-phase certificate controls all phases. No numerical optimization or finite list of passing fields is used to establish this continuum statement.

The other new result is the entire characteristic geometry. Every background with a zero rank-one second variation has the form

\[
z=(-1/4+iq)b^2,\qquad w=-(q/2+i/4)b,\quad |b|=1,
\]

and has exactly one null rank-one line. Its invariant z\bar w²=(1+12q²)/64+iq³/4 makes uniqueness exact. Consequently zero quadratic Schur gap b=0 forces any actual periodic gradient into one rank-one direction and forces its cubic correlation r=0. No separation can arise solely by placing r≠0 on b=0.

This geometry is nevertheless a cusp. At q=0 the acoustic determinant is 9l⁴ in coordinates aligned with the null direction, while generic characteristic backgrounds have second-order angular degeneracy. Distinct characteristic affine lines can have distance only cubic in their angular separation. A uniform coarse angular-coercivity shortcut is therefore invalid.

The almost-parallel resonant family above was the hardest concrete test. Exact elimination yields

\[
a=111/4+O(e^2),\quad b=e^4/56+O(e^6),\quad r=5e^3/54+O(e^5),
\qquad r^2/(ab)=\frac{1400}{80919}e^2+O(e^4)\to0.
\]

These are limits of genuine two-phase resonant fields; substituting e=0 into their frequency set would create extra resonances and give different moments.

The inherited failure most relevant here is the impossibility of a pointwise polynomial heat correction. That ansatz demands positivity at each jet and cannot use a cancellation specific to a complete resonant triangle. This continuation instead preserves exact Fourier resonance and actual gradient compatibility. A naive coefficient shift intended to cover acute triangles produced 2,228 negative coefficients; those were a failed sufficient certificate, not an energy violation. Using the triangle's geometric constraint and a Bernstein basis resolved that obstruction. `shift_3_2.json` preserves the failed test.

The proof and all scope boundaries are in `PROOF.md`. Useful exact replays, from this directory:

```sh
python3 triad_wedge.py
python3 verify_triads.py
python3 verify_geometry.py
python3 triad_symbolic.py
python3 check_direct_field.py
```

The main determinant reconstruction took about 109 seconds locally. Its complete 7,197-term intermediate coefficient list is `triad_wedge_certificate.json`; the shifted orthant and acute-triangle certificates are `shift_1.json` and `acute_test.json`. `triad_symbolic.py` reconstructs the explicit rational Schur formulas and asymptotics. `check_direct_field.py` independently checks the moment convention against the actual energy of a two-phase map with nonzero phases and a nonzero mean; that numerical check is implementation QA, not the continuum proof. An initial NumPy matrix-broadcasting error in that check was corrected; its final replay passed.

The exact geometry receiver, determinant sign conversion, Bernstein receiver, fixed-ratio rational construction, and direct-field check passed. No external review or historical-priority claim is made. Homogeneous QC, P0 admission, and the general compatible moment reduction remain credited to the frozen packet/checkpoint. The new result is the specific compatible all-triangle certificate and the characteristic/cusp classification, not the inherited general reduction.

What remains is control of arbitrary output polarizations and interactions among unrestricted Fourier modes, followed by arbitrary M and admitted Q in the full face. No counterexample was obtained, and no global QC conclusion is asserted.
