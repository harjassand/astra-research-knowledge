# Actual selector state as a pre-input programme

## Exact state interface

Consider the state after the original complete local instruments have run and all relevant classical histories have been dephased. Write the normalized preselection state as
\[
 \Phi=\sum_h \pi_h\,|h_A,h_B\rangle\!\langle h_A,h_B|\otimes\phi_h,
 \qquad \pi_h\ge0,\quad \sum_h\pi_h=1,
\]
where each \(\phi_h\) is a normalized state on the actual residual quantum outputs. Any independent, previously shared entanglement \(\eta\) can be appended; it is not selected and is unchanged.

A selector \(e_\Gamma(h)\in[0,1]\), implemented as an external classical accept coin after observing the dephased history, produces
\[
 \tau_\Gamma=\sum_h\pi_h e_\Gamma(h)
 |h_A,h_B\rangle\!\langle h_A,h_B|\otimes\phi_h,
 \qquad p_\Gamma=\operatorname{Tr}\tau_\Gamma,
 \qquad \omega_\Gamma=\tau_\Gamma/p_\Gamma
\]
when \(p_\Gamma>0\). Thus \(0\le\tau_\Gamma\le\Phi\), and the programme resource is \(\omega_\Gamma\otimes\eta\). Its preparation uses the original complete instruments and a global offline selector; it is not an online local operation by either player. For a fixed \(\Gamma\), it is a legitimate pre-input shared state if the game permits arbitrary shared resources. No resource-size or efficient preparation bound follows.

A candidate reconstruction must specify, before the fresh inputs are sampled, local readout instruments \(\{\mathcal R^A_{a|x}\}\) and \(\{\mathcal R^B_{b|y}\}\). They may act on each player's retained local history register, actual residual output, and their share of \(\eta\), but are fixed independently of \(\Gamma\); neither readout can query the predicate or the other player's history. The induced fresh-input table is exactly
\[
 P_\Gamma(a,b|x,y)=
 \operatorname{Tr}\!\left[
  (\mathcal R^A_{a|x}\otimes\mathcal R^B_{b|y})
  (\omega_\Gamma\otimes\eta)\right],
\]
with traces over retained outputs understood. A history-dependent readout is just a block-diagonal local instrument controlled by that player's own \(h_A\) or \(h_B\). This equation is the reconstruction interface; knowing \(\tau_\Gamma\le\Phi\) does not supply the readouts or prove their payoff.

## BG all-live selector

For the literal \(r\)-block BG source, put \(N=k^r\), and let the original full questions \(X,Y\in[k]^r\) be independent uniform strings. Assume the all-live success event on this source is exactly
\[
 e_\Gamma(h)=\mathbf 1\{(X,Y)\in\Gamma\},
\]
as in the designated block strategy, with all live coordinates winning on that event. If \(q_\Gamma=|\Gamma|/N^2>0\), then \(p_\Gamma=q_\Gamma\), and the old-input marginal in the pre-input programme is
\[
 \Pr_{\omega_\Gamma}[X=X_0,Y=Y_0]
 =\frac{\mathbf 1\{(X_0,Y_0)\in\Gamma\}}{|\Gamma|}.
\]
Now draw independent fresh base questions \(x,y\) after preparing the programme. They are independent of the old, selected pair \((X,Y)\). The local readouts must use \(x\) and \(y\) as their actual inputs. Reusing old answer records as if their old questions were these fresh questions is not a reconstruction: the old pair is edge-conditioned, while the new pair is uniform and independent. The selected history may be a useful graph-dependent programme, but whether it supports a high-payoff fixed blind readout is a separate question that needs an explicit construction or bound.

## Why low per-coordinate drift is insufficient

For the deterministic selector above, the old-input posterior has
\[
 D\bigl((X,Y)\mid (X,Y)\in\Gamma\ \|\ \mathrm{Unif}([k]^r)^2\bigr)
 =\ln(1/q_\Gamma),
 \qquad
 \operatorname{TV}\bigl((X,Y)\mid\Gamma,\mathrm{Unif}\bigr)=1-q_\Gamma.
\]
Thus if \(q_\Gamma=k^{-1/5}\) and \(r=k^{1/3}\), the relative-entropy cost per coordinate is \((\ln k)/(5k^{1/3})\to0\), while the total variation tends to one. A small normalized referee drift does not make the old selected questions look like fresh questions, and it does not construct \(\mathcal R^A,\mathcal R^B\).

There is an exact fine-payoff comparison, but it is only \(1-p_\Gamma\) in general. Set \(\kappa_\Gamma=\Phi-\tau_\Gamma\), so \(\kappa_\Gamma\ge0\) and \(\operatorname{Tr}\kappa_\Gamma=1-p_\Gamma\). Then
\[
 \omega_\Gamma-\Phi
 =\left(\frac1{p_\Gamma}-1\right)\tau_\Gamma-\kappa_\Gamma,
 \qquad
 \frac12\|\omega_\Gamma-\Phi\|_1\le1-p_\Gamma.
\]
The same holds after tensoring both states with \(\eta\). Consequently every fixed readout family, fresh-input law, and fine acceptance test \(0\le F_\Gamma\le I\) obey
\[
 |\operatorname{Tr}F_\Gamma(\omega_\Gamma\otimes\eta)
   -\operatorname{Tr}F_\Gamma(\Phi\otimes\eta)|
 \le1-p_\Gamma.
\]
For the BG event itself, the old-history event effect has value \(1\) under \(\omega_\Gamma\) and \(p_\Gamma\) under \(\Phi\), attaining this bound. When \(p_\Gamma\) is a small graph density, the bound is order one, not a useful transfer of fine payoff.

The selector is a classical-history reweighting, not a license to apply a graph-dependent local Lüders filter during the fresh game. Although \(\tau_\Gamma\le\Phi\) implies an operator-domination bound on the prepared states, that order relation neither makes the global selector local nor determines the fresh-input response channels. This note establishes the legal programme format and the missing reconstruction obligation; it proves neither that a successful BG readout exists nor that all such readouts fail.
