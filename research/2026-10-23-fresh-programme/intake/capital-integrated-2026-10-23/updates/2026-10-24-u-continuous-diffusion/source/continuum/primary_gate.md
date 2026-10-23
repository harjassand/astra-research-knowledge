# Periodically driven metastable ring: primary-source gate

## Finding

The closest primary work-extraction construction I found is a driven Brownian ring used as a nonequilibrium bath for a separate harmonic oscillator. It proves that a cyclic conservative stiffness protocol can extract work from a maintained NESS, but it does not establish extraction by modulating one field on the same overdamped ring particle. The closest periodic metastability framework gives the right continuous-density reconstruction and time-dependent coarse rates, but it supplies no uniform error bound for the full-cycle field-work functional. A rigorous time-inhomogeneous metastability theorem controls two-state exit windows at exponential accuracy, not a three-state periodic law or work.

Accordingly, a negative work-per-cycle result in the reduced three-state CTMC is not yet a finite-barrier continuum result. The sharp next check is to solve the full periodically forced Fokker–Planck equation on the ring at finite \(H\), obtain its periodic law, and calculate the field and drive work over the same cycle.

## Three primary sources

1. **Wulfert, Oechsle, Speck & Seifert (2017), “Driven Brownian particle as a paradigm for a nonequilibrium heat bath: Effective temperature and cyclic work extraction,” PRE 95, 050103(R), [primary arXiv paper](https://arxiv.org/abs/1705.00877).** Their driven subsystem is an underdamped Brownian particle in a periodic potential on a ring, driven by a constant force (f); it weakly couples to a separate harmonic oscillator. The oscillator is cyclically operated between frequencies ω₁ and ω₂. Their extracted work per cycle is
   \[
   \Delta W=\tfrac12(1-\Omega^2)T_1+\tfrac12(1-\Omega^{-2})T_2,\qquad \Omega=\omega_2/\omega_1,
   \]
   and is positive when \(T_2/T_1>\Omega^2\) (Eqs. 13–18). This is a real primary theoretical/numerical engine construction and a useful thermodynamic incumbent, but its load is the separate oscillator, its control is oscillator stiffness, and its heat bath is maintained out of equilibrium. The authors explicitly omit the energetic cost of maintaining the driven thermostat (PDF pp. 1, 4; Eq. 18 and discussion immediately after). It therefore neither gives the proposed one-coordinate field-work sign nor a net-efficiency advantage. The paper also shows why a work-sign claim must state the load and all maintained-drive costs.

2. **Kim, Talkner, Lee & Hänggi (2010), “Rate description of Fokker–Planck processes with time-periodic parameters,” Chemical Physics 370, 277–289, [primary arXiv paper](https://arxiv.org/abs/0908.1730).** For weak-noise periodic Fokker–Planck dynamics with metastable states, they reconstruct the long-time density from the coarse probabilities and state-conditioned densities, \(\rho_p(x,t)=\sum_\alpha \rho(x,t|\alpha)p_\alpha(t)\) (Eq. 19). The probability evolution is \(\dot p_\alpha=\sum_\beta k_{\alpha\beta}(t)p_\beta\) (Eq. 23), with
   \[
   k_{\alpha\beta}(t)=\int \partial_t\chi_\alpha(x,t)\rho(x,t|\beta)\,dx
   +\int \chi_\alpha(x,t)L(t)\rho(x,t|\beta)\,dx
   \]
   (Eq. 24). The first term is the moving-localizer/geometric correction. Their introduction defines the semiadiabatic regime as driving slow against intrawell relaxation, with no restriction on the driving period relative to metastable sojourn times (PDF p. 2, lines 59–65). This is the closest formulaic interface for the candidate’s order-one evolution on the Kramers clock and for reconstructing \(\langle f\rangle\). Crucially, they state that formal positivity of the reduced rates is unproved; negative rates signal breakdown of the rate-process assumption (PDF p. 8, lines 363–367). The paper provides no uniform-in-phase error bound for \(\rho_p\), \(\langle f\rangle\), or an integrated work sign. Thus it is a reduction framework, not the needed finite-H convergence theorem.

3. **Herrmann, Imkeller & Peithmann (2006), “Transition times and stochastic resonance for multidimensional diffusions with time periodic drift: A large deviations approach,” Ann. Appl. Probab. 16, 1851–1892, [primary paper PDF](https://arxiv.org/abs/math/0411386), DOI [10.1214/105051606000000385](https://doi.org/10.1214/105051606000000385).** This is the rigorous time-inhomogeneous result nearest the requested metastability theorem. With small-noise diffusion and forcing on exponential time \(T_\epsilon=e^{\mu/\epsilon}\), Theorem 2.3 gives an exponentially sharp probability for the first exit/entrance time to lie outside a forcing-phase window and makes that asymptotic uniform for \(\mu\) in compact subsets (PDF pp. 20–22, Theorem 2.3). The hypotheses are two stable equilibria and two time-independent attraction basins (Assumption 2.1); the drift is potential-type for the barrier interpretation. It controls exit-time windows, not Eyring–Kramers prefactors, a three-well jump-path law, the periodic stationary density, or a work functional. It also does not cover the ring’s constant nonconservative tilt. It establishes that the external period can live on the Kramers exponential scale, but it does not close the candidate’s required interface.

## Work-functional gap and finite-barrier falsifier

For the specified field \(U_H=HV+v-hf\), the field work on the system is exactly
\[
W_h^{(H)}=-\int_0^{P_H}\dot h(t)\,\langle f\rangle_{\rho_H(t)}\,dt.
\]
The CTMC expression uses \(\sum_i f_i p_i(t)\). To transfer its sign, one needs a bound over a full period on
\[
\left|W_h^{(H)}-W_h^{\rm CTMC}\right|
\leq \int_0^{P_H}|\dot h(t)|\left|\langle f\rangle_{\rho_H(t)}-\sum_i f_i p_i(t)\right|dt
\]
that is smaller than the CTMC negative-work margin. The state-conditioned values should be \(f_i(t)=\int f(x)\rho(x,t|i)dx\), not automatically the binary well labels: finite-width wells and transition paths contribute. For the same trajectory or periodic Fokker–Planck law, report separately the nonconservative input \(W_F=F\int j(x,t)\,dx\,dt\) with winding counted on the ring. A negative \(W_h\) alone means the field actuator receives work; it does not show that total external input is negative or that the process has positive net efficiency.

The falsifier is direct: at several finite (H), solve or converge the full periodic Fokker–Planck law, integrate \(W_h^{(H)}\) and \(W_F^{(H)}\), and compare against the CTMC with the same (h(t)), calibrated rates, basin assignment, and cycle. If the continuum work margin changes sign or shrinks into the reduction error, the CTMC witness has not transferred. The Kramers prefactor and modulation of each barrier action must be kept in the rates; a common clock \(\kappa_H\sim H e^{-H}\) alone does not determine finite-H work or physical power. If the negative work per slow-clock cycle remains (O(1)) while the physical cycle time scales as \(\kappa_H^{-1}\), the output power scales as \(O(\kappa_H)\to0\) as (H\to\infty\). A finite-H operating point is needed for any nonzero-power claim.
