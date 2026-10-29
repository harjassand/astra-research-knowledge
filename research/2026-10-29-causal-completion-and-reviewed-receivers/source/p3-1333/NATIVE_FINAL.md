**I constructed a frozen receiver for many already noisy data, with calibration cost linear in the number of future uses at fixed dimension and accuracy.** The guarantee covers joint, entangled and adaptive use, retains the source’s original reset weight, and requires no lower bound on the individual mixing eigenvalues.

This turns the spectral exchange into a reusable service: training systems are measured and consumed; the retained object is a classical description of a receiver circuit.

## 1. The service theorem

Write the promised source as
\[
\mathcal E(X)=V(X\otimes S)V^\dagger+\operatorname{Tr}(X)C,
\qquad
p=\operatorname{Tr}S,
\]
with
\[
S\ge0,\qquad C\ge \nu I_D/D,\qquad
\operatorname{Tr}S+\operatorname{Tr}C=1.
\]

Here \(d\) is the logical dimension, \(D\) the physical dimension, and \(\nu>0\) a supplied lower bound on the **input-independent reset component**. The mixing spectrum may contain arbitrarily small eigenvalues or zeros.

After calibration, the classical record \(Y\) specifies a decoder \(\mathcal D_Y\). With probability at least \(1-\alpha\), one calibration event guarantees
\[
\operatorname{dist}_{M,\mathrm{ad}}
\left(
\mathcal D_Y\mathcal E,\;
p\,\mathrm{id}_d+\mathcal R_{\mathcal D_Y(C)}
\right)
\le\epsilon.
\]

The distance is the largest final normalized trace distance over ordinary adaptive protocols using at most \(M\) calls, including arbitrary entangled inputs, external references and retained quantum memory. For an unnormalized positive operator \(B\), \(\mathcal R_B(X)=\operatorname{Tr}(X)B\).

The benchmark retains the **actual** coefficient \(p\). In the uniform-reset case,
\[
C=(1-p)I_D/D,
\]
the ideal service is exactly
\[
p\,\mathrm{id}_d+(1-p)\mathcal R_{I_d/d},
\]
independent of the training record.

This remains service of data produced by the specified source. It does not become uniform recovery of every state concentrated in an arbitrarily rare gauge component.

## 2. The constructive step that makes it work

I fit a complete channel within the promised source model, then compile its logical exchange. This supplies an exact logical algebra even when a tiny spectral component is poorly estimated.

The exchange ancilla is initialized **maximally mixed**:
\[
\widehat{\mathcal D}(Z)=
\operatorname{Tr}_R\!\left[
\widehat W(I_d/d\otimes Z)\widehat W^\dagger
\right].
\]
Consequently,
\[
\widehat{\mathcal D}(I_D/D)=I_d/d,
\qquad
\widehat{\mathcal D}(C)\ge\nu I_d/d.
\]

The inherited centered-channel identities then give a stability bound without an inverse mixing eigenvalue:
\[
\|J_F-J_G\|_\infty
\le
\sqrt{dD}\left(2+\frac{4d}{d^2-1}\right)
\|J_{\mathcal E}-J_{\widehat{\mathcal E}}\|_2,
\]
where
\[
F=\widehat{\mathcal D}\mathcal E,\qquad
G=p\,\mathrm{id}_d+\mathcal R_{\widehat{\mathcal D}(C)}.
\]

Thus the fitted exchange can change abruptly on a tiny-weight component while its effect on the **noisy service** remains small.

The second ingredient is a complete composition bound:
\[
J_G\ge\mu I
\quad\Longrightarrow\quad
\operatorname{dist}_{M,\mathrm{ad}}(F,G)
\le
\min\!\left\{1,\sqrt M\,\frac{\|J_F-J_G\|_\infty}{\mu}\right\}.
\]

