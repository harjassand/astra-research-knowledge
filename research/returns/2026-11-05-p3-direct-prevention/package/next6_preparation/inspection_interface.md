# Mean-only initialization and a finite one-bit physical interface

Completed 5 November 2026. This construction is for the new direct intervention decision. All preserved sources and the separate relative-density preparation remain unchanged. The main result prepares a law whose **unbounded mean** is comparable to the equilibrium-safe benchmark. It does not prepare the equilibrium-safe distribution, a CDF or a marked-path law.

## 1. Operating assumptions and the safe-start theorem

For each menu item \(u\), the actual installation, after installation and settling, has generator

\[
Q^u=\sum_i r_i^u(s)(H_i-I),\qquad
0<q_i(s)\le\bar q<1/2,\qquad 0<r_-\le r_i^u(s)\le r_+.
\]

A bit equal to 1 is failed. The context excludes the focal bit, and \(r_i^u(s)\) is the same for both focal starting values. Every intervention has the same strictly positive invariant law \(\pi\); a common operating gap lower bound is \(\gamma>0\). Set \(b=(1,\ldots,1)\), \(p=\pi(b)\), and

\[
M_u=\mathbb E_{\pi(\cdot\mid b^c),Q^u}\tau_b,\qquad
\tau_b=\inf\{t\ge0:X_t=b\}.
\]

In particular, an initially failed state has lifetime zero. The installation must remain repairable during commissioning; a visit to \(b\) does not stop the preparation dynamics or destroy the source.

The boundary certificate uses the true mathematical uniformization
\[
R=Nr_+,\quad P=I+Q/R,\quad g=\gamma/R,\quad
\bar p=\bar q^N,\quad a=\bar q/(1-\bar q).
\]
The kernel is reversible and positive semidefinite, \(p\le\bar p\), and \(\pi(b)/\pi(x)\le a^{w(x)}\), where \(w\) counts working bits. Finite integers \(2\le k<N,L\ge1\) and a number \(z<1\) certify
\[
\Pr_x(\tau_b<\tau_{C_k})\le z\quad(1\le w(x)<k),
\qquad C_k=\{x:w(x)=k\}.
\]
This does not assume lumpability. Explicitly, with
\[
C=\frac{r_+\bar q}{r_-(1-\bar q)},\quad R_0=1,\quad
R_j=\prod_{\ell=1}^j\frac{C\ell}{N-\ell},\quad
H(w)=\frac{\sum_{j=w}^{k-1}R_j}{\sum_{j=0}^{k-1}R_j},
\]
the stopped process \(H(w(X))\) is a supermartingale: the actual upward \(w\)-transition probability is at least \((N-w)r_-(1-\bar q)/(Nr_+)\), and its downward probability is at most \(w\bar q/N\). Optional stopping gives \(z=H(1)\). The simpler choice
\[
\rho=Ck/(N-k)<1,\qquad z=C/[(N-1)(1-\rho)]<1
\]
is also valid.

Define the finite certificate
\[
s_*=(1-\bar p)^2,\quad E_*=La^k+a^{k/2}e^{-gL}/g,
\]
\[
A_*=(1-z)(1-\bar p)(1-E_*/s_*),\qquad
B_*=1+(L\bar p+e^{-gL}/g)/s_*.
\tag{1}
\]
Require \(E_*<s_*\). Then
\[
\boxed{A_*M_u\le\mathbb E_{x,Q^u}\tau_b\le B_*M_u
\quad\text{for every }x\ne b.}
\tag{2}
\]
Consequently, **any actual law** \(\nu_u\) with \(\nu_u(b)\le f\) obeys
\[
\boxed{(1-f)A_*M_u\le\mathbb E_{\nu_u,Q^u}\tau_b\le B_*M_u.}
\tag{3}
\]

### Proof

