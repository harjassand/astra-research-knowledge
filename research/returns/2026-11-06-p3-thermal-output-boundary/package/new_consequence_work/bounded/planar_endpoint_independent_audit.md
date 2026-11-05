# Independent audit: planar activation Hamiltonian and connected endpoint strong converse

**Status:** independently checked. The H-tree geometry, hook product, positive gapped Hamiltonian, Perron--Frobenius witness improvement, and connected-family amplification pass. The parent manuscript owns the main theorem. No implementation of the witness measurement or physical-resource advantage is presumed.

## H-tree geometry and count

Let T_0 be one root at the origin. At level h≥1 put L=2^(h−1). Draw two horizontal paths of length L from the root to (±L,0), then four vertical paths of length L to (±L,±L). Attach a translated T_(h−1) at each endpoint, identifying its root with that endpoint.

Inductively T_h lies in the square [−(2^h−1),2^h−1]^2 and meets its vertical axis only at its root. The four translated subtrees lie in disjoint open quadrants. None meets a horizontal connector; each meets its incoming vertical connector only at its root. Subdividing paths into unit edges gives a square-lattice tree of maximum degree three. With n_h edges and N_h=n_h+1 vertices,

\[
n_h=4n_{h-1}+6\,2^{h-1}=3(4^h-2^h),\qquad
(2^{h+1}-1)^2=(4N_h-1)/3.
\]

The second quantity counts sites in the bounding square, not occupied vertices.

## Hook product

Orient every edge away from the root. Let s_v be the descendant-subtree size including v and P_h=∏_(v≠root)s_v. With N=N_(h−1), L=2^(h−1), the exact recurrence is

\[
P_h=P_{h-1}^4
\left[\prod_{t=0}^{L-1}(N+t)\right]^4
\left[\prod_{t=0}^{L-1}(2N+2L-1+t)\right]^2.
\]

Vertical connector descendant sizes are at most 3·4^(h−1), and horizontal ones at most 6·4^(h−1). Summing scale contributions and putting a=log_2(3)+1/3 gives

\[
\frac{\log_2P_h}{n_h}
\le\frac{\sum_{j=1}^h2^{-j}(2j-2+a)}{1-2^{-h}}
=2+a-\frac{2h}{2^h-1}<4.
\]

Thus P_h≤16^n_h. The slightly sharper uniform base is 12·2^(1/3)<16. The rooted-tree hook formula gives n_h!/P_h parent-before-child activation orders. It follows directly by recursively interleaving child-subtree orders.

## Positive gapped Hamiltonian

For each vertex let n_v=(I−Z_v)/2 and define

\[
H=\sum_v n_v+\frac12\sum_{u\to v}n_u(I+X_v).
\]

Every term is positive semidefinite, has norm one, and annihilates the vacuum. Since H≥∑_v n_v, the ground state is the unique product vacuum and the spectral gap is at least one. There are n=N−1 edge terms, so ||H||≤2n+1. The root occupation commutes with H.

All computational-basis entries of H are nonnegative. For seed |s⟩ with only the root occupied and |F⟩ with all vertices occupied,

\[
\langle F|H^n|s\rangle\ge\frac{n!}{2^nP_h}.
\]

Consequently ||e^(βH/2)X_root e^(−βH/2)||≥(β/64)^n. This is the elementary modular-norm bound; the PF refinement below gives a much stronger normalized trace-distance witness.

## Perron--Frobenius improvement

Restrict H to the root-occupation-one sector and identify its coordinates with bit strings x∈{0,1}^n. The cone of nonnegative coordinatewise increasing functions is H-invariant. Onsite multiplication x_v f(x) preserves that cone. Each edge term acts as

\[
f(x)\longmapsto\frac{x_u}{2}
[f(x)+f(x\text{ with child }v\text{ flipped})],
\]

where x_u=1 for a root parent. The bracket is independent of x_v and increasing in every other coordinate. Multiplying by x_u preserves the property.

