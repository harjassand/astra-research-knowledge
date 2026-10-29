# Independent review: entropy-tight completion in a record closure

29 October 2026. Root proposed the common-duration-bin Erlang-channel
construction. The relaxed equality is valid under the explicit assumptions
below. Exact finite attainment is more restricted than exact finite
realizability of a common-Erlang-mixture record. This note supplies the
distinction, the endpoint-parity accounting, and an L1 convergence route.

## 1. Statement with the necessary scope

There are finitely many resolved singleton ports B, fixed individually by
physical reversal. Their weights w_i>0 and escape rates lambda_i>0 are
specified. Direct port flux d_ij is nonnegative for i!=j and d_ii=0.
Positive-duration excursion flux has density K_ij(t), t>0. Assume

    rho_i=w_i lambda_i=sum_j[d_ij+integral K_ij(t)dt]
         =sum_j[d_ji+integral K_ji(t)dt],
    R=sum_i rho_i<infinity,
    V=sum_ij integral t K_ij(t)dt<infinity,

and reciprocal support with finite

    J(K,d)=sum_ij integral K_ij log(K_ij/K_ji)
           +sum_(i!=j) d_ij log(d_ij/d_ji).

Terms with both arguments zero vanish. If irreducible microscopic
realizations are required, the positive port-flow graph must be connected
(equivalently strongly connected under reciprocal support). Otherwise the
construction can be reducible. A zero-duration self-event is not an
ordinary CTMC self-jump and is not included among the direct atoms.

Consider finite CTMC realizations with arbitrary hidden parity and
unrestricted hidden state counts/rates, preserving w_B, direct d, all
port clocks and total hidden mass V. Let their native K_n converge to K
in sum_ij integral (1+t)|K_n,ij-K_ij|dt. The infimum of limiting intrinsic
generalized path entropy rates, in the unnormalized flux units below, is

    E_relaxed(K,d)=J(K,d).

This is a statement about a closure of records. It is not a claim that
every exact record has a finite realization attaining J, nor that the
required density, moments, parity or preparation interface has been
acquired. State and clock resources diverge in the general approximation.

## 2. The intrinsic rate and the stationary boundary term

Let Q be a finite stationary CTMC with positive weights w and W=sum w,
pi=w/W. Theta is an involution fixing ports, with no assumption that
pi_Theta(x)=pi_x. Compare its stationary microscopic path law over [0,T]
with the pushforward under time reversal followed by Theta. Exactly,

    D(P_[0,T] || Theta Reverse P_[0,T])
      =D(pi || pi_Theta)+T E/W,

where

    E=sum_(x!=y) w_x q_xy log[q_xy/q_Theta(y),Theta(x)]
      +sum_x w_x[lambda_Theta(x)-lambda_x].                  (1)

The endpoint expectation gives D(pi||pi_Theta). Stationarity gives the
jump and holding terms in (1). The same rate is obtained by the usual
relative-entropy-rate formula against the parity-conjugated stationary
reverse generator. It is nonnegative.

If pi is not parity invariant, the simpler sum of stationary edge-flux
log ratios f_xy/f_Theta(y),Theta(x) is generally NOT (1). That expression
can count extra entropy once for every phase. The construction must use
the path rate, rather than importing an all-even flux identity.

D(pi||pi_Theta) is a stationary boundary information term. Calling it a
literal physical preparation work would need an additional thermodynamic
resource model. It can be nonzero or large even when the intrinsic rate
has already been accounted for correctly.

## 3. Native regeneration removes that boundary term from excursion KL

Let mu be the finite measure on complete microscopic excursions from a
port departure to the first subsequent port arrival, with direct port
jumps as zero-duration atoms. Its entry flux is w_i q_ix, not a freely
chosen hidden preparation. Its total mass is R. Let mu^R be its reversal
with Theta applied to hidden states. Then

    D_flux(mu || mu^R)=integral log(dmu/dmu^R) dmu=E.          (2)

**Proof.** A path from i through a hidden itinerary to j has log ratio

    log(w_i/w_j)
      +sum_edges log[q_xy/q_Theta(y),Theta(x)]
      +integral_hidden [lambda_Theta(X_t)-lambda_X_t]dt.

Native entrance and exit masses at each port are both rho_i, so the port
gradient averages to zero. Integrated hidden occupation under mu equals
w_I: stationarity gives

    w_B Q_BI(-Q_II)^-1=w_I.

