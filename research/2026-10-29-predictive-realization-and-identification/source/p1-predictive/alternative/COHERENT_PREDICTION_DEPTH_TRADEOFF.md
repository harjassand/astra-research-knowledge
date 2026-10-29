# A depth–precision tradeoff with a uniformly conditioned predictive core

29 October 2026, Brisbane. Independent alternative-opening construction.

## Scientific role

An alternative to macroscopic-transition prediction is a reusable learned
predictive process that answers arbitrary future legal intervention programs
without identifying its physical hidden state. This is a consequential
positive direction, already supported by predictive-state and hidden-quantum-
Markov-model theory, and by current Astra N1148/N1166. It is not a new idea
merely because its coordinates are observable probabilities.

The following ordinary theorem isolates a resource that a finite, well-
conditioned predictive core does **not** supply: the precision needed by a
later coherent consequence. The example has no rare activation, hidden slow
classical state, unknown graph, ill-conditioned short core, or large physical
dimension. Strong conventional inference achieves the resulting order. A
change in legal experimental depth removes the apparent difficulty. This is
an information/access test of the alternative, not a new quantum-metrology
speedup or a claim of historical novelty.

## 1. Declared legal interface

Each independent episode starts in the qubit state |0>. The legal primitive
R_theta is rotation through angle theta about the y axis. A terminal Z test
reports 1 with probability

    p_k(theta) = (1 - cos(k theta))/2

after k primitive calls. The k=0 test is legal. The trace test always returns
one. Each episode's k may be chosen from earlier episode outcomes, including
private classical randomization. It must satisfy 0 <= k <= L. The unknown
source is one of two explicitly supplied possibilities; the learner knows
both possibilities, not which one is used. Independent whole-process starts
and access to the unitary rotation are supplied operations. No coherent
control beyond repeated R_theta, no cross-episode quantum memory, and no
intermediate measurement library are assumed.

For any H divisible by four with H >=128, put

    theta_0 = pi/2,        theta_1 = pi/2 + pi/H.

The future query is the same terminal outcome after H primitive calls.
Exactly,

    p_H(theta_0)=0,        p_H(theta_1)=1.                 (1)

There is no rare-event waiting time in this query.

## 2. Full observable dimension is three; a normalized core stays conditioned

Every normalized state after k calls is represented by

    v_k=(1, cos(k theta), sin(k theta)).

The native action rotates the last two coordinates. Every terminal test is
a linear functional of these three coordinates. Thus the entire declared
observable process has rank at most three. Use the three legal normalized
preparations R^i|0>, i=0,1,2, and the three tests: trace, terminal test now,
and terminal test after one more R. Their probability matrix is

    A(theta) = [[1,1,1],
                [p_0,p_1,p_2],
                [p_1,p_2,p_3]].

At theta_0 this is

    A_0 = [[1,1,1], [0,1/2,1], [1/2,1,1/2]],
    det A_0=-1/2,
    A_0^(-1)=[[3/2,-1,-1],[-1,0,2],[1/2,1,-1]].

Consequently ||A_0^(-1)||_infinity=7/2. Since |p_j'|<=j/2,

    ||A(theta_1)-A_0||_infinity <=3 pi/H.

Using pi<22/7 gives

    ||A_0^(-1)[A(theta_1)-A_0]||_infinity <33/H <=33/128.

The Neumann bound therefore proves

    ||A(theta_1)^(-1)||_infinity < (7/2)/(1-33/128)
                                 =448/95 <4.716.         (2)

Both full ranks are exactly three. This is not a finite numerical rank test:
the coordinate realization is an upper bound and the invertible legal core
is the matching lower bound. The probability core is normalized and contains
the trace row, as required by the relevant Astra constructions.

## 3. Adaptive short-episode lower bound

Let an algorithm use at most Q independently reset episodes, of adaptively
chosen depths k<=L. Suppose its estimate of the H-step probability has error
strictly less than 1/4 with probability at least 1-alpha in **both** sources,
where 0<alpha<1/2. Then

    Q >= 4(1-2 alpha)^2 H^2 / (pi^2 L^2).                 (3)

The claim is nontrivial for L>=1; L=0 supplies no source information.

### Proof