Let \(Z(x)=\sum_{j\ge0}[P^j(x,b)-p]\), \(S=Z(b)\) and \(q_0=1-P(b,b)\). The singleton Green identity and resolvent Cauchy--Schwarz give
\[
\frac{\mathbb E_x\tau_b}{M_u}=(1-p)(1-Z(x)/S),
\qquad q_0S\ge(1-p)^2,\qquad S\ge s_*.
\]
For a reversible kernel with nonconstant spectrum in \([0,1-g]\),
\[
|P^j(x,b)-p|\le\sqrt{\pi(b)/\pi(x)}(1-g)^j.
\tag{4}
\]
At \(x\in C_k\), reversibility also gives \(P^j(x,b)\le a^k\). The first \(L\) summands and the spectral remainder therefore give \(Z(x)\le E_*\), proving the desired lower ratio without \(1-z\) on \(C_k\). From \(1\le w<k\), reach \(C_k\) before \(b\) with probability at least \(1-z\). From \(w>k\), a single-site path to \(b\) must cross \(C_k\). Strong Markov at the first hit of \(\{b\}\cup C_k\), discarding elapsed nonnegative time, proves the lower bound everywhere safe.

For every state, \(\pi(b)/\pi(x)\le1\). Each initial summand of \(Z(x)\) is at least \(-p\), and (4) bounds the remaining sum, so \(Z(x)\ge-Lp-e^{-gL}/g\). Substitution proves the upper bound. Integrate over \(\nu_u\), with zero lifetime at \(b\), to prove (3).

This is a direct bound on an unbounded mean, not an inference from TV distance. It uses the singleton target, uniform recovery bias and mixing certificate. At fixed margins, the finite tails can be small and the explicit return correction is \(z=O(1/N)\). The arithmetic length \(L\) is not a physical waiting time.

## 2. Main finite physical realization: one working-bit witness

The actual source needs **one noninvasive binary read port** on a chosen component. Inherited whole-state inspection access supplies it; local experimental copies alone do not. Its capture semantics, error, response and propagation times must be specified and priced. This is a stated sensor service, not a sensor invention inferred from the reliability model. No source pin, source-wide freeze, or full-state inspection is used.

Set \(a_{\rm w}=r_-(1-\bar q)\), \(b_{\rm w}=r_+\bar q\). Uniformly in the neighborhood, the selected bit has failed-to-working rate at least \(a_{\rm w}\) and working-to-failed rate at most \(b_{\rm w}\). Its working probability satisfies
\[
v'(t)\ge a_{\rm w}(1-v(t))-b_{\rm w}v(t).
\]
Thus, from every starting law and every previous service history,
\[
v(t)\ge v_0:=\frac{a_{\rm w}}{a_{\rm w}+b_{\rm w}}
(1-e^{-(a_{\rm w}+b_{\rm w})t_0})\quad(t\ge t_0).
\tag{5}
\]
For example, choose \(t_0=\log2/(a_{\rm w}+b_{\rm w})\), with an outward-rounded lower elapsed-time bound.

One attempt runs the actual repairable installation at the selected fixed intervention for at least \(t_0\), then captures the bit in a certified window \([t_c^-,t_c^+]\), where \(t_c^-\ge t_0\). The source continues to evolve under the same \(Q^u\) during capture, detector service, computation and propagation. A complete valid working report must arrive by a fixed terminal deadline. Accept or reject at that deadline; do not begin deployment at an unpriced instantaneous read or early reply. The certified actual end-time interval is \([D_-,D_+]\), after capture. Write
\[
W_c=t_c^+-t_c^-,\qquad \Delta=D_+-t_c^-.
\]

The conditional read contract is: given the true captured bit and all preceding service history, a working bit yields a valid working report by the deadline with probability at least \(1-\beta\), whereas a failed bit yields one with probability at most \(\beta\). Missing or invalid messages count as rejection. The contract includes completion and processing errors and must remain valid for reused apparatus. Persistent common faults must be charged in a separately calibrated common confidence event or this conditional envelope. A marginal one-shot error calibration is insufficient. The read must leave the operating generator unchanged, and conditioning on service history must preserve the declared physical rate bounds.

