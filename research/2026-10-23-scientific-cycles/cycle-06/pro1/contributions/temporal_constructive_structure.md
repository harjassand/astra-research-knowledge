# A guard–meander lower bound for the full temporal operator problem

**Cycle6 constructive contribution.** This note proves a lower bound uniform in
the complete, possibly coherent and entangled, finite bath-prefix state. It does
not replace the operator constraint by a prefix average. It supplies the
load-bearing constructive input to `temporal_operator_dual.md`. Nonlinear
positivity, exact inward drift, and the communication coding consequence are
separate obligations retained by the principal investigator.

## 1. Result and interface

Let \(A=(\mathbb C^3)^{\otimes k}\), let \(Q=\sum_iq_i\) count nonzero
input ports, and let

\[
 \sigma=\rho_c^{\otimes k},\qquad
 \rho_c=\operatorname{diag}(1/2,1/4,1/4).
\]

Use the exact charge-pinched bulk displacement coefficient \(G_1\) defined by
the preserved Cycle5 finite-prefix representation. For an arbitrary density
operator \(\tau\) on that prefix define

\[
 H_\tau=\operatorname{Tr}_{E}[(I\otimes\tau)G_1]+2Q-kI,
 \qquad v_\tau=\operatorname{Tr}(\sigma H_\tau^2).
\]

The partial trace means the Hermitian bath-state contraction. No physical bath
preparation or reachability of \(\tau\) is assumed: it is a dual variable.

**Theorem.** For every \(k\ge3\), and every prefix density \(\tau\),

\[
 v_\tau\ \ge\ \frac14\sum_{r=0}^{k-3}(k-r-2)p_r,
 \qquad
 p_r=2^{-r}\binom r{\lfloor r/2\rfloor}.
 \tag{1}
\]

In particular, for every \(k\ge4\),

\[
 v_\tau\ge \frac{k^{3/2}}{32}.
 \tag{2}
\]

Combined with the separately proved exact closest-point duality
\(\mathcal A_k=(\ln2)\min_\tau v_\tau/8\), this gives

\[
 \frac{\mathcal A_k}{k}\ge\frac{\ln2}{256}\sqrt{k},\qquad k\ge4.
 \tag{3}
\]

Thus the attainable local variational benefit per call is unbounded with
temporal extent. The optimizer supplied by the dual theorem satisfies the
**full operator** drift inequality. Equation (3) alone is not a communication
rate or a nonlinear statement at a fixed nonzero \(\beta\).

## 2. Endpoint-pair representation and orthogonality

Index ports by \(0,\ldots,k-1\). Let \(U_i\) be the edge-reversal unitary on
port \(i\) and the same bath. Define the self-adjoint toggles

\[
 C_i=U_0\cdots U_{i-1}U_iU_{i-1}\cdots U_0.
\]

On a sufficiently deep coordinate core, \(C_i\) changes only the zero/nonzero
bit at port \(i\). It can change earlier color values but restores their
charge bits. Write \(C_i=C_i^++C_i^-\), where the superscript is the change
in total input charge. The inherited finite-prefix identity, equivalently
the toggling expansion proved in `temporal_operator_dual.md`, is

\[
 G_1=[C_-,C_+],\qquad C_\pm=\sum_iC_i^\pm.
 \tag{4}
\]

The same-index terms in (4) sum to \(kI-2Q\). For \(i<j\), the remaining
pair term maps charge pattern \(q_iq_j=01\) to (10) by

\[
 K_{ij}=C_j^-C_i^+-C_i^+C_j^-,
 \tag{5}
\]

