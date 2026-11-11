# P2 completed response — 053c72e6

Pro chat: https://chatgpt.com/c/6af2d0d2-f500-83ec-a7d0-20e80bd42677
Prompt: P2_FULL_NONLINEAR_RESPONSE_AFTER_JOINT_MEMORY_PRO_20261111.txt, SHA-256 4c43e83088bce5d9a62b4fec953c1d94161c373fc17284217d9c59a99e638eba. Full UI-copied final matches the native first 20,000 characters after whitespace and citation normalization; its ending matches the UI. Expanded activity and helper details were not captured. Outputs panel says no outputs yet; archive availability otherwise unknown. No native database-byte identity is claimed.

**The full compiler is still not established, and I do not have a universal negative.** There is, however, a new result beyond the supplied premises: the prepared weak-packet window can be placed on an arbitrary unknown smooth joint background, with an actual endpoint estimate that preserves that background and clears the unwanted output. Its errors can be accumulated without multiplying a fixed stability constant at every write.

I also obtain a coupled internal operation encoding \((\nu+\rho)r\) from a prepared odd register \(r\). Together with the supplied \(\rho r\) operation, this addresses the additional \(\nu^2\rho\) normalization that appears in one proposed reload mechanism.

The unresolved physical step is **loading or regenerating the packets from unknown registers while preserving the velocity already computed**. The results below do not silently supply that operation.

## 1. A prepared weak-packet window on an unknown background

Write
\[
B=H+b,\qquad z=(u,b),\qquad \mu=\min(\nu_-,\rho_-).
\]
Let \(\mathbb S_H(t,s)\) denote the exact non-autonomous linear evolution around the constant magnetic mean:
\[
\begin{aligned}
u_t&=\nu(t)\Delta u+(H\cdot\nabla)b,\\
b_t&=\rho(t)\Delta b+(H\cdot\nabla)u.
\end{aligned}
\]
Its Fourier blocks obey
\[
\|\mathbb S_H(t,s;k)\|
\le e^{-\mu\kappa^2|k|^2(t-s)},\qquad \kappa=2\pi.
\tag{1}
\]

Consider an already prepared initial state
\[
z(0)=z_0+p_Q,
\]
where \(z_0\) is the unknown background and \(p_Q\) is initially magnetic.

For the first version of the estimate, suppose
\[
\operatorname{supp}\widehat z_0\subset\{|k|\le F_0\},
\qquad
\|z_0\|_{X^0}\le P_0,\qquad
\|z_0\|_{X^1}\le P_1.
\]
The packet frequencies have the form
\[
k_j=Q\ell_j+\omega_j,\qquad
\ell_j\in\mathbb Z^3\setminus\{0\},\quad
|\ell_j|\le J,\quad |\omega_j|\le F_p,
\tag{2}
\]
including real conjugates, and
\[
\|p_Q\|_{X^{-1}}\le \sigma.
\]

The carrier-offset form (2) is a finite, checkable condition on the constructed packet list. It is useful because nonlinear interactions either cancel their integer carrier labels or remain at high frequency.

Define
\[
\gamma_0=\sqrt\mu\,P_0\sqrt T,\qquad
\vartheta=\frac{C(\sigma+\gamma_0)}{\mu}.
\]
Assume
\[
\vartheta\le\frac14,\qquad
P_0^2T\le c\sigma,\qquad P_1T\le1.
\tag{3}
\]

Let
\[
\mathcal Q_Q(T)
=
\mathfrak B\bigl(\mathbb S_H(\cdot,0)p_Q,
                 \mathbb S_H(\cdot,0)p_Q\bigr)(T)
\tag{4}
\]
be the exact quadratic term in the coupled MHD Duhamel expansion. This expression is proof notation; the compiler does not evaluate the coefficient histories in it.

Choose a logarithmic expansion cutoff \(n_*\), with
\[
Q\ge4n_*\max(F_0,F_p),
\]
and a rational duration of the form
\[
T\asymp
\frac{n_*\log\!\bigl(\operatorname{poly}(JQ,\mu^{-1},\zeta^{-1})\bigr)}
{\mu Q^2}.
\tag{5}
\]

