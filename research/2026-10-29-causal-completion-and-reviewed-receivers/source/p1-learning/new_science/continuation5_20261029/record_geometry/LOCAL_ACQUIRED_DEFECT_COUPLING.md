# A scoped bridge from acquired local L2 defects to positive many-body predictions

29 October 2026. Complementary construction in the existing Astra P1 role.
The receiving argument is ordinary graphical/Dobrushin coupling. The useful
bridge is the identification of a physically acquired forcing term and the
precise stationary or local-density contract needed to use it. No priority
is claimed for the comparison technique.

## 1. Interface: a local operation, not merely a local sensor

Let I be a finite set of sites. A full microscopic configuration is
X=(X_i)_(i in I), with visible Y_i in a finite alphabet of size k_i. Hidden
coordinates may be arbitrarily numerous and need not mix. An actual site
kernel T_i changes only X_i and depends on a declared finite neighbourhood
N_i. All kernels and conditional distributions below are on finite or
standard Borel spaces, so the couplings can be realized by disintegration.

The fixed Poisson-call program has generator

    L=sum_i r_i(T_i-I).                               (1)

Its physical implementation must actually supply these local event
opportunities, or the parameter in (1) is only a randomized endpoint
program's operational time. Finite word durations, overlapping calls,
boundary control and controller latency are not erased by writing (1).

A warranted probability mu supplies the acquisition geometry and initial
full marginal. At first assume **each actual T_i preserves mu**. The
fixed, state-independent schedule in (1) then preserves mu. There is no
assumption that mu is a product, that hidden coordinates equilibrate, or
that the visible law is in a uniqueness regime.

Define the actual conditional output row and its local visible projection:

    p_i(b|x)=T_i 1_{Y_i=b}(x),
    q_i(b|a)=E_mu[p_i(b|X) | Y_(N_i)=a].              (2)

The q_i are positive stochastic rows. Let the reference process replace
Y_i with q_i(.|Y_(N_i)) at the same site-clock rates. It starts with the
same visible configuration as the actual process. This reference is
genuine. It need not preserve the full visible marginal mu_Y: projection
onto a neighbourhood need not retain the conditional law given all other
visible sites. Exact closure would remove that distinction.

## 2. What the original acquisition interface actually measures

Put phi_a=1_{Y_(N_i)=a}, G_aa=mu(phi_a),
K_ab=mu[phi_a T_i 1_{Y_i=b}], and

    D_bc=<T_i 1_{Y_i=b},T_i 1_{Y_i=c}>_mu.

Remove zero-mass contexts or give their use a separate deployment
contract. The acquired output-row defect is

    epsilon_i^2
      =sum_b {D_bb-sum_a K_ab^2/G_aa}
      =E_mu sum_b [p_i(b|X)-q_i(b|Y_(N_i))]^2.        (3)

If T_i is reversible for mu, D_bc=mu[1_b T_i^2 1_c]. This is an actual
two-call return experiment with the neighbourhood recorded initially.
For known weighted reversibility, use the actual weighted-adjoint word
from the preserved acquisition theorem. Mere invariance supplies no
adjoint experiment. An unmeasured intervention is not inferred from
equilibrium weights.

With d_i(x)=TV(p_i(.|x),q_i(.|Y_(N_i)(x))),

    E_mu d_i(X) <= (sqrt(k_i)/2) epsilon_i =: e_i.    (4)

This uses the l1/l2 inequality on the output row, followed by
Cauchy-Schwarz over mu. It is an average bound, not a pointwise one.
Finite samples must upper-bound the true expression (3), including
conditioning, sensing, clocks and actual operation errors. A small
plug-in defect is not that certificate.

## 3. Local coupling theorem

Let C_ij be a valid influence coefficient for the reference row:

    TV(q_i(.|y),q_i(.|z)) <= C_ij

whenever y,z differ only at site j. Thus C_ij=0 outside N_i. Let
D=diag(r_i), M=D(C-I), and e=(e_i).

There is a coupling of actual and reference processes such that, for
d_i(t)=P(Y_i(t) differs from Ybar_i(t)),

    d(t) <= integral_0^t exp[M(t-s)] D e ds.           (5)

All inequalities between vectors are coordinatewise. Consequently, for
any fixed finite observation region A,

    TV(Law(Y_A(t)),Law(Ybar_A(t))) <= sum_(i in A) d_i(t). (6)

Cap probability bounds at one.

