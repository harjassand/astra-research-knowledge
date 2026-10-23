# Independent cross-check of the unflagged logarithmic reconstruction

Reviewer: `exact_initializer_review`, checking a second, distinct load-bearing step without relying on another review's conclusion.

Date: 21 October 2026. Status: **the proposed reconstruction gives a valid analytic matching upper bound and, together with the independently rechecked first-failure converse, proves the stated two-term asymptotic law for the specified exact Bell-output task.** This reviews the supplied reconstruction, not an unavailable producer archive. No numerical check count is used as proof.

## 1. Task and conventions

Fix an integer `J≥1`. Every call has one output qubit on Alice's side and one on Bob's side; any finite external input ports are ignored by the construction. The first `J` outputs must be exactly `B_+=|Φ_+><Φ_+|`, where `|Φ_+>=(|00>+|11>)/sqrt(2)`. Equivalently the complete useful output state is `B_+^{⊗J}`. Its purity automatically implies independence of those outputs and their lack of correlations with the remaining memory.

Return error is **half** the trace norm of the complete memory difference. Let `R_term(J,δ)` be the infimum of `E_R(τ)` over admissible devices/normal initializers supplying these outputs and satisfying terminal return at call `J` within `δ`. Let `R_all(J,δ)` impose that bound after every prefix `j=1,…,J`. All logarithms and entanglement units here are natural-log units.

The asymptotic statement below is for fixed `J` and `δ↓0`:

\[
R_{\rm term}(J,\delta)=R_{\rm all}(J,\delta)
=\frac{J\ln2}{2\delta}-\ln(1/\delta)+O_J(1).
\tag{1}
\]

The equality in (1) is an equality of asymptotic expressions, **not** a claim that the two infima agree exactly for each finite parameter. “Minimum” in an informal notation must not be read as an attained optimization unless attainability is separately proved. The construction uses a single fixed countable-memory device for the entire family; the law does not claim that every arbitrarily prescribed fixed device has these attainable costs.

## 2. State and exact operation

Set `L≥1`, `M=J+L−1`, and define the separable two-qubit state

\[
C=\frac{|00\rangle\langle00|+|11\rangle\langle11|}{2}
 =\frac{B_++B_-}{2},
\quad |\Phi_-\rangle=(|00\rangle-|11\rangle)/\sqrt2.
\]

For `0≤k≤M`, put

\[
\rho_k=B_+^{\otimes k}\otimes C^{\otimes(M-k)},
\qquad
\tau=\frac1L\sum_{k=J}^{M}\rho_k.
\tag{2}
\]

There is **no retained register identifying the sampled value of `k`**. Equation (2) is an unflagged mixture. A sampled preparation may know `k`, but that label must be discarded before the designated initial state is supplied to the device. If the label is retained anywhere in the counted shared memory, the entropy reduction derived below is no longer the claimed resource value.

Each call releases the first qubit from each memory string, shifts the rest left, and appends one shared fair classical bit as `C`. Generating that bit requires only one finite two-outcome local instrument and one classical message. It supplies no entanglement. All outcomes are included; there is no success conditioning.

For every `j≤J`, all components of (2) have at least `j` initial Bell cells, giving the complete output-memory state

\[
\Omega_j=B_+^{\otimes j}\otimes\tau_j,
\qquad
\tau_j=\frac1L\sum_{k=J}^{M}\rho_{k-j}.
\tag{3}
\]

The same operation is defined after exhaustion; it eventually replaces every cell by `C`. More generally at any horizon, each original component contributes `B_+^{⊗min(k,j)}⊗C^{⊗(j-k)_+}` to outputs and `B_+^{⊗(k-j)_+}⊗C^{⊗[M-(k-j)_+]}` to memory. Their unflagged mixture includes all branches and any resulting output-memory correlations. Thus the construction is a finite consumable reservoir, not a recurrent resource.

## 3. One fixed normal finite-outcome device

To keep the device and memory spaces fixed while `M` varies, use

\[
\mathcal H_C=\bigoplus_{M\geq1}(\mathbb C^2)^{\otimes M}
\]

on each side. This is separable. The construction at a given `M` is supported on the matching `(M,M)` local sectors; the deterministic sector label is a product label and adds no entanglement.

For each shared coin result `b∈{0,1}`, define a local isometry

\[
V_b|q_1\ldots q_M\rangle_M
=|q_1\rangle_{\rm out}\otimes|q_2\ldots q_Mb\rangle_M
\tag{4}
\]

and extend it block diagonally to the whole direct sum. The `M=1` formula is `|q_1>_1↦|q_1>_out⊗|b>_1`. Because images from different `M` sectors are orthogonal, `V_b^*V_b=I` on the entire memory space. The global channel has two product Kraus operators

\[
K_b=\frac1{\sqrt2}V_b^A\otimes V_b^B,
\quad b=0,1,
\quad \sum_bK_b^*K_b=I.
\tag{5}
\]

