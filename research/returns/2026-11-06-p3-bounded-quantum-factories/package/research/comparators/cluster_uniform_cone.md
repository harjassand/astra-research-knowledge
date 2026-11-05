# An explicit all-length entangled Gibbs factory at fixed component noise

Research construction, 5 November 2026. This is a finite-constant companion to
the general channel-interior compiler. It uses the accepted noisy classical
history-erasure tree and the accepted stationary Pauli acquisition contract.
It does not use the large universal Gibbs block length or the abstract polymer
positivity constant. Its new positivity proof is a small transfer-matrix cone.

The companion script `cluster_cone_certificate.py` checks its constants using
exact rational arithmetic and independently reproduces both a positive small
instance and the useful negative preimage at the larger rate `p=1/200`.
Finite-chain tests are not the all-length proof.

## 1. The delivered family and its quantum character

On an open chain, let

\[
 U=\prod_{i=0}^{N-2}CZ_{i,i+1},\qquad
 K_i=UX_iU^\dagger.
\]

The target is

\[
 H=-\sum_i J_iK_i,\qquad
 \rho_{\beta}=\frac{e^{-\beta H}}{\operatorname{tr}e^{-\beta H}},\qquad
 t_i=\tanh(\beta J_i)\in(1/2,11/20].                 \tag{1}
\]

This is a connected finite-range commuting quantum Gibbs family, not a tensor
product in the physical site basis. It includes inhomogeneous couplings.
In the graph basis `|G_s>=UZ^s|+>^N`, its label law is

\[
 \pi(s)=\prod_i\frac{1+t_i(-1)^{s_i}}2.             \tag{2}
\]

Every nontrivial cut is entangled. Across the cut `(i,i+1)`, the two restrictions
of `K_i,K_{i+1}` on either side anticommute and square to identity. The two
expectation values on either side of a product state have Euclidean norm at
most one. Cauchy--Schwarz and convexity therefore give

\[
 \langle K_i+K_{i+1}\rangle\le1
\]

for states separable across that cut, while (1) has value `t_i+t_{i+1}>1`.
This proves cut entanglement; it does not assert genuine multipartite
entanglement under every decomposition. Thermal graph states, their ideal
source, and these stabilizer representations are established machinery.

## 2. A fully specified finite quantum schedule

All classical sampling, reliable computation, local-stochastic fanout, and
root regeneration occur before output qubits are reset. The quantum schedule
then has these six data fault layers:

1. Reset each output cell to `|0>`.
2. Load its actual raw classical root bit through an always-scheduled CNOT.
3. Apply H at every site.
4. Apply CZ on `(0,1),(2,3),...`, including an idle on an unmatched last site.
5. Apply CZ on `(1,2),(3,4),...`, with boundary idles.
6. Execute the specified local delivery/terminal idle slot.

Every outgoing data wire in every layer has an independent depolarizing Pauli
fault: `I` with probability `1-p`, each of `X,Y,Z` with probability `p/3`.
The component parameter is stationary and may be unknown before acquisition.
The loading control is an actual noisy bit. Its reference law is independent
BSC(`q_i`), obtained from the classical tree below; its actual departure from
that reference law is charged in the final error budget. The last control
storage/transfer exposure is assigned to the tree link or root, not omitted.

No gate pattern, active bond, output address, or quantum route depends on the
sample. All nearest-neighbor bonds are fixed. Thus a wrong sample bit cannot
join blocks through an erroneously activated mask. There is no dynamic block
mask in this architecture.

The circuit-location model is substantive. Unmodelled coherent crosstalk,
missing CZs, long-memory drift, or incorrectly addressed quantum gates are not
Pauli depolarization and are not covered by this special finite-constant
theorem. The general channel-menu construction addresses a broader local
apparatus class. Here the declared layout and synchronization are fixed, with
their paid physical fault locations included.

Each gate module has bounded quantum size, the quantum depth is fixed, and
every newly reset data qubit has bounded coherent lifetime until delivery.
The output has N qubits and can be entangled across the whole chain. This is
a bounded-module fabric, not permanently quantum-isolated factories.

## 3. Exact label channel

Put

\[
 c=1-4p/3.
\]

A depolarizing Pauli fault on a two-generator syndrome subgroup `G` induces

\[
 D_G(c)=c I+(1-c)\Pi_G,\qquad
 \Pi_G=\frac14\sum_{g\in G}T_g.                  \tag{3}
\]

Here `T_g` translates graph labels by XOR. For N at least two, the relevant
two generators are independent. At early singleton locations the induced
label bit-flip channel has nontrivial Fourier eigenvalue c.

