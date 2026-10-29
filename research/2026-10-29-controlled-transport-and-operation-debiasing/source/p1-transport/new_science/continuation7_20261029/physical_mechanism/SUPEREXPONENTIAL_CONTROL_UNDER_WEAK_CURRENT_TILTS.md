# Deterministic and Poisson phase controls under weak current tilts

29 October 2026. Followup to `COLLECTIVE_PATHS_FROM_ACTUAL_PHASE_CONTROLS.md`. This is the requested stronger ordinary comparison at large-deviation speed. It proves a current/compensator replacement lemma; it does not independently assert a complete density/current large-deviation principle.

## 1. Result

The deterministic gauge construction continues to work under every fixed bounded smooth weak current tilt. If the physical primitive size of the zero-mean drive is \(H_N\), and one exchange changes at most \(D_N\) current summands, then

\[
H_ND_N\to0 \tag{1}
\]

makes its integrated modulation residual **superexponentially small at speed \(N\)**, uniformly over every initial visible law and every frozen hidden parameter/initial phase allowed by the model. For global pi cycles \(H_N=h_N/2\); for uniform continuous rotation the two-drive gauge has effective primitive at most \(3/\Omega_N\).

In particular, fixed finite-range unknown context amplitudes admit arbitrarily slow \(\Omega_N\to\infty\), or arbitrarily slow \(h_N\to0\), even for this rare-history receiving lemma. The deterministic controller is therefore a strong conventional supplier for a smooth-current action argument on that physical subclass, not just a law-of-large-numbers fallback.

Independent local Poisson pi kicks give the same superexponential replacement for every \(\gamma_N\to\infty\), without the context-influence restriction. Initial signs may be deterministic and retained. Its stronger nonlocal scope is supplied by actual independent local actuation.

Weak tilted laws below are mathematical changes of measure used in an action proof. No new physical directional-clock actuator is assumed merely because a tilted law can be defined.

## 2. Exact tilted process and source class

Use the ring, canonical uniform \(\pi_N\), exchange \(\eta\mapsto\eta^i\), and native symmetric rates from the companion note. Write

\[
r_i(u,\eta)=c[1+q_N(u)b_i(\eta)],\quad
0<r_i\le c_*,\quad r_i(u,\eta^i)=r_i(u,\eta). \tag{2}
\]

Continuous rotation permits the corresponding sum of cosine and sine drives. The argument only uses positivity, boundedness, and exchange symmetry of these instantaneous native rates.

Let \(E_i(t)\) be a prescribed field on macroscopic time \(0\le t\le T\), with \(|E_i(t)|\le E_*\). It may be the evaluation of any fixed smooth space-time field at the bonds. Put

\[
\xi_i(u,\eta)=\frac{E_i(u/N^2)}{N}(\eta_i-\eta_{i+1}),
\qquad \xi_i(u,\eta^i)=-\xi_i(u,\eta). \tag{3}
\]

The tilted generator is

\[
L_u^Ef(\eta)=\sum_i r_i(u,\eta)e^{\xi_i(u,\eta)}
                         [f(\eta^i)-f(\eta)]. \tag{4}
\]

It need not preserve \(\pi_N\). The proof below explicitly pays for this; it does not apply a reversible Feynman–Kac variational formula to (4).

Let \(V_N(t,\eta)\) be a prescribed real source with uniform constants

\[
\|V_N\|_\infty\le v,\quad
\|\partial_tV_N\|_\infty\le\dot v,
\quad |\Delta_iV_N|\le C D_N/N,
\quad\sup_{u,\eta}\sum_i r_i(u,\eta)|\Delta_iV_N|^2\le C D_N^2/N. \tag{5}
\]

Finite total variation in macroscopic time can replace the derivative bound, with its variation paid as a boundary term. This note does not claim an arbitrary adaptive history-dependent tilt whose extra controller state has not been included in the estimate.

The residual is

\[
R_N(t)=\frac1N\int_0^{N^2t}q_N(u)V_N(u/N^2,\eta_u)\,du. \tag{6}
\]

For every \(\delta>0\), the claim is

\[
\limsup_{N\to\infty}\frac1N\log\sup_{\rho_N,z,\theta(0)}
\mathbb P_{\rho_N}^{E}\!\left(\sup_{t\le T}|R_N(t)|>\delta\right)=-\infty. \tag{7}
\]

