# Independent audit: strict five-bit classical protection and raw export

This note repairs the failed repetition-three export claim. It concerns only
classical basis information. It never introduces a growing coherent quantum
code. The main compiler can incorporate these statements directly.

## 1. The invariant must be stronger than arbitrary correctability

Let `V_0(b)={b}`. Recursively, `V_j(b)` consists of five-child words with at
least four children in `V_{j-1}(b)`; the fifth child is completely arbitrary.
The two sets `V_j(0),V_j(1)` are disjoint. Call a word *coarsely clean* when all
five children belong to the same `V_{j-1}(b)`.

Do not substitute the full two-error-correcting set of the repetition-five
code. The spare error margin is essential. A majority-three recursive code
with one old bad child has no spare margin for a fresh error in another child;
the supplied `001,000,111` counterexample exposes precisely that defect.

Native operations are fixed bounded-input/output classical Boolean gates,
bounded fanout, preparations and charged wire/idle locations. Faults are
independent or obey the stipulated local-stochastic support bound. Gates act
only on their assigned wires; a consumed input is not an uncharged unlimited
fanout resource. Majority-five can be a bounded classical subcircuit; all its
internal faults are charged.

## 2. Refresh and the needed strong induction statement

One refresh `R_j` distributes each of the five child bits to five columns using
a separate bounded fanout row. Each column then computes majority-five using
private workspace. These are complete level-(j-1) classical gadgets.

Use two refreshes `E_j=R_j R_j`. Surround every transversal logical Boolean
gate by separate input `E_j`s and separate output `E_j`s. No adjacent gadgets
share an error-correction region. This includes logical fanout gadgets.

The correct induction statement is **input-selective normalization**:

- For a good gadget and arbitrary encoded inputs, each input is normalized to
  some classical bit, and outputs lie in strict `V_j` blocks for the Boolean
  function of those chosen bits.
- If a particular input was already in `V_j(b)`, its chosen bit must be b.
- For logical fanout all its output blocks have the same chosen input bit.
- A good gadget means at most one bad immediately lower-level gadget. At the
  physical level, good means no physical fault.

This is stronger than simply assuming an arbitrary invalid input has a
well-defined decoder label. It is what permits a bad lower gadget's arbitrary
row outputs to enter otherwise good majority columns.

### Refresh correctness

For an input in `V_j(b)`, a single bad lower gadget in a fanout row can corrupt
one row of a column in addition to the one old arbitrary row. At least three
inputs to every unaffected majority column remain valid b. Input-selective
normalization preserves those three bits, so majority is b regardless of the
other two. A bad majority-column gadget can corrupt only that output child.
Thus one refresh with one bad lower gadget still produces `V_j(b)`. With no
bad lower gadgets it produces a coarsely clean word.

### Refresh validity on arbitrary input

If all row fanouts are good, each arbitrary input child is normalized once to
some bit and copied consistently to all five columns. All good majority
columns therefore compute the same majority. An entirely good refresh gives
a coarsely clean word even from arbitrary input.

If the one bad lower gadget occurs in the first refresh, the second entirely
good refresh cleans its arbitrary output. If it occurs in the second refresh,
the first gave a clean word and refresh correctness applies. Therefore `E_j`
maps arbitrary inputs into `V_j` under one bad lower gadget, while preserving
the bit of every initially strict valid input.

### Gate correctness and validity

Consider the complete unshared input-EC / transversal-gate / output-EC gadget.
If its one bad lower gadget is in an input EC, that input becomes strict valid
and every other input EC is coarsely clean. At most one child position can
therefore give a wrong transversal result, and the clean output EC corrects
it. If the bad lower gadget is in the transversal gate, all input ECs were
clean, and again at most one child position is damaged. If the bad gadget is
in an output EC, it follows a clean transversal result. The same reasoning
works for every output of a bounded fanout function. It proves the strong
input-selective statement simultaneously with EC validity.

These arguments require private voter workspace and explicit row fanout, not
an unspecified gadget that can mutate unrelated stored inputs.

## 3. Reliability and actual prepared copy pools

Let L bound the number of lower-level locations in any complete classical
gadget, including its unshared ECs, idles, reset and routing primitives. A bad
level-j gadget then requires at least two bad level-(j-1) gadgets. For
`A>=binom(L,2)`, the usual disjoint-region recursion gives

