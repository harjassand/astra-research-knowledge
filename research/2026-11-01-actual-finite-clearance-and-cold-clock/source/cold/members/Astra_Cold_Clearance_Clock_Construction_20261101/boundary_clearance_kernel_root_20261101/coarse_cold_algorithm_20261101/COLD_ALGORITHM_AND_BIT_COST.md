# A materially coarser cold scalar-and-window algorithm

**Author construction, independent receiving review pending.** The accepted old
fine scalar, its three-run ledger, and the accepted two-fixture windows are not
modified. This is a NEW prospective algorithm and a separate slightly enlarged
receiver. It uses ordinary validated ODE methods. No novelty, wall-time bound,
advantage over ordinary validated/multiscale/retained predictors, or retrospective
research-expenditure speedup is claimed.

## 1. Enabling result and exact scope

Starting with the encoded polynomial ODE and exact initial datum

    e'=2(s+3e^2/4)^2, e(0)=0,

not a stored numerical value of its explosion time, the fixed coarse construction
returns the outward enclosure

    1.106580470126746169 <= s_* <=1.106580556897779284.       (1)

Its exact width is less than 8.678*10^-8, hence much less than the requested
10^-5. The fixed parameters are degree28 forward startup, 80-bit dyadic grid,
order6 inverse Taylor integration, dyadic steps with grid power6, and terminal
inverse coordinate E=16. There are315 steps. Two exact constructor passes agree.
A DIFFERENT rational-endpoint implementation then independently reconstructs
startup, all steps, centering, and the tail, comparing23 mathematical fields.
It imports no constructor code. Its pass is charged too; the first two passes
are accurately described as self-recomputation, not independent implementations.

For the SPECIFIED fixed-input algorithm on a conventional deterministic
multitape binary machine, including the source/data reads, all arithmetic,
control, storage movement, hashing, exact self-recomputation, different-implementation
verification, and BOTH fixture evaluations, the following conservative bound is
available:

    fewer than 3*10^20 elementary bit steps,
    fewer than 2^27 simultaneously stored bits.             (2)

This is an explicit algorithmic upper bound, not measured Python instructions,
a wall-time guarantee, a reclassification of a measured rational-operation
subtotal, or an unpriced retained scalar query. The machine model and counted
operations are specified in Sections4–6. Optional `monotonic_ns` calls and the
`wall_nanoseconds_nonproof` field are OMITTED from the abstract bit algorithm
(the two assignments and that observation field are deleted); neither verifier
nor scientific decision uses them. The reference records this environmental
observation only, with no cost or wall-time inference drawn from it. The Python files are executable exact
reference implementations of the arithmetic algorithms, not claims about the
cost of CPython imports, operating-system scheduling, or storage-device latency.

At N=10^25, the separately accepted successful-path lower bound is at least
2*10^21-1 actual reaction events for a literal event enumerator. Every algorithm
that explicitly emits those events needs at least one bit operation per event
in the same ordinary sequential accounting. Hence (2) is below that event-count
lower bound. This narrow prospective comparison is genuine, but says nothing
about non-enumerative ordinary predictors or samplers, parallel hardware, or
research already spent discovering the proof. The two algorithms have different
outputs: a certified timing INTERVAL versus a complete firing history.

## 2. Completely paid scalar acquisition

The deterministic scalar argument is the ordinary accepted inverse construction,
now evaluated at materially coarser parameters. No previous certificate endpoint
is read. Nonnegative Taylor coefficients construct a degree28 forward polynomial
P on 0<=s<=1/2. The exact residual

    R(s)=2s^2+3sP^2+(9/8)P^4-P'

has zero coefficients below degree28 and nonnegative remaining coefficients;
the program checks this. With L=105/128, delta=R(1/2)/(1-L/2), comparison with
P+delta*s gives a paid positive inverse start and its outward80-bit enclosure.
The upper supersolution is checked below1/4, so no unknown startup datum or
blow-up crossing is imported.

For the inverse equation

    ds/de=1/[2(s+3e^2/4)^2],

