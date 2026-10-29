# Quantitative static force balance and a warranted density floor

29 October 2026. Independent physical-frontier construction. This proves
a negative-norm residual and an explicit static Gibbs approximation. It
does not provide an effective controlled-path stability modulus.

## 1. Native domain and exact residual

Keep the side-2pi torus, unit masses, gamma,tau>0, smooth periodic
position-only F with ||F||<=A, and the stationary finite-entropy/Fisher
domain of the accepted bath identity. Let rho be the stationary law,
nu its position marginal, and

    s=grad_p log[rho/(nu M_tau)],
    sigma=gamma tau E|s|^2,
    R=F nu-tau grad nu.

For a periodic C1 vector test phi, with (Dphi)_ik=partial_k phi_i,
conditional momentum integration by parts gives

    E[p_i|q]=tau E[s_i|q],
    E[p_i p_k-tau delta_ik|q]=tau E[s_i p_k|q].

The stationary test phi(q) dot p then yields the exact weak identity

    <R,phi>=tau E[s dot (gamma phi-Dphi p)].             (1)

Momentum cutoffs are justified by the bounded-force moment estimates.
Stationarity of the position test |phi|^2/2 cancels the cross term in
E|gamma phi-Dphi p|^2. Consequently,

    |<R,phi>| <=sqrt(tau sigma/gamma)
       sqrt[gamma^2 E|phi(q)|^2+E|Dphi(q)p|^2]
     <=sqrt(tau sigma/gamma)
       sqrt[gamma^2||phi||_infinity^2
                     +P_2||Dphi||_infinity,op^2],       (2)

where P_2=(A/gamma+sqrt(d tau))^2 is a uniform upper bound on E|p|^2.
This is an explicitly defined W^(-1,1)-type control, with no force
derivative or hidden mixing premise. Fourier testing also gives

    |Rhat(k)|<=sqrt(tau sigma/gamma)*sqrt(gamma^2+|k|^2 P_2),

and hence an explicit H^(-a) bound for every a>d/2+1 by summing the
squared expression with weights (1+|k|^2)^(-a).

On the same stationary entropy domain, Shannon balance gives
I_p(rho)=d/tau. Expansion of the score square and energy stationarity give

    sigma=(gamma/tau)(E|p|^2-d tau)=E[F dot p]/tau.       (3)

Thus d tau+tau sigma/gamma can replace P_2. This identity is for the
baseline position-force, single-bath source, not arbitrary controlled
velocity-dependent drift. A small upper bound requires actual energy
precision and bath calibration; a lower entropy certificate is insufficient.

## 2. Elementary all-set bound

For t>0 define the free position-noise kernel and its variance

    K(v)=sqrt(2gamma tau)(1-exp(-gamma v))/gamma,
    V_t=int_0^t K(v)^2dv
       =(tau/gamma^2)[2gamma t-3+4exp(-gamma t)-exp(-2gamma t)].

Put D=pi sqrt(d), V=(2pi)^d, and

    m_t=V(2pi V_t)^(-d/2)exp[-D^2/(2V_t)]>0.

A nearest winding of the free Gaussian position density gives this lower
bound relative to normalized uniform position, independently of the
initial q,p. Inverse Girsanov has second moment at most
exp[A^2t/(2gamma tau)]. Cauchy--Schwarz, with the same stationary initial
law on both free and forced paths, therefore proves for every set E

    nu(E)>=exp[-A^2t/(2gamma tau)]m_t^2 u_Torus(E)^2.     (4)

This validates the root's quadratic all-set lower bound without any
initial momentum moment assumption. A positive smoothing bump then has
density floor of order delta^d, giving the root static rate
O(sigma^(1/(4d+4))). The next section strengthens the endpoint estimate.

## 3. Pointwise floor from an explicit terminal-position Gaussian bridge

Fix an initial state and work on the free Brownian reference. Its lifted
position at t is q_0+a_t p_0+Y_t, where

    a_t=(1-exp(-gamma t))/gamma,
    Y_s=int_0^s K(t-v)dW_v,
    Y_t~N(0,V_t I).

Condition on Y_t=r. Bayes' Gaussian conditional density on paths up to
s<t is proportional to the remaining Gaussian density
exp[-|r-Y_s|^2/(2V_(t-s))]/V_(t-s)^(d/2). Differentiating this likelihood
gives the conditional Brownian decomposition

    dW_s=dB_s+b_s ds,
    b_s=K(t-s)(r-Y_s)/V_(t-s).                          (5)

Under this conditioned law,

    E[r-Y_s]=[V_(t-s)/V_t]r,
    Cov(r-Y_s)=V_(t-s)[1-V_(t-s)/V_t]I.

Writing J_t=int_0^t K(v)dv therefore gives

    E int_0^t |b_s|ds
       <=|r|J_t/V_t+sqrt(d)int_0^t K(v)/sqrt(V_v)dv
       <=|r|J_t/V_t+2sqrt(3dt).                         (6)

The last step follows from concavity of K: K(w)>=w K(v)/v for w<=v,
so V_v>=v K(v)^2/3. The finite bound also makes the bridge drift
integrable almost surely and extends its Brownian innovation to time t.