Proof. Use identical site clocks. At an i event, couple the actual visible
output row to the reference output row maximally, then sample the actual
hidden output conditional on its visible output. The triangle inequality
and one-site telescoping give the conditional disagreement probability
at the refreshed site at most

    d_i(X)+sum_j C_ij 1_{Y_j != Ybar_j}.

The old disagreement at i is removed from the derivative at rate r_i.
The actual marginal remains mu, so (4) bounds the expected forcing at
every time, irrespective of correlations created by the coupling. Hence

    d'_i <= r_i[-d_i+sum_j C_ij d_j+e_i].             (7)

The matrix M is Metzler. Variation of constants and d(0)=0 give (5).
The union bound in the same coupling proves (6).

For equal rates r_i=r and max_i sum_j C_ij<=c, if e_i<=e then

    max_i d_i(t) <=
      e [1-exp(-r(1-c)t)]/(1-c),       c<1;
      r e t,                          c=1;
      e [exp(r(c-1)t)-1]/(c-1),        c>1.           (8)

This uses a **row-sum** influence condition for a fixed-site error. The
earlier normalized-Hamming receiver used a column-sum condition for a
different metric; those conditions should not be interchanged.

Formula (8) has no total-volume factor. It supplies finite-time control
even outside contraction. A useful uniform-in-time bound follows in the
contractive case or, more generally, from an integrable influence kernel.
Locality by itself does not make that time integral finite.

## 4. Old records: a positive joint statement and its exact limit

Let Z be any old record, possibly correlated with the initial microscopic
state. Assume only that the actual **unconditional** initial full marginal
is mu and the fixed actual schedule does not change with Z. Start the
reference with the same pair (Z,Y_0). The coupling above keeps Z equal,
so (6) also bounds

    TV(Law(Z,Y_A(t)),Law(Z,Ybar_A(t))).                (9)

There is no cardinality factor for Z. The conclusion is joint, not
conditional accuracy for every rare realized Z. The proof succeeds
because the forcing in (4) is fixed and is averaged against the actual
stationary marginal, while the coupled visible initial configurations
agree exactly.

For finitely many fixed regions/times (A_l,t_l), the joint record error
is at most sum_l sum_(i in A_l) d_i(t_l), by the same coupling. Any
postprocessing of that retained record obeys the same bound.

An arbitrary Z-selected **site**, schedule, intervention, or stopping
time is not automatically included. The rare-device construction in
COUNTEREXAMPLES_AND_INTERFACE_BOUNDARIES.md gives a visible-record-selected
one-call error tending to 1/2 while every fixed-site defect tends to zero.
Pointwise or conditional calibration can support a stronger interface;
unconditional equilibrium L2 calibration cannot simply be renamed that.

## 5. Statistical fitting and physical feedback are different selections

For a fitted reference q_hat_i(Dcal), suppose a simultaneous confidence
event G of probability at least 1-beta guarantees

    sup_a TV(q_hat_i(.|a),q_i(.|a)) <= delta_i.

If the actual deployment operations and schedule are fixed, replace
e_i by e_i+delta_i on G and add beta to the final joint TV bound. Even
when Dcal and the deployment state are correlated, the fixed population
residual d_i(X) is still averaged against the unconditional mu. One can
formalize this by following P(G and disagreement_i); its forcing is at
most E[d_i(X)]+delta_i. The fitted reference's influence matrix must also
be bounded on the same event, or by a uniform deterministic envelope.

This observation does not permit the *actual* intervention schedule to
be selected arbitrarily from correlated calibration data. Kernels which
individually preserve mu can fail to preserve it when selected using
information correlated with the current state. Independent deployment
conditional on the physical parameters, an actual conditional stationary
preparation, or a direct density bound is then needed.

A useful nontrivial stationary feedback class is possible. If T_i^j
changes only X_i, is reversible for mu, and selection j depends only on
the currently visible coordinates outside i which the call leaves fixed,
then the selected kernel remains reversible for mu. The selector is
constant across each microscopic transition edge. This is a local
configuration-dependent kinetic control, not unrestricted history feedback.
Its residual can be bounded by the sum of the menu residual energies:
E_mu d_selected^2 <= sum_j E_mu d_j^2. The actual neighbourhood and
influence coefficients include the selector's dependence.

## 6. A finite-horizon extension when the calls change equilibrium

The elementary density version of (5) is useful. If the actual marginal
rho_s has a proved density ceiling

    d rho_s/d mu <= B(s),

then replace e_i in (5) by sqrt(B(s)) e_i. This is Cauchy-Schwarz under
mu applied to the same fixed residual. A density ceiling is sufficient,
not necessary; local conditional bounds on the residual itself may be
better.

