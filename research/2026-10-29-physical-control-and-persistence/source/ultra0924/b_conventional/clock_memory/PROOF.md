# Local multi-time Gaussian MEMORY faults around an exact fresh-block process

29 October 2026. Completed mathematical construction; parent has whole-read
the main proof. Broader coherent-fault/decoder admission remains under the
parent's separate investigation and is not claimed here. No new
Hamiltonian case, dynamics, reservoir table or physical action is executed.
The earlier clock_controller packet remains frozen. This proof does not assume
that physical bath reuse is an ideal Markovian controller.

## 1. What is compared

Let a system, possibly including arbitrary finite reference and coherent control
registers, have an arbitrary time-dependent self-adjoint H_S(t). Let bounded
Hermitian operators A_j(t), ||A_j(t)||<=1, couple to independent centered Gaussian
baths through alpha sum_j A_j(t) tensor B_j(t). Their free interaction-picture
correlations are

    <B_j(t)B_l(s)>=delta_jl C_j(t,s).

Assume bosonic Wick, a factorized initial system/bath state, and bounded C_j on
each finite time square. Gaussian thermal passive chains/continua satisfy these
assumptions. B_j themselves may be unbounded. The joint unitary and the usual
Dyson/Wick expansions are assumed well defined; bounded correlations justify
absolute convergence on every finite horizon. No control-dependent Gaussian
state of the EVOLVED bath is assumed.

Partition each bath's use into consecutive time intervals I_k, possibly with
different durations. A slot v=(j,k) is one specified seed used in interval I_k.
There are finitely many slots V on any chosen finite horizon. Discontinuous
switching is allowed in the ideal mathematical comparison; finite ramps have
their own implementation budget. For the actual clock apparatus A_j is the
known constant-body prefix pullback, not an unqualified physical onsite seed.

For K subset V define a PHYSICAL Gaussian process C[K]: slots in K use the
same original bath j across their intervals, while EVERY slot outside K uses
its OWN independent Gaussian copy. Within each slot the correlation is exactly
unchanged. Cross-slot covariance survives precisely when both endpoints belong
to K (and have the same j). This construction preserves positivity AND the
quantum commutator kernel: it is realized by actual independent oscillator
copies with time-dependent switching, not by declaring an arbitrary covariance
mask positive. Let Phi[K] be its reduced multi-time process, including any
specified system interventions and all their unnormalized records.

The norm used below is the supremum of the final output trace norm after
inserting any common causal sequence of CPTP system interventions, with
arbitrary finite ancillas and complete classical records. Equivalently test
with Hermitian final O of norm<=1 and include inert references. No conditional
postselected state is normalized. This convention fixes any factor-of-two
distinction between trace norm and measurement bias. The maps are Hermiticity
preserving; the usual ancilla Hermitianization extends the bound from states
to the corresponding complete linear-map norm.

Thus Phi[V] is the actual reused-bath process. Phi[empty] is the EXACT fresh-
bath-per-slot process. The reference includes all nonperturbative interactions
within a slot. It is not the KMS generator, a zero-coupling unitary, or a claim
that resetting the system resets its bath. In particular alpha^2 |I_k| need
not be small. The reference's microscopic reset/ancilla costs are separate.

## 2. A consistent fault expansion

Define linear process maps, indexed by the set of faulty slots, by Mobius
inversion:

    F_M=sum_(K subset M) (-1)^(|M|-|K|) Phi[K].          (1)

Then

    Phi[V]=sum_(M subset V) F_M,  F_empty=Phi[empty].

For R subset V the inclusive bad-set sum has the simpler form

    Bad(R):=sum_(M superset R) F_M
           =sum_(T subset R) (-1)^|T| Phi[V\T].         (2)

Indeed the coefficient of Phi[K] on the first side is zero unless
V\R subset K, in which case it is (-1)^(|V|-|K|). These are algebraic
identities for the same consistent F_M, not separately chosen errors for
each query R. F_M need not be CP or positive. Claiming positive CPTP fault
flags from(1) would be a substantive extra step and is NOT done here.

