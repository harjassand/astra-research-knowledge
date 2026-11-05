# Classical failure records cannot complete the crossed reader

## Scope

This result concerns the actual homogeneous tracial partial-SWAP source,
but only a specified class of receiver completions. It permits arbitrary
quantum memory, computation, and continuation on failure branches. It
does not cover fully coherent success/failure histories or extra quantum
bond information retained on a success.

Write \(c=\cos\theta\), \(s=\sin\theta\), and \(g=1+3s^2\). Initialize
receiver qubits \(R,A\) in a Bell state. A successful encounter applies

\[
 K_{AE}=\frac{cI-2is\Phi_{AE}}{\sqrt g}
\]

and discards the spent carrier, retaining exactly the two-qubit folded
statistic on \(R,A\). The success/failure outcome is measured or dephased.
On a failure the receiver may keep arbitrary additional systems and
perform an arbitrary subsequent operation. Any further restriction on
the failure branch is unnecessary for the result.

## The all-continuation bound

Let \(\rho_n^\pm=\sigma_n\pm\delta_n\) be the joint source/receiver states
conditioned on the first \(n\) encounters all succeeding, for the
orthogonal source inputs \(|0\rangle,|1\rangle\). These states are
normalized. Define

\[
 D_n=\|\delta_n\|_1 .
\]

Every eventual recovery operation, regardless of its later physical
cost, has half-diamond error at least

\[
 \boxed{\quad
 \epsilon\ \ge\ \frac{g^{-n}}2(1-D_n)
 \quad}
\]

for every prefix \(n\) to which the specified success rule applies.
The conclusion still holds if the receiver is granted the true source
at that prefix.

**Proof.** The probability of the all-success event is \(p_n=g^{-n}\),
independent of the input. This is the exact normalization of the folded
channel, not an independence approximation. Because the flag has been
dephased, the two possible accessible joint source/receiver states have
trace distance at most

\[
 p_nD_n+(1-p_n).
\]

The second term grants perfect distinguishability on the union of all
failure branches and hence grants any quantum records retained there.
All future encounters with independent tracial carriers and all future
receiver actions are a CPTP continuation of this cut, even when the
source is included among the accessible systems. They cannot increase
the distance. A recovered identity channel of half-diamond error
\(\epsilon\) must distinguish these two inputs with trace distance at
least \(1-2\epsilon\). Combining the two statements gives the bound.

## A fixed-size exact expression

The following formula is inherited from the independently constructed
folded-statistic calculation in
../online/crossed_statistic_obstruction.txt and its executable
../online/verify_crossed_statistic.py.

Use source Pauli operators \(S_a\), receiver Pauli operators \(R_a\),
and time-reversed Pauli operators
\(\widetilde A=(X_A,-Y_A,Z_A)\). Put

\[
 Q=\sum_aS_a\widetilde A_a=4\Phi_{SA}-I,
\]

\[
 u=c^{2n},\qquad v=(1-s^4)^n,\qquad
 w=[c^2(c^2-s^2)]^n,\qquad h=nc^{2n-1}s^3 .
\]

Then

\[
 \sigma_n=\frac{I_S}{2}\otimes
 \left[u\Phi_{RA}+(1-u)\frac{I_{RA}}4\right]
\]

and

\[
\begin{aligned}
8\delta_n={}&uS_z+(1-v)R_z+\frac v3R_zQ\\
&+\frac u2\sum_aR_a(S_z\widetilde A_a-S_a\widetilde A_z)\\
&+w\sum_aR_a\left[
\frac{S_z\widetilde A_a+S_a\widetilde A_z}{2}
-\frac{\delta_{az}}3Q\right]\\
&+h\left[R_x(S_y-\widetilde A_y)-R_y(S_x-\widetilde A_x)\right].
\end{aligned}
\]

Thus the theorem is evaluable by diagonalizing a fixed \(8\times8\)
Hermitian matrix. For example, at \(\theta=0.1,n=25\), ordinary
double-precision evaluation gives

\[
 D_n\simeq0.8189685947225367,\qquad
 \frac{g^{-n}}2(1-D_n)\simeq0.0433357252129197 .
\]

The exact expression above is the mathematical bound; these decimals
are an arithmetic illustration, not a physical-device simulation or an
interval-arithmetic certificate.

## Elementary positive constant without diagonalization

The same obstruction has a simple analytic weak-action limit. Pauli
orthogonality gives

\[
 \operatorname{Tr}(\rho_n^+\rho_n^-)
 =\operatorname{Tr}(\sigma_n^2)-\operatorname{Tr}(\delta_n^2)
 =\frac18\left[
 u^2+2v-\frac43v^2-\frac53w^2-4h^2\right].
\]

For density matrices, their root fidelity squared is at least their
Hilbert-Schmidt overlap. The fidelity/trace-distance inequality therefore
implies, whenever the displayed overlap is nonnegative,

\[
 D_n\le
 \sqrt{1-\operatorname{Tr}(\rho_n^+\rho_n^-)}.
\]

Choose \(n\theta^2\longrightarrow\log(5/4)\) as
\(\theta\longrightarrow0\). Then

\[
 u\to\frac45,\quad v\to1,\quad
 w\to\left(\frac45\right)^3,\quad h\to0,\quad
 p_n\to\left(\frac45\right)^3=\frac{64}{125}.
\]

The overlap tends exactly to \(1359/12500\). Consequently every receiver
completion in the stated class obeys

\[
 \boxed{\quad
 \liminf_{\theta\to0}\epsilon
 \ \ge\
 \frac{32}{125}
 \left(1-\sqrt{\frac{11141}{12500}}\right)
 \ >\ 0.014 .
 \quad}
\]

This obstruction arises on the faster \(\theta^{-2}\) prefix scale,
before the full bath has acquired the payload on the \(\theta^{-4}\)
scale. It remains even if the failure histories carry unbounded memory.

## Why coherent flags are different

For the isometric completion

\[
 W=|0\rangle K+|1\rangle L,\qquad
 L=\frac{2s(I-\Phi)}{\sqrt g},
\]

the success/failure off-diagonal operators remain available if the flag
is retained coherently. The accessible states need not be a direct sum
of the success and failure states. The convex trace-distance step in the
proof then does not apply. No bound here rules out that coherent route.
Likewise, additional quantum information preserved on every success
changes \(\rho_n^\pm\) and can evade the theorem.

This is a completion obstruction for a particular acquired statistic,
not a general memory bound for the physical source.