`q_j <= A q_{j-1}^2`, hence `q_j <= (A p)^(2^j)/A`.

Choose a fixed physical rate below this explicit gadget threshold and choose
level `j=O(log log(K/delta))` for a K-location classical computation/fanout
prefix. Its total bad-gadget probability is at most delta. On the complement,
all requested logical output copies are in strict `V_j(b)` for the intended
classical bits, including every fanout copy. Their gauges may be arbitrarily
correlated with each other, the computation history, and retained records.
The raw export below tolerates exactly those correlations.

This is classical protection only. Its encoded word sizes, time, wire count,
fabrication, synchronization and reset grow and remain paid. No assertion of
a convenient numerical threshold follows without counting the chosen native
classical gadgets and links.

## 4. Plain majority-five export: no level-down idealization

For each requested copy block, recursively decode all five children with
disjoint fresh physical classical majority-five trees and take their majority.
Use fresh links and gates after the prefix; different copy trees are disjoint.
The decoding tree has O(5^j) nodes and depth O(j), all classical.

Define a fresh failure tag without looking at the old gauge: a node is tagged
if its local voter has any fault, or at least two of its five child/edge
subtrees are tagged. If the node is untagged and its old block is in `V_j(b)`,
then at most one child is old-arbitrary and at most one more child has a fresh
failure; at least three child outputs equal b. The actual voter outputs b.

Writing v for voter-macro fault probability and e for the incoming link bound,
the pure-fault tag law satisfies

`r_0=0`, `r_{k+1} <= v + 10(r_k+e)^2`.

For `s=max(v,e)<=1/90`, the interval `[0,2s]` is invariant. To supply pools
with parameter at most .01, choose the native rate so `s<=1/200`. This is a
fixed classical hardware condition independent of computation size or desired
accuracy.

Conditioned on any old physical word, gauge or retained record, the new tag
events of distinct copy trees are independent and have probability at most
2s. Actual wrong output bits are a subset of the tags. Thus for every set S
of raw copies,

`Pr[all outputs in S wrong | prefix success] <= (2s)^|S|`.

The bad-prefix probability delta is charged once. This is the required actual
raw local-stochastic pool. Its tags need not be observable. No final raw bit
is asserted to have vanishing error. The accepted ternary history-erasure
tree can now act on this pool, with its floor and execution costs retained.

## 5. Actual logical randomness without an ideal bit port

A bounded Pauli-noisy `|0>` reset, H, Z-measurement template yields an exactly
fair raw classical bit: conditioned on every Pauli fault pattern the measured
state is an X eigenstate, and a readout bit flip preserves the fair law. Fresh
templates give independent raw bits. All shots, resets and capture are paid.

Prepare an independent uniform raw word of length `5^j` and apply `E_j`. On
the good-gadget event its arbitrary-input validity produces `V_j(B)` for a
well-defined bit B. If refresh primitives are complement covariant, global
complementation of the uniform input word flips B for every fixed fresh fault
pattern, so B is exactly fair. Good tags depend only on faults. Disjoint coin
blocks therefore yield independent fair logical bits, up to the paid global
bad-prefix event. Their gauges may be correlated with their values; the
strict-invariant/export proof already allows that.

An explicit complement-covariant majority-five circuit uses an anchor a.
Compute the four differences `a xor b,a xor c,a xor d,a xor e` using CNOTs.
Then XOR into a the predicate that at least three differences are one. Its
algebraic-normal-form is

`bcd xor bce xor bde xor cde xor bcde`.

Four triple-controlled NOTs and one four-controlled NOT implement this using
two reset ancillas; standard classical Toffoli decompositions use at most
seventeen Toffolis, in addition to the four CNOTs. With seven wires and a
serial schedule, a conservative constant such as 200 counts outgoing faults,
idles and reset. The quantum state stays classical throughout. Under global
complementation only the anchor changes after the difference stage; thereafter
it is only a target. Every fixed bit-flip pattern preserves that covariance.

This closes random sampling inputs without assuming a perfect raw sampled
bit or a noiseless final selector. General input data still obey the declared
classical source/access contract and their transfer errors remain paid.
