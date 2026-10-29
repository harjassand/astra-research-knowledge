# Constructed dynamic FIFO; reliable logical acceptance remains a gate

The completed operation is a state-based, noisy asynchronous FIFO. Source
capture, transfer, acknowledgement and overwrite are local atomic actions.
A source changes its offered symbol after capture; each internal payload
waits until its local downstream acknowledgement permits overwrite. No
external copy interval, perfect clock, protected tag register or retained
history is used by the controller.

The key representation is occupancy

    e_i=t_(i-1) xor t_i.

EVERY tag configuration represents a valid exclusion/FIFO state. Every
nominal move preserves the packet word, input appends, and output removes
its head. At most q physical-bit replacements at a fault cause at most2q
unlocated packet edits, for arbitrary future-dependent fault labels.
Pathwise, through every horizon,

    d_edit(output + current_queue, initial_queue + accepted_input)
         <=2q * actual_fault_count.

This is genuine bounded-effect composition: downstream nominal stages do
not amplify one tag error into an indefinitely misaligned sequence. It
also does NOT herald which packets were altered or make every scalar
notification trustworthy.

A schedule-only coverage/workload theorem pays recovery under continuing
noise and a TRANSFER deadline-or-edit while later real inputs continue.
It is simultaneous over every physical starting state and future-selected
accepted packet/time; no false fresh-source or strong-Markov assumption is
made. For capacity M, q-bit faults, N=(B+1)M+1 controller bits and
w=2ceil(log2(16M)), the sufficient per-bit noise bound is

    lambda<=1/[16 N (2Mq+1)w].

An undamaged packet is delivered within the returned latency except on
the stated small schedule event. A damaged packet may be dropped, inserted
or substituted without a receiver flag. The reset theorem is an EMPTY-
EPOCH hitting time, not certainty that an arbitrary later read sees empty.

## Actual acquired finite contract

The one native instance is M=3, B=2, q=2: all10 physical bits are noisy.
The consumer checked all1024 states,7168 nominal transitions and57344
up-to-two-bit fault masks. All queue identities, overwrite/commit guards,
nonempty-state progress and edit/work bounds passed in0.117026s with
22.74MB peak RSS. These finite checks support the literal implementation;
the arbitrary-capacity proof is analytical, not finite extrapolation.

The exact scalar receiver took0.0000514s with zero trajectories or state
samples. At the sufficient rate lambda=1/24960, it returns latency13728
for every input accepted through time1024, with probability at most2^-20
that ANY UNDAMAGED packet misses that latency. The expected fixed-grid
empty-epoch time is at most576/7. These are conservative theoretical
bounds in nominal physical-time units, not measured hardware performance.

No small RAW edit probability is implied at that rate/horizon. Expected
fault count through1024 is16/39, so even the upper mean edit budget is
64/39. A claimed exponentially reliable stream would need an additional
encoded consumer/codec and its own noisy-state proof. No such layer is
assumed or claimed.

## Strong ordinary comparison and next gate

Sutherland already supplies asynchronous micropipeline composition and
request/acknowledgement capture/hold semantics. Stabilizing data-link
theory already quantifies ghosts, duplication and stale-channel recovery.
Queueing, coverage and exponential-supermartingale methods are ordinary.
This packet is an explicit paid sustained-noise instantiation, not a new
generic architecture or a claimed practical advantage.

The sharper surviving question is now an unlocated-edit/deadline-tolerant
classical consumer with real noisy state, rather than a raw phase bit that
can retain arbitrary permanent corruption. A scalar acceptance port has
a constant-noise false-accept floor. Closing the FIFO into a feedback ring
also permits full/empty nominal deadlocks, so a feedback controller needs
actual protected hole/token restoration. The stronger mutable-logical-
register/quantum-decoder target remains NOT_ACQUIRED.

Governing theorem: PROOF.md. Reusable input contract: COVERAGE_ERODER.md.
Literal controller: fifo.py. Scalar acquisition: compile_deadline.py and
DEADLINE.json. Whole finite native consumer: consume_fifo.py and
NATIVE_REPLAY.json. Exact conventional/source disposition:
PRIOR_AND_DECISION.md. No earlier frozen research was modified.
