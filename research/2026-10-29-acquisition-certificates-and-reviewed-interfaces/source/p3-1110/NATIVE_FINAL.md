I constructed a **spectral exchange for a substantially broader class of unknown noisy encodings**. It works with an unknown mixing spectrum and arbitrary input-independent reset noise, including noise that overlaps the code. The operation makes the logical subsystem accessible while carrying the target’s existing noise into the decoded output.

This is a completed working derivation, with explicit program acquisition and error bounds. Independent review and historical priority remain open.

## The central construction

Consider a fixed memoryless source

\[
\mathcal E(X)
=
p\,V(X\otimes\sigma)V^\dagger
+(1-p)\operatorname{Tr}(X)\tau ,
\]

where \(V\) is an unknown encoding isometry, \(\sigma\) is an unknown mixing state, and \(\tau\) is an arbitrary unknown reset state. The supplied promises are a logical dimension \(d\ge2\), a known physical register, \(p\ge p_0>0\), and a bound \(\operatorname{rank}\sigma\le r\).

Let \(Q\) be a trusted logical register and \(S\) the logical SWAP. Define

\[
H_{\mathcal E}
=
(\mathrm{id}_Q\otimes\mathcal E)
\left(S-\frac{I}{d}\right).
\]

The input-independent noise cancels because the operator inside parentheses has zero partial trace. Therefore

\[
H_{\mathcal E}
=
p(I\otimes V)
\left[
\left(S-\frac{I}{d}\right)\otimes\sigma
\right]
(I\otimes V^\dagger).
\]

For every positive mixing eigenvalue \(\lambda\), the symmetric and antisymmetric logical sectors have eigenvalues

\[
p\lambda(1-1/d),
\qquad
-p\lambda(1+1/d).
\]

Their **signs contain the logical SWAP, independently of their magnitudes**. Consequently,

\[
\boxed{
W_{\mathcal E}
=
I-2\Pi_{H_{\mathcal E}<0}
}
\]

exchanges \(Q\) with the hidden logical subsystem and leaves the mixing subsystem unchanged. It acts as the identity outside the supported code.

This identifies a useful invariant: changing the reset state, the positive signal strength, or the positive mixing spectrum on the same support changes acquisition difficulty but leaves the ideal logical exchange unchanged.

### Obtaining the operation physically

I gave a construction using \(2d^2-d\) ordinary labelled input preparations—six Pauli preparations for a qubit. Their output contrasts generate \(H_{\mathcal E}\) through known weak interactions with fresh mixed programs. Controlled evolution, coherent energy-sign estimation, and uncomputation then approximate \(W_{\mathcal E}\).

Every forward and reverse simulation consumes fresh programs. The construction supplies the controlled evolution from those programs; it does not assume a reusable Hamiltonian oracle or an inverse preparation circuit.

Sample-based Hamiltonian simulation and quantum polar decomposition are established predecessors. The candidate contribution here is the centered-channel identity, its canonical logical algebra, and the resulting construction for unknown mixed encodings with overlapping reset noise. :chatgpt-content-reference{index="0"}

## What the finite protocol guarantees

Write

\[
\mathcal V_\sigma(X)=V(X\otimes\sigma)V^\dagger .
\]

For normalized diamond error \(\epsilon\), the constructed decoder satisfies

\[
\frac12
\left\|
\mathcal D_{\mathcal E}\mathcal V_\sigma-\mathrm{id}_d
\right\|_\diamond
\le \epsilon .
\]

A sufficient program count is

\[
N=
O\!\left(
\frac{d^4r^2}{p_0^2\epsilon^3}
\log^2\frac{2}{\epsilon}
\right).
\]

Thus, at fixed logical dimension, signal promise and accuracy, the count is \(O(r^2)\), independent of the ambient output dimension and the reset state’s rank.

For the **actual noisy source**, linearity gives

