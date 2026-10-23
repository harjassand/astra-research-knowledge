# Independent check of the weak-return full-output theorem

24 October 2026. Bounded audit of WEAK_RETURN_FULL_OUTPUT_RISK_THEOREM.txt. I checked the literal weak-drive subclass and its complete output (live state, first-death time record, and retained independent references). This does not extend the theorem to strong controls or to arbitrary controllers.

## Generator and second-order elimination

In the stated rotating frame, the fast coherence block for an input \(p_{bb}\) has the equations
\[
\dot x_{eb}= -[\lambda+i(\Delta-\omega)]x_{eb}-igx_{ab}-ifp_{bb},\qquad
\dot x_{ab}=-(2\kappa-i\omega)x_{ab}-igx_{eb},
\]
where \(\lambda=(\gamma+\kappa)/2\). Solving the stationary fast equations gives
\[
x_{eb}=-if\chi_g p_{bb},\quad
x_{ab}=-\frac{ig}{2\kappa-i\omega}x_{eb},\quad
\chi_g=\left[\lambda+i(\Delta-\omega)+\frac{g^2}{2\kappa-i\omega}\right]^{-1}.
\]
The same block for \(p_{br}\) replaces \(p_{bb}\) by \(p_{br}\), since \(r\) and \(b\) carry the same \(Z=-1\), and gives the same susceptibility. Substituting into the slow flux equations yields
\[
p_{bb}'=-2|f|^2\operatorname{Re}\chi_g\,p_{bb},\qquad
p_{br}'=-|f|^2\chi_g p_{br},\qquad p_{rr}'=0.
\]
Thus \(r_g=2|f|^2\operatorname{Re}\chi_g\), \(h_g=|f|^2\operatorname{Im}\chi_g\) give the amplitude-damping plus phase evolution in (5); I find no additional returned-\(b\) dephasing at this order. The signs agree with the rotating-frame Hamiltonian in (2).

The second-order jump identity also checks. From \(L_0q_2=p'-L_1q_1\), partial trace over the physical system gives
\[
-\gamma\,\operatorname{Tr}_{\rm sys}(P_eq_2)
=\operatorname{Tr}_{\rm sys}(p')
=-r_g\,\operatorname{Tr}_{\rm sys}(P_bp).
\]
The commutator \(L_1q_1\) has zero physical partial trace. Off-diagonal \(b/r\) terms contribute no \(e\)-population. This gives the operator-valued death map \(\gamma Jq_2J^\dagger=r_gJ_bpJ_b^\dagger\), not merely equality of total death probabilities.

The residual in (8) follows by matching orders \(\eta^{-1}\), \(1\), and the remaining \(\eta,\eta^2\) terms. The displayed bounds for \(q_1'\), \(L_1q_2\), and \(q_2'\) follow by differentiating (3) and using the extended superoperator norm of \(R\), including its \(Q\) projection. The endpoint condition \(f(0)=f(S)=0\) removes both dressings. I find no sign or missing fast-block recycling term.

## Death-time record and effective information bound

The exact match of the lifted jump density to the effective record density makes the augmented residual live-only. Propagation of each Hermitian live residual through the physical future evolution, including later death timestamps and the terminal live state, is a CPTP instrument. Its trace-norm contraction therefore supports the L1-in-time record bound in (9), in addition to the final live-state error. This does not justify transferring local QFI by continuity; the theorem correctly does not do so.

For the effective constant-exposure channel, write \(q=1-e^{-r\tau}\). The no-death Kraus amplitude on \(b\) is \(e^{-(r/2+ih)\tau}\); the death-time amplitude is \(\sqrt r\,e^{-(r/2+ih)t}e^{i\theta(g,t)}\). With \(\theta'=h't+c\), choosing \(c=e^{-r\tau}h'\tau/q\) cancels \(K_0^\dagger K_0'+\int K_t^\dagger K_t'dt\). The derivative cost is
\[
\beta=\left[\frac{q r'^2}{4r^2}+\frac{e^{-r\tau}\tau^2h'^2}{q}\right]P_b.
\]
The second term is bounded using \(e^{-r\tau}\tau^2/q^2\le r^{-2}\). The Kraus phase is an allowed gauge only because the timestamp is a classical record and no coherent cross-time loss-environment output is available; that boundary is stated in the theorem.

Finally,
\[
\operatorname{Re}\chi_g=\left(\lambda+\frac{g^2(2\kappa)}{|2\kappa-i\omega|^2}\right)|\chi_g|^2,\qquad
\chi_g'=-\frac{2g\chi_g^2}{2\kappa-i\omega},
\]
so \(|\chi_g'|/\operatorname{Re}\chi_g\le[\kappa(\gamma+\kappa)]^{-1/2}\). This gives the coefficient in (13), and the stepwise death compensator yields (14) for the effective accessible instrument, including classical timestamps and adaptive operations between stages. The full-output physical consequence follows at the stated finite-parameter, uniform-along-the-path risk scope.

## Audit result and boundary

I found no generator-sign error, missing second-order \(b\)-dephasing, or lost death-time statistic in the stated weak-drive theorem. The result is consequential for that fixed-carrier, weak-envelope, finite-stage family: complete diagonal output and retained classical death timing do not preserve a fixed coupling distinction when total actual death and accumulated approximation/cleanup error both vanish. Its uniform compact-\(g\), fixed-hardware constants and summed stage errors are essential.

This does not answer the original all-controller question. It does not analyze strong \(a/e\) controls, moving both logical branches, active finite-rate correction during sensing, or measurement feedback inside a weak stage. No physical implementation or advantage claim follows from this audit.
