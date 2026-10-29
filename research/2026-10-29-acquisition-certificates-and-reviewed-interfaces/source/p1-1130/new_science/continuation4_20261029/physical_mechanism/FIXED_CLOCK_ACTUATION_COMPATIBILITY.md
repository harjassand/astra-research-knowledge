# Fixed-clock invariant laws: actuation compatibility and the exact price of visible-preserving activity

29 October 2026. Independent physical-mechanism construction within Astra P1.
This direction was selected before the root disclosed its next mechanism.

## 1. Question and result

The bounded counter changes the law at selected completion epochs. This note asks
a different question: when can a controller maintain the desired microscopic law
at every ordinary operation boundary, and, with a stated semigroup supplier, at
every physical time, while continuously executing a native operation?

For a finite visible move graph G and a uniform visible baseline, the answer is
an exact fractional matching condition. The controller chooses actual native
operations before executing them; it never rejects a realized microscopic state.
The transition probabilities and hidden kinetic memory are not inputs.

Let pi be the desired visible law. Write N(S) for the open graph neighborhood and

    delta_G(pi) = max_{S subset V} [pi(S)-pi(N(S))].                    (1)

The maximum is nonnegative and may equivalently be restricted to independent
sets. A universally valid controller without a visible-preserving action exists
exactly when delta_G(pi)=0, under the menu and robustness scope below. If an
actual baseline-stationary, visible-preserving operation is supplied, the minimum
worst-case stationary expected fraction of its use is exactly delta_G(pi).
This is a universal-menu optimum, not a pointwise optimum for every particular
device. The construction achieves
this fraction for every compatible hidden kernel; a common-rate native witness
proves the lower bound against arbitrary causal policies with retained history,
not merely memoryless mixtures.

This is a graph-theoretic physical-interface consequence, not a claim that
fractional matching, flow balance, data augmentation, or rejection minimization
are new. Strong predecessors are discussed in PRIMARY_COMPARISON_AND_FAILURES.md.
In particular, known probability-flow methods already optimize holding in a
fully specified software transition graph. The present construction identifies
which of those flows survive unknown complete-state native operations and which
additional real activity supplies the missing mass. Historical priority is not
established.

## 2. Actual interface

The full physical state x includes every bath/apparatus variable affecting the
future. Its noninvasive finite label is y=Y(x) in V. The warranted baseline mu
has uniform label marginal, mu(Y=y)=1/|V|. Conditional hidden laws can differ
across labels and can contain conserved sectors. Put

    nu(dx) = |V| pi(Y(x)) mu(dx),   pi(y)>0.                         (2)

Each native operation P_i preserves mu. Its allowed label transitions form a
matching: there is a fixed-point-free involution sigma_i on the labels where the
operation is available, and P_i preserves the unordered pair
{Y(x),sigma_i(Y(x))}. Availability is an actual part of the menu. Choosing an
unavailable operation as a free identity is forbidden. Coordinate operations
on a binary register are the main example: sigma_i flips coordinate i, while
all other visible coordinates remain fixed.

Hidden evolution within each pair is unrestricted subject to the full-state
stationarity premise. It can change continuously, retain arbitrary memory, or
be nonreversible. No finite predictive model is assumed. The visible move graph
has edges {y,sigma_i(y)}. Distinct controls for the same edge may be allocated
separately; one representative per edge suffices for the construction.

At each ordinary boundary the controller must select and execute exactly one
available operation. Native calls have the same declared duration if boundary
fractions are to be interpreted as physical-time fractions. Sensing, selection
and switching must have a compatible actual implementation; an unmodeled gap
cannot be treated as a hold. The continuous-time supplier in Section 8 avoids
instantaneous selection in the mathematical model, at the price of an explicit
state-dependent selector-rate interface.

An optional additional operation R preserves mu and Y. R may move hidden
coordinates extensively; it need not fix x or reset hidden memory. Its actual
availability, duration and cost are additional resources. Label preservation
without stationarity does not suffice.

The universal robustness class includes the visible-only common-rate witness:
each selected edge attempts its involution with one common probability p in
(0,1), otherwise it leaves y fixed. There is no additional state-dependent
native rate control or variable call duration in this witness. A physical
menu known to be outside this class can have a different capability set.

## 3. Constructive scheduling from a fractional matching

Choose symmetric nonnegative edge masses f_e satisfying

    d_f(y) := sum_{e incident to y} f_e <= pi(y).                    (3)

For edge e={y,z} supplied by operation i, select that operation at y with

    q_i(y) = f_e/pi(y).                                             (4)

