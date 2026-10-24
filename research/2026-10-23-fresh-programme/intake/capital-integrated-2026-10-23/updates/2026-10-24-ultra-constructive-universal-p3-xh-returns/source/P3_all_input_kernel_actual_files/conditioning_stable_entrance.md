# Conditioning-stable entrance certificates and reusable reaction-record filters

New research work in this Pro3 continuation. This file gives the mathematical
contract connecting a pointwise relative entrance compiler to later scientific
operations. It does not claim novelty for Hilbert projective distance, positive
operator nonexpansion, or classical Bayesian filtering. Its constructive target
is an entrance representation obtained from a compact reaction source, with a
certificate that remains useful under arbitrary later observations.

No original research script is modified by this file. The all-record theorem
below is proved here. The companion relative entrance compiler and its output
are separate new code and data; the general additive-local filter is specified
and proved here rather than claimed as a general implemented solver. Its
site-resolved local-count specialization is implemented in the new
`conditioned_count_queries.py`, with the concrete certificate reviewed below.

## 1. The retained certificate

Let M and L be finite nonzero nonnegative measures on the same retained state
space E. M is the exact unnormalized entrance law and L is an acquired positive
representation. Obtain constants

    0 < a <= b < infinity,
    a L <= M <= b L.                                      (1)

The inequalities are measure inequalities: they hold on every measurable set.
For finite E they are simply componentwise inequalities. Define

    D = log(b/a),
    tau(D) = tanh(D/4)
           = (sqrt(b/a)-1)/(sqrt(b/a)+1).                 (2)

D is a certified upper bound on the Hilbert projective distance. A common
positive scaling of a and b changes the mass calibration but not D. Retaining
the scale as well as the spread is useful for record likelihoods.

The lower bound a>0 and finite upper bound b are substantive. They require M
and L to have the same support up to null sets. Structural zero coordinates
are allowed if both measures have those zeros. Strict positivity on every
configuration of the ambient state space is unnecessary.

## 2. All-record propagation and conditioning theorem

A scientific operation is represented by a common positive kernel K from E
to an output space. Its mass need not be at most one: an exact observation
time contributes a density kernel, which can have larger mass. The necessary
condition is that MK and LK have finite mass and are nonzero for the record
under consideration.

The kernel can combine propagation, observations, resets, integration over
unobserved variables, selection of an event, and retention of a later hidden
state or a future trajectory. For a fixed observed record y, write

    K_y = K_1(y_1) K_2(y_2) ... K_N(y_N).

The kernels may depend on earlier public observations and on a common protocol.
For that realized record they must be the same kernels for M and L.

### Theorem 1: a once-only entrance guarantee

If (1) holds, then for every finite record y and every such common operation,

    a L K_y <= M K_y <= b L K_y.                         (3)

Consequently the normalized output laws satisfy

    TV( M K_y / (M K_y 1), L K_y / (L K_y 1) )
       <= tau(D).                                      (4)

Here TV(P,Q)=sup_A |P(A)-Q(A)|=(1/2)||P-Q||_1 for
probability measures. The bound does not contain the probability or density
of the record, the number of observations, or the elapsed time. It holds
simultaneously for all finite records whose output mass is positive.

The exact and acquired laws agree on which records have zero likelihood: (3)
and a>0 imply that one output mass is zero if and only if the other is zero.
Conditioning is not defined on these common zero-likelihood records.

**Proof.** If M-aL and bL-M are nonnegative measures, applying a positive
kernel to either difference preserves nonnegativity. Induct over the common
kernels. Normalize only at the end and apply Lemma 2 below. Normalizing
intermediate filters gives the same final law because all removed constants
cancel. No mixing or strict positivity of the kernels is needed. QED.

An observed continuous-time record is interpreted using a fixed density
version, such as the matrix-exponential formula in Section 6. Otherwise a
regular conditional law is only defined almost everywhere, and an unsupported
claim about every possible zero-measure record would be inappropriate.

The theorem also covers a later query selected after seeing the record:
append its common positive kernel to K_y. It covers hidden-state smoothing
and path queries starting at the certified entrance when the output kernel
retains that path information. It does not reconstruct unretained history
before the entrance.

### Lemma 2: sharp conversion to normalized total variation

If a V<=U<=b V for nonzero finite measures, then

    TV(U/U1,V/V1) <= (sqrt(b)-sqrt(a))/(sqrt(b)+sqrt(a)).  (5)

The constant is sharp given only a and b.

**Proof.** Put q=V/V1, r=dU/dV, and z=E_q r=U1/V1. Thus
a<=r<=b and a<=z<=b. For a<b, convexity of |r-z| gives

    E_q |r-z| <= 2 (b-z)(z-a)/(b-a).

The normalized TV is E_q|r-z|/(2z), so it is at most

    (b-z)(z-a)/(z(b-a))
      = (a+b-z-ab/z)/(b-a).

