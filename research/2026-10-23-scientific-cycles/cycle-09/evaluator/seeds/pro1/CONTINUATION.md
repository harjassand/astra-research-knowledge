# Pro1 Cycle8 continuation

22 October 2026, Australia/Brisbane. The scientific mission remains active.

## Current result and decision

The nonlinear endpoint-response problem now has an exact all-length solution
strong enough to enlarge the physical coding window. For every fixed
\(0<\beta\le1/8\), the original same-bath device has an initializer-independent
deterministic unassisted code sequence with rate
\[
 \mathsf Q(V_\beta,\tau)\ge \frac32+\frac{\ln2}{8192}\beta^3.
\]
The full-diamond error tends to zero pointwise for every fixed normal
initializer. No terminal bath return is required. This improves the attainable
small-angle power from the inherited \(7/2\) to \(3\); it is not a sharp
capacity exponent or a feedback converse.

The chosen next question is **the one-sided positive spectral scale of the
explicit \(H\), and whether a positive input parametrization can extend the
temporal range while retaining full operator drift**. The current response
estimate itself only requires \(b k\) small. Our present linear density and
entropy proof uses the coarser \(\|H\|\le k^2\), imposing \(b k^2=O(1)\).
Determine whether its positive spectrum makes that scale intrinsic to this
density, or whether a sharper spectral or free-energy argument pays longer
blocks. This is a scientific continuation decision, not a claim that such an
extension exists.

No spectral job or new exponent has been launched or certified at this
checkpoint. A positive exponential parametrization introduces four-endpoint
and higher coherences. The explicit four-endpoint counterexample below shows
why it cannot borrow the pair-supported response formula without further work.

## Sources and continuity

The native proof is `NONLINEAR_ENDPOINT_RESPONSE.tex`; its two complete
inherited appendices are included. `COMPLETE_PROOF.tex.txt` is the literal
include expansion. `UNIFORM_TRANSFER.md` gives the principal physical transfer.
The exact unchanged Cycle7 original is
`preserved/Astra_Amplification_Cycle7_PRO1_20261022.zip`, 4,800,520 bytes,
SHA256 `4fe694bb30a7e6515af2a96b2bdabd8e81fb8308ea9981ae7611fb661ae8d9ff`.
It preserves Cycle6 and the earlier chain.

The common Cycle8 packet was supplied locally and its actual bytes verified.
Its included original exactly matched the already completed local Cycle7
return. No newer local science was overwritten. The exact \(v_k\) law and
full-prefix optimizer are inherited, read from actual source, and were not
re-proved. Optional anisotropic meta-research was not used in this theorem.

## Complete operation

\[
 E=\mathbb C^2_{\rm seed}\otimes\mathcal F(\mathbb C^2),\qquad
 U=\begin{pmatrix}R&S_1&S_2\\S_1^*&0&0\\S_2^*&0&0\end{pmatrix},
 \qquad V_\beta=\sqrt{1-\beta^2}\,U+i\beta I.
\]
\(S_j\) prepends a color; \(R\) exchanges vacuum seeds and vanishes off the
vacuum. The actual root is retained and \(L+Q_k\) is conserved. The actual
initializer has depth mass \((2/3)3^{-h}\), uniform over \(2^{h+1}\) vertices;
the stationary reference input is \(\eta=(3/4,1/8,1/8)\).

All physical calls, outcomes and retained registers count. The bath evolves
throughout; blocks are not independent fresh channels. There is no bath
access, reset, fresh bath, preshared entanglement, postselection, backward
quantum wire, timing resource, or terminal bath-return promise. Beta, block
length, and input density are fixed before the coding horizon. Pointwise
all-normal convergence is distinct from uniform finite-horizon convergence.

## Objects retained for continuation

Put \(b=\beta^2\), \(a=1-b\),
\(\sigma=\operatorname{diag}(1/2,1/4,1/4)^{\otimes k}\), and let \(Q\) count
nonzero input ports. Thus \(-\log_2\sigma=kI+Q\).

The explicit Cycle7 operator \(H=\sum_{i<j}H_{ij}\) is input-offdiagonal,
Hermitian and charge preserving. It commutes with \(\sigma\) and \(Q\).
Its endpoint blocks couple only binary-charge patterns \(01\) and \(10\).
The unmatched-push/middle-deficit classification gives blocks
\(P(I-\mathrm{SWAP})\), \(P/2\), or zero, including their adjoints.
The analytic prefix \(P_{\rm sym}/(k+1)\) is never physically prepared.

\[
 v=\operatorname{Tr}\sigma H^2,\quad
 T_k(\sigma H)=vI,\quad
 \frac{k^2}{32}\le v\le\frac{k(k-1)}8,\quad
 \|H\|\le k(k-1).
\]
The inherited exact formula is
\[
 v=\frac{k(k-1)}8-\frac18
       \sum_{n=0}^{k-2}(k-1-n)\Pr(S_n=0).
\]
Here \(S_n\) is a fair nearest-neighbor random walk. No growth conjecture
remains at this first-order level.

## Exact new operation

