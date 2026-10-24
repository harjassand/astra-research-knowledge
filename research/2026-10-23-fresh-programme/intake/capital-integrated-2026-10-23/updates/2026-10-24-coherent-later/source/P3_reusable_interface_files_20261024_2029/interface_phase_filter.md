# Compact reaction phases with correlated entrance information

New mathematical construction in this Pro3 continuation. This file develops a
specific extension of the finite-gate event operation. It does not claim
historical novelty for filtering, renewal equations or conditional independence.
The accompanying code and numerical outputs are newly written work.

## 1. Scientific operation

The requested output is the next marked reaction law, the entrance information
needed by later reaction phases, and the likelihood of an observed reaction
record. The construction does not require a finite closed population state or
an expanded generator on every combined molecular configuration.

There are finite local modules `E_i`. A finite public chemical phase `q` selects
local generators `Q_{q,i}` and an active module set `A_q`. All unmarked rules in
that phase read and change just one admitted local module, so the unmarked
generator is their Kronecker sum.

Gate `j` of phase `q` has finite nonnegative rate `kappa_{q,j}` and specifies a
complete assignment `a_{q,j}` on `A_q`. The gate is a cylinder in the full
configuration space: it does not inspect the other modules. Multiple competing
gates are permitted, but every gate in the phase must specify all of `A_q`.
There are no additional unrecorded cross-module reactions.

The phase changes only at a recorded marked event, by a known rule `q'=g(q,j)`.
The active sets can change and overlap arbitrarily along these changes. The
post-event reset is a tensor product of local stochastic kernels, with its
choice determined by the known phase and mark. Deterministic local updates and
identity updates are special cases. A reset may affect inactive modules too,
provided the reset kernel still factors across the admitted modules.

At the beginning of an operation the hidden entrance law is supplied as a
positive mixture of products:

    mu = sum_{r=1}^R w_r tensor_i mu_{r,i},
    w_r >= 0, sum_r w_r = 1.

This is a substantive initialization contract. A short list of marginal
distributions alone does not specify the correlations. A generic correlated
law can need exponentially many product components. The mixture may come from
an explicit finite preparation choice, from a previous operation below, or
from an approximation with a separately supplied total-variation error.

## 2. Exact closure at observed event times

Write `P_{q,i}(t)=exp(t Q_{q,i})`. For the active coordinates define

    K_{ij}(t) = kappa_j product_{ell in A_q}
                 P_{q,ell}(t)[a_{i,ell}, a_{j,ell}],

    b_{r,j}(t) = kappa_j product_{ell in A_q}
                   (mu_{r,ell} P_{q,ell}(t))[a_{j,ell}].

The component first-event densities solve the shared Volterra operator

    f_r + f_r * K = b_r.

Only the active coordinates enter these densities. All initial components use
the same kernel K and different right-hand sides. Thus a numerical factorization
or other reusable solver state for the causal operator can serve every r.

Suppose the observed next event has mark j and elapsed time t, at which the
mixture event density

    z_j(t) = sum_r w_r f_{r,j}(t)

is positive. Before the reset, define local factors

    nu_{r,i}^{j,t} = delta_{a_{j,i}}            if i in A_q,
    nu_{r,i}^{j,t} = mu_{r,i} P_{q,i}(t)       if i outside A_q.

Apply the corresponding local reset kernel `R_{q,j,i}` to each factor. Then the
post-event conditional law is exactly

    mu_new = sum_r w'_r tensor_i [nu_{r,i}^{j,t} R_{q,j,i}],
    w'_r = w_r f_{r,j}(t) / z_j(t).

### Theorem

Under the stated source, initialization and reset contracts, the positive
product-mixture width at successive exactly observed event times never exceeds
its initial value R. The tuple consisting of the public phase, mixture weights
and local factors is sufficient for every later marked-event prediction. Its
stored size is O(R sum_i |E_i|), in addition to the local generators and finite
gate descriptions. No global configuration enumeration is needed by the
representation update.

This is a nonlinear conditional-state representation. It is not a claim of a
small homogeneous finite-state Markov realization for the observed process.

### Proof

