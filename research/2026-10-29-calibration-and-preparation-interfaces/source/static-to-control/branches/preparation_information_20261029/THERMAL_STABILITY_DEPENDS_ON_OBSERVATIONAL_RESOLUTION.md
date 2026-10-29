# Small dissipation, thermal model geometry, and observational resolution

29 October 2026. Root construction. The shear-force counterexample was also
constructed independently by the alternative-frontier reviewer. The finite-path
separation, coupling and feedback consequences below are the root continuation.
Ordinary proofs are included; this is a mathematical native thermal source class,
not an acquired physical device or an instrument-precision claim.

## 1. The stronger claim that fails

The parity projection theorem constructs a nearby stationary reversible process
when a warranted bath controls reversal-changing modes. That process can have
velocity-dependent forces. Does low entropy instead imply proximity to an
equilibrium source with the SAME conventional thermostat and a conservative
position-only force? In full trajectory KL, and even finite-window total
variation with a common force-amplitude ceiling, the answer is NO.

This failure persists with fixed dimension, mass, friction, temperature and
bounded force amplitude. The missing resource is spatial regularity/resolution.
In a coarser path metric the same native family is close to ordinary equilibrium,
with an explicit coupling that also survives specified finite-gain feedback.

## 2. A conventional autonomous thermal family

Positions (x,y) lie on the 2pi-periodic two-dimensional torus. Momenta are
(v,w); mass is one, friction gamma>0 and temperature tau>0. Brownian motions
W1,W2 are independent. For an integer n>=1 and fixed amplitude a>0, set

    dx=v dt,                 dv=-gamma v dt+sqrt(2 gamma tau)dW1,
    dy=w dt,                 dw=[a sin(nx)-gamma w]dt
                                                +sqrt(2 gamma tau)dW2. (1)

The actual reversal is (x,y,v,w)->(x,y,-v,-w). There are no odd external
fields. The position force F_n=(0,a sin(nx)) is nonconservative and divergence
free. Its sup norm is a, while its spatial Lipschitz norm grows like an.
All odd variables have the same fixed thermal damping gamma.

### Stationary construction

Take a two-sided stationary OU v and a uniform independent torus phase for x.
Let zeta be an independent stationary OU with variance tau. Define

    Y_n(t)= integral_0^infinity exp(-gamma s) a sin(n x(t-s)) ds,
    w(t)=zeta(t)+Y_n(t).                                  (2)

Y is bounded by a/gamma and is differentiable with Y'=F_n(x)-gamma Y.
A uniform independent initial y phase, transported by w, gives a stationary
source. At each time the positional marginal is UNIFORM on the torus.
The x phase is uniform conditional on the entire OU v trajectory. The y
phase is uniform conditional on the entire remaining stationary driver.
Noise in both momenta and kinetic streaming supply the usual smooth positive
stationary density; bounded force gives momentum Lyapunov control. The explicit
stationary construction is sufficient for the identities below.

### Exact entropy rate

The force correlation is

    E[F_n(x(t)) F_n(x(t-s))]
      = (a^2/2) exp[-n^2 tau/gamma
                          (s-(1-exp(-gamma s))/gamma)].   (3)

Indeed the integrated stationary OU increment is Gaussian of variance
2 tau/gamma [s-(1-exp(-gamma s))/gamma], and the independent uniform
phase removes the sum-frequency term. Therefore physical heat divided by
temperature, equivalently intrinsic stationary reversal-divergence rate, is

    sigma_n = (a^2/(2tau)) integral_0^infinity
       exp[-gamma s-n^2 tau/gamma
                          (s-(1-exp(-gamma s))/gamma)] ds. (4)

It is positive and

    n sigma_n -> a^2 sqrt(pi/2)/(2 tau^(3/2)).              (5)

For a direct dominated-asymptotic proof, rescale s=u/(n sqrt(tau)). Near
zero, s-(1-exp(-gamma s))/gamma = gamma s^2/2+O(s^3).
For 0<=gamma s<=1 its value is >= gamma s^2/3. For gamma s>=1,
gamma s-1+exp(-gamma s) >= e^-1+(1-e^-1)(gamma s-1).
These inequalities dominate the short part by exp(-u^2/3) and make the
long tail exponentially small. They also give an explicit O(1/n) upper bound.