and maps (10) to (01) by its adjoint. Every other charge bit is
unchanged. Distinct unordered pairs \(\{i,j\}\) change different pairs of
bits, and therefore their contracted operators are orthogonal in the
\(\sigma\)-weighted Hilbert–Schmidt inner product. More explicitly, if
\(P_z\) projects onto complete binary charge pattern
\(z\in\{0,1\}^k\), a nonzero block \(P_{z'}H_{\tau,ij}P_z\)
requires \(z'=z\oplus e_i\oplus e_j\). Two distinct pairs cannot have
the same ordered pair of input/output pattern blocks. This is an exact
matrix-block orthogonality statement, unaffected by a bath contraction.

Consequently \(v_\tau\) is the sum of nonnegative endpoint-pair
contributions. Within one pair, restrictions to different full input
patterns are also orthogonal. We may retain any selected pattern blocks
to lower-bound it.

## 3. Exact guard–meander word identity

Fix \(1\le i<j\le k-1\), and put \(g=i-1\). Select a complete input
charge pattern satisfying:

1. \(z_g=1\) (the guard);
2. \(z_i=0\) and \(z_j=1\);
3. interpreting the middle bits \(z_{i+1},\ldots,z_{j-1}\) as \(+1\)
   for a colored port and \(-1\) for a zero port, every partial sum is
   nonnegative.

All other charge bits are arbitrary. Condition 3 is a nonnegative
meander, not merely a nonnegative final displacement.

Let

\[
 E=U_{i-2}\cdots U_0,
 \qquad M=U_{j-1}\cdots U_{i+1},
\]

with an empty product interpreted as \(I\). Pure word cancellations using
\(U_l^2=I\) give the exact identities

\[
 \begin{aligned}
 C_jC_i&=E^*\,[U_gU_iM^*U_jMU_g]\,E,\\
 C_iC_j&=E^*\,[U_gM^*U_jMU_iU_g]\,E.
 \end{aligned}
 \tag{6}
\]

Products act on vectors from right to left. These equalities hold on the
whole bath, retaining the vacuum exchange.

A nonnegative meander has a unique decomposition

\[
 D_0\,1\,D_1\,1\cdots1\,D_h,
 \tag{7}
\]

where the \(D_r\) are balanced nonnegative Dyck words and \(h\ge0\) is
the final height. The displayed \(1\)'s are exactly the unmatched
colored pushes. On a fixed Dyck charge pattern, the all-move device
transfers each input color to its matching pop position and leaves the
entire bath unchanged. This follows by stack matching: each zero pops a
color inserted earlier within that Dyck block, and the final stack is
the initial stack. The inverse block restores those input colors and
also leaves an arbitrary intervening bath unchanged. No initial bath
depth is required for this statement.

In each bracketed word in (6), \(M\) and \(M^*\) therefore cancel all
matched Dyck factors of (7), including their input-color permutations.
It remains to follow the \(h\) unmatched middle pushes. Denote the
initial guard color by \(a_0\), the unmatched middle colors in temporal
order by \(a_1,\ldots,a_h\), and the initial endpoint-\(j\) color by
\(a_{h+1}\). Let \(w\) be the arbitrary initial bath word, including the
possibility of the vacuum. The initial reduced local registers are

\[
 (a_0,0,a_1,\ldots,a_h,a_{h+1};w).
\]

The first bracket in (6) has the following action:

\[
 (a_0,0,a_1,\ldots,a_h,a_{h+1};w)
 \longmapsto
 (a_0,a_1,a_2,\ldots,a_h,a_{h+1},0;w).
 \tag{8}
\]

Here and below, when \(h=0\), \(a_1=a_{h+1}\) is the endpoint color
and there are no middle registers. To verify (8), \(U_g\) first pushes
\(a_0\), \(M\) pushes the unmatched \(a_1,\ldots,a_h\), \(U_j\)
pushes \(a_{h+1}\), and \(M^*\) restores the middle registers with the
one-position shift. The remaining stack is \(a_1a_0w\). Then \(U_i\)
pops \(a_1\) into port \(i\), and \(U_g\) pops \(a_0\) back into the
guard. Every pop uses a color pushed by the displayed local word.

The second bracket in (6) instead gives

\[
 (a_0,0,a_1,\ldots,a_h,a_{h+1};w)
 \longmapsto
 (a_1,a_0,a_2,\ldots,a_h,a_{h+1},0;w).
 \tag{9}
\]

Now \(U_i\) immediately pops the guard color \(a_0\), so after the
middle and endpoint operations the remaining stack is \(a_1w\);
\(U_g\) takes \(a_1\). The bath is again exactly \(w\). All matched
middle colors are restored in (8) and (9).

Thus the two bracketed words are input-only color permutations tensor
the identity on the **entire** bath, on the selected local charge
sector. They commute with \(E\), which acts on earlier ports and the
bath. The outer \(E^*,E\) in (6) cancel. This proves that, on every
selected complete charge sector, both \(C_jC_i\) and \(C_iC_j\) are
input-only maps tensor \(I_E\), with the two maps differing by a single
transposition of distinct input color wires.

Define the raw word difference
\(\Delta_{ij}^{\mathrm{raw}}=C_jC_i-C_iC_j\), without charge
raising/lowering restrictions. The preceding whole-bath calculation
proves

\[
 \Delta_{ij}^{\mathrm{raw}}|_{P_zA\otimes E}
       =P(I-S)\otimes I_E,
 \tag{10}
\]

where \(P\) is a color-register unitary from pattern \(z\) to the
endpoint-swapped pattern, and \(S\) swaps the guard wire with the first
unmatched middle wire, or with the endpoint-\(j\) wire when \(h=0\).
Those wires are distinct. Equation (10) is an identity for the
**raw words on the entire bath**, obtained by checking an arbitrary
color basis and an arbitrary bath basis. It extends to coherent bath
vectors and to entanglement with any untouched tail by linearity and
boundedness.

The connection to (5) and \(G_1\) has a different scope. On a
sufficiently deep bulk coordinate core, the raising/lowering
restrictions in (5) select these two raw products. The inherited
finite-prefix identity therefore identifies the selected block of the
**bulk coefficient** \(K_{ij}^{\mathrm{bulk}}\) with
\(P(I-S)\otimes I_{E_k}\), where \(E_k\) is the finite prefix space.
This is not an assertion that the charge raising/lowering
decomposition, or formula (4) for \(G_1\), remains valid at the root.
The root correction in the full displacement is separate.

Consequently the finite-prefix contraction is

\[
 \operatorname{Tr}_{E_k}[(I\otimes\tau)K_{ij}^{\mathrm{bulk}}]
       |_{P_zA}=P(I-S)
 \tag{11}
\]

for **every** density \(\tau\), without a diagonal, product,
permutation-symmetric, or uncorrelated assumption. In particular, no
positive or negative interference from other bath coordinates can
remove this selected contribution.

## 4. Exact color norm and probability counting

If \(q=|z|\) is the number of colored input positions, the color space
of pattern \(z\) has dimension \(2^q\). Under its normalized uniform
color density,

\[
 2^{-q}\operatorname{Tr}[(P(I-S))^*P(I-S)]
 =2^{-q}\operatorname{Tr}(2I-2S)=1.
 \tag{12}
\]

Indeed the swap has trace \(2^{q-1}\): on its two color qubits the
swap trace is \(2\), and the other \(q-2\) qubits are spectators.
Both maps in (10) act between equal-charge sectors, so their
\(\sigma\) weights agree.

The product state \(\sigma\) gives every binary charge pattern
probability \(2^{-k}\), with conditional color state \(I/2^{|z|}\).
For a fixed pair \(i<j\) with \(i\ge1\), the guard and the oriented
endpoint pattern have joint probability \(1/8\). The middle has length
\(r=j-i-1\), and its probability of being a nonnegative meander is

\[
 p_r=2^{-r}\binom r{\lfloor r/2\rfloor}.
 \tag{13}
\]

For completeness, reflection gives the number of nonnegative walks
ending at height \(h\ge0\), of the correct parity, as

\[
 \binom r{(r+h)/2}-\binom r{(r+h)/2+1}.
\]

Summing over \(h\) telescopes to the central binomial coefficient in
(13). Each selected forward block contributes the color norm (12).
Its Hermitian adjoint is the reverse endpoint block and contributes
the same weight. The oriented forward and reverse domains are
disjoint, so this is a genuine factor of two, not double counting.
Consequently

\[
 v_{\tau,ij}\ge\frac14p_{j-i-1}.
 \tag{14}
\]

The remaining pattern blocks are nonnegative Hilbert–Schmidt terms
and can be dropped. Endpoint orthogonality from Section 2 permits
summing (14). For a given \(r\in\{0,\ldots,k-3\}\), there are
\(k-r-2\) choices of \(i\ge1\). This proves (1).

## 5. A uniform power lower bound

The elementary estimate

\[
 p_r\ge\frac1{\sqrt{2(r+1)}}
 \tag{15}
\]

holds for every \(r\ge0\). One proof sets
\(a_m=\binom{2m}m/4^m\) and proves \(a_m\ge1/(2\sqrt m)\)
for \(m\ge1\) by induction: \(a_1=1/2\), and

\[
 \frac{a_{m+1}}{a_m}=\frac{2m+1}{2m+2}
 \ge\sqrt{\frac m{m+1}}.
\]

Even \(r=2m\) then satisfies (15); odd values follow from
\(p_{2m+1}=p_{2m+2}=a_{m+1}\); \(r=0\) is immediate. In (1),
\(r+1\le k\), so

\[
 v_\tau\ge\frac{(k-2)(k-1)}{8\sqrt{2k}}
 \ge\frac{3}{64\sqrt2}k^{3/2}
 >\frac1{32}k^{3/2}\quad(k\ge4).
 \tag{16}
\]

The second inequality uses \((k-2)(k-1)\ge3k^2/8\), valid for
\(k\ge4\). This proves (2) without a limit exchange or a fixed-\(k\)
constant hidden in the lower bound.

## 6. Why weaker premises fail

The guard and the nonnegative path condition perform different jobs.
The word \(011\), endpoints \(i=0,j=2\), satisfies the nonnegative
middle condition but has no preceding guard. One toggle order changes
an original bath color; therefore the guard cannot simply be omitted.

Conversely, keep the guard but replace the path condition by positive
final displacement. Take \(100111\), endpoints \(i=1,j=5\), so the
middle is \(011\): final height \(+1\), but its first partial sum is
\(-1\). Give the four colored inputs distinct labels \(I_0,I_3,I_4,I_5\)
and let the bath start \(B_0B_1\cdots\). Then the exact two orders are

\[
 \begin{aligned}
 C_jC_i &: (I_3,I_0,0,I_4,I_5,0;B_0B_1\cdots),\\
 C_iC_j &: (B_0,I_0,0,I_4,I_5,0;I_3B_1\cdots).
 \end{aligned}
\]

One restores the bath; the other exchanges its top color with an input
color. Thus positive final displacement is insufficient even with the
guard present. These are failures of the stated sufficient identity,
not assertions that every excluded word has zero useful drift.

Uniform prefix averaging is also insufficient to infer the full
operator optimum. The preserved \(k=4\) computation has nonconstant
operator drift after uniform averaging. A Laplacian certificate on a
symmetric prefix and a conjectured quadratic variance law are useful
diagnostics, but neither is used in (1)–(3). The proof instead retains
the full dual bath-state minimization and exhibits input-only
subblocks that survive every bath state.

## 7. Executable evidence, limits, and receiving use

`temporal_constructive_structure_guard_replay.py` executes the exact
symbolic stack permutations with distinct input and bath labels. It
checks the guard/meander identity, unchanged bath, the precise
two-wire transposition, and an omitted-premise counterexample on a
bounded family. Its JSON receipt records the actual range, counts,
runtime and memory. The completed replay covered 639 selected pattern-pair
sectors and 2,556 symbolic configurations for \(3\le k\le8\), using both
vacuum and deep bath words and both seeds. It took 0.023829981 seconds,
with 10,112 KiB peak resident memory in this run. This is a verification
aid, not the proof of the all-\(k\) theorem.

Earlier diagnostic files `temporal_constructive_structure_probe.py`
and its receipts evaluate exact leading finite-prefix coefficients
through \(k=6\). They motivated, but are not premises of, this theorem.
The unproved stronger conjecture suggested by those diagnostics is
quadratic growth of the optimum. No such conclusion is claimed here.

**Receiving use.** Combine (2) with the sibling closest-point theorem
to choose its full-operator optimizer \(X_k\). Use its proved uniform
norm bounds when controlling input positivity and the nonlinear
remainder for a block size selected as a function of the fixed device
parameter. Then prove exact negative bulk drift with the root
remainder retained, and invoke the inherited arbitrary-reference
coding interface. The selected block size is fixed before the coding
horizon. Only that completed chain can convert this contribution
into an improved small-angle communication theorem.

This note establishes neither a general capacity converse nor a
feedback conclusion, a useful blocklength, an efficient compiler, a
laboratory capability, an externally accepted result, or historical
priority. The total discovery and review costs are unknown; the
replay cost is recorded separately.
