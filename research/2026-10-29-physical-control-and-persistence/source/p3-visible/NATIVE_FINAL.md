## A separation between certifying a quantum resource and acquiring its use

I have derived a stronger boundary: **constant negativity, bounded likelihood ratios, and a fixed global preparation-noise floor do not give a dimension-independent copy bound for obtaining a fixed operational advantage.**

The construction separates three tasks on the same noisy source:

| Task | Access supplied | Resource cost at fixed confidence |
|---|---|---:|
| Distinguish the constructed family from every PPT source | Independently prepared mixed copies | **\(\Theta(r)\) copies** |
| Learn enough to obtain half its available advantage in a specified discrimination experiment | Independently prepared mixed copies | **\(\Theta(r^2)\) copies** |
| Obtain that advantage when ordinary complex-conjugate copies are also available | Product copies of either orientation | **\(\Theta(r^2)\) copies** |
| Obtain that advantage with coherent preparation of a purification and its inverse | Preparation and inverse oracle calls | **\(O(r)\) calls**, an upper bound only |

The lower bounds allow arbitrary joint quantum measurements and unlimited computation. Standard quantum tomography matches the quadratic acquisition bound. The distinction is therefore about **access to information needed for a measurement**, rather than the speed of a particular learning algorithm.

These are new working derivations from this turn, not an independent review or a claim of established publication novelty.

### 1. A fixed resource with a growing acquisition cost

Let \(A\) be a qubit and let the reference \(R\) have dimension \(2r\). Write \(R\cong B\otimes F\), where \(B\) is a qubit and \(\dim F=r\), and define

\[
J_U=(I_A\otimes U_R)
\left(\Phi_{2,AB}\otimes\frac{I_F}{r}\right)
(I_A\otimes U_R^\dagger),
\]

\[
\tau=\frac{I_{4r}}{4r},
\qquad
\rho_U=\frac23J_U+\frac13\tau.
\]

Here \(\Phi_2\) is a normalized Bell-state projector. The unknown unitary \(U\) is **fixed across all copies**.

Every member has the same resource parameters:

\[
\rho_{U,A}=\frac{I_2}{2},
\qquad
\rho_{U,R}=\frac{I_{2r}}{2r},
\qquad
\frac{\tau}{3}\le \rho_U\le3\tau.
\]

Its partial transpose has eigenvalues

\[
-\frac1{4r}\quad\text{with multiplicity }r,
\qquad
\frac5{12r}\quad\text{with multiplicity }3r,
\]

so its negativity is exactly

\[
\mathcal N(\rho_U)=\frac14.
\]

The noise is a genuine global white-noise mixture of weight \(1/3\). For this family, the same state also results from local depolarization of \(A\) with strength \(1/3\).

Thus the growing acquisition cost does not come from a vanishing entanglement amount, a rare informative flag, or a diverging likelihood ratio.

### 2. The advantage is a concrete decision advantage

I use the standard Werner–Holevo discrimination construction:

\[
\Phi_+(X)=\frac{\operatorname{Tr}(X)I+X^T}{3},
\qquad
\Phi_-(X)=\operatorname{Tr}(X)I-X^T,
\]

with prior probabilities \(3/4\) and \(1/4\). Its weighted channel difference implements a scaled transpose. :chatgpt-content-reference{index="0"}

The receiver gets \(n\) training copies of \(\rho_U\). One additional, independently prepared copy passes through the selected channel on \(A\), and the receiver must identify the channel from its complete \(AR\) output and the training bank.

This is a **fixed-probe experiment**: replacing the supplied source copy with a separately prepared Bell pair changes the task.

Writing the two outputs as \(\omega_{\pm,U}\),

\[
\frac34\omega_{+,U}-\frac14\omega_{-,U}
=\frac12\rho_U^{T_A}.
\]

Consequently, a receiver informed of \(U\) achieves

\[
P_{\mathrm{informed}}
=\frac34+\frac12\mathcal N(\rho_U)
=\frac78.
\]

Every PPT fixed probe has success at most \(3/4\). The acquisition target is