If an operation i supplies multiple disjoint pairs, apply this formula on each
pair. Define q_0(y)=1-d_f(y)/pi(y), and select the actual R operation with q_0.
If d_f=pi, no R is used. Every selector probability depends only on the desired
visible weights and the known move graph.

### Full microscopic invariance

For each i the density of the selected input submeasure is

    d(nu q_i)/dmu = |V| f_{ {Y,sigma_i(Y)} }.                       (5)

It is constant on each native invariant pair. Any invariant measure multiplied
by a bounded function of a preserved quantity remains invariant. Hence
(nu q_i)P_i=nu q_i. Likewise nu q_0 has density depending only on Y, so
(nu q_0)R=nu q_0. Summing gives

    nu K=nu,    K=sum_i q_i P_i+q_0 R.                             (6)

If the native operations are mu-reversible, the same pairwise multiplication
proves nu-reversibility. No adjoint actuator, microscopic rollback, copied
proposal, output overwrite, or stationary restart occurs.

This is a direct mixture of actual kernels on the complete state. The visible
process need not itself be Markov. Arbitrary old records may be retained, but
invariance does not say that an arbitrary record-conditioned initial law is nu.

## 4. Exact optimum by a finite flow construction

Build the bipartite double cover of G. A source connects to each left vertex
y_L with capacity pi(y); each right vertex z_R connects to the sink with
capacity pi(z). Add y_L -> z_R whenever {y,z} is an edge, with capacity at least
1. Let a maximum flow be g(y,z), of total value F. Define

    f_{ {y,z} } = [g(y,z)+g(z,y)]/2.                              (7)

Both the row and column capacities of g are bounded by pi, so (3) holds and
2 sum_e f_e=F. Conversely every feasible f gives a double-cover flow of value
2 sum_e f_e. Standard max-flow/min-cut therefore gives

    max_f 2 sum_e f_e = 1-delta_G(pi).                             (8)

For completeness, a finite cut which retains left vertices S must retain all
their right neighbors N(S). Its capacity is
1-pi(S)+pi(N(S)); optimizing over S proves (8).

The extra-operation fraction at target stationarity is

    sum_y pi(y)q_0(y) = 1-2 sum_e f_e = delta_G(pi).                (9)

The independent-set version of (1) follows without an additional graph theorem.
Given S, set I=S\N(S). I is independent and N(I) is contained in N(S)\S. Thus
pi(S)-pi(N(S)) <= pi(I)-pi(N(I)).

If pi is proportional to positive integer weights W, the flow can be computed
using integer capacities W rather than normalized pi. Max flow is then integral,
and the symmetrized edge weights are half-integral. If every W(y) is a power of
two, all q_i(y), including q_0, have dyadic denominator dividing 2 max W. A
fixed number 1+log2(max W) of fair bits then implements the complete selector.
This does not itself establish bounded sensing/computation/actuation time.
For general rational weights exact selectors can have unbounded fair-bit
rejection time. Flow computation and its potentially exponential visible-state
table are genuine acquisition/computation costs, not a hidden free oracle.

## 5. Lower bound against all causal controllers

Consider the common-rate witness with p>0. At each boundary a causal controller
may use the full old history, arbitrary internal memory, independent seeds,
and any preceding calibration. It chooses an incident edge or the actual
visible-preserving R. Write U_t=1 when it selects R, and Y_t for the label.

For any independent set I, native motion exits I with probability p whenever
an ordinary edge is selected there. Entry into I is possible only from N(I).
Conditioning on the complete controller history therefore gives

 E[1_I(Y_{t+1})-1_I(Y_t)]
    <= p {Pr(Y_t in N(I))-Pr(Y_t in I)+E[U_t 1_I(Y_t)]}.           (10)

Summing and writing rho_T=T^(-1)sum_{t<T} Law(Y_t),

    E[T^(-1)sum_{t<T} U_t]
       >= rho_T(I)-rho_T(N(I))-1/(pT).                            (11)

If the visible marginal equals pi at every boundary, the boundary term in the
telescoping sum is actually zero, so (11) gives at once

    average R duty >= delta_G(pi).                               (12)

The same conclusion holds asymptotically whenever rho_T -> pi. Bounded
martingale differences give the analogous almost-sure occupation statement
along paths where the empirical label occupation converges. No stationarity
of the controller memory is needed for the expected finite-horizon inequality.

Thus no clever retained-history policy, no known-p calibration, and no
nonreversible controller circulation can reduce the worst-case duty below
(9). The constructive selector attains it for every compatible hidden menu.
Calibrating a different particular menu with favorable unequal rates can lower
its duty; that does not remove the common-rate member from the universal class.
The all-policy lower bound is not asserted separately for every connected
diffusion realization used as a sufficient physical supplier.

