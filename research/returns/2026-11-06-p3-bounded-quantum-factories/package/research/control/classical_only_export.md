# Classical-only protection and history-erasing export

5 November 2026. This corrected construction uses strict repetition FIVE, TWO refresh rounds per EC, and a fresh physical majority-five decoder tree. It supersedes the false arbitrary-gauge repetition-three export preserved in failed_repetition3_export.md. No quantum code is used.

## 1. Model and physical refresh

Controller registers are computational-basis mixtures. Native reset, NOT,
CNOT/copy, Toffoli, Boolean circuits, fixed routes and idles have independent
faults of probability at most p per counted location. In the acquired
specialization the same one-qubit Pauli law follows every outgoing wire.
Reset is replacement followed by fresh noise. All ancillas, routes, storage
and programming count. Quantum references may correlate with the classical
labels and remain untouched.

Repetition-five encodes b as bbbbb. A refresh uses five separate voter
workspaces. Every voter receives separate copies of all five source lanes
and executes a fixed finite majority-five Boolean circuit. Voters share
neither internal gates nor buffers. A source/copy fault can spoil several
copies of ONE source lane. A fault within one voter affects only ONE output.
Physical routing must preserve these incidence properties. Native majority
can be replaced by a finite NOT/CNOT/Toffoli circuit confined to its voter.

A clean refresh maps every input word to its repeated majority. With <=1
incoming error and <=1 fault, any clean voter sees at least three correct
inputs: a source fault adds at most one lane to the existing bad lane.
A faulty voter spoils only its own output. The refresh therefore leaves
<=1 error relative to b. Simultaneous incoming-error/fault tolerance is
the spare distance missing from repetition three.

## 2. Two rounds earn arbitrary-input validity

EC comprises TWO successive refreshes on fresh separate buffers. With at
most one fault it has both properties:

* On arbitrary input it outputs within one error of some codeword. A fault
  in round one is cleaned by fault-free round two. A fault in round two
  receives a clean codeword from round one and leaves at most one error.
* On input within one error of bbbbb it outputs within one error of bbbbb,
  even with one fault. A faulty first round leaves <=1 error and clean
  second round removes it; a faulty second round receives a clean input.

A rectangle consists of leading EC on every input, transversal Boolean
gate, then trailing EC on every output. Adjacent ECs are NOT shared. One
transversal fault affects one coordinate per output. Known-bit preparation
uses five noisy reset/NOT templates followed by EC.

With <=1 fault, a rectangle maps arbitrary inputs to valid outputs. If a
leading EC is faulty, only its block has <=1 coordinate error, removed by
clean trailing correction. A transversal fault is likewise corrected. A
fault in trailing EC sees a clean input and leaves <=1 error. On inputs
with <=1 error per block the same argument preserves the intended logical
Boolean outputs, despite one fresh fault.

A good CNOT with a valid-zero target also normalizes an arbitrary source
to one valid value and copies that SAME value to the target. Leading EC
selects a source value (preserving regular inputs), then the transversal
gate and trailing correction preserve the two common logical outputs.
This property prevents unrelated values on repeated reads of one invalid
source during recursive correction.

## 3. Strict hierarchical regularity and reliability

A level-zero bit is regular. A level-(j+1) block is regular of value b
when at least FOUR of its FIVE children are level-j regular of value b;
the remaining child can be arbitrary. A clean parent has all five children
regular of one value. Two arbitrary children are not admitted, even if a
majority decoder would happen to return b. This strict invariant is needed
by the export below.

Replace each native operation by an unshared lower-level rectangle. A
higher rectangle is good when it contains <=1 bad lower rectangle. Induct
simultaneously on validity, logical correctness for regular inputs, and
the common-value copying property of Section 2. More precisely, a good
gadget has input-selective semantics: each invalid input may be normalized
to a chosen bit by its private leading EC, while every regular input keeps
its value; outputs are regular with the Boolean function of those chosen
inputs. An invalid source is never treated as a perfectly accessible
already decoded bit.

