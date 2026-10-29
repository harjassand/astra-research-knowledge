# Finite native-position acquisition and reusable Gibbs selection

29 October 2026. Independent construction by
producer-workspace/different_consequential_opening; root subsequently checked the proof at
the preserved exact version. No physical samples were acquired. The later
QUANTITATIVE_CONTROL_FROM_STATIC_INFORMATION.md supplies a controlled rate
in named analytic constants, whose numerical values remain uninstantiated.
The original qualitative transfer below remains valid.

Dependency: physical_frontier/MARKOV_INTERVENTION_CLOSURE_INDEPENDENT_PROOF.md
section 7, SHA256 590d9c4d165f3cce554ee5f843a9ef44cb6fa9a79c9a7d77a56f132cd65a234c.
Root intervention theorem SHA256
db1dcfba5eda825e3ba6465736072bc2e0761681c95ef732d6fc2c24075a24ca.
This note constructs finite static-law selection; it does not duplicate the
controlled-limit proof. STATIC_INFORMATION_TO_CONTROL.md section 4 now
supplies an explicit population approximation ceiling, separately reviewed.

## 1. Acquired information and finite guarantee

Use the side-2pi native configuration torus, dimension d, diameter
D=pi sqrt(d), calibrated temperature tau>0 and force ceiling A.
Data are N genuinely independent draws q_i from the source's COMPLETE
stationary position law nu_F. Reports obey d(qhat_i,q_i)<=eta_pos in the
calibrated native actuator coordinates. Independence is a preparation
contract; one stationary trajectory does not supply it. Position-error
bounds may be dependent across reports. Their calibration must be warranted.

Let G_A be Gibbs position laws proportional to exp(-U/tau), for periodic
A-Lipschitz U, modulo constants, and

    Delta_A(F)=inf_(nu_U in G_A) W1(nu_F,nu_U).

Smooth potentials are dense in this class. Neither physical entropy,
coordinate completeness nor bath calibration is inferred from these data.

The scheme returns a finite representation of smooth Uhat with
||grad Uhat||<=A. If the empirical grid law phat has error e_N in W1,
the grid radius is r, smoothing displacement is at most b and the total
certified optimization/coefficient error is eta_opt, then

    W1(nu_F,nu_Uhat)
      <=Delta_A(F)+2e_N+kappa(r,0)+kappa(r,b)+eta_opt,     (1)

    kappa(r,b)
      =min{D, r+D min[1,(exp(2A(r+b)/tau)-1)/2]}.        (2)

The actually achieved grid transport cost Lhat gives the useful
a posteriori static-fit certificate

    W1(nu_F,nu_Uhat)<=e_N+Lhat+kappa(r,b).               (3)

Root's explicit approximation theorem can replace Delta_A(F) in (1) by

    delta+D min{1,D epsilon_delta/(4tau)},

with epsilon_delta and all constants specified in
STATIC_INFORMATION_TO_CONTROL.md, equations (10)--(14).
Its optimized order is O(s^(1/(4d+4))) for an independently warranted
baseline entropy ceiling s. This note does not re-audit that new bound.
The controlled-error modulus remains qualitative despite this effective
static approximation ceiling.

## 2. Explicit distribution-free sample costs

For the empirical true-position law nu_N, dyadic partitions into
2^(d ell) cells yield

    E W1(nu_N,nu_F)
      <=b_(N,J):=2D 2^(-J)
          +(D/sqrt(N)) sum_(ell=1)^J 2^[ell(d/2-1)].     (4)

Ordinary proof: move both measures to level-J centres, costing at most
2D 2^(-J). Route cell-mass differences along the nested centre tree.
Each edge at level ell has length at most D 2^(-ell).
For M cells, multinomial variance and Cauchy--Schwarz give
E||phat-p||_1<=sqrt(M/N). Summing the edge costs proves (4).
No equilibrium or density assumption enters this sampling statement.

Replacing one sample changes W1 by at most D/N. Bounded differences
therefore give, with probability at least 1-alpha,

    W1(nu_N,nu_F)<=b_(N,J)+D sqrt[log(1/alpha)/(2N)].

