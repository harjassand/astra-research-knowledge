# A complete fixed-depth alternative: thermally mixed Clifford fabrics

Research note, 5 November 2026. This note uses the accepted local inverse-noise
positivity theorem and accepted classical tree history-erasure lemma. It does
not re-prove either input, claim priority for thermal graph states, or establish
a practical resource advantage. Its new operation is the compilation of every
fault in a fixed physical Clifford preparation circuit into a one-dimensional
classical inverse problem, followed by a finite-bit solution of that problem.

## 1. Scope and concrete consequence

Let `U_N` be a specified geometrically local Clifford circuit of depth `d_U`,
range `R_U`, and bounded gate density. All three bounds are fixed independently
of chain length `N` and requested trace-distance error `epsilon`.

Begin with the independent classical thermal-bit distribution

\[
 \pi(s)=\prod_{i=1}^N
 \frac{e^{\beta J_i(-1)^{s_i}}}{2\cosh(\beta J_i)},
 \qquad 0<J_i\le J_{\max}<\infty.
\]

The delivered target is

\[
 \rho_N=U_N\Big(\sum_s\pi(s)|s\rangle\langle s|\Big)U_N^\dagger.
\]

In particular, take `U_N` to be a Hadamard layer followed by the two
nearest-neighbor CZ edge-color layers on an open chain. Then

\[
 H_N=-\sum_{i=1}^N J_iK_i,
 \quad K_1=X_1Z_2,\quad
 K_i=Z_{i-1}X_iZ_{i+1},\quad K_N=Z_{N-1}X_N,
\]

and `rho_N` is exactly its Gibbs state. This is a connected interacting quantum
family at every finite nonzero coupling. It has an explicitly entangled regime:
if `t_i=tanh(beta J_i)` and `t_i+t_{i+1}>1`, it is entangled across the cut
between sites `i` and `i+1`. To see this, the restrictions of `K_i,K_{i+1}` to
either half anticommute and square to identity. For every product state across
that cut their expectation vectors each have Euclidean norm at most one.
Cauchy-Schwarz gives `<K_i+K_{i+1}> <= 1`; convexity extends the bound to
separable states. The Gibbs state has expectation `t_i+t_{i+1}`. Uniform
`beta J > atanh(1/2)` therefore gives entanglement across every bulk cut, for
every chain length. This does not assert genuine N-partite entanglement.

The architecture is a **fixed-depth quantum fabric** of constant-size cells
with fixed nearest-neighbor quantum links. It is not a bank of permanently
quantum-isolated factories. Its coherent circuit depth, each causal cone, and
the lifetime of every fresh data qubit are bounded constants; its total output
contains N qubits. This explicit interpretation of a bounded factory is
essential.

## 2. Physical model and exact execution

Retain the acquired stationary Pauli apparatus model: every outgoing wire of
every specified preparation/gate/idle/delivery location suffers an independent
one-qubit Pauli channel, with total nonidentity probability at most `p`. A
homogeneous unknown channel is the simplest acquisition contract; finitely many
stationary location types also suffice with separately paid acquisition. Reset
and measurement use the same fixed physical templates as the accepted model.

The actual locations are:

1. Complete all sampling, digital error correction, timing preparation, and
   controller history erasure while no data qubits are carrying the output.
2. At a fixed common deadline, reset the N output cells.
3. Copy each regenerated classical sample bit into its fresh data qubit using
   an always-scheduled CNOT. The source bit is an actual noisy classical wire.
4. Execute the fixed circuit `U_N`, including its idle locations.
5. Deliver all physical data qubits at their already assigned chain positions
   after a specified, constant-depth terminal transfer/idle layer.

No quantum gate, routing path, output address, or coupler pattern depends on a
sampled partition. Every graph edge in the cluster example is always executed.
The physical CNOT in step 3 is itself noisy; no ideal raw selector is presumed.
Actual noisy classical computations and actual final source-bit noise remain
in the analysis below.

The noise assumption is substantive. An arbitrary missed CZ is a correlated
Clifford error, not generally a Pauli fault. Unknown coherent crosstalk,
long-memory drift, and unmodelled timing errors are not covered. Timing is a
fixed synchronous circuit-location contract. Eliminating random coupler masks
removes one control problem; it does not prove a reduction from arbitrary
hardware faults to the assumed Pauli law.