In a refresh with no bad lower rectangle, the first good copy normalizes
each arbitrary source child to one regular value. Subsequent copies keep
that value. All voters see the same effective input word and the output
parent is clean. One bad lower rectangle in the copy phase corrupts only
one source lane and its buffers; one within a voter corrupts only that
voter's output. For regular input, four source lanes began regular b, so
even an additional faulty lane leaves three correct lanes per clean voter.
The lower good Boolean rectangles normalize invalid buffers and compute
the correct majority. Hence refresh with <=1 bad lower rectangle preserves
regular b. On unrestricted input a bad first refresh is cleaned by the
second; a bad second refresh follows a clean first output. These give the
two EC properties at the next level. The leading/transversal/trailing
cases prove the next rectangle properties, including common-value CNOT.
The physical lane/voter proof is the base of this induction.

Let g bound the number of lower rectangles per unshared rectangle,
including routing and idle padding, and let A>=binom(g,2). Badness needs
two bad lower rectangles with disjoint fault regions. Thus

    p0=p,       p_(j+1)<=A p_j^2,
    p_j<=A^(-1)(A p)^(2^j),       sum_j p_j<=2p if A p<=1/2.

Disjoint witness counting gives joint support bounds for disjoint rectangles.
There is no shared-EC truncation. A T-operation classical computation has
complete logical discrepancy delta using j=O(log log(T/delta)) levels and
T times a power of log(T/delta) physical operations. All programming,
arithmetic, random bits, storage, routing and synchronization are counted.
Outputs remain strict hierarchical repetition blocks.

This is the classical specialization of spare-distance concatenation with
validity, rather than the distance-three exRec interface. The distinction
is explained by Aliferis, Gottesman and Preskill, Sections 1 and 10,
https://arxiv.org/html/quant-ph/0504218v3 . Their quantum code and flawless
measurement postprocessing are not run here; the gadget induction and
physical export are specified separately on classical registers.

## 4. Fresh physical majority-five export

The protected prefix computes b and fans it out into M strict regular
level-j blocks. Charge its total logical discrepancy delta_prefix once.
Each block is consumed by its OWN fresh physical majority-five tree. Its
leaves are the actual stored classical bits, and each node uses an actual
fixed noisy majority-five macro. Edges and voters have fresh independent
faults. There are O(5^j) nodes and j stages. No protected downconversion or
ideal decoder is inserted.

Define tags from fresh fault support only: leaf tags are zero; a parent is
tagged if its macro is faulty OR at least TWO of its five children have a
tag or faulty incoming edge. The definition uses all five children and does
not consult which old child is exceptional. With edge probability e and
macro-fault probability v,

    q_0=0,       q_(l+1)<=v+10(q_l+e)^2.

For s=max(e,v)<=1/200, the interval q_l<=2s is invariant because
s+90s^2<=2s. Hence the root tag probability q_c<=2s=O(p), independent of j.

An untagged parent of a strict regular-b subtree returns b. At least four
old child subtrees are regular b; at most one child has a fresh tag/edge
fault. At least three received bits are therefore b, and the clean macro
returns b. Induction proves this uniformly over every old strict gauge,
including the arbitrary exceptional subtree.

Disjoint copy trees have disjoint fresh fault regions. Their tags are
independent of all old bits, gauges and records. Wrong output requires its
tag, so for every subset S of raw outputs,

    Pr[all outputs in S are wrong]<=q_c^|S|.

This is the required LS raw pool; the wrong-bit events themselves need not
be independent. No faulty raw bit is copied M times. Use a hybrid with
correct logical prefix and arbitrary allowed regular gauges, adding
delta_prefix once; do not condition the original noise law on success.
Uniform fresh-tag correctness makes this valid with all old records.

At j=O(log log(T/delta_prefix)), 5^j is a fixed power of log(T/delta_prefix).
Copy storage, decoder trees, reset and routes are paid. Blocks remain
protected until decoder launch; raw stages then run on fixed clocks with
all delays included in the edge law.

## 5. Accepted ternary history-erasing trees