Its proof constructs two common channels whose classical mixture probabilities differ slightly. Any adaptive experiment becomes a common physical map of \(M\) independent Bernoulli programs, so ordinary statistical distance bounds apply. This is a finite form of the established local classical simulation method in noisy metrology; the note proves the required operational statement explicitly. [Nature Communications](https://www.nature.com/articles/ncomms2067?utm_source=chatgpt.com)

For this receiver, \(\mu=\nu/d^2\). Calibration error therefore needs to scale as \(M^{-1/2}\). The shared training record is retained throughout the argument; the bad-calibration probability contributes once.

## 3. Acquisition cost and the matching horizon obstruction

Two acquisition constructions are available:

| Construction | Sufficient consumed training count, fixed logical \(d\) |
|---|---:|
| Explicit finite measurements on individual outputs | \(O_d\!\left(D^3M\,\nu^{-2}\epsilon^{-2}\log(1/\alpha)\right)\) |
| Collective state tomography, followed by model fitting | \(\widetilde O_d\!\left(D^2M\,\nu^{-2}\epsilon^{-2}\log(1/\alpha)\right)\) |

The collective route uses positive states prepared through ordinary labelled inputs; it does not assume coherent access to the source’s Choi preparation. Its tomography rate comes from Haah–Harrow–Ji–Wu–Yu. I derived the additional stability estimate needed to preserve the \(D^2\) dependence. [arxiv.org](https://arxiv.org/abs/1508.01797?utm_source=chatgpt.com)

For the inherited flat family, \(D=2r\) and \(\nu=1/3\), giving
\[
N=\widetilde O\!\left(
\frac{r^2M}{\epsilon^2}\log\frac1\alpha
\right).
\]
The original \(1/3\) reset weight remains. The \(M\) payload preparations are additional.

I also derived an **\(\Omega(M)\) lower bound using genuinely noisy targets**. Two nearby noisy qubit phase sources can produce the same physical mixed payload from different logical inputs. At a phase separation of order \(M^{-1/2}\), their required \(M\)-datum decoded outputs have constant separation, while each training program distinguishes the sources only to order \(1/M\).

Therefore, at fixed physical dimension, noise and nontrivial accuracy, the horizon dependence is now matched:
\[
\boxed{\text{already noisy service: }\Theta(M)\text{ training copies}.}
\]

The earlier clean-data \(\Omega(M^2)\) result remains intact. No matching \(r^2M\) product lower bound has been established.

## 4. A second operation: exact programming with a prescribed reset

A separate construction reaches beyond the encoding family.

Suppose independent Choi programs of an arbitrary channel \(\mathcal T\) are supplied, together with a preparable reset state \(\omega\) and a known \(p<1\). Probabilistic exact port-based teleportation yields a finite processor implementing
\[
\boxed{p\,\mathcal T+(1-p)\mathcal R_\omega}
\]
**exactly**.

Successful teleportation branches implement \(\mathcal T\); every failure is filled with the prescribed reset. Excess successes are thinned to retain exactly weight \(p\). This uses the established EPR-resource port-based teleportation construction and its exact success formula. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7847469/?utm_source=chatgpt.com)

For a qubit input, my exact rational evaluation gives
\[
s_{16}=\frac{185517}{278528}<\frac23,
\qquad
s_{17}=\frac{795449}{1179648}>\frac23.
\]
Thus **17 product Choi programs suffice** for the exact channel
\[
\tfrac23\mathcal T+\tfrac13\mathcal R_\omega.
\]

Those programs are consumed. Programs for a noisy source do not automatically supply Choi programs for its clean component.

The same construction proves an adaptive composition inequality, even for a rank-deficient reset:
\[
\operatorname{dist}_{M,\mathrm{ad}}
\left(
p\mathcal T+(1-p)\mathcal R_\omega,\;
p\,\mathrm{id}+(1-p)\mathcal R_\omega
\right)
\le
\sqrt{kM\,[1-F_e(\mathcal T)]}.
\]

This exposes the next substantial connection: **which source geometries permit calibration in a metric compatible with finite exact programming?** The faithful-reset theorem answers one broad case. Extending the acquisition result to singular resets requires a new estimation argument; deleting the noise-floor parameter would not prove it.

## Status and retained boundaries

The proofs and executable checks are saved in place under  
`producer-workspace/p3_noisy_service_20261029`.

The run passed **667 finite assertions**, with maximum equality residual \(6.04\times10^{-14}\). These include reconstruction identities, fitted-decoder checks, tiny-weight examples, finite adaptive experiments, noisy-target fidelity identities and exact rational teleportation probabilities. They are diagnostics alongside analytical proofs, without independent review or an established priority claim. The global model optimizer, optimal collective tomography measurement and multiport circuit have not been implemented.

The device costs remain substantial: ambient-size control, classical fitting, synthesis precision, storage and payload handling are paid separately. Extract once, compute in trusted registers, and return once remains the direct route for a long computation on one datum. Record-versus-replay, instrument ambiguity, rare-component limits and the accepted resource/computability foundations are preserved.