Introduce the mixture label r as a latent variable. Conditional on r at the
start of the phase, the module paths are independent. Both the absence of an
earlier marked event and the event (t,j) depend only on the paths in A_q. Hence
the inactive module paths retain their free product law, conditional on r and
the exact event time t. At the event, all active coordinates are pinned to
`a_{q,j}`. The no-event conditioning may have produced complicated correlations
inside A_q before the event; pinning its entire endpoint removes the need to
retain those internal correlations for the future Markov evolution.

Bayes' formula updates the mixture weights by f_{r,j}(t). A product of local
reset kernels maps each product component to another product component.
Therefore the displayed post-event mixture is exact and has at most R terms.
The strong Markov property, applied at each event, proves the assertion by
induction, even when the next active set overlaps the previous one arbitrarily.

### What the theorem permits

* Different phases may inspect different small or very large subsets.
* The unspecified variables can matter to a later phase; they are not discarded.
* Correlations across those unspecified variables persist through the mixture
  weights and are updated by event timing and identity.
* Local generators may change when the public phase changes.
* A finite static latent model index may be combined with r if every candidate
  model has the certified factorization. In that case each candidate may have
  its own K. This gives likelihoods within a supplied model family, not general
  identification of unknown biology.

### What it does not permit without further work

* A gate that omits a variable inspected by another active gate in the same
  phase can leave correlated, unpinned active information.
* Changing the active support after a timeout with no event can retain those
  correlations. The exact fixed-width theorem requires support changes at
  recorded marked events.
* Integrating out an unknown event time generally introduces a continuous
  shared latent variable. Fixed width R is an exact-time result; the controlled
  finite-resolution construction below handles that integration.
* A reset that draws a shared latent choice among L product kernels can increase
  the width to RL. That cost must be retained or compressed with an error bound.

## 3. Joint event-and-entrance error, without a Bayes denominator

For component r let an approximate event subdensity be nonnegative, with total
mass at most one up to a deadline T. Include the no-event atom. Let its compact
Volterra residual be

    rho_r = f_tilde_r + f_tilde_r * K - b_r.

The preceding event-law theorem supplies

    TV(event law_r, approximate event law_r)
      <= epsilon_r := integral_0^T sum_j |rho_{r,j}(t)| dt.

Attach to each actual event (t,j) the product entrance channel given in Section
2, including the known reset. Map a censored no-event outcome to a terminal
symbol; no post-timeout hidden law is claimed. Attaching a common Markov kernel
cannot increase total variation. Mixing the labeled component laws therefore
gives

    TV(joint event/entrance law, approximate joint law)
      <= sum_r w_r epsilon_r.

This includes correlated hidden entrance information without requiring an
expanded hidden-state vector. It does not divide by a rare observation
probability. It can be used in a coupling proof for a sequence of operations:
uniform per-operation errors add up to the number of operations, or to the
corresponding expected count when a valid rate domination is available.

This unconditional joint guarantee must not be confused with a guarantee for a
posterior conditioned on one rare observation.

## 4. Conditional posterior error

### A finite event-time bin

Suppose true and approximate joint laws P,Q obey `TV(P,Q)<=epsilon`, and the
observed bin/mark event B has probabilities p=P(B)>0 and q=Q(B)>0. Then

    TV(P(.|B), Q(.|B)) <= epsilon / max(p,q) <= epsilon/p.

To see this, let m be their common overlap mass inside B. The overlap outside
B is at most `min(1-p,1-q)=1-max(p,q)`. The global TV bound implies
`m >= max(p,q)-epsilon`. The normalized conditional overlap is at least
`m/max(p,q)`, which proves the result. A certified positive lower bound on p
therefore gives a usable conditional certificate. If epsilon is not smaller
than the observation probability, the bound can be uninformative.

### An exactly observed time

An integrated time-law TV bound alone says nothing about a posterior at an exact
time of probability zero. The event model can supply a pointwise certificate
instead. If F_{ij}(u) is the true first-event density from gate i to mark j,
then `0<=F_{ij}(u)<=kappa_j`. The residual identity is

    f_tilde_r - f_r = rho_r - rho_r * F.