## 3. Compile the entire noisy quantum circuit

For a Pauli fault `P` at a circuit location, conjugate it through the remaining
Clifford suffix. The result is a Pauli `P_f`. Write

\[
 U_N^\dagger P_f U_N=\omega X^{v(P)}Z^{w(P)}.
\]

For every input bit string `s`, that fault therefore changes the final basis
label from `s` to `s xor v(P)`; its phase has no effect on this classical
mixture. Each physical location gives a convolution

\[
 K_\ell=\sum_{P\in\{I,X,Y,Z\}}q_{\ell,P}T_{v_\ell(P)}.
\]

The map from the one-qubit Pauli group modulo phases to syndrome translations
is a group homomorphism. The accepted inverse-noise theorem therefore applies
directly, with at most four labels per virtual location. There are `M=O(N)`
such locations. Their syndrome translations have constant interval diameter,
constant weight `w`, and bounded check incidence `d`; hence their overlap graph
has degree at most `D=w(d-1)`. All convolution factors commute, even though the
underlying quantum gates do not.

The regenerated classical input bit has a fresh BSC reference noise law and a
paid total coupling error. Include that reference BSC as one more virtual
location at the corresponding site. Include reset, load-CNOT, every gate and
idle, and terminal delivery errors. The resulting complete channel is

\[
 K=\prod_{\ell=1}^M K_\ell,
 \qquad
 \rho_{\rm physical}(\mu)
 =\sum_s(K\mu)(s)U_N|s\rangle\langle s|U_N^\dagger.
\]

This identity is about the actual fixed-depth noisy circuit, not a perfect
factory followed by a supplied output-noise abstraction.

For the cluster schedule with reset, load, H, two CZ layers and terminal
delivery, a conservative bound is `w<=3`, `d<=19` (six data fault layers on
at most three neighboring wires, plus the local classical-root event), and
`D<=54`. These are illustrative safe counts; the exact compiler can compute
smaller supports from the specified schedule. Different physical reset and
delivery templates require their own counts.

## 4. Positive preimage, with the actual constants retained

Put `lambda_max=2 beta J_max`, and let `q` bound the largest nonidentity rate
among every virtual location, including regenerated roots. By the accepted
inverse-noise theorem, the sufficient condition

\[
 \frac{2q}{1-2q}\,e^{w\lambda_{\max}}
 \le\frac{1}{32e^3(D+1)}
\]

implies

\[
 \mu=K^{-1}\pi\ge0,
 \qquad \sum_s\mu(s)=1.
\]

Sampling this classical law and executing the physical circuit gives the exact
target under exact parameters and exact classical sampling. Approximate
sampling, parameter estimation, reliable classical computation, and tree
coupling errors add to the final trace-distance budget because all subsequent
physical maps are channels.

These constants are mathematically nonvanishing but can still be very small.
For the illustrative cluster counts and `beta J_max=0.6`, the displayed bound
is approximately `q < 3.9e-7`; the component rate must be smaller again by the
actual amplification into controller-root noise. This is not a useful current
hardware threshold or a resource advantage claim. The construction nevertheless
avoids the enormous mixed-block length of the general noncommuting Gibbs
decomposition and provides a transparent finite-depth target class.

## 5. Independent finite-bit sampler

This section does not use the inherited all-temperature sampler's arithmetic
convention.

Each `K_l` acts on a fixed finite XOR group and is invertible for `q<1/2`.
Compute its inverse kernel `a_l` by a constant-size Fourier transform or linear
solve. Its coefficients may be signed. The Neumann estimate gives

\[
 \|a_\ell\|_1\le(1-2q)^{-1}=:A.
\]

The exact preimage has a signed factor-graph representation

\[
 \mu(s)=\sum_{z_1,\ldots,z_M}
 \left[\prod_{\ell=1}^M a_\ell(z_\ell)\right]
 \prod_{i=1}^N
 \pi_i\left(s_i\mathbin\oplus
       \bigoplus_{\ell}z_{\ell,i}\right).
\]

Every factor occupies an interval of uniformly bounded length, and only a
constant number of factors cross any cut. Thus this signed network has a
transfer representation of constant dimension `D_T`, depending only on the
fixed circuit range, depth and local alphabet. Prefix masses can be contracted
in polynomial time. Its total absolute expansion weight is at most `A^M`.