On the full physical bulk prefix, initially at depth at least \(k\),
\[
 \operatorname{Tr}_A[(\sigma H\otimes I)G(b)]
   =b(1-b)F_k(b),\qquad G(b)=Q-W_k^*QW_k,
\]
\[
 F_k(b)=\sum_{i<j}\sum_{S\subset[k]\setminus\{i,j\}}
       b^{|S|}(1-b)^{k-2-|S|}A_{ij,S},\quad
 F_k(0)=vI,\quad \|A_{ij,S}\|\le\tfrac12.
\]
Spectators have identical stay masks in the two histories selected by \(H\).
Endpoint masks are complementary. Unitarity cancels the common spectator
output charge; the surviving endpoint operator is a difference of two
contractions. The exact input trace budget is
\(\|\sigma H_{ij}\|_1\le1/4\).

Consequently, with \(N=\binom{k}{2}\),
\[
 \|F_k(b)-vI\|\le N[1-(1-b)^{k-2}]\le N(k-2)b.
\]
This is a full coherent-prefix operator inequality. The Bernstein weights
arise after summing exact quantum amplitudes; they are not an assumption of
classical physical errors. The original \(H_{ij}\) remains in every term,
including after spectators are analytically deleted.

For \(G=G_0+bG_1+R_b\),
\[
 \|\operatorname{Tr}_A[(\sigma H\otimes I)R_b]\|
 \le b^2v+b(1-b)N[1-(1-b)^{k-2}].
\]
The source also exports a version for other pair-supported inputs with a
trace-norm budget and a genuine full-operator first certificate.

## Physical transfer that must be preserved

Set \(l=\ln2\), \(m=3lv/16\),
\[
 \rho=\sigma-\frac{lb}{2}\sigma H
              +\frac{4mb^2}{k}\sigma(Q-k/2).
\]
For \(k\ge2\), \(b>0\), \(bk^2\le1/16\), this is strictly positive and
normalized, with
\[
 S(\rho)-3k/2\ge lvb^2/32.
\]
Exact diagonal drift gives \(D_b(\sigma)=0\) and
\(D_b(Y)=2m(1-b)I\) at every \(b\). Hence
\[
 D_b(\rho)=lb^2(1-b)[3vI/8-F_k(b)/2]\le-\kappa I,\qquad
 \kappa=lvb^2(1-b)/16>0.
\]
The inward inequality holds in the bulk. The finite root remainder is paid
by the inherited homogeneous-Kraus operator Lyapunov theorem. Exact spectral
types, the \(r^2\) positivity factor, auxiliary CPTP normalization and polar
repair then give real arbitrary-reference codes. The auxiliary channel is a
proof device, not a physical resource or a non-isometric actual encoder.

Choose \(k=\lfloor1/(4\beta)\rfloor\). For \(\beta\le1/8\),
\(k\ge1/(8\beta)\) and \(bk^2\le1/16\), giving the cubic floor.
For actual \(\tau_\pi\), the repeated-block coherent-information limit equals
\(S(\rho)/k\).

## Counterexamples to preserve

- Scalar first response does not imply scalar higher response. At \(k=4\),
  the contracted \(b^2\) coefficient is
  \(-113I/64-(3/64)\mathrm{SWAP}\) on the first two bath colors.
- Deleting a spectator does not replace the input by a shorter optimizer.
  At \(k=3\), the three single-deletion contractions sum to \(9I/32\),
  while that substitution would give \(3I/8\).
- Pair support is essential. The four-endpoint matrix element
  \(\langle0101,1211|G(b)|1010,1211\rangle=b^2(1-b)^2\)
  is nonzero despite vanishing first order.
- The bulk formula is not a root identity. Port \(0\) and a \(+1\) vacuum
  eigenvector of \(R\) give zero one-call drift, not \(-(1-b)\).

Do not reopen fixed-four-call power searches, iid stabilization, diagonal
compression, balanced-only gain, exact product stationarity or reflecting
cutoffs. The present full nonlinear operation closes its stated task; the
positive-spectrum question is distinct.

## Comparator and resource meaning

The prior actual nonscalar four-call construction is retained, not replaced
by an obsolete iid control. At \(\beta=1/512\), the new uniform excess is
\(6.304136882681135\times10^{-13}\) qubits per call; its actual four-call
comparator has excess \(1.881142991895676\times10^{-14}\).
An analytic inequality proves the ordering independently of decimal rounding.
No optimum over all four-call inputs is claimed.

The new input has \(k=128\), rank \(3^{128}\), and enormous type/Lyapunov
constants. No useful blocklength or efficient encoder is established.
Exact finite diagnostics and closed-form evaluations measure replay costs
only; total discovery, inference, design and review costs remain unknown.

## Status

The assembled new proof has received a separate internal challenge with no
surviving gap at the recorded hashes. This is not external certification or
historical priority. Primary perfect-memory and forgetful-memory coding
theorems are compared in REFERENCES.md; neither substitutes for the new
infinite-bath drift and input-selection obligations.

Max owns integration. Private delivery, receiving-side reading, scientific
acceptance and repository integration are separate events. Protected
independent programmes and retired engineering operations remain untouched.