Consequently

    |f_tilde_{r,j}(t)-f_{r,j}(t)|
      <= |rho_{r,j}(t)|
         + kappa_j integral_0^t sum_i |rho_{r,i}(s)| ds.

If pointwise residual and integral enclosures give bounds delta_{r,j}(t), the
unnormalized mixture-weight L1 error is at most

    E_j(t)=sum_r w_r delta_{r,j}(t).

Provided the true event density has a certified lower bound z_min>0, normalized
weight TV, and hence posterior-state TV after the common entrance channels, is
at most `min(1,E_j(t)/z_min)`. A positive approximate density alone is not a
sufficient lower-bound warrant.

## 5. Finite-resolution entrance information with controlled width

Assume inactive modules are binary, time-homogeneous and independent within
each mixture component. Let their active probabilities be

    p_{r,i}(t)=pi_i+(p_{r,i}(0)-pi_i) exp(-lambda_i t).

Frozen modules have zero variation and can be omitted from the following sum.
For an observed waiting-time bin B=[a,b] and known mark j, define

    V_r(t)=sum_{i outside A_q} |p_{r,i}(0)-pi_i| exp(-lambda_i t).

For s,t in a cell [u,v], product coupling gives

    TV(product_i mu_{r,i}P_i(s), product_i mu_{r,i}P_i(t))
      <= sum_i |p_{r,i}(s)-p_{r,i}(t)|
      <= V_r(u)-V_r(v).

The active coordinates are pinned by j, and the local reset is a contraction,
so the same bound applies to the complete entrance channel.

Choose, separately for each r, a partition of B on which every drop in V_r is
at most eta. Attach to a cell c any representative time t_{r,c}, and assign the
positive weight

    W_{r,c} = w_r integral_c f_{r,j}(t) dt.

After normalization over r,c, the resulting mixture of product entrance laws
approximates the exact posterior given (T in B,J=j) with TV at most eta, when
the weights are exact.

The required number of product components is bounded by

    sum_r max(1, ceil((V_r(a)-V_r(b))/eta))
      <= R (1 + n_inactive/eta).

This is independent of the silent rate magnitudes and the waiting-time horizon.
It pays explicitly for desired accuracy and the total change of the retained
local distributions. Very fast silent modes simply place partition boundaries
near the start; they do not increase total variation travel beyond this bound.

If the component/cell probabilities are obtained from a certified numerical
event law with joint TV error epsilon, and the observed bin has true probability
at least p_min>0, the posterior error is bounded by

    eta + epsilon/p_min,

capped at one. The cell-index mapping is deterministic given r and t, so
coarsening the certified event law into these cell weights does not amplify
its unconditional error.

This result does not claim exact fixed width after binning. It provides a
controlled positive-mixture width increase. It approximates the hidden state
at the reaction, averaged over the uncertain reaction time, conditional on the
observed timing bin and mark. Applying the same later transition or query
kernel to these entrance laws contracts their TV difference. Such a kernel
must depend only on the retained hidden state, public chemical phase and time
elapsed since the event. This covers autonomous later phases and protocols
restarted relative to the reaction.

If the future protocol depends on the uncertain absolute event time, that
clock is additional correlated entrance information. The hidden-state
certificate alone does not preserve it. One must retain the joint time/state
law, or obtain a separate temporal regularity certificate for the later
operation. In particular, replacing a continuous event time by representative
atoms can have total-variation distance one for the joint clock law, even
when the hidden-state approximation is excellent. Representative times stored
with the finite mixture identify where its state factors were evaluated;
they are not a certified approximation to the full continuous clock law.

For general finite modules one can replace V by a certified bound on the total
variation path length of `mu_{r,i}P_i(t)`. A crude local bound uses maximal exit
rates. The binary monotonic formula is stronger and is the implemented class.
Section 9 gives a finite obtaining algorithm for a general local variation
clock, without claiming that general algorithm has been implemented.

## 6. A representation boundary

A compact guard need not preserve compact positive product-mixture entrance
information. Take n frozen fair binary sites and one reaction that fires only
at even parity, with identity reset. The guard can be described in O(n) syntax.
Conditional on any observed event time, the hidden state is uniform on the
2^(n-1) even-parity configurations.

