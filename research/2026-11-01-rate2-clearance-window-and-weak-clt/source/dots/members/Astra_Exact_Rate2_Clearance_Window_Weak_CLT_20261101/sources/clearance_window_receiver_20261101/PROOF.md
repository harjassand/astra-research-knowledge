# Ordinary proof of the executable clearance-window receiver

**Author receiving-code candidate; independent whole-code review pending.**
This is an ordinary mathematical/program audit, not a proof-assistant artifact.
No source theorem is expanded by this program. Its only model is the exact
rate-2 tree with falling factorial A(A-1), unit-rate 0↔A, the specified two-body
reversible reactions and coefficient two only for CD→AE. Initial state is
(A,B,C,D,E)=(0,N,1,1,0), so initial **total is N+2**, not N. The target is the
first actual S≤15(N+2)/16 time. The result is a confidence window, not a
point-mass approximation in CDF/KS/TV distance.

## 1. Scientific authorities and executable input

SOURCE_BINDINGS.json binds the exact accepted finite-level source `e0700bad…`,
analytical continuation `0eeb3110…`, dyadic stage `0ddcfb78…`, its first-crossing
and band-priority receiving conventions, scalar freeze and independent receipt,
explicit harmonic source `4d1ad7a9…`, and explicit clearance replacement
`9465869a…`. The harmonic receipt is `6ce86803…`, its audit `2c04e65a…`, and
final join receipt `823c1e2c…`. All final qualifications were read. The manifest
is hash-pinned in receiving code; it is not an editable user authority list.
The replacement removes precisely the old c(ε),n0(ε) acquisition gate. It does
not remove the large K,N,δ,h conditions or any probability cost.

The external input is a bounded flat ASCII JSON object with exactly nine fields,
all strings: schema, model, N, K, a_num, a_den, error_num, error_den, work_budget.
Schema is 1; model is `exact_rate2_corner_clearance_v1`. Integer strings are
canonical unsigned decimals with positive value; denominators are nonzero.
Limits: 16,384 bytes; N at most 2,048 digits; K at most 128; rational components
at most 64; work budget at most 32 digits and at most 10^31. Model/schema and
flat grammar are checked before integer conversion. Unknown/duplicate fields,
nesting, booleans, bare numbers, NaN, escapes, Unicode, signs, leading zeroes,
overlong data and invalid rates all return UNKNOWN. No global parser limit is
changed. Main reads at most 16,385 bytes. Source reads are likewise capped.
The exact externally requested model, N, K, a and failure tolerance determine
all tests; they are not recovered from a self-asserted result certificate.

This first version admits **only exact fifth-power N**. All other N return
UNKNOWN. The arithmetic accepts integer K, using conservative square-root
bounds rather than requiring square K. There is no simulation or reaction
expansion. No exponentially sized denominator is materialized.

## 2. Roots and all source hypotheses

Binary integer-root search maintains lo^k≤n<hi^k, starting from zero and
2^ceil(bit_length(n)/k), with a possible exact upper endpoint. Each midpoint
is tested exactly; every rejected candidate is counted, not free. Final explicit
checks establish r^k≤n<(r+1)^k. For N the receiver requires r^5=N and sets T=r.
For K+1 use r_ceiling=r+1 if r²<K+1, otherwise r; set

- p=K+1;
- q_hat=2r_ceiling+1≥2√(K+1)+1;
- H_hat=p+q_hat+1≥p+2√(K+1)+2.

All affected inequalities and positive error prefactors increase with q,H, so
these ceilings are adverse, never favorable. Required tests are literally

N≥10^200, K≥10^40, 0<a≤1/4,
T²≥16H_hat, T³≥64p², aT²≥4pq_hat,
KT≤δN, δ=10^-100, h=1600δ^-2, N≥32h.

The program additionally checks δN≥4, m0=δ/2≤10^-6, N≥200000,
KT/(3·10^12)≥1, the dyadic delay <T and the full 4T+h time envelope.
The joined proof already earns the actual macro entrance
(1-δ)N≤S≤(1+δ)N, M=A+min(C,D)≥δN/2, hence the harmonic theorem's literal
3N/4<S≤5N/4 and M≥m0N. No arbitrary already-macro upper overshoot is inferred.
The source size condition is exactly N≥12800/m0²=N≥51200δ^-2=32h.

## 3. Exact probability receiving

The polynomial clock price is the rational upper bound

C=10^5 H_hat^6/(a^6 T).

Eight remaining terms are each independently upper-bounded by 2^-40. They are:

1. 36H_hat³T³ exp(1-KT/64): paid actual fast-A cap.
2. P(Pois(4T+h)>δN/2-2): ONE original immigration counter over the full horizon.
3. 32 exp(-KT/(3·10^12)): all dyadic common-good-event failures, including
   clocks, event counts and stopping boundaries.
