# Capital transfer: compile the radial Pauli POVM into one projective shot

**Decision.** The strongest constructive operation from this narrow pass is to compile the supplied positive radial Pauli kernel into one randomly oriented qubit projective measurement followed by classical randomization. In the ideal continuous model, this samples the exact POVM outcome in one copy; it does not require characteristic-function tomography or Fourier inversion over many copies. The operation is exact for this rotationally covariant qubit kernel. It is not a general compiler for arbitrary operator tuples, and it does not establish practical advantage: the specified gamma noise makes the sample substantially less informative than a random-Pauli classical-shadow sample. A certified finite-precision radius sampler and an acquired, calibrated axis-control interface remain absent.

Status throughout this note is **source-derived-unreviewed** for the supplied representation claim and Capital claims. The derivation below is a reconstruction of the stated kernel and its stochastic implementation, not external mathematical review, formal verification, priority clearance, or hardware validation.

## 1. Opportunity and transfer choices

The supplied Pauli example starts from

\[
p(x)=\frac{C}{\Gamma(2+|x|/2)},\qquad
M(x)=u(r)I+v(r)n\cdot\sigma,
\quad r=|x|,\ n=x/r,
\]

with the all-linear Fourier identity \(\int e^{it\cdot x}M(x)\,dx=\widehat p(t)e^{it\cdot\sigma}\), positivity \(u\pm v\ge 0\), and normalization \(\int M(x)dx=I\). The exact source states that the kernel is positive for this Pauli triple and supplies the eigenvalue argument; it also explicitly leaves efficient evaluation/acquisition and advantage open.

Three distinct Capital transfers were screened:

| Capital source | Transfer being tested | Decision |
|---|---|---|
| **N712**, `frontier/dossiers/N712.txt`; status JSON `frontier/cards/N712-local-readout-thermal-information-loss-and-variance-certificate.json` records original `card_sha256` `ae9a787317bbd1b4d2957935605a24a2b44bdd3a17cf9618864170a73031c9e7`; materialized review card `frontier/review_cards/N712-local-readout-thermal-information-loss-and-variance-certificate.txt` has SHA-256 `e10f4ccef0289f715ed8390114e3ec74ab47a7c824b3c915307d9457171c9027`. Source pin: `updates/EC/package/local_readout_information/ORIGINAL_PASTED_SOURCE.txt`, SHA-256 `f366b1fe4464bfe42a0a36801b6ce66553b2d39f650fc5dc19e62ac08edb0bd0`, lines 20–73 (measurement/Fisher contract), 126–169 (variance acquisition), 170–202 (correlated-detector counterexample), 203–214 (scope and prior-art boundary). | Use its one-copy randomized Pauli readout and explicit covariance/Fisher/acquisition accounting as the matched information comparator. | **Selected as comparator, not as theorem transfer.** N712 concerns Gibbs Hamiltonian parameters, structural sparsity and a calibrated local Pauli detector. Those thermal Fisher bounds do not transfer to this single-qubit radial POVM. The shared reusable interface is one-copy readout plus a fully charged variance comparison; N712 also makes independent detector-error calibration a visible premise. |
| **N796**, `frontier/dossiers/N796.txt`; raw card `frontier/cards/N796-molecular-two-history-interferometry-and-erasure-completion.txt`, SHA-256 `131dd3908f8ce74b8423218711b4d0e83f67a66b461e18aa9664df679b876cb6`. Proof pin: `updates/FE/synthesis/interferometry/ERASURE_AND_CROSS_HISTORY_THEOREMS.md`, SHA-256 `a6d5872d48b94646e13daf20d4932da83e3b960be7af3ca5e1ed168b1fdeec8b`, lines 40–84 and 162–192. | Set a history unitary to \(e^{it\cdot\sigma}\) and the other to identity to obtain characteristic-function access; ask whether this can be made into a sampler. | **Rejected as the sampler.** The operation returns interferometric quadrature/characteristic-value estimates. Reconstructing the radial law from many frequencies is not one-copy sampling of \(M\); it adds frequency-grid, inversion, conditioning and copy costs. Its own molecular branch-control and erasure gates are unrelated to the qubit mathematical sampler. |
| **N810**, `frontier/dossiers/N810.txt`; raw card `frontier/review_cards/N810-thermal-anchor-obstruction-and-bounded-transition-observation.txt`, SHA-256 `4334b031bfb7a7e3a95f5fb0d1de8fe084b347fc992d8355c7542276b0e50b7e` (status JSON: `frontier/cards/N810-thermal-anchor-obstruction-and-bounded-transition-observation.json`). Source pin: `updates/FK/package/thermal/REPORT.md`, SHA-256 `a3648914ffa0adb7fc34a26b01bbd103517c9285fc1a9340b326f5d441f2b96a`, lines 24–47 (input/output and cost contract), 336–361 (cost/comparator and status). | Transfer a stochastic readout compiler into scientific access for a thermal response. | **Incompatible target.** N810's constructive route measures Gibbs energy, applies a bounded-observable CP filter, then resolves energy transitions to estimate a regularized dynamical response. A static draw from \(M\) gives a qubit-state outcome law; it does not provide Gibbs preparation, a legal \(f(H)\) instrument, or transition-energy response. This is a useful warning against calling any positive sampler a scientific acquisition primitive. |