For numerical evaluation set lambda=n^2 tau/gamma^2 and u=exp(-gamma s):

    sigma_n=(a^2/(2 gamma tau)) integral_0^1
                                  exp[lambda(1+log u-u)] du. (6)

There is no assumption of an unknown large preparation time or small friction.
The dissipation falls because a bounded, increasingly fine spatial force
oscillates too rapidly along inertial trajectories to build momentum energy.

## 3. No same-thermostat equilibrium approximation in full path KL

Every stationary equilibrium source in the declared same-bath class has
force H=-grad U for a periodic scalar U and Gibbs density

    nu_U(q,p) proportional to exp[-(U(q)+|p|^2/2)/tau].

Conversely zero entropy in this class forces conditional Maxwell momenta;
the stationary equation then forces H=tau grad log nu_q, hence a gradient.

For any such smooth U, Girsanov gives the stationary forward KL rate

    I_n(U)=(1/(4 gamma tau)) E_uniform |F_n+grad U|^2
           >= a^2/(8 gamma tau).                        (7)

The cross term is zero by periodic integration by parts and div F_n=0;
E_uniform |F_n|^2=a^2/2. The minimum is attained by constant U. Initial
stationary KL is nonnegative and finite for every smooth torus U, so

    D(P_n[0,h] || P_U[0,h]) >= h a^2/(8 gamma tau).        (8)

Thus sigma_n->0 does NOT imply vanishing KL distance to an equilibrium
process inside the same force/bath class, even on one fixed positive horizon.
This is stronger than observing that the explicit parity projection leaves
the class: no alternative potential improves the KL rate below (7).

The initial density is nevertheless close to the uniform Maxwell law mu_0.
The conditional Gaussian logarithmic-Sobolev inequality and the thermal
Fisher identity give

    D(rho_n || mu_0) <= sigma_n/(2gamma).                 (9)

Uniform position is essential here. Equation (9) is a KL to a physical
Maxwell reference, not a bound on D(rho_n||rho_n Theta).

## 4. A finite-window separation, not only a KL-rate artifact

Restrict equilibrium alternatives to a common known force-amplitude bound
|grad U|<=A. No common derivative bound is imposed. Consider the path statistic

    S_n = integral_0^h F_n(q_t) dot (dp_t+gamma p_t dt).   (10)

The integrand has finite variation in time, so Ito and Stratonovich integrals
coincide. Under (1), E S_n=a^2 h/2. Under ANY Gibbs equilibrium potential,

    E_U S_n=h integral F_n dot (-grad U) nu_q dq
            = h tau integral F_n dot grad nu_q dq = 0.   (11)

This uses div F_n=0 and periodicity, not knowledge of U. Drift/noise bounds
and Ito isometry imply

    E_n S_n^2 <= 2a^4 h^2+4 gamma tau a^2 h,
    E_U S_n^2 <= 2a^2 A^2 h^2+4 gamma tau a^2 h.          (12)

For any common statistic S,
|E_P S-E_Q S|^2 <= 2 TV(P,Q) (E_P S^2+E_Q S^2).
Combining this with (11)--(12) gives, for every n and every such U,

    TV(P_n[0,h],P_U[0,h])
      >= a^2 h / {16[(a^2+A^2)h+4 gamma tau]}.           (13)

The lower bound is independent of n. For a=A=gamma=tau=h=1 it is 1/96.
This is a consequence of analytic moment bounds, not a numerical trial.

### The separating information is asymptotically time symmetric

The statistic S_n^even=integral F_n(q_t) dot dp_t is invariant under the
actual path reversal. It has equilibrium mean zero and source mean

    E_n S_n^even = a^2 h/2 - gamma tau sigma_n h.         (14)

Its second moments are uniformly bounded as n grows, using |F_n|<=a and
E w^2=tau+tau sigma_n/gamma<=tau+a^2/gamma^2. Consequently a nonzero
finite-window separation can also be witnessed with a reversal-even test
once n is large. No persistent observable time arrow is needed for this
same-thermal-class incompatibility. This does not contradict the nearby
broader reversible model supplied by the parity projection theorem.

## 5. Native equilibrium DOES approximate finite-resolution behavior