\[
P_{\mathrm{learned}}\ge\frac{13}{16},
\]

which obtains half the available \(1/8\) advantage.

Both hypotheses arise through genuine channels applied to the same unknown source. They have equal marginals, share the global floor \(\tau/3\), and obey a two-sided relative likelihood bound of \(9\).

### 3. The controlling quantity is information about a fresh datum

The useful principle is more general than this example.

Suppose a latent parameter \(\theta\) determines an independently repeated source \(\rho_\theta\). Let \(T\) be a training bank, \(D\) one fresh source copy, and \(Z\) an independent label selecting a known channel. If every label channel sends the average source to the same state, then its output \(Q\) satisfies

\[
\boxed{I(Z:TQ)\le I(T:D).}
\]

The proof is a short chain of conditional mutual information and data processing:

\[
I(Z:TQ)
=I(Z:T\mid Q)
\le I(T:QZ)
\le I(T:DZ)
=I(T:D).
\]

**Information accumulated inside the training bank is useful for this decision only to the extent that it predicts the fresh system.**

For the constructed family, let

\[
\Omega_k=\mathbb E_U[\rho_U^{\otimes k}],
\qquad
F_k=D\!\left(\Omega_k\middle\|\tau^{\otimes k}\right).
\]

Then

\[
I(T:D)=F_{n+1}-F_n.
\]