Write delta=theta_1-theta_0=pi/H. For one k-call episode the square-root
probability vectors are the absolute-value components of the two real qubit
amplitudes. Their Bhattacharyya affinity is therefore

    f_k = sqrt(p_k(theta_0)p_k(theta_1))
        + sqrt((1-p_k(theta_0))(1-p_k(theta_1)))
        >= |cos(k delta/2)|
        >= 1-k^2 delta^2/8.

The last inequality holds even when its right-hand side is negative. In the
useful regime L delta is small, it is a positive bound. Conditional on any
common classical history, the algorithm selects the same distribution over
its next experiment in the two models. A private random seed may be included
in the transcript and then averaged. Iterating conditional affinities yields

    F(P_0,P_1) >= (1-L^2 delta^2/8)^Q
               >= 1-Q L^2 delta^2/8

when L^2 delta^2/8<=1. If the final lower bound is negative it is simply
unused. For classical laws, Cauchy–Schwarz gives

    TV(P_0,P_1) <= sqrt(1-F(P_0,P_1)^2)
                <= min(1, delta L sqrt(Q)/2).             (4)

Indeed, write |P-Q|=|sqrt(P)-sqrt(Q)|(sqrt(P)+sqrt(Q)) and
sum; the two squared sums are 2-2F and 2+2F. Whenever the right-hand
nontrivial estimate would exceed one, the trivial TV<=1 gives (4).

By (1), thresholding the returned prediction at 1/2 distinguishes the two
sources with each error probability at most alpha. Hence
TV(P_0,P_1)>=1-2 alpha. Combine this with (4) to prove (3). QED.

The same proof also permits arbitrary terminal POVMs separately chosen for
each episode: measurement cannot reduce the affinity below the pure-state
overlap. That extension does not permit a coherent quantum connection
between episodes, nor a richer uncontrolled primitive library.

## 4. Total native-call form

If every acquisition path makes at most C native rotation calls and each
episode has depth at most L, then

    C >= 4(1-2 alpha)^2 H^2 / (pi^2 L).                    (5)

For completeness, at a node h of the adaptive acquisition tree the affinity
loss is its weight sqrt(P_0(h)P_1(h)) times (1-f_k). Summing node losses is
an exact telescoping expression for 1-F of the leaf laws. Bound
sqrt(P_0(h)P_1(h)) by [P_0(h)+P_1(h)]/2. Thus

    1-F <= delta^2/16 [ E_0 sum k^2 + E_1 sum k^2 ]
         <= delta^2 L C/8,

since sum k^2<=L sum k<=LC on each path. Apply the previous TV bound.
Zero-depth episodes add no information and can be omitted; finitely many
positive-depth episodes follow from the hard cost cap. Variable-length or
stopped algorithms are therefore covered at this stated pathwise budget.

## 5. An equally informed conventional method matches the order

Assume H>=4L. Choose the largest positive odd k<=L. Then k>=L/2, except
the harmless L=1 case where k=L. At theta_0, p_k=1/2. The absolute difference
between the two known Bernoulli probabilities is

    Delta_k = sin(k pi/H)/2 >= k/H,

using sin(x)>=2x/pi on [0,pi/2]. Repeat this ordinary experiment Q times
and compare the empirical frequency with the midpoint between the two known
probabilities (reverse the inequality when k mod4 changes the sign).
Hoeffding gives a failure probability at most

    exp(-Q Delta_k^2/2) <= exp(-Q k^2/(2H^2)).

Thus Q>=2H^2 k^(-2) log(1/alpha) suffices. For fixed confidence this matches
(3) in order. It is a one-parameter binary-hypothesis test, requiring no
predictive model construction, gauge search or hidden-state identification.
The classical learner can also propagate a three-dimensional rotation
representation if many future queries are desired; neither its rank nor its
arithmetic is a unique Astra advantage.

If the legal acquisition depth is changed to L=H, **one** H-step experiment
distinguishes the two sources exactly by (1), at cost H native calls. Rarity
and the printed H do not create intrinsic hardness; legal access determines
the tradeoff. This is the ordinary coherent-interrogation resource known in
phase estimation, not a proposed new physical operation.

## 6. Executable control and its exact scope