Use the same x,v,zeta and initial y phase to construct a free equilibrium
process with w_0=zeta and y_0'=w_0. Its difference from (1) is

    w_n-w_0=Y_n,
    y_n(t)-y_0(t)=integral_0^t Y_n(s)ds                 (lifted difference).

Stationarity of Y and Y'=F_n-gamma Y gives

    E Y_n^2 = E(F_n Y_n)/gamma = tau sigma_n/gamma.       (15)

Therefore the coupling obeys

    E integral_0^h |p_n-p_0|^2dt = h tau sigma_n/gamma,
    E sup_(0<=t<=h) d_torus(q_n(t),q_0(t))^2
                                      <= h^2 tau sigma_n/gamma. (16)

Every path functional with Lipschitz constants L_q for the position sup
metric and L_p for the momentum L2 metric consequently satisfies

    |E G(P_n)-E G(P_0)|
      <= (L_q h+L_p sqrt(h)) sqrt(tau sigma_n/gamma).     (17)

The same ordinary free equilibrium thus predicts this explicitly defined
class of finite-resolution consequences with error tending to zero. Full
trajectory TV and bounded-gain path observables answer different questions.
In particular, any statistic that maintains a fixed expectation gap in (17)
must have a diverging Lipschitz sensitivity in these path metrics.

## 6. Specified feedback does not automatically amplify the hidden difference

An explicit control extension is possible; it is not a claim for arbitrary
interventions. Add the SAME causal Markov feedback force u(t,x,v,y,w) to
the w equation in both sources, starting from the stationary baseline
preparations used above. The control does not act on x or v. Assume global
Lipschitz constant K in (y,w), uniformly in (t,x,v), with the usual growth
conditions for well-posedness. Both systems then retain the same x,v driver.

Let delta y=y_n-y_0 on a common torus lift and write delta w=Y_n+z.
Initially delta y=z=0, and

    (delta y)'=z+Y_n,
    z'=-gamma z+u(t,x,v,y_n,w_n)-u(t,x,v,y_0,w_0).

The upper derivative of Z=|delta y|+|z| is at most

    Z' <= (1+gamma+K) Z + (1+K)|Y_n|.

Set C_h=(1+K)exp[(1+gamma+K)h]. Gronwall and Cauchy--Schwarz give

    E sup |delta y|^2 <= C_h^2 h^2 tau sigma_n/gamma,
    E integral_0^h |delta w|^2dt
          <= 2(1+C_h^2 h^2) h tau sigma_n/gamma.          (18)

Thus fixed-horizon, fixed-gain feedback in this declared interface preserves
the vanishing predictive difference. The free controlled comparison need
not remain equilibrium while control is active; it is the same conventional
baseline model subjected to exactly the same controller. These are complete
controlled trajectories, not just fitted stationary moments.

This does not cover actuation on x/v, unbounded feedback gain, acceleration-
based path classifiers, or arbitrary discontinuous experiments. Such access
can change the inference boundary. Nor does it make the force family known
from data; n,a and the source class are supplied for the construction.

## 7. What observation actually costs

Statistic (10) requires the spatial phase sin(nx) and momentum increments.
Exact continuous position paths determine momenta mathematically, but finite
samples/noisy positions do not provide this for free. To control the force
error by eta uniformly, x resolution of order eta/(an) is sufficient; bounded
temporal discretization error also needs a specified cadence and noise model.
The exact test has unbounded sensitivity in the topology of (16) as n grows.
No fixed number of scalar observations buys that resolution.

The current results are existence, incompatibility and stability theorems.
They do not claim a favorable experimental acquisition cost or superiority
to force inference when velocities and calibrated response are available.
An equally informed conventional route already has Girsanov, Hodge/gradient
orthogonality, stochastic energetics and stable-system coupling. The proposed
addition is their explicit common physical family separating dissipation,
same-bath equilibrium explanation, and the resolution of consequential tests.
Historical priority is not established; source comparison is saved separately.

## 8. Revised scientific principle

Local thermalization closes the hidden-orientation loophole for proximity to
reversible path models. It does not collapse physical explanation to the
original Gibbs source class at unlimited observational resolution. A warranted
spatial regularity class can restore native compactness; a specified consequence
metric can instead give a quantitative guarantee without that regularity.
Which claim is useful must be decided before selecting the information metric.