the derivative in s is negative. Therefore perturbations of the starting value
cannot increase. At each step the constructor computes the point Taylor series
through order6 and a tube Taylor coefficient of order7. The tube is
`s_center <=s(e)<=s_center+h f(a,s_center)`. Outward dyadic arithmetic encloses
the complete Taylor remainder. The incoming radius is added using inverse
nonexpansivity, not multiplied by a positive Gronwall factor.

The final tail is NOT omitted. For terminal inverse coordinate16, the exact
ordinary two-term bounds are

    t0=8/(27*16^3), U=H+t0,
    t_minus=t0-64U/(135*16^5),
    t_plus=t0-64L/(135*16^5)+128L^2/(189*16^7).

The code verifies 0<t_minus<=t_plus<=t0 and returns [L+t_minus,H+t_plus].
Every division, centering error, startup error, local remainder and tail width
is present in COARSE_CERTIFICATE.json. The fixed first candidate succeeded;
there is no adaptive parameter search or hidden discarded solve.

The constructor is `coarse_clock.py`. The different implementation is
`independent_coarse_verify.py`, using rational interval endpoints rather than
the constructor's integer ticks. It reconstructs the recurrence and all output
fields without importing the constructor. Its initial endpoint and coefficient
facts are earned by its own exact startup, not read from the certificate as
assumptions. INDEPENDENT_COARSE_CHECK.json records the successful comparison.

## 3. Initial source/data and the separate scientific receiver

The finite-window receiver receives the same exact twelve rates, raw count state,
N=10^20 or10^25, and the previously independently accepted SAME-PATH state,
residual, bracket, and actual entropy5 continuation theorems. They are mathematical
components of the fixed problem specification, not noisy experimental inputs or
an unevaluated stochastic oracle. Proving these fixed theorems for the first time
was research; (2) does not assert an algorithm for discovering arbitrary new
stochastic theorems from a network description.

COLD_SOURCE_BINDINGS.json binds36 source/program files, totaling402,781 bytes;
together with that manifest the current read is412,323 bytes. The new pipeline
reads ZERO old numerical scalar certificates, scalar freezes or scalar acceptance
receipts. The old scalar is not hidden in another input: the new numerical center
is obtained solely from the ODE computation in Section2. The code contains no
old decimal scalar constant. The non-scalar source closure and the input law are
paid as bytes, not treated as free I/O.

`coarse_windows.py` hashes and checks the bounded source closure, requires the
fresh scalar and different-implementation verification result, and computes the
two intervals using exact fractions and outward integer square roots. It keeps

    r=.00055+4380/(19T)+7254/T^2,
    v=1449/(800T)+1285200/T^3, j=27/(25T),
    m=2j+sqrt_up(12v+4j^2),
    epsilon=1/T+r+m+3000000/T^6.

The martingale choice has cost2exp(-6)<1/200; the remaining accepted fixture
failures are charged by the same exact elementary inequalities as in the existing
receiver. The strict original4T condition is rechecked using the NEW upper scalar
endpoint. This yields a separate, slightly enlarged99%-confidence candidate:

| N | model-time lower endpoint | model-time upper endpoint |
|---|---:|---:|
| 10^20 | 10358.028789 | 11778.581481 |
| 10^25 | 108894.954785 | 112426.147917 |

The output is the first S<=15(N+2)/16 hitting-time interval, with the original4T
admission and physical/model-time5 continuation. No Gaussian law or finite-N CDF
is claimed. Independent receiving review must approve this new coarse-center
join before it replaces any accepted output. The older accepted window files
remain byte-for-byte unchanged.

The complete prospective algorithm is the fixed sequence:

1. Validate the bounded encoded model/source domain; execute `coarse_clock.py`
   (including its two fixed exact passes).
2. Execute `independent_coarse_verify.py` once on that newly generated certificate.
3. Execute `coarse_windows.py` and emit both new intervals and the finite ledger.