4. P(Pois(40000√δ)≥ceil(δN)): actual lower-band death count; not false clearance.
5. 32N²h exp(-δN/2000): harmonic lower-barrier entry excursions.
6. exp(-200N²/(32h+20/3)): acquired actual A-occupation martingale event.
7. exp(-N/2): actual death-clock lower count.
8. exp(-N/96): harmonic original immigration, including all unused physical wait.

For P≥1 integer, b=bit_length(P) gives P<2^b (P=1 uses b=0). For x≥0,
e^-x≤2^-floor(x), since e≥2. Thus the integer test floor(x)≥b+40 proves
P e^-x≤2^-40. For term 1 the exponent is x=KT/64-1; that explicit +1 is not
lost. Term 6 is represented as 600N²/(96h+20), exactly the displayed value.
The floor exponent may have thousands of bits but only that **integer** is
constructed, never 2 raised to it or an exponential approximation.

For X~Pois(λ), Chernoff with θ=log 2 gives
P(X≥r)≤exp(λ-r log 2)≤exp(λ-r/2). Here log 2≥1/2 follows, for example, by
integrating 1/t≥1/2 on [1,2]. Therefore use x=r/2-λ in the same bit test.
For strict immigration, the exact integer threshold is
r=floor(δN/2-2)+1=floor(N/(2·10^100))-1, valid even for nonintegral δN.
For the band count r=ceil(N/10^100) and λ=40000/10^50 exactly.
No assumed independence, floating logarithm, numerical Poisson summation or
unpriced truncation appears. All event intersections use a union bound.
The sole probability output is C+8/2^40, checked against the **external**
requested error. Double-charging conditional immigration only weakens it.
Optional occupation outputs are **not** emitted: their separate prices were
not silently included in this window-only request.

## 4. Scalar and actual time receiving

The independent scalar receipt certifies rational sL≤s_*≤sU from the frozen
fine certificate, not merely its decimal endpoints. This program verifies those
bytes and the receipt bindings. Runtime readback is not called a fresh ODE solve.
A separate metered independent coarse+fine replay is preserved and charged.
No scalar solve at K=10^40 is needed.

The accepted continuation proves
0<s_*-s_K≤√3/[9(K-2)^(3/2)]. For K≥4,
K³≤27(K-2)³ (indeed K/(K-2)≤2 and 8≤27), so β_K≤K^-3/2.
With r=floor√K>0, b=1/(Kr)≥K^-3/2 is a rational upper bound. The program
checks the squared polynomial inequality too. From the accepted actual window

(s_K-a)T≤τ_clear≤(s_K+a)T+32T/K^(3/2)+h

and the scalar interval it follows that

max(0,sL-a-b) T ≤ τ_clear ≤ (sU+a+32b)T+h.

Every term, including beta replacement, dyadic delay and h of actual physical
service, is retained. Since s_K<2 and 2+a+32b≤4, all physical activity lies
inside the charged original [0,4T+h] immigration horizon. The harmonic endpoint
is at the **end** of service even if a mass hit occurs earlier, so unused time
is paid rather than dropped. Since 13N/16<15(N+2)/16, actual clearance has
occurred by that endpoint. Exact rational physical and normalized endpoints
are output; decimal endpoints are independently rounded outward using integer
floor/ceiling. The displayed 18-place interval may hide tiny positive terms,
but the rational output never omits them.

## 5. Work and bit charges — conservative, not unit-cost arithmetic

The receiver uses ordinary exact integer roots, rational arithmetic, certified
scalar Taylor integration and elementary Chernoff/bit comparisons. No novelty
or universal solver lower bound is claimed.

For the bounded schema, N has at most 6804 bits and K at most 426 bits. N² and its fixed
prefactors have <15000 bits. The clock fraction, source endpoints and final
physical fractions have <5000 bits; their cross-products remain below 32768.
All mathematical intermediate integers are thus bounded by **32768 bits**.
This is a proven conservative ceiling, not a claim that the sparse recorded
maximum catches every Python temporary. The result separately reports recorded
operand/result maxima and root/comparison counts.

Each of three root searches has fewer than 1400 iterations for admitted inputs;
each uses a bounded-degree power, comparison and fixed number of bookkeeping
operations. Fixed post-root arithmetic has fewer than 1000 rational operations.
Parsing the bounded external object, reading/parsing the fixed 159-file manifest
payload set, all rejects, rounding and bookkeeping are conservatively bounded
by 10^7 high-level arithmetic/control operations. A primitive on B-bit integers
can be implemented with ≤256(B+1)^3 elementary schoolbook bit steps, covering
addition, multiplication, division and Euclidean gcd normalization. Rational
operations reduce to a fixed number of such operations; degree-six or lower
powers are bounded products. At B=32768 the resulting bound is <10^24, the
receiving reserve. No CPython wall-time upper guarantee is inferred from this
abstract bit model. Hash/scan I/O is charged separately at 2^20 bit steps per
byte, with at most 2MiB sources plus 16KiB input. This covers SHA256 compression,
scan and fixed-shape decoding without treating acquisition as free.