Set a_0=A/sqrt(2gamma tau) and theta_s=F(q_s)/sqrt(2gamma tau). The
forced-path likelihood is Z=exp[int theta dot dW-(1/2)int|theta|^2].
The conditional stochastic integral has a common version: since F is
smooth and dq=p dt, theta has finite variation on each finite path,

    int theta dot dW=theta_t dot W_t-int W dot dtheta.

This pathwise integration-by-parts expression is identical under the
free law and every Gaussian bridge. No uniform bound on DF is used.
Under the bridge the integral against B has zero expectation; the drift
term has expectation at least -a_0 E int|b_s|ds. Conditional Jensen gives

    E[Z|Y_t=r]>=
      exp[-a_0(D J_t/V_t+2sqrt(3dt))-a_0^2t/2], |r|<=D. (7)

The conditional logarithm is integrable by (6) and bounded theta. The
inequality also holds if the conditional exponential expectation is
infinite. Disintegration gives the usual endpoint density almost
everywhere. Choosing a nearest winding and multiplying the free density
by (7) proves a UNIFORM forced position-transition density floor

    c_*=m_t exp[-a_0(D J_t/V_t+2sqrt(3dt))-a_0^2t/2]>0,  (8)
    J_t=[sqrt(2gamma tau)/gamma]
                         [t-(1-exp(-gamma t))/gamma].

Stationarity consequently implies dnu/du_Torus>=c_* almost everywhere.
This is a one-time position marginal statement. It does not regenerate
hidden momentum, make position Markov, or give global phase-space
contraction. The fixed t is a mathematical parameter, not an executed
reset or waiting operation.

## 4. Explicit smoothed Gibbs construction

Choose a nonnegative smooth Euclidean probability bump eta supported
in the unit ball. For 0<delta<=delta_0<=min(1,pi), periodize
K_delta(q)=V delta^(-d)eta(q/delta) relative to normalized torus measure.
Set C_0=V||eta||_infinity, C_1=V||grad eta||_infinity and
n_delta=K_delta*nu. Then n_delta>=c_* and W1(n_delta u_Torus,nu)<=delta.
Convolving (2) yields

    ||K_delta*R||_infinity <=sqrt(tau sigma/gamma)
       sqrt[gamma^2 C_0^2 delta^(-2d)+P_2 C_1^2 delta^(-2d-2)].

Because the smoothing kernel is nonnegative,

    tau grad n_delta=K_delta*(F nu)-K_delta*R,
    |K_delta*(F nu)|<=A n_delta.

Hence U_delta=-tau log n_delta is smooth with gradient ceiling A+e_delta,
where

    e_delta=c_*^(-1)sqrt(tau sigma/gamma)
       sqrt[gamma^2 C_0^2 delta^(-2d)+P_2 C_1^2 delta^(-2d-2)].           (9)

Scale U_delta by lambda=A/(A+e_delta), setting lambda=1 if both vanish.
Then ||grad U_delta^sharp||<=A. Its difference from U_delta has gradient
norm at most e_delta and oscillation at most D e_delta. For a normalized
exponential tilt by h, Hoeffding's centered exponential inequality gives
relative entropy at most (osc h)^2/8, and Pinsker gives TV<=osc(h)/4.
Therefore

    W1(nu_(U_delta^sharp),nu)<=delta+D^2 e_delta/(4tau).  (10)

For delta<=delta_0 this is delta+C sqrt(sigma)delta^(-d-1), with

    C=[D^2/(4tau c_*)]sqrt(tau/gamma)
                 sqrt[gamma^2 C_0^2 delta_0^2+P_2 C_1^2].

Choosing delta=[(d+1)C sqrt(sigma)]^(1/(d+2)), when it is <=delta_0,
proves the explicit STATIC fitting bound

    [(d+2)/(d+1)] [(d+1)C]^(1/(d+2)) sigma^(1/(2d+4)).  (11)

The constants are finite and explicit, potentially extremely large. No
optimality or practical efficiency claim is made.

## 5. Feasibility, sharpness and remaining acquisition obligation

Qualitative class-fit feasibility also follows independently from the
reviewed closure theorem. Normalized Lipschitz potentials of gradient
ceiling A form a compact class; the Gibbs density map is continuous.
Periodic mollification supplies smooth candidates preserving that ceiling.
One must fit this constrained class: positive sigma does not by itself
put unsmoothed -tau log nu within gradient ceiling A.

If an acquired position law has weak-distance error e_data and numerical
optimization error e_opt, the true fit error is at most best true class
fit+2e_data+e_opt. This is only a triangle inequality, not free independent
samples, density precision or optimization complexity.

A constant tilt F=epsilon e_i has sigma=epsilon^2/(gamma tau) and k=0
residual epsilon e_i. It saturates the square-root scaling. The earlier
oscillatory shear has residual F nu of nonvanishing L2 norm while sigma
tends to zero, so no strong residual or force reconstruction is inferred.

The construction needs a warranted UPPER bound on true physical sigma,
complete position information and the stated bath/source parameters.
The static heat identity requires actual instrument precision, bath
calibration and justified sampling. Estimating n_delta, its derivatives,
and a positivity floor under error remains an acquisition problem.

Finally, the static-to-control theorem transfers sufficiently accurate
static fitting qualitatively. No effective controlled-path error modulus
has been proved here. The new explicit static rate must not be presented
as a quantitative dynamical prediction guarantee.
