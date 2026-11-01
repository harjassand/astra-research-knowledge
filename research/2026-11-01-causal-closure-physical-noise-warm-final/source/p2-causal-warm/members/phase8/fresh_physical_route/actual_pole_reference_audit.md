# Audit of the restricted-input actual-pole dilation comparison

Audited and, with root authorization, repaired: `phase8/root/actual_pole_reference.py`.

## Verdict after the repair

The proposed restricted-input dilation bound is mathematically valid for the stated commuting-Z linear force window. Its Weyl phase has the correct **plus** sign, and its displacement norm correctly includes the retained oscillator and all outgoing loss modes. The comparison reference may depend on the actual unknown scalar pole without becoming a control oracle: it is a mathematical comparison channel, not an implemented calibration operation.

I found and repaired one interface gap. Projecting the force waveforms onto both actual-pole null constraints did not preserve orthogonality of their radiation modes. The reference therefore did not exactly have the intended projective parity CP instrument, although the small dilation distance to that nonorthogonal reference was itself valid. A complex Gram-Schmidt step preserves both null constraints and restores the required orthogonality with negligible additional cost.

The displayed constants remain numerical quadrature evaluations at sampled parameter points. They do not certify a continuous parameter box, a hardware model, or a measured physical error rate.

## 1. Comparing two drives at the same actual pole

Let the actual pole be

\[
 \lambda=\kappa/2+i\Delta.
\]

The implemented force f and mathematical reference force r are propagated through the **same** actual passive oscillator-field scattering map S. Their output displacement vectors, for a data/ancilla eigenvalue branch z, are

\[
 d_{f,z}=\left(\beta_{f,z}(T),\sqrt\kappa\,\beta_{f,z}(t)\right),
\]

and analogously for r, where

\[
 \dot\beta=-\lambda\beta-if,\qquad \beta(0)=0.
\]

The full one-particle inner product is therefore

\[
 \langle d_r,d_f\rangle
 =\beta_r(T)^*\beta_f(T)
  +\kappa\int_0^T\beta_r(t)^*\beta_f(t)dt. \tag{A1}
\]

Omitting the endpoint term would compare only the emitted field and would miss a retained conditional displacement. The root code includes both terms.

Write the conditional dilations in output-displacement form as

\[
 U_{f,z}=e^{i\phi_{f,z}}D(d_{f,z})U_0,
 \qquad U_{r,z}=e^{i\phi_{r,z}}D(d_{r,z})U_0.
\]

The Weyl identity is

\[
 D(d_r)^\dagger D(d_f)
 =e^{+i\operatorname{Im}\langle d_r,d_f\rangle}D(d_f-d_r).
\]

Hence the relative phase is

\[
 \Omega_z=\phi_{f,z}-\phi_{r,z}
       +\operatorname{Im}\langle d_{r,z},d_{f,z}\rangle. \tag{A2}
\]

This verifies the sign used in the implementation.

## 2. Initial-mode and fresh-field displacement components

Pull \(\delta d_z=d_{f,z}-d_{r,z}\) back through the common passive map S. Its initial oscillator component is

\[
 \xi_z=-i\int_0^T e^{(-\kappa/2+i\Delta)t}
                 [f_z(t)-r_z(t)]dt. \tag{A3}
\]

Unitarity of S gives

\[
 \|\delta d_{F,z}\|^2
 =|\delta\beta_z(T)|^2
  +\kappa\int_0^T|\delta\beta_z(t)|^2dt
  -|\xi_z|^2. \tag{A4}
\]

The right side is nonnegative in exact arithmetic. Clamping a tiny negative floating-point value is reasonable for exploratory computation, but a rigorous numerical bound must enclose the full norm and the subtraction with certified errors.

Suppose the actual input oscillator is supported on N≤L, with arbitrary correlations to the data and any additional reference. The oscillator displacement bound is