Since z+ab/z>=2 sqrt(ab), this is bounded by (5). Equality occurs for a
two-point q with r taking a and b and E_q r=sqrt(ab). The case a=b gives
identical normalized measures. QED.

The same proof gives a sharper bound when the output mass ratio z is known:

    TV <= (b-z)(z-a)/(z(b-a)).                           (6)

Multiplying an observation kernel by an arbitrarily small positive scalar
makes its record arbitrarily rare without changing either posterior. Thus
the sharpness example can occur at arbitrarily small observation probability.

### Operational characterization by future selection

For fixed finite measures M,L that are positive on the same finite support,
let

    a_* = min_x M(x)/L(x),
    b_* = max_x M(x)/L(x),
    H = log(b_*/a_*).

Then

    sup_{0<=ell<=1, L ell>0}
      TV(ell M/(M ell), ell L/(L ell)) = tanh(H/4).

Here ell is the state-dependent probability of a selected observation. Thus
the transformed projective distance is exactly the worst-case posterior TV
over all possible common future selections of the retained state.

**Proof.** The upper bound is Theorem 1. If a_*=b_*, the two normalized laws
coincide. Otherwise choose states x_a,x_b attaining the extrema, and let

    q_a = sqrt(b_*)/(sqrt(a_*)+sqrt(b_*)),
    q_b = sqrt(a_*)/(sqrt(a_*)+sqrt(b_*)).

Set ell(x_a)=c q_a/L(x_a), ell(x_b)=c q_b/L(x_b), and ell=0 elsewhere.
Choose c>0 small enough that both nonzero values are at most one. The
normalized selected L law is (q_a,q_b), while its M/L ratio takes a_*,b_*
and has mean sqrt(a_* b_*). This is the equality case of Lemma 2. QED.

Taking a smaller c makes the selecting event arbitrarily rare without
changing the equality. Allowing arbitrary common positive output kernels
does not increase this supremum, since Theorem 1 bounds them all and the
selection kernels already attain it. In particular, a uniform error target
epsilon<1 for every such future selection is equivalent to

    H <= 4 atanh(epsilon).

This characterizes the actual pair of entrance laws. A computable upper
bound D>=H is a sufficient certificate and need not be optimal. A restricted
scientific operation class may have a smaller worst-case error, and may not
physically realize the selecting likelihood above.

This is an operational corollary of established projective-metric theory,
derived explicitly here; no historical novelty is claimed. The sharp
comparison and its endpoint optimization are treated in Cohen and Fausti,
Theorem 5.1 and Remark 15. The characterization explains why a relative
entrance certificate is the right contract for unrestricted future selection.

## 3. Record likelihoods: keep normalization and mass calibration distinct

The raw unnormalized record weights obey

    a <= (M K_y 1)/(L K_y 1) <= b.                       (7)

For normalized entrance laws, let

    z_0 = M1/L1.

The actual record probability or density ratio obeys

    a/z_0 <= P_M(y)/P_L(y) <= b/z_0.                    (8)

If z_0 has not been separately evaluated, (1) implies z_0 in [a,b], yielding

    a/b <= P_M(y)/P_L(y) <= b/a,
    |log P_M(y)-log P_L(y)| <= D.                        (9)

If the measures in (1) already have unit mass, z_0=1 and the sharper interval
[a,b] applies. It is incorrect to apply [a,b] directly to normalized record
likelihoods when (1) compares unnormalized entrance measures of unequal mass.

These are whole-record bounds, not bounds to be multiplied once for every
observation. The product of incremental likelihood ratios telescopes to the
single ratio in (8). Conditional prediction after any earlier record has the
same spread b/a, so every later event probability is likewise bounded
multiplicatively by [a/b,b/a], conservatively, whenever its reference
probability is positive.

For a bounded observable f with range [u,v], (4) implies an expectation error
at most (v-u) tau(D). For any nonnegative observable, (3) also supplies raw
multiplicative integral bounds, provided the integrals are finite.

### Corollary: common entrance and different future kinetic models

Suppose the same uncertain physical entrance M is used by every proposed
future model theta, and the same acquired entrance L has certificate (1).
Let pi_theta be a common prior on a finite candidate family, and K_theta the
candidate's exact positive record/output operator. The direct-sum operation

    K(x,{theta} x B) = pi_theta K_theta(x,B)

is one positive kernel. Therefore the true and acquired joint measures of
the candidate label and retained output satisfy the SAME sandwich a,b.
Their normalized joint distributions, and hence their model-posterior
marginals, have TV at most tanh(D/4).

For two candidates of positive record likelihood,

    1/(b/a) <= BF_true(theta,phi)/BF_acquired(theta,phi) <= b/a.

The common entrance mass normalization cancels between the models. Applying
separate conservative intervals [a/b,b/a] to each model and dividing them
would unnecessarily square this factor. The direct-sum argument retains
the shared calibration and avoids that loss.