Every nonnegative product component whose support is confined to even parity
must be a point mass: if any coordinate had both values in its support, fixing
the others would produce both parities. Therefore the exact posterior needs
at least 2^(n-1) positive product components.

This is a lower bound for the declared product-mixture representation, not for
all compact inference methods. Parity itself admits other concise symbolic
representations. Its purpose is to show why the entrance contract must be
obtained rather than inferred from the length of the rule syntax.

## 7. New executable check and its scope

`interface_phase_filter.py` implements compact K and b evaluation and the
product-mixture entrance update. The numerical check alternates between active
supports (0,1) and (1,2,3), each with two competing gates, starting from a
two-component correlated product mixture. Deterministic local resets are
applied after the marked events.

The check obtains event densities from small expanded active-block matrices
and compares the resulting entrance update with an independent full 16-state
global killed-generator/reset calculation. This is a check of the new entrance
theorem and implementation, not a claim to have implemented a new general
certified Volterra discretization in this file.

Four successive alternating observations retained mixture width two. The
largest posterior L1 discrepancy against the expanded reference was below
4.6e-16; the joint log-density discrepancy was below 1.8e-15.

After the first observation, the two inactive variables had covariance
0.04748590694496546. Replacing the true correlated entrance mixture by the
product of its marginals changed the next selected event density from
0.3671953090656504 to 0.34621425581430526, a relative error of approximately
-5.7139 percent. The error is therefore not only a formal possibility.

These numbers are newly executed floating-point consistency checks. They are
not interval numerical certificates or experimental measurements. The
mathematical error-transfer results above have separate stated premises.

## 8. Consequential use and limits

The construction is suitable for a specified sequential catalytic or molecular
control program in which successive chemical phases inspect different internal
site sets, and the marked event identifies a complete configuration on the
currently inspected set. It can retain a compact correlated preparation
mixture, compute event-record likelihoods, update hidden entrance information
and predict later reaction events.

An unconditional distribution over every possible long event record may still
require integration over the continuous conditional state. The theorem does
not silently make all such workloads inexpensive. Its direct operations are
conditional next-event prediction, marked-record likelihood, event-level
simulation, and reusable entrance approximations for later queries.

Known renewal and network-free methods are actual comparators. The additional
claim to assess is the obtainable phase-and-entrance representation with its
explicit correlation, reset, timing and numerical error contracts. A
conventional programme can adopt exactly this operation.

## 9. Obtainable variation clocks for general finite local CTMCs

The finite-resolution entrance construction is not limited to binary modules.
It requires a monotone function W(t) such that, for any s<=t,

    TV(mu exp(Qs), mu exp(Qt)) <= W(s)-W(t).

The product entrance variation is then bounded by the sum of the local W drops.
This section supplies finite rational obtaining procedures for arbitrary finite
local CTMCs. The irreducible case has a simpler contraction certificate; the
general case uses its rational stationary projection. A reversible source
also admits a sharper analytical bound.

### 9.1 Uniformization and a local contraction certificate

Let Q be a finite rational generator with d>=2 states. Choose a rational
Lambda strictly larger than its maximal exit rate, and put

    P = I + Q/Lambda.

P is stochastic and has positive diagonal entries. For an irreducible Q, every
state can reach every other along a path of at most d-1 edges. Self-loops pad
these paths, so P^(d-1) is entrywise positive. Thus one can obtain an integer
m<=d-1 with the Dobrushin contraction coefficient

    delta = 1 - min_{i,j} sum_k min((P^m)_{ik}, (P^m)_{jk}) < 1.

All these quantities can be computed exactly from the local rational matrix.
Smaller m can be tried when useful; no global product matrix enters this step.
For a frozen local law with mu Q=0, the variation budget is zero and no
contraction certificate is needed.

Let v=mu Q and c=||v||_TV=(1/2)sum_i |v_i|. If mu is rational, c is obtained
exactly by rational arithmetic. Otherwise a certified upper bound on c can
replace c in every clock below; the matrix certificate itself remains rational.
Since v has total mass zero,

    ||v P^k||_TV <= delta^floor(k/m) c.

