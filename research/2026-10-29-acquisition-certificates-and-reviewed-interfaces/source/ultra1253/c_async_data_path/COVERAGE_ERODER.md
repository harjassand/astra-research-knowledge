# Reusable finite-cell coverage-to-recovery contract

The FIFO proof isolates a general, ordinary workload construction. Its
value is a checkable protocol input contract, not a claim that every
asynchronous decoder has such a potential.

Suppose a finite controller has m independent nominal Poisson attempt
clocks of fixed rates>=r_min>0 and a function W with values0,...,Wmax.
Require the following STRUCTURAL facts for its actual local transition
functions, on every state:

* Every nominal nonidentity operation decreases W by at least1. Identity
  attempts leave the entire W-relevant state unchanged.
* If W>0, at least one nominal operation is nonidentity/enabled.
* Each admitted supported fault increases W by at most C, with any
  replacement labels, including future-dependent choices.

It suffices to require these facts up to a stopping event, such as packet
delivery or a separately charged alteration of that packet. All additional
operations during the interval must leave the relevant state/potential
unchanged, or satisfy the same decrease condition. Later FIFO inputs obey
this for a chosen packet's prefix.

Fix analysis-window width w with m exp(-r_min w)<=1/16. For independent
fault support streams of total rate Lambda, let F_j be fault counts and
J_j the event of failed nominal clock coverage. The PATHWISE inequality

    W_(j+1)<=(W_j-1)^+ +(C+1)F_j+J_j

holds for every starting state and every fault labelling. Why coverage
works must be checked, not assumed: without a fault, either an earlier
nonidentity event already lowered W, or the unchanged initial state still
has its enabled action when that clock rings. Nominal state changes at
zero W-cost could invalidate this reasoning.

If Lambda w<=1/[16(C+1)], put z=1+1/(C+1) and
r=5/[16(C+1)]. The dominating Lindley queue begun at DETERMINISTIC Wmax
then satisfies

    E exp(r tau)<=z^Wmax,
    E tau<=8Wmax/7,
    Pr(tau>k)<=exp{[Wmax-5k/16]/(C+1)}.

These are a genuine recovery-time tail under continuing noise. Starting
at worst-case Wmax makes the good-schedule event simultaneous over all
controller states. Fixed-window unions pay future-selected activation
times; Finner/read-q pays several independent-clock cells coupled by
q-site fault support streams. PROOF.md contains the complete calculations.

The input contract is NOT merely a positive average correction velocity,
a quiet-interval self-stabilization theorem or a Gibbs/Peierls estimate.
It excludes uncharged zero-cost state rotations which can move an enabled
action around, absorbing clock configurations and a faulty input source
which can inject unlimited unaccounted work. A closed FIFO ring fails it.

For many clocks or a volume-growing potential, total Lambda and C must be
charged. This lemma does not manufacture a size-independent noise threshold.
Constant-body cells can have a paid constant-rate contract; a spatial
composition still needs its actual interference/flow-control argument.
All methods in this lemma are standard coverage, queueing and exponential
supermartingale techniques. No generic novelty claim is made.