Any failed check refuses; there is NO automatic refinement or retry. Running only
step3 against stored outputs is a retained query, not this cold algorithm.
A standalone postprocessor is not an adversarial-certificate validator: the
complete pipeline creates and verifies its own fresh certificate first.
AUTHOR_FREEZE.json binds ALL THREE implementations, their source closure,
outputs, and this cost specification. No standalone step3 execution is counted
as cold. The new different verifier source is read/hashed by the final consumer
as well as bound by that freeze; its program bytes are included in the I/O and
program-storage budgets.

## 4. Bit-machine and arithmetic bundles

Use a deterministic multitape binary machine with a fixed finite program,
ordinary sequential source input/output, a register-bank tape, and a fixed
number of arithmetic work tapes. Stored rational numerators/denominators and grid endpoints have magnitude
bit length<=2048. Auxiliary integer counters and cumulative-width ledgers may
use up to4096 bits; their only operations are bounded add/compare/shift or
conversion after the final successful enclosure check. Sign bits and array indices are included in the accounting.
Rationals are reduced signed numerator/positive-denominator pairs. Integer-tick
intervals and rational-endpoint intervals are alternative representations of the
same80-bit outward grid; neither implementation receives floating arithmetic.

Set W=8192. This bounds EVERY unnormalized arithmetic work word, not just reduced
stored results. An **arithmetic bundle** is one of the following bounded routines:

* a rational add/subtract/multiply/divide/compare or construction;
* a dyadic interval add/multiply/reciprocal, including endpoint coercions,
  outward rounding, construction, comparisons and result guards;
* a bounded conversion, dyadic coefficient operation, or integer-root step.

For each bundle a deliberately loose implementation ceiling is

    C_bundle=256*(W+1)^3 elementary bit steps.               (3)

Here is why (3) is an implementable ceiling rather than an assigned price tag.
On the fixed multitape machine, the finite control implements a one-bit
full-adder/subtractor truth table in one transition. Addition/comparison/shift
uses at most eight scans of its word, hence <=8(w+1) bit steps. A schoolbook
product scans/adds the appropriately shifted multiplicand once per multiplier
bit; binary long division uses compare, subtract and reposition passes once
per quotient bit. At most eight word scans per outer bit suffice, so multiplication
or binary long division on w-bit words takes <=8(w+1)^2 on the work tapes, with
ordinary copying included. Euclidean normalization takes at most2w+2 remainder
divisions because bit length decreases at least once per two remainders. For
2048-bit stored rational inputs, raw products/sums have <=4097 bits. Thus one
ordinary rational operation, including normalization and quotient construction,
fits well below4*(8193)^3 bit steps.

Each interval routine in the two supplied implementations expands into at most64
such ordinary rational/integer operations, including both endpoint conversions
and guards. Most require far fewer. In the rational-endpoint implementation,
quantization can encounter a temporary numerator of <=4177 bits, but its
denominator is a dyadic power of at most160 bits. Its Euclidean normalization
therefore has at most322 divisions, still within the same elementary ceiling.
Cross-product comparisons have <=4257-bit temporary words. Negative endpoints
only change signs. Hence the entire interval bundle is covered by (3).
All inverse denominators are checked away from zero before reciprocal. The
value w in these elementary bounds includes the length of result/scratch words,
not merely the shorter input operand.

The arithmetic routines are replaceable by these explicit schoolbook routines;
no uncharged unit-cost unbounded integer, oracle integer root, gcd, division,
logarithm, exponential, or fast-multiplication primitive is assumed. The square
root used by the fixture is upward-rounded by binary search on the scaled
integer, with at most1024 iterations under the declared word bounds. Python's
isqrt is only the exact reference implementation of that same result.

### Work-word bounds, including unguarded exact startup expressions