If a numerical executor supplies positive lower joint outputs L_theta with

    L_theta <= L K_theta <= C_theta L_theta,

then the assembled prior-weighted joint approximation has spread at most

    (b/a) max_theta C_theta.

Its model-posterior TV is bounded by the corresponding tanh(log-spread/4).
The Bayes-factor interval relative to the ratio of the two lower computed
likelihoods is

    [1/((b/a) C_phi), (b/a) C_theta].

The maximum over candidate numerical spreads is appropriate because these
are alternative branches in a positive sum, not successive operations.

### Corollary: model-specific entrances and separately calibrated likelihoods

Consider a finite family of specified kinetic models theta, each with its own
certified entrance and exact later record operator. Let p_theta(y) and
q_theta(y) denote its exact and acquired record likelihoods, with proved

    l_theta <= p_theta(y)/q_theta(y) <= u_theta.

For normalized conditional entrance laws these multipliers are supplied by
(8) or (9). If the preparation event itself is part of the observed record,
the raw joint preparation-and-record weights instead use (7), retaining that
event's model evidence.

For candidates theta and phi of positive likelihood, the multiplicative
error of their Bayes factor lies in

    [l_theta/u_phi, u_theta/l_phi].                     (10)

With the same prior over the candidate models, their exact and acquired
posteriors are related by the sandwich with

    l_* = min_theta l_theta,   u_* = max_theta u_theta.

Therefore their model-posterior TV is at most

    tanh( log(u_*/l_*)/4 ).                              (11)

For example, if every candidate has entrance projective spread at most D
and only the conservative normalized likelihood bounds (9) are used, the
model-posterior TV is at most tanh(D/2). The guarantee does not degrade merely
because the record is long or rare. It certifies the computational comparison
of the supplied models, not their biological adequacy or identification from
insufficient data. A continuous parameter family would additionally require
uniformly obtained multipliers over that family.

## 4. Composition of newly introduced approximation errors

The once-only guarantee concerns one certified entrance and identical exact
later operators. New numerical, reduction, or recompression errors require
additional certificates.

Suppose the exact step T_k and acquired step T_hat_k satisfy positive-kernel
order bounds

    alpha_k T_hat_k <= T_k <= beta_k T_hat_k,
    0 < alpha_k <= beta_k < infinity.                   (12)

For finite state spaces, entrywise kernel inequalities suffice. More general
state-dependent certificates may be used if they establish the needed
measure order for every reachable input to which they are applied.

With the initial certificate (1), positivity and induction give

    a_total = a product_k alpha_k,
    b_total = b product_k beta_k,
    D_total = log(b/a) + sum_k log(beta_k/alpha_k).       (13)

The final normalized TV is at most tanh(D_total/4). Replacing a current
representation by a new one with a proved order sandwich obeys the same
rule. Exact normalizations and positive rescalings do not consume spread.

Thus independent local approximation factors add in log-spread. Ordinary
floating-point evaluation without such an enclosure is not silently covered
by the entrance certificate. Arbitrarily many new errors of a fixed positive
spread need not have a bounded accumulated spread. A summable error budget,
a proved additional contraction, or a fresh global certificate would be
needed for that stronger claim.

### Product and positive-sum assembly

If local nonnegative factors satisfy

    a_i l_i <= m_i <= b_i l_i,

then their tensor products satisfy the sandwich with multipliers
product_i a_i and product_i b_i. This is a local obtaining route that avoids
enumerating the product configuration space.

For matched positive mixture components, suppose

    a_r L_r <= M_r <= b_r L_r.

Then

    (min_r a_r) sum_r L_r <= sum_r M_r
                          <= (max_r b_r) sum_r L_r.      (14)

Weights can be included in each component's factors. Combining tensor
products with (14) gives a checkable certificate from local factor and weight
bounds. Positive summation is essential; cancellation in a signed expansion
does not satisfy this argument. A newly obtained quadrature certificate can
compare whole measures directly and need not match a discrete component to
each member of a continuous latent-time mixture.

## 5. Contract supplied by the relative Gauss entrance compiler

The companion new work obtains the following form of certificate. Let M be
the true unnormalized entrance measure, G the exact positive Gauss sum, and
L the retained rational lower-node product mixture. The required bounds are

    |M(x)-G(x)| <= delta M(x),   delta<1,
    L <= G <= U <= c_round L.                           (15)

They hold componentwise on the retained hidden state, with shared structural
zeros handled exactly. Therefore

    a = 1/(1+delta),
    b = c_round/(1-delta),
    D <= log(c_round) + log((1+delta)/(1-delta)).          (16)

The relative quadrature error and numerical node spread are distinct parts
of the obtaining certificate. A relative claim only for the total entrance
mass would not establish (15), and would not support Theorem 1.