For completeness, expose samples one at a time. Each conditional Doob
martingale difference has conditional range at most D/N. Hoeffding's
exponential bound then gives total centered moment generating function
at most exp(lambda^2 D^2/(8N)); Chernoff minimization gives the displayed
one-sided tail exp(-2N t^2/D^2).

If reports are rounded to a fitting grid of radius r, it suffices to use

    e_N=eta_pos+r+b_(N,J)+D sqrt[log(1/alpha)/(2N)].     (5)

An uncertain positional-calibration event spends its own failure budget.
It is not made valid by the independence of the physical configurations.

For d=1 choose J=ceil(log2 N); for d>=2 choose
J=floor(log2 N/d), or optimize the explicit finite expression (4).
The following convenient bounds follow from geometric sums:

    d=1: b<=2D/N+D/[(sqrt(2)-1)sqrt(N)];
    d=2: b<=D[4+0.5 log2 N]/sqrt(N);
    d>2: b<=D[4+a_d/(a_d-1)]N^(-1/d),
          a_d=2^(d/2-1).

Thus sufficient statistical sample counts at fixed confidence scale as
epsilon^-2 for d=1, epsilon^-2 log^2(1/epsilon) for d=2,
and epsilon^-d for d>2, with explicit dimension-dependent constants.
These are sufficient bounds, not claims of sharp minimax constants.
N must satisfy (5) along with the separate observation/grid budgets.

## 3. A cheaper conventional route than exhaustive potential search

Use a uniform grid x_1,...,x_M, M=m^d, radius r=D/m.
Fit probability masses p by the ordinary transport LP

    minimize sum_(a,b) d(x_a,x_b) pi_ab
    subject to pi_ab>=0,
      sum_b pi_ab=phat_a,  sum_a pi_ab=p_b,
      p_i<=exp[A d(x_i,x_j)/tau] p_j for all i,j.       (6)

There are M^2+M variables, 2M equalities, M(M-1) ratio inequalities
and O(M^2) nonzero coefficients. Data binning costs O(Nd).
The solve, coefficient precision and gap certification remain additional
computation; O(M^2) is a problem-size bound, not a runtime claim.

Every feasible p is positive, with p_i>=exp(-AD/tau)/M.
Set v_i=-tau log p_i, subtract v_1, and form the McShane envelope

    V(q)=min_i[v_i+A d(q,x_i)].                         (7)

The ratio constraints imply |v_i-v_j|<=A d(x_i,x_j), so V(x_i)=v_i.
The envelope is periodic and A-Lipschitz. Convolve with a known smooth
periodic probability kernel k_b of expected displacement at most b:

    Uhat=k_b*V-(k_b*V)(0).                             (8)

This is smooth, with gradient ceiling A. Periodic Gaussian convolution
with Euclidean standard deviation b/sqrt(d) is one explicit choice.

For q in the cell of x_i,
|(k_b*V)(q)-v_i|<=A(r+b). True Gibbs cell weights therefore differ
from exp(-v_i/tau) times cell volume by factors in
[exp(-A(r+b)/tau),exp(A(r+b)/tau)]. Normalization bounds cell-mass TV
by min{1,[exp(2A(r+b)/tau)-1]/2}; quantizing within cells costs r.
This proves W1(nu_Uhat,sum p_i delta_xi)<=kappa(r,b).

For any U in G_A, normalized weights exp[-U(x_i)/tau] are LP-feasible
and approximate nu_U to kappa(r,0). Optimality, two data-error terms
and the preceding reconstruction bound prove (1). One data-error term
and the achieved transport cost prove (3). EVERY near-minimizer satisfies
the guarantee; no unique optimizer is required.

## 4. Finite numerical intervals and certificates

Distances, exponentials, logarithms and convolution are not free reals.
Use warranted intervals dminus<=d<=dplus and
cminus<=exp(A d/tau)<=cplus, with rational 1<=cminus.
The inner rational LP p_i<=cminus_ij p_j preserves the actual force
ceiling. The uniform vector remains feasible.