The uniformization series and Q's commutation with its semigroup give

    ||d(mu exp(Qt))/dt||_TV
       = ||v exp(Qt)||_TV
       <= c E[delta^floor(N_(Lambda t)/m)],

where N_z is Poisson with mean z. Therefore the total variation path length is
bounded by

    integral_0^infinity ||d(mu exp(Qt))/dt||_TV dt
       <= c m / (Lambda (1-delta)).

Indeed, integrating each Poisson basis function gives 1/Lambda, and
`sum_{k>=0} delta^floor(k/m)=m/(1-delta)`.

This bound is invariant under uniform scaling Q -> a Q when Lambda is scaled
accordingly. Slow contraction or a badly conditioned local chain can still
make it large; rate-scale invariance is not a uniform bound over all kinetics.

### 9.2 A finite representation of the monotone clock

Set

    g(t)=E[delta^floor(N_(Lambda t)/m)],
    W(t)=c integral_t^infinity g(u) du.

Then the required cell inequality follows by integrating the derivative bound.
W itself has a finite local phase-type representation. Let C_delta be the m by
m substochastic cycle matrix: it advances each phase to the next with weight
one, except that the wrap from phase m-1 to zero has weight delta. Put

    T = Lambda (C_delta-I).

Then

    g(t)=e_0^T exp(Tt) 1,
    W(t)=c e_0^T exp(Tt) (-T)^(-1) 1.

For m=1, T=-Lambda(1-delta). For larger m this is an Erlang clock that survives
each completed cycle with probability delta. Its initial value is exactly

    W(0)=c m / (Lambda (1-delta)).

The clock can be evaluated and enclosed with local positive uniformization
and rational linear algebra. Its construction is paid once per local source
generator; changing the entrance law changes only c in this conservative
version. Exact local matrix and numerical evaluation costs remain explicit.

For R entrance components, partitioning each observed timing bin using drops
of `sum_i W_{r,i}` at most eta gives at most

    R + (1/eta) sum_{r,i} W_{r,i}(0)

product terms, with the same conditional entrance error eta plus certified
event-weight error divided by the observed-bin probability lower bound.

### 9.3 Reducible finite chains: contraction after removing the stationary part

Global Dobrushin contraction can fail when Q has several closed classes. The
variation clock still exists and can be obtained without a spectral calculation.
Use a rational Lambda larger than the maximal exit rate, as above. Compute the
stationary projection H of P by the following exact local steps.

1. Find the strongly connected components of Q's positive off-diagonal graph,
   identify the closed classes C_1,...,C_k, and let T_0 contain the transient
   states.
2. In each closed class obtain its normalized stationary row pi_j by solving
   `pi_j Q_(C_j,C_j)=0`, `pi_j 1=1` over the rationals.
3. For each class solve the transient absorption-probability equations
   `Q_(T_0,T_0) h_j = -Q_(T_0,C_j) 1`. The transient block is invertible.
   No solve is needed when there are no transient states.
4. Set H's row on a state in C_j to pi_j, extended by zero outside C_j. For a
   transient state x, set its row to `sum_j h_j(x) pi_j` with the same extensions.

H is rational and stochastic, with `H^2=H`, `PH=HP=H`, and `QH=HQ=0`.
Because the chosen P has positive diagonal, each closed irreducible block is
aperiodic; its transient block loses all mass. Consequently `P^n -> H`.

Compute successive rational powers, for example at m=1,2,4,8,..., until

    theta = max_i sum_j |(P^m-H)_(i,j)| < 1.

This search terminates. The stored rational matrix H, integer m and rational
theta are a checkable contraction certificate. Its obtaining cost depends on
the local chain and need not be small for a slowly mixing local source.

For `v=mu Q`, `vH=0`. If a signed row u satisfies uH=0, then

    uP^m = u(P^m-H),
    ||uP^m||_TV <= theta ||u||_TV.

The second inequality is the row-sum operator-norm bound, with the same factor
1/2 in the TV norm on both sides. The subspace uH=0 is P-invariant, and the
remaining powers of a stochastic P do not increase TV. Thus

    ||vP^n||_TV <= theta^floor(n/m) ||v||_TV.

