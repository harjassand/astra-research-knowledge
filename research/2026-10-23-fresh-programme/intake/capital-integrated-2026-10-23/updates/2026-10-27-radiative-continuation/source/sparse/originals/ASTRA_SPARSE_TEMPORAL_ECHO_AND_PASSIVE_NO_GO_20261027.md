# Spatiotemporal radiation echo: sparse inverse control, passive obstruction, and moving-window radiation

27 October 2026 — constructive research continuation. **Scope:** number-conserving one-excitation Fano Hamiltonian with two propagation directions, a genuinely gapless but finite-band bath, time-dependent real internal couplings, and a designated terminal time. All statements of novelty, hardware feasibility, or experimental performance remain unresolved. Energy units B=1. This note uses the previous exact delayed-source identity and independently verifies the changed internal Hamiltonian and controls; it does **not** reassert arbitrary-particle occupancy capacity.

## 1. Scientific choice and primary competing mechanism

The previous five-internal-mode radiation echo has a complete continuum theorem, but its inverse-engineered internal controls are dense. The strongest alternative is passive giant-atom/waveguide engineering. A relevant **20 October 2026** PRX Quantum result (Diekmann et al., *Enabling Deterministic Passive Quantum State Transfer with Giant Atoms*, DOI:10.1103/6wcb-nj42) derives ideal passive transfer with continuously distributed coupling sites, and >99% numerical transfer with at least ten finite coupling points, prominently in chiral and engineered-dispersion settings. A 2025 graph-with-tails theorem (Bernard et al., DOI:10.1016/j.laa.2025.02.005) finds exact stationary transfers in a **decoupled dark subspace**. Neither establishes the finite-time, fully returned *reciprocal radiative* protocol below. Conversely, they show that the general physical goal is established and that this construction cannot claim discovery of state transfer itself.

I chose to make the exact reciprocal construction sparse and establish what controls are intrinsically necessary for its chosen smooth trajectory, rather than repeat a weakly constrained bandwidth optimization. The passive alternative remains consequential; Section 5 gives a broad stationary reciprocal obstruction and explicitly states its exceptions.

## 2. Exact symmetry reduction

For emitters at x=(-tau,0,tau), with tau=1/2, let

    (W q)_sigma(omega)=v(omega)*sum_j exp(i*sigma*omega*x_j)*q_j,
    sigma=+/-; v(omega)=eta*sqrt(omega)*(1-omega/12)^2,
    0<omega<12; eta=0.01.

The two outer emitter amplitudes are identical in the exact temporal-source identity. The outer antisymmetric mode consequently never couples to the prescribed trajectory. In the active basis o=(e1+e3)/sqrt(2), c=e2 the bath has two columns

    W_(sigma,o)=sqrt(2)*v(omega)*cos(omega*tau),
    W_(sigma,c)=v(omega).

Thus the active internal space is (a,b,o,c), not (a,b,e1,e2,e3). All bath amplitudes remain present. The inactive antisymmetric emitter can be retained with a constant positive energy mu and no internal source; the restriction is an invariant subspace of a physical mirror-symmetric five-mode Hamiltonian.

Set mu=2*pi, T=12, alpha=.16, and define f(t)=[4u(1-u)]^3 for u=(t-tau)/(T-2tau) in [0,1], zero elsewhere. Define

    h_o(t)=sqrt(2)*alpha*f(t),
    h_c(t)=alpha*[f(t-tau)+f(t+tau)],
    q(t)=i*exp(-i*mu*t)*h(t).

The carrier condition mu*tau=pi ensures exactly

    q1=q3=i*alpha*exp(-i*mu*t)*f(t),
    q2=-q1(t-tau)-q1(t+tau).

This cancels the complete Fourier radiation source at t=T for both directions. Define the **actual** transient radiation

    xi(t)=-i*int_0^t exp[-i*omega*(t-s)] Wq(s) ds,

which generally is not vacuum for 0<t<T, and the positive storage norm rho=sqrt(1-||h||^2-||xi||^2). Choose storage amplitudes r=rho*(cos theta,sin theta), where theta(0)=0, theta(T)=pi/2, theta'=pi*f(t)^2/(2I), I=int f^2 dt. We use the same exact, time-dependent emitter trajectory as the previous theorem.

## 3. A reusable sparse inverse-control lemma