The complete local-derivative, positive-Peano-remainder and node-rounding
construction is in `relative_gauss_entrance_proof.md`. That companion proof
also supplies a more conservative midpoint obtaining algorithm for the
admitted source class; this file uses its resulting measure sandwich.

The file `relative_correlated_entrance_24sites.json` stores exact rational
multipliers, weights and local factors for a concrete new instance. Its
reported posterior-TV upper was independently checked against those exported
rationals using the exact equivalent inequality

    b/a <= ((1+u)/(1-u))^2,  0<=u<1,

where u is the reported upper bound. That arithmetic check validates the
conversion and conservative rounding, not by itself the entire quadrature
proof or a biological model.

In that source instance the retained state is the post-event leaf
configuration, the known open controller and the exact observed timestamp.
The continuous opening time is marginalized. Mixture labels are
representation indices, not an approximation to a continuous opening-time
law. Future Markov operations on the retained state are covered;
retrospective queries about the discarded opening history are not.

## 6. Exact reusable filter for additive local killing and product resets

The general all-record theorem does not guarantee cheap execution. The
following compact source class makes execution explicit.

### Source contract

There are finite modules E_1,...,E_n and a known public phase q. In each phase:

1. Unmarked dynamics act independently on the modules, with local generators
   Q_(q,i). Every unmarked rule reads and changes only its own admitted module.
2. Each recorded mark j identifies a local hazard source c(q,j). Its
   nonnegative rate is h_(q,j)(x_c), depending only on that module.
3. At mark j, the state reset is a tensor product of local stochastic kernels
   R_(q,j,i). Resets may change several modules simultaneously, but each local
   output depends only on its own local input and the known phase and mark.
4. The next phase is known from the public record. There are no additional
   hidden cross-module reactions, hidden phase changes, or unrecorded common
   resets omitted by the local generators.

An admitted module may itself be a finite block of molecular coordinates.
The local obtaining and execution costs of that block are paid explicitly.

Define the total local marked hazard and killed local generator by

    k_(q,i)(x_i) = sum_{j:c(q,j)=i} h_(q,j)(x_i),
    S_(q,i) = Q_(q,i) - diag(k_(q,i)).

Between recorded marks, the global subgenerator is the Kronecker sum of the
S_(q,i), hence its no-mark propagator factors exactly:

    exp(t S_q) = tensor_i exp(t S_(q,i)).                 (17)

For mark j define local nonnegative matrices

    B_(q,j,c) = diag(h_(q,j)) R_(q,j,c),
    B_(q,j,i) = R_(q,j,i),              i != c.

The event-density/reset operator is

    B_(q,j) = tensor_i B_(q,j,i).                         (18)

Allowing diagonal entries in B correctly includes recorded events that do
not change a local hidden state. Killed generators remove their hazard from
the no-mark law even when the reset is the identity.

### Theorem 3: fixed positive mixture width for every observed record

Suppose the acquired entrance is a positive product mixture

    L/L1 = sum_{r=1}^R w_r tensor_i u_(r,i),
    w_r>=0, sum_r w_r=1, u_(r,i)1=1.

For every finite observed sequence of elapsed times and marks, including
terminal intervals with no mark, the exact filter from this acquired
entrance remains a positive product mixture with at most R components.
The exact record likelihood and local factors can be updated using only
local matrix operations and scalar products. If (1) holds for the true
entrance, the exact true filter is within tau(D) of this acquired filter
for every such record, without a record-rarity denominator.

**Constructive proof.** For elapsed time t and mark j in phase q, compute

    v_(r,i) = u_(r,i) exp(t S_(q,i)) B_(q,j,i),
    s_(r,i) = v_(r,i) 1,
    s_r = product_i s_(r,i),
    Z = sum_r w_r s_r.

For Z>0, drop components with s_r=0 and set

    w'_r = w_r s_r/Z,
    u'_(r,i) = v_(r,i)/s_(r,i).

These are exactly the factorized images of each product component under
(17) and (18). The scalar Z is the incremental record density. For a
terminal no-mark interval omit the B matrices. Induction proves the width
claim and multiplying the Z factors gives the record likelihood. Apply
Theorem 1 to compare the true and acquired filters. QED.

The exact representation has O(R sum_i |E_i|) stored probabilities, plus
the local generators, local event matrices and source description. Once
local propagators are available, dense factor updates take
O(R sum_i |E_i|^2) arithmetic per event; sparse or analytic modules can cost
less. The total work still grows with record length. Neither the structural
width nor the inherited entrance-error bound grows with record length or
rarity. Evaluating local propagators to certified numerical accuracy is an
additional task, and its errors are governed by Section 4.

Per-component rescaling and log-likelihood accumulation can avoid numerical
underflow. They do not themselves establish a rounding certificate. The
number of bits or precision needed for a requested numerical likelihood
accuracy is not claimed independent of the record.

### Exact closure boundaries