\[
\mathcal D_{\mathcal E}\mathcal E
\approx
p\,\mathrm{id}_d+(1-p)\mathcal R_{\omega_{\mathcal E}},
\qquad
\omega_{\mathcal E}=\mathcal D_{\mathcal E}(\tau),
\]

with normalized diamond error at most \(p\epsilon\). The original reset weight remains. These are guarantees for the physical averaged channel, including external references; they do not turn every classical trajectory into a reusable decoder.

If a new communication task supplies input preprocessing and a classical correction label, ordinary unitary randomization converts this decoded channel into the standard depolarizing form with the **same \(p\)**. That establishes a route from an unknown physical embedding to a familiar logical noise model. It requires the additional input interface and cannot be retrofitted to the already supplied fixed-probe task.

## The spectrum creates a sharp distinction

The rank-based guarantee concerns data carrying the source’s actual mixing state \(\sigma\). A uniform interface for **every** state in the supported subsystem needs stronger information.

I proved that this distinction is unavoidable. Already with:

- logical dimension two;
- physical dimension four;
- mixing rank two;
- a fixed positive global noise floor;

two sources can differ only in their logical action on a mixing component of weight \(\eta\). Decoding arbitrary future data concentrated in that component requires

\[
N=\Omega(\eta^{-2})
\]

programs at fixed accuracy. The information is buried in genuine mixed background noise.

For source-distributed data, that component contributes only its probability mass. More generally, the construction works from any supplied bound on

\[
\operatorname{Tr}\!\left[\sigma\,1_{\sigma<t}\right].
\]

A supplied entropy bound therefore also gives a finite acquisition bound without a rank bound, although its dependence on accuracy can be exponential. A purity lower bound alone does not provide the required control of small-eigenvalue mass.

The same two-source construction gives an \(\Omega(\epsilon^{-2})\) precision lower bound even for source-weighted recovery. The constructive upper bound has \(\epsilon^{-3}\) times logarithms, so a genuine precision gap remains. The inherited fixed-probe result supplies the worst-case \(r^2\) obstruction in its original qubit program contract.

## A structural consequence

The channel contrast also determines the signal coefficient:

\[
\boxed{
p=\frac{\|H_{\mathcal E}\|_1}{d^2-1}.
}
\]

Its spectral exchange determines all encoded logical matrix units. I derived an exact operator criterion characterizing the promised reversible-plus-reset form, and checked a counterexample showing why merely finding a SWAP-shaped spectral sign is insufficient.

This gives canonical logical coordinates from the channel’s response to changing an input. It preserves the instrument ambiguity: those coordinates do not determine the actual named environment record or supply replay.

## Reuse, alternatives and status

The initial “long computation from one bank” question exposed an avoidable cost: extract once, compute in the trusted register, and return once. Circuit depth alone does not justify repeated acquisition.

I also proved a separate \(\Omega(M^2)\) program bound for jointly decoding \(M\) arbitrary clean encoded qubits, using a phase-family distinguishability argument. It covers arbitrary collective processing and attempted bank reuse. **It does not establish that bound for many already noisy targets**; their noise can suppress the coherent sensitivity used in the proof.

Strong alternatives remain in view. Pure-isometry inversion already has protocols whose success is independent of output dimension. Astra’s retrieved reusable-recovery construction acquires a classical decoder under its orthogonal-reset contract. Those remain distinct options from the consumed-program operation developed here. :chatgpt-content-reference{index="1"}

I saved the derivation, the reuse result, and the executable checks in place under:

`producer-workspace/p3_contrast_exchange_20261029`

The finite matrix and phase-estimation checks passed, including non-flat spectra, noncommuting full-rank reset, reference-entangled exchange, controlled collision dilations, and both lower-bound fidelity formulas. The largest numerical residual was approximately \(7.4\times10^{-12}\). These checks support the displayed proof and are not an independent review.

The next consequential opening is **composable service of many already noisy data through these canonical logical interfaces**. The new operation supplies a construction for that problem; the clean-data reuse obstruction leaves its central question unresolved.