The unexpected high-leverage connection is narrower and concrete: positivity of the supplied continuous operator density can be converted into an elementary measurement program using a standard rank-one projective shot plus classical randomization. Capital contributes the matched readout/noise accounting and the boundary between an acquired characteristic value and an actual sample.

## 2. Explicit kernel and one-shot compiler

Let
\[
f(r)=r p(r),\qquad I(r)=\int_{|r-1|}^{r+1}f(s)\,ds.
\]
The three-dimensional spherical-wave formula gives the scalar shell convolution
\[
g_\tau(r)=\frac{1}{2r}\int_{|r-\tau|}^{r+\tau}f(s)\,ds.
\]
For the Fourier convention in the supplied identity, \(u(r)=\partial_\tau g_\tau(r)|_{\tau=1}\) and \(v(r)=-\partial_r g_1(r)\). Thus, for \(0<r<1\),
\[
u(r)=\frac{f(r+1)-f(1-r)}{2r},\qquad
v(r)=\frac{I(r)}{2r^2}-\frac{f(r+1)+f(1-r)}{2r},
\]
and, for \(r\ge1\),
\[
u(r)=\frac{f(r+1)+f(r-1)}{2r},\qquad
v(r)=\frac{I(r)}{2r^2}-\frac{f(r+1)-f(r-1)}{2r}.
\]
These formulas reproduce the supplied identity
\[
u(r)-v(r)=\frac{f(r+1)}{r}-\frac{I(r)}{2r^2}.
\]
The value at \(r=0\) is immaterial to the continuous outcome law and can be set by the radial limit. Positivity of the supplied kernel means \(u(r)>0\) on its positive-mass support and
\[
a(r)=v(r)/u(r)\in[-1,1].
\]
Normalization gives the radial probability density \(w(r)=4\pi r^2u(r)\), with \(\int_0^\infty w(r)dr=1\).

For input \(\rho=(I+s\cdot\sigma)/2\), run:

1. Draw \(r\sim w\), independently of the state.
2. Draw \(n\) uniformly on \(S^2\), and perform the projective measurement of \(n\cdot\sigma\), obtaining \(b\in\{\pm1\}\) with probability \((1+b\,s\cdot n)/2\).
3. Set \(n_0=bn\). Independently draw \(\varepsilon\in\{\pm1\}\) with \(\mathbb E[\varepsilon\mid r]=a(r)\), equivalently \(\Pr(\varepsilon=-1\mid r)=(1-a(r))/2\).
4. Return \(X=r\varepsilon n_0\).

The two projective outcomes/axis pairs that yield a given \(n_0\) are \((n_0,+1)\) and \((-n_0,-1)\). Their total angular density is \((1+s\cdot n_0)/(4\pi)\). After the sign flip, the output direction at fixed \(r\) has density \((1+a(r)s\cdot n)/(4\pi)\). Since \(w=4\pi r^2u\), the density per unit volume is
\[
\frac{w(r)}{4\pi r^2}(1+a(r)s\cdot n)
=u(r)+v(r)s\cdot n
=\operatorname{Tr}\!\left[\rho\,M(x)\right].
\]
This proves the compiler realizes the exact stated POVM in the ideal real-valued model. It uses one projective quantum measurement; all later steps are state-independent classical randomness. Equivalently, the radial POVM is a classical post-processing of the covariant random-axis qubit measurement.

The construction implements one sample from the positive all-linear-marginal law. It does not turn characteristic-function inversion into a sampler. Scope is the particular qubit radial kernel (or another rotationally covariant qubit POVM with a normalized \(w\) and \(|a|\le1\)); no higher-dimensional or arbitrary-tuple extension follows.

## 3. Sampler precision and finite interface

For the stated gamma profile, normalization reduces to
\[
C=\left(32\pi\int_0^\infty\frac{t^2}{\Gamma(2+t)}dt\right)^{-1}.
\]
I evaluated this integral and the fourth radial moment numerically with 60-decimal mpmath quadrature. The outputs were
\[
\int_0^\infty\frac{t^2}{\Gamma(2+t)}dt\approx1.7226275776710492808946345437692983,
\]
\[
\int_0^\infty\frac{t^4}{\Gamma(2+t)}dt\approx9.8705492010831225769104973904119567,
\qquad C\approx0.00577442511206735120467801479861685.
\]
Using the explicit \(u\) formula, a separate 60-decimal nested quadrature gave \(\int_0^{12}w(r)dr\approx0.9965544580121781\) and \(\int_0^{20}w(r)dr\approx0.9999988698984579\). If the exact normalization is used, these suggest radial tail masses of about \(3.45\times10^{-3}\) at 12 and \(1.13\times10^{-6}\) at 20. These are numerical diagnostics only, not interval-certified tail bounds or a sampler receipt.