Then the **actual unforced coupled endpoint** satisfies
\[
\boxed{
z(T)=
\mathbb S_H(T,0)z_0+
P_{\le2F_p}\mathcal Q_Q(T)+\mathcal E,
}
\tag{6}
\]
where
\[
\boxed{
\begin{aligned}
\|\mathcal E\|_{H^1}\le{}&
C\zeta+
C(1+F_p)^2\frac{\sigma^3}{\mu^2}\\
&+
C(1+\max(F_0,F_p))^2
\left[
\sigma P_0\sqrt{\frac T\mu}+P_0^2T
\right].
\end{aligned}
}
\tag{7}
\]

The projection in (6) identifies the intended quadratic signal. **It is not applied to the physical state.** All remaining physical frequencies are included in \(\mathcal E\), whose complete \(H^1\) norm is bounded.

Thus, once the packet is present, the window:

- retains the old joint background up to its contractive short linear evolution;
- adds the pure-packet quadratic slow signal;
- clears the unwanted carrier output;
- pays every mixed Lorentz and induction interaction with the old background.

The proof does not freeze \(\nu\) or \(\rho\). Their positive bounds suffice for this window.

### 1.1 Why a large background does not invalidate the expansion

The correct small quantity for the background is its short-time norm, not its initial \(X^{-1}\) norm.

Put
\[
\gamma(v)=\sqrt\mu\,\|v\|_{L^2(0,T;X^0)}.
\]
Interpolation gives
\[
\gamma(v)^2
\le
\left(\sup_t\|v(t)\|_{X^{-1}}\right)
\left(\mu\int_0^T\|v(t)\|_{X^1}\,dt\right)
\le\frac14\|v\|_{E_T}^2.
\tag{8}
\]
Your accepted bilinear estimate therefore implies
\[
\|\mathfrak B(v,w)\|_{E_T}
+\gamma(\mathfrak B(v,w))
\le C\mu^{-1}\gamma(v)\gamma(w).
\tag{9}
\]

For the free packet and background,
\[
\gamma(\mathbb S_Hp_Q)\le C\sigma,\qquad
\gamma(\mathbb S_Hz_0)\le\sqrt\mu P_0\sqrt T.
\tag{10}
\]

Contraction takes place in this short-time space. The potentially large linear background is retained exactly as \(\mathbb S_Hz_0\); it is not falsely charged as a small critical-norm term.

Colour each leaf of the homogeneous expansion according to whether it originates from \(p_Q\) or \(z_0\). An \(n\)-leaf nonlinear term has the majorant
\[
C^{n-1}\mu^{1-n}(\sigma+\gamma_0)^n.
\]
The sum of terms with at least one background leaf is bounded by
\[
\begin{aligned}
&\sum_{n\ge2}C^{n-1}\mu^{1-n}
\bigl[(\sigma+\gamma_0)^n-\sigma^n\bigr]\\
&\hspace{2cm}\le
C\left[
\sigma P_0\sqrt{T/\mu}+P_0^2T
\right].
\end{aligned}
\tag{11}
\]

This estimates all mixed trees, including interactions involving the already-written velocity. It is not a calculation of one nominated interaction.

### 1.2 Carrier labels pay the slow remainder without a growing cutoff factor

Retain the carrier label \(\ell_j\) of each packet leaf. Background leaves have carrier label zero.

An \(n\)-leaf term whose total carrier label is zero has frequency at most

\[
nF_p
\]
for a pure-packet term, and at most
\[
n\max(F_0,F_p)
\]
for a mixed term.

On a frequency band of radius \(F\),
\[
\|v\|_{H^1}\le C(1+F)^2\|v\|_{X^{-1}}.
\tag{12}
\]

Apply this at each homogeneous order, then sum. The factors \(n^2\) are summable against the geometric majorant. Consequently, the slow pure-packet remainder is
\[
C(1+F_p)^2\sigma^3/\mu^2,
\]
with no factor \(n_*^2\). The analogous argument gives the mixed term in (7).

Keeping \(F_p\), rather than the background cutoff \(F_0\), in the pure-packet error is important for the parameter hierarchy below.

### 1.3 The high-frequency clearing argument survives the background

At every time slice of an \(n\)-leaf tree, the active frequencies sum to the output frequency \(m\). Therefore
\[
\sum_{\mathrm{active}}|k_e|^2\ge\frac{|m|^2}{n}.
\tag{13}
\]

For \(|m|\ge Q/2\), this gives \(Q^2/(4n)\).

