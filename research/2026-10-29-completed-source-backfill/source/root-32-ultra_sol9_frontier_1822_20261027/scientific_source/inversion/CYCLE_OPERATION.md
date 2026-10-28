# Loss-pulse cycle witness with unknown preparation and gains

This is a second, smaller operation derived from the two-pulse contrast in
PROOF.md. It requires only the selected cycle labels to be addressable; the
number or connectivity of unaddressed states need not be known. It does not
require a full transition matrix, its invertibility, population conservation,
or calibration of pulse efficiencies, aggregate gain, or initial population.
The cycle criterion itself is established Kolmogorov reversibility theory.
The finite acquisition/cancellation construction here is not novelty-cleared.

## Exact operation

Let a finite classical population evolve by a fixed nonnegative linear
operator P from time 0 to tau. It may be a substochastic operator. Selected
labels i_1,...,i_k, k>=3, are distinct *individual kinetic states*; all other
states can be inaccessible. The initial unnormalized population p is fixed
across settings and has p_i>0 at these selected states. A pulse at label i
and slot E or L removes an unknown fixed fraction a_i^E or a_i^L in (0,1].
The two slot efficiencies may differ. Apart from this deletion, survivors
have exactly the same dynamics. The scalar detector immediately after the
late slot has fixed unknown affine law beta+gamma*1^T x, gamma>0, counting
all surviving states with equal weight.

Measure baseline, k early-only settings, k late-only settings, and the 2k
ordered pairs on the forward and reverse cycle edges: M=4k+1 settings.
Form, for each directed edge i->j,

    C_ji = yPair_ji - yEarly_i - yLate_j + y0.

Expanding (I-a_j^L E_j)P(I-a_i^E E_i) gives

    C_ji = gamma*a_j^L*a_i^E*p_i*P_ji.                    (1)

For all 2k P entries positive, the measured cycle log ratio is

    A = sum_edges(i->j) log(C_ji/C_ij)
      = sum_edges(i->j) log(P_ji/P_ij).                   (2)

Proof of cancellation: each selected vertex appears exactly once as a source
and exactly once as a destination on each oriented cycle. Both products
contain gamma^k, product_i(a_i^E a_i^L), and product_i p_i. Thus unknown
preparation and asymmetric early/late pulse efficiencies cancel exactly.
This is an invariant of independent positive row/column scaling of the
selected transition submatrix. No stationary preparation is assumed.

If P=exp(tau Q) and Q is reversible with respect to a positive measure pi,
then Q_ji*pi_i=Q_ij*pi_j implies P_ji*pi_i=P_ij*pi_j. The ratios on every
cycle telescope, so A=0. The same proof holds for a reversible generator
with arbitrary added diagonal killing: its semigroup remains symmetrizable.
Therefore A!=0 certifies violation of this reversible full-state model even
when the selected states connect only through inaccessible intermediate
states. A=0 does not certify reversibility. A is a finite-lag transition
affinity, not in general a single-edge rate affinity, entropy-production rate,
or a lower bound on either. Those stronger claims are not made.

## Rigorous finite-sample decision

For independent [0,1] trial readouts, m trials at each of M settings and
epsilon=sqrt(log(2M/alpha)/(2m)) make every empirical mean epsilon-close with
probability >=1-alpha. Add any acquired systematic mean-error budget zeta.
Each C is then in [Chat-4(epsilon+zeta), Chat+4(epsilon+zeta)]. Physical
contrasts are nonnegative. A valid lower endpoint is

    A_lower = sum log(max(0,Chat_forward-4(epsilon+zeta)))
              - sum log(Chat_reverse+4(epsilon+zeta)).    (3)

A zero lower contrast gives A_lower=-infinity. For A_upper, exchange lower
and upper endpoints, yielding +infinity when a reverse lower contrast is
zero. A_lower>0 or A_upper<0 rejects reversible models at error <=alpha,
conditional on all interface premises and the deterministic error budget.
Shared baseline/single measurements make the interval conservative; they
are not falsely treated as statistically independent contrasts.

The k=3 design has 13 configurations and 18 elementary pulses per one
trial/configuration sweep. Thus m=10^6 costs 13 million fresh preparations,
13 million terminal readouts and 18 million loss pulses, plus reset,
population preparation, pulse energy, timing and selectivity calibration.
An ensemble has not reduced this to 13 trials: its particle statistics and
correlations would require a measured acquisition model.

## Equally informed ordinary method

The ordinary comparator gets all 13 Bernoulli counts and the same nuisance
model. It uses the shared-mean contrast covariance or fits the raw means
under the single constraint product(C_forward)=product(C_reverse). This
null is a *superset* of physically reversible hidden-generator models, so
it does not need to know the hidden network. The plug-in point estimate is
identical to (2); constrained likelihood can be more statistically efficient
than the conservative rectangular confidence bound. An asymptotic likelihood
ratio is labeled asymptotic, not promoted to a rigorous finite-sample p value.
No computational or statistical advantage over that comparator is claimed.

The repeated-complement-state-filter comparator in PROOF.md needs selective
loss at *every* unwanted state. It is available for full tomography only when
that stronger control interface is supplied. It is not available in this
partial-access operation merely because three labels are addressable.

## Essential physical boundaries and exact falsifier

1. A label must be one kinetic state, or a rigorously acquired lumpable class.
   Arbitrarily unresolved groups invalidate transient-preparation cancellation
   as a reversibility test. For example, consider the reversible symmetric
   six-state ring one-step operator P with diagonal 4/5 and nearest-neighbor
   entries 1/10. Group states as A={0,1}, B={2,3}, C={4,5}, and prepare
   p=(1,2,3,4,5,6)/21. Uniform loss at each group gives a forward/reverse
   contrast-product ratio (2*4*6)/(3*5*1)=16/5, despite microscopic
   reversibility. For the symmetric continuous-time ring, the same ratio
   tends to 16/5 as tau->0, so the failure also occurs for reversible CTMCs.
   The implementation preserves this counterexample rather than silently
   generalizing to spectrally unresolved substates.

2. All survivors must be counted with a common affine detector. Unknown
   state-dependent readout weights or nonlinear saturation are not covered.
   If an affine approximation is independently bounded by zeta on all
   relevant populations, it can be charged in (3); otherwise there is no
   certified conclusion from this operation.

3. The same preparation, timing and pulse maps must be reproduced across
   settings. Unknown off-target loss, pulse-induced transitions, altered
   survivor dynamics or drift can manufacture a contrast cycle. Bounds on
   those effects are physical acquisitions. Interleaving settings can help
   measure drift but is not a proof that drift is absent.

4. State-selective removal and temporal correlation acquisition are prior art:
   Robens et al., Phys. Rev. X 5, 011003 (2015),
   https://doi.org/10.1103/PhysRevX.5.011003. Correlation asymmetry and
   thermodynamic cycle-affinity theory are also prior art; see Ohga et al.,
   Phys. Rev. Lett. 131, 077101 (2023),
   https://doi.org/10.1103/PhysRevLett.131.077101. Neither source is claimed
   to prove this entire acquisition theorem. Historical originality remains
   UNKNOWN after the bounded search, and no new general reversibility
   criterion is claimed.

## What has actually been obtained

An explicit finite scalar-acquisition operation, algebraic recovery of a
selected finite-lag cycle invariant under unknown positive nuisance gains,
a conservative finite-confidence decision rule, and a sharp coarse-state
failure case. Code execution below is synthetic/model evidence. There is no
acquired physical pulse/detector system, practical-advantage demonstration,
external review, or foundational breakthrough in this worker.