The first three fault layers each give a singleton label channel at every
site. After the first CZ matching, a fault on either endpoint of a pair has
syndrome generators `e_i,e_j`. The two endpoint channels therefore compose
to `D_{ij}(c^2)`. An unmatched odd last site instead has one extra singleton
factor c.

After the second CZ matching the graph is complete. A fault at site i has
generators

\[
 e_i,\qquad e_{i-1}+e_{i+1},                    \tag{4}
\]

with missing neighbors omitted. The second-matching and terminal fault layers
therefore give `D_{G_i}(c^2)` at every site. This follows by conjugating a
Pauli through the remaining Clifford circuit; Pauli convolution of graph
labels is standard and is also explicit in the primary graph-noise source
listed below.

All label convolutions commute. Consequently the preimage of (2) can be
analyzed by first inverting the singleton factors and root BSCs, then the
pair factors, then the remaining factors (4).

## 4. Coarse pairs and exact inverse coefficients

Group sites into consecutive pairs `(0,1),(2,3),...`, with one final singleton
when N is odd. Invert all singleton label channels first. The resulting
product polarizations are

\[
 u_i=\frac{t_i}{c^3(1-2q_i)},
\]

except the unmatched odd last site has `c^4` in its denominator. Define the
uniform bound

\[
 u_*:=\frac{11/20}{c^4(1-20p)},\qquad q_i\le10p. \tag{5}
\]

For every pair, combine its first-matching inverse with any endpoint factors
(4) wholly contained in that pair. The resulting forward pair factor is
`D_pair(a_j)` with `a_j=c^2,c^4`, or `c^6` (the last case occurs at N=2).
The local preimage distribution is exactly

\[
 f_j(x)=a_j^{-1}\pi_{u_{2j}}(x_1)\pi_{u_{2j+1}}(x_2)
       -\frac{a_j^{-1}-1}{4}.                  \tag{6}
\]

It is normalized. It is positive if

\[
 (1-u_*)^2>1-c^6.                              \tag{7}
\]

For every such pair its ratio of largest to smallest value is at most

\[
 R:=\frac{(1+u_*)^2-(1-c^6)}{(1-u_*)^2-(1-c^6)}.\tag{8}
\]

The final singleton has the positive distribution `(1±u_i)/2`; its value
ratio is smaller than R. Formula (8) is conservative for ordinary interior
pairs, since their actual parameter is `c^2`, not `c^6`.

The remaining two factors (4) at each boundary between coarse blocks form a
link. Each individual inverse has coefficients

\[
 D_G(a)^{-1}=\alpha I-\beta\sum_{g\ne0}T_g,
 \quad a=c^2,
 \quad\alpha=\frac{3+a}{4a},
 \quad\beta=\frac{1-a}{4a}.                    \tag{9}
\]

In particular `alpha-3 beta=1`; this identity is checked in the receipt.
For the product of two such inverses, write its translation coefficients as
`b_j(z)`. Its identity coefficient is positive and satisfies

\[
 b_j(0)\ge\alpha^2,\qquad
 \frac{\sum_{z\ne0}|b_j(z)|}{b_j(0)}
 \le\zeta:=6r+9r^2,
 \qquad r=\frac{\beta}{\alpha}
          =\frac{1-c^2}{3+c^2}.                \tag{10}
\]

For an ordinary two-pair boundary the two rank-two subgroups intersect only
at zero, so identity is exactly `alpha^2`, the six single-factor terms have
coefficient `-alpha beta`, and the nine double-factor terms have coefficient
`beta^2`. At the final pair/singleton boundary some translations coincide.
The identity gains only positive double-factor terms, and the triangle
inequality can only decrease the bound (10). This handles odd-N endpoints
without adding an ideal boundary gate.

## 5. The all-length cone proof

Let `z_j` denote the finite link translation at coarse boundary j. Its
restrictions to the adjacent blocks are denoted `L(z_j)` and `R(z_j)`. The
complete preimage of the physical noise channel has the exact signed tensor
form

\[
 \mu(x_1,\ldots,x_m)=
 \sum_{z_1,\ldots,z_{m-1}}
 \prod_{j=1}^{m-1} b_j(z_j)
 \prod_{j=1}^{m} f_j\bigl(x_j\oplus R(z_{j-1})\oplus L(z_j)\bigr),
                                                        \tag{11}
\]

where missing links equal zero. Every link has at most sixteen translations.

Suppose a real forward message obeys

\[
 v(0)>0,\qquad\sum_{z\ne0}|v(z)|\le\kappa v(0).\tag{12}
\]