The possible loss from inward coefficients is explicit. Any outer-feasible
p can be replaced by (1-lambda)p+lambda uniform. For each i!=j its
inner-constraint violation is at most

    (1-lambda)(cplus_ij-cminus_ij)
                  -lambda(cminus_ij-1)/M.

It is therefore enough to choose

    lambda_coeff=max_(i!=j)
      (cplus_ij-cminus_ij) /
      [(cplus_ij-cminus_ij)+(cminus_ij-1)/M].            (9)

This moves a law by at most D lambda_coeff in W1.
For A>0 and distinct grid points, refining intervals makes
lambda_coeff tend to zero. A=0 is exactly the uniform-law case.
This proves that inward coefficients do not silently exclude saturated
target potentials at an uncontrolled cost.

A rational feasible transport plan scored with dplus is an upper
certificate. A rational dual feasible for dminus and the inner ratios
gives a lower certificate. Their gap plus D lambda_coeff is a valid
eta_opt in (1). Rounding a floating candidate to rational probabilities
can be repaired by mixing with uniform: for a positive violation
v_ij=p_i-cminus_ij p_j, choose a mixture fraction at least

    v_ij/[v_ij+(cminus_ij-1)/M].

This preserves exact normalization and restores all constraints.
An exact residual transport can repair rounded transport marginals.
The executable records these rational certificates on a modest 1D fixture;
its floating solve is a proposal, not the mathematical certificate.

The mass floor exp(-AD/tau)/M exposes the logarithm precision cost:
absolute probability accuracy of order
exp(-AD/tau)epsilon_v/(M tau) suffices for potential accuracy epsilon_v.
Bit precision includes log M, AD/tau and log(tau/epsilon_v).
The energies remain computable interval-defined numbers -tau log p_i.

Representation (7)--(8) consists of finite grid data and a specified kernel.
Evaluating V costs O(Md); smoothing and force evaluation require numerical
integration. With an A-Lipschitz potential evaluated to error beta on
a quadrature grid of radius rho, Gibbs integration contributes at most

    rho+D min{1,[exp(2(A rho+beta)/tau)-1]/2}

to W1. Gaussian convolution itself can be bounded by truncating the
Gaussian tail and integrating a known Lipschitz integrand on a finite
mesh. Refinement and its node count must be charged. It does not require
physical equilibrium samples, but it does require computation and precision.

Here is an explicit convolution budget. Shift V so 0<=V<=AD, and put
sigma_b=b/sqrt(d), phi_max=(2pi)^(-d/2), L_phi=phi_max exp(-1/2).
For a standard Gaussian G, truncate to [-R,R]^d; its discarded mass is
at most q_tail=2d exp(-R^2/2). Use a midpoint mesh of radius rho_z and
normalize its Gaussian weights. Write Vol=(2R)^d. If q_tail<=1/4 and
Vol rho_z L_phi<=1/4, the convolution error is at most

    AD q_tail
       +2 Vol rho_z[A sigma_b phi_max+2AD L_phi]

plus the warranted node-evaluation and arithmetic error. This follows by
bounding numerator and denominator Riemann errors separately; the computed
denominator is at least 1/2. A grid with ceil(R sqrt(d)/rho_z)^d nodes
suffices. Every constant, Gaussian weight, log energy and torus distance
can be enclosed in rational intervals; refine until the displayed upper
bound meets its budget. This specifies a finite evaluation operation.
The executable below certifies the LP and energy intervals, not an executed
convolution or force simulator.

## 5. Explicit exhaustive finite net, for comparison

For A>0, normalize U(0)=0, so |U|<=AD. For a target potential error epsilon,
use grid radius r_net<=epsilon/(16A), value spacing delta=epsilon/8,
and smoothing displacement b_net<=epsilon/(8A).
Enumerate all arrays of multiples of delta in
[-AD-delta,AD+delta], fixing the zero-grid value to zero.
Form (7), then smooth and normalize.