Consequently all hidden-edge counts have their stationary flux values.
Boundary/direct edges have those values by definition. Ports are fixed
under Theta, so their omitted holding contribution is zero. Averaging
therefore gives (1). No parity symmetry of w was used.

After normalization, E/R is the KL per native excursion. Independent
trials can realize mu/R by selecting the starting port with probability
rho_i/R, preparing that known singleton port, and observing its next
native excursion. Its initial port hold may be timed for cost accounting,
but must not be naively reversed as though a start-port hold were an
end-port hold. The entropy calculation concerns the excursion record.
The average complete trial time, including the port hold, is W/R.

An uninterrupted stationary sequence gives the same intrinsic rate by
regeneration. The equation does not waive the operational cost of port
resets, flux-weighted start selection, timing, or acquiring w_B/lambda_B.
It does avoid postulating a preparation of the asymmetric hidden pi.

Projecting mu to (i,j,t), including direct atoms, gives K and d. Data
processing applied to (2) establishes E>=J(K,d) for every completion,
whatever the hidden parity or state count.

## 4. Finite channel construction and exact resource identities

Take a finite common partition (I_k) of (0,infinity), including lower and
upper tail bins. Put

    a_ij,k=integral_(I_k) K_ij(t)dt,
    A_k=sum_ij a_ij,k,
    c_k=[sum_ij integral_(I_k) t K_ij(t)dt]/A_k.

Omit bins with A_k=0. Every retained c_k is positive and finite. Choose
an integer n>=1. For every positive a_ij,k add a distinct n-stage directed
chain from port i to port j. Its entrance rate is a_ij,k/w_i; all stage
rates are r_k=n/c_k; each stage weight is a_ij,k/r_k. Keep direct rate
d_ij/w_i. This includes i=j hidden return chains.

The phase weights solve stationarity on each chain, and port balance
holds by the assumed native flow balance. Port clocks are exactly the
specified lambda_i. The total hidden mass is exactly

    sum_ij,k n a_ij,k/r_k=sum_k A_k c_k=V.

Hence W=sum_B w_i+V and the total mean trial duration are preserved
exactly at every approximation stage. Pairwise mean durations need not
be exact at finite stage, but converge in the weighted L1 topology.

Pair each i->j chain with its j->i counterpart, reversing phase order
under Theta. For self-return chains, reverse the phase order within the
same chain. Pairing is possible by reciprocal support. Both paired
stages have escape rate r_k, although their stationary weights may differ.

For one forward channel, the entrance and exit rate ratios telescope to

    (a_ij,k/a_ji,k)(w_j/w_i).

The internal stage rate ratios equal one. Direct-edge ratios are
(d_ij/d_ji)(w_j/w_i). The port gradients cancel after summation by native
flow balance, and all holding-rate differences vanish. Therefore

    E_n= sum_ij,k a_ij,k log(a_ij,k/a_ji,k)
          +sumdirect d_ij log(d_ij/d_ji).                    (3)

Log-sum gives E_n<=J(K,d). The realized native kernel is exactly

    K_n,ij(t)=sum_k a_ij,k g_(n,c_k)(t),

where g_(n,c) is the Gamma/Erlang density with shape n and mean c.

The stationary boundary term is explicitly

    D(pi_n||pi_n,Theta)
       =(1/W) sum_ij,k a_ij,k c_k log(a_ij,k/a_ji,k).          (4)

It must not be silently dropped from a stationary fixed-horizon path KL.
It is absent from the intrinsic-rate and native-excursion identities.

## 5. Weighted L1 convergence: order of approximation matters

Making the gamma stages arbitrarily sharp before making bins sufficiently
fine can fail L1 convergence: separated narrow spikes can converge weakly
to a density while retaining almost maximal L1 error. A valid construction
uses log-bin mesh delta_n with sqrt(n) delta_n -> 0.

First define the continuous gamma smoothing operator

    (S_n f)(t)=integral f(s) g_(n,s)(t)ds.

If Y_n has Gamma(n,rate n) law, then

    S_n f(t)=E[Y_n^-1 f(t/Y_n)].

Since Y_n->1 and E Y_n=1, strong continuity of dilations in
L1((1+t)dt), first for compact continuous functions and then by density,
gives ||S_n f-f||_(1+t)->0 for every f in that space. Uniform
integrability of 1+Y_n follows from E Y_n^2=1+1/n.

Now replace s within each finite log bin by the common c_k. The mean c_k
lies inside that bin. If |log(c/s)|<=delta, the gamma KL formula and
Pinsker give

    ||g_(n,c)-g_(n,s)||_1 <= sqrt(n) delta exp(delta/2).