\[
 \|(D(\xi)-I)\Pi_L\|
 \le |\xi|\,[\sqrt L+\sqrt{L+1}]. \tag{A5}
\]

This follows by integrating the displacement generator. It does not impose a cutoff during the displacement evolution, and it does not replace the physical oscillator by a truncated oscillator.

For an independent homogeneous thermal fresh field of occupation n, use any purification \(|\Sigma\rangle\). Its characteristic function gives

\[
 \|(D(\zeta)-I)|\Sigma\rangle\|^2
 =2\left(1-e^{-(n+1/2)\|\zeta\|^2}\right)
 \le(2n+1)\|\zeta\|^2. \tag{A6}
\]

Combining (A2), (A5), and (A6) by the triangle inequality bounds the relative isometry norm in branch z by

\[
 b_z=|\Omega_z|+|\xi_z|[\sqrt L+\sqrt{L+1}]
       +\sqrt{(2n+1)\|\delta d_{F,z}\|^2}. \tag{A7}
\]

The conditional operations are diagonal in the data/ancilla branch basis. Those branch spaces are orthogonal even when the data, ancilla, oscillator, and an external reference are entangled. The maximum branch bound consequently bounds the entire restricted-input isometry norm. The channel distance is at most

\[
 \|\mathcal N_f-\mathcal N_r\|_{\diamond,N\le L}
 \le 2\max_z b_z. \tag{A8}
\]

This is a complete input-reference bound, not a vacuum-input estimate or a test on one oscillator state.

## 3. Self-phase alignment and the target parity angle

Here the branch variables are \(z=(J_D,Z_A)\), where \(J_D\in\{-2,0,2\}\) and \(Z_A\in\{-1,1\}\). Expand the actual geometric phase as

\[
 \phi_f=s_{f,x}J_D^2+s_{f,y}Z_A^2+\theta_fJ_DZ_A.
\]

Let \(C_{jk}=\langle d_{r,j},d_{f,k}\rangle\). Choosing the mathematical reference self phases as

\[
 s_{r,j}=s_{f,j}+\operatorname{Im}C_{jj}
\]

and its cross phase as \(\pi/4\) makes

\[
 \Omega_z=\left[\theta_f-\pi/4+
 \operatorname{Im}(C_{xy}+C_{yx})\right]J_DZ_A. \tag{A9}
\]

This is exactly the implemented formula. The reference phase is not simply the phase generated by its projected force: it includes a mathematical diagonal adjustment. That is legitimate in a channel comparison because the full difference to the implemented operation, including its target cross phase, is counted in (A9). It is not a claim that an unknown correction is physically applied for free.

The self terms need the declared operational justification. \(Z_A^2=I\) is global, and \(J_D^2=2I+2Z_1Z_2\) is gauge when the measured parity is a code gauge. In the ideal projective parity instrument, a phase depending only on the measured sector also cancels within each outcome branch. One may not drop this term as a free logical phase in a different unmeasured consumer.

## 4. The orthogonality repair

The two actual-pole closure rows are the span of

\[
 e^{i\Delta(t-T/2)}\cosh[\kappa(t-T/2)/2],\qquad
 e^{i\Delta(t-T/2)}\frac{\sinh[\kappa(t-T/2)/2]}{\kappa/2}.
\]

The weighted projection used by the code imposes both exact linear nulls. It does not, by itself, force the reference displacement vectors to be mutually orthogonal.

At the selected point before repair,

\[
 G_{xy}\simeq-1.04062356\times10^{-12},\qquad
 G_{xx}\simeq5.62290195\times10^{-6}.
\]

This produces a nonzero cross-parity Schur entry of approximately \(2.49736\times10^{-12}i\) in the nominal parity instrument. Thus even this tiny correlation obstructed an **exact** projective independent-tag claim.

The authorized repair performs

\[
 q=\frac{G_{xy}}{G_{xx}},\qquad r_y\leftarrow r_y-q r_x,
 \quad \beta_{r,y}\leftarrow\beta_{r,y}-q\beta_{r,x}. \tag{A10}
\]