Half of the scalar heat can be factored out of every exact coupled propagator. The remaining evolution has diffusivities \(\nu-\mu/2,\rho-\mu/2\), both still positive, and the same skew-Hermitian \(H\)-coupling. It remains contractive even when the time-dependent matrices do not commute.

An \(n\)-leaf high output thus gains
\[
e^{-c\mu Q^2T/n}.
\tag{14}
\]

The support of the \(n\)-leaf term is at most \(CnJQ\), so its entire \(H^1\) norm is bounded using \((nJQ)^2\) times its \(X^{-1}\) majorant. The complete tail beyond \(n_*\) satisfies
\[
\sum_{n>n_*}\|z_n(T)\|_{H^1}
\le
C(JQ)^2\mu(n_*+1)^2\vartheta^{n_*+1}.
\tag{15}
\]

A logarithmic \(n_*\) pays (15); the duration (5) pays the remaining high-output terms.

For \(n\le n_*\), a nonzero carrier label puts the output above \(Q/2\). A zero carrier label puts it in the explicitly bounded slow band. Orders beyond \(n_*\) are controlled in the whole space. No intermediate-frequency region is omitted.

## 2. Smooth backgrounds, rough errors and every weak realization

The finite-band restriction on \(z_0\) can be removed with a fixed-order smooth envelope.

First observe that (3) and the expansion give
\[
\int_0^T
\bigl(\|\nabla u_{\rm ref}\|_\infty+
      \|\nabla b_{\rm ref}\|_\infty\bigr)\,dt
\le CP_1T+C\sigma/\mu\le C.
\tag{16}
\]

This is an estimate on the actual coupled reference. It yields polynomial fixed-order Sobolev bounds:
\[
\sup_{t\le T}\|z_{\rm ref}(t)\|_{H^m}
\le
C_m\left(\|z_0\|_{H^m}+(JQ)^{m+1}\sigma\right).
\tag{17}
\]

The exponential in the differentiated energy argument is an exponential of the bounded quantity in (16), not an exponential of the input envelope or frequency.

### 2.1 Two-norm perturbation estimate

Let \(e_0,e_1\) be incoming joint \(L^2,H^1\) errors. Relative energy gives
\[
\sup_{t\le T}E_0(t)\le C(e_0+\eta T).
\tag{18}
\]

The differentiated comparison can be arranged as
\[
\begin{aligned}
(E_1^2)'+\mu E_2^2
\le{}&
CG_1(t)E_1^2+CG_2(t)E_0E_1\\
&+C\mu^{-3}E_1^6+C\eta^2/\mu,
\end{aligned}
\tag{19}
\]
where
\[
G_1=\|\nabla z_{\rm ref}\|_\infty,\qquad
G_2=\|D^2z_{\rm ref}\|_\infty.
\]

Here \(\int G_1\le C\), while
\[
G_*:=\int_0^TG_2(t)\,dt
\le CT\left(P_4+(JQ)^5\sigma\right)
\tag{20}
\]
is polynomial. A bootstrap gives
\[
\boxed{
E_1(T)\le
C\left[
e_1+G_*(e_0+\eta T)+\eta\sqrt{T/\mu}
\right].
}
\tag{21}
\]

The bracket must lie in the corresponding inverse-polynomial continuation ball. Crucially, the second reference derivatives multiply the already-controlled \(L^2\) error; they do not introduce another exponential.

This permits arbitrary spatial modes in the disturbance. Strong continuation of the disturbed solution, followed by weak–strong uniqueness, covers every corresponding Leray–Hopf realization. On this completed window, the strong endpoint agrees with the specified one-sided energy trace.

### 2.2 A concrete noncircular smooth-background cutoff

Take
\[
Q=q^4
\]
and truncate the unknown smooth background only in the proof at frequency \(q\). A supplied \(H^{24}\) envelope \(P_{24}\) gives
\[
e_0\le CP_{24}q^{-24},\qquad
e_1\le CP_{24}q^{-23}.
\]

Since \(T\) is of order \(\log^2q/(\mu q^8)\), (20) grows at most as a fixed polynomial times \(q^{12}\log^2q\). The propagated tail is therefore bounded by
\[
\operatorname{poly}(P_{24},J,\mu^{-1},\sigma)
\left(q^{-23}+q^{-12}\log^2q\right).
\tag{22}
\]

