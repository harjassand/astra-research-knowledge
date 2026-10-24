# Rank-two acquired-reset fixture: cost, record, and forgetting controls

2026-10-24. Bounded audit of the executable fixture in
`../private_plant.py`, `../reset_learner.py`, `../run_reset_bootstrap.py`, and
`../run_seed_20261024/`. This is an evaluator-side accounting note for a
synthetic HMM, not physical acquisition or validation.

## What the saved run did

The interface declares three one-step actions: `s` (hidden-state identity,
with a noisy binary readout), `a`, and `b`. The rank-at-most-two full controlled
Hankel promise is supplied; nine frequency cells do not establish that rank
promise. The calibration block has 3 preparations times 3 macros, each with
50,000 independently initialized trials: 450,000 external starts. Their
concatenated words have total length 21 primitive actions per set of nine
50,000-trial cells, for 1,050,000 calibration actions/readouts. The learner
receives integer counts, the declared interface/rank promise, and confidence
width; it fits no hidden-state matrices.

The count-only learner selected basis `(initial,b)`, with observed gap
`-917/1250=-0.7336` and certified lower magnitude `446/625=0.7136`. It found
the count-derived cancellation weight `9701/20697` for action `a`, then used
the nearest 16-bit dyadic

    lambda_a = 30718/65536 = 15359/32768,
    lambda_b = 34818/65536 = 17409/32768.

The integer threshold is positive and interior. Its observed dyadic contrast
residual is `1713/327680000` (about `5.23e-6`); the finite-count uniform
future-event certificate is `4097070625/104289271808` (about `0.039286`).
This certificate already uses the implemented dyadic weights, so no separate
rounding-error term should be added. The run asked for tolerance `0.05`, and
the bound passed. The saved future sampling margin is `0.02` per program; the
combined stated confidence failure bound is about `8.75e-4`.

The three new programs each ran 20,000 trials, for 60,000 reset invocations and
no external starts. Each reset uses exactly one `a` or `b` action, hence one
fixed-duration primitive step and exactly 16 selection bits. The programs
then use 1, 3, and 3 primitive steps per trial, respectively. The saved
ledger therefore reports 200,000 total future actions/readouts: 60,000 reset
steps/readouts (discarded) and 140,000 task steps/readouts. It reports
960,000 selection bits. The synthetic held-out means were `0.50385`, `0.50450`,
and `0.84470`; all three were within the saved `certificate + 0.02` allowance
of post-execution evaluator truth. This is a finite simulator replay only.

## Amortization against the matched external start

Let `C_init` be a complete external initialization, `C_step` one primitive
step, and let `C_other` include all acquisition computation, readout,
precision, random-bit, isolation, and any noncommon validation costs. The
acquisition ledger is at least

    C_A = 450000 C_init + 1050000 C_step + C_other.

Against the explicit same-target baseline that pays one external initializer
and then applies the same reset `S` on each future trial, the per-trial `S`
cost is common. The candidate saves only the future `C_init`, so break-even is

    T C_init > C_A.

At the executed `T=60000`, this fails for every positive `C_init`, even if
`C_step=C_other=0`: the 450,000 calibration starts are 7.5 times the 60,000
future starts. With positive noncommon costs, the necessary use count is
strictly above 450,000. The saved run summary correctly says total cost
advantage is not established. If the external baseline can directly prepare
the same target without applying `S`, then the candidate's one-step/16-bit
operation and record-isolation costs are additionally noncommon. The target
is `S(rho0)`, not the original initializer `rho0`; substituting it is valid
only for a future task defined on that new reference.

The strongest same-data conventional contrast learner estimates the same two
preparation contrasts and uses the same positive dyadic mixture. It obtains
the identical operation and certificate, so there is no method advantage in
this fixture. The following pure-word comparison is a separate truth-side
control, not a data-only confidence certificate emitted by `reset_learner.py`.

## Pure-word approximate forgetting in the evaluator model

The evaluator-only HMM has hidden-state-one probability `p` and transition
maps

    a: p -> 1/20 + (9/10)p,   b: p -> 9/10 - (4/5)p,   s: p -> p.

Every finite deterministic word has nonzero slope: a factor `1`, `9/10`, or
`-4/5` is multiplied for each step. Thus no pure word is an exact reset. For
length `k`, the strongest pure word in hidden-state contraction is `b^k`,
with slope magnitude `(4/5)^k`. The private truth for the acquired dyadic
mixture is slope

    d_mix = -1041/327680,   |d_mix| = 0.0031768798828125.

At length 25, `(4/5)^25 = 0.003777893186...`, which is worse; at length 26,
`(4/5)^26 = 0.003022314549...`, which is slightly better. So the one-step
mixture buys the same or stronger contraction than the best pure word through
25 steps, while `b^26` narrowly beats it in diameter at 26 steps. Every
future-event probability is affine in the initial hidden distribution with
endpoint values in `[0,1]`, so its slope is at most one; these hidden-p
contraction values are valid evaluator-side bounds on visible-event
differences for this two-state HMM.

For the same reference `rho_star=S(rho0)`, the true hidden probability is
`p_star=32683679/65536000`. The one-step mixture's worst hidden-p distance to
that reference over `p in [0,1]` is

    (19/20)|d_mix| = 19779/6553600 = 0.003018035888671875.

The output interval of `b^26` is centered at `1/2` with radius
`(4/5)^26/2`; its maximum distance to this same `p_star` is
`|1/2-p_star|+(4/5)^26/2 = 0.002797793627...`, also slightly smaller.
This is a truth-side statement because `p_star` and the exact maps are private
fixture facts. A learned pure-word comparator would have to derive and
certify its own interval from counts. Operationally, `b^26` costs 26 action
steps and produces 26 internal readouts that must also be hidden; the acquired
mixture costs one action, 16 bits, and its reset record must be hidden. At the
executed 60,000 uses, that is 1.56 million versus 60,000 reset steps, before
the common 140,000 future program steps.

## Record and timing boundary

The 16-bit threshold method avoids variable-rejection runtime: every reset
uses the same bit count, one of two equal-duration actions, and one public
completion time. The simulator suppresses the selected action and its reset
output from returned future counts. Its outputs report `selection_words_exposed
false`, `reset_outputs_exposed false`, and `public_reset_duration=1`.

Those are interface choices in Python, not physical isolation. In particular,
`del selection` removes the current 16-bit integer but does not erase the
`selection_rng` object's internal state; that PRNG persists across the 60,000
draws. The simulator seed is deterministic, not a certified independent
entropy source. No constant-time hardware path, action/power side-channel
protection, protected seed state, secure record discard, or thermodynamic
erasure was validated. Fixed duration removes the modeled rejection-time
channel, but does not establish these other physical gates.

There is also a strict learner-input mismatch in the saved run: `calibration_counts`
serializes `simulator_seed` into `counts.json`, which is passed directly to the
count-only learner. `reset_learner.py` currently ignores that field, but the
field is still learner-visible; move it to an evaluator-only manifest before
describing the actual interface as counts-only. The adjacent private plant
file is likewise not OS-isolated from a hypothetical untrusted learner, even
though the fixed learner script does not import it. The post-run retained
evaluation JSON also contains `simulation_seed`; that must stay evaluator-only
if future held-out outputs are subsequently supplied to a learner.

The certification is therefore conditional on a two-state full-interface
rank bound, stationary complete-process starts during calibration, and a
private fixed-bit reset controller with hidden reset records. The saved
synthetic run demonstrates those code-level contracts and one finite held-out
replay; it does not validate entropy, physical record isolation, or the
amortization inequality.
