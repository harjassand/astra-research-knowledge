# Tunable memory port: finite capture, release, and idle heat

Bounded Markov input-output calculation, 24 October 2026. This is an exact
linear model under the stated bosonic/Markov assumptions, not a device result.

## Model and capture mode

A memory mode \(a\) at frequency \(\omega_0\) couples to independent continuum
ports \(j\in\{H,C,i\}\), with energy-decay rates \(\kappa_j(t)\) and
occupations \(n_j=(e^{\hbar\omega_0/k_BT_j}-1)^{-1}\). Port \(i\) denotes
intrinsic loss (a bath, not a free sink). In the rotating frame,
\[
 \dot a=-\tfrac12\Lambda(t)a+\sum_j\sqrt{\kappa_j(t)}b_{j,\rm in}(t),
 \quad b_{j,\rm out}=b_{j,\rm in}-\sqrt{\kappa_j}a,
 \quad \Lambda=\sum_j\kappa_j.
\]
Rates are nonnegative and the input fields have delta-function bosonic
commutators. Define \(K(t)=\int_0^t\Lambda(s)ds\) over any stage of duration
\(T\). Solving the Langevin equation gives the exact endpoint relation
\[
 a(T)=e^{-K(T)/2}a(0)+\sum_j\sqrt{\eta_j}B_{j,F_j},\quad
 \eta_j=\int_0^T\kappa_j(s)e^{-[K(T)-K(s)]}ds,\quad
 F_j(s)={\sqrt{\kappa_j(s)}e^{-[K(T)-K(s)]/2}\over\sqrt{\eta_j}}.
\]
Here \(B_{j,F_j}=\int F_j^*(s)b_{j,\rm in}(s)ds\), and the mode is omitted
when \(\eta_j=0\). The normalization identity is
\(e^{-K(T)}+\sum_j\eta_j=1\). Thus all open ports, including an allegedly
off coupler with nonzero floor, contribute actual input modes.

For capture, set \(j=H\) as the signal port. Write
\(r_H=e^{-K_H(T_c)/2}\), with \(\eta_{H,c},\eta_{C,c},\eta_{i,c}\) from the
endpoint formula. Then
\[
 a_c=r_Ha_0+\sqrt{\eta_{H,c}}B_{H,F_H}
       +\sqrt{\eta_{C,c}}B_{C,F_C}
       +\sqrt{\eta_{i,c}}B_{i,F_i}.
\]
In particular, capture does not separate a signal from thermal occupation in
the same hot temporal mode: the captured hot thermal noise is
\(\eta_{H,c}n_H\); cold off-floor and intrinsic contributions are
\(\eta_{C,c}n_C\) and \(\eta_{i,c}n_i\). If \(n_0=\langle a_0^\dagger a_0\rangle\),
independent zero-mean inputs give
\[
 n_c=r_H^2n_0+\eta_{H,c}n_H+\eta_{C,c}n_C+\eta_{i,c}n_i,
\]
with any signal occupancy in \(B_{H,F_H}\) added using the same coefficient.
For ideal hot-only capture with no intrinsic loss,
\(\eta_{H,c}=1-e^{-K_H}\); for constant \(\kappa_H\) and intrinsic
\(\kappa_i\),
\(\eta_{H,c}=\kappa_H(1-e^{-(\kappa_H+\kappa_i)T_c})/(\kappa_H+\kappa_i)\).
This displays both the finite-coupling/time penalty and the intrinsic-loss
ceiling.

## Release into one selected output mode

During a release interval choose the desired cold output mode
\[
 F_{C,\rm out}(t)={\sqrt{\kappa_C(t)}e^{-K(t)/2}\over\sqrt{\eta_{C,r}}},
 \qquad \eta_{C,r}=\int_0^{T_r}\kappa_C(t)e^{-K(t)}dt.
\]
Projecting \(b_{C,\rm out}\) onto this normalized mode gives
\[
 B_{C,\rm out}=-\sqrt{\eta_{C,r}}a_c+\sum_j\int_0^{T_r}c_j(s)b_{j,\rm in}(s)ds,
\]
where the exact continuum coefficients are
\[
 c_j(s)=\mathbf1_{j=C}F_{C,\rm out}(s)
 -{\sqrt{\kappa_j(s)}e^{K(s)/2}\over\sqrt{\eta_{C,r}}}
       \int_s^{T_r}\kappa_C(t)e^{-K(t)}dt.
\]
Canonical commutation gives \(\sum_j\int|c_j(s)|^2ds=1-\eta_{C,r}\).
For independent stationary thermal input ports the release noise occupancy is
\(\nu_r=\sum_j n_j\int|c_j|^2ds\), and
\(n_{\rm out}=\eta_{C,r}n_c+\nu_r\). The end-to-end signal transmissivity
for the selected captured mode is exactly
\(\eta_{\rm sig}=\eta_{H,c}\eta_{C,r}\); the output also contains
\(\eta_{C,r}r_H^2n_0\), capture-stage baths multiplied by \(\eta_{C,r}\),
and the release noise \(\nu_r\). These terms include initial memory,
intrinsic bath, and cold-line occupancy without treating any as a free vacuum.