Both closure equations remain zero because they are linear. The full output displacement Gram matrix now satisfies \(G_{xy}=0\), so homogeneous thermal input supplies the independent modes required by the exact parity CP decomposition. The implementation recomputes the force difference, action, phases, incoming coefficient, and dilation comparison after this step.

## 5. Numerical verification

Independent code is saved as `audit_actual_pole_reference.py`; results are in `actual_pole_reference_audit_results.json`.

For \(\kappa=1.1\times10^{-4}\), \(\Delta=10^{-6}\), L=320, n=0.1:

| Quadrature points | Repaired restricted channel bound |
|---:|---:|
| 8,001 | 1.4177034353 × 10⁻⁸ |
| 16,001 | 1.4176824200 × 10⁻⁸ |
| 32,001 | 1.4176806675 × 10⁻⁸ |

The coefficient q is approximately \(-1.85068772576\times10^{-7}\), with only numerical imaginary residual at this parameter point. The root implementation, rerun after repair, gives \(1.4176824239\times10^{-8}\). Across its sampled two-sided cases, the largest closure residual is \(2.22\times10^{-16}\), and the largest post-repair cross-Gram magnitude is \(7.63\times10^{-22}\).

The much looser time-domain force-action bound is not contradicted. It charges transient excursions in absolute norm. The exact linear dilation comparison retains the cancellation of those excursions and accounts for the small final displacement and small radiated-field difference. This improvement is specific to the linear model and the actual parameter range.

## 6. Record and history semantics

Bound (A8) is obtained before tracing the field. Therefore it also bounds any common subsequent measurement or processing of the retained oscillator and outgoing field, including a classical record, by channel contraction.

However, the **reference interface** still needs its own record scope. Its simple data–retained product channel and parity CP tags were proved with gate radiation traced. If an arbitrary radiation record is retained and used by the receiver, the comparison remains valid but the chosen reference might not have the claimed record-inclusive product/tag structure. These are distinct obligations.

The reference construction is pointwise in the actual scalar pole. To obtain a robust operating regime, bound the quantities uniformly over the admitted parameter domain; a small sampled grid is not that proof. The model also has to state whether the unknown pole is a classical calibration/drift parameter. A quantum operator-valued detuning coherently coupled to another memory is not automatically covered by pointwise scalar calculations.

The exact branch comparison assumes the nominal conserved-Z force window. Additional data/ancilla/control faults inside that window must be included through their own local physical terms or a correctly regrouped channel comparison. They must not be treated as arbitrary switched force histories that nevertheless retain the endpoint formula for fixed branch z.

Finally, N≤L is an analysis input-sector condition. The separate replacement/tail lemma is responsible for comparing the unrestricted physical experiment to that restricted reference. This audit does not turn it into a physical photon cutoff, a cooling step, or a fresh-state assumption. The initial-state dependence appears explicitly in the \(\sqrt L\) term.

## 7. Resource-comparison convention

The four-stage dirty-qubit parity comparator remains strong ordinary prior art. A timing illustration must identify its generator normalization. If each native controlled-Pauli rotation is charged area π/2 in a \(P_1(\mathrm{control})\otimes\mathrm{Pauli}\) coefficient and the sum coefficient cap is 3, each simultaneous two-data stage takes π/3 and each ancilla stage takes π/6. Four stages take π before ramps. Two rise/fall ramps of duration 0.1 per stage, each of half mean height, add 0.1 area-equivalent overhead per stage, giving π+0.4≈3.5416.

If instead the native interaction is normalized as a Pauli–Pauli coupling of area π/4 plus separately charged local rotations, the division of time and exposure changes. No universal coupling conversion follows from comparing this illustrative number with the oscillator pulse duration 1.84. Use the same actual preparation, readout, records, waiting, and receiver in both comparisons, and charge the physical local controls needed by each hardware model.
