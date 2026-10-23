# Observable-only finite-data certificate for field-port work

**Frozen before reading any other kinetics candidate.** This is a source-only
statistical protocol for one prescribed periodic command. It is not an
operating-engine result or a physical demonstration.

## Model and target

Let \(X_t\) be a finite-state CTMC under a known periodic command
\(h(t+\tau)=h(t)\), with calibrated state energies
\(E_i(h)=-h f_i\), \(|f_i|\leq1\), at bath temperature \(T=1\). Field-port
work **on** the system in cycle \(k\) is
\[
W_k=-\int_0^\tau \dot h(s) f(X_{k\tau+s})\,ds.
\]
The target stationary periodic mean is \(w_*=\mathbb E_{\pi_*}W_k\), where
\(\pi_*\) is the phase-zero invariant law of the driven one-period kernel.
Negative \(w_*\) means work leaves the system through the field port; it does
not by itself imply net output after chemical fuel and controller work are
charged.

Assume the scalar sensor reports \(Y=f(X_t)+b+\epsilon\). Here \(b\) is an
unknown offset common to the paired readings within a period, and the
residual noise is independent, conditionally zero-mean, and bounded by
\(|\epsilon|\leq\eta\). If residual bias can vary with phase, bound its
magnitude by \(\beta\). Unknown, unbounded, or rapidly varying bias prevents
the certificate. The readout is assumed non-invasive; otherwise its
measurement-induced dynamics must be included in the specified CTMC.

## Paired random-phase estimator

Let \(V_h=\int_0^\tau|\dot h(s)|\,ds\). For a nonconstant closed field cycle,
positive and negative variations each equal \(V_h/2\). In every sampled
period, independently draw \(U_+\) and \(U_-\) with densities
\[
q_+(s)=\frac{2\dot h(s)}{V_h}\mathbf 1_{\dot h(s)>0},
\qquad
q_-(s)=\frac{-2\dot h(s)}{V_h}\mathbf 1_{\dot h(s)<0}.
\]
Take one scalar readout at each timestamp and set
\[
Z_k=-\frac{V_h}{2}(Y_{k,+}-Y_{k,-}).
\]
The common additive offset cancels exactly. Conditional on the hidden path,
averaging over the randomized times and zero-mean readout noise gives
\[
\mathbb E[Z_k\mid X_{[k\tau,(k+1)\tau]}]
=-\int_0^\tau\dot h(s)f(X_{k\tau+s})\,ds=W_k.
\]
This uses only \(h\), randomized timestamps, and scalar readings. It does
not infer the generator or hidden state; it remains unbiased at any drive
frequency and despite arbitrary intracycle state correlations. The pair
mark obeys \(|Z_k|\leq B=V_h(1+\eta)\). There are two readouts per sampled
period.

For \(L\) consecutive operated periods, \(\widehat W_L=\sum_{k=0}^{L-1}Z_k\).
Conditioned on the complete physical path, independent timestamp
randomization and sensor noise give
\[
\Pr\!\left(\left|\widehat W_L-\sum_k W_k\right|\geq r
\mid X_{[0,L\tau]}\right)
\leq2\exp\!\left[-\frac{r^2}{2LB^2}\right].
\]
Thus \(\widehat W_L+r+LV_h\beta<0\) certifies negative **realized** field
work on that run at the selected tail probability. This finite-run result
needs no reset or mixing assumption. It is not a certificate for the CTMC
ensemble mean.

## Stationary-mean certificate from one correlated trajectory

To certify \(w_*<0\), supply an independently known mixing bound. Let \(P\)
be the one-period transition kernel and assume its Dobrushin coefficient
satisfies
\[
\sup_{x,x'}\|P(x,\cdot)-P(x',\cdot)\|_{\rm TV}\leq\rho<1.
\]
This guarantees a unique periodic phase-zero law and bounds the effect of an
arbitrary initial state after \(b\) warm-up periods by \(\rho^b\). Then
sample one pair in each of \(n\) periods whose start times are \(D\) periods
apart. Coupling the first sampled phase-zero state to stationarity, then
each later one after the \(D-1\) transitions since the previous sampled
period ended, bounds the joint mark law's total-variation distance from
\(n\) independent stationary marks by
\[
\delta_{\rm mix}\leq\rho^b+(n-1)\rho^{D-1}.
\]
The plant is never reset. The \(D-1\) omitted periods continue to run and
consume their associated resources.

For \(\bar Z=n^{-1}\sum_jZ_j\), define
\[
r_n=B\sqrt{\frac{2\ln(2/\alpha_s)}{n}}.
\]
The rule
\[
\boxed{\bar Z+r_n+V_h\beta<0}
\]
certifies \(w_*<0\) with confidence at least
\(1-\alpha_s-\delta_{\rm mix}\). Choose \(b,D\) such that
\(\rho^b+(n-1)\rho^{D-1}\leq\alpha_m\) and
\(\alpha_s+\alpha_m\leq\alpha\); the total elapsed operating time through
the last sampled period is
\[
T_{\rm elapsed}=[b+(n-1)D+1]\tau.
\]
There are \(2n\) readouts. This is conservative when \(\rho\) is near one;
the mixing guarantee is an external model/design certificate, not something
learned from the same finite scalar trace.

## Work, fuel, and failure boundary

This protocol certifies field-port work only. For an \(n\)-ring obeying local
detailed balance with edge-rate ratio \(k_+/k_-\), the dimensionless cycle
affinity is \(n\ln(k_+/k_-)\) at \(T=1\); chemical work depends on net ring
winding. A scalar \(f\) trace does not generally identify that winding.
Report chemical fuel separately using a measured reaction count or a
justified stoichiometric observable, and report field-controller work and
losses. A negative field-port work estimate is not a net-output claim.

Without a readout-bias bound and a known mixing bound, no distribution-free
finite-trace guarantee for the stationary mean follows: phase-dependent
sensor bias can mimic the work integral, and an irreducible CTMC can hide a
metastable sector behind a transition rate small enough that it is unseen
throughout the observation window while controlling the eventual periodic
mean. The random-phase identity still estimates the realized finite-path
work, but a single path cannot then certify the stationary ensemble mean.
