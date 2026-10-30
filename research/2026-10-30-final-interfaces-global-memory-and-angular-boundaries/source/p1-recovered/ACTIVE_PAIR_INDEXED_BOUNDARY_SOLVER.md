# Ordinary optimization on the active-pair clock

30 October 2026. Constructive implementation change requested by root.
This reuses the exact PacketPort, ADCs, rails, target, seeds, activity
schedule and 262144 calendar-pair budget of the root bounded-task
check. The preceding sparse-matrix and continuous-port files are
unchanged. No additional physical source or hidden initialization is
introduced.

## 1. Update when an observation is actually acquired

Let t_k be the kth active calendar pair. Between active pairs, execute
the prescribed two zero-incident matched windows per calendar pair
and hold the numerical command unchanged. On active pair k use the
same two-sign bounded physical operation, and define

    g_k = lambda u_k + tau_k zhat_k/kappa,
    u_(k+1) = projection_D[u_k - 2 g_k/(lambda(k+1))].

There is no factor 1/p_(t_k). The predeclared output averages are

    ubar_K = (1/K) sum_(k=1)^K u_k,
    gbar_K = (1/K) sum_(k=1)^K g_k.

The command u_k is the value before its physical pair and update.
Every active pair enters both averages, including saturated ones.
This is ordinary projected SGD on its actual observation clock.
The calendar duty schedule still controls physical energy occupation,
waiting, sensing and completion cost; reindexing does not erase time.

## 2. The same guard and observed-square certificates

Condition immediately before the fresh sign of an active pair, with
the complete physical/controller/instrument history included. The
actual source state may depend on every intervening idle window.
The fixed linear two-window decomposition is nevertheless the same,
and the sign/dither conditioning proves the same clipping-bias bound.
The binding ADC mean contract must hold conditional on that full
history and on the present command/sign, not merely conditional on
the numerical raw value. The supplied independent fresh dither has
that property.

Use the root guards F_k and cap C_F without modification. If

    h_k = E[g_k | pre-sign history] - grad F(u_k),

then ||h_k|| <= E[F_k | pre-sign history]. The known regularizer is
predictable and contributes no martingale noise. For K active pairs,
write O_K=sum F_k and Q_(Kj)=sum (tau_k zhat_(kj)/kappa)^2.

Every root certificate now has p_k=1, w_k=1 and a_K=1. In particular,
with c0=1-exp(-1), b0=R_z/kappa,

    D_K = [O_K + C_F log(1/delta_B)]/c0,
    Vhat_(Kj) = [Q_(Kj) + b0^2 log(d/delta_V)]/c0.

Use the same preallocated dyadic variance grid and Bernstein bound
with active horizon K. If H_K is the resulting vector noise radius,

    ||gbar_K - grad F(ubar_K)|| <= (D_K+H_K)/K

with total failure at most delta_B+delta_V+delta_M. This exploits
affinity of the quadratic gradient; uniform averaging is fixed before
the data. The root projected fixed-point residual then bounds the
distance to the constrained optimum. No fitted transfer matrix,
hidden state or independent validation experiment enters this bound.

The basic digital signal bound is now R_z/kappa, independent of the
small calendar duty p_i. The guard debit contains actual guard counts,
not importance weights. This removes a needless implementation cost
when the task is to learn from the acquired pairs rather than to
estimate a separately prescribed calendar-weighted objective.

## 3. Why the random final active count is legitimate here

The executed comparison uses the same predeclared calendar checkpoints
64,128,...,262144 and the same total alpha=0.05 allocation as root.
At checkpoint N, the number K_N of active pairs is random. A fixed-K
bound must not simply be asserted at an arbitrary data-selected K_N.

Here the complete activity schedule is generated independently of the
source, initial state, signs and ADC dithers, using predetermined
probabilities. Condition for the proof on that entire schedule. Each
K_N and every idle gap is then deterministic, while future signs and
dithers remain fresh. The bounded-pair martingale proofs apply at the
active-index horizon K_N with precisely the constants above. They
hold for every possible schedule; integrating the conditioning gives
the unconditional statement. A union bound over the predeclared
calendar checkpoints uses the identical root allocation

    alpha_j = 6 alpha/[pi^2 (j+1)^2],  N=2^j,

split equally among guard, predictable-square and Bernstein events.
The first pair is active with probability one, so K_N is nonzero.

The controller does not receive future activity keys. Conditioning on
them is a proof device, permitted by their independence. This argument
would fail for a duty schedule chosen from current or future ADC data.
For that larger interface one should instead predeclare checkpoints
in the active index, or supply a valid optional-stopping extension.
No such larger schedule is used by this comparison.

## 4. Exact matched implementation and retained reports

The new script imports the unchanged root PacketPort. It has the
same unknown orthogonal mixing, retentions 0.75 and 0.999999, warm
initial coordinates (30,10), and dark coordinate 3. Every native call
obeys the same exact power balance. The input limit is 0.7;
lambda=kappa=0.5; the target is (0.32,-0.24); the first rail is 2.8;
the second rail and replay limit are inherited verbatim. Both ADCs
have 257 levels. No fixture is resized to favour this learner.

The physical RNG and controller RNG seeds are identical to root's.
The script checks that active calendar indices, activity probabilities
and both signs exactly match the saved incumbent record. The same
number and ordering of ADC reads uses the same fresh dither stream.
Commands and therefore material states differ as the optimizer changes.
This is a paired population comparison, not a physical hidden-state
copying operation.

The learner record keeps every command, two ADC outputs, two sign
keys, active/calendar indices, guard flags, rail codes and gradient.
Finite integer ADC codes are retained separately. A distinct auditor
file records actual per-pair saturation counts; the controller is not
given a new analogue saturation sensor. A rail code can also arise
by stochastic rounding without true saturation. No inconvenient
record is excluded or retrospectively downweighted.

