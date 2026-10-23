# Phase-twirled FMS source: checked-round update

## Source and one-round payoff

Let
\[
|\psi_\theta\rangle=\frac{|00\rangle+e^{i\theta}\sqrt2\sum_{j=1}^4|jj\rangle}{3},
\qquad
Q_n=\int_0^{2\pi}\frac{d\theta}{2\pi}
\bigl(|\psi_\theta\rangle\langle\psi_\theta|\bigr)^{\otimes n}.
\]
The phase is common across the \(n\) copies. Expanding in the Hamming-weight sectors gives
\[
|\psi_\theta\rangle^{\otimes n}=\sum_{a=0}^n e^{ia\theta}\sqrt{p_a}|\Phi_a\rangle,
\qquad
Q_n=\sum_{a=0}^n p_a|\Phi_a\rangle\langle\Phi_a|,
\quad p_a=\binom na\frac{8^a}{9^n}.
\]
The phase integral dephases only different total weights; it leaves each maximally entangled sector intact. This is not the product of independently phase-twirled one-copy states.

For the original FMS PVMs and uniform law on its 25 question pairs, the one-copy win probability on \(|\psi_\theta\rangle\) is
\[
f(\theta)=1-\frac4{225}(1-\cos\theta).
\]
To check the coefficient, all non-frustrated question pairs retain the perfect strategy's zero pattern. On each of the four bridge/bridge pairs \((T_x,U_y)\), a losing sign pair has overlap
\[
\frac{1}{3}\langle t_x^a|D_\theta|u_y^b\rangle
=\frac{1-e^{i\theta}}{6},\qquad
D_\theta=|\bot\rangle\langle\bot|+\sqrt2e^{i\theta}I_4,
\quad ab=-(-1)^{xy},
\]
using \(\sqrt2\langle c_x|r_y\rangle=(-1)^{xy}\). Its probability is \((1-\cos\theta)/18\); there are two losing sign pairs per bridge/bridge pair, so each such input pair loses with probability \((1-\cos\theta)/9\). Averaging the four pairs among 25 yields the displayed \(f\). In particular \(f(0)=1\), \(0<f(\theta)<1\) for \(\theta\ne0\pmod{2\pi}\), and \(f\) has a unique maximum on the phase circle.

## Accepted checked-round instrument and live state

Use the original fine product PVMs on the first \(t\) copies. Draw their question pairs independently from the original law, accept exactly when all \(t\) rounds win, then discard the checked quantum systems and fine records. This is a trace-decreasing accepted branch of the actual measurement instrument. Conditional on fixed \(\theta\), each checked copy succeeds with average probability \(f(\theta)\); because the state and measurements factor over copies, tracing out the accepted checked copies leaves the live copies unchanged apart from the scalar factor \(f(\theta)^t\). Linearity over the common-phase mixture therefore gives
\[
p_C=Z_t:=\int\frac{d\theta}{2\pi}f(\theta)^t>0,
\qquad
\rho_t^{(m)}=
\frac{\displaystyle\int\frac{d\theta}{2\pi}f(\theta)^t
\bigl(|\psi_\theta\rangle\langle\psi_\theta|\bigr)^{\otimes m}}
{Z_t},
\quad m=n-t.
\]
This is an explicit normalized residual quantum state in the accepted branch, not merely a conditional table or an abstract cq-information bound. The live question tuple remains exactly distributed as the original \(\mu^{\otimes m}\): it was independent of \(\theta\), the checked questions, and checked outcomes before selection, while \(E_C\) depends only on checked questions/outcomes. Thus the live input KL is zero.

One remaining coordinate, measured with the same complete FMS PVMs, wins with probability
\[
R_t=\frac{Z_{t+1}}{Z_t}.
\]
This tends to one. Indeed, under the posterior phase law \(d\nu_t=f^t d\theta/(2\pi Z_t)\), the phase concentrates at the unique maximizer \(\theta=0\). For any neighborhood \(U\) of zero, choose a smaller neighborhood \(V\subset U\); continuity gives \(f\ge1-\eta\) on \(V\), while compactness gives \(f\le1-\gamma\) outside \(U\), with \(0<\eta<\gamma\). Then
\[
\nu_t(U^c)\le\frac{(1-\gamma)^t}{(|V|/2\pi)(1-\eta)^t}\longrightarrow0.
\]
As \(U\) can be arbitrarily small and \(f(0)=1\), \(R_t=\int f\,d\nu_t\to1\). Since the FMS tracial gap is \(\varepsilon_{\rm tr}=1-\omega_{\rm tr}>0\), fix a finite \(t\) with \(R_t>1-\varepsilon_{\rm tr}/2>\omega_{\rm tr}\). Then \(p_C=Z_t\) and \(L_C=-\ln Z_t\) are positive finite constants independent of \(n\); for \(m=n-t\), \(L_C/m\to0\).

## Finite realization and boundary

The phase integral can be replaced exactly by \(K\) equally spaced phases \(\theta_j=2\pi j/K\) for any integer \(K>m+t=n\). The entries of \(f(\theta)^t(|\psi_\theta\rangle\langle\psi_\theta|)^{\otimes m}\) are trigonometric polynomials of degree at most \(m+t\), so the uniform \(K\)-point average equals the integral. The initial \(Q_n\), success probability, and entire conditioned live density then have an exact finite shared-classical-mixture realization; after selection, phase weights are proportional to \(f(\theta_j)^t\).

The accepted branch is a global referee postselection, not a deterministic local channel available on every run. The unconditional initial table is tracial: \(Q_n=\sum_a p_a\Phi_a\Phi_a^*\) is a mixture of maximally entangled sectors, and its complete effects can be compressed within each sector and put in a direct-sum tracial representation. That is a static table representation. The specified original PVM instrument is not block diagonal in the sector label: its bridge measurements mix the flag and magic-square subspaces, so the accepted CP branch can transfer phase coherence from the checked systems into the unmeasured copies. This is why one cannot replace the physical checked-round update by a sectorwise instrument inferred from the initial table alone.

The postselected residual state need not remain tracial; indeed its complete one-coordinate FMS behavior has value \(R_t>\omega_{\rm tr}\). No contradiction follows: the gap applies to complete tracial strategies, whereas the checked-success branch has changed the resource. The claim uses the specified product PVM instrument and its success branch; it is not a generic payoff-only guarantee for other instruments or predicates.