A mark that combines unknown triggering modules generally has an operator
that is a sum of tensor products. Applying it can increase mixture width.
Separate observed marks for the alternatives avoid that particular hidden
mixture. Likewise, a cross-module hazard usually makes the no-mark killing
nonadditive and destroys (17). A reset that reads another module's hidden
state can destroy (18). Enlarging local blocks can repair some sources, at
an explicit cost.

Unknown common event times can correlate otherwise independent modules:
integrating a tensor product over a shared unknown time is generally not a
single tensor product. The all-record order theorem still holds for that
positive integral operator, but Theorem 3's fixed-width execution claim does
not automatically hold. A new certified entrance compilation or another
compact representation would be needed.

The protocol may be chosen adaptively from the common observed history. If
two agents instead choose different physical interventions using different
posterior estimates, their future operators are no longer common, and the
theorem does not compare those distinct experiments.

### 6.1 Site-resolved counts without event timestamps or event ordering

For this operation impose an additional local-source condition: each counted
reaction resets only its own module, and there is no unobserved event-dependent
change to a shared phase or controller during an observation window. Local
rates may change according to a known protocol between windows. These
conditions hold for the implemented continuation, whose controller remains
open and whose turnover events reset their firing site from one to zero.

For a finite local module write A for its generator with counted events
removed but their hazards retained as killing, and J for the nonnegative
counted-event/reset matrix. Assume A+J is a conservative generator. J may
have diagonal entries when a counted event leaves the state unchanged.

The count-resolved transition matrix is

    B_k(t) = [z^k] exp(t(A+z J)),

where B_k(t)(x,y) is the joint probability of exactly k counted reactions
in the window and final local state y, given initial local state x. To obtain
it, construct k+1 counter layers, each with the original local states:

    augmented diagonal blocks: A,
    augmented first upper-diagonal blocks: J,
    all other blocks: zero.

An attempted counted event beyond layer k is killed. The upper-right block
from initial layer zero to final layer k in the augmented exponential is
exactly B_k(t). Its size is |E_i|(k+1), involving local states only.

This generating matrix and the count equations are established Markovian
arrival-process machinery; for an explicit primary treatment see Neuts
(1996), Section 3, equation (9) and the following generating-function formula.
They are used as local execution primitives here, not claimed as new formulas.

**Proof.** Coefficients of exp(t(A+zJ)) satisfy

    dB_0/dt = B_0 A,
    dB_k/dt = B_k A + B_(k-1) J,
    B_0(0)=I, B_k(0)=0 for k>0.

These are precisely the forward equations for the indicated blocks of the
augmented subgenerator. Uniqueness proves the identity. Killing on overflow
ensures that paths with more than k counts do not contaminate the result.

### Theorem 4: count-record closure

For independent local dynamics under the preceding source conditions, the
operator for a site-resolved vector of observed counts k_1,...,k_n over a
common known time window is

    B_vector(t) = tensor_i B_(i,k_i)(t).

Consequently every sequence of such count windows preserves a positive
product-mixture width of at most R, even though event timestamps and the
global event ordering are not observed. Updates use the same formula as
Theorem 3 with each local factor replaced by u_(r,i) B_(i,k_i)(t).
The projective entrance certificate propagates through the whole record.

The tensor identity follows by independence of the local path processes
conditional on the initial product component. Counting and integrating local
event times occur separately in each module, so no shared latent integration
variable is introduced. The correlated entrance is retained by summing the
same R product components with updated weights.

An unresolved total count over all sites instead produces a sum over count
allocations. An event that resets another module, or changes an unobserved
shared controller within the window, can also couple the local path laws.
The tensor identity and fixed-width count theorem cannot be asserted for
those sources without additional construction.

### 6.2 Positive uniformization and the implemented numerical certificate

For an augmented subgenerator T choose Lambda at least its maximum exit rate,
so P=I+T/Lambda is nonnegative and substochastic. With z=Lambda t,

    exp(tT) = exp(-z) sum_{m>=0} z^m P^m/m!.

Every entry of P^m lies in [0,1]. The sum through order N is a componentwise
lower bound. If z<N+2, the omitted tail is bounded by

    exp(-z) z^(N+1)/(N+1)! / (1-z/(N+2)).

This follows because the ratio of consecutive omitted Poisson terms is at
most z/(N+2). It avoids subtracting a nearly unit partial Poisson sum from
one. Outward enclosures for exp(-z), followed by directed arithmetic, turn
this into entrywise interval bounds on each local B_k.

The implemented binary source has

    A = [[-alpha, alpha], [beta, -beta-kappa]],
    J = [[0,0],[kappa,0]].

`conditioned_count_queries.py` uses Lambda=max(alpha,beta+kappa), N=64,
and the local counting augmentation above. It requires a strictly positive
resolved lower bound for every local transition entry used in the positive
ratio certificate; if the numerical enclosure cannot resolve that support,
it raises an error. A zero lower bound cannot be divided away.