Alice can implement the two Kraus outcomes and send `b` to Bob, who applies his conditional isometry. This is a fixed finite-round, two-outcome LOCC operation. Its finite Kraus form defines a normal CPTP channel. It does not measure `M`, communicate an unbounded label, or require countably many measurement outcomes. It is also defined on unequal local sector pairs and on coherences between sectors; the proof does not rely on an undefined extension outside the initializer's support. Ignoring a finite-dimensional external input is a local trace operation and causes no difficulty.

Appending `C` need not retain an additional persistent classical transcript: the coin is used for preparation, and no extra label remains between calls. If a model required every past outcome to remain forever in the memory, this would be a different return task. The present handoff counts every retained register and all branches in the average operation; (5) respects that convention.

## 4. Return error, with the factor of two explicit

When `j≤L`, cancel the common summands of (2) and (3):

\[
\tau_j-\tau
=\frac1L\left(\sum_{r=J-j}^{J-1}\rho_r
 -\sum_{r=M-j+1}^{M}\rho_r\right).
\]

Each of the two sums contains `j` normalized states. Therefore

\[
\|\tau_j-\tau\|_1\leq\frac{2j}{L},
\qquad
\frac12\|\tau_j-\tau\|_1\leq\frac{j}{L}.
\tag{6}
\]

For `j>L` the right side of the half-norm inequality is at least one and the estimate is trivial. Thus the half-return bound holds for all useful prefixes. Choosing

\[
L=\lceil J/\delta\rceil
\tag{7}
\]

ensures it after every call `j≤J`. Equality in (6) is not claimed: the unflagged component states are not orthogonal. The upper bound is enough for the asymptotic law.

## 5. Resource identity, independently derived

The state `τ` is maximally correlated in the computational basis:

\[
\tau=\sum_{x,y}a_{xy}|xx\rangle\langle yy|,
\qquad
\tau_A=\tau_B=2^{-M}I.
\]

Its computational diagonal is the separable state `Δτ=2^{-M}Σ_x|xx><xx|`, and hence

\[
E_R(\tau)\leq D(\tau\Vert\Delta\tau)=M\ln2-S(\tau).
\tag{8}
\]

A direct lower bound avoids depending on an unexamined maximally-correlated-state formula. Every finite-dimensional separable `γ` obeys the reduction inequality `γ≤I_A⊗γ_B`, since each local factor of a separable-state decomposition is bounded by the identity; continuity extends this to all separable states. Operator monotonicity of logarithm, with full-rank regularization when needed, gives

\[
D(\tau\Vert\gamma)
\geq -S(\tau)-\operatorname{Tr}\tau_B\ln\gamma_B
=S(\tau_B)-S(\tau)+D(\tau_B\Vert\gamma_B)
\geq M\ln2-S(\tau).
\tag{9}
\]

For the countable direct-sum embedding, a local CPTP operation can project to the fixed `M` sector and reset its complement to a local state inside that sector, leaving `τ` invariant and preserving separability. Data processing thus reduces the infimum to the finite sector; an initializer in a larger direct sum cannot decrease the value below (9). Combining (8)–(9),

\[
\boxed{E_R(\tau)=M\ln2-S(\tau).}
\tag{10}
\]

This derivation includes the deterministic `M` label and does not omit an entangled sector register.

## 6. The logarithmic entropy saving

All `ρ_k` commute in the tensor-product Bell-sign basis. Introduce an analytical random variable `K` uniform on `{J,…,M}`; conditioned on `K=k`, let the first `k` signs of `Y∈{+,−}^M` be `+` and the remaining signs be independent fair bits. These are the eigenvalue probabilities of `τ`, so `S(τ)=H(Y)` exactly.

The elementary entropy chain rule gives

\[
S(\tau)=\ln L+(M-\mathbb E K)\ln2-H(K\mid Y),
\quad \mathbb E K=J+\frac{L-1}{2}.
\]

Consequently

\[
\boxed{
E_R(\tau)=\left[J+\frac{L-1}{2}\right]\ln2-\ln L+H(K\mid Y).
}
\tag{11}
\]

Although `K` is used to analyze the mixture, it is not a retained physical register. Confusing those roles would replace the resource by the flagged average and remove the desired term.

Given a string `y`, let `s` be its first minus position, using `s=M+1` for the all-plus string, and set `R=min(s−1,M)`. Exactly the values `J≤k≤R` are compatible. Their likelihoods satisfy

\[
\Pr(Y=y\mid K=k)=2^{-(M-k)},
\quad
\Pr(K=k\mid Y=y)=\frac{2^k}{\sum_{u=J}^{R}2^u}.
\]

Thus `r=R−K` has a truncated geometric distribution