For fixed or exogenous capture time, the probability of capturing a working bit is at least \(v_0\). Even if the bounded capture time adapts to the current record, the event of being working at \(t_c^-\) and remaining working through the full capture window has probability at least
\[
h_0=v_0e^{-b_{\rm w}W_c}.
\tag{6}
\]
This follows from the uniform upper bound on the failure intensity, even while neighbors change. This event forces every permitted capture to see a working bit. Therefore every reached attempt, conditional on its previous history, accepts with probability at least
\[
s_{\rm acc}=(1-\beta)h_0>0.
\tag{7}
\]
Use \(h_0=v_0\) in the fixed/exogenous case.

An accepted but globally failed terminal state requires either an incorrect working report or a working-to-failed transition of the correctly captured bit between capture and deployment. The first has probability at most \(\beta\). The latter is contained in a transition event over \([t_c^-,D_+]\), whose expected count is at most \(b_{\rm w}\Delta\). Therefore
\[
\boxed{\Pr(X_{\rm end}=b\mid\mathrm{accept})
\le f_{\rm start}:=\min\left\{1,
\frac{\beta+b_{\rm w}\Delta}{(1-\beta)h_0}\right\}.}
\tag{8}
\]
This accounts for actual evolution after capture and bounded end-clock error. A correct earlier working report is not asserted to establish a certainly safe terminal state. The clock/read tolerances are set by the desired decision loss, not by global rarity. At fixed local margins and desired loss they need not tighten with \(N\). If the actual meter latency or fidelity cannot pass (8), this realization is unavailable at that target accuracy.

### Finite retries and the successful law

Repeat at most
\[
J=\left\lceil\frac{\log\delta_{\rm abort}}{\log(1-s_{\rm acc})}\right\rceil
\tag{9}
\]
attempts. No source reset is required after rejection: (5) is uniform from its actual state. Conditional envelopes replace independence between attempts. The probability of no acceptance is at most \(\delta_{\rm abort}\).

At each reached attempt the bad-and-accepted probability is at most \(f_{\rm start}\) times its acceptance probability. Summing over mutually exclusive first-accepted attempts proves that the law **conditional on successful preparation before the cap** has \(\nu_u(b)\le f_{\rm start}\). Return an explicit abort if all attempts reject. If the mission definition assigns lifetime zero to abort, multiply the successful-law lower bound by \(1-\delta_{\rm abort}\). Calibration confidence, preparation abort, and failed initial mass within successful preparations remain separate.

## 3. Complete deployed comparison and cost

If the acquired decision gives \(M_{\widehat u}/\max_u M_u\ge F_{\rm dec}\) on its joint confidence event, then the actual successful preparation laws satisfy
\[
\boxed{
\frac{\mathbb E_{\nu_{\widehat u},Q^{\widehat u}}\tau_b}
{\max_u\mathbb E_{\nu_u,Q^u}\tau_b}
\ge (1-f_{\rm start})\frac{A_*}{B_*}F_{\rm dec}.}
\tag{10}
\]
Check all factors against the requested tolerance. Only the selected source is physically prepared; the other laws define the same counterfactual physical procedure. A changed deployed generator requires its own valid uncertainty composition or widened actual operating certificate.

Each attempt pays the actual whole-system waiting and deadline time, one source capture/read, detector and controller service, propagation, clock calibration and setup. Capped full-system wall time is at most \(J D_+\), plus setup intervals; **summed component exposure is \(N J D_+\)**, plus installation/ramp intervals. Add actual field installation, precision, slew, settling, actuator work, source repair and the acquisition needed to certify the service. Fixed margins, target loss and service specifications give \(O(N)\) component exposure, not constant exposure. Any size-dependent propagation or hardware price remains explicit.

The source must be repairable during commissioning, including after visits to \(b\). If such visits are irreversible physical catastrophes, a paid replacement/reset mechanism is necessary. No inference about absent hidden common-cause failures or external mechanisms is made. The conditional read contract cannot be supplied by assertions about the simulator.

## 4. Independent stronger bound: constant wait may already suffice

The following optional improvement is fully proved and uses only the same rate bounds. It makes the finite-read interface robust to long latency, or removes inspection when the mean-only endpoint permits a small certified failed mass.

