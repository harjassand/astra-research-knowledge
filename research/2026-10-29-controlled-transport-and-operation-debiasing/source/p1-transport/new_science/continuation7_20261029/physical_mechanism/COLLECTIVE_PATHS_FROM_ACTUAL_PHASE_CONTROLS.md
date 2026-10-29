# Collective density paths from actual phase controls

29 October 2026. Complementary construction within the existing physical-mechanism role. Earlier files remain unchanged. This is an ordinary-controller comparison, not a priority or apparatus claim. The main proofs below are self-contained.

## 1. Outcome and the changed comparison

The round5 failure of a volume-independent quadratic mirror bound on *all microscopic observables* does not prevent an ordinary deterministic actuator from controlling an entire empirical density trajectory.

For a conserving nearest-neighbor ring with bounded, unknown, configuration-dependent rate amplitudes, an actual uniform rotation of all modulation phases yields the ordinary heat equation on the diffusive clock whenever

\[
\frac{D_N}{\Omega_N}\longrightarrow0. \tag{1}
\]

Here \(D_N\) bounds the number of local current summands changed by one particle exchange. A fixed finite interaction range has \(D_N=O(1)\). Its rotation speed can tend to infinity arbitrarily slowly with volume. A global pi-pulse cycle gives the same conclusion when its physical half-period \(h_N\) satisfies \(h_ND_N\to0\). No invariant linear observable sector is assumed. The proof controls a path on every fixed macroscopic time interval, not merely an equilibrium endpoint correlation.

The deterministic construction allows arbitrary fixed initial phases and frozen hidden information, arbitrary retained calibration data compatible with the declared future native generator, and every deterministic visible configuration associated with the desired initial density profile. It needs no phase equilibrium, phase reset, erased initial control key, or visible equilibrium preparation.

There is a stronger ordinary randomized supplier if *independent local pi shifts* are actual operations. Independent Poisson pi kicks at rate \(\gamma_N\) produce the same empirical heat path for **any** \(\gamma_N\to\infty\), including arbitrary nonlocal dependence of the amplitudes on the unchanged visible context. The signs may all start deterministically at +1. An entropy cost of \(N\log2\), rather than a product-initialization identity, is enough for this macroscopic statement.

Neither control follows from a noise-only diffusion interface. A deterministic rotation, local pi actuator, and uniform phase refresh remain separate suppliers. The strongest matched ordinary controller gets the same capability once given that supplier.

## 2. Exact native model and information interface

There are \(N\) sites on a periodic one-dimensional lattice. A configuration is \(\eta\in\{0,1\}^N\). Write \(\eta^i\) for exchange of sites \(i,i+1\), with periodic indices. For a fixed particle number, let \(\pi_N\) be uniform on that sector. The generator convention in this note is negative-semidefinite Markov convention.

The actual native generator, conditional on frozen \(z\), is

\[
L_\theta f(\eta)=c\sum_i[1+\alpha_i(\eta,z)\cos\theta_i]
                      [f(\eta^i)-f(\eta)],\qquad c=s/2, \tag{2}
\]

where \(s>0\) is the homogeneous mean rate and

\[
|\alpha_i|\le\alpha<1,\qquad \alpha_i(\eta^i,z)=\alpha_i(\eta,z). \tag{3}
\]

The amplitude can depend on all other occupations and on arbitrary frozen hidden information. Equation (3), not merely knowledge of the equilibrium weights, supplies reversibility of each actual native generator. Every phase is unchanged by native particle motion. The mean generator is

\[
L_0=c\sum_i(\tau_i-I),\qquad (\tau_i f)(\eta)=f(\eta^i). \tag{4}
\]

It is SSEP with swap rate \(c\). Its macroscopic equation is

\[
\partial_t\rho=c\,\partial_x^2\rho. \tag{5}
\]

Times in (2) are physical times. The empirical density path is

\[
\mathsf\pi_t^N=\frac1N\sum_i\eta_i(N^2t)\delta_{i/N},\quad 0\le t\le T. \tag{6}
\]

The actual phase control must leave \(\eta,z\) unchanged and preserve (2) during its execution. A prescribed continuous phase velocity changes (2) continuously. An ideal pi pulse is instantaneous in the declared model; a finite pulse needs its actual waveform. Uncontrolled additional phase drift or diffusion is not automatically covered by the deterministic proof.