Physical time is reported in fixed packet-window units; multiply by
the actual packet duration for a dimensional implementation. Both
idle and active windows, ADC reads, matched-load energy export,
incident energy, calibration, actuation accuracy, randomness and
arithmetic remain paid. No continuing uncharged material bath is
assumed. Existing source/ADC scope limitations are unchanged.

## 5. Execution scope

check_active_pair_learning.py saves ACTIVE_PAIR_LEARNING_CHECKS.json,
ACTIVE_PAIR_LEARNING_RECORD.npz and ACTIVE_PAIR_CLIPPING_AUDIT.json.
The output pins the exact root supplier, certificate proofs and
incumbent result used by the comparison. Assertions check matched
keys, physical power balance, input limits, fresh-read chronology and
absence of reset. One run can verify its execution and realized
certificate; it cannot establish coverage or universal superiority.

The root's stronger decreasing-duty energy theorem is a separate
construction. The finite-record certificate here is already valid
from the bounded active operation and retained guards. No claim about
all future guard encounters or an optimal infinite schedule is
imported before that physical theorem is proved.

## 6. Executed matched comparison

The run completed with the same 262144 calendar pairs, 524288 native
windows, 4815 active pairs, 9630 ADC vector reads and 19260 scalar
reports as the incumbent. It used all 514658 zero-input windows.
The active calendar indices, activity probabilities and both sign
sequences were checked for exact equality with the saved root record.
No hidden reset, outcome exclusion or range change occurred.

| Final quantity | Calendar-index incumbent | Active-index solver |
|---|---:|---:|
| Observed-square gradient radius | 0.9143210 | 0.3927021 |
| Clipping debit in that radius | 0.0819278 | 0.0371995 |
| Optimum-distance certificate | 1.8331484 | 0.7907801 |
| Audited distance to optimum | 0.0025341 | 0.0020637 |
| Audited mean-gradient error | 0.00044785 | 0.00477682 |
| Incident energy | 395.20842 | 391.98756 |
| First/second guard counts | 4 / 1 | 4 / 1 |
| Actual saturated scalar reports, auditor only | 4 | 4 |

Both certificates use the same global checkpoint failure budget 0.05
and the same final allocation 0.00008420043. The active certificate is
below the known feasible-set diameter 1.4, although it remains far
larger than the realized error. The active average command is
(-0.2225365089, 0.1555497095); its audited objective excess is
2.41010e-6. The incumbent has a smaller realized mean-gradient error
on this trajectory. There is no claim of universal statistical
dominance or of a practical speedup from these values.

The source ends with energy 43.8988261 from initial energy 1009,
including the exactly frozen dark energy 9. Total outgoing energy is
1357.0887296; the cumulative identity residual is 6.90e-10 and the
largest single-call residual is 6.98e-14. The maximum actual input
norm 1.961632 stays below the unchanged replay limit 2.179899.
These are population audits, not learner-accessible state information.

The operational improvement is concrete: the same physical record
budget no longer carries 1/p_i digital gradient amplification or a
calendar-time regularizer update unsupported by a new observation.
The real zero-input evolution remains essential and fully charged.

## 7. Binding correction: the zero-call baseline is stronger

Root identified a material missing ordinary comparison after the
execution. Being below the feasible-set diameter does not establish
useful certified optimization on this task. The following comparison
is binding on the interpretation of Section 6 and the initial report.

For the unconstrained ridge objective, the optimum is

    u_* = (A^* A + lambda I)^(-1) A^* b.

Its singular-value multiplier is s/(s^2+lambda). Since

    s/(s^2+lambda) <= 1/(2 sqrt(lambda))

for every s>=0, the supplied task information alone gives

    ||u_*|| <= ||b||/(2 sqrt(lambda)).

Here ||A||<=1, lambda=0.5, ||b||=0.4 and U=0.7. Consequently

    ||u_*|| <= 0.282842712474619 < 0.7.

The unconstrained optimum is therefore inside the actual feasible
ball and is also its constrained optimum. Returning u=0 with no
physical calls deterministically certifies distance at most
0.2828427125. It requires no ADC readings, calibration experiment,
incident probe energy or stochastic failure allocation.

| Operation | Physical windows | Certified optimum-distance bound |
|---|---:|---:|
| Return zero from the declared task information | 0 | 0.2828427125 |
| Executed calendar-index learner | 524288 | 1.8331484282 |
| Executed active-index learner | 524288 | 0.7907800665 |

Thus the active-index implementation genuinely improves the recorded
learning certificate over the calendar-index implementation, but
neither executed certificate establishes a useful certified
optimization gain over this zero-call baseline at the stated budget.
The much smaller audited errors do not repair that certification
comparison: the oracle matrix is unavailable to the learner. The
physical sparse-operation and energy results remain separate from
this failed finite-budget usefulness test. No fixture was rerun,
resized or tuned in response to the correction.

The original reviewed source is retained byte-for-byte at
receiving_versions/ACTIVE_PAIR_INDEXED_BOUNDARY_SOLVER_0b14aa87a1d5.md,
SHA256 0b14aa87a1d5ed394d78c28ec92294b56e9d3b471207f81d1509a4d1924ce3a9.
The execution artifacts are unchanged, including
check_active_pair_learning.py at
64bd1124d87c31b238c405d235eca29ba8da34ed0239a71ca5f2b5da2603a606
and ACTIVE_PAIR_LEARNING_CHECKS.json at
a4011c1d5083e4a5b91326b75d3dc5cc09025dfa92af4eedf48c5a439af1e8ac.
This is a scope correction, not a new numerical result or a change
to the validity of either conservative confidence bound.