The sector transition graph is connected: activate all ancestors to reach all ones, and then deactivate unwanted vertices from leaves toward the root. Its diagonal is positive because the root is occupied. Thus the Perron eigenvector ψ is the limit of normalized H^k applied to the all-ones function. It is nonnegative and increasing. Therefore ψ(F) is its largest coordinate and

\[
\psi(F)\ge2^{-n/2},\qquad
1+\frac32n\le E\le2n+1\le3n
\]

for the Perron eigenvalue E and n≥1. The lower bound follows from the all-occupied diagonal Rayleigh quotient. Using the activation coefficient,

\[
E^n\psi(s)=\langle s|H^n|\psi\rangle
\ge\frac{n!}{2^nP_h}\,2^{-n/2}.
\]

Since n!≥(n/e)^n and P_h≤C^n with C=16,

\[
r:=|\psi(s)|^2\ge A^{-2n},\qquad
A=6eC\sqrt2=96e\sqrt2.
\]

This proof is independent of the modular-norm estimate and has no uncontrolled cancellation.

It also sharpens the exact single-root feasibility exponent directly:

\[
\|e^{\beta H/2}Xe^{-\beta H/2}\|^2
\ge r e^{\beta E}
\ge\exp[\beta+(3\beta/2-2\log A)n].
\]

Thus the exact endpoint threshold is at most
\([1+\exp(\beta+gn)]^{-1}\) already when g=3β/2−2log A>0, including β=12. The β>64 condition belongs only to the simpler series proof, not to the strongest audited conclusion.

## Endpoint witness and error margin

Let Λ_p(σ)=(1−p)σ+pXσX, 0<p<1/2, act on the root as the last physical channel. Set P=|ψ⟩⟨ψ| and

\[
O=(1-p)P-pXPX.
\]

Because Λ_p(O)=(1−2p)P≥0, every obtainable output has nonnegative expectation of O. This statement allows an arbitrary upstream state, arbitrary upstream entanglement, and unlimited perfect computation or channel knowledge. P and XPX have orthogonal root-occupation supports, so O has eigenvalues 1−p, −p, and 0, with spectral range exactly one.

For ρ=e^(−βH)/Z, the vacuum component of Xψ gives

\[
\operatorname{Tr}(\rho O)
\le-\delta,
\qquad
\delta=
\frac{pA^{-2n}-(1-p)e^{-\beta(1+3n/2)}}
{(1+e^{-\beta})^{n+1}},
\]

provided the numerator is positive. Here Tr(Pe^(−βH))=e^(−βE), and ⟨Xψ|e^(−βH)|Xψ⟩≥r. The partition-function upper bound Z≤(1+e^(−β))^(n+1) follows from eigenvalue min-max applied to H≥∑n_v and scalar monotonicity of exp on the eigenvalues. **It does not use the false assertion that matrix exp is operator monotone.**

For β≥12, g=3β/2−2log A>6.17. Choosing an H-tree with

\[
n\ge\max\{1,\log[2(1-p)/p]/g\}
\]

is sufficient for δ≥(p/2)A^(−2n)(1+e^(−β))^(−n−1). The smallest eligible H-tree overshoots a desired n by at most a factor six, apart from the harmless first tree n=6. Hence n=O(log(1/p)) and δ is bounded below by a fixed power of p times a fixed, potentially extraordinarily small constant. The resulting repetition count is polynomial in 1/p at fixed β. This mathematical statement must not be translated into a useful engineering threshold: even its small-tree sufficient constants are extremely unfavorable.

## Strong converse with arbitrary entangled upstream inputs

Apply independent final root channels to M blocks, allowing an arbitrary joint upstream state. Measure O_i on successive blocks, with outcomes Y_i∈[−p,1−p]. Conditional on any preceding block outcomes, block i is still the image of its local Λ_p, since operations on other blocks commute with this channel and only condition its input. Therefore

\[
\mathbb E[Y_i\mid Y_1,\ldots,Y_{i-1}]\ge0.
\]