Use 3^h raw copies per bit in the accepted static ternary tree. Its finite
complement-covariant voter is CNOT(a,b), CNOT(a,c), Toffoli(b,c,a). Let s3
bound q_c and the ternary tree's edge and macro probabilities. For
s3<=0.01, alpha=21s3<1. The root is within q_c alpha^h in trace distance
of b XOR Z_h, jointly with all old records; Z_h is fresh independent error
with r_h=F_P^h(0)<=2s3. Reference errors from disjoint trees are independent.
Perfect leaves exist only in the coupling.

For M_calls factories and m program bits per call choose

    h=max(0,ceil(log(M_calls m q_c/delta_tree)/log(1/alpha))).

Total history discrepancy is delta_tree. Raw-leaf count is M_calls m 3^h,
before classical protected-copy and physical five-ary decoder costs. All
growing registers and trees are classical.

## 6. Reference-root calibration sensitivity

For admitted primitive Pauli laws P,P', a local ternary voter step has at
most g_F primitive stochastic locations. Coupling them gives

    |F_P(u)-F_P'(u)|<=g_F TV(P,P').

On 0<=u<=2s3, its derivative in u has magnitude at most
6(u+e)+3v<=alpha<1. Ideal majority supplies the first term; a faulty
three-input Boolean truth table has derivative magnitude at most three.
Starting at r0=0 and iterating,

    |r_h(P)-r_h(P')|<=g_F TV(P,P')/(1-alpha),

uniformly in h. Therefore a bounded factory with G native stochastic
locations and m reference roots has diamond sensitivity at most

    2[G+m g_F/(1-alpha)] TV(P,P').

This is a forward bound on the simple reference channel, not on the giant
physical tree. The separate history-erasure discrepancy permits the
reference replacement; calibration need not acquire parameters to precision
inverse in the full number of tree nodes.

## 7. Programming, capture and timing

Known digital target data are loaded redundantly by noisy reset/NOT
templates with programming locations paid. An unknown raw bit supplied
once retains an input floor. Known/repeatable target specification is the
task; actual final selectors use the noisy roots above.

Fresh fair bits use constant-size Pauli-noisy |+> preparation and Z readout.
Every Pauli-conditioned outcome is fair and becomes classical immediately.
Capture it with complement-covariant classical encoding, then apply a final
level-j EC. The EC's arbitrary-input validity gives strict regular output
except on its bad event of probability p_j, charged to prefix discrepancy.
Earlier logical flips do not bias this coin: conditional on every fixed
fault pattern, complementation of the uniform raw bit complements the final
logical value. This earns unbiased protected random seeds without demanding
an arbitrarily accurate raw classical input port.

For a calibration probe bit whose actual value matters, level-by-level
encoding uses bounded protected copy/zero circuits with O(p_j) interface
risk at level j. The total O(sum p_j)=O(p) capture error is a stable affine
binary response with nonzero visibility. A final high-level EC gives strict
regularity. Opposite-sign idle-ratio calibration cancels the response; no
ideal record import or growing coherent controller is used.

An explicit complement-covariant MAJ5 uses anchor a. Apply CNOT a into
b,c,d,e, making four difference bits. XOR their threshold-three function
into a. Its algebraic normal form is

    bcd XOR bce XOR bde XOR cde XOR bcde.

Four triple-controlled NOTs cost three Toffolis each; one four-controlled
NOT costs five, using two reset ancillas. Thus four CNOTs and seventeen
Toffolis, plus reset/idles, suffice. After the difference phase a is only
a target, so every fixed intervening bit-flip pattern preserves global
complement covariance. All seven wires and every slot are paid. A safe
constant C5 such as 200 covers this serial macro's outgoing/reset/idle
fault locations before additional routing; use its actual complete count
when adding a hardware-specific route.

Growing computation/routing occurs before quantum initialization. Launch
raw copy decoders and ternary trees at fixed staggered clocks so their
roots arrive at the bounded factory slots. Include bounded raw waits in
the acquired wire law. Keep the supplied paid links and actual latency;
there is no free bounded-density realization of a growing tree.

Reset scratch locally in parallel immediately after last use. Terminal
roots/opcodes reset inside padded quantum calls, whose idles include reset
and release. Erasure costs extensive gates/resets/heat, with no long final
wait after preparation. Old external records remain. Fine new records
must be erased for an averaged-channel claim, or their actual cq extension
must be reported.