Every argument in Sections 9.1 and 9.2 now applies with theta in place of delta.
In particular, the finite m-phase substochastic clock is obtained using wrap
weight theta, and

    W(0) = c m / (Lambda (1-theta)).

This proves an obtainable finite local variation budget for every finite
rational generator, including multiple absorbing classes. It neither assumes
a unique stationary distribution nor contracts differences between arbitrary
initial laws: it contracts the derivative direction after its stationary part
has been removed. Frozen laws have c=0. Uniform scaling of all local rates
preserves P, H, m and theta and scales c and Lambda equally, leaving the budget
unchanged. Rational powers and linear solves suffice; no eigendecomposition is
required.

### 9.4 A stronger reversible variation budget

Suppose Q is reversible with positive stationary law pi. In L^2(pi), put

    h = mu/pi - 1,

and let Pi_lambda be the orthogonal projection onto the eigenspace of -Q with
positive eigenvalue lambda. Define

    W_spec(t) = (1/2) sum_{lambda>0}
                   exp(-lambda t) ||Pi_lambda h||_{L1(pi)}.

For s<=t, the coefficients `exp(-lambda s)-exp(-lambda t)` are nonnegative.
The triangle inequality therefore proves

    TV(mu exp(Qs), mu exp(Qt)) <= W_spec(s)-W_spec(t).

If there are M distinct positive eigenvalues, orthogonality and Cauchy-Schwarz
give

    W_spec(0)
       <= (1/2) sqrt(M) ||h||_{L2(pi)}
       <= (1/2) sqrt((d-1) chi_squared(mu||pi)).

No eigenvalue magnitude appears in this last bound. The binary monotonic clock
is the one-eigenspace special case and gives the sharper exact initial budget
`TV(mu,pi)` rather than the L2 upper bound.

Certified local spectral projectors supply the explicit clock W_spec; the
eigendecomposition and its numerical error cannot be treated as free. When
that route is inconvenient, the rational contraction clock above applies
without reversibility. For a reversible source, a simpler alternative uses a
certified gap gamma and the bound

    W_gap(t) = ||Qh||_{L2(pi)} exp(-gamma t)/(2 gamma).

That follows from L2 contraction of the derivative and is also invariant under
uniform rate scaling. A bare total-length bound cannot automatically be used
as `C exp(-gamma t)`: its cell drops need a derivative or spectral justification.

### 9.5 Three-state rational examples and implementation status

Take the irreversible directed cycle

    Q = [[-1, 1, 0],
         [ 0,-1, 1],
         [ 1, 0,-1]],
    mu = [1,0,0].

Choose Lambda=2. Then P is one half identity plus one half cyclic shift. Any
two distinct rows overlap in mass 1/2, so m=1 and delta=1/2. The initial
derivative has c=||mu Q||_TV=1. The obtained variation clock is

    W(t)=exp(-t),   W(0)=1.

This is a nonreversible local module; no reversible eigendecomposition is used.
Scaling all three rates by seven gives Lambda=14, the same P and delta, c=7,
and W(t)=exp(-7t), with the unchanged total variation budget one. These values
and the scaling identity were checked with exact Fraction arithmetic.

For a reducible example, take

    Q = [[-2, 1, 1],
         [ 0, 0, 0],
         [ 0, 0, 0]],
    mu = [1,0,0], Lambda=3.

The last two states are separate absorbing classes, so every global Dobrushin
coefficient equals one. Nevertheless,

    H = [[0,1/2,1/2],
         [0,  1,  0],
         [0,  0,  1]],
    max_i sum_j |(P-H)_(i,j)| = 2/3.

Hence m=1, theta=2/3, c=2 yield the valid clock `W(t)=2 exp(-t)` and budget
two. The true local path length is one; the certificate is conservative but
finite. Scaling both outgoing rates equally leaves this certified budget
unchanged. The stated projection, matrix norms and budget were checked by exact
rational arithmetic.

The general finite-local clock construction is a proved obtaining algorithm.
It has not been implemented as a general solver in `interface_phase_filter.py`
or the binary finite-timing-bin implementation. The implemented binary case,
the general theorem and its exact three-state arithmetic examples must remain
distinguishable.