There is also a fault-location interpretation. Expand around the fully fresh
Gaussian kernel. Only cross-slot Wick pairs differ. Mobius inversion selects
exactly those diagrams whose cross-pair endpoint-slot union is M. All other
slots execute their exact fresh-bath dynamics, with the same ideal H_S(t).
The insertions marking a faulty slot are the bounded A_j at times inside that
slot. They are local in the physical source support of A_j. Propagation by
the intended H_S is retained, not misidentified as instantaneous local error.

## 3. The resummation that avoids a global-time prefactor

Use the rigorous Gaussian correlation-variation identity of Liu--Lu,
arXiv2408.04009v3, Lemma1, with its multi-index/time-dependent extension given
here explicitly. Fix R, and use C[V\R] as the common reference. It is physical:
the unmarked slots share their original baths; the marked slots have individual
independent bath copies. For every T subset R,

    C[V\T]-C[V\R]

contains only cross-slot correlations incident on R, and omits pairs touching T.
Expand each Phi[V\T] around this SAME physical reference. Each difference pair
is a scalar correlation times two bounded system insertions on the unfolded
forward/backward contour. ALL reference pairs resum into the FULL reference
joint-unitary propagators between insertions. Their norm is1. Thus their number
or the duration/strength of the reference process introduces no prefactor.

For completeness, this identity follows by expanding each Gaussian pair in
the exact Wick series as C_reference+delta C. Select which pairs are delta C,
sum every remaining reference pair and insertion into the exact reference
Dyson propagators, and retain the selected pair endpoints as A_j insertions.
Each original pairing has exactly one such colored decomposition. All series
are absolutely convergent for fixed finite |V| and horizon, so the interchanges
are legitimate. This is the combinatorial argument of the primary Lemma1;
multiple bath indices and time-dependent A_j only add bounded labels to each
endpoint. Piecewise-switched copies change the correlation kernel but not the
argument. The resummed propagator remains time-ordered unitary.

Sum with signs over T in(2). A chosen family of delta pairs survives iff its
endpoint slots cover every vertex of R. Otherwise a missing vertex's two
inclusion--exclusion terms cancel. Reference pairs are NEVER marked. This
last distinction is essential: bounding all bath insertions as faults would
throw away the strong useful within-block relaxation.

Let unordered distinct-slot edges have weights

    w_vw=8 alpha^2 integral_(I_v)dt integral_(I_w)ds
                      |C_j(t,s)|,                     (3)

when their seed j agrees, and zero otherwise. The factor8 overpays the four
forward/backward branch choices and unordered-pair convention. Define

    eta=sup_v sum_(w!=v) w_vw.                          (4)

The sum of absolute weights of k selected delta pairs incident on R is at
most (|R| eta)^k/k!: each edge touches R, their total unordered-edge mass is
at most |R|eta, and pair permutations give the exponential-series factor.
Repeated edges are allowed and already paid. There is no constraint of
connectedness and no unproved single-polymer-to-multi-polymer conversion.

In testing the process with a norm-one final observable, the resummed full
reference unitary and all A_j insertions have operator norm<=1. This also
holds with arbitrary inert references and deferred measurements/feedback:
include their Stinespring unitaries and coherent classical records as system
registers. Outcomes are NOT renormalized by postselection. The scalar integral
majorant therefore bounds the corresponding complete trace/strategy norm.

## 4. Horizon-free local coherent noise condition

Put r=|R|. Covering R by pairs requires at least ceil(r/2) selected pairs.
Consequently

    ||Bad(R)||_strategy
       <=sum_(k>=ceil(r/2)) (r eta)^k/k!.               (5)

For eta<=1/2 choose z=1/(2eta)>=1 and multiply the series by the Chernoff
majorant z^(k-r/2). This gives

    ||Bad(R)||_strategy <=(2e eta)^(r/2).                (6)

