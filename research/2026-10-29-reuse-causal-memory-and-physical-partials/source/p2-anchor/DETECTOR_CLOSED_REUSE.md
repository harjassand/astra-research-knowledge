# Causal collection and detection preserve the reusable-memory certificate

29 October 2026, Australia/Brisbane. Root corollary; independent review
is separate. Neither frozen input proof is modified.

## 1. The output operation

The main contact theorem traces the departing b_j. Its proof actually
controls the full output BEFORE that trace. This allows collection,
detection and later feedback while preserving the retained oscillator a,
its source correlations and every actual record.

The same supplied collection/detector process appears in both models.
It need not have ideal efficiency, zero dark counts or memoryless noise.
Uncertainty in that process needs its own compatible complete-channel
allowance. A small model-comparison error does not say that the noisy
record contains enough information to perform a useful computation.

## 2. Precise causal interface

Let K contain source, controller, arbitrary reference, detector memory,
all actual records, and any already departed modes retained for processing.
K may be arbitrarily correlated with a, with <N_a><=P_*^2. Each new b_j
is thermal and independent of ALL of K and a. During the contact use the
anchored Hamiltonian, prescribed passive pulse and common pointwise source
envelope from the main theorem.

Once the contact ends, b_j has no further passive coupling to a or another
currently active b. It can join the collected-output part of K. Collection
and detection can be arbitrary COMMON complete instruments on K and already
departed modes. They may retain quantum outputs, actual records and internal
detector memory. They act trivially on a and on active/future thermal input
modes. Subsequent source controls act on K and obey the same declared
bounded source envelope during their interactions with a.

This permits finite detection delay, joint processing of several departed
modes, imperfect collection and correlated detector memory, when their
complete channels and timing are supplied. A returned mode coupling directly
to a, or measurement of b_j during its still-active passive interaction,
does not satisfy this boundary. Those need an enlarged contact model.
An instrument acting directly on a needs an additional moment contract.

## 3. Local comparison before tracing the output port

For equal thermal inputs the v and g terms are purified-vector Duhamel
bounds on the full a,b_j,K output. For differing thermal means compare the
mixed inputs directly in trace norm, then apply the common contact. Thus

    d(rho_(a,b_j,K)^actual,rho_(a,b_j,K)^model)
                  <=epsilon_v+epsilon_g+epsilon_n.     (1)

The arbitrary reference in that proof includes all earlier collected modes
and detector memory. The physical canonical a,b_j and generator are common;
no abstract bath Gram gauge identifies a detector output for free.

A complete collector/detector, including its actual outcomes, is a CPTP
map and contracts (1). No division by a heralding probability occurs.
The result does not give a uniform error for normalized rare branches.

## 4. Detection preserves the needed occupation region

Every allowed complete instrument D acts trivially on a. Its unital dual
therefore obeys, first for bounded number truncations N_a^M,

    Tr[(N_a^M tensor I) D(rho)]
                       =Tr[(N_a^M tensor I)rho].        (2)

Monotone convergence gives the same identity for N_a. Actual record
retention and source-only feedback do not change it. These operations can
change conditional memory states, but they preserve the UNCONDITIONAL
mean. The contact invariant hence survives all those causal operations.

At each next contact, fresh thermal independence supplies anew

    ||J_j psi_in||^2=(2n_j+1)<N_a>+n_j.

Only current a and current b_j enter this row. The total occupation of
earlier emitted modes may grow; it is not the number operator controlling
this local estimate. Their storage, detector state, source and records are
additional resources. One retained oscillator does not mean constant total
computing memory or a free collection apparatus.

## 5. Full delayed-record composition

Place each common collection/detector step and feedback operation at its
actual causal time. Replace contacts one at a time using (1). Prefixes
remain in the invariant moment region by (2), and later common operations
are contractive on the enlarged retained state. For every finite J,

    d(rho_final^actual,rho_final^model)
                    <=min(1,sum_(j=1)^J epsilon_j).     (3)

The output can include a, logical source, reference, actual detector
records, unmeasured collected outputs and detector memory. No independence
of detector errors or outcomes is needed: a supplied correlated detector
process is included in K and appears identically in the two models.

Known common detector noise need not be small for (3) to hold. It can still
make a proposed computing task inaccurate or useless. Comparison against
an ideal computing instrument must separately charge detector, preparation
and control error on compatible hybrids. An isolated detector-use bound
cannot automatically stand in for a complete multi-use detector-memory
contract. Likewise, an output POVM alone does not identify an instrument
whose surviving quantum output will be used later.

## 6. Statistical and physical reach

On a simultaneous parameter-confidence event, (3) covers every admitted
source program, including data-selected programs and source feedback from
actual detector outcomes. The event does not acquire the detector process,
prove thermal freshness, or calibrate its own control/readout apparatus.

This is a complete monitored persistent-memory instrument. It extends the
anchored contact comparison; it does NOT extend the earlier unanchored
source-only kernel theorem to physical bath outputs. That theorem retains
its accepted scope. A physical realization still needs native coupling,
collection, paid calibration starts, a fresh thermal input for each contact,
controls, detectors and the no-return condition. No equipment has been
operated and no useful-computation advantage is asserted.

## Frozen inputs

Root main theorem: REUSABLE_ANCHORED_MEMORY.md, SHA256
52aadce16a2e08e0c96a71662fc9c04382cc0a26364580d369980a2c227275fc.
Challenger lemma: ../challenger/THERMAL_CONTACT_FIRST_MOMENT_SENSITIVITY.md,
SHA256 5c10503d7254a2af09eedc0780a2c653618e67b6a518ea16f2b2fd91aa3d678b.
No nonlinear numerical solver is required for this causal-composition proof.