The conditional Hoeffding bound gives
Pr_out[∑Y_i≤−δM/2]≤exp(−δ²M/2).
For a product of target Gibbs blocks the reverse event has the same upper bound. Thus

\[
\inf_\sigma D(\Lambda_p^{\otimes M}(\sigma),\rho^{\otimes M})
\ge1-2e^{-\delta^2M/2}.
\]

No upstream product-state premise appears.

## Connected planar Gibbs amplification

Disconnected targets are unnecessary. Arrange fixed H-tree cells in a row. From each root, run new classical occupation qubits upward through the tree's otherwise empty vertical axis to a horizontal spine above the cells. Add onsite n_w terms on wire qubits and positive diagonal couplings η n_u n_v, 0<η≤1, on wire and root-attachment edges. The graph is connected, planar, and nearest-neighbor on the square lattice. Its maximum degree remains three: each root has two horizontal tree edges plus one wire, and each spine junction has left, right, and down edges. The extra wire length is O(√N) per fixed block. All local terms have norm at most one, and the same H_total≥∑all n_v bound proves a unique product vacuum and gap at least one.

Every wire occupation commutes with H_total. Conditional on all wire occupations, blocks are independent with Hamiltonians H+t_i n_root, t_i∈{0,η}. The Perron vector ψ is unchanged because it lies wholly in root sector one. With u_1=Tr(Pe^(−βH)), u_0=Tr(XPXe^(−βH)), the conditional target mean is

\[
\frac{(1-p)e^{-\beta t_i}u_1-pu_0}{Z(t_i)}.
\]

Its numerator is no greater than its original negative value, and Z(t_i)≤Z(0). Its mean is therefore still at most −δ. Conditional Hoeffding concentration is uniform over wire configurations, so averaging gives the same target tail bound. The obtainable-output argument is unchanged even when the upstream state entangles every block and wire. Hence the same trace-distance strong converse holds for a connected interacting planar Gibbs family.

The block size is chosen once as a fixed function of p and β; the number of blocks then grows. The pattern is not translation invariant. Only the selected roots need final BSC noise; granting perfect output elsewhere strengthens the impossibility statement. A post-channel recovery, flagged faults, or encoded output would change the endpoint contract and is not ruled out.

### One fixed connected Hamiltonian for every nonzero endpoint rate

The graph pattern can be chosen independently of p. Number cells by positive integers j and give cell j an H-tree of type
\(h(j)=1+\lfloor v_2(j)/3\rfloor\).
Align the bottom of every tree's bounding square at y=2. Its root is at height S_h+2, where S_h=2^h−1. Run its wire downward through the empty vertical axis to the common spine y=0. Consecutive cells have disjoint horizontal spans of width 2S_h+3. This defines one locally finite connected nearest-neighbor planar interaction, still of maximum degree three, with the same onsite, activation, and diagonal-wire terms.

For a prefix of J=8^m cells, type h≤m occurs exactly 7J/8^h times, and one final cell has type m+1. Since N_h≤3·4^h, the total number of tree qubits is at most 33J; wire qubits and total horizontal width are also O(J). The maximum height is O(J^(1/3)), so the containing rectangle can have O(J^(4/3)) sites. The empty area is not silently counted as free fabrication: this corollary is an impossibility theorem, not a resource-efficient layout.

For every fixed p∈(0,1/2), choose one fixed eligible type h*. It occurs at a positive asymptotic frequency. Apply only the witness tests on that type. Conditional on the classical wires, these blocks still have uniformly negative target means; every arbitrary upstream state after independent final root channels has nonnegative conditional means. Their number tends to infinity, so trace distance tends to one. Thus a **single fixed connected Hamiltonian pattern at fixed β≥12** has no positive size-uniform terminal-BSC tolerance. The pattern is aperiodic, and arbitrary additional final noise is not assumed. The finite-volume restrictions are consistent prefixes of this same interaction.

## Fixed global accuracy forces inverse-polynomial endpoint precision