\[
\Pr(r\mid y)=\frac{2^{-r}}{Z_N},\quad
0\leq r\leq N=R-J,
\quad Z_N=\sum_{r=0}^{N}2^{-r}\leq2.
\]

Its mean is

\[
\mathbb E(r\mid y)=1-\frac{N+1}{2^{N+1}-1}\leq1.
\]

Therefore

\[
H(K\mid Y=y)=\ln Z_N+\mathbb E(r\mid y)\ln2\leq2\ln2,
\]

and hence

\[
0\leq H(K\mid Y)\leq2\ln2. \tag{12}
\]

Equations (11)–(12) prove the uniform finite bound

\[
\left[J+\frac{L-1}{2}\right]\ln2-\ln L
\leq E_R(\tau)
\leq\left[J+\frac{L-1}{2}\right]\ln2-\ln L+2\ln2.
\tag{13}
\]

With (7), the upper bound is

\[
R_{\rm all}(J,\delta)
\leq\frac{J\ln2}{2\delta}-\ln(1/\delta)
 +J\ln2-\ln J+2\ln2.
\tag{14}
\]

The displayed constant is conservative. No optimization of its value is needed or claimed.

## 7. Independent recheck of the matching converse

Take any admissible device whose `J`-call block `T` has

\[
T(\tau)=B_D\otimes\tau',\quad D=2^J,
\quad \tfrac12\|\tau'-\tau\|_1\leq\delta.
\]

`B_D` is the joint maximally entangled state of the `J` output pairs. Define the trace-nonincreasing CP success map

\[
S(x)=\operatorname{Tr}_{\rm out}[(B_D\otimes I)T(x)(B_D\otimes I)].
\]

Then `S(τ)=τ'`, and `s_m=Tr S^m(τ)` is the probability that the first `m` blocks pass Bell tests. Since `(S^*)^{m-1}(I)` is an effect and `τ'−τ` has trace zero,

\[
s_m-s_{m-1}
=\operatorname{Tr}[(S^*)^{m-1}(I)(\tau'-\tau)]\geq-\delta.
\]

Together with `s_1=1`, this yields `s_m≥[1−(m−1)δ]_+`.

Repeat the actual device block `N` times, retaining all external outputs, and only then perform the Bell tests. Let `F` count initial successes, capped at `N`. Its actual law `p` is supported on `{1,…,N}` and `E F=Σ_{m=1}^N s_m`. From any separable initializer `γ`, the entire unconditioned output is separable across all Alice outputs versus all Bob outputs. Therefore the probability of passing its first `k` Bell tests is at most `D^{-k}`; in particular its law `r` obeys `r_k≤D^{-k}`. Relative-entropy data processing gives

\[
D(\tau\Vert\gamma)
\geq D(p\Vert r)
\geq \ln D\,\mathbb EF-H(p)
\geq J\ln2\sum_{m=1}^{N}[1-(m-1)\delta]_+-\ln N.
\tag{15}
\]

The Bell tests are analytical distinguishability measurements. No separability after global Bell postselection is asserted. The bound uses separability before the tests and includes all temporal correlations.

Choosing `N=ceil(1/δ)` and writing `N=1/δ+θ`, `0≤θ<1`, gives

\[
\sum_{m=1}^{N}[1-(m-1)\delta]_+
=\frac1{2\delta}+\frac12+\frac\delta2\theta(1-\theta)
\geq\frac1{2\delta}+\frac12.
\]

Infimizing (15),

\[
R_{\rm term}(J,\delta)
\geq J\ln2\left(\frac1{2\delta}+\frac12\right)
 -\ln\lceil1/\delta\rceil.
\tag{16}
\]

Since `R_term≤R_all`, (14) and (16) sandwich both resource functions and prove (1). The lower bound needs only terminal return; the construction satisfies every-use return. This distinction is explicit rather than erased by notation.

## 8. Resource accounting and conclusion

One explicit preparation samples `K`, supplies exactly `K` Bell pairs and `M−K` separable `C` cells, then discards the label. Its **expected Bell consumption is `E K=J+(L−1)/2`**, with maximum `M`. The intrinsic relative entropy after discarding the flag is smaller by

\[
\ln L-H(K\mid Y).
\]

This proves a logarithmic saving in the chosen state monotone. It does **not** demonstrate a matching saving in exact one-shot Bell formation cost, expected Bell consumption of the supplied preparation, energy, hardware, or a physical implementation. Initializing a mixed state and forgetting a classical label cannot justify subtracting the erased information from the actual resource ledger of that preparation.

The normal direct-sum device, exact complete useful outputs, full/half return conversion, unflagged-state entropy, posterior entropy bound, and first-failure converse all survive this review. The two-term law is therefore independently reconstructed analytically within the stated optimization task. Whether the producer used this exact argument, the producer's finite-check claims, external mathematical certification, and historical priority remain separate unverified matters. No additional reservoir family or additive-constant campaign is justified by this cross-check.
