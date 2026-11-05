# FAILED ROUTE: repetition-three arbitrary-gauge suffix export

Status: false; do not use this raw-pool lemma. Counterexample: level-two children 001,000,111 encode zero. A fresh source fault in the first child leading EC changes its second zero; the parent then reads 1,0,1 and returns one despite good descent exRecs. Replaced by strict repetition-five, two refresh rounds, and a fresh physical majority-five decoder tree.

---

# Classical-only protected computation and history-erasing program export

5 November 2026. This closes the classical precursor for the bounded quantum
factory. The accepted static-tree coupling theorem is used, not reproved.
No concatenated quantum code is employed.

## Model and repetition gadgets

All controller registers are computational-basis mixtures. Reset, NOT,
CNOT/copy, Toffoli, bounded Boolean gates, fixed routing and idles have
independent faults of probability at most p per counted location. In the
acquired specialization the same one-qubit Pauli channel follows each
outgoing wire. Z errors do not affect basis registers. Reset is a replacement
map followed by fresh noise, so it erases the old record exactly without
producing a perfect surviving zero. Fanout/read routes and buffer resets
are counted. Native gates have bounded arity.

Use the repetition code 0 -> 000, 1 -> 111, concatenated only on classical
labels. Its EC gadget comprises three separate majority voters. Each voter
has separate buffers for one copy of each of the three input coordinates.
Source coordinates may be copied sequentially, but no voter workspace is
shared with another voter.

The deterministic gadget properties are:

1. A fault-free EC maps any input triple to three copies of its majority,
   and therefore corrects one input-coordinate error.
2. From a clean codeword, one physical fault leaves at most one output
   error. A source/copy fault can spoil several copies of one source lane,
   but each clean voter still has two correct lanes. An internal voter fault
   spoils only that voter's output. A two-output copy fault still affects
   only its one source lane and a buffer in that same lane.
3. Every three-bit output is within distance one of some codeword, giving
   validity on unrestricted classical input. It does not give correctness
   relative to an arbitrarily corrupted input's earlier intended bit.

Thus with r incoming errors and s faults, r+s<=1 gives the correct logical
bit with at most s output errors. **One incoming error plus a further fault
is not claimed to be corrected.** Shared corrections require extended-
rectangle accounting.

NOT, CNOT and Toffoli act transversally on repetition coordinates. A single
input-coordinate error or gate fault produces at most one bad coordinate
per output block. Put EC before and after each transversal gate, sharing
adjacent ECs. Zero preparation is three noisy resets; one preparation adds
transversal NOT. Logical fanout uses protected CNOT into these zero blocks.
All operations are basis preserving at every concatenation level.

## Classical recursive reliability

The distance-three extended-rectangle counting argument applies to these
classical deterministic properties. It is a combinatorial fault-support
argument and does not require a quantum code. A good extended rectangle
has at most one bad lower rectangle. The leading-EC, transversal-gate and
trailing-EC cases above show that it implements its logical Boolean gate
after virtual majority decoding. Assign shared ECs by the usual right-to-
left truncated-rectangle rule. Moving the virtual decoder across each good
rectangle replaces it by the intended Boolean gate; bad rectangles have
at least two independent bad lower rectangles after truncation. This step
is essential: a shared bad EC is not counted twice as independent evidence.

For a fixed constant A exceeding the pair counts, boundary and truncation
factors of the chosen finite gadgets, the recursion is

    p0=p,                 p_(j+1) <= A p_j^2.

The same disjoint witness induction yields local-stochastic joint support
bounds for independent rectangles. For A p<=1/2,

    p_j <= A^(-1) (A p)^(2^j),       sum_j p_j <= 2p.

A finite T-location classical computation can consequently have complete
logical discrepancy delta using j=O(log log(T/delta)) levels and T times
a power of log(T/delta) physical operations. Its outputs remain encoded;
this is not an arbitrarily accurate raw-bit-output theorem. Include all
routing, memory and synchronization locations in T and the gadget costs.

The counting technique is that of Aliferis, Gottesman and Preskill,
*Quantum accuracy threshold for concatenated distance-3 codes*,
https://arxiv.org/abs/quant-ph/0504218 . Here its gadget hypotheses have
been checked for classical repetition; neither its quantum code nor a
quantum input/output interface is run. The argument is uniform in all
correctable incoming classical error patterns and their correlations with
external classical or quantum records.

## Raw-pool export lemma

A protected classical prefix produces an encoded bit b and protected
fanout makes M encoded copies. Charge the total logical prefix discrepancy
delta_prefix once. Each copy then follows a disjoint physical descent
circuit using fresh suffix fault locations. At level j to j-1 a fixed
majority decoder is executed by at most g_dec level-(j-1) rectangles.