The fixed field's bounds \(E_*\), and the source constants in (5), are held fixed while taking this limit. A compact bounded family of such fields has the same uniform estimate.

## 3. Conjugating a weakly nonreversible generator

Fix time and abbreviate \(r_i=r_i(u,\eta)\), \(\xi_i=\xi_i(u,\eta)\). For a real multiplication function \(W\), define

\[
\mathcal D_r(f)=\frac12\sum_{\eta,i}\pi_N(\eta)r_i(\eta)
                                      [f(\eta^i)-f(\eta)]^2.
\]

Pairing each exchange with its reverse yields the exact identity

\[
\begin{aligned}
\langle f,e^{-W}L^Ee^Wf\rangle_{\pi_N}
={}&-\mathcal D_r(f)\\
&+\sum_{\eta,i}\pi_Nr_i[\cosh(\xi_i+\Delta_iW)-1]f(\eta)f(\eta^i)\\
&-\sum_{\eta,i}\pi_Nr_i(e^{\xi_i}-1)f(\eta)^2. \tag{8}
\end{aligned}
\]

The odd part of the last line is controlled using the *same* exchange symmetry:

\[
\sum_{\eta,i}\pi_Nr_i\sinh\xi_i\,f(\eta)^2
=\frac12\sum_{\eta,i}\pi_Nr_i\sinh\xi_i
                         [f(\eta)^2-f(\eta^i)^2].
\]

Consequently,

\[
\left|\sum\pi_Nr_i\sinh\xi_i f^2\right|
\le\sqrt{2Nc_*}\sinh(E_*/N)\sqrt{\mathcal D_r(f)}\|f\|_2
\le\frac12\mathcal D_r(f)+Nc_*\sinh^2(E_*/N)\|f\|_2^2. \tag{9}
\]

The even part of the last line of (8) is nonpositive and may be dropped. For the middle line, use \(2ff'\le f^2+(f')^2\). If \(\max_i|\Delta_iW|\le w\), the result is

\[
\begin{aligned}
\langle f,e^{-W}L^Ee^Wf\rangle
\le{}&-\tfrac12\mathcal D_r(f)\\
&+\left[Nc_*\sinh^2(E_*/N)
+e^{E_*/N+w}\left(\frac{c_*E_*^2}{N}
                 +\sup_\eta\sum_i r_i|\Delta_iW|^2\right)\right]\|f\|_2^2. \tag{10}
\end{aligned}
\]

Here \(\cosh x-1\le x^2e^{|x|}/2\) and \((x+y)^2\le2x^2+2y^2\) were used. The weak-current cost is order \(1/N\), independent of the unknown context functions.

The unnormalized Feynman–Kac *density* for (4) evolves with \((L_u^E)^*\), not \(L_u^E\). This causes no omission: the quadratic form of \(e^{-W}(L_u^E)^*e^W\) equals that of \(e^WL_u^Ee^{-W}\), so (10) applies with \(W\mapsto-W\) and the same upper bound.

## 4. The gauge bound and superexponential consequence

