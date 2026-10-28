# Two-pulse self-calibration of a hidden conservative transition operator

Status: new derivation in this worker; not independently audited. Historical
novelty, acquired physical access and practical advantage are UNKNOWN. This is
a conditional operation, not a claimed civilization-changing discovery.

## Input and accessible operation

There are n labeled internal states. A repeatable preparation has an unknown
probability vector p, with p_i>0. Between two pulse times a fixed unknown
column-stochastic matrix P acts on the unnormalized surviving population.
The pulse with label i applies R_i=I-a_i e_i e_i^T, with an unknown fixed
efficiency 0<a_i<=1. It removes that fraction of state i and leaves all other
states and all future dynamics of survivors unchanged. This is an assumption
about *state-selective loss*, not a supplied local measurement. Each trial has
one terminal scalar readout y=beta+gamma*1^T x, gamma>0, with unknown fixed
beta and gamma. Reset, pulse selectivity, timing, stationarity of efficiencies,
linearity of this aggregate detector, and conserved population between pulses
are interface premises. No state trajectory is observed.

Measure the n^2+2n+1 configurations:

- baseline y0;
- early-only pulse Ei for every i;
- late-only pulse Lj for every j;
- ordered pair (early i, late j) for every i,j.

An early pulse and a late pulse with the same label are allowed. Every trial
starts from the same p and ends at the same time. Thus aggregate detector
offset and global drift common to that fixed readout time can cancel, but
uncontrolled drift between configurations does not automatically cancel.

## Exact construction and proof

Write ell_i=y0-yEi and r_j=y0-yLj. Direct multiplication gives

    ell_i = gamma*a_i*p_i,
    r_j = gamma*a_j*(Pp)_j,
    C_ji = yPair_ji-yEi-yLj+y0 = gamma*a_i*a_j*p_i*P_ji.

Consequently B_ji=C_ji/ell_i=a_j*P_ji. Put c_i=1/a_i. Conservation says

    B^T c = 1.                                              (1)

If P is nonsingular, B is nonsingular and the unique reconstruction is

    c = B^(-T)1,
    a_i = 1/c_i,
    P = diag(c)B,
    gamma = sum_i c_i*ell_i,
    p_i = c_i*ell_i/gamma,
    beta = y0-gamma.                                       (2)

All quantities on the right are measured scalars or elementary linear algebra.
The formulas prove global uniqueness in the declared class, without a supplied
initial distribution, pulse efficiency, or detector gain/offset. There is no
spectral gap, detailed balance, sparsity, or stationary preparation assumption.
The n^2+2n+1 number counts *settings*, not acquired trials or physical cost.

The late singles provide an additional exact relation that is useful in noise:

    B diag(ell)c = r.                                      (3)

For singular P one can replace invertibility by full column rank of the stacked
matrix [B^T; B diag(ell)]. Equations (1) and (3) then identify c uniquely, and
(2) still follows. This is a sufficient condition; no necessity is claimed.
Complete mixing with stationary preparation fails this condition, and no
general singular-operator identifiability claim is made.

## Continuous-time generator

Suppose P=exp(tau Q), with Q_ji>=0 for j!=i, 1^T Q=0, and every exit rate
-Q_ii<=Lambda. Then P is nonsingular. If Lambda*tau<log(2),

    ||P-I||_1 <= 2*(1-exp(-Lambda*tau)) = rho < 1.           (4)

Indeed the chance of at least one jump by tau is at most
1-exp(-Lambda*tau), and each column's distance to its initial point mass is
2*(1-P_ii). The principal matrix logarithm satisfies log(P)=tau Q: Gershgorin
puts every eigenvalue of tau Q in the strip |Im z|<log(2)<pi, where the
exponential has the indicated principal logarithm. Equivalently the convergent
power-series logarithm of P agrees with tau Q. Thus Q=log(P)/tau is a
constructive generator recovery under the declared rate bound. An arbitrary
large lag does not identify a unique generator because matrix embedding can
be ambiguous; it also makes calibration numerically ill-conditioned.

## Deterministic readout-error and acquisition bound

