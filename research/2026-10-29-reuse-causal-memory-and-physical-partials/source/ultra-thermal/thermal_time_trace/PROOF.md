# Time-trace information for one hidden quartic

This is a challenge of the SAME-bath temporal experiment, not an extension
of the root's IID snapshot lower bound by analogy. Two different results
are proved: a **finite-alternative continuous-path KL upper bound of order
g^2 per unit time**, and a **local stationary Fisher bound of order
polynomial(N) g^4** at a=0. The local statement is not a finite-Delta KL
bound. No observations, trajectories, physical instrument, optimal test
or improved complete filtering algorithm are claimed acquired.

The frozen root model is `inputs/ROOT_THERMAL_PROOF.txt`:

    dX=-(KX+a e_v X_v^3)dt+sqrt(2theta)dW, a>=0,
    K=K^T>0, K_ij<=0 (i!=j), only Y=X_p observed, p!=v.

K, mobility, theta, all-coordinate independent bath excitation, and the
absence of every other quartic are warranted inputs. They are not
physical conclusions of this calculation. R=K^-1, b=R_pp,d=R_vv,g=R_pv.
The actual scalar packet uses C's locked path N32, p1,v32,
K=3I-A_path, theta1, Delta1/2, zero drive, finite rectangular electronics
with PSD1/100, and 95%-each classification target. It contains no data.

## 1. An adapted port cancellation with a paid g^2 KL rate

Partition coordinates into p and H. Write B=-K_Hp>=0, Q=K_HH>0.
Under the alternative let Z_H be the *linear* hidden system driven by
the actual observed X_p and the same hidden Brownian noise:

    dZ_H=(B X_p-Q Z_H)dt+sqrt(2theta)dW_H,
    Z_H(0)=X_H(0).

Then R_H^err=Z_H-X_H satisfies

    R_H^err(t)=a int_0^t exp[-Q(t-s)] e_v X_v(s)^3 ds.

The augmented path U=(X_p,Z_H) solves the harmonic reference equation,
with only the port drift changed by minus

    F_t=a int_0^t k(t-s) X_v(s)^3 ds,
    k(t)=B^T exp(-Qt)e_v>=0.

This is an adapted drift. X_H can be reconstructed from U by the
well-posed nonlinear error ODE, so no inaccessible variable is being
claimed measured. This is a law comparison for an upper information
bound, not an implementable cancellation actuator. Its DC gain is

    r=int_0^infty k(t)dt=B^T Q^-1 e_v=g/b.               (1)

The last equality is the block-inverse identity. Positivity and weighted
Cauchy give

    E int_0^T F_t^2dt
      <=a^2 r^2 int_0^T E X_v(t)^6dt.                  (2)

For bounded stopped controls, ordinary Girsanov and data processing
bound path KL by initial KL plus E int F^2/(4theta). Stop when the
original state/control leaves bounded sets. Nonexplosion and finite
moments imply convergence of the controlled paths on compact time
intervals; lower semicontinuity of KL and (2) give the same inequality
without assuming an unbounded Gaussian sixth-moment exponential is
integrable. No false Novikov claim is needed.

### Stationary initialization

Root's exact Gaussian elimination proves, under pi_a,

    E_a X_v^6<=15(theta d)^3.

The augmented U initially has pi_a, while the stationary harmonic
reference has pi_0. Their full initial divergence is explicitly bounded:

    D(pi_a||pi_0)<=-log E_0 exp[-a X_v^4/(4theta)]
                 <=3a theta d^2/4.

Consequently, for the observed continuous coordinate,

    D(P_a^{Y[0,T]}||P_0^{Y[0,T]})
       <=3a theta d^2/4
          +(15/4)a^2 theta^2 d^3 (g/b)^2 T.            (3)

The initial term is deliberately the full-state upper, not an assertion
that the observed initial port carries that much information. It can
be loose. The asymptotic information-rate upper is the coefficient of T.

### Zero initialization, matching the actual burn-in plan

No initial-divergence term occurs if both models start at zero. If
K>=kappa I, Ito's formula for ||X||^(2m), and induction for m=1,2,3,
give for every t>=0

    E||X(t)||^6 <=(theta/kappa)^3 N(N+2)(N+4).

The extra quartic drift is dissipative. One direct induction uses
d E R^m/dt<=-2m kappa E R^m
+2m theta(N+2m-2)E R^(m-1), R=||X||^2.
Thus

    D(P_a^{Y[0,T],zero}||P_0^{Y[0,T],zero})
      <= [a^2 theta^2 N(N+2)(N+4)/(4kappa^3)]
                                  (g/b)^2 T.          (4)