Let \(Q_N'=q_N\), \(Q_N(0)=0\), \(\|Q_N\|_\infty\le H_N\). For the potential \(a q_NV_N\), use

\[
W(u,\eta)=aQ_N(u)V_N(u/N^2,\eta). \tag{11}
\]

Its derivative is the desired potential plus
\(aQ_N\partial_tV_N/N^2\). The latter contributes at most \(aH_N\dot v T\) to the log norm over physical time \(N^2T\). The endpoint gauge contributes at most \(aH_Nv\).

For fixed \(a\), (5) gives

\[
|\Delta_iW|\le CaH_ND_N/N,
\quad\sup\sum_i r_i|\Delta_iW|^2\le Ca^2H_N^2D_N^2/N.
\]

Combining (10)-(11), uniformly for \(t\le T\),

\[
\begin{aligned}
\log\mathbb E_{\pi_N}^{E}e^{\pm aNR_N(t)}
\le{}&aH_N(v+\dot vT)\\
&+N^2T\left[Nc_*\sinh^2(E_*/N)
+\exp\!\left(\frac{E_*+CaH_ND_N}{N}\right)
\left(\frac{c_*E_*^2}{N}+\frac{Ca^2H_N^2D_N^2}{N}\right)\right]. \tag{12}
\end{aligned}
\]

If (1) holds, then for every fixed \(a\),

\[
\limsup_N\frac1N\log\mathbb E_{\pi_N}^{E}e^{\pm aNR_N(t)}
\le2c_*E_*^2T. \tag{13}
\]

Its right side is independent of \(a\). The residual is Lipschitz in macroscopic time with constant at most \(Nv\), so a grid of order \(N\) suffices for each fixed deviation \(\delta\). Its logarithmic cost divided by \(N\) vanishes.

Unlike a mere entropy assumption, the present finite canonical initial interface gives the uniform density domination

\[
\rho_N(\eta)\le\binom N{M}\pi_N(\eta)\le2^N\pi_N(\eta). \tag{14}
\]

The same pointwise factor dominates complete path laws with the same conditional evolution. Chernoff, the grid, and (13)-(14) therefore yield, for every fixed \(a\),

\[
\limsup_N\frac1N\log\sup_{\rho_N}\mathbb P_{\rho_N}^{E}
\left(\sup_{t\le T}|R_N(t)|>\delta\right)
\le\log2+2c_*E_*^2T-a\delta/2. \tag{15}
\]

Sending \(a\to\infty\) proves (7). This is an iterated-limit argument with fixed \(a\) during the volume limit; no hidden rate relation between \(a\) and \(N\) is imposed.

For continuous rotation use the sum of the two multiplication gauges in (22) of the companion note. Their effective primitive is at most \(3/\Omega_N\), their increments obey the same influence estimate, and the proof is identical. A finite number of prescribed slow time fields can be included without changing the condition \(D_N/\Omega_N\to0\).

## 5. The exact weak-current likelihood compensator is in the source class

The exponential current tilt has microscopic log likelihood

\[
\sum_{\text{particle jumps at }(u,i)}\xi_i(u,\eta_{u-})
-\int_0^{N^2T}\sum_i r_i(u,\eta_u)(e^{\xi_i(u,\eta_u)}-1)du. \tag{16}
\]

The jump term is independent of which physical mobility produced the path. The difference between the actual and mean-rate compensators is

\[
\int_0^{N^2T}q_N(u)V_N^E(u/N^2,\eta_u)du,
\]

where

\[
V_N^E(t,\eta)=c\sum_i b_i(\eta)
\left[\exp\!\left(\frac{E_i(t)}{N}(\eta_i-\eta_{i+1})\right)-1\right]. \tag{17}
\]

Each summand has magnitude at most \(c\alpha E_*e^{E_*/N}/N\), so its total is bounded independently of \(N\). If at most \(D_N\) summands change per exchange, then

\[
|\Delta_jV_N^E|\le2c\alpha E_*e^{E_*/N}D_N/N.
\]

If \(\sup|\dot E_i|\) is bounded, \(\|\partial_tV_N^E\|_\infty\) is also uniformly bounded. Thus (17) satisfies (5), and its normalized compensator difference is superexponentially negligible under the weakly tilted laws themselves.

This is the precise bridge offered to a smooth-current action proof. Further ingredients—replacement of local activity by its density function, exponential tightness, the lower-bound construction for a sufficiently rich set of paths, initial rate functions, and extension from smooth paths—must still be proved or supplied by an appropriate established theorem. This note does not infer all those steps from (7).

## 6. Independent Poisson pi kicks under the same tilts

Use the actual joint process (30) of the companion note, with signs flipped at rate \(\gamma_N\), and tilt only the native particle exchanges by (3). The reference is \(\nu_N=\pi_N\otimes\text{Unif}\{-1,+1\}^N\).

At \(W=0\), the same reverse-pair argument yields

\[
\langle f,L_{\rm native}^{E}f\rangle
\le-\tfrac12\mathcal D_{\rm native}(f)+C_E/N\,\|f\|_2^2, \tag{18}
\]

with one finite constant depending only on \(c_*,E_*\). For example (10) at \(W=0\) supplies such a constant uniformly in \(N\). The sign generator still contributes exactly \(-\mathcal D_{\rm sign}(f)\).

For any source

\[
V_N(t,\eta,\sigma)=\sum_i v_i(t,\eta)\sigma_i,
\qquad \sum_i\|v_i\|_\infty^2\le C/N, \tag{19}
\]

the sign-flip estimate (31) of the companion note gives

\[
\langle f,(\mathcal L^E+aV_N)f\rangle
\le\left(\frac{C_E}{N}+\frac{Ca^2}{2\gamma_NN}\right)\|f\|_2^2. \tag{20}
\]

The identical quadratic bound applies to the adjoint. It is valid pointwise in time even for time-dependent prescribed sources. Therefore

\[
\log\mathbb E_{\nu_N}^{E}e^{\pm aNR_N(t)}
\le NT\left(C_E+\frac{Ca^2}{2\gamma_N}\right). \tag{21}
\]

Every initial joint law on the finite visible/sign state space has density at most \(4^N\) relative to \(\nu_N\). The time-grid and Chernoff argument now gives (7) whenever \(\gamma_N\to\infty\), with \(\log4\) replacing \(\log2\) in (15). No locality of the coefficients \(v_i(t,\eta)\) is needed. In particular, the exact compensator coefficients

\[
v_i^E(t,\eta)=c b_i(\eta)(e^{\xi_i(t,\eta)}-1)
\]

satisfy (19) even when the unknown amplitudes depend on the entire unchanged visible configuration.

This is not a hidden initial sign randomization: the actual initial law can be a recorded point mass. Fresh Poisson innovations after the deployment record remain required. Retaining their outcomes as generated is compatible with a statement about the same actual joint law; conditioning on an arbitrarily rare complete future record is stronger and is not claimed.

## 7. Apparatus accuracy and ordinary-control comparison

The exact cancellation in (11) uses a genuinely bounded primitive. Small systematic drive error can leave a nonzero mean modulation. If \(q_N\) is replaced by \(q_N+\varepsilon_N\), a constant \(\varepsilon_N\) is not a bounded-primitive perturbation on physical time \(N^2T\). The proof does not absorb it merely because a pulse or phase error is numerically small.

For example, a spatially homogeneous uncompensated phase bias changes a configuration-independent mobility by a fixed relative factor; its hydrodynamic diffusion coefficient then changes by that factor. Exact equality of a limiting action demands an appropriate vanishing/calibrated bias, not just a finite apparatus tolerance. Bounded jitter, finite pulse waveforms, addressing errors, residual mean disorder and persistent uncontrolled phase noise require their actual quantitative models. No ideal control accuracy is inferred from a mathematical clock parameter.

With those premises stated, deterministic rotation is an ordinary implementation of the stronger replacement lemma for finite-range contexts. Its full many-body parity micromotion failure does not invalidate this specific large-deviation-scale current result. Arbitrary global contexts remain materially different: the exact collective heat-bath obstruction in the companion note requires rotation faster than the \(N\)-scale, while independent local Poisson pi kicks avoid that coherence through separately supplied local randomness. One shared stochastic phase cannot be substituted for the independent phase family.

The proof uses established Feynman–Kac bounds, exponential conjugation and jump-process current tilting. The companion note records the actual primary predecessors. A complete action theorem constructed using this lemma should compare both real actuator suppliers, and should not claim novelty for deterministic averaging or for the basic entropy/large-deviation method.

## 8. Direct current-large-deviation predecessor

L. Bertini, A. De Sole, D. Gabrielli, G. Jona-Lasinio and C. Landim, *Large deviations of the empirical current in interacting particle systems*, [primary preprint](https://arxiv.org/pdf/math/0512394), [published DOI](https://doi.org/10.1137/S0040585X97982256). Read the model and Theorem 2.2, Section 3.1's weak external-field rates, the superexponential replacement statement in Theorem 3.2, and Section 3's likelihood/exponential-martingale formulas. The paper already proves the SSEP density/current action and uses precisely this kind of weak current change of measure. The operation-specific question here is whether an actually controlled, unknown context-modulated native dynamics supplies the needed replacement uniformly, at its real control-rate scaling. Equations (8)-(21) address that supplier question; neither the SSEP action nor its standard tilting mechanism is an invention of this unit.