For one block, let `m_j=min f_j`, `M_j=max f_j`, so `M_j/m_j<=R`. The new
message is

\[
 v'(z')=b_j(z')\sum_z v(z)
 f_j\bigl(x_j\oplus R(z)\oplus L(z')\bigr).
\]

Direct triangle inequalities give

\[
 v'(0)\ge b_j(0)m_j(1-\kappa R)v(0),
\]

\[
 \sum_{z'\ne0}|v'(z')|
 \le b_j(0)\zeta M_j(1+\kappa)v(0).            \tag{13}
\]

Choose `kappa=1/(2R)`. Then (12) is invariant whenever

\[
 \boxed{\zeta\le\frac1{4R^2+2R}}.              \tag{14}
\]

Indeed `1-kappa R=1/2>0`, and (14) is exactly
`zeta R(1+kappa)<=kappa(1-kappa R)`. Start with `v(0)=1` and all other
entries zero. At the last block the final scalar is at least
`m_m(1-kappa R)v(0)>0`. Thus (11) is strictly positive for every complete
label string and **every chain length**. Every inverse preserves total mass,
so it is a probability law. This proof does not truncate an expansion or
infer infinite-length positivity from numerical chains.

For N=1, the graph has no bond. All six fault layers induce singleton channels;
the positive preimage polarization is `t_0/[c^6(1-2q_0)]<1` at the numerical
range below. N=2 is covered by the positive pair (6) without transfer links.

## 6. A concrete fixed nonzero quantum-fabric rate

For

\[
 \boxed{0\le p\le1/3000,\quad 1/2<t_i\le11/20,
        \quad 0\le q_i\le10p,}                \tag{15}
\]

(7) and (14) hold. At the worst endpoint,

\[
 u_*=0.5546767098966332\ldots,\quad
 R=12.340233768365868\ldots,
\]

\[
 \zeta=0.001333777711875619\ldots
 <0.0015777699898645605\ldots
   =\frac1{4R^2+2R}.                           \tag{16}
\]

The receipt evaluates these as exact rational inequalities, not floating-point
comparisons. As p increases, `u_*`, R, and zeta increase while the right side
of (14) decreases; therefore checking the endpoint proves the entire interval.
The strict margin also permits slightly larger certified design bounds or
small numerical uncertainties, but no larger hardware claim is made here.

The quantum-fabric component rate is about 0.033 percent in this specified
stochastic model. A complete operation also obeys the threshold of the actual
reliable-classical compiler used to produce its local-stochastic copy pools.
If that compiler has certified threshold `p_cl`, a common-rate apparatus uses
`p<=min(1/3000,p_cl)`. Alternatively the quantum rate can reach `1/3000` while
classical components have their own fixed rate below both that rate and
`p_cl`, with the corresponding classical parameters separately acquired.
No classical reliability threshold at `1/3000` is inferred from the cone proof.
The explicit quantum rate is much larger than the abstract polymer certificate for the same circuit
and avoids the universal mixed-block constants. It is not a threshold for
arbitrary hardware noise and is not a demonstrated laboratory operating point.
At `p=1/200`, `q_i=p`, `t_i=11/20`, N=8, the exact inverse has three negative
entries, including a minimum about `-2.6064e-7`. This retains the useful failed
route: even this simple architecture cannot be advertised as admitting
arbitrarily high fixed noise by formal inversion.

## 7. The actual noisy classical loading boundary

Use the accepted static ternary-tree history eraser on actual local-stochastic
copy pools from a protected *classical* computer. No output qubit is reset
until those pools, trees, and sample are scheduled for use. The last voter is
scheduled during the fresh-data reset slot, and its output immediately
controls the next-slot loading CNOT at an adjacent fixed port. There is no
extra raw root idle or outgoing routing link in this six-slot schedule. A raw
root is not left waiting for the long classical computation. Any additional
deployment exposure must be included in its actual law.

For a concrete voter, the classical reversible circuit `CNOT(a,b)`,
`CNOT(a,c)`, `Toffoli(b,c;a)` retains majority in a. Its seven outgoing wire
locations have independent bit flips of probability at most p, so the macro
fault probability is at most `v=7p`. Each fault-conditioned truth table is
complement covariant, as established in the accepted tree theorem. A tree
link has bit-flip probability at most `e=p`. These are classical basis bits;
this operation does not require a coherent quantum Toffoli factory.

In the independent reference process, root error r obeys the bound

\[
 F(r)\le 7p+3(r+p)^2.
\]

Starting from exact reference leaves, the interval `[0,10p]` is invariant,
because `7p+3(11p)^2<=10p` throughout (15). Thus the actual reference root law
has the promised `q_i<=10p`; it is not supplied as an ideal physical bit.
The reference exact leaves occur only in the proof coupling.

For example, one extra noisy root transfer still admits `q_i<=10p` after
rechecking the bound with eight voter-equivalent fault sites. Then (18) uses
`90p<=.03` and (19)-(20) use eleven local fault sites rather than ten. The
numerical cone certificate is unchanged, since it only uses `q_i<=10p`.

Let `q_leaf` be the actual local-stochastic pool parameter and
`s=max(q_leaf,e,v)<=.01`. The accepted tree coupling gives error at most

\[
 \epsilon_{tree}\le N q_{leaf}(21s)^h           \tag{17}
\]

at depth h, jointly with all pre-existing records and arbitrary references.
All upstream protected-classical failures are charged separately. The tree
has `3^h` leaves and O(`3^h`) classical gates/links per delivered bit, so this
is a paid polynomial classical overhead. It does not turn a single bad raw
bit copied many times into a valid local-stochastic pool.

The graph-label sample and controller history are correlated with the output.
They may be retained as that explicit cq extension. For a delivery contract
excluding such accessible records, their storage, reliable reset and erasure
are charged, including any decoupling error from the actual reset operation.
The proof does not silently declare a correlated transcript harmless.

## 8. Explicit finite-bit sampling

Equation (11) is a signed transfer network of dimension at most sixteen with
a fixed finite local alphabet. The positive preimage exists by the cone proof.
One may compute prefix marginal masses and sequentially sample with an
ordinary classical algorithm. Numerical precision must still be controlled;
positivity of the final result alone does not license unstable division.

A robust independent bit-cost construction is as follows. Approximate both
child masses of every visited prefix to absolute accuracy delta, clip negative
numerical child masses to zero, and normalize; if both are zero, use any coin.
For true nonnegative child masses a,b and clipped approximations a',b', each
within delta, normalization satisfies

\[
 (a+b)\,d_{TV}\left(\frac{(a,b)}{a+b},
                         \frac{(a',b')}{a'+b'}\right)\le2\delta.
\]

The same bound holds when the approximate denominator vanishes. Summing the
sequential hybrid bound over at most `2^j` prefixes at layer j yields total
sampling TV error at most `2^(N+1) delta`. Set
`delta=epsilon_s/2^(N+3)` and budget the remaining error for rounded coins.

The absolute sum of signed transfer terms is at most `A^(c_0 N)` for fixed
constants A and `c_0`; each inverse has bounded l1 norm. Hence
`b=O(N+log(N/epsilon_s))` bits, with explicit O(N) guard bits, suffice for all
contractions. A simple implementation uses O(`N^2`) constant-size arithmetic
operations; cached suffix messages reduce this to O(N). Either gives ordinary
polynomial bit complexity. Computable fixed-temperature coefficients and
finite-precision elementary functions are included. This conclusion is
independent of the numerical convention in the general Gibbs source theorem.

## 9. Acquisition without a hidden tree-size precision penalty

Use the accepted constant-quantum-size stationary Pauli assay to acquire the
homogeneous component rate p, with its actual preparation, noisy readout,
classical capture, contrast visibility, repeated shots, and resets paid.
For a finite collection of stationary component types, acquire each type;
without such a finite-template model the acquisition count must grow with the
number of independently unknown components.

The reference root probability is computed from the actual finite voter truth
table. Its sensitivity does not grow with h. On `[0,10p]`, the accepted
general faulty-voter derivative bound gives

\[
 |F'(r)|\le6(r+e)+3v\le87p\le.029.             \tag{18}
\]

Changing all local homogeneous component probabilities by eta changes one
voter-plus-three-links update by at most `10 eta`, since that template has at
most ten independent bit-fault sites. Therefore the recursive root law changes
by at most

\[
 |q_i-\widehat q_i|\le\frac{10\eta}{1-.029},    \tag{19}
\]

uniformly in tree depth. This is a forward recursion bound. The high-depth
classical computation itself is protected to its separately assigned error
budget; its exact fault distribution need not be simulated.

Let the positive preparation law be computed for estimated parameters in the
certified design interval. Couple the actual and estimated quantum circuits
forward from that same positive input law. Their six N quantum fault locations
and N roots give

\[
 d_{TV}(K\widehat\mu,\widehat K\widehat\mu)
 \le N\left(6+\frac{10}{1-.029}\right)\eta.      \tag{20}
\]

Thus eta of order `epsilon/N` suffices, despite the many classical tree nodes.
The inverse's extensive condition number is not inserted into (20). Ordinary
independent bounded-output assay estimates require O(`(N/epsilon)^2
log(1/delta_acq)`) shots for the homogeneous finite-parameter model, with
the assay visibility constant retained. A finite-precision p estimate can be
clipped to a *prior certified* design interval; clipping does not manufacture
an upper noise certificate for an uncertified device.

The explicit two-rate bridge and sharper forward statistical bound are in
`../forward_metrology.md`. Quantum data wires may have one unknown stationary
depolarizing rate `p_Q<=1/3000`, while classical basis wires have an independent
unknown stationary flip rate `p_C<=min(p_Q,p_cl)`. The actual reference roots
obey `q_h<=10p_C<=10p_Q`, with height-uniform Lipschitz constant `10/(1-.029)`.
Quantum idle contrasts acquire `p_Q`; opposite-sign classical preparations,
zero/one classical idle and the same actual protected capture give
`m_t=A_C(1-2p_C)^t`, acquiring `p_C` with preparation/capture visibility
cancelled and all acquisition costs paid. This is a finite-template bridge,
not identification of arbitrary heterogeneous hardware. Holding the same
estimated positive source law fixed in both forward experiments, relative
entropy of their independent fault histories gives an `O(N/epsilon^2)` shot
bound on fixed positive certified rate intervals, with the lower-rate and
visibility constants retained. The TV-coupling bound above is the
boundary-safe quadratic fallback. No inverse amplification is used.

## 10. Final accuracy and complete costs

For every desired epsilon and acquisition failure probability delta, choose
budgets whose sum is at most epsilon for classical sampler discretization,
protected classical computation, tree coupling, calibration-induced forward
error, and record reset if required. With probability at least `1-delta`, the
delivered quantum marginal has half-trace distance at most epsilon from (1).
For graph-diagonal states this is exactly the label-law TV distance.

Quantum hardware has O(N) output cells and nearest-neighbor couplers, fixed
ancilla size per module, six fixed data fault layers, and no quantum code whose
size or duration grows with N or epsilon. Every calibration shot also has
bounded coherent quantum size and duration. Classical computation, copies,
tree size/depth, protected storage and routing, synchronization preparation,
reset, and metrology grow and are all paid. Fixed-port simultaneous delivery
is the endpoint; long holding or a growing-distance quantum transfer would be
another operation and cannot be appended for free.

The six layers count data preparation, not all quantum activity. Under the
uniform-raw-word logical coin construction in `classical_five_block_audit.md`,
a level-j logical coin uses `5^j` bounded-size quantum `|+>`/Z probes unless a
separate classical entropy source is earned. Count these as `Q_coin`, and
quantum acquisition probes as `Q_acq`; total quantum activity includes
`6N+Q_coin+Q_acq` up to fixed per-probe location counts. A reusable single-qubit
coin source still meets bounded coherence. Lazy binary Bernoulli comparison
uses at most two fair bits in expectation; a per-choice cap
`ceil(log2(N/epsilon_coin))` adds at most `epsilon_coin` over N choices.
Numerical b-bit precision remains paid but does not itself require b fresh
random bits per sampled decision. Every probe, capture, reset and waiting
interval remains in the execution ledger.

Energy is the sum of actual gate, link, memory-time, reset, cooling and erasure
costs for this schedule and commissioning. No joule estimate follows without
a hardware model. The same resources and target knowledge must be granted to
ordinary quantum fault-tolerant preparation. That comparator may adopt the
same state-specific precompensation. The theorem removes a need for growing
quantum coherence for this known entangled thermal family; it proves no
total-resource advantage over the strongest equally informed method.

## Primary-source overlap and boundaries

- Graph noise tailoring/convolution and its limits:
  <https://arxiv.org/html/2503.12870v3>. Main tailoring is ideal; noisy detection
  appendix uses PEC. Efficient global l1 learning needs additional support and
  total-infidelity conditions, not supplied by fixed positive per-location
  noise on growing chains.
- Known state precompensation:
  <https://arxiv.org/abs/2309.01434>.
- Noisy channel menus and positive versus signed decompositions:
  <https://arxiv.org/html/2409.01000v2>.
- Ideal all-temperature 1D sources:
  <https://arxiv.org/abs/2609.35973> and
  <https://arxiv.org/abs/2610.03578>.
- Actual quantum FT I/O and qLDPC comparators:
  <https://arxiv.org/abs/2408.05260> and
  <https://arxiv.org/abs/2602.16948>.

The cone theorem and complete noisy composition above are distinct from those
standard ingredients. Generic noncommuting thermal families use the separate
channel-interior construction; their constants and source cost do not acquire
the favorable six-layer values proved for this special family.