In the lossless single-port release limit \(\kappa_C>0,\kappa_i=0\),
\(\eta_{C,r}=1-e^{-K_C}\), and the cold input noise coefficient has norm
squared \(e^{-K_C}\); it is a specific orthogonal input temporal mode. A
finite release therefore leaves both residual memory amplitude
\(e^{-K_C/2}\) and a reflected cold-line component. Increasing \(K_C\) removes
these only by keeping the coupler open long enough/strongly enough; a bounded
\(\kappa_C\le\kappa_{\max}\) imposes \(K_C\le\kappa_{\max}T_r\).

## Heat ledger for two finite thermal isochores

For a no-signal cycle, first couple only to hot bath H for integrated decay
\(K_H\), then only to cold bath C for \(K_C\); ignore intrinsic loss in this
paragraph. Put \(r_H=e^{-K_H}\), \(r_C=e^{-K_C}\). The supplied isochore maps
are
\[
 n_1=n_H+(n_0-n_H)r_H,\qquad n_0'=n_C+(n_1-n_C)r_C.
\]
At periodic steady state \(n_0'=n_0\),
\[
 n_0={n_C(1-r_C)+r_Cn_H(1-r_H)\over1-r_Hr_C},\qquad
 n_1-n_0={(1-r_H)(1-r_C)\over1-r_Hr_C}(n_H-n_C).
\]
Each bath heat is an actual per-cycle energy, not just a memory-energy proxy.
With positive \(Q_j\) defined as heat delivered *to* reservoir j,
\[
 Q_H=\hbar\omega_0(n_0-n_1)=-Q_{H\to C},\quad
 Q_C=\hbar\omega_0(n_1-n_0)=Q_{H\to C},\quad
 Q_{H\to C}=\hbar\omega_0{(1-r_H)(1-r_C)\over1-r_Hr_C}(n_H-n_C).
\]
Power is this quantity divided by the full cycle time. It tends to zero if
either isochore is shut; finite contact time reduces but does not remove the
heat moved per completed cycle.

For any stage with constant rates to several reservoirs, including off-state
floors and intrinsic loss, let \(\Lambda=\sum_j\kappa_j\) and
\(n_*=(\sum_j\kappa_jn_j)/\Lambda\). Then
\[
 n(t)=n_*+(n(0)-n_*)e^{-\Lambda t},\quad
 Q_j^{\rm to\ bath}=\hbar\omega_0\kappa_j\left[(n_*-n_j)T
 +(n(0)-n_*){1-e^{-\Lambda T}\over\Lambda}\right].
\]
This gives each reservoir’s heat, including the intrinsic bath, during the
finite stage. With both nominally-off couplers held at positive floor rates
\(\kappa_H^{off},\kappa_C^{off}\) in idle and no intrinsic bath, the exact
steady idle cross-current is
\[
 P_{H\to C}^{idle}=\hbar\omega_0
 {\kappa_H^{off}\kappa_C^{off}\over\kappa_H^{off}+\kappa_C^{off}}
 (n_H-n_C).
\]
If intrinsic loss is also open, use \(n_*\) above: the cold-bath heat current
is \(\hbar\omega_0\kappa_C^{off}(n_*-n_C)\), which includes both the
hot-to-cold term and exchange with the intrinsic bath. For an idle interval
\(T_i\), transient heat follows the finite-stage equation rather than the
steady asymptote. Therefore a positive off floor creates real idle heat flow
whenever the ports have a temperature bias.

## Relation to ordinary tunable-coupler memory

This is the standard input-output catch/store/release architecture, made
explicit as a thermal channel. Yin et al., *Controlled catch and release of
microwave photon states*, demonstrated a resonator with variable transmission-
line coupling, reported a tunable emission rate up to about \(1/(5\,\rm ns)\),
about 2ns switching, and intrinsic lifetime about 4.5µs; they also showed
phase-coherent controlled release and tunable waveforms. The paper is a primary
precedent for the coupler operation ([arXiv:1208.2950](https://arxiv.org/abs/1208.2950),
[Phys. Rev. Lett. 110, 107001 (2013)](https://doi.org/10.1103/PhysRevLett.110.107001)).
It supports the feasibility of a tunable memory port, not a zero-cost or
zero-noise thermal valve: the same coupling that captures the desired mode
admits its bath, intrinsic loss remains when the external coupling is reduced,
and both ports’ measured off floors must be included in the idle-current
ledger. This calculation identifies no advantage over an ordinary switched
heat valve without a matched control, noise, and finite-leak comparison.