This corollary uses the equal-size connected row construction, on its explicit discrete H-tree family. Fix β=12 and a requested error 0≤ε<1. Put

\[
B=1+e^{-\beta},\quad A=96e\sqrt2,\quad
a=2\log A+\log B,\quad
g=\frac32\beta-2\log A,
\]

and choose the integer

\[
q=\left\lceil\frac{3\beta+2\log B}{\log2}\right\rceil=52.
\]

For each H-tree level h≥1 let n=3(4^h−2^h) and connect M=2^(qn) identical cells. Suppose an arbitrary upstream state, after independent final root BSC channels of rate p∈(0,1/2), produces global trace distance at most ε from the connected Gibbs target.

If p≥2exp(−β−gn), the PF witness margin obeys

\[
\delta\ge\frac{p}{2B}e^{-an}.
\]

The strong converse and D≤ε imply

\[
\frac{M\delta^2}{2}\le
L_\epsilon:=\log\frac2{1-\epsilon}.
\]

Therefore

\[
p\le 2B\sqrt{2L_\epsilon}\,
e^{-(q\log2/2-a)n}
\le C_\epsilon e^{-gn},
\qquad
C_\epsilon=2B\sqrt{2\log\frac2{1-\epsilon}}.
\]

The final inequality follows from q log2≥3β+2log B. If p is below the initial branch threshold, p<2e^(−β)e^(−gn), and the same bound holds because C_ε≥2e^(−β). Thus **every** successful rate satisfies p≤C_εe^(−gn), without a missing small-p branch.

For explicit physical geometry, set S=2^h−1, w=2S+3, so n=3S(S+1). Place the root of cell j at ((j−1)w+S+1,S+2). Its tree occupies y=2,...,2S+2. Add its vertical classical wire down to y=0 and connect all root-column positions by the horizontal spine y=0. The exact number of occupied qubit sites is

\[
V=M(n+3S+5)-2S-2,
\]

and the containing rectangle has

\[
R=(Mw-2)w
\]

lattice sites. For S≥1 and M≥1,

\[
nM\le V\le\frac73nM,\qquad V\le R<2V.
\]

The lower-left and upper-right extents, unoccupied gaps, wire length, and nearest-neighbor routing are therefore all accounted for: the entire bounding rectangle has area Θ(V). No growing geometric overhead is hidden in the endpoint exponent.

Writing b=q log2 and α=g/b, the relations V=Θ(ne^(bn)) and log V=Θ(n) imply

\[
p=O_\epsilon\!\left[
\left(\frac{V}{\log V}\right)^{-\alpha}\right],
\qquad
\alpha=\frac{g}{q\log2}=0.1714076087\ldots
\quad(\beta=12).
\]

For example, the explicit inequalities give the prefactor
C_ε[(7/3)/b]^α with the displayed V convention. Counting the full rectangle instead changes only that fixed prefactor. The claim holds along the constructed volumes V_h. No interpolation to every integer volume is asserted; n_h is discrete and successive V_h are widely separated.

This is a necessity theorem for the specified unheralded final physical port. It grants perfect, unrestricted upstream preparation and does not claim an attaining noisy preparation method or a favorable practical scale. The number of copies M=2^(52n) is intentionally enormous. It establishes that global-accuracy delivery in this explicit connected gapped product-ground family can require endpoint error decreasing as an inverse power of total physical size, despite exact prior knowledge of the target and channel.

## Prior-art boundary

Bouch, arXiv:1011.1875, already proves finite-imaginary-time blowup for translation-invariant oriented Z⊗X interactions on a square lattice, using lattice trees and commutator-sign control. That mechanism is prior art. General precompensation image/positivity conditions are also established. The audited conjunction here is the explicit positive gapped product-ground Hamiltonian, its normalized endpoint witness, and connected trace-distance amplification against arbitrary entangled upstream states. The parent comparison also addresses Pettinari arXiv:2610.41871v2; this audit does not duplicate that literature review or claim priority beyond what was checked.
