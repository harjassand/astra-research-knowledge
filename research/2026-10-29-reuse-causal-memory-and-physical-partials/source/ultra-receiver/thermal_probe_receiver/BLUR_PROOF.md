# A finite-exposure receiver for the distant quartic contrast

The root's exact Gibbs/Schur identity is the stationary input. This note
extends that input to an actual finite-duration read with correlated
sampling. It does not supply a physical instrument, the bath, calibration,
or independent equilibrium samples. FKG association, cooperative diffusion
comparison, semigroup gaps and passive calibration are ordinary principles.

## 1. Warranted model and the contrast

Let K be symmetric positive definite with K_ij<=0 for i!=j and
R_pv>0 (for example the two vertices lie in the same connected path), and

    dX=-[KX+alpha e_v X_v^3]dt+sqrt(2theta)dW, alpha>=0.

Only coordinate p!=v is observed. All other quartics are absent. R=K^-1
is entrywise nonnegative. Root's exact Gaussian elimination gives

    Cov_alpha(X)=theta R-eta R_.v R_v.,
    eta=[theta R_vv-Var_alpha(X_v)]/R_vv^2>=0.

For known reference alpha0 versus alpha>=Delta, the stationary port
variance decrease is at least

    s=(R_pv/R_vv)^2[theta R_vv-v(Delta)]>0.

The one-dimensional integral acquiring v(Delta) is a separate finite
computation in this folder. No N-state trajectory is simulated.

## 2. A dynamic contrast lower bound paying motion blur

Let C_alpha(t)=E_alpha[X(t)X_p(0)] be a COLUMN covariance, t>=0.
The stationary law has a log-supermodular density: off-diagonal mixed
derivatives of log density are -K_ij/theta>=0. The continuous FKG
inequality follows, for example, by applying finite-grid FKG on bounded
boxes and taking limits. Polynomial moments are finite. Hence its
increasing observables are positively correlated.

The diffusion is order-preserving under synchronous Brownian coupling.
At a first possible coordinate crossing, its drift difference in that
coordinate is -sum_(j!=i)K_ij Delta_j>=0; the cubic is diagonal and
does not violate the comparison. Thus P_t(X_v^3) is increasing. Global
sign symmetry gives its mean0, so FKG proves

    h_alpha(t)=E_alpha[X_v(t)^3 X_p(0)]>=0.               (1)

Differentiating the covariance column and using stationarity gives

    C_alpha'(t)=-K C_alpha(t)-alpha e_v h_alpha(t).

The harmonic reference has C_0(t)=theta exp(-Kt)R_.p. Its covariance
difference D=C_0-C_alpha obeys the EXACT variation-of-constants identity

    D(t)=exp(-Kt) eta R_pv R_.v
       +alpha integral_0^t exp[-K(t-r)]e_v h_alpha(r)dr.  (2)

All entries of both terms are nonnegative. Since
`[exp(-Kt)]_pp>=exp(-K_pp t)` for this cooperative matrix (expand the
nonnegative off-diagonal semigroup, or use its killed-walk form),

    C_0,pp(t)-C_alpha,pp(t)>=s_alpha exp(-K_pp t),
    s_alpha=eta R_pv^2>=s.                               (3)

This is a full nonlinear-in-alpha inequality, not a weak-quartic or
short-exposure approximation. It uses the M-matrix/one-quartic structure.
It is not asserted for arbitrary signed K or arbitrary unknown baths.

For a rectangular exposure of duration delta,

    Ybar=(1/delta)integral_0^delta X_p(t)dt,

stationarity and(3) prove

    Var_0(Ybar)-Var_alpha(Ybar)>=s B(K_pp delta),
    B(z)=2(z-1+exp(-z))/z^2, B(0)=1.                    (4)

In particular delta=1/K_pp retains at least2/e of the equilibrium
contrast. There is no need to shrink the exposure with s. That point
matters when detector averaging noise has a fixed spectral density,
so its variance is proportional to1/delta. Applying only the generic
absolute-blur error theta*delta/3 would unnecessarily demand an
exposure of order s and would impose a large extra noise cost. The
comparison in(4) instead uses the SAME known harmonic reference and
the nonlinear dynamics. Ordinary source-aware covariance methods are
allowed this construction too.

The harmonic reference exposure variance is computable exactly as

    b_delta=2theta/delta^2
       [delta K^-2-K^-3(I-exp(-K delta))]_pp.             (5)

Equivalent scalar matrix-series evaluation avoids cancellation; no
thermal data or harmonic-fit coefficient is granted free. Matrix K is
known. The expression has units of squared displacement.

## 3. Finite correlated readouts and a paid detector