Here is a finite-bit sequential sampler that avoids assuming conditional
probabilities are bounded away from zero. For every visited prefix `u`, compute
its mass `a=mu(u)` and the mass `b=mu(u0)` to absolute error at most `eta`.
Clip the approximate conditional `b/a` into `[0,1]`; if the approximate
denominator is too small, choose any conditional distribution. For any true
prefix with `a>4 eta`, the conditional error is at most `C eta/a`. If
`a<=4 eta`, its true probability mass is at most `4 eta`, so arbitrary behavior
costs at most that mass. In both cases the contribution weighted by the true
prefix mass is at most `C' eta`.

The chain-rule coupling bound, or a hybrid sampler replacing one exact
conditional layer at a time, yields

\[
 d_{\rm TV}(\widehat\mu,\mu)
 \le C'\sum_{j=0}^{N-1}2^j\eta
 \le C'2^N\eta.
\]

Choose `eta=epsilon_s/(C'2^N)`. Although the absolute accuracy is exponentially
small, its precision is only

\[
 b=O\left(N+\log(1/\epsilon_s)+M\log A\right)
  =O\left(N+\log(1/\epsilon_s)\right)
\]

bits. The contraction is a fixed-width tensor network with `O(N)` arithmetic
operations per prefix in a simple implementation, so at most `O(N^2)`
constant-width arithmetic operations suffice for the whole sample. Reusing
suffix messages reduces this arithmetic count to linear in N; either version
already proves polynomial ordinary bit complexity. Factor approximation and
roundoff are budgeted using the explicit `A^M` bound, adding only `O(N)` guard
bits. Sampling rational conditional approximations to `O(b)` bits per step
adds at most `epsilon_s` when their conditional rounding budget is included.

No quantum subroutine and no growing quantum code appears in this sampler.

## 6. Actual classical boundary and records

The allowed protected classical computer samples the law with failure
probability `delta_c`; all of its computation, storage, fanout and routing are
paid. Its intended output is supplied as local-stochastic noisy classical leaf
pools, with parameter `q_c` below the accepted classical majority threshold.
This is a classical fault-tolerant digital output requirement, not a quantum
encoder. It can be implemented by ordinary reliable classical computation;
no quantum state must remain coherent during it.

Apply the accepted noisy ternary-tree compiler to each source bit, using a
fresh disjoint tree. With link/voter error bound `s<=.01`, depth `h` gives a
coupling discrepancy at most `q_c(21s)^h` per output, uniformly over arbitrary
old records. Choose

\[
 h\ge\frac{\log(Nq_c/\epsilon_t)}{\log(1/(21s))}.
\]

Then the total deviation from independent fresh reference BSC outputs is at
most `epsilon_t`. The physical root laws are included in `K`, not ignored.
The classical tree depth and number of classical wires can grow; the data
qubits are only reset after the tree output deadline. Trees use `O(N 3^h)`
noisy classical gates and corresponding routing/storage; this is a paid
polynomial in `N/epsilon_t` with potentially unfavorable exponent.

For delivery of a Gibbs state without a revealing correlated transcript,
erase the sampled bit string, sampler random seed and all retained controller
records after loading, using the accepted paid erasure convention. A retained
classical record of the sampled graph-basis label is a correlated extension,
not a product Gibbs output plus harmless metadata. The record may instead be
retained if that correlated extension is explicitly the requested operation.

This note does not assert that classical redundancy, a noisy final selector,
or a clock is free. The growth is shifted into classical control and
calibration. An implementation still needs the usual reliable-classical-
computation contract including its finite fanout, synchronization and raw
output interfaces; no growing quantum error correction is needed for it.

## 7. Acquisition and complete cost ledger

There are a constant number of stationary physical location types. Acquire
their Pauli laws with the accepted noisy-calibration template, or retain the
homogeneous common-channel contract. Let `L_C` be the complete paid number of
classical and quantum noisy locations whose acquired parameters are used in
the compiled reference process. Estimating each primitive parameter to
`delta_p=O(epsilon_a/L_C)` is a conservative sufficient precision: couple the
two full physical experiments location by location and charge their total
variation difference. This avoids concealing sensitivity of a deep classical
tree inside a constant.