I adapted the entropy-increment mechanism from Astra’s [N1104 mixed-flag lower bound](https://github.com/harjassand/astra-research-knowledge/blob/c64402f357e69975df195c4925cb882f5d4b8177/research/2026-10-27-dot-scientific/source/quantum_operational_certification_20261024/mixed_flag_quadratic_choi_program_lower_bound.md). Exchangeability and strong subadditivity give

\[
F_{n+1}-F_n\le\frac{F_{2n}}n.
\]

A Haar-overlap calculation, using the established logarithmic Sobolev inequality on \(SU(2r)\), yields

\[
F_k\le \frac{256}{81}\frac{k^2}{r^2},
\qquad
I(Z:TQ)\le\frac{1024}{81}\frac{n}{r^2}.
\]

The concentration inequality is a known input; the application and constants here are part of the new derivation. :chatgpt-content-reference{index="1"}

Binary Fano then forces

\[
n\ge
\frac{81}{1024}
\left[h\!\left(\frac14\right)-h\!\left(\frac3{16}\right)\right]r^2
>0.00630\,r^2
\]

to reach the target success probability. Here \(h\) uses natural logarithms.

This also gives an exact representation of the acquired advantage:

\[
\boxed{
A_n=
\frac12\,
\mathcal N_{A_{n+1}:T R_{n+1}}(\Omega_{n+1}).
}
\]

The relevant negativity belongs to the averaged **training-plus-fresh-system state**. This representation is explanatory; materializing its \((4r)^{n+1}\)-dimensional matrix is not supplied for free. An exact two-copy calculation further shows that **one training copy gives zero advantage for every \(r\ge2\)**.

### 4. Certification is provably cheaper

The linear-copy certificate tests the family against **every independently repeated PPT state**, without assuming its marginals.

On \(n\) copies, measure

\[
\widehat\mu=
\binom n2^{-1}
\sum_{i<j}
\left(F^{AR}_{ij}-F^R_{ij}\right),
\]

where \(F\) denotes a swap. Its expectation is

\[
\mu=\operatorname{Tr}\rho^2-\operatorname{Tr}\rho_R^2.
\]

For a qubit \(A\), PPT implies the reduction inequality

\[
\rho\le I_A\otimes\rho_R,
\]

and hence \(\mu\le0\). For every constructed \(\rho_U\),

\[
\mu=\frac1{12r}.
\]

The useful step is controlling the variance of the collective observable despite its overlapping terms. With

\[
G=I_A\otimes\rho_R,\quad
t=\operatorname{Tr}\rho(\rho-G)^2,\quad
s_2=2(1-\operatorname{Tr}\rho_A^2),
\]

the exact identity is

\[
\operatorname{Var}(\widehat\mu)
=
\frac{s_2-\mu^2}{\binom n2}
+
\frac{6\binom n3}{\binom n2^2}(t-\mu^2).
\]

For PPT states, \(t\le-\mu\). For the alternative family,

\[
t-\mu^2=\frac1{12r^2}.
\]

Thresholding at \(1/(24r)\), **\(2048r\) copies suffice with both errors below \(1/8\)**. Conversely, the same overlap estimate and Pinsker’s inequality require \(\Omega(r)\) copies, even just to distinguish the family from \(\tau\).

The measurement is constructive: the two sums of swaps commute and can be measured through Schur transforms. Known circuits have cost polynomial in copy number, physical dimension, and logarithmic inverse implementation error. Direct collective storage uses \(O(n\log(4r))\) qubits. :chatgpt-content-reference{index="2"}

One limitation is retained: this particular certificate detects the more general mixture \(cJ_U+(1-c)\tau\) only when \(c>1/\sqrt3\), although negativity begins at \(c>1/3\). Its linear upper bound has not been extended to that entire interval.

### 5. What changes the acquisition boundary

**Conventional tomography matches the quadratic bound.** In dimension \(4r\), standard tomography gives fixed trace-norm accuracy with \(O(r^2)\) copies. Measuring the sign of the estimated partial transpose then achieves the required decision advantage. The regret is bounded by the trace-norm estimation error. This pays for a dense classical description and measurement synthesis; the resulting decoder can be reused. :chatgpt-content-reference{index="3"}

A receiver using fresh consumed copies through Hermitian-preserving map exponentiation also achieves \(O(r^2)\), without reconstructing the whole state. That uses the public exponentiation construction and the inherited N1102 treatment of decision regret; it is not a newly invented exponentiation primitive. :chatgpt-content-reference{index="4"}

**Ordinary conjugate copies do not improve the exponent.** For any fixed mixture of \(\rho_U\) and \(\rho_U^*\) programs, their pair overlaps remain identical. Appending fresh original copies restores the exchangeability needed for the entropy-increment argument. The quadratic lower bound survives. Classically adaptive requests for either kind change constants only.

**Coherent purification preparation and its inverse do change the available construction.** Granted those oracles, the known BELT construction block-encodes \(\rho_U^{T_A}/2\). Its spectral gap around zero is \(1/(8r)\). A standard QSVT sign approximation therefore gives the decision measurement using \(O(r)\) oracle calls at fixed error, without postselection. :chatgpt-content-reference{index="5"}

That is an upper bound under stronger access. Preparing and coherently reversing the purification—including the relevant noise environment—is an additional resource. I have not proved a matching coherent-query lower bound.

### Scope and research status

The resulting boundary is concrete: **negativity, likelihood and a global noise floor cannot by themselves specify a uniform acquisition budget for this fixed-probe inference task.** A predictive-information or preparation-access contract is also necessary.

The construction survives finite preparation precision. If \(\|U-V\|_{\mathrm{op}}\le\epsilon\), the training-plus-output trace distance changes by at most

\[
\frac23(n+1)\epsilon.
\]

Thus finite circuit approximations with error of order \(r^{-2}\) preserve the quadratic lower bound up to constants. Their preparation, description and synthesis costs remain separate. Haar averaging is a proof device, not a requirement to physically prepare an infinitely precise random unitary.

I completed **68 exact-arithmetic checks** of the noncommuting overlap identities, variance formula, PPT inequality and noisy-family moments. They corroborate the analytic derivation; they are not an external review. The accepted N675 dependencies, N972/N677 foundations, earlier repairs and computability results remain unchanged, including the SLD-specific scope of the no-cutoff deduction.

The workspace could not initialize, so **no durable proof or code file was saved this turn**. The theorem and proof argument are recorded here.

The consequential unresolved question is now sharper: **which physically specified controls over a source can reduce this acquisition cost, and what does obtaining those controls itself require?** The mixed-copy and coherent-preparation contracts already produce different answers.