Read nonoverlapping exposures beginning at t0+j*h, h>=delta:

    Z_j=Ybar_j+eta_j,
    eta_j independent N(0,sigma_delta^2).

The electronics are independent of the bath. For an explicitly warranted
white output-noise spectral density Sdet, `sigma_delta^2=Sdet/delta`;
otherwise that finite-exposure variance must be qualified directly.
No pointwise square of ideal white noise is observed. Constant read
variance while shrinking exposure is not assumed.

Root's Gaussian domination gives E X_p^4<=3(theta R_pp)^2. Jensen in
the exposure and independent Gaussian detector moments give

    E Z_j^4<=3S0^2, S0=theta R_pp+sigma_delta^2.

For two exposure functionals separated by a gap r, the reversible
Markov semigroup contracts centered L2 functions by exp(-kappa r),
kappa<=lambda_min K. Condition the earlier functional on its last
endpoint and the later one on its first endpoint; conditional
expectation cannot increase L2 norm. Independent detector noises make
cross-read covariance equal that of the squared exposure means. Thus

    Var[Q^-1 sum(Z_j^2-sigma_delta^2)]<=V_delta/Q,
    V_delta=3S0^2+6(theta R_pp)^2
                             exp(kappa delta)/(exp(kappa h)-1). (6)

Taking h=delta+1/kappa implies V_delta<=9S0^2. This bound uses
CORRELATED raw readouts, not effective IID samples. A smaller source-
specific correlation estimate may improve it, but none is granted here.

Starting the process from zero is also charged. The root's synchronous
contraction supplies

    B(t)=2sqrt(theta TrR)[sqrt(theta R_pp)+sigma_delta]
                  exp(-kappa t)+theta TrR exp(-2kappa t).

Using the same detector noise in the comparison and Jensen over an
exposure gives the same B(t0) upper for the expected absolute average
score difference from a stationary experiment. An initial second-moment
bound M0 uses the root's larger coupling constant. Actual initialization
and its energy qualification are inputs.

## 4. A finite classification contract

Let sL be a certified positive lower endpoint for the RHS of(4). Let the
combined reference, gain, temperature, detector-variance and other
model/calibration error in SCORE VARIANCE UNITS be at most sL/8.
For a chosen total error probability zeta, use

    B(t0)<=zeta*sL/16,
    Q>=128 V_delta/(zeta*sL^2).                           (7)

Stationary Chebyshev and coupling Markov bounds each fail with probability
at most zeta/2 when their allocated error is sL/8. Compare the measured
decrease from the qualified reference b_delta to sL/2. Under alpha0
the total decrease error is at most3sL/8; under every alpha>=Delta the
true decrease is at least sL. This separates the hypotheses with each
risk at most zeta. It is a sufficient plan and actually returns after
Q readouts; it is not a full time-series information lower bound.

The computational receiver returns t0,Q,delta,h and calibration budgets.
It acquires NO device data. It must mark an actual decision UNQUALIFIED
unless those physical access/calibration/initialization conditions and
the full observation record have been supplied. Knowing a reference
formula is distinct from acquiring detector/gain/temperature accuracy.

## 5. Ordinary comparators and physical scope

Passive Boltzmann/equipartition inference and exact integration-time
corrections are established. Perez-Garcia et al.,
[arXiv2305.07245](https://arxiv.org/abs/2305.07245), develops the full
joint sampled harmonic law with integration and sampling corrections,
including likelihood and common calibration statistics. That strongest
ordinary method receives the same K, bath, detector access and records;
our finite reference(5) is not a novelty claim. Its harmonic formulas
alone are not silently asserted to be exact for the hidden nonlinear
alternative; inequality(4) explicitly pays that comparison.

FKG and cooperative diffusion association are prior. The primary FKG
theorem is Fortuin--Kasteleyn--Ginibre, Commun.Math.Phys22(1971)89--103,
DOI10.1007/BF01651330. Herbst--Pitt1991,
DOI10.1007/BF01312211, is a governing diffusion-monotonicity antecedent.
The elementary checks above expose the exact conditions used; no claim
to have invented correlation inequalities or semigroup contraction is
made. Historical priority of the assembled finite receiver is UNKNOWN.

The thermal bath acting independently at every coordinate is an
ADDITIONAL warranted physical access, not automatically Johnson noise
in a resistor circuit. The same-bath driven susceptibility equals
Var(Y)/theta, so an informed active thermal experiment also sees the
g^2 contrast. The g^2 versus deterministic g^4 comparison changes the
internal bath interface and is not passive beating active on identical
hardware. A high-drive scalar DC comparator may spend peak U~1/g and
work of order g^-2; those resources must be charged rather than forbidden.
Unknown multiple quartics, unknown K/topology/mobility, unqualified
readout noise and actual device access are not solved by this theorem.