At a particular update let the currently retained normalized mixture be nu.
For each of its components, outward arithmetic encloses the weight and each
updated local vector. The product of their lower endpoints defines a
nonnegative component L_r. The product of the weight endpoint ratio and the
largest local endpoint ratios gives c_r satisfying

    L_r <= exact updated component <= c_r L_r.

Summing components gives the step certificate

    L_step <= nu B_vector <= c_step L_step,
    c_step = max_r c_r.

The implementation converts every chosen lower endpoint to an exact rational,
computes the lower component masses exactly, and normalizes their sum exactly.
Let z_k=L_step 1 at step k. If

    Z_N = product_{k<=N} z_k,
    C_N = product_{k<=N} c_step,k,

and nu_N is the retained final normalized mixture, induction gives

    Z_N nu_N <= nu_0 B_1...B_N <= C_N Z_N nu_N.

Combining this with entrance spread R_0=b/a gives final posterior spread at
most R_0 C_N and final posterior TV at most tanh(log(R_0 C_N)/4). For the
true normalized entrance and no separately evaluated initial mass calibration,
the complete record probability belongs to

    [Z_N/R_0, Z_N R_0 C_N].

This is the interval used by the program. It contains no repeated division
by the small record probability. The exact rational Z_N multiplies the
chosen lower masses; C_N certifies their numerical approximation error.

### 6.3 Concrete reviewed execution and its limits

The completed new execution uses the already acquired 24-site, 256-component
entrance. It observes twelve half-unit windows, with one turnover at each of
six rotating sites and zero turnovers at the other eighteen sites per window.
The record contains 72 turnovers in six time units. Each actual local
augmentation has two or four states; no global counter or global event
ordering is enumerated.

The recorded complete count-record probability interval is

    [4.07290438597226966622023033511964966554584529e-69,
     4.07290440107994958582641393628708542512249069e-69].

All 256 product components are retained. The reported final posterior-TV
upper bound, including subsequent numerical errors, is

    4.63664208016393462417317532333672842002897586e-10.

The accumulated later numerical spread minus one is at most

    1.42500000000000000000000000000000000000000931e-41.

This last quantity is a multiplicative spread increment, not a separately
defined TV error. The reported posterior-TV bound uses it in R_0 C_N.

Independent inspection of the code confirmed the augmented-generator
orientation, overflow killing, positive Poisson tail, componentwise ratio
assembly, and exact normalization induction. Checks of the saved outputs
confirmed exact normalization of the 256 positive weights, valid local
probabilities, exact agreement between the stored cumulative spread and the
product of step certificates, and conservatively rounded posterior-TV and
relative-likelihood bounds. These checks did not rerun source acquisition
or the twelve-window filter.

The saved local floating-point matrix-exponential comparisons are consistency
checks, not the numerical certificate; that certificate is the positive
uniformization and directed-arithmetic construction. The record is synthetic.
The implementation tests a specified reaction source and observation model,
not empirical biological identification.

## 7. Why a TV-only entrance certificate is insufficient for this operation

### Rare conditioning with positive support

For 0<epsilon<1 and 0<eta<1/2, take three hidden states and

    P = (1-epsilon, epsilon(1-eta), epsilon eta),
    Q = (1-epsilon, epsilon eta, epsilon(1-eta)).

Both laws have full support and

    TV(P,Q) = epsilon(1-2 eta).

The common observation B={second state,third state} has probability epsilon
under both laws. Nevertheless,

    TV(P(.|B),Q(.|B)) = 1-2 eta.

The unconditional discrepancy can be arbitrarily small while the conditional
discrepancy approaches one. This is a limitation of the TV-only information,
not just a weakness of a particular normalization inequality.

### A finite controller and a Poisson-count truncation

Consider a controller with states 0,1,...,K+1, initially 0. It jumps from i
to i+1 at rate lambda for i<=K, and K+1 is absorbing. At time T,

    P(controller=K+1) = P(Poisson(lambda T)>=K+1) > 0.

Uniformization at rate lambda gives the exact local transition law. Retaining
only Poisson terms n<=K and renormalizing yields a law with zero mass at K+1.
Its full path-law error is at most the discarded Poisson probability, which
can be tiny; its endpoint error is no larger. Yet a later recorded reaction
enabled only at controller state K+1 has positive likelihood in the exact
model and zero likelihood in the truncated model.

No finite upper multiplier b can repair that support failure. The subsequent
conditional law is undefined in the truncated model. This construction is a
finite rational-source example when lambda and T are rational; it does not
depend on an infinite hidden-state space.

The example does not say that every count truncation loses endpoint support.
Even if the retained part has full support, its small discarded total mass
alone still gives no useful uniform relative bound. To promote

    M = L_keep + T_tail

to the present contract, one can instead prove the componentwise domination

    0 <= T_tail <= rho L_keep.