Without R, a finite-time approximate consequence is

    TV(rho_T,pi) >= [delta_G(pi)-1/(pT)]_+/2.                      (13)

Indeed the contrast 1_I-1_{N(I)} has range [-1,1]. This is an occupation or
all-boundaries maintenance statement. It is not a no-go theorem for a single
carefully chosen transient output time, a stopping-time preparation, an added
initializer, a physical hold, another actuator, or a different clock interface.

## 6. A qualitative limit for physical logical memory

Let C be a code with minimum Hamming distance at least two, and let the native
menu consist of individual bit operations. C is independent in the move graph.
If a desired physical law gives valid code configurations probability
pi(C)>=1-epsilon, then pi(N(C))<=epsilon and

    minimum visible-preserving duty >= 1-2 epsilon.                (14)

A controller maintaining 99.9% valid-code occupation therefore requires at
least 99.8% such activity in the common-rate witness. The rate p may be unknown
and arbitrarily slow; it cancels from the stationary duty requirement. Native
self-transitions remain present and costly. They do not become a selectable
safe operation.

This does not prove a universal thermodynamic cost of memory. It is a precise
actuation-menu limitation: every mandatory selected bit operation in the
witness has the same nonzero chance of moving out of a valid codeword. An
operation along a code-preserving physical direction supplies the missing
duty. Energy-biased controls, actual waiting/holding, collective code motions,
replacement specimens, or uncontrolled background noise change the model.

For the three-bit repetition code C={000,111}, weights W=B on C and W=1 on
the six other states have

    delta = (B-3)_+/(B+3).                                       (15)

For B>=3, choose edge coefficient 1 on each edge from a codeword to a
one-error neighbor, and zero elsewhere. Each error state selects its repairing
bit with probability one. A codeword selects each bit with probability 1/B
and the preserving operation R with probability 1-3/B. The two logical basins
are separate; this is a
valid invariant-law controller, not a claim to prepare the prescribed mixture
of logical values. Small positive extra flows can restore inter-basin
communication at a strictly higher duty. The full-state invariant statement
continues to allow unknown, evolving hidden memory.

### A scalable exact family, not a larger numerical fixture

The same controller has a closed form for every binary single-error perfect
Hamming code of length d=2^r-1. Index coordinates by the nonzero r-bit vectors.
The syndrome s(y) is the xor of the indices of the occupied coordinates. The
code C={s(y)=0} has |C|=2^d/(d+1) elements; every other vertex has the unique
code neighbor obtained by flipping coordinate s(y). These elementary code
properties are the classical Hamming construction, not a new code.

Give codewords weight B>=d and all other states weight 1. At a codeword choose
each bit operation with probability 1/B and R with probability 1-d/B. At a
non-codeword choose its unique repairing bit deterministically. Every selected
pair has the same weighted selection coefficient at both ends. The full hidden
target (2) is invariant for arbitrary compatible native kinetics, and

    pi(C)=B/(B+d),   preserving duty=(B-d)/(B+d).                  (15a)

The independent-set bound is attained because N(C)=C^c. The selector needs only
the actual syndrome, not a table over 2^d labels or a kinetic model. If B is a
power of two, a codeword uses log2 B fresh fair bits: values 0,...,d-1 choose
the respective bit, and every other value chooses R. Computing and sensing
the syndrome still cost O(d r) elementary bit operations/reads in the direct
implementation; this is not an uncharged collective detector.

The decoded codeword is exactly conserved by this restricted controlled menu:
each used edge remains within one codeword's radius-one basin. This is an
invariant controlled-activity model, not protection against arbitrary ambient
noise. If uncontrolled errors can occur on inactive coordinates, an R operation
that merely declines to add more errors does not preserve Y; the hypotheses
fail. An actual R could also be used permanently, so this model alone supplies
no memory advantage over ordinary protected holding. Its useful result is the
sharp duty law for a declared amount of mandatory stochastic actuation.

For contrast, compiling one fixed baseline-stationary native operation with
the accepted endpoint counter gives the same code mass B/(B+d) at macro
completion. Its stationary mean number of native calls is B(d+1)/(B+d), while
the concatenated native-time code occupation stays at the baseline 1/(d+1).
This comparison follows directly from the accepted occupation identity. The
fixed-clock selector pays for an actual preserving mode to maintain the changed
law continuously. Padding an early endpoint to a common deadline is a separate
operation: a kernel preserving only the visible label need not preserve the
complete hidden conditional law when its duration is correlated with the
stopping record.

## 7. A real hold is a strong ordinary comparator

Uniformly choosing a coordinate and preaccepting its actual call with
min{1,W(y^i)/W(y)} gives coefficients

    q_i(y)=(1/d)min{1,W(y^i)/W(y)}.                               (16)