For eta=0 take the continuous limit. One may replace2e by6 and require
eta<=1/6. This is a local coherent SUPEROPERATOR fault condition around the
exact fresh reference, with strength epsilon_mem=sqrt(2e eta). It is neither
a probability per slot nor a demonstrated CPTP flag distribution. The shape
of the marked slots is physical seed-support times time interval. Translating
to individual qubits must retain constant body size/overlap and the possibility
that one pair marks two slots; no single-site exponent is silently claimed.

Equation(6) is uniform over the number of clocks and the elapsed time, provided
(4) is uniform. It concerns every finite experiment/strategy, not an exchange
of the thermodynamic and infinite-time limits. It compares multi-time processes,
not merely one final density matrix. It does not assert that their global
trace distance remains small for arbitrarily long storage.

## 5. The actual compact-band continuum pays eta

For stationary Hermitian bath variables C_j(t,s)=C_j(t-s), |C_j(-u)|=|C_j(u)|.
For I=[a,a+ell], correlations with both past and future obey

    integral_I dt integral_(outside I)ds |C_j(t-s)|
          <=2 integral_0^infty u |C_j(u)| du.

This follows by fixing u>0: the allowed crossing positions have length at
most min(ell,u), separately on each side. Thus

    eta<=8alpha^2 sup_j integral_R |u C_j(u)|du.         (7)

This bound is independent of ell as well as total horizon. The fixed passive
band spectrum in frozen clock_controller has an explicit A_B satisfying

    integral_R |u C_j(u)|du<=32 A_B^2.

Therefore eta<=256 alpha^2 A_B^2. A specified coherent slot-error threshold
epsilon_0 is met, for example, by the completely scalar fixed-coupling gate

    alpha<=epsilon_0/(40 A_B),  epsilon_0<=1,             (8)

because 6*256/1600<1. This alpha depends on temperature/desired local budget,
but NOT on system size, total time or chosen block duration. Unlike treating
the whole bath as noise, the gate remains small while alpha^2 ell is order1.
No native value or physical rate has been evaluated in this assignment.

The independent analytic sharpening in TEMPERATURE_UNIFORM.md replaces
A_B by A_0=4C_B, uniformly for every b>=1. Thus even the bath coupling in
this MEMORY gate may be chosen temperature-independent. This is not a
uniform-coupling bare-KMS-controller approximation.

## 6. Strong prior and exact remaining admission gates

Ng--Preskill, arXiv0810.4953, Eq27, already bounds Gaussian NON-MARKOVIAN
Hamiltonian noise using a local double integral of the full correlation.
Our raw compact-band bath is admitted there relative to a closed-system
ideal circuit. That is an important ordinary incumbent, not a new result.
It does not keep the bath's beneficial within-slot relaxation as ideal.
Liu--Lu's exact variation resummation is the ordinary input enabling that
different reference here. The local Mobius coverage receiver is spelled out
rather than inferring it from their global exp(total kernel error) bound.
Historical novelty is UNKNOWN and not claimed.

Three further bridges are NOT inferred:

1. The exact fresh-block reference must itself implement the desired controller
   with an admitted local error. The frozen Scandi global preparation theorem
   is not automatically a local multi-time KMS-controller comparison.
2. A decoder needing positive CPTP fault flags cannot be given the signed
   coherent maps(1) for free. Its particular coherent-admission theorem must
   actually accept the norm condition(6), including slot size/causality.
3. The continuum is an unlimited reservoir. Finite closed banks do not have
   an all-time L1 correlation bound. FINITE_BANKS.md proves the precise
   obstruction and gives a local-epoch replacement with explicit renewal
   resource costs. System reset is not bath reset.

This is therefore a paid local multi-time MEMORY interface for a genuine
Gaussian physical model, not yet an accepted fixed-noise long-storage theorem
for the native code or a bounded-density3D controller.