Standard independent bounded observations require
`O(delta_p^{-2} log(1/delta_fail))` shots per calibrated constant-size template,
with its actual contrasts/visibility retained. If one instead acquires the
entire regenerated-root BSC as a repeatable classical template, the cost of
each such template includes its entire tree. Calibration constants and
stationarity over the commissioning/delivery interval are explicit assumptions.
No claim is made for arbitrary drifting apparatus.

Resources for one output include:

* `O(N)` fixed-position quantum output cells and `O(N)` fabricated
  nearest-neighbor quantum couplers; each cell has constant ancillary quantum
  workspace and constant quantum coherent lifetime.
* Constant quantum gate depth and `O(N)` noisy quantum locations after the
  final reset, plus every acquisition shot and reset needed beforehand.
* Polynomial finite-bit classical sampling; noisy classical protection; all
  regeneration trees, fanout, signal routing, waiting, and erasure.
* Paid metrology to accuracy dictated by the complete experiment, and the
  memory/time for its numerical estimates and circuit compiler.
* Simultaneous fixed-port delivery or an explicitly fixed, bounded-depth local
  terminal transfer. Long-term holding after delivery is a separate operation.

An energy model must charge those events, refrigeration, and erasure according
to the proposed hardware. This note gives event/spacetime counts and does not
invent a joule advantage. The classical apparatus may dominate total hardware
and execution time even though the quantum coherence requirement is bounded.

## 8. Matched comparison and earned conclusion

An ordinary ideal stabilizer preparation uses the very same constant-depth
H/CZ circuit. That already supplies the ideal source. Running it directly at
fixed component noise generally supplies a different graph-diagonal law `K pi`
and does not meet arbitrarily small global trace error. The present operation
changes the classical input law to `K^{-1}pi`; it does not improve the ideal
circuit depth or claim a new graph-state source.

Ordinary quantum fault-tolerant preparation can reduce the noise of that
circuit using growing code resources, subject to its physical output interface.
Give it the same cooling, links, calibration, classical controls and input
access. The demonstrated change here is that this explicit interacting,
entangled finite-temperature family needs no growing quantum code for global
delivery at all. It does not prove that its total resource cost beats such a
fault-tolerant implementation, especially under the conservative threshold and
tree/calibration costs above.

Known quantum error precompensation supplies the formal inverse idea. Thermal
graph states, Clifford circuits and classical noise-to-syndrome propagation
are standard. The completed content of this construction is the combination
with every fault in the finite circuit, an actual noisy classical boundary,
and a positive finite-bit efficiently sampled preimage. No claim is made that
this solves the random-partition composition problem for all noncommuting
one-dimensional Gibbs states.

The exact scientific consequence is therefore a representation-dependent
control separation: a physically specified connected and entangled many-body
Gibbs family can be delivered to arbitrary global trace accuracy with bounded
quantum coherent depth and cell size at fixed stochastic component noise,
while every accuracy-dependent resource is classical or metrological. The
stationary Pauli and fixed-circuit assumptions, fixed nearest-neighbor quantum
links, and potentially very small sufficient noise rate remain essential.

## 9. An exact failed extrapolation

`verify_cluster_boundary.py` retains a genuine finite-system boundary for this
particular six-layer circuit. For `N=8`, thermal bias `t=11/20`, depolarizing
total nonidentity rate `p=1/200` independently at every data-wire location,
and an independent input BSC of the same rate, exact rational Walsh inversion
gives `mu(11111111)=-2.606420378394434...e-7`, with three negative entries.
Its full channel has Walsh eigenvalue

\[
 \widehat K(S)=(149/150)^{a(S)}(99/100)^{|S|},
 \qquad
 \widehat\mu(S)=(5/9)^{|S|}(150/149)^{a(S)},
\]

where `a(S)` counts the virtual Pauli locations with a nontrivial syndrome
character. The executable specifies every translation and checks the sign
with rational arithmetic. Thus a half-percent component rate does not support
this target through this exact fixed fabric with only an input-law change.
Arbitrary coherent inputs do not rescue the same fixed channel: output graph
diagonals depend only on input diagonals under a Pauli/Clifford circuit, and
the required input diagonal is negative. This is not a general obstruction
to bounded factories, different circuits, added ancillas or correction.