The scalar acquisition is separate. Repaired `meter_replay.py` verifies the exact
independent checker bytes and executes `compile` of THOSE SAME bytes in a fresh
module namespace, bypassing both caller module caches and on-disk pycache.
Verified certificate/source bytes are supplied through immutable text snapshots.
The two historical acquisition runs predated this loading repair; no claim is
made that their original loader had the repaired execution provenance. A third,
ordinary coarse+fine acquisition has now run to completion under the current
repaired code; it is the final SCALAR_ACQUISITION.json, with code SHA51bf3b65…. Its Fraction
subclass preserves exact results and charges rational primitives, startup,
self-tests and both coarse/fine solves. The first measured run had 30,824,985
charged rational operations, max conservative temporary width 1618 bits and
353,708,997,150,364,928 rational schoolbook bit charges. Fine/coarse interval
operation counts still exactly match their original certificates. The second
historical rerun agrees on all mathematical and arithmetic count fields. The
loading repair changes no scalar arithmetic. After the repair, one ordinary
third acquisition completed, with all mathematical/count fields exactly matching
both historical runs and the current code hash recorded. It charged 30,824,985
rational operations and 353,708,997,150,364,928 rational bit-work units, max1618
temporary bits; observed runtime136.265528930s is nonproof metadata. No new
non-numerical experiment accompanied this final numerical replay. A future
optional fresh replay compares all mathematical/count fields and current code
hash, but no fourth acquisition has been run for this deliverable.

The total acquisition **reserve is 10^27**, not the measured rational subtotal.
It covers at most 10^8 charged rational calls and at most 100 times that many
integer/control operations on ≤65536-bit values, as can be bounded directly
from the fixed-degree, fixed-step loops; 10^10·256·65537³<10^27. This includes
all exact-fraction startup and parsing/normalization work excluded from the
original solver's narrower interval-operation ledger. Counter metadata and
SHA/readback are absorbed in this deliberately loose reserve. The extra integer
and control charge is the remainder of that total after the measured subtotal,
not a second total being silently dropped.

Two historical acquisitions are preserved with **two separate 10^27 charges**.
The first had the same mathematical results but lacked an explicit pre-import
hash pin and had an ambiguous metadata label for the total reserve. The second
had that pin but retained the subsequently discovered bytecode-loading defect.
Neither is hidden or substituted for the final repaired-loader execution. There are no rejected
adaptive ODE refinements in either run; all rejected binary-root candidates
are charged. Previous human proof discovery and unrelated historical research
are not represented as fully measured algorithmic work.

The independently discovered loading defect, preserved in the historical freeze
and ACQUISITION_LOADING_AMENDMENT.json, was that SourceFileLoader could execute
unbound timestamp-valid bytecode even after the .py file had been hashed.
The loader-only repair/regressions receive a further conservative 10^24 charge.
Verifier and replay wrappers likewise pin admit.py and compile the SAME verified
byte string; a repaired optional acquisition executes verified meter bytes via
an isolated subprocess stdin, not a second pathname load.

The external work budget must cover 3·10^27+2·10^24 plus the maximal source/input
scan allowance before roots are allocated. The sample requests 10^30. For a
reusable certified-input execution, the ledger still exposes all three acquisition
charges rather than silently amortizing them. Observed nanoseconds are explicitly
nonproof metadata and not guaranteed runtime. UNKNOWN inputs incur only their
performed bounded work; the reserve fields are ceilings, not claims those
operations ran.

## 6. Concrete fixture and honest comparison

N=10^1300, K=10^40, a=1/20, requested error 10^-6 has T=10^260,
b=10^-60 and h=1600·10^200. N is 4319 bits. The rational C is slightly above
6.4·10^-8 because H is rounded upward; C<10^-7. All eight remaining gates pass.
The exact total is outward-bounded by **0.000000064007275958**, below 10^-6.
The normalized window has outward 18-place endpoints
**[1.056580521912579472, 1.156580521912579663]**.
This is near [s_*-a,s_*+a] with all literal correction terms retained.

N=100,1000,10000 each return UNKNOWN before roots. Ordinary SSA is a strong
baseline there. No measured SSA benchmark or superiority over all numerical
solvers is asserted. N=10^1300 is a theoretical encoded-input example, not a
practical chemical population. The severe conservative theorem constants and
large work reserves are visible. Encoded-input, offline scalar-acquisition and runtime costs are distinct from
physically preparing N molecules or implementing this reaction model. No
physical source preparation or practical hardware advantage is established.
No installation, publication, hardware or operational chemistry action occurs. Morrey is outside this task.