All constants below are uniform in \(z\) and in initial phase offsets. They may therefore be conditioned on an old record \(D\) which fixes or correlates these quantities. The native future must still have the asserted conditional Markov law. There is no assumption that recorded old information is statistically independent of the initial visible state.

## 3. The macroscopic current observable

For a real smooth periodic test function \(\varphi\), put

\[
F_N(\eta)=\frac1N\sum_i\varphi(i/N)\eta_i,\qquad A=\|\varphi'\|_\infty.
\]

If an actual sign protocol makes the rates \(c(1+q(t)b_i(\eta))\), with \(|b_i|\le\alpha\), \(b_i(\eta^i)=b_i(\eta)\), write \(L_t=L_0+q(t)B\) and

\[
V_N=NBF_N
=c\sum_i b_i(\eta)\,[\varphi((i+1)/N)-\varphi(i/N)]\,(\eta_i-\eta_{i+1}). \tag{7}
\]

Thus

\[
\|V_N\|_\infty\le v:=c\alpha A. \tag{8}
\]

Let \(D_N\ge1\) bound, for every exchange \(j\), the number of summands in (7) which can change. This count includes summands whose occupation difference changes, as well as summands whose coefficient changes. A fixed interaction range gives a constant \(D_N\); without any locality assumption one may take \(D_N=N\).

For every \(j,\eta\),

\[
|\Delta_jV_N|\le d_N:=\frac{2c\alpha A D_N}{N}. \tag{9}
\]

Every native jump rate is at most \(c_*:=c(1+\alpha)\). Hence

\[
\sup_{t,\eta}\sum_j c_j(t,\eta)|\Delta_jV_N|^2
\le g_N:=\frac{4c_*c^2\alpha^2A^2D_N^2}{N}. \tag{10}
\]

A sharper measured or structural influence estimate may replace (9)-(10). Merely having local sensors does not certify a local influence graph.

## 4. A general oscillatory-potential lemma

