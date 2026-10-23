# Bounded source boundary: binary-mixture SLD metric

24 October 2026. This note compares the proposed binary-mixture metric with Temme et al.'s quantum χ² contraction and Wan–Lasenby QFI flow. It does not audit the opening's source-term algebra or prove a risk-only bound.

## Exact overlap with Temme et al.

For $R=(\rho_0+\rho_1)/2$, $Q=(\rho_0-\rho_1)/2$, and $Q=(RA+AR)/2$,

\[
C=\operatorname{Tr}(QA)=\left\langle Q,\,2(L_R+R_R)^{-1}(Q)\right\rangle.
\]

This is exactly Temme et al.'s Bures quantum χ² divergence $\chi^2_{\rm Bures}(R+Q,R)$, with their Bures inverse $\Omega_R^{\rm Bures}=2(L_R+R_R)^{-1}$. It is also $\chi^2_{\rm Bures}(R-Q,R)$. Their channel-monotonicity theorem therefore gives

\[
C(T\rho_0,T\rho_1)\le C(\rho_0,\rho_1)
\]

for every common CPTP map $T$, including nonunital reset/detector channels represented with their records in the output. Their trace-distance comparison gives $\tfrac12\|\rho_0-\rho_1\|_1=\|Q\|_1\le\sqrt C$. The mixture reference is support-safe: $\operatorname{supp}(\rho_i)\subseteq\operatorname{supp}(R)$. See Theorem 4 and Lemma 5 in the current [arXiv:1005.2358v3](https://arxiv.org/abs/1005.2358); this audit does not rely on propositions removed from older versions.

The metric also has an exact finite-pair dissipation identity under a common GKSL generator. Differentiating its variational form at the optimizer $A$, and applying the Lindblad product rule, gives

\[
\dot C=-\operatorname{Tr}\!\left(R\,\Gamma(A)\right),\qquad
\Gamma(A)=\sum_j[L_j,A]^\dagger[L_j,A]\succeq0,
\]

with the Hamiltonian derivation canceling. This identity holds without detailed balance or a faithful stationary state and permits a time-dependent common generator. For the full trace-preserving system with the absorbing jump $J=\sqrt\gamma\,|\mathrm{dead}\rangle\langle e|$, the jump contributes the positive term $\operatorname{Tr}(R[J,A]^\dagger[J,A])$. Local reset channels likewise cannot increase $C$. This is an established metric contraction / direct carré-du-champ calculation for the common evolution; it is not yet a compensation bound for parameter-dependent source terms.

## Boundary against the risk claim

When the two worlds have different signal strengths, the metric derivative acquires the opening's source term $S$. Temme's common-channel contraction controls only the nonpositive common part; it does not bound the time integral of $S$ by the actual probability mass in the dead branch. Nor does positivity of the loss contribution $\operatorname{Tr}(R[J,A]^\dagger[J,A])$ by itself identify it with, or upper-bound it by, $\gamma\operatorname{Tr}(P_eR)$ in the needed direction. The open step remains a dynamical compensator or another argument that ties the signal source to actual terminal-loss risk. Metric monotonicity alone is not a risk theorem.

## Wan–Lasenby: local limit, no risk ledger

Wan and Lasenby's QFI-flow treats a smooth scalar parameter in a Markovian master equation, with time-dependent Hamiltonians/noise and adaptive controls. For nearby worlds $g\pm\delta g/2$, this binary metric has the local expansion

\[
C=\frac{(\delta g)^2}{4}\,F_Q(g)+o((\delta g)^2),
\]

so the QFI flow is the infinitesimal-parameter counterpart of the finite-pair Bures-χ² ledger. It is not an identity for finite $\delta g$, though one may seek a separate integration along parameter space. In either form, QFI/metric sensitivity does not impose a cost for the absorbing event. Even if the dead flag and timestamp are included as accessible registers, a separate risk-to-source estimate is required. See the SLD-flow and adaptive-control sections of [Wan and Lasenby, arXiv:2108.11390](https://arxiv.org/abs/2108.11390), published as [Phys. Rev. Research 4, 033092 (2022)](https://doi.org/10.1103/PhysRevResearch.4.033092).

## Bounded conclusion

The finite-parameter binary SLD/Bures-χ² metric and its contraction under common CPTP resets are established tools; this is the strongest direct overlap. Its common-generator dissipation can be written as an exact Σ-commutator/carré-du-champ ledger even for an absorbing full-state dilation. Neither Temme's contraction result nor Wan–Lasenby's local QFI flow provides the missing bound of the different-world source (S) by actual terminal death. The proposed compensated source-to-risk step remains the substantive gate. This is a bounded scope finding, not a novelty or correctness determination.