**Lemma (real four-mode synthesis).** Take real differentiable storage and emitter amplitudes r in R^2, h=(h_o,h_c) in R^2 with rho=||r||>0 and h_c>0. Suppose a prescribed continuum trajectory gives g=exp(i*mu*t)*W^*xi, and put y=-h'-Re g and z=-Im g. A real symmetric internal Hamiltonian of the form

    H_int(t)=mu I_4 + [[0,C],[C^T,Q]]

can generate the trajectory only if r dot r'=h dot y. That condition is also sufficient, and it can be met with **four storage-emitter hopping controls, one emitter-emitter hopping, and one center-emitter detuning**, specifically:

    C[:,o]=(y_o/||r||^2)*r,
    C[:,c]=(r'-h_o*C[:,o])/h_c,
    Q_oo=0,
    Q_oc=Q_co=z_o/h_c,
    Q_cc=(z_c-h_o*Q_oc)/h_c.

Indeed C h=r' by construction and r^T C=(y_o,y_c) because r dot r'=h dot y. The two Q entries give Qh=z. These are exactly the real and imaginary parts of the Schrödinger equation with q=i exp(-i mu t)h. The compatibility condition follows from conservation of the norm of the full emitter+storage+continuum target state; it is not an assumed extra constraint.

The present bump satisfies h_c(t)>0 for 0<t<T and h_o<=sqrt(2)*h_c, so ||h||<=sqrt(3)*h_c. All six controls extend continuously by zero at the endpoints: h_c=O(t^3), g=O(t^4) and r'=O(t^5) near the start, with reversed counterparts near the end. Thus there is no divergent control hidden in the division by h_c.

**Strict continuous-time stability.** For the parameter set above, without any time grid,

    ||W||<0.053666,
    ||h||<0.391919, ||h'||<0.427548,
    ||xi||<0.046208, rho>0.918838,
    ||xi(t)||/||h(t)||<0.321994,
    ||r'||/||h||<2.318761.

Proof details: ||W||<=sqrt(6)||v||_2; ||W^*omega^-1 W||<=6*eta^2*12/5=0.00144. Fourier Plancherel with the truncated emitter sources gives ||xi||<=alpha*||v||_infinity*sqrt(72*pi*I). Symmetry and the explicitly verified monotonicity of both nonnegative emitter envelopes up to T/2, together with xi(0)=xi(T)=0, give ||xi(t)||<=||W||(T/2)||h(t)||. The derivative estimates then follow by differentiating the normalized storage state. The monotonicity of f(t-tau)+f(t+tau) reduces to the derivative sign of u*(1-4u^2/L^2)^2 over 0<u<2tau, since 2tau<L/(2sqrt(5)), L=11.

Using h_o/h_c<=sqrt(2), these estimates imply

    ||C[:,o]||<0.469,
    ||C[:,c]||<4.681,
    ||C||<4.71,
    ||Q||<0.104.

Therefore, for the **continuous** bath and all 0<=t<=T,

    H_int(t) - W^*omega^-1 W
      >= (6.28-4.71-0.104-0.0015)I >1.46 I.

This proves the entire one-particle Hamiltonian is nonnegative after square completion with its positive-energy gapless continuum. It is a uniformly positive *internal Schur margin*, not a gap of the full field, whose spectrum reaches zero.

## 4. Exact minimum-graph and control obstructions, scoped to the prescribed trajectory

The source involves six types of independent scalar controls (five real hopping envelopes and one real emitter-energy envelope). None of their graph positions can be deleted while preserving **this source trajectory and its fixed real-carrier gauge**, provided no additional storage-storage or synthetic complex hopping is introduced.

For 0<t<tau, h_o=0, h_c>0, r_b=0, and r_a>0. Define the emitter cross spectral moments

    M0_oc=2*sqrt(2)*int_0^12 |v(omega)|^2*cos(omega*tau)domega
       =sqrt(2)*(-5+6 sin6+5 cos6)/67500 <0,
    M1_oc=2*sqrt(2)*int_0^12 |v|^2*(omega-mu)*cos(omega*tau)domega
       =sqrt(2)*[-96-5*pi*cos6+6*sin6-6*pi*sin6+5*pi+60*cos6]/33750 <0,
    M1_cc=2*int_0^12 |v|^2*(omega-mu)domega
       =72/21875-6*pi/3125 <0.

Signs are certified without relying on the printed decimals: sin(6) in (-0.280,-0.279), cos(6) in (0.960,0.961), pi in (3.141592,3.141593), with Taylor remainder bounds. Since h_c(t)=c*t^3+O(t^4) near zero, the early backaction is

    Re g_o(t)=M0_oc*int_0^t h_c(s)ds+O(t^5),
    Im g_o(t)=-M1_oc*int_0^t (t-s)h_c(s)ds+O(t^6),
    Im g_c(t)=-M1_cc*int_0^t (t-s)h_c(s)ds+O(t^6).

All are nonzero for sufficiently small t. Consequently C_ao is required for the real outer-emitter equation, C_ac for the central emitter derivative, Q_oc for the imaginary outer-emitter equation and Q_cc for the imaginary center-emitter equation. The mirrored final interval, with r_a=0 and r_b>0, requires C_bo and C_bc. This **does not** prove six controls minimal among all possible trajectories or encodings; it proves graph necessity for this specified echo and real-gauge control class.

**A stronger physical-locality failure of this source waveform:** if storage a is attached *only* to the left outer emitter and storage b *only* to the right outer emitter, with no direct storage bypass, the prescribed trajectory is impossible even with arbitrarily variable real couplings inside the emitter chain. Throughout 0<t<tau both outer emitter amplitudes vanish, while the center emitter has h_c(t)>0. The source for the center emitter from its adjacent outer emitters is then zero, and initially there is no radiation field. Uniqueness of the coupled equations would keep the center emitter and bath identically vacant until some outer emitter is excited, contradicting h_c>0. Therefore the exact echo derived here still relies on storage-center controls or similarly extended physical connections. Indeed the internal transfer already exists when eta=0: this is *not* yet remote quantum communication mediated exclusively by the waveguide.

There is an independent no-go for the appealing **fixed hopping + time-dependent onsite energies only** alternative. Since the source amplitudes have q_e'(0)=0 and the bath starts empty, the emitter Schrödinger equation requires every hopping from initial storage a to an emitter to vanish at t=0. If these hoppings are time-independent, all such edges vanish permanently. With no storage-storage bypass, |a> cannot transfer. A symmetric argument applies at the final endpoint. This conclusion depends on the cubic onset; it does not forbid all state-transfer paths with linear onset or extra intermediate storage modes.

## 5. Broader no-go: passive reciprocal transfer through an actual continuous spectrum

**Theorem.** Let H be a time-*independent* self-adjoint Hamiltonian invariant under an antiunitary time reversal Theta with Theta^2=1. Let orthogonal localized initial/final vectors a,b be Theta-invariant. If there exists T>0 and phase phi for which exp(-iHT)a=exp(i phi)b **exactly**, the spectral measure of a is pure point and supported on an arithmetic congruence lattice. In particular a cannot have nonzero absolutely continuous spectral weight in a radiative band.

**Proof.** In a Theta-real basis, the time-independent Hamiltonian is real symmetric, hence U(T)=exp(-iHT) is symmetric. Unitarity and U(T)a=exp(i phi)b force U(T)b=exp(i phi)a. Thus U(2T)a=exp(2i phi)a. The spectral theorem gives

    0 = ||[U(2T)-exp(2i phi)]a||^2
      = int |exp(-2i E T)-exp(2i phi)|^2 dmu_a(E).

This integrand vanishes only at a countable arithmetic progression of energies, proving the claim.

**Exceptions are essential:** a,b may inhabit an invariant bound/dark subspace with only point spectrum; H may break reciprocity (chiral setups); time-dependent controls may be used; or exact finite-time transfer may be replaced by asymptotic or approximate transfer. The recent passive giant-atom paper explicitly studies chiral/engineered coupling geometries, so there is no contradiction. This spectral observation has antecedents in perfect-state-transfer theory (including the graph-with-tails dark-subspace exception); no novelty is claimed.

The current temporal echo uses time-dependent real Hamiltonians and therefore is *not* prohibited by this stationary theorem.

## 6. Moving-window radiation identity (stronger explanatory result)

For the point-emitter sources q1=q3=q_outer and q2(t)=-q_outer(t-tau)-q_outer(t+tau), define F(z,t)=int_0^t exp(i z s) q_outer(s)ds with zero extension outside the experiment. At any intermediate time the radiative source in either direction is **exactly**

    A(z,t)=exp(i z tau)*int_(t-tau)^t exp(i z s)q_outer(s)ds
            -exp(-i z tau)*int_t^(t+tau) exp(i z s)q_outer(s)ds.

There is no integral over the entire earlier history: all radiation is determined by a moving window of width 2tau. The formula holds at *every* frequency, including off-shell modes, and the field is xi_sigma=-i v(z)exp(-izt)A(z,t). At t=T both window integrals vanish, exactly.

For the present nonnegative bump, monotonicity shows sup_(s in [t-tau,t+tau]) f(s)<=f(t-tau)+f(t+tau). Independently, |A|<=2alpha*tau*sup f<=2alpha*tau. Therefore at every intermediate time

    ||xi(t)|| <= 2sqrt(2)*alpha*tau*||v||_2,
    P_radiation(t) <=8 alpha^2 tau^2 ||v||_2^2.

At eta=.01 this gives ||xi||<0.004958 (observed max 0.002844), P<2.4576e-5. For eta=.60 the analytic bound is ||xi||<0.2975 and P<0.08848; the **numerically observed** transient probability is 0.02912, with terminal radiation norm 8.2e-12. This latter stronger-coupling case retains positive **sampled** Schur margin 2.428, but lacks a continuous-time interval certificate, so must not be presented as another proven all-time positive model. At eta=.80 the sampled internal Schur margin turns negative (-0.287), giving a decisive failure of the stable quadratic all-particle interpretation despite excellent terminal radiation cancellation.

The moving-window identity was verified independently against radiation-ODE output with maximum amplitude discrepancy 4.34e-15 over 30 sampled time-frequency pairs.

## 7. Digitized local control: executed unitary checks

Instead of continuously varying the six scalar controls, hold their exact values at the midpoint of each of K equal time steps. For each step we exponentiated the full finite-mode Hamiltonian using a Hermitian eigendecomposition; no loss or postselection was introduced. Bath quadrature retained 40 positive-energy modes per propagation direction.

    K      complete state-vector error      final bath-amplitude norm
    16          0.01611182                      2.9451e-4
    32          0.00401759                      7.2841e-5
    64          0.00100677                      1.8254e-5
    128         0.00025146                      4.5554e-6
    256         0.00006290                      1.1397e-6

For a simple **full-state control-calibration certificate**, suppose every one of the six independent real scalar controls differs from its calibrated value by at most epsilon at every instant, while the bath coupling is unchanged. The largest absolute row sum of the resulting four-by-four perturbation is at most 4*epsilon, hence ||delta H||<=4*epsilon and Duhamel gives ||delta Psi(T)||<=4*T*epsilon=48*epsilon. This is a rigorous worst-case coherent *amplitude* estimate for arbitrary initial/reference states; it includes the radiation sector and does not assume independent random errors. For example epsilon=10^-4*B implies a conservative state-vector error below 0.0048. No experimental tolerance has been inferred.

The errors empirically scale as K^-2 for these smooth midpoint controls. This observed rate is **not** a uniform operator-norm theorem. A general Duhamel estimate for a Lipschitz Hamiltonian gives the conservative bound ||U(T)-U_K(T)||<=L_H*T^2/(4K), where L_H is any valid essential sup of ||dH/dt||. That quantity was not independently interval-certified here. These are model-level sampling results, not an experimental AWG specification.

## 8. Scientific boundary and next strongest attack

The exact four-mode inverse-control theorem, its analytic continuous-time positive Schur margin, the scoped minimum-control obstructions, and stationary reciprocal spectral no-go are proven within their declared Hamiltonian classes. The strong-coupling and digitized-pulse numbers are executed finite-mode diagnostics. The process acts in the one-excitation sector and does not establish a conditional multiphoton quantum gate or finite dressed capacity. The original continuum capacity-two conjecture remains open.

The strongest still-unacquired physical input is a microwave/acoustic/cavity system that supplies the prescribed frequency-dependent waveguide coupling and the six bounded time-dependent local controls while retaining low independent radiation. Passive chiral giant-atom transfer remains a scientifically serious comparator, not a straw man. A compelling further attack is to replace the whole inverse-engineered control waveform by a small fixed set of physical modulation harmonics, or derive a quantitative control-bandwidth lower bound under that restriction.

## Reproduction

1. `astra_spatiotemporal_sparse_echo.py` — independent reduced Hamiltonian construction and complete finite-mode Schrödinger propagation, result `astra_spatiotemporal_sparse_echo_results.json`.
2. `astra_spatiotemporal_sparse_certificates.py` — continuous-time positivity estimates and exact cross-moment signs, result `astra_spatiotemporal_sparse_certificates.json`.
3. `astra_spatiotemporal_control_digitization.py` — exact unitary midpoint-constant pulses, result `astra_spatiotemporal_control_digitization_results.json`.
4. `astra_spatiotemporal_moving_window.py` — independent Fourier moving-window identity check, result `astra_spatiotemporal_moving_window_results.json`.
5. `astra_spatiotemporal_sparse_eta_{0.10,0.25,0.40,0.50,0.60,0.80}.json` — high-coupling diagnostics, each run with `ASTRA_ECHO_ETA=<value>` and `ASTRA_ECHO_OUT=<file>` environment variables for `astra_spatiotemporal_sparse_echo.py`.

Governing predecessor: `/mnt/data/ASTRA_SPATIOTEMPORAL_RADIATION_ECHO_20261027.md`. External comparators: https://doi.org/10.1103/6wcb-nj42 ; https://doi.org/10.1016/j.laa.2025.02.005 ; https://doi.org/10.1103/m2md-rxkv .

## 9. Next attack: where may terminally dark emission begin and end?

The previous exact three-emitter echo is not yet an actual spatially remote storage-to-storage interface: its initially nonzero source is at the middle emitter and both storage nodes require connections into the central network. A more general radiation-causality theorem pinpoints the geometry of this failure.

**Theorem (boundary emitters cannot lead or finish a finite terminal echo).** Consider distinct ordered positions x1<...<xn in a bidirectional frequency-linear waveguide, with compactly time-supported emitter histories q_j and nonzero coupling over any open frequency interval. Assume initially empty radiation and exact vacuum in *both* directions at the final time. Let t_min be the earliest nonzero emitter-source time and t_max the latest. Then neither spatially outermost emitter j=1 or j=n can attain t_min or t_max. Therefore an exactly returning three-emitter echo must start and end at its **middle** emitter, regardless of the precise pulse envelope.

**Proof.** The entire functions F_j(z)=int exp(i z t)q_j(t)dt obey sum_j exp(±iz x_j)F_j(z)=0 on an open real interval and hence for all complex z. Their inverse Fourier transforms give sum_j q_j(t∓x_j)=0 for every real t. If the leftmost emitter began at global t_min, the `+` source sum would contain its strictly earliest shifted contribution at t_min+x1, with no other source able to cancel it. If the rightmost began first, apply the `-` sum. By considering the latest shifted contribution instead, the `+` sum excludes the rightmost emitter from ending last, and the `-` sum excludes the leftmost. This is a support-order argument, not a Markov approximation. At coincident positions the statement requires modification, as does an imperfect or one-direction-only vacuum condition.

A **four-emitter source algebra** already evades the three-emitter initial/final-location constraint. Let the positions be (0,tau,2tau,3tau), and put z=exp(i omega tau). Two exact null-generator columns for both propagation directions are

    A(z)=(1,-[z+z^-1],1,0)^T,
    B(z)=(0,1,-[z+z^-1],1)^T.

Indeed sum_j z^j A_j=sum_j z^-j A_j=0, and likewise for B. In time, with pulses f_A and f_B,

    q1=f_A,
    q2=-f_A(t-tau)-f_A(t+tau)+f_B,
    q3=f_A-f_B(t-tau)-f_B(t+tau),
    q4=f_B.

Taking f_A supported on (.5,1.5), f_B on (10.5,11.5), tau=.5 and T=12 gives earliest nonzero radiation source at **emitter 2** and latest at **emitter 3**. Independent Laurent-polynomial identities are exact; six numerical frequency checks give maximum Fourier residual below 7.62e-16. The script `astra_spatiotemporal_four_emitter_sources.py` and its JSON data preserve the calculation.

**This is not yet quantum transfer.** The exhibited pulses are separated in time, and source nullity alone says nothing about an internal positive Hamiltonian that moves the excitation from storage at emitter 2 to storage at emitter 3. In fact, the simple common-carrier real-gauge ansatz is incompatible with the strict endpoint-only storage-attachment graph: the real part of the outer-emitter Schrödinger equation requires a directly supplied amplitude derivative, while real emitter-emitter hoppings between identically phased emitters only rotate their phase. New relative-phase freedom, additional controls, or a genuinely propagating photonic intermediate state will be necessary. This is the decisive new physical-interface obstruction, and it defines the next useful construction target.