This is looser in N than (3), but applies to the actual zero-start
experiment, including any discarded burn-in. It does not import a
stationary Fisher result into a transient experiment.

Any finite bandwidth, rectangular integration, independent detector
noise, subsampling, adaptive choice of *readouts*, or subsequent
nonlinear filtering is a parameter-independent channel of the ideal
passive port path. KL cannot increase. These bounds therefore include
the declared finite noisy records without supplying a noiseless device.
Actuating the dynamics, changing bath covariance, measuring more ports,
or changing the initial preparation is a different experiment.

For testing 0 against Delta, with each error <=p<1/2, Pinsker requires
KL>=2(1-2p)^2. Insert a=Delta in (3) or (4). This also constrains the
composite alternative a>=Delta, since it contains that one alternative.
The experiment remains exponentially costly with fixed-gap endpoint
g=1/F_(2N+2); (3),(4) do NOT match the snapshot g^-4 exponent.

## 2. Exact stationary harmonic-reference path score

Now initialize each parameter at its own stationary law, and take only
the one-sided derivative at a=0. Under reference a=0, X is a stationary
Gaussian OU process with covariance theta R and constant diffusion.
The full-data score on [0,T] is

    S_T=-(X_v(0)^4-3theta^2 d^2)/(4theta)
        -(1/sqrt(2theta)) int_0^T X_v(t)^3 dW_v(t).       (5)

Its information is

    E_0 S_T^2=6theta^2 d^4+(15/2)theta^2 d^3 T.        (6)

The initial term and martingale are orthogonal. All the required
polynomial moments are finite. Here is a precise one-sided
quadratic-mean qualification, without granting a positive Gaussian
sixth-moment exponential. Nonexplosive, locally bounded drift changes
give the localized Girsanov density; removing the stops is justified
by nonexplosion of both laws. Write this full path density L_a, and
its score at a as S_a. Its exact norm is

    E_a S_a^2=Var_(pi_a)(X_v^4)/(16theta^2)
                          +T E_(pi_a) X_v^6/(2theta).

The right side is continuous as a down to0, by the scalar quartic tilt
and Gaussian domination on compact nonnegative parameter intervals.
The explicit likelihood and its polynomial score are pointwise smooth
at0. Therefore sqrt(L_a) S_a converges in probability to S_0, has L2
norm converging to ||S_0||2, and is L2 bounded. Weak L2 convergence
followed by norm convergence proves strong L2 convergence. Integrating
d sqrt(L_a)/da=sqrt(L_a)S_a/2 gives differentiability of sqrt(L_a) in
L2. This proves the needed one-sided quadratic-mean statement. The
ordinary observed-score identity is conditional expectation,

    S_T^obs=E_0[S_T|observed record].                   (7)

This is Fisher's smoothing identity, not a new filtering formalism.

An integration by parts using Ito X_v^4 makes its *locality in hidden
Gaussian coordinates* explicit:

    S_T=3theta d^2/4-[X_v(0)^4+X_v(T)^4]/(8theta)
          +(3/2)int_0^T X_v^2dt
          -(1/(2theta))int_0^T X_v^3(KX)_vdt.          (8)

For endpoint v=N of the unit path, this is a centered even functional
of only the trajectories (X_(N-1),X_N). It does not require the rest
of the hidden path. Its Hermite rank is at least2. This precise
locality is what permits a spatially small complete-path bound.

## 3. Gaussian path canonical correlation controls the score

Let rho be the maximal linear Gaussian correlation between the
Hilbert spaces generated by the ideal port trajectory and the remote
two-coordinate trajectory. Both can be extended to all real times to
upper bound the correlation of the finite [0,T] subspaces.

For jointly Gaussian Hilbert spaces, conditional expectation contracts
a centered functional of Hermite rank at least m in L2 by rho^m.
This is the ordinary Gebelein/Gaussian-chaos inequality. A direct
proof expands Wick exponentials: conditioning maps a degree-m Wick
polynomial to degree-m Wick polynomials of the projected linear
Gaussian variables; their tensor norm contracts by rho^m. Density
gives the statement for general L2 functionals. Nourdin–Peccati–Yang,
2019, Theorem2.3 and §5 give a primary theorem/proof in exactly this
isonormal-Hilbert formulation.

Applying m=2 to (8), then squaring, gives

    I_port,T(0)<=rho^4[6theta^2 d^4+(15/2)theta^2 d^3T]. (9)