The remaining probability is spent in an actual mu-stationary operation
preserving Y. Equation (5) immediately proves this conventional Metropolis
prechoice is valid without knowing the native kinetics. It requires no
microscopic rejection/rollback. It can be much easier to compute locally than
the optimal global flow. Optimizing the flow can reduce the preserving duty,
but not the unavoidable bound (12), and that optimization is conventional
network-flow mathematics. No practical speedup is established.

## 8. Two honest physical-time suppliers

### Fixed-duration addressed semigroups

Suppose every native call is P_i(t_0), from a mu-stationary semigroup P_i(t)
which preserves its visible pair at all intermediate times; similarly R(t)
preserves Y. Conditional selected input nu q_i is invariant under P_i(t) for
every t. Thus, when started at nu and selected according to q, the microscopic
marginal remains nu throughout the entire interval, not only at its endpoint.
Induction covers all intervals. This requires compatible actual boundary
sensing/selection; declaring a fixed native duration does not supply it.

The accepted addressed-diffusion family in continuation3 supplies the native
semigroup part: operation i evolves (x_i,z), fixes all other coordinates, and
preserves a separately sign-even baseline with the conormal reflecting domain.
An extra operation acting only on z with generator

    L_0 f = e^U div_z(e^(-U) B grad_z f)                           (17)

for positive symmetric B preserves the baseline and every visible sign. It
is an explicit mathematical supplier of R. It need not reset or mix all hidden
variables. The additional ability to isolate all visible coordinates while
driving z is a physical assumption, not already licensed by the endpoint
counter theorem.

### Finite-rate autonomous selector

There is also a complete continuous-time Markov supplier, avoiding zero-time
decisions as a mathematical assumption. Include a controller mode i. While
that mode is active, x evolves under its actual generator L_i. Independently,
mode i changes to j at rate

    s_ij(x)=gamma q_j(Y(x)),   i != j,   gamma>0.                  (18)

All rates are bounded by gamma. The joint measure

    rho(dx,i)=nu(dx)q_i(Y(x))                                    (19)

is invariant: each native component is stationary by (5), and controller
switching satisfies rho_i s_ij=rho_j s_ji. Hence its physical x marginal is
nu at every real time at stationarity. If all native generators are reversible,
the complete joint process is reversible. Selection remains valid when hidden
kinetic rates differ without being measured.

Duty here means the stationary ensemble fraction (and the long-run fraction
under the corresponding ergodicity assumptions). Conserved components do not
automatically share one trajectory-wise duty or a common preparation rate.

This construction supplies a precise finite-rate hybrid generator; actual
state-dependent selector rates, sensors and compatible couplings must be
realized. It does not assert an apparatus. A Hamiltonian interpretation, when
native mu is Boltzmann, assigns mode energy

    V_i(y)=-k_B T log[W(y) q_i(y)] + constant.                     (20)

This energy is unchanged along the active native fiber, while mode jumps obey
the corresponding equilibrium rate ratio. Its sum over modes produces W.
Zero q_i means a forbidden mode/state combination, so finite-energy hardware
needs strict-positive compatible flows or a controlled approximation. An
optimum that sets some q_i to zero may be an infimum for a stricter hardware
class requiring every gate rate to remain positive. The exact mathematical
optimum allows genuinely unavailable transitions. There
is no free energy creation or free implementation of the detector in (18).

For the common-rate continuous-time witness (all active bit flips at rate
lambda), integrating the same indicator generator proves the physical-time
counterpart of (11), with pT replaced by lambda times elapsed time. Thus the
minimum stationary time fraction in the preserving mode remains delta.

## 9. Preparation and other limits

The optimum flow can be disconnected or can turn off useful native modes.
Invariance alone is not convergence or preparation. If all required edges can
be given positive compatible flow, known irreducibility conditions can be
applied; unknown hidden sectors still retain their own masses. To retain all
native edges with an available R, mix the optimum with a positive feasible
small-flow solution. This costs additional duty and does not furnish a rate.

The uniform visible baseline matters. For a nonuniform baseline b(y), the
pair-constant condition concerns the tilt W(y)=pi(y)/b(y), not pi itself. The
simple delta_G(pi) formula and common-p witness cannot be transferred unchanged.

State-dependent selection with arbitrary probabilities is generally biased.
The graph condition is not satisfied merely because each native operation
preserves the same baseline. Nor do native endpoint kernels alone determine
their intermediate physical-time laws.

The present result is an independent constructive intermediate and a strong
counterexample to equating completion-law control with sustained physical
memory. It does not currently displace the root's preparation question as the
more consequential research destination.
