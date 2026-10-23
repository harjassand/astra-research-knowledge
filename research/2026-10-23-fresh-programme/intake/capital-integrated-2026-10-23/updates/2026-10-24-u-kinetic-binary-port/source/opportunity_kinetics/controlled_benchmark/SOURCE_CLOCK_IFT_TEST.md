# Fixed-horizon source-clock IFT test

This is a conventional fluctuation-identity test for the source-clock null,
not a novelty or physical-engine claim. It requires no generator reconstruction
and no resets during operation. The protocol and horizon are fixed before
observing the run.

## Null and exact identity

Use a finite state space and column-vector convention. Let \(Q_0\) be a
conservative generator with stationary vector \(\pi_0\), and for a prescribed
state-energy vector \(E(t)\), set
\[
Q_{E(t)}=Q_0\,\mathrm{diag}(e^{\beta E_i(t)}),\qquad
\pi_{E(t),i}=\frac{\pi_{0,i}e^{-\beta E_i(t)}}{Z_E(t)},\qquad
Z_E(t)=\sum_i\pi_{0,i}e^{-\beta E_i(t)}.
\]
The initial distribution is \(\pi_{E(0)}\). The field-port work **on** the system
along a path is
\[
W_{\rm on}(0,T)=\int_0^T \dot E_{X_t}(t)\,dt.
\]
It contains parameter work only; jump-energy changes and chemical fuel are
separate. For \(E_i(t)=-h(t)f_i\), this is the scalar-work functional
\[
W_{\rm on}=-\int_0^T\dot h(t)f(X_t)\,dt.
\]

Let \(w_i(t)=\mathbb E[e^{-\beta W_{\rm on}(0,t)}1_{X_t=i}]\). The
Feynman–Kac equation and its exact solution are
\[
\dot w=[Q_{E(t)}-\beta\,\mathrm{diag}(\dot E_i(t))]w,
\qquad
w_i(t)=\frac{\pi_{0,i}e^{-\beta E_i(t)}}{Z_E(0)}.
\]
Indeed, \(Q_Ew=Q_0\pi_0/Z_E(0)=0\), leaving precisely
\(\dot w_i=-\beta\dot E_iw_i\). Therefore
\[
\mathbb E_{\pi_{E(0)}}e^{-\beta W_{\rm on}(0,T)}
=\frac{Z_E(T)}{Z_E(0)}.
\]
For any predeclared closed control \(E(T)=E(0)\), including any fixed number
of cycles without resets, this equals one. No detailed balance for \(Q_0\) is
used; it may carry stationary chemical currents.

For \(w>0\), Markov's inequality gives the exact source-clock tail bound
\[
\Pr_{\rm clock}\{W_{\rm on}\le -w\}\le e^{-\beta w}.
\]
With \(T=1\) in energy units, \(\beta=1\). If \(f\in\{0,1\}\) and \(h(0)=h(T)=0\),
integration by parts gives the observable jump expression
\[
W_{\rm on}=\int_0^T h(t)\,df(X_t)
=\sum_{t_j\le T}h(t_j)[f(X_{t_j})-f(X_{t_j^-})].
\]
This expression needs only the scalar trajectory and jump times, not hidden
state labels. If jumps are not observed, use the randomized-time estimator
below; do not substitute hidden jump information.

## Finite scalar-readout test

For a known closed piecewise-smooth \(h\) over \(L\) fixed periods, write
\(V_h=\int_0^\tau|\dot h(s)|\,ds\). In each period independently draw
\(U_+,U_-\) with densities
\[
q_+(s)=\frac{2\dot h(s)}{V_h}\mathbf 1_{\dot h(s)>0},\qquad
q_-(s)=\frac{-2\dot h(s)}{V_h}\mathbf 1_{\dot h(s)<0},
\]
and form
\[
Z_k=-\frac{V_h}{2}[Y(U_+)-Y(U_-)],\qquad
\widehat W_L=\sum_{k=1}^L Z_k.
\]
The readout is \(Y=f(X)+b+\xi(t)+\epsilon\): the unknown constant \(b\)
cancels within each pair; ε is independent, conditionally zero-mean and
bounded by \(\eta\); phase-varying bias obeys \(|\xi(t)|\le b_{\rm ph}\). Readout must be
noninvasive. Then, conditional on the entire physical path,
\[
\mathbb E[\widehat W_L\mid X]
=W_{\rm on}+d_L,\quad |d_L|\le LV_hb_{\rm ph},
\qquad |Z_k|\le B=V_h(1+\eta+b_{\rm ph}).
\]
The independent timestamps and noise give the one-sided bound
\[
\Pr\{W_{\rm on}>\widehat W_L+r+LV_hb_{\rm ph}\mid X\}
\le e^{-r^2/(2LB^2)}.
\]
Thus choosing \(r=B\sqrt{2L\log(1/\alpha_{\rm read})}\) makes
\(U=\widehat W_L+r+LV_hb_{\rm ph}\) a \((1-\alpha_{\rm read})\) upper
confidence bound on the realized field-port work. This concentration is
conditional on the physical trajectory, so correlations between operated
cycles and lack of resets do not invalidate it.

Suppose the one initial preparation has externally certified total-variation
error at most \(\delta_0\) from \(\pi_{E(0)}\). For any complete-run event, including the
probe randomization and sensor noise, its probability changes by at most
δ_0. Therefore the fixed-horizon rule
\[
\boxed{U\le -w}
\]
rejects the source-clock null with type-I probability at most
\[
e^{-\beta w}+\delta_0+\alpha_{\rm read}.
\]
For target level \(\gamma\), require \(\delta_0+\alpha_{\rm read}<\gamma\) and take
\(w=\beta^{-1}\log[1/(\gamma-\delta_0-\alpha_{\rm read})]\).
An exact scalar path integral sets α_read=0; bounded sensor error may be
handled with the stated margin. If the phase bias is unknown or unbounded, no
such margin is certified.

## Scope and resources

This test uses one stationary preparation, \(L\) continuously operated cycles,
and \(2L\) scalar readouts; it uses no in-operation reset. Report elapsed
operation time \(L\tau\), plus the actual preparation time and its external
error certificate. The test says a sufficiently large negative field-work
excursion is unlikely under this source-clock family. It does not certify
negative mean work, useful net output, or an alternative mechanism. Scalar
readout alone does not in general give reaction count or winding, so fuel,
chemical dissipation, field-controller work and losses remain separate
measurements and resource entries.

The claim is for a predeclared fixed horizon. It does not automatically hold
when stopping after a threshold crossing or repeatedly checking until the
threshold is met: the fixed-time exponential identity is not, by itself, a
time-uniform martingale bound. An optional-stopping claim needs a separate
proof. A source-clock preparation must also be justified externally; waiting
for an unspecified time is not a \(\delta_0\) certificate.