The stored guards are not the entire proof. Let D_n=8^n n!. The exact forward
coefficient p_n has denominator dividing D_n, by induction in the polynomial
recurrence: products of factorial denominators with total index n divide n!.
The scalar supersolution e(s)<=s on[0,1/2] follows from
`2(s+3s^2/4)^2<=121/128<1`. Nonnegative truncated Taylor polynomials are
subsolutions, so p_n<=2^n. A coefficient of P^4 has at most29^3 terms.
For all indices<=112, its reduced denominator divides D_112; residual
coefficients have denominator dividing8D_112 and magnitude less than2^(112+21).
Use112!<128^112. Coefficient numerator/denominator lengths are then below1280.
Horner evaluation at1/2, the factor256/151 in the startup barrier, and the80-bit
outward inverse-start rounding keep all reduced startup results below1536 bits.
This explicitly covers the unguarded `coeff` assembly and every residual-array
accumulation before the later peval guard: their summands have the same displayed
common denominator and finite term-count bound. Partial sums satisfy those same
bounds. Their raw products are below3072 bits. Thus the entire Fraction startup, not merely guarded final
coefficients, fits the2048 stored/8192 work bounds.

`ceilq` multiplies a below1536-bit startup numerator by2^80; its work word
remains below1616 bits. The `s_hi` hitting-time enclosure adds a dyadic80-bit
value and the already bounded P(1/2), divides by the fixed1/2, and stays below
2048 bits. Cumulative local-width ticks are a sum of at most320 nonnegative
2048-bit widths, hence below2058 bits; the auxiliary4096-bit ledger allowance
pays this before any final successful-width check. The rational-endpoint
verifier has the same dyadic common denominator and bound. They cannot grow
unboundedly through repeated normalization. On a successful output the final
width check further bounds these accumulated widths by the final finite
enclosure width. Constructor and verifier arithmetic selftests contain only
fixed small rational inputs and jets of order<=3; their arithmetic and
serialization are included in the per-pass selftest allowance.

Both interval implementations guard the encoded grid endpoints at2048 bits.
Any enabled arithmetic operation on these stored words has the raw bounds above;
if a result exceeds the guard it refuses before another operation can use it.
For this fixed successful certificate no guard fires. Exact tail fractions and
all fixture expressions are below1024 stored bits by their80-bit grid values,
E=16, T<=100000, and fixed exponents<=7. Decimal conversion uses at most1024
output digits per number. No bit-size inference is made merely from a measured
maximum. The observed guarded rational maximum207 bits is diagnostic only.

## 5. Static operation, control, storage and I/O ceilings

There are at most320 inverse steps: at most128 while e<2, and at most64 in each
of[2,4),[4,8),[8,16]. The start is in(0,1), each threshold crossing is handled
by the actual dyadic scale rule, and the last step is clipped. No unsuccessful
step proposal can trigger a hidden retry. The explicit512-step guard is a
secondary refusal guard, not the source of the sharper320 bound.

For one scalar pass, a conservative static bundle ledger is:

| part | bundle ceiling |
|---|---:|
| exact startup, all polynomial loops/conversions/residual checks | 100000 |
| declared interval operations and up to three extra construction/coercion bundles each | 326400 |
| additional scalar/dyadic/bookkeeping arithmetic, <=200 per step | 64000 |
| arithmetic selftests, tail, all checkpoint/decimal conversions | 20000 |
| **one pass ceiling** | **less than600000** |

The dense startup multiply/add count itself is

    2 sum_(k=1)^28[k^2+(2k-1)^2]+2(29^2+57^2)=82128,

leaving margin for every remaining startup expression. At order6 the literal
per-step interval counts are106 adds,134 multiplies,15 reciprocals, totaling255;
thus4*255*320=326400. These formulas hold for the two different interval
representations, and are checked against their exact reported counts. Empty
coefficient slots and loop comparisons are counted, not priced as free.

Three complete passes cost less than1,800,000 bundles. The two-fixture consumer,
all fixed exponential-series inequalities, exact square roots, and verification
comparisons cost fewer than10000 more; even THREE development consumer runs fit
under another30000. The shared conservative bound used in (2) is therefore

    B_total=2,000,000 arithmetic bundles.                   (4)

Control and data movement are separately charged, not hidden in (4). A bank of
4096 arithmetic records of at most8192 bits suffices for the startup arrays,
interval work arrays, checkpoints, counters and metadata. Source bytes are
streamed rather than retained as arbitrarily many arithmetic objects. Including
all byte buffers, program text, output, arithmetic work tapes and verification
copies, reserve2^27 bits of simultaneous storage.