The omitted linear background is added back using the \(H^1\) contraction of \(\mathbb S_H\).

The mixed error in (7) becomes, once \(q\ge F_p\),
\[
O\!\left(
\operatorname{poly}\,
\sigma P_0q^{-2}\log q/\mu
+
\operatorname{poly}\,
P_0^2q^{-6}\log^2q/\mu
\right).
\tag{23}
\]

Meanwhile the pure-packet error remains
\[
C(1+F_p)^2\sigma^3/\mu^2,
\]
independent of \(q\).

Thus the order of choices is valid:

1. choose \(\sigma\) and the number of writes from the pure-packet budget;
2. choose the smoothing and local-error budgets;
3. compute the resulting fixed-order reference envelope;
4. choose \(q\) last.

There is no degree-dependent Sobolev order or precision cycle here.

## 3. Physical smoothing retains historical errors

Before a prepared write, suppose the actual incoming state has a known joint \(H^1\) envelope \(P\). Run a genuine unforced interval
\[
s\le c\mu^3P^{-4}.
\]

Define the zero-disturbance reference from that same actual state. Local \(H^1\) control and the mild equation give
\[
\boxed{
\|z^0(s)-\mathbb S_H(s,0)z_{\rm in}\|_{H^1}
\le CP^2\mu^{-3/4}s^{1/4}.
}
\tag{24}
\]
The actual disturbance adds
\[
C\eta\sqrt{s/\mu}.
\]

Positive-time spatial smoothing supplies an \(H^{24}\) envelope polynomial in \(P,\mu^{-1},s^{-1}\). Spatial differentiation does not require higher time regularity of \(\nu,\rho\).

This is a legitimate way to restart the proof reference:

- the physical state undergoes real unforced evolution;
- the reference begins from the actual incoming state;
- all historical errors remain in \(\mathbb S_H(s,0)z_{\rm in}\);
- no projection deletes them.

It is consequently possible to seek a complete write estimate of the form
\[
z_{i+1}
=
\mathbb S_H(t_{i+1},t_i)z_i
+\text{intended packet signal from the actual registers}
+\text{absolute local error}.
\tag{25}
\]

The new weak-window result supplies the unforced part of this estimate. It does not supply the intervening packet preparation.

## 4. Polynomially many weak writes need not incur a constant to the number of writes

Suppose the missing preparation operation has been supplied and the normalized signal has the intended triangular dependence: it changes velocity using the odd registers, while leaving those registers unchanged up to the local budget.

There is a minor but important complication: \(\mathbb S_H\) mixes velocity and magnetic errors. It is jointly contractive, but it is not componentwise identity.

Its off-diagonal blocks satisfy
\[
\|\mathbb S_H^{ub}(t,s)\|_{H^1\to H^1}
+
\|\mathbb S_H^{bu}(t,s)\|_{H^1\to H^1}
\le CM\sqrt{(t-s)/\mu}.
\tag{26}
\]
This follows by Duhamel around diagonal heat and maximizing
\[
M|k|(t-s)e^{-c\mu|k|^2(t-s)}.
\]

Let \(\alpha_i\) bound the intended transfer of magnetic-register error into the \(i\)-th velocity increment. For a weak quadratic write,
\[
\alpha_i=\sigma^2\operatorname{poly}(\text{signal envelope},\mu^{-1}).
\]
Set
\[
A_0=\sum_i\alpha_i,\qquad
B_0=\sum_i CM\sqrt{t_i/\mu}.
\]

Choose the prescribed durations so that
\[
B_0\le \frac{c}{1+A_0}.
\tag{27}
\]
In the weighted error norm
\[
E_u+(1+A_0)E_B,
\tag{28}
\]
the total multiplicative factor is bounded by
\[
\exp\!\left(
C\left[(1+A_0)B_0+\frac{A_0}{1+A_0}\right]
\right)\le e^C.
\tag{29}
\]

The metric condition number is polynomial. This pays the reverse Alfvén transfer without producing \(\exp(A_0)\).

For \(N\) writes of order \(\sigma^2\), the total pure-packet remainder is
\[
N\,O\!\left((1+F_p)^2\sigma^3/\mu^2\right).
\]
When \(N=\operatorname{poly}(R)/\sigma^2\), inverse-polynomial \(\sigma\) suffices. The mixed errors, smoothing errors and condition (27) are then paid by choosing the final carrier frequency large enough.

