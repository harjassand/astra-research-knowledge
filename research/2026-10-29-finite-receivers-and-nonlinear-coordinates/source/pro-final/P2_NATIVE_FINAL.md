I followed the finite-information route through to a **reviewed causal receiver compiler and an exact memory-fault interface**. The central result now connects three things: which information must remain coherent, how to transfer it into finite qubits, and how faults in those qubits change the intended operation.

## 1. A constructive principle for what must remain quantum

For the finite projective interaction families considered here, let \(B_t\) describe the accumulated commutation relations at arrival cut \(t\). The exact coherent-memory requirement is

\[
D_t=2^{\operatorname{rank}_{\mathbb F_2}(B_t)/2}.
\]

The noncommuting matrix factor remains quantum; commuting information can become a record; the remaining multiplicity can be retired. The theorem includes arbitrary initial source–field–reference correlations and preserves the actual receiver record.

I then removed the assumed ideal subsystem extractor from the binary construction. The new compiler uses finite phase estimation, controlled access to the **actual** source-relative unitaries, finite qubit operations and readout. It constructs one compatible receiver across the entire arrival schedule, including increases and decreases in retained memory.

The executable emits the controlled words, their execution order, normalization phases, retained Pauli frames, record-dependent feedback and a rational error/resource ledger. Its worked schedule retains **\(1,2,1,0\) qubits** across successive boundaries. These are symbolic controlled-query circuits; their physical coupling and capture interface remains explicit.

Proof and executable: :chatgpt-content-reference{index="3"}[FINITE_PROJECTIVE_COMPILER.md](producer-workspace/FINITE_PROJECTIVE_COMPILER.md) · :chatgpt-content-reference{index="4"}[compile_receiver.py](producer-workspace/compile_receiver.py)

### The construction survives imperfect anticommutation

For actual unitaries satisfying \(\|UV+VU\|\leq\eta\), the receiver controls the disturbance caused by estimating \(U^2\) and then \(V^2\). It never replaces the actual Weyl operators by supposedly nearby rational ones.

For the two-arrival example, with both defects at most \(10^{-5}\):

| Receiver resource across the cut | Complete-operation statement |
|---|---:|
| One retained qubit, explicit finite circuit | Sufficient error \(<0.10438\) |
| Classical memory only, arbitrary allowed receiver processing | Necessary error \(>0.124999\) |

Both statements use the same arbitrary-input, complete-record, source-phase-feedback contract. This establishes a conditional resource separation. The quantum upper bound is neither an attained optimum nor a device error rate.

The binary implementation uses **1,020 controlled field queries and 30 recorded bits**. The generic compiler is considerably more conservative: its four-arrival example requests a \(1/100\) comparison allowance and emits 1,048,560 queries. That is a construction cost, not a physical lower bound. The specialized circuit—or a conventional oscillator receiver—should be used when it serves the operation better.

:chatgpt-content-reference{index="5"}[NEAR_ANTICOMMUTING_EXTRACTOR.md](producer-workspace/NEAR_ANTICOMMUTING_EXTRACTOR.md)

## 2. The same algebra determines how memory faults reach the computation

I continued past the compression result to construct its noise interface.

For a retained-memory Pauli fault \(Q\), define its source error character by

\[
QP_i=(-1)^{\chi_t(Q)_i}P_iQ.
\]

For the minimal retained register,

\[
\operatorname{Im}\chi_t=\operatorname{Im}B_t.
\]

Thus **the same matrix determines both coherent memory requirements and possible source phase-error patterns**. This has an immediate architectural consequence: a small receiver register does not imply local source noise. One exact example maps a single retained-qubit \(Y\) fault to a six-source-qubit \(Z\) pattern.

For an acquired, state-independent classical Pauli fault process—with arbitrary time correlations—the accumulated character is

\[
\chi(f)=\bigoplus_t\chi_t(Q_t).
\]

For the prescribed correction protocol, the actual complete-instrument error is exactly

\[
\boxed{\epsilon_{\mathrm{complete}}
=1-\Pr[\chi(f)=0].}
\]

Every actual record remains included. The comparison uses the same noisy receiver on the common input. Correlated faults can cancel; counting every occurrence as an operation failure can substantially overestimate the error.

With finite compiler allowance \(\epsilon_c\), the actual error lies within \(\epsilon_c\) of that value, clipped to \([0,1]\). Physical implementation discrepancies remain separate.

This provides a concrete interface to conventional quantum-memory protection: a logical-memory instrument that supplies the required Pauli/syndrome law gives a calculable source-operation error. Its encoding, syndrome acquisition, controls and residual-noise assumptions still have to be supplied.

:chatgpt-content-reference{index="6"}[MEMORY_FAULT_INTERFACE.md](producer-workspace/MEMORY_FAULT_INTERFACE.md)

## 3. A coherent fault exposes what the Pauli approximation misses

The challenge work produced an exact counterexample to replacing coherent memory noise by a classical Pauli mixture.

For the prescribed fault \(E=(4I-3iZ)/5\) in the Bell receiver:

| Output interface or substituted model | Exact universal error |
|---|---:|
| Source output only | \(3/5\) |
| Source plus complete actual record | \(24/25\) |
| Falsely substituted classical Pauli mixture | \(9/25\) |

The first two norms allow arbitrary joint source/environment inputs and references. The source-only result does not assume one environment-independent source channel.

The larger error has a particularly clear witness: **the source remains unchanged**, while the actual and common-input receivers interchange record probabilities \(1/50\) and \(49/50\). The record alone attains distance \(24/25\). Matching analytic upper bounds establish both universal values.

This is the missing information in the failed approximation: coherent cross terms alter the actual record law. Marginal twirling or a Pauli expansion does not establish the process-level classical fault law required above; the primary randomized-compiling comparison retains related memory and control qualifications. :chatgpt-content-reference{index="0"}

:chatgpt-content-reference{index="7"}[Complete-record extension](producer-workspace/COHERENT_RECORD_EXTENSION.md) · :chatgpt-content-reference{index="8"}[COHERENT_SOURCE_METRIC.md](producer-workspace/COHERENT_SOURCE_METRIC.md)

## What this makes possible

The completed instrument can now take a declared interaction schedule, identify the finite coherence that needs protection, emit a receiver construction, and propagate a compatible memory-noise law into an actual operation metric. It gives a basis for comparing architectures and error-correction interfaces without treating oscillator dimension, covariance error or memory infidelity as interchangeable quantities.

The conventional ingredients remain credited: efficient sine-state preparation and oscillator Pauli constructions already exist. The constructed bridge is their finite-record causal-operation contract and its noise interface. :chatgpt-content-reference{index="1"} A retained oscillator and the stronger known-vacuum recovery remain serious alternatives. No hardware or workload advantage is claimed before coupling, capture, energy, timing, loss, calibration and reuse are accounted for.

All core claims above passed separate independent internal reviews. The executable review caught an omitted normalization-phase instruction; it was corrected, and the failed interface was preserved. Exact algebra/channel checks, floating diagnostics and analytic guarantees remain distinguished.

The complete package is in :chatgpt-content-reference{index="9"}[README.md](producer-workspace/README.md), with :chatgpt-content-reference{index="10"}[REPRODUCE.md](producer-workspace/REPRODUCE.md) and the :chatgpt-content-reference{index="11"}[integrity manifest](producer-workspace/MANIFEST.json). Final verification checked 94 review pins and confirmed all 181 manifested predecessor files unchanged. No computation remains running.