# Independent review: one-bit acquisition boundary

29 October 2026. Exact reviewed causal-branch source:

    ONE_BIT_CAUSAL_CONTROLLER_BOUNDARY.md
    a76e98fae0acc9fed1a5e2344b4329811e503160aee3fe22122314a84af0ebde

The newly used adaptive-position acquisition theorem was checked in:

    FINITE_RESOLUTION_TRANSCRIPT_THEOREMS.md
    6bdce13548ddeaaec782c37e8b5400b7036c119d986a2c6b4ac59c19d12f02c2

## Outcome

The construction is valid at its explicitly restricted native reporter
interface. Its deterministic candidate-before-controller result and its
stronger candidate-independent randomized score test both hold. Reporter
independence, noisy macroscopic transduction, robustness constants and
the specified Gaussian-position necessary budget check out.

One scope clarification should be made explicit when quoting the necessary
budget: query times/settings/stops must be chosen from PREVIOUS CHARGED
REPORTS and independent randomization, as in the imported theorem. They
cannot be triggered by an uncharged exact native trajectory or hidden
event time. The preceding theorem already states this requirement; the
one-bit note's reference to that interface imports it. No broader sensor
lower bound is justified merely by saying that queries are "adaptive."

No empirical test or physical operation was needed for this review.

## 1. Uniform score and clipping constants

For S_n=int a sin(nx)(dw+gamma w dt), the source mean is
Delta=a^2 T0/2. Every admitted Gibbs candidate has mean zero because its
position flux identity is G nu_U=tau grad nu_U and the score field is
divergence-free. The stated second moments follow from
(drift integral+martingale)^2<=2 drift^2+2 martingale^2 and the common
noise intensity. Thus

    C=M_P+M_Q=2a^2 T0[(a^2+A^2)T0+4gamma tau],
    delta0=Delta^2/(2C)
           =a^2 T0/[16((a^2+A^2)T0+4gamma tau)]

are correct. The general expectation-gap/TV inequality also has the
correct factor two, using the dominating measure P+Q.

For M=C/(2Delta), the pointwise clipping bound is exact at |s|=2M:

    |s-clip(s,-M,M)|<=s^2/(4M).

Therefore the clipped expectation gap is at least
Delta-C/(4M)=Delta/2. Division by 2M in g yields

    E_P g(S_n)-E_Q g(S_n)>=Delta/(4M)=delta0.

The same rule depends on n and the known force ceiling, but not on the
candidate potential U. This validates the stronger randomized
sup_controller inf_U statement without changing the deterministic
candidate-before-controller argument.

A uniform midpoint grid of K thresholds approximates each bit probability
with error at most 1/K (indeed 1/(2K) suffices). The claimed gap loss at
most 2/K is safe, and K>=4/delta0 preserves delta0/2. The temporary random
bits and score acquisition remain additional resources.

## 2. Reporter independence and the exact transduction law

The driving record is independent of the entire unforced reporter.
Thus for a driving-record test, r(T0) is Maxwell and independent of the
prepared bit, as are future reporter Brownian increments. Under the
constant command B b, the endpoint is therefore exactly

    r(T0+h)|b ~ N(m b,tau),
    m=(B/gamma)(1-exp(-gamma h)).

The optional angle-based randomizer also preserves the required JOINT
independence. Conditional on the entire free reporter momentum path and
the entire driving system, ell(T0) is an independent uniform starting
angle plus a fixed shift modulo 2pi. Its conditional law is uniform.
Hence its bin index is independent jointly of S_n, r(T0), and the free
reporter's future noise. It is not merely pairwise independent. Using it
as the threshold thus leaves the displayed conditional endpoint law intact.
The angle readout and its required noninvasive preparation are declared
extra resources, rather than a driving-record-only deterministic test.

Adding independent readout noise eta Z changes variance to tau+eta^2.
The mixture weight difference p-q multiplies the difference of the two
Gaussian shift densities, whose sign changes at zero. Therefore both
the full noisy readout and its sign have exactly

    TV=beta|p-q|,
    beta=2Phi(m/sqrt(tau+eta^2))-1.

The fixed sign-readout probability Phi(r/eta) is Lipschitz with the stated
constant. This validates the claimed controlled physical-path d_BL gap;
the result is not dependent on exposing an exact command trace.

The known free reporter restriction is necessary for this proof. A
comparison potential coupling that reporter is not included in the
declared source class, and the note explicitly does not claim otherwise.

## 3. The explicit free-candidate rule

Conditional on the complete x path, the receiver innovation eliminates
the correlated stationary initial receiver term. Future W2 is independent
of the autonomous driver. Thus S_n has the two stated conditional normal
laws with V_n=int a^2 sin^2(nx)dt.

The bound 0<=V_n<=a^2T0 and its mean a^2T0/2 imply
P(V_n>=a^2T0/4)>=1/3. Substitution into the normal probability proves the
displayed delta_free, with its factor 2sqrt(2gamma tau) in the denominator.
The positive gap is uniform in n.

## 4. Precision robustness and necessary acquisition budget

Expanding the endpoint terms and the three products in the integration-
by-parts score formula gives exactly the stated sufficient error bound:

    a[nP(2+gamma T0)+n^2P^2T0] epsilon_x
      +a[2+gamma T0+2nPT0] epsilon_p.

Both true and acquired momentum paths are assumed bounded by P, as the
note states. This is a sufficient continuous-record error condition; it
does not purchase discrete-time quadrature, interpolation or sensor
precision. Since g is 1/(2M)-Lipschitz and takes values in [0,1], score
error epsilon except with probability zeta changes either bit probability
by at most epsilon/(2M)+zeta. The two-hypothesis loss
epsilon/M+2zeta is therefore correct. Random thresholds must remain
independent of the acquired score and its apparatus randomness.

At the imported Gaussian-position interface, stationary shear/free
coupling gives

    E sup_(t<=T0) d_Torus(q_source(t),q_free(t))^2
                          <=T0^2 tau sigma_n/gamma.

At a common report history the query setting and time are identical in
the two augmented experiments. The Gaussian conditional KL chain rule
and the PATHWISE precision/gain ceiling J then give

    KL(acquisition_source||acquisition_free)
                     <=(J/2)T0^2 tau sigma_n/gamma,
    TV<= (T0/2)sqrt[(tau sigma_n/gamma)J].

This includes the complete permitted transcript. Independent randomization
does not increase its TV, nor does bit computation. A bit gap d therefore
necessarily requires J>=4gamma d^2/(tau T0^2 sigma_n). Since sigma_n=O(1/n),
the Omega(n) conclusion at that sensor interface follows. The bound is
necessary, not sufficient, and does not cover uncharged force-feature,
momentum, hidden timing or microscopic measurements. Adaptive times are
legitimate only under the charged-report causal restriction stated above.

## 5. Work and the memory boundary

The reporter's conditional mean is B b(1-exp(-gamma s))/gamma. Multiplying
by the commanded force and integrating yields the stated work

    (B^2/gamma)[h-(1-exp(-gamma h))/gamma].

The variance remains tau, so mean kinetic-energy increase is m^2/2 and
the remaining work is exactly gamma times the integral of squared mean
momentum. No low-entropy assertion about the actuated reporter follows
from low baseline source entropy, and none is made.

The construction contracts the acquired bit's TV by beta. Its role is
to transfer increasingly fine native-path information into a fixed noisy
macroscopic report. It neither creates information nor refutes the
positive fixed-sensor finite-tree theorem. That theorem fixes the actual
acquisition kernels; this family changes them with n. One retained state
bit does not bound the information or preparation needed to produce it.