All logarithms in these choices can be replaced by integer bit-length bounds and geometric-series tests. No tree enumeration, coefficient-history evaluation or norm oracle is required.

This closes a genuine iteration issue **conditional on a physical loading operation with the stated endpoint action**. It does not prove that operation.

## 5. An actual internal multiplication by \(\nu+\rho\)

A separate calculation gives a useful normalization operation from a prepared register.

Use coordinates \((x,y,z)\), put
\[
s(y)=\sin(\kappa y),\qquad c(y)=s'(y),
\]
and prepare
\[
u(0)=e_1s(y),\qquad
B(0)=\bigl(H_1,H_2+r(z),H_3\bigr),
\]
where \(r\) is an unknown smooth mean-zero odd register bank.

Apply no force during the short window.

### 5.1 The sector is an exact coupled MHD sector

The full equations preserve
\[
u=(w(y,z,t),v(z,t),0),
\]
\[
B=(H_1+d(y,z,t),H_2+b(z,t),H_3).
\]

The exact equations are
\[
v_t=\nu(t)v_{zz}+H_3b_z,\qquad
b_t=\rho(t)b_{zz}+H_3v_z,
\tag{30}
\]
and
\[
\begin{aligned}
w_t&=\nu(t)\Delta w-vw_y+(H_2+b)d_y+H_3d_z,\\
d_t&=\rho(t)\Delta d-vd_y+(H_2+b)w_y+H_3w_z.
\end{aligned}
\tag{31}
\]

There is no omitted pressure correction: these nonlinear vector fields are divergence free in this ansatz. Lorentz backreaction is included in (30)–(31).

Let
\[
N(t)=\int_0^t\nu(s)\,ds,\qquad
R(t)=\int_0^t\rho(s)\,ds.
\]
Duhamel expansion on a polynomially short interval gives
\[
b(t)=r+R(t)r''+O_{H^m}(P^Ct^2),
\]
\[
w(t)=s-\kappa^2N(t)s+O_{H^{m+1}}(P^Ct^2).
\]

For \(d\),
\[
\begin{aligned}
d(t)={}&tc(H_2+r)+tR(t)c\,r''\\
&-\kappa^2c(H_2+r)
\left[
\int_0^t(t-s)\nu(s)\,ds+
\int_0^t s\rho(s)\,ds
\right]\\
&+O_{H^m}(P^Ct^3).
\end{aligned}
\tag{32}
\]

The code Laplacian cancels in
\[
tc(H_2+b(t))-d(t).
\]

### 5.2 The factor multiplies the entire register bank

Let \(\mathcal E\) extract the \(c(y)\) quadrature and retain the nonzero \(z\)-code frequencies, normalized so that \(\mathcal E(cr)=r\). Then
\[
\boxed{
\frac{2}{\kappa^2t^2}
\left[t\,b(t)-\mathcal E d(t)\right]
=
\alpha_t r+O_{H^m}(P^Ct),
}
\tag{33}
\]
where
\[
\alpha_t=
\frac2{t^2}
\left[
\int_0^t(t-s)\nu(s)\,ds+
\int_0^t s\rho(s)\,ds
\right].
\tag{34}
\]

For a window starting at \(t_0\),
\[
|\alpha_t-\nu(t_0)-\rho(t_0)|\le\Lambda t.
\tag{35}
\]

No derivative of either coefficient is used. No actual coefficient value is read, estimated numerically or inserted into the force.

The extraction in (33) is a known linear code operation. **It is not a new actuator.** Its physical implementation must use the magnetic routing/restore mechanism. The \(t^{-2}\) gain requires prepared-state and routing errors of order \(\delta t^2\), which is still a fixed polynomial precision requirement.

An idle copy can be placed in a separate \(y\)-independent \(x\)-component code: the zero and nonzero \(y\)-Fourier sectors of (31) separate, and the idle copy undergoes only a short diffusion–Alfvén evolution. This avoids assuming that the original register is observed or recreated.

With physical routing in place, the admitted internal \(\rho r\) operation and (33) give
\[
(\nu+\rho)r-\rho r=\nu r
\]
up to the assigned errors. A fixed number of stages can prepare \(\nu^2\rho\,r\). Keeping these stages and the subsequent readout in a sufficiently short interval pays the Lipschitz drift of the factors.