Let \(L_t\) be any finite-state, time-dependent generator reversible in one fixed probability \(\pi\). Let \(V\) be multiplication by a real function and let \(q=Q'\), \(Q(0)=0\), \(|Q(t)|\le H\). Assume

\[
\|V\|_\infty\le v,\quad |\Delta V|\le d,\quad
\sup_{t,x}\sum_{x'}c_t(x,x')\,[V(x')-V(x)]^2\le g.
\]

Then, for \(a\ge0\),

\[
\log\mathbb E_\pi\exp\!\left(a\int_0^tq(u)V(X_u)\,du\right)
\le aHv+\frac{a^2H^2g}{2}\,e^{aHd}\,t. \tag{11}
\]

The same bound holds with \(a\) replaced by \(-a\). The time dependence of \(L_t\) may be correlated with the prescribed drive \(q\). There is no commutation premise.

### Proof

The unnormalized Feynman–Kac density started at \(\pi\) solves

\[
\dot u=(L_t+a q(t)V)u,\qquad u(0)=1.
\]

Write \(u=e^{aQ(t)V}w\). The potential cancels exactly:

\[
\dot w=e^{-aQV}L_te^{aQV}w. \tag{12}
\]

For an arbitrary real multiplication function \(W\), reversibility gives

\[
\begin{aligned}
\langle w,e^{-W}L_te^Ww\rangle_\pi
={}&-\frac12\sum_{x,x'}\pi(x)c_t(x,x')[w(x')-w(x)]^2\\
&+\sum_{x,x'}\pi(x)c_t(x,x')
 [\cosh(W(x')-W(x))-1]w(x)w(x').
\end{aligned} \tag{13}
\]

Using \(2ww'\le w^2+(w')^2\), the last expression is at most

\[
\sup_x\sum_{x'}c_t(x,x')[\cosh(\Delta W)-1]\,\|w\|_2^2.
\]

Since \(\cosh r-1\le r^2e^{|r|}/2\), (12) implies

\[
\|w(t)\|_2\le
\exp\!\left(\frac{a^2H^2g}{2}e^{aHd}t\right).
\]

Finally \(\langle1,u(t)\rangle\le e^{aHv}\|w(t)\|_2\). This proves (11). This is the ordinary exponential-conjugation/Davies method with a time-dependent potential chosen to cancel the drive, not a new semigroup technique. The source comparison below identifies the predecessor explicitly.

## 5. Actual global pi cycles: a whole-path bound

Use the actual symmetric schedule

\[
+\text{ for }h/2,\quad -\text{ for }h,\quad +\text{ for }h/2,
\]

repeated with period \(2h\). A global pi pulse changes every cosine's sign. Its primitive has \(|Q|\le h/2\), \(Q(0)=0\). Initial phase offsets are arbitrary and absorbed into \(b_i=\alpha_i\cos\theta_i(0)\).

Define the drift error on the entire macroscopic path by

\[
R_N(t)=\int_0^{N^2t}q(u)BF_N(\eta_u)\,du
      =\frac1N\int_0^{N^2t}q(u)V_N(\eta_u)\,du. \tag{14}
\]

By (11), for every \(t\le T\),

\[
\log\mathbb E_{\pi_N}e^{\pm aNR_N(t)}
\le C_N(a):=\frac{ahv}{2}
 +\frac{a^2h^2g_NN^2T}{8}e^{ahd_N/2}. \tag{15}
\]

This becomes a uniform-path bound without an unproved maximal-semigroup assertion. Equation (8) gives the deterministic Lipschitz bound

\[
|R_N(t)-R_N(u)|\le Nv|t-u|. \tag{16}
\]

Use a grid on \([0,T]\) of spacing at most \(\delta/(2Nv)\), with

\[
K_N\le2+\left\lceil2NvT/\delta\right\rceil
\]

points (if \(v=0\), the residual is zero). A union bound and (15) give

\[
\mathbb P_{\pi_N}\!\left(\sup_{t\le T}|R_N(t)|>\delta\right)
\le2K_N\exp[-aN\delta/2+C_N(a)]. \tag{17}
\]

For any initial law \(\rho_N\), the path relative entropy against this same controlled process started at \(\pi_N\) is exactly \(H(\rho_N\mid\pi_N)\). Data processing to an event gives

\[
\mathbb P_{\rho_N}(E)
\le\frac{H(\rho_N\mid\pi_N)+\log2}{\log(1/\mathbb P_{\pi_N}(E))}. \tag{18}
\]

For a fixed conserved sector, **every** initial law has

\[
H(\rho_N\mid\pi_N)\le\log\binom N{M}\le N\log2. \tag{19}
\]

This includes a point mass. No equilibration operation was used to obtain (19).

Set \(a=(hD_N)^{-1}\), with time measured in the fixed native-rate units. Then

\[
C_N(a)\le\frac{v}{2D_N}
 +\frac{c_*c^2\alpha^2A^2NT}{2}
   \exp(c\alpha A/N). \tag{20}
\]

The positive term in the exponent of (17) is \(N\delta/(2hD_N)\). Therefore, if \(h_ND_N\to0\), (17)-(20) prove

\[
\sup_{\rho_N,z,\theta(0)}
\mathbb P\!\left(\sup_{t\le T}|R_N(t)|>\delta\right)\longrightarrow0. \tag{21}
\]

For fixed \(T,\delta,\varphi\), the elementary entropy estimate has order \(h_ND_N\) once the displayed denominator is positive. This is a conservative sufficient bound, not a sharp finite-volume error law. Restoring units replaces a small period by its ratio to the fixed native timescale, such as \(s h_N\).

## 6. Continuous deterministic rotation also works

Suppose an actual actuator imposes

\[
\theta_i(t)=\theta_i(0)+\Omega t
\]

for all sites while leaving \(\eta,z\) unchanged. No phase sensing or absolute setting is needed. Decompose

\[
\alpha_i\cos(\theta_i(0)+\Omega t)
=b_i\cos\Omega t+d_i\sin\Omega t,
\]

where \(b_i=\alpha_i\cos\theta_i(0)\), \(d_i=-\alpha_i\sin\theta_i(0)\). Both are bounded by \(\alpha\), exchange-invariant, and have the same influence degree.

The current is \(\cos\Omega t\,V_N^b+\sin\Omega t\,V_N^d\). In the proof of (11), use the multiplication gauge

\[
W(t)=a\left[\frac{\sin\Omega t}{\Omega}V_N^b
       +\frac{1-\cos\Omega t}{\Omega}V_N^d\right]. \tag{22}
\]

The two multiplication operators commute, so its time derivative cancels the potential exactly. Now

\[
\|W\|_\infty\le3av/\Omega,\qquad
|\Delta_jW|\le3ad_N/\Omega.
\]

Equation (13) gives

\[
\log\mathbb E_{\pi_N}e^{\pm aNR_N(t)}
\le\frac{3av}{\Omega}
 +\frac{9a^2g_NN^2T}{2\Omega^2}e^{3ad_N/\Omega}. \tag{23}
\]

Use \(a=\Omega/D_N\), (18)-(19), and the same time grid. This proves (21) whenever \(D_N/\Omega_N\to0\). The schedule is not palindromic; a mirror is unnecessary for this macroscopic result. This also removes an ideal instantaneous-pulse premise when deterministic phase velocity is the actual supplier.

The proof does not assert that periodic rotation reverses native noise, or that it implements a phase-diffusion kernel. It controls only the averaged density path derived below.

## 7. From a current residual to the entire empirical heat path

For either deterministic supplier, Dynkin's formula gives

\[
F_N(\eta_{N^2t})=F_N(\eta_0)
 +\int_0^tN^2L_0F_N(\eta_{N^2u})du+R_N(t)+M_N(t). \tag{24}
\]

Each exchange changes \(F_N\) by at most \(A/N^2\), so

\[
\mathbb E\langle M_N\rangle_T
\le c_*A^2T/N,\qquad
\mathbb E\sup_{t\le T}|M_N(t)|^2\le4c_*A^2T/N. \tag{25}
\]

These bounds hold for every initial configuration and do not use equilibrium.

For a real sine or cosine Fourier mode with fixed integer \(m\),

\[
N^2L_0F_N=-\lambda_{m,N}F_N,
\qquad \lambda_{m,N}=sN^2[1-\cos(2\pi m/N)]. \tag{26}
\]

The integral equation (24) has the exact stability bound

\[
\sup_{t\le T}|F_N(\eta_{N^2t})-e^{-\lambda_{m,N}t}F_N(\eta_0)|
\le2\sup_{t\le T}|R_N(t)+M_N(t)|. \tag{27}
\]

Indeed, if \(E=R_N+M_N\), the difference is
\(E_t-\lambda_{m,N}\int_0^te^{-\lambda_{m,N}(t-u)}E_u du\).

Assume the actual initial empirical measures converge weakly in probability to \(\rho_0(x)dx\). The limit necessarily satisfies \(0\le\rho_0\le1\). Equations (21), (25)-(27), and \(\lambda_{m,N}\to2\pi^2s m^2\) imply simultaneous convergence of every fixed finite set of density modes, uniformly on \([0,T]\), to the heat solution (5).

To state the full measure path without hiding a topology, enumerate real trigonometric tests \(\psi_k\), including the constant, with \(\|\psi_k\|_\infty\le1\), and use

\[
d(\nu,\nu')=\sum_{k\ge1}2^{-k}\left|\int\psi_k\,d(\nu-\nu')\right|. \tag{28}
\]

On measures of mass at most one this metrizes weak convergence. A finite-mode truncation bounds the tail uniformly. Hence

\[
\sup_{t\le T}d(\mathsf\pi_t^N,\rho_t(x)dx)
\xrightarrow{\mathbb P}0. \tag{29}
\]

This is an entire empirical trajectory result on each fixed macroscopic horizon. It is neither a fluctuation-process theorem nor total variation approximation of the microscopic jump record. It also is not uniform over \(T=\infty\).

## 8. Independent Poisson pi kicks: arbitrary context and no sign preparation

Suppose an actual local phase operation adds pi to one selected \(\theta_i\), preserving \(\eta,z\) and all other phases. Use independent Poisson clocks of rate \(\gamma\), one per phase. Let \(\sigma_i\in\{-1,+1\}\) be the orientation relative to its original offset. The original offsets and \(z\) are frozen parameters; let \(b_i=\alpha_i\cos\theta_i(0)\). The actual joint generator is

\[
\mathcal Lf=c\sum_i(1+b_i(\eta)\sigma_i)[f(\eta^i,\sigma)-f(\eta,\sigma)]
 +\gamma\sum_i[f(\eta,F_i\sigma)-f(\eta,\sigma)]. \tag{30}
\]

It is reversible in \(\nu_N=\pi_N\otimes\text{Unif}\{-1,+1\}^N\), regardless of how nonlocally \(b_i\) depends on \(\eta\). Put

\[
V_N(\eta,\sigma)=\sum_i v_i(\eta)\sigma_i,
\quad v_i=c\,b_i(\eta)\,[\varphi((i+1)/N)-\varphi(i/N)](\eta_i-\eta_{i+1}).
\]

Then \(\sum_i\|v_i\|_\infty^2\le c^2\alpha^2A^2/N\). For a real \(g\) with \(\|g\|_2=1\), sign symmetry and Cauchy–Schwarz give

\[
\begin{aligned}
\langle V_Ng^2\rangle
&=\tfrac12\sum_i\langle v_i\sigma_i(g-F_ig)(g+F_ig)\rangle,\\
|\langle V_Ng^2\rangle|
&\le\left(\sum_i\|v_i\|_\infty^2\right)^{1/2}
        \left(\frac{2}{\gamma}\mathcal D_{\rm sign}(g)\right)^{1/2},\\
\mathcal D_{\rm sign}(g)&=\frac\gamma2\sum_i\|g-F_ig\|_2^2.
\end{aligned} \tag{31}
\]

Native reversibility contributes a nonnegative Dirichlet form. Optimizing the scalar square root in (31) therefore proves

\[
\lambda_{\max}(\mathcal L+aV_N)
\le\frac{a^2c^2\alpha^2A^2}{2\gamma N}. \tag{32}
\]

Consequently, for \(R_N(t)=N^{-1}\int_0^{N^2t}V_N(\eta_u,\sigma_u)du\),

\[
\log\mathbb E_{\nu_N}e^{\pm aNR_N(t)}
\le\frac{a^2c^2\alpha^2A^2NT}{2\gamma}. \tag{33}
\]

There is no initial product assumption in the receiving step. Every joint initial law of \((\eta,\sigma)\) has

\[
H(\rho_N\mid\nu_N)\le2N\log2. \tag{34}
\]

In particular, the *actual* initial signs can all be +1, deterministically and with that fact retained. We did not apply a fresh fair kick or discard a key. The equilibrium law in (33) is an auxiliary reference for a large-deviation estimate; (34) explicitly pays for the actual nonstationary initial condition.

Using the same grid, the reference probability that \(\sup|R_N|>\delta\) is at most

\[
2K_N\exp\left[-\frac{N\gamma\delta^2}{8c^2\alpha^2A^2T}\right], \tag{35}
\]

where the optimizing \(a\) is \(\gamma\delta/(2c^2\alpha^2A^2T)\). Equations (18), (34)-(35) imply residual convergence for every \(\gamma_N\to\infty\), with no influence-degree restriction. The martingale and Fourier proof (24)-(29) is unchanged. For fixed \(T,\delta\), the displayed entropy estimate has order \(1/(\gamma\delta^2)\) after its denominator is positive.

The future Poisson innovations must be fresh with the asserted conditional law given the old deployment record. If an old record already fixes the complete future clock path, the conditional Markov premise is unavailable. It is nevertheless permissible to *retain clock events as they occur*: (29) then holds with high probability under the same actual joint law of density and controller record. It does not say that every rare selected controller record has a good conditional density law.

### Full phase refresh, if actually supplied

An actual local refresh \(\theta_i\mapsto U_i\), with fresh independent uniform \(U_i\), at rate \(\gamma\) is a different actuator. The same variational proof, using the conditional phase averaging projection, gives a bound of the form (33), with at most twice its displayed coefficient. Arbitrary initial angles can be handled by a short actual refresh interval: by time \(u\), the probability that some phase has never refreshed is at most \(Ne^{-\gamma u}\). Conditional on every phase having refreshed, their marginal law is product uniform, although the visible configuration can be correlated with them. Since there are at most \(2^N\) visible configurations, the joint entropy relative to \(\pi_N\otimes\text{Unif}\) is at most \(N\log2\); no visible hold is needed for this entropy conclusion. The weak empirical variation during the interval has expectation at most \(c_*A u/N\). Taking, for example, \(u=3\log N/\gamma\) gives a negligible warm-up on the diffusive clock when \(\gamma_N\to\infty\). The full phase refresh operation and its random marks must actually exist; it is not supplied by relative pi access alone.

## 9. Why arbitrary global contexts remain a deterministic obstruction

The factor \(D_N\) is not safely removable merely because the target is a collective observable. An exact obstruction exists in the broader heat-bath family of round5. It does **not** establish sharpness of the sufficient scaling for the conserving nearest-neighbor SSEP family.

Take \(N\) visible spins \(y_i\in\{-1,+1\}\), uniform equilibrium, fair heat-bath projections \(E_i\), and the actual generator

\[
L_t=\sum_i\left[1+\alpha q(t)\prod_{j\ne i}y_j\right](E_i-I),
\qquad0<\alpha<1. \tag{36}
\]

Each multiplier is unchanged by its own update, so all native generators are reversible with the same product equilibrium. It is exactly the declared cosine family with original phases zero and global rotation \(q(t)=\cos\Omega t\), or global pi control \(q=\pm1\). Native rates remain bounded per site. The context influence degree is \(N\).

Let

\[
m_N=N^{-1}\sum_i y_i,\qquad p_N=\prod_i y_i.
\]

There is an exact two-observable closure:

\[
L_tm_N=-m_N-\alpha q(t)p_N,\qquad
L_tp_N=-Np_N-\alpha Nq(t)m_N. \tag{37}
\]

### Continuous rotation: exact crossover scale

Let \(q=\cos\Omega t\) and define

\[
u(t)=-\frac{\alpha[N\cos\Omega t-\Omega\sin\Omega t]}{N^2+\Omega^2},
\qquad G_N=m_N+u(t)p_N.
\]

Then \(u'-Nu=\alpha q\), so

\[
(\partial_t+L_t)G_N=-k_N(t)m_N,
\]

\[
k_N(t)=1-\frac{\alpha^2N^2}{N^2+\Omega^2}\cos^2\Omega t
       +\frac{\alpha^2N\Omega}{N^2+\Omega^2}\sin\Omega t\cos\Omega t. \tag{38}
\]

We have \(|G_N-m_N|\le\alpha/N\), \(1-\alpha^2\le k_N(t)\le1+\alpha^2\), and each native jump of \(G_N\) has magnitude at most \(2(1+\alpha)/N\). Its martingale quadratic variation up to fixed physical time \(T\) is at most

\[
2(1+\alpha)^3T/N. \tag{39}
\]

The deterministic comparison equation \(\dot x=-k_N(t)x\) is therefore the path limit up to an error tending to zero in probability, uniformly on fixed \([0,T]\), for every initial configuration with \(m_N(0)\to m_0\). This follows directly from the integral equation, (39), and Gronwall; no equilibrium initial condition is imposed.

The oscillatory part of \(\int_0^t k_N(u)du\) is bounded by a constant times \(1/\Omega\), uniformly in \(N,t\). Its mean is

\[
\bar k_N=1-\frac{\alpha^2N^2}{2(N^2+\Omega^2)}. \tag{40}
\]

Thus, if \(\Omega_N\to\infty\) and \(\Omega_N/N\to r\in[0,\infty]\),

\[
m_N(t)\ \longrightarrow\
m_0\exp\left[-\left(1-\frac{\alpha^2}{2(1+r^2)}\right)t\right]
\quad\text{uniformly in probability on }[0,T]. \tag{41}
\]

The mean native generator would predict \(m_0e^{-t}\). Every finite \(r\) leaves a nonzero mobility correction when \(m_0\ne0\). Consequently, rotation merely tending to infinity is insufficient in the unrestricted heat-bath family; \(\Omega_N/N\to\infty\) is necessary in this exact family. This matches the order of the influence-based sufficient condition, at the level of the broader class.

### Pi cycles

For \(q=\pm1\), use \(G_N=m_N-\alpha q p_N/N\) between pulses. Its drift is exactly \(-(1-\alpha^2)m_N\). Each pulse changes the corrector by at most \(2\alpha/N\). If the number of pulses on \([0,T]\) is \(o(N)\), equivalently \(Nh_N\to\infty\) for the stated cycle, then

\[
m_N(t)\longrightarrow m_0e^{-(1-\alpha^2)t}. \tag{42}
\]

The residual martingale again has order \(N^{-1/2}\). The collective failure is caused by fast configuration parity, not by the all-spin observable being the requested output: the requested output here is the ordinary empirical magnetization itself.

## 10. Actual records, costs, and limits of the capability

**Trajectory scope.** The result is convergence in probability in the uniform weak-measure path metric (28), over a fixed macroscopic horizon. Native jump times, microscopic occupancy paths, phase records, and fluctuations need not match those of SSEP. Persistent hidden information is neither reconstructed nor reset. A future controller record may be retained in the actual joint probability space, but rare-record postselection is not uniformly controlled.

**Initial state.** The initial empirical profile is an input, not a consequence of this theorem. The visible microscopic configuration may otherwise be arbitrary. For deterministic control, arbitrary phases and all their old records are permitted pointwise. For Poisson pi kicks, deterministic initial signs are permitted pointwise, while the future clock innovations retain their actual conditional stochastic law.

**Costs.** On a physical interval \(N^2T\), global pi cycling requires order \(N^2T/h\) broadcast pulse events, each acting on \(N\) phases. Uniform rotation requires an actual speed \(\Omega\) on every phase over that interval. Independent Poisson pi kicks require \(\gamma N^3T\) expected local physical kicks. A global Poisson clock plus a uniformly selected site has total rate \(N\gamma\); it does not remove the local-event count. No relation between these mathematical frequencies and power, torque, heat, pulse errors, or fabrication cost has been supplied.

**No kinetic fit.** The controller uses the declared amplitude bound and phase interface. It never estimates the unknown functions \(\alpha_i\). A finite-range influence claim is a structural supplier premise; arbitrary unknown long-range dependencies fall under the weaker deterministic guarantee. The Poisson result needs independent local control, not only one common random sign.

**No free stronger control.** An actual absolute phase setter and compatible hold could set every phase to \(\pi/2\) and remove the modulation exactly. That conventional stronger operation wins immediately if supplied. Relative phase shifts or phase diffusion do not imply it. Additional Brownian fluctuations during a purported deterministic retracing protocol are not undone by the drive.

**No optimality claim.** The deterministic influence condition is sufficient. Its \(N\)-scale is necessary in the explicit global-context heat-bath example, not yet proved necessary for the conserving ring. The entropy-derived finite-error bounds are conservative. No comparative energy advantage or practical speedup is established.

## 11. Primary predecessors and actual reading scope

The governing Astra mission and sixth-continuation handoff were read before this construction, along with the actual round5 supplier and mirror proof. N675 and accepted thermal-information interfaces were not reopened.

* **Exponential conjugation is established.** S. Andres, J.-D. Deuschel and M. Slowik, *Heat kernel estimates for random walks with degenerate weights*, EJP 21 (2016), paper 33, [DOI](https://doi.org/10.1214/16-EJP4382), [primary preprint](https://arxiv.org/pdf/1412.4338). Read the generator setup, Lemma 2.1, its energy proof, and the corresponding variable-speed estimate. Their Davies perturbation method has the same exponential-conjugation and cosh jump-increment structure. Equation (11) is derived here to make the time-dependent oscillatory cancellation and physical-control scope explicit, without claiming a new analytic method.

* **Hydrodynamic paths in dynamic environments are established.** F. Redig, E. Saada and F. Sau, *Symmetric simple exclusion process in dynamic environment: hydrodynamics*, EJP 25 (2020), article 138, [DOI](https://doi.org/10.1214/20-EJP536), [primary preprint](https://arxiv.org/pdf/1811.01366). Read the introduction, dynamic conductance setup, Theorem 3.2 and its arbitrary-starting-point premise, and the mild-solution construction. Their conductances are a quenched external field and preserve the single-particle duality structure. Our unknown \(\eta\)-context amplitudes can break that structure. Their theorem is a strong predecessor for path-space SSEP homogenization, not a direct replacement for the context-dependent current estimate above.

* **Entropy hydrodynamics is established.** M. Z. Guo, G. C. Papanicolaou and S. R. S. Varadhan, *Nonlinear diffusion limit for a system with nearest neighbor interactions*, CMP 118 (1988), 31–59, [primary author-hosted paper](https://math.stanford.edu/~papanico/pubftp/pubs_old/Guo_pap_vara_CMP_88.pdf). Read the model, initial entropy premise, theorem statement and basic entropy inequality. Their model is interacting conservative diffusions, not the phase-controlled exclusion supplier. The proof above uses only the explicitly proved event entropy inequality and elementary martingales; no unverified general hydrodynamic theorem is imported.

* **Fast modulation and deterministic/random cycling have longstanding predecessors.** The actual round5 source note preserves Anderson's 1954 motional-narrowing model, Strang's symmetric splitting, and Viola–Knill's randomized decoupling comparison with its separate quantum interface. This continuation does not relabel those mechanisms as inventions. Its useful addition to this research comparison is the explicit full density-path receiving argument, the initialization distinction, and the exact global-context collective obstruction.

The matched ordinary controllers are therefore strong positive alternatives. A diffusion-only supplier remains a different physical interface. The consequential question is which selective actuator can actually be supplied while preserving the native model and its costs.