Rounding a true target's grid values downward gives an envelope between
U-delta and U+2A r_net. Therefore smoothing and normalization yield

    ||U_candidate-U||_infinity
       <=2delta+4A r_net+2A b_net<=epsilon.

All enumerated arrays produce admissible A-Lipschitz envelopes, even when
the arrays themselves violate the Lipschitz constraints. With
m_net>=16AD/epsilon and M_net=m_net^d, candidate count is at most

    H<=[2 ceil(8AD/epsilon)+3]^(M_net-1).               (10)

A potential error epsilon changes its Gibbs law in W1 by at most
D min{1,[exp(2epsilon/tau)-1]/2}. Uniform objective integration error xi
and eta-near-minimization then give total static-fit error at most

    Delta_A(F)+2e_N
      +D min{1,[exp(2epsilon/tau)-1]/2]+2xi+eta.

This is finite in principle but is a poor default beside LP (6) on the
same information. Ordinary convex methods remain the stronger route here.
For A=0 the net is the singleton constant potential.

## 6. Reuse, preparation and the remaining stopping boundary

For sources with sigma_j->0, let N_j->infinity while positional, grid,
smoothing and numerical errors tend to zero. Equations (1) and the
population approximation ceiling give W1(nu_Fj,nu_Uhatj)->0 in probability.
Summable failure budgets give eventual almost-sure control of all sample
events across batches. The static-law corollary then gives, for each
fixed B,T, uniform controlled path convergence over all admitted bounded
Markov forces, with its fixed-record TV and finite-Wasserstein extensions.
The selected potential serves the whole interface.

The finite static-fit certificate (3) is effective. A stopping rule for a
requested controlled error still needs an effective entropy/static-fit to
controlled-error modulus, or additional acquired response information.
Small static mismatch alone does not supply the missing threshold.

Selection does not physically prepare Gibbs states or acquire independent
native configurations. For a computational model, uniform-position rejection
sampling needs at most exp(AD/tau) expected proposals: use the unnormalized
smoothed envelope, whose value lies in [min_i v_i,min_i v_i+AD], with
interval evaluations and random-bit accuracy. Additional interval slack
adds its explicit acceptance overhead. Maxwell
momentum is a separate ordinary initialization. Physical preparation is a
different operation. Prediction also requires solving controlled Kramers
dynamics with the selected intervention and a solver-error guarantee.

An arbitrary mathematical Borel u may be noncomputable. The uniform
stability theorem does not supply an executable simulator for every such
u; an actual protocol needs its description, sensing, execution and
numerical approximation contract. No controlled mean lifetime or unbounded
time consequence follows from the finite-window theorem.

The scientific addition is static-information sufficiency for reusable
controlled prediction in the native low-entropy class. Transport LP,
ratio constraints, Lipschitz extension, Gibbs inversion and sampling are
conventional constructions. No computational speedup is claimed.

## 7. Saved executable check

certified_gibbs_grid_selection.py implements the 1D grid LP and a separate
exact-rational verifier. GIBBS_GRID_EXACT_CERTIFICATE.json uses the fixed
histogram [2,4,8,16,18,10,4,2], A=tau=1 and b=1/20. This histogram is
an arithmetic fixture, not acquired native data or an iid experiment.

Pi is enclosed by Machin's formula and alternating arctangent series;
exponentials by positive Taylor sums and geometric remainder bounds;
logarithms by range reduction and the atanh series. All interval endpoints
are rounded OUTWARD to rationals. The verifier recomputes them and checks
primal marginals, ratio constraints, dual feasibility and the gap exactly.

The verified transport upper cost is 0.004714926423083843, the dual lower
cost is 0.004714926364895322, and the total optimization error including
inward-coefficient loss is at most 5.818852122984356e-11 (rounded displays;
exact rationals are saved). A separate A=0 run returns the uniform vector
and verifies the degenerate case. No continuum dynamics or physical
preparation was tested. Smooth convolution is finitely represented and has
the explicit quadrature budget above; it was not numerically executed.