Then L_keep<=M<=(1+rho)L_keep and the all-record theorem applies. Obtaining
rho is additional scientific work; a total tail-probability bound is not its
substitute. A positive support-covering correction is another possible
construction, but must itself come with the requisite pointwise bounds.

## 8. Complete-state and support obligations

The order comparison concerns a specified retained state. It must contain all
information needed by the future kernel. If an unobserved absolute event time
controls a later external protocol, that time is part of the needed state or
must be integrated using its correct correlation with the retained variables.
A state-only certificate does not justify silently replacing it by a
representative time. A continuous joint time law and a finitely atomic
replacement can be mutually singular even when their hidden-state marginals
are very close.

Conversely, a latent preparation or opening time need not be retained when
the exact post-event state and known public phase already make later dynamics
Markov. Integrating that history into the entrance law is then legitimate.
Which of these cases applies must follow from the source's conditional
independence and reset structure.

Structural zeros must be proved, not inferred from numerical underflow.
Relative bounds on configurations whose exact mass is zero must preserve that
zero. Entrywise relative bounds for later approximations need corresponding
support care. A generic TV approximation cannot be relabelled as a
projective certificate without this additional obtaining work.

## 9. Scientific operation and relation to existing machinery

One useful composition is a difficult preparation phase with common latent
timing, followed by many local measurements or reactions. The preparation
creates correlated local states. A source-obtained positive mixture with
the certificate (1) can then support every later event record admitted by
Section 6, including records whose probabilities decrease exponentially
with the number of probes, while retaining a nontrivial posterior for
unobserved modules.

For example, frozen binary sites followed by sequential site-local probes
give record weights proportional to

    sum_r w_r product_{i in S} p_(r,i)

for records requiring the sites in S to be active, times known probe-density
factors. The posterior over unprobed sites uses the same updated mixture
weights. The formula keeps the correlations, evaluates without enumerating
all binary configurations, and is covered by the once-only certificate.
This is a stated synthetic operation, not a claim of experimentally identified
molecular kinetics.

The projective-metric facts used here are established mathematical machinery.
Le Gland and Oudjane's Theorem 4.1 already propagates initial Hilbert error
to later filtering TV without extra assumptions on the nonnegative kernels.
Their Remark 4.3 gives pointwise multiplicative kernel bounds as sufficient
local error certificates, and Theorem 4.4 propagates local Hilbert errors.
Mixing strengthens those statements to contraction and stronger indefinitely
recurring-error bounds; it is not needed for the basic nonexpansion used
here. Cohen and Fausti give the sharp comparison with TV. Thus avoiding a
Bayes-normalizer denominator and composing local relative errors are also
established machinery. The present work's candidate obtaining contribution
is the compact source-to-entrance construction, its explicitly computed
pointwise certificate, and its executable local reaction operations.

An ordinary retaining programme, a conventional filter, or another network-free
implementation supplied with the same representation and certificate can
adopt exactly these algorithms. There is no architecture-necessity claim.
Nor does this theorem show that every compact reaction program admits a
small relative entrance representation: support, correlations, local block
sizes, quadrature conditions, and later operator structure are substantive.

## 10. A kinetic comparison with exactly matched stationary flux

The implemented local turnover source has silent rates alpha for 0 -> 1 and
beta for 1 -> 0, and a counted turnover 1 -> 0 at rate kappa. Its full
unobserved generator has 0 -> 1 rate alpha and 1 -> 0 rate beta+kappa.
Put r=alpha+beta+kappa and lambda=alpha*kappa/r. For a scale s>=1 define

    alpha_s = s alpha,
    beta_s = s(beta+kappa)-kappa,
    kappa_s = kappa.

These are nonnegative rates, and the full generator becomes s times the
original generator. Hence both the stationary active fraction alpha/r and
the stationary turnover rate lambda are exactly unchanged. The reaction
record nevertheless changes because the count mark remains at rate kappa.

Every turnover resets the module to state zero. Its subsequent interevent
time tau_s is therefore a phase-type renewal interval. The two-state
first-step equations, or the transform of its absorbing generator, give

    E[tau_s] = r/(alpha*kappa),
    Var(tau_s)/(E[tau_s])^2 = 1 - 2 alpha*kappa/(s r^2).

For a direct derivation, before scaling the Laplace transform from reset
state zero is alpha*kappa/[z^2+r z+alpha*kappa]. After scaling it is
s*alpha*kappa/[z^2+s*r*z+s*alpha*kappa]. Differentiating at zero gives
E[tau_s]=r/(alpha*kappa) and
E[tau_s^2]=2r^2/(alpha^2*kappa^2)-2/(s*alpha*kappa), from which the
displayed squared coefficient of variation follows. Consecutive local
interevent intervals after resets are independent under this specified
time-homogeneous source; this example does not claim serial interval
correlation. Increasing s makes this SCV approach one from below.

