# Expander mixed-probe certification and mixed-output memory

This is a separate constructive result from P1's package. **Read the [complete governing derivation](../package/expander_mixed_bath_companion.txt).** It supplies explicit mathematical arguments while importing stated quantum-expander constructions and standard capacity coding. No companion-specific independent audit artifact is supplied; the main theorem's audit is not extended to this note. Publication adds no reproof or scientific execution.

The note has two substantial operations: a quantitative mixed-probe test for fidelity and quantum memory, and a constant-source mixed collision-stream construction whose **whole output** requires large retained quantum memory. These are not premises of the main hidden-noise theorem.

## Exact test contract

On dimension N, let the known observables H_j be traceless Hermitian involutions, with positive weights p_j summing to one. Require the **quantitative** commutator gap

```text
sum_j p_j ||[K,H_j]||_2^2
    >= kappa ||K-(Tr(K)/N)I||_2^2
```

for every complex matrix K. The Hilbert–Schmidt norm is unnormalised. A scalar commutant alone does not provide this dimension-uniform gap.

For known `0<a<=1`, prepare `tau_(j,±)=(I±aH_j)/N`. In each trial choose j with probability p_j and a fair sign b, pass the specimen through the same channel T, measure H_j with outcome h, and record `Y=b h`. Then

```text
S(T) = E[Y] = (a/N) sum_j p_j Tr[H_j T(H_j)].
```