This is a bound for the whole ideal temporal record, not for IID
snapshots. Arbitrary parameter-independent measurement processing
remains bounded by (9). It is still only local at a=0.

## 4. A fully acquired rho bound for K=3I-A_path

The stationary harmonic spectral density is

    S(omega)=2theta (K^2+omega^2 I)^-1=2theta M(omega).

Put J={N-1,N} and p=1, N>=4. Since eigenvalues of K lie in (1,5),

    S_pp>=2theta/(25+omega^2),
    S_JJ>=(2theta/(25+omega^2)) I.

The covariance theta e^(-K|t|)R has nonnegative entries, so its Fourier
transform obeys |M_ij(omega)|<= (K^-2)_ij. Also

    omega^2 M=I-K^2M.

K^2 has first row (10,-6,1,0,...). Hence for j in J,

    (25+omega^2)|M_1j|
      <=35(K^-2)_1j+6(K^-2)_2j+(K^-2)_3j=:U_j.        (10)

The norm of S_pp^-1/2 S_pJ S_JJ^-1/2 is at most
sqrt(U_(N-1)^2+U_N^2). A Fourier Cauchy inequality bounds all
cross-correlations of time-integrated linear functionals by this same
quantity; approximation and Hilbert closure include point values and
the continuous trajectory. Thus no time-grid/precision limit is hidden
in this mathematical upper bound.

All U_j are acquired by continuants, not a spectral-fit oracle. Set
D_0(c)=1,D_1(c)=c,D_n(c)=cD_(n-1)(c)-D_(n-2)(c), evaluated at c=3.
Let

    g=1/D_N, mu=D_N'/D_N=Tr K^-1.

The exact inverse formula R_ij=D_(i-1)D_(N-j)/D_N (i<=j) and
K^-2=-dR/dc give

    U_N=g(61mu-12),   U_(N-1)=g(183mu-97).

Therefore the explicit input-qualified bound is

    rho^2<=min(1,g^2[(61mu-12)^2+(183mu-97)^2]).         (11)

Since mu<=N, this is at most min(1,37210 N^2g^2). The polynomial
constants are conservative, but (9) gives the genuine local
information-rate bound O(N^4g^4). No numerical frequency maximization
or unbounded sampling rate is an acquisition premise.

## 5. The strongest ordinary local comparator is explicit

Introduce a *linear* shunt parameter c in the SAME harmonic model,
potential x^TKx/2+c X_v^2/2. Its full stationary score is

    S_lin=-(X_v(0)^2-theta d)/(2theta)
              -(1/sqrt(2theta))int_0^T X_v dW_v.

Wick's identity X_v^3=3theta d X_v+:X_v^3: and the corresponding
fourth-moment identity give the EXACT orthogonal split

    S_T=3theta d S_lin+S_4,                            (12)

where S_lin is in the second Gaussian chaos, and S_4 is in the
fourth. Ito integral increments are independent of the past Gaussian
integrands, so the normal-ordered cubic integral is pure fourth chaos.
The variances are

    I2_full=(9/2)theta^2 d^4+(9/2)theta^2 d^3T,
    I4_full=(3/2)theta^2 d^4+3theta^2 d^3T.

Gaussian conditioning onto the ideal path, or a fixed linear set of
Gaussian-noisy measurements, preserves chaos order. Consequently

    I_obs,quartic(0)=(3theta d)^2 I_obs,linear(0)+I_obs,4,
    0<=I_obs,4<=rho^8 I4_full,
    I_obs,quartic(0)<=rho^4 I2_full+rho^8 I4_full.       (13)

For a finite mean-zero Gaussian reference record z with covariance C0,
the ordinary linear-shunt likelihood score is the executable quadratic
form

    (1/2)[z^T C0^-1 C_c' C0^-1 z-Tr(C0^-1 C_c')].

C_c' is obtained by differentiating the known harmonic covariance
with the SAME exposure, sampling, bath and detector noise. The
quartic's entire second-chaos score is 3theta d times this form.
The complete nonlinear likelihood receives those same inputs and
is not artificially restricted to a variance statistic. At large
separation, the additional non-Gaussian *local* information is suppressed
by rho^8, whereas the ordinary Gaussian component has the rho^4
upper. No new score/likelihood algorithm or finite-Delta validity is
claimed. We have not acquired or run such a likelihood on device data.

There is a quantitative SAME-record consequence. Use C's fixed Gaussian
reads at delta=1/3,h=4/3 (the warranted kappa lower1), noise variance
3Sdet, and let S0=theta b+3Sdet. C's nonlinear covariance contrast,
differentiated at0, gives a magnitude at least

    mprime=3theta^2 d g^2 B0, B0=2/e>8/11,

