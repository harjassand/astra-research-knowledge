# All-time absolute passage CDF from separate well/slab source currents

Status: new finite receiving construction, not covered by the accepted older
survival wrapper. The inherited well-current receiver and this complete join
require separate whole reviews. This file changes no earlier source or receipt.

## Actual task and premises

The task is the CDF of first arrival at B={y>=1/2}, from the EXACT FULL Gibbs
law conditioned on A={y<=-1/2}, for the ordinary constant-SPD reversible
Langevin model F=v(y)U(z), v=1+kappa(1-y^2)^2. The raw positive quartic grammar,
constant isotropic/diagonal mobility interface, positive exact beta/kappa,
coercivity and complete task/budget validation are acquired by the pinned
well-current engine. It is not the engineered radial model. In particular
M_z=I is allowed without changing the actual generator. The explicit current
is a variational witness, not implemented control or an assumed fiber solver.

Let q=v^-alpha, alpha=m/4, M=int_A q, S=int_slab q, R=int_slab q^-1,
T0=beta M R, eta=S/M. The unknown angular partition cancels from all quantities.
The well-current engine proves the separate inverse-form estimates

 QA=<1A,K^-1 1A> <= B_A,
 QS=<1S,K^-1 1S> <= beta S^2 R(1+C_s),

for the killed generator K, after the zero-resolvent/full-tail joins. It also
outputs an outward U_A>=B_A/M. IMPORTANT: the new A-current does NOT establish
QS<=eta^2 B_A. Thus the old wrapper's single-current spectral formula may not
be substituted without a new argument.

## Separate-source spectral bound

Use the explicit scalar trial h=1 on A, h=0 on B and
h(y)=R^-1 int_y^(1/2) q(t)^-1 dt on the slab. It lies between0 and1 and has
Dirichlet energy C0=1/(beta R). The independently received trial-function and
separate-source theorem applies. Its spectral defect is bounded by

 epsilon <= C0( sqrt(B_A)+sqrt(B_S) )^2/M^2 -1.

Write b_A=B_A/(beta M^2 R), c_s=1+C_s. Substitution gives
(sqrt(b_A)+eta sqrt(c_s))^2-1. Weighted Cauchy yields

 (sqrt(b_A)+eta sqrt(c_s))^2 <=(1+eta)(b_A+eta c_s),

because the difference is eta(sqrt(b_A)-sqrt(c_s))^2>=0.
Thus a rational bound requiring no extra source square root is

 epsilon_bar=(1+eta_bar)(b_bar+eta_bar c_bar)-1,            (1)

where the acquired outward values satisfy eta_bar>=eta, c_bar>=c_s and
b_bar=U_A_upper/(beta M_lower R_lower)>=b_A. All factors are nonnegative.
In particular b_A>=1 follows from the scalar A-source Poisson lower bound;
this also makes the admitted epsilon_bar nonnegative. A negative computed
value is rejected rather than silently clipped.

The killed positive self-adjoint semigroup spectral lemma gives a uniform
absolute survival error epsilon_bar for the trial spectral correlation versus
exp(-k0 t), k0=1/T0. Its exact full-GibbsA initialization comparison adds

 I_bar=eta_bar+sqrt(eta_bar(1+eta_bar)).                   (2)

The square root is evaluated outward at a charged finite bit precision. No
conditional mixing, committor computation or spectral gap is supplied.

## One finite rational reference rate and optional time queries

The scalar intervals give

 k_low=1/(beta M_upper R_upper) <= k0
       <=k_high=1/(beta M_lower R_lower).

Set k_star=(k_low+k_high)/2. The previously received midpoint lemma gives

 sup_(t>=0)|exp(-k0 t)-exp(-k_star t)|
       <=(3/16)(k_high/k_low-1)=E_rate.                 (3)

It uses sup t exp(-a t)=1/(ea) and 1/(2e)<3/16, not a sampled time grid.
The final proof-bearing result is

 sup_(t>=0)|P_A[tau_B<=t]-(1-exp(-k_star t))|
       <=delta=epsilon_bar+I_bar+E_rate.               (4)

The original external KS request must contain this TOTAL delta. For optional
exact nonnegative rational query times, paid directed exponentials produce
outward actual-CDF intervals clipped to[0,1]. The interval at t=0 is exactly0.
Each query must also meet the original external absolute-width request.
All core scalar powers and optional exp operations share one total operation
budget. The outer verifier recomputes acquisition, scalar integration, source
bounds, all error joins and queries from the original raw input and ORIGINAL
external task, then strictly compares every proof-bearing field.

This is absolute CDF accuracy on the entire time axis, not relative tail
accuracy, exact exponentiality, arbitrary-start kinetics or a higher/exponential
moment theorem. The separate MFPT result is not inferred from CDF accuracy.
Approximate finite-bit preparation does not automatically preserve an unbounded
hitting-time mean. Mathematical model membership is checked; empirical
membership, parameters and physical preparation are not authenticated.

## Information and comparison scope

The new enabling operation is ordinary original unit-mobility all-time passage
prediction using explicit well redistribution rather than angular relaxation
reconstruction. The earlier accepted spectral and exponential arithmetic
machinery is deliberately reused, not claimed new. Ordinary Dirichlet/Poisson
variational and completely-monotone spectral tools get the same exact model
and acquired current. The stronger numerical certificate comes from the new
source witness and separate-source join, not exclusive access or a different
physical model. No priority, generic solver separation or physical upgrade is
claimed. Finite budgets or an intrinsic witness width may return UNKNOWN.