`coherent_prediction_depth_tradeoff.py` checks the rational inverse and
conditioning constants, the target parity identities, the affinity bound
in ordinary floating diagnostic arithmetic, and the predicted scaling over
several H,L.
It executes one small synthetic two-source comparison with H=128,L=15 and
Q=ceil(16 H^2/k^2) per source. It stores individual pseudorandom outcome bits,
counts and hashes. Each binary trial is actually generated; native-call and
whole-start costs are charged rather than inferred from Python runtime.

The executable source uses a 53-bit integer Bernoulli threshold. Exact
rational Machin and sine-series intervals prove its floor is the floor of
the ideal probability, with rounding error below 2^-53. The gap budget is much
larger; a conservative lower separation k/H-2^-52 is checked against the
Hoeffding budget. The ideal-independent sampling premise is a theorem
premise; a deterministic PRNG replay is not a physical randomness test.
No qubit, gate, laboratory measurement or real source was operated.
The analytic lower bound is proved above, not inferred from the simulated
classification successes. Float checks use tolerance 10^-12 and are
diagnostics; the rational Neumann bound and trigonometric proof supply
certification. The two 1,166-shot fixtures generated 2,332 individual binary
outcomes and charge 2,332 whole starts plus 34,980 native rotation calls.
Their retained counts are 595 and 373 respectively; both binary decisions
are correct. Runtime was about 0.0076 seconds and is not physical time.

## 7. Relation to current Astra and to the opportunity choice

The current Astra sources are stronger than the obsolete statement that all
predictive-operation bounds remain vacuous. N1148 constructs restricted
count-certified virtual CP predictive realizations under exact source rank,
repeatable starts, acquired cores, gauge and strict Choi margins. The later
N1166 physical residual simulator admits unitary/boundary maps by requiring
an actual physical same-observable-rank candidate and proving classical
full-transcript TV<=b E_true[L]. Its completed independent review accepts
that conditional mathematical scope. Its exact rank and physical-candidate
search can be real-algebraic and potentially enormous; no such acquisition
search was executed. The governing sources and completed review have been
read in full, including continuation pages and current scope notices, and
are preserved under `sources/`.

This example is outside N1148's unrestricted two-sided strict-interior test
because rotations are boundary CP maps, but it is not outside the physical
candidate regime of N1166. Equation (3) explains why count accuracy must
still tighten for a much longer requested future. Nothing here disputes the
accepted rank, residual or prefix/suffix theorems. The learner is even given
the two candidate models and their rank, so gauge-search costs are removed
from the lower bound.

The different opportunity remains substantial: discovering affordable
predictive representations for unknown controlled memory could support
reusable scientific simulators and controllers. However, the decisive
missing steps are experimentally affordable core design, condition-sensitive
accuracy, actual rank/completeness warranties, and efficient physical model
search. A rank-only universal-prediction agenda would discard the very
information the consequence demands. The result therefore supports a
task-sensitive information theory as the larger shared destination, while
not supplying a stronger immediately constructive opening than the current
macroscopic-transition program. No historical-priority or resource-advantage
claim is made for this alternative lemma.

## Primary-source starting points

1. Littman, Sutton and Singh, *Predictive Representations of State*, NIPS
   2001. Observable predictions as state and finite linear representations:
   https://proceedings.neurips.cc/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf
2. Huang, Liang and Yang, *Provably Efficient UCB-type Algorithms For Learning
   Predictive State Representations*, ICLR 2024. The current positive PSR
   learning literature is a comparator, not an absent method:
   https://proceedings.iclr.cc/paper_files/paper/2024/hash/cbfa01fae7875353d954429795d954f5-Abstract-Conference.html
3. Adhikary, Srinivasan, Gordon and Boots, *Expressiveness and Learning of
   Hidden Quantum Markov Models*, AISTATS 2020. CP observable models and
   physical parametrized learners predate this construction:
   https://proceedings.mlr.press/v108/adhikary20a.html
4. Higgins et al., *Entanglement-free Heisenberg-limited phase estimation*,
   Nature 2007, preprint https://arxiv.org/abs/0709.2996 . Repeated coherent
   interrogation is an established physical information resource. The present
   elementary two-point calculation is not a new metrological scaling law.

All external sources are starting material/comparators. The lower and upper
bounds in this document have complete ordinary proofs above.