Construct independent comparison bits \(Y_i\), initially all failed, with recovery rate \(a_{\rm w}\) and failure rate \(b_{\rm w}\). Couple any actual initial state below \(Y\). Independent rate-\(b_{\rm w}\) birth clocks set \(Y_i=1\), while true births are thinned to their actual context-dependent rate. Independent rate-\(a_{\rm w}\) death clocks set both failed bits to zero; extra true death clocks supply remaining recovery. This preserves \(X_i(t)\le Y_i(t)\). No attractiveness of the actual interactions is needed. The clocks are a proof device, not additional experimental control.

At every deterministic \(t\), from every actual initial distribution,
\[
\Pr(X_t=b)\le q_{\rm dom}(t)^N,\qquad
q_{\rm dom}(t)=\frac{b_{\rm w}}{a_{\rm w}+b_{\rm w}}
+\frac{a_{\rm w}}{a_{\rm w}+b_{\rm w}}e^{-(a_{\rm w}+b_{\rm w})t}.
\tag{11}
\]
At the above \(t_0\), \(q_{\rm dom}(t_0)=1-c_0\), with
\[
c_0=\frac{a_{\rm w}}{2(a_{\rm w}+b_{\rm w})}>0.
\]
A fixed operating wait of \(t_0\), followed by unconditional deployment, thus has failed mass at most \((1-c_0)^N\). If this error fits (3), no inspection or rejection is needed. This is neither an exact safe state nor an approximation to equilibrium.

For one-bit acceptance at a fixed deadline \(D\ge t_0\), division by the acceptance floor gives the alternative bound
\[
\Pr(X_D=b\mid\mathrm{accept})\le q_{\rm dom}(D)^N/s_{\rm acc}.
\tag{12}
\]
No independence between the read and terminal state is asserted. This can improve (8) despite a long, fully charged read latency.

For actual terminal time in \([D_-,D_+]\), put \(q=q_{\rm dom}(D_-)\) and \(\Delta_D=D_+-D_-\). A visit to \(b\) in the interval requires either starting there or an entry. Its expected entry count is at most
\[
b_{\rm w}\sum_i\int_{D_-}^{D_+}\Pr(X_{-i}(t)=1)\,dt
\le N b_{\rm w}\Delta_D q^{N-1},
\]
using the same coupling on every \((N-1)\)-coordinate marginal. Hence
\[
\boxed{\Pr(\exists t\in[D_-,D_+]:X_t=b)
\le\chi_D:=\min\{1,q^N+N b_{\rm w}\Delta_D q^{N-1}\}.}
\tag{13}
\]
Unconditional deployment at any actual time in the window has failed mass at most \(\chi_D\); accepted witness deployment has failed mass at most \(\chi_D/s_{\rm acc}\). This event-inclusion argument handles even bounded adaptive terminal timing. It does not insert a path-dependent random time into a fixed-time marginal bound. The actual repairable operating process must remain in force through the entire window. It introduces no exponentially precise clock.

## 5. Relation to the retained stronger preparation

The earlier relative-law preparation and the separate logarithmic-Sobolev construction in relative_density_preparation.tex are stronger distributional operations. They retain their actual exposure and subsequent inspection requirements. The mean-only interface here cannot replace them when a CDF or joint marked-path guarantee requires that initial law.

Green identities, strong Markov arguments, supermartingales and graphical comparison are established tools. The new deduction in this package is their explicit all-safe-state mean envelope, together with its finite terminal interface and composition with the acquired direct intervention decision. No physical sensor execution or historical firstness is claimed.

Primary background: D. Aldous and J. Fill, *Reversible Markov Chains and Random Walks on Graphs*, https://www.stat.berkeley.edu/~aldous/RWG/book.html ; J. Loper, G. Zhou and S. Geman, *Capacities and efficient computation of first-passage probabilities*, Physical Review E 102, 023304 (2020), https://doi.org/10.1103/PhysRevE.102.023304 . The actual preparation deductions and costs are proved explicitly above.