There is also a comparison with exactly matched finite-window count means
when each model starts in its full stationary distribution. A turnover at
time zero resets the state to zero, so its future conditional event
intensity at lag u is lambda*(1-exp(-s*r*u)). Therefore the stationary
second-order event product density at positive lag is
lambda^2*(1-exp(-s*r*u)). Integrating its covariance gives

    E[N_s(T)] = lambda*T,
    Var(N_s(T)) = lambda*T
      - 2*lambda^2*( T/(s*r) - (1-exp(-s*r*T))/(s^2*r^2) ).

The executed common acquired entrance is generally nonstationary. Thus its
finite-window means are not asserted equal. The stationary identities
identify which coarse long-run summaries are uninformative for this pair;
the actual record comparison retains transients and full count statistics.
For the first module, alpha=3/5, beta=2/5, kappa=3/2, and s=4, the common
stationary active fraction is 6/25, the common stationary turnover rate is
9/25, and the two interevent SCVs are 89/125 and 116/125.

`kinetic_model_comparison.py` obtains the changed local generators and
hazards through the rule compiler, imports the same prepared correlated
entrance, and reads the retained baseline filter instead of repeating it.
On the supplied twelve-window synthetic record its certified Bayes factor
for the changed model over the baseline lies in

    [0.0000033307523354329459560,
     0.0000033307523477877511286].

The common preparation is stipulated before either proposed future kinetic
model acts. If the models had also differed during preparation, their
entrance laws and preparation likelihoods would need separate obtaining.
This is a certified likelihood comparison of two specified mathematical
mechanisms, not physical evidence that either describes a real system.
The joint probability object retains exact rational model weights and the
two conditional hidden-state laws; both coefficient uncertainties and
subsequent numerical spreads are included in its certificate.

## 11. Rare reaction-guard probabilities from the retained law

A projective certificate also gives useful relative enclosures for a rare
query, even when its probability is far below the absolute TV bound. Let
P,Q be normalized laws with projective spread at most R, and let A be an
event with q=Q(A) in (0,1). Integrating the density-ratio envelope over A
and its complement gives

    (1/R) <= [P(A)/(1-P(A))] / [q/(1-q)] <= R.

Solving for P(A) yields the sharp interval based on q and R alone,

    q/[q+R(1-q)] <= P(A) <= Rq/[1-q+Rq].

The same result follows after any common positive propagation, because it
does not increase the certified projective spread. If interval arithmetic
encloses q, monotonicity allows its lower endpoint in the lower formula and
its upper endpoint in the upper formula.

`cooperative_gate_queries.py` consumes the retained count-conditioned laws
and evaluates the event that all 24 modules are active at a selected later
time. It uses the exact local unobserved propagation

    p_i(t) = alpha_i/r_i
               + (p_i(0)-alpha_i/r_i) exp(-r_i*t),
    r_i = alpha_i+beta_i+kappa_i,

inside each positive mixture component. No preparation acquisition or count
filter is repeated. Immediately after the baseline count record the
all-active probability is enclosed by

    [3.4019514859289284070e-16,
     3.4019514985478335619e-16].

The upper/lower ratio minus one is below 3.710e-9. This is also the
instantaneous hazard divided by its specified rate constant for a candidate
reaction enabled only by the all-active guard. Activating that new reaction
over a finite future interval would change the dynamics and introduce
coupled killing. The present calculation is not its first-passage law.

## Primary references for established mathematical machinery

- Francois Le Gland and Nadia Oudjane, *Stability and uniform approximation of
  nonlinear filters using the Hilbert metric and application to particle
  filters*, Annals of Applied Probability 14(1), 144-187, 2004.
  DOI: https://doi.org/10.1214/aoap/1075828050
  Publisher: https://projecteuclid.org/journals/annals-of-applied-probability/volume-14/issue-1/Stability-and-uniform-approximation-of-nonlinear-filters-using-the-Hilbert/10.1214/aoap/1075828050.full
  Accessible copy of the published primary text:
  https://scispace.com/pdf/stability-and-uniform-approximation-of-nonlinear-filters-5cqc16nut7.pdf
- Samuel N. Cohen and Eliana Fausti, *Hyperbolic contractivity and the Hilbert
  metric on probability measures*, arXiv:2309.02413v2, revised November 2024.
  Theorem 5.1 and Corollary 5.2.1 concern the sharp TV comparison.
  https://arxiv.org/abs/2309.02413v2
  https://arxiv.org/html/2309.02413v2
- Marcel F. Neuts, *Descriptors for point processes based on runs: the
  Markovian arrival process*, Journal of Applied Mathematics and Stochastic
  Analysis 9(4), 469-488, 1996. Section 3 gives the local count equations and
  their matrix generating function.
  Primary article PDF: https://pdfs.semanticscholar.org/25f8/b5fa0e13149824f259a97c8ef0a807a45187.pdf