Also t g_(n,c)(t)=c h_(n+1,c)(t), where h has shape n+1 and rate n/c.
The same inequality yields

    integral t |g_(n,c)-g_(n,s)|dt
       <=s[exp(delta)-1+sqrt(n+1) delta exp(delta/2)].

Integrating these bounds against all K_ij(s) controls the finite-bin
quantization error by its total mass and first moment. Lower/upper tails
can be replaced by their common conditional means: the total weighted
L1 error there is at most twice the target tail mass plus first moment,
because both the smoothing and the replacement preserve those aggregate
quantities. Choose the tails so that this bound tends to zero.

Therefore a diagonal sequence with n->infinity, shrinking log mesh as
above, and vanishing weighted tails gives

    sum_ij ||K_n,ij-K_ij||_(1+t) -> 0.

Finite partitions suffice at each stage. Nested partitions may be used
if monotonically increasing bin KL is desired, but monotonicity is not
needed for the final entropy conclusion.

## 6. Closing the entropy bounds

Let J_n=J(K_n,d). Microscopic data processing and (3) give

    J_n <= E_n <= J(K,d).

Relative entropy is lower semicontinuous under L1 convergence of both
finite measures with their common total mass. It follows that

    J(K,d) <= liminf J_n <= liminf E_n <= J(K,d).

Thus J_n and E_n both converge to J. Conversely, every approximating
sequence of completions has E_n>=J_n, so lower semicontinuity gives
liminf E_n>=J. This proves the stated relaxed equality.

No numerical entropy optimizer is used to establish the theorem. The
construction is information-theoretic: its a_ij,k and c_k require exact
record integrals. It establishes neither their finite-data acquisition
nor a favorable state, clock, precision or preparation cost.

## 7. Exact finite attainment is strictly more restrictive

Realizing a common-Erlang-mixture record exactly by distinct component
channels does NOT generally attain its observed J. The microscopic path
reveals the component k. Positive Erlang components overlap at every
t>0, so observing duration does not determine that component. Equality
in data processing requires the forward/backward component ratio to be
the same across all overlapping components for each pair.

A concrete two-port example is

    K_12(t)=3 exp(-t)+2 exp(-2t),
    K_21(t)=exp(-t)+6 exp(-2t).

Each row mass is four, so w_B=(1,1), lambda_B=(4,4), and d=0 are balanced.
Four one-phase channels realize this record exactly: component masses
(3,1) forward and (1,3) backward, with means (1,1/2). Their hidden mass is
six. The construction has

    E_components=4 log 3,

whereas direct integration of the observed record gives

    J=-8/3+(15/2)log(5/3)-(7/18)log 7 < 4 log 3.

The integral follows by substituting x=exp(-t):
J=integral_0^1 (2-4x)log[(3+2x)/(1+6x)]dx.

### Necessary shape of an exactly entropy-tight finite record

**Theorem 2.** If a finite CTMC completion with finite E attains E=J,
then for every nonzero positive-duration endpoint pair,

    K_ij(t)/K_ji(t)=C_ij exp(delta_ij t)                    (5)

for almost every t>0. Finite CTMC kernels are analytic there, so the
identity extends wherever the pair is positive.

**Proof.** Equality in data processing makes the microscopic excursion
likelihood ratio measurable from (i,j,t). Fix one positive-rate hidden
itinerary Gamma=(i,x_1,...,x_l,j). Its ratio is

    C_Gamma exp{sum_(r=1)^l [lambda_Theta(x_r)-lambda_x_r] s_r},

with s_r>0 the hidden holding times. Conditional on sum s_r=t, the dwell
vector has positive density over the full simplex. Hence the coefficients
of all s_r along this itinerary must be equal, and the ratio is
C_Gamma exp(delta_Gamma t). Every such finite itinerary has positive
duration density at every t>0. Therefore all itineraries for the same
endpoint pair must give the same exponential function, proving (5).
For one-stage itineraries the simplex step is automatic. Lack of a
parity-reversed itinerary would instead make E infinite.

The displayed common-mixture example has a non-exponential ratio, so NO
finite completion can attain J for that exact record, even though the
record has a finite six-state realization and its relaxed infimum is J.
This is a genuine finite-versus-closure distinction, not merely a defect
of one chosen Erlang construction.

The companion `EXACT_ATTAINMENT_CLASSIFICATION.md` completes the
sufficiency argument for finite phase-type pair laws using reversed
phase-type channels and an exponential h-transform. At that scope,
exponential pair ratios are an if-and-only-if condition for exact finite
attainment of J. This does not classify exact-record infima when no
finite model attains them.

