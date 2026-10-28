# Acquiring missing coarse-state memory without refreshing the source

29 October 2026, Brisbane. This continues the failed coarse-boundary extension.
The first-return records in COARSE_BOUNDARY_OBSTRUCTION.md cannot reveal
within-cell redistribution. Uninterrupted probes can. Two executed procedures
below use the same coarse live/absorbed interface and fresh preparations; the
stronger procedure buys physical evolution time instead of extreme moment
precision.

## A finite memory witness

Let f(h) be survival after h source applications from the declared preparation,
with f(0)=1. A one-state time-homogeneous linear model requires f(h)=p^h. Hence

    Delta_L = f(2L)-f(L)^2 > 0

rejects that model. Equivalently the 2 by 2 Hankel matrix with entries
1,f(L),f(2L) has rank at least two. This is a lower bound on the dimension of
a linear realization, not an upper bound on the hidden system's dimension.
For selfadjoint sources with matching preparation/readout, it is also the
Gram determinant of the actual two-word dictionary {v,A^L v}.

The source is A_g=diag(1-g^3,1-g), prepared uniformly, at g=1/32. Neither
hidden microstate is reported to inference. Every trial receives a fresh
preparation; a coarse live report never triggers an assumed restart.

## Executed short probe: valid, expensive

The first procedure runs two steps, stopping early only on irreversible loss.
Let r1 be death at the first step and r2 death at the second step. Then

    Delta_1=r1-r2-r1^2.

Thirty-two million fresh trials produced counts 500,902 and 484,903. Exact
binomial Chernoff intervals and monotonicity of r1(1-r1), on r1<1/2, give

    Delta_1 in [.00004499735298,.00046485681363].

Thus memory is certified. The resource bill is 63,499,098 primitive
applications, the same number of coarse reports, and 32,000,000 fresh
preparations. These are executed integer-RNG software trajectories, not a
precision promise substituted for acquisition. Only the trial count and two
observable death counts enter the inference.

This is a poor operational route on this example. Its true determinant is
order g^2 while the rare death probabilities fluctuate on scale g. Resolving
that small difference by fixed two-step statistics has the familiar g^-3
sample scale. The count of just two moments conceals that cost.

## Stronger equally informed route: choose a longer experimental word

A separate procedure pays for its own 2,048 one-step pilot preparations. Its
34 observed deaths select block length

    L=ceil(pilot_trials/(2 pilot_deaths))=31.

The pilot is used only for design. It need not produce a valid parameter
estimate: the fresh main batch has valid conditional confidence for whatever
finite length the pilot chooses.

Ten thousand new trials run one length-L block and read the coarse endpoint.
The 6,799 observed survivors continue for a second block without resetting;
5,640 survive both. A complete block is charged even if the hidden backend
absorbs earlier, because no intermediate report was acquired. The two
unconditional main survival counts estimate f(L) and f(2L). Their intervals
yield

    Delta_31 in [.04617706029,.15682885293].

The joint failure probability is below .001. No microscopic label, precision
oracle or hidden-rank promise enters the witness. The intervals may be
correlated; a simultaneous union bound makes the squared-endpoint calculation
sound.

| Complete resource | Two-step witness | Pilot-selected block witness |
|---|---:|---:|
| Primitive applications | 63,499,098 | 522,817 |
| Coarse reports | 63,499,098 | 18,847 |
| Fresh preparations | 32,000,000 | 12,048 |

Both certify a need for at least two linear features on the same source and
interface. The block procedure uses about 121.5 times fewer source applications
in these executed examples. This is a comparison with the specified short
procedure, not a universal optimality or hardware-time claim. The sources,
instrument accuracy and preparation distributions are identical; the pilot
cost is included.

## Physical time explains the gain

For g=1/m, taking L=m gives the exact determinant

    Delta_m=[(1-g^3)^m-(1-g)^m]^2/4.

For m>=32, the first term is at least 1-g^2 and the second is below 2/5.
Thus Delta_m exceeds a positive numerical constant. A fixed number of bounded
binary observations suffices to certify it at fixed confidence, while each
observation costs order 1/g physical applications. The resulting source cost
is O(1/g) when that scale is supplied. The executed independent pilot finds
a comparable length for this example; its fixed 2,048-trial budget is not
claimed to find the right scale for every g or every source.

There is a matching order lower bound on the known pair A_g and B_g=p_g I,
even if the learner sees and can prepare either microscopic state. Each
informative source application is a survival coin. Its two possible death
rates differ from p_g's death rate d=(g+g^3)/2 by (g-g^3)/2. Therefore

    KL(one application under A || B)
      <= [(g-g^3)/2]^2/[d(1-d)] <= (16/31)g < g.

Operations at cemetery and source-independent preparations add no information.
Adaptive transcript KL is at most g times expected source applications.
Errors at most 1/3 under both hypotheses require total variation at least
1/3, hence KL>=2/9. Expected source applications are therefore at least
2/(9g). The h=10/g response separation above .48 makes uniform error below
.2 sufficient to distinguish the pair. This is the standard change-of-measure
argument, applied to this new source pair, not a new information inequality.
This constant-separation memory test is a different accuracy task from the
O(g) uniform prediction task with g^-3 calibration cost. Its 1/g rate does
not evade or contradict that earlier lower bound.

## What has and has not been repaired

The experiment discovers a missing direction through an actual word Gram
matrix, preserving the source rather than physically randomizing it. This
returns a valuable piece of P1 machinery to the broader composition question.
It does not yet acquire a closed two-state model, certify that no additional
features matter, or provide an all-word error certificate for the coarse
interface. Those are distinct remaining obligations.

The executable records are core/coarse_memory_witness.py and
core/coarse_block_witness.py, with raw counts and exact intervals under
results. The source constructor's parameters enter only trajectory generation
and private checks; the witness formulas use the observable counts. No new
physical equipment or third-party interaction occurred.