Mark output i bad if any rectangle in its descent is bad. For a correctable
incoming encoded copy, unmarked descent produces b irrespective of its
correctable gauge. The tag probability is at most

    q_c = g_dec sum_(j>=0) p_j <= 2 g_dec p.

Different descents have disjoint physical locations, and tags are determined
by fault support independently of b and incoming gauges. Hence for every
set S of raw outputs,

    Pr[all outputs in S are wrong] <= q_c^|S|.

Wrong outputs can remain correlated with one another and with old records;
the required conclusion is the local-stochastic support bound, not their
independence. No copying of an already faulty raw output bit is used.

Do not condition the original fault process on prefix success. Instead use
a hybrid with correct logical prefix, keep arbitrary allowed incoming
gauges and old records, and add delta_prefix to the full cq discrepancy.
The independent-suffix theorem is uniform over those inputs. Every descent
is repetition decoding on basis bits, with its actual gates and links paid.

## Static trees and final program words

The accepted static-tree theorem takes 3^h raw copies per bit. Its voter is
the finite complement-covariant CNOT(a,b), CNOT(a,c), Toffoli(b,c,a) macro;
all wire, voter, reset and storage faults are counted. Let s bound q_c,
edge error e and macro fault probability v. If s<=0.01, alpha=21s<1.
The root is within q_c alpha^h in trace distance of b XOR Z_h, jointly with
b and every old record, where Z_h is independent of that history and has
known reference error r_h=F_P^h(0)<=2s. Disjoint trees have independent
reference root errors. Exact reference leaves are only a proof coupling.

For M_calls factories and at most m roots per factory, take

    h=max(0, ceil(log(M_calls m q_c/delta_tree)/log(1/alpha))).

The total root replacement error is at most delta_tree. Leaf count is
M_calls m 3^h, plus protected fanout/descent. At fixed alpha this is
polynomial in M_calls/delta_tree. Every growing tree is classical.

## A uniform calibration sensitivity bound

Let P,P' be two primitive Pauli laws in the same admitted small-noise
domain, and d_P=TV(P,P'). A full local voter step has g_F primitive
stochastic locations including its incoming wires. Coupling them gives

    |F_P(u)-F_P'(u)| <= g_F d_P.

On the invariant interval 0<=u<=2s,

    |dF_P(u)/du| <= 6(u+e)+3v <= alpha<1.

The first term bounds the derivative of ideal majority with noisy incoming
wires. For a faulty three-input truth table the derivative of its Bernoulli
expectation has magnitude at most three; its probability is at most v.
Complement covariance supplies the same reference error law for both b.
Starting at r0=0 and iterating gives

    |r_h(P)-r_h(P')| <= g_F d_P (1-alpha^h)/(1-alpha)
                      <= g_F d_P/(1-alpha).

For a bounded factory with m reference roots and G local primitive noise
locations, stochastic coupling therefore gives

    ||T_j(P,h)-T_j(P',h)||_diamond
       <= 2 [G+m g_F/(1-alpha)] d_P.

This constant is independent of h. It bounds the simple reference channel,
not the full giant tree; the separate history-erasure discrepancy licenses
the reference replacement. Component acquisition therefore need not gain
a wasteful factor 3^h in its precision requirement.

## Programming, random bits, capture and timing

Known digital target inputs are loaded redundantly by fixed noisy reset/
NOT templates, with programming locations paid. A bit supplied only once
through an unknown raw input has an irreducible input floor; repeatable
known target specification is the contract. This does not assume perfect
final selectors, which are the raw roots handled above.

Fresh fair bits use a constant-size noisy |+> preparation and Z readout.
Every Pauli-conditioned outcome is uniform. Complement-covariant capture
retains this symmetry. Ordinary arithmetic then uses basis-preserving
Boolean gates. A raw measurement bit is captured through level-by-level
classical encoding; bounded copy/zero gadgets incur O(p_j) error at level
j, giving total O(sum p_j)=O(p). Its response is a stable binary affine
channel with nonzero visibility at small p. Opposite-sign idle-ratio
calibration cancels this capture response; ideal record import is not used.

All protected computation, routing and synchronization is prepared before
quantum output initialization. Stagger fixed raw descents/trees so roots
arrive at their prescribed bounded factory slots. Any bounded raw waiting
is included in the wire law. Growing classical routing time is paid; no
free bounded-density realization of a giant tree is claimed.

Reset scratch locally in parallel after its last use. Terminal roots and
selector bits reset inside each padded bounded factory call; data idles
during this are part of its channel. Thus record erasure costs extensive
gates, resets and heat, but never requires a long post-preparation wait.
Old external records can be retained. Fine new program/tree records must
be erased for the averaged-channel claim, or their actual cq extension
must be reported instead.
