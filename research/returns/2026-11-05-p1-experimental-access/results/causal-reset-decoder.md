# Structured output-only recovery through causal reset/export

This is an independent result from P1's experimental-access package. **Read the [complete governing derivation](../package/causal_reset_decoder.txt).** It is a completed direct mathematical construction for the source class below. The main access theorem's `proof_audit.txt` is not a blanket audit of this companion; no separate companion-specific audit artifact is supplied. This page extracts the operation and its costs without re-proving or executing it.

## Operation and exact access contract

The input is an arbitrary state of n fixed-dimensional q-level source sites, including entanglement across sites and with an inaccessible reference. The source follows a known finite circuit with gates of arity at most k. Local depolarizing noise has the actual channel

```text
D_p(rho) = (1-p) rho + p Tr(rho) I/q.
```

Its **actual calibrated pure Stinespring environment** is delivered coherently and without loss. The receiver has exported qudits and observed flags and never touches the surviving source. A reduced noise channel alone does not supply these quantum records. Unspecified inaccessible Z noise is outside the exact-recovery contract.

The receiver applies a finite environment-only Kraus isometry, constructed from the calibrated Kraus operators. It gives

```text
V|psi> = sqrt(1-p)|psi>_S|empty>
       + sqrt(p)|Phi_q>_SA |psi>_B.

I_0(rho_SR) = (1-p) rho_SR
I_1(rho_SR) = p (I/q)_S tensor rho_BR.
```

Only the empty versus reset/export subspace is measured; the auxiliary A is discarded. The old unknown state and all its reference correlations are **exported**, not measured. Reset flags are independent of the payload. This earns an input-independent reset/export instrument rather than assuming that forgetting automatically supplies a decoder. [Source, lines 12–36](../package/causal_reset_decoder.txt#L12-L36).

## A stopping certificate that acquires the decoder

Track **wire segments**, not a count of which physical sites have reset:

1. All original payload wires start active.
2. Record a gate if any input is active; mark all its output wires active.
3. Ignore gates whose inputs are all inactive.
4. On an active reset, store the old wire and begin a fresh inactive source wire.
5. Stop when no source wire is active.

The gate schedule and observed payload-independent flags provide this classical stopping certificate. If G gates were recorded, the receiver applies their inverses in reverse chronological order, then discards restored boundary-ancilla wires. It exactly recovers the input and its arbitrary external-reference correlations, using

```text
M <= n + (k-1)G   stored qudits.
```

The proof permits the boundary ancillas to be mixed and entangled with inaccessible systems. Inactive operations prepare a payload-independent state `omega_AF`; at extinction the active subcircuit has all its outputs in receiver memory. Undoing that subcircuit restores `rho_XR` without accessing F.

“Every physical site has reset once” is insufficient: resetting a site, coupling its fresh wire to a still-active site, and then resetting the latter can make the first site active again. [Theorem, proof and counterexample, lines 38–59](../package/causal_reset_decoder.txt#L38-L59).

## Finite discrete-time costs

Each round consists of disjoint known unitary gates of arity at most k, followed by independent reset/export events. Set `alpha=k(1-p)`. The active count obeys

```text
E[a_t] <= n alpha^t
Pr(active set remains at t) <= n alpha^t.
```

If `p>1-1/k`, so `alpha<1`, then

```text
T = ceil(log(n/delta)/[-log(alpha)])
```

gives success at least `1-delta`. This is a sufficient branching bound, not a sharp quantum threshold.

| Resource | Bound and qualification |
|---|---|
| Noise-port uses | `nT` |
| Full flag processing and bookkeeping | `O(nT)` for bounded k |
| Worst-case stored qudits and inverse gates | `O(nT)` |
| Expected inverse gates | `E[G] <= n/(1-alpha)` |
| Expected stored qudits | `E[M] <= n+(k-1)n/(1-alpha) = kp n/(1-alpha)` |

At fixed distance from the sufficient threshold, retained memory and inverse work are linear in expectation, while the total interface work remains `O(n log(n/delta))`. This avoids synthesis of an exponentially dense matrix on dimension `q^n` **for this structured class**.

The ideal successful map is `s id`, with payload-independent `s>=1-delta`. Replacing failure by an arbitrary output gives **full diamond error** at most `2delta`. Continuing to collect the same input until extinction is legitimate here because its information remains coherently available; this is not a restart of an already destroyed unknown state.

For L implemented receiver operations with full diamond error at most nu each, the complete instrument error is at most `L nu`. For an unconditional target epsilon, the source chooses `2delta<=epsilon/2` and `nu<=epsilon/(2L)`. Gate synthesis precision, memory waiting errors, classical latency and error correction remain paid resources. [Source, lines 61–82](../package/causal_reset_decoder.txt#L61-L82).

## Precisely delimited continuous-time corollary

An ideal Markov subclass allows local depolarization at rate r, known k-local **unitary jumps** with rates `gamma_X`, and arbitrary one-site Hamiltonians. All modeled ports are actual calibrated coherent outputs. Adding a source-independent identity coherent port and mixing the Weyl ports realizes the reset/export jump representation with a state-independent Poisson replacement clock. The unitary jump labels and times are observed.

Let `g=max_i sum_{X containing i} gamma_X` and `kappa=r-(k-1)g`. If `kappa>0`,

```text
Pr(tau>t) <= n exp(-kappa t)
E[tau] <= (log(n)+1)/kappa
E[G] <= gn/kappa
E[M] <= rn/kappa.
```

This remains an **ideal port model**. A finite-bandwidth detector and coherent capture of the internal quantum marks require a separate physical construction.

**Arbitrary interacting continuous Hamiltonians are not covered.** Naive Trotterization reactivates every output of each infinitesimal entangling gate, so this Boolean branching argument diverges as the step shrinks. The source explicitly leaves a norm-sensitive extension open. [Source, lines 84–101](../package/causal_reset_decoder.txt#L84-L101).

## Comparators and relation to earlier results

- Parallel source SWAP is simpler if that additional source access is granted. With the same reset/export ports and no interactions, collecting original wires already has logarithmic stopping time.
- N1732 covers a much more general known finite-dimensional pure-port Markov source and preserves the full canonical Stinespring channel approximately, but its dense compilation scales in `d=q^n`. This companion earns polynomial n-cost by using a local reset/export structure and an efficiently recorded active circuit; it does not compress every residual source/environment correlation.
- The accessible noncommuting environment records differ from the main access theorem's inaccessible-noise model. Hidden Z dephasing cannot be silently relabeled as an accessible port, and additional such noise can invalidate exact recovery.
- Kraus-isometry equivalence and percolation machinery have prior work, credited in the original. Historical priority, a general continuous-Hamiltonian extension and a working-device advantage are not established. [Source, lines 103–120](../package/causal_reset_decoder.txt#L103-L120).

[Main package and audit boundaries](../README.md) · [Independent mixed-output memory result](expander-mixed-output-memory.md) · [Other supplied results](../../README.md)