The preparation setting **must remain hidden from the device**, with no side channel. Otherwise it could discard the specimen and reprepare the announced state. All quantum systems crossing the storage cut count toward memory, including entanglement halves, quantum records and external delay lines. Trusted preparation and readout are explicit premises. [Source, lines 13–41](../package/expander_mixed_bath_companion.txt#L13-L41).

## Rigidity becomes an operational fidelity and memory bound

For any CPTP T with Kraus operators K_alpha, including a nonunital channel,

```text
sum_alpha ||[K_alpha,H]||_2^2 = 2N-2 Re Tr[H T(H)]
F_e(T) = sum_alpha |Tr K_alpha|^2 / N^2
F_e(T) >= 1-(2/kappa)[1-S(T)/a].
```

If all probes are preserved to **full trace-norm** error epsilon, this gives `F_e>=1-2epsilon/(a kappa)`.

Suppose the common compression/reconstruction channel factors through quantum memory dimension at most m in each classical branch; unlimited classical records are allowed. Every composite Kraus operator has rank at most m, so `F_e<=m/N`. Therefore

```text
m >= N {1-(2/kappa)[1-S(T)/a]}
m >= N [1-2epsilon/(a kappa)]       under the preservation condition.
```

Negative lower bounds are vacuous. A fixed finite mixed-state family can therefore require almost its entire ambient quantum dimension for robust **single-specimen blind preservation**. This does not apply when the preparation label is supplied or the task is only one preselected measurement. A small alphabet, small Holevo-information bound or zero preparation-channel capacity does not itself bound this memory cost. [Source, lines 43–99](../package/expander_mixed_bath_companion.txt#L43-L99).

### Heralding keeps its success cost

For a trace-decreasing success map Q, define average success `s=Tr Q(I)/N` and the unconditional signed score `S(Q)`. Count every trial; failure contributes zero to both the signed score and success indicator. For `s>0`,

```text
F_e(Q) >= s-(2/kappa)[s-S(Q)/a]
F_e(Q) <= s m/N
m >= N {1-(2/kappa)[1-S(Q)/(a s)]}.
```

Input-dependent success is allowed. All settings and failures must be recorded. Conditional score alone does not establish ordinary quantum capacity; low success and nonlinear normalisation are still paid. [Source, lines 101–128](../package/expander_mixed_bath_companion.txt#L101-L128).

## Acquire the probes from one biased qubit

A known quantum expander on dimension D with conjugation contraction `1-gamma` yields a lifted family on `N=2D`:

```text
H_X = X_f tensor I
H_Z = Z_f tensor I
H_j = |0><1|_f tensor U_j + |1><0|_f tensor U_j^dagger
p_X=p_Z=1/4, p_j=1/(2k), kappa=gamma/5.
```

The construction handles non-Hermitian U_j and arbitrary complex K. Each probe is prepared from `[(I+aZ)/2] tensor I_D/D` using a controlled U_j and a flag Hadamard; measurement applies the inverse circuit and reads the flag. No entangled reference is retained during the test.

The tested register uses one biased qubit, or one pure qubit when `a=1`. This is **not** a claim that the controller, calibrated gates, preparation and readout need only one clean qubit. The supplied Gross–Eisert choice has 20 states and 10 observables with efficient circuits in `log D`; circuit precision and total implementation error remain paid. It does not itself supply the constant-buffer streaming example below. [Source, lines 130–189](../package/expander_mixed_bath_companion.txt#L130-L189).

## Finite data, trusted errors and capacity

For independent repetitions of a fixed channel and a valid combined preparation/measurement score-bias bound nu,

```text
S_low = S_hat-sqrt[2 log(1/delta)/M]-nu.
```

Substitute this into the fidelity and memory inequalities. The conservative trial count for fixed target infidelity eta is `O((a kappa eta)^-2 log(1/delta))`, independent of N. Every trial still prepares, routes, stores and measures a `log N`-qubit register.

With `a=1`, zero signed-test failures and appropriately accounted trusted errors, the one-sided binomial bound gives the improved sufficient count `M>=4 log(1/delta)/(kappa eta)`. This zero-failure regime does not extend unchanged to `a<1`, which has intrinsic baseline failure `(1-a)/2`. Heralded tests estimate success and unconditional score from complete logs; conservative ratio estimation can cost order `1/s^2`.

For g elementary preparation/readout gates with error p each, the note charges `nu=O(gp)` plus state-preparation and readout errors. Fixed gate error is not automatically harmless as the circuit grows. A circuit description does not manufacture a laboratory calibration bound.

For an ordinary trace-preserving **memoryless** repeated-use channel with `F_e>=1-eta`, `0<=eta<=1/2`, the standard coherent-information coding theorem gives

```text
Q(T) >= log_2 N-h_2(eta)-eta log_2(N^2-1),
```

or zero when that expression is negative. Encoding, decoding, buffering and repeatability remain premises. This is not a throughput claim, a certificate for a future drifted device, or a dimension-independent worst-input diamond bound. [Source, lines 191–227](../package/expander_mixed_bath_companion.txt#L191-L227).

## Constant source, almost uncompressed mixed output

The streaming example imports the stated depth-1 expander construction with 16 local generators and uniform gap `gamma>=1/(2*10^8)`. After the lift it uses 36 probes and conservative `kappa>=10^-9`. This is a poor constant for experimental economics; a better finite-size observed gap cannot silently replace the proved uniform bound.

The time-programmed source has a 36-level label, one biased flag and a constant buffer. Incoming collision qubits are **maximally mixed**, and their purifiers are unavailable. A bounded sliding window and held boundary sites implement the finite-range controlled layer. A loose source-dimension bound is `36*2^16`, independent of n. Gate count and duration are `O(n)` at fixed strength, with an `O(n)` program and an external clock or programmed horizon.

Its full output channel is

```text
B_n(rho) = sum_(j,b) rho_(j,b),(j,b) tau_(j,b),
N = 2^(n+1).
```

Thus it is entanglement breaking with fixed input dimension 36. Nevertheless preserving its complete output experiment to full diamond error epsilon through one reconstruction channel requires

```text
dim(M_n) >= 2^(n+1)[1-2epsilon/(a kappa)].
```

For `epsilon<=a kappa/4`, at least n retained quantum bits are necessary, even with unlimited classical side memory. Ordinary direct storage of all n+1 output qubits matches the bound to an additive constant.

This is a **known finite time-programmed mixed collision source**, not an immutable stationary thermal Lindblad source or a fixed microscopic optical port. It neither establishes useful noise tolerance at that tiny gap nor contradicts pure-port collection. Mixed incoming bins and unavailable purifiers change the premises; zero quantum capacity does not imply that the entire blind output experiment can be kept in small quantum memory. [Source, lines 229–259](../package/expander_mixed_bath_companion.txt#L229-L259).

## Ordinary comparisons and review boundary

The original compares quantitative finite-error blind compression with Koashi–Imoto; expander tests with Aharonov et al.; process-fidelity tests with Hofmann and Reich–Gualdi–Koch; and the obstruction with direct storage. Gross–Eisert and the depth-1 expander are imported constructions. Expander rigidity, efficient channel certification and capacity coding are not claimed as new inventions.

The contribution supplied by this note is the explicit mixed-probe conversion, quantitative memory/fidelity witness and bounded-source mixed-stream composition under their exact contracts. No separate audit of these companion claims is supplied by the parent's main-theorem audit. No historical priority, constant-noise fault-tolerant implementation, raw-data calibration, stationary thermal no-go or working-device advantage is established. [Comparators, lines 261–279](../package/expander_mixed_bath_companion.txt#L261-L279); [sources and final boundaries, lines 281–319](../package/expander_mixed_bath_companion.txt#L281-L319).

[Main package and audit boundaries](../README.md) · [Independent causal reset/export result](causal-reset-decoder.md) · [Other supplied results](../../README.md)