Suppose a site call is reversible for mu*w_i with known positive visible
weights, and R_i=max w_i/min w_i. Then

    T_i^*1=w_i T_i(1/w_i)<=R_i.

For a prescribed Poisson-call program on a set J of active sites,
starting from mu, positivity and the independent clock counts give

    B(s) <= exp[s sum_(i in J) r_i(R_i-1)].           (10)

One way to see this is to bound the L-infinity norm of each adjoint call
by R_i and average the resulting product over its Poisson count.
Time-dependent externally prescribed calls may use uniform R_i bounds.
The formula is not asserted for a globally communicating arbitrary
feedback controller using unbounded additional memory.

For a finite region of driven sites, (10) is already independent of total
system size. The remaining obstruction for drive everywhere is its
volume factor. Physical finite propagation localizes that factor.

## 7. Localizing the density cost to a causal neighbourhood

Assume both actual and reference calls have dependency neighbourhoods of
size at most D0, per-site Poisson opportunity rate at most lambda, and
the corresponding finite-range dependency graph is warranted at the
**full microscopic and controller interface**. Fix an observation set A
and horizon T. Let J_L contain all sites within L-1 graph steps of A.
Compare each full process to the process which freezes all call sites
outside J_L, from the identical initial full configuration.

A disagreement at A requires an oriented, time-ordered graphical path
from A reaching outside J_L. Counting paths and ordered Poisson events
gives the conservative bound

    xi_L(T)=|A| sum_(n>=L) (D0 lambda T)^n/n!.         (11)

This is an upper bound for either full-versus-truncated coupling error
at time T; cap it at one. Repeated visits to a site are allowed in the
count. Their ordered factorial moment is still bounded by
lambda^n T^n/n!. Initial spatial correlations cause no extra term
because the initial microscopic configuration is shared exactly.

Apply (5) to the two truncated processes. Their actual law obeys (10)
with J=J_L, even though the full driven network need not. Thus a complete
endpoint bound is

    TV(Law(Y_A(T)),Law(Ybar_A(T)))
      <= 2 xi_L(T)
         + sum_(i in A) integral_0^T
             [exp(M_J(T-s)) D_J e_J]_i
             exp[(s/2) sum_(j in J_L) r_j(R_j-1)] ds. (12)

Outside visible coordinates remain the shared frozen initial values in
the truncated coupling. M_J uses only active-site disagreements; this
can only improve the uniform influence envelope. All old records kept
equal and unused for the operation schedule can be included as in (9).

On a bounded-degree lattice, the size of J_L depends on A,L and geometry,
not on the total number of sites. For fixed A,T, first choose L to make
(11) small, then acquire the finite set of local residuals accurately
enough for the second term. This is a genuine finite-horizon,
volume-independent implication from equilibrium L2 errors without a
contractivity assumption. The density factor can be enormous in the
causal spacetime volume; no useful practical precision or all-time
certificate is claimed.

The construction also shows why merely removing an exponential in total
volume is not automatically a foundational advance. Graphical locality
and local perturbation comparison are established. The scientifically
useful supplier must make the required local residual precision and
physical locality attainable for an important receiver.

## 8. Costs and unresolved premises

Calibration in (3) records only a finite neighbourhood and actual call
endpoints. It still uses the warranted stationary preparations and
adjoint access of the original acquisition interface. A finite local
readout does not make preparation of a very large critical sample free.
Neither the finite sample size nor a common statistical law proves
uniformity over unmeasured heterogeneous devices or changing boundaries.

For stationary programs, the substantive new connection is that the
acquired L2 defect is averaged against exactly the law which actually
persists during deployment. For driven programs, the gap is paid by the
proved density/causal-neighbourhood contract. For uniform all-time
critical response, the stronger relative kinetic receiver in
GAP_FREE_RELATIVE_KINETIC_RECEIVER.md is a possible alternative supplier
objective. Its perturbation theorem is explicitly a primary predecessor.

Primary comparisons: Rebeschini and van Handel, *Comparison Theorems for
Gibbs Measures*, Proposition 3.2 and their one-sided comparison theorem,
<https://web.math.princeton.edu/~rvan/dobrushin130819.pdf>; Lucia, Cubitt,
Michalakis and Pérez-García, *Rapid mixing and stability of quantum
dissipative systems*, <https://arxiv.org/html/1409.7809v3>. The first
already uses average local coupling errors and influence matrices. The
second gives local, volume-independent stability under rapid mixing and
also covers classical Markov dynamics.