### 5.3 Why \(\nu^2\rho\) arises in a reload proposal

For a frozen fast Alfvén/Stokes pair
\[
X'=-\nu X-\lambda Z,\qquad
Z'=\lambda X-\rho Z,\qquad X(0)=1,\ Z(0)=0,
\]
a direct energy calculation gives
\[
\int_0^\infty(Z^2-X^2)\,ds
=
-\frac{\rho}{2(\nu\rho+\lambda^2)}.
\]
Subtracting the zero-coupling value yields
\[
\boxed{
\frac{\lambda^2}{2\nu(\nu\rho+\lambda^2)}
=
\frac{\lambda^2}{2\nu^2\rho}+O(\lambda^4).
}
\tag{36}
\]

Thus the induced Maxwell stress alone is not the whole leading response. The Lorentz correction to the velocity stress contributes at the same order. For this reload design, the correct leading normalization is \(1/(\nu^2\rho)\).

Equation (33) supplies an internal way to form the compensating factor. It does not by itself supply the reload design.

## 6. The remaining physical problem

The required operation is approximately
\[
(u,B)\longmapsto (u,B)+p_Q(r),
\tag{37}
\]
where \(r\) denotes unknown values already stored in magnetic registers.

Its force may depend on the known encoding and on norm envelopes, but it may not evaluate \(r\). It must preserve the existing unknown velocity, retain the needed magnetic registers, and return—after the weak window—to a background envelope independent of \(Q\).

The accepted joint-memory increments add **known velocity fields**. They do not imply (37). The accepted setters and heat services may erase the velocity, so they cannot simply be inserted after an even response has been written.

I examined two possible ways around this.

**A permanent amplified parallel bank.** A bank
\[
B_{\rm bank}=H+A_0r(y,z)e_1
\]
has a vanishing self-Lorentz term. Known weak velocity pulses can regenerate magnetic packets from it, potentially avoiding a magnetic-only loading service.

But the generic background estimate cannot be used unchanged when \(A_0\) grows with \(Q\). For instance, \(A_0\sim Q\sqrt{s}\) makes \(P_0^2T\) of order \(s\) per cell, which is too large over order \(s^{-2}\) writes. The parallel geometry cancels some of that bound; all retained-memory interactions and final bank removal still need a structural estimate. I have not proved it.

**One weak write followed by Euler-only amplification.** The inverse of the accepted contracting word preserves the ideal magnetic transport. However, its compact generator has a small gap at high target frequencies. Amplifying a variable target band by this inverse can create exponentially large gain on lower-frequency errors.

A spectrally flattened family of such words could avoid that problem, but its required symbol bounds do not follow from the supplied integer-lattice contraction estimate. I have not constructed that family.

Neither issue is a universal obstruction. They identify why these particular constructions are incomplete.

## 7. Relation to the literature

The new prepared-window argument uses your accepted coupled Fourier estimate. Lei–Lin’s original theorem is for constant-viscosity Navier–Stokes on \(\mathbb R^3\); its proof explains the critical Fourier norm and integrated-gradient mechanism, but it is not the non-autonomous MHD control theorem asserted here. [arxiv.org](https://arxiv.org/pdf/1203.2699?utm_source=chatgpt.com)

Gérard-Varet’s oscillatory MHD work treats actual nonlinear stability and instability around specified oscillatory velocity profiles, with \(\mathrm{Re}=\mathrm{Rm}=1\). It supports investigating complete low/high-frequency estimates, but does not supply packet loading, unknown-register routing or the requested compiler costs. [dgerardv.github.io](https://dgerardv.github.io/files/go_roberts.pdf?utm_source=chatgpt.com)

The derivations above therefore remain separated from those papers’ theorems.

## Status

The new weak-window estimate removes the previously explicit limitation to a pure-packet reference. It handles an unknown smooth joint background, physically bounds the complete endpoint remainder, admits polynomial rough-error budgets, and supports a stable accumulation metric. The coupled identity (33) adds a whole-register route to viscosity-factor normalization.

**The entire nonlinear-response compiler remains unresolved here.** Actual register execution and, especially, packet loading or an alternative final readout must still preserve the unknown computed velocity with the same global polynomial error contract. Until that physical step is proved and assembled, I cannot provide valid universal \(A,p\) for the full claim; I also have no argument ruling out all admitted programmes.
