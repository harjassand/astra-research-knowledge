# Actual Markov-noise Duhamel audit

## Result and assumptions

Under the stated assumptions, the proposed noise comparison is valid. Take the actual Heisenberg generator to be the ideal Hamiltonian generator plus onsite dissipators,
\[
\mathcal L_t=\mathcal L_{H,t}+\mathcal D_t,\qquad
\mathcal D_t=\sum_x\mathcal D_{x,t},
\]
where each jump \(L_{xa}(t)\) is supported on cell \(x\) and
\[
\sup_{x,t}\sum_a\|L_{xa}(t)\|^2\le\kappa.
\]
The ideal Hamiltonian is time dependent, closed, and nearest neighbor, with each bond term bounded by \(J\); put \(g=J/\hbar\). Use the supplied ideal Lieb–Robinson commutator estimate
\[
\|[\tau_H(T,s)(P_i),L_{xa}(s)]\|
\le 2\|P_i\|\,\|L_{xa}(s)\|F_{|x-i|}(6g(T-s)),
\]
and its one-dimensional sum \(\sum_x F_{|x-i|}(z)=(1+2z)e^z\). Here \(P_i\) is an onsite projection, so \(\|P_i\|=1\).

## Time ordering and Duhamel bound

Write \(\Lambda_{t,s}\) and \(\tau_{H;t,s}\) for the actual and ideal Heisenberg propagators, respectively, taking observables at \(t\) back to \(s\). Their composition order gives the interpolation
\[
F(s)=\Lambda_{s,0}\circ\tau_{H;T,s}.
\]
It has endpoints \(F(0)=\tau_{H;T,0}\) and \(F(T)=\Lambda_{T,0}\). Differentiating the upper endpoint of \(\Lambda_{s,0}\) and the lower endpoint of \(\tau_{H;T,s}\) gives
\[
\Lambda_{T,0}(O)-\tau_{H;T,0}(O)
=\int_0^T\Lambda_{s,0}\!\left(\mathcal D_s\bigl(\tau_{H;T,s}(O)\bigr)\right)\,ds.
\]
This ordering is useful: the noisy Heisenberg propagator is the outer map, while the commutator is evaluated on the ideal future-evolved observable. Since \(\Lambda_{s,0}\) is unital completely positive, it contracts operator norm.

For a self-adjoint \(O\), each jump dissipator obeys
\[
\mathcal D_L(O)
=\tfrac12\left(L^\dagger[O,L]+[L^\dagger,O]L\right),\qquad
\|\mathcal D_L(O)\|\le\|L\|\,\|[O,L]\|.
\]
The norm equality \(\|[L^\dagger,O]\|=\|[O,L]\|\) uses \(O=O^\dagger\). The ideal image of \(P_i\) remains a projection, so this applies throughout the Duhamel integral. The LR estimate then yields, cell by cell,
\[
\|\mathcal D_{x,s}(\tau_H(T,s)(P_i))\|
\le 2\kappa F_{|x-i|}(6g(T-s)).
\]
Summing over all cells and integrating gives the system-size-independent bound
\[
\|\Lambda_{T,0}(P_i)-\tau_{H;T,0}(P_i)\|
\le \nu(T):=2\kappa\int_0^T(1+12gt)e^{6gt}\,dt.
\]
For \(g>0\),
\[
\nu(T)=\frac{\kappa}{3g}\left((12gT-1)e^{6gT}+1\right),
\]
with continuous limit \(\nu(T)=2\kappa T\) at \(g=0\). Since the integrand is increasing for \(g\ge0\),
\[
\nu(T)\le 2\kappa T(1+12gT)e^{6gT}.
\]
Both \(gT\) and \(\kappa T\) are dimensionless: \(g\) has units of inverse time and \(\|L\|^2,\kappa\) have units of inverse time. Because both evolved observables are effects, their difference also has norm at most one; one may replace \(\nu\) by \(\min\{1,\nu\}\).

## Transfer to a finite-depth construction

Suppose a constructed ideal observable \(\Phi_C(P_i)\) has a separately established locality error
\[
\|\Phi_C(P_i)-\tau_{H;T,0}(P_i)\|\le\eta_{\rm LR}.
\]
For the same input density \(\rho\) and reference projection \(P_{\rm ref}\), define
\[
e_{\rm actual}=\operatorname{Tr}\rho\,P_{\rm ref}(I-\Lambda_{T,0}(P_i))P_{\rm ref},\quad
e_C=\operatorname{Tr}\rho\,P_{\rm ref}(I-\Phi_C(P_i))P_{\rm ref}.
\]
Then
\[
e_C\le e_{\rm actual}+\eta_{\rm LR}+\min\{1,\nu(T)\},
\]
by the triangle inequality and \(\|P_{\rm ref}XP_{\rm ref}\|\le\|X\|\). This is only an observable-error transfer bound. The noisy Markov propagator is not assigned an automorphism/QCA index by this argument.

## Scope checks

The Duhamel bound depends on the actual generator having the same Hamiltonian part as the comparison ideal evolution, with all deviations represented by the specified onsite dissipators. An additional Hamiltonian perturbation, a jump with support beyond one cell, or a per-cell rate bound that grows with system size needs its own term or a different estimate. The bound uses no factorization between rails and no finite-size factor; it assumes the stated uniform LR estimate and the onsite support/rate bounds.
