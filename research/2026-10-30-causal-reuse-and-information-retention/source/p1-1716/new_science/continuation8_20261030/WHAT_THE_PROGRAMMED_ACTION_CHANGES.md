# What the programmed action changes at fixed equilibrium and diffusion

30 October 2026. Root consequences of the complete nonlocal action, within its
actual operation, initialization and fixed-alpha premises. These calculations
give a capability beyond changing a single scalar circulation variance.

Write c=s/2, chi=rho(1-rho), C=int chi, beta=alpha^2/(1-alpha^2), and

    I_alpha=(1/(2s))int dt [int (j+c rho_x)^2/chi
                                               +beta (int j)^2/C]. (1)

## 1. Complete density histories can distinguish the programmed law

Fix a smooth interior density history with conserved mass and initial m. Its
continuity equation determines a unique zero-spatial-mean current j_0; every
compatible current is j=j_0+q(t). Put

    a_0=j_0+c rho_x,  A_rho=int 1/chi,
    B_rho=int a_0/chi,  D_rho=A_rho+beta/C.                (2)

The current contraction is an exact square completion:

    q_alpha^*=-B_rho/D_rho,
    I_alpha(rho,j_0+q)
      =I_alpha^density(rho)+(1/(2s))int D_rho(q-q_alpha^*)^2dt,
    I_alpha^density(rho)
      =(1/(2s))int [int a_0^2/chi-B_rho^2/D_rho]dt.       (3)

The density-only action therefore increases relative to ordinary exclusion by

    I_alpha^density-I_0^density
      =(1/(2s))int B_rho^2[1/A_rho-1/(A_rho+beta/C)]dt>=0. (4)

It is strictly larger whenever alpha>0 and B_rho is nonzero for positive time.
Thus preserving the ordinary heat equation does not preserve the probabilities
of all atypical density histories. The complete density/current action supplies
which change occurs, including the remaining current freedom conditional on a
density history. Equation (3) is a large-deviation contraction, not an assertion
that every finite-system conditional current distribution is Gaussian.

A concrete nontrivial path is a growing traveling density wave,

    rho(t,x)=m+a(t)sin(2pi(x-vt)),
    j_0=v a(t)sin(2pi(x-vt))
                    +a'(t)/(2pi)cos(2pi(x-vt)),          (5)

with a(0)=0 and 0<rho<1. The cosine terms in B_rho integrate to zero. The
remaining v a sin/chi term is generally nonzero away from m=1/2. This gives
strict density-history cost separation, not only a different unobserved loop
noise. For a standing single sinusoid, in contrast, B_rho can vanish exactly;
that failed demonstration is preserved rather than described as a separation.

## 2. Thermodynamic reversal and static fluctuations remain the same

Let F(rho)=int [rho log rho+(1-rho)log(1-rho)]. For a smooth admissible path,
reverse time and current. The second term of (1) is even in j, while expansion
of the first term gives

    I_alpha^dyn(rho,j)-I_alpha^dyn(rho^R,-j^R)
      =int j rho_x/chi dxdt=F(rho_T)-F(rho_0).            (6)

Here I^dyn denotes the dynamic integral without an imposed initial profile;
this algebra does not extend the proved initial-law LDP by renaming it. It
shows explicitly why the designed nonlocal mobility does not contradict
equilibrium fluctuation-response structure.

The variational quasipotential at fixed mass is F(rho)-F(m), for smooth interior
targets. The lower bound follows from (6) and nonnegativity of reversed cost.
For the upper bound, reverse ordinary heat relaxation from the target. Its
reverse current is +c rho_x and has zero spatial mean, so the new term vanishes.
At an increasingly remote past the density approaches m. Connect m to that
near-flat density over a fixed short interval with a smooth continuity-respecting
path; its H1-size and action tend to zero. This supplies the usual infinite-time
variational upper bound. No new finite-time initialization preparation is inferred.

Static canonical probabilities and their free-energy cost therefore remain
unchanged while selected dynamical histories become more expensive.

## 3. Linear density fluctuations and circulating-force response are different questions

At flat rho=m the covariance form is

    M_m(H,G)=s chi(m)[int HG-alpha^2(int H)(int G)].       (7)

Spatial derivatives have zero mean, so the formal linearized density-noise
covariance is unchanged, while the constant current mode is suppressed by
1-alpha^2. The separate equilibrium fluctuation receiver must justify any CLT;
one cannot deduce it by differentiating the LDP.

The exact finite-network force theorem already gives stationary response
EA_c(1-alpha^2)sinh h when the actual load rates are multiplied by exp(h delta).
Thus this construction does not retain the old conducting response to a
circulating force while reducing its equilibrium noise. It retains heat
relaxation without that circulation load. The two experimental questions use
different forcings and observables.

## 4. Operational reach and the strongest ordinary comparisons

With the compatible two-layer supplier, the action and these consequences are
uniform over arbitrary bounded frozen microscopic phase amplitudes, without
learning them. A conventional fluctuation or control solver can use (1)--(4)
to predict or optimize transport histories. That is the intended consequence
of the operation bridge; no computational superiority is asserted.

Autonomous common speed modulation supplies another full action and can create
correlated rare bursts, but at fixed mean speed it broadens circulation tails.
An actual threshold-and-hold controller can clip rare circulation, with sensing,
timely stopping, and a true hold, while arresting all density evolution after
the threshold. An all-to-all matched Gaussian pair bath preserves an entire
density law while killing total current, at its own stronger pair-current
interface. These are working alternatives, not excluded conventional solvers.

The locality theorem makes a further restriction explicit: a reversible,
bounded-rate, bounded-local-memory counter for all physical displacement needs
range of order N to retain ordinary diffusion with vanishing leakage. The
shared gate pays for this range through its event-wide coupling. It does not
obtain global fluctuation control from independent local operations for free.

Known MFT, dipole-conserving dynamics, bounded-current gauge transformations and
switching-diffusion programs are primary predecessors. The candidate contribution
is the actual compatible operation and its complete receiving law with this
hidden-kinetics scope, rather than the generic fact that kinetics affects paths.