Addressed bank reads/writes may be implemented by a full sequential bank scan,
not a unit-cost random-access assumption. There are fewer than10^9 such accesses
and other outer control actions, allowing500 per charged bundle. A full bank
scan/copy is bounded by2^28 bit steps. This costs less than2.685*10^17 bit steps.
Gcd/long-division inner control stays on local arithmetic tapes and was already
included in (3), not repeated as a bank scan per bit operation.

All input reads are capped. The source closure is capped at2^20 bytes total,
manifest/certificate/verification objects at2^16 bytes each, with64 or fewer
known source paths of at most256 characters. The reference uses bounded reads
before decoding and hashes the frozen manifest before parsing it. Other source
JSON is parsed only after its fixed hash matches, so an adversarial nesting
structure is not silently given unlimited parser work. The fresh scalar and
verification schemas are generated by the preceding bounded phases. The
combined program/source/input/output traffic is conservatively below2^22 bytes.
A literal bit implementation of SHA-256 costs below2^16 bit steps per input byte
by expanding its64 fixed rounds into32-bit Boolean/add/rotate instructions;
streaming/hash work is therefore below2^38 bit steps. A simple bounded-schema
parser/formatter, including decimal repeated division and all verification
comparisons, fits under10^15 further bit steps. Certificate creation/stringify
and exact dictionary/string equality are included: there are fewer than256
scalar fields/checkpoint entries, each integer has at most1024 decimal digits,
and the produced certificate is capped by its fixed schema below2^16 bytes.
The independent verifier reconstructs23 fields and performs its own arithmetic
selftest; the final consumer additionally validates this result and uses the
new endpoints. Neither comparison is replaced by an uncharged Boolean flag. This is vastly above the fixed
files' actual size, but finite and explicit.

Reserve the single combined amount

    C_control+storage_moves+I/O+hash+parse+format <=10^18.    (5)

The counts above sum below (5), including reject paths in the stated bounded
input domain. Source authentication is not treated as free. Storage-device
latency, interpreter startup and human/mathematical proof-discovery effort are
NOT bit-machine operations and are not advertised as covered wall time.

Combining (3)–(5), exact integer arithmetic gives

    2,000,000 *256*8193^3 +10^18
      =282578068509184000000 <3*10^20.                     (6)

This establishes (2). It is not necessary to optimize this generous constant to
obtain the narrow comparison against2*10^21-1 literal events.

## 6. Verification scope, failure history, and old ledgers

RESEARCH_LEDGER.json records every completed NEW numerical run: one constructor
transaction containing two exact coarse passes; one different-implementation
coarse verification; and three tiny receiver runs while bounded-read and
verification requirements were added. Their endpoints agree where comparable.
There were ZERO rejected scalar parameter candidates and ZERO denied/retried
experiments in this branch. All these new numerical runs fit the same generous
bundle reserve in (4); no run is discarded from the record. Editing/reasoning
costs are disclosed as programme development, not misrepresented as numerical
bit-step measurements.

The OLD ledger remains binding history: three ordinary fine acquisition runs,
92,474,955 charged rational operations, a measured subtotal
1,061,126,991,451,094,784 rational schoolbook bit units, conservative acquisition
reserves3*10^27, and the two separate1*10^24 reserves. Nothing in this document
reduces or overwrites them. No fourth old fine solve was performed. No excluded
loading/cache experiment was repeated or mirrored.

The prospective fixed algorithm begins from the encoded law and exact datum;
it need not repeat the programme's historical exploration. That is the same
sense in which a finished SSA implementation need not rediscover its algorithm
on every run. Conversely, if the comparison asks for the TOTAL EXPENDITURE OF
THIS RESEARCH PROGRAMME, the old reserves remain and no speedup against the
2*10^21 event bound has been established. Both statements are retained.

The numerical source proof and static machine ledger require independent
ordinary review. The reference's different-implementation exact check is useful
verification work and is fully priced, but is not by itself an independent
acceptance of the bit-complexity theorem or the scientific join. No physical
preparation, hardware implementation, CDF solver, or superiority over ordinary
validated ODE techniques is acquired.
