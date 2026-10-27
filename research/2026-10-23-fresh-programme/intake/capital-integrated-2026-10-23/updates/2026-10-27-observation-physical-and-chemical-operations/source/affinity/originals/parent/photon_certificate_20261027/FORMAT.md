# Frozen JSONL interface v1

`photon_certificate.py INPUT.jsonl [-o OUTPUT.json]`; use `-`/stdin for a pipe.
The standard-library implementation reads one block at a time, waits for EOF,
and outputs a single exact-rational JSON result. No result is issued for a
prefix of a longer stream. Exit0 means a valid conditional result or UNKNOWN;
exit2/INVALID_INPUT means no certificate. An internal programming error is not
silently converted into a statistical conclusion.

First line: the JSON object in header.example.json, written on ONE line. Replace
its explicit nonphysical test metadata only with the user's own supplied record
and contract references. All header fields are mandatory. Rational quantities
are integers or finite rational strings, such as "3/5". Decimal strings are
also exact rationals. JSON floating numbers, booleans in integer/rational
fields, NaN/Infinity, duplicate keys, unknown fields and malformed records are
rejected. `sqrt_bits`>=1 selects relative dyadic arithmetic enclosure precision;
it does not alter the statistical confidence allocation. The natural logarithm
is conservatively upper bounded by ceil(log2(32/alpha_stat)), proved with e>2.
Poisson bounds use the fixed Taylor degree cutoff+1, not a data-tuned degree.

N>=2 and both cutoffs are positive integers. `lambda_on` and `lambda_dark`
each contain two NONNEGATIVE externally acquired upper bounds on conditional
total count means PER RECORD. The on cap applies to each of a,b. They are not
observed-count bounds. Per-channel block dominator means are2*lambda_on+
lambda_dark. The reader does not acquire or validate these envelopes.

`alpha_stat` is in(0,1). Every `alpha_other_total` entry is a nonnegative TOTAL
DATASET failure bound, not per-record. `budget_scope` must be TOTAL_DATASET.
The sum of all failure budgets must be<1; the output displays1 minus that sum.
All capture, initial preparation, coupling, readout/coder or other failure
events must be included unless the supplied contract grants them exactly.
Empty/zero other budgets are not a claim that such operations were acquired.
The example has total1/50 failure and conditional confidence49/50 (98%).

The analysis frequency is an exact rational in cycles per supplied time unit;
physical event phase is exp(2*pi*i*frequency*time). The file contains NO timestamp
transcendental evaluations. Instead a fixed supplied coder gives rational
per-event [real,imag] pairs of norm<=1, with a supplied uniform complex error
bound eta>=0 relative to that phase. The scalar eta is added once to complex
mean disks and2*eta to covariance disks. Its physical clock/coder qualification
is SUPPLIED. Gate, capture, fixed coder, frequency, N and cutoffs must have been
chosen before the records. A header/hash only fixes this reader execution;
it does not establish historical precommitment or protect post-data reruns.

Each next line is exactly this block shape (indices0 throughN-1, consecutively):

```
{"kind":"block","index":0,
 "bright_a":[{"count":2,"phasors":[[1,0],[0,1]]},
             {"count":1,"phasors":[[1,0]]}],
 "bright_b":[{"count":1,"phasors":[[-1,0]]},
             {"count":2,"phasors":[[0,1],[0,-1]]}],
 "dark":[{"count":1,"phasors":[[0,1]]},
         {"count":1,"phasors":[[-1,0]]}]}
```

The displayed whitespace is for reading; each block is one JSONL line. Exactly
two channels are required per record, with the declared count equal to its
phasor array length. Zero photons means count0/phasors[]. Every phasor is
checked even in a subsequently clipped block. If the sum of a,b,d counts in
EITHER channel exceeds its cutoff, the ENTIRE block's eight coordinates are
zeroed. Count equals cutoff is retained. Blank/extra/truncated/reordered lines
are rejected, including any extra record beyond N.

For retained blocks, M_i=((Y_i^a+Y_i^b)/2-Y_i^d)/K_i,
D_i=Y_i^a-Y_i^b, and W_ij=D_i conjugate(D_j)/(K_i K_j).
The fixed order is ReM1,ImM1,ReM2,ImM2,W11,W22,ReW12,ImW12.
Their range lengths are2,2,2,2,1,1,2,2. Thus the target is
m_i=(mean bright_i-mean dark_i)/K_i and
C_ij=2*Cov(Y_on)_ij/(K_i K_j); these positive rescalings preserve the affinity
operation. Means/covariance share records; joint disks use a union bound,
never a spurious independence assumption between estimators.

Results are always CONDITIONAL_ON_SUPPLIED_CONTRACTS; data_kind is retained.
UNKNOWN means no positive bound at the supplied budgets/precision, not evidence
of equilibrium. A positive result contains exact rational rlo_squared,
Amax_squared_lower=36*rlo_squared/(1-rlo_squared), and a lower rational square
root as `affinity_lower`; pi>3 is enough. rlo_squared>=1 is UNKNOWN with an
inconsistent-geometry reason, never clipped into a spectacular bound.
Amax's units are dimensionless maximum microscopic simple-cycle LOG RATE RATIO.
Thermodynamic entropy per traversal additionally needs local detailed balance;
this is not an entropy-production rate. No physical or IID qualification is
inferred from counts, maxima, hash, byte transport or software-test success.
