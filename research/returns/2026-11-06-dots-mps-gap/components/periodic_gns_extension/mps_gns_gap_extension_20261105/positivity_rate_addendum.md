# Independent addendum: logarithmic-over-volume comparison rate

Date: 2026-11-05. This sharpens only the projection estimate in `independent_periodic_gns_audit.md`. No main proof file was read or modified.

## Verdict

The proposed positivity argument is correct. Under the same assumptions it improves the one-sided bound to

\[
\Delta_{\mathrm{GNS}}\leq\Delta_N^{\mathrm{per}}
+O\!\left(\frac{\log N}{N}\right).
\]

The constant is model dependent. This remains a one-sided rate, not a two-sided rate for convergence of periodic gaps.

## Checked calculation

Let each translated positive interaction term have range r and norm at most M. Take a buffer B of ell sites, with its complement C also longer than r. Write

\[
H_N=H_B+H_C+V,\qquad
V\geq0,\qquad \|V\|\leq B_0:=bM,\qquad b=2(r-1).
\]

Here V is the sum of the b translates crossing either seam. For a translation eigenvector psi of norm one and energy expectation E, each translate has expectation E/N. Thus e_V:=<psi,V psi>=bE/N. The argument also works with the corresponding upper bound if one uses fewer crossing terms.

Set P=1_C tensor P_B, Q=1-P, chi=Q psi, phi=P psi=psi-chi, and q=||chi||^2. The uniform open gap gives

\[
q\leq\frac{\ell E}{gN}.
\]

Because H_C commutes with P and is positive,

\[
\langle\phi,H_C\phi\rangle
\leq\langle\psi,H_C\psi\rangle.
\]

Also H_B phi=0. Consequently

\[
\begin{aligned}
\langle\phi,H_N\phi\rangle
&\leq E-\langle\psi,H_B\psi\rangle
+\langle\phi,V\phi\rangle-\langle\psi,V\psi\rangle\\
&\leq E-2\operatorname{Re}\langle\psi,V\chi\rangle
+\langle\chi,V\chi\rangle\\
&\leq E+2\sqrt{e_V B_0q}+B_0q\\
&\leq E+\frac{E}{N}
\left(2\sqrt{\frac{bB_0\ell}{g}}+\frac{B_0\ell}{g}\right).
\end{aligned}
\]

The penultimate step is Cauchy–Schwarz for the positive form defined by V, followed by <chi,V chi><=B_0 q. No commutation of V with P is assumed. In fact the energy estimate requires only translation covariance of psi's expectations, not the energy-eigenvector equation.

## Transfer and normalization do not lose the improvement

As before phi=O_C Omega_N with uniformly bounded ||O_C|| and phi orthogonal to Omega_N. The centered infinite-volume trial vector has squared norm at least

\[
1-q-K\theta^\ell-K^2\theta^{2\ell},
\]

and energy at most the improved finite energy above plus K' N theta^(ell-2(r-1)). Periodic first gaps have a model-dependent uniform upper bound E_*. Therefore the normalization loss is O(ell/N), rather than a square-root loss.

Choose ell=ceil(a log N), where a>2/|log theta|. Then N theta^(ell-2(r-1))=o(1/N), q=O(log N/N), and the displayed GNS rate follows. Exact orthogonality to the ring ground state is preserved by P, while centering removes the exponentially small infinite-state expectation.

The sole extra ingredient over the earlier seam-norm estimate is positivity of V. It is available for the positive frustration-free parent interaction under discussion and must not be assumed for signed/telescoping parent terms.