## 8. Finite mean and finite J do not uniformly control the boundary term

For general density records, the two assumptions in Section 1 need not
bound (4) as partitions are refined. For example, on disjoint unit bins
[2^k,2^k+1], take forward mass a_k=2^(-3k), reverse mass
b_k=a_k exp(-4^k). The mean sum (a_k+b_k)(2^k+1/2) is finite, and the
event KL sum (a_k-b_k)4^k is finite. But the duration-weighted KL sum
(a_k-b_k)(2^k+1/2)4^k diverges. Finite positive direct fluxes can balance
the two total port flows without changing these conclusions.

This record need not itself have a finite CTMC realization. It shows why
the stated finite-mean/finite-J hypotheses do not justify a uniform
stationary microscopic preparation bound in the general closure theorem.
The intrinsic-rate conclusion and the native-port excursion identity
remain valid.

## 9. Stronger obstruction: exact finite cost can be infinite

Root supplied the following sharper example, independently confirmed here:

    K_12(t)=exp(-t),       K_21(t)=t exp(-t),
    d=0,  w_B=(1,1),      F_12=F_21=1,
    V=3,  W=5,  R=2.

The target has a five-state finite CTMC realization: the unit-rate directed
cycle port 1 -> hidden a -> port 2 -> hidden b -> hidden c -> port 1.
All five stationary weights equal one. Its native kernels are respectively
one- and two-phase unit-rate Erlang laws. Their observed event KL is

    J=integral_0^infinity exp(-t)(1-t)(-log t)dt
      =-Gamma'(1)+Gamma'(2)=1.

Nevertheless every exact finite CTMC completion fixing both ports under
Theta has E=infinity. Finite E requires positive-rate support to be
preserved by the reversed parity map: q_xy>0 implies
q_Theta(y),Theta(x)>0. Since K_12(0)=1, there must be a hidden state x
with q_1x q_x2>0. The two reversed edges then give
q_2,Theta(x) q_Theta(x),1>0, forcing K_21(0)>0. This contradicts
K_21(t)=t exp(-t).

More generally, finite E forces equal shortest hidden path lengths in
opposite directions. If the shortest i->j excursion uses l hidden states,
then K_ij(t) has a positive leading coefficient of order t^(l-1) at zero.
Parity reversal preserves the number of states on each itinerary, so the
opposite shortest path has the same length. This follows directly from
the first nonzero term in F_BI exp(Q_II t) Q_IB: at the shortest order only
positive off-diagonal hidden path products contribute; diagonal terms
cannot create a shorter connection.

The closure construction still preserves all listed weights, endpoint
masses, clocks and total mean, with weighted L1 convergence and E_n->1.
Thus the exact-record infimum is infinity while the relaxed intrinsic
floor is finite. Per physical time the latter is 1/5, and per native
departure it is 1/2, using the preserved W and R.

This is about exact structural information at zero duration. Finite
precision observations do not establish an identically absent one-phase
route or an exact zero Taylor coefficient. Nor does this ideal directed
cycle establish physically infinite heat in a laboratory source.

## 10. Review of root's Sections 3–4

`../ENTROPY_COMPLETION_CONVERSE.md` was read after its ordinary proof was
saved. Its choice n_m=2^m, logarithmic mesh delta_m=2^-m, and tail cutoffs
exp(-m), exp(m) has sqrt(n_m)delta_m=2^(-m/2)->0, so it repairs the spike
failure. The partitions are nested: integer endpoints and the previous
dyadic grid lie on the next grid. They generate the Borel duration
sigma-algebra. Aggregate bin means, including tails, preserve total V
exactly. The weighted L1 contraction of continuous gamma smoothing is
valid because its kernel preserves both mass and first moment.

The tail quantization estimate is valid after summing over endpoint
pairs; it should not be read as preserving each pair's first moment
separately. Total variation convergence of event measures and their
reversals follows from the unweighted part of the asserted weighted L1
convergence; their total mass R is fixed. Relative-entropy lower
semicontinuity therefore applies. Trace irreducibility ensures all new
hidden phases communicate through the retained ports.

No remaining substantive gap was found in those two sections. A harmless
degenerate case should be stated: assume R>0 for all per-departure and
mean-cycle expressions, or treat the single constant-port zero-event
process separately. Irreducibility already guarantees positive rho_i
when there is more than one port.