for the derivative of each exposure variance. For the average-square
statistic A_Q, its reference variance is <=9S0^2/Q and it lies entirely
in the second chaos. Cauchy with its exact score derivative therefore
gives the finite-record lower

    I_obs,2 >=Q theta^4 d^2 g^4 (8/11)^2/S0^2.         (14)

The record ends at T_Q=(Q-1)h+delta<=Qh. Combining (13),(14), for EVERY
Q>=1, the extra non-Gaussian reference information obeys

    I_obs,4/I_obs,2
       <=rho^8 S0^2[(3/2)theta^2 d^4+3theta^2 d^3 h]
                    /[theta^4 d^2 g^4(8/11)^2].       (15)

For K3 and fixed theta,Sdet this is O(N^8g^4). In the actual N32 source
the exact rational consumer returns the numerical bound in
`LOCAL_COMPARATOR.json`. This qualifies local near-sufficiency of the
ordinary Gaussian covariance likelihood on those SAME finite noisy
records. It does not say that a variance statistic is optimal (the
Gaussian likelihood uses all correlations), nor does it establish any
finite-Delta near-sufficiency or physical receiver performance.

## 6. Why this does not close the finite-Delta g^4 question

Evenness alone is insufficient for a global KL contraction with rho^4.
For a Gaussian channel W=rho U+sqrt(1-rho^2)Z, change the input from
N(0,1) to the even N(0,s). As s goes to infinity, the ratio

    D(N(0,1+rho^2(s-1))||N(0,1)) / D(N(0,s)||N(0,1))

tends to rho^2, not rho^4. This is a counter to the proposed *generic*
even-input entropy lift, not to this confining quartic's path family.
The path likelihood's evenness gives a rho^4 chi-square contraction
if its full L2 norm is qualified, but an exponentially-in-T full
chi-square cost cannot simply be replaced by a linear information
rate. No such missing bound is supplied here.

Nor does the stationary local result automatically transfer to the
zero-start trace after a finite burn-in. The root/C moment-coupling
receiver pays finite-risk errors directly; that is not a path-Fisher
continuity theorem. Equations (3),(4) are the available honest global
finite-alternative path statements. An improved finite-Delta rate,
or a source-aware temporal test attaining g^-2 instead of g^-4, remains
UNESTABLISHED. This assignment does not claim time traces and IID
snapshots have identical information.

## 7. Actual acquisition and physical scope

`compile_interface.py` executes only exact continuant recurrences and
rational arithmetic on C's already declared N32 source. It acquires
g,b,d,TrK^-1,TrK^-2 and the displayed global/local information
coefficients. `INTERFACE.json` preserves exact fractions and display
values. The run used 31 continuant steps /93 integer recurrence updates,
at most53-bit continuant integers, and .0000876 seconds after imports.
There were zero new scalar Gibbs integrals, trajectories, readouts,
random bits or physical actions. General scalar acquisition costs
O(N) integer steps with O(N)-bit continuants for this path, so the
arithmetic is not unit-cost over exponentially small g.

At theta1,a=Delta1/2 the stationary KL coefficient in (3) is
4.6408495268e-28 per native time unit. Its full initial upper is charged,
giving a 95%-each duration lower >3.3728e27. From zero, (4) gives
2.1745202974e-23 and duration lower >7.4499e22. Different initialization
experiments are kept separate. These are necessary durations for an
even stronger ideal observation; they remain valid under the declared
finite exposure/noise channel, but supply no actual observed decision.

At the stationary a0 reference, (13) bounds the leading local Fisher
rate by2.0315481706e-41 and the fourth-chaos rate by1.0971760466e-81.
These are local information upper bounds, not required durations for
testing the fixed Delta. The root IID g^4 theorem remains confined to
its stated snapshot interface.

The same scalar recurrence also supplies a travel-time/long-exposure
interface handed to C; its governing lemma is `LONG_EXPOSURE_INTERFACE.md`.
C owns the receiver/retention composition, finite-risk budget, burn-in,
exposure comparison and physical calibration. This package does not
duplicate that receiver. Generic full nonlinear filtering/likelihood,
Gaussian smoothing, Girsanov, Gebelein contraction, Brascamp–Lieb and
birth-death/hypoexponential laws are credited ordinary methods. Priority,
practical advantage, physical bath/readout acquisition, and a cure of
the fixed-gap exponential-depth cost are not established.