A real-valued exact sampler still requires evaluating/inverting the CDF of \(w\) and evaluating \(a(r)\). The supplied text gives an analytic positivity proof but no certified CDF enclosure, inverse-CDF algorithm, rejection envelope, bit complexity, or finite-precision error. A concrete digital implementation would need to:

- certify \(C\), radial bin masses, and a tail cutoff with interval bounds;
- certify each computed \(a(r)\) lies in \([-1,1]\), then round/clip its flip probability with a bounded error;
- specify the measurement's finite radial and angular output bins and integrate the operator effects over those bins;
- bound the total probability error on that *coarsened* outcome space.

A finite list of radii/axes is a discrete measure and is singular to the exact continuous law, so raw total-variation closeness on \(\mathbb R^3\) cannot be claimed just from a fine grid. The operational comparator must use finite-resolution bins (or another stated weak metric) and certify the corresponding effects. For an \(m\)-bin POVM, one usable uniform-state error target is \(\frac12\sum_{j=1}^m\|E_j-\widetilde E_j\|_{\rm op}\le\epsilon\). No such certificate is currently supplied. The projective axis itself also needs a calibrated finite-resolution control/readout interface in a physical implementation.

## 4. Scientific output and matched comparator

The supplied characteristic function factors as \(\widehat q_\rho(t)=\widehat p(t)\operatorname{Tr}(\rho e^{it\cdot\sigma})\). Expanding at zero, with \(\mathbb E Z=0\) and isotropic coordinate variance \(\sigma_p^2=\mathbb E Z_1^2\), gives
\[
\mathbb E X=s,\qquad \operatorname{Cov}_\rho(X)=(1+\sigma_p^2)I-ss^{\mathsf T}.
\]
For the gamma density, spherical symmetry and \(r=2t\) give \(\mathbb E|Z|^2=4I_4/I_2\), hence
\[
\sigma_p^2=\frac{4I_4}{3I_2}\approx7.63991732090102785940842523197758.
\]
Thus one POVM draw is an unbiased three-component Bloch-vector observation with covariance
\[
\operatorname{Cov}(X)\approx8.63991732\,I-ss^{\mathsf T}.
\]
The approximation is again quadrature, not interval-certified.

For the matched one-copy random-Pauli classical-shadow estimator, choose \(J\in\{x,y,z\}\) uniformly, measure \(\sigma_J\) with outcome \(b\), and report \(Y=3b e_J\). Then \(\mathbb E Y=s\), \(\mathbb E[YY^{\mathsf T}]=3I\), and
\[
\operatorname{Cov}(Y)=3I-ss^{\mathsf T}.
\]
The gamma-kernel output therefore has an extra isotropic covariance \((\sigma_p^2-2)I\approx5.63991732I\), at identical one-copy count. The cost buys the exact prescribed law for every linear projection, not a better estimator of the Bloch vector. If a single coordinate is the only target, directly measuring that Pauli is sharper still.

There is also a Fisher-information check. At the maximally mixed state \(s=0\), the radial outcome density is \(w(r)(1+a(r)s\cdot n)/(4\pi)\), so its classical Fisher matrix is
\[
F_\gamma(0)=\frac{1}{3}\left(\int_0^\infty w(r)a(r)^2dr\right)I\preceq\frac13 I.
\]
The random-Pauli measurement has \(F_{\rm RP}(0)=I/3\). The inequality also follows from the classical post-processing construction; for this kernel it is strict because \(a(r)\to0\) as \(r\to0\) while \(w\) has positive mass on every sufficiently small radial interval. This is a comparison at one state, not a uniform Fisher theorem. It reinforces that the all-linear exactness property does not create an information advantage over the standard one-copy comparator.

N712 is a useful Capital reference for insisting on the full covariance/Fisher/acquisition chain: its random local Pauli readout gives an explicit bounded additive information-loss statement under a specified Gibbs, sparsity, and independent calibrated-detector contract. The radial Pauli compiler has a transparent exact sample law and covariance but supplies no thermal response coefficient or many-body Fisher guarantee. The real scientific output currently established by the construction is a precisely specified measurement sample; a downstream estimation advantage is not established.

## 5. Exact source pins and status boundary

- Supplied foundational text: `/Users/harjas/.codex/attachments/ee52f2ba-f701-464e-80b9-e8f12bb93bae/Pasted text.txt`, SHA-256 `dbf21495f91208654d6cdc7883b26a912d6430cd2c3390204a746d3daaf8ab8a`, lines 373–413 for the explicit Pauli kernel and positivity proof; lines 428 onward for the remaining computational/acquisition boundary.
- Live Capital main was read-only at `b7cada92d2eb304578be5ed974f1e44b10a89928` (N842). Local PR-92 at `5eb2441c93011d4fefb819b6f751f33537427dc3` contains N843–N847 and is a separate worker branch; those packages were not read. No Capital worktree changes or publication were made.
- N712 and N796 references above retain `source_derived_unreviewed` status. N810’s physical response route retains its independent access/cost gate. The direct compiler is a mathematical construction from the supplied positive kernel plus an ordinary projective qubit measurement; novelty, external correctness, finite-bit complexity, calibrated physical execution, and useful downstream capability remain UNKNOWN.