Assume each of the M=n^2+2n+1 measured means has absolute error <=epsilon.
Let ell_min=min_i ell_i>2epsilon and a_min=min_i a_i. Every contrast error
is <=4epsilon and every ell error is <=2epsilon. Since 0<=B_ji<=1,

    max_ji |Bhat_ji-B_ji| <= b=6epsilon/(ell_min-2epsilon),
    delta=||Bhat-B||_1 <= n*b.                             (5)

Set kappa=||B^(-1)||_1. If kappa*delta<1, the Neumann perturbation formula
for (1) gives

    ||chat-c||_infinity <= h
       = kappa*delta/[a_min*(1-kappa*delta)].               (6)

Because ||B||_1<=1 and ||c||_infinity=1/a_min,

    ||Phat-P||_1 <= d = h+(1/a_min+h)*delta.                (7)

The bound remains an error bound even if a noisy raw estimate has negative
entries. Such an estimate must be rejected or fitted under physical
constraints; it is not certified as a stochastic matrix by this argument.
If d+rho<1, telescoping each power of the logarithm series gives

    ||log(Phat)/tau-Q||_1 <= d/[tau*(1-rho-d)].              (8)

The logarithm error is thus explicit and includes acquisition. At fixed
Lambda*tau<log(2), kappa<=exp(2Lambda*tau)/a_min follows from
B^(-1)=exp(-tau Q)diag(1/a) and ||Q||_1<=2Lambda. No exponentially deep
boundary observability assumption is hidden here; instead every state has
its own selective loss control and contributes to the aggregate detector.
If p_min or a_min is tiny, the small ell_min is charged rather than bypassed.

For independent bounded [0,1] scalar trials at each setting, Hoeffding and a
union bound give simultaneous mean error epsilon with probability >=1-alpha
using m>=log(2M/alpha)/(2epsilon^2) trials *per setting*. Total preparations
are M*m. A detector with another known bounded range rescales epsilon.
Equations (5)-(8) are a sufficient conservative design, not an efficient
statistical estimator or a physical work calculation.

## Pulse leakage, duration and drift are not free

If each realized pulse differs from its ideal R_i in induced 1-norm by at
most nu, and realized detector/preparation means contribute at most zeta
absolute error per setting, contraction of P and ideal loss pulses bounds
the population error of a two-pulse setting by 2nu (plus nu^2 if the realized
operator norm is only known <=1+nu). For physically substochastic realized
pulses both norms are <=1 and a telescoping argument gives exactly 2nu.
The readout budget epsilon must include 2gamma*nu+zeta in addition to sample
noise. A finite pulse is covered only after its actual map has such a bound.
Pulses that feed population back, alter the surviving dynamics, or have
unknown off-target action do not meet the exact theorem.

## Strong comparators and scope

1. An ordinary constrained joint likelihood or weighted least-squares fit gets
   *all the same configuration records*, unknown gains and initial population,
   plus the same conservation/rate promises. It can use (3), whereas the simple
   formula (1) does not. The construction makes no advantage claim over it.

2. The same loss controls can approximate state projectors: apply r loss pulses
   at every label k!=i. If a_k>=a_min and there is negligible evolution during
   this pulse block, the resulting preparation filter F_i has diagonal 1 at i
   and diagonal <=eta=(1-a_min)^r at all other labels. A second filter F_j at
   the endpoint makes total survival approximate p_i*P_ji, with nonnegative
   absolute bias <=2eta. Immediate F_i survival approximates p_i within eta.
   There is no supplied pulse calibration here either; the lower bound a_min
   is an acquisition promise and the pulse duration/energy cost is charged.
   This counted-endpoint comparator avoids differencing large signals and can
   be statistically much stronger for rare transitions. Each pair uses
   2r(n-1) elementary loss pulses instead of two. It cannot be ignored merely
   because it uses the candidate's own controls.

3. State-selective removal to obtain temporal correlations is established in
   ideal-negative-measurement experiments (Robens et al., Phys. Rev. X 5,
   011003, 2015, https://doi.org/10.1103/PhysRevX.5.011003). Self-consistent
   calibration and tomography are established general ideas. The particular
   finite reconstruction above is derived here; the search has not established
   historical novelty of it. It is not a new claim that removal is a readout.

No physical interface has been acquired or experiment run in this worker.
No practical advantage or foundational breakthrough follows from exact
reconstruction, synthetic trials, or successful code execution alone